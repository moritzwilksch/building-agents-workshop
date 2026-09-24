# Building reliable agents

Build an expense agent, inspect its mistakes, and improve it one capability at a time. Stage 0 is your template; later tagged checkouts reveal reference approaches. See [workshop context](CONTEXT.md) for the task and learning goals.

## Installation

Supported: Apple Silicon macOS, Windows x64, and Linux x64. Pixi supplies Python and dependencies.

### 1. Install Pixi

macOS / Linux terminal:

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://pixi.sh/install.ps1 | iex"
```

Reopen your terminal, then run `pixi --version`. See the [Pixi installation guide](https://pixi.sh/latest/installation/) for alternatives.

### 2. Get the repository and data

Use the instructor's repository URL. This command supplies Git and Git LFS:

```bash
pixi exec --spec git --spec git-lfs -- git clone WORKSHOP_REPOSITORY_URL building-agents-workshop
cd building-agents-workshop
pixi install --locked
pixi run git lfs install --local
pixi run git lfs pull
```

Run remaining commands from this directory. The first download takes a few minutes; receipts and the handbook are included. Use `pixi run git ...` for Git commands.

### 3. Configure model access

Copy `.env.example` to `.env` and replace `...` with your instructor-approved OpenAI API key. Keep it private; `.env` is ignored by Git. If the instructor gave you a password, `pixi run get-api-key` prompts for it and prints the key.

Confirm access to the model in `expense_agent/model.py` and agree on a spending limit. Benchmarks send synthetic workshop data to OpenAI and incur API charges, separate from a ChatGPT subscription.

### 4. Check setup without spending API credits

```bash
pixi run check-setup
pixi run benchmark --help
```

This checks local data and tools without model calls. Credentials and model access remain untested. Stage 0 is intentionally blank: implement it before benchmarking, or run a reference stage from the commands below.

## Exercise loop

Stuck? [hints.md](hints.md) offers ideas for prompts, search, calculation tools, and page images—available from Stage 0 onward.

1. Open `expense_agent/stage0/`. Implement `build_agent()`, write a prompt, and add only the helpers you need. Use the interface and Pydantic AI examples below for guidance.
2. Run `pixi run benchmark --stage 0 --suite small`. Each run gets a timestamp ID.
3. In a second terminal, run `pixi run viewer` and open <http://127.0.0.1:8000>. Select your run, then a failed or mismatched case. Compare the receipt, reimbursement differences, and model/tool trace.
4. Write down one hypothesis, change one thing, and rerun the same suite. Compare correctness, failures, tokens, and cost. A failed request is not a policy mistake.
5. Try the hard suite, then the full suite. Record what improved, what regressed, and what you would try next. A useful explanation matters more than a perfect score.

Work in your assigned stage. Extend your previous implementation, or copy Stage 0 into `stageN/` for a fresh start. Use relative imports within the copied stage; the benchmark discovers it automatically.

### Stage checkouts

Start at `stage-0`. When you want a reference implementation or need to catch up, check out the next tag. Each tag adds one stage directory; earlier stages remain available. Save your changes before switching: a tag checkout does not carry your implementation into the reference stage.

```bash
pixi run git switch --detach stage-0
# When you explicitly want to see the Stage 1 reference:
pixi run git switch --detach stage-1
```

To keep working on your own code, create a branch before editing (for example, `pixi run git switch -c my-stage-0 stage-0`). Commit your work on that branch before switching to another tag. You can return with `pixi run git switch my-stage-0`. Ask your coding agent to help you build the next stage before opening its reference.

For optional guidance, the reference approaches explore:

- **Stage 1:** What happens when all handbook text goes into the prompt?
- **Stage 2:** Can retrieval and deterministic arithmetic improve the trade-off?
- **Stage 3:** Which mistakes remain because text extraction cannot see a rule?

Try your own approach before opening a later stage. Use the next tag only when you want to inspect or fast-forward to its reference.

### Working with a coding agent

Name your stage and ask for one small change at a time:

> Help me build Stage 0. Explain each change and let me choose the approach. Stay in this stage and shared scaffolding; leave later stages, Git history, labels, and instructor files unread. Diagnose mistakes from benchmark traces without hard-coding payouts.

Leave data, scoring, and the harness unchanged. Expected decisions are evaluation evidence, not agent inputs. These boundaries are an honor system, not access control.

## Commands

```bash
# Run 5 cases
pixi run benchmark --stage 1 --suite small

# Run all 50 cases
pixi run benchmark --stage 1 --suite full

# Run the 10 cases agents get wrong most often
pixi run benchmark --stage 1 --suite hard

# Inspect saved runs
pixi run viewer
```

Replace `1` with your stage. Optionally add `--run-id NAME` with a fresh name. Runs live in `data/runs.sqlite3`; the viewer starts empty.

Cost estimates may show zero for unpriced models; check provider billing.

## What to edit

Each stage has the same structure:

```text
expense_agent/stageN/
├── __init__.py
├── agent.py
├── tools.py
└── prompts/
    └── system.md
```

- Edit `prompts/system.md` to change the prompt.
- Edit `tools.py` to add or change tools.
- Edit `agent.py` to assemble the agent.

Every `agent.py` must expose this entry point:

```python
def build_agent() -> Agent[CaseInput, AgentOutput]:
    ...
```

Keep earlier stages intact and import tools you reuse rather than copying them.

The benchmark supplies `CaseInput`. Return reimbursements in charge order and reasoning as `AgentOutput`; the harness adds IDs, totals, and the overall decision.

## Pydantic AI cheat sheet

### Add a tool

A tool's signature and docstring tell the model how to call it. Access the current case through `RunContext`:

```python
from pydantic_ai import RunContext

from expense_agent.harness import CaseInput


def read_note(ctx: RunContext[CaseInput]) -> str:
    """Read the employee's submission note."""
    return ctx.deps.note or "(none)"
```

For expensive setup, construct an object once in `build_agent()` and register its methods as tools:

```python
from pathlib import Path


class HandbookSearch:
    def __init__(self, pdf_path: Path) -> None:
        self.index = ...  # a few seconds of work

    def search_handbook(self, query: str) -> str:
        """Search the policy handbook for relevant pages."""
        return ...
```

### Assemble an agent

Connect the model, case data, tools, and output schema. Register the reimbursement validator to let the model correct invalid output once. Keep prompt text in `prompts/system.md`.

This example assumes you have implemented `HandbookSearch` in your stage's `tools.py`; the sketch above is not a working search tool.

```python
from pathlib import Path

from pydantic_ai import Agent

from expense_agent.harness import OUTPUT_RETRIES, CaseInput, validate_reimbursements
from expense_agent.label import AgentOutput
from expense_agent.model import MODEL

from .tools import HandbookSearch

SYSTEM_PROMPT = (Path(__file__).parent / "prompts" / "system.md").read_text(encoding="utf-8")
HANDBOOK_PDF = Path("data/handbook.pdf")


def build_agent() -> Agent[CaseInput, AgentOutput]:
    handbook = HandbookSearch(HANDBOOK_PDF)
    agent = Agent(
        MODEL,
        deps_type=CaseInput,
        output_type=AgentOutput,
        system_prompt=SYSTEM_PROMPT,
        tools=[handbook.search_handbook],
        retries=OUTPUT_RETRIES,
    )
    agent.output_validator(validate_reimbursements)
    return agent
```

## Troubleshooting

| Symptom | Next step |
| --- | --- |
| `pixi` not found | Reopen the terminal after installation. |
| Unsupported platform | Ask the instructor for a supported machine or hosted environment. |
| PDF/image cannot be read, or a tiny text file replaces an image | Run `pixi run git lfs pull`, then `pixi run check-setup`. |
| Missing API key / 401 | Check `.env` in the repository root; restart the benchmark. |
| Model not found / access denied | Confirm the model in `expense_agent/model.py` and account access with the instructor. |
| 429 / rate limit | Retry with `--concurrency 1`; check account quota and billing. |
| Stage 0 is a template | Implement `build_agent()` and return an `Agent`; this is not an installation failure. |
| Run ID already exists | Choose a fresh `--run-id`, or omit it. |
| No runs in the viewer | Complete a benchmark first and start the viewer from the same checkout. |

Stop the viewer with Ctrl+C. Its styling and icons need internet access. Saved traces can contain prompts and notes; use only the workshop's synthetic data.

## Maintaining the workshop

- `pixi run test`: offline scaffolding tests.
- `pixi run lint`: format and fix code.
- `pixi run pre-commit-install`: optional maintainer hook.

See [workshop context](CONTEXT.md) for the exercise goals.
