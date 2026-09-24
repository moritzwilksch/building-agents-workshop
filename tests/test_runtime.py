"""Exercise agent construction, persistence, tools, and viewer without API calls."""

import asyncio
import importlib
import io
import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from pydantic_ai import Agent
from pydantic_ai.messages import ModelRequest, ModelResponse, ToolCallPart, UserPromptPart
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.models.test import TestModel

from expense_agent import benchmark
from expense_agent.benchmark import available_stages
from expense_agent.harness import AgentRunner, CaseInput, CaseLoader
from expense_agent.label import AgentOutput
from expense_agent.tracking import RunStore


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(tempfile.TemporaryDirectory())
        self.store = RunStore(Path(directory) / "runs.sqlite3")
        self.loader = CaseLoader()
        self.case_id = self.loader.case_ids()[0]
        case = self.loader.load_input(self.case_id)
        self.model = TestModel(
            call_tools=[],
            custom_output_args={
                "reimbursements": ["0"] * len(case.charges),
                "reasoning": "Offline smoke test; not a policy judgment.",
            },
        )
        self.enterContext(patch("pydantic_ai.models.ALLOW_MODEL_REQUESTS", False))

    def run_agent(self, agent, run_id):
        return asyncio.run(AgentRunner(agent, self.store, self.loader).run([self.case_id], run_id))

    def test_reference_agents_and_saved_traces(self):
        for stage in sorted(set(available_stages()) & {1, 2, 3}):
            with self.subTest(stage=stage):
                module = importlib.import_module(f"expense_agent.stage{stage}.agent")
                with patch.object(module, "MODEL", self.model):
                    agent = module.build_agent()
                run = self.run_agent(agent, f"stage-{stage}")
                self.assertEqual(run.metrics.failed_cases, 0)
                saved = self.store.load(run.run_id)
                self.assertEqual(saved.cases[0].actual, run.cases[0].actual)
                self.check_viewer(run.run_id)

    def test_benchmark_cli_runs_small_suite(self):
        def respond(messages, info):
            content = next(
                part.content
                for message in messages
                if isinstance(message, ModelRequest)
                for part in message.parts
                if isinstance(part, UserPromptPart)
            )
            prompt = content[0]
            charges = json.loads(prompt.split("amount):\n", 1)[1].split("\nReceipt:", 1)[0])
            return ModelResponse(
                parts=[
                    ToolCallPart(
                        info.output_tools[0].name,
                        {
                            "reimbursements": ["0"] * len(charges),
                            "reasoning": "Offline CLI test.",
                        },
                    )
                ]
            )

        agent = Agent(FunctionModel(respond), deps_type=CaseInput, output_type=AgentOutput)
        with (
            patch.object(sys, "argv", ["benchmark", "--stage", "0", "--suite", "small"]),
            patch.object(benchmark, "import_module") as module,
            patch.object(benchmark, "RunStore", return_value=self.store),
            patch.object(benchmark, "configure_logging"),
            redirect_stdout(io.StringIO()) as output,
        ):
            module.return_value.build_agent.return_value = agent
            benchmark.main()
        run = self.store.list_runs()[0]
        self.assertEqual(run.metrics.total_cases, 5)
        self.assertEqual(run.metrics.failed_cases, 0)
        self.assertIn("pass_rate=", output.getvalue())

    def test_duplicate_run_id_stops_before_model_call(self):
        agent = Agent(self.model, deps_type=CaseInput, output_type=AgentOutput)
        self.run_agent(agent, "existing")
        with patch.object(agent, "run") as request:
            with self.assertRaisesRegex(ValueError, "choose a new --run-id"):
                self.run_agent(agent, "existing")
            request.assert_not_called()

    def test_database_connections_close(self):
        with self.store._connect() as connection:
            connection.execute("SELECT 1")
        with self.assertRaises(sqlite3.ProgrammingError):
            connection.execute("SELECT 1")

    def test_failed_request_is_saved_and_viewable(self):
        def fail(messages, info):
            raise RuntimeError("Offline simulated API failure")

        agent = Agent(FunctionModel(fail), deps_type=CaseInput, output_type=AgentOutput)
        run = self.run_agent(agent, "failure")
        self.assertEqual(run.metrics.failed_cases, 1)
        self.assertIn("simulated API failure", self.store.load("failure").cases[0].error)
        self.check_viewer(run.run_id)

    def check_viewer(self, run_id):
        # Keep the app's import-time store out of the participant's database.
        with patch("expense_agent.tracking.RunStore", return_value=self.store):
            viewer = importlib.import_module("expense_agent.viewer.app")
        with patch.object(viewer, "store", self.store), TestClient(viewer.app) as client:
            for route in (
                "/",
                "/api/runs",
                f"/api/runs/{run_id}",
                f"/api/runs/{run_id}/cases/{self.case_id}",
                f"/api/runs/{run_id}/cases/{self.case_id}/trace",
                f"/api/cases/{self.case_id}/receipt",
            ):
                response = client.get(route)
                self.assertEqual(response.status_code, 200, route)
            self.assertEqual(client.get("/api/runs/missing").status_code, 404)

    def test_handbook_search_calculation_and_image_rendering(self):
        if 2 not in available_stages():
            self.skipTest("Stage 2 is not in this checkout")
        from decimal import Decimal

        from expense_agent.stage2.tools import HandbookSearch, calculate_tax

        search = HandbookSearch(Path("data/handbook.pdf"))
        hits = search.search_pages("taxi")
        self.assertTrue(hits)
        self.assertIn(f"Page {hits[0].number}", search.search_handbook("taxi"))
        self.assertIn(hits[0].text, search.read_handbook_page(hits[0].number))
        self.assertEqual(calculate_tax([Decimal("10")], Decimal("19")), Decimal("1.90"))
        if 3 in available_stages():
            from expense_agent.stage3.tools import HandbookImages

            images = HandbookImages(Path("data/handbook.pdf"), search)
            image = images.view_page_image(hits[0].number)
            self.assertEqual(image.media_type, "image/png")
            self.assertTrue(image.data.startswith(b"\x89PNG"))
            self.assertIs(images.view_page_image(hits[0].number), image)


if __name__ == "__main__":
    unittest.main()
