"""Generate synthetic invoice data according to the invoice specification.

Samples an invoice archetype from a weighted distribution and generates a validated
Pydantic model instance using PydanticAI and Gemini.
"""

from __future__ import annotations

import argparse
import random
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Annotated, Literal, Union

from dotenv import load_dotenv
from pydantic import BaseModel, Field, TypeAdapter
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

load_dotenv()


# Invoice schemas (see invoice-spec.md).


class LineItemCategory:
    MEAL = "meal"
    ALCOHOL = "alcohol"
    LODGING = "lodging"
    TRANSIT = "transit"
    FUEL = "fuel"
    SUPPLIES = "supplies"
    INCIDENTAL = "incidental"
    FEES = "fees"


class LineItem(BaseModel):
    description: str
    quantity: Decimal = Decimal("1.0")
    unit_price: Decimal
    total_price: Decimal
    tax_rate: Decimal | None = None
    category: str = LineItemCategory.MEAL
    is_alcohol: bool = False


class TaxItem(BaseModel):
    name: str
    rate: Decimal | None = None
    amount: Decimal


class CardPayment(BaseModel):
    card_brand: str
    last_four: str
    auth_code: str | None = None


class Vendor(BaseModel):
    name: str
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    country: str = "DE"
    tax_id: str | None = None
    phone: str | None = None


class BaseInvoice(BaseModel):
    note: str | None = Field(
        default=None,
        description=(
            "Note attached by the employee submitting the expense for reimbursement. "
            "Must be down-to-earth, realistic, and square with the actual items on the invoice. "
            "Keep it to 1-2 short sentences without forced humor or artificial emergencies. "
            "For restaurant expenses, must state the business context and number of attendees (e.g. 'Dinner with 2 clients from Acme Corp to discuss project timeline'). "
            "If the purchase is unusual or unhinged, explain why it was necessary and why the company should reimburse it."
        ),
    )


class TaxiReceipt(BaseInvoice):
    invoice_type: Literal["taxi"] = "taxi"
    id: str
    issued_at: datetime
    currency: str = "EUR"

    vendor_name: str
    taxi_license: str | None = None

    pickup: str | None = None
    dropoff: str | None = None
    distance_km: Decimal | None = None

    fare_amount: Decimal
    tip_amount: Decimal = Decimal("0.00")
    total_amount: Decimal

    payment_method: Literal["cash", "card"] = "card"
    card: CardPayment | None = None


class RestaurantReceipt(BaseInvoice):
    invoice_type: Literal["restaurant"] = "restaurant"
    id: str
    issued_at: datetime
    currency: str = "EUR"

    vendor: Vendor
    receipt_number: str
    table_number: str | None = None
    number_of_guests: int = 1

    items: list[LineItem]
    subtotal: Decimal
    taxes: list[TaxItem] = Field(default_factory=list)
    tip_amount: Decimal = Decimal("0.00")
    total_amount: Decimal

    payment_method: Literal["cash", "card"] = "card"
    card: CardPayment | None = None


class HotelFolio(BaseInvoice):
    invoice_type: Literal["hotel"] = "hotel"
    id: str
    folio_number: str
    issued_date: date
    currency: str = "EUR"

    hotel: Vendor
    guest_name: str
    room_number: str
    room_category: str = "Standard"
    check_in: date
    check_out: date
    number_of_nights: int = 1

    room_charges: list[LineItem]
    incidentals: list[LineItem] = Field(default_factory=list)

    subtotal: Decimal
    city_tax: Decimal = Decimal("0.00")
    vat: Decimal = Decimal("0.00")
    total_amount: Decimal

    paid: bool = True
    card: CardPayment | None = None


class FlightSegment(BaseModel):
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    seat: str | None = None
    cabin_class: Literal["economy", "premium_economy", "business", "first"] = "economy"


class FlightInvoice(BaseInvoice):
    invoice_type: Literal["flight"] = "flight"
    id: str
    booking_reference: str
    ticket_number: str
    issued_at: datetime
    currency: str = "EUR"

    airline: Vendor
    passenger_name: str

    segments: list[FlightSegment]
    base_fare: Decimal
    taxes_and_fees: list[TaxItem]
    total_amount: Decimal

    card: CardPayment | None = None


class TrainTicket(BaseInvoice):
    invoice_type: Literal["train"] = "train"
    id: str
    booking_code: str
    issued_at: datetime
    currency: str = "EUR"

    operator: Vendor
    passenger_name: str
    travel_class: Literal["1st", "2nd"] = "2nd"

    origin_station: str
    destination_station: str
    departure_time: datetime
    is_flexible: bool = False

    ticket_fare: Decimal
    seat_reservation_fee: Decimal = Decimal("0.00")
    total_amount: Decimal


class FuelReceipt(BaseInvoice):
    invoice_type: Literal["fuel"] = "fuel"
    id: str
    issued_at: datetime
    currency: str = "EUR"

    vendor: Vendor
    station_id: str | None = None
    pump_number: int = 1

    fuel_type: str
    liters: Decimal
    price_per_liter: Decimal
    fuel_total: Decimal

    non_fuel_items: list[LineItem] = Field(default_factory=list)
    total_amount: Decimal

    payment_method: Literal["card", "cash"] = "card"
    card: CardPayment | None = None


class StandardInvoice(BaseInvoice):
    invoice_type: Literal["standard"] = "standard"
    id: str
    invoice_number: str
    issued_date: date
    due_date: date | None = None
    currency: str = "EUR"

    vendor: Vendor
    buyer_name: str
    buyer_company: str | None = None
    buyer_tax_id: str | None = None

    items: list[LineItem]
    subtotal: Decimal
    taxes: list[TaxItem]
    total_amount: Decimal

    paid: bool = True
    payment_terms: str | None = None


class CardSlip(BaseInvoice):
    invoice_type: Literal["card_slip"] = "card_slip"
    id: str
    issued_at: datetime
    currency: str = "EUR"

    merchant_name: str
    terminal_id: str
    total_amount: Decimal
    card: CardPayment


InvoiceCase = Annotated[
    Union[
        TaxiReceipt,
        RestaurantReceipt,
        HotelFolio,
        FlightInvoice,
        TrainTicket,
        FuelReceipt,
        StandardInvoice,
        CardSlip,
    ],
    Field(discriminator="invoice_type"),
]


invoice_adapter = TypeAdapter(InvoiceCase)

InvoiceType = Literal["hotel", "standard", "restaurant", "taxi", "flight", "train", "card_slip", "fuel"]

# Sampling weights for invoice types.

INVOICE_TYPE_DISTRIBUTION: dict[InvoiceType, float] = {
    "hotel": 0.28,
    "standard": 0.25,
    "restaurant": 0.22,
    "taxi": 0.12,
    "flight": 0.06,
    "train": 0.03,  # skewed down away from standard DB tickets
    "card_slip": 0.02,
    "fuel": 0.02,
}


def sample_invoice_type(rng: random.Random) -> InvoiceType:
    types = list(INVOICE_TYPE_DISTRIBUTION)
    weights = list(INVOICE_TYPE_DISTRIBUTION.values())
    return rng.choices(types, weights=weights, k=1)[0]


SYSTEM_PROMPT = """You are a synthetic invoice generator producing colorful, varied business expense receipt data.
Generate realistic receipts matching the requested invoice type, but crank up the entropy, personality, and realism.

Guidelines:
- Embrace the chaotic reality of real-world expense submissions: employees buying weird or oddly specific things on the company dime (e.g., emergency replacement socks at an airport kiosk, 400 rubber ducks for a hackathon booth, artisan goat cheese tasting for a client dinner, room service midnight artisanal waffles, an absurd "conference survival kit", 3 AM minibar energy drinks, ultra-niche tech peripherals or hardware store tools).
- In standard invoices ("standard"), generate wild varieties of arbitrary purchases: boutique electronics, custom team swag, odd office supplies, courier emergency delivery of a single adapter, botanical rental plants, escape room team bonding, hardware store supplies.
- In hotel folios ("hotel"), include quirky incidentals: dry cleaning of a single stained silk tie, luxury spa massage, late-night minibar snacks (overpriced Toblerone, boutique craft sodas), pet cleaning fee, valet parking with EV charging surcharge.
- In restaurant receipts ("restaurant"), pick interesting cuisines and memorable item names rather than generic "Meal" (e.g., "Triple Truffle Smashed Burger", "Espresso Martini x3", "Ghost Pepper Tasting Flight", "Sparkling Water (Large)").
- Note field (`note`):
  - Every invoice includes a top-level `note` representing the comment the employee attached when submitting this expense to their workplace system.
  - The note must be down-to-earth, realistic, and square with the actual content/items of the invoice.
  - Keep it to 1-2 short sentences. Avoid forced humor, slapstick tropes, or pretending everything is an urgent emergency.
  - If the expense is unusual or unhinged, provide a clear, plausible business explanation for why the company should reimburse it (e.g. why the team needed 400 rubber ducks for a conference booth, why specialized simulation gear was purchased for an onsite workshop, why hotel laundry was required).
  - Routine transit/taxi/train: can be null, empty string, or a brief destination/purpose.
  - Restaurant expenses: MUST explicitly mention the business purpose and number of attendees (e.g. "Dinner with 2 clients from Acme Corp to celebrate contract signing (3 attendees total)").
- Maintain strict numerical consistency: subtotal, taxes, tips, and total amounts must calculate accurately.
- Ensure all dates, merchant details, addresses, and line item sums are internally consistent.
"""

agent = Agent(
    "google:gemini-3.8-flash",
    output_type=InvoiceCase,
    system_prompt=SYSTEM_PROMPT,
    model_settings=ModelSettings(thinking="low"),
)


def generate_invoice(invoice_type: InvoiceType, seed: int | None = None) -> InvoiceCase:
    prompt = (
        f"Generate a realistic expense receipt of type '{invoice_type}'. "
        f"Ensure `invoice_type` is set exactly to '{invoice_type}'."
    )
    settings = ModelSettings(thinking="low")
    if seed is not None:
        settings["seed"] = seed
    result = agent.run_sync(prompt, model_settings=settings)
    print(f"Usage: {result.usage}")
    print(f"Cost (USD): {result.usage.cost}")
    return result.output


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic invoice objects adhering to the invoice spec.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for archetype sampling and generation")
    parser.add_argument(
        "--type",
        type=TypeAdapter(InvoiceType).validate_python,
        choices=list(INVOICE_TYPE_DISTRIBUTION),
        default=None,
        help="Explicit invoice type (default: randomly sampled)",
    )
    parser.add_argument(
        "--num-cases",
        type=int,
        default=1,
        help="Number of cases to generate into --output-dir",
    )
    parser.add_argument(
        "--start-idx",
        type=int,
        default=1,
        help="Starting case index (e.g. 1 for case-0001)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save generated cases (e.g. data)",
    )
    args = parser.parse_args()

    rng = random.Random(args.seed)

    if args.output_dir:
        output_dir = Path(args.output_dir)
        for offset in range(args.num_cases):
            case_index = args.start_idx + offset
            case_name = f"case-{case_index:04d}"
            case_dir = output_dir / case_name
            case_dir.mkdir(parents=True, exist_ok=True)

            case_seed = rng.randint(0, 1_000_000)
            case_rng = random.Random(case_seed)
            chosen_type = args.type if args.type else sample_invoice_type(case_rng)
            print(f"[{case_name}] Generating {chosen_type} (seed={case_seed})...")

            invoice = generate_invoice(chosen_type, seed=case_seed)
            output_path = case_dir / "invoice.json"
            output_path.write_text(invoice.model_dump_json(indent=2), encoding="utf-8")
            print(f"[{case_name}] Saved to {output_path}")
    else:
        chosen_type = args.type if args.type else sample_invoice_type(rng)
        print(f"Sampled invoice type: {chosen_type} (seed={args.seed})")
        invoice = generate_invoice(chosen_type, seed=args.seed)
        print("\nGenerated Invoice Object:")
        print(invoice.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
