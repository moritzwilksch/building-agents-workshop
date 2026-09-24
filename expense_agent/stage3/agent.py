"""Stage 3 agent: Stage 2's tools plus handbook page-image inspection."""

from pathlib import Path

from pydantic_ai import Agent

from expense_agent.harness import OUTPUT_RETRIES, TOOL_RETRIES, CaseInput, validate_reimbursements
from expense_agent.label import AgentOutput
from expense_agent.model import MODEL
from expense_agent.stage2.tools import HandbookSearch, calculate_tax
from expense_agent.stage3.tools import HandbookImages

SYSTEM_PROMPT = (Path(__file__).parent / "prompts" / "system.md").read_text(encoding="utf-8")
HANDBOOK_PDF = Path("data/handbook.pdf")


def build_agent() -> Agent[CaseInput, AgentOutput]:
    """Build the Stage 3 agent.

    Indexes the handbook here, before any case runs, for the reason given in
    `expense_agent.stage2.agent.build_agent`.
    """
    handbook = HandbookSearch(HANDBOOK_PDF)
    images = HandbookImages(HANDBOOK_PDF, handbook)
    agent = Agent(
        MODEL,
        deps_type=CaseInput,
        output_type=AgentOutput,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            handbook.search_handbook,
            handbook.read_handbook_page,
            images.view_page_image,
            calculate_tax,
        ],
        retries={"tools": TOOL_RETRIES, "output": OUTPUT_RETRIES},
    )
    agent.output_validator(validate_reimbursements)
    return agent
