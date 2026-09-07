#import "template.typ": policy-rule, policy-warning

= Appendix: Reference Rate Tables

== Hotel Nightly Rate Caps by Destination Tier

#table(
  columns: (1fr, 1.5fr, 1fr, 1fr),
  align: (center, left, center, center),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Tier*][*Designated Metropolitan Areas*][*EUR Cap (€)*][*USD Cap (\$)*],
  [Tier 1], [London, New York, San Francisco, Zurich, Geneva, Paris, Tokyo, Singapore], [€220.00], [\$250.00],
  [Tier 2], [Berlin, Munich, Frankfurt, Amsterdam, Dublin, Chicago, Boston, Seattle, Toronto], [€160.00], [\$180.00],
  [Tier 3], [All other secondary cities, regional hubs, and suburban territories], [€120.00], [\$140.00],
)

== Daily Meal Allowances & Maximum Per Diems

#table(
  columns: (1.5fr, 1fr, 1fr, 1.5fr),
  align: (left, center, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Meal Type*][*EUR (€)*][*USD (\$)*][*Eligibility Window*],
  [Breakfast], [€15.00], [\$18.00], [Travel before 07:00 / hotel unprovided],
  [Lunch], [€25.00], [\$30.00], [Trip spanning 12:00 to 14:00],
  [Dinner], [€45.00], [\$55.00], [Trip spanning after 19:00],
  [*Maximum Daily Total*], [*€85.00*], [*\$100.00*], [Maximum aggregate per calendar day],
)

== Mileage & Ground Transport Rates

#table(
  columns: (1.5fr, 1fr, 1fr),
  align: (left, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Vehicle Category*][*Standard Rate*][*Notes / Documentation*],
  [Personal Vehicle (EU)], [€0.38 / km], [Odometer log or route map required],
  [Personal Vehicle (US)], [\$0.67 / mile], [IRS benchmark conforming standard],
  [Bicycle Allowance], [€0.25 / km], [Encouraging eco-friendly transit (< 20km)],
  [Rental Car Fuel], [Actual receipt], [Standard pump receipt; pre-paid fuel disallowed],
)

== Rule Citation Quick Reference

#table(
  columns: (1.2fr, 1.2fr, 2fr),
  align: (center, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Rule Code*][*Domain*][*Key Standard*],
  [POL-DOC-001], [Submission], [Strict 30-day submission deadline],
  [POL-DOC-002], [Receipts], [Itemized receipts required (> €10 / \$10)],
  [POL-AIR-001], [Aviation], [Economy mandatory for flights under 8 hours],
  [POL-LOD-001], [Lodging], [Nightly caps: Tier 1 €220 / Tier 2 €160],
  [POL-LOD-002], [Incidentals], [Minibar, spa, and movies strictly excluded],
  [POL-MEA-001], [Meals], [Max daily allowance €85 / \$100],
  [POL-MEA-002], [Meals], [Zero alcohol reimbursement on solo dining],
  [POL-ENT-002], [Entertaining], [Client dinner max €90 / \$100 per person],
  [POL-WKD-001], [Weekend], [Weekend travel requires business justification],
  [POL-NON-001], [Exclusions], [Fines, penalties, and traffic tickets rejected],
)
