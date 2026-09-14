"""Web UI for browsing tracked experiment runs.

Serves a two-view interface: a table of all runs with their headline
metrics, and a run detail view with per-case results, the receipt image,
and the agent trajectory rendered by pydantic-ai-trace.

Per-case token cost and token counts are stored with the run. Metrics
the store does not keep (overpaid and underpaid dollars) are derived
here from the stored messages and labels; costs for runs saved before
cost tracking are derived from the stored messages.

Usage:
    pixi run viewer   # http://127.0.0.1:8000
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic_ai.messages import ModelResponse
from pydantic_ai_trace import TraceView

from expense_agent.eval import evaluate
from expense_agent.harness.cases import DEFAULT_DATA_DIR, RECEIPT_FILENAME
from expense_agent.tracking import CaseSuccess, Run, RunCase, RunStore
from expense_agent.tracking.cost import messages_cost, messages_tokens

INDEX_HTML = Path(__file__).parent / "index.html"
ZERO = Decimal("0")

app = FastAPI(title="Expense agent runs")
store = RunStore()


def _case_cost(case: RunCase) -> Decimal:
    """Stored token cost; derived from messages for pre-tracking runs."""
    if case.cost is not None:
        return case.cost
    return messages_cost(case.agent_messages)


def _case_tokens(case: RunCase) -> int:
    """Stored input plus output tokens; derived for pre-tracking runs."""
    if case.tokens is not None:
        return case.tokens
    return messages_tokens(case.agent_messages)


def _case_row(case: RunCase) -> dict[str, Any]:
    """One row for the case list: outcome, amounts, and cost."""
    row: dict[str, Any] = {
        "case_id": case.case_id,
        "failed": not isinstance(case, CaseSuccess),
        "cost": float(_case_cost(case)),
        "tokens": _case_tokens(case),
        "expected_decision": case.expected.decision,
        "expected_amount": float(case.expected.reimbursed_amount),
    }
    if isinstance(case, CaseSuccess):
        result = evaluate(case.expected, case.actual)
        row |= {
            "correct": result.decision_match and result.reimbursed_error == ZERO,
            "decision_match": result.decision_match,
            "actual_decision": case.actual.decision,
            "actual_amount": float(case.actual.reimbursed_amount),
            "overpaid": float(result.overpaid),
            "underpaid": float(result.underpaid),
        }
    else:
        row |= {"correct": False, "decision_match": False, "error": case.error}
    return row


def _run_summary(run: Run) -> dict[str, Any]:
    """Headline metrics for one run, as shown in the runs table."""
    rows = [_case_row(case) for case in run.cases]
    costs = [row["cost"] for row in rows]
    total_cost = run.metrics.total_cost if run.metrics.total_cost is not None else sum(costs)
    return {
        "run_id": run.run_id,
        "created_at": run.created_at.isoformat(),
        "total_cases": run.metrics.total_cases,
        "failed_cases": run.metrics.failed_cases,
        "pass_rate": run.metrics.pass_rate,
        "decision_accuracy": run.metrics.decision_accuracy,
        "mean_reimbursed_error": float(run.metrics.mean_reimbursed_error or 0),
        "overpaid": sum(row.get("overpaid", 0.0) for row in rows),
        "underpaid": sum(row.get("underpaid", 0.0) for row in rows),
        "mean_cost": sum(costs) / len(costs) if costs else 0.0,
        "total_cost": float(total_cost),
    }


def _load_run(run_id: str) -> Run:
    try:
        return store.load(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"run not found: {run_id}") from None


def _find_case(run: Run, case_id: str) -> RunCase:
    for case in run.cases:
        if case.case_id == case_id:
            return case
    raise HTTPException(status_code=404, detail=f"case not found: {case_id}")


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """The single-page user interface."""
    return INDEX_HTML.read_text(encoding="utf-8")


@app.get("/api/runs")
def list_runs() -> list[dict[str, Any]]:
    """All runs with headline metrics, newest first."""
    return [_run_summary(run) for run in reversed(store.list_runs())]


@app.get("/api/runs/{run_id}")
def get_run(run_id: str) -> dict[str, Any]:
    """One run: headline metrics plus one row per case."""
    run = _load_run(run_id)
    return _run_summary(run) | {"cases": [_case_row(case) for case in run.cases]}


@app.get("/api/runs/{run_id}/cases/{case_id}")
def get_case(run_id: str, case_id: str) -> dict[str, Any]:
    """One case: the expected and actual decision plus their diff."""
    case = _find_case(_load_run(run_id), case_id)
    detail = _case_row(case) | {"expected": case.expected.model_dump(mode="json")}
    if isinstance(case, CaseSuccess):
        result = evaluate(case.expected, case.actual)
        detail |= {
            "actual": case.actual.model_dump(mode="json"),
            "reimbursed_error": float(result.reimbursed_error),
            "line_item_deltas": [delta.model_dump(mode="json") for delta in result.line_item_deltas],
        }
    return detail


@app.get("/api/runs/{run_id}/cases/{case_id}/trace", response_class=HTMLResponse)
def get_trace(run_id: str, case_id: str) -> str:
    """The case trajectory as a self-contained pydantic-ai-trace document."""
    case = _find_case(_load_run(run_id), case_id)
    return TraceView.from_messages(case.agent_messages, title=case_id).html()


@app.get("/api/cases/{case_id}/receipt")
def get_receipt(case_id: str) -> FileResponse:
    """The receipt image straight from the case directory on disk."""
    path = DEFAULT_DATA_DIR / case_id / RECEIPT_FILENAME
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"receipt not found: {path}")
    # Receipts are regenerated in place; without this, browsers heuristically
    # cache the unchanged URL and keep showing the previous image.
    return FileResponse(path, headers={"Cache-Control": "no-cache"})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
