"""Invoice schema shared by the data generator and the case harness.

The canonical models live in the importable package so the generation
scripts and the harness share one definition.

Usage:
    from expense_agent.invoice import ChargeLine
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field


class ChargeLine(BaseModel):
    """One numbered charge as it appears on the receipt, top to bottom.

    Every invoice type carries its charges in different fields (items, room
    charges, fares, taxes, tips). `charge_lines` flattens them into this one
    numbered list so `invoice.json` and `label.json` share the same ids and a
    label entry always refers to exactly one receipt line.
    """

    id: int = Field(ge=0)
    description: str = Field(min_length=1)
    amount: Decimal = Field(ge=0)
