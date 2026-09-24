"""SQLite store for experiment runs.

The database keeps each run as one validated JSON document. SQLite owns
atomic writes, identity, and ordering.

Usage:
    from expense_agent.tracking import RunStore

    store = RunStore()
    store.save(run)
    store.load(run.run_id)
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from pydantic_ai import BinaryContent

from expense_agent.tracking.run import Run

DEFAULT_RUNS_DB = Path("data/runs.sqlite3")


class RunStore:
    """Read and write runs in one SQLite database."""

    def __init__(self, path: Path = DEFAULT_RUNS_DB) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    data TEXT NOT NULL
                )
                """
            )

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path)
        try:
            with connection:
                yield connection
        finally:
            # SQLite's transaction context does not close the connection.
            connection.close()

    def exists(self, run_id: str) -> bool:
        """Check an ID before starting paid model requests."""
        with self._connect() as connection:
            return (
                connection.execute("SELECT 1 FROM runs WHERE run_id = ?", (run_id,)).fetchone()
                is not None
            )

    def save(self, run: Run) -> None:
        """Save one run without persisting binary message data."""
        stored_run = run.model_copy(deep=True)
        _strip_binary_data(stored_run)
        try:
            with self._connect() as connection:
                connection.execute(
                    "INSERT INTO runs (run_id, created_at, data) VALUES (?, ?, ?)",
                    (run.run_id, run.created_at.isoformat(), stored_run.model_dump_json()),
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"run already exists: {run.run_id}") from exc

    def load(self, run_id: str) -> Run:
        """Read one run by ID. Raise `KeyError` when it does not exist."""
        with self._connect() as connection:
            row = connection.execute("SELECT data FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        if row is None:
            raise KeyError(f"run not found: {run_id}")
        return Run.model_validate_json(row[0])

    def list_runs(self) -> list[Run]:
        """Load all runs, sorted oldest first."""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT data FROM runs ORDER BY created_at, run_id"
            ).fetchall()
        return [Run.model_validate_json(row[0]) for row in rows]


def _strip_binary_data(value: Any, seen: set[int] | None = None) -> None:
    """Empty `BinaryContent.data` without changing the in-memory run."""
    if seen is None:
        seen = set()

    identity = id(value)
    if identity in seen:
        return
    seen.add(identity)

    if isinstance(value, BinaryContent):
        identifier = value.identifier
        _strip_binary_data(value.vendor_metadata, seen)
        value.data = b""
        value._identifier = identifier
    elif isinstance(value, BaseModel):
        for name in type(value).model_fields:
            _strip_binary_data(getattr(value, name), seen)
    elif is_dataclass(value) and not isinstance(value, type):
        for field in fields(value):
            _strip_binary_data(getattr(value, field.name), seen)
    elif isinstance(value, Mapping):
        for item in value.values():
            _strip_binary_data(item, seen)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for item in value:
            _strip_binary_data(item, seen)
