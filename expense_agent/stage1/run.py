"""Run the Stage 1 agent over cases and persist the graded run.

Extracts the handbook once, builds the agent, runs the requested cases
through `AgentRunner`, and saves the resulting `Run` with `RunStore`.

Usage:
    python -m expense_agent.stage1.run
    python -m expense_agent.stage1.run --cases case-0001 case-0002 case-0003 --run-id stage1-smoke
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from dotenv import load_dotenv

from expense_agent.harness import AgentRunner, CaseLoader
from expense_agent.stage1.agent import DEFAULT_MODEL, build_agent, extract_handbook_text, handbook_prompt
from expense_agent.tracking import RunStore

DEFAULT_CASES = ["case-0001", "case-0002", "case-0003"]


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", nargs="+", default=DEFAULT_CASES, help="case ids to run")
    parser.add_argument("--run-id", default=None, help="run id; defaults to a random hex id")
    parser.add_argument("--data-dir", type=Path, default=Path("data"), help="case data directory")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="pydantic-ai model id")
    args = parser.parse_args()

    loader = CaseLoader(args.data_dir)
    handbook = handbook_prompt(extract_handbook_text(args.data_dir / "handbook.pdf"))
    agent = build_agent(args.model)
    store = RunStore()
    runner = AgentRunner(agent, store, loader, prompt=handbook)

    run = asyncio.run(runner.run(case_ids=args.cases, run_id=args.run_id))

    print(f"run {run.run_id} -> {store.path}")
    print(
        f"pass_rate={_format_rate(run.metrics.pass_rate)} "
        f"decision_accuracy={_format_rate(run.metrics.decision_accuracy)} "
        f"mean_reimbursed_error={run.metrics.mean_reimbursed_error}"
    )
    for case in run.cases:
        if case.kind == "success":
            print(f"  {case.case_id}: expected={case.expected.decision} actual={case.actual.decision} "
                  f"reimbursed {case.actual.reimbursed_amount} (expected {case.expected.reimbursed_amount})")
        else:
            print(f"  {case.case_id}: FAILED {case.error}")


def _format_rate(rate: float | None) -> str:
    return f"{rate:.2f}" if rate is not None else "n/a"


if __name__ == "__main__":
    main()
