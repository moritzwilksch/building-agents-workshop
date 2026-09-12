"""Minimal harness that runs cases through a participant-provided agent.

The runner owns the plumbing: it loads cases, runs them concurrently under
a semaphore, isolates a raising case as a `CaseFailure`, grades the rest,
prices token usage per case, and persists the whole run with `RunStore`. Participants own the agent:
its prompt and tools. The harness grades `CaseDecision` output.

The runner passes `CaseInput` as pydantic-ai deps and sends the receipt
image beside the stage-specific prompt.

Usage:
    import asyncio
    from expense_agent.harness import AgentRunner, CaseLoader
    from expense_agent.tracking import RunStore

    runner = AgentRunner(agent, RunStore(), CaseLoader())
    run = asyncio.run(runner.run(run_id="stage-2"))
"""

from __future__ import annotations

import asyncio
from typing import Any

from pydantic_ai import Agent, BinaryContent, capture_run_messages

from expense_agent.harness.cases import CaseInput, CaseLoader
from expense_agent.label import CaseDecision
from expense_agent.tracking import CaseFailure, CaseSuccess, Run, RunCase, RunStore
from expense_agent.tracking.cost import messages_cost, messages_tokens

MAX_CONCURRENCY = 4
DEFAULT_PROMPT = "Evaluate the expense case and return your decision."

CaseAgent = Agent[CaseInput, Any]


async def run_case(
    agent: CaseAgent,
    case_input: CaseInput,
    expected: CaseDecision,
    prompt: str,
) -> RunCase:
    """Run one case. Any exception becomes a `CaseFailure` for that case."""
    with capture_run_messages() as messages:
        try:
            receipt = BinaryContent.from_path(case_input.receipt_image)
            result = await agent.run(
                [prompt, f"Case ID: {case_input.case_id}\nReceipt:", receipt],
                deps=case_input,
            )
            actual = CaseDecision.model_validate(result.output)
        except Exception as exc:
            return CaseFailure(
                case_id=case_input.case_id,
                expected=expected,
                error=f"{type(exc).__name__}: {exc}",
                agent_messages=messages,
                cost=messages_cost(messages),
                tokens=messages_tokens(messages),
            )
    return CaseSuccess(
        case_id=case_input.case_id,
        expected=expected,
        actual=actual,
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
        prompt: str = DEFAULT_PROMPT,
    ) -> None:
        if concurrency < 1:
            raise ValueError("concurrency must be at least 1")
        self.agent = agent
        self.store = store
        self.loader = loader
        self.concurrency = concurrency
        self.prompt = prompt

    async def run(self, case_ids: list[str] | None = None, run_id: str | None = None) -> Run:
        """Run the requested cases, save the run, and return it.

        `case_ids` defaults to every case the loader finds. Results keep
        the input order. A missing case file raises rather than becoming a
        case failure, because the label is needed to represent a failure.
        """
        ids = self.loader.case_ids() if case_ids is None else case_ids
        if not ids:
            raise ValueError("at least one case is required")
        semaphore = asyncio.Semaphore(self.concurrency)

        async def bounded(case_id: str) -> RunCase:
            async with semaphore:
                case_input = self.loader.load_input(case_id)
                expected = self.loader.load_expected(case_id)
                return await run_case(self.agent, case_input, expected, self.prompt)

        cases = list(await asyncio.gather(*(bounded(case_id) for case_id in ids)))
        run = Run.from_cases(cases, run_id=run_id)
        self.store.save(run)
        return run
