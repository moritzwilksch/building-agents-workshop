"""Pydantic models for expense case ground-truth labels.

The canonical models live in the importable package so the eval suite
and the labeling scripts share one definition. This module only
re-exports them for the `.data-generation` scripts.

Usage:
    from label_schema import CaseLabel

    label = CaseLabel.model_validate_json(path.read_text())
"""

from expense_agent.label import CaseLabel, Decision, LineItem

__all__ = ["CaseLabel", "Decision", "LineItem"]
