// Shared template and styling for the Corporate Travel & Expense Policy Handbook

#let corporate-handbook(
  title: "Corporate Travel & Expense Reimbursement Policy",
  subtitle: "Global Guidelines, Spending Thresholds & Compliance Procedures",
  version: "4.2",
  effective-date: "January 1, 2024",
  organization: "Apex Global Technologies Inc.",
  body,
) = {
  // Page configuration
  set page(
    paper: "a4",
    margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
    header: context {
      let page-num = counter(page).get().first()
      if page-num > 2 {
        text(9pt, fill: luma(100))[
          #organization -- #title
          #h(1fr)
          v#version
        ]
        v(-0.5em)
        line(length: 100%, stroke: 0.5pt + luma(180))
      }
    },
    footer: context {
      let page-num = counter(page).get().first()
      if page-num > 2 {
        line(length: 100%, stroke: 0.5pt + luma(180))
        v(-0.5em)
        text(9pt, fill: luma(100))[
          Strictly Confidential -- Internal Corporate Use Only
          #h(1fr)
          Page #counter(page).display("1")
        ]
      }
    },
  )

  // Typography settings
  set text(
    font: ("Helvetica", "Arial"),
    size: 10pt,
    fill: rgb("#1f2937"),
  )
  set par(
    justify: true,
    leading: 0.7em,
  )

  // Heading numbering and styling
  set heading(numbering: "1.1")
  show heading.where(level: 1): it => block(
    breakable: false,
    above: 1.5em,
    below: 0.8em,
    [
      #text(16pt, weight: "bold", fill: rgb("#0f172a"))[#it]
      #v(0.2em)
      #line(length: 100%, stroke: 1.5pt + rgb("#2563eb"))
    ]
  )
  show heading.where(level: 2): it => block(
    breakable: false,
    above: 1.2em,
    below: 0.6em,
    text(12pt, weight: "bold", fill: rgb("#1e3a8a"))[#it]
  )
  show heading.where(level: 3): it => block(
    breakable: false,
    above: 1em,
    below: 0.4em,
    text(10.5pt, weight: "semibold", fill: rgb("#1e293b"))[#it]
  )

  // Cover Page
  align(center + horizon)[
    #block(
      width: 100%,
      fill: rgb("#f8fafc"),
      inset: 3em,
      radius: 8pt,
      stroke: 1pt + rgb("#e2e8f0"),
      [
        #text(12pt, tracking: 2pt, weight: "bold", fill: rgb("#2563eb"))[
          #upper(organization)
        ]
        #v(1.5em)
        #text(24pt, weight: "bold", fill: rgb("#0f172a"))[
          #title
        ]
        #v(0.8em)
        #text(12pt, fill: rgb("#475569"))[
          #subtitle
        ]
        #v(2em)
        #line(length: 40%, stroke: 2pt + rgb("#2563eb"))
        #v(2em)
        #grid(
          columns: (auto, auto),
          column-gutter: 2em,
          row-gutter: 0.8em,
          align: (right, left),
          [#text(weight: "bold")[Version:]], [#version],
          [#text(weight: "bold")[Effective Date:]], [#effective-date],
          [#text(weight: "bold")[Applies To:]], [All Employees, Contractors & Subsidiaries],
          [#text(weight: "bold")[Policy Owner:]], [Global Finance & Compliance Operations],
          [#text(weight: "bold")[Document ID:]], [POL-CORP-EXP-2024-V4],
        )
      ]
    )
  ]

  pagebreak()

  // Table of Contents
  {
    set page(footer: context {
      let page-num = counter(page).get().first()
      line(length: 100%, stroke: 0.5pt + luma(180))
      v(-0.5em)
      text(9pt, fill: luma(100))[
        Internal Corporate Use Only
        #h(1fr)
        Page #counter(page).display("i")
      ]
    })
    counter(page).update(1)

    text(18pt, weight: "bold", fill: rgb("#0f172a"))[Table of Contents]
    v(1em)
    outline(
      title: none,
      indent: 1.5em,
      depth: 2,
    )
  }

  pagebreak()
  counter(page).update(1)

  body
}

// Rule callout box helper
#let policy-rule(id, title, body) = block(
  width: 100%,
  stroke: (left: 4pt + rgb("#2563eb"), rest: 0.5pt + rgb("#cbd5e1")),
  fill: rgb("#f8fafc"),
  inset: (x: 12pt, y: 10pt),
  radius: (right: 4pt),
  breakable: false,
  [
    #grid(
      columns: (1fr, auto),
      [
        #text(weight: "bold", fill: rgb("#1e3a8a"), size: 10.5pt)[#title]
      ],
      [
        #box(
          fill: rgb("#dbeafe"),
          inset: (x: 6pt, y: 2pt),
          radius: 3pt,
          text(8pt, weight: "bold", fill: rgb("#1d4ed8"))[#id]
        )
      ]
    )
    #v(0.4em)
    #body
  ]
)

// Warning / Disallowed callout box helper
#let policy-warning(id, title, body) = block(
  width: 100%,
  stroke: (left: 4pt + rgb("#dc2626"), rest: 0.5pt + rgb("#fecaca")),
  fill: rgb("#fef2f2"),
  inset: (x: 12pt, y: 10pt),
  radius: (right: 4pt),
  breakable: false,
  [
    #grid(
      columns: (1fr, auto),
      [
        #text(weight: "bold", fill: rgb("#991b1b"), size: 10.5pt)[#title]
      ],
      [
        #box(
          fill: rgb("#fee2e2"),
          inset: (x: 6pt, y: 2pt),
          radius: 3pt,
          text(8pt, weight: "bold", fill: rgb("#b91c1c"))[#id]
        )
      ]
    )
    #v(0.4em)
    #body
  ]
)
