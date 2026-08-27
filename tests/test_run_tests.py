"""Evidence for REQ-TST-001 and REQ-TST-002 (WO-TST-001): the parallel runner and the scale marker."""

from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = REPOSITORY_ROOT / "scripts" / "run_tests.py"


def _load_runner():
    # imported by its real module name so spawned worker processes can import it too
    scripts = str(RUNNER_PATH.parent)
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import run_tests

    return run_tests


RUNNER = _load_runner()

SCRATCH_SUITE = {
    "test_alpha.py": '''
        import os, unittest
        class Alpha(unittest.TestCase):
            def test_passes(self): self.assertTrue(True)
            def test_skipped(self): self.skipTest("on purpose")
            def test_sees_the_scale_marker(self):
                (__import__("pathlib").Path(__file__).parent / "marker.txt").write_text(os.environ.get("SE_HARNESS_TEST_SCALE", "unset"))
        class Beta(unittest.TestCase):
            def test_fails(self): self.assertEqual(1, 2)
            def test_passes(self): pass
    ''',
    "test_gamma.py": '''
        import unittest
        class Gamma(unittest.TestCase):
            def test_errors(self): raise RuntimeError("boom")
            def test_passes(self): pass
    ''',
    "test_broken.py": '''
        import unittest
        import module_that_does_not_exist  # noqa: F401
    ''',
}


class ScratchSuite:
    def __init__(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "suite").mkdir()
        for name, source in SCRATCH_SUITE.items():
            (self.root / "suite" / name).write_text(textwrap.dedent(source), encoding="utf-8")

    def plan(self, scale: str = "reduced") -> "RUNNER.Plan":
        return RUNNER.Plan(start_dir=str(self.root / "suite"), pattern="test_*.py", root_dir=str(self.root), scale=scale)

    def cleanup(self) -> None:
        self.temporary.cleanup()


class RunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = ScratchSuite()
        self.addCleanup(self.scratch.cleanup)

    def _run(self, workers: int, scale: str = "reduced", timings: Path | None = None):
        stream = io.StringIO()
        code, results = RUNNER.run(self.scratch.plan(scale), workers=workers, timings_path=timings, stream=stream)
        return code, results, stream.getvalue()

    def test_serial_and_parallel_report_the_same_verdict_including_the_import_error(self) -> None:
        serial_code, serial, serial_out = self._run(1)
        parallel_code, parallel, parallel_out = self._run(3)
        self.assertEqual(1, serial_code)
        self.assertEqual(1, parallel_code)

        def sets(results):
            return (
                sum(r.tests_run for r in results),
                sorted(identifier for r in results for identifier, _ in r.failures),
                sorted(identifier for r in results for identifier, _ in r.errors),
                sorted(identifier for r in results for identifier, _ in r.skipped),
            )

        self.assertEqual(sets(serial), sets(parallel))
        tests_run, failures, errors, skipped = sets(serial)
        self.assertEqual(7, tests_run)  # unittest counts the failed import as a run test, as discover does
        self.assertEqual(["test_alpha.Beta.test_fails"], failures)
        self.assertEqual(2, len(errors))
        self.assertIn("test_gamma.Gamma.test_errors", errors)
        self.assertTrue(any("test_broken" in identifier for identifier in errors), errors)
        self.assertEqual(["test_alpha.Alpha.test_skipped"], skipped)
        for out in (serial_out, parallel_out):
            self.assertIn("FAIL: test_alpha.Beta.test_fails", out)
            self.assertIn("AssertionError: 1 != 2", out)
            self.assertIn("RuntimeError: boom", out)
            self.assertIn("module_that_does_not_exist", out)
            self.assertIn("Ran 7 tests in", out)
            self.assertIn("FAILED (failures=1, errors=2, skipped=1)", out)

    def test_timings_are_written_and_order_the_next_run_longest_first(self) -> None:
        timings = self.scratch.root / "timings.json"
        self._run(2, timings=timings)
        recorded = json.loads(timings.read_text(encoding="utf-8"))
        self.assertEqual(RUNNER.TIMINGS_SCHEMA, recorded["schema"])
        self.assertEqual({"test_alpha.Alpha", "test_alpha.Beta", "test_gamma.Gamma"}, set(recorded["classes"]))
        order = RUNNER.order_classes({"a.X": 1, "a.Y": 5, "a.Z": 2}, {"a.X": 9.0, "a.Z": 1.0})
        self.assertEqual(["a.X", "a.Z", "a.Y"], order)  # timed classes first, then by test count
        self.assertEqual({}, RUNNER.load_timings(self.scratch.root / "absent.json"))

    def test_scale_marker_reaches_the_workers(self) -> None:
        marker = self.scratch.root / "suite" / "marker.txt"
        self._run(2, scale="full")
        self.assertEqual("full", marker.read_text(encoding="utf-8"))
        self._run(1, scale="reduced")
        self.assertEqual("reduced", marker.read_text(encoding="utf-8"))

    def test_a_worker_crash_is_reported_as_errors_not_dropped(self) -> None:
        def explode(task):
            raise RuntimeError("worker died")

        with mock.patch.object(RUNNER, "run_class", side_effect=explode):
            stream = io.StringIO()
            code, results = RUNNER.run(self.scratch.plan(), workers=1, timings_path=None, stream=stream)
        self.assertEqual(1, code)
        self.assertTrue(all(r.errors for r in results if r.tests_run == 0), results)

    def test_cli_defaults_and_scale_choices(self) -> None:
        parser = RUNNER.build_parser()
        args = parser.parse_args([])
        self.assertEqual("tests", args.start_dir)
        self.assertEqual("reduced", args.scale)
        self.assertGreaterEqual(args.workers, 1)
        self.assertEqual(2, RUNNER.main(["--workers", "0"]))


class ScaleMarkerTests(unittest.TestCase):
    """REQ-TST-002: the 1,000 size runs only with SE_HARNESS_TEST_SCALE=full."""

    def test_the_scale_test_reads_the_marker(self) -> None:
        source = (REPOSITORY_ROOT / "tests" / "test_workflow_execution.py").read_text(encoding="utf-8")
        self.assertIn('SE_HARNESS_TEST_SCALE', source)
        self.assertIn("scale_sizes()", source)
        self.assertIn("def scale_sizes()", source)
        self.assertNotIn("for target_count in (100, 500, 1000):", source)

    def test_sizes_by_marker(self) -> None:
        from tests.test_workflow_execution import scale_sizes

        with mock.patch.dict(os.environ, {"SE_HARNESS_TEST_SCALE": "full"}):
            self.assertEqual((100, 500, 1000), scale_sizes())
        with mock.patch.dict(os.environ, {"SE_HARNESS_TEST_SCALE": "reduced"}):
            self.assertEqual((100, 500), scale_sizes())
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("SE_HARNESS_TEST_SCALE", None)
            self.assertEqual((100, 500), scale_sizes())


if __name__ == "__main__":
    unittest.main()
