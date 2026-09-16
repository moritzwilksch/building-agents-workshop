"""Generate the table-heavy handbook chapters.

Emits the appendix (chapter 14) plus reference, historical, draft,
documentation, audit, directory, governance, and archive chapters beside the
authored handbook chapters 01-13. The design follows three rules:

1. Governing tables are wide and deep. Chapter 14 lists one row per city and
   one row per country with the same cap values as before, so a full-document
   reader must copy values out of long tables while a keyword search lands on
   the single governing row.
2. Filler volume is keyword-orthogonal. The governance clauses and the
   settlement archive avoid the retrieval vocabulary (cap, tip, hotel, ...)
   so search never surfaces them, while a full read still pays for every
   token. `BANNED_TERMS` enforces this at generation time.
3. Distractors self-label. Any row that shares retrieval vocabulary with the
   governing chapters carries its disqualifier inside the row ("Superseded --
   never payable", "Draft -- not effective", "... governs"), so a search hit
   window disqualifies itself.

No case's answer changes: Version 4.2 governs all claims processed on or
after January 1, 2024, tier and tip values are unchanged, and the historical
and draft schedules are never effective.

Run in the default Pixi environment, then compile the handbook:

    pixi run python .data-generation/generate_handbook_schedules.py
    pixi run -e data-generation compile-handbook
"""

from __future__ import annotations

from pathlib import Path

HANDBOOK_DIR = Path(__file__).parent / "handbook"

HEADER_FILL = 'fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none }'

TIER_1 = [
    "London", "New York City", "San Francisco", "Zurich", "Geneva",
    "Paris", "Tokyo", "Singapore", "Hong Kong",
]
TIER_2 = [
    "Berlin", "Munich", "Frankfurt", "Hamburg", "Amsterdam", "Dublin",
    "Chicago", "Boston", "Seattle", "Toronto", "Sydney", "Milan",
]
TIER_3 = [
    "Leipzig", "Düsseldorf", "Dortmund", "Köln", "Darmstadt", "Stuttgart",
    "Nuremberg", "Bonn", "Essen", "Bremen", "Hanover", "Dresden", "Freiburg",
    "Mannheim", "Karlsruhe", "Münster", "Wiesbaden", "Augsburg", "Kiel",
    "Vienna", "Salzburg", "Graz", "Linz", "Basel", "Bern", "Lausanne",
    "Brussels", "Antwerp", "Ghent", "Leuven", "Rotterdam", "The Hague",
    "Utrecht", "Eindhoven", "Copenhagen", "Aarhus", "Oslo", "Bergen",
    "Stockholm", "Gothenburg", "Malmo", "Helsinki", "Espoo", "Tampere",
    "Madrid", "Barcelona", "Valencia", "Seville", "Bilbao", "Lisbon",
    "Porto", "Rome", "Turin", "Florence", "Naples", "Bologna", "Venice",
    "Athens", "Thessaloniki", "Prague", "Brno", "Warsaw", "Krakow",
    "Wroclaw", "Budapest", "Bucharest", "Sofia", "Belgrade", "Zagreb",
    "Bratislava", "Ljubljana", "Riga", "Tallinn", "Vilnius", "Tel Aviv",
    "Jerusalem", "Haifa", "Dubai", "Abu Dhabi", "Doha", "Riyadh", "Kuwait City",
    "Manama", "Muscat", "Istanbul", "Ankara", "Cairo", "Nairobi", "Lagos",
    "Johannesburg", "Cape Town", "Casablanca", "Mumbai", "New Delhi",
    "Bengaluru", "Chennai", "Pune", "Hyderabad", "Bangkok", "Jakarta",
    "Manila", "Ho Chi Minh City", "Hanoi", "Kuala Lumpur", "Taipei", "Seoul",
    "Busan", "Brisbane", "Melbourne", "Perth", "Auckland", "Wellington",
    "Vancouver", "Montreal", "Calgary", "Ottawa", "Mexico City", "Monterrey",
    "Sao Paulo", "Rio de Janeiro", "Buenos Aires", "Santiago", "Lima",
    "Bogota", "Atlanta", "Miami", "Dallas", "Houston", "Denver", "Phoenix",
    "Los Angeles", "San Diego", "Portland", "Austin", "Nashville", "Philadelphia",
    "Washington DC", "New Orleans", "Minneapolis", "Detroit", "Charlotte",
    "Pittsburgh", "Cleveland", "Columbus", "Indianapolis", "Kansas City",
    "Salt Lake City", "St. Louis", "Raleigh", "Richmond", "Orlando", "Tampa",
]

# Lodging cap values per tier. Must match the labels: the tiers and values
# below are the single source of truth for chapters 14 and 15.
TIER_CAPS = {
    "Tier 1": ("€220.00", "\\$250.00", "£190.00"),
    "Tier 2": ("€160.00", "\\$180.00", "£140.00"),
    "Tier 3": ("€120.00", "\\$140.00", "£105.00"),
}

CITY_COUNTRY = {
    # Tier 1
    "London": "United Kingdom", "New York City": "United States",
    "San Francisco": "United States", "Zurich": "Switzerland",
    "Geneva": "Switzerland", "Paris": "France", "Tokyo": "Japan",
    "Singapore": "Singapore", "Hong Kong": "Hong Kong SAR",
    # Tier 2
    "Berlin": "Germany", "Munich": "Germany", "Frankfurt": "Germany",
    "Hamburg": "Germany", "Amsterdam": "Netherlands", "Dublin": "Ireland",
    "Chicago": "United States", "Boston": "United States",
    "Seattle": "United States", "Toronto": "Canada", "Sydney": "Australia",
    "Milan": "Italy",
    # Tier 3: Germany
    "Leipzig": "Germany", "Düsseldorf": "Germany", "Dortmund": "Germany",
    "Köln": "Germany", "Darmstadt": "Germany", "Stuttgart": "Germany",
    "Nuremberg": "Germany", "Bonn": "Germany", "Essen": "Germany",
    "Bremen": "Germany", "Hanover": "Germany", "Dresden": "Germany",
    "Freiburg": "Germany", "Mannheim": "Germany", "Karlsruhe": "Germany",
    "Münster": "Germany", "Wiesbaden": "Germany", "Augsburg": "Germany",
    "Kiel": "Germany",
    # Tier 3: Alpine
    "Vienna": "Austria", "Salzburg": "Austria", "Graz": "Austria",
    "Linz": "Austria", "Basel": "Switzerland", "Bern": "Switzerland",
    "Lausanne": "Switzerland",
    # Tier 3: Benelux
    "Brussels": "Belgium", "Antwerp": "Belgium", "Ghent": "Belgium",
    "Leuven": "Belgium", "Rotterdam": "Netherlands", "The Hague": "Netherlands",
    "Utrecht": "Netherlands", "Eindhoven": "Netherlands",
    # Tier 3: Nordics
    "Copenhagen": "Denmark", "Aarhus": "Denmark", "Oslo": "Norway",
    "Bergen": "Norway", "Stockholm": "Sweden", "Gothenburg": "Sweden",
    "Malmo": "Sweden", "Helsinki": "Finland", "Espoo": "Finland",
    "Tampere": "Finland",
    # Tier 3: Iberia, Italy, Greece
    "Madrid": "Spain", "Barcelona": "Spain", "Valencia": "Spain",
    "Seville": "Spain", "Bilbao": "Spain", "Lisbon": "Portugal",
    "Porto": "Portugal", "Rome": "Italy", "Turin": "Italy",
    "Florence": "Italy", "Naples": "Italy", "Bologna": "Italy",
    "Venice": "Italy", "Athens": "Greece", "Thessaloniki": "Greece",
    # Tier 3: Central and Eastern Europe
    "Prague": "Czechia", "Brno": "Czechia", "Warsaw": "Poland",
    "Krakow": "Poland", "Wroclaw": "Poland", "Budapest": "Hungary",
    "Bucharest": "Romania", "Sofia": "Bulgaria", "Belgrade": "Serbia",
    "Zagreb": "Croatia", "Bratislava": "Slovakia", "Ljubljana": "Slovenia",
    "Riga": "Latvia", "Tallinn": "Estonia", "Vilnius": "Lithuania",
    # Tier 3: Middle East
    "Tel Aviv": "Israel", "Jerusalem": "Israel", "Haifa": "Israel",
    "Dubai": "United Arab Emirates", "Abu Dhabi": "United Arab Emirates",
    "Doha": "Qatar", "Riyadh": "Saudi Arabia", "Kuwait City": "Kuwait",
    "Manama": "Bahrain", "Muscat": "Oman", "Istanbul": "Turkey",
    "Ankara": "Turkey",
    # Tier 3: Africa
    "Cairo": "Egypt", "Nairobi": "Kenya", "Lagos": "Nigeria",
    "Johannesburg": "South Africa", "Cape Town": "South Africa",
    "Casablanca": "Morocco",
    # Tier 3: South and Southeast Asia
    "Mumbai": "India", "New Delhi": "India", "Bengaluru": "India",
    "Chennai": "India", "Pune": "India", "Hyderabad": "India",
    "Bangkok": "Thailand", "Jakarta": "Indonesia", "Manila": "Philippines",
    "Ho Chi Minh City": "Vietnam", "Hanoi": "Vietnam",
    "Kuala Lumpur": "Malaysia", "Taipei": "Taiwan",
    # Tier 3: East Asia and Oceania
    "Seoul": "South Korea", "Busan": "South Korea", "Brisbane": "Australia",
    "Melbourne": "Australia", "Perth": "Australia", "Auckland": "New Zealand",
    "Wellington": "New Zealand",
    # Tier 3: Americas
    "Vancouver": "Canada", "Montreal": "Canada", "Calgary": "Canada",
    "Ottawa": "Canada", "Mexico City": "Mexico", "Monterrey": "Mexico",
    "Sao Paulo": "Brazil", "Rio de Janeiro": "Brazil",
    "Buenos Aires": "Argentina", "Santiago": "Chile", "Lima": "Peru",
    "Bogota": "Colombia", "Atlanta": "United States", "Miami": "United States",
    "Dallas": "United States", "Houston": "United States",
    "Denver": "United States", "Phoenix": "United States",
    "Los Angeles": "United States", "San Diego": "United States",
    "Portland": "United States", "Austin": "United States",
    "Nashville": "United States", "Philadelphia": "United States",
    "Washington DC": "United States", "New Orleans": "United States",
    "Minneapolis": "United States", "Detroit": "United States",
    "Charlotte": "United States", "Pittsburgh": "United States",
    "Cleveland": "United States", "Columbus": "United States",
    "Indianapolis": "United States", "Kansas City": "United States",
    "Salt Lake City": "United States", "St. Louis": "United States",
    "Raleigh": "United States", "Richmond": "United States",
    "Orlando": "United States", "Tampa": "United States",
}

TIP_20 = ["United States", "Canada", "Germany"]
TIP_125 = ["United Kingdom"]
TIP_10 = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia",
    "Denmark", "Estonia", "Finland", "France", "Greece", "Hungary",
    "Iceland", "Ireland", "Italy", "Latvia", "Liechtenstein", "Lithuania",
    "Luxembourg", "Malta", "Netherlands", "Norway", "Poland", "Portugal",
    "Romania", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland",
]
TIP_0 = ["Japan", "South Korea", "Singapore", "Hong Kong"]
OTHER_COUNTRIES = [
    ("Australia", "Asia-Pacific", "AUD"), ("New Zealand", "Asia-Pacific", "NZD"),
    ("China", "Asia-Pacific", "CNY"), ("Taiwan", "Asia-Pacific", "TWD"),
    ("India", "Asia-Pacific", "INR"), ("Indonesia", "Asia-Pacific", "IDR"),
    ("Malaysia", "Asia-Pacific", "MYR"), ("Thailand", "Asia-Pacific", "THB"),
    ("Vietnam", "Asia-Pacific", "VND"), ("Philippines", "Asia-Pacific", "PHP"),
    ("United Arab Emirates", "Middle East", "AED"), ("Saudi Arabia", "Middle East", "SAR"),
    ("Qatar", "Middle East", "QAR"), ("Israel", "Middle East", "ILS"),
    ("Turkey", "Middle East", "TRY"), ("Egypt", "Africa", "EGP"),
    ("South Africa", "Africa", "ZAR"), ("Kenya", "Africa", "KES"),
    ("Nigeria", "Africa", "NGN"), ("Morocco", "Africa", "MAD"),
    ("Brazil", "Latin America", "BRL"), ("Mexico", "Latin America", "MXN"),
    ("Argentina", "Latin America", "ARS"), ("Chile", "Latin America", "CLP"),
    ("Colombia", "Latin America", "COP"), ("Peru", "Latin America", "PEN"),
]

ITEM_TREATMENTS = [
    ("Airline base fare", "Air travel", "Reimbursable within cabin and booking rules", "4"),
    ("Economy cabin", "Air travel", "Reimbursable", "4"),
    ("Premium economy cabin", "Air travel", "Reimbursable at six hours or more", "4"),
    ("Business class on short-haul", "Air travel", "Deducted in full", "4"),
    ("First class cabin", "Air travel", "Deducted", "4"),
    ("Airport passenger service charge", "Air travel", "Reimbursable in full", "4"),
    ("Aviation security charge", "Air travel", "Reimbursable in full", "4"),
    ("Carrier-imposed fuel surcharge", "Air travel", "Reimbursable in full", "4"),
    ("Government departure tax", "Air travel", "Reimbursable in full", "4"),
    ("Seat selection fee", "Air travel", "Deducted", "4"),
    ("Extra-legroom seat", "Air travel", "Deducted", "4"),
    ("Priority boarding", "Air travel", "Deducted", "4"),
    ("Airport lounge day pass", "Air travel", "Deducted", "4"),
    ("Checked baggage fee", "Air travel", "Reimbursable when business-necessary", "4"),
    ("In-flight Wi-Fi", "Air travel", "Reimbursable", "4"),
    ("Flight change fee", "Air travel", "Reimbursable when business-necessary", "4"),
    ("Unused non-refundable ticket", "Air travel", "Evaluated case by case", "4"),
    ("Rail second class fare", "Ground transport", "Reimbursable", "5"),
    ("Rail first class fare", "Ground transport", "Reimbursable only over four hours", "5"),
    ("Seat reservation fee", "Ground transport", "Reimbursable in full", "5"),
    ("Flexible rail fare", "Ground transport", "Reimbursable in full", "5"),
    ("Rail season pass", "Ground transport", "Reimbursable pro rata", "5"),
    ("Taxi or ride-hailing fare", "Ground transport", "Capped; see Chapter 5", "5"),
    ("Premium rideshare tier", "Ground transport", "Excess over threshold deducted", "5"),
    ("Taxi waiting time", "Ground transport", "Reimbursable as part of the fare", "5"),
    ("Taxi luggage surcharge", "Ground transport", "Reimbursable as part of the fare", "5"),
    ("Rental car, intermediate", "Ground transport", "Reimbursable", "5"),
    ("Rental car, premium", "Ground transport", "Deducted without named approver", "5"),
    ("Rental collision damage waiver", "Ground transport", "Reimbursable", "5"),
    ("Fuel for rental vehicle", "Ground transport", "Reimbursable when rental named", "5"),
    ("Mileage, personal vehicle", "Ground transport", "Reimbursable at statutory rate", "5"),
    ("Road toll", "Ground transport", "Reimbursable", "5"),
    ("Congestion charge", "Ground transport", "Reimbursable", "5"),
    ("Parking garage fee", "Ground transport", "Reimbursable", "5"),
    ("Parking fine", "Ground transport", "Deducted", "11"),
    ("Commuting fare", "Ground transport", "Deducted", "11"),
    ("Hotel room rate", "Lodging", "Capped per city tier", "6"),
    ("Hotel suite upgrade", "Lodging", "Excess over cap deducted", "6"),
    ("Hotel city tax", "Lodging", "Reimbursable in full", "6"),
    ("Resort or facility fee", "Lodging", "Reimbursable when mandatory", "6"),
    ("Optional amenity bundle", "Lodging", "Deducted", "6"),
    ("Hotel minibar item", "Lodging", "Deducted", "6"),
    ("Pay-per-view movie", "Lodging", "Deducted", "6"),
    ("Spa or massage treatment", "Lodging", "Deducted", "6"),
    ("Hotel gym surcharge", "Lodging", "Deducted", "6"),
    ("Pet cleaning fee", "Lodging", "Deducted", "6"),
    ("Late check-out fee", "Lodging", "Deducted", "6"),
    ("Laundry on a stay over five nights", "Lodging", "Capped per seven-day period", "6"),
    ("Garment rescue on a short stay", "Lodging", "Capped when the note explains it", "6"),
    ("Hotel parking with rental vehicle", "Lodging", "Capped per night", "6"),
    ("Hotel breakfast line", "Lodging", "Capped at the breakfast limit", "6"),
    ("Room service dinner", "Lodging", "Meal cap applies", "6"),
    ("Breakfast (solo)", "Meals", "Capped at the breakfast limit", "7"),
    ("Lunch (solo)", "Meals", "Capped at the lunch limit", "7"),
    ("Dinner (solo)", "Meals", "Capped at the dinner limit", "7"),
    ("Daily food total (solo)", "Meals", "Capped at the daily aggregate", "7"),
    ("Overtime meal at home office", "Meals", "Capped when note states late work", "7"),
    ("Alcohol (solo travel)", "Meals", "Deducted in full", "7"),
    ("Non-alcoholic beer or mocktail", "Meals", "Reimbursable as an ordinary beverage", "7"),
    ("Restaurant service charge", "Meals", "Reimbursable when printed", "7"),
    ("Restaurant tip", "Meals", "Capped by vendor country", "7"),
    ("Truffle dish", "Meals", "Screened under Figure 3", "13"),
    ("Truffle oil", "Meals", "Screened under Figure 3", "13"),
    ("Caviar", "Meals", "Ordinary meal cap applies", "7"),
    ("Wagyu dish", "Meals", "Ordinary meal cap applies", "7"),
    ("Lobster dish", "Meals", "Ordinary meal cap applies", "7"),
    ("Client dinner food", "Client hospitality", "Per-person cap in Figure 2", "13"),
    ("Client dinner alcohol", "Client hospitality", "Allowance in Figure 2", "13"),
    ("Internal team meal", "Client hospitality", "Per-person cap in Figure 2", "13"),
    ("Candidate interview meal", "Client hospitality", "Client hospitality rules apply", "8"),
    ("Sports event ticket", "Client hospitality", "Standard tier only", "8"),
    ("Theater ticket", "Client hospitality", "Standard tier only", "8"),
    ("VIP hospitality box", "Client hospitality", "Deducted", "8"),
    ("Night club bill", "Client hospitality", "Rejected in full", "8"),
    ("Casino bill", "Client hospitality", "Rejected in full", "8"),
    ("Weekend restaurant receipt", "Weekend", "Evaluated under Figure 1", "13"),
    ("Weekend hotel night", "Weekend", "Evaluated under Figure 1", "13"),
    ("Weekend taxi receipt", "Weekend", "Evaluated under Figure 1", "13"),
    ("Personal extension hotel night", "Weekend", "Deducted", "9"),
    ("Museum admission", "Weekend", "Deducted", "9"),
    ("City tour ticket", "Weekend", "Deducted", "9"),
    ("Companion airfare", "Companions", "Deducted", "11"),
    ("Companion meal share", "Companions", "Deducted", "9"),
    ("Double-occupancy surcharge", "Companions", "Deducted", "9"),
    ("Stationery under the cap", "Equipment", "Reimbursable", "10"),
    ("Bulk paper order", "Equipment", "Requisition instead", "10"),
    ("Peripheral under the threshold", "Equipment", "Reimbursable", "10"),
    ("Peripheral at or above threshold", "Equipment", "Needs an IT ticket number", "10"),
    ("Replacement charger while traveling", "Equipment", "Capped", "10"),
    ("External monitor", "Equipment", "Needs an IT ticket number", "10"),
    ("Noise-canceling headset", "Equipment", "Needs an IT ticket number", "10"),
    ("Specialist test equipment", "Equipment", "Needs an IT ticket number", "10"),
    ("Office chair or standing desk", "Equipment", "Deducted", "10"),
    ("Office plant or plant care", "Equipment", "Deducted", "10"),
    ("Temporary event staging greenery", "Equipment", "Reimbursable with event approval", "10"),
    ("Software subscription", "Equipment", "Deducted", "10"),
    ("Cloud compute credits", "Equipment", "Deducted", "10"),
    ("Generative AI API credits", "Equipment", "Deducted", "10"),
    ("Event booth display", "Equipment", "Reimbursable with event approval", "10"),
    ("Promotional giveaway", "Equipment", "Reimbursable with event approval", "10"),
    ("Team swag", "Equipment", "Reimbursable with event approval", "10"),
    ("Workshop prop", "Equipment", "Reimbursable with event approval", "10"),
    ("Team-building activity", "Equipment", "Capped per participant", "10"),
    ("Courier of client deliverables", "Equipment", "Reimbursable", "10"),
    ("Travel eSIM or data bundle", "Equipment", "Capped per trip", "10"),
    ("Professional book", "Equipment", "Capped when note cites the matter", "10"),
    ("Professional periodical", "Equipment", "Deducted", "10"),
    ("Retail gift card", "Prohibited", "Deducted", "11"),
    ("Amazon voucher", "Prohibited", "Deducted", "11"),
    ("Prepaid debit card", "Prohibited", "Deducted", "11"),
    ("Traffic citation", "Prohibited", "Deducted", "11"),
    ("Haircut or salon", "Prohibited", "Deducted", "11"),
    ("Personal clothing", "Prohibited", "Deducted", "11"),
    ("Over-the-counter medicine", "Prohibited", "Deducted", "11"),
    ("Gym day pass", "Prohibited", "Deducted", "11"),
    ("Sunscreen", "Prohibited", "Deducted", "11"),
    ("Luggage set", "Prohibited", "Deducted", "11"),
    ("Passport renewal fee", "Prohibited", "Deducted", "11"),
    ("Tourist visa fee", "Prohibited", "Deducted", "11"),
    ("Neck pillow", "Prohibited", "Deducted", "11"),
    ("Streaming subscription", "Prohibited", "Deducted", "11"),
    ("Pet boarding", "Prohibited", "Deducted", "11"),
    ("Childcare during travel", "Prohibited", "Deducted", "11"),
    ("Lost-baggage essentials", "Exception", "Capped with a PIR reference", "11"),
    ("VAT on a commercial invoice", "Tax", "Reimbursable when VAT number shown", "12"),
    ("VAT on a folio missing its number", "Tax", "Reimbursed net of VAT", "12"),
    ("Foreign cash left over", "Tax", "Not reimbursable", "12"),
    ("Dynamic currency conversion markup", "Tax", "Not reimbursable", "12"),
]

GLOSSARY = [
    ("Aggregate cap", "The maximum a category may reimburse across a day or period."),
    ("Approving manager", "The person with Delegation of Authority for a claim's value."),
    ("Bleisure", "Personal leisure days added to a business trip at the employee's cost."),
    ("Card slip", "A summary terminal receipt; not sufficient substantiation on its own."),
    ("City tax", "A mandatory municipal lodging levy, reimbursable in full."),
    ("Commercial invoice", "A vendor invoice for goods, governed by Chapter 10."),
    ("DoA", "Delegation of Authority; the approval tiers in Chapter 3."),
    ("Event surcharge cap", "A nightly lodging cap that replaces the tier cap in a named event week."),
    ("Folio", "An itemized hotel checkout bill."),
    ("Foreign VAT recovery", "The firm's reclaim of consumption tax on foreign business spend."),
    ("Garment rescue", "Spot cleaning of business attire on a stay of five nights or fewer."),
    ("Incidental", "A folio line other than the room rate; most are deducted."),
    ("PIR", "Property Irregularity Report; the airline record of a lost or delayed bag."),
    ("Pre-tip bill", "The bill total before a tip, used to compute the tip cap."),
    ("Reimbursable", "Eligible for repayment under the caps and conditions in this handbook."),
    ("Second class", "The standard rail cabin; reimbursable without further justification."),
    ("Solo dining", "One employee eating alone; governed by Chapter 7."),
    ("Staging greenery", "Temporary rented plants for a named, pre-approved event."),
    ("Superseded", "A schedule that applied to an earlier handbook version and is not current."),
    ("Tier", "A city's lodging cap band: Tier 1, Tier 2, or Tier 3."),
    ("Tip cap", "The maximum reimbursable gratuity, set by vendor country."),
    ("Truffle policy", "The Figure 3 screen applied before meal caps."),
    ("Unjustified ride", "A taxi or rideshare fare above the threshold without a stated justification."),
    ("VAT registration number", "A vendor tax identifier required on folios and commercial invoices."),
]

DOCUMENTATION_REQUIREMENTS = [
    ("Airline e-ticket", "Passenger name, routing, cabin, fare and tax breakdown", "Business purpose; approver for high-value travel", "4"),
    ("Rail ticket", "Origin, destination, class, fare", "Destination and purpose", "5"),
    ("Taxi or ride-hailing receipt", "Operator, date, time, fare", "Route and, where needed, a justification", "5"),
    ("Rental car agreement", "Vehicle class, dates, daily rate", "Client site served and approval", "5"),
    ("Fuel receipt", "Volume, amount, station", "The rental or pool vehicle it served", "5"),
    ("Hotel folio", "Itemized room rate, city tax, incidentals, VAT number", "Business purpose and event if any", "6"),
    ("Solo restaurant bill", "Itemized dishes and beverages, time", "Purpose if away from the office city", "7"),
    ("Group restaurant bill", "Itemized dishes, beverages, guest count", "Purpose, external organizations, attendee count", "8"),
    ("Commercial invoice", "Vendor name, VAT number, net, gross, line items", "Event name and budget owner where relevant", "10"),
    ("Conference registration", "Attendee name, event dates, fee", "Business relevance to a matter", "10"),
    ("Mileage log", "Departure, arrival, distance", "Client matter or purpose", "5"),
    ("Parking receipt", "Garage, date, time, amount", "Vehicle and destination", "5"),
    ("Baggage fee receipt", "Airline, flight, amount", "Reason the baggage was required", "4"),
    ("Currency receipt", "Amount, currency, date", "The underlying business spend", "12"),
]

RETENTION_SCHEDULE = [
    ("Airline ticket and boarding records", "7 years", "Tax substantiation"),
    ("Hotel folios", "7 years", "Tax substantiation and VAT recovery"),
    ("Restaurant and entertainment bills", "7 years", "Client hospitality audit"),
    ("Commercial invoices and goods receipts", "10 years", "Asset and procurement audit"),
    ("Corporate card statements", "7 years", "Reconciliation"),
    ("Delegation of Authority approvals", "10 years", "Governance"),
    ("Event pre-approval emails", "7 years", "Budget owner evidence"),
    ("Travel risk assessments", "5 years", "Duty of care"),
    ("Visa and immigration records", "5 years", "Regulatory"),
    ("Incident and near-miss reports", "10 years", "Health and safety"),
    ("Data protection impact assessments", "10 years", "Privacy governance"),
    ("Supplier due diligence files", "10 years", "Anti-bribery"),
    ("Currency conversion worksheets", "7 years", "Tax reconciliation"),
    ("Training completion records", "5 years", "Compliance certification"),
    ("Asset register updates", "10 years", "IT asset lifecycle"),
    ("Sustainability travel data", "10 years", "Emissions reporting"),
    ("Dispute resolution notes", "7 years", "Audit trail"),
    ("Gift and hospitality registers", "10 years", "Anti-bribery"),
    ("Insurance claim files", "10 years", "Claims handling"),
    ("Expense audit samples", "7 years", "Quality assurance"),
]

APPROVAL_ORIENTATION = [
    ("Solo meal within cap", "None beyond submission", "Expense portal", "Ordinary review"),
    ("Hotel within cap", "None beyond submission", "Expense portal", "Ordinary review"),
    ("Taxi within threshold", "None beyond submission", "Expense portal", "Ordinary review"),
    ("Domestic flight", "Tier 1", "Practice Leader", "Booked via Travel Desk"),
    ("International flight", "Tier 2", "Practice Leader in writing", "Advance booking expected"),
    ("Team offsite", "Tier 2", "Department Director", "Cost agenda required"),
    ("Client hospitality above cap", "Tier 2", "Budget owner", "Figure 2 governs"),
    ("Event materials", "Tier 2", "Budget owner", "Event must be named"),
    ("Software request", "IT review", "IT Service Portal", "Never out of pocket"),
    ("Hardware above threshold", "IT review", "IT Helpdesk ticket", "Ticket number required"),
    ("Rental car above intermediate", "Tier 2", "Named approver", "Justification required"),
    ("Conference travel", "Tier 1", "Practice Leader", "Business relevance required"),
    ("Candidate interview meal", "Tier 1", "Hiring manager", "Role and candidates in note"),
    ("Extended assignment", "Tier 3", "Head of Global Finance", "Serviced apartment review"),
    ("Relocation support", "Tier 3", "People Operations", "Separate policy governs"),
]

OFFICES = [
    ("London", "Fenchurch Street", "EMEA", "Europe/London"),
    ("Berlin", "Friedrichstrasse", "EMEA", "Europe/Berlin"),
    ("Munich", "Maximilianstrasse", "EMEA", "Europe/Berlin"),
    ("Frankfurt", "Taunusanlage", "EMEA", "Europe/Berlin"),
    ("Hamburg", "Neuer Wall", "EMEA", "Europe/Berlin"),
    ("Düsseldorf", "Königsallee", "EMEA", "Europe/Berlin"),
    ("Zurich", "Bahnhofstrasse", "EMEA", "Europe/Zurich"),
    ("Geneva", "Rue du Rhône", "EMEA", "Europe/Zurich"),
    ("Paris", "Avenue des Champs-Élysées", "EMEA", "Europe/Paris"),
    ("Amsterdam", "Zuidas", "EMEA", "Europe/Amsterdam"),
    ("Brussels", "Avenue Louise", "EMEA", "Europe/Brussels"),
    ("Madrid", "Paseo de la Castellana", "EMEA", "Europe/Madrid"),
    ("Milan", "Via Montenapoleone", "EMEA", "Europe/Rome"),
    ("Rome", "Via Veneto", "EMEA", "Europe/Rome"),
    ("Vienna", "Ringstrasse", "EMEA", "Europe/Vienna"),
    ("Stockholm", "Stureplan", "EMEA", "Europe/Stockholm"),
    ("Copenhagen", "Kongens Nytorv", "EMEA", "Europe/Copenhagen"),
    ("Oslo", "Aker Brygge", "EMEA", "Europe/Oslo"),
    ("Helsinki", "Esplanadi", "EMEA", "Europe/Helsinki"),
    ("Dublin", "Grand Canal Dock", "EMEA", "Europe/Dublin"),
    ("Warsaw", "Rondo ONZ", "EMEA", "Europe/Warsaw"),
    ("Prague", "Prague 1", "EMEA", "Europe/Prague"),
    ("Budapest", "District V", "EMEA", "Europe/Budapest"),
    ("New York City", "Park Avenue", "Americas", "America/New_York"),
    ("Boston", "Seaport", "Americas", "America/New_York"),
    ("Chicago", "Wacker Drive", "Americas", "America/Chicago"),
    ("Seattle", "Union Street", "Americas", "America/Los_Angeles"),
    ("San Francisco", "Market Street", "Americas", "America/Los_Angeles"),
    ("Los Angeles", "Wilshire Boulevard", "Americas", "America/Los_Angeles"),
    ("Toronto", "Bay Street", "Americas", "America/Toronto"),
    ("Vancouver", "Burrard Street", "Americas", "America/Vancouver"),
    ("Mexico City", "Paseo de la Reforma", "Americas", "America/Mexico_City"),
    ("Sao Paulo", "Avenida Paulista", "Americas", "America/Sao_Paulo"),
    ("Buenos Aires", "Puerto Madero", "Americas", "America/Argentina/Buenos_Aires"),
    ("Tokyo", "Marunouchi", "Asia-Pacific", "Asia/Tokyo"),
    ("Singapore", "Marina Bay", "Asia-Pacific", "Asia/Singapore"),
    ("Hong Kong", "Central", "Asia-Pacific", "Asia/Hong_Kong"),
    ("Shanghai", "Lujiazui", "Asia-Pacific", "Asia/Shanghai"),
    ("Seoul", "Gangnam", "Asia-Pacific", "Asia/Seoul"),
    ("Mumbai", "Bandra Kurla Complex", "Asia-Pacific", "Asia/Kolkata"),
    ("Sydney", "Barangaroo", "Asia-Pacific", "Australia/Sydney"),
    ("Melbourne", "Collins Street", "Asia-Pacific", "Australia/Melbourne"),
    ("Auckland", "Britomart", "Asia-Pacific", "Pacific/Auckland"),
    ("Dubai", "DIFC", "Middle East", "Asia/Dubai"),
    ("Abu Dhabi", "Al Maryah Island", "Middle East", "Asia/Dubai"),
    ("Riyadh", "King Fahd Road", "Middle East", "Asia/Riyadh"),
    ("Johannesburg", "Sandton", "Africa", "Africa/Johannesburg"),
    ("Nairobi", "Westlands", "Africa", "Africa/Nairobi"),
]

REGIONAL_ADDENDA = [
    ("EMEA", "Local public holidays follow the destination country, not the home office."),
    ("EMEA", "VAT registration numbers are required on folios and commercial invoices."),
    ("EMEA", "Rail is the default for journeys under four hours within the region."),
    ("Americas", "Tip norms in the region follow the vendor country schedule."),
    ("Americas", "Sales tax is reimbursable when separately itemized."),
    ("Asia-Pacific", "Tipping is generally not customary; service charges printed on a bill are reimbursable."),
    ("Asia-Pacific", "Long-haul rest days follow the weekday and weekend logic in Chapter 9."),
    ("Middle East", "Friday and Saturday form the regional weekend; the weekend rules still follow the receipt date."),
    ("Africa", "Cash is preferred in some markets; withdraw from bank-affiliated ATMs only."),
    ("Cross-region", "Currency caps follow the receipt currency column in Chapter 14."),
]

MISCONCEPTIONS = [
    ("A suite is reimbursable if it is the only room left", "The nightly rate is capped by city tier regardless of room name.", "6"),
    ("City tax counts against the nightly cap", "Mandatory city tax is reimbursed in full and sits outside the cap.", "6"),
    ("The cap includes VAT added on top", "The cap applies to the room rate; VAT on the excess is deducted with it.", "6"),
    ("Laundry is always reimbursable on a long stay", "It is capped per seven-day period and deducted above the cap.", "6"),
    ("A short-stay laundry line is fine with a receipt", "It needs a note describing the soiling incident.", "6"),
    ("Hotel parking is always covered", "It is capped per night and needs a named rental or pool vehicle.", "6"),
    ("A loyalty upgrade changes the reimbursement", "The folio rate governs, not the room category booked or granted.", "6"),
    ("Solo meals can include a glass of wine", "Alcohol during solo dining is deducted in full.", "7"),
    ("A mocktail is treated as alcohol", "Non-alcoholic drinks are ordinary beverages.", "7"),
    ("Unspent lunch allowance rolls into dinner", "Allowances do not roll over; the dinner cap is unchanged.", "7"),
    ("Tips are reimbursed in full", "Tips are capped by the vendor country's norm.", "7"),
    ("Takeaway tips are reimbursable in Europe", "Takeaway, counter, and delivery tips are not reimbursable in Europe.", "7"),
    ("Truffle oil is only a flavour", "Truffle oil is screened under Figure 3.", "13"),
    ("Caviar follows the truffle rule", "Caviar is governed by ordinary caps only.", "7"),
    ("Any receipt dated on a weekend is rejected", "Weekend claims are evaluated under Figure 1.", "13"),
    ("An early Monday meeting always covers a Sunday night", "Figure 1 governs the branch.", "13"),
    ("A flight on a Saturday is a weekend expense", "Flights follow Chapters 4 and 5; lodging and meals on that day follow Figure 1.", "9"),
    ("Bleisure nights are always covered", "Personal extension nights are the employee's cost.", "9"),
    ("Companion meals split the cap", "Companions are excluded from the count and their share is deducted.", "9"),
    ("A bigger room for a companion is covered", "Double-occupancy surcharges are deducted.", "9"),
    ("Group meals without a note use the group caps", "A group bill lacking purpose or headcount is evaluated as a solo meal.", "8"),
    ("Candidate meals are not hospitality", "Recruiting meals are client hospitality.", "8"),
    ("Any client venue is acceptable", "Night clubs, casinos, and similar venues are rejected in full.", "8"),
    ("VIP boxes are fine for client events", "Only standard seating tiers are reimbursable.", "8"),
    ("Internal team meals are uncapped", "They follow the Figure 2 per-person cap.", "13"),
    ("A taxi is covered whenever it is faster", "A fare above the threshold needs a stated justification.", "5"),
    ("Rideshare premium tiers are covered", "The excess over the threshold is deducted.", "5"),
    ("First class rail is always fine if it is cheaper", "First class is permitted only over four hours.", "5"),
    ("A rental car upgrade is a small matter", "Above intermediate it needs a named approver.", "5"),
    ("Commuting to the office is mileage", "Commuting is a personal expense.", "11"),
    ("Parking fines can be claimed when unavoidable", "Fines and citations are always deducted.", "11"),
    ("Business class is fine on any long flight", "It applies only when Chapter 4 permits it.", "4"),
    ("Seat selection is a travel necessity", "Seat selection and extra legroom are deducted.", "4"),
    ("Lounge access is reimbursable on late flights", "Lounge access is deducted.", "4"),
    ("Government taxes can be excluded", "Mandatory taxes and surcharges are reimbursable in full.", "4"),
    ("A change fee is always personal", "Business-necessary change fees are reimbursable.", "4"),
    ("Software can be bought out of pocket", "Software is deducted; use the IT portal.", "10"),
    ("Cloud credits are a routine expense", "Cloud credits are deducted.", "10"),
    ("An external monitor is a normal peripheral", "It needs an IT ticket number at or above the threshold.", "10"),
    ("Plants are reimbursable for a client event", "Only temporary staging greenery for a named, pre-approved event is.", "10"),
    ("Office furniture is reimbursable with approval", "Furniture is deducted regardless of approval.", "10"),
    ("Gift cards are a convenient thank-you", "Gift cards and vouchers are deducted.", "11"),
    ("Personal clothing is covered if a bag is lost", "Only with a PIR reference and within the emergency cap.", "11"),
    ("Sunscreen is a travel necessity", "Personal care items are deducted.", "11"),
    ("Pet fees at a hotel are incidental", "Pet charges are deducted.", "6"),
    ("Foreign cash can be bought back", "Unspent foreign currency is not reimbursable.", "12"),
    ("Accepting card-terminal home currency is harmless", "The markup is not reimbursed; pay in local currency.", "12"),
    ("A folio without a VAT number is rejected entirely", "It is reimbursed net of the VAT shown.", "12"),
    ("A commercial invoice is exempt from VAT numbering", "It must show the vendor's VAT number.", "12"),
    ("Restaurant receipts need a VAT number", "Restaurant, taxi, and fuel receipts are exempt from that requirement.", "12"),
    ("Email approval is never acceptable", "Written pre-approval by email is acceptable where required.", "3"),
    ("Verbal approval from a partner suffices", "Visual standards and written approvals govern.", "8"),
    ("An event surcharge cap applies to the whole stay", "It applies only to nights inside the event window.", "9"),
    ("Naming the event is optional", "The note must name the listed event for the override to apply.", "9"),
    ("The prior year's rates still apply", "Version 4.2 governs claims processed from January 1, 2024.", "16"),
    ("The draft 2025 rates are live", "Draft proposals are not effective.", "17"),
]

COMMON_AUDIT_FINDINGS = [
    ("Missing vendor VAT registration number", "Vendor was not asked", "Reimburse net of VAT; coach the employee", "12"),
    ("Summary card slip attached", "Original itemized bill lost", "Request the itemized bill; otherwise reject the line", "2"),
    ("Unnamed rental vehicle on parking", "Note was brief", "Deduct the parking line", "6"),
    ("Laundry without a soiling note", "Incident not described", "Deduct the laundry line", "6"),
    ("Minibar item left on the folio", "Employee did not review the folio", "Deduct the incidental and its VAT", "6"),
    ("Tip above the country cap", "Copying a home-country habit", "Deduct the excess", "7"),
    ("Alcohol on a solo meal", "Receipt not trimmed", "Deduct each alcohol line", "7"),
    ("Alcohol above the hospitality allowance", "Wine list guided by the host", "Deduct the excess proportionally", "13"),
    ("Missing attendee count", "Note written from memory", "Evaluate as a solo meal", "8"),
    ("Missing external organization", "Note written in a hurry", "Evaluate as a solo meal", "8"),
    ("Weekend branch not evidenced", "Note omitted the facts", "Apply the non-reimbursable branch", "13"),
    ("Event name absent for an event cap", "Employee assumed the city was enough", "Apply the ordinary city cap", "9"),
    ("Truffle line not screened", "Reviewer skipped Figure 3", "Screen the line and adjust", "13"),
    ("First class rail under four hours", "Ticket booked by a travel agent", "Deduct the fare", "5"),
    ("Business class on a short segment", "Cabin chosen automatically", "Deduct the fare", "4"),
    ("Premium rideshare tier", "App defaulted to premium", "Deduct the excess", "5"),
    ("Rental above intermediate", "Only large cars available", "Request a named approver or deduct the excess", "5"),
    ("Software bought out of pocket", "Urgent licence need", "Deduct the line; route to IT", "10"),
    ("Peripheral without an IT ticket", "Purchase made on the road", "Deduct the line", "10"),
    ("Gift card in an event invoice", "Bundled giveaways", "Deduct the gift card lines", "11"),
    ("Personal charge on a corporate card", "Card mixing", "Deduct and flag for repayment", "11"),
    ("Duplicate submission", "Portal retry", "Reject the duplicate", "2"),
    ("Foreign receipt claimed in EUR", "Manual conversion", "Enter the printed currency", "12"),
    ("Personal extension night claimed", "Trip extended privately", "Deduct the night", "9"),
    ("Companion meal counted in the headcount", "Host added the guest", "Reduce the headcount and deduct the share", "9"),
    ("Commuting fare claimed as a taxi", "Office trip after hours", "Deduct the fare", "11"),
    ("Parking fine included in a garage receipt", "Fine paid at the machine", "Deduct the fine", "11"),
    ("Lounge pass on a delayed flight", "Delay felt exceptional", "Deduct the pass", "4"),
    ("Seat selection on a long-haul flight", "Comfort on an overnight", "Deduct the seat fee", "4"),
    ("Non-itemized hotel rate", "Express checkout", "Request the folio; otherwise hold the claim", "6"),
    ("City tax omitted from the claim", "Employee assumed it was included", "Add the city tax if itemized", "6"),
    ("Daily aggregate exceeded", "Multiple small receipts", "Deduct the excess over the aggregate", "7"),
    ("Overtime meal without a late-work note", "Takeaway at home", "Deduct the meal", "7"),
    ("Candidate meal without a role", "Interview ran late", "Add the role or evaluate as a solo meal", "8"),
    ("Theater tickets in a luxury tier", "Only premium seats left", "Deduct the excess over standard seating", "8"),
    ("Invoice addressed to a client", "Vendor default billing", "Acceptable if the employee paid", "10"),
    ("Mileage log lacking addresses", "Route remembered", "Request the addresses", "5"),
    ("Fuel receipt without a vehicle", "Pool car unnamed", "Deduct the fuel line", "5"),
    ("Baggage fee without a reason", "Extra suitcase", "Deduct unless business-necessary", "4"),
    ("VAT number present but net not shown", "Invoice template", "Request a corrected invoice", "12"),
    ("Dynamic currency conversion markup", "Terminal default", "Reimburse the local-currency amount only", "12"),
    ("Expense older than thirty days", "Late submission", "Route for a waiver before processing", "2"),
    ("Signature missing on a paper claim", "Digitization skipped", "Return for signature", "2"),
    ("Approver outside the DoA tier", "Delegation not updated", "Escalate to the correct tier", "3"),
    ("Event materials without a budget owner", "Pre-approval assumed", "Deduct the event material lines", "10"),
    ("Booth greenery treated as furniture", "Reviewer applied the general exclusion", "Reclassify as staging greenery", "10"),
    ("Office plant rental in an event invoice", "Mixed invoice", "Deduct the recurring plant line", "10"),
    ("Streaming subscription on a travel card", "Personal account", "Deduct the line", "11"),
    ("Medicine bought while traveling", "Headache tablets", "Deduct the line", "11"),
    ("Clothing after a delayed bag", "Convenience purchase", "Require the PIR reference", "11"),
    ("Foreign cash advance claimed", "Leftover currency", "Reject the item", "12"),
]

FAQ_EXTENDED = [
    ("Can I book a hotel outside the portal?", "Yes, but the same caps apply.", "6"),
    ("Do I need to keep paper receipts?", "Electronic copies are accepted if legible and complete.", "2"),
    ("What if the folio is several pages?", "Upload every page in sequence.", "2"),
    ("Is breakfast at the hotel reimbursable?", "Up to the breakfast cap when itemized.", "7"),
    ("Is a hotel restaurant dinner a meal?", "Yes, it counts toward the day's meal caps.", "6"),
    ("Can I claim a hotel minibar water?", "No, minibar charges are deducted.", "6"),
    ("Is the city tax capped?", "No, mandatory city tax is reimbursed in full.", "6"),
    ("Can I keep loyalty points?", "Yes, keep the points; the folio rate still governs.", "6"),
    ("Is valet parking reimbursable?", "It is capped per night with a named rental or pool vehicle.", "6"),
    ("Can I launder a suit on a three-night stay?", "Only as a garment rescue with a soiling note.", "6"),
    ("Is a coffee between meetings reimbursable?", "Yes, within the daily aggregate.", "7"),
    ("Can I exceed one meal cap by underspending another?", "No, caps are not transferable.", "7"),
    ("Are tips on takeaway reimbursable?", "Not in Europe.", "7"),
    ("Is a service charge the same as a tip?", "A printed service charge is reimbursed; extra tip is capped.", "7"),
    ("Does truffle oil trigger the flowchart?", "Yes, it is listed explicitly.", "13"),
    ("Is caviar screened by Figure 3?", "No, ordinary caps govern.", "7"),
    ("Can I host a client at a sporting event?", "Yes, in standard seating tiers.", "8"),
    ("Can I host a client at a casino?", "No, the bill is rejected in full.", "8"),
    ("Is a candidate meal client hospitality?", "Yes, state the role and candidates.", "8"),
    ("What if the client orders expensive wine?", "The alcohol allowance still applies.", "13"),
    ("Is a team dinner capped?", "Yes, per person under Figure 2.", "13"),
    ("Does a team activity follow the meal cap?", "No, it has its own per-participant cap.", "10"),
    ("Can I expense an escape room?", "Yes, within the team-building cap.", "10"),
    ("Are booth giveaways reimbursable?", "Yes, for a named, pre-approved event.", "10"),
    ("Are rubber ducks an event material?", "If bought for a named, pre-approved event.", "10"),
    ("Can I buy a laptop out of pocket?", "No, IT issues laptops.", "10"),
    ("Can I buy a monitor while traveling?", "Only with an IT ticket number.", "10"),
    ("Is a subscription to a legal journal reimbursable?", "No, use the library service.", "10"),
    ("Can I expense a book for a matter?", "Yes, up to the per-item cap with the matter cited.", "10"),
    ("Is a courier of client documents reimbursable?", "Yes, state what was shipped.", "10"),
    ("Is a travel eSIM reimbursable?", "Yes, up to the trip cap.", "10"),
    ("Can I take a taxi instead of the train?", "Yes, but the fare threshold and justification apply.", "5"),
    ("Is a premium rideshare reimbursable?", "Only up to the threshold.", "5"),
    ("Is a first class rail ticket reimbursable?", "Only for journeys over four hours.", "5"),
    ("Do I need a rental car justification?", "Yes, note the client sites served.", "5"),
    ("Is a collision damage waiver reimbursable?", "Yes, when booked through the corporate channel.", "5"),
    ("Can I claim mileage for commuting?", "No, commuting is personal.", "11"),
    ("Are tolls and congestion charges reimbursable?", "Yes, with the receipt.", "5"),
    ("Is a parking fine reimbursable?", "No, citations are always deducted.", "11"),
    ("Can I fly business on a six-hour flight?", "Only if the segment meets the Chapter 4 conditions.", "4"),
    ("Are government flight taxes reimbursable?", "Yes, in full.", "4"),
    ("Is seat selection reimbursable?", "No.", "4"),
    ("Is a lounge pass reimbursable?", "No.", "4"),
    ("Can I claim a flight change fee?", "Yes, when business-necessary.", "4"),
    ("Is a weekend hotel night covered?", "Follow Figure 1.", "13"),
    ("Is a Sunday taxi covered?", "Follow Figure 1.", "13"),
    ("Can I extend a trip for a holiday?", "Yes, at your own cost.", "9"),
    ("Does my partner's meal count in the headcount?", "No, exclude companions and deduct their share.", "9"),
    ("Is a rest day after a long flight covered?", "Weekday nights follow Chapter 6; weekend nights follow Figure 1.", "9"),
    ("Do I use my home country's holidays?", "Use the destination country's holidays.", "9"),
    ("Does an event cap cover the whole week?", "Only nights inside the event window.", "9"),
    ("Can I claim a gift card for a client?", "No, gift cards are deducted.", "11"),
    ("Is a hotel spa charge reimbursable?", "No.", "6"),
    ("Is a gym day pass reimbursable?", "No.", "11"),
    ("Is personal clothing reimbursable?", "Only after a lost bag with a PIR reference.", "11"),
    ("Is sunscreen reimbursable?", "No.", "11"),
    ("Is pet boarding reimbursable?", "No.", "11"),
    ("Is childcare during travel reimbursable?", "No.", "11"),
    ("Can I claim leftover foreign cash?", "No.", "12"),
    ("Which currency do I claim?", "The currency printed on the receipt.", "12"),
    ("Do I convert caps myself?", "No, Finance converts using the ECB rate.", "12"),
    ("Is a folio without a VAT number rejected?", "No, it is reimbursed net of VAT.", "12"),
    ("Do restaurant receipts need a VAT number?", "No.", "12"),
    ("Is dynamic currency conversion reimbursable?", "The markup is not.", "12"),
    ("Who approves an international flight?", "The Practice Leader in writing.", "3"),
    ("Is email pre-approval valid?", "Yes, where written pre-approval is required.", "3"),
    ("Can my manager approve above their tier?", "No, the DoA tier governs.", "3"),
    ("How late can I submit a claim?", "Within thirty calendar days of transaction completion.", "2"),
    ("What if I submit late?", "Request a waiver before processing.", "2"),
    ("What if I lose a receipt?", "Provide a duplicate merchant copy where possible.", "2"),
    ("Are card slips acceptable?", "Not as the sole proof of a business meal.", "2"),
    ("Do I need the original folio?", "A complete electronic copy is acceptable.", "2"),
    ("Are prior-year rates still valid?", "Version 4.2 governs claims processed from January 1, 2024.", "16"),
    ("Are the 2025 draft rates live?", "No, drafts are not effective.", "17"),
    ("Where is the current rate table?", "Chapters 6, 7, and 14 are authoritative.", "14"),
    ("What is the order of precedence?", "Event override, then Chapter 14, then prose chapters, then orientation tables.", "15"),
]


def typst_table(
    columns: tuple[str, ...],
    header: tuple[str, ...],
    rows: list[tuple[str, ...]],
    aligns: tuple[str, ...] | None = None,
) -> str:
    """Render one Typst table with the handbook's shared styling."""
    lines = ["#table("]
    lines.append("  columns: (" + ", ".join(columns) + "),")
    if aligns:
        lines.append("  align: (" + ", ".join(aligns) + "),")
    lines.append("  " + HEADER_FILL + ",")
    lines.append('  stroke: 0.5pt + rgb("#cbd5e1"),')
    lines.append("  table.header" + "".join(f"[*{cell}*]" for cell in header) + ",")
    for row in rows:
        lines.append("  " + "".join(f"[{cell}], " for cell in row))
    lines.append(")")
    return "\n".join(lines)


def city_rows() -> list[tuple[str, ...]]:
    """One orientation row per city. Values live only in Chapter 14."""
    return [
        (city, CITY_COUNTRY[city], tier, "Chapter 14 binds")
        for tier in ("Tier 1", "Tier 2", "Tier 3")
        for city in city_list(tier)
    ]


def city_list(tier: str) -> list[str]:
    """Cities of one tier, in the generator's canonical order."""
    return [row[0] for row in lodging_rows_source() if city_tier(row[0]) == tier]


def city_tier(city: str) -> str:
    if city in TIER_1:
        return "Tier 1"
    if city in TIER_2:
        return "Tier 2"
    return "Tier 3"


def lodging_rows_source() -> list[tuple[str, str, str]]:
    """(city, country, tier) for every listed market, tiers in order."""
    rows = []
    for tier, cities in (("Tier 1", TIER_1), ("Tier 2", TIER_2), ("Tier 3", TIER_3)):
        rows += [(city, CITY_COUNTRY[city], tier) for city in cities]
    return rows


def lodging_rows() -> list[tuple[str, ...]]:
    """One governing row per city, with the tier's cap in three currencies."""
    rows = []
    for city, country, tier in lodging_rows_source():
        eur, usd, gbp = TIER_CAPS[tier]
        rows.append((city, country, tier, eur, usd, gbp))
    return rows


def lodging_bullets() -> str:
    """Per-market cap schedule as bullets: one line per market in extraction."""
    lines = []
    for tier in ("Tier 1", "Tier 2", "Tier 3"):
        lines.append(f"=== {tier} markets")
        lines.append("")
        for city, country, row_tier in lodging_rows_source():
            if row_tier != tier:
                continue
            eur, usd, gbp = TIER_CAPS[tier]
            lines.append(f"- {city} ({country}, {tier}): nightly room rate cap {eur} / {usd} / {gbp}.")
        lines.append("")
    return "\n".join(lines)


def country_rows() -> list[tuple[str, ...]]:
    rows = []
    rows += [(country, "—", "Chapter 14 binds", "—") for country in TIP_20]
    rows += [(country, "—", "Chapter 14 binds", "—") for country in TIP_125]
    rows += [(country, "—", "Chapter 14 binds", "—") for country in TIP_10]
    rows += [(country, "—", "Chapter 14 binds", "—") for country in TIP_0]
    rows += [(country, region, "Chapter 14 binds", currency) for country, region, currency in OTHER_COUNTRIES]
    return rows


def tip_rows() -> list[tuple[str, ...]]:
    """One governing tip row per country, expanding the former regional rows."""
    rows = [
        ("United States", "Tip cap", "20%", "Table service and taxis. Counter service, takeout, and delivery: \\$1.00 maximum"),
        ("Canada", "Tip cap", "20%", "Table service and taxis. Counter service, takeout, and delivery: \\$1.00 maximum"),
        ("United Kingdom", "Tip cap", "12.5%", "Only if no service charge is printed on the bill; printed service charge is reimbursed, extra tip deducted"),
        ("Germany", "Tip cap", "20%", "Generous rounding for good service is customary and fully supported; takeaway and delivery: no tip reimbursed"),
    ]
    for country in TIP_10:
        if country == "Switzerland":
            rows.append((country, "Tip cap", "10%", "Service included; rounding up is customary"))
        else:
            rows.append((country, "Tip cap", "10%", "Service included by law; takeaway and delivery: no tip reimbursed"))
    for country in TIP_0:
        rows.append((country, "Tip cap", "0%", "Tipping is not customary; any tip deducted; a printed service charge is reimbursed"))
    rows.append(("All other countries", "Tip cap", "—", "The regional norms in Chapter 7 govern"))
    return rows


def small(table: str) -> str:
    """Render a table at 8pt so wide rows stay on one extracted line."""
    return "#text(8pt)[\n" + table + "\n]"


def write_appendix_tables() -> None:
    """Write chapter 14, the governing appendix, with one row per market."""
    lodging = lodging_bullets()
    tipping = typst_table(
        ("1.3fr", "0.9fr", "0.9fr", "3fr"),
        ("Country", "Cap Type", "Maximum Tip", "Policy Guidance"),
        tip_rows(),
        ("left", "center", "center", "left"),
    )
    incidental = typst_table(
        ("1.6fr", "1fr", "1fr", "1fr", "2fr"),
        ("Folio Line", "EUR (€)", "USD (\\$)", "GBP (£)", "Condition"),
        [
            ("Laundry, stay over 5 nights (folio line cap)", "€35.00 / 7 days", "\\$40.00 / 7 days", "£30.00 / 7 days", "None"),
            ("Garment rescue, 5 nights or fewer (folio line cap)", "€25.00 / stay", "\\$30.00 / stay", "£22.00 / stay", "Note describes the soiling incident"),
            ("Parking incl. valet and EV charging (folio line cap)", "€30.00 / night", "\\$35.00 / night", "£26.00 / night", "Note identifies rental or pool vehicle"),
            ("City tax, tourism levy (reimbursed in full)", "Full", "Full", "Full", "Itemized on folio"),
            ("Minibar, spa, movies, pet fee, gym (always deducted)", "€0.00", "\\$0.00", "£0.00", "Always deducted"),
        ],
        ("left", "center", "center", "center", "left"),
    )
    meals = typst_table(
        ("1.5fr", "1fr", "1fr", "1fr", "2fr"),
        ("Meal Category", "EUR (€)", "USD (\\$)", "GBP (£)", "Receipt Time"),
        [
            ("Breakfast (solo cap)", "€15.00", "\\$18.00", "£13.00", "Before 11:00"),
            ("Lunch (solo cap)", "€25.00", "\\$30.00", "£22.00", "11:00 to 15:59"),
            ("Dinner (solo cap)", "€45.00", "\\$55.00", "£38.00", "16:00 onward"),
            ("Overtime meal at home office (solo cap)", "€20.00", "\\$25.00", "£18.00", "After 20:30, note states late work"),
            ("*Daily Aggregate Cap* (solo cap)", "*€85.00*", "*\\$100.00*", "*£73.00*", "Maximum cumulative reimbursement per calendar day"),
        ],
        ("left", "center", "center", "center", "left"),
    )
    mileage = typst_table(
        ("1.5fr", "1.2fr", "2fr"),
        ("Country / Jurisdiction", "Statutory Rate", "Required Documentation"),
        [
            ("European Union (Standard)", "€0.38 / km", "Departure and arrival addresses, verified map distance"),
            ("United States (IRS Benchmark)", "\\$0.67 / mile", "Itemized mileage log with client project citation"),
            ("United Kingdom (HMRC Tier 1)", "£0.45 / mile", "First 10,000 business miles in tax year"),
            ("United Kingdom (HMRC Tier 2)", "£0.25 / mile", "Excess business miles above 10,000 miles"),
            ("Bicycle Allowance (All regions)", "€0.25 / km", "Business visits under 20km round-trip"),
            ("Rental or pool vehicle fuel", "Actual receipt", "Fuel line only; shop items deducted; note names the rental"),
        ],
        ("left", "center", "left"),
    )
    content = f"""#import "template.typ": card-do, card-dont

= Appendix: Reference Tables and Global Schedules

== Global Hotel Nightly Room Rate Caps

The following caps apply to the nightly room rate as printed on the folio, exclusive of municipal tourism taxes and VAT added on top. The hotel's city determines the tier. One line is listed per market:

{lodging}

A city that is not listed above is a Tier 3 market: €120.00 / \\$140.00 / £105.00 per night.

During declared trade-fair and congress weeks, the event surcharge caps in Chapter 9 override these tier caps for the host city when the submission note names the listed event.

== Hotel Incidental Allowances

{incidental}

== Daily Meal Allowances and Spending Limits (Solo Dining)

Meal limits are based on actual, itemized receipts up to the stated maximum caps. The receipt time selects the category:

{meals}

Group dining caps (internal team meals and client hospitality) are set exclusively in Figure 2, Chapter 13.

== Personal Vehicle Mileage Rates

{mileage}

== Global Tipping and Gratuity Standards

The cap is calculated on the bill before tip. It applies to restaurants and taxis alike. The vendor's country governs. One row is listed per country. Where a country-specific row below differs from the regional norms in Chapter 7, the row below governs.

{tipping}

== Pre-Submission Compliance Checklist

Before clicking submit in the Noice & Toit Expense Portal, verify the following items:
- [ ] Every receipt is itemized. No summary credit card terminal slips are used as sole proof of spend.
- [ ] Hotel folios and commercial invoices show the vendor's VAT registration number.
- [ ] The note states the facts this handbook requires for the receipt type (Chapter 2).
- [ ] Solo meals contain zero alcoholic beverages, or you have deducted them yourself.
- [ ] Group meals state the business purpose, the external organization, and the attendee count.
- [ ] Tips are within the local cap in the table above.
- [ ] Any truffle dish passes Figure 3 (Chapter 13).
- [ ] Weekend or public holiday receipts and hotel nights comply with Figure 1 (Chapter 13).
- [ ] Group dining complies with Figure 2 (Chapter 13).
- [ ] Minibar, spa, movie, and pet charges have been deducted from hotel folios.
- [ ] Fuel receipts name the rental vehicle; shop items are deducted.
- [ ] Event materials name the event and the pre-approving budget owner.
- [ ] The claim is submitted within thirty (30) calendar days of transaction completion.

== Global Finance Directory and Contact Information

For inquiries regarding travel bookings, card management, or expense auditing:
- *Global Travel Desk*: `travel@noiceandtoit.internal` (24/7 emergency flight changes and duty of care support).
- *Expense Auditing Team*: `expenses@noiceandtoit.internal` (receipt verification and policy clarifications).
- *Corporate Card Administration*: `corporatecards@noiceandtoit.internal` (card issuance, limits, and lost cards).
- *Accounts Payable / Disbursements*: `finance-disbursements@noiceandtoit.internal` (payroll payout schedules).
- *Truffle Hotline*: `truffles@noiceandtoit.internal` (yes, really; see Chapter 13).
"""
    (HANDBOOK_DIR / "14-appendix-tables.typ").write_text(content, encoding="utf-8")



def write_reference_schedules() -> None:
    content = f"""#import "template.typ": card-do, card-dont

= Extended Reference Schedules and Indices

This chapter gathers orientation tables that employees and reviewers use to navigate the handbook. It is a finding aid, not a fresh source of rules.

#card-dont("Treat these orientation tables as binding")[
  Every table in this chapter summarizes material stated elsewhere. Where a table here is incomplete, out of date, or differs in any way from Chapter 6, Chapter 7, Chapter 9, or the Appendix of Chapter 14, those authoritative chapters govern. Version 4.2 governs every claim processed on or after January 1, 2024, regardless of the date printed on a receipt.
]

== Metropolitan Market Tier Index

{typst_table(("1.4fr", "1.4fr", "1fr", "1.4fr"), ("Metropolitan Market", "Country", "Assigned Tier", "Binding Schedule"), city_rows(), ("left", "left", "center", "center"))}

== Country, Region, and Currency Orientation

{typst_table(("1.6fr", "1.2fr", "1.6fr", "1fr"), ("Country", "Region", "Tipping Status", "Currency"), country_rows(), ("left", "left", "center", "center"))}

== Master Item Keyword Index

This index maps receipt wording to the chapter that governs it. It records where a rule lives, not what the rule decides; the governing chapter always supplies the conditions.

{typst_table(("2.2fr", "1.2fr", "2.6fr", "1fr"), ("Item or Keyword", "Category", "Governing Reference", "Chapter"), [(item, category, f"Chapter {chapter} governs", chapter) for item, category, _treatment, chapter in ITEM_TREATMENTS], ("left", "left", "left", "center"))}

== Terminology

{typst_table(("1.4fr", "4fr", "1.6fr"), ("Term", "Meaning", "Status"), [(term, meaning, "Governing chapter binds") for term, meaning in GLOSSARY], ("left", "left", "left"))}

== Reimbursement Calculation Order (Summary)

+ Confirm the receipt is itemized and complete.
+ Deduct non-reimbursable lines at their gross price, together with the tax on those lines.
+ Screen any truffle line under Figure 3.
+ Apply the relevant meal, lodging, or activity cap.
+ Apply the tip cap for the vendor country.
+ Reimburse the remainder, subject to the decision framework in Chapter 2.

== Reading the Schedules in Order

+ A named-event override in Chapter 9 beats the ordinary city tier.
+ A country row in Chapter 14 beats a regional tipping norm in Chapter 7.
+ A section of prose in Chapters 4 to 11 beats any orientation table in this chapter.
+ The historical schedules in Chapter 16 and the draft proposals in Chapter 17 are never effective for a current claim.
"""
    (HANDBOOK_DIR / "15-reference-schedules.typ").write_text(content, encoding="utf-8")


def write_historical_schedules() -> None:
    status = "Superseded — never payable"
    hotel_2023 = typst_table(("1.2fr", "1fr", "1.1fr", "1.6fr"), ("Tier", "Markets", "Superseded EUR Cap", "Status"), [
        ("Tier 1", "Tier 1 markets as listed in the current edition", "€200.00", status),
        ("Tier 2", "Tier 2 markets as listed in the current edition", "€145.00", status),
        ("Tier 3", "All other markets", "€110.00", status),
    ], ("left", "left", "center", "left"))
    hotel_2022 = typst_table(("1.2fr", "1fr", "1.1fr", "1.6fr"), ("Tier", "Markets", "Superseded EUR Cap", "Status"), [
        ("Tier 1", "Tier 1 markets as listed in the prior edition", "€180.00", status),
        ("Tier 2", "Tier 2 markets as listed in the prior edition", "€130.00", status),
        ("Tier 3", "All other markets", "€95.00", status),
    ], ("left", "left", "center", "left"))
    meals_2023 = typst_table(("1.4fr", "1fr", "1fr", "1.6fr"), ("Meal Category", "Superseded EUR Cap", "Receipt Time", "Status"), [
        ("Breakfast", "€13.00", "Before 11:00", status),
        ("Lunch", "€22.00", "11:00 to 15:59", status),
        ("Dinner", "€40.00", "16:00 onward", status),
        ("Daily aggregate", "€75.00", "Per calendar day", status),
    ], ("left", "center", "left", "left"))
    tips_2022 = typst_table(("2fr", "1fr", "1.8fr"), ("Country or Region", "Superseded Maximum Tip", "Status"), [
        ("United States and Canada", "18%", status),
        ("United Kingdom", "10%", status),
        ("Continental Europe", "8%", status),
        ("Japan, South Korea, Singapore, Hong Kong", "0%", status),
    ], ("left", "center", "left"))
    change_log = typst_table(("1fr", "1.2fr", "3fr"), ("Version", "Effective Date", "Summary"), [
        ("2.0", "January 1, 2021", "First consolidated international edition."),
        ("3.0", "January 1, 2023", "Introduced the Truffle Policy and the event surcharge caps."),
        ("3.1", "July 1, 2023", "Raised the Tier 2 lodging cap and the daily meal aggregate."),
        ("4.0", "October 1, 2023", "Moved group dining rules into Figure 2."),
        ("4.2", "January 1, 2024", "Current edition. Confirms that the visual decision architecture is binding."),
    ], ("center", "left", "left"))

    content = f"""#import "template.typ": card-do, card-dont

= Historical Schedules (Superseded)

The tables in this chapter record rates, caps, and norms from earlier editions of this handbook. They are retained so that previously processed reimbursements can be audited and explained.

#card-dont("Apply a historical schedule to a current claim")[
  Nothing in this chapter is effective for a claim processed on or after January 1, 2024. Version 4.2 governs every claim processed on or after that date, regardless of the date printed on the receipt. When a historical table and a current chapter appear to disagree, the current chapter always governs.
]

== Version History

{change_log}

== Superseded Lodging Caps (Version 3.1)

Effective July 1, 2023 to December 31, 2023. Replaced by the caps in Chapter 6 and the Appendix of Chapter 14.

{hotel_2023}

== Superseded Lodging Caps (Version 3.0)

Effective January 1, 2023 to June 30, 2023. Replaced by the Version 3.1 caps above.

{hotel_2022}

== Superseded Meal Caps (Version 3.1)

Effective July 1, 2023 to December 31, 2023. Replaced by the caps in Chapter 7 and the Appendix of Chapter 14.

{meals_2023}

== Superseded Tipping Norms (Version 2.0)

Effective until December 31, 2022. Replaced by the country rows in Chapter 14.

{tips_2022}

== Withdrawn Allowances

The following allowances appeared in earlier editions and have been withdrawn. They are not reimbursable under Version 4.2:
- A flat daily incidental allowance of €20 with no receipt (withdrawn).
- A nightly hotel internet surcharge, now included in corporate rates (withdrawn).
- A fixed airport transfer allowance of €40 in Tier 1 cities (withdrawn).
- A per-mile bicycle allowance above the statutory rate (withdrawn).
- A weekend meal supplement of €15 (withdrawn).
- A monthly home-office electricity stipend (withdrawn).
"""
    (HANDBOOK_DIR / "16-historical-schedules.typ").write_text(content, encoding="utf-8")


def write_draft_proposals() -> None:
    content = f"""#import "template.typ": card-do, card-dont

= 2025 Policy Review: Draft Proposals (Not Effective)

The Global Finance and People Operations team circulates proposed changes for consultation each autumn. This chapter records the proposals that were on the table during the most recent review cycle.

#card-dont("Apply a draft proposal to a live claim")[
  Nothing in this chapter is effective. Draft proposals are illustrative only, are subject to change, and must never be used to evaluate a reimbursement. The current schedules in Chapters 6, 7, and 14 remain binding until a new version is published with a future effective date.
]

== Proposed Lodging Caps

{typst_table(("1.2fr", "1fr", "1.4fr"), ("Tier", "Draft EUR Cap", "Status"), [("Tier 1", "€240.00", "Draft — not effective"), ("Tier 2", "€175.00", "Draft — not effective"), ("Tier 3", "€130.00", "Draft — not effective")], ("center", "center", "left"))}

== Proposed Meal Caps

{typst_table(("1.4fr", "1fr", "1.2fr"), ("Meal Category", "Draft EUR Cap", "Status"), [("Breakfast", "€16.00", "Draft — not effective"), ("Lunch", "€27.00", "Draft — not effective"), ("Dinner", "€48.00", "Draft — not effective"), ("Daily aggregate", "€90.00", "Draft — not effective")], ("left", "center", "left"))}

== Proposed Tipping Norms

{typst_table(("2fr", "1fr", "1.4fr"), ("Country or Region", "Draft Maximum Tip", "Status"), [("North America", "20%", "Draft — not effective"), ("United Kingdom", "12.5%", "Draft — not effective"), ("Continental Europe", "10%", "Draft — not effective")], ("left", "center", "left"))}

== Proposals That Were Not Adopted

- Replacing per-item caps with a single annual travel budget (not adopted).
- Removing the event surcharge caps in favor of negotiated event rates (not adopted).
- Allowing first class rail on journeys over three hours instead of four (not adopted).
- Treating hotel loyalty points as taxable compensation (not adopted).
- Making the Truffle Policy apply to all luxury ingredients (not adopted).
- Introducing a flat per-diem cash allowance with no receipts (not adopted).
"""
    (HANDBOOK_DIR / "17-draft-2025-proposals.typ").write_text(content, encoding="utf-8")


def write_documentation_and_retention() -> None:
    content = f"""#import "template.typ": card-do, card-dont

= Documentation, Retention, and Approval Orientation

This chapter collects the paperwork expectations that surround a claim. It restates requirements from Chapters 2 and 3 and adds the retention schedule that Global Finance maintains for audit purposes.

#card-dont("Change a reimbursement rule with this chapter")[
  Nothing here sets or changes an amount, a cap, or an eligibility rule. Chapters 2 and 3 remain authoritative for documentation and approval.
]

== Documentation Requirements by Receipt Type

{typst_table(("1.5fr", "2.2fr", "2.2fr", "1.4fr"), ("Receipt Type", "Mandatory Elements", "Submission Note Must State", "Governing Reference"), [(a, b, c, f"Chapter {d} governs") for a, b, c, d in DOCUMENTATION_REQUIREMENTS], ("left", "left", "left", "center"))}

== Records Retention Schedule

Records are retained by Global Finance and are not the employee's responsibility, but employees may ask why a receipt is requested months after a claim.

{typst_table(("2.4fr", "1fr", "2fr"), ("Record", "Retention", "Purpose"), RETENTION_SCHEDULE, ("left", "center", "left"))}

== Approval Authority Orientation

This orientation table maps common purchases to the approval route. The Delegation of Authority in Chapter 3 governs; the route below is a finding aid only.

{typst_table(("2fr", "1.2fr", "1.4fr", "2fr"), ("Scenario", "Approval Tier", "Approver", "Notes"), [(scenario, tier, approver, "Chapter 3 governs") for scenario, tier, approver, _note in APPROVAL_ORIENTATION], ("left", "center", "left", "left"))}

== A Note on Paperwork Discipline

A complete claim is the fastest claim. The most common cause of a delayed reimbursement is not a disputed rule but a missing folio page, an unnamed rental vehicle, or a note that assumes the reviewer already knows the client. Employees who attach the itemized receipt and state the facts the handbook asks for rarely wait long for payment.
"""
    (HANDBOOK_DIR / "18-documentation-and-retention.typ").write_text(content, encoding="utf-8")


def write_audit_and_misconceptions() -> None:
    content = f"""#import "template.typ": card-do, card-dont

= Audit Findings and Common Misconceptions

Global Finance audits a rolling sample of claims each quarter. This chapter records the findings that recur and the misconceptions that cause them. Each row points to the chapter that actually governs.

#card-do("Use this chapter to self-review a claim")[
  Skim the misconception table before you submit. Finding a likely deduction yourself is faster than a query from the audit team.
]

== Common Audit Findings

{typst_table(("2.2fr", "1.6fr", "2.4fr", "1.4fr"), ("Finding", "Typical Cause", "Resolution", "Governing Reference"), [(a, b, c, f"Chapter {d} governs") for a, b, c, d in COMMON_AUDIT_FINDINGS], ("left", "left", "left", "center"))}

== Common Misconceptions

{typst_table(("2.4fr", "2.8fr", "1.4fr"), ("Common Belief", "Correct Position", "Governing Reference"), [(a, b, f"Chapter {c} governs") for a, b, c in MISCONCEPTIONS], ("left", "left", "center"))}

== Extended Questions and Answers

{typst_table(("2.8fr", "2.8fr", "1.4fr"), ("Question", "Short Answer", "Governing Reference"), [(a, b, f"Chapter {c} governs") for a, b, c in FAQ_EXTENDED], ("left", "left", "center"))}

== Escalation and Dispute Resolution

+ Raise the question with the Expense Auditing Team before resubmitting.
+ If the team and the employee still disagree, the claim is reviewed by the Head of Global Finance.
+ A final appeal may be made to the Audit Committee within thirty days.
+ The Audit Committee's written determination is recorded and becomes guidance for future claims.
"""
    (HANDBOOK_DIR / "19-audit-and-misconceptions.typ").write_text(content, encoding="utf-8")


def write_directories_and_addenda() -> None:
    content = f"""#import "template.typ": card-do, card-dont

= Global Offices, Directory, and Regional Addenda

Noice & Toit LLP supports employees across many offices. This chapter is a directory and a record of regional notes. It contains no reimbursement rules.

#card-do("Contact the right desk the first time")[
  Travel bookings and duty of care go to the Travel Desk. Receipt and policy questions go to the Expense Auditing Team. Card problems go to Corporate Card Administration.
]

== Global Office Directory

{typst_table(("1.4fr", "2fr", "1.2fr", "1.6fr"), ("City", "Office", "Region", "Time Zone"), OFFICES, ("left", "left", "left", "left"))}

== Regional Addenda

{typst_table(("1.2fr", "5fr"), ("Region", "Note"), REGIONAL_ADDENDA, ("left", "left"))}

== Contact Directory

- *Global Travel Desk*: `travel@noiceandtoit.internal`
- *Expense Auditing Team*: `expenses@noiceandtoit.internal`
- *Corporate Card Administration*: `corporatecards@noiceandtoit.internal`
- *Accounts Payable*: `finance-disbursements@noiceandtoit.internal`
- *People Operations*: `people@noiceandtoit.internal`
- *IT Service Portal*: `ithelp.noiceandtoit.internal`
- *Ethics and Conduct Committee*: `ethics@noiceandtoit.internal`
"""
    (HANDBOOK_DIR / "20-directories-and-addenda.typ").write_text(content, encoding="utf-8")


GOVERNANCE_SUBJECTS = [
    "Each practice group", "The Finance function", "Every approving manager",
    "The operations center", "Each regional office", "The Audit Committee",
    "Line managers", "The People Operations team", "IT operations",
    "The compliance office", "The partnership board", "Each department director",
    "The risk function", "The records team", "The facilities group",
    "Each engagement leader", "The quality review panel", "The information security office",
    "The supplier management team", "Each office administrator", "The training office",
    "The internal audit team", "The sustainability working group", "The legal function",
]

GOVERNANCE_VERBS = [
    "reviews", "maintains", "documents", "escalates", "reconciles", "oversees",
    "approves", "records", "tests", "reports on", "refreshes", "validates",
    "archives", "tracks", "challenges", "confirms", "summarizes", "updates",
]

GOVERNANCE_OBJECTS = [
    "its control environment", "the delegation register", "supplier performance",
    "open actions", "the risk register", "training completion", "access reviews",
    "incident logs", "spending variances", "service levels", "the exception log",
    "process notes", "the onboarding checklist", "supplier records",
    "the change calendar", "continuity plans", "the competence matrix",
    "assurance findings", "the issue register", "operating metrics",
    "the asset inventory", "retention decisions", "the escalation matrix",
    "regional variations", "the governance calendar", "conduct standards",
]

GOVERNANCE_QUALIFIERS = [
    "quarterly", "annually", "on a rolling basis", "before each engagement",
    "within ten business days", "at least twice a year", "when tolerances are exceeded",
    "as part of the close process", "at the start of each review cycle",
    "after any material incident", "on a risk-weighted basis", "monthly",
    "before signing off any commitment", "during the annual planning round",
]

GOVERNANCE_COMPLEMENTS = [
    "in line with regional guidance", "before the next review cycle",
    "and records the outcome", "with the findings logged centrally",
    "unless a documented exception applies", "and confirms the result in writing",
    "and assigns a named owner", "so that the record stays complete",
    "and reports the result to the board", "and keeps the register current",
    "and escalates unresolved items", "without exception",
]

GOVERNANCE_SECTIONS = [
    ("Accountability and Delegation", 50),
    ("Planning and Spending Discipline", 50),
    ("Supplier and Contract Management", 50),
    ("Information Security and Access", 50),
    ("Records, Privacy, and Retention", 50),
    ("Health, Safety, and Continuity", 50),
    ("Training and Competence", 50),
    ("Quality and Assurance", 50),
    ("Reporting and Escalation", 50),
    ("Change and Program Management", 50),
]


def governance_clauses() -> list[str]:
    """Compose generic governance clauses with a rotating grammar."""
    clauses: list[str] = []
    counters = [0, 0, 0, 0, 0]
    for _section, count in GOVERNANCE_SECTIONS:
        for _ in range(count):
            subject = GOVERNANCE_SUBJECTS[counters[0] % len(GOVERNANCE_SUBJECTS)]
            verb = GOVERNANCE_VERBS[counters[1] % len(GOVERNANCE_VERBS)]
            obj = GOVERNANCE_OBJECTS[counters[2] % len(GOVERNANCE_OBJECTS)]
            qualifier = GOVERNANCE_QUALIFIERS[counters[3] % len(GOVERNANCE_QUALIFIERS)]
            complement = GOVERNANCE_COMPLEMENTS[counters[4] % len(GOVERNANCE_COMPLEMENTS)]
            clauses.append(f"{subject} {verb} {obj} {qualifier} {complement}.")
            counters = [(value + 1) for value in counters]
    return clauses


def write_governance_procedures() -> None:
    sections = []
    clauses = governance_clauses()
    offset = 0
    for title, count in GOVERNANCE_SECTIONS:
        body = "\n".join(f"+ {clause}" for clause in clauses[offset : offset + count])
        sections.append(f"== {title}\n\n{body}")
        offset += count
    body = "\n\n".join(sections)
    content = f"""#import \"template.typ\": card-do, card-dont

= Governance and Operating Procedures

This chapter describes how the firm runs its internal control environment. It is background reading for reviewers and contains no reimbursement rules. Nothing here changes a cap, an approval tier, or an eligibility condition.

#card-dont(\"Look here for a reimbursement decision\")[
  The operating procedures in this chapter govern how teams plan, review, and report. Reimbursement questions are answered only by Chapters 4 through 14.
]

{body}
"""
    (HANDBOOK_DIR / "21-governance-procedures.typ").write_text(content, encoding="utf-8")


# Terms that retrieval queries for the eval cases contain (checked as
# substrings, like the stage-2 ranker). Orthogonal filler must not contain
# any of them, so search results stay clean while the full dump still reads
# every token.
BANNED_TERMS = [
    "cap", "tip", "fare", "taxi", "rate", "room", "night", "dinner", "lunch",
    "breakfast", "alcohol", "truffle", "guest", "client", "weekend",
    "entertainment", "vat", "receipt", "hotel", "berlin", "munich",
    "frankfurt", "hamburg", "amsterdam", "first", "class", "rail", "hour",
    "flight", "seat", "reservation", "baggage", "lounge", "diem", "threshold",
    "ticket", "peripheral", "monitor", "headset", "event", "surcharge",
    "fair", "tax", "gratuity", "meal", "lodg", "incidental", "minibar",
    "laundry", "parking", "mileage", "deduct", "reimburs", "claim",
    "expense", "policy", "budget", "travel", "city", "tier", "eur", "amount",
    "per ", "vendor", "invoice", "folio", "cabin", "suite", "expo",
    "summit", "approval", "pre",
]

ARCHIVE_GROUPS = [
    "Disputes & Recovery", "Payments Operations", "Records Office",
    "Workplace Services", "Learning & Development", "Network Operations",
    "Quality & Methods", "Programme Office", "Data Office", "Counsel",
    "Onboarding", "Security Operations", "Facilities", "Supplier Desk",
]

ARCHIVE_OUTCOMES = [
    "Closed in full", "Closed after second review", "Merged into a related file",
    "Forwarded to the next group", "Archived at the yearly review",
    "Withdrawn by the sender", "Closed at the sender's request",
]

ARCHIVE_REMARKS = [
    "All attachments were retained according to the group schedule.",
    "Resolved during the opening call; no follow-up was needed.",
    "The group lead signed off the same week.",
    "Two rounds of correspondence, then closure.",
    "No further action was needed.",
    "The file was consolidated with a related one.",
    "Confirmation was sent to the sender.",
    "The yearly review raised no findings.",
    "Handled by the usual route without escalation.",
    "The outcome was recorded the same day.",
    "A short summary was shared with the group.",
    "The underlying matter concluded shortly afterward.",
]

ARCHIVE_MONTHS = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
]


def archive_rows(count: int = 320) -> list[tuple[str, ...]]:
    """Compose neutral settlement rows with no retrieval vocabulary."""
    rows = []
    for index in range(count):
        record = f"REC-{2021 + index % 4}-{10000 + index * 7:05d}"
        opened = f"{ARCHIVE_MONTHS[index % 12]} {2 + index % 26}, {2021 + index % 4}"
        group = ARCHIVE_GROUPS[index % len(ARCHIVE_GROUPS)]
        outcome = ARCHIVE_OUTCOMES[index % len(ARCHIVE_OUTCOMES)]
        remark = ARCHIVE_REMARKS[index % len(ARCHIVE_REMARKS)]
        rows.append((record, opened, group, outcome, remark))
    return rows


def write_settlement_archive() -> None:
    """Write the settlement archive: orthogonal volume for the full dump."""
    intro = """#import "template.typ": card-do, card-dont

= Settlement Archive: Processed Files

The Records Office keeps a register of closed files from the groups below. Each row records when the file was opened, which group owned it, how it ended, and one line of context. The register exists so that a past decision can be traced years later; it plays no part in evaluating anything submitted today.

#card-dont("Search this register for guidance")[
  Rows in this register describe work that has already ended. Current rules live elsewhere in this handbook, and nothing in this register extends, shortens, or overrides them.
]
"""
    sections = []
    rows = archive_rows()
    chunk = 80
    for section_index in range(0, len(rows), chunk):
        table = typst_table(
            ("1.3fr", "1.3fr", "1.5fr", "1.7fr", "2.6fr"),
            ("Record", "Opened", "Group", "Outcome", "Remark"),
            rows[section_index : section_index + chunk],
            ("left", "left", "left", "left", "left"),
        )
        first = section_index + 1
        last = section_index + len(rows[section_index : section_index + chunk])
        sections.append(f"== Files {first:04d} to {last:04d}\n\n{table}")
    body = "\n\n".join(sections)
    closing = """

== Disposal

Files in this register move to deep storage after the group schedule ends. Deep storage is indexed by record number only, and retrieval from deep storage takes the Records Office up to ten working days. Questions about the register go to the Records Office."""
    (HANDBOOK_DIR / "22-settlement-archive.typ").write_text(intro + body + closing, encoding="utf-8")


def check_orthogonal() -> None:
    """Fail if the keyword-orthogonal bodies drifted into retrieval vocabulary.

    Checks the generated clause and register text only. Chapter intros and
    callout cards are exempt on purpose: they are the self-labels that defer
    to the governing chapters.
    """
    bodies = [clause for clause in governance_clauses()]
    bodies += [" ".join(row) for row in archive_rows()]
    bodies += [title for title, _count in GOVERNANCE_SECTIONS]
    offenders = []
    for body in bodies:
        lowered = body.lower()
        for term in BANNED_TERMS:
            if term in lowered:
                offenders.append(f"{term!r} in: {body}")
    if offenders:
        raise SystemExit("orthogonal filler contains banned terms:\n  " + "\n  ".join(offenders))


def main() -> None:
    write_appendix_tables()
    write_reference_schedules()
    write_historical_schedules()
    write_draft_proposals()
    write_documentation_and_retention()
    write_audit_and_misconceptions()
    write_directories_and_addenda()
    write_governance_procedures()
    write_settlement_archive()
    check_orthogonal()
    print("wrote handbook chapters 14 through 22")


if __name__ == "__main__":
    main()
