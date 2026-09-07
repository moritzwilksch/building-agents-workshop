#import "template.typ": card-do, card-dont

= Appendix: Reference Tables and Global Schedules

== Global Hotel Nightly Room Rate Caps

The following caps apply to standard single occupancy hotel rooms, exclusive of mandatory municipal tourism taxes and local VAT:

#table(
  columns: (1fr, 2fr, 1fr, 1fr, 1fr),
  align: (center, left, center, center, center),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Tier*][*Metropolitan Markets Covered*][*EUR (€)*][*USD (\$)*][*GBP (£)*],
  [Tier 1], [London, New York City, San Francisco, Zurich, Geneva, Paris, Tokyo, Singapore, Hong Kong], [€220.00], [\$250.00], [£190.00],
  [Tier 2], [Berlin, Munich, Frankfurt, Amsterdam, Dublin, Chicago, Boston, Seattle, Toronto, Sydney, Milan], [€160.00], [\$180.00], [£140.00],
  [Tier 3], [All other regional cities, secondary metropolitan markets, university hubs, and suburban districts], [€120.00], [\$140.00], [£105.00],
)

== Daily Meal Allowances and Spending Limits

Meal limits are based on actual, itemized receipts up to the stated maximum caps:

#table(
  columns: (1.5fr, 1fr, 1fr, 1fr, 2fr),
  align: (left, center, center, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Meal Category*][*EUR (€)*][*USD (\$)*][*GBP (£)*][*Conditions and Eligibility*],
  [Breakfast], [€15.00], [\$18.00], [£13.00], [Departure prior to 07:00 or room excludes breakfast],
  [Lunch], [€25.00], [\$30.00], [£22.00], [Travel spans 12:00 PM to 2:00 PM away from office],
  [Dinner], [€45.00], [\$55.00], [£38.00], [Travel extends past 7:00 PM local time],
  [*Daily Aggregate Cap*], [*€85.00*], [*\$100.00*], [*£73.00*], [Maximum cumulative reimbursement across all meals],
)

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
  [Commercial Rental Fuel], [Actual receipt], [Standard petrol pump receipt showing date and volume],
)

== Global Tipping and Gratuity Standards

#table(
  columns: (1.2fr, 1.2fr, 2fr),
  align: (left, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Country / Region*][*Customary Tip*][*Policy Guidance and Caps*],
  [United States & Canada], [15% to 20%], [Reimbursable up to 20% max on table dining; takeout max \$1.00],
  [United Kingdom], [Optional 12.5%], [Reimbursable if not already added as service charge to bill],
  [Germany, France, Spain, Italy], [Round up / 5% to 10%], [Service included by law; discretionary tips capped at €5.00],
  [Switzerland], [Small round up], [Service included; modest rounding up to nearest 5 CHF allowed],
  [Japan, South Korea], [0% (No tip)], [Tipping is not customary; zero reimbursement],
  [Singapore, Hong Kong], [0% to 10%], [10% service charge standard on bills; do not add extra tip],
)

== Pre-Submission Compliance Checklist

Before clicking submit in the Noice & Toit Expense Portal, verify the following items:
- [ ] Every line item over €10.00 / \$10.00 has an attached itemized receipt showing goods, unit prices, and tax.
- [ ] No summary credit card terminal slips are used as sole proof of spend.
- [ ] All hotel folios are attached in full, and all minibar, spa, or movie charges have been deducted.
- [ ] Solo meals contain zero alcoholic beverages (or alcohol and associated tax have been deducted).
- [ ] All hosted client meals include an attendee roster (names, titles, organizations) and business purpose.
- [ ] Weekend or public holiday travel strictly complies with the visual flowchart in Figure 1 (Chapter 13).
- [ ] Group dining and entertainment comply with the visual approval matrix in Figure 2 (Chapter 13).
- [ ] All line items are allocated to the correct client matter code or administrative cost center.
- [ ] The claim is submitted within thirty (30) calendar days of transaction completion.

== Global Finance Directory and Contact Information

For inquiries regarding travel bookings, card management, or expense auditing:
- *Global Travel Desk*: `travel@noiceandtoit.internal` (24/7 emergency flight changes and duty of care support).
- *Expense Auditing Team*: `expenses@noiceandtoit.internal` (receipt verification and policy clarifications).
- *Corporate Card Administration*: `corporatecards@noiceandtoit.internal` (card issuance, limits, and lost cards).
- *Accounts Payable / Disbursements*: `finance-disbursements@noiceandtoit.internal` (payroll payout schedules).
