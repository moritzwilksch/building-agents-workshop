"""Deterministic evaluation: compare an agent decision to the ground truth.

Takes an expected and an actual `CaseLabel` (the agent's structured
output uses the same shape) and returns a `CaseEval` with the full
delta, not just a pass/fail flag.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from expense_agent.label import CaseLabel, Decision


class LineItemEval(BaseModel):
    """Delta for one expected receipt line, matched by description."""

    model_config = ConfigDict(extra="forbid")

    description: str
    matched: bool
    expected_reimbursed: Decimal
    actual_reimbursed: Decimal | None = None
    delta: Decimal | None = None  # actual - expected; positive = overpaid


class CaseEval(BaseModel):
    """Rich comparison of expected vs. actual for one case."""

    model_config = ConfigDict(extra="forbid")

    case_id: str
    passed: bool
    decision_match: bool
    expected_decision: Decision
    actual_decision: Decision | None = None
    expected_reimbursed: Decimal
    actual_reimbursed: Decimal
    reimbursed_error: Decimal  # absolute difference on the total
    overpaid: Decimal  # how much extra we would pay; 0 if none
    line_items: list[LineItemEval]
    extra_items: list[str]  # actual items with no expected match
    problems: list[str]  # human-readable list of every mismatch


def evaluate(expected: CaseLabel, actual: CaseLabel) -> CaseEval:
    """Grade one agent decision against its ground-truth label."""
    problems: list[str] = []

    decision_match = expected.decision == actual.decision
    if not decision_match:
        problems.append(f"decision: expected {expected.decision!r}, got {actual.decision!r}")

    reimbursed_error = abs(expected.reimbursed_amount - actual.reimbursed_amount)
    overpaid = max(Decimal("0"), actual.reimbursed_amount - expected.reimbursed_amount)
    if reimbursed_error > 0:
        problems.append(
            f"reimbursed_amount: expected {expected.reimbursed_amount}, got {actual.reimbursed_amount} (off by {reimbursed_error})"
        )

    actual_items = {item.description: item for item in actual.line_items}
    line_items: list[LineItemEval] = []
    for item in expected.line_items:
        actual_item = actual_items.get(item.description)
        if actual_item is None:
            line_items.append(LineItemEval(
                description=item.description,
                matched=False,
                expected_reimbursed=item.reimbursed,
            ))
            problems.append(f"line item missing: {item.description!r} (expected {item.reimbursed})")
            continue
        delta = actual_item.reimbursed - item.reimbursed
        line_items.append(LineItemEval(
            description=item.description,
            matched=True,
            expected_reimbursed=item.reimbursed,
            actual_reimbursed=actual_item.reimbursed,
            delta=delta,
        ))
        if delta != 0:
            problems.append(f"line item {item.description!r}: expected {item.reimbursed}, got {actual_item.reimbursed} (delta {delta:+})")

    extra = [item.description for item in actual.line_items if item.description not in
             {e.description for e in expected.line_items}]
    for description in extra:
        problems.append(f"line item not in ground truth: {description!r}")

    return CaseEval(
        case_id=expected.case_id,
        passed=decision_match and reimbursed_error == 0,
        decision_match=decision_match,
        expected_decision=expected.decision,
        actual_decision=actual.decision,
        expected_reimbursed=expected.reimbursed_amount,
        actual_reimbursed=actual.reimbursed_amount,
        reimbursed_error=reimbursed_error,
        overpaid=overpaid,
        line_items=line_items,
        extra_items=extra,
        problems=problems,
    )
