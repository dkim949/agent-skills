"""Exercise runtime safety checks with tiny commands and simulated capacity."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT_PATH = ROOT / "skills/engineering/safe-local-run/scripts/preflight.py"
RUNNER_PATH = ROOT / "skills/engineering/run-and-verify/scripts/run_logged.sh"
SAFE_RUN_PATH = ROOT / "skills/engineering/safe-local-run/scripts/safe_run.sh"
SPEC = importlib.util.spec_from_file_location("runtime_preflight", PREFLIGHT_PATH)
assert SPEC is not None and SPEC.loader is not None
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)


class RuntimeTests(unittest.TestCase):
    """Keep runtime regressions independent of host RAM and operating system."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="runtime-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)

    def run_preflight(
        self, *args: str, available: float | None = 16.0, total: float | None = 32.0
    ) -> tuple[int, str]:
        output = io.StringIO()
        with (patch.object(sys, "argv", [str(PREFLIGHT_PATH), *args]),
              patch.object(preflight, "total_ram_gb", return_value=total),
              patch.object(preflight, "available_ram_gb", return_value=available),
              contextlib.redirect_stdout(output), contextlib.redirect_stderr(output)):
            try:
                code = preflight.main()
            except SystemExit as error:
                code = error.code
        return code, output.getvalue()

    def test_zero_available_capacity_refuses_safe_verdict(self) -> None:
        code, output = self.run_preflight("--budget-gb", "8", "--est-gb", "1", available=0.0)
        self.assertNotEqual(code, 0)
        self.assertNotIn("verdict: SAFE", output)

    def test_unknown_or_invalid_capacity_refuses_safe_verdict(self) -> None:
        for available in (None, -1.0, float("nan"), float("inf"), -float("inf")):
            with self.subTest(available=available):
                code, output = self.run_preflight("--est-gb", "1", available=available)
                self.assertNotEqual(code, 0)
                self.assertIn("verdict: ABORT", output)

    def test_unavailable_capacity_probe_returns_unknown(self) -> None:
        with (patch.dict(sys.modules, {"psutil": None}),
              patch.object(preflight.subprocess, "check_output", side_effect=OSError("unavailable"))):
            self.assertIsNone(preflight.available_ram_gb())
            self.assertIsNone(preflight.total_ram_gb())

    def test_unknown_total_cannot_supply_default_budget(self) -> None:
        code, output = self.run_preflight("--est-gb", "1", total=None)
        self.assertNotEqual(code, 0)
        self.assertIn("verdict: ABORT", output)

    def test_budget_must_be_positive_and_finite(self) -> None:
        for budget in ("0", "-1", "nan", "inf"):
            with self.subTest(budget=budget):
                code, output = self.run_preflight("--budget-gb", budget, "--est-gb", "1")
                self.assertNotEqual(code, 0)
                self.assertIn("--budget-gb must be positive and finite", output)

    def test_estimate_must_be_nonnegative_and_finite(self) -> None:
        for estimate in ("-1", "nan", "inf"):
            with self.subTest(estimate=estimate):
                code, output = self.run_preflight("--est-gb", estimate)
                self.assertNotEqual(code, 0)
                self.assertIn("--est-gb must be finite and nonnegative", output)

    def test_missing_input_cannot_support_safe_verdict(self) -> None:
        code, output = self.run_preflight("--est-gb", "1", str(self.base / "missing.csv"))
        self.assertNotEqual(code, 0)
        self.assertIn("verdict: ABORT", output)
        self.assertNotIn("verdict: SAFE", output)

    def test_positive_capacity_can_report_safe_for_small_input(self) -> None:
        source = self.base / "tiny.csv"
        source.write_text("value\n1\n", encoding="utf-8")
        code, output = self.run_preflight(str(source))
        self.assertEqual(code, 0)
        self.assertIn("verdict: SAFE", output)

    def test_zero_estimate_requires_more_information(self) -> None:
        code, output = self.run_preflight("--est-gb", "0")
        self.assertEqual(code, 0)
        self.assertIn("verdict: NO ESTIMATE", output)

    def test_displayed_sample_fraction_stays_within_half_headroom(self) -> None:
        for estimate in (1000, 600):
            with self.subTest(estimate=estimate):
                code, output = self.run_preflight(
                    "--budget-gb", "2", "--est-gb", str(estimate), available=2.0
                )
                self.assertEqual(code, 0)
                match = re.search(r"sample frac<= ([0-9.]+)", output)
                self.assertIsNotNone(match, output)
                fraction = float(match.group(1))
                self.assertLessEqual(fraction * estimate, 1.0)
                self.assertEqual(fraction, 0.001)

    def test_fraction_below_display_precision_requires_abort_and_stream(self) -> None:
        code, output = self.run_preflight(
            "--budget-gb", "2", "--est-gb", "1500", available=2.0
        )
        self.assertNotEqual(code, 0)
        self.assertIn("verdict: ABORT", output)
        self.assertIn("stream by row-group/chunk", output)
        self.assertNotIn("sample frac<=", output)

    def test_supervisor_preserves_output_and_success_metadata(self) -> None:
        log = self.base / "success.log"
        result = subprocess.run(
            ["bash", str(RUNNER_PATH), "--timeout", "3", "--log", str(log), "--",
             sys.executable, "-c", "import sys; print('stdout marker'); print('stderr marker', file=sys.stderr)"],
            capture_output=True, text=True, timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        for marker in ("stdout marker", "stderr marker"):
            self.assertIn(marker, result.stdout)
            self.assertIn(marker, log.read_text(encoding="utf-8"))
        for marker in ("PRODUCER_EXIT_CODE=0", "LOGGER_EXIT_CODE=0", "EXIT_CODE=0"):
            self.assertIn(marker, result.stdout)

    def test_supervisor_preserves_failure_exit_metadata(self) -> None:
        result = subprocess.run(
            ["bash", str(RUNNER_PATH), "--timeout", "3", "--log", str(self.base / "failure.log"),
             "--", sys.executable, "-c", "raise SystemExit(7)"],
            capture_output=True, text=True, timeout=5,
        )
        self.assertEqual(result.returncode, 7, result.stderr)
        self.assertIn("PRODUCER_EXIT_CODE=7", result.stdout)
        self.assertIn("LOGGER_EXIT_CODE=0", result.stdout)
        self.assertIn("EXIT_CODE=7", result.stdout)

    def test_supervisor_short_timeout(self) -> None:
        result = subprocess.run(
            ["bash", str(RUNNER_PATH), "--timeout", "0.1", "--log", str(self.base / "timeout.log"),
             "--", sys.executable, "-c", "import time; time.sleep(2)"],
            capture_output=True, text=True, timeout=5,
        )
        self.assertEqual(result.returncode, 124, result.stderr)
        self.assertIn("TIMED_OUT=1", result.stdout)
        self.assertIn("EXIT_CODE=124", result.stdout)

    def test_safe_runner_missing_companion_does_not_launch_command(self) -> None:
        isolated_runner = self.base / "safe-local-run/scripts/safe_run.sh"
        isolated_runner.parent.mkdir(parents=True)
        shutil.copyfile(SAFE_RUN_PATH, isolated_runner)
        sentinel = self.base / "command-launched"
        result = subprocess.run(
            ["bash", str(isolated_runner), "--", sys.executable, "-c",
             "from pathlib import Path; import sys; Path(sys.argv[1]).touch()", str(sentinel)],
            capture_output=True, text=True, timeout=3,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("install the companion run-and-verify skill", result.stderr)
        self.assertFalse(sentinel.exists())


if __name__ == "__main__":
    unittest.main()
