#import "template.typ": card-do, card-dont

= Approval Workflows and Authority Limits

== The Delegation of Authority (DoA) Framework

Noice & Toit LLP maintains a structured Delegation of Authority framework designed to balance operational efficiency with robust financial oversight. Every expenditure incurred on behalf of the firm must be reviewed and approved by an authorized manager before reimbursement or invoice settlement can take place.

Our approval hierarchy ensures that spending decisions are evaluated by individuals with direct visibility into practice group budgets, client billing arrangements, and firm-wide fiscal targets.

== Approval Tiers and Limits

The approval matrix is based on the total monetary value of an individual expense report:

=== Tier 1: Up to €1,000 / \$1,000
- *Authorized Approver*: Direct Line Manager or Engagement Manager.
- *Scope*: Routine local travel, day-to-day client dining, standard office supplies, and short domestic trips.
- *Review Criteria*: Verification of receipts, confirmation that charges align with project scope, and adherence to daily per diem caps.

=== Tier 2: €1,001 to €5,000 / \$1,001 to \$5,000
- *Authorized Approver*: Department Director, Practice Group Leader, or Partner-in-Charge.
- *Scope*: Multi-day domestic travel, regional client audits, group team events, and cross-border European transit.
- *Review Criteria*: Budget availability, client cost recovery terms, and overall travel proportionality.

=== Tier 3: Over €5,000 / \$5,000
- *Authorized Approver*: Practice Vice President and Head of Global Finance.
- *Scope*: Intercontinental client engagements, major conference sponsorships, high-value technical procurement, and extended overseas assignments.
- *Review Criteria*: Strategic necessity, senior partner alignment, and executive committee compliance.

#card-do("Route reports to the manager funding the expenditure")[
  When submitting your expense claim, confirm that the routing destination corresponds to the budget owner responsible for the project code. If your trip was funded by another practice group, route the report to that group's lead manager.
]

#card-dont("Self-approve your own claims")[
  Under no circumstances may an individual approve their own expense claim, regardless of corporate title, seniority, or equity partner status. Even Managing Partners must have their expense claims approved by the Audit Committee Chair or Chief Operating Officer.
]

== Pre-Approval Requirements for Exceptional Travel

Certain high-cost or high-risk activities require written authorization before travel is booked or commitments are made with vendors.

#card-do("Secure written pre-approval before booking high-value travel")[
  Obtain written confirmation (via email or ticketing workflow) from your Practice Leader before booking international flights, team offsites, or any purchase exceeding €2,500 / \$2,500. State in the submission note who approved the purchase and in what role (for example, "pre-approved by the Head of Engineering"). Finance accepts this statement at face value and verifies it in retrospective audits.
]

#card-dont("Commit firm resources without prior sign-off")[
  Do not sign agreements with venues, caterers, or travel agencies without prior budget approval. Commitments entered into without pre-approval may be rejected, leaving the individual personally liable for deposits or cancellation charges.
]

== Reviewer Duties and Verification Standards

Approving managers bear personal responsibility for the integrity of the claims they endorse. Managers should never treat expense approval as a rubber-stamp administrative formality.

=== Checklist for Approving Managers
Before clicking the digital approval button in the Expense Portal, every reviewing manager must verify:
- *Legitimacy*: Does the expense support a genuine business requirement of Noice & Toit LLP or a billable client matter?
- *Completeness*: Are all receipts attached, fully itemized, legible, and matched to claim line items?
- *Policy Conformance*: Do hotel rates, meal costs, and travel classes comply with the limits set out in this handbook?
- *Allocation*: Are billable project codes, task numbers, and non-billable cost centers correctly assigned?
- *Exception Flagging*: Are any non-reimbursable items (such as minibar charges, alcohol on solo meals, spa treatments, or excess tips) properly removed or deducted following the calculation steps in Chapter 2?

== Out-of-Office and Delegation Rules

When an approving manager is away on annual leave, extended medical leave, or intense trial commitments:
- The manager must set up a formal delegation delegate in the Expense Portal before departing.
- Approvals may only be delegated to peers of equal seniority or to an immediate superior. Delegating approval authority downward to direct reports is strictly prohibited.
- Temporary delegations expire automatically after thirty days unless renewed in writing through People Operations.

== The Delegation of Authority Register

The Delegation of Authority framework is administered through a living register maintained by the Records Office in conjunction with Finance and People Operations. The register records, for every approving role in the firm, the categories of commitment that role may authorize, the practice groups or cost centers over which the authority extends, and the body consulted before each authorization is exercised. The register is the single point of reference when a question arises about who may approve what; verbal assurances, habit, and organizational folklore carry no weight in an audit.

Entries in the register are created, amended, and retired only through a written request countersigned by the Chief Operating Officer. When a manager changes role, transfers between practice groups, or leaves the firm, People Operations updates the register within a reporting cycle and confirms the change to the affected manager in writing. An approval exercised by a person whose register entry has lapsed is treated as undelegated and must be re-endorsed by the correct holder before the claim proceeds to payment.

#card-do("Check the register before routing an unusual request")[
  If a commitment does not fit neatly into an existing approval tier, consult the register entry for the category concerned before submitting. The register names the holding role, not the incumbent; where two managers share a role, either may act unless the entry records a joint-signature condition.
]

== Authority Sub-Tiers for Non-Financial Approvals

Not every approval in the firm is monetary, and the tier matrix above does not exhaust the approvals a matter may require. For contracts, data access, travel risk, and supplier onboarding, authority is defined by role and category rather than by value. These sub-tiers run alongside the financial tiers: a commitment that carries both a financial and a non-financial dimension requires sign-off under each.

#table(
  columns: (1.2fr, 1.4fr, 1.3fr, 1.4fr, 1fr),
  align: (left, left, left, left, center),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Authority Area*][*Holding Role*][*Consulted Body*][*Record Produced*][*Cadence*],
  [Standard client contract], [Practice Group Leader], [General Counsel], [Signed execution memo], [Per matter],
  [Non-standard contract terms], [Practice Vice President], [General Counsel], [Counsel review note], [Per matter],
  [Confidential data access], [Department Director], [Information Security Office], [Access grant log entry], [Quarterly],
  [Client-system credentials], [Engagement Manager], [Information Security Office], [Credential issuance record], [Per engagement],
  [Elevated travel-risk destination], [Practice Vice President], [Travel Desk], [Risk clearance notice], [Per trip],
  [New supplier onboarding], [Department Director], [Procurement Review Panel], [Supplier due-diligence file], [Per supplier],
  [Supplier renewal or exit], [Department Director], [Procurement Review Panel], [Relationship review note], [Annual],
  [Practice-group tooling adoption], [Head of Global Finance], [Technology Steering Group], [Adoption decision memo], [Semi-annual],
  [Records disclosure to third parties], [General Counsel], [Audit Committee], [Disclosure register entry], [Per disclosure],
)

=== Contract Execution Authority

Only roles named in the register may sign or verbally accept terms on behalf of Noice & Toit LLP. Engagement Managers may confirm scope in writing within an executed master agreement, but any new agreement, amendment, or side letter belongs to the Practice Group Leader or above. Where counterparties press for same-day acceptance, the holding role may grant a conditional go-ahead in writing; the written record of that condition forms part of the engagement file and is retained by the Records Office.

=== Data Access and Tooling Authority

Access to client systems, restricted data rooms, and privileged internal datasets is granted by the holding role for the dataset concerned, on the advice of the Information Security Office. Access is granted for a stated engagement or purpose and lapses when that purpose ends; it is not carried forward informally between matters. The Information Security Office reconciles live access grants against the register each quarter and reports dormant grants to the Audit Committee.

=== Travel Risk Authority

The Travel Desk classifies destinations using the firm's risk rating, refreshed against published government guidance. Travel to an elevated-risk destination proceeds only after the Practice Vice President countersigns the trip plan prepared with the Travel Desk. The countersignature covers itinerary, contact arrangements, and check-in cadence; it does not alter the financial approval tiers, which continue to apply in the ordinary way.

=== Supplier Onboarding Authority

No supplier, contractor, or platform is engaged before the Procurement Review Panel completes its due-diligence file. The file records the supplier's legal identity, insurance position, data-handling posture, and references, and names the Department Director who accepted it. Engaging a supplier ahead of onboarding shifts the engagement onto personal liability and is treated as a reportable control breach.

== Segregation of Duties in the Approval Chain

The firm's control environment rests on a simple principle: the person who orders, the person who approves, and the person who pays must never be the same person, and no single role may span two of those steps for the same commitment. In practice this means a manager who negotiates a supplier arrangement may not also approve the resulting invoices, and a consultant who prepares a claim may not route it to a delegate they control.

Segregation extends to the tools as well as the titles. Portal administrator rights, register-editing rights, and payment-release rights are held by three separate teams within Finance and the Technology Steering Group, and no standing exception permits one team to exercise another's rights. Where workload makes strict separation impractical in a small practice group, the matter is escalated to the Chief Operating Officer, who may appoint a peer from another group rather than relax the control.

#card-dont("Arrange approvals around a busy diary")[
  Approvals follow the register, not convenience. Routing a claim to whichever manager replies first, holding a claim open until a particular approver returns, or splitting a commitment so it lands beneath a senior role's attention are all treated as control breaches even when the underlying expense is entirely legitimate.
]

== Standing Delegation and Recall Procedure

In addition to the out-of-office arrangements described above, the Chief Operating Officer may grant a standing delegation to a named peer where a role is expected to be continuously occupied by two holders, for example in job-share arrangements or during a planned transition between incumbents. A standing delegation is recorded in the register, names both the delegating and the receiving role, and remains in force until recalled in writing. Either party may request recall through People Operations; recall takes effect on the day the updated register entry is published, not on the day the request was made.

Approvals exercised under any delegation must name the delegating role in the decision note. A delegate who extends, amends, or declines a commitment on the delegating role's behalf signs in that role's name and inherits the same documentation duties and the same exposure in retrospective audit.

== Review Service Levels and Escalation

Approving managers are accountable not only for the quality of their decisions but for their timeliness. The service levels below apply to every approval queue in the Expense Portal and the contract workflow. Where a service level cannot be met, the approver must record the reason in the queue notes before the escalation point passes; an unexplained breach is itself a reportable event, independent of whether the underlying claim is later found to be in order.

#table(
  columns: (1.4fr, 1.2fr, 1.6fr, 1.4fr),
  align: (left, center, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Queue*][*Service Level*][*Escalation Path*][*Escalation Owner*],
  [Routine expense report], [Three business days], [Line Manager, then Department Director], [People Operations],
  [Corrected or re-submitted report], [Two business days], [Department Director, then Practice Vice President], [People Operations],
  [Contract execution memo], [Five business days], [General Counsel, then Chief Operating Officer], [Records Office],
  [Data access grant], [Two business days], [Information Security Office duty officer], [Technology Steering Group],
  [Travel-risk clearance], [Two business days], [Travel Desk duty manager, then Practice Vice President], [Travel Desk],
  [Supplier onboarding file], [Ten business days], [Procurement Review Panel chair, then Department Director], [Procurement Review Panel],
  [Register change request], [Five business days], [Chief Operating Officer], [Records Office],
)

Escalation is automatic and unremarkable; it is a routing mechanism, not a censure. An escalated matter carries a flag that names the escalation owner, and the receiving role acquires the full approval duty, including the documentation standards below.

== Approver Training and Certification

No employee may exercise approval authority before completing the Approver Certification course run by People Operations. The course covers the DoA framework, the reviewer checklist, segregation of duties, and the documentation standards set out below, and concludes with a scenario assessment marked by Finance. Certification attaches to the person, not the role: a manager moving to a new practice group retains certification but must re-confirm their register entry before approving in the new cost center.

Certification is renewed every two years, and People Operations runs a short refresher whenever a handbook revision materially changes the approval chapters. An approver whose certification has lapsed is suspended from the approval queues automatically; claims routed to them hold in the queue rather than fail, and the service-level clock pauses until certification is restored. Finance samples a small selection of decisions from every certified approver each year, and persistent documentation shortfalls are returned to People Operations for targeted retraining.

== Decision Documentation Standards

Every approval decision produces a record, and the record is the decision as far as the firm is concerned. A decision note should let a colleague with no prior knowledge of the matter understand what was approved, on whose authority, and why the commitment was proportionate to its purpose. Notes reading "approved", "ok", or "please process" are treated as absent for audit purposes, and the decision is re-taken in the approver's presence if the shortfall is material.

A complete decision note contains, at minimum: the matter and cost-center reference; the authority relied upon, citing the register entry; the consulted body, where the sub-tier table requires one; the principal reason for the decision; and any condition attached to it. Where an approver adjusts a claim rather than accepting or rejecting it outright, the note must state which lines were adjusted and the reason for each. Decision notes are retained by the Records Office for the firm's standard retention period and are disclosable to the external auditors on request.

#card-do("Write the note for the auditor who was not there")[
  Draft every decision note as if the reader is a colleague reconstructing the matter two years later. Name the authority, state the reason, record the condition. A note that survives that test will also survive the annual sample review without follow-up.
]

== Frequently Asked Questions

*Q: What happens if an expense report is rejected by my manager?*\
A: If an approver rejects a report, the portal sends an automated notification with the manager's written feedback. You can edit line items, attach missing receipts, update cost centers, and re-submit the report directly through the workflow.

*Q: Can an approving manager approve part of a report and reject part of it?*\
A: Yes. Managers can approve valid lines and place contentious lines on hold or adjust them downward. Approved items move directly to payment, while flagged lines return to the employee for explanation or correction.

*Q: How long does manager review typically take?*\
A: Managers are expected to review pending expense reports within five business days of submission. If a report sits unreviewed for more than seven business days, the Expense Portal escalates it automatically to the next management level.
