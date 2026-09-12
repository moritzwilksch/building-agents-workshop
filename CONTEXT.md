# Workshop context

In this workshop, participants build reliable AI agents through an iterative engineering exercise. The audience is mixed: some are experienced engineers, while others rely on coding agents to write code. Keep participant-facing code simple and explicit. Scaffolding, evals, and setup can stay technical.

## Running example

Participants build an expense reimbursement agent that checks employee claims and receipts against a company policy document.

Each claim includes:
- **Metadata**: employee, dates, purpose, and amounts claimed.
- **Receipts**: invoices and itemized bills.
- **Policy manual**: a PDF containing rules, exceptions, per diems, and flowcharts.

The agent must determine:
1. **Decision**: `approved`, `rejected`, or `partially_approved`.
2. **Amount**: exact reimbursement in USD or EUR.
3. **Policy rules**: citations that justify the decision.

## Workshop progression

Participants build and refine the agent across four stages. Each stage addresses a concrete failure mode:

### Stage 1: Full-context prompt dump
- **Setup**: Put the claim, receipts, and full policy text into the prompt. Ask for a freeform prose decision.
- **Failure mode**: Unstructured, non-deterministic output that downstream systems cannot use and tests cannot grade reliably. Hallucinations are common.

### Stage 2: Structured outputs and deterministic evals
- **Setup**: Require a strict schema (`decision`, `amount`, `cited_rules`) with Pydantic or JSON schema. Run deterministic evaluations against test cases.
- **Failure mode**: The outputs are testable, but passing full policy manuals into context is slow and expensive. The agent struggles with complex exceptions and combinations of rules scattered across pages.

### Stage 3: Text search tool
- **Setup**: Give the agent a text search tool over chunked policy text so it retrieves relevant guidelines before returning structured JSON.
- **Failure mode**: Scores plateau around 60% to 70%. Real policies contain visual rules; this policy PDF includes a decision flowchart for weekend and client entertainment claims. Text extraction turns that diagram into garbled text or a placeholder (`[Figure 2: Approval Policy Flowchart]`). Cases that depend on the flowchart fail every time.

### Stage 4: Multimodal inspection and tool engineering
- **Setup**: Participants inspect execution traces and tool logs for failing cases and find that the agent misses diagram content.
- **Fix**: Add a multimodal tool, `view_page_image(page_number)`, that renders a PDF page for the vision model.
- **Result**: The agent searches text to locate sections, detects diagram references, inspects the page image, and resolves exceptions. Test accuracy reaches 95% to 100%.

## Deterministic evaluation

Avoid LLM-as-a-judge. Grade against ground-truth test cases instead:

- **Decision accuracy**: exact match on status (`approved`, `rejected`, `partially_approved`).
- **Reimbursement error**: absolute dollar difference between calculated and expected payout.
- **Citation accuracy**: precision and recall of cited policy rule IDs.
- **Tool efficiency**: tool call count, valid call sequence, and consistency across repeated runs.

## Repository and architecture constraints

- **Stage modularity**: Keep code for stages 1 to 4 self-contained so we can separate them into branches, git tags, or directories later.
- **No leakage**: Keep later-stage solutions (such as visual tools or tuned prompts) out of earlier stages where coding agents could read them.
- **Minimal abstractions**: Use pydantic-ai for the agent and its tool loop. Avoid heavyweight orchestration frameworks (LangChain, CrewAI); participants focus on prompt, tools, and system design.
