"""Stage 2: structured output plus a handbook search tool.

The agent no longer receives the full handbook. It calls `search_handbook`
to retrieve the passages a case turns on, then returns the same structured
`CaseDecision` as Stage 1.

Participant-facing reference implementation. Not a solution to later
stages: text search cannot reach the rules that live only in diagrams,
because those pages extract to placeholder text.
"""

from expense_agent.stage2.agent import build_agent
from expense_agent.stage2.bm25 import HandbookBM25
from expense_agent.stage2.prompts import SYSTEM_PROMPT
from expense_agent.stage2.search import (
    Hit,
    HandbookSearch,
    Line,
    SearchBackend,
    build_lines,
    extract_pages,
)

__all__ = [
    "SYSTEM_PROMPT",
    "Hit",
    "HandbookBM25",
    "HandbookSearch",
    "Line",
    "SearchBackend",
    "build_agent",
    "build_lines",
    "extract_pages",
]
