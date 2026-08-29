from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import tomllib
import unittest
import zipfile
from pathlib import Path
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
from se_harness.installer import HarnessError, apply_changes, plan_install, tracked_content
from tests.skill_contract_support import build_skill_manifest
from se_harness.integrity import canonical_sha256
from tests.mutation_guard_support import trusted_mutation_authority
from se_harness.preflight import inspect_installation
from se_harness.runtime_identity import _lexically_within, _within, inspect_runtime_identity


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FAILED_PR_RECORDS = (
    "docs/engineering/release-0.2.2/verification-records/VREC-SEH-003.md",
    "docs/engineering/release-0.2.2/releases/RLS-SEH-003.md",
)


class StandardRepositoryLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.guard = mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=trusted_mutation_authority,
        )
        self.guard.start()
        self.addCleanup(self.guard.stop)

    def make_candidate_wheel(self, root: Path, version: str = "0.4.1") -> tuple[Path, str]:
        wheel = root / f"se_harness-{version}-py3-none-any.whl"
        with zipfile.ZipFile(wheel, "w") as archive:
            archive.writestr(
                f"se_harness-{version}.dist-info/METADATA",
                f"Metadata-Version: 2.1\nName: se-harness\nVersion: {version}\n",
            )
        return wheel, hashlib.sha256(wheel.read_bytes()).hexdigest()

    def test_standard_install_manages_all_canonical_cores_and_thin_host_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            changes, old_lock = plan_install(target, project_name="Agentic Fixture", mode="init")
            skill_changes = [item for item in changes if item.path.startswith(".agents/skills/")]
            self.assertEqual(
                [
                    ".agents/skills/harness-operator-brief/SKILL.md",
                    ".agents/skills/harness-operator-brief/scripts/check_brief.py",
                    ".agents/skills/harness-operator-brief/skill-contract.json",
                    ".agents/skills/harness-orient/SKILL.md",
                    ".agents/skills/harness-orient/scripts/orient.py",
                    ".agents/skills/harness-orient/skill-contract.json",
                ],
                [item.path for item in skill_changes],
            )
            self.assertTrue(all(item.mode == "managed" and item.action == "add" for item in skill_changes))
            adapter_changes = [item for item in changes if item.path.startswith(".claude/skills/")]
            self.assertEqual(
                [
                    ".claude/skills/harness-orient/SKILL.md",
                ],
                [item.path for item in adapter_changes],
            )
            self.assertTrue(all(item.mode == "managed" and item.action == "add" for item in adapter_changes))

            apply_changes(target, changes, old_lock, allow_updates=False)
            for name in ("harness-orient", "harness-operator-brief"):
                installed = target / ".agents/skills" / name
                source = REPOSITORY_ROOT / "templates/repository/standard/.agents/skills" / name
                self.assertEqual(build_skill_manifest(source).sha256, build_skill_manifest(installed).sha256)
                contract = json.loads((installed / "skill-contract.json").read_text(encoding="utf-8"))
                self.assertEqual(name, contract["name"])
            lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
            self.assertTrue(
                all(lock["files"][item.path]["mode"] == "managed" for item in skill_changes + adapter_changes)
            )
            replay, _ = plan_install(target, project_name=None, mode="upgrade")
            replay_actions = {item.path: item.action for item in replay}
            for item in skill_changes + adapter_changes:
                self.assertEqual("unchanged", replay_actions[item.path])

    def test_agents_only_upgrade_adds_host_surfaces_without_changing_orientation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            changes, old_lock = plan_install(target, project_name="Phase 3 Fixture", mode="init")
            phase3_only = [
                item
                for item in changes
                if not item.path.startswith(".claude/skills/")
                and not item.path.endswith("/agents/openai.yaml")
            ]
            apply_changes(target, phase3_only, old_lock, allow_updates=False)
            orientation = target / ".agents/skills/harness-orient"
            orientation_before = {
                path.relative_to(orientation).as_posix(): path.read_bytes()
                for path in orientation.rglob("*")
                if path.is_file()
            }

            upgrade, upgrade_lock = plan_install(target, project_name=None, mode="upgrade")
            actions = {item.path: item.action for item in upgrade}
            expected_additions = {".claude/skills/harness-orient/SKILL.md"}
            self.assertEqual({relative: "add" for relative in expected_additions}, {
                relative: actions[relative] for relative in expected_additions
            })
            apply_changes(target, upgrade, upgrade_lock, allow_updates=True)

            orientation_after = {
                path.relative_to(orientation).as_posix(): path.read_bytes()
                for path in orientation.rglob("*")
                if path.is_file()
            }
            self.assertEqual(orientation_before, orientation_after)
            lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
            self.assertTrue(all(lock["files"][relative]["mode"] == "managed" for relative in expected_additions))

    def test_standard_upgrade_reports_customized_skills_without_overwriting_them(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            changes, old_lock = plan_install(target, project_name="Agentic Fixture", mode="init")
            apply_changes(target, changes, old_lock, allow_updates=False)
            customized_files = {}
            for relative in (
                ".agents/skills/harness-orient/SKILL.md",
                ".agents/skills/harness-operator-brief/scripts/check_brief.py",
                ".claude/skills/harness-orient/SKILL.md",
            ):
                destination = target / relative
                customized = destination.read_bytes() + b"\nRepository-owned customization.\n"
                destination.write_bytes(customized)
                customized_files[relative] = customized

            changes, _ = plan_install(target, project_name=None, mode="upgrade")
            actions = {item.path: item.action for item in changes}
            for relative, customized in customized_files.items():
                self.assertEqual("customized", actions[relative])
                self.assertEqual(customized, (target / relative).read_bytes())

    def test_standard_upgrade_detects_a_customized_technical_communication_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            changes, old_lock = plan_install(target, project_name="Policy Fixture", mode="init")
            apply_changes(target, changes, old_lock, allow_updates=False)
            policy = target / "docs/engineering/TECHNICAL_COMMUNICATION.md"
            customized = policy.read_bytes() + b"\nRepository-owned customization.\n"
            policy.write_bytes(customized)

            changes, _ = plan_install(target, project_name=None, mode="upgrade")
            action = {
                item.path: item.action
                for item in changes
            }["docs/engineering/TECHNICAL_COMMUNICATION.md"]
            self.assertEqual("customized", action)
            self.assertEqual(customized, policy.read_bytes())
            checks = {item.name: item for item in inspect_installation(target)}
            self.assertFalse(checks["managed:docs/engineering/TECHNICAL_COMMUNICATION.md"].passed)

    # The fifteen managed paths of the three skills 0.11.0 retired from the
    # 0.10.0 template; the SPEC-DST-022 DST-UPR-007 conformance pair.
    RETIRED_0_10_0_SKILL_PATHS = (
        ".agents/skills/harness-draft-change/SKILL.md",
        ".agents/skills/harness-draft-change/agents/openai.yaml",
        ".agents/skills/harness-draft-change/scripts/guard.py",
        ".agents/skills/harness-draft-change/skill-contract.json",
        ".agents/skills/harness-execute-work-order/SKILL.md",
        ".agents/skills/harness-execute-work-order/agents/openai.yaml",
        ".agents/skills/harness-execute-work-order/scripts/check_scope.py",
        ".agents/skills/harness-execute-work-order/skill-contract.json",
        ".agents/skills/harness-prepare-assurance/SKILL.md",
        ".agents/skills/harness-prepare-assurance/agents/openai.yaml",
        ".agents/skills/harness-prepare-assurance/scripts/check_prepare.py",
        ".agents/skills/harness-prepare-assurance/skill-contract.json",
        ".claude/skills/harness-draft-change/SKILL.md",
        ".claude/skills/harness-execute-work-order/SKILL.md",
        ".claude/skills/harness-prepare-assurance/SKILL.md",
    )

    def install_root_with_leaving_set_paths(self, target: Path) -> dict[str, bytes]:
        changes, old_lock = plan_install(target, project_name="Leaving Set", mode="init")
        apply_changes(target, changes, old_lock, allow_updates=False)
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        planted: dict[str, bytes] = {}
        for relative in self.RETIRED_0_10_0_SKILL_PATHS:
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            content = f"retired 0.10.0 managed content: {relative}\n".encode("utf-8")
            path.write_bytes(content)
            lock["files"][relative] = {"mode": "managed", "sha256": canonical_sha256(content)}
            planted[relative] = content
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return planted

    def test_standard_upgrade_removes_managed_files_that_left_the_managed_set(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            self.install_root_with_leaving_set_paths(target)

            changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
            actions = {item.path: item.action for item in changes}
            self.assertEqual(
                {relative: "remove" for relative in self.RETIRED_0_10_0_SKILL_PATHS},
                {relative: actions[relative] for relative in self.RETIRED_0_10_0_SKILL_PATHS},
            )
            apply_changes(target, changes, old_lock, allow_updates=True)

            for relative in self.RETIRED_0_10_0_SKILL_PATHS:
                self.assertFalse((target / relative).exists(), relative)
            for retired_directory in (
                ".agents/skills/harness-draft-change",
                ".agents/skills/harness-execute-work-order",
                ".agents/skills/harness-prepare-assurance",
                ".claude/skills/harness-draft-change",
            ):
                self.assertFalse((target / retired_directory).exists(), retired_directory)
            self.assertTrue((target / ".agents/skills/harness-orient/SKILL.md").is_file())

            lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
            self.assertFalse(set(self.RETIRED_0_10_0_SKILL_PATHS) & set(lock["files"]))
            replay, _ = plan_install(target, project_name=None, mode="upgrade")
            self.assertEqual({"unchanged"}, {item.action for item in replay})

    def test_standard_upgrade_reports_a_customized_leaving_set_copy_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            planted = self.install_root_with_leaving_set_paths(target)
            edited = ".agents/skills/harness-execute-work-order/SKILL.md"
            customized = planted[edited] + b"\nRepository-owned customization.\n"
            (target / edited).write_bytes(customized)

            changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
            actions = {item.path: item.action for item in changes}
            self.assertEqual("customized", actions[edited])
            with self.assertRaisesRegex(HarnessError, "conflicts or customizations"):
                apply_changes(target, changes, old_lock, allow_updates=True)
            self.assertEqual(customized, (target / edited).read_bytes())
            for relative, content in planted.items():
                if relative != edited:
                    self.assertEqual(content, (target / relative).read_bytes())

    def test_standard_upgrade_retires_seed_and_missing_leaving_set_entries_silently(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            changes, old_lock = plan_install(target, project_name="Leaving Set", mode="init")
            apply_changes(target, changes, old_lock, allow_updates=False)
            lock_path = target / ".engineering-harness.lock"
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            seed_relative = "docs/notes/legacy-seed-note.md"
            seed_content = b"Owner-owned seed content.\n"
            (target / seed_relative).parent.mkdir(parents=True, exist_ok=True)
            (target / seed_relative).write_bytes(seed_content)
            lock["files"][seed_relative] = {"mode": "seed", "state": "present"}
            missing_relative = "docs/legacy/retired-and-deleted.md"
            lock["files"][missing_relative] = {"mode": "managed", "sha256": canonical_sha256(b"gone\n")}
            lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
            actions = {item.path: item.action for item in changes}
            self.assertNotIn(seed_relative, actions)
            self.assertNotIn(missing_relative, actions)
            apply_changes(target, changes, old_lock, allow_updates=True)
            self.assertEqual(seed_content, (target / seed_relative).read_bytes())
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            self.assertNotIn(seed_relative, lock["files"])
            self.assertNotIn(missing_relative, lock["files"])

    def test_standard_upgrade_removes_a_leaving_set_fragment_block_preserving_owner_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            changes, old_lock = plan_install(target, project_name="Leaving Set", mode="init")
            apply_changes(target, changes, old_lock, allow_updates=False)
            lock_path = target / ".engineering-harness.lock"
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            block = b"<!-- se-harness:begin -->\nRetired fragment body.\n<!-- se-harness:end -->\n"
            owner_remainder = b"# Owner heading\n\nOwner prose that must survive.\n\n"
            mixed_relative = "LEGACY_POLICY.md"
            (target / mixed_relative).write_bytes(owner_remainder + block)
            block_only_relative = "LEGACY_BLOCK_ONLY.md"
            (target / block_only_relative).write_bytes(block)
            for relative in (mixed_relative, block_only_relative):
                tracked = tracked_content("fragment", (target / relative).read_bytes())
                assert tracked is not None
                lock["files"][relative] = {"mode": "fragment", "sha256": canonical_sha256(tracked)}
            lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
            actions = {item.path: item.action for item in changes}
            self.assertEqual("remove", actions[mixed_relative])
            self.assertEqual("remove", actions[block_only_relative])
            apply_changes(target, changes, old_lock, allow_updates=True)
            self.assertEqual(owner_remainder, (target / mixed_relative).read_bytes())
            self.assertFalse((target / block_only_relative).exists())
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            self.assertNotIn(mixed_relative, lock["files"])
            self.assertNotIn(block_only_relative, lock["files"])

    def test_standard_upgrade_records_remove_actions_in_transaction_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            self.install_root_with_leaving_set_paths(target)
            changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
            evidence_relative = Path("docs/engineering/harness-distribution/evidence/upgrade-transition.json")
            apply_changes(target, changes, old_lock, allow_updates=True, evidence_output=evidence_relative)
            evidence = json.loads((target / evidence_relative).read_text(encoding="utf-8"))
            self.assertEqual("se-harness-evaluator-upgrade-evidence-v1", evidence["schema"])
            recorded = {item["path"]: item["action"] for item in evidence["plan"]}
            self.assertEqual(
                {relative: "remove" for relative in self.RETIRED_0_10_0_SKILL_PATHS},
                {relative: recorded[relative] for relative in self.RETIRED_0_10_0_SKILL_PATHS},
            )

    def test_standard_upgrade_restores_removed_files_after_interrupted_apply(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            self.install_root_with_leaving_set_paths(target)
            changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
            before = {
                path.relative_to(target).as_posix(): path.read_bytes()
                for path in target.rglob("*")
                if path.is_file()
            }
            real_replace = os.replace
            failed = False

            def interrupt_lock_write(source: str | bytes | os.PathLike[str] | os.PathLike[bytes], destination: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> None:
                nonlocal failed
                if not failed and Path(destination).name == ".engineering-harness.lock":
                    failed = True
                    raise OSError("injected transaction interruption")
                real_replace(source, destination)

            with mock.patch("se_harness.installer.os.replace", side_effect=interrupt_lock_write):
                with self.assertRaisesRegex(OSError, "injected transaction interruption"):
                    apply_changes(target, changes, old_lock, allow_updates=True)
            after = {
                path.relative_to(target).as_posix(): path.read_bytes()
                for path in target.rglob("*")
                if path.is_file()
            }
            self.assertEqual(before, after)

    def test_alpha_can_convert_legacy_controls_in_a_disposable_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            changes, old_lock = plan_install(target, project_name="se_harness", mode="init")
            apply_changes(target, changes, old_lock, allow_updates=False)

            legacy_paths = (
                ".engineering-harness.toml",
                ".github/workflows/engineering-harness.yml",
            )
            legacy_bytes = {
                ".engineering-harness.toml": (
                    "[harness]\n"
                    "schema = 2\n"
                    "tool_version = \"0.4.1\"\n"
                    "installed_at = \"2026-01-01T00:00:00Z\"\n"
                    "project_name = \"se_harness\"\n"
                    "artifact_root = \"docs/engineering\"\n\n"
                    "[dashboard]\n"
                    "output = \"docs/engineering/dashboard\"\n\n"
                    "[self_hosting]\n"
                    "enabled = true\n"
                    "governor_version = \"0.3.0\"\n"
                    "governor_descriptor = \".self-hosting/governor.toml\"\n"
                ).encode(),
                ".github/workflows/engineering-harness.yml": (
                    "name: Legacy engineering harness\n"
                    "on: [push]\n"
                    "permissions:\n"
                    "  contents: read\n"
                    "jobs:\n"
                    "  legacy-governor:\n"
                    "    runs-on: ubuntu-latest\n"
                    "    steps:\n"
                    "      - run: echo legacy\n"
                ).encode(),
            }
            lock_path = target / ".engineering-harness.lock"
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            for relative in legacy_paths:
                destination = target / relative
                destination.write_bytes(legacy_bytes[relative])
                lock["files"][relative]["sha256"] = canonical_sha256(destination.read_bytes())
            lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            descriptor = target / ".self-hosting/governor.toml"
            descriptor.parent.mkdir(parents=True)
            descriptor.write_text(
                "schema = 1\n"
                "governor_version = \"0.3.0\"\n"
                "governor_python = \"python3\"\n"
                "governor_module = \"se_harness\"\n"
                "governor_workflow = \".github/workflows/self-hosting-governor.yml\"\n"
                "governor_template = \"self_hosting/engineering-harness.yml.tpl\"\n"
                "migration_metadata = \"self_hosting/governor-migration.toml\"\n"
                "active_config = \".engineering-harness.toml\"\n"
                "active_lock = \".engineering-harness.lock\"\n"
                "active_workflow = \".github/workflows/engineering-harness.yml\"\n",
                encoding="utf-8",
            )

            changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
            actions = {item.path: item.action for item in changes}
            self.assertEqual(
                {relative: "update" for relative in legacy_paths},
                {relative: actions[relative] for relative in legacy_paths},
            )
            apply_changes(target, changes, old_lock, allow_updates=True)
            descriptor.unlink()

            config = tomllib.loads((target / ".engineering-harness.toml").read_text(encoding="utf-8"))
            self.assertNotIn("self_hosting", config)
            self.assertEqual(__version__, config["harness"]["tool_version"])
            workflow = (target / ".github/workflows/engineering-harness.yml").read_text(encoding="utf-8")
            self.assertEqual(1, workflow.count(f'SE_HARNESS_VERSION: "{__version__}"'))
            self.assertNotIn("self-hosting-governor", workflow)
            self.assertEqual([], [item for item in inspect_installation(target) if not item.passed])

    def test_candidate_evidence_is_repository_owned_and_non_authoritative(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github/workflows/candidate-evidence.yml").read_text(encoding="utf-8")
        self.assertRegex(workflow, r"(?m)^  candidate-source:$")
        self.assertRegex(workflow, r"(?m)^  candidate-package:$")
        self.assertRegex(workflow, r"(?m)^  governance-migration:$")
        # WO-CIP-001 folded the reconcile-only job into a step on job outputs
        self.assertNotIn("governance-migration-reconcile", workflow)
        self.assertEqual(3, workflow.count("actions/checkout@v4"))
        self.assertEqual(3, workflow.count("fetch-depth: 0"))
        self.assertEqual(3, workflow.count("persist-credentials: false"))
        self.assertRegex(workflow, r"(?s)candidate-package:.*?needs: candidate-source")
        self.assertRegex(workflow, r"(?s)governance-migration:.*?needs: \[candidate-source, candidate-package\]")
        self.assertIn("needs.governance-migration.outputs.Linux", workflow)
        self.assertIn("git archive \"$GITHUB_SHA\"", workflow)
        self.assertIn("non-promotable candidate wheel", workflow)
        self.assertIn("python scripts/run_tests.py --workers 4 --scale full", workflow)  # WO-TST-001
        self.assertIn("qualify complete-candidate", workflow)
        self.assertIn("--candidate-commit \"$GITHUB_SHA\"", workflow)
        self.assertIn("complete-candidate-qualification", workflow)
        self.assertIn("--role candidate-package", workflow)
        self.assertIn("--role released-evaluator", workflow)
        self.assertIn("accept-candidate", workflow)
        self.assertIn("se-harness-functional-acceptance-v1", workflow)
        # WO-CIP-003: the predecessor facts are derived, not restated; the values
        # the lock and the legacy contract table yield are asserted in
        # tests/test_ci_pipeline.py.
        self.assertIn("candidate-package-legacy-bootstrap-${{ needs.candidate-source.outputs.predecessor_version }}", workflow)
        self.assertIn("repository_tools.evaluator_facts derive", workflow)
        self.assertNotIn("2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7", workflow)
        self.assertIn('assert "independence" not in value', workflow)
        self.assertIn("check_portable_release_surface.py --repository .", workflow)
        self.assertIn("--require-isolated-python", workflow)
        self.assertIn("repository_tools.upgrade_rehearsal", workflow)  # WO-ECP-010
        self.assertNotIn("rehearse-migration", workflow)
        self.assertIn("windows-latest", workflow)
        self.assertIn("ubuntu-latest", workflow)
        self.assertIn("PREDECESSOR_VERSION: ${{ needs.candidate-source.outputs.predecessor_version }}", workflow)
        self.assertNotIn("MIGRATION_SCENARIO", workflow)
        self.assertNotIn("974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f", workflow)
        self.assertNotIn("historical-0.5.0-to-0.6.0.json", workflow)
        self.assertIn("git diff --exit-code", workflow)
        self.assertNotIn("Review preflight", workflow)
        self.assertNotIn("Validate candidate artifact graph", workflow)
        self.assertNotIn("Validate repository release-distribution policy", workflow)
        self.assertNotIn("pull_request_target", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertNotIn("id-token: write", workflow)
        # WO-REB-027 (SPEC-REB-012 rule 6): the candidate-package operation is
        # selected by the released verifier's capability, never by a restated
        # version; both branches assert the shape of what ran.
        self.assertIn("qualify --help", workflow)
        self.assertIn("qualify candidate-package", workflow)
        self.assertIn('value["independence"] == "released-verifier"', workflow)

    def test_specialized_product_surface_is_absent(self) -> None:
        for relative in (
            ".github/workflows/self-hosting-governor.yml",
            ".self-hosting/governor.toml",
            "se_harness/governor_reconciliation.py",
            "se_harness/self_hosting.py",
            "se_harness/self_hosting_policy.py",
            "self_hosting",
        ):
            with self.subTest(relative=relative):
                self.assertFalse((REPOSITORY_ROOT / relative).exists())
        pyproject = (REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertNotIn("share/se-harness/self-hosting", pyproject)
        completed = subprocess.run(
            [sys.executable, "-m", "se_harness", "--help"],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertNotIn("reconcile-governor", completed.stdout)

    def test_evaluator_evidence_bytes_are_portable_across_git_checkouts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            changes, old_lock = plan_install(target, project_name="Attributes", mode="init")
            apply_changes(target, changes, old_lock, allow_updates=False)
            # WO-HBI-005: the candidate fragment carries only the template-region
            # evaluator-evidence rule; the migration-protocol rules that only this
            # repository can satisfy are no longer shipped to consumers.
            expected_fragment = (
                "# Preserve canonical evaluator-evidence bytes and their bound SHA-256 on every platform.\n"
                "docs/engineering/**/evidence/*.json text eol=lf\n"
            )
            released_fragment = expected_fragment + (
                "# Keep the packaged migration protocol, its hash-bound implementation, and canonical scenarios byte-stable.\n"
                "se_harness/governance_migration*.py text eol=lf\n"
                "se_harness/governance_migration_contract.json text eol=lf\n"
                "tests/fixtures/governance_migration/*.json text eol=lf\n"
            )
            self.assertEqual(
                expected_fragment,
                (REPOSITORY_ROOT / "templates/repository/standard/gitattributes.fragment")
                .read_text(encoding="utf-8"),
            )
            attributes = (target / ".gitattributes").read_text(encoding="utf-8")
            self.assertEqual(
                "# se-harness:begin\n" + expected_fragment + "# se-harness:end\n",
                attributes,
            )
            root_attributes_path = REPOSITORY_ROOT / ".gitattributes"
            root_attributes = root_attributes_path.read_text(encoding="utf-8")
            self.assertNotEqual(attributes, root_attributes)
            root_managed = root_attributes.split("# se-harness:begin\n", 1)[1].split(
                "# se-harness:end\n", 1
            )[0]
            # The root managed block is the released evaluator's fragment and is
            # hash-locked. Under the 0.7.1 root (WO-HUP-007) it still carried the
            # migration rules; since WO-HUP-008 adopted 0.8.0 it is the candidate
            # fragment. The owner region keeps its copies until issue #210's follow-up
            # deletes the retired stage machine under its own work order.
            root_version = json.loads(
                (REPOSITORY_ROOT / ".engineering-harness.lock").read_text(encoding="utf-8")
            )["evaluator"]["version"]
            self.assertEqual(
                released_fragment if root_version == "0.7.1" else expected_fragment, root_managed
            )
            root_owner = root_attributes.split("# se-harness:end\n", 1)[1]
            for rule in (
                "se_harness/governance_migration*.py text eol=lf",
                "se_harness/governance_migration_contract.json text eol=lf",
                "tests/fixtures/governance_migration/*.json text eol=lf",
            ):
                # Under the 0.7.1 root the owner region had to carry the migration
                # rules; WO-ECP-011 deleted them with the stage machine once the root
                # advanced (WO-HUP-008).
                (self.assertIn if root_version == "0.7.1" else self.assertNotIn)(rule, root_owner)
            root_lock = json.loads(
                (REPOSITORY_ROOT / ".engineering-harness.lock").read_text(encoding="utf-8")
            )
            self.assertEqual(
                root_lock["files"][".gitattributes"]["sha256"],
                canonical_sha256(tracked_content("fragment", root_attributes_path.read_bytes())),
            )
            lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
            self.assertEqual("fragment", lock["files"][".gitattributes"]["mode"])
            evidence_relative = "docs/engineering/product/evidence/RLS-TST-001-evaluator.json"
            subprocess.run(
                ["git", "-C", str(target), "init"],
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(target), "config", "user.name", "Harness Test"],
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(target), "config", "user.email", "harness@example.invalid"],
                capture_output=True,
                text=True,
                check=True,
            )
            evidence = target / evidence_relative
            evidence.parent.mkdir(parents=True, exist_ok=True)
            evidence_bytes = b'{"schema":"se-harness-evaluator-evidence-v1"}\n'
            evidence.write_bytes(evidence_bytes)
            subprocess.run(
                ["git", "-C", str(target), "-c", "core.autocrlf=false", "add", "."],
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(target), "commit", "-m", "canonical evidence"],
                capture_output=True,
                text=True,
                check=True,
            )

            isolated_git = os.environ.copy()
            isolated_git["GIT_CONFIG_NOSYSTEM"] = "1"
            isolated_git["GIT_CONFIG_GLOBAL"] = str(Path(temporary) / "empty.gitconfig")
            Path(isolated_git["GIT_CONFIG_GLOBAL"]).write_text("", encoding="utf-8")
            expected_digest = hashlib.sha256(evidence_bytes).hexdigest()
            for autocrlf, eol in (("true", "crlf"), ("input", "crlf"), ("false", "crlf")):
                clone = Path(temporary) / f"clone-{autocrlf}"
                subprocess.run(
                    [
                        "git",
                        "-c",
                        "protocol.file.allow=always",
                        "clone",
                        "-c",
                        f"core.autocrlf={autocrlf}",
                        "-c",
                        f"core.eol={eol}",
                        "--no-local",
                        str(target),
                        str(clone),
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                    env=isolated_git,
                )
                checked_out = (clone / evidence_relative).read_bytes()
                self.assertEqual(evidence_bytes, checked_out)
                self.assertEqual(expected_digest, hashlib.sha256(checked_out).hexdigest())
                completed = subprocess.run(
                    ["git", "-C", str(clone), "check-attr", "text", "eol", "--", evidence_relative],
                    capture_output=True,
                    text=True,
                    check=True,
                    env=isolated_git,
                )
                self.assertEqual("", completed.stderr)
                self.assertIn(f"{evidence_relative}: text: set", completed.stdout)
                self.assertIn(f"{evidence_relative}: eol: lf", completed.stdout)

            conflict = Path(temporary) / "clone-true"
            (conflict / Path(evidence_relative).parent / ".gitattributes").write_text(
                "*.json eol=crlf\n", encoding="utf-8", newline="\n"
            )
            completed = subprocess.run(
                ["git", "-C", str(conflict), "check-attr", "eol", "--", evidence_relative],
                capture_output=True,
                text=True,
                check=True,
                env=isolated_git,
            )
            self.assertIn(f"{evidence_relative}: eol: crlf", completed.stdout)

    def test_standard_upgrade_restores_every_file_after_interrupted_apply(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repository"
            changes, old_lock = plan_install(target, project_name="Transaction", mode="init")
            apply_changes(target, changes, old_lock, allow_updates=False)

            lock_path = target / ".engineering-harness.lock"
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            managed = (
                "ENGINEERING_HARNESS.md",
                "docs/engineering/QUALITY_GATES.md",
                ".agents/skills/harness-orient/SKILL.md",
                ".agents/skills/harness-operator-brief/skill-contract.json",
            )
            for relative in managed:
                path = target / relative
                path.write_bytes(path.read_bytes() + b"\nLegacy released content.\n")
                lock["files"][relative]["sha256"] = canonical_sha256(path.read_bytes())
            lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
            actions = {item.path: item.action for item in changes}
            self.assertEqual({relative: "update" for relative in managed}, {relative: actions[relative] for relative in managed})
            before = {
                path.relative_to(target).as_posix(): path.read_bytes()
                for path in target.rglob("*")
                if path.is_file()
            }
            real_replace = os.replace
            failed = False

            def interrupt_once(source: str | bytes | os.PathLike[str] | os.PathLike[bytes], destination: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> None:
                nonlocal failed
                if not failed and Path(destination).name == "QUALITY_GATES.md":
                    failed = True
                    raise OSError("injected transaction interruption")
                real_replace(source, destination)

            with mock.patch("se_harness.installer.os.replace", side_effect=interrupt_once):
                with self.assertRaisesRegex(OSError, "injected transaction interruption"):
                    apply_changes(target, changes, old_lock, allow_updates=True)

            after = {
                path.relative_to(target).as_posix(): path.read_bytes()
                for path in target.rglob("*")
                if path.is_file()
            }
            self.assertEqual(before, after)

    def test_candidate_source_identity_is_deterministic_and_bounded(self) -> None:
        commit = "a" * 40
        with mock.patch.dict(os.environ, {"EXAMPLE_SECRET_TOKEN": "must-not-appear"}, clear=True), mock.patch(
            "se_harness.runtime_identity.site.ENABLE_USER_SITE", False
        ), mock.patch(
            "se_harness.runtime_identity._distribution_root", return_value=REPOSITORY_ROOT
        ):
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
        self.assertTrue(_lexically_within(environment / "bin/python", environment))
        self.assertFalse(_lexically_within(Path("/opt/python/bin/python3.11"), environment))

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
            "se_harness.runtime_identity._distribution_root", return_value=Path(temporary)
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

    def test_released_evaluator_rejects_inherited_pythonpath(self) -> None:
        with mock.patch.dict(os.environ, {"PYTHONPATH": str(REPOSITORY_ROOT)}):
            identity = inspect_runtime_identity(
                role="released-evaluator",
                expected_version=__version__,
                expected_root=Path(sys.prefix),
                checkout_root=REPOSITORY_ROOT,
                evaluator_wheel_sha256="c" * 64,
            )
        self.assertIn("RID008", {item.code for item in identity.diagnostics})

    def test_candidate_identity_cannot_claim_released_evaluator_digest(self) -> None:
        identity = inspect_runtime_identity(
            role="candidate-source",
            expected_version=__version__,
            expected_root=REPOSITORY_ROOT,
            checkout_root=REPOSITORY_ROOT,
            candidate_commit="f" * 40,
            evaluator_wheel_sha256="a" * 64,
        )
        self.assertIn("RID016", {item.code for item in identity.diagnostics})

    def test_path_containment_is_component_aware(self) -> None:
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
            candidate_version="0.4.1",
            candidate_commit="b" * 40,
            candidate_wheel_sha256="c" * 64,
            python_version="3.11.0",
            scenarios=scenarios,
        )
        parsed = json.loads(manifest.canonical_bytes())
        self.assertEqual(list(SCENARIO_IDS), [item["scenario_id"] for item in parsed["scenarios"]])
        self.assertEqual(CONTRACT_SHA256, parsed["verifier"]["contract_sha256"])

    def test_acceptance_normalizes_json_escaped_temporary_paths(self) -> None:
        from se_harness.candidate_acceptance import _normalize

        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            first = parent / "first"
            second = parent / "second"
            first_value = json.dumps({"path": str(first / "candidate-env" / "python")})
            second_value = json.dumps({"path": str(second / "candidate-env" / "python")})
            self.assertEqual(
                _normalize(first_value, first, first / "candidate.whl", None),
                _normalize(second_value, second, second / "candidate.whl", None),
            )

    def test_candidate_checkout_cannot_supply_released_acceptance_runner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            wheel, digest = self.make_candidate_wheel(Path(temporary))
            with self.assertRaisesRegex(HarnessError, "checkout cannot supply"):
                assess_candidate_wheel(
                    wheel,
                    candidate_commit="b" * 40,
                    candidate_wheel_sha256=digest,
                    verifier_wheel_sha256="a" * 64,
                    checkout_root=REPOSITORY_ROOT,
                )

    def test_candidate_acceptance_requires_the_selected_wheel_digest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            wheel, _ = self.make_candidate_wheel(Path(temporary))
            with self.assertRaisesRegex(HarnessError, "candidate wheel SHA-256 mismatch"):
                assess_candidate_wheel(
                    wheel,
                    candidate_commit="b" * 40,
                    candidate_wheel_sha256="0" * 64,
                    verifier_wheel_sha256="a" * 64,
                )

    def test_checkout_snapshot_is_bounded(self) -> None:
        from se_harness.candidate_acceptance import _snapshot

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "one").write_text("1", encoding="utf-8")
            with mock.patch("se_harness.candidate_acceptance.MAX_SNAPSHOT_FILES", 0):
                with self.assertRaisesRegex(HarnessError, "bounded file count"):
                    _snapshot(root)

    def test_failed_pr_records_are_excluded_from_recovery_candidate(self) -> None:
        for relative in FAILED_PR_RECORDS:
            with self.subTest(relative=relative):
                self.assertFalse((REPOSITORY_ROOT / relative).exists())


if __name__ == "__main__":
    unittest.main()
