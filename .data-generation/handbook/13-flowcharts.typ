#import "template.typ": policy-rule, policy-warning

= Decision Flowcharts & Visual Guidelines

This chapter contains visual decision trees and flowcharts governing complex, conditional expense determinations. Employees, managers, and auditing agents must follow the explicit branches illustrated below.

== Weekend and Holiday Expense Eligibility Flowchart

#policy-rule("POL-FLW-001", "Weekend & Holiday Expense Decision Logic")[
  When an expense claim contains line items dated on a Saturday, Sunday, or declared public holiday, auditors and automated agents must evaluate eligibility strictly against the decision logic illustrated in Figure 1.
]

#v(1em)

#figure(
  block(
    width: 100%,
    stroke: 1pt + rgb("#cbd5e1"),
    radius: 6pt,
    fill: rgb("#f8fafc"),
    inset: 1.5em,
    [
      #align(center)[
        #block(
          width: 70%,
          fill: rgb("#dbeafe"),
          stroke: 1.5pt + rgb("#2563eb"),
          radius: 4pt,
          inset: 8pt,
          [#text(weight: "bold", fill: rgb("#1e3a8a"))[START: Expense Incurred on Weekend or Holiday?]]
        )

        #v(0.6em)
        #text(12pt, fill: rgb("#64748b"))[↓]
        #v(0.6em)

        #block(
          width: 75%,
          fill: rgb("#fef3c7"),
          stroke: 1.5pt + rgb("#d97706"),
          radius: 4pt,
          inset: 8pt,
          [#text(weight: "bold", fill: rgb("#92400e"))[Is there an official client event, conference, or trade show on that day?]]
        )

        #v(0.6em)
        #grid(
          columns: (1fr, 1fr),
          gutter: 1em,
          [
            #text(10pt, weight: "bold", fill: rgb("#16a34a"))[YES ↓]
            #v(0.4em)
            #block(
              width: 90%,
              fill: rgb("#dcfce7"),
              stroke: 1.5pt + rgb("#16a34a"),
              radius: 4pt,
              inset: 8pt,
              [#text(weight: "bold", fill: rgb("#14532d"))[FULLY REIMBURSABLE]\
               #text(8pt)[Attach agenda & client details to claim]]
            )
          ],
          [
            #text(10pt, weight: "bold", fill: rgb("#dc2626"))[NO ↓]
            #v(0.4em)
            #block(
              width: 90%,
              fill: rgb("#fef3c7"),
              stroke: 1.5pt + rgb("#d97706"),
              radius: 4pt,
              inset: 8pt,
              [#text(weight: "bold", fill: rgb("#92400e"))[Is it a Sunday arrival for a pre-10:00 AM Monday meeting?]]
            )
          ]
        )

        #v(0.6em)
        #grid(
          columns: (1fr, 1fr),
          gutter: 1em,
          [],
          [
            #grid(
              columns: (1fr, 1fr),
              gutter: 0.5em,
              [
                #text(9pt, weight: "bold", fill: rgb("#16a34a"))[YES ↓]
                #v(0.2em)
                #block(
                  fill: rgb("#dcfce7"),
                  stroke: 1pt + rgb("#16a34a"),
                  radius: 3pt,
                  inset: 6pt,
                  [#text(8.5pt, weight: "bold", fill: rgb("#14532d"))[Sunday Lodging & Dinner Reimbursed]\
                   #text(7.5pt)[Requires written manager sign-off]]
                )
              ],
              [
                #text(9pt, weight: "bold", fill: rgb("#dc2626"))[NO ↓]
                #v(0.2em)
                #block(
                  fill: rgb("#fee2e2"),
                  stroke: 1pt + rgb("#dc2626"),
                  radius: 3pt,
                  inset: 6pt,
                  [#text(8.5pt, weight: "bold", fill: rgb("#991b1b"))[STRICTLY DISALLOWED]\
                   #text(7.5pt)[Personal leisure extension]]
                )
              ]
            )
          ]
        )
      ]
    ]
  ),
  caption: [Figure 1: Weekend and Statutory Holiday Expense Approval Flowchart],
) <fig:weekend-flowchart>

== Client Entertainment & Alcohol Approval Matrix

#policy-rule("POL-FLW-002", "Client Entertainment Decision Matrix")[
  Group hospitality claims must be processed through the multi-factor threshold verification shown in Figure 2. Claims lacking verified attendee rosters must be flagged for partial or complete deduction.
]

#v(1em)

#figure(
  block(
    width: 100%,
    stroke: 1pt + rgb("#cbd5e1"),
    radius: 6pt,
    fill: rgb("#f8fafc"),
    inset: 1.5em,
    [
      #align(center)[
        #table(
          columns: (1.5fr, 1.2fr, 1.2fr, 1.5fr),
          align: (left, center, center, left),
          fill: (_, y) => if y == 0 { rgb("#e2e8f0") } else if calc.even(y) { rgb("#f1f5f9") } else { none },
          stroke: 0.5pt + rgb("#cbd5e1"),
          table.header[*Expense Type*][*Attendee Ratio*][*Alcohol Permitted?*][*Audit Action Required*],
          [Solo Employee Dining], [1:0 (No external)], [No -- 0%], [Reject any alcohol line items],
          [Internal Team Meal], [N:0 (Internal only)], [Beer/Wine up to 15%], [Manager pre-approval required],
          [Client Hospitality Dinner], [At least 1:1 ratio], [Beer/Wine up to 30%], [Verify external attendee names & titles],
          [Late Night Entertainment], [Any ratio], [Disallowed (0%)], [Reject all items after 23:00],
        )
      ]
    ]
  ),
  caption: [Figure 2: Client Hospitality and Dining Approval Matrix],
) <fig:dining-matrix>
