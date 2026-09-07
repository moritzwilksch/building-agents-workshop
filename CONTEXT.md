# Workshop Context

This workshop teaches how to build reliable enterprise AI agents through a concrete, hill-climbing engineering exercise. The audience is mixed: some participants are experienced engineers, while others have limited coding background and rely on coding agents (e.g. Codex) to implement solutions. Keep participant-facing code simple, explicit, and easy to reason about. Scaffolding, evals, and setup can remain technical under the hood.

## Running Example

The running example is an **expense reimbursement agent** adjudicating employee expense claims and receipts against an enterprise policy document.

A single claim case contains:
- Structured claim metadata (employee, dates, purpose, amounts claimed).
- Raw receipts (invoices, itemized bills).
- The company policy document: a single comprehensive PDF containing rules, exceptions, per diems, and visual decision flowcharts.

The decision requires determining:
1. Decision: `approved`, `rejected`, or `partially_approved`.
2. Exact reimbursement amount in USD/EUR.
3. Policy rules cited to justify the adjudication.

## Workshop Progression (4 Stages)

Participants evolve the agent across four discrete stages. Each stage exposes a specific failure mode in real-world agent design:

### Stage 1: Full-Context Prose Dump
- **Setup**: Dump the claim, receipts, and full policy text directly into prompt context. Ask the model for a freeform prose decision.
- **Failure mode**: Unstructured, non-deterministic output. Impossible to evaluate programmatically or integrate into downstream automated systems. High hallucination risk.

### Stage 2: Structured Outputs & Deterministic Evals
- **Setup**: Enforce a strict JSON / Pydantic schema (`decision`, `amount`, `cited_rules`). Connect the agent to a deterministic evaluation runner.
- **Failure mode**: While responses can now be graded automatically, dumping large policy manuals into context is slow, expensive, and fails on complex multi-rule scenarios or subtle exceptions buried across pages.

### Stage 3: Naive Text RAG / Search Tool
- **Setup**: Agent receives a standard text search / retrieval tool over chunked policy text to look up relevant guidelines on demand before outputting structured JSON.
- **The Trap**: Real enterprise policy documents contain non-textual rules. In this case, the policy PDF includes a critical visual flowchart (e.g. *Weekend / Client Entertainment Approval Decision Tree*) on one of the pages. Text extraction renders this diagram as garbled ASCII or a placeholder (`[Figure 2: Approval Policy Flowchart - see document]`).
- **Failure mode**: Evaluation score plateaus (~60–70%). Cases that depend on the visual flowchart fail consistently because text search cannot resolve the logic.

### Stage 4: Tool Engineering & Multimodal Inspection (Hill Climbing)
- **Setup**: Participants run the eval runner, inspect execution traces and tool call logs for failing cases, and identify that the model is blinded by the missing flowchart.
- **Solution**: Participants equip the agent with a multimodal tool: `view_page_image(page_number)` that renders the specified PDF page as an image for the vision model.
- **Outcome**: The agent uses fast text search to locate relevant policy sections, detects the visual diagram reference, calls `view_page_image` to inspect the flowchart, and resolves the exception correctly. Eval score reaches ~95–100%.

## Deterministic Evaluation

Avoid LLM-as-a-judge where possible. Evaluate solely against ground-truth synthetic test cases:

- **Decision accuracy**: Exact match on status (`approved` / `rejected` / `partially_approved`).
- **Reimbursement error**: Absolute difference ($) between model-calculated payout and ground-truth payout.
- **Policy citation accuracy**: Set overlap / precision-recall of cited policy rule IDs.
- **Tool efficiency & variance**: Valid tool call sequence, tool call count, and consistency over $N$ runs where appropriate.

## Repository & Architecture Constraints

- **Modularity between stages**: Code for Stages 1–4 must remain self-contained and modular so they can be separated into discrete git tags, branches, or subdirectories later.
- **No leakages**: Ensure later-stage solutions (such as visual tools or golden prompts) do not leak into earlier stages where coding agents like Codex could inspect them.
- **Minimal abstractions**: Avoid heavy agent frameworks (LangChain, CrewAI, etc.). Use lightweight, standard Python with direct API calls and clear tool loops so participants focus on system design rather than framework quirks.
