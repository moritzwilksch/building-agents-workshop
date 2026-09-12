"""Data model for expense case ground-truth labels and agent decisions.

The agent's structured output uses the same shape as the ground-truth
label, so `evaluate` can compare them directly.

Usage:
    from expense_agent.label import CaseLabel

    label = CaseLabel.model_validate_json(path.read_text())
"""

from __future__ import annotations

from decimal import Decimal
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

Decision = Literal["approved", "partially_approved", "rejected"]


class LineItem(BaseModel):
    """One receipt line: what was charged and what we reimburse."""

    # Reject unknown fields so typos in JSON fail loudly.
    model_config = ConfigDict(extra="forbid")

    description: str = Field(min_length=1)
    claimed: Decimal = Field(ge=0)
    reimbursed: Decimal = Field(ge=0)


class CaseLabel(BaseModel):
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
    def check_amounts(self) -> Self:
        if self.reimbursed_amount > self.claimed_amount:
            raise ValueError("reimbursed_amount must not exceed claimed_amount")

        if self.decision == "approved":
            if self.reimbursed_amount != self.claimed_amount:
                raise ValueError("approved requires reimbursed_amount == claimed_amount")
        elif self.decision == "rejected":
            if self.reimbursed_amount != 0:
                raise ValueError("rejected requires reimbursed_amount == 0")
        else:  # partially_approved
            if not 0 < self.reimbursed_amount < self.claimed_amount:
                raise ValueError("partially_approved requires 0 < reimbursed_amount < claimed_amount")

        claimed = sum(item.claimed for item in self.line_items)
        if claimed != self.claimed_amount:
            raise ValueError(f"line items claim {claimed}, not claimed_amount={self.claimed_amount}")

        reimbursed = sum(item.reimbursed for item in self.line_items)
        if reimbursed != self.reimbursed_amount:
            raise ValueError(f"line items reimburse {reimbursed}, not reimbursed_amount={self.reimbursed_amount}")

        return self
