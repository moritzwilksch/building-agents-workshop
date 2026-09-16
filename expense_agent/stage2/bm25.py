"""BM25 search over the handbook's extracted text.

A second Stage 2 retrieval backend, alongside the grep-style
`HandbookSearch`. `bm25s` indexes each page-tagged line and ranks lines by
Okapi BM25 relevance, so a query retrieves passages by term importance
instead of raw substring counts. Hits reuse the grep backend's context
window and page tags.

Usage:
    from expense_agent.stage2.bm25 import HandbookBM25

    search = HandbookBM25.from_pdf(Path("data/handbook.pdf"))
    print(search.format(search.search("nightly room cap Berlin")))
"""

from __future__ import annotations

from pathlib import Path

import bm25s

from expense_agent.stage2.search import (
    CONTEXT_LINES,
    DEFAULT_RESULTS,
    Hit,
    build_lines,
    extract_pages,
    format_hits,
    window,
)


class HandbookBM25:
    """Rank handbook lines with BM25 and return them with context."""

    def __init__(self, pages: list[str]) -> None:
        self.lines = build_lines(pages)
        self._retriever: bm25s.BM25 | None = None
        if self.lines:
            corpus = [line.text for line in self.lines]
            tokenized = bm25s.tokenize(corpus, show_progress=False)
            self._retriever = bm25s.BM25()
            self._retriever.index(tokenized, show_progress=False)

    @classmethod
    def from_pdf(cls, pdf_path: Path) -> "HandbookBM25":
        """Read a handbook PDF into a BM25 index over its lines."""
        return cls(extract_pages(pdf_path))

    def search(self, query: str, k: int = DEFAULT_RESULTS) -> list[Hit]:
        """Return up to `k` scored hits, best first, windows merged.

        BM25 scores every line, so the full ranking is available before we
        drop lines that fall inside an already-selected hit's window.
        """
        if self._retriever is None:
            return []
        tokens = bm25s.tokenize([query], show_progress=False)
        if not tokens or not tokens[0]:
            return []
        indices, scores = self._retriever.retrieve(tokens, k=len(self.lines), show_progress=False)

        hits: list[Hit] = []
        used: list[int] = []
        for index, score in zip(indices[0], scores[0]):
            if score <= 0:
                continue
            if any(abs(int(index) - other) <= CONTEXT_LINES for other in used):
                continue
            hits.append(window(self.lines, int(index)))
            used.append(int(index))
            if len(hits) == k:
                break
        return hits

    def format(self, hits: list[Hit]) -> str:
        """Render hits as compact blocks, each tagged with its page number."""
        return format_hits(hits)
