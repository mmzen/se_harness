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
from se_harness.installer import BEGIN_MARKER, END_MARKER, HarnessError, _templates, plan_install, safe_destination, template_root, tracked_content
from se_harness.integrity import HASH_ALGORITHM, HASH_MODE, LOCK_SCHEMA, IntegrityError, canonical_sha256, canonical_text_bytes, parse_lock
from tests.mutation_guard_support import trusted_mutation_authority


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class HarnessCtlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.guard = mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=trusted_mutation_authority,
        )
        self.guard.start()
        self.addCleanup(self.guard.stop)
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

    def assert_portable_release_surfaces(self, target: Path) -> None:
        release_template = (target / "docs/engineering/templates/RELEASE_RECORD.template.md").read_text(
            encoding="utf-8"
        )
        validator_source = (target / "scripts/validate_engineering_artifacts.py").read_text(
            encoding="utf-8"
        )
        for forbidden in (
            "distribution-manifest",
            "python-wheel-sdist",
            "se_harness-VERSION",
            "SHA256SUMS",
        ):
            self.assertNotIn(forbidden, release_template)
            self.assertNotIn(forbidden, validator_source)

    def make_pre3_lock(self, target: Path, schema: int) -> dict:
        # WO-HUP-012: a pre-3 lock is refused at read, so its entry digests
        # never matter; only the schema field and the absent schema-3 extras do.
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["schema"] = schema
        if schema == 1:
            lock.pop("hash_algorithm", None)
            lock.pop("hash_mode", None)
        lock.pop("evaluator", None)
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return lock

    def test_no_pre3_lock_machinery_survives_in_the_package_or_scripts(self) -> None:
        # WO-HUP-012 (HUP-LSF-008): the deleted symbols, comparison labels and
        # variant recognition are gone from every product and script source.
        repository = Path(__file__).resolve().parents[1]
        sources = [
            path
            for base in ("se_harness", "scripts", "repository_tools")
            for path in sorted((repository / base).rglob("*.py"))
            if "__pycache__" not in path.parts
        ]
        self.assertGreater(len(sources), 10)
        for forbidden in (
            "LEGACY_CANONICAL_LOCK_SCHEMA",
            "legacy_tracked_sha256",
            "matches_legacy_newline_variant",
            "legacy-canonical",
            "legacy-newline-variant",
            "legacy exact",
        ):
            with self.subTest(forbidden=forbidden):
                hits = [
                    path.name for path in sources
                    if forbidden in path.read_text(encoding="utf-8")
                ]
                self.assertEqual([], hits)

    def test_cli_and_template_expose_one_standard_installation(self) -> None:
        parser = build_parser()
        help_text = parser.format_help()
        self.assertNotIn("--profile", help_text)
        command_action = next(
            action for action in parser._actions if isinstance(getattr(action, "choices", None), dict)
        )
        prepare_help = command_action.choices["prepare-release"].format_help()
        self.assertNotIn("--distribution-manifest", prepare_help)
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
        # WO-HUP-012 (HUP-LSF-001): a pre-3 schema is refused with the floor
        # diagnostic naming re-adoption, before any other field is read.
        for legacy_schema in (1, 2):
            with self.assertRaisesRegex(IntegrityError, r"predates the supported floor \(schema 3\).*re-adopt"):
                parse_lock(json.dumps({"schema": legacy_schema, "hash_algorithm": "sha256", "hash_mode": "unknown", "files": {}}))
        valid = {
            "schema": 3,
            "tool_version": "1.2.3",
            "hash_algorithm": "sha256",
            "hash_mode": "utf8-text-lf-v1",
            "evaluator": {
                "version": "1.2.3",
                "payload_manifest": "se-harness-installed-payload-v1",
                "payload_sha256": "a" * 64,
            },
            "files": {},
        }
        self.assertEqual(valid, parse_lock(json.dumps(valid)))
        invalid = json.loads(json.dumps(valid))
        invalid["evaluator"]["archive_name"] = "se_harness-1.2.3-py3-none-any.whl"
        with self.assertRaisesRegex(IntegrityError, "must appear together"):
            parse_lock(json.dumps(invalid))
        invalid = json.loads(json.dumps(valid))
        invalid["evaluator"]["unexpected"] = "value"
        with self.assertRaisesRegex(IntegrityError, "unknown evaluator lock field"):
            parse_lock(json.dumps(invalid))

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
        retired = target / "docs/engineering/REPOSITORY_CONTEXT.md"
        self.assertFalse(retired.exists(), "the retired repository-context scaffold must not be installed")
        installed_lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertNotIn("docs/engineering/REPOSITORY_CONTEXT.md", installed_lock["files"])
        self.assert_portable_release_surfaces(target)

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
        adopted_lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertNotIn("docs/engineering/REPOSITORY_CONTEXT.md", adopted_lock["files"])
        report = (target / "docs/engineering/ADOPTION_REPORT.md").read_text(encoding="utf-8")
        self.assertIn("Detected ecosystems: Rust", report)
        self.assertIn("does not approve or infer product intent", report)
        self.assertIn("Human decisions required", report)
        self.assertEqual(0, self.invoke("validate", str(target))[0])
        self.assertEqual(0, self.invoke("dashboard", str(target))[0])
        self.assertTrue((target / "target/harness-dashboard/index.html").is_file())
        self.assert_portable_release_surfaces(target)

    def test_adopt_adds_dedicated_workflow_without_changing_existing_ci(self) -> None:
        target = self.root / "existing-ci"
        workflows = target / ".github" / "workflows"
        workflows.mkdir(parents=True)
        existing = {
            "build.yml": b"name: Build\non: [push]\n",
            "deploy.yml": b"name: Deploy\non: workflow_dispatch\n",
        }
        for name, content in existing.items():
            (workflows / name).write_bytes(content)

        code, _, error = self.invoke("adopt", str(target), "--project-name", "Existing CI")
        self.assertEqual(0, code, error)
        for name, content in existing.items():
            self.assertEqual(content, (workflows / name).read_bytes())
        managed = workflows / "engineering-harness.yml"
        self.assertTrue(managed.is_file())
        self.assertIn(f'SE_HARNESS_VERSION: "{__version__}"', managed.read_text(encoding="utf-8"))

    def test_adopt_rejects_unknown_dedicated_workflow_without_writes(self) -> None:
        target = self.root / "workflow-conflict"
        workflows = target / ".github" / "workflows"
        workflows.mkdir(parents=True)
        managed = workflows / "engineering-harness.yml"
        original = b"name: Repository owned\non: [push]\n"
        managed.write_bytes(original)

        code, output, error = self.invoke("adopt", str(target))
        self.assertEqual(1, code)
        self.assertIn("conflict", output)
        self.assertIn("another workflow filename", error)
        self.assertEqual(original, managed.read_bytes())
        self.assertFalse((target / ".engineering-harness.lock").exists())

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

    def test_upgrade_migrates_unmodified_consumer_workflow_and_blocks_customization(self) -> None:
        target = self.root / "workflow-upgrade"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        workflow = target / ".github" / "workflows" / "engineering-harness.yml"
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        legacy = b"name: Legacy managed consumer workflow\non: [push]\n"
        workflow.write_bytes(legacy)
        lock["files"][".github/workflows/engineering-harness.yml"]["sha256"] = canonical_sha256(legacy)
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        code, output, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertIn("update     .github/workflows/engineering-harness.yml", output)
        self.assertIn(f'SE_HARNESS_VERSION: "{__version__}"', workflow.read_text(encoding="utf-8"))
        self.assertEqual(0, self.invoke("upgrade", str(target), "--apply")[0])

        workflow.write_text(workflow.read_text(encoding="utf-8") + "\n# Owner edit\n", encoding="utf-8")
        original = workflow.read_bytes()
        missing = target / "docs" / "engineering" / "TRACEABILITY.md"
        missing.unlink()
        code, _, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(1, code)
        self.assertIn("separate workflow", error)
        self.assertEqual(original, workflow.read_bytes())
        self.assertFalse(missing.exists())

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

    def test_upgrade_adds_cross_agent_files_without_reviving_the_retired_scaffold(self) -> None:
        target = self.root / "older-installation"
        self.assertEqual(0, self.invoke("init", str(target), "--project-name", "Legacy Project")[0])
        claude_path = target / "CLAUDE.md"
        retired = "docs/engineering/REPOSITORY_CONTEXT.md"
        claude_path.unlink()
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"].pop("CLAUDE.md")
        lock["files"][retired] = {"mode": "seed", "state": "present"}
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        code, output, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertIn("add        CLAUDE.md", output)
        self.assertNotIn(retired, output)
        self.assertIn("@AGENTS.md", claude_path.read_text(encoding="utf-8"))
        self.assertFalse((target / retired).exists())
        regenerated = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertNotIn(retired, regenerated["files"])

    def test_upgrade_preserves_claude_customization_and_owner_content_at_the_retired_path(self) -> None:
        target = self.root / "repository-owned-context"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        claude_path = target / "CLAUDE.md"
        retired = "docs/engineering/REPOSITORY_CONTEXT.md"
        context_path = target / retired
        claude_path.write_text(claude_path.read_text(encoding="utf-8") + "\n## Claude-specific\nKeep this.\n", encoding="utf-8")
        context_path.write_bytes(b"# Curated\r\nUse `python -m unittest`.\r\n")
        before = context_path.read_bytes()

        code, _, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertIn("Keep this.", claude_path.read_text(encoding="utf-8"))
        self.assertEqual(before, context_path.read_bytes())
        lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertNotIn(retired, lock["files"])

        context_path.unlink()
        code, _, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertFalse(context_path.exists())
        lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertNotIn(retired, lock["files"])

    def test_pre3_locks_are_refused_with_the_floor_diagnostic(self) -> None:
        # WO-HUP-012 (HUP-LSF-001, HUP-LSF-004): a schema-1 or schema-2 lock is
        # refused at read by doctor and by upgrade, before any write, and the
        # tree stays byte-identical.
        for legacy_schema in (1, 2):
            with self.subTest(schema=legacy_schema):
                target = self.root / f"pre3-schema-{legacy_schema}"
                self.assertEqual(0, self.invoke("init", str(target), "--project-name", "Legacy")[0])
                self.make_pre3_lock(target, legacy_schema)
                snapshot = {
                    path: path.read_bytes()
                    for path in sorted(target.rglob("*"))
                    if path.is_file()
                }

                code, output, error = self.invoke("doctor", str(target))
                self.assertEqual(1, code)
                self.assertIn("predates the supported floor (schema 3)", output + error)
                self.assertIn("re-adopt", output + error)

                for arguments in (("upgrade", str(target)), ("upgrade", str(target), "--apply")):
                    code, output, error = self.invoke(*arguments)
                    self.assertEqual(2, code)
                    self.assertIn("predates the supported floor (schema 3)", output + error)

                for path, content in snapshot.items():
                    self.assertEqual(content, path.read_bytes(), path)

    def test_removing_the_stale_lock_and_readopting_writes_schema_three(self) -> None:
        # WO-HUP-012 (HUP-LSF-001, HUP-LSF-003): the diagnostic's route works —
        # remove the pre-3 lock, re-adopt, and the emitted lock is schema 3.
        target = self.root / "pre3-readopted"
        self.assertEqual(0, self.invoke("init", str(target), "--project-name", "Legacy")[0])
        self.make_pre3_lock(target, 2)
        lock_path = target / ".engineering-harness.lock"
        lock_path.unlink()

        code, _, error = self.invoke("adopt", str(target), "--project-name", "Legacy")
        self.assertEqual(0, code, error)
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertEqual(LOCK_SCHEMA, lock["schema"])
        self.assertEqual(HASH_ALGORITHM, lock["hash_algorithm"])
        self.assertEqual(HASH_MODE, lock["hash_mode"])
        self.assertEqual(__version__, lock["evaluator"]["version"])
        self.assertRegex(lock["evaluator"]["payload_sha256"], r"^[0-9a-f]{64}$")
        self.assert_portable_release_surfaces(target)

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

    def test_doctor_detects_stale_canonical_lock_digest(self) -> None:
        target = self.root / "stale-lock"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"]["docs/engineering/WORKFLOW.md"]["sha256"] = "0" * 64
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        code, output, _ = self.invoke("doctor", str(target))
        self.assertEqual(1, code)
        self.assertIn("FAIL managed:docs/engineering/WORKFLOW.md", output)

    def test_doctor_detects_missing_claude_import_and_ignores_the_retired_path(self) -> None:
        target = self.root / "doctor-instructions"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        claude_path = target / "CLAUDE.md"
        claude_path.write_text(claude_path.read_text(encoding="utf-8").replace("@AGENTS.md", "Claude rules only."), encoding="utf-8")

        code, output, _ = self.invoke("doctor", str(target))
        self.assertEqual(1, code)
        self.assertIn("FAIL claude-import", output)
        self.assertNotIn("docs/engineering/REPOSITORY_CONTEXT.md", output)

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
        self.assertIn("Harness inspection (repository_wide)", inspection.stdout)
        self.assertIn("repository-local, derived observation", inspection.stdout)
        inspection_json = subprocess.run(
            [sys.executable, "-m", "se_harness", "inspect", str(target), "--json"],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, inspection_json.returncode, inspection_json.stderr)
        decoded_inspection = json.loads(inspection_json.stdout)
        self.assertEqual("se-harness-inspection-v2", decoded_inspection["schema"])
        self.assertEqual("repository_wide", decoded_inspection["mode"])
        self.assertEqual({"primary": None, "artifacts": []}, decoded_inspection["selection"])
        self.assertEqual(before, sorted(path.relative_to(target).as_posix() for path in target.rglob("*")))
        self.assertEqual(0, self.invoke("dashboard", str(target))[0])
        dashboard = target / "target/harness-dashboard"
        self.assertTrue((dashboard / "dashboard-manifest.json").is_file())
        self.assertTrue((dashboard / "data/summary").is_dir())
        self.assertTrue((dashboard / "data/topology").is_dir())
        self.assertTrue((dashboard / "data/readiness").is_dir())
        manifest = json.loads((dashboard / "dashboard-manifest.json").read_text(encoding="utf-8"))
        self.assertFalse(any(item["role"] == "artifact" for item in manifest["resources"]))

    def test_harness_commands_execute_distribution_scripts_not_target_copies(self) -> None:
        target = self.root / "distribution-commands"
        self.assertEqual(0, self.invoke("init", str(target))[0])
        for name in (
            "validate_engineering_artifacts.py",
            "inspect_engineering_artifacts.py",
            "generate_harness_dashboard.py",
        ):
            (target / "scripts" / name).write_text("raise SystemExit(73)\n", encoding="utf-8")

        self.assertEqual(0, self.invoke("validate", str(target))[0])
        self.assertEqual(0, self.invoke("inspect", str(target))[0])
        self.assertEqual(0, self.invoke("dashboard", str(target))[0])
        code, output, error = self.invoke("doctor", str(target))
        self.assertEqual(1, code, error)
        self.assertIn("FAIL managed:scripts/validate_engineering_artifacts.py", output)

    def test_lock_contains_hashes_without_generated_adoption_report(self) -> None:
        target = self.root / "lock"
        target.mkdir()
        self.assertEqual(0, self.invoke("adopt", str(target))[0])
        lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual(LOCK_SCHEMA, lock["schema"])
        self.assertEqual(HASH_ALGORITHM, lock["hash_algorithm"])
        self.assertEqual(HASH_MODE, lock["hash_mode"])
        self.assertEqual(__version__, lock["evaluator"]["version"])
        self.assertRegex(lock["evaluator"]["payload_sha256"], r"^[0-9a-f]{64}$")
        self.assertIn("scripts/validate_engineering_artifacts.py", lock["files"])
        self.assertIn("scripts/inspect_engineering_artifacts.py", lock["files"])
        self.assertEqual("fragment", lock["files"]["CLAUDE.md"]["mode"])
        self.assertEqual({"mode": "seed", "state": "present"}, lock["files"]["docs/engineering/README.md"])
        self.assertNotIn("docs/engineering/REPOSITORY_CONTEXT.md", lock["files"])
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
