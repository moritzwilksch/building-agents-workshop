#import "template.typ": card-do, card-dont

= Global Offices, Directory, and Regional Addenda

Noice & Toit LLP supports employees across many offices. This chapter is a directory and a record of regional notes. It contains no reimbursement rules.

#card-do("Contact the right desk the first time")[
  Travel bookings and duty of care go to the Travel Desk. Receipt and policy questions go to the Expense Auditing Team. Card problems go to Corporate Card Administration.
]

== Global Office Directory

#table(
  columns: (1.4fr, 2fr, 1.2fr, 1.6fr),
  align: (left, left, left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*City*][*Office*][*Region*][*Time Zone*],
  [London], [Fenchurch Street], [EMEA], [Europe/London], 
  [Berlin], [Friedrichstrasse], [EMEA], [Europe/Berlin], 
  [Munich], [Maximilianstrasse], [EMEA], [Europe/Berlin], 
  [Frankfurt], [Taunusanlage], [EMEA], [Europe/Berlin], 
  [Hamburg], [Neuer Wall], [EMEA], [Europe/Berlin], 
  [Düsseldorf], [Königsallee], [EMEA], [Europe/Berlin], 
  [Zurich], [Bahnhofstrasse], [EMEA], [Europe/Zurich], 
  [Geneva], [Rue du Rhône], [EMEA], [Europe/Zurich], 
  [Paris], [Avenue des Champs-Élysées], [EMEA], [Europe/Paris], 
  [Amsterdam], [Zuidas], [EMEA], [Europe/Amsterdam], 
  [Brussels], [Avenue Louise], [EMEA], [Europe/Brussels], 
  [Madrid], [Paseo de la Castellana], [EMEA], [Europe/Madrid], 
  [Milan], [Via Montenapoleone], [EMEA], [Europe/Rome], 
  [Rome], [Via Veneto], [EMEA], [Europe/Rome], 
  [Vienna], [Ringstrasse], [EMEA], [Europe/Vienna], 
  [Stockholm], [Stureplan], [EMEA], [Europe/Stockholm], 
  [Copenhagen], [Kongens Nytorv], [EMEA], [Europe/Copenhagen], 
  [Oslo], [Aker Brygge], [EMEA], [Europe/Oslo], 
  [Helsinki], [Esplanadi], [EMEA], [Europe/Helsinki], 
  [Dublin], [Grand Canal Dock], [EMEA], [Europe/Dublin], 
  [Warsaw], [Rondo ONZ], [EMEA], [Europe/Warsaw], 
  [Prague], [Prague 1], [EMEA], [Europe/Prague], 
  [Budapest], [District V], [EMEA], [Europe/Budapest], 
  [New York City], [Park Avenue], [Americas], [America/New_York], 
  [Boston], [Seaport], [Americas], [America/New_York], 
  [Chicago], [Wacker Drive], [Americas], [America/Chicago], 
  [Seattle], [Union Street], [Americas], [America/Los_Angeles], 
  [San Francisco], [Market Street], [Americas], [America/Los_Angeles], 
  [Los Angeles], [Wilshire Boulevard], [Americas], [America/Los_Angeles], 
  [Toronto], [Bay Street], [Americas], [America/Toronto], 
  [Vancouver], [Burrard Street], [Americas], [America/Vancouver], 
  [Mexico City], [Paseo de la Reforma], [Americas], [America/Mexico_City], 
  [Sao Paulo], [Avenida Paulista], [Americas], [America/Sao_Paulo], 
  [Buenos Aires], [Puerto Madero], [Americas], [America/Argentina/Buenos_Aires], 
  [Tokyo], [Marunouchi], [Asia-Pacific], [Asia/Tokyo], 
  [Singapore], [Marina Bay], [Asia-Pacific], [Asia/Singapore], 
  [Hong Kong], [Central], [Asia-Pacific], [Asia/Hong_Kong], 
  [Shanghai], [Lujiazui], [Asia-Pacific], [Asia/Shanghai], 
  [Seoul], [Gangnam], [Asia-Pacific], [Asia/Seoul], 
  [Mumbai], [Bandra Kurla Complex], [Asia-Pacific], [Asia/Kolkata], 
  [Sydney], [Barangaroo], [Asia-Pacific], [Australia/Sydney], 
  [Melbourne], [Collins Street], [Asia-Pacific], [Australia/Melbourne], 
  [Auckland], [Britomart], [Asia-Pacific], [Pacific/Auckland], 
  [Dubai], [DIFC], [Middle East], [Asia/Dubai], 
  [Abu Dhabi], [Al Maryah Island], [Middle East], [Asia/Dubai], 
  [Riyadh], [King Fahd Road], [Middle East], [Asia/Riyadh], 
  [Johannesburg], [Sandton], [Africa], [Africa/Johannesburg], 
  [Nairobi], [Westlands], [Africa], [Africa/Nairobi], 
)

== Regional Addenda

#table(
  columns: (1.2fr, 5fr),
  align: (left, left),
  fill: (_, y) => if y == 0 { rgb("#dbeafe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  table.header[*Region*][*Note*],
  [EMEA], [Local public holidays follow the destination country, not the home office.], 
  [EMEA], [VAT registration numbers are required on folios and commercial invoices.], 
  [EMEA], [Rail is the default for journeys under four hours within the region.], 
  [Americas], [Tip norms in the region follow the vendor country schedule.], 
  [Americas], [Sales tax is reimbursable when separately itemized.], 
  [Asia-Pacific], [Tipping is generally not customary; service charges printed on a bill are reimbursable.], 
  [Asia-Pacific], [Long-haul rest days follow the weekday and weekend logic in Chapter 9.], 
  [Middle East], [Friday and Saturday form the regional weekend; the weekend rules still follow the receipt date.], 
  [Africa], [Cash is preferred in some markets; withdraw from bank-affiliated ATMs only.], 
  [Cross-region], [Currency caps follow the receipt currency column in Chapter 14.], 
)

== Contact Directory

- *Global Travel Desk*: `travel@noiceandtoit.internal`
- *Expense Auditing Team*: `expenses@noiceandtoit.internal`
- *Corporate Card Administration*: `corporatecards@noiceandtoit.internal`
- *Accounts Payable*: `finance-disbursements@noiceandtoit.internal`
- *People Operations*: `people@noiceandtoit.internal`
- *IT Service Portal*: `ithelp.noiceandtoit.internal`
- *Ethics and Conduct Committee*: `ethics@noiceandtoit.internal`
