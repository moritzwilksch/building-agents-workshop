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

#let decision(body) = block(
  width: 100%,
  fill: rgb("#fef3c7"),
  stroke: 1.5pt + rgb("#d97706"),
  radius: 5pt,
  inset: 9pt,
  text(weight: "bold", fill: rgb("#92400e"))[#body],
)
#let ok(title, body) = block(
  width: 100%,
  fill: rgb("#dcfce7"),
  stroke: 1.5pt + rgb("#16a34a"),
  radius: 5pt,
  inset: 9pt,
  [
    #text(weight: "bold", fill: rgb("#14532d"), size: 10pt)[#title]\
    #v(0.2em)
    #text(8.5pt)[#body]
  ],
)
#let bad(title, body) = block(
  width: 100%,
  fill: rgb("#fee2e2"),
  stroke: 1.5pt + rgb("#dc2626"),
  radius: 5pt,
  inset: 9pt,
  [
    #text(weight: "bold", fill: rgb("#991b1b"), size: 10pt)[#title]\
    #v(0.2em)
    #text(8.5pt)[#body]
  ],
)
#let arrow = text(14pt, fill: rgb("#64748b"))[↓]
#let yes = text(11pt, weight: "bold", fill: rgb("#16a34a"))[YES  ↓]
#let no = text(11pt, weight: "bold", fill: rgb("#dc2626"))[NO  ↓]

#align(center)[
  #block(
    width: 100%,
    stroke: 1.5pt + rgb("#0f172a"),
    radius: 8pt,
    fill: rgb("#f8fafc"),
    inset: 16pt,
    [
      #text(13pt, weight: "bold", fill: rgb("#0f172a"))[
        Figure 3: Truffle Policy Flowchart -- Luxury Ingredient Screening
      ]
      #v(0.3em)
      #text(9pt, fill: rgb("#64748b"))[
        Applied to every restaurant line item mentioning truffle, before the dining caps of Figure 2
      ]
      #v(1em)

      #block(
        width: 80%,
        fill: rgb("#dbeafe"),
        stroke: 1.5pt + rgb("#2563eb"),
        radius: 5pt,
        inset: 9pt,
        [#text(weight: "bold", fill: rgb("#1e3a8a"))[START: Line item description mentions truffle (Trüffel, tartufo, truffe, truffle oil, truffle butter, shaved truffle ...)]]
      )

      #v(0.5em) #arrow #v(0.5em)

      // Decision 1
      #block(width: 85%, decision[Step 1: Is the line a pure truffle supplement or upcharge? ("add shaved truffle", "truffle supplement", "extra truffle")])

      #v(0.6em)
      #grid(
        columns: (1fr, 1fr),
        gutter: 14pt,
        [
          #yes
          #v(0.4em)
          #bad("DEDUCT THE SUPPLEMENT")[The upcharge line is deducted in full. The dish it was added to is screened separately from Step 2.]
        ],
        [
          #no
          #v(0.4em)
          #text(9pt, fill: rgb("#475569"))[Continue to Step 2.]
        ]
      )

      #v(0.8em)
      #line(length: 60%, stroke: 0.5pt + rgb("#cbd5e1"))
      #v(0.8em)

      // Decision 2
      #block(width: 85%, decision[Step 2: Is the dish a main course? A side, starter, shared plate, garnish, sauce, fries, dessert, or bar snack is not a main.])

      #v(0.6em)
      #grid(
        columns: (1fr, 1fr),
        gutter: 14pt,
        [
          #no
          #v(0.4em)
          #ok("REIMBURSABLE")[Sides, starters, and desserts with truffle are ordinary food. Normal dining caps of Figure 2 apply.]
        ],
        [
          #yes
          #v(0.4em)
          #text(9pt, fill: rgb("#475569"))[Continue to Step 3.]
        ]
      )

      #v(0.8em)
      #line(length: 60%, stroke: 0.5pt + rgb("#cbd5e1"))
      #v(0.8em)

      // Decision 3
      #block(width: 85%, decision[Step 3: Is the unit price of the main strictly below €40.00 / \$45.00 / £35.00 per portion?])

      #v(0.6em)
      #grid(
        columns: (1fr, 1fr),
        gutter: 14pt,
        [
          #yes
          #v(0.4em)
          #ok("REIMBURSABLE")[A modest truffle main is fine. Normal dining caps of Figure 2 apply.]
        ],
        [
          #no
          #v(0.4em)
          #bad("DEDUCT THE DISH")[The entire line (quantity × unit price) is deducted, plus any tax charged on top of it. The rest of the bill continues to Figure 2.]
        ]
      )

      #v(1em)
      #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
      #v(0.4em)
      #text(8pt, fill: rgb("#64748b"))[
        *Note*: This flowchart is the sole binding authority for truffle dishes at Noice & Toit LLP. It applies to solo meals, internal team meals, and client hospitality alike. Minibar truffle snacks are minibar items and are deducted under Chapter 6 regardless of this figure.
      ]
    ]
  )
]
