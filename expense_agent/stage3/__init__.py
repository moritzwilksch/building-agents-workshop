"""Stage 3: BM25 search plus page-image inspection.

The agent searches the handbook by topic, reads the page number on each
hit, and opens the flowchart pages as images with `view_page_image`. It
returns the same structured `CaseDecision` as the earlier stages.

Participant-facing reference implementation. This is the stage that
recovers the rules Stage 2 cannot reach, because Figures 1 to 3 exist
only as images.
"""

from expense_agent.stage3.agent import build_agent
from expense_agent.stage3.pages import render_page
from expense_agent.stage3.prompts import SYSTEM_PROMPT

__all__ = [
    "SYSTEM_PROMPT",
    "build_agent",
    "render_page",
]
