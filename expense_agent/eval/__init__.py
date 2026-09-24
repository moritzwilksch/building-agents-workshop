"""Evaluation harness: scoring, ground-truth loading, and reporting.

Instructor-provided boilerplate. Participants do not edit this
subpackage; it grades the `expense_agent` code they write.
"""

from expense_agent.eval.scoring import CaseEval, LineItemDelta, evaluate

__all__ = [
    "CaseEval",
    "LineItemDelta",
    "evaluate",
]
