"""Retrieval gate for the inflated handbook.

The main-content distractor prose must be lexically isolated from the terms the
stage-2 search agents use. This gate replays the canonical queries through the
real BM25 backend and asserts three things:

1. the governing text for every query is reachable within the top hits;
2. no query's decisive hit regresses by more than `RANK_TOLERANCE` versus the
   recorded baseline (pages shift as the handbook grows, ranks should not);
3. no competing page outranks the decisive page while carrying the governing
   numbers without the rest of the governing fragments.

Run:

    pixi run python .data-generation/check_retrieval.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from expense_agent.stage2.tools import RESULTS, HandbookSearch, Page  # noqa: E402

PDF = Path(__file__).parent.parent / "data" / "handbook.pdf"

RANK_TOLERANCE = 2

# (query, governing fragments that must co-occur in one page, baseline rank)
CASES: list[tuple[str, list[str], int]] = [
    ("breakfast cap", ["breakfast", "15.00"], 2),
    ("lunch cap", ["lunch", "25.00"], 4),
    ("dinner cap", ["dinner", "45.00"], 2),
    ("daily aggregate meals", ["aggregate", "85.00"], 1),
    ("overtime meal home office late work", ["overtime", "20.00"], 1),
    ("nightly room cap Berlin", ["berlin", "160.00"], 1),
    ("nightly room cap Munich", ["munich", "160.00"], 1),
    ("nightly room cap Amsterdam", ["amsterdam", "160.00"], 1),
    ("hotel room rate cap tier", ["nightly room"], 1),
    ("hotel laundry seven nights cap", ["laundry", "35.00"], 1),
    ("garment rescue soiling note", ["garment rescue", "25.00"], 1),
    ("hotel parking EV charging rental", ["parking", "30.00"], 1),
    ("city tax folio", ["city tax"], 1),
    ("minibar deduction folio", ["minibar", "deduct"], 1),
    ("tip cap Germany restaurant", ["germany", "20%"], 1),
    ("gratuity cap vendor country", ["gratuity standards"], 1),
    ("tip United Kingdom service charge", ["united kingdom", "12.5%"], 1),
    ("taxi fare threshold justification", ["threshold", "fare"], 1),
    ("first class rail four hours", ["first class", "four"], 1),
    ("seat reservation reimbursement", ["seat reservation"], 2),
    ("mileage rate personal vehicle", ["0.38"], 1),
    ("checked bag fee reimbursement", ["bag fee"], 1),
    ("flight change fee business", ["change fee"], 1),
    ("weekend approval flowchart", ["weekend", "flowchart"], 1),
    ("international flight pre-approval", ["pre-approval"], 1),
    ("truffle policy flowchart", ["truffle policy flowchart"], 1),
    ("client entertainment per person cap", ["per-person", "cap"], 1),
    ("team meal per person cap", ["per-person", "cap"], 1),
    ("event surcharge trade fair override", ["event surcharge cap"], 1),
    ("Medica Expo event window", ["medica", "200.00"], 1),
    ("FinTech Summit event cap", ["fintech summit", "200.00"], 1),
    ("peripheral IT ticket threshold", ["peripheral", "threshold"], 2),
    ("event materials budget owner", ["event materials", "budget owner"], 1),
    ("VAT registration number folio", ["vat registration number"], 1),
    ("currency conversion receipt", ["ecb"], 1),
    ("submission deadline thirty days", ["thirty", "calendar days"], 1),
    ("dynamic currency conversion markup", ["dynamic currency conversion"], 1),
    ("staging greenery event approval", ["staging greenery"], 1),
]

NUMBER = re.compile(r"\d")


def decisive_rank(hits: list[Page], fragments: list[str]) -> int | None:
    """Return the rank of the first page carrying every governing fragment."""
    for rank, page in enumerate(hits, start=1):
        text = page.text.lower()
        if all(fragment.lower() in text for fragment in fragments):
            return rank
    return None


def main() -> None:
    search = HandbookSearch(PDF)
    failures: list[str] = []
    ranks: list[int] = []

    for query, fragments, baseline in CASES:
        hits = search.search_pages(query)
        rank = decisive_rank(hits, fragments)
        if rank is None:
            failures.append(f"{query!r}: governing fragments {fragments} not in top {RESULTS}")
            continue
        ranks.append(rank)
        if rank > baseline + RANK_TOLERANCE:
            failures.append(f"{query!r}: decisive rank {rank} vs baseline {baseline}")

        numeric = [fragment for fragment in fragments if NUMBER.search(fragment)]
        for above_rank, page in enumerate(hits[: rank - 1], start=1):
            text = page.text.lower()
            if any(fragment.lower() in text for fragment in numeric):
                failures.append(
                    f"{query!r}: competing numeric page at rank {above_rank} "
                    f"(page {page.number}) contains {numeric}"
                )

    if failures:
        print(f"RETRIEVAL GATE FAILED ({len(failures)} problems)")
        for failure in failures:
            print("  " + failure)
        raise SystemExit(1)

    mean_rank = sum(ranks) / len(ranks)
    print(
        f"retrieval gate passed: {len(CASES)} queries, "
        f"decisive ranks within baseline+{RANK_TOLERANCE}, mean rank {mean_rank:.2f}"
    )


if __name__ == "__main__":
    main()
