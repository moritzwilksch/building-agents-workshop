"""Offline checks for shared scaffolding, not participant implementations."""

import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from pydantic_ai import ModelRetry

from expense_agent import benchmark
from expense_agent.check_setup import check_data
from expense_agent.harness import CaseInput, CaseLoader
from expense_agent.harness.runner import complete_decision, validate_reimbursements
from expense_agent.invoice import ChargeLine
from expense_agent.label import AgentOutput


class BenchmarkTests(unittest.TestCase):
    def test_discovery_works_with_only_stage_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "stage0").mkdir()
            (root / "stage0" / "agent.py").touch()
            with patch.object(benchmark, "__file__", str(root / "benchmark.py")):
                self.assertEqual(benchmark.available_stages(), [0])

    def test_help_does_not_import_stage_implementations(self):
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import sys; import expense_agent.benchmark; "
                "assert not any(name.startswith('expense_agent.stage') for name in sys.modules)",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unimplemented_agent_has_actionable_error(self):
        with (
            patch.object(sys, "argv", ["benchmark", "--stage", "0", "--suite", "small"]),
            patch.object(benchmark, "import_module") as import_module,
            patch.object(benchmark, "RunStore") as store,
            patch("argparse.ArgumentParser.error", side_effect=ValueError) as error,
        ):
            import_module.return_value.build_agent.return_value = None
            with self.assertRaises(ValueError):
                benchmark.main()
            self.assertIn("implement build_agent()", error.call_args.args[0])
            store.assert_not_called()

    def test_suites_use_existing_cases(self):
        loader = CaseLoader()
        self.assertEqual(len(benchmark.select_cases(loader, "small")), 5)
        self.assertEqual(len(benchmark.select_cases(loader, "hard")), 10)
        self.assertEqual(benchmark.select_cases(loader, "full"), loader.case_ids())


class SetupTests(unittest.TestCase):
    def test_shipped_data_is_readable_and_consistent(self):
        loader = CaseLoader()
        self.assertEqual(check_data(loader), len(loader.case_ids()))

    def test_lfs_pointer_has_recovery_command(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "handbook.pdf").write_text("version https://git-lfs.github.com/spec/v1\n")
            with self.assertRaisesRegex(ValueError, "pixi run git lfs pull"):
                check_data(CaseLoader(root))


class InterfaceTests(unittest.TestCase):
    def setUp(self):
        self.case = CaseInput(
            case_id="test-case",
            receipt_image=Path("receipt.jpg"),
            handbook_pdf=Path("handbook.pdf"),
            charges=[ChargeLine(id=0, description="Meal", amount=Decimal("10"))],
        )

    def test_harness_completes_agent_output(self):
        output = AgentOutput(reimbursements=[Decimal("5")], reasoning="A policy cap applies.")
        decision = complete_decision(self.case, output)
        self.assertEqual(decision.decision, "partially_approved")
        self.assertEqual(decision.claimed_amount, Decimal("10"))
        self.assertEqual(decision.reimbursed_amount, Decimal("5"))
        self.assertEqual(decision.line_items[0].id, 0)

    def test_validator_requests_retry_for_overpayment(self):
        from types import SimpleNamespace

        output = AgentOutput(reimbursements=[Decimal("11")], reasoning="Too much.")
        with self.assertRaises(ModelRetry):
            validate_reimbursements(SimpleNamespace(deps=self.case), output)


if __name__ == "__main__":
    unittest.main()
