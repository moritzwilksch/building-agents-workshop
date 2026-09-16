"""Retrieval gate: the stage-2 ranker must surface governing text.

For each canonical query, asserts that
1. one top hit window contains all of the query's decisive governing
   fragments (from chapters 1 to 14), and
2. no hit from the generated distractor chapters (15 to 22) outranks that
   hit unless it carries its own disqualifier ("Superseded", "Draft",
   "...governs"). Filler from chapters 21 to 22 must never appear at all.

    pixi run python .data-generation/check_retrieval.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from expense_agent.stage2.search import (  # noqa: E402
    DEFAULT_RESULTS,
    HandbookSearch,
    _is_toc_page,
    extract_pages,
)

PDF = Path(__file__).parent.parent / "data" / "handbook.pdf"

# (query, fragments that must all appear in one hit window)
CASES = [
    ("breakfast cap", ["breakfast", "15.00"]),
    ("lunch cap", ["lunch", "25.00"]),
    ("dinner cap", ["dinner", "45.00"]),
    ("daily aggregate meals", ["aggregate", "85.00"]),
    ("overtime meal home office late work", ["overtime", "20.00"]),
    ("dinner cap receipt time", ["dinner", "45.00"]),
    ("nightly room cap Berlin", ["berlin", "160.00"]),
    ("nightly room cap Munich", ["munich", "160.00"]),
    ("nightly room cap Amsterdam", ["amsterdam", "160.00"]),
    ("hotel room rate cap tier", ["nightly room"]),
    ("hotel laundry seven nights cap", ["laundry", "35.00"]),
    ("garment rescue soiling note", ["garment rescue", "25.00"]),
    ("hotel parking EV charging rental", ["parking", "30.00"]),
    ("city tax folio", ["city tax"]),
    ("minibar deduction folio", ["minibar", "deduct"]),
    ("hotel incidental allowance", ["incidental"]),
    ("tip cap Germany restaurant", ["germany", "20%"]),
    ("gratuity cap vendor country", ["gratuity standards"]),
    ("tip United Kingdom service charge", ["united kingdom", "12.5%"]),
    ("taxi fare threshold justification", ["threshold", "fare"]),
    ("first class rail four hours", ["first class", "four"]),
    ("seat reservation reimbursement", ["seat reservation"]),
    ("mileage rate personal vehicle", ["0.38"]),
    ("checked bag fee reimbursement", ["bag fee"]),
    ("flight change fee business", ["change fee"]),
    ("weekend approval flowchart", ["weekend", "flowchart"]),
    ("international flight pre-approval", ["pre-approval"]),
    ("truffle policy flowchart", ["truffle policy flowchart"]),
    ("client entertainment per person cap", ["per-person", "cap"]),
    ("team meal per person cap", ["per-person", "cap"]),
    ("event surcharge trade fair override", ["event surcharge cap"]),
    ("Medica Expo event window", ["medica", "200.00"]),
    ("FinTech Summit event cap", ["fintech summit", "200.00"]),
    ("peripheral IT ticket threshold", ["peripheral", "threshold"]),
    ("event materials budget owner", ["event materials", "budget owner"]),
    ("VAT registration number folio", ["vat registration number"]),
    ("currency conversion receipt", ["ecb"]),
    ("submission deadline thirty days", ["thirty", "calendar days"]),
    ("dynamic currency conversion markup", ["dynamic currency conversion"]),
    ("staging greenery event approval", ["staging greenery"]),
]

SELF_LABELS = ("superseded", "draft", "governs", "never payable", "not effective", "not adopted", "withdrawn", "binds", "governing")


def chapter_start_pages(pages: list[str]) -> dict[str, int]:
    starts: dict[str, int] = {}
    for number, page in enumerate(pages, 1):
        if _is_toc_page(page):
            continue
        for line in page.splitlines():
            for chapter in ("15 Extended", "21 Governance", "22 Settlement"):
                if line.strip().startswith(chapter):
                    starts.setdefault(chapter, number)
    missing = [name for name in ("15 Extended", "21 Governance", "22 Settlement") if name not in starts]
    if missing:
        raise SystemExit(f"chapter starts not found: {missing}")
    return starts


def main() -> None:
    search = HandbookSearch.from_pdf(PDF)
    starts = chapter_start_pages(extract_pages(PDF))
    first_distractor = starts["15 Extended"]
    filler_start = starts["22 Settlement"]

    failures = []
    for query, fragments in CASES:
        hits = search.search(query, k=DEFAULT_RESULTS)
        decisive_rank = None
        for rank, hit in enumerate(hits, 1):
            if hit.page >= first_distractor:
                continue
            text = hit.text.lower()
            if all(fragment.lower() in text for fragment in fragments):
                decisive_rank = rank
                break
        if decisive_rank is None:
            failures.append(f"{query!r}: fragments {fragments} not together in any top {DEFAULT_RESULTS} hit")
            continue
        for rank, hit in enumerate(hits, 1):
            if rank >= decisive_rank or hit.page < first_distractor:
                continue
            text = hit.text.lower()
            if hit.page >= filler_start:
                failures.append(f"{query!r}: filler (ch22, page {hit.page}) at rank {rank} outranks decisive text")
            elif not any(label in text for label in SELF_LABELS):
                failures.append(f"{query!r}: unlabelled distractor (page {hit.page}) at rank {rank}: {hit.text[:80]!r}")
    if failures:
        print(f"RETRIEVAL GATE FAILED ({len(failures)} problems)")
        for failure in failures:
            print("  " + failure)
        raise SystemExit(1)
    print(f"retrieval gate passed: {len(CASES)} queries, decisive text retrievable, distractors self-labelled")


if __name__ == "__main__":
    main()
