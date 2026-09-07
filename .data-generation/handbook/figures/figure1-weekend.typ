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
        Figure 1: Weekend and Public Holiday Travel Approval Flowchart
      ]
      #v(0.3em)
      #text(9pt, fill: rgb("#64748b"))[
        Mandatory decision sequence for all Saturday, Sunday, and statutory holiday expense claims
      ]
      #v(1em)

      // Start Node
      #block(
        width: 80%,
        fill: rgb("#dbeafe"),
        stroke: 1.5pt + rgb("#2563eb"),
        radius: 5pt,
        inset: 9pt,
        [#text(weight: "bold", fill: rgb("#1e3a8a"))[START: Expense incurred on a Saturday, Sunday, or public holiday?]]
      )

      #v(0.5em)
      #text(14pt, fill: rgb("#64748b"))[↓]
      #v(0.5em)

      // Decision 1
      #block(
        width: 85%,
        fill: rgb("#fef3c7"),
        stroke: 1.5pt + rgb("#d97706"),
        radius: 5pt,
        inset: 9pt,
        [#text(weight: "bold", fill: rgb("#92400e"))[Is there an official client conference, trade show, or scheduled client delivery on that calendar day?]]
      )

      #v(0.6em)
      #grid(
        columns: (1fr, 1fr),
        gutter: 14pt,
        [
          #text(11pt, weight: "bold", fill: rgb("#16a34a"))[YES  ↓]
          #v(0.4em)
          #block(
            width: 100%,
            fill: rgb("#dcfce7"),
            stroke: 1.5pt + rgb("#16a34a"),
            radius: 5pt,
            inset: 10pt,
            [
              #text(weight: "bold", fill: rgb("#14532d"), size: 10pt)[FULLY REIMBURSABLE]\
              #v(0.3em)
              #text(8.5pt)[Lodging, travel, and meals covered under standard caps.\
              *Requirement*: Attach event registration or client agenda.]
            ]
          )
        ],
        [
          #text(11pt, weight: "bold", fill: rgb("#dc2626"))[NO  ↓]
          #v(0.4em)
          #block(
            width: 100%,
            fill: rgb("#fef3c7"),
            stroke: 1.5pt + rgb("#d97706"),
            radius: 5pt,
            inset: 9pt,
            [
              #text(weight: "bold", fill: rgb("#92400e"))[Is arrival on Sunday evening for a mandatory business meeting scheduled Monday before 10:00 AM?]
            ]
          )
        ]
      )

      #v(0.6em)
      #grid(
        columns: (1fr, 1fr),
        gutter: 14pt,
        [],
        [
          #grid(
            columns: (1fr, 1fr),
            gutter: 8pt,
            [
              #text(10pt, weight: "bold", fill: rgb("#16a34a"))[YES  ↓]
              #v(0.3em)
              #block(
                fill: rgb("#dcfce7"),
                stroke: 1.5pt + rgb("#16a34a"),
                radius: 4pt,
                inset: 8pt,
                [
                  #text(8.5pt, weight: "bold", fill: rgb("#14532d"))[PARTIALLY REIMBURSED]\
                  #v(0.2em)
                  #text(7.5pt)[Sunday night hotel and dinner reimbursable under standard caps.\
                  *Condition*: Manager pre-approval required.]
                ]
              )
            ],
            [
              #text(10pt, weight: "bold", fill: rgb("#dc2626"))[NO  ↓]
              #v(0.3em)
              #block(
                fill: rgb("#fee2e2"),
                stroke: 1.5pt + rgb("#dc2626"),
                radius: 4pt,
                inset: 8pt,
                [
                  #text(8.5pt, weight: "bold", fill: rgb("#991b1b"))[STRICTLY DISALLOWED]\
                  #v(0.2em)
                  #text(7.5pt)[Treated as personal leisure (bleisure).\
                  Zero reimbursement for weekend lodging, meals, or transit.]
                ]
              )
            ]
          )
        ]
      )

      #v(1em)
      #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
      #v(0.4em)
      #text(8pt, fill: rgb("#64748b"))[
        *Note*: This visual flowchart is the sole binding authority for weekend and holiday reimbursement determinations at Noice & Toit LLP.
      ]
    ]
  )
]
