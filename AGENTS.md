# Repository guidance

Read [`README.md`](README.md) for setup, stage checkouts, the exercise loop, and the shared agent interface. Read [`CONTEXT.md`](CONTEXT.md) for the participant-facing task and learning goals.

## Participant exercises

When helping a participant, establish their current stage and work there. Use shared scaffolding to understand the interface. When they need a direction or a hint, read [`hints.md`](hints.md); it is available from Stage 0 onward. Explain changes and let the participant choose an approach. The `stage-0` through `stage-3` tags are reference checkpoints for catching up, not the default route through the exercise. Guide the participant through their implementation first; inspect or check out a later tag only when they explicitly request the reference or a fast-forward. Keep later-stage implementations, Git history, and `.data-generation/` out of the exercise otherwise. Never use `data/case-*/label.json` or saved expected decisions as agent inputs or hard-code case-specific reimbursements. Use benchmark traces to diagnose failures; leave evaluation data and scoring unchanged.

This repository supports a teaching workshop. Keep code that participants build simple, explicit, and easy to reason about.

Prioritize clear examples over abstractions, cleverness, and premature optimization. Keep scaffolding and setup practical; it does not need the same teaching focus.

Treat the stages as cumulative. Participants receive each stage as a tagged checkout of this repository, so stage N starts from stage N-1 and adds one capability on top. A later stage imports participant-facing code from the stage it extends instead of copying it, and leaves the earlier stage's behavior intact. Keep each stage's increment small enough to read in one sitting, and keep design boundaries between stages clear without introducing abstractions that confuse non-technical participants.

## Commands

- Check local setup without model calls: `pixi run check-setup`.
- Test scaffolding without model calls: `pixi run test`.
- Bench an implemented stage: `pixi run benchmark --stage N --suite {small,hard,full} [--run-id NAME]`. Stage 0 starts unimplemented. Persists to `data/runs.sqlite3`.
- View runs: `pixi run viewer`.
- Rebuild handbook PDF (and figures): `pixi run -e data-generation compile-handbook`.
- Lint and fix all code: `pixi run lint`.
- Install the lefthook pre-commit hook: `pixi run pre-commit-install`.

## Prompts

- Store each stage's prompt text in a `prompts/` directory beside that stage's main agent module. Keep prompt text out of Python modules.
- Make each stage's prompt a superset of the previous stage's: carry every helpful instruction forward and add the new stage's instructions to it.

## Tools

- Put the tools a stage adds in that stage's `tools.py`. Reuse an earlier stage's tools by importing them.

## Synthetic data

- `.data-generation/` is the instructor workspace for scripts that generate synthetic data.
- Run those scripts in the default Pixi environment; do not create a separate Pixi environment for them.
- Persist generated data in `data/`.
- Store large binary files, such as images and PDFs, with Git LFS.
