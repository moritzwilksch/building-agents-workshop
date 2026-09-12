"""Build the Stage 1 agent: handbook and receipt in, `CaseDecision` out.

The full policy handbook goes into the user prompt. `AgentRunner` adds the
case-specific receipt image.

Usage:
    from expense_agent.stage1 import build_agent, handbook_prompt

    handbook = handbook_prompt(extract_handbook_text(Path("data/handbook.pdf")))
    agent = build_agent()
    runner = AgentRunner(agent, RunStore(), CaseLoader(), prompt=handbook)
"""

from __future__ import annotations

from pathlib import Path

from pydantic_ai import Agent
from pypdf import PdfReader

from expense_agent.harness import CaseInput
from expense_agent.label import CaseDecision
from expense_agent.stage1.prompts import HANDBOOK_PROMPT, SYSTEM_PROMPT

DEFAULT_MODEL = "openai:gpt-5.6-luna"


def extract_handbook_text(pdf_path: Path) -> str:
    """Extract all handbook text in page order. Images yield no text."""
    reader = PdfReader(pdf_path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages).strip()


def handbook_prompt(handbook_text: str) -> str:
    """Insert the extracted handbook into the user prompt."""
    return HANDBOOK_PROMPT.format(handbook=handbook_text).strip()


def build_agent(model: str = DEFAULT_MODEL) -> Agent[CaseInput, CaseDecision]:
    """Build the Stage 1 agent. The caller supplies the handbook user prompt."""
    return Agent(model, deps_type=CaseInput, output_type=CaseDecision, system_prompt=SYSTEM_PROMPT)
