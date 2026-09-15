"""Generate synthetic invoice data according to the invoice specification.

Samples an invoice archetype from a weighted distribution and generates a validated
Pydantic model instance using PydanticAI and Gemini.
"""

from __future__ import annotations

import argparse
import json
import random
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Annotated, Literal, Union

from dotenv import load_dotenv
from pydantic import BaseModel, Field, TypeAdapter
from pydantic_ai import Agent, ModelRetry, UnexpectedModelBehavior
from pydantic_ai.settings import ModelSettings

load_dotenv()


# Invoice schemas (see invoice-spec.md).

# Arithmetic validation helpers.
#
# Every archetype must add up: line items multiply out, listed charges sum to
# the subtotal, and the subtotal plus tax and tip equals `total_amount`. The
# generation agent runs these checks as an output validator (see
# `check_arithmetic`), so an invoice that does not add up is sent back to the
# model instead of reaching disk.

CENT = Decimal("0.01")

# Sums of listed amounts must be exact to the cent (one cent of slack absorbs
# rounding of a quantity like 2.5 L). Tax amounts derived from a rate get a
# little more room, because a real receipt rounds its tax line.
SUM_TOLERANCE = Decimal("0.01")
TAX_TOLERANCE = Decimal("0.02")


def _money(value: Decimal) -> Decimal:
    return value.quantize(CENT)


def _tax_fraction(rate: Decimal) -> Decimal:
    """Rates appear both as percentages (19) and as fractions (0.19)."""
    return rate / Decimal(100) if rate > 1 else rate


def _mismatch(label: str, actual: Decimal, expected: Decimal, tolerance: Decimal) -> str | None:
    if abs(actual - expected) <= tolerance:
        return None
    return f"{label}: {_money(actual)} != {_money(expected)} (off by {_money(actual - expected)})"


def _sum_items(items: list[LineItem]) -> Decimal:
    return sum((item.total_price for item in items), Decimal(0))


def _check_tax(
    label: str,
    rate: Decimal | None,
    amount: Decimal,
    base: Decimal,
    *,
    inclusive: bool,
) -> str | None:
    """Cross-check one invoice-global tax against the base it is levied on.

    `inclusive` means the tax is already contained in `base` (a restaurant's
    MwSt); otherwise it is added on top of the net base.
    """
    if rate is None:
        # A tax without a rate cannot be checked, so it is not allowed to exist.
        return f"{label}: {_money(amount)} charged without a rate" if amount else None
    fraction = _tax_fraction(rate)
    expected = base - base / (1 + fraction) if inclusive else base * fraction
    return _mismatch(label, amount, expected, TAX_TOLERANCE)


def _problems(*problems: str | None) -> list[str]:
    return [problem for problem in problems if problem]


def _all_line_items(invoice: InvoiceCase) -> list[LineItem]:
    return [
        item
        for field in ("items", "room_charges", "incidentals", "non_fuel_items")
        for item in getattr(invoice, field, [])
    ]


def line_item_problems(item: LineItem) -> list[str]:
    return _problems(
        _mismatch(
            f"line item '{item.description}' total_price",
            item.total_price,
            item.quantity * item.unit_price,
            SUM_TOLERANCE,
        )
    )


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
    category: str = LineItemCategory.MEAL
    is_alcohol: bool = False


class ChargeLine(BaseModel):
    """One numbered charge as it appears on the receipt, top to bottom.

    Every invoice type carries its charges in different fields (items, room
    charges, fares, taxes, tips). `charge_lines` flattens them into this one
    numbered list so `invoice.json` and `label.json` share the same ids and a
    label entry always refers to exactly one receipt line.
    """

    id: int
    description: str
    amount: Decimal


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
    tax_rate: Decimal | None = None  # MwSt, already included in the item prices
    tax_amount: Decimal = Decimal("0.00")
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
    vat_rate: Decimal | None = None  # added on top of the net subtotal
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
    tax_rate: Decimal | None = None  # USt, added on top of the net subtotal
    tax_amount: Decimal = Decimal("0.00")
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

# Per-archetype arithmetic checks. Each returns a list of human-readable
# problems, empty when the invoice adds up. `check_arithmetic` replays them to
# the LLM as a retry; `validate_invoices.py` reports them for files on disk.


def taxi_problems(invoice: TaxiReceipt) -> list[str]:
    return _problems(
        _mismatch("total_amount", invoice.total_amount, invoice.fare_amount + invoice.tip_amount, SUM_TOLERANCE)
    )


def restaurant_problems(invoice: RestaurantReceipt) -> list[str]:
    # A restaurant's MwSt is included in the item prices, so it is not added
    # to the total; only the tip is.
    return _problems(
        _mismatch("subtotal", invoice.subtotal, _sum_items(invoice.items), SUM_TOLERANCE),
        _mismatch("total_amount", invoice.total_amount, invoice.subtotal + invoice.tip_amount, SUM_TOLERANCE),
        _check_tax("tax_amount", invoice.tax_rate, invoice.tax_amount, invoice.subtotal, inclusive=True),
    )


def hotel_problems(invoice: HotelFolio) -> list[str]:
    charges = invoice.room_charges + invoice.incidentals
    return _problems(
        _mismatch("subtotal", invoice.subtotal, _sum_items(charges), SUM_TOLERANCE),
        _mismatch(
            "total_amount",
            invoice.total_amount,
            invoice.subtotal + invoice.city_tax + invoice.vat,
            SUM_TOLERANCE,
        ),
        _check_tax("vat", invoice.vat_rate, invoice.vat, invoice.subtotal, inclusive=False),
        _mismatch(
            "number_of_nights",
            Decimal(invoice.number_of_nights),
            Decimal((invoice.check_out - invoice.check_in).days),
            Decimal(0),
        ),
    )


def flight_problems(invoice: FlightInvoice) -> list[str]:
    expected = invoice.base_fare + sum((tax.amount for tax in invoice.taxes_and_fees), Decimal(0))
    return _problems(_mismatch("total_amount", invoice.total_amount, expected, SUM_TOLERANCE))


def train_problems(invoice: TrainTicket) -> list[str]:
    return _problems(
        _mismatch(
            "total_amount",
            invoice.total_amount,
            invoice.ticket_fare + invoice.seat_reservation_fee,
            SUM_TOLERANCE,
        )
    )


def fuel_problems(invoice: FuelReceipt) -> list[str]:
    return _problems(
        _mismatch("fuel_total", invoice.fuel_total, invoice.liters * invoice.price_per_liter, SUM_TOLERANCE),
        _mismatch(
            "total_amount",
            invoice.total_amount,
            invoice.fuel_total + _sum_items(invoice.non_fuel_items),
            SUM_TOLERANCE,
        ),
    )


def standard_problems(invoice: StandardInvoice) -> list[str]:
    # A B2B invoice lists net item prices and adds VAT on top.
    return _problems(
        _mismatch("subtotal", invoice.subtotal, _sum_items(invoice.items), SUM_TOLERANCE),
        _mismatch(
            "total_amount",
            invoice.total_amount,
            invoice.subtotal + invoice.tax_amount,
            SUM_TOLERANCE,
        ),
        _check_tax("tax_amount", invoice.tax_rate, invoice.tax_amount, invoice.subtotal, inclusive=False),
    )


def invoice_problems(invoice: InvoiceCase) -> list[str]:
    """Every arithmetic problem on an invoice, empty when it all adds up."""
    checks = {
        "taxi": taxi_problems,
        "restaurant": restaurant_problems,
        "hotel": hotel_problems,
        "flight": flight_problems,
        "train": train_problems,
        "fuel": fuel_problems,
        "standard": standard_problems,
    }
    check = checks.get(invoice.invoice_type)
    problems = list(check(invoice)) if check else []
    for item in _all_line_items(invoice):
        problems += line_item_problems(item)
    return problems




def charge_lines(invoice: InvoiceCase) -> list[ChargeLine]:
    """Number every charge on the invoice in the order it appears on paper.

    Only charges that add to `total_amount` get a line. A tax already baked
    into the item prices (a restaurant's MwSt) is not its own charge.
    """
    charges: list[tuple[str, Decimal]] = []

    match invoice:
        case TaxiReceipt():
            charges.append(("Taxi fare", invoice.fare_amount))
            charges.append(("Tip", invoice.tip_amount))
        case RestaurantReceipt():
            charges += [(item.description, item.total_price) for item in invoice.items]
            charges.append(("Tip", invoice.tip_amount))
        case HotelFolio():
            charges += [(item.description, item.total_price) for item in invoice.room_charges]
            charges += [(item.description, item.total_price) for item in invoice.incidentals]
            charges.append(("City tax", invoice.city_tax))
            charges.append(("VAT", invoice.vat))
        case FlightInvoice():
            charges.append(("Base fare", invoice.base_fare))
            charges += [(tax.name, tax.amount) for tax in invoice.taxes_and_fees]
        case TrainTicket():
            charges.append(("Ticket fare", invoice.ticket_fare))
            charges.append(("Seat reservation", invoice.seat_reservation_fee))
        case FuelReceipt():
            charges.append((f"{invoice.fuel_type} ({invoice.liters} L)", invoice.fuel_total))
            charges += [(item.description, item.total_price) for item in invoice.non_fuel_items]
        case StandardInvoice():
            charges += [(item.description, item.total_price) for item in invoice.items]
            charges.append(("VAT", invoice.tax_amount))
        case CardSlip():
            charges.append((invoice.merchant_name, invoice.total_amount))

    # Zero-amount charges (no tip, no seat reservation) never appear on paper.
    return [
        ChargeLine(id=index, description=description, amount=amount)
        for index, (description, amount) in enumerate(
            [(description, amount) for description, amount in charges if amount]
        )
    ]


def validate_charges(invoice: InvoiceCase, charges: list[ChargeLine]) -> list[str]:
    """Check a persisted `charges` list against the invoice it belongs to."""
    problems: list[str] = []
    expected = charge_lines(invoice)

    expected_ids = [charge.id for charge in expected]
    if [charge.id for charge in charges] != expected_ids:
        problems.append(f"charge ids {[charge.id for charge in charges]} != expected {expected_ids}")

    problem = _mismatch(
        "charges sum",
        sum((charge.amount for charge in charges), Decimal(0)),
        invoice.total_amount,
        SUM_TOLERANCE,
    )
    if problem:
        problems.append(problem)
    return problems


def invoice_json(invoice: InvoiceCase) -> str:
    """Serialize an invoice with its numbered `charges` list appended.

    Last line of defence: an invoice that does not add up never gets
    serialized, so no invalid JSON can reach disk even if the agent's output
    validator is bypassed.
    """
    problems = invoice_problems(invoice) + validate_charges(invoice, charge_lines(invoice))
    if problems:
        raise ValueError("invoice does not add up: " + "; ".join(problems))

    data = invoice.model_dump(mode="json")
    data["charges"] = [charge.model_dump(mode="json") for charge in charge_lines(invoice)]
    return json.dumps(data, indent=2, ensure_ascii=False)

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
- Embrace the chaotic reality of real-world expense submissions: employees buying weird or oddly specific things on the company dime (e.g., emergency replacement socks at an airport kiosk, room service midnight artisanal waffles, an absurd "conference survival kit", ultra-niche tech peripherals or hardware store tools).
- Vary the specifics across invoices. Treat the examples above as inspiration for the *kind* of purchase, not a template to copy: invent your own items, dish names, incidentals, and vendor names instead of reusing common motifs. In particular, avoid the well-worn staples rubber ducks, express dry cleaning after a spill, minibar Toblerone, and ghost pepper dishes unless explicitly asked for them.
- In standard invoices ("standard"), generate wild varieties of arbitrary purchases: boutique electronics, custom team swag, odd office supplies, courier emergency delivery of a single adapter, botanical rental plants, escape room team bonding, hardware store supplies. Pick a fresh theme each time (one invoice might be telescope equipment, the next screen-printing supplies, the next rehearsal-room rental).
- In hotel folios ("hotel"), include one or two quirky incidentals drawn from a wide pool: guest laundry or pressing, spa or wellness add-ons, late-night minibar snacks with specific brands, pet cleaning fee, valet or self-parking (possibly with EV charging), workspace pod rental, late checkout, bonus-point purchases, or a gadget forgotten at home ordered to the hotel. Mix different incidentals per invoice rather than repeating the same combo.
- In restaurant receipts ("restaurant"), pick interesting cuisines and memorable item names rather than generic "Meal" (e.g., "Triple Truffle Smashed Burger", "Espresso Martini x3", "Ghost Pepper Tasting Flight", "Sparkling Water (Large)").
- Note field (`note`):
  - Every invoice includes a top-level `note` representing the comment the employee attached when submitting this expense to their workplace system.
  - The note must be down-to-earth, realistic, and square with the actual content/items of the invoice.
  - Keep it to 1-2 short sentences. Avoid forced humor, slapstick tropes, or pretending everything is an urgent emergency.
  - If the expense is unusual or unhinged, provide a clear, plausible business explanation for why the company should reimburse it (e.g. why the team needed 400 rubber ducks for a conference booth, why specialized simulation gear was purchased for an onsite workshop, why hotel laundry was required).
  - Routine transit/taxi/train: can be null, empty string, or a brief destination/purpose.
  - Restaurant expenses: MUST explicitly mention the business purpose and number of attendees (e.g. "Dinner with 2 clients from Acme Corp to celebrate contract signing (3 attendees total)").
- Maintain strict numerical consistency: subtotal, taxes, tips, and total amounts must calculate accurately.
  - Every line item: `total_price` = `quantity` x `unit_price`.
  - Tax is invoice-global: a single `tax_rate` plus `tax_amount` (hotels: `vat_rate` plus `vat`). Line items carry no tax rate of their own, so put every item on the same rate.
  - Restaurant: `subtotal` = sum of items, `total_amount` = `subtotal` + `tip_amount`. MwSt is INCLUDED in the item prices, so `tax_amount` = `subtotal` - `subtotal` / (1 + `tax_rate`) - it is never added to the total.
  - Standard invoice: `subtotal` = sum of net items, `tax_amount` = `subtotal` x `tax_rate`, `total_amount` = `subtotal` + `tax_amount`.
  - Hotel: `subtotal` = sum of room charges + incidentals (net), `vat` = `subtotal` x `vat_rate`, `total_amount` = `subtotal` + `city_tax` + `vat`, and `number_of_nights` = `check_out` - `check_in`.
  - Flight: `total_amount` = `base_fare` + all taxes and fees. Train: `total_amount` = `ticket_fare` + `seat_reservation_fee`. Taxi: `total_amount` = `fare_amount` + `tip_amount`.
  - Fuel: `fuel_total` = `liters` x `price_per_liter`, `total_amount` = `fuel_total` + non-fuel items.
- Ensure all dates, merchant details, addresses, and line item sums are internally consistent.
"""

# Retries cover both output-tool validation failures (the schema's own
# arithmetic validators) and the output validator below.
MAX_RETRIES = 5

agent = Agent(
    "google:gemini-3.8-flash",
    output_type=InvoiceCase,
    system_prompt=SYSTEM_PROMPT,
    model_settings=ModelSettings(thinking="low"),
    retries=MAX_RETRIES,
)


@agent.output_validator
def check_arithmetic(invoice: InvoiceCase) -> InvoiceCase:
    """Feed every arithmetic mistake back to the model so it can fix them.

    Raising `ModelRetry` returns the message to the LLM as a tool-retry prompt;
    the agent then regenerates and is re-validated, up to `MAX_RETRIES` times.
    """
    problems = invoice_problems(invoice)
    if problems:
        print(f"  Retrying, invoice does not add up: {'; '.join(problems)}")
        raise ModelRetry(
            "The invoice does not add up. Fix these and return the whole invoice again:\n"
            + "\n".join(f"- {problem}" for problem in problems)
        )
    return invoice


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

            try:
                invoice = generate_invoice(chosen_type, seed=case_seed)
                payload = invoice_json(invoice)
            except (UnexpectedModelBehavior, ValueError) as error:
                # The model never produced an invoice that adds up. Skip the
                # case rather than write numbers that do not.
                print(f"[{case_name}] Skipped, no valid invoice after {MAX_RETRIES} retries: {error}")
                continue

            output_path = case_dir / "invoice.json"
            output_path.write_text(payload, encoding="utf-8")
            print(f"[{case_name}] Saved to {output_path}")
    else:
        chosen_type = args.type if args.type else sample_invoice_type(rng)
        print(f"Sampled invoice type: {chosen_type} (seed={args.seed})")
        invoice = generate_invoice(chosen_type, seed=args.seed)
        print("\nGenerated Invoice Object:")
        print(invoice_json(invoice))


if __name__ == "__main__":
    main()
