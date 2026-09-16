#import "template.typ": card-do, card-dont

= Documentation, Retention, and Approval Orientation

This chapter collects the paperwork expectations that surround a claim. It restates requirements from Chapters 2 and 3 and adds the retention schedule that Global Finance maintains for audit purposes.

#card-dont("Change a reimbursement rule with this chapter")[
  Nothing here sets or changes an amount, a cap, or an eligibility rule. Chapters 2 and 3 remain authoritative for documentation and approval.
]

== Documentation Requirements by Receipt Type

#table(
  columns: (1.5fr, 2.2fr, 2.2fr, 1.4fr),
  align: (left, left, left, center),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Receipt Type*][*Mandatory Elements*][*Submission Note Must State*][*Governing Reference*],
  [Airline e-ticket], [Passenger name, routing, cabin, fare and tax breakdown], [Business purpose; approver for high-value travel], [Chapter 4 governs], 
  [Rail ticket], [Origin, destination, class, fare], [Destination and purpose], [Chapter 5 governs], 
  [Taxi or ride-hailing receipt], [Operator, date, time, fare], [Route and, where needed, a justification], [Chapter 5 governs], 
  [Rental car agreement], [Vehicle class, dates, daily rate], [Client site served and approval], [Chapter 5 governs], 
  [Fuel receipt], [Volume, amount, station], [The rental or pool vehicle it served], [Chapter 5 governs], 
  [Hotel folio], [Itemized room rate, city tax, incidentals, VAT number], [Business purpose and event if any], [Chapter 6 governs], 
  [Solo restaurant bill], [Itemized dishes and beverages, time], [Purpose if away from the office city], [Chapter 7 governs], 
  [Group restaurant bill], [Itemized dishes, beverages, guest count], [Purpose, external organizations, attendee count], [Chapter 8 governs], 
  [Commercial invoice], [Vendor name, VAT number, net, gross, line items], [Event name and budget owner where relevant], [Chapter 10 governs], 
  [Conference registration], [Attendee name, event dates, fee], [Business relevance to a matter], [Chapter 10 governs], 
  [Mileage log], [Departure, arrival, distance], [Client matter or purpose], [Chapter 5 governs], 
  [Parking receipt], [Garage, date, time, amount], [Vehicle and destination], [Chapter 5 governs], 
  [Baggage fee receipt], [Airline, flight, amount], [Reason the baggage was required], [Chapter 4 governs], 
  [Currency receipt], [Amount, currency, date], [The underlying business spend], [Chapter 12 governs], 
)

== Records Retention Schedule

Records are retained by Global Finance and are not the employee's responsibility, but employees may ask why a receipt is requested months after a claim.

#table(
  columns: (2.4fr, 1fr, 2fr),
  align: (left, center, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Record*][*Retention*][*Purpose*],
  [Airline ticket and boarding records], [7 years], [Tax substantiation], 
  [Hotel folios], [7 years], [Tax substantiation and VAT recovery], 
  [Restaurant and entertainment bills], [7 years], [Client hospitality audit], 
  [Commercial invoices and goods receipts], [10 years], [Asset and procurement audit], 
  [Corporate card statements], [7 years], [Reconciliation], 
  [Delegation of Authority approvals], [10 years], [Governance], 
  [Event pre-approval emails], [7 years], [Budget owner evidence], 
  [Travel risk assessments], [5 years], [Duty of care], 
  [Visa and immigration records], [5 years], [Regulatory], 
  [Incident and near-miss reports], [10 years], [Health and safety], 
  [Data protection impact assessments], [10 years], [Privacy governance], 
  [Supplier due diligence files], [10 years], [Anti-bribery], 
  [Currency conversion worksheets], [7 years], [Tax reconciliation], 
  [Training completion records], [5 years], [Compliance certification], 
  [Asset register updates], [10 years], [IT asset lifecycle], 
  [Sustainability travel data], [10 years], [Emissions reporting], 
  [Dispute resolution notes], [7 years], [Audit trail], 
  [Gift and hospitality registers], [10 years], [Anti-bribery], 
  [Insurance claim files], [10 years], [Claims handling], 
  [Expense audit samples], [7 years], [Quality assurance], 
)

== Approval Authority Orientation

This orientation table maps common purchases to the approval route. The Delegation of Authority in Chapter 3 governs; the route below is a finding aid only.

#table(
  columns: (2fr, 1.2fr, 1.4fr, 2fr),
  align: (left, center, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Scenario*][*Approval Tier*][*Approver*][*Notes*],
  [Solo meal within cap], [None beyond submission], [Expense portal], [Chapter 3 governs], 
  [Hotel within cap], [None beyond submission], [Expense portal], [Chapter 3 governs], 
  [Taxi within threshold], [None beyond submission], [Expense portal], [Chapter 3 governs], 
  [Domestic flight], [Tier 1], [Practice Leader], [Chapter 3 governs], 
  [International flight], [Tier 2], [Practice Leader in writing], [Chapter 3 governs], 
  [Team offsite], [Tier 2], [Department Director], [Chapter 3 governs], 
  [Client hospitality above cap], [Tier 2], [Budget owner], [Chapter 3 governs], 
  [Event materials], [Tier 2], [Budget owner], [Chapter 3 governs], 
  [Software request], [IT review], [IT Service Portal], [Chapter 3 governs], 
  [Hardware above threshold], [IT review], [IT Helpdesk ticket], [Chapter 3 governs], 
  [Rental car above intermediate], [Tier 2], [Named approver], [Chapter 3 governs], 
  [Conference travel], [Tier 1], [Practice Leader], [Chapter 3 governs], 
  [Candidate interview meal], [Tier 1], [Hiring manager], [Chapter 3 governs], 
  [Extended assignment], [Tier 3], [Head of Global Finance], [Chapter 3 governs], 
  [Relocation support], [Tier 3], [People Operations], [Chapter 3 governs], 
)

== A Note on Paperwork Discipline

A complete claim is the fastest claim. The most common cause of a delayed reimbursement is not a disputed rule but a missing folio page, an unnamed rental vehicle, or a note that assumes the reviewer already knows the client. Employees who attach the itemized receipt and state the facts the handbook asks for rarely wait long for payment.
