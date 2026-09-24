"""Data model for expense case ground-truth labels and agent decisions.

The agent's structured output uses the same shape as the ground-truth
label, so `evaluate` can compare them directly.

Usage:
    from expense_agent.label import CaseDecision

    decision = CaseDecision.model_validate_json(path.read_text())
"""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

Decision = Literal["approved", "partially_approved", "rejected"]
ReimbursedAmount = Annotated[Decimal, Field(ge=0)]


class AgentOutput(BaseModel):
    """The policy judgments the agent must make.

    Reimbursements correspond to the invoice charges in order. The harness
    fills in identifiers, claimed amounts, totals, and the overall decision.
    """

    model_config = ConfigDict(extra="forbid")

    reimbursements: list[ReimbursedAmount] = Field(min_length=1)
    reasoning: str = Field(min_length=1)


class LineItem(BaseModel):
    """One receipt line: what was charged and what we reimburse.

    `id` is the line's position on the receipt, numbered from 0 top to
    bottom with the tip last. Evaluation matches items by `id`, so the
    agent's free-form `description` never has to match ours verbatim.
    """

    # Reject unknown fields so typos in JSON fail loudly.
    model_config = ConfigDict(extra="forbid")

    id: int = Field(ge=0)
    description: str = Field(min_length=1)
    claimed: Decimal = Field(ge=0)
    reimbursed: Decimal = Field(ge=0)


class CaseDecision(BaseModel):
    """One expense case: decision, amounts, line-item breakdown.

    Enforces the decision rules from LABELING.md and that line items
    sum to the top-level amounts.
    """

    # Reject unknown fields so typos in JSON fail loudly.
    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(min_length=1)
    decision: Decision
    claimed_amount: Decimal = Field(ge=0)
    reimbursed_amount: Decimal = Field(ge=0)
    line_items: list[LineItem] = Field(min_length=1)
    reasoning: str = Field(min_length=1)

    @model_validator(mode="after")
    def check_line_item_ids(self) -> Self:
        ids = [item.id for item in self.line_items]
        if ids != list(range(len(ids))):
            raise ValueError(f"line item ids must be 0..{len(ids) - 1} in receipt order, got {ids}")
        return self

    @model_validator(mode="after")
    def check_amounts(self) -> Self:
        if self.reimbursed_amount > self.claimed_amount:
            raise ValueError("reimbursed_amount must not exceed claimed_amount")

        overpaid_items = [item.id for item in self.line_items if item.reimbursed > item.claimed]
        if overpaid_items:
            raise ValueError(
                f"reimbursement exceeds claimed amount for line items {overpaid_items}"
            )

        if self.decision == "approved":
            if self.reimbursed_amount != self.claimed_amount:
                raise ValueError("approved requires reimbursed_amount == claimed_amount")
        elif self.decision == "rejected":
            if self.reimbursed_amount != 0:
                raise ValueError("rejected requires reimbursed_amount == 0")
        else:  # partially_approved
            if not 0 < self.reimbursed_amount < self.claimed_amount:
                raise ValueError(
                    "partially_approved requires 0 < reimbursed_amount < claimed_amount"
                )

        claimed = sum(item.claimed for item in self.line_items)
        if claimed != self.claimed_amount:
            raise ValueError(
                f"line items claim {claimed}, not claimed_amount={self.claimed_amount}"
            )

        reimbursed = sum(item.reimbursed for item in self.line_items)
        if reimbursed != self.reimbursed_amount:
            raise ValueError(
                f"line items reimburse {reimbursed}, not reimbursed_amount={self.reimbursed_amount}"
            )

        return self
