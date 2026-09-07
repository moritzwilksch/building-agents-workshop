"""Generate synthetic receipt/invoice images grounded in structured invoice data.

Uses PydanticAI and gemini-3.1-flash-lite-image to generate realistic photographs
or flatbed scans of printed expense receipts and invoices submitted by employees.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
from decimal import Decimal
import json
from pathlib import Path
import sys

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, BinaryImage
from pydantic_ai.capabilities.image_generation import ImageGeneration

# Import schemas and discriminator union from generate_invoice
from generate_invoice import (
    CardPayment,
    CardSlip,
    FlightInvoice,
    FlightSegment,
    FuelReceipt,
    HotelFolio,
    InvoiceCase,
    LineItem,
    RestaurantReceipt,
    StandardInvoice,
    TaxiReceipt,
    TaxItem,
    Vendor,
)

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

DEFAULT_ASPECT_RATIO = "3:4"

image_agent = Agent(
    IMAGE_MODEL,
    output_type=BinaryImage,
    capabilities=[ImageGeneration(aspect_ratio=DEFAULT_ASPECT_RATIO)],
    system_prompt=SYSTEM_PROMPT,
)


def _json_serializable(val: object) -> object:
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    if isinstance(val, Decimal):
        return str(val)
    return str(val)


def generate_invoice_image(
    invoice: BaseModel | dict,
    aspect_ratio: str = DEFAULT_ASPECT_RATIO,
) -> BinaryImage:
    """Generate a realistic photograph or scan of an invoice in portrait orientation.

    Args:
        invoice: Pydantic model instance (e.g., InvoiceCase) or JSON-compatible dictionary.
        aspect_ratio: Desired image aspect ratio (default: '3:4' portrait).

    Returns:
        BinaryImage containing the generated image bytes and media type.
    """
    if isinstance(invoice, BaseModel):
        invoice_dict = invoice.model_dump(mode="json")
    else:
        invoice_dict = dict(invoice)

    # Exclude internal/submission metadata like 'note' from the physical receipt prompt
    invoice_dict.pop("note", None)

    invoice_json_str = json.dumps(invoice_dict, indent=2, default=_json_serializable)

    user_prompt = (
        "Generate a realistic expense submission photograph or scan of the following invoice data in portrait orientation:\n\n"
        f"```json\n{invoice_json_str}\n```\n\n"
        "Ensure all details, items, vendor information, and monetary totals match the data exactly."
    )

    if aspect_ratio == DEFAULT_ASPECT_RATIO:
        agent = image_agent
    else:
        agent = Agent(
            IMAGE_MODEL,
            output_type=BinaryImage,
            capabilities=[ImageGeneration(aspect_ratio=aspect_ratio)],  # type: ignore[arg-type]
            system_prompt=SYSTEM_PROMPT,
        )

    result = agent.run_sync(user_prompt)
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
        help="Path to write the output image (default: <input_dir>/receipt.png or receipt.png)",
    )
    parser.add_argument(
        "--case-dir",
        type=str,
        help="Path to a case directory containing invoice.json; writes receipt.png inside it",
    )
    parser.add_argument(
        "--aspect-ratio",
        type=str,
        default=DEFAULT_ASPECT_RATIO,
        help=f"Aspect ratio for generated image (default: {DEFAULT_ASPECT_RATIO})",
    )
    args = parser.parse_args()

    if args.case_dir:
        input_path = Path(args.case_dir) / "invoice.json"
        ext = "jpg"
        output_path = Path(args.case_dir) / f"receipt.{ext}"
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
    with open(input_path, encoding="utf-8") as f:
        invoice_data = json.load(f)

    print(f"Generating realistic invoice image using {IMAGE_MODEL} (aspect ratio: {args.aspect_ratio})...")
    image = generate_invoice_image(invoice_data, aspect_ratio=args.aspect_ratio)

    ext = "jpg" if "jpeg" in image.media_type else "png"
    if args.case_dir or (args.input and not args.output):
        output_path = output_path.with_suffix(f".{ext}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image.data)
    print(f"Saved generated image ({image.media_type}, {len(image.data)} bytes) to {output_path}")


if __name__ == "__main__":
    main()
