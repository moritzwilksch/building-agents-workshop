"""Generate synthetic receipt/invoice images grounded in structured invoice data.

Uses PydanticAI and gemini-3.1-flash-lite-image to generate realistic photographs
or flatbed scans of printed expense receipts and invoices submitted by employees.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import get_args

from dotenv import load_dotenv
from pydantic import TypeAdapter
from pydantic_ai import Agent, BinaryImage
from pydantic_ai.capabilities.image_generation import ImageGeneration
from pydantic_ai.native_tools import ImageAspectRatio

from generate_invoice import InvoiceCase, invoice_adapter

load_dotenv()

SYSTEM_PROMPT = """You are an expert realistic document and photograph generator specializing in workplace expense submissions.
You render authentic, documentary-style photographs or scans of physical invoices, bills, and receipts as submitted by employees into an enterprise expense management system (such as Concur, Expensify, or Navan).

Visual Style & Realism:
- Authenticity: The output must look like an authentic document or real photo/scan of physical paper, NOT a digital mock-up, vector graphic, or synthetic render.
- Capture Modality: Produce either:
  1. A smartphone camera photo taken under varied real-world conditions (desk, hotel nightstand, cafe table, car seat, clipboard, dim bar lighting, bright fluorescent office lighting, slight camera angle/tilt, natural shadows, slight paper creases, folds, or curled thermal paper edges).
  2. A flatbed scanner / feeder scan (straight or slight skew, paper texture, subtle scan lines, staple holes, or contrast characteristics of office scanning).
- Paper & Print Quality:
  - Match the paper medium to the vendor type:
    * Taxi, restaurant, bar, fuel, parking, card slips: narrow thermal paper rolls or small register slips, faint purple/black dot-matrix or thermal ink, slight fading, merchant header logo, micro-perforations, tear edges.
    * Hotel folios, formal business invoices, flight itineraries, standard service bills: A4 or US Letter bond paper, laser-printed or inkjet, formal corporate letterhead, tabular line items, tax breakdowns, footer disclaimers.
    * Train tickets, boarding passes: cardstock ticket stock, magnetic stripe back or thermal card, barcode/QR code, travel class badges.
- Environmental Variance: Introduce natural variations across images:
  - Lighting: overhead fluorescent, warm table lamp, daylight through a window, slight flash reflection, or slight shadows cast by a phone.
  - Backgrounds: wooden tabletop, granite counter, office desk, mousepad, dark laminate, steering wheel, or scanner white/gray backing.
  - Physical wear: subtle creases, wallet folds, slight dog-ears, faint coffee ring or ballpoint pen notation (e.g. checkmarks, tip additions, signature), staple holes at the top corner.

Grounding & Accuracy:
- You will be given a complete structured JSON representation of the invoice.
- Ground ALL visible text, numbers, dates, and amounts in the provided JSON data:
  - Vendor/merchant name, address, phone, tax ID / VAT number.
  - Receipt / invoice / folio / booking number and timestamp.
  - Line item descriptions, quantities, unit prices, and line totals.
  - Subtotals, tax rates, tax breakdown amounts, tip amounts, and total final charge.
  - Payment method, card brand, and masked account number (e.g., **** 1234) if present.
- Do NOT invent conflicting amounts or dates. The numbers on the physical receipt must strictly match the financial amounts in the JSON.
- For foreign characters, currency symbols (€, $, £), and formatting, format them naturally according to the document's locale and country.
"""

IMAGE_MODEL = "google:gemini-3.1-flash-lite-image"

DEFAULT_ASPECT_RATIO: ImageAspectRatio = "3:4"

image_agent = Agent(
    IMAGE_MODEL,
    output_type=BinaryImage,
    capabilities=[ImageGeneration(aspect_ratio=DEFAULT_ASPECT_RATIO)],
    system_prompt=SYSTEM_PROMPT,
)


def generate_invoice_image(
    invoice: InvoiceCase,
    aspect_ratio: ImageAspectRatio = DEFAULT_ASPECT_RATIO,
) -> BinaryImage:
    """Render invoice data as a photograph or scan, excluding the employee note."""
    # The employee note belongs to the claim, not the physical receipt.
    invoice_json = invoice.model_dump_json(indent=2, exclude={"note"})

    user_prompt = (
        "Generate a realistic expense submission photograph or scan of the following invoice data in portrait orientation:\n\n"
        f"```json\n{invoice_json}\n```\n\n"
        "Ensure all details, items, vendor information, and monetary totals match the data exactly."
    )

    if aspect_ratio == DEFAULT_ASPECT_RATIO:
        agent = image_agent
    else:
        agent = Agent(
            IMAGE_MODEL,
            output_type=BinaryImage,
            capabilities=[ImageGeneration(aspect_ratio=aspect_ratio)],
            system_prompt=SYSTEM_PROMPT,
        )

    result = agent.run_sync(user_prompt)
    print(f"Usage: {result.usage}")
    print(f"Cost (USD): {result.usage.cost}")
    return result.output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate realistic receipt/invoice images from structured invoice data."
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        help="Path to invoice.json file",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output image path with --input (default: receipt.jpg or receipt.png beside the input)",
    )
    parser.add_argument(
        "--case-dir",
        type=str,
        help="Case directory containing invoice.json; writes receipt.jpg or receipt.png inside it",
    )
    parser.add_argument(
        "--aspect-ratio",
        type=TypeAdapter(ImageAspectRatio).validate_python,
        choices=get_args(ImageAspectRatio),
        default=DEFAULT_ASPECT_RATIO,
        help=f"Aspect ratio for generated image (default: {DEFAULT_ASPECT_RATIO})",
    )
    args = parser.parse_args()

    if args.case_dir:
        input_path = Path(args.case_dir) / "invoice.json"
        output_path = Path(args.case_dir) / "receipt.jpg"
    elif args.input:
        input_path = Path(args.input)
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = input_path.parent / "receipt.jpg"
    else:
        parser.error("Either --input or --case-dir must be provided.")

    if not input_path.exists():
        sys.exit(f"Error: file not found: {input_path}")

    print(f"Reading invoice from {input_path}...")
    invoice = invoice_adapter.validate_json(input_path.read_text(encoding="utf-8"))

    print(
        f"Generating realistic invoice image using {IMAGE_MODEL} (aspect ratio: {args.aspect_ratio})..."
    )
    image = generate_invoice_image(invoice, aspect_ratio=args.aspect_ratio)

    extension = "jpg" if "jpeg" in image.media_type else "png"
    if args.case_dir or (args.input and not args.output):
        output_path = output_path.with_suffix(f".{extension}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image.data)
    print(f"Saved generated image ({image.media_type}, {len(image.data)} bytes) to {output_path}")


if __name__ == "__main__":
    main()
