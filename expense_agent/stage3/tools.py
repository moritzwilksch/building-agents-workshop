"""Handbook page images for Stage 3.

Stage 3 keeps Stage 2's page search, page reading, and tax arithmetic and adds
one capability: rendering a handbook page so the vision model can read its
diagrams.

`HandbookImages` holds the rendered pages, so `build_agent()` constructs it
once and hands the model its bound method as a tool. Rendering shells out to
poppler, so each page is rendered once and kept.
"""

import io
import threading
from pathlib import Path

from pdf2image import convert_from_path
from pydantic_ai import BinaryContent

from expense_agent.stage2.tools import HandbookSearch

RENDER_DPI = 150


class HandbookImages:
    """Handbook pages rendered as PNGs, each page rendered once.

    Cases run concurrently and often want the same figure page, so the lock
    keeps two of them from rendering it twice.
    """

    def __init__(self, pdf_path: Path, search: HandbookSearch) -> None:
        self.pdf_path = pdf_path
        self.search = search
        self.rendered: dict[int, BinaryContent] = {}
        self.lock = threading.Lock()

    def view_page_image(self, page_number: int) -> BinaryContent | str:
        """Open one handbook page as an image.

        Use a page number returned by `search_handbook`. Page numbers start at 1.
        """
        if self.search.find_page(page_number) is None:
            return f"Page {page_number} is not a handbook page. Use a page number from `search_handbook`."
        with self.lock:
            if page_number not in self.rendered:
                self.rendered[page_number] = self._render(page_number)
            return self.rendered[page_number]

    def _render(self, page_number: int) -> BinaryContent:
        """Render one handbook page as a PNG image."""
        image = convert_from_path(
            self.pdf_path,
            first_page=page_number,
            last_page=page_number,
            fmt="png",
            dpi=RENDER_DPI,
        )[0]
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return BinaryContent(data=buffer.getvalue(), media_type="image/png")
