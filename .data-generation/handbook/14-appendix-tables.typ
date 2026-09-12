#import "template.typ": card-do, card-dont

= Appendix: Reference Tables and Global Schedules

== Global Hotel Nightly Room Rate Caps

The following caps apply to the nightly room rate as printed on the folio, exclusive of municipal tourism taxes and VAT added on top. The hotel's city determines the tier:

#table(
  columns: (1fr, 2fr, 1fr, 1fr, 1fr),
  align: (center, left, center, center, center),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Tier*][*Metropolitan Markets Covered*][*EUR (€)*][*USD (\$)*][*GBP (£)*],
  [Tier 1], [London, New York City, San Francisco, Zurich, Geneva, Paris, Tokyo, Singapore, Hong Kong], [€220.00], [\$250.00], [£190.00],
  [Tier 2], [Berlin, Munich, Frankfurt, Hamburg, Amsterdam, Dublin, Chicago, Boston, Seattle, Toronto, Sydney, Milan], [€160.00], [\$180.00], [£140.00],
  [Tier 3], [All other cities, secondary metropolitan markets, university hubs, and suburban districts], [€120.00], [\$140.00], [£105.00],
)

== Hotel Incidental Allowances

#table(
  columns: (1.6fr, 1fr, 1fr, 1fr, 2fr),
  align: (left, center, center, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Folio Line*][*EUR (€)*][*USD (\$)*][*GBP (£)*][*Condition*],
  [Laundry, stay over 5 nights], [€35.00 / 7 days], [\$40.00 / 7 days], [£30.00 / 7 days], [None],
  [Garment rescue, stay of 5 nights or fewer], [€25.00 / stay], [\$30.00 / stay], [£22.00 / stay], [Note describes the soiling incident],
  [Parking incl. valet and EV charging], [€30.00 / night], [\$35.00 / night], [£26.00 / night], [Note identifies rental or pool vehicle],
  [City tax, tourism levy], [Full], [Full], [Full], [Itemized on folio],
  [Minibar, spa, movies, pet fee, gym], [€0.00], [\$0.00], [£0.00], [Always deducted],
)

== Daily Meal Allowances and Spending Limits (Solo Dining)

Meal limits are based on actual, itemized receipts up to the stated maximum caps. The receipt time selects the category:

#table(
  columns: (1.5fr, 1fr, 1fr, 1fr, 2fr),
  align: (left, center, center, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Meal Category*][*EUR (€)*][*USD (\$)*][*GBP (£)*][*Receipt Time*],
  [Breakfast], [€15.00], [\$18.00], [£13.00], [Before 11:00],
  [Lunch], [€25.00], [\$30.00], [£22.00], [11:00 to 15:59],
  [Dinner], [€45.00], [\$55.00], [£38.00], [16:00 onward],
  [Overtime meal at home office], [€20.00], [\$25.00], [£18.00], [After 20:30, note states late work],
  [*Daily Aggregate Cap*], [*€85.00*], [*\$100.00*], [*£73.00*], [Maximum cumulative reimbursement per calendar day],
)

Group dining caps (internal team meals and client hospitality) are set exclusively in Figure 2, Chapter 13.

== Personal Vehicle Mileage Rates

#table(
  columns: (1.5fr, 1.2fr, 2fr),
  align: (left, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Country / Jurisdiction*][*Statutory Rate*][*Required Documentation*],
  [European Union (Standard)], [€0.38 / km], [Departure and arrival addresses, verified map distance],
  [United States (IRS Benchmark)], [\$0.67 / mile], [Itemized mileage log with client project citation],
  [United Kingdom (HMRC Tier 1)], [£0.45 / mile], [First 10,000 business miles in tax year],
  [United Kingdom (HMRC Tier 2)], [£0.25 / mile], [Excess business miles above 10,000 miles],
  [Bicycle Allowance (All regions)], [€0.25 / km], [Business visits under 20km round-trip],
  [Rental or pool vehicle fuel], [Actual receipt], [Fuel line only; shop items deducted; note names the rental],
)

== Global Tipping and Gratuity Standards

The cap is calculated on the bill before tip. It applies to restaurants and taxis alike. The vendor's country governs.

#table(
  columns: (1.2fr, 1fr, 2.2fr),
  align: (left, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Country / Region*][*Maximum Tip*][*Policy Guidance*],
  [United States & Canada], [20%], [Table service and taxis. Counter service, takeout, and delivery: \$1.00 maximum],
  [United Kingdom], [12.5%], [Only if no service charge is printed on the bill; printed service charge is reimbursed, extra tip deducted],
  [EU countries (Germany, France, Spain, Italy, Netherlands, ...)], [10%], [Service included by law; takeaway and delivery: no tip reimbursed],
  [Switzerland], [10%], [Service included; rounding up is customary],
  [Japan, South Korea], [0%], [Tipping is not customary; any tip deducted],
  [Singapore, Hong Kong], [0%], [Printed 10% service charge reimbursed; any additional tip deducted],
)

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
