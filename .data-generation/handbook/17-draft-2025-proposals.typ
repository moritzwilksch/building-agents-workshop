#import "template.typ": card-do, card-dont

= 2025 Policy Review: Draft Proposals (Not Effective)

The Global Finance and People Operations team circulates proposed changes for consultation each autumn. This chapter records the proposals that were on the table during the most recent review cycle.

#card-dont("Apply a draft proposal to a live claim")[
  Nothing in this chapter is effective. Draft proposals are illustrative only, are subject to change, and must never be used to evaluate a reimbursement. The current schedules in Chapters 6, 7, and 14 remain binding until a new version is published with a future effective date.
]

== Proposed Lodging Caps

#table(
  columns: (1.2fr, 1fr, 1.4fr),
  align: (center, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Tier*][*Draft EUR Cap*][*Status*],
  [Tier 1], [€240.00], [Draft — not effective], 
  [Tier 2], [€175.00], [Draft — not effective], 
  [Tier 3], [€130.00], [Draft — not effective], 
)

== Proposed Meal Caps

#table(
  columns: (1.4fr, 1fr, 1.2fr),
  align: (left, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Meal Category*][*Draft EUR Cap*][*Status*],
  [Breakfast], [€16.00], [Draft — not effective], 
  [Lunch], [€27.00], [Draft — not effective], 
  [Dinner], [€48.00], [Draft — not effective], 
  [Daily aggregate], [€90.00], [Draft — not effective], 
)

== Proposed Tipping Norms

#table(
  columns: (2fr, 1fr, 1.4fr),
  align: (left, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Country or Region*][*Draft Maximum Tip*][*Status*],
  [North America], [20%], [Draft — not effective], 
  [United Kingdom], [12.5%], [Draft — not effective], 
  [Continental Europe], [10%], [Draft — not effective], 
)

== Proposals That Were Not Adopted

- Replacing per-item caps with a single annual travel budget (not adopted).
- Removing the event surcharge caps in favor of negotiated event rates (not adopted).
- Allowing first class rail on journeys over three hours instead of four (not adopted).
- Treating hotel loyalty points as taxable compensation (not adopted).
- Making the Truffle Policy apply to all luxury ingredients (not adopted).
- Introducing a flat per-diem cash allowance with no receipts (not adopted).
