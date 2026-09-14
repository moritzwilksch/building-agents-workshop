# Ground-truth labels

One JSON file per case, stored next to the case as `data/case-XXXX/label.json`.

A label records what the *correct* reimbursement decision is: the top-level
decision, the amounts, the line-item breakdown, and a plain-English reason.

## Format

| Field | Type | Meaning |
| --- | --- | --- |
| `case_id` | string | Matches the data directory, e.g. `"case-0001"` |
| `decision` | string | `"approved"`, `"partially_approved"`, or `"rejected"` |
| `claimed_amount` | number | Total the employee asked for |
| `reimbursed_amount` | number | Total we pay |
| `line_items` | array | One entry per charge on the receipt |
| `reasoning` | string | Plain-English explanation of the decision |

Each line item:

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | integer | Position on the receipt, `0` for the topmost charge |
| `description` | string | What the item was |
| `claimed` | number | What was charged for it |
| `reimbursed` | number | What we pay for it |

## Line items and ids

The ids come from the `charges` list in the case's `invoice.json`, which
numbers every charge in receipt order (see `invoice-spec.md`): one label line
item per charge, same id, same `claimed` amount.

List one entry per line that adds to the total: the items, any separately
charged tax or fee, and the tip. A tax already included in the item prices (a
restaurant's MwSt) is not its own line. Number the entries top to bottom
starting at `0`; the ids must be `0..n-1` in that order, and evaluation matches
the agent's items to ours by `id`, not by description.

## Decision rules

- `approved` → `reimbursed_amount == claimed_amount`
- `rejected` → `reimbursed_amount == 0`
- `partially_approved` → `0 < reimbursed_amount < claimed_amount`

## Amounts and currency

All amounts are in the receipt's currency. Every case in `data/` is in EUR, so
we leave currency out. If we ever mix currencies, add a single top-level
`currency` field.

## Example

```json
{
  "case_id": "case-0001",
  "decision": "partially_approved",
  "claimed_amount": 247.00,
  "reimbursed_amount": 178.50,
  "line_items": [
    { "id": 0, "description": "Duck breast (x2)", "claimed": 58.00, "reimbursed": 58.00 },
    { "id": 1, "description": "Truffle risotto (x2)", "claimed": 46.00, "reimbursed": 46.00 },
    { "id": 2, "description": "Octopus", "claimed": 21.50, "reimbursed": 21.50 },
    { "id": 3, "description": "Mezcalita cocktails (x3)", "claimed": 43.50, "reimbursed": 0.00 },
    { "id": 4, "description": "Non-alcoholic spritz", "claimed": 9.50, "reimbursed": 9.50 },
    { "id": 5, "description": "Mineral water (x2)", "claimed": 15.00, "reimbursed": 15.00 },
    { "id": 6, "description": "Desserts (x3)", "claimed": 28.50, "reimbursed": 28.50 },
    { "id": 7, "description": "Tip", "claimed": 25.00, "reimbursed": 0.00 }
  ],
  "reasoning": "Business dinner for 4. Alcohol is not covered for client dinners, and tips are capped, so the cocktails and tip are deducted."
}
```

## How we evaluate against labels

- **Decision accuracy** — match `decision`.
- **Average amount wasted** — average of `claimed_amount - reimbursed_amount`.
- **Reimbursement error** — `abs(predicted - expected)` on `reimbursed_amount`.
- **Line-item check** — compare `reimbursed` per line `id`.
- **Reason quality** — read `reasoning`, or compare loosely. No exact match.

## Out of scope (on purpose)

- No structured deduction codes.
- No rule IDs or citations.
- No currency conversion.

These add complexity a teaching workshop does not need. `reasoning` carries the
"why" in plain language.
