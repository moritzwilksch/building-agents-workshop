"""Handbook loading for Stage 1."""

from pathlib import Path

from pypdf import PdfReader


def read_handbook(pdf_path: Path) -> str:
    """Extract the complete handbook text in page order.

    Takes a few seconds, so `build_agent()` calls it once at startup rather
    than per case.
    """
    pages = [page.extract_text() or "" for page in PdfReader(pdf_path).pages]
    return "\n\n".join(pages).strip()
