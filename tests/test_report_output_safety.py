"""Report destinations must not overwrite the installation they inspect."""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from se_harness import cli
from se_harness.engine import dashboard_bundle, generate_harness_dashboard
from se_harness.engine.generate_harness_dashboard import generate_bundle
from se_harness.engine.dashboard_snapshot import GenerationError, resolve_output_root
from se_harness.installer import HarnessError
from se_harness.release_qualification import failed_qualification, write_qualification_result


class ReportOutputSafetyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="report-output-safety-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / "repository"
        self.root.mkdir()
        (self.root / "docs/engineering").mkdir(parents=True)
        self.skill = self.root / ".agents/skills/harness-orient/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        (self.skill.parent / "owner-note.txt").write_bytes(b"Owner content keeps the retired parent.\n")
        workflow = self.root / ".github/workflows/engineering-harness.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_bytes(b"name: protected workflow\n")
        (self.root / ".github/PULL_REQUEST_TEMPLATE.md").write_bytes(b"Owner pull-request template\n")

    def snapshot(self):
        return {p.relative_to(self.base).as_posix(): p.read_bytes() if p.is_file() else None
                for p in self.base.rglob("*") if not p.is_symlink()}

    def invoke(self, arguments):
        output, error = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = cli.main(arguments)
        return code, output.getvalue(), error.getvalue()

    def roles(self):
        return (
            ("released-root", [str(self.root)], "qualify_released_root"),
            ("complete-candidate", [str(self.root), "--candidate-commit", "a" * 40], "qualify_complete_candidate"),
            ("candidate-package", ["--checkout-root", str(self.root), "--candidate-wheel", "fixture.whl",
                                   "--candidate-commit", "a" * 40, "--candidate-wheel-sha256", "b" * 64,
                                   "--verifier-wheel-sha256", "c" * 64], "qualify_candidate_package"),
            ("public-install", [str(self.root), "--release-record", "RLS-TEST-001", "--public-wheel", "fixture.whl",
                                "--public-wheel-sha256", "b" * 64, "--payload-sha256", "c" * 64], "qualify_public_install"),
        )

    def test_qualification_exception_cannot_recreate_retired_skill_in_each_role(self):
        for role, arguments, function in self.roles():
            with self.subTest(role=role), mock.patch.object(cli, function, side_effect=HarnessError("fixture inspection failed")):
                before = self.snapshot()
                code, output, error = self.invoke(["qualify", role, *arguments, "--output", str(self.skill), "--json"])
                after = self.snapshot()
                # Clean only the disposable output after observation so every role runs independently on the baseline.
                if self.skill.exists():
                    self.skill.unlink()
                self.assertEqual(before, after)
                self.assertEqual(1, code, error)
                self.assertEqual("RQ002", json.loads(output)["checks"][0]["id"])

    def test_qualification_failure_can_still_be_reported_outside_target_in_each_role(self):
        for role, arguments, function in self.roles():
            with self.subTest(role=role), mock.patch.object(cli, function, side_effect=HarnessError("fixture inspection failed")):
                destination = self.base / (role + ".json")
                code, output, error = self.invoke(["qualify", role, *arguments, "--output", str(destination), "--json"])
                self.assertEqual(1, code, error)
                self.assertEqual(json.loads(output), json.loads(destination.read_bytes()))
                self.assertEqual("RQ001", json.loads(output)["checks"][0]["id"])
                self.assertFalse(self.skill.exists())

    def test_returned_qualification_failure_keeps_output_protection(self):
        for role, arguments, function in self.roles():
            result = failed_qualification(role, code="RQ001", subject="fixture", message="fixture failed")
            with self.subTest(role=role), mock.patch.object(cli, function, return_value=result):
                before = self.snapshot()
                code, output, error = self.invoke(["qualify", role, *arguments, "--output", str(self.skill), "--json"])
                self.assertEqual(before, self.snapshot())
                self.assertEqual(1, code, error)
                self.assertEqual("RQ002", json.loads(output)["checks"][0]["id"])

    def test_dashboard_cli_cannot_replace_installed_workflow_directory(self):
        before = self.snapshot()
        code, output, error = self.invoke(["dashboard", str(self.root), "--output", ".github", "--json"])
        self.assertEqual(before, self.snapshot())
        self.assertEqual(2, code, output + error)
        self.assertIn("protected", error)

    def test_dashboard_direct_api_cannot_replace_installed_workflow_directory(self):
        before = self.snapshot()
        with self.assertRaises(GenerationError):
            generate_bundle(self.root, output=Path(".github"))
        self.assertEqual(before, self.snapshot())

    def test_dashboard_refuses_absent_retired_and_case_variant_destinations(self):
        for value in (".agents", ".agents/skills/harness-orient", ".agents/skills/harness-orient/SKILL.md",
                      ".claude/skills/harness-operator-brief", ".GITHUB", ".git", ".engineering-harness.lock",
                      ".engineering-harness.skill-ownership.pending.json", ".engineering-harness.skill-ownership.mutex"):
            with self.subTest(output=value):
                before = self.snapshot()
                with self.assertRaises(GenerationError):
                    resolve_output_root(self.root, self.root / "docs/engineering", Path(value))
                self.assertEqual(before, self.snapshot())

    def test_dashboard_preserves_normal_custom_and_external_destinations(self):
        workflow = self.root / ".github/workflows/engineering-harness.yml"
        for destination in (None, Path("target/custom-report"), self.base / "external-report"):
            with self.subTest(output=destination):
                output = resolve_output_root(self.root, self.root / "docs/engineering", destination)
                generate_bundle(self.root, output=destination)
                self.assertTrue((output / "dashboard-manifest.json").is_file())
                self.assertEqual(b"name: protected workflow\n", workflow.read_bytes())
        # Component boundaries matter: a sibling containing the repository name is still external.
        sibling = self.base / "repository-reports"
        self.assertEqual(sibling.resolve(), resolve_output_root(self.root, self.root / "docs/engineering", sibling))

    def link(self, path, target):
        if os.name == "nt":
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(path), str(target)], capture_output=True)
            if result.returncode:
                self.skipTest("junction creation unavailable: " + result.stderr.decode(errors="replace"))
            self.addCleanup(path.rmdir)
        else:
            try:
                path.symlink_to(target, target_is_directory=True)
            except OSError as exc:
                self.skipTest("directory symlink unavailable: " + str(exc))
            self.addCleanup(path.unlink)

    def test_report_aliases_cannot_redirect_into_protected_paths(self):
        alias = self.base / "alias"
        self.link(alias, self.root)
        for destination in (alias / ".github", alias / ".agents/skills/harness-orient"):
            with self.subTest(output=str(destination)), self.assertRaises(GenerationError):
                resolve_output_root(self.root, self.root / "docs/engineering", destination)
        with mock.patch.object(cli, "qualify_released_root", side_effect=HarnessError("fixture failed")):
            code, output, error = self.invoke(["qualify", "released-root", str(self.root), "--output",
                str(alias / ".agents/skills/harness-orient/SKILL.md"), "--json"])
        self.assertEqual(1, code, error)
        self.assertFalse(self.skill.exists())
        self.assertEqual("RQ002", json.loads(output)["checks"][0]["id"])

    def test_dashboard_rechecks_output_after_projection_and_before_promotion(self):
        protected = {p.name: p.read_bytes() for p in (self.root / ".github").rglob("*") if p.is_file()}
        for stage in ("projection", "staging"):
            destination = self.root / ("report-" + stage)
            module = generate_harness_dashboard if stage == "projection" else dashboard_bundle
            function = "build_snapshot" if stage == "projection" else "verify_serialized_bundle"
            original = getattr(module, function)

            def replace_output(*args, **kwargs):
                result = original(*args, **kwargs)
                self.link(destination, self.root / ".github")
                return result

            with self.subTest(stage=stage), mock.patch.object(module, function, side_effect=replace_output):
                with self.assertRaises(GenerationError):
                    generate_bundle(self.root, output=destination)
            self.assertEqual(protected, {p.name: p.read_bytes() for p in (self.root / ".github").rglob("*") if p.is_file()})
            self.assertFalse(list(self.root.glob("." + destination.name + ".next-*")))
            self.assertFalse(list(self.root.glob("." + destination.name + ".previous-*")))

    @unittest.skipUnless(os.name == "nt", "Windows namespace aliases only")
    def test_windows_alias_spellings_cannot_bypass_report_output_protection(self):
        extended_root = Path("\\\\?\\" + str(self.root))
        extended_output = Path("\\\\?\\" + str(self.skill))
        failure = failed_qualification("released-root", code="RQ001", subject="fixture", message="fixture failed")
        before = self.snapshot()
        for destination, forbidden in ((extended_output, self.root), (self.skill, extended_root)):
            with self.subTest(output=str(destination), root=str(forbidden)), self.assertRaises(HarnessError):
                write_qualification_result(destination, failure, forbidden_roots=(forbidden,))
        for destination in (Path("\\\\?\\" + str(self.root / ".github")),
                            Path(".github."), Path(".github "), Path(".github::$INDEX_ALLOCATION")):
            with self.subTest(output=str(destination)), self.assertRaises(GenerationError):
                resolve_output_root(self.root, self.root / "docs/engineering", destination)
        with self.assertRaises(GenerationError):
            resolve_output_root(extended_root, extended_root / "docs/engineering", Path(".github"))
        for destination in (self.skill.with_name("SKILL.md."), self.skill.with_name("SKILL.md:report")):
            with self.subTest(output=str(destination)), self.assertRaises(HarnessError):
                write_qualification_result(destination, failure, forbidden_roots=(self.root,))
        self.assertEqual(before, self.snapshot())
