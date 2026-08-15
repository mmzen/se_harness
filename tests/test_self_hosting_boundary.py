from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import tomllib
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from se_harness import __version__
from se_harness.candidate_acceptance import (
    ACCEPTANCE_SCHEMA,
    CONTRACT_SHA256,
    SCENARIO_IDS,
    AcceptanceManifest,
    ScenarioResult,
    assess_candidate_wheel,
)
from se_harness.installer import HarnessError, apply_changes, plan_install
from se_harness.governor_reconciliation import (
    WORKFLOW_TEMPLATE,
    _render_workflow,
    apply_governor_reconciliation,
    plan_governor_reconciliation,
    self_hosting_template_root,
)
from se_harness.integrity import HASH_ALGORITHM, HASH_MODE, canonical_sha256
from se_harness.preflight import inspect_installation
from se_harness.runtime_identity import _lexically_within, _within, inspect_runtime_identity
from se_harness.self_hosting import (
    DESCRIPTOR_PATH,
    load_governor_descriptor,
    self_hosting_enabled,
)
from se_harness.self_hosting_policy import PROTECTED_CONTROL_PATHS, classify_self_hosting


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GOVERNOR_SHA256 = "533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454"
FAILED_PR_RECORDS = (
    "docs/engineering/release-0.2.2/verification-records/VREC-SEH-003.md",
    "docs/engineering/release-0.2.2/releases/RLS-SEH-003.md",
)


class SelfHostingBoundaryTests(unittest.TestCase):
    def make_self_hosting_target(self, root: Path) -> None:
        for relative in (
            ".engineering-harness.toml",
            ".engineering-harness.lock",
            ".github/workflows/engineering-harness.yml",
            ".self-hosting/governor.toml",
            "pyproject.toml",
            "se_harness/__init__.py",
        ):
            source = REPOSITORY_ROOT / relative
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    def make_reconcilable_target(self, root: Path) -> None:
        root.mkdir(parents=True)
        for relative in ("pyproject.toml", "se_harness/__init__.py"):
            source = REPOSITORY_ROOT / relative
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        config = (REPOSITORY_ROOT / ".engineering-harness.toml").read_text(encoding="utf-8")
        config = config.replace("require_clean_worktree = true", "require_clean_worktree = false")
        (root / ".engineering-harness.toml").write_text(config, encoding="utf-8")
        descriptor_text = "\n".join(
            (
                "schema = 1",
                f'version = "{__version__}"',
                f'tag = "v{__version__}"',
                f'wheel = "se_harness-{__version__}-py3-none-any.whl"',
                f'url = "https://github.com/mmzen/se_harness/releases/download/v{__version__}/se_harness-{__version__}-py3-none-any.whl"',
                f'sha256 = "{"a" * 64}"',
                'selected_release_record = "RLS-SHB-900"',
                f'selected_candidate_commit = "{"b" * 40}"',
                "",
            )
        )
        descriptor_path = root / ".self-hosting/governor.toml"
        descriptor_path.parent.mkdir(parents=True)
        descriptor_path.write_text(descriptor_text, encoding="utf-8")
        descriptor = load_governor_descriptor(root)
        workflow = _render_workflow(
            (self_hosting_template_root() / WORKFLOW_TEMPLATE).read_bytes(),
            descriptor,
            __version__,
        )
        workflow_path = root / ".github/workflows/engineering-harness.yml"
        workflow_path.parent.mkdir(parents=True)
        workflow_path.write_bytes(workflow)
        lock = {
            "schema": 2,
            "hash_algorithm": HASH_ALGORITHM,
            "hash_mode": HASH_MODE,
            "tool_version": __version__,
            "files": {
                ".engineering-harness.toml": {
                    "mode": "managed",
                    "sha256": canonical_sha256((root / ".engineering-harness.toml").read_bytes()),
                },
                ".github/workflows/engineering-harness.yml": {
                    "mode": "managed",
                    "sha256": canonical_sha256(workflow),
                },
            },
        }
        (root / ".engineering-harness.lock").write_text(
            json.dumps(lock, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def make_target_wheel(
        self,
        root: Path,
        *,
        version: str = "0.3.0",
        migration_suffix: str = "",
    ) -> tuple[Path, str]:
        wheel = root / f"se_harness-{version}-py3-none-any.whl"
        material = self_hosting_template_root()
        prefix = "payload.data/data/share/se-harness/self-hosting"
        migration = (material / "governor-migration.toml").read_text(encoding="utf-8") + migration_suffix
        with zipfile.ZipFile(wheel, "w") as archive:
            archive.writestr(
                f"se_harness-{version}.dist-info/METADATA",
                f"Metadata-Version: 2.1\nName: se-harness\nVersion: {version}\n",
            )
            archive.writestr(f"{prefix}/governor-migration.toml", migration)
            archive.writestr(
                f"{prefix}/engineering-harness.yml.tpl",
                (material / "engineering-harness.yml.tpl").read_bytes(),
            )
            archive.writestr(
                f"{prefix}/self-hosting-governor.yml",
                (material / "self-hosting-governor.yml").read_bytes(),
            )
            archive.writestr("se_harness/malicious.py", "raise RuntimeError('target code executed')\n")
        return wheel, hashlib.sha256(wheel.read_bytes()).hexdigest()

    def test_governor_descriptor_is_exact_and_matches_self_hosting_workflow(self) -> None:
        descriptor = load_governor_descriptor(REPOSITORY_ROOT)
        self.assertEqual("0.2.1", descriptor.version)
        self.assertEqual("v0.2.1", descriptor.tag)
        self.assertEqual(GOVERNOR_SHA256, descriptor.sha256)
        self.assertEqual("RLS-SEH-002", descriptor.selected_release_record)

        workflow = (REPOSITORY_ROOT / ".github/workflows/engineering-harness.yml").read_text(
            encoding="utf-8"
        )
        for value in (
            descriptor.version,
            descriptor.tag,
            descriptor.wheel,
            descriptor.url,
            descriptor.sha256,
        ):
            self.assertIn(value, workflow)

    def test_invalid_governor_descriptor_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / DESCRIPTOR_PATH
            path.parent.mkdir(parents=True)
            source = (REPOSITORY_ROOT / DESCRIPTOR_PATH).read_text(encoding="utf-8")
            path.write_text(source.replace(GOVERNOR_SHA256, "0" * 63), encoding="utf-8")
            with self.assertRaisesRegex(Exception, "SHA-256"):
                load_governor_descriptor(root)

    def test_candidate_source_identity_is_deterministic_and_bounded(self) -> None:
        commit = "a" * 40
        with mock.patch.dict(
            os.environ,
            {"EXAMPLE_SECRET_TOKEN": "must-not-appear"},
            clear=True,
        ), mock.patch("se_harness.runtime_identity.site.ENABLE_USER_SITE", False):
            first = inspect_runtime_identity(
                role="candidate-source",
                expected_version=__version__,
                expected_root=REPOSITORY_ROOT,
                checkout_root=REPOSITORY_ROOT,
                candidate_commit=commit,
            )
            second = inspect_runtime_identity(
                role="candidate-source",
                expected_version=__version__,
                expected_root=REPOSITORY_ROOT,
                checkout_root=REPOSITORY_ROOT,
                candidate_commit=commit,
            )
        self.assertTrue(first.passed, first.diagnostics)
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertNotIn("must-not-appear", json.dumps(first.to_dict(), sort_keys=True))

    def test_virtualenv_launcher_boundary_does_not_follow_base_interpreter_symlink(self) -> None:
        environment = Path("/tmp/candidate-env")
        launcher = environment / "bin/python"
        base_interpreter = Path("/opt/python/bin/python3.11")

        self.assertTrue(_lexically_within(launcher, environment))
        self.assertFalse(_lexically_within(base_interpreter, environment))
        self.assertFalse(_within(base_interpreter, environment))

    def test_equal_version_cannot_substitute_checkout_source_for_installed_role(self) -> None:
        identity = inspect_runtime_identity(
            role="candidate-package",
            expected_version=__version__,
            expected_root=Path(sys.prefix),
            checkout_root=REPOSITORY_ROOT,
            candidate_commit="b" * 40,
        )
        self.assertFalse(identity.passed)
        codes = {item.code for item in identity.diagnostics}
        self.assertTrue({"RID003", "RID006"}.intersection(codes), codes)

    def test_candidate_source_rejects_external_distribution_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, mock.patch(
            "se_harness.runtime_identity._distribution_root",
            return_value=Path(temporary),
        ):
            identity = inspect_runtime_identity(
                role="candidate-source",
                expected_version=__version__,
                expected_root=REPOSITORY_ROOT,
                checkout_root=REPOSITORY_ROOT,
                candidate_commit="d" * 40,
            )
        self.assertIn("RID018", {item.code for item in identity.diagnostics})

    def test_installed_role_rejects_entry_point_from_another_environment(self) -> None:
        identity = inspect_runtime_identity(
            role="candidate-package",
            expected_version=__version__,
            expected_root=Path(sys.prefix),
            checkout_root=REPOSITORY_ROOT,
            candidate_commit="e" * 40,
            entry_point=REPOSITORY_ROOT / "foreign-harnessctl",
            require_entry_point=True,
        )
        self.assertIn("RID010", {item.code for item in identity.diagnostics})

    def test_installed_role_rejects_inherited_pythonpath(self) -> None:
        with mock.patch.dict(os.environ, {"PYTHONPATH": str(REPOSITORY_ROOT)}):
            identity = inspect_runtime_identity(
                role="governor",
                expected_version=__version__,
                expected_root=Path(sys.prefix),
                checkout_root=REPOSITORY_ROOT,
                governor_wheel_sha256="c" * 64,
            )
        self.assertIn("RID008", {item.code for item in identity.diagnostics})

    def test_path_containment_is_component_aware_and_resolves_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            boundary = root / "candidate"
            inside = boundary / "package" / "module.py"
            sibling = root / "candidate-shadow" / "module.py"
            inside.parent.mkdir(parents=True)
            sibling.parent.mkdir(parents=True)
            inside.write_text("", encoding="utf-8")
            sibling.write_text("", encoding="utf-8")
            self.assertTrue(_within(inside, boundary))
            self.assertFalse(_within(sibling, boundary))

    def test_self_hosting_exception_is_narrow_and_descriptor_backed(self) -> None:
        self.assertTrue(self_hosting_enabled(REPOSITORY_ROOT))
        checks = inspect_installation(REPOSITORY_ROOT)
        governor = [item for item in checks if item.name == "self-hosting-governor"]
        self.assertEqual(1, len(governor))
        self.assertTrue(governor[0].passed)
        self.assertTrue(all(item.passed for item in checks), [item for item in checks if not item.passed])
        exceptions = [
            item
            for item in checks
            if item.name.startswith("distribution:")
            and item.detail == "repository-specific self-hosting control"
        ]
        self.assertEqual(
            {
                "distribution:.engineering-harness.toml",
                "distribution:.github/workflows/engineering-harness.yml",
            },
            {item.name for item in exceptions},
        )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".engineering-harness.toml").write_text(
                '[self_hosting]\nrole = "implementation-repository"\n',
                encoding="utf-8",
            )
            self.assertFalse(self_hosting_enabled(root))

    def test_shared_policy_is_tri_state_and_protected_set_is_exact(self) -> None:
        self.assertEqual(
            {
                ".engineering-harness.toml",
                ".github/workflows/engineering-harness.yml",
            },
            set(PROTECTED_CONTROL_PATHS),
        )
        self.assertEqual("self-hosting", classify_self_hosting(REPOSITORY_ROOT).kind)
        with tempfile.TemporaryDirectory() as temporary:
            consumer = Path(temporary) / "consumer"
            consumer.mkdir()
            self.assertEqual("consumer", classify_self_hosting(consumer).kind)
            ambiguous = Path(temporary) / "ambiguous"
            self.make_self_hosting_target(ambiguous)
            (ambiguous / ".engineering-harness.toml").write_text(
                '[self_hosting]\nrole = "implementation-repository"\n',
                encoding="utf-8",
            )
            self.assertEqual("ambiguous", classify_self_hosting(ambiguous).kind)
            with self.assertRaisesRegex(HarnessError, "ambiguous self-hosting target"):
                plan_install(ambiguous, project_name=None, mode="upgrade")

    def test_normal_upgrade_protects_controls_and_updates_only_ordinary_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "implementation"
            self.make_self_hosting_target(root)
            config_before = (root / ".engineering-harness.toml").read_bytes()
            workflow_before = (root / ".github/workflows/engineering-harness.yml").read_bytes()

            changes, old_lock = plan_install(root, project_name=None, mode="upgrade")
            actions = {item.path: item.action for item in changes}
            self.assertEqual("protected", actions[".engineering-harness.toml"])
            self.assertEqual("protected", actions[".github/workflows/engineering-harness.yml"])
            self.assertEqual("add", actions["ENGINEERING_HARNESS.md"])

            apply_changes(root, changes, old_lock, allow_updates=True)
            self.assertEqual(config_before, (root / ".engineering-harness.toml").read_bytes())
            self.assertEqual(workflow_before, (root / ".github/workflows/engineering-harness.yml").read_bytes())
            self.assertTrue((root / "ENGINEERING_HARNESS.md").is_file())

    def test_protected_drift_blocks_every_upgrade_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "implementation"
            self.make_self_hosting_target(root)
            workflow = root / ".github/workflows/engineering-harness.yml"
            workflow.write_bytes(workflow.read_bytes() + b"\n# unauthorized drift\n")
            before = workflow.read_bytes()

            changes, old_lock = plan_install(root, project_name=None, mode="upgrade")
            actions = {item.path: item.action for item in changes}
            self.assertEqual("protected-mismatch", actions[workflow.relative_to(root).as_posix()])
            with self.assertRaisesRegex(HarnessError, "protected-control mismatches"):
                apply_changes(root, changes, old_lock, allow_updates=True)
            self.assertEqual(before, workflow.read_bytes())
            self.assertFalse((root / "ENGINEERING_HARNESS.md").exists())

    def test_reconcile_governor_migrates_policy_and_complete_control_set(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "implementation"
            self.make_reconcilable_target(root)
            wheel, digest = self.make_target_wheel(
                Path(temporary),
                migration_suffix=(
                    "\n[[fields]]\n"
                    'path = "harness.validation_mode"\n'
                    'ownership = "release-managed"\n'
                    'type = "string"\n'
                    'value = "strict"\n'
                ),
            )
            with mock.patch(
                "se_harness.governor_reconciliation.run_preflight",
                return_value=SimpleNamespace(ready=True, diagnostics=()),
            ):
                plan = plan_governor_reconciliation(
                    root,
                    version="0.3.0",
                    commit="c" * 40,
                    release_record="RLS-SHB-901",
                    sha256=digest,
                    work_order="WO-SHB-002",
                    wheel_path=wheel,
                )
            self.assertFalse(plan.blocked, plan.changes)
            desired_config = next(item.desired for item in plan.changes if item.path == ".engineering-harness.toml")
            self.assertIsNotNone(desired_config)
            parsed = tomllib.loads(desired_config.decode("utf-8"))  # type: ignore[union-attr]
            self.assertFalse(parsed["revision_provenance"]["require_clean_worktree"])
            self.assertEqual("strict", parsed["harness"]["validation_mode"])
            self.assertEqual("0.3.0", parsed["harness"]["tool_version"])

            apply_governor_reconciliation(root, plan)
            self.assertEqual("0.3.0", load_governor_descriptor(root).version)
            workflow = (root / ".github/workflows/engineering-harness.yml").read_text(encoding="utf-8")
            self.assertIn("@" + "c" * 40, workflow)
            self.assertIn('governor-version: "0.3.0"', workflow)
            lock = json.loads((root / ".engineering-harness.lock").read_text(encoding="utf-8"))
            self.assertEqual("0.3.0", lock["governor"]["version"])
            self.assertEqual(
                canonical_sha256((root / ".engineering-harness.toml").read_bytes()),
                lock["files"][".engineering-harness.toml"]["sha256"],
            )

    def test_reconcile_governor_reports_decision_required_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "implementation"
            self.make_reconcilable_target(root)
            wheel, digest = self.make_target_wheel(
                Path(temporary),
                migration_suffix=(
                    "\n[[fields]]\n"
                    'path = "revision_provenance.new_authority_policy"\n'
                    'ownership = "repository-policy"\n'
                    'type = "boolean"\n'
                ),
            )
            before = {
                relative: (root / relative).read_bytes()
                for relative in (
                    ".self-hosting/governor.toml",
                    ".engineering-harness.toml",
                    ".github/workflows/engineering-harness.yml",
                    ".engineering-harness.lock",
                )
            }
            with mock.patch(
                "se_harness.governor_reconciliation.run_preflight",
                return_value=SimpleNamespace(ready=True, diagnostics=()),
            ):
                plan = plan_governor_reconciliation(
                    root,
                    version="0.3.0",
                    commit="c" * 40,
                    release_record="RLS-SHB-901",
                    sha256=digest,
                    work_order="WO-SHB-002",
                    wheel_path=wheel,
                )
            self.assertTrue(plan.blocked)
            decision = next(item for item in plan.changes if item.action == "decision-required")
            self.assertIn("new_authority_policy", decision.detail)
            with self.assertRaisesRegex(HarnessError, "blocked"):
                apply_governor_reconciliation(root, plan)
            self.assertEqual(before, {relative: (root / relative).read_bytes() for relative in before})

            with mock.patch(
                "se_harness.governor_reconciliation.run_preflight",
                return_value=SimpleNamespace(ready=True, diagnostics=()),
            ):
                resolved = plan_governor_reconciliation(
                    root,
                    version="0.3.0",
                    commit="c" * 40,
                    release_record="RLS-SHB-901",
                    sha256=digest,
                    work_order="WO-SHB-002",
                    wheel_path=wheel,
                    decisions=("revision_provenance.new_authority_policy=true",),
                )
            self.assertFalse(resolved.blocked, resolved.changes)
            desired = next(
                item.desired for item in resolved.changes if item.path == ".engineering-harness.toml"
            )
            self.assertTrue(
                tomllib.loads(desired.decode("utf-8"))["revision_provenance"]["new_authority_policy"]  # type: ignore[union-attr]
            )

    def test_reconcile_governor_rejects_accepted_unknown_workflow_delta(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "implementation"
            self.make_reconcilable_target(root)
            workflow = root / ".github/workflows/engineering-harness.yml"
            workflow.write_bytes(workflow.read_bytes() + b"\n# governed but undocumented local delta\n")
            lock_path = root / ".engineering-harness.lock"
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            lock["files"][".github/workflows/engineering-harness.yml"]["sha256"] = canonical_sha256(
                workflow.read_bytes()
            )
            lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            wheel, digest = self.make_target_wheel(Path(temporary))
            with mock.patch(
                "se_harness.governor_reconciliation.run_preflight",
                return_value=SimpleNamespace(ready=True, diagnostics=()),
            ):
                plan = plan_governor_reconciliation(
                    root,
                    version="0.3.0",
                    commit="c" * 40,
                    release_record="RLS-SHB-901",
                    sha256=digest,
                    work_order="WO-SHB-002",
                    wheel_path=wheel,
                )
            self.assertTrue(plan.blocked)
            self.assertEqual(
                "conflict",
                next(item.action for item in plan.changes if item.path.endswith("engineering-harness.yml")),
            )

    def test_reconcile_governor_restores_prior_state_on_interrupted_apply(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "implementation"
            self.make_reconcilable_target(root)
            wheel, digest = self.make_target_wheel(Path(temporary))
            with mock.patch(
                "se_harness.governor_reconciliation.run_preflight",
                return_value=SimpleNamespace(ready=True, diagnostics=()),
            ):
                plan = plan_governor_reconciliation(
                    root,
                    version="0.3.0",
                    commit="c" * 40,
                    release_record="RLS-SHB-901",
                    sha256=digest,
                    work_order="WO-SHB-002",
                    wheel_path=wheel,
                )
            before = {item.path: (root / item.path).read_bytes() for item in plan.changes}
            real_replace = os.replace
            failed = False

            def interrupt(source: str | os.PathLike[str], destination: str | os.PathLike[str]) -> None:
                nonlocal failed
                if Path(destination) == root / ".engineering-harness.toml" and not failed:
                    failed = True
                    raise OSError("simulated interruption")
                real_replace(source, destination)

            with mock.patch("se_harness.governor_reconciliation.os.replace", side_effect=interrupt):
                with self.assertRaisesRegex(HarnessError, "prior state restored"):
                    apply_governor_reconciliation(root, plan)
            self.assertEqual(before, {path: (root / path).read_bytes() for path in before})
            self.assertFalse((root / ".self-hosting/.reconcile-governor-transaction").exists())

    def test_acceptance_manifest_is_canonical_and_contract_is_complete(self) -> None:
        scenarios = tuple(
            ScenarioResult(item, "passed", hashlib.sha256(item.encode("utf-8")).hexdigest())
            for item in SCENARIO_IDS
        )
        manifest = AcceptanceManifest(
            schema=ACCEPTANCE_SCHEMA,
            verifier_version=__version__,
            verifier_wheel_sha256="a" * 64,
            contract_sha256=CONTRACT_SHA256,
            candidate_version="0.3.0",
            candidate_commit="b" * 40,
            candidate_wheel_sha256="c" * 64,
            python_version="3.11.0",
            scenarios=scenarios,
        )
        first = manifest.canonical_bytes()
        second = manifest.canonical_bytes()
        self.assertEqual(first, second)
        parsed = json.loads(first)
        self.assertEqual(list(SCENARIO_IDS), [item["scenario_id"] for item in parsed["scenarios"]])
        self.assertEqual(CONTRACT_SHA256, parsed["verifier"]["contract_sha256"])

    def test_candidate_checkout_cannot_supply_released_acceptance_runner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            wheel, _ = self.make_target_wheel(Path(temporary))
            with self.assertRaisesRegex(HarnessError, "checkout cannot supply"):
                assess_candidate_wheel(
                    wheel,
                    candidate_commit="b" * 40,
                    candidate_wheel_sha256=hashlib.sha256(wheel.read_bytes()).hexdigest(),
                    verifier_wheel_sha256="a" * 64,
                    checkout_root=REPOSITORY_ROOT,
                )

    def test_candidate_acceptance_requires_the_selected_wheel_digest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            wheel, _ = self.make_target_wheel(Path(temporary))
            with self.assertRaisesRegex(HarnessError, "candidate wheel SHA-256 mismatch"):
                assess_candidate_wheel(
                    wheel,
                    candidate_commit="b" * 40,
                    candidate_wheel_sha256="0" * 64,
                    verifier_wheel_sha256="a" * 64,
                )

    def test_checkout_snapshot_is_bounded_and_rejects_symlinks(self) -> None:
        from se_harness.candidate_acceptance import _snapshot

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "one").write_text("1", encoding="utf-8")
            with mock.patch("se_harness.candidate_acceptance.MAX_SNAPSHOT_FILES", 0):
                with self.assertRaisesRegex(HarnessError, "bounded file count"):
                    _snapshot(root)

    def test_workflow_has_non_substitutable_three_plane_gates(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github/workflows/engineering-harness.yml").read_text(
            encoding="utf-8"
        )
        self.assertRegex(workflow, r"(?m)^  governor:$")
        self.assertRegex(workflow, r"(?m)^  candidate-source:$")
        self.assertRegex(workflow, r"(?m)^  candidate-package:$")
        self.assertRegex(workflow, r"(?s)candidate-source:.*?needs: governor")
        self.assertRegex(workflow, r"(?s)candidate-package:.*?needs: candidate-source")
        self.assertIn('doctor "$RUNNER_TEMP/governor-target"', workflow)
        self.assertNotIn("harnessctl doctor .", workflow)
        self.assertIn("git archive \"$GITHUB_SHA\"", workflow)
        self.assertIn("non-promotable candidate wheel", workflow)
        candidate_workflow = (REPOSITORY_ROOT / "self_hosting/self-hosting-governor.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("--candidate-wheel-sha256", candidate_workflow)
        self.assertIn("--require-isolated-python", workflow)
        self.assertIn("--entry-point", workflow)
        governor_lane = workflow.split("  governor:", 1)[1].split("  candidate-source:", 1)[0]
        self.assertNotIn("validate_engineering_artifacts.py", governor_lane)
        self.assertIn("compatibility_scope", governor_lane)
        self.assertIn("git diff --exit-code", workflow)
        self.assertNotIn("pull_request_target", workflow)
        self.assertNotIn("permissions:\n  contents: write", workflow)
        self.assertIn("python_launcher = pathlib.Path(sys.executable).absolute()", workflow)
        self.assertNotIn("pathlib.Path(sys.executable).resolve())", workflow)

    def test_failed_pr_records_are_excluded_from_recovery_candidate(self) -> None:
        for relative in FAILED_PR_RECORDS:
            with self.subTest(relative=relative):
                self.assertFalse((REPOSITORY_ROOT / relative).exists())


if __name__ == "__main__":
    unittest.main()
