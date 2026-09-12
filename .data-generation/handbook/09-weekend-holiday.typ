#import "template.typ": card-do, card-dont

= Weekends, Holidays, and Bleisure Travel

== Weekend Travel Context and Governance

Business engagements at Noice & Toit LLP generally occur during regular business days from Monday morning through Friday evening. Travel schedules should be structured to allow professionals to return home for their personal weekends and public holidays whenever feasible.

However, complex multi-jurisdictional matters, international cross-border transactions, client audits, and trade conferences occasionally require travel over weekends or declared public holidays. Because weekend expenditures naturally blend business obligations with personal downtime, tax authorities and compliance auditors subject weekend claims to rigorous scrutiny.

== The Weekend Approval Decision Logic

To ensure complete fairness and objective auditing across all practice groups, Noice & Toit LLP does not rely on subjective narrative rules for weekend reimbursement. Instead, all eligibility rules for Saturday, Sunday, and statutory holiday expenses are defined strictly within our centralized visual flowchart.

#card-do("Evaluate weekend claims against the visual flowchart")[
  Any receipt dated on a Saturday, Sunday, or declared public holiday, and any hotel night beginning on such a day, is governed exclusively by Figure 1: Weekend and Public Holiday Travel Approval Flowchart in Chapter 13. The facts the flowchart asks about (a conference or client delivery on that day, a Monday morning meeting) must be stated in the submission note.
]

#card-dont("Assume weekend stays are automatically reimbursed")[
  Do not assume that an early Monday meeting or late Friday flight automatically justifies company reimbursement for an entire weekend. If your circumstance leads to a non-reimbursable branch in Figure 1, you must cover those costs personally.
]

=== What Counts as a Weekend Expense
- A *restaurant, taxi, or fuel receipt* is a weekend expense when its printed date falls on a Saturday, Sunday, or public holiday.
- A *hotel night* is a weekend expense when it begins on such a day (see Chapter 6). Weekday nights on the same folio are evaluated normally.
- A *flight or train ticket* is not a weekend expense merely because the travel day is a weekend; the ticket is evaluated under Chapters 4 and 5. Lodging and meals at the destination on that weekend are.
- *Commercial invoices* for goods (Chapter 10) are never weekend expenses.

== Combining Business Travel with Personal Leisure (Bleisure)

Noice & Toit LLP supports employee well-being and recognizes that combining business journeys with personal leisure (often called "bleisure" travel) can be an enjoyable benefit of professional life. Employees are welcome to extend business trips over weekends or take personal vacation days in destination cities, provided this is done with absolute cost neutrality to the firm.

=== The Cost-Neutrality Principle
Personal extensions must impose zero incremental financial cost on Noice & Toit LLP or our billing clients:
- *Airfare*: A ticket whose dates include a personal extension is reimbursable as long as the note states the business dates and confirms that the fare did not exceed the direct business-only fare.
- *Lodging and Daily Expenses*: Hotel nights, local transit, meals, and incidentals on personal extension days are the exclusive responsibility of the employee. Where a folio covers such nights, Finance deducts them.

#card-dont("Expense personal sightseeing or recreational activities")[
  Never claim expenses for museum admissions, guided city tours, sporting event tickets, ski passes, beach equipment rentals, or cultural excursions, regardless of whether they take place during a weekend or on an extended business trip.
]

== Family Members, Spouses, and Travel Companions

Partners, associates, and staff are welcome to have family members, spouses, or companions accompany them on business trips, subject to strict boundaries:
- All tickets, meals, and transit for accompanying companions must be paid privately. Restaurant bills that include a companion are evaluated with the companion excluded from the attendee count and their share deducted.
- If a companion shares a standard business hotel room, the firm covers the nightly rate up to the regional cap. Extra-person, rollaway, or double-occupancy surcharges on the folio are deducted.

== International Travel and Transit Rest Days

On long-haul intercontinental journeys crossing more than six (6) time zones (London to Singapore, New York to Tokyo), travelers may arrange an arrival schedule that includes an overnight rest day before commencing formal client meetings. Whether such a night is reimbursable depends only on the day of the week: a weekday rest night is an ordinary hotel night under Chapter 6, a weekend rest night follows Figure 1. Jet lag is real, but it is not a branch in the flowchart.

== Public Holidays Around the World

Which days count as public holidays is a surprisingly deep question in a firm with offices on three continents. For the purposes of Figure 1, a public holiday is a statutory holiday in the country where the expense was incurred, not in the employee's home country. Whit Monday in Berlin is a holiday; Whit Monday in New York is a Monday. Employees are encouraged to check the destination calendar before assuming either.

== Trade Fair and Congress Weeks

Hotel rates in trade-fair and congress cities surge during major events, and the ordinary tier caps in Chapter 6 can make a compliant booking impossible in those weeks. For the events listed below, Noice & Toit LLP therefore maintains event surcharge caps that override the regional tier caps in Chapter 6 and the appendix table in Chapter 14 for the host city concerned.

#card-do("Claim the event surcharge cap when your stay overlaps a listed event")[
  When your hotel stay overlaps the window of one of the events below and your submission note names the event, each night falling within the event window is reimbursed up to the event surcharge cap instead of the city's ordinary tier cap. All other lodging rules (incidentals, laundry, parking, city tax) are unchanged. Where the note names no listed event, or the stay falls outside the event window, the ordinary tier cap governs even if you attended the event.
]

#table(
  columns: (1.1fr, 1.5fr, 1.1fr, 1.6fr),
  align: (left, left, center, center),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*City*][*Event*][*Event Window*][*Nightly Surcharge Cap*],
  [Berlin], [FinTech Summit], [March], [€200.00 / \$225.00 / £175.00],
  [Munich], [Bauma construction fair], [April], [€200.00 / \$225.00 / £175.00],
  [Hamburg], [SMM Wind Energy], [September], [€200.00 / \$225.00 / £175.00],
  [Frankfurt], [Frankfurt Book Fair], [October], [€200.00 / \$225.00 / £175.00],
  [Düsseldorf], [Medica], [November], [€200.00 / \$225.00 / £175.00],
)

== Frequently Asked Questions

*Q: What if extending my stay over a Saturday night makes the return airfare significantly cheaper than a Friday departure?*\
A: If staying over a Saturday night reduces the round-trip airfare by more than the cost of one extra hotel night and one day of meals, the firm may cover the Saturday night hotel. State the fare saving and the approving Practice Leader in the note; without both, Figure 1 applies unchanged.

*Q: My conference ran Thursday to Saturday. Is Saturday night reimbursable?*\
A: Follow Figure 1. The conference was on Saturday, so Saturday night is decided by the conference branch; name the conference in the note.
