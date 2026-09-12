"""Data model for experiment runs: metrics plus one trajectory per case.

A run is one agent execution over a set of expense cases. It carries
top-level `RunMetrics` and a `RunCase` trajectory per case. Each
trajectory stores the expected decision, the actual decision, and the
native pydantic-ai messages, so it can be replayed without translation.

Usage:
    from expense_agent.tracking import Run, RunCase

    run = Run.from_cases([RunCase(case_id="case-0001", expected=label, actual=decision, agent_messages=messages)])
    run.model_dump_json()
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field
from pydantic_ai.messages import ModelMessage

from expense_agent.eval import CaseEval, evaluate
from expense_agent.label import CaseDecision

ZERO = Decimal("0")


class RunMetrics(BaseModel):
    """Aggregate eval statistics for one run.

    `pass_rate` counts full passes: decision match and zero amount error.
    """

    model_config = ConfigDict(extra="forbid")

    total_cases: int = Field(ge=0)
    pass_rate: float = Field(ge=0, le=1)
    decision_accuracy: float = Field(ge=0, le=1)
    mean_reimbursed_error: Decimal = Field(ge=0)

    @classmethod
    def from_evals(cls, evals: list[CaseEval]) -> RunMetrics:
        """Aggregate per-case evals into run-level metrics."""
        total = len(evals)
        if total == 0:
            return cls(total_cases=0, pass_rate=0.0, decision_accuracy=0.0, mean_reimbursed_error=ZERO)

        passes = sum(1 for e in evals if e.decision_match and e.reimbursed_error == ZERO)
        decisions = sum(1 for e in evals if e.decision_match)
        error = sum((e.reimbursed_error for e in evals), ZERO) / total
        return cls(
            total_cases=total,
            pass_rate=passes / total,
            decision_accuracy=decisions / total,
            mean_reimbursed_error=error,
        )


class RunCase(BaseModel):
    """Trajectory and grade for one expense case."""

    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(min_length=1)
    expected: CaseDecision
    actual: CaseDecision
    agent_messages: list[ModelMessage] = Field(default_factory=list)

    def evaluate(self) -> CaseEval:
        """Grade the actual decision against the expected decision."""
        return evaluate(self.expected, self.actual)


class Run(BaseModel):
    """One agent execution over a set of cases."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(default_factory=lambda: uuid4().hex, min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metrics: RunMetrics
    cases: list[RunCase]

    @classmethod
    def from_cases(cls, cases: list[RunCase], run_id: str | None = None) -> Run:
        """Build a run and derive its metrics from the case trajectories."""
        metrics = RunMetrics.from_evals([case.evaluate() for case in cases])
        return cls(run_id=run_id or uuid4().hex, metrics=metrics, cases=cases)
