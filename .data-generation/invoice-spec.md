# Invoice Case Specification & Evaluation Taxonomy

## Context Alignment with Workshop Goals

According to `CONTEXT.md`, the workshop's core challenge is an **expense reimbursement agent** auditing claims against a **company travel & expense policy manual**:
- Decisions: `approved`, `rejected`, or `partially_approved`.
- Calculated payout: Exact currency amounts, deducting non-reimbursable items.
- Cited policy rules: Deterministic rule IDs cited to justify adjustments.

To create rich, realistic failure modes and test cases across Stages 1–4, invoice generation must model not just visual variety, but **expense compliance edge cases**:
1. **Alcohol / minibar split**: Requires line-item parsing to partially approve (reimburse meal/hotel, reject alcohol/spa).
2. **Weekend / holiday dates**: Triggers flowchart logic (Stage 3/4 visual flowchart test case).
3. **Currency mismatch**: Foreign currency requiring conversion against caps or claim currency.
4. **Missing itemization**: Card slips showing only total amount (policy violation requiring itemized bill).
5. **Class of travel / room upgrades**: Business class flights or luxury suites exceeding caps.
6. **Per diem & cap limits**: Daily meal limit caps, tip percentage caps (e.g. max 15-20% tip).

---

## Expanded Invoice Archetypes for Expense Reimbursement

| Archetype | Key Policy Relevance | Typical Layout |
| :--- | :--- | :--- |
| `taxi` | Ride, transit, tolls, tip cap checks | Thermal slip (80mm) |
| `restaurant` | Itemized meal, alcohol deduction, tip cap, attendee counts | Thermal receipt |
| `hotel` | Room rate vs. cap, minibar/spa exclusions, city tax | Multi-line hotel folio (A4) |
| `flight` | Fare class (Economy vs Business), change fees, luggage | Airline e-ticket / itinerary |
| `train` | Rail tickets (often approved over flight for short distances) | Rail ticket / PDF booking |
| `fuel` | Mileage/fuel reimbursement, fuel type, non-fuel items (snacks) | Gas station POS receipt |
| `office_supplies` | Per-item cap, software subscriptions, peripherals, VAT compliance | Standard commercial B2B invoice |
| `card_slip` *(unitemized)* | Card terminal receipt with total only (test case for missing itemization policy rule) | Short terminal printout |

---

## Numbered charges

Each invoice archetype keeps its charges in different fields (`items`,
`room_charges` plus `incidentals`, `base_fare` plus `taxes_and_fees`, tips,
city tax, VAT). After generation, `charge_lines` in `generate_invoice.py`
flattens them into one list in the order they appear on the printed receipt,
top to bottom, and writes it to `invoice.json` as `charges`:

```json
"charges": [
  { "id": 0, "description": "Dry-Aged Smoked Duck Breast", "amount": "58" },
  { "id": 7, "description": "Tip", "amount": "25" }
]
```

Rules:
- One entry per charge that adds to `total_amount`; the amounts sum to it.
- A tax already included in the item prices (a restaurant's MwSt) is not a
  charge; one added on top (a standard invoice's USt, a hotel's VAT) is.
- Zero-amount charges (no tip, no seat reservation) are dropped.
- Ids run `0..n-1` in receipt order.

`label.json` reuses these ids one-to-one, so evaluation matches an agent's
line items to the ground truth by `id` rather than by description text. The
`charges` list is metadata for labeling and evaluation only: the image
generator validates `invoice.json` against the archetype schema, which
ignores the field, so ids never appear on the rendered receipt.

---

## Discriminated Union Pydantic Schema

```python
from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Reusable Building Blocks
# ---------------------------------------------------------------------------

class LineItemCategory:
    MEAL = "meal"
    ALCOHOL = "alcohol"
    LODGING = "lodging"
    TRANSIT = "transit"
    FUEL = "fuel"
    SUPPLIES = "supplies"
    INCIDENTAL = "incidental"  # Minibar, spa, pay-per-view
    FEES = "fees"              # Booking fees, luggage, tips


class LineItem(BaseModel):
    description: str
    quantity: Decimal = Decimal("1.0")
    unit_price: Decimal
    total_price: Decimal
    tax_rate: Decimal | None = None
    category: str = LineItemCategory.MEAL
    is_alcohol: bool = False           # Crucial for partial reimbursement tests


class TaxItem(BaseModel):
    name: str                          # "VAT 19%", "Sales Tax", "City Tax"
    rate: Decimal | None = None
    amount: Decimal


class CardPayment(BaseModel):
    card_brand: str                    # "Visa", "Mastercard", "Amex"
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


# ---------------------------------------------------------------------------
# Archetype 1: Taxi & Ride Receipt
# ---------------------------------------------------------------------------

class TaxiReceipt(BaseModel):
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


# ---------------------------------------------------------------------------
# Archetype 2: Restaurant Receipt (Meals & Entertainment)
# ---------------------------------------------------------------------------

class RestaurantReceipt(BaseModel):
    invoice_type: Literal["restaurant"] = "restaurant"
    id: str
    issued_at: datetime
    currency: str = "EUR"

    vendor: Vendor
    receipt_number: str
    table_number: str | None = None
    number_of_guests: int = 1          # Relevant for client entertainment rules

    items: list[LineItem]
    subtotal: Decimal
    taxes: list[TaxItem] = Field(default_factory=list)
    tip_amount: Decimal = Decimal("0.00")
    total_amount: Decimal

    payment_method: Literal["cash", "card"] = "card"
    card: CardPayment | None = None


# ---------------------------------------------------------------------------
# Archetype 3: Hotel Folio (Lodging & Incidentals)
# ---------------------------------------------------------------------------

class HotelFolio(BaseModel):
    invoice_type: Literal["hotel"] = "hotel"
    id: str
    folio_number: str
    issued_date: date
    currency: str = "EUR"

    hotel: Vendor
    guest_name: str
    room_number: str
    room_category: str = "Standard"    # "Standard", "Deluxe", "Executive Suite"
    check_in: date
    check_out: date
    number_of_nights: int = 1

    room_charges: list[LineItem]       # Daily room rate lines
    incidentals: list[LineItem] = Field(default_factory=list)  # Minibar, laundry, room service

    subtotal: Decimal
    city_tax: Decimal = Decimal("0.00")
    vat: Decimal = Decimal("0.00")
    total_amount: Decimal

    paid: bool = True
    card: CardPayment | None = None


# ---------------------------------------------------------------------------
# Archetype 4: Flight Itinerary & E-Ticket
# ---------------------------------------------------------------------------

class FlightSegment(BaseModel):
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    seat: str | None = None
    cabin_class: Literal["economy", "premium_economy", "business", "first"] = "economy"


class FlightInvoice(BaseModel):
    invoice_type: Literal["flight"] = "flight"
    id: str
    booking_reference: str             # PNR
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


# ---------------------------------------------------------------------------
# Archetype 5: Train / Public Transit Ticket
# ---------------------------------------------------------------------------

class TrainTicket(BaseModel):
    invoice_type: Literal["train"] = "train"
    id: str
    booking_code: str
    issued_at: datetime
    currency: str = "EUR"

    operator: Vendor                   # e.g. "Deutsche Bahn", "SNCF", "Amtrak"
    passenger_name: str
    travel_class: Literal["1st", "2nd"] = "2nd"

    origin_station: str
    destination_station: str
    departure_time: datetime
    is_flexible: bool = False          # Flexible fares vs non-refundable saver

    ticket_fare: Decimal
    seat_reservation_fee: Decimal = Decimal("0.00")
    total_amount: Decimal


# ---------------------------------------------------------------------------
# Archetype 6: Fuel & Gas Station POS
# ---------------------------------------------------------------------------

class FuelReceipt(BaseModel):
    invoice_type: Literal["fuel"] = "fuel"
    id: str
    issued_at: datetime
    currency: str = "EUR"

    vendor: Vendor
    station_id: str | None = None
    pump_number: int = 1

    fuel_type: str                     # "Diesel", "Super E10", "Super Plus"
    liters: Decimal
    price_per_liter: Decimal
    fuel_total: Decimal

    non_fuel_items: list[LineItem] = Field(default_factory=list)  # Car wash, coffee, snacks
    total_amount: Decimal

    payment_method: Literal["card", "cash"] = "card"
    card: CardPayment | None = None


# ---------------------------------------------------------------------------
# Archetype 7: Standard B2B / Office & Software Invoice
# ---------------------------------------------------------------------------

class StandardInvoice(BaseModel):
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


# ---------------------------------------------------------------------------
# Archetype 8: Unitemized Card Terminal Slip (Common Policy Violation)
# ---------------------------------------------------------------------------

class CardSlip(BaseModel):
    """Credit card payment slip without itemized breakdown.
    Crucial negative test case: policy often requires full itemized bills."""
    invoice_type: Literal["card_slip"] = "card_slip"
    id: str
    issued_at: datetime
    currency: str = "EUR"

    merchant_name: str
    terminal_id: str
    total_amount: Decimal
    card: CardPayment


# ---------------------------------------------------------------------------
# Discriminated Union
# ---------------------------------------------------------------------------

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
```

---

## Ground-Truth Expected Policy Evaluation Mapping

To grade agents deterministically as outlined in `CONTEXT.md`, each case can pair with an expected reimbursement ground truth:

```python
class ExpectedPolicyOutcome(BaseModel):
    expected_decision: Literal["approved", "partially_approved", "rejected"]
    expected_reimbursement: Decimal
    expected_currency: str
    cited_rules: list[str]             # e.g. ["RULE_MEAL_CAP", "RULE_NO_ALCOHOL"]
    deductions: list[str] = Field(default_factory=list)  # e.g. ["EUR 14.50 wine excluded"]
```

This pairs directly with each synthetic case so test harnesses can run deterministic assertions.
