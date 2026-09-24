# Hints

Stuck? Pick one idea below and try a small experiment. These hints are available from Stage 0 onward; they suggest directions, not a required design.

## Start with the simplest agent

The harness already supplies the receipt, employee note, and invoice charges. Your agent needs the policy rules and instructions for returning reimbursements in charge order. Getting one benchmark run into the viewer is a useful first milestone—even if the decisions are wrong.

One starting point is to extract the handbook's text and put it in the prompt. This is easy to reason about, but watch how much text the model receives and what the extraction leaves out.

## Find the relevant rule instead of loading everything

Most receipts need only a few handbook sections. Could a search tool help the agent find them?

Simple keyword search is a reasonable starting point. Give each result a page number and a short preview, then let a separate tool read the selected page in full. A preview helps locate a rule; it is not enough evidence to apply it. Preserve page numbers, and consider rules that continue onto the next page.

Prepare the searchable text once when building the agent, rather than extracting the PDF on every tool call. Inspect a trace: did the agent search for a useful phrase, find the right page, and actually read it?

## Give arithmetic a small, reliable tool

Choosing which policy applies requires judgment. Adding amounts, calculating a percentage, and rounding to cents usually do not.

Consider a specialized calculation tool with explicit inputs: eligible amounts and a tax rate, for example. Its description should make units clear—does five percent mean `5` or `0.05`? Use decimal arithmetic and a consistent rounding rule for money.

Keep the boundary clear: the agent decides which charges qualify; the tool performs the calculation. A correct calculation cannot rescue the wrong policy choice. When several lines share a cap, think about how to divide it and where a leftover cent should go.

## Read what text extraction cannot see

A PDF can contain a rule in a diagram or an image of a table. Opening the document and extracting its text are not the same thing.

If a trace points to a relevant page but the extracted text lacks the rule, inspect that page yourself. Would a tool that returns an image of one requested page give the model the missing evidence? Keep text search for finding pages; add image inspection only where it helps.

## Let the trace choose your next change

For one mismatch, ask:

- Was the needed evidence available?
- Did the agent find and read it?
- Did it apply the rule to the right charge?
- Was the arithmetic correct?
- Did the output follow the shared interface?

Fix one likely cause, then rerun the same suite. Prefer a rule or capability that generalizes over a patch for one receipt. Expected answers help you diagnose mistakes; they should never become inputs to the expense agent.
