# Repository guidance

Read [`CONTEXT.md`](CONTEXT.md) for the workshop's goals, running example, progression, and evaluation approach.

This repository supports a teaching workshop. Keep code that participants build simple, explicit, and easy to reason about.

Prioritize clear examples over abstractions, cleverness, and premature optimization. Keep scaffolding and setup practical; it does not need the same teaching focus.

Code produced across the different workshop stages must remain modular and self-contained enough to be cleanly separated later (e.g. into discrete git tags or subdirectories). Maintain clear design boundaries between stages without introducing complex abstractions that confuse non-technical participants.

## Synthetic data

- `.data-generation/` is the instructor workspace for scripts that generate synthetic data.
- Run those scripts in the default Pixi environment; do not create a separate Pixi environment for them.
- Persist generated data in `data/`.
- Store large binary files, such as images and PDFs, with Git LFS.
