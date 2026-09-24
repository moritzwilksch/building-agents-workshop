"""Check local workshop setup without making model requests."""

import os
import shutil
import subprocess
import sys

from dotenv import load_dotenv
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError, PDFSyntaxError, PopplerNotInstalledError
from PIL import Image
from pypdf import PdfReader
from pypdf.errors import PyPdfError

from expense_agent.harness import CaseLoader
from expense_agent.model import MODEL


def check_data(loader: CaseLoader) -> int:
    """Read the handbook, receipts, and labels; catch missing LFS downloads."""
    handbook = loader.data_dir / "handbook.pdf"
    with handbook.open("rb") as source:
        if source.read(5) != b"%PDF-":
            raise ValueError(f"{handbook} is not a PDF; run pixi run git lfs pull")
    if not PdfReader(handbook).pages:
        raise ValueError(f"{handbook} has no pages")

    case_ids = loader.case_ids()
    for case_id in case_ids:
        case = loader.load_input(case_id)
        expected = loader.load_expected(case_id)
        if expected.case_id != case_id:
            raise ValueError(f"{case_id}: label has a different case ID")
        charges = [(charge.id, charge.amount) for charge in case.charges]
        labeled = [(item.id, item.claimed) for item in expected.line_items]
        if charges != labeled:
            raise ValueError(f"{case_id}: invoice charges and label claims differ")
        with Image.open(case.receipt_image) as image:
            image.verify()
    return len(case_ids)


def main() -> None:
    # Keep status emojis readable in redirected output on Windows too.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    load_dotenv()
    try:
        for executable in ("git", "git-lfs", "pdftoppm", "pdfinfo"):
            if shutil.which(executable) is None:
                raise ValueError(f"{executable} not found; run pixi install --locked")
        subprocess.run(["git", "--version"], check=True)
        subprocess.run(["git", "lfs", "version"], check=True)
        loader = CaseLoader()
        count = check_data(loader)
        # Finding Poppler on PATH is not enough: verify it can render this PDF.
        pages = convert_from_path(
            loader.data_dir / "handbook.pdf", first_page=1, last_page=1, dpi=30
        )
        for page in pages:
            page.close()
    except (
        OSError,
        ValueError,
        PyPdfError,
        PDFPageCountError,
        PDFSyntaxError,
        PopplerNotInstalledError,
        subprocess.CalledProcessError,
    ) as error:
        print(f"🚫 Setup check failed: {error}", file=sys.stderr)
        print("Run from the repository root. Try pixi run git lfs pull.", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Local data OK: {count} cases and handbook. PDF rendering works.")
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key or key == "...":
        print("🚫 Before benchmarking: set OPENAI_API_KEY in .env (see .env.example).")
    else:
        print("✅ OPENAI_API_KEY is set; credentials and model access have not been tested.")
    print(f"Configured model: {MODEL}. No model requests made.")


if __name__ == "__main__":
    main()
