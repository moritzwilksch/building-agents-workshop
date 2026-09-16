#import "template.typ": card-do, card-dont

= Historical Schedules (Superseded)

The tables in this chapter record rates, caps, and norms from earlier editions of this handbook. They are retained so that previously processed reimbursements can be audited and explained.

#card-dont("Apply a historical schedule to a current claim")[
  Nothing in this chapter is effective for a claim processed on or after January 1, 2024. Version 4.2 governs every claim processed on or after that date, regardless of the date printed on the receipt. When a historical table and a current chapter appear to disagree, the current chapter always governs.
]

== Version History

#table(
  columns: (1fr, 1.2fr, 3fr),
  align: (center, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Version*][*Effective Date*][*Summary*],
  [2.0], [January 1, 2021], [First consolidated international edition.], 
  [3.0], [January 1, 2023], [Introduced the Truffle Policy and the event surcharge caps.], 
  [3.1], [July 1, 2023], [Raised the Tier 2 lodging cap and the daily meal aggregate.], 
  [4.0], [October 1, 2023], [Moved group dining rules into Figure 2.], 
  [4.2], [January 1, 2024], [Current edition. Confirms that the visual decision architecture is binding.], 
)

== Superseded Lodging Caps (Version 3.1)

Effective July 1, 2023 to December 31, 2023. Replaced by the caps in Chapter 6 and the Appendix of Chapter 14.

#table(
  columns: (1.2fr, 1fr, 1.1fr, 1.6fr),
  align: (left, left, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Tier*][*Markets*][*Superseded EUR Cap*][*Status*],
  [Tier 1], [Tier 1 markets as listed in the current edition], [€200.00], [Superseded — never payable], 
  [Tier 2], [Tier 2 markets as listed in the current edition], [€145.00], [Superseded — never payable], 
  [Tier 3], [All other markets], [€110.00], [Superseded — never payable], 
)

== Superseded Lodging Caps (Version 3.0)

Effective January 1, 2023 to June 30, 2023. Replaced by the Version 3.1 caps above.

#table(
  columns: (1.2fr, 1fr, 1.1fr, 1.6fr),
  align: (left, left, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Tier*][*Markets*][*Superseded EUR Cap*][*Status*],
  [Tier 1], [Tier 1 markets as listed in the prior edition], [€180.00], [Superseded — never payable], 
  [Tier 2], [Tier 2 markets as listed in the prior edition], [€130.00], [Superseded — never payable], 
  [Tier 3], [All other markets], [€95.00], [Superseded — never payable], 
)

== Superseded Meal Caps (Version 3.1)

Effective July 1, 2023 to December 31, 2023. Replaced by the caps in Chapter 7 and the Appendix of Chapter 14.

#table(
  columns: (1.4fr, 1fr, 1fr, 1.6fr),
  align: (left, center, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Meal Category*][*Superseded EUR Cap*][*Receipt Time*][*Status*],
  [Breakfast], [€13.00], [Before 11:00], [Superseded — never payable], 
  [Lunch], [€22.00], [11:00 to 15:59], [Superseded — never payable], 
  [Dinner], [€40.00], [16:00 onward], [Superseded — never payable], 
  [Daily aggregate], [€75.00], [Per calendar day], [Superseded — never payable], 
)

== Superseded Tipping Norms (Version 2.0)

Effective until December 31, 2022. Replaced by the country rows in Chapter 14.

#table(
  columns: (2fr, 1fr, 1.8fr),
  align: (left, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Country or Region*][*Superseded Maximum Tip*][*Status*],
  [United States and Canada], [18%], [Superseded — never payable], 
  [United Kingdom], [10%], [Superseded — never payable], 
  [Continental Europe], [8%], [Superseded — never payable], 
  [Japan, South Korea, Singapore, Hong Kong], [0%], [Superseded — never payable], 
)

== Withdrawn Allowances

The following allowances appeared in earlier editions and have been withdrawn. They are not reimbursable under Version 4.2:
- A flat daily incidental allowance of €20 with no receipt (withdrawn).
- A nightly hotel internet surcharge, now included in corporate rates (withdrawn).
- A fixed airport transfer allowance of €40 in Tier 1 cities (withdrawn).
- A per-mile bicycle allowance above the statutory rate (withdrawn).
- A weekend meal supplement of €15 (withdrawn).
- A monthly home-office electricity stipend (withdrawn).
