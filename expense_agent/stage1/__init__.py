"""Stage 1: full-context prompt dump.

The simplest agent that can produce a gradeable decision. It extracts the
entire policy handbook to text, puts it and the receipt image in the user
prompt, and asks the model for a `CaseDecision`.

Participant-facing reference implementation. Not a solution to later
stages: the flowchart pages are images, so their rules never reach the
text prompt.
"""

from expense_agent.stage1.agent import (
    build_agent,
    extract_handbook_text,
    handbook_prompt,
)
from expense_agent.stage1.prompts import SYSTEM_PROMPT

__all__ = [
    "SYSTEM_PROMPT",
    "build_agent",
    "extract_handbook_text",
    "handbook_prompt",
]
