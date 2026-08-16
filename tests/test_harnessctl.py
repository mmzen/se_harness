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

from se_harness import __version__
from se_harness.cli import build_parser, main
from se_harness.installer import BEGIN_MARKER, END_MARKER, HarnessError, _templates, plan_install, safe_destination, sha256, template_root, tracked_content
from se_harness.integrity import HASH_ALGORITHM, HASH_MODE, IntegrityError, canonical_sha256, canonical_text_bytes, digest_for_schema, parse_lock


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

    def make_schema_one_lock(self, target: Path) -> dict:
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        for relative, entry in lock["files"].items():
            if entry.get("mode") not in {"managed", "fragment"}:
                continue
            content = (target / relative).read_bytes()
            tracked = tracked_content(entry["mode"], content)
            self.assertIsNotNone(tracked)
            entry["sha256"] = digest_for_schema(tracked, 1, entry["mode"])
        lock["schema"] = 1
        lock.pop("hash_algorithm", None)
        lock.pop("hash_mode", None)
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return lock

    def test_cli_and_template_expose_one_standard_installation(self) -> None:
        parser = build_parser()
        help_text = parser.format_help()
        self.assertNotIn("--profile", help_text)
        repository_templates = template_root().parent
        self.assertEqual(["standard"], sorted(item.name for item in repository_templates.iterdir() if item.is_dir()))

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parser.parse_args(["init", str(self.root / "target"), "--profile", "minimal"])

    def test_canonical_text_integrity_vectors(self) -> None:
        lf = b"alpha\nbeta\n"
        self.assertEqual(canonical_text_bytes(lf), canonical_text_bytes(b"alpha\r\nbeta\r\n"))
        self.assertEqual(canonical_text_bytes(lf), canonical_text_bytes(b"alpha\rbeta\r"))
        self.assertEqual(canonical_sha256(lf), canonical_sha256(b"alpha\r\nbeta\r\n"))
        self.assertNotEqual(canonical_sha256(lf), canonical_sha256(b"alpha\nbeta"))
        self.assertNotEqual(canonical_sha256(lf), canonical_sha256(b"alpha\nBeta\n"))
        with self.assertRaises(IntegrityError):
            canonical_text_bytes(b"\xff")

    def test_lock_schema_validation_rejects_ambiguous_or_unsupported_input(self) -> None:
        with self.assertRaisesRegex(IntegrityError, "duplicate JSON key"):
            parse_lock('{"schema": 1, "schema": 1, "files": {}}')
        with self.assertRaisesRegex(IntegrityError, "unsupported lock schema"):
            parse_lock('{"schema": true, "files": {}}')
        with self.assertRaisesRegex(IntegrityError, "unsupported lock hash mode"):
            parse_lock('{"schema": 2, "hash_algorithm": "sha256", "hash_mode": "unknown", "files": {}}')

    def test_init_installs_complete_valid_harness_and_dashboard(self) -> None:
        target = self.root / "new-repository"
        code, output, error = self.invoke("init", str(target), "--project-name", "Example")
        self.assertEqual(0, code, error)
        self.assertIn("installed se-harness", output)
        required = [
            ".engineering-harness.toml",
            ".engineering-harness.lock",
            "AGENTS.md",
            "CLAUDE.md",
            "ENGINEERING_HARNESS.md",
            ".github/workflows/engineering-harness.yml",
            "docs/engineering/REPOSITORY_CONTEXT.md",
            "docs/engineering/templates/REQUIREMENT.template.md",
            "docs/engineering/templates/VERIFICATION_RECORD.template.md",
            "docs/engineering/templates/RELEASE_RECORD.template.md",
            "scripts/validate_engineering_artifacts.py",
            "scripts/inspect_engineering_artifacts.py",
            "scripts/generate_harness_dashboard.py",
            "scripts/harness_explorer/index.template.html",
        ]
        for relative in required:
            self.assertTrue((target / relative).is_file(), relative)
        self.assertIn('project_name = "Example"', (target / ".engineering-harness.toml").read_text(encoding="utf-8"))
        self.assertIn("schema_version = 2", (target / ".engineering-harness.toml").read_text(encoding="utf-8"))
        self.assertIn("@AGENTS.md", (target / "CLAUDE.md").read_text(encoding="utf-8"))
        context = (target / "docs/engineering/REPOSITORY_CONTEXT.md").read_text(encoding="utf-8")
        self.assertIn("Repository Context for Example", context)
        self.assertIn("repository-owned", context.lower())

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
        (target / "CLAUDE.md").write_text("# Existing Claude rules\n", encoding="utf-8")
        (target / ".gitignore").write_text("/build/\n", encoding="utf-8")
        context_path = target / "docs/engineering/REPOSITORY_CONTEXT.md"
        context_path.parent.mkdir(parents=True)
        context_path.write_text("# Owner-curated context\n", encoding="utf-8")

        code, _, error = self.invoke("adopt", str(target))
        self.assertEqual(0, code, error)
        agents = (target / "AGENTS.md").read_text(encoding="utf-8")
        claude = (target / "CLAUDE.md").read_text(encoding="utf-8")
        ignored = (target / ".gitignore").read_text(encoding="utf-8")
        self.assertTrue(agents.startswith("# Existing agent rules"))
        self.assertIn(BEGIN_MARKER, agents)
        self.assertIn(END_MARKER, agents)
        self.assertTrue(claude.startswith("# Existing Claude rules"))
        self.assertIn("@AGENTS.md", claude)
        self.assertIn(BEGIN_MARKER, claude)
        self.assertTrue(ignored.startswith("/build/"))
        self.assertEqual("# Owner-curated context\n", context_path.read_text(encoding="utf-8"))
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
        self.assertIn("manual review; no files were written", error)
        self.assertEqual(original, managed.read_bytes())
        self.assertFalse(missing.exists())
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

        claude_target = self.root / "bad-claude-markers"
        claude_target.mkdir()
        (claude_target / "CLAUDE.md").write_text(f"rules\n{END_MARKER}\n", encoding="utf-8")
        code, _, error = self.invoke("adopt", str(claude_target))
        self.assertEqual(2, code)
        self.assertIn("markers", error)
        self.assertFalse((claude_target / ".engineering-harness.lock").exists())

    def test_upgrade_adds_cross_agent_and_context_files_to_older_installation(self) -> None:
        target = self.root / "older-installation"
        self.assertEqual(0, self.invoke("init", str(target), "--project-name", "Legacy Project")[0])
        claude_path = target / "CLAUDE.md"
        context_path = target / "docs/engineering/REPOSITORY_CONTEXT.md"
        claude_path.unlink()
        context_path.unlink()
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"].pop("CLAUDE.md")
        lock["files"].pop("docs/engineering/REPOSITORY_CONTEXT.md")
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        code, output, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertIn("add        CLAUDE.md", output)
        self.assertIn("add        docs/engineering/REPOSITORY_CONTEXT.md", output)
        self.assertIn("@AGENTS.md", claude_path.read_text(encoding="utf-8"))
        self.assertIn("Repository Context for Legacy Project", context_path.read_text(encoding="utf-8"))

    def test_upgrade_preserves_claude_customization_and_repository_context(self) -> None:
        target = self.root / "repository-owned-context"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        claude_path = target / "CLAUDE.md"
        context_path = target / "docs/engineering/REPOSITORY_CONTEXT.md"
        claude_path.write_text(claude_path.read_text(encoding="utf-8") + "\n## Claude-specific\nKeep this.\n", encoding="utf-8")
        context_path.write_text("# Curated\nUse `python -m unittest`.\n", encoding="utf-8")

        code, _, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertIn("Keep this.", claude_path.read_text(encoding="utf-8"))
        self.assertEqual("# Curated\nUse `python -m unittest`.\n", context_path.read_text(encoding="utf-8"))

        context_path.unlink()
        code, _, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertFalse(context_path.exists())
        lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual({"mode": "seed", "state": "removed"}, lock["files"]["docs/engineering/REPOSITORY_CONTEXT.md"])

    def test_upgrade_migrates_unmodified_schema_one_installation(self) -> None:
        target = self.root / "schema-one"
        self.assertEqual(0, self.invoke("init", str(target), "--project-name", "Legacy")[0])
        lock = self.make_schema_one_lock(target)
        config_path = target / ".engineering-harness.toml"
        current = config_path.read_text(encoding="utf-8")
        legacy = current.replace("schema_version = 2", "schema_version = 1").replace(f'tool_version = "{__version__}"', 'tool_version = "0.1.0"')
        legacy = legacy.split("\n[revision_provenance]", 1)[0].rstrip() + "\n"
        config_path.write_bytes(legacy.encode("utf-8"))
        new_templates = [
            target / "docs/engineering/templates/VERIFICATION_RECORD.template.md",
            target / "docs/engineering/templates/RELEASE_RECORD.template.md",
        ]
        for path in new_templates:
            path.unlink()
        lock_path = target / ".engineering-harness.lock"
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
        migrated_lock = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertEqual(2, migrated_lock["schema"])
        self.assertEqual(HASH_MODE, migrated_lock["hash_mode"])

    def test_schema_two_doctor_and_upgrade_ignore_newline_representation(self) -> None:
        target = self.root / "portable-newlines"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        for relative in ("docs/engineering/WORKFLOW.md", "AGENTS.md"):
            path = target / relative
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))

        code, output, error = self.invoke("doctor", str(target))
        self.assertEqual(0, code, error)
        self.assertIn("PASS managed:docs/engineering/WORKFLOW.md", output)
        self.assertIn("PASS managed:AGENTS.md", output)

        code, output, error = self.invoke("upgrade", str(target))
        self.assertEqual(0, code, error)
        self.assertNotIn("docs/engineering/WORKFLOW.md", output)
        self.assertNotIn("AGENTS.md", output)

    def test_schema_one_canonical_advisory_migrates_safely(self) -> None:
        target = self.root / "legacy-newlines"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        self.make_schema_one_lock(target)
        workflow = target / "docs/engineering/WORKFLOW.md"
        workflow.write_bytes(workflow.read_bytes().replace(b"\n", b"\r\n"))

        code, output, error = self.invoke("doctor", str(target))
        self.assertEqual(0, code, error)
        self.assertIn("legacy canonical match; upgrade recommended", output)

        code, _, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual(2, lock["schema"])
        self.assertEqual(HASH_ALGORITHM, lock["hash_algorithm"])
        self.assertEqual(HASH_MODE, lock["hash_mode"])

    def test_ambiguous_schema_one_customization_is_preserved(self) -> None:
        target = self.root / "legacy-customized"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        self.make_schema_one_lock(target)
        workflow = target / "docs/engineering/WORKFLOW.md"
        workflow.write_bytes(workflow.read_bytes() + b"\nOwner customization.\n")
        original = workflow.read_bytes()

        code, _, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(1, code)
        self.assertIn("manual review", error)
        self.assertEqual(original, workflow.read_bytes())
        lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual(1, lock["schema"])

    def test_untracked_customization_does_not_block_safe_lock_migration(self) -> None:
        target = self.root / "legacy-untracked-customized"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        lock = self.make_schema_one_lock(target)
        lock["files"].pop("ENGINEERING_HARNESS.md")
        lock_path = target / ".engineering-harness.lock"
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        contract = target / "ENGINEERING_HARNESS.md"
        contract.write_bytes(contract.read_bytes() + b"\nOwner customization.\n")
        original = contract.read_bytes()

        code, _, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(1, code)
        self.assertIn("manual review", error)
        self.assertEqual(original, contract.read_bytes())
        migrated = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertEqual(1, migrated["schema"])
        self.assertNotIn("ENGINEERING_HARNESS.md", migrated["files"])

    def test_doctor_hashes_only_the_managed_fragment(self) -> None:
        target = self.root / "fragment-doctor"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        agents = target / "AGENTS.md"
        agents.write_text("# Owner rules\n\n" + agents.read_text(encoding="utf-8") + "\nOwner tail.\n", encoding="utf-8")
        self.assertEqual(0, self.invoke("doctor", str(target))[0])

        agents.write_text(agents.read_text(encoding="utf-8").replace("Read `ENGINEERING_HARNESS.md`", "Skip `ENGINEERING_HARNESS.md`"), encoding="utf-8")
        code, output, _ = self.invoke("doctor", str(target))
        self.assertEqual(1, code)
        self.assertIn("FAIL managed:AGENTS.md", output)

    def test_doctor_detects_managed_drift(self) -> None:
        target = self.root / "doctor"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        self.assertEqual(0, self.invoke("doctor", str(target))[0])
        path = target / "docs/engineering/WORKFLOW.md"
        path.write_text("changed\n", encoding="utf-8")
        code, output, _ = self.invoke("doctor", str(target))
        self.assertEqual(1, code)
        self.assertIn("FAIL managed:docs/engineering/WORKFLOW.md", output)

    def test_doctor_detects_stale_schema_two_digest(self) -> None:
        target = self.root / "stale-lock"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"]["docs/engineering/WORKFLOW.md"]["sha256"] = "0" * 64
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        code, output, _ = self.invoke("doctor", str(target))
        self.assertEqual(1, code)
        self.assertIn("FAIL managed:docs/engineering/WORKFLOW.md", output)

    def test_doctor_detects_missing_claude_import_and_repository_context(self) -> None:
        target = self.root / "doctor-instructions"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        claude_path = target / "CLAUDE.md"
        claude_path.write_text(claude_path.read_text(encoding="utf-8").replace("@AGENTS.md", "Claude rules only."), encoding="utf-8")
        (target / "docs/engineering/REPOSITORY_CONTEXT.md").unlink()

        code, output, _ = self.invoke("doctor", str(target))
        self.assertEqual(1, code)
        self.assertIn("FAIL docs/engineering/REPOSITORY_CONTEXT.md", output)
        self.assertIn("FAIL claude-import", output)

    def test_validate_inspect_and_dashboard_commands_preserve_success(self) -> None:
        target = self.root / "operate"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        self.assertEqual(0, self.invoke("validate", str(target))[0])
        before = sorted(path.relative_to(target).as_posix() for path in target.rglob("*"))
        inspection = subprocess.run(
            [sys.executable, "-m", "se_harness", "inspect", str(target)],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, inspection.returncode, inspection.stderr)
        self.assertIn("Harness inspection", inspection.stdout)
        self.assertIn("repository-local, derived observation", inspection.stdout)
        inspection_json = subprocess.run(
            [sys.executable, "-m", "se_harness", "inspect", str(target), "--json"],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, inspection_json.returncode, inspection_json.stderr)
        self.assertEqual("se-harness-inspection-v2", json.loads(inspection_json.stdout)["schema"])
        self.assertEqual(before, sorted(path.relative_to(target).as_posix() for path in target.rglob("*")))
        self.assertEqual(0, self.invoke("dashboard", str(target))[0])
        self.assertTrue((target / "target/harness-dashboard/dashboard-data.json").is_file())

    def test_lock_contains_hashes_without_generated_adoption_report(self) -> None:
        target = self.root / "lock"
        target.mkdir()
        self.assertEqual(0, self.invoke("adopt", str(target))[0])
        lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual(2, lock["schema"])
        self.assertEqual(HASH_ALGORITHM, lock["hash_algorithm"])
        self.assertEqual(HASH_MODE, lock["hash_mode"])
        self.assertIn("scripts/validate_engineering_artifacts.py", lock["files"])
        self.assertIn("scripts/inspect_engineering_artifacts.py", lock["files"])
        self.assertEqual("fragment", lock["files"]["CLAUDE.md"]["mode"])
        self.assertEqual({"mode": "seed", "state": "present"}, lock["files"]["docs/engineering/REPOSITORY_CONTEXT.md"])
        self.assertEqual({"mode": "seed", "state": "present"}, lock["files"]["docs/engineering/README.md"])
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
        code, output, _ = self.invoke("doctor", str(target))
        self.assertEqual(1, code)
        self.assertIn("escapes the target", output)

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
