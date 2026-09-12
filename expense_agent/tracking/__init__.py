"""Experiment tracking: minimal run and trajectory storage.

Participant-facing. Runs carry top-level eval metrics and one
trajectory per case, persisted as JSON by `RunStore`.
"""

from expense_agent.tracking.run import CaseFailure, CaseSuccess, Run, RunCase, RunMetrics
from expense_agent.tracking.store import DEFAULT_RUNS_DIR, RunStore

__all__ = [
    "CaseFailure",
    "CaseSuccess",
    "DEFAULT_RUNS_DIR",
    "Run",
    "RunCase",
    "RunMetrics",
    "RunStore",
]
