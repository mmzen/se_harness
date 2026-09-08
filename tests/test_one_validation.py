"""WO-ECP-035 (SPEC-ECP-024 ECP-ENG-010 to ECP-ENG-015): one validation per governance command.

Each command validates the repository at most once, and a command that validates
does so exactly once; `doctor` reads its layout warnings without the graph passes;
the report travels into preflight, the snapshot builder, provenance and
qualification; preflight and the check share one skew classifier.
"""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from se_harness import cli, preflight, provenance, release_qualification, workflow_compliance
from se_harness.engine import generate_harness_dashboard, validate_engineering_artifacts
from tests.artifact_support import create_base_chain
from tests.fixture_support import standard_repository
from tests.git_support import git, init_repository
from tests.mutation_guard_support import trusted_mutation_authority

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def _fixture(temporary: Path, status: str) -> Path:
    root = temporary / f"repository-{status}"
    standard_repository(root)
    create_base_chain(root, work_order_status=status, operating_contract_status="draft")
    init_repository(root)
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    return root


class ValidationCountTests(unittest.TestCase):
    """ECP-ENG-010: `validate_repository` under a counting patch, per command."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="se-harness-one-validation-")
        temporary = Path(cls.temporary.name)
        cls.approved = _fixture(temporary, "approved")
        cls.implemented = _fixture(temporary, "implemented")
        cls.output = temporary / "dash"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def _run(self, *argv: str) -> tuple[int, int]:
        real = validate_engineering_artifacts.validate_repository
        calls = {"n": 0}

        def counting(*args, **kwargs):
            calls["n"] += 1
            return real(*args, **kwargs)

        with mock.patch.object(validate_engineering_artifacts, "validate_repository", side_effect=counting), \
             mock.patch.object(generate_harness_dashboard, "validate_repository", side_effect=counting), \
             mock.patch("se_harness.mutation_guard.require_mutation_authority", side_effect=trusted_mutation_authority), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                code = cli.main([*argv])
            except SystemExit as exc:
                code = int(exc.code or 0)
        return calls["n"], code

    def test_each_governance_command_validates_at_most_once(self) -> None:
        approved, implemented = str(self.approved), str(self.implemented)
        validating = {
            "validate": ["validate", approved],
            "inspect": ["inspect", approved],
            "dashboard": ["dashboard", approved, "--output", str(self.output)],
            "preflight": ["preflight", approved, "--work-order", "WO-001"],
            "check projection": ["check", approved],
            "check start": ["check", approved, "--artifact", "WO-001", "--checkpoint", "start"],
            "check scope": ["check", approved, "--artifact", "WO-001", "--checkpoint", "scope", "--changed-path", "README.md", "--changes-complete"],
            "check handoff --from-git": ["check", implemented, "--artifact", "WO-001", "--checkpoint", "handoff", "--from-git", "HEAD"],
            "evidence": ["evidence", approved, "--artifact", "WO-001", "--checkpoint", "start"],
            "pr-body": ["pr-body", approved, "--artifact", "WO-001"],
            "transition plan": ["transition", approved, "--set", "WO-001=in_progress", "--decision", "WO-001=engineering-owner"],
            "capture-verification": [
                "capture-verification", implemented, "--id", "VREC-002", "--work-order", "WO-001", "--verification", "VER-001",
                "--evidence", "docs/engineering/product/evidence/WO-001-verification.md", "--owner", "quality-owner",
            ],
        }
        for label, argv in validating.items():
            with self.subTest(command=label):
                count, _ = self._run(*argv)
                self.assertEqual(1, count)
        # ECP-ENG-012: doctor obtains W013 without the graph passes; a command that does not read
        # the graph validates nothing.
        for label, argv in {"doctor": ["doctor", approved], "create-artifact --dry-run": ["create-artifact", approved, "--domain", "product", "--type", "requirement", "--dry-run"]}.items():
            with self.subTest(command=label):
                count, _ = self._run(*argv)
                self.assertEqual(0, count)


class ReportTravelsTests(unittest.TestCase):
    def test_preflight_takes_the_report_and_does_not_validate_again(self) -> None:
        # ECP-ENG-011
        with tempfile.TemporaryDirectory() as temporary:
            root = _fixture(Path(temporary), "approved")
            report = validate_engineering_artifacts.validate_repository(root)
            with mock.patch.object(validate_engineering_artifacts, "validate_repository", side_effect=AssertionError("validated again")):
                result = preflight.run_preflight(root, work_order_id="WO-001", phase="start", report=report)
            self.assertEqual("WO-001", result.work_order["id"])
            self.assertIs(workflow_compliance.lifecycle_relevant, preflight.lifecycle_relevant)

    def test_the_snapshot_builder_and_qualification_take_the_report(self) -> None:
        # ECP-ENG-011, ECP-ENG-015
        with tempfile.TemporaryDirectory() as temporary:
            root = _fixture(Path(temporary), "implemented")
            report = validate_engineering_artifacts.validate_repository(root)
            with mock.patch.object(generate_harness_dashboard, "validate_repository", side_effect=AssertionError("validated again")):
                same, snapshot, summary = generate_harness_dashboard.generate_bundle(root, None, Path(temporary) / "out", report=report)
            self.assertIs(report, same)
            self.assertEqual(summary["artifact_count"], len(snapshot["artifacts"]))
            self.assertTrue((Path(temporary) / "out" / "dashboard-manifest.json").is_file())
            check = release_qualification._validation_check(root, "RR003", report)
            self.assertEqual("engineering-graph", check.subject)
            catalog = provenance._validation_catalog(root, report)
            self.assertIs(catalog["WO-001"], next(item for item in report.artifacts if item.artifact_id == "WO-001"))
            # ECP-ENG-011: provenance reads the validator's metadata, never a file
            with mock.patch("se_harness.front_matter.read", side_effect=AssertionError("re-parsed")):
                self.assertEqual("implemented", provenance._load_metadata(root, catalog["WO-001"])["status"])
                self.assertEqual([], provenance.standing_deviations_for_work(root, catalog, ["WO-001"]))

    def test_doctor_reads_the_layout_pass_alone_and_agrees_with_the_full_run(self) -> None:
        # ECP-ENG-012
        with tempfile.TemporaryDirectory() as temporary:
            root = _fixture(Path(temporary), "approved")
            misplaced = root / "docs" / "engineering" / "product" / "REQ-002.md"  # inside the domain, outside its type directory
            misplaced.write_text((root / "docs/engineering/product/requirements/REQ-001.md").read_text(encoding="utf-8").replace("REQ-001", "REQ-002"), encoding="utf-8")
            layout = [item for item in validate_engineering_artifacts.canonical_layout_diagnostics(root) if item.code == "W013"]
            self.assertEqual(["docs/engineering/product/REQ-002.md"], [item.path for item in layout])
            # The full run hides the warning for an artifact it rejects for another reason (the
            # copy lacks coverage); the layout pass reports it. On a clean graph the two agree.
            misplaced.unlink()
            full = [item for item in validate_engineering_artifacts.validate_repository(root).warnings if item.code == "W013"]
            self.assertEqual(full, [item for item in validate_engineering_artifacts.canonical_layout_diagnostics(root) if item.code == "W013"])

    def test_preflight_reports_skew_apart_and_the_check_reads_the_same_verdict(self) -> None:
        # ECP-ENG-014
        with tempfile.TemporaryDirectory() as temporary:
            root = _fixture(Path(temporary), "approved")
            (root / "ENGINEERING_HARNESS.md").write_text("customized\n", encoding="utf-8")
            report = preflight.run_preflight(root, work_order_id="WO-001", phase="start")
            skew_paths = {item.path for item in report.skew}
            self.assertIn("distribution:ENGINEERING_HARNESS.md", skew_paths)
            self.assertFalse(any(item.path.startswith("distribution:") for item in report.diagnostics))
            rendered = preflight.render_preflight(report)
            self.assertIn("Candidate-versus-released skew (not blocking):", rendered)
            self.assertEqual(report.ready, not report.diagnostics)
            self.assertEqual(list(report.diagnostics), workflow_compliance.lifecycle_relevant_diagnostics(root, report))
            payload = json.loads(preflight.render_preflight_json(report))
            self.assertEqual([item.path for item in report.skew], [item["path"] for item in payload["skew"]])
            faked = SimpleNamespace(ready=False, diagnostics=[SimpleNamespace(code="I001", path="distribution:AGENTS.md", message="differs")])
            self.assertEqual([], workflow_compliance.lifecycle_relevant_diagnostics(root, faked))


if __name__ == "__main__":
    unittest.main()
