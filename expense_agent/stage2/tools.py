"""BM25 handbook page retrieval and precise tax arithmetic for Stage 2.

Search returns short previews. The model reads a page in full by passing its
page number to `read_handbook_page`, which also shows a few lines from the
previous and next page so a rule that spans a page boundary stays visible.

`HandbookSearch` holds the index, so `build_agent()` constructs it once and
hands the model its bound methods as tools. Reading the PDF and building the
index takes a few seconds, so doing it per tool call would stall a run.
"""

import re
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import bm25s
from pypdf import PdfReader

RESULTS = 5
PREVIEW_CHARS = 400
CONTEXT_LINES = 5
TOC_LEADERS = ". . ."
CENT = Decimal("0.01")


def calculate_tax(net_amounts: list[Decimal], rate_percent: Decimal) -> Decimal:
    """Calculate tax on eligible net amounts, rounded half-up to cents.

    Pass each net amount as a single plain decimal number, already computed
    — for example `19.6`, not `"19.6*45/148.59"`. The tool only multiplies
    the sum of `net_amounts` by `rate_percent`; it cannot evaluate arithmetic
    or unit conversions. Work those out first and pass the resulting numbers.
    Pass the percentage as a whole number, for example `19` for 19%.
    """
    taxable_net = sum(net_amounts, start=Decimal("0"))
    return (taxable_net * rate_percent / Decimal("100")).quantize(
        CENT,
        rounding=ROUND_HALF_UP,
    )


@dataclass(frozen=True)
class Page:
    number: int
    text: str


class HandbookSearch:
    """A BM25 index that ranks whole handbook pages."""

    def __init__(self, pdf_path: Path) -> None:
        self.pages = self._read_pages(pdf_path)
        corpus = [page.text for page in self.pages]
        self.index = bm25s.BM25()
        self.index.index(bm25s.tokenize(corpus, show_progress=False), show_progress=False)

    def search_handbook(self, query: str) -> str:
        """Search the policy handbook for the page stating one rule.

        Search one rule at a time, with one call per rule. The index ranks
        whole pages, and a page usually carries several unrelated rules, so
        a query naming more than one rule tends to rank a page for the wrong
        reason. Each result previews only the line of that page best matching
        the query, so a mixed query previews the wrong rule even when the
        page is the right one.

        Use `read_handbook_page` to read a page in full before relying on it.

        Args:
            query: A few words naming a single rule, in the handbook's own
                wording, such as "nightly room cap", "consumables cap per
                invoice", or "peripheral unit price threshold". Search
                "minibar" and "city tax" as two calls, not as one query.
        """
        if not query.strip():
            return "Enter a few policy keywords."

        pages = self.search_pages(query)
        if not pages:
            return "No policy text matched. Try different keywords."
        return "\n\n".join(
            f"Page {page.number}\n{self._preview(page.text, query)}" for page in pages
        )

    def read_handbook_page(self, page_number: int) -> str:
        """Read the complete extracted text of a handbook page.

        Use a page number returned by `search_handbook`. Page numbers start
        at 1. The response also shows the last few lines of the previous page
        and the first few lines of the next page. When a rule continues past
        the shown excerpt, call this tool again with that page's number to
        read the whole page.
        """
        page = self.find_page(page_number)
        if page is None:
            return f"Page {page_number} is not a handbook page. Use a page number from `search_handbook`."

        sections: list[str] = []
        previous = self._neighbour(page, -1)
        if previous is not None:
            tail = self._edge_lines(previous.text, from_end=True)
            sections.append(f"[PREVIOUS PAGE {previous.number}]\n...\n{tail}")
        sections.append(f"[PAGE {page.number}]\n{page.text}")
        following = self._neighbour(page, 1)
        if following is not None:
            head = self._edge_lines(following.text, from_end=False)
            sections.append(f"[NEXT PAGE {following.number}]\n{head}\n...")
        return "\n\n".join(sections)

    def find_page(self, page_number: int) -> Page | None:
        """Return one indexed page, or None when the number is not indexed."""
        return next((page for page in self.pages if page.number == page_number), None)

    def _neighbour(self, page: Page, offset: int) -> Page | None:
        """Return the indexed page `offset` positions away, or None at the ends."""
        index = next(
            index for index, candidate in enumerate(self.pages) if candidate.number == page.number
        )
        neighbour = index + offset
        if 0 <= neighbour < len(self.pages):
            return self.pages[neighbour]
        return None

    @staticmethod
    def _edge_lines(text: str, *, from_end: bool) -> str:
        """Return a few non-empty lines from the start or end of a page."""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        selected = lines[-CONTEXT_LINES:] if from_end else lines[:CONTEXT_LINES]
        return "\n".join(selected)

    def search_pages(self, query: str) -> list[Page]:
        """Return the best pages, in ranked order."""
        query_tokens = bm25s.tokenize([query], show_progress=False)
        indices, scores = self.index.retrieve(
            query_tokens,
            k=min(RESULTS, len(self.pages)),
            show_progress=False,
        )
        return [self.pages[int(index)] for index, score in zip(indices[0], scores[0]) if score > 0]

    @staticmethod
    def _preview(text: str, query: str) -> str:
        """Return a short page excerpt around the line matching the query best."""
        terms = set(re.findall(r"[a-z0-9]+", query.lower()))
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        best = max(
            range(len(lines)),
            key=lambda index: sum(term in lines[index].lower() for term in terms),
        )
        start = max(0, best - 1)
        stop = min(len(lines), best + 2)
        compact = " ".join(" ".join(lines[start:stop]).split())
        if len(compact) <= PREVIEW_CHARS:
            return compact
        return f"{compact[:PREVIEW_CHARS].rstrip()}…"

    @staticmethod
    def _read_pages(pdf_path: Path) -> list[Page]:
        pages: list[Page] = []
        for number, page in enumerate(PdfReader(pdf_path).pages, start=1):
            text = (page.extract_text() or "").strip()
            if not text or text.count(TOC_LEADERS) >= 3:  # Skip blank and table-of-contents pages.
                continue
            pages.append(Page(number=number, text=text))
        return pages
