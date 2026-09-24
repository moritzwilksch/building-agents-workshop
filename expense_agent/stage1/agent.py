"""Stage 1 agent: put the complete handbook in the prompt."""

from pathlib import Path

from pydantic_ai import Agent

from expense_agent.harness import OUTPUT_RETRIES, CaseInput, validate_reimbursements
from expense_agent.label import AgentOutput
from expense_agent.model import MODEL
from expense_agent.stage1.tools import read_handbook

SYSTEM_PROMPT = (Path(__file__).parent / "prompts" / "system.md").read_text(encoding="utf-8")
HANDBOOK_PDF = Path("data/handbook.pdf")


def build_agent() -> Agent[CaseInput, AgentOutput]:
    """Build the Stage 1 agent.

    Extracts the handbook text once here, before any case runs, and closes
    the system prompt over it. Left to the first system prompt, every
    concurrent case would extract its own copy at the same time and the run
    would stall for minutes at the start.
    """
    handbook = read_handbook(HANDBOOK_PDF)
    agent = Agent(MODEL, deps_type=CaseInput, output_type=AgentOutput, retries=OUTPUT_RETRIES)
    agent.output_validator(validate_reimbursements)

    @agent.system_prompt
    def system_prompt() -> str:
        return SYSTEM_PROMPT.format(handbook=handbook)

    return agent
