"""Render handbook PDF pages to images the vision model can read.

Stage 3 adds one capability to Stage 2: the `view_page_image` tool. Text
extraction flattens the handbook's decision flowcharts into a title and a
placeholder, so the rules that live only in Figures 1 to 3 never reach a
text search. `render_page` renders any page to a PNG `BinaryContent`, so
the agent can open the page a search hit points at and read the diagram.

Rendering delegates to poppler's `pdftoppm`, which `pdf2image` runs in its
own process per call. That keeps page rendering safe from the worker
threads pydantic-ai uses for synchronous tools.

Usage:
    from pathlib import Path

    from expense_agent.stage3.pages import render_page

    content = render_page(Path("data/handbook.pdf"), page_number=30)
"""

from __future__ import annotations

import io
from functools import lru_cache
from pathlib import Path

from pdf2image import convert_from_path
from pydantic_ai import BinaryContent

RENDER_DPI = 150


@lru_cache(maxsize=None)
def render_page(pdf_path: Path, page_number: int) -> BinaryContent:
    """Render one handbook page as PNG content. Pages are numbered from 1.

    Repeated views of the same page return the cached image.
    """
    image = convert_from_path(
        pdf_path,
        first_page=page_number,
        last_page=page_number,
        fmt="png",
        dpi=RENDER_DPI,
    )[0]
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return BinaryContent(data=buffer.getvalue(), media_type="image/png")
