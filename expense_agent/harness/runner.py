"""Minimal harness that runs cases through a participant-provided agent.

The runner owns the plumbing: it loads cases, runs them concurrently under
a semaphore, isolates a raising case as a `CaseFailure`, completes and grades
the rest, prices token usage per case, and persists the whole run with `RunStore`.
Participants own the agent: its prompt and tools. The harness turns its
`AgentOutput` into a complete `CaseDecision`.

The runner passes `CaseInput` as pydantic-ai deps and sends the receipt
image, the employee's submission note, and the invoice charges beside the
stage-specific prompt.

Usage:
    import asyncio
    from expense_agent.harness import AgentRunner, CaseLoader
    from expense_agent.tracking import RunStore

    runner = AgentRunner(agent, RunStore(), CaseLoader())
    run = asyncio.run(runner.run(run_id="stage-2"))
"""

from __future__ import annotations

import asyncio
from uuid import uuid4

from loguru import logger
from pydantic import TypeAdapter
from pydantic_ai import Agent, BinaryContent, ModelRetry, RunContext, capture_run_messages

from expense_agent.eval import evaluate
from expense_agent.harness.cases import CaseInput, CaseLoader
from expense_agent.invoice import ChargeLine
from expense_agent.label import AgentOutput, CaseDecision, LineItem
from expense_agent.tracking import CaseFailure, CaseSuccess, Run, RunCase, RunStore
from expense_agent.tracking.cost import messages_cost, messages_tokens

MAX_CONCURRENCY = 8
CHARGE_LIST = TypeAdapter(list[ChargeLine])

# One retry per run: enough for the model to correct an ungradeable output, and
# a second rejection still fails the case so the benchmark records it.
OUTPUT_RETRIES = 1

# Two retries per tool: a bad tool argument is usually a fixable formatting slip
# (for example an arithmetic expression sent where a decimal is required).
TOOL_RETRIES = 2

REIMBURSEMENT_RULE = (
    "Return one reimbursement per invoice charge, in the order the charges are listed, "
    "and never more than that charge's claimed amount."
)

CaseAgent = Agent[CaseInput, AgentOutput]


def describe_outcome(case: RunCase) -> str:
    """One-line result for a finished case, for benchmark progress logs."""
    if isinstance(case, CaseFailure):
        return f"FAILED {case.error}"
    status = "pass" if evaluate(case.expected, case.actual).passed else "mismatch"
    return (
        f"{status} expected={case.expected.decision} actual={case.actual.decision} "
        f"reimbursed={case.actual.reimbursed_amount}"
    )


def user_message(case_input: CaseInput) -> str:
    """Assemble the user message from the case facts and invoice charges."""
    charges = CHARGE_LIST.dump_json(case_input.charges, indent=2).decode("utf-8")
    return (
        f"Employee note: {case_input.note or '(none)'}\n"
        f"Invoice charges (id, description, amount):\n{charges}\n"
        "Receipt:"
    )


def reimbursement_problem(case_input: CaseInput, output: AgentOutput) -> str | None:
    """Why these reimbursements cannot be graded, or `None` when they can."""
    if len(output.reimbursements) != len(case_input.charges):
        return (
            f"expected {len(case_input.charges)} reimbursements, got {len(output.reimbursements)}"
        )
    for charge, reimbursed in zip(case_input.charges, output.reimbursements, strict=True):
        if reimbursed > charge.amount:
            return (
                f"reimbursement for charge {charge.id} exceeds its claimed amount: "
                f"{reimbursed} > {charge.amount}"
            )
    return None


def validate_reimbursements(ctx: RunContext[CaseInput], output: AgentOutput) -> AgentOutput:
    """Reject an output the harness cannot grade and ask the model to correct it.

    Raising `ModelRetry` sends the reason back to the model as a retry prompt,
    so the agent can redo its line items within the run's output retry budget.
    """
    problem = reimbursement_problem(ctx.deps, output)
    if problem is not None:
        raise ModelRetry(f"{problem}. {REIMBURSEMENT_RULE}")
    return output


def complete_decision(case_input: CaseInput, output: AgentOutput) -> CaseDecision:
    """Combine the agent's policy judgments with deterministic case data."""
    problem = reimbursement_problem(case_input, output)
    if problem is not None:
        raise ValueError(problem)

    line_items = []
    for charge, reimbursed in zip(case_input.charges, output.reimbursements, strict=True):
        line_items.append(
            LineItem(
                id=charge.id,
                description=charge.description,
                claimed=charge.amount,
                reimbursed=reimbursed,
            )
        )

    claimed_amount = sum(charge.amount for charge in case_input.charges)
    reimbursed_amount = sum(output.reimbursements)
    if reimbursed_amount == claimed_amount:
        decision = "approved"
    elif reimbursed_amount == 0:
        decision = "rejected"
    else:
        decision = "partially_approved"

    return CaseDecision(
        case_id=case_input.case_id,
        decision=decision,
        claimed_amount=claimed_amount,
        reimbursed_amount=reimbursed_amount,
        line_items=line_items,
        reasoning=output.reasoning,
    )


async def run_case(
    agent: CaseAgent,
    case_input: CaseInput,
    expected: CaseDecision,
) -> RunCase:
    """Run one case. Any exception becomes a `CaseFailure` for that case."""
    with capture_run_messages() as messages:
        try:
            receipt = BinaryContent.from_path(case_input.receipt_image)
            result = await agent.run(
                [user_message(case_input), receipt],
                deps=case_input,
                # Isolate this case from OpenAI's cross-request prompt cache while
                # keeping the model-visible prompt deterministic.
                model_settings={"openai_prompt_cache_key": f"{case_input.case_id}-{uuid4().hex}"},
            )
            output = AgentOutput.model_validate(result.output)
            actual = complete_decision(case_input, output)
        except Exception as exc:
            return CaseFailure(
                case_id=case_input.case_id,
                expected=expected,
                error=f"{type(exc).__name__}: {exc}",
                note=case_input.note,
                agent_messages=messages,
                cost=messages_cost(messages),
                tokens=messages_tokens(messages),
            )
    return CaseSuccess(
        case_id=case_input.case_id,
        expected=expected,
        actual=actual,
        note=case_input.note,
        agent_messages=result.all_messages(),
        cost=messages_cost(result.all_messages()),
        tokens=messages_tokens(result.all_messages()),
    )


class AgentRunner:
    """Run cases concurrently through one agent and save the resulting run."""

    def __init__(
        self,
        agent: CaseAgent,
        store: RunStore,
        loader: CaseLoader,
        concurrency: int = MAX_CONCURRENCY,
    ) -> None:
        if concurrency < 1:
            raise ValueError("concurrency must be at least 1")
        self.agent = agent
        self.store = store
        self.loader = loader
        self.concurrency = concurrency

    async def run(self, case_ids: list[str] | None = None, run_id: str | None = None) -> Run:
        """Run the requested cases, save the run, and return it.

        `case_ids` defaults to every case the loader finds. Results keep
        the input order. A missing case file raises rather than becoming a
        case failure, because the label is needed to represent a failure.
        """
        if run_id is not None and self.store.exists(run_id):
            raise ValueError(f"run already exists: {run_id}; choose a new --run-id")
        ids = self.loader.case_ids() if case_ids is None else case_ids
        if not ids:
            raise ValueError("at least one case is required")
        semaphore = asyncio.Semaphore(self.concurrency)

        async def bounded(case_id: str) -> RunCase:
            async with semaphore:
                case_input = self.loader.load_input(case_id)
                expected = self.loader.load_expected(case_id)
                case = await run_case(self.agent, case_input, expected)
                logger.info(f"{case.case_id}: {describe_outcome(case)}")
                return case

        cases = list(await asyncio.gather(*(bounded(case_id) for case_id in ids)))
        run = Run.from_cases(cases, run_id=run_id)
        self.store.save(run)
        return run
