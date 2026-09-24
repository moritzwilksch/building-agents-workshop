#import "template.typ": card-do, card-dont

= Expense Submission and Documentation

== Overview of the Submission Process

Timely and accurate submission of expenses keeps our financial records current, supports accurate billing to clients, and ensures you get reimbursed quickly. All expense submissions at Noice & Toit LLP must be filed through the central Noice & Toit Expense Portal (accessible via single sign-on from your desktop or mobile device).

Each receipt is submitted as its own expense line. A line consists of exactly two things: the receipt image and a short submission note written by the employee. Finance evaluates every line on those two inputs alone.

== Deadlines and the Accounting Calendar

Our accounting team closes general ledger accounts at the end of each calendar month. Untracked expenses distort monthly departmental budgeting, delay billable client invoices, and create complications for quarterly tax returns.

#card-do("Submit expense reports within 30 days")[
  File your expense report within thirty calendar days of returning from a business trip or incurring a local out-of-pocket expense. Submitting reports promptly guarantees reimbursement in the next bi-weekly payroll cycle.
]

#card-dont("Hold claims longer than 60 days")[
  Do not hold receipts past sixty days. Reports submitted between 61 and 90 days after the expense date require formal written approval from your practice vice president. Claims submitted after 90 days are strictly forfeited and will not be reimbursed under any circumstance.
]

=== Fiscal Year-End Cut-Off Notice
Special cut-off rules apply at the end of our fiscal year (December 31st). All expenses incurred through December 15th must be submitted no later than December 20th to ensure costs are accrued into the correct tax year. Expenses incurred between December 16th and December 31st must be filed no later than the first Friday of January.

== Receipt Substantiation Standards

Both tax authorities (including the IRS, HMRC, and German Finanzamt) and our commercial clients require full substantiation before business deductions or reimbursements are recognized. A proof of payment must establish five core facts:
+ *Who*: The legal name and business address of the vendor. Hotel folios and commercial invoices must additionally show the vendor's VAT or tax registration number.
+ *When*: The date and, for restaurants and taxis, the time the transaction occurred.
+ *What*: An itemized list showing individual line items, service descriptions, unit costs, and quantities.
+ *How much*: The total gross amount paid, broken down by net price, applicable tax rates, and tips.
+ *Currency*: The exact currency in which the transaction was charged.

#card-do("Upload itemized merchant folios and bills")[
  Always request and upload the complete itemized bill. For restaurant visits, provide the detailed dining bill listing all dishes and beverages ordered. For hotels, upload the itemized checkout folio showing daily room charges, taxes, and incidentals.
]

#card-dont("Rely on credit card charge slips")[
  Never submit terminal charge slips showing only a merchant name, a total amount, and a masked card number. A card slip proves that money changed hands, but it does not prove what was purchased. Finance rejects any expense line supported only by a summary card slip, regardless of amount or explanation in the note.
]

== The Submission Note

The submission note is the only narrative Finance reads. No screenshots, e-mail threads, approval tickets, or card statements can be attached to an expense line; anything Finance needs to know must be stated in the note. Statements in the note are accepted at face value and audited retrospectively. A knowingly false statement is misconduct under Chapter 1.

#card-do("State the facts that unlock reimbursement")[
  Keep notes to one or two plain sentences and include the facts relevant to the receipt type:
  - *Restaurants and bars*: The business purpose, the external organization(s) present, and the total number of attendees including yourself. For a recruiting meal, the role being recruited and the number of candidates take the place of the organization name; job candidates are external guests under Chapter 8 and no employer need be named.
  - *Hotels*: The trip purpose. For nights falling on a weekend or public holiday, name the conference or client meeting (see Figure 1). For laundry or parking charges, state the garment incident or the vehicle (see Chapter 6).
  - *Taxis and ride-hailing*: Destination and purpose. For fares above the unjustified-ride threshold, state which justification in Chapter 5 applies.
  - *Fuel*: Identify the rental vehicle the fuel was for.
  - *Flights*: The trip purpose. For bookings made inside seven days of departure, the reason. For premium cabins, the qualifying condition from Chapter 4.
  - *Rail*: The trip purpose. For first-class rail, the qualifying condition from Chapter 5.
  - *Commercial invoices (equipment, supplies, event materials)*: What the items are for, the event or project name, and, where Chapter 10 requires it, the approver's name and department or the IT ticket number. The approver's job title is not required.
]

#card-dont("Leave the note blank or generic")[
  Notes such as "dinner", "business lunch", or "supplies" do not satisfy any documentation requirement. Where this handbook says a fact must be stated in the note and it is missing, Finance applies the less favorable branch of the rule. Routine transit (public transport, short taxi rides, standard rail tickets) may carry an empty note.
]

=== Notes We Have Actually Received
The Expense Auditing Team keeps an anonymized collection of memorable notes for training purposes. "Evening meal." is the most common entry and the least useful. "Emergency ducks, see Hamburg" has become shorthand for a note that assumes context the reader does not have. The best notes in the collection are short, specific, and slightly boring: "Lunch with 2 engineers from Acme (3 attendees total) to review the Q3 rollout plan." Aim for boring.

== Mobile Capture and Document Legibility

Most employees photograph receipts with smartphone cameras. The resulting image must be clear, legible, and suitable for formal tax inspection.

- Lay the receipt flat with adequate lighting and keep the entire receipt in frame, from the merchant header to the total footer.
- Thermal paper receipts from taxis, petrol stations, and cafes fade quickly; capture the photo within 24 hours of purchase.
- For multi-page hotel folios, upload every page in sequence.
- Finance may reject lines where amounts, line items, or the vendor cannot be read.

== How Finance Calculates the Reimbursable Amount

Finance applies the rules in this handbook in a fixed order so that every reviewer arrives at the same figure. The steps are:

+ *Eligibility check*. If the receipt is a summary card slip, or the expense category is prohibited outright (Chapter 11), the line is *rejected* and nothing further is calculated.
+ *Remove non-reimbursable line items*. Deduct every prohibited item (alcohol where not permitted, minibar, spa, personal goods, prohibited fees) at its gross line price. Where the receipt adds tax on top of the subtotal, also deduct the tax charged on that item at the rate shown for the line. Where prices already include tax, the gross line price is the deduction.
+ *Apply item caps*. Where a specific line is capped (a nightly room rate, a laundry charge, a hotel parking night, a tip), reimburse up to the cap and deduct the excess.
+ *Apply category caps*. Apply the per-meal, per-person, or per-day caps in Chapter 7, Figure 2, and Chapter 10 to what remains.
+ *Determine the outcome*. If nothing was deducted, the line is *approved* in full. If something was deducted but a positive amount remains, the line is *partially approved* for the remaining amount. If nothing remains, the line is *rejected*.

#card-do("Work through the steps yourself before submitting")[
  Employees may enter the net business amount they expect to receive. Finance recalculates every line independently, so a self-reduced claim does not shortcut the audit, but it does speed up settlement.
]

== Portal Workflow Mechanics

Every expense line moves through the same set of statuses in the Noice & Toit Expense Portal. The status is visible to the employee, the practice approver, and Finance at all times, and each transition is logged with a timestamp and the acting account. Understanding the workflow prevents the most common support requests to the Expense Desk: lines sitting quietly in *Draft* are not submitted, and lines in *Queried* do not progress until the employee responds.

#table(
  columns: (1fr, 1.2fr, 2fr, 1.6fr),
  align: (left, left, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Status*][*Set by*][*Meaning*][*Your next action*],
  [*Draft*], [Employee], [Line created but not filed. Not visible to Finance and not counted toward any filing date.], [Review the note and image, then submit.],
  [*Submitted*], [Employee], [Line filed and locked against silent edits. It now enters the review queue for the current period.], [None. Wait for review.],
  [*In Review*], [Finance], [A reviewer has picked up the line and is checking image, note, and rule application.], [None. Reviews are worked oldest-first.],
  [*Queried*], [Finance], [The reviewer needs one specific fact or a better image before deciding.], [Respond or correct within the query window (see below).],
  [*Resubmitted*], [Employee], [A corrected image or note has been filed in answer to a query.], [None. The line returns to the front of the queue.],
  [*Approved*], [Finance], [The line has passed review and is queued for settlement.], [None.],
  [*Settled*], [Payroll], [The reimbursable amount has been paid in a payroll cycle.], [None.],
  [*Rejected*], [Finance], [The line fails an eligibility or substantiation requirement outright.], [Read the rejection reason. Rejection of a line does not affect the rest of the report.],
)

#card-do("File drafts before the period closes")[
  A report left in *Draft* is, for accounting purposes, unfiled. The Expense Desk closes the submission queue for a period on the same calendar the ledger closes, and draft lines do not move. Open the portal, check for stranded drafts at the end of each business week, and file what is complete.
]

=== The Query Window

When a reviewer raises a query, the portal starts a response window of five business days. A query answered with the requested fact is usually resolved in a single pass. A query that lapses is not a rejection: the line returns to *Submitted* and rejoins the queue at its original filing date, but the reviewer's follow-up questions grow shorter and less patient. Employees with more than three lapsed queries in a rolling quarter are invited to a brief refresher session with the Expense Desk.

== Accounting-Period Closure and Accruals

At each month-end the Ledger Control Team must state, with evidence, which expenses were incurred in the month and which will settle later. Submitted lines that are still *In Review* at closure are accrued on the strength of the receipt image and the note alone; draft lines do not exist for this purpose and are simply absent from the accrual. Every absent line becomes a difference between the accrued figure and the actual figure that the Audit Committee reviews line by line. Small, recurring differences are treated as a process failure of the practice that produced them, not as rounding.

This is why the portal distinguishes so sharply between *Draft* and *Submitted*. An employee who photographs a receipt and leaves it on a phone has done nothing the Ledger Control Team can accrue. An employee who files a legible image with a plain note has given Finance everything needed to record the cost in the correct month, even if the review completes after closure. The note matters here more than anywhere else: during closure week, reviewers work from the note, not from follow-up e-mails, and a note that names the client, the occasion, and the attendees lets the line accrue to the right cost centre without a query.

=== The Accrual Narrative

For each month-end, Ledger Control publishes a short accrual narrative to practice leaders: what was filed on time, what arrived in the grace days after closure, and which practices account for the oldest unsettled lines. The narrative is factual and free of adjectives. It has nevertheless been described as the most quietly feared document in the firm, because its charts are sorted by practice name and the sort order is not alphabetical.

== Document-Imaging Standards

An image that Finance cannot read is, for review purposes, an image that does not exist. The portal accepts photographs and scans in JPEG, PNG, HEIC, and PDF form. Images must be captured at a resolution at which the merchant header, every line item, the tax breakdown, and the total footer are individually legible on a standard office monitor without zooming. If you must choose between a sharp photograph of two overlapping pages and a flat photograph of one page, take the flat photograph twice.

- *Colour*: Submit colour images wherever the receipt uses colour to carry meaning, as restaurant bills, hotel folios, and event invoices frequently do. Greyscale is acceptable for plain thermal rolls, which print in one colour anyway and fade to grey soon after.
- *Completeness*: The full receipt must be in frame. Foldouts, tear-off stubs, and the printed reverse of cards or vouchers must be captured as separate images and attached to the same line.
- *Orientation*: Portrait orientation, text upright. Rotated and mirrored images are the second most common cause of a legibility query, after blurred totals.
- *Multi-page folios*: Upload every page of a hotel folio or multi-page invoice, in page order, and check before submitting that no page is duplicated or missing. The review of a multi-page folio stalls if the page carrying the grand total is absent.

#card-do("Flatten, light, and frame before you shoot")[
  Lay the receipt on a flat, matte, lightly coloured surface. Use indirect light; direct light and camera flash both white out thermal paper. Hold the camera parallel to the page, fill the frame with the receipt, and tap to focus before capturing.
]

#card-dont("Staple, fold, or crumple and then photograph")[
  A photograph of a receipt still folded around a coffee cup, crossed by a staple shadow, or printed on paper that has been through a coat pocket captures the coat pocket as faithfully as the receipt. Ask for a reprinted invoice at the point of sale when the paper copy has suffered; most merchants reprint on request, and a reprint submitted instead of a rescue attempt saves everyone a query.
]

=== Long and Narrow Receipts

Parking garage tickets, fuel pump rolls, and some till rolls from continental train stations print in a strip longer than the scanner glass. Photograph these in overlapping segments, each segment showing a row of print that the next segment also shows, so the reviewer can verify that no strip is missing. Label the segments implicitly by uploading them in order against the same line; the portal stacks attachments in upload order.

== A Short Guide to Better Notes

Most queries are note queries. The reviewer had an image, had a rule, and lacked exactly one fact that only the employee knew. The fix costs one sentence at submission time and one review cycle otherwise. The patterns below are drawn from the Expense Auditing Team's training collection; the weak column reproduces the structure of the notes most often queried, and the strong column shows the shape Finance can act on without asking.

#table(
  columns: (1.2fr, 1.6fr, 2.2fr),
  align: (left, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Weak pattern*][*Why it queries*][*Stronger shape*],
  ["Evening meal."], [No purpose, no attendees, no counterparty. The reviewer must ask all three.], ["Evening table with the Kestrel LLP restructuring team, 4 attendees including me, to close the scope for phase two."],
  ["Taxi (see trip last week)."], [Assumes the reviewer reads across reports. They do not, and cross-report references are not visible in review.], ["Taxi from the client's Hamburg plant to the main station after the site walkthrough; return leg claimed on its own line."],
  ["Hotel as per booking."], ["As per" defers to a document the reviewer cannot open. The note is the only narrative there is.], ["Two nights for the Frankfurt audit close; checkout folio attached in full."],
  ["Client entertainment, you know the one."], [Reviewer folklore does not survive staff turnover, and it does not survive audits either.], ["Welcome supper for the visiting delegation from our Rotterdam partner office, 6 attendees including 2 partners."],
  ["Supplies for the thing we discussed."], [Conversational register, no noun, no project. Queries this note and cites the meeting invite in the same breath.], ["Whiteboard markers and flip-chart pads for the practice offsite planning session."],
  ["Same as my colleague's."], [Each line is reviewed on its own image and its own note, whoever else filed one.], ["Shared team table at the venue on the attached invoice; my portion of the bill, 5 attendees total."],
)

#card-do("Write for a reviewer who knows the rules but not your week")[
  The reviewer has the handbook open and your receipt on screen. What they cannot reconstruct is the occasion: who was there, what it was for, and which project or client it served. One or two plain sentences covering those facts will pass review unanswered nearly every time.
]

#card-dont("Argue the rules inside the note")[
  Notes that quote chapter and verse, pre-empt objections, or explain why a line "should obviously" be reimbursable in full read as advocacy, not documentation. State the facts and let the rules do their work. If you believe a line needs a judgement call, say so once, plainly, and name the practice vice president who agreed to it.
]

== Queries, Corrections, and Resubmission

A query is a request, not a penalty. The reviewer names the missing fact, the employee supplies it through the portal's response field or a corrected attachment, and the line resumes review. Corrections replace the original image or note; they do not append to it, so a resubmission should carry the complete, corrected version rather than a supplement. A line may pass through the query cycle more than once, but repeated queries on the same line trigger a review of the report as a whole, and patterns across reports trigger the refresher session described above.

Rejections follow queries and differ from them in one respect: the reviewer has decided, not asked. A rejection names the requirement that failed. Employees who believe a rejection rests on a misreading may appeal once, in writing, to the Expense Desk within the response window; appeals are decided by a second reviewer who had no part in the original decision, and their outcome is final. Note that appeal is available for misreading, not for disagreement with a rule.

=== Correspondence Tone

All portal correspondence, from either side, is dry, specific, and free of adjectives of surprise. Reviewers do not write "as you must know by now", and employees should not write "as I have explained repeatedly". The firm's correspondence standard is that any sentence would read identically if it were read aloud in a corridor to a colleague's face. Names are spelled as on the invoice, dates are written in full, and references to earlier messages cite them by date rather than by "above" or "see my last".

== Audit Trail and Archiving

Every status change, note revision, image replacement, query, response, and appeal on a line is retained by the Records Office as an immutable audit trail. Employees cannot delete a submitted line, and corrections are versioned rather than overwritten; the reviewer can always see what was originally filed. This is deliberate. Client auditors and the tax authorities named earlier in this chapter sample our expense records against the trail, and a gap in the trail is treated as a missing record even where a present record would have passed.

Archived reports remain retrievable by the filer and by Finance for the full retention period applicable in the filer's jurisdiction, and for longer where a client engagement or audit requires it. The Expense Desk publishes the retention schedule per office; where jurisdictions differ, the longest applicable period governs. Requests to expunge a filed line, however embarrassing its note, are declined without exception, on the ground that an expense system which forgets on request is an expense system that cannot be believed when it remembers.

== Frequently Asked Questions

*Q: Do I need to keep the original paper receipts after uploading photos to the portal?*\
A: Once you have uploaded a legible image to the portal and your report has been approved by Finance, you may discard the paper slips, unless your local office jurisdiction requires physical paper retention. Check with your local office administrator.

*Q: What happens if my expense report contains both billable and non-billable items?*\
A: Tag each line with the appropriate client billing code or internal administrative cost center. Your practice leader reviews the billable allocation during the approval step. Allocation does not change whether a line is reimbursable.

*Q: My receipt is in a foreign language. Do I need to translate it?*\
A: No. Finance reads receipts in all major European and Asian languages. Do add a short English description of the purchase in the note when the item names are not self-explanatory.
