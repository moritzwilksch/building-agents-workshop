#import "template.typ": card-do, card-dont

= Multi-Currency Expenses and Foreign Exchange

== Global Operations and Multi-Currency Reporting

Noice & Toit LLP operates across multiple currency zones. Our professionals regularly incur expenses denominated in Euros (EUR, €), United States Dollars (USD, \$), British Pounds (GBP, £), Swiss Francs (CHF), Singapore Dollars (SGD), Japanese Yen (JPY), and other world currencies.

Every source document is evaluated in its own denomination, and reimbursement is paid in that denomination where it is EUR, USD, or GBP. This chapter explains how caps and conversions work for other monies.

== Applying Caps to Foreign Receipts

All caps in this handbook are published in EUR, USD, and GBP. Finance applies the cap column that matches the source document's denomination.

#card-do("Convert caps for other currencies at the ECB reference rate")[
  For a receipt in any other currency (CHF, SGD, JPY, and so on), Finance converts the *EUR* cap into the receipt currency using the European Central Bank (ECB) daily reference rate for the receipt date, applies the converted cap, and pays out the resulting amount converted back to EUR at the same rate. Employees do not need to perform any conversion themselves.
]

#card-dont("Mix currencies within one claim line")[
  Do not enter a EUR amount for a receipt printed in USD, or vice versa. Enter the amount and currency exactly as printed; the portal performs any conversion.
]

== Tipping Norms Follow the Vendor Country

The tipping caps in Chapters 7 and 14 depend on the country of the vendor as printed on the receipt, not on the currency or on the employee's home office. A receipt from a restaurant in Zurich follows the Swiss rule even if paid in EUR.

== Good Practice at the Card Terminal

None of the following changes how a receipt is evaluated, but all of it saves the firm money over a year of travel:

#card-dont("Accept Dynamic Currency Conversion (DCC) at card terminals")[
  When a foreign terminal offers to charge your card in your home currency, decline and pay in the local currency. Merchant DCC rates carry hidden markups of 5% to 12%. Finance reimburses the local-currency amount printed on the receipt either way, so accepting DCC only costs you.
]

- Avoid airport currency kiosks. If you need cash in a cash-preferred economy (Japan, parts of Germany), withdraw it from a bank-affiliated ATM.
- Keep foreign receipts flat. Thermal paper in a humid climate fades faster than the ECB updates its rates.
- The Singapore office maintains an informal list of restaurants that still add a 10% service charge and then present a tip line. Do not fill in the tip line.

== Foreign Value Added Tax (VAT) Recovery

In many European and Asian jurisdictions, business expenditures (hotel accommodation, meals, conference fees) include Value Added Tax (VAT), Goods and Services Tax (GST), or similar consumption taxes:
- Under international tax treaties, Noice & Toit LLP can reclaim foreign VAT paid on business expenses, generating substantial annual recoveries for the partnership.
- To enable VAT recovery, hotel folios and commercial invoices must show the vendor's VAT registration number, the net amount, the applicable rate (e.g., 19% MwSt in Germany, 20% VAT in the UK), and the gross total. Restaurant, taxi, and fuel receipts are exempt from the registration number requirement.
- A hotel folio or commercial invoice that omits the vendor's VAT registration number is reimbursed net of the VAT shown, since the firm cannot recover it.

== Country Payment Practice Directory

The Trade Finance Desk maintains a directory of prevailing payment practices in the markets where the firm routinely operates. It exists so that a professional arriving in an unfamiliar market does not have to rediscover, at the counter and at their own embarrassment, what every local colleague already knows. It is reviewed twice a year with the local office administrators, and immediately after any market introduces a payment mandate or a widely reported card outage. The directory explains what vendors will accept, not what the firm will reimburse; reimbursement is governed exclusively by the chapters of this handbook. Corrections go to the Trade Finance Desk with a dated receipt or vendor statement attached.

#table(
  columns: (1.2fr, 1.7fr, 1.4fr, 2.2fr, 1.8fr),
  align: (left, left, left, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  inset: 6pt,
  table.header[*Market*][*Card acceptance*][*Cash preference*][*Tipping custom*][*Documentation note*],
  [Germany], [Near universal; some artisan vendors remain cash-first], [Moderate], [Rounding up is a courtesy, not an obligation; service is understood to be included], [Full tax invoices are routine on request],
  [France], [Very broad, including kiosks], [Low], [A small "pourboire" is appreciated for table service], [Receipts are terse; ask for the detailed fiscal invoice],
  [Switzerland], [Universal in cities], [Low], [Rounding up is common but discretionary], [Request the guest folio at departure, not by post],
  [United Kingdom], [Universal; many venues are cashless], [Very low], [A discretionary addition for table service is the norm; counter service carries none], [Tax invoices must be requested by name at the till],
  [United States], [Universal], [Very low], [A structural expectation for table service, taxis, and delivered food; the amount is not set by the firm], [Itemised receipts are standard; sales tax is a separate line],
  [Japan], [Broad, but independent restaurants and ryokan may be cash-centred], [High], [Not customary in any setting; leaving money on the table causes confusion], [Receipts ("ryoshusho") issued on request; ask for the formatted version],
  [Singapore], [Universal], [Low], [A service charge appears on most hospitality bills; further tipping is not expected], [Tax invoices must carry the vendor's registration details for recovery],
)

The directory records practice, not preference. A vendor's refusal to accept a particular card type is never a reason to depart from this chapter's rules on currency at the terminal.

== Corporate Card Programme Operations

The firm's cards are issued and administered by the Cards & Payments Desk, which reports to Treasury Operations. Every card belongs to one of the tiers below, and the tier determines who may hold it, what it is intended for, and which body reviews its usage. Holding a card is tied to a role, not to a person: cards are reassigned within one business day of a role change and cancelled within one business day of a departure:

#table(
  columns: (1.4fr, 1.6fr, 2.2fr, 1.8fr, 1.4fr),
  align: (left, left, left, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  inset: 6pt,
  table.header[*Card tier*][*Issued to*][*Intended use*][*Excluded use*][*Reviewing body*],
  [Standard travel card], [All fee-earning staff], [Accommodation, ground transport, and meals while travelling], [Client entertainment; subscriptions], [Cards & Payments Desk],
  [Practice card], [Practice Group Leaders and above], [Client entertainment and working sessions, in addition to the standard tier], [Personal expenditure], [Audit Committee, semi-annually],
  [Events card], [Named event coordinators], [Venue deposits and conference vendor payments], [Recurring vendor relationships], [Cards & Payments Desk, monthly],
  [Vendor virtual card], [Procurement coordinators only], [Single-use payments to approved suppliers], [Any physical point of sale], [Procurement and the Cards & Payments Desk],
  [Emergency travel card], [Issued ad hoc by Treasury Operations], [Bookings during disruption when the primary card is unavailable], [Anything unrelated to the disruption], [Treasury Operations, per issuance],
)

#card-do("Report a lost card before you finish looking for it")[
  Report a lost or cloned card to the Cards & Payments Desk immediately, by phone and not only by e-mail. The Desk freezes a card within minutes; the hours you spend searching your hotel room are the hours a fraudulent merchant spends shopping.
]

Card statements are delivered to the cardholder and mirrored to the Cards & Payments Desk automatically. The cardholder attaches the underlying receipt to each statement line in the portal; the Desk chases unattached lines rather than silently accruing them. Persistent non-attachment is a People Operations matter.

== The Currency Reconciliation Cycle

Reconciliation is the least glamorous activity described in this handbook and the one that most often prevents an awkward audit finding. The cycle runs monthly. First, Treasury Operations snapshots the reference rates on the closing day and locks the snapshot; nobody revises a locked rate, whatever the outcome. Second, the Finance shared-service team matches each foreign-currency statement line to its portal claim and records the differences that arise from timing between the reference rate and the card scheme's own settlement rate. Third, the differences are classified: pure rate timing, merchant revaluation after the fact, or genuine posting errors — and only the third generates correspondence with the cardholder.

The desk then produces a monthly variance note for Treasury Operations describing the classified differences in qualitative terms — which currencies drifted, which merchant categories revalued most often, whether any pattern points to a systemic entry error. The note is deliberately narrative: a variance note that reads like a table of numbers invites the reader to hunt for a rule that does not exist.

#card-dont("Keep a private spreadsheet of exchange rates")[
  Private rate spreadsheets diverge from the locked snapshots, and once they diverge, every subsequent number is untraceable. If you need a historical rate, ask Finance for the locked snapshot. It exists, it is authoritative, and asking costs nothing.
]

The Records Office retains each monthly reconciliation pack, including the locked rate snapshots and the variance notes, under the standard financial-records retention schedule. Internal Audit may sample any closed month without notice; the pack is expected to stand on its own.

== Consumption Tax Recovery Workflow

Recovering foreign consumption taxes is a partnership-level income stream, and the partnership treats it with the discipline that implies. The Indirect Tax Team runs the recovery programme in quarterly cycles aligned to the jurisdictions that permit refund claims. Each cycle has three phases: the team assembles eligible invoices from the portal and reconciles them against card statements; it vets each invoice against the destination country's documentary requirements and rejects incomplete invoices back to the claiming employee with a stated reason; and it bundles the vetted claims through the firm's appointed recovery intermediaries, tracking each submission to a decision.

The vetting phase is where claims most often fail, and the failure is almost always a receipt defect: a casual till slip standing in for a proper tax invoice, a folio missing the vendor's fiscal identifiers, or a name that does not match the travelling employee. The Indirect Tax Team publishes, at the start of each cycle, a list of the defects observed in the previous one; reading it takes minutes and saves everyone a round of rejections.

#table(
  columns: (1.3fr, 1.7fr, 1.7fr, 1.4fr, 2fr),
  align: (left, left, left, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  inset: 6pt,
  table.header[*Jurisdiction cluster*][*Tax type typically encountered*][*Handled by*][*Filing rhythm*][*Most common defect*],
  [European Union], [Value added tax], [Indirect Tax Team, in-house], [Quarterly], [Till slips submitted instead of full tax invoices],
  [United Kingdom], [Value added tax], [Indirect Tax Team, in-house], [Quarterly], [Missing vendor fiscal identifiers on folios],
  [Switzerland], [Value added tax], [Appointed intermediary], [Per intermediary schedule], [Invoices in the guest's name only],
  [Canada], [Goods and services tax and provincial components], [Appointed intermediary], [Annual], [Summary folios without room-level detail],
  [Japan], [Consumption tax], [Local advisors], [Annual], [Simplified receipts lacking the formatted business fields],
  [Singapore], [Goods and services tax], [Local advisors], [Annual], [Vendors not registered for the tax],
)

Some levies are not recoverable at all — occupancy and tourism charges at hotels, for instance, are a cost of travel, not a recovery opportunity. The Indirect Tax Team marks such items as non-recoverable in the portal so that nobody re-files them next cycle. Re-filing a rejected item without addressing the stated defect is recorded and visible to People Operations.

== Intercompany Settlement Between Offices

When a professional from one office incurs expenditure that properly belongs to another office's client matter — a Frankfurt partner hosting a New York working group, for example — the expenditure is still claimed through the claimant's own portal in the claimant's own currency. The claimant never invoices the other office directly. The Finance shared-service team identifies these cross-charges each month, converts them at the locked closing snapshot, and books them to a dedicated intercompany account.

Settlement between offices occurs on a quarterly netting run rather than payment by payment. Netting keeps the ledger readable: a quarter of cross-office charges resolves into one settlement instruction per currency pair instead of dozens. The run is prepared by the Finance shared-service team, confirmed by Treasury Operations, and countersigned by the Finance Directors of both entities involved. Any office disputing a netted item raises the dispute before countersigning; the disputed item is carved out and settled separately, so one disagreement never stalls the whole settlement.

Transfer pricing documentation is the anchor for all of this. The netting schedule must reconcile to the intercompany positions reported in the firm's transfer pricing file, and the Tax Team reviews that reconciliation twice a year. A netting run that cannot be reconciled is a finding waiting to happen, and it is treated as one.
== Reporting Mechanics and Publication Calendar

Multi-currency activity is reported through a fixed suite of recurring reports, each with a named preparer, a defined audience, and a publication rhythm. The suite exists so that the same questions need not be answered ad hoc from raw extracts.

#table(
  columns: (1.7fr, 1.6fr, 1.7fr, 1.3fr, 1.7fr),
  align: (left, left, left, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  inset: 6pt,
  table.header[*Report*][*Prepared by*][*Audience*][*Cadence*][*Distribution*],
  [Currency exposure summary], [Treasury Operations], [Finance Directors and the Audit Committee], [Monthly], [With the month-end pack],
  [Card programme utilisation review], [Cards & Payments Desk], [Treasury Operations and People Operations], [Monthly], [Portal dashboard and PDF extract],
  [Recovery pipeline report], [Indirect Tax Team], [Finance Directors and office administrators], [Quarterly], [At each cycle opening],
  [Reconciliation variance note], [Finance shared-service team], [Treasury Operations], [Monthly], [Filed with the reconciliation pack],
  [Intercompany netting schedule], [Finance shared-service team], [Finance Directors of the settling entities], [Quarterly], [Countersigned copy to the Records Office],
  [Year-end attestation pack], [Treasury Operations], [Audit Committee and external auditors], [Annually], [Retained by the Records Office],
)

Each report carries a standard header stating the preparation date, the reporting period, the preparer, and the underlying source (portal extract, card scheme file, or locked rate snapshot). A report without its source note is returned unopened, in the polite sense that it is returned.

== Frequently Asked Questions

*Q: My card was charged in EUR for a receipt printed in CHF. Which amount do I claim?*\
A: Claim the CHF amount printed on the receipt. The firm reimburses at the ECB reference rate; small differences to your card statement are not reimbursed.

*Q: Can I claim reimbursement for leftover foreign cash currency?*\
A: No. Unspent foreign currency bills and coins belong to the employee and cannot be "bought back" by the firm. Only actual, documented business expenditures are eligible for reimbursement.
