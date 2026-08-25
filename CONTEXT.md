# Workshop context

This workshop teaches how to engineer enterprise AI agents through a fictional expense reimbursement agent. The audience is mixed: some participants are technical, while others may not have coded before. Teach the ideas and system design first; keep code simple and optional.

## Running example

The agent decides which employee expenses should be reimbursed, how much to reimburse, and which company policy supports each decision. A case contains multiple expenses and receipts. The decision depends on a large, messy body of policies, exceptions, local rules, and effective dates.

## Workshop progression

Evolve the same agent through versions. Each version must fix a concrete failure from the previous one:

1. Naive one-shot LLM
2. Structured outputs
3. Deterministic validation
4. Agentic tool loop
5. Improved access to policy knowledge
6. Domain-specific tools that expose stable business concepts directly

The main lesson: strong enterprise agents do not come from increasingly elaborate prompts. They come from engineering the environment around the model: clear interfaces, deterministic checks, good information access, useful tools, and measurable feedback.

## Evaluation

Maintain a small evaluation set throughout the workshop and rerun it after every version. Track:

- Decision accuracy
- Fully correct reports
- Reimbursement error
- Cost
- Latency
- Policy-citation correctness, where useful

Use the results to make improvement visible. Treat the workshop as a concrete hill-climbing exercise, not a sequence of disconnected demos.
