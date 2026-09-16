"""Grep-style keyword search over the handbook's extracted text.

The handbook is kept as page-tagged lines. A query matches a line when the
line contains one of the query's terms, so there is no index to build and
the ranker stays trivial. Each hit returns the matching line plus a few
lines on either side as context.

Usage:
    from expense_agent.stage2.search import HandbookSearch

    search = HandbookSearch.from_pdf(Path("data/handbook.pdf"))
    print(search.format(search.search("nightly room cap Amsterdam")))
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from pypdf import PdfReader

TOKEN_RE = re.compile(r"[a-z0-9]+")

CONTEXT_LINES = 2
DEFAULT_RESULTS = 10


@dataclass(frozen=True)
class Line:
    """One line of handbook text and the page it came from."""

    page: int
    text: str


@dataclass(frozen=True)
class Hit:
    """A matching line together with its surrounding context lines."""

    page: int
    text: str


class SearchBackend(Protocol):
    """A handbook retrieval backend the Stage 2 agent can call."""

    def search(self, query: str, k: int = DEFAULT_RESULTS) -> list[Hit]:
        """Return up to `k` hits for a query, best first."""

    def format(self, hits: list[Hit]) -> str:
        """Render hits as text for the model."""


def window(lines: list[Line], index: int) -> Hit:
    """Build a hit from the line at `index` plus its surrounding context."""
    start = max(0, index - CONTEXT_LINES)
    stop = min(len(lines), index + CONTEXT_LINES + 1)
    context = lines[start:stop]
    return Hit(page=lines[index].page, text="\n".join(line.text for line in context))


def format_hits(hits: list[Hit]) -> str:
    """Render hits as compact blocks, each tagged with its page number."""
    if not hits:
        return "No policy text matched that query. Try different keywords."
    return "\n\n".join(f"[{rank}] page {hit.page}\n{hit.text}" for rank, hit in enumerate(hits, start=1))


def extract_pages(pdf_path: Path) -> list[str]:
    """Extract handbook text page by page. Images yield no text."""
    reader = PdfReader(pdf_path)
    return [page.extract_text() or "" for page in reader.pages]


def tokenize(text: str) -> list[str]:
    """Lowercase a string into alphanumeric search terms."""
    return TOKEN_RE.findall(text.lower())


def _is_toc_page(text: str) -> bool:
    """Detect a table-of-contents page from its dot-leader rows."""
    return text.count(". . .") >= 3


def build_lines(pages: list[str]) -> list[Line]:
    """Turn extracted pages into page-tagged non-empty lines.

    Table-of-contents pages are skipped so their dot-leader rows do not
    crowd out the real policy matches. Page numbers are preserved.
    """
    lines: list[Line] = []
    for page_number, text in enumerate(pages, start=1):
        if _is_toc_page(text):
            continue
        for raw in text.splitlines():
            stripped = raw.strip()
            if stripped:
                lines.append(Line(page=page_number, text=stripped))
    return lines


class HandbookSearch:
    """Find lines that contain the query's terms and return them with context."""

    def __init__(self, pages: list[str]) -> None:
        self.lines = build_lines(pages)

    @classmethod
    def from_pdf(cls, pdf_path: Path) -> "HandbookSearch":
        """Read a handbook PDF into a searchable line list."""
        return cls(extract_pages(pdf_path))

    def search(self, query: str, k: int = DEFAULT_RESULTS) -> list[Hit]:
        """Return up to `k` hits, best first, with overlapping windows merged.

        A line scores by how many distinct query terms appear in it. Lines
        in the context window of an already-selected hit are skipped, so the
        results cover distinct passages instead of repeating one.
        """
        terms = set(tokenize(query))
        if not terms:
            return []
        scored = [
            (self._score(line.text, terms), index)
            for index, line in enumerate(self.lines)
        ]
        scored = [(score, index) for score, index in scored if score > 0]
        scored.sort(key=lambda pair: pair[0], reverse=True)

        hits: list[Hit] = []
        used: list[int] = []
        for _, index in scored:
            if any(abs(index - other) <= CONTEXT_LINES for other in used):
                continue
            hits.append(self._window(index))
            used.append(index)
            if len(hits) == k:
                break
        return hits

    def format(self, hits: list[Hit]) -> str:
        """Render hits as compact blocks, each tagged with its page number."""
        return format_hits(hits)

    @staticmethod
    def _score(text: str, terms: set[str]) -> int:
        lowered = text.lower()
        return sum(1 for term in terms if term in lowered)

    def _window(self, index: int) -> Hit:
        return window(self.lines, index)
