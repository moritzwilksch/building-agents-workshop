#import "template.typ": card-do, card-dont

= Decision Flowcharts and Approval Diagrams

== The Visual Decision Architecture

Certain operational expense categories involve conditional logic, multi-factor dependencies, and strict thresholds that cannot be adequately captured through static prose without introducing conflicting interpretations.

To maintain unambiguous standards across all offices and client engagements, Noice & Toit LLP mandates the use of visual decision flowcharts. The diagrams presented in this chapter serve as the exclusive binding authority for:
+ Weekend and statutory holiday travel eligibility determinations.
+ Group dining categories, per-person caps, and alcohol allowances.
+ Truffle and luxury-ingredient dishes on any restaurant bill.

#card-do("Inspect the visual flowcharts directly")[
  Review the decision branches in Figures 1, 2, and 3 carefully before committing funds or submitting your claim. To prevent conflicting interpretations, no written text summary of these decision branches is provided anywhere in this handbook. The visual graphics below are the sole source of binding policy for these scenarios.
]

#card-dont("Rely on text summaries or verbal exemptions")[
  Do not search for alternative textual descriptions of weekend travel rules, dining caps, or the truffle rule. If a claim does not satisfy the visual decision tree, the claim is rejected or adjusted by Finance.
]

== Weekend and Statutory Holiday Travel Approval Flowchart

All receipts dated on a Saturday, Sunday, or declared public holiday, and all hotel nights beginning on such a day, are audited strictly against the visual logic set forth in Figure 1. The facts the flowchart asks about must be stated in the submission note.

#v(1em)

#figure(
  image("figures/figure1-weekend.png", width: 100%),
  caption: [Figure 1: Weekend and Public Holiday Travel Approval Flowchart],
) <fig:weekend-flowchart>

#v(1em)

== Dining, Entertainment, and Beverage Approval Matrix

All meals, whether solo, internal, or hosted, are evaluated against the multi-factor criteria in Figure 2. The dining category is determined from the attendee composition stated in the note (Chapter 8).

#v(1em)

#figure(
  image("figures/figure2-dining.png", width: 100%),
  caption: [Figure 2: Approval Policy Flowchart -- Dining, Entertainment & Alcohol Matrix],
) <fig:dining-matrix>

#v(1.5em)

== Truffle Policy Flowchart

Every restaurant line item whose description mentions truffle is screened under Figure 3 before the dining caps in Figure 2 are applied. A dish that reaches a red branch is deducted at its gross line price.

#v(1em)

#figure(
  image("figures/figure3-truffle.png", width: 100%),
  caption: [Figure 3: Truffle Policy Flowchart -- Luxury Ingredient Screening],
) <fig:truffle-flowchart>

#v(1.5em)

== Navigating Edge Cases and Escalation Procedures

When a proposed client engagement or emergency travel scenario presents an unprecedented set of facts that does not clearly fit into the branches of Figures 1 to 3:
- The employee must prepare a short written briefing note outlining the client context, financial scale, and operational urgency.
- The briefing note must be submitted to the Practice Group Leader and the Head of Global Finance for joint determination.
- Verbal determinations or informal email notes from colleagues will not be accepted during retrospective compliance audits.

== Governance of the Visual Decision Standards

The diagrams reproduced in this chapter are controlled documents of the firm. They are not illustrative decorations, and they are not owned by whichever team happened to commission them. Like the financial policies they encode, the graphics are subject to formal custody, version control, scheduled review, and attestation. This section describes how the visual standards themselves are governed. It deliberately says nothing about what any individual branch decides; for that, consult the figures.

The controlling body is the Diagram Standards Board, a standing committee chaired by the Head of Global Finance and staffed by one representative each from People Operations, the Records Office, the Travel Desk, and the Practice Group secretaries. The Board meets quarterly and maintains a register of every controlled graphic in circulation. Membership is recorded in the Board's minute book, which the Records Office holds on behalf of the Audit Committee.

=== Ownership and Custody

Every controlled graphic has exactly one accountable owner and one deputy. Ownership is a role, not a person: when a named individual leaves the firm or changes practice, the role transfers automatically to the deputy until the Board confirms a permanent appointment. The master copies of all figures live in the Records Office document system under a single collection; copies saved to laptops, shared drives, or slide decks are working copies by definition and carry no authority. If a working copy and the master disagree, the master governs, and the discrepancy is reported under the procedure later in this section.

#table(
  columns: (auto, auto, auto),
  fill: (x, y) => if y == 0 { gray.lighten(60%) },
  [Figure], [Accountable owner], [Deputy custodian],
  [Figure 1 -- non-working-day travel logic], [Travel Desk], [Practice Group secretaries],
  [Figure 2 -- dining and entertainment logic], [People Operations], [Head of Global Finance],
  [Figure 3 -- luxury-ingredient screening logic], [Head of Global Finance], [Records Office],
  [Collection index and naming conventions], [Records Office], [Diagram Standards Board chair],
  [Alt-text catalogue], [People Operations], [Records Office],
  [Translation masters], [Records Office], [Diagram Standards Board],
)

=== Version Control and Change Management

Controlled graphics carry a two-part version mark: a whole number for a change in decision logic and a decimal for a change in presentation only. A decimal increment may alter colour, typography, or layout; it may never alter what a branch concludes. A whole-number increment reflects a substantive amendment and requires a recorded vote of the Diagram Standards Board, minuted with the rationale and the effective quarter. Amended figures enter force at the start of the quarter announced in the minute book, never mid-quarter, so that claims are always audited against one unambiguous version for the period they cover.

Retired versions are not deleted. The Records Office preserves superseded masters in the archive collection, marked in the register with their effective and retirement quarters, so that an audit of a past period can reconstruct exactly which logic applied. Only the Board may withdraw a figure entirely, and only by minute.

#table(
  columns: (auto, auto, auto, auto),
  fill: (x, y) => if y == 0 { gray.lighten(60%) },
  [Change class], [Effect on decision logic], [Approval required], [Register entry],
  [Presentation revision], [None permitted], [Owner plus Records Office], [Decimal increment, noted],
  [Substantive amendment], [Authorised branch change], [Board vote, minuted], [Whole-number increment],
  [Erratum (drafting fault)], [Clarification only], [Owner plus Board chair], [Whole-number increment],
  [Withdrawal], [Figure ceases to apply], [Board vote, minuted], [Register marked retired],
  [Custodial transfer], [None], [Board confirmation], [Owner and deputy updated],
)

=== Periodic Review

No controlled graphic may run a full fiscal year without review, whether or not anything changed. The Board's standing calendar fixes the review quarter for each figure; the review examines legal developments, office feedback, audit findings, and rendering quality. A review that concludes no amendment is needed is recorded as a review with no action, which is a real outcome and is minuted with the same care as an amendment. Skipping a scheduled review is a reportable control failure and is escalated to the Audit Committee at its next sitting.

#table(
  columns: (auto, auto, auto),
  fill: (x, y) => if y == 0 { gray.lighten(60%) },
  [ artefact ], [Review cadence], [Reviewer of record],
  [Figure 1 -- non-working-day travel logic], [Twice per fiscal year], [Travel Desk],
  [Figure 2 -- dining and entertainment logic], [Twice per fiscal year], [People Operations],
  [Figure 3 -- luxury-ingredient screening logic], [Every quarter], [Head of Global Finance],
  [Alt-text catalogue], [Twice per fiscal year], [People Operations],
  [Translation masters], [Every fiscal year], [Records Office],
  [Board minute book], [Every fiscal year], [Audit Committee],
)

=== Accessibility and Alt-Text Requirements

A decision standard that some employees cannot read is no standard at all. Each controlled graphic ships with a written alternative description held in the alt-text catalogue, maintained by People Operations to the firm's accessibility convention. The catalogue entry states, in prose, the entry conditions, the decision points, and the possible outcomes of the figure -- in full sentences, at reading level, without reference to colour alone as the carrier of meaning. Colour-blind-safe palettes are mandatory for all new masters; a figure whose branches are distinguishable only by hue fails review on that ground alone. Screen-reader users must be able to reconstruct the complete decision path from the catalogue entry, which is why catalogue drafting is a named custodial duty and not a favour.

#table(
  columns: (auto, auto),
  fill: (x, y) => if y == 0 { gray.lighten(60%) },
  [Catalogue element], [Requirement],
  [Entry conditions], [Stated in full prose, no abbreviation],
  [Decision points], [Enumerated in the order they appear],
  [Possible outcomes], [Each named explicitly, none merged],
  [Colour reliance], [Prohibited as sole carrier of meaning],
  [Palette], [Colour-blind-safe for all new masters],
  [Reading level], [Plain office prose, complete sentences],
  [Review sign-off], [People Operations, countersigned by Records Office],
)

=== Translation and Multilingual Distribution

The English masters are the binding versions in every office. Where an office operates principally in another language, the Records Office commissions a translation of the figures and the alt-text catalogue from an approved external provider, and the translation is checked by a second linguist before release. Translations are working aids: they carry a prominent notice, in both languages, that the English master prevails wherever readings diverge. A divergent reading discovered in circulation is treated as a discrepancy and reported under the procedure below, not argued out locally between colleagues in a corridor.

The Records Office also maintains the distribution list for each figure. Offices and shared inboxes on the list receive amended masters automatically on the effective date; anyone else who wants the current version retrieves it from the Records Office collection. Printing a figure and pinning it above a desk is permitted and even encouraged, provided the printout carries the version mark and is replaced when the register shows a newer one. A pinned printout of a retired version is a compliance finding waiting to happen, and the audit team finds them with depressing regularity.

=== Training and Attestation

People Operations includes the correct use of the controlled graphics in induction training for all fee-earning and finance staff. The training module explains what the figures are, where the masters live, how the version mark works, and how to read a branch to its outcome; it does not rehearse individual branches, which would only create a second, drift-prone copy of the logic. Staff attest annually, as part of the standing compliance attestation, that they know where the current masters are held and that they will consult them before committing funds in the categories the figures govern. Practice Group Leaders attest on behalf of joiners and seconded staff in their groups.

#table(
  columns: (auto, auto, auto),
  fill: (x, y) => if y == 0 { gray.lighten(60%) },
  [Module], [Audience], [Cadence],
  [Using the visual standards], [All fee-earning and finance staff], [Induction, then annual refresh],
  [Custodial duties], [Owners, deputies, secretaries], [On appointment],
  [Alt-text drafting], [Catalogue custodians], [On appointment, then on convention change],
  [Register and archive handling], [Records Office staff], [Every fiscal year],
  [Discrepancy reporting], [All staff], [Induction],
)

=== Reporting Discrepancies and Escalation

Discrepancies in the graphics themselves -- a rendering fault, a branch that cannot be resolved as drawn, a working copy that disagrees with the master, a translation that reads differently -- are reported to the Records Office through the standard service line, quoting the figure number and version mark. The Records Office acknowledges within a small number of business days, issues an interim reading signed by the Board chair where a claim would otherwise stall, and places the matter before the Board at its next sitting. Interim readings bind until the next whole-number increment and are filed with the minute book.

Staff do not adjudicate discrepancies themselves, do not improvise a branch the figure does not contain, and do not treat a colleague's confident recollection of an outcome as authority. The hierarchy is simple and is enforced in that order: the current master, then a signed interim reading, then nothing.

#table(
  columns: (auto, auto, auto),
  fill: (x, y) => if y == 0 { gray.lighten(60%) },
  [Situation], [First step], [Decides],
  [Rendering fault in a distributed copy], [Report to Records Office], [Records Office],
  [Working copy disagrees with master], [Discard working copy], [Master, by definition],
  [Branch unresolvable as drawn], [Report, request interim reading], [Board chair, in writing],
  [Translation diverges from master], [Report to Records Office], [English master],
  [Repeated or systemic fault], [Escalate to Audit Committee], [Audit Committee],
)

=== Archiving and the Long Memory

The Records Office retains every master, minute, interim reading, and register entry for the full retention period set out in the firm's records schedule. The archive exists because the figures change and the audit of a past claim does not: an examiner reconstructing last year's determination must be able to summon the exact graphic, and the exact version mark, that governed the date on the receipt. The archive is indexed by figure, version, and effective quarter, and the Audit Committee samples it annually. A governance system whose history cannot be produced on demand is a filing cabinet with delusions, and the firm does not operate one of those.
