"""Stage 0: assemble your first expense agent here."""

from pydantic_ai import Agent

from expense_agent.harness import CaseInput
from expense_agent.label import AgentOutput


def build_agent() -> Agent[CaseInput, AgentOutput]:
    # TODO: Build and return an agent; see README.md for the shared interface.
    pass
