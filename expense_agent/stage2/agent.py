"""Build the Stage 2 agent: handbook search tool in, `CaseDecision` out.

Instead of dumping the whole handbook into the prompt, the agent gets a
`search_handbook` tool. The tool greps the handbook's text for the query
terms and returns the top ten matching lines with surrounding context,
each tagged with a page number, so the model retrieves only what it needs.

Usage:
    from pathlib import Path

    from expense_agent.stage2 import HandbookSearch, build_agent

    search = HandbookSearch.from_pdf(Path("data/handbook.pdf"))
    agent = build_agent(search)
"""

from __future__ import annotations

from pydantic_ai import Agent

from expense_agent.harness import CaseInput
from expense_agent.label import CaseDecision
from expense_agent.stage2.prompts import SYSTEM_PROMPT
from expense_agent.stage2.search import DEFAULT_RESULTS, HandbookSearch

DEFAULT_MODEL = "openai:gpt-5.6-luna"


def build_agent(
    search: HandbookSearch,
    model: str = DEFAULT_MODEL,
) -> Agent[CaseInput, CaseDecision]:
    """Build the Stage 2 agent around a prepared handbook search index."""
    agent = Agent(model, deps_type=CaseInput, output_type=CaseDecision, system_prompt=SYSTEM_PROMPT)

    @agent.tool_plain
    def search_handbook(query: str) -> str:
        """Search the policy handbook for passages relevant to the expense case.

        Pass a few keywords or a short question, such as "nightly room cap
        Amsterdam" or "weekend dinner approval". Returns a ranked list of
        numbered passages, each tagged with its handbook page number.
        """
        return search.format(search.search(query, k=DEFAULT_RESULTS))

    return agent
