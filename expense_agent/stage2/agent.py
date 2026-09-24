"""Stage 2 agent: retrieve handbook text with BM25 page search and compute tax."""

from pathlib import Path

from pydantic_ai import Agent

from expense_agent.harness import OUTPUT_RETRIES, TOOL_RETRIES, CaseInput, validate_reimbursements
from expense_agent.label import AgentOutput
from expense_agent.model import MODEL
from expense_agent.stage2.tools import HandbookSearch, calculate_tax

SYSTEM_PROMPT = (Path(__file__).parent / "prompts" / "system.md").read_text(encoding="utf-8")
HANDBOOK_PDF = Path("data/handbook.pdf")


def build_agent() -> Agent[CaseInput, AgentOutput]:
    """Build the Stage 2 agent.

    Indexes the handbook here, before any case runs, and gives the model the
    index's own methods as tools. Indexing takes a few seconds, so leaving it
    to the first tool call would stall every concurrent case at once.
    """
    handbook = HandbookSearch(HANDBOOK_PDF)
    agent = Agent(
        MODEL,
        deps_type=CaseInput,
        output_type=AgentOutput,
        system_prompt=SYSTEM_PROMPT,
        tools=[handbook.search_handbook, handbook.read_handbook_page, calculate_tax],
        retries={"tools": TOOL_RETRIES, "output": OUTPUT_RETRIES},
    )
    agent.output_validator(validate_reimbursements)
    return agent
