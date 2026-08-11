from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from se_harness.cli import build_parser, main
from se_harness.installer import BEGIN_MARKER, END_MARKER, HarnessError, _templates, plan_install, safe_destination, sha256, template_root


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class HarnessCtlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = main(list(arguments))
        return result, stdout.getvalue(), stderr.getvalue()

    def test_cli_and_template_expose_one_standard_installation(self) -> None:
        parser = build_parser()
        help_text = parser.format_help()
        self.assertNotIn("--profile", help_text)
        repository_templates = template_root().parent
        self.assertEqual(["standard"], sorted(item.name for item in repository_templates.iterdir() if item.is_dir()))

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parser.parse_args(["init", str(self.root / "target"), "--profile", "minimal"])

    def test_init_installs_complete_valid_harness_and_dashboard(self) -> None:
        target = self.root / "new-repository"
        code, output, error = self.invoke("init", str(target), "--project-name", "Example")
        self.assertEqual(0, code, error)
        self.assertIn("installed se-harness", output)
        required = [
            ".engineering-harness.toml",
            ".engineering-harness.lock",
            "AGENTS.md",
            "ENGINEERING_HARNESS.md",
            ".github/workflows/engineering-harness.yml",
            "docs/engineering/templates/REQUIREMENT.template.md",
            "docs/engineering/templates/VERIFICATION_RECORD.template.md",
            "docs/engineering/templates/RELEASE_RECORD.template.md",
            "scripts/validate_engineering_artifacts.py",
            "scripts/generate_harness_dashboard.py",
            "scripts/harness_explorer/index.template.html",
        ]
        for relative in required:
            self.assertTrue((target / relative).is_file(), relative)
        self.assertIn('project_name = "Example"', (target / ".engineering-harness.toml").read_text(encoding="utf-8"))
        self.assertIn("schema_version = 2", (target / ".engineering-harness.toml").read_text(encoding="utf-8"))

        validation = subprocess.run(
            [sys.executable, str(target / "scripts/validate_engineering_artifacts.py"), "--root", str(target)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, validation.returncode, validation.stderr)
        dashboard = subprocess.run(
            [sys.executable, str(target / "scripts/generate_harness_dashboard.py"), "--root", str(target)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, dashboard.returncode, dashboard.stderr)
        self.assertTrue((target / "target/harness-dashboard/index.html").is_file())

    def test_adopt_preserves_existing_content_and_labels_observations(self) -> None:
        target = self.root / "existing"
        target.mkdir()
        (target / "Cargo.toml").write_text("[package]\nname='existing'\n", encoding="utf-8")
        (target / "AGENTS.md").write_text("# Existing agent rules\n", encoding="utf-8")
        (target / ".gitignore").write_text("/build/\n", encoding="utf-8")

        code, _, error = self.invoke("adopt", str(target))
        self.assertEqual(0, code, error)
        agents = (target / "AGENTS.md").read_text(encoding="utf-8")
        ignored = (target / ".gitignore").read_text(encoding="utf-8")
        self.assertTrue(agents.startswith("# Existing agent rules"))
        self.assertIn(BEGIN_MARKER, agents)
        self.assertIn(END_MARKER, agents)
        self.assertTrue(ignored.startswith("/build/"))
        report = (target / "docs/engineering/ADOPTION_REPORT.md").read_text(encoding="utf-8")
        self.assertIn("Detected ecosystems: Rust", report)
        self.assertIn("does not approve or infer product intent", report)
        self.assertIn("Human decisions required", report)
        self.assertEqual(0, self.invoke("validate", str(target))[0])
        self.assertEqual(0, self.invoke("dashboard", str(target))[0])
        self.assertTrue((target / "target/harness-dashboard/index.html").is_file())

    def test_adopt_conflict_causes_no_partial_writes(self) -> None:
        target = self.root / "conflict"
        target.mkdir()
        original = b"repository-owned contract\n"
        (target / "ENGINEERING_HARNESS.md").write_bytes(original)
        (target / "AGENTS.md").write_text("existing\n", encoding="utf-8")

        code, output, error = self.invoke("adopt", str(target))
        self.assertEqual(1, code)
        self.assertIn("conflict", output)
        self.assertIn("no files were written", error)
        self.assertEqual(original, (target / "ENGINEERING_HARNESS.md").read_bytes())
        self.assertEqual("existing\n", (target / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertFalse((target / ".engineering-harness.lock").exists())
        self.assertFalse((target / "docs").exists())

    def test_upgrade_plan_is_read_only_and_apply_preserves_customized_file(self) -> None:
        target = self.root / "upgrade"
        self.assertEqual(0, self.invoke("init", str(target), "--project-name", "Stable Name")[0])
        managed = target / "ENGINEERING_HARNESS.md"
        managed.write_text(managed.read_text(encoding="utf-8") + "\nLocal policy.\n", encoding="utf-8")
        original = managed.read_bytes()
        missing = target / "docs/engineering/TRACEABILITY.md"
        missing.unlink()

        code, output, error = self.invoke("upgrade", str(target))
        self.assertEqual(0, code, error)
        self.assertIn("customized ENGINEERING_HARNESS.md", output)
        self.assertIn("add        docs/engineering/TRACEABILITY.md", output)
        self.assertFalse(missing.exists())

        code, _, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(1, code)
        self.assertIn("manual review", error)
        self.assertEqual(original, managed.read_bytes())
        self.assertTrue(missing.is_file())
        self.assertIn('project_name = "Stable Name"', (target / ".engineering-harness.toml").read_text(encoding="utf-8"))

    def test_invalid_project_name_and_malformed_markers_fail_closed(self) -> None:
        invalid = self.root / "invalid-name"
        code, _, error = self.invoke("init", str(invalid), "--project-name", 'bad"\nname')
        self.assertEqual(2, code)
        self.assertIn("project name", error)
        self.assertFalse(invalid.exists())

        target = self.root / "bad-markers"
        target.mkdir()
        (target / "AGENTS.md").write_text(f"rules\n{BEGIN_MARKER}\nbroken\n", encoding="utf-8")
        code, _, error = self.invoke("adopt", str(target))
        self.assertEqual(2, code)
        self.assertIn("markers", error)
        self.assertEqual(f"rules\n{BEGIN_MARKER}\nbroken\n", (target / "AGENTS.md").read_text(encoding="utf-8"))

    def test_upgrade_migrates_unmodified_schema_one_installation(self) -> None:
        target = self.root / "schema-one"
        self.assertEqual(0, self.invoke("init", str(target), "--project-name", "Legacy")[0])
        config_path = target / ".engineering-harness.toml"
        current = config_path.read_text(encoding="utf-8")
        legacy = current.replace("schema_version = 2", "schema_version = 1").replace('tool_version = "0.2.0"', 'tool_version = "0.1.0"')
        legacy = legacy.split("\n[revision_provenance]", 1)[0].rstrip() + "\n"
        config_path.write_bytes(legacy.encode("utf-8"))
        new_templates = [
            target / "docs/engineering/templates/VERIFICATION_RECORD.template.md",
            target / "docs/engineering/templates/RELEASE_RECORD.template.md",
        ]
        for path in new_templates:
            path.unlink()
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["tool_version"] = "0.1.0"
        lock["files"][".engineering-harness.toml"]["sha256"] = sha256(config_path.read_bytes())
        for path in new_templates:
            lock["files"].pop(path.relative_to(target).as_posix())
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        code, output, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertIn("update     .engineering-harness.toml", output)
        self.assertTrue(all(path.is_file() for path in new_templates))
        migrated = config_path.read_text(encoding="utf-8")
        self.assertIn("schema_version = 2", migrated)
        self.assertIn("[revision_provenance]", migrated)

    def test_doctor_detects_managed_drift(self) -> None:
        target = self.root / "doctor"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        self.assertEqual(0, self.invoke("doctor", str(target))[0])
        path = target / "docs/engineering/WORKFLOW.md"
        path.write_text("changed\n", encoding="utf-8")
        code, output, _ = self.invoke("doctor", str(target))
        self.assertEqual(1, code)
        self.assertIn("FAIL managed:docs/engineering/WORKFLOW.md", output)

    def test_validate_and_dashboard_commands_preserve_success(self) -> None:
        target = self.root / "operate"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        self.assertEqual(0, self.invoke("validate", str(target))[0])
        self.assertEqual(0, self.invoke("dashboard", str(target))[0])
        self.assertTrue((target / "target/harness-dashboard/dashboard-data.json").is_file())

    def test_lock_contains_hashes_without_generated_adoption_report(self) -> None:
        target = self.root / "lock"
        target.mkdir()
        self.assertEqual(0, self.invoke("adopt", str(target))[0])
        lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual(1, lock["schema"])
        self.assertIn("scripts/validate_engineering_artifacts.py", lock["files"])
        self.assertNotIn("docs/engineering/ADOPTION_REPORT.md", lock["files"])

    def test_symlinked_destination_directory_is_rejected_when_supported(self) -> None:
        target = self.root / "symlink"
        outside = self.root / "outside"
        target.mkdir()
        outside.mkdir()
        try:
            os.symlink(outside, target / "scripts", target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("directory symlinks are unavailable")
        with self.assertRaisesRegex(Exception, "symlinked directory"):
            plan_install(target, project_name=None, mode="adopt")
        self.assertEqual([], list(outside.iterdir()))

    def test_path_traversal_and_unsafe_lock_entry_fail_closed(self) -> None:
        target = self.root / "contained"
        target.mkdir()
        with self.assertRaises(HarnessError):
            safe_destination(target, Path("../outside.txt"))

        self.assertEqual(0, self.invoke("adopt", str(target))[0])
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"]["../outside.txt"] = {"mode": "managed", "sha256": "0" * 64}
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        code, _, error = self.invoke("doctor", str(target))
        self.assertEqual(2, code)
        self.assertIn("escapes the target", error)

    def test_distribution_metadata_covers_every_template_directory(self) -> None:
        pyproject = (REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('harnessctl = "se_harness.cli:main"', pyproject)
        root = template_root()
        expected = {
            str(path.parent.relative_to(REPOSITORY_ROOT)).replace("\\", "/")
            for path in root.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts and path.suffix.lower() not in {".pyc", ".pyo"}
        }
        for directory in expected:
            data_path = directory.replace("templates/repository/standard", "share/se-harness/templates/repository/standard")
            self.assertIn(data_path, pyproject, directory)

    def test_installer_ignores_bytecode_created_beside_packaged_scripts(self) -> None:
        isolated = self.root / "template"
        (isolated / "scripts/__pycache__").mkdir(parents=True)
        (isolated / "README.md").write_text("ok\n", encoding="utf-8")
        (isolated / "scripts/__pycache__/tool.pyc").write_bytes(b"\x00\xff\x00")
        with mock.patch("se_harness.installer.template_root", return_value=isolated):
            selected = _templates()
        self.assertEqual([Path("README.md")], [item.target for item in selected])


if __name__ == "__main__":
    unittest.main()
