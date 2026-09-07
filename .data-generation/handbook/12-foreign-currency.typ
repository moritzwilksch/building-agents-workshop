#import "template.typ": policy-rule, policy-warning

= Multi-Currency Expenses & Foreign Exchange

== Accepted Claim Currencies

Expense submissions must be denominated in either Euros (EUR, €) or United States Dollars (USD, \$), corresponding to the employee's payroll entity.

#policy-rule("POL-CUR-001", "Exchange Rate Substantiation")[
  When expenses are incurred in foreign currencies:
  + If paid via corporate credit card or personal credit card, the employee must attach the card statement or transaction printout demonstrating the actual settled conversion rate and local currency charge.
  + In the absence of a card statement showing the exact conversion, reimbursement will be calculated using the European Central Bank (ECB) or Federal Reserve benchmark reference exchange rate for the exact transaction date.
]

== Foreign Transaction and ATM Surcharges

International travel incurs unavoidable currency handling and payment processor fees.

#policy-rule("POL-CUR-002", "Foreign Payment Transaction Fees")[
  Mandatory credit card foreign transaction fees (typically 1.5% to 3.0%) incurred while settling bona fide business expenditures in a foreign currency are reimbursable. Discretionary ATM cash advance fees and dynamic currency conversion (DCC) markup fees at merchant POS terminals are non-reimbursable.
]
