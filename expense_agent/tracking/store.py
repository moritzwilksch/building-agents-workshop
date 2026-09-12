"""Minimal JSON file store for experiment runs.

One JSON document per run, named by `run_id`, under a root directory.
There is no index: the filename is the run identity.

Usage:
    from expense_agent.tracking import RunStore

    store = RunStore()
    store.save(run)
    store.load(run.run_id)
"""

from __future__ import annotations

from pathlib import Path

from expense_agent.tracking.run import Run

DEFAULT_RUNS_DIR = Path("data/runs")


class RunStore:
    """Read and write `Run` documents as JSON files under `root`."""

    def __init__(self, root: Path = DEFAULT_RUNS_DIR) -> None:
        self.root = root

    def _path(self, run_id: str) -> Path:
        return self.root / f"{run_id}.json"

    def save(self, run: Run) -> Path:
        """Write one run to `<root>/<run_id>.json` and return the path."""
        self.root.mkdir(parents=True, exist_ok=True)
        path = self._path(run.run_id)
        path.write_text(run.model_dump_json(indent=2))
        return path

    def load(self, run_id: str) -> Run:
        """Read one run by id. Raises FileNotFoundError when absent."""
        return Run.model_validate_json(self._path(run_id).read_text())

    def list_runs(self) -> list[Run]:
        """Load all runs, sorted oldest first. Empty when the root is absent."""
        if not self.root.exists():
            return []
        runs = [Run.model_validate_json(path.read_text()) for path in self.root.glob("*.json")]
        return sorted(runs, key=lambda run: run.created_at)
