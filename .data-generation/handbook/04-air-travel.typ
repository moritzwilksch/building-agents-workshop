#import "template.typ": card-do, card-dont

= Air Travel Guidelines

== Commercial Air Travel Principles

Air travel constitutes one of the largest single budget lines across Noice & Toit LLP. Flying is often necessary to conduct client discovery sessions, deliver high-stakes litigation arguments, or participate in executive steering committees across continents.

Our policy balances employee health, safety, and productivity with our partnership's duty to manage travel costs responsibly. Airline bookings should be made through our designated corporate travel management portal, which provides direct corporate discounts, duty of care tracking, and centralized billing. Tickets purchased directly from an airline remain reimbursable under the rules below when submitted with the airline's e-ticket receipt or itinerary invoice.

== Advance Booking Expectations

Airfares fluctuate wildly based on capacity, seasonality, and booking lead time. Last-minute bookings represent an unnecessary drain on partnership resources. Finance compares the ticket issue date printed on the e-ticket receipt with the departure date of the first segment. This booking-window screen applies to every e-ticket, including compliant economy fares, and it is applied before the cabin, taxes, and fee rules later in this chapter.

#card-do("Book flights at least 14 days in advance")[
  Plan your travel early and reserve flights at least fourteen calendar days prior to domestic travel and twenty-one calendar days prior to international flights. Advance booking ensures access to competitive economy inventory.
]

#card-dont("Book inside the seven-day window without a stated reason")[
  A ticket issued fewer than seven calendar days before departure is reimbursable only if the submission note states the business reason that prevented earlier booking (a client meeting scheduled at short notice, a court date moved, an urgent site incident). Without a stated reason, the entire ticket is rejected.
]

== Cabin Class Policies and Travel Thresholds

Our cabin class policy is governed by scheduled flight duration. Finance reads the cabin class and the scheduled departure and arrival times from the e-ticket itinerary.

=== Standard Economy Class
Economy class is the default for all flights. It is mandatory for domestic flights and for any flight segment with a scheduled duration under eight (8) hours.

=== Premium Economy
Premium Economy is permitted for segments with a scheduled duration of six (6) hours or more.

=== Long-Haul Business Class Exception
Business class is permitted on a segment only when one of the following holds:
- The scheduled segment duration strictly exceeds eight (8) hours, or
- The submission note states that the traveler had to conduct a documented client presentation or court hearing within four (4) hours of scheduled arrival without an intervening rest night.

#card-dont("Fly business on short-haul routes")[
  A business class segment that satisfies neither condition makes the entire ticket non-reimbursable, because the e-ticket shows no separate economy fare that Finance could reimburse instead. Employees who want more comfort on short flights must buy the upgrade privately on a split invoice.
]

#card-dont("Book First Class under any circumstance")[
  First Class travel is strictly prohibited across all routes, regardless of flight length, seniority, or client billing status. Any ticket containing a First Class segment is rejected in full.
]

== Taxes, Surcharges, and Ancillary Fees

Airline e-tickets itemize government taxes, airport charges, and carrier surcharges separately from the base fare. Fee lines follow the ticket they belong to: screen the e-ticket against the advance-booking window in Section 4.2 and the cabin rules in Section 4.3 before assessing any fee, because a ticket rejected for booking inside the seven-day window without a stated reason, or for an unpermitted cabin, carries its taxes, charges, and surcharges down with it. Where the ticket itself is reimbursable, Finance treats each fee line as follows:

#card-do("Claim mandatory taxes and carrier surcharges")[
  Government air transport taxes, passenger service charges, security fees, and carrier-imposed fuel or distribution surcharges are part of the ticket price and are fully reimbursable. So is one standard checked bag fee per traveler when the itinerary spans more than two calendar days between the first departure and the last arrival.
]

#card-dont("Expense seat selection or priority perks")[
  Seat selection fees, extra-legroom seats, priority boarding, fast-track security, lounge access, and onboard Wi-Fi charges listed on the e-ticket are deducted from the claim. A second or third checked bag, and any checked bag on a trip of two days or less, is likewise deducted.
]

== Flight Changes and Unused Tickets

Business schedules change rapidly, but ticket alterations must be managed with care:
- *Change fees*: A rebooking or change fee shown on the e-ticket is reimbursable when the note states the client or court reason for the change. Changes made for personal convenience are deducted.
- *Unused Ticket Credits*: When a non-refundable flight is canceled for business reasons, the resulting airline credit belongs to Noice & Toit LLP. The employee must track this credit and apply it to their next business journey.
- *Flight Disruption Assistance*: In the event of severe weather cancellations or carrier delays, contact the 24/7 Noice & Toit Travel Assistance Desk for rebooking support.

== Airport Time, Lounges, and Productivity

Partners occasionally argue that lounge access pays for itself in billable hours. The Audit Committee has heard this argument in 2016, 2019, and 2022 and has rejected it each time, most recently by a vote of six to one. The dissenting member was traveling at the time. Lounge fees remain personal. Employees who need a quiet place to work at an airport are reminded that most terminals have a chapel.

== In-Flight Connectivity

Onboard Wi-Fi has improved considerably since the days when a single e-mail attachment could occupy the Atlantic crossing. It remains a personal convenience for policy purposes: onboard Wi-Fi charges are deducted whether they appear on the e-ticket or on a separate receipt. Download your materials before boarding.

== Sustainable Aviation

Noice & Toit LLP is committed to reducing corporate carbon emissions by 30% by 2030, a target the Sustainability Working Group describes as "ambitious but achievable" and the Travel Desk describes as "ambitious". Before booking, assess whether video conferencing achieves the same outcome, and for regional European and US Northeast corridor routes evaluate high-speed rail first (see Chapter 5). Corporate bookings automatically include carbon offset contributions funded centrally; offset fees printed on an e-ticket are reimbursable.

Employees who take the train instead of flying on a route under four hours may note this in the report. The note has no financial effect, but the Sustainability Working Group reads them and, once a year, sends a small reusable cup to the most consistent rail traveler in each office. The cup is not an expense.

== Preferred Carrier and Alliance Directory

The Travel Desk maintains a directory of preferred carriers under framework agreements renegotiated every three years. Preference reflects schedule reliability on the routes our practices actually fly, corporate reporting quality, and the honesty of the carrier's disruption communications, in that order. Bookings made through the corporate travel management portal are matched against this directory automatically; a booking with a preferred carrier requires no justification, while a booking outside the directory asks the submission note to name the reason.

#table(
  columns: (1.6fr, 1.1fr, 1.8fr, 1.2fr, 1.3fr),
  align: (left, center, left, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Carrier*][*Alliance*][*Primary Regions*][*Directory Status*][*Booking Channel*],
  [Lufthansa Group], [Star], [Europe, Asia], [Preferred], [Corporate portal],
  [Swiss International], [Star], [Europe, long-haul hubs], [Preferred], [Corporate portal],
  [SAS], [SkyTeam], [Nordic, transatlantic], [Preferred], [Corporate portal],
  [KLM], [SkyTeam], [Europe, intercontinental], [Preferred], [Corporate portal],
  [Air France], [SkyTeam], [Europe, Africa, Latin America], [Preferred], [Corporate portal],
  [American Airlines], [oneworld], [North America, transatlantic], [Preferred], [Corporate portal],
  [British Airways], [oneworld], [UK, transatlantic], [Preferred], [Corporate portal],
  [Japan Airlines], [oneworld], [East Asia, transpacific], [Preferred], [Corporate portal],
  [Turkish Airlines], [Star], [Türkiye, Middle East, Africa], [Approved], [Corporate portal],
  [Low-cost regional carriers], [None], [Secondary European airports], [Case by case], [Direct with note],
)

The directory status of a carrier can change between editions of this handbook. The portal always reflects the current status, and the portal prevails over any printed list. Directory status is a booking preference only: it neither enlarges nor restricts what is reimbursable, which remains governed by the cabin, booking-window, and fee rules in this chapter. A carrier absent from the list is booked through the portal like any other, and the Travel Desk follows up so that the next edition reflects reality.

== Route Planning and Itinerary Construction

The Travel Desk asks employees to plan routes as a professional would plan a case: the cheapest available sequence of flights is not automatically the best one, and neither is the fastest. A connecting itinerary that saves a modest amount of fare but adds a misconnection risk to a fixed court date is a bad trade. Conversely, a nonstop flight booked purely to avoid a well-timed connection wastes partnership resources and, more often than not, also wastes the day.

Route planning follows three working rules. First, for any engagement with a fixed external deadline — a hearing, a client sign-off, a filing — build the itinerary so that the traveler is on the ground with at least one earlier flight still available as a fallback. Second, prefer connections where the inbound and outbound carriers share the directory status "Preferred", because rebooking after a missed connection is materially simpler within a single carrier's network. Third, avoid itineraries that require an overnight airport stay under any circumstances; if no same-day connection exists, book a hotel and treat the trip as two travel days.

#card-do("Check the whole journey, not just the flight")[
  The value of a route is judged on door-to-door time. A flight with an early departure from a distant airport, or an arrival at an airport from which ground transport to the client site is poor, is frequently worse than a calmer alternative. State the full journey in your note when you choose the less obvious option; the Travel Desk reads notes and adjusts future guidance accordingly.
]

== Duty of Care and Travel-Risk Assessment

Noice & Toit LLP owes every traveler a working knowledge of where they are, whether they can be reached, and what happens if something goes wrong. This is a legal and ethical obligation the partnership takes seriously, and it is administered jointly by People Operations and the Travel Desk through the corporate travel management portal, which keeps a live traveler register for every booked itinerary.

Every international booking triggers an automatic risk review against the firm's destination classification, which People Operations refreshes each quarter from government advisory sources and the firm's security counsel. The classification determines the process, not the traveler's judgment:

#table(
  columns: (1.2fr, 2.2fr, 1.6fr, 1.6fr),
  align: (left, left, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Classification*][*What It Means*][*Process*][*Owner*],
  [Standard], [No elevated security, health, or infrastructure concerns], [Portal registration only], [Travel Desk],
  [Elevated], [Advisories note regional instability, health systems under strain, or infrastructure gaps], [Briefing pack issued; traveler confirms receipt], [People Operations],
  [Enhanced], [Advisories recommend limiting non-essential travel], [Written engagement plan agreed with the responsible Practice Leader], [People Operations],
  [Suspended], [Advisories advise against all travel], [Bookings blocked at the portal; exceptions only by the Managing Partners], [Managing Partners],
)

Travelers to Elevated and Enhanced destinations must complete the firm's short travel-safety module before booking, and must keep the portal's emergency contact current for the duration of the trip. Employees who decline registration cannot be booked; this is not bureaucracy but the minimum condition under which the partnership is willing to send anyone anywhere. The register is read, genuinely, when things go wrong — the record of what it has been used for is kept by the Records Office and summarized to the Audit Committee annually.

== Irregular Operations: Delays, Misconnections, and Denied Boarding

Disruption is a normal feature of commercial aviation and is handled under a standing routine rather than ad hoc improvisation. When a flight is delayed or canceled, the traveler's first contact is the 24/7 Travel Assistance Desk, which holds rebooking authority across all directory carriers. Rebook through the Assistance Desk before rebooking yourself; parallel bookings create duplicate ticket credits that Finance must then untangle, and the untangling is nobody's idea of a productive afternoon.

For misconnections, the carrier that sold the ticket is responsible for rerouting, and travelers should ask the carrier's ground staff to rebook the remainder of the itinerary before leaving the transit area. Keep every document the carrier issues — revised itineraries, delay confirmations, meal or accommodation vouchers — as these support both the expense report and, where relevant, any statutory compensation claim. Vouchers for future travel issued by a carrier in a disruption belong to the firm, consistent with the treatment of unused ticket credits elsewhere in this chapter.

Where a flight is overbooked and the airline seeks volunteers to give up seats, accepting is a personal decision. Cash payments for voluntary or involuntary denied boarding belong to the traveler, provided the acceptance does not cause a missed client commitment or additional costs for the firm. Travelers who expect to be needed at a fixed appointment the next morning should decline the offer and let the airline solve its own yield-management problem with someone else.

The Assistance Desk logs every disruption event, and the Travel Desk reviews the log quarterly. Routes and carriers with recurring disruption are flagged to the directory committee; this review has quietly moved more volume between carriers than any negotiated discount ever has.

== Sustainability Programme Governance and Reporting

The emissions commitment described earlier in this chapter is administered through a standing programme owned by the Sustainability Working Group and audited annually by the Audit Committee. The programme's targets are categorical and published internally each year:

#table(
  columns: (1.5fr, 1.7fr, 1.4fr, 1.4fr),
  align: (left, left, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Objective*][*Direction of Travel*][*Owner*][*Reporting Cadence*],
  [Short-haul substitution by rail], [Increase year over year], [Sustainability Working Group], [Quarterly],
  [Load of booked segments onto directory carriers], [Increase within agreement terms], [Travel Desk], [Quarterly],
  [Use of video conferencing in place of discovery travel], [Increase where equivalent], [Practice Leaders], [Semi-annual],
  [Central offset coverage of booked itineraries], [Maintain full coverage], [Sustainability Working Group], [Annual],
  [Traveler awareness of this policy], [Maintain], [People Operations], [Annual],
)

Reporting is built from portal data, not from employee self-declaration, and is published without naming individuals. The reusable-cup tradition described earlier is the sole exception, and it is administered with appropriate solemnity. Employees with questions about the programme's method are welcome to attend the Working Group's quarterly open session; the minutes are held by the Records Office.

== Airport Ground Connections

The flight is rarely the last leg of the journey. For arrival airports served by rail, the firm expects rail into the city center as the default, with taxis and app-hailed cars justified by luggage, late arrival, or the absence of a reasonable service. Where a client site is closer to a secondary airport than to the city the flight schedule implies, book the flight to the secondary airport; the itinerary serves the work, not the other way round.

Airport-area shuttles operated by hotels are reimbursable when used for a nights-away itinerary under the lodging rules of Chapter 6. Airport parking is reimbursable only when no practical public alternative exists for the departure time in question; the note should say so plainly. Car rental at the destination follows Chapter 5 and is out of scope here.

== Accessibility and Health-Related Travel

Travelers with accessibility needs, prescribed equipment, or conditions requiring in-flight arrangements should record these in the portal profile once, after which the Travel Desk applies them to every booking without further requests. Assistive devices, prescribed equipment and supplies, and documented service animals travel under carrier rules that take precedence over any general luggage guidance in this handbook, and no fee arising from such a requirement falls on the traveler.

For travel during pregnancy, recent surgery, or a condition that may require in-flight care, obtain the carrier's fitness-to-fly clearance where the carrier requires it and note the clearance reference in the portal. People Operations coordinates extended travel for employees with ongoing treatment and will, on request, build itineraries around appointment schedules. These conversations are confidential between the employee and People Operations; the Travel Desk sees only the resulting booking requirements, never the clinical background.

#card-do("Ask early, not at the gate")[
  Carrier arrangements for assistance, equipment, and service animals are made well in advance of travel, not improvised at the airport. Requests lodged with the Travel Desk at booking time are reliably honored; requests lodged at the gate are honored when possible, which is a weaker promise than anyone deserves.
]

== Frequently Asked Questions

*Q: Can I keep frequent flyer miles and airline status points earned on business flights?*\
A: Yes. Employees may retain airline frequent flyer miles and loyalty perks for personal use. However, you may not select a more expensive flight, inconvenient layover, or non-preferred carrier simply to earn loyalty points on a specific airline.

*Q: The e-ticket shows a return flight two weeks after the outbound. Is that a problem?*\
A: The gap itself is not. Whether nights between the flights are reimbursable is decided per night under Chapter 6 and Figure 1. The flight is reimbursable as long as cabin class and booking window comply.

*Q: What happens if an airline involuntarily bumps me and offers cash compensation?*\
A: Denied-boarding compensation belongs to the traveler, provided accepting it does not cause the traveler to miss client commitments or incur extra hotel costs for the firm. Vouchers for future travel, however, must be used for firm travel.

*Q: The airline charged me for a bag that turned out to be under the free allowance. Now what?*\
A: Claim the fee as printed on the e-ticket. Disputes with the airline are between you and the airline; if a refund arrives later, notify Finance and it is offset against your next report.

*Q: A colleague and I are on the same e-ticket. How do I claim it?*\
A: Submit the ticket once, name the second traveler in the note, and route the line to the budget owner. Finance evaluates each passenger's segments individually under the same rules.
