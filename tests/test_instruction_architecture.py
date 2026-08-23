from __future__ import annotations

import contextlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness import __version__
from se_harness.cli import main
from se_harness.installer import BEGIN_MARKER, END_MARKER, plan_install, tracked_content
from se_harness.integrity import HASH_ALGORITHM, HASH_MODE, LOCK_SCHEMA, canonical_sha256
from tests.mutation_guard_support import trusted_mutation_authority


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKET_ROOT = REPOSITORY_ROOT / "docs" / "engineering" / "instruction-architecture"
OLD_ROUTER_PROCEDURE = (
    "After a separately authorized candidate commit contains implementation and evidence, "
    "`harnessctl capture-verification` may prepare a `ready` VREC in a later governance commit. "
    "After accountable assurance review, `harnessctl prepare-release` may prepare a `ready` "
    "release record bound to the same candidate commit. These commands never commit, push, "
    "tag, approve, release, publish, or deploy."
)
ROUTER_INVARIANT_SUMMARY = (
    "`HRN-006` - A transition MUST change only the artifacts explicitly selected by"
)
OLD_REVIEW_PROCEDURE = (
    "Run `harnessctl preflight . --work-order WO-... --phase review` for a completed "
    "pull-request candidate. Generate Harness Explorer with `harnessctl dashboard .` and "
    "open `target/harness-dashboard/index.html`. Both outputs are derived, read-only evidence."
)
ROUTER_REVIEW_SUMMARY = (
    "| Lifecycle states, transitions, procedures, next actions, and handoff fields |"
)
OLD_WORKFLOW_REVIEW_STEP = (
    "6. Retain evidence keyed to every release-bearing work-order ID and run review preflight "
    "with `--phase review`."
)
WORKFLOW_REVIEW_STEP = (
    "6. The implementation actor MUST change only the authorized scope, retain"
)
ROUTER_HANDOFF_HEADING = "## Lifecycle restitution"
WORKFLOW_HANDOFF_HEADING = "## Lifecycle restitution procedure"
HANDOFF_FIELDS = (
    "Outcome",
    "Done",
    "Not done",
    "Blocked by",
    "Current lifecycle state",
    "Decision required",
    "Next",
    "Command or response",
    "Alternatives",
)


class InstructionArchitectureTests(unittest.TestCase):
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

    def installed_target(self, name: str = "target") -> Path:
        target = self.root / name
        code, _, error = self.invoke("init", str(target), "--project-name", "Example")
        self.assertEqual(0, code, error)
        return target

    def add_active_packet(self, target: Path, *, status: str = "in_progress") -> None:
        destination = target / "docs" / "engineering" / "instruction-architecture"
        shutil.copytree(PACKET_ROOT, destination)
        operating_contract = destination / "operations" / "OPS-IAR-001.md"
        text = operating_contract.read_text(encoding="utf-8")
        text = re.sub(r'^status = "[^"]+"$', 'status = "draft"', text, count=1, flags=re.MULTILINE)
        operating_contract.write_text(text, encoding="utf-8")
        work_order = destination / "work-orders" / "WO-IAR-001.md"
        text = work_order.read_text(encoding="utf-8")
        text = re.sub(r'^status = "[^"]+"$', f'status = "{status}"', text, count=1, flags=re.MULTILINE)
        if "[assurance]" not in text:
            text = text.replace(
                "\n[relations]\n",
                "\n[assurance]\n"
                'commit_bound_verification = "required"\n'
                'rationale = "The fixture changes trusted engineering behavior."\n'
                'decided_by = "test-owner"\n\n'
                "[relations]\n",
                1,
            )
        if "[execution_scope]" not in text:
            text = text.replace(
                "\n[relations]\n",
                '\n[execution_scope]\npaths = ["src/"]\n\n[relations]\n',
                1,
            )
        work_order.write_text(text, encoding="utf-8")
        # The copied packet is history; a synthetic active work order needs an active
        # governing chain, so requirements superseded later are restored to implemented.
        for requirement in sorted((destination / "requirements").glob("REQ-*.md")):
            text = requirement.read_text(encoding="utf-8")
            if 'status = "superseded"' in text:
                requirement.write_text(
                    text.replace('status = "superseded"', 'status = "implemented"', 1),
                    encoding="utf-8",
                )

    def test_instruction_route_and_ownership_modes_are_explicit(self) -> None:
        target = self.installed_target()
        agents = (target / "AGENTS.md").read_text(encoding="utf-8")
        managed = agents.split(BEGIN_MARKER, 1)[1].split(END_MARKER, 1)[0]
        self.assertIn("ENGINEERING_HARNESS.md", managed)
        self.assertNotIn("REPOSITORY_CONTEXT.md", managed)
        claude = (target / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertEqual(1, sum(line.strip() == "@AGENTS.md" for line in claude.splitlines()))

        router = (target / "ENGINEERING_HARNESS.md").read_text(encoding="utf-8")
        for name in ("WORKFLOW.md", "DECISION_RIGHTS.md", "QUALITY_GATES.md", "TRACEABILITY.md"):
            self.assertIn(name, router)
        index = (target / "docs" / "engineering" / "README.md").read_text(encoding="utf-8")
        self.assertIn("Repository-owned after installation", index)
        self.assertNotIn("## Workflow", index)

        lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual("fragment", lock["files"]["AGENTS.md"]["mode"])
        self.assertEqual("fragment", lock["files"]["CLAUDE.md"]["mode"])
        self.assertEqual("managed", lock["files"]["ENGINEERING_HARNESS.md"]["mode"])
        self.assertEqual("seed", lock["files"]["docs/engineering/README.md"]["mode"])
        self.assertNotIn("docs/engineering/REPOSITORY_CONTEXT.md", lock["files"])
        self.assertTrue((target / ".github" / "PULL_REQUEST_TEMPLATE.md").is_file())

    def test_inspection_guidance_packet_preserves_the_authority_boundary(self) -> None:
        requirement = (PACKET_ROOT / "requirements" / "REQ-IAR-017.md").read_text(encoding="utf-8")
        specification = (PACKET_ROOT / "specifications" / "SPEC-IAR-009.md").read_text(
            encoding="utf-8"
        )
        decision = (PACKET_ROOT / "architecture" / "adr" / "ADR-IAR-009.md").read_text(
            encoding="utf-8"
        )
        work_order = (PACKET_ROOT / "work-orders" / "WO-IAR-009.md").read_text(
            encoding="utf-8"
        )
        baseline = (PACKET_ROOT / "requirements" / "REQ-IAR-016.md").read_text(
            encoding="utf-8"
        )

        self.assertIn('status = "implemented"', requirement)
        self.assertIn('status = "implemented"', specification)
        self.assertIn('status = "approved"', decision)
        self.assertIn(
            'status = "implemented"',
            (PACKET_ROOT / "architecture" / "ARCH-IAR-009.md").read_text(encoding="utf-8"),
        )
        self.assertIn('status = "implemented"', work_order)
        self.assertIn("automatic = false", requirement)
        self.assertIn("closed catalog", specification.lower())
        self.assertIn("unknown rule IDs", specification)
        self.assertIn("Do not include executable commands", decision)
        self.assertIn("free-form recommendation", baseline)

    def test_router_keeps_invariants_while_workflow_owns_ordered_procedure(self) -> None:
        target = self.installed_target()
        router = (target / "ENGINEERING_HARNESS.md").read_text(encoding="utf-8")
        workflow = (target / "docs" / "engineering" / "WORKFLOW.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(ROUTER_INVARIANT_SUMMARY, router)
        self.assertNotIn(OLD_ROUTER_PROCEDURE, router)
        self.assertNotIn("capture-verification", router)
        for required in (
            "`WFL-WO-PREPARE-VREC`",
            "`WFL-VREC-DECIDE`",
            "`WFL-RLS-DECIDE`",
            "A VREC decision MUST NOT change a referenced work order",
            "Release status performs no external action",
        ):
            self.assertIn(required, workflow)

    def test_stage_aware_handoffs_preserve_authority_and_policy_ownership(self) -> None:
        target = self.installed_target()
        agents = (target / "AGENTS.md").read_text(encoding="utf-8")
        managed = agents.split(BEGIN_MARKER, 1)[1].split(END_MARKER, 1)[0]
        router = (target / "ENGINEERING_HARNESS.md").read_text(encoding="utf-8")
        workflow = (target / "docs" / "engineering" / "WORKFLOW.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(ROUTER_HANDOFF_HEADING, router)
        router_handoff = router.split(ROUTER_HANDOFF_HEADING, 1)[1].split("\n## ", 1)[0]
        normalized_router_handoff = " ".join(router_handoff.split())
        for field in HANDOFF_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, normalized_router_handoff)
        self.assertIn("actual artifact IDs", normalized_router_handoff)
        self.assertIn("preserve every stated non-effect", normalized_router_handoff)
        self.assertIn("WORKFLOW.md", router_handoff)
        self.assertNotIn("--phase review", router_handoff)
        self.assertNotIn("capture-verification", router_handoff)
        self.assertNotIn("Current lifecycle state", managed)

        self.assertIn(WORKFLOW_HANDOFF_HEADING, workflow)
        workflow_handoff = workflow.split(WORKFLOW_HANDOFF_HEADING, 1)[1]
        for phrase in (
            "`Outcome`",
            "`Done`",
            "`Not done`",
            "`Blocked by`",
            "`Current lifecycle state`",
            "`Decision required`",
            "`Next`",
            "`Command or response`",
            "`Alternatives`",
            "actual artifact IDs",
            "exactly one current typed procedure step",
            "open-ended question",
            "unchanged state",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, workflow_handoff)

    def test_stage_aware_handoff_upgrade_is_safe_and_idempotent(self) -> None:
        target = self.installed_target("prior-handoff")
        router_path = target / "ENGINEERING_HARNESS.md"
        workflow_path = target / "docs" / "engineering" / "WORKFLOW.md"
        desired_router = router_path.read_text(encoding="utf-8")
        desired_workflow = workflow_path.read_text(encoding="utf-8")
        router_parts = desired_router.split(f"\n{ROUTER_HANDOFF_HEADING}\n", 1)
        workflow_parts = desired_workflow.split(f"\n{WORKFLOW_HANDOFF_HEADING}\n", 1)
        self.assertEqual(2, len(router_parts))
        self.assertEqual(2, len(workflow_parts))
        _, next_router_section = router_parts[1].split("\n## ", 1)
        prior_router = router_parts[0] + "\n## " + next_router_section
        prior_workflow = workflow_parts[0] + "\n"
        self.assertNotEqual(desired_router, prior_router)
        self.assertNotEqual(desired_workflow, prior_workflow)
        router_path.write_text(prior_router, encoding="utf-8")
        workflow_path.write_text(prior_workflow, encoding="utf-8")
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"]["ENGINEERING_HARNESS.md"]["sha256"] = canonical_sha256(
            prior_router.encode("utf-8")
        )
        lock["files"]["docs/engineering/WORKFLOW.md"]["sha256"] = canonical_sha256(
            prior_workflow.encode("utf-8")
        )
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        code, output, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertIn("update     ENGINEERING_HARNESS.md", output)
        self.assertIn("update     docs/engineering/WORKFLOW.md", output)
        self.assertEqual(desired_router, router_path.read_text(encoding="utf-8"))
        self.assertEqual(desired_workflow, workflow_path.read_text(encoding="utf-8"))
        first_lock = lock_path.read_bytes()
        self.assertEqual(0, self.invoke("upgrade", str(target), "--apply")[0])
        self.assertEqual(first_lock, lock_path.read_bytes())

    def test_router_responsibility_refinement_upgrades_safely(self) -> None:
        target = self.installed_target("prior-router")
        router_path = target / "ENGINEERING_HARNESS.md"
        current = router_path.read_text(encoding="utf-8")
        prior = current.replace(ROUTER_INVARIANT_SUMMARY, OLD_ROUTER_PROCEDURE)
        self.assertNotEqual(current, prior)
        router_path.write_text(prior, encoding="utf-8")
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"]["ENGINEERING_HARNESS.md"]["sha256"] = canonical_sha256(
            prior.encode("utf-8")
        )
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        code, output, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertIn("update     ENGINEERING_HARNESS.md", output)
        self.assertEqual(current, router_path.read_text(encoding="utf-8"))
        first_lock = lock_path.read_bytes()
        self.assertEqual(0, self.invoke("upgrade", str(target), "--apply")[0])
        self.assertEqual(current, router_path.read_text(encoding="utf-8"))
        self.assertEqual(first_lock, lock_path.read_bytes())

        customized = self.installed_target("customized-router")
        customized_router = customized / "ENGINEERING_HARNESS.md"
        desired = customized_router.read_text(encoding="utf-8")
        prior = desired.replace(ROUTER_INVARIANT_SUMMARY, OLD_ROUTER_PROCEDURE)
        customized_content = prior + "\nRepository-local edit inside managed content.\n"
        customized_router.write_text(customized_content, encoding="utf-8")
        customized_lock_path = customized / ".engineering-harness.lock"
        customized_lock = json.loads(customized_lock_path.read_text(encoding="utf-8"))
        customized_lock["files"]["ENGINEERING_HARNESS.md"]["sha256"] = canonical_sha256(
            prior.encode("utf-8")
        )
        customized_lock_path.write_text(
            json.dumps(customized_lock, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        original_router = customized_router.read_bytes()
        original_lock = customized_lock_path.read_bytes()

        code, output, error = self.invoke("upgrade", str(customized), "--apply")
        self.assertEqual(1, code)
        self.assertIn("customized ENGINEERING_HARNESS.md", output)
        self.assertIn("no files were written", error)
        self.assertEqual(original_router, customized_router.read_bytes())
        self.assertEqual(original_lock, customized_lock_path.read_bytes())

    def test_workflow_owns_review_and_visualization_procedure(self) -> None:
        target = self.installed_target()
        router = (target / "ENGINEERING_HARNESS.md").read_text(encoding="utf-8")
        workflow = (target / "docs" / "engineering" / "WORKFLOW.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(ROUTER_REVIEW_SUMMARY, router)
        self.assertNotIn(OLD_REVIEW_PROCEDURE, router)
        review_section = router.split("## Routing", 1)[1].split("\n## ", 1)[0]
        self.assertNotIn("--phase review", review_section)
        self.assertNotIn("harnessctl dashboard .", review_section)
        self.assertIn(WORKFLOW_REVIEW_STEP, workflow)
        self.assertNotIn(OLD_WORKFLOW_REVIEW_STEP, workflow)

    def test_review_routing_upgrade_is_transactional_and_idempotent(self) -> None:
        target = self.installed_target("prior-review-routing")
        router_path = target / "ENGINEERING_HARNESS.md"
        workflow_path = target / "docs" / "engineering" / "WORKFLOW.md"
        desired_router = router_path.read_text(encoding="utf-8")
        desired_workflow = workflow_path.read_text(encoding="utf-8")
        prior_router = desired_router.replace(ROUTER_REVIEW_SUMMARY, OLD_REVIEW_PROCEDURE)
        prior_workflow = desired_workflow.replace(WORKFLOW_REVIEW_STEP, OLD_WORKFLOW_REVIEW_STEP)
        self.assertNotEqual(desired_router, prior_router)
        self.assertNotEqual(desired_workflow, prior_workflow)
        router_path.write_text(prior_router, encoding="utf-8")
        workflow_path.write_text(prior_workflow, encoding="utf-8")
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"]["ENGINEERING_HARNESS.md"]["sha256"] = canonical_sha256(
            prior_router.encode("utf-8")
        )
        lock["files"]["docs/engineering/WORKFLOW.md"]["sha256"] = canonical_sha256(
            prior_workflow.encode("utf-8")
        )
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        code, output, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertIn("update     ENGINEERING_HARNESS.md", output)
        self.assertIn("update     docs/engineering/WORKFLOW.md", output)
        self.assertEqual(desired_router, router_path.read_text(encoding="utf-8"))
        self.assertEqual(desired_workflow, workflow_path.read_text(encoding="utf-8"))
        first_lock = lock_path.read_bytes()
        self.assertEqual(0, self.invoke("upgrade", str(target), "--apply")[0])
        self.assertEqual(first_lock, lock_path.read_bytes())

        customized = self.installed_target("customized-review-routing")
        customized_router = customized / "ENGINEERING_HARNESS.md"
        customized_workflow = customized / "docs" / "engineering" / "WORKFLOW.md"
        desired_router = customized_router.read_text(encoding="utf-8")
        desired_workflow = customized_workflow.read_text(encoding="utf-8")
        prior_router = desired_router.replace(ROUTER_REVIEW_SUMMARY, OLD_REVIEW_PROCEDURE)
        prior_workflow = desired_workflow.replace(WORKFLOW_REVIEW_STEP, OLD_WORKFLOW_REVIEW_STEP)
        customized_router.write_text(prior_router, encoding="utf-8")
        customized_workflow.write_text(
            prior_workflow + "\nRepository-local edit inside managed workflow.\n",
            encoding="utf-8",
        )
        customized_lock_path = customized / ".engineering-harness.lock"
        customized_lock = json.loads(customized_lock_path.read_text(encoding="utf-8"))
        customized_lock["files"]["ENGINEERING_HARNESS.md"]["sha256"] = canonical_sha256(
            prior_router.encode("utf-8")
        )
        customized_lock["files"]["docs/engineering/WORKFLOW.md"]["sha256"] = canonical_sha256(
            prior_workflow.encode("utf-8")
        )
        customized_lock_path.write_text(
            json.dumps(customized_lock, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        original_router = customized_router.read_bytes()
        original_workflow = customized_workflow.read_bytes()
        original_lock = customized_lock_path.read_bytes()

        code, output, error = self.invoke("upgrade", str(customized), "--apply")
        self.assertEqual(1, code)
        self.assertIn("customized docs/engineering/WORKFLOW.md", output)
        self.assertIn("no files were written", error)
        self.assertEqual(original_router, customized_router.read_bytes())
        self.assertEqual(original_workflow, customized_workflow.read_bytes())
        self.assertEqual(original_lock, customized_lock_path.read_bytes())

    def test_managed_readme_to_seed_migration_is_safe_and_transactional(self) -> None:
        target = self.installed_target("exact")
        readme = target / "docs" / "engineering" / "README.md"
        old_managed = b"# Old managed engineering index\n"
        readme.write_bytes(old_managed)
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"]["docs/engineering/README.md"] = {
            "mode": "managed",
            "sha256": canonical_sha256(old_managed),
        }
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        changes, _ = plan_install(target, project_name=None, mode="upgrade")
        action = {item.path: item.action for item in changes}
        self.assertEqual("update", action["docs/engineering/README.md"])
        code, output, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertIn("update     docs/engineering/README.md", output)
        self.assertIn("Repository-owned after installation", readme.read_text(encoding="utf-8"))
        migrated = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertEqual({"mode": "seed", "state": "present"}, migrated["files"]["docs/engineering/README.md"])
        self.assertEqual(0, self.invoke("upgrade", str(target), "--apply")[0])

        customized = self.installed_target("customized")
        customized_readme = customized / "docs" / "engineering" / "README.md"
        customized_readme.write_bytes(old_managed + b"Owner customization.\n")
        customized_lock_path = customized / ".engineering-harness.lock"
        customized_lock = json.loads(customized_lock_path.read_text(encoding="utf-8"))
        customized_lock["files"]["docs/engineering/README.md"] = {
            "mode": "managed",
            "sha256": canonical_sha256(old_managed),
        }
        customized_lock_path.write_text(
            json.dumps(customized_lock, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        missing = customized / "docs" / "engineering" / "TRACEABILITY.md"
        missing.unlink()
        original_readme = customized_readme.read_bytes()
        original_lock = customized_lock_path.read_bytes()

        code, output, error = self.invoke("upgrade", str(customized), "--apply")
        self.assertEqual(1, code)
        self.assertIn("customized docs/engineering/README.md", output)
        self.assertIn("no files were written", error)
        self.assertEqual(original_readme, customized_readme.read_bytes())
        self.assertEqual(original_lock, customized_lock_path.read_bytes())
        self.assertFalse(missing.exists())

        legacy = self.installed_target("legacy-newlines")
        legacy_readme = legacy / "docs" / "engineering" / "README.md"
        legacy_lf = b"# Legacy managed index\n\nLine two.\n"
        legacy_readme.write_bytes(legacy_lf.replace(b"\n", b"\r\n"))
        legacy_lock_path = legacy / ".engineering-harness.lock"
        legacy_lock = json.loads(legacy_lock_path.read_text(encoding="utf-8"))
        legacy_lock["schema"] = 1
        legacy_lock.pop("hash_algorithm", None)
        legacy_lock.pop("hash_mode", None)
        legacy_lock.pop("evaluator", None)
        legacy_lock["files"]["docs/engineering/README.md"] = {
            "mode": "managed",
            "sha256": canonical_sha256(legacy_lf),
        }
        legacy_lock_path.write_text(
            json.dumps(legacy_lock, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        changes, _ = plan_install(legacy, project_name=None, mode="upgrade")
        self.assertEqual(
            "update",
            {item.path: item.action for item in changes}["docs/engineering/README.md"],
        )

    def test_preflight_returns_deterministic_reading_manifest_without_writes(self) -> None:
        target = self.installed_target()
        self.add_active_packet(target)
        before = {
            path.relative_to(target).as_posix(): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }

        code, output, error = self.invoke(
            "preflight",
            str(target),
            "--work-order",
            "WO-IAR-001",
            "--json",
        )
        self.assertEqual(0, code, error)
        report = json.loads(output)
        self.assertEqual("se-harness-preflight-v2", report["schema"])
        self.assertTrue(report["ready"])
        self.assertEqual("start", report["phase"])
        self.assertEqual("in_progress", report["work_order"]["status"])
        self.assertEqual("required", report["assurance"]["commit_bound_verification"])
        self.assertEqual("test-owner", report["assurance"]["decided_by"])
        self.assertEqual([], report["diagnostics"])
        for path in (
            "ENGINEERING_HARNESS.md",
            "docs/engineering/WORKFLOW.md",
            "docs/engineering/instruction-architecture/intent/INT-IAR-001.md",
            "docs/engineering/instruction-architecture/work-orders/WO-IAR-001.md",
        ):
            self.assertIn(path, report["reading_manifest"])
        self.assertNotIn("repository_commands", report)
        after = {
            path.relative_to(target).as_posix(): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }
        self.assertEqual(before, after)

    def test_preflight_reports_phase_integrity_and_id_failures(self) -> None:
        fresh = self.installed_target("fresh")
        self.add_active_packet(fresh)
        code, output, _ = self.invoke("preflight", str(fresh), "--work-order", "WO-IAR-001")
        self.assertEqual(0, code)
        self.assertIn("Harness preflight: PASS", output)
        self.assertNotIn("[C0", output)

        completed = self.installed_target("completed")
        self.add_active_packet(completed, status="implemented")
        code, output, _ = self.invoke("preflight", str(completed), "--work-order", "WO-IAR-001")
        self.assertEqual(1, code)
        self.assertIn("[W005]", output)
        code, output, error = self.invoke(
            "preflight",
            str(completed),
            "--work-order",
            "WO-IAR-001",
            "--phase",
            "review",
        )
        self.assertEqual(0, code, error)
        self.assertIn("Harness preflight: PASS", output)

        agents = completed / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8").replace(
                "Read `ENGINEERING_HARNESS.md`",
                "Skip `ENGINEERING_HARNESS.md`",
            ),
            encoding="utf-8",
        )
        code, output, _ = self.invoke(
            "preflight",
            str(completed),
            "--work-order",
            "WO-IAR-001",
            "--phase",
            "review",
        )
        self.assertEqual(1, code)
        self.assertIn("[I001] managed:AGENTS.md", output)

        code, output, _ = self.invoke(
            "preflight",
            str(completed),
            "--work-order",
            "WO-IAR-001;echo-pwned",
        )
        self.assertEqual(1, code)
        self.assertIn("[W001]", output)

    def test_preflight_requires_and_projects_explicit_assurance_for_selected_work(self) -> None:
        target = self.installed_target("assurance-preflight")
        self.add_active_packet(target)

        code, output, error = self.invoke(
            "preflight",
            str(target),
            "--work-order",
            "WO-IAR-001",
        )
        self.assertEqual(0, code, error)
        self.assertIn("Assurance classification:", output)
        self.assertIn("Commit-bound verification: required", output)
        self.assertIn("Decided by: test-owner", output)

        work_order = target / "docs/engineering/instruction-architecture/work-orders/WO-IAR-001.md"
        text = work_order.read_text(encoding="utf-8")
        text = re.sub(
            r"\n\[assurance\]\n.*?(?=\n\[relations\]\n)",
            "\n",
            text,
            count=1,
            flags=re.DOTALL,
        )
        work_order.write_text(text, encoding="utf-8")

        code, output, _ = self.invoke(
            "preflight",
            str(target),
            "--work-order",
            "WO-IAR-001",
        )
        self.assertEqual(1, code)
        self.assertIn("[A-E019]", output)
        self.assertIn("[W023]", output)
        self.assertIn("accountable explicit assurance decision", output)

        text = work_order.read_text(encoding="utf-8").replace(
            'status = "in_progress"', 'status = "implemented"', 1
        )
        work_order.write_text(text, encoding="utf-8")
        code, output, _ = self.invoke(
            "preflight",
            str(target),
            "--work-order",
            "WO-IAR-001",
            "--phase",
            "review",
        )
        self.assertEqual(1, code)
        self.assertNotIn("[A-E019]", output)
        self.assertIn("[W023]", output)

    def test_distribution_comparison_detects_coordinated_file_and_lock_change(self) -> None:
        target = self.installed_target()
        agents = target / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8").replace(
                "Read `ENGINEERING_HARNESS.md`",
                "Skip `ENGINEERING_HARNESS.md`",
            ),
            encoding="utf-8",
        )
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        managed = tracked_content("fragment", agents.read_bytes())
        self.assertIsNotNone(managed)
        lock["files"]["AGENTS.md"]["sha256"] = canonical_sha256(managed)
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        code, output, _ = self.invoke("doctor", str(target))
        self.assertEqual(1, code)
        self.assertIn("PASS managed:AGENTS.md", output)
        self.assertIn("FAIL distribution:AGENTS.md", output)

    def test_pull_request_work_order_selection_is_strict(self) -> None:
        target = self.installed_target()
        script = target / "scripts" / "select_harness_work_order.py"
        event = self.root / "event.json"
        event.write_text(
            json.dumps({"pull_request": {"body": "Summary\n\nHarness-Work-Order: WO-IAR-001\n"}}),
            encoding="utf-8",
        )
        completed = subprocess.run(
            [sys.executable, str(script), "--event", str(event)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("WO-IAR-001", completed.stdout.strip())
        code, output, error = self.invoke("select-work-order", "--event", str(event))
        self.assertEqual(0, code, error)
        self.assertEqual("WO-IAR-001", output.strip())

        for body in (
            "No declaration",
            "Harness-Work-Order: WO-IAR-001\nHarness-Work-Order: WO-IAR-002\n",
            "Harness-Work-Order: WO-IAR-001; echo pwned\n",
            "Harness-Work-Order: WO-...\n",
        ):
            event.write_text(json.dumps({"pull_request": {"body": body}}), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(script), "--event", str(event)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(2, completed.returncode)
            self.assertIn("expected exactly one", completed.stderr)
            code, _, error = self.invoke("select-work-order", "--event", str(event))
            self.assertEqual(2, code)
            self.assertIn("expected exactly one", error)

        event.write_text(
            '{"pull_request":{"body":"Harness-Work-Order: WO-IAR-001"},'
            '"pull_request":{"body":"Harness-Work-Order: WO-IAR-002"}}',
            encoding="utf-8",
        )
        code, _, error = self.invoke("select-work-order", "--event", str(event))
        self.assertEqual(2, code)
        self.assertIn("duplicate JSON key", error)

        event.write_bytes(b" " * (2 * 1024 * 1024 + 1))
        code, _, error = self.invoke("select-work-order", "--event", str(event))
        self.assertEqual(2, code)
        self.assertIn("exceeds the size limit", error)

    def test_consumer_workflow_uses_one_released_package_evaluator(self) -> None:
        target = self.installed_target()
        workflow = (target / ".github" / "workflows" / "engineering-harness.yml").read_text(
            encoding="utf-8"
        )
        self.assertRegex(workflow, r"(?m)^  validate:$")
        self.assertEqual(1, len(re.findall(r"(?m)^  [a-z][a-z-]*:$", workflow.split("jobs:\n", 1)[1])))
        self.assertIn(f'SE_HARNESS_VERSION: "{__version__}"', workflow)
        self.assertIn('"se-harness==$SE_HARNESS_VERSION"', workflow)
        self.assertIn("--only-binary=:all:", workflow)
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn("-I -c", workflow)
        self.assertIn("'role':'consumer-evaluator'", workflow)
        self.assertIn("select-work-order --event", workflow)
        self.assertIn("--phase review", workflow)
        self.assertIn("-I -m se_harness preflight .", workflow)
        self.assertIn("-I -m se_harness doctor .", workflow)
        self.assertIn("-I -m se_harness validate .", workflow)
        self.assertIn("-I -m se_harness dashboard .", workflow)
        self.assertNotIn("/harnessctl", workflow)
        self.assertNotIn("select_harness_work_order.py", workflow)
        self.assertNotIn("validate_engineering_artifacts.py", workflow)
        self.assertNotIn("generate_harness_dashboard.py", workflow)
        self.assertNotIn("governor:", workflow)
        self.assertNotIn("candidate:", workflow)
        self.assertNotIn("GOVERNOR_", workflow)
        self.assertNotIn("governor-target", workflow)
        self.assertNotIn("${{ github.event.pull_request.body", workflow)
        self.assertNotIn("{{HARNESS", workflow)
        self.assertNotIn("{{GOVERNOR", workflow)

    def test_lock_records_standard_evaluator_identity_after_instruction_install(self) -> None:
        target = self.installed_target()
        lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual(LOCK_SCHEMA, lock["schema"])
        self.assertEqual(HASH_ALGORITHM, lock["hash_algorithm"])
        self.assertEqual(HASH_MODE, lock["hash_mode"])
        self.assertEqual(__version__, lock["evaluator"]["version"])
        self.assertRegex(lock["evaluator"]["payload_sha256"], r"^[0-9a-f]{64}$")


AGENTS = REPOSITORY_ROOT / "AGENTS.md"
LOCK = REPOSITORY_ROOT / ".engineering-harness.lock"
OWNER_REGION_SIZE_LIMIT = 6_000
OWNER_EDITABLE_SCRIPTS = (
    "bind_release_distribution.py",
    "check_portable_release_surface.py",
    "create_release_bundle_manifest.py",
    "normalize_sdist.py",
    "validate_release_distributions.py",
)
REQUIRED_OWNER_CONTENT = (
    'python -m unittest discover -s tests -p "test_*.py"',
    "python scripts/validate_engineering_artifacts.py --root .",
    "python scripts/validate_release_distributions.py --root .",
    "se_harness/cli.py",
    "pyproject.toml",
    "docs/engineering/REPOSITORY_CONTEXT.md",
    "templates/repository/standard/",
    "`.engineering-harness.lock` is authoritative",
    "Harness-Work-Order: WO-",
    "stored event payload",
    "RID018",
    "docs/engineering/README.md",
    "Product invariants are governed requirements",
)
WITHDRAWN_RESTATEMENTS = (
    "preflight-required",
    "harness-seeded",
    "so it stays",
    "Python 3.11+",
)


class OwnerInstructionRegionTests(unittest.TestCase):
    """Evidence for REQ-IAR-020 and SPEC-IAR-012: this repository's own owner region."""

    def setUp(self) -> None:
        self.raw = AGENTS.read_bytes()
        self.text = self.raw.decode("utf-8")
        self.lock = json.loads(LOCK.read_text(encoding="utf-8"))

    def owner_region(self) -> str:
        begin = self.text.index(BEGIN_MARKER)
        end = self.text.index(END_MARKER) + len(END_MARKER)
        return self.text[:begin] + self.text[end:]

    def test_owner_region_edit_leaves_the_managed_block_digest_at_its_lock_value(self) -> None:
        entry = self.lock["files"]["AGENTS.md"]
        self.assertEqual("fragment", entry["mode"])
        self.assertEqual(entry["sha256"], canonical_sha256(tracked_content("fragment", self.raw)))

    def test_owner_file_carries_exactly_one_ordered_marker_pair(self) -> None:
        self.assertEqual(1, self.text.count(BEGIN_MARKER))
        self.assertEqual(1, self.text.count(END_MARKER))
        self.assertLess(self.text.index(BEGIN_MARKER), self.text.index(END_MARKER))

    def test_owner_region_stays_within_the_size_bound(self) -> None:
        size = len(self.owner_region().encode("utf-8"))
        self.assertLess(size, OWNER_REGION_SIZE_LIMIT, f"owner region is {size} bytes")

    def test_owner_region_carries_the_required_operational_facts(self) -> None:
        region = self.owner_region()
        for fact in REQUIRED_OWNER_CONTENT:
            with self.subTest(fact=fact):
                self.assertIn(fact, region)
        self.assertIn("none is configured", region)
        self.assertIn("Do not invent one as a required gate", region)

    def test_owner_region_states_no_withdrawn_or_governed_restatement(self) -> None:
        region = self.owner_region()
        for withdrawn in WITHDRAWN_RESTATEMENTS:
            with self.subTest(withdrawn=withdrawn):
                self.assertNotIn(withdrawn, region)

    def test_owner_region_identifies_every_managed_path_from_the_lock(self) -> None:
        region = self.owner_region()
        managed = sorted(path for path, entry in self.lock["files"].items() if entry.get("mode") == "managed")
        self.assertEqual(30, len(managed))
        self.assertIn("docs/engineering/", region)
        self.assertIn("in `scripts/`", region)
        for path in managed:
            with self.subTest(path=path):
                if path.startswith("docs/engineering/templates/"):
                    self.assertIn("every file in `docs/engineering/templates/`", region)
                    continue
                # A shared directory prefix may be stated once, so a basename identifies the path.
                name = path.rsplit("/", 1)[-1]
                self.assertTrue(path in region or name in region, f"{path} is not identified")

    def test_owner_region_separates_owner_editable_scripts_from_managed_ones(self) -> None:
        region = self.owner_region()
        managed_scripts = {
            path.split("/", 1)[1]
            for path, entry in self.lock["files"].items()
            if path.startswith("scripts/") and entry.get("mode") == "managed"
        }
        self.assertEqual(8, len(managed_scripts))
        for name in OWNER_EDITABLE_SCRIPTS:
            with self.subTest(script=name):
                self.assertIn(name, region)
                self.assertNotIn(name, managed_scripts)
                self.assertNotIn(f"scripts/{name}", self.lock["files"])

    def test_owner_region_keeps_the_retained_agent_constraints(self) -> None:
        region = self.owner_region()
        for constraint in (
            "deterministic boundary and failure tests",
            "Treat target paths, repository content, lock data, artifact metadata, "
            "and pull-request text as untrusted input.",
            "Do not build promotable release distributions unless an approved release "
            "work order authorizes that build.",
            "Never rewrite historical `VREC-*` or `RLS-*` facts, and preserve unrelated changes.",
        ):
            with self.subTest(constraint=constraint[:40]):
                self.assertIn(constraint, region)

    def test_owner_region_claims_no_authority(self) -> None:
        region = self.owner_region().lower()
        for claim in (
            "i approve",
            "approved by",
            "takes precedence",
            "overrides `docs/engineering/`",
            "authorizes release",
        ):
            with self.subTest(claim=claim):
                self.assertNotIn(claim, region)

    def test_owner_region_directs_the_evaluator_outside_the_checkout(self) -> None:
        region = self.owner_region()
        self.assertIn("outside the checkout", region)
        self.assertIn("se-harness==0.6.0", region)
        for governed_command in ("focus", "check", "transition", "rehearse-recovery"):
            with self.subTest(command=governed_command):
                self.assertIn(f"`{governed_command}`", region)


if __name__ == "__main__":
    unittest.main()
