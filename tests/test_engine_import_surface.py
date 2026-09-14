"""The supported engine module entry points remain usable after refactoring."""

import subprocess
import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ImportSurfaceTests(unittest.TestCase):
    def test_each_entry_module_runs_as_a_module_with_its_arguments(self) -> None:
        for name in ("validate_engineering_artifacts", "generate_harness_dashboard", "inspect_engineering_artifacts"):
            with self.subTest(module=name):
                completed = subprocess.run(
                    [sys.executable, "-m", f"se_harness.engine.{name}", "--help"],
                    cwd=REPOSITORY_ROOT, capture_output=True, text=True, timeout=120,
                )
                self.assertEqual(0, completed.returncode, completed.stderr)
                self.assertIn("--root", completed.stdout)


if __name__ == "__main__":
    unittest.main()
