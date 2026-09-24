"""Load expense cases from disk into a runner-provided input bundle.

`CaseInput` is the read-only bundle handed to the agent as pydantic-ai
deps. It deliberately excludes the ground-truth label, so an agent cannot
read the answer. `CaseLoader` owns the file paths and the parsing.

Usage:
    from expense_agent.harness import CaseLoader

    loader = CaseLoader()
    case_input = loader.load_input("case-0001")
    expected = loader.load_expected("case-0001")
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

from expense_agent.invoice import ChargeLine
from expense_agent.label import CaseDecision

DEFAULT_DATA_DIR = Path("data")

RECEIPT_FILENAME = "receipt.jpg"
INVOICE_FILENAME = "invoice.json"
LABEL_FILENAME = "label.json"
HANDBOOK_FILENAME = "handbook.pdf"


class CaseInput(BaseModel):
    """Case bundle passed to the agent as deps. Excludes the label.

    `note` is what the employee wrote when submitting the claim. It carries
    the business purpose and attendee count that several policy rules turn
    on, so it belongs in the agent's context beside the receipt. `charges`
    are the invoice positions, in order, that the decision must cover.
    """

    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(min_length=1)
    receipt_image: Path
    handbook_pdf: Path
    note: str | None = None
    charges: list[ChargeLine] = Field(min_length=1)

    @model_validator(mode="after")
    def check_charge_ids(self) -> CaseInput:
        ids = [charge.id for charge in self.charges]
        if ids != list(range(len(ids))):
            raise ValueError(f"charge ids must be 0..{len(ids) - 1} in receipt order, got {ids}")
        return self


class CaseLoader:
    """Locate and parse cases under a data directory."""

    def __init__(self, data_dir: Path = DEFAULT_DATA_DIR) -> None:
        self.data_dir = data_dir

    def _case_dir(self, case_id: str) -> Path:
        return self.data_dir / case_id

    def _required(self, path: Path) -> Path:
        if not path.is_file():
            raise FileNotFoundError(path)
        return path

    def case_ids(self) -> list[str]:
        """Return sorted case directory names, e.g. `case-0001`."""
        if not self.data_dir.is_dir():
            raise FileNotFoundError(f"case data directory not found: {self.data_dir.resolve()}")
        case_ids = sorted(path.name for path in self.data_dir.glob("case-*") if path.is_dir())
        if not case_ids:
            raise ValueError(f"no cases found in {self.data_dir.resolve()}")
        return case_ids

    def load_input(self, case_id: str) -> CaseInput:
        """Read one case into its agent-facing input bundle."""
        case_dir = self._case_dir(case_id)
        invoice_path = self._required(case_dir / INVOICE_FILENAME)
        invoice = json.loads(invoice_path.read_text(encoding="utf-8"))
        charges = [ChargeLine.model_validate(charge) for charge in invoice["charges"]]
        return CaseInput(
            case_id=case_id,
            receipt_image=self._required(case_dir / RECEIPT_FILENAME),
            handbook_pdf=self._required(self.data_dir / HANDBOOK_FILENAME),
            note=invoice.get("note"),
            charges=charges,
        )

    def load_expected(self, case_id: str) -> CaseDecision:
        """Read the ground-truth label for one case."""
        path = self._required(self._case_dir(case_id) / LABEL_FILENAME)
        return CaseDecision.model_validate_json(path.read_text(encoding="utf-8"))
