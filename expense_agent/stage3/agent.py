"""Build the Stage 3 agent: search plus page images, `CaseDecision` out.

Stage 3 keeps Stage 2's handling of the handbook's text and adds the
missing half: the decision flowcharts are images, so a text search only
ever returns their title. The agent gets a second tool,
`view_page_image(page_number)`, which renders the page a search hit named
and hands the image to the vision model.

`search_handbook` reports each hit's page number, which is what lets the
agent move from a text match to the page it must inspect.

Usage:
    from pathlib import Path

    from expense_agent.stage2 import HandbookBM25
    from expense_agent.stage3 import build_agent

    pdf_path = Path("data/handbook.pdf")
    agent = build_agent(HandbookBM25.from_pdf(pdf_path), pdf_path)
"""

from __future__ import annotations

from pathlib import Path

from pydantic_ai import Agent, BinaryContent

from expense_agent.harness import CaseInput
from expense_agent.label import CaseDecision
from expense_agent.stage2.bm25 import HandbookBM25
from expense_agent.stage2.search import DEFAULT_RESULTS
from expense_agent.stage3.pages import render_page
from expense_agent.stage3.prompts import SYSTEM_PROMPT

DEFAULT_MODEL = "openai:gpt-5.6-luna"


def build_agent(
    search: HandbookBM25,
    pdf_path: Path,
    model: str = DEFAULT_MODEL,
) -> Agent[CaseInput, CaseDecision]:
    """Build the Stage 3 agent around a BM25 index and the handbook PDF."""
    agent = Agent(model, deps_type=CaseInput, output_type=CaseDecision, system_prompt=SYSTEM_PROMPT)

    @agent.tool_plain
    def search_handbook(query: str) -> str:
        """Search the policy handbook for passages relevant to the expense case.

        Pass a few keywords or a short question, such as "nightly room cap
        Amsterdam" or "weekend dinner approval". Returns a ranked list of
        numbered passages, each tagged with its handbook page number. Open a
        result's page with `view_page_image` when the passage is cut off or a
        rule depends on a diagram.
        """
        return search.format(search.search(query, k=DEFAULT_RESULTS))

    @agent.tool_plain
    def view_page_image(page_number: int) -> BinaryContent:
        """Open one handbook page as an image.

        Use the page number printed in a `search_handbook` result, counted
        from 1. Returns the rendered page so you can read diagrams, tables,
        and decision flowcharts that have no extractable text.
        """
        return render_page(pdf_path, page_number)

    return agent
