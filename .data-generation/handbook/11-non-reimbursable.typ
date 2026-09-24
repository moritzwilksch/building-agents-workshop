#import "template.typ": card-do, card-dont

= Non-Reimbursable Expenses and Prohibited Purchases

== The Boundary Between Business and Personal Life

Business travel and client advisory work inevitably blur the lines between professional duties and everyday personal living. However, tax authorities and partnership financial standards require a clear, consistent boundary. The firm reimburses only the incremental, necessary expenses caused directly by conducting business on behalf of Noice & Toit LLP.

Expenses that represent ordinary personal maintenance, leisure choices, discretionary upgrades, or the consequences of avoidable individual negligence are strictly the financial responsibility of the employee.

== Master Catalog of Non-Reimbursable Expenditures

The following items are non-reimbursable across all offices, projects, and billing arrangements. Where such an item appears as one line on an otherwise valid receipt, that line is deducted (with its tax) under the calculation steps in Chapter 2. Where the entire receipt consists of such items, the receipt is rejected.

=== Legal Penalties, Fines, and Citations
#card-dont("Claim traffic tickets or legal citations")[
  Speeding tickets, red-light camera fines, parking violation tickets, bus lane penalties, wheel clamping release fees, vehicle impound charges, and toll violation surcharges are strictly personal obligations. The firm will not reimburse any fine or citation under any circumstance, even if incurred while rushing to a client emergency.
]

=== Personal Grooming, Health, and Apparel
#card-dont("Expense haircuts, spa treatments, or clothing")[
  The firm does not reimburse routine personal care expenditures, including:
  - Haircuts, hair salon styling, blowouts, and manicures.
  - Spa treatments, massages (including hotel "express" or "de-stress" massages), saunas, and beauty therapies.
  - Suits, ties, shirts, dresses, shoes, belts, socks, and any other clothing, however urgently needed.
  - Over-the-counter pharmaceuticals, vitamins, headache tablets, or sunscreen.
  - Health club day-passes, gym drop-in fees, hotel fitness center surcharges, or fitness trainer sessions.
  The only exception is the delayed-baggage allowance below.
]

=== Luggage, Bags, and Travel Accessories
- Luggage sets, suitcases, carry-on roller bags, garment bags, and briefcases.
- Passport renewal fees, tourist visa fees, and passport photo fees.
- Travel umbrellas, neck pillows, earplugs, sleep masks, and luggage tags.

=== Discretionary Upgrades and Luxury Preferences
- Business or First Class cabins where Chapter 4 does not permit them; First Class rail where Chapter 5 does not permit it.
- The portion of a hotel rate above the regional cap (Chapter 6).
- Rental car categories above Intermediate without a named approver (Chapter 5).
- Airline seat selection, extra-legroom seats, priority boarding, and lounge access (Chapter 4).
- Premium rideshare tiers above the unjustified-ride threshold (Chapter 5).

=== Hotel Incidentals
- Minibar snacks and beverages of any kind, in-room movies and streaming, spa and wellness charges, pet or animal cleaning fees, and late check-out fees (Chapter 6).
- Laundry outside the allowances in Chapter 6.

=== Gifts, Gift Cards, and Cash Equivalents
#card-dont("Purchase gift cards or retail vouchers")[
  Retail gift cards, Amazon vouchers, prepaid debit cards, and cash equivalents are deducted wherever they appear. Tax regulations classify gift cards as cash compensation, triggering mandatory payroll tax withholding. Client gift initiatives and employee recognition programs must be coordinated through People Operations.
]

=== Family, Companion, and Pet Expenses
- Airfare, train tickets, meals, and transit fares for spouses, domestic partners, children, friends, or other travel companions.
- Pet boarding, kennel fees, dog walking services, hotel pet fees, and in-home pet care during business travel.
- Babysitting services, childcare fees, house-sitting fees, or home plant watering services.

=== Personal Subscriptions, Software, and Entertainment
- Streaming media services (Netflix, Spotify, Apple Music, Disney+, YouTube Premium) and consumer magazines.
- Software licenses, app purchases, cloud credits, and AI API credits (Chapter 10).
- Museum admissions, city tours, ski passes, and other recreational activities (Chapter 9).

=== Office Furnishing
- Furniture, lamps, decor, artwork, and plants, including plant rental and plant care services (Chapter 10). The sole exception is temporary staging greenery rented for a named, pre-approved event, which Chapter 10 treats as an event material.

=== Venues
- Any bill from a night club, gentleman's club, or casino (Chapter 8) is rejected in full.

== Delayed or Lost Baggage Emergency Allowance

The only exception to the apparel and grooming exclusion occurs when an airline mishandles or loses an employee's checked bag on an outbound business flight:
- You may purchase essential toiletries and one modest change of business attire up to a cumulative *€100.00 / \$120.00 / £90.00*. The excess is deducted.
- The note must state that the airline lost or delayed the bag, name the flight, and quote the Property Irregularity Report (PIR) reference issued by the airline baggage desk. Without a PIR reference in the note, apparel and toiletries are deducted like any other personal item.
- No emergency apparel or toiletry reimbursement is permitted upon return to your home residence city.

== The Extended Catalogue of Excluded Categories

The master catalog above records the exclusions that employees attempt most often. Behind it sits a fuller schedule, maintained by the Policy Stewardship Committee, that classifies every category of expenditure the firm has ever been asked to reimburse and declined. The extended catalogue is reproduced below. The rationale column is not decoration: an employee who understands _why_ a category is excluded can usually predict how a genuinely novel item will be treated. Questions about any row go to the steward listed before the expense is incurred, not after.

#table(
  columns: (1.3fr, 2.6fr, 1.4fr),
  align: (left, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Category*][*Rationale for Exclusion*][*Steward*],
  [Transport citations and penalties], [Imposed by a public authority on an individual for that individual's conduct; the firm accepts no liability for them, however sympathetic the itinerary], [Travel Desk],
  [Personal grooming and aesthetics], [Ordinary maintenance of the self, which continues whether or not the employee travels], [People Operations],
  [Apparel, footwear, and accessories], [Worn after the engagement ends and retained in personal service at home; the delayed-baggage provision above is the sole exception], [People Operations],
  [Luggage, bags, and travel hardware], [Durable goods that outlast the trip and remain useful for years of private travel], [Travel Desk],
  [Companion and family travel], [The engagement is performed by the employee alone; costs of accompanying persons carry no business purpose], [Travel Desk],
  [Pet care and boarding], [Relates to the household, not the engagement; the pet does not attend the client meeting], [People Operations],
  [Household and domestic services], [These maintain the home, not the work; the home does not cease to need them because the employee is away], [People Operations],
  [Recreation, sport, and wellness leisure], [Pursued for private enjoyment; client hospitality is governed separately, and more leniently, by Chapter 8], [Policy Stewardship Committee],
  [Consumer subscriptions and personal devices], [Licences and hardware that remain in personal use long after the claim has been paid], [Global Finance],
  [Collectibles, memorabilia, and auction purchases], [Value accrues to the individual, and no reliable business purpose can be documented for a signed photograph], [Legal / General Counsel],
  [Games of chance, lotteries, and wagering], [Prohibited outright rather than merely discouraged; recovery of any such charge is treated as a conduct matter], [Audit Committee],
  [Political and religious donations], [Outside the firm's centrally administered charitable giving framework, which exists so that the firm speaks with one voice], [Legal / General Counsel],
  [Loyalty redemptions and travel credits], [Points and credits belong to the traveller under the supplier's terms; their redemption is a private arrangement], [Travel Desk],
)

== The Boundary Principle Between Personal and Business Living

A catalogue, however long, cannot enumerate every object an employee might buy in a decade of client work. When a receipt line matches no named category, reviewers apply the boundary principle: the firm pays for the _incremental cost of doing the work away from home_, and the employee pays for the cost of living, wherever that living happens to occur. The operative question is whether the cost would have arisen in substantially the same form had the engagement never existed. If the answer is yes, the cost belongs to the employee, no matter how convenient it was to settle it on a corporate card while travelling.

The principle asks a second question only when the first is inconclusive: does the expenditure buy access to a client, a work product, or a statutory obligation? A cost that exists to produce something the client receives, or that a jurisdiction requires before work may begin, passes the boundary even if it resembles a personal purchase in shape. A cost that merely makes the employee more comfortable while producing the work does not. The firm does not adjudicate taste; it adjudicates whether the cost exists because of the work.

Where a single receipt blends both kinds of cost, the reviewer apportions it: the business portion is reimbursed under the relevant chapter and the personal portion is deducted with its tax under the calculation steps in Chapter 2. Reviewers must record the basis for any apportionment in the claim file so that the reasoning survives the reviewer's own holidays.

== Tax Treatment of Excluded Items

The firm's severity on this chapter is not temperament; it is tax arithmetic. Most jurisdictions treat a reimbursed personal expense as remuneration in kind. A casually reimbursed personal item converts a private cost into a taxable benefit, generating a reporting obligation for the employee, a payroll liability for the firm, and a restatement exposure in the firm's indirect tax recovery positions, since input tax claimed on a personal element is input tax claimed wrongly. The deduction of an excluded line _with its tax_ under Chapter 2 is therefore not a punishment. It is the mechanism that keeps the valid portion of the claim clean in the eyes of every authority that may later read it.

Three treatments follow from this. First, the common case: an excluded line on an otherwise valid receipt is simply deducted, and the claim proceeds. Second, where an excluded item has been _enjoyed_ and cannot be separated from a settled sum that no reviewer can apportion, People Operations characterises the amount as a benefit and processes it through payroll. Third, a receipt consisting entirely of excluded items is rejected in full and must be resubmitted without it if a valid underlying claim exists. The Records Office retains the documentation for every deduction, characterisation, and rejection on the schedule in Chapter 1, because the firm's position must be reconstructable long after the traveller and every reviewer have moved on. Employees who believe an item has been wrongly classified should not resubmit the same receipt with a longer note; the appeals workflow below exists for that purpose.

== Appeals and Investigation Workflow

An exclusion is a classification, and classifications can be wrong. The firm therefore maintains a short, written, and non-punitive workflow for challenging one. Using the workflow is a sign of a well-run claims process, not of a difficult employee, and no manager may treat an appeal as a blemish on a performance record. The steps are as follows.

#table(
  columns: (0.6fr, 3.2fr, 1.6fr),
  align: (left, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Step*][*What Happens*][*Responsible Body*],
  [1], [The reviewer flags a line as excluded and states, in the claim file, the catalogue heading or chapter relied upon. A flag without a stated basis is invalid and is treated as not raised], [Global Finance],
  [2], [The employee submits a written statement, through the portal, explaining why the item passes the boundary principle. Statements are made in good faith and are kept confidential to the reviewers], [Claimant],
  [3], [A reviewer who did not raise the original flag considers the statement against the rationale column of the catalogue and issues a written determination, which is filed with the claim], [Global Finance],
  [4], [If the employee disputes the determination on a question of principle — not arithmetic — the Policy Stewardship Committee reviews the item at its next session and may confirm, reverse, or refer the classification], [Policy Stewardship Committee],
  [5], [Where a pattern of repeated excluded claims suggests mischaracterisation rather than confusion, the matter passes to for-cause review under the audit streams in Chapter 1], [Audit Committee],
  [6], [The Records Office archives the full file — flag, statement, determination, and any Committee minute — on the standard retention schedule], [Records Office],
)

Three ground rules govern the workflow. An appeal suspends recovery of the disputed amount but does not delay payment of the undisputed remainder. A determination on a question of principle is circulated in anonymised form to all reviewers, so the next traveller with the same item meets the same answer. And no employee suffers any disadvantage in appraisal or staffing for having appealed in good faith, a commitment the Audit Committee polices with the same energy it applies to the exclusion lists themselves.

== Resolving Borderline Cases

Certain situations recur often enough that stewards record their determinations. Each case below was resolved by applying the boundary principle, not by adding a numbered rule, and they are reproduced here as reasoning aids rather than as a parallel catalogue.

#table(
  columns: (2.1fr, 2.7fr, 1.3fr),
  align: (left, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Situation*][*How the Boundary Principle Applies*][*Determination*],
  [A pharmacy purchase combining headache tablets with a rehydration solution, bought during a demanding engagement], [Both items are maintenance of the self, which the body requires in every city and every week, whatever the workload], [Non-reimbursable],
  [A taxi from a client site to a hospital after a minor injury sustained during client work], [The journey exists only because the engagement placed the employee at the site; the cost fails the but-for test in the employee's favour], [Reimbursable, with documentation],
  [A travel umbrella bought during a downpour while walking to a client site], [Staying dry is a personal comfort in any city; the umbrella has no client-facing output], [Non-reimbursable],
  [Business-centre printing of pitch materials the evening before a client presentation], [The output goes to the client and exists only for the engagement; the principle's second question is answered squarely in favour of the claim], [Reimbursable],
  [An entry visa required by the destination jurisdiction before work may lawfully begin], [A statutory precondition of the engagement itself; without it there is no trip and no work], [Reimbursable, via the Travel Desk],
  [A day of rented workspace because the hotel room cannot host confidential discussions], [The cost buys access to a client-capable working environment that the engagement genuinely requires], [Reimbursable],
  [A courier fee to return signed engagement papers to the client's counsel], [The cost exists to discharge an obligation the firm owes the client; it has no private analogue], [Reimbursable],
  [A taxi from the home office to a client site across the same city], [The journey arises only because of the client; residence in the city does not convert client travel into commuting], [Reimbursable, under Chapter 5],
  [A translator engaged for two hours to review a client document drafted in a second language], [The work product is delivered to the client; the translator is as much a cost of the engagement as the reviewer's own time], [Reimbursable],
)

Where a situation resembles none of these, reviewers reason from the principle and write the reasoning into the claim file. The Policy Stewardship Committee reviews the accumulated reasoning annually and, where a determination recurs, considers whether the item has outgrown this chapter and belongs in a numbered one.

== Frequently Asked Questions

*Q: What if I received a parking ticket because the client office parking lot was full?*\
A: The ticket remains your personal responsibility. Plan parking in designated public lots or garages when client visitor parking is unavailable.

*Q: Can I expense a hotel laundry bill if my suit was stained during a client dinner?*\
A: Possibly. Chapter 6 sets the conditions and the per-stay cap for garment rescue on short trips; the incident must be described in the note.

*Q: I bought emergency socks at the airport before a client meeting. Reimbursable?*\
A: No, unless the airline lost your bag and the note quotes the PIR reference. Clothing is otherwise personal regardless of circumstance.
