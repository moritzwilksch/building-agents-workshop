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
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from expense_agent.label import CaseDecision

DEFAULT_DATA_DIR = Path("data")

RECEIPT_FILENAME = "receipt.jpg"
INVOICE_FILENAME = "invoice.json"
LABEL_FILENAME = "label.json"
HANDBOOK_FILENAME = "handbook.pdf"


class CaseInput(BaseModel):
    """Case bundle passed to the agent as deps. Excludes the label."""

    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(min_length=1)
    invoice: dict[str, Any]
    receipt_image: Path
    handbook_pdf: Path


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
        if not self.data_dir.exists():
            return []
        return sorted(path.name for path in self.data_dir.glob("case-*") if path.is_dir())

    def load_input(self, case_id: str) -> CaseInput:
        """Read one case into its agent-facing input bundle."""
        case_dir = self._case_dir(case_id)
        invoice = json.loads(self._required(case_dir / INVOICE_FILENAME).read_text(encoding="utf-8"))
        return CaseInput(
            case_id=case_id,
            invoice=invoice,
            receipt_image=self._required(case_dir / RECEIPT_FILENAME),
            handbook_pdf=self._required(self.data_dir / HANDBOOK_FILENAME),
        )

    def load_expected(self, case_id: str) -> CaseDecision:
        """Read the ground-truth label for one case."""
        path = self._required(self._case_dir(case_id) / LABEL_FILENAME)
        return CaseDecision.model_validate_json(path.read_text(encoding="utf-8"))
