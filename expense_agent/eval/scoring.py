"""Deterministic evaluation: compare an agent decision to the ground truth.

Takes an expected and an actual `CaseDecision` (the agent's structured
output uses the same shape) and returns a `CaseEval` with the numeric
delta, so aggregate stats can be computed across cases.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from expense_agent.label import CaseDecision


class LineItemDelta(BaseModel):
    """Reimbursement delta for one receipt line, matched by line id.

    Missing expected items appear with `actual_reimbursed=0`; extra
    actual items appear with `expected_reimbursed=0`. `description` is
    the ground-truth wording, falling back to the agent's for an item
    the ground truth does not have.
    """

    model_config = ConfigDict(extra="forbid")

    id: int
    description: str
    expected_reimbursed: Decimal
    actual_reimbursed: Decimal
    delta: Decimal  # actual - expected; positive = we pay too much


class CaseEval(BaseModel):
    """Numeric diff between expected and actual for one case.

    `decision_match and reimbursed_error == 0` is a full pass.
    """

    model_config = ConfigDict(extra="forbid")

    case_id: str
    decision_match: bool
    reimbursed_error: Decimal  # |actual - expected| on the total
    overpaid: Decimal  # extra payout vs. ground truth, 0 if under
    underpaid: Decimal  # missing payout vs. ground truth, 0 if over
    line_item_deltas: list[LineItemDelta]  # only items that differ


def evaluate(expected: CaseDecision, actual: CaseDecision) -> CaseEval:
    """Grade one agent decision against its ground-truth label."""
    expected_items = {item.id: item for item in expected.line_items}
    actual_items = {item.id: item for item in actual.line_items}

    deltas: list[LineItemDelta] = []
    for line_id, expected_item in expected_items.items():
        actual_item = actual_items.get(line_id)
        actual_reimbursed = actual_item.reimbursed if actual_item else Decimal("0")
        if actual_reimbursed != expected_item.reimbursed:
            deltas.append(LineItemDelta(
                id=line_id,
                description=expected_item.description,
                expected_reimbursed=expected_item.reimbursed,
                actual_reimbursed=actual_reimbursed,
                delta=actual_reimbursed - expected_item.reimbursed,
            ))
    for line_id, actual_item in actual_items.items():
        if line_id not in expected_items:
            deltas.append(LineItemDelta(
                id=line_id,
                description=actual_item.description,
                expected_reimbursed=Decimal("0"),
                actual_reimbursed=actual_item.reimbursed,
                delta=actual_item.reimbursed,
            ))

    reimbursed_error = abs(expected.reimbursed_amount - actual.reimbursed_amount)
    return CaseEval(
        case_id=expected.case_id,
        decision_match=expected.decision == actual.decision,
        reimbursed_error=reimbursed_error,
        overpaid=max(Decimal("0"), actual.reimbursed_amount - expected.reimbursed_amount),
        underpaid=max(Decimal("0"), expected.reimbursed_amount - actual.reimbursed_amount),
        line_item_deltas=deltas,
    )
