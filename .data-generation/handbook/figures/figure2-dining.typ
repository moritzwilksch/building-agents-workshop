#set page(
  width: 190mm,
  height: auto,
  margin: 10mm,
  fill: white,
)
#set text(
  font: ("Helvetica", "Arial"),
  size: 9.5pt,
  fill: rgb("#1f2937"),
)

#align(center)[
  #block(
    width: 100%,
    stroke: 1.5pt + rgb("#0f172a"),
    radius: 8pt,
    fill: rgb("#f8fafc"),
    inset: 16pt,
    [
      #text(13pt, weight: "bold", fill: rgb("#0f172a"))[
        Figure 2: Approval Policy Flowchart -- Dining, Entertainment & Alcohol Matrix
      ]
      #v(0.3em)
      #text(9pt, fill: rgb("#64748b"))[
        Binding decision hierarchy for all meal claims, team dinners, client entertainment, and beverage expenses
      ]
      #v(1em)

      #block(
        width: 80%,
        fill: rgb("#dbeafe"),
        stroke: 1.5pt + rgb("#2563eb"),
        radius: 5pt,
        inset: 9pt,
        [#text(weight: "bold", fill: rgb("#1e3a8a"))[START: Dining Expense Submitted for Reimbursement]]
      )

      #v(0.5em)
      #text(14pt, fill: rgb("#64748b"))[↓]
      #v(0.5em)

      #text(10pt, weight: "bold", fill: rgb("#475569"))[Determine Dining Category & Attendee Composition:]

      #v(0.6em)

      #grid(
        columns: (1fr, 1fr),
        gutter: 12pt,
        [
          #block(
            width: 100%,
            stroke: 1pt + rgb("#93c5fd"),
            fill: rgb("#eff6ff"),
            radius: 5pt,
            inset: 9pt,
            [
              #text(10pt, weight: "bold", fill: rgb("#1d4ed8"))[Solo Employee Dining]\
              #v(0.3em)
              #text(8.5pt)[
                - *Allowed spend*: Up to daily caps (€15 breakfast, €25 lunch, €45 dinner; daily max €85).
                - *Alcohol policy*: *Strictly 0%*. Any beer, wine, or spirits must be deducted in full.
                - *Mandatory*: Itemized restaurant slip.
              ]
            ]
          )
        ],
        [
          #block(
            width: 100%,
            stroke: 1pt + rgb("#a7f3d0"),
            fill: rgb("#f0fdf4"),
            radius: 5pt,
            inset: 9pt,
            [
              #text(10pt, weight: "bold", fill: rgb("#047857"))[Internal Team Dinner]\
              #v(0.3em)
              #text(8.5pt)[
                - *Allowed spend*: Up to €35.00 / \$40.00 per person.
                - *Alcohol policy*: Moderate beer or wine up to *15%* of food subtotal.
                - *Mandatory*: Manager pre-approval and quarterly milestone justification.
              ]
            ]
          )
        ]
      )

      #v(0.6em)

      #grid(
        columns: (1fr, 1fr),
        gutter: 12pt,
        [
          #block(
            width: 100%,
            stroke: 1pt + rgb("#fed7aa"),
            fill: rgb("#fff7ed"),
            radius: 5pt,
            inset: 9pt,
            [
              #text(10pt, weight: "bold", fill: rgb("#c2410c"))[Client Hospitality Dinner]\
              #v(0.3em)
              #text(8.5pt)[
                - *Attendee ratio*: At least 1 external guest per employee.
                - *Allowed spend*: Lunch €50 / \$55; Dinner €90 / \$100 per attendee.
                - *Alcohol policy*: Beer/wine up to *30%* of food subtotal. Hard spirits strictly banned.
                - *Mandatory*: Full attendee roster (names, titles, companies).
              ]
            ]
          )
        ],
        [
          #block(
            width: 100%,
            stroke: 1pt + rgb("#fecaca"),
            fill: rgb("#fef2f2"),
            radius: 5pt,
            inset: 9pt,
            [
              #text(10pt, weight: "bold", fill: rgb("#b91c1c"))[Late-Night Spending (After 23:00)]\
              #v(0.3em)
              #text(8.5pt)[
                - *Eligibility*: *Strictly Non-Reimbursable (0%)*.
                - *Coverage*: All bar bills, night clubs, lounge tabs, and meal charges after 23:00.
                - *Action*: Deduct all post-23:00 line items from the claim.
              ]
            ]
          )
        ]
      )

      #v(1em)
      #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
      #v(0.4em)
      #text(8pt, fill: rgb("#64748b"))[
        *Note*: This visual flowchart is the sole binding authority for dining, hospitality, and beverage reimbursements at Noice & Toit LLP.
      ]
    ]
  )
]
