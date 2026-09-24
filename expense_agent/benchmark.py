"""Run one workshop stage against a small, hard, or full benchmark suite."""

from __future__ import annotations

import argparse
import asyncio
import sys
from importlib import import_module
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from expense_agent.harness import AgentRunner, CaseLoader
from expense_agent.harness.runner import MAX_CONCURRENCY
from expense_agent.tracking import Run, RunStore

SMALL_SUITE_SIZE = 5

# Cases the benchmark agents get consistently wrong, picked from the runs in
# `data/runs.sqlite3` by pass rate and reimbursement error.
HARD_CASE_IDS = [
    "case-0002",
    "case-0003",
    "case-0008",
    "case-0026",
    "case-0034",
    "case-0038",
    "case-0043",
    "case-0045",
    "case-0047",
    "case-0049",
]


def available_stages() -> list[int]:
    """List stages present in this checkout without importing their code."""
    return sorted(
        int(path.parent.name.removeprefix("stage"))
        for path in Path(__file__).parent.glob("stage*/agent.py")
        if path.parent.name.removeprefix("stage").isdigit()
    )


def select_cases(loader: CaseLoader, suite: str) -> list[str]:
    """Select the first five cases, the curated hard cases, or every case."""
    case_ids = loader.case_ids()
    if suite == "small":
        if len(case_ids) < SMALL_SUITE_SIZE:
            raise ValueError(f"small suite requires {SMALL_SUITE_SIZE} cases")
        return case_ids[:SMALL_SUITE_SIZE]
    if suite == "hard":
        missing = [case_id for case_id in HARD_CASE_IDS if case_id not in case_ids]
        if missing:
            raise ValueError(f"hard suite cases not found: {', '.join(missing)}")
        return list(HARD_CASE_IDS)
    return case_ids


def print_summary(run: Run, store: RunStore) -> None:
    """Print the run metrics and one line per case."""
    metrics = run.metrics
    pass_rate = f"{metrics.pass_rate:.2f}" if metrics.pass_rate is not None else "n/a"
    accuracy = (
        f"{metrics.decision_accuracy:.2f}" if metrics.decision_accuracy is not None else "n/a"
    )

    print(f"run {run.run_id} -> {store.path}")
    print(
        f"pass_rate={pass_rate} "
        f"decision_accuracy={accuracy} "
        f"mean_reimbursed_error={metrics.mean_reimbursed_error}"
    )
    for case in run.cases:
        if case.kind == "failure":
            print(f"  {case.case_id}: FAILED {case.error}")
        else:
            print(
                f"  {case.case_id}: expected={case.expected.decision} "
                f"actual={case.actual.decision} reimbursed={case.actual.reimbursed_amount} "
                f"expected_reimbursed={case.expected.reimbursed_amount}"
            )


def configure_logging() -> None:
    """Send benchmark progress logs to stdout, beside the printed summary."""
    logger.remove()
    logger.add(sys.stdout)


def main() -> None:
    configure_logging()
    load_dotenv()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=int, choices=available_stages(), required=True)
    parser.add_argument("--suite", choices=["small", "hard", "full"], required=True)
    parser.add_argument("--run-id", help="run id; defaults to a UTC timestamp")
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--concurrency", type=int, default=MAX_CONCURRENCY)
    args = parser.parse_args()

    loader = CaseLoader(args.data_dir)
    module = import_module(f"expense_agent.stage{args.stage}.agent")
    agent = module.build_agent()
    if agent is None:
        parser.error(
            f"stage {args.stage} is a template: implement build_agent() in "
            f"expense_agent/stage{args.stage}/agent.py first"
        )
    store = RunStore()
    runner = AgentRunner(agent, store, loader, concurrency=args.concurrency)
    run = asyncio.run(
        runner.run(
            case_ids=select_cases(loader, args.suite),
            run_id=args.run_id,
        )
    )
    print_summary(run, store)


if __name__ == "__main__":
    main()
