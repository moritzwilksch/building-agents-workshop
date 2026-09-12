"""Data model for experiment runs: metrics plus one trajectory per case.

A run is one agent execution over a set of expense cases. It carries
top-level `RunMetrics` and one `RunCase` per case. A `RunCase` is either
a `CaseSuccess`, which stores the expected decision, the actual decision,
and the native pydantic-ai messages, or a `CaseFailure`, which stores the
error raised while running the case.

Usage:
    from expense_agent.tracking import CaseSuccess, Run

    run = Run.from_cases([CaseSuccess(case_id="case-0001", expected=label, actual=decision, agent_messages=messages)])
    run.model_dump_json()
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic_ai.messages import ModelMessage

from expense_agent.eval import evaluate
from expense_agent.label import CaseDecision

ZERO = Decimal("0")


def default_run_id() -> str:
    """Timestamp-based run id, e.g. `2026-09-12 16:50:00` (UTC)."""
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")


class CaseSuccess(BaseModel):
    """A graded case trajectory: expected and actual decisions plus messages.

    `cost` and `tokens` are captured when the case runs and persisted with
    the run. They are `None` for runs saved before cost tracking existed;
    derive them from `agent_messages` in that case.
    """

    # No `extra="forbid"` here: it propagates into the nested pydantic-ai
    # `RequestUsage` dataclass and rejects provider-specific usage fields
    # (`input_text_tokens`, `output_reasoning_tokens`), so a saved run could
    # not be loaded again.
    model_config = ConfigDict(extra="ignore")

    kind: Literal["success"] = "success"
    case_id: str = Field(min_length=1)
    expected: CaseDecision
    actual: CaseDecision
    agent_messages: list[ModelMessage] = Field(default_factory=list)
    cost: Decimal | None = None
    tokens: int | None = None


class CaseFailure(BaseModel):
    """A failed case with its error and partial message history.

    `cost` and `tokens` cover the partial trajectory before the failure.
    """

    # See `CaseSuccess`: provider-specific usage fields must survive loading.
    model_config = ConfigDict(extra="ignore")

    kind: Literal["failure"] = "failure"
    case_id: str = Field(min_length=1)
    expected: CaseDecision
    error: str = Field(min_length=1)
    agent_messages: list[ModelMessage] = Field(default_factory=list)
    cost: Decimal | None = None
    tokens: int | None = None


RunCase = Annotated[CaseSuccess | CaseFailure, Field(discriminator="kind")]


class RunMetrics(BaseModel):
    """Aggregate eval statistics for one run.

    Average metrics include successful cases only. They are `None` when
    every case failed.
    """

    model_config = ConfigDict(extra="forbid")

    total_cases: int = Field(ge=0)
    failed_cases: int = Field(ge=0)
    pass_rate: float | None = Field(default=None, ge=0, le=1)
    decision_accuracy: float | None = Field(default=None, ge=0, le=1)
    mean_reimbursed_error: Decimal | None = Field(default=None, ge=0)
    total_cost: Decimal | None = None

    @classmethod
    def from_cases(cls, cases: list[RunCase]) -> RunMetrics:
        """Aggregate per-case results into run-level metrics."""
        successes = [case for case in cases if isinstance(case, CaseSuccess)]
        evals = [evaluate(case.expected, case.actual) for case in successes]
        total = len(cases)
        successful = len(successes)

        passes = sum(1 for e in evals if e.decision_match and e.reimbursed_error == ZERO)
        decisions = sum(1 for e in evals if e.decision_match)
        costs = [case.cost for case in cases if case.cost is not None]
        return cls(
            total_cost=sum(costs, ZERO) if costs else None,
            total_cases=total,
            failed_cases=total - successful,
            pass_rate=passes / successful if successful else None,
            decision_accuracy=decisions / successful if successful else None,
            mean_reimbursed_error=(
                sum((e.reimbursed_error for e in evals), ZERO) / successful if successful else None
            ),
        )


class Run(BaseModel):
    """One agent execution over a set of cases."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(default_factory=default_run_id, min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metrics: RunMetrics
    cases: list[RunCase] = Field(min_length=1)

    @classmethod
    def from_cases(cls, cases: list[RunCase], run_id: str | None = None) -> Run:
        """Build a run and derive its metrics from the case results."""
        if not cases:
            raise ValueError("at least one case is required")
        return cls(run_id=run_id or default_run_id(), metrics=RunMetrics.from_cases(cases), cases=cases)
