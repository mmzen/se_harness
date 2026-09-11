"""Evidence for REQ-CIP-001, REQ-CIP-002 (WO-CIP-001) and REQ-CIP-006 (WO-CIP-003)."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from tests.git_support import git, init_repository
from tests.root_identity_support import load_module

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = REPOSITORY_ROOT / ".github/workflows"
TEMPLATE_WORKFLOWS = REPOSITORY_ROOT / "templates/repository/standard/.github/workflows"

CANDIDATE_EVIDENCE_WORKFLOWS = {
    "candidate-evidence": WORKFLOWS / "candidate-evidence.yml",
    # WO-CIP-007 (CIP-ONE-011): the concurrency group is the workflow's own name.
    "predecessor-evaluator-assessment": WORKFLOWS / "predecessor-evaluator-assessment.yml",
    "engineering-harness": TEMPLATE_WORKFLOWS / "engineering-harness.yml",
}
PROTECTED_LINES = ("main", '"release/**"', '"candidate/**"')

# WO-CIP-007: the workflows this repository owns. The managed template is
# SPEC-DST-027's and its hash-locked root copy follows a release, so neither is
# subject to the rules of SPEC-CIP-003.
REPOSITORY_OWNED = tuple(
    sorted(path for path in WORKFLOWS.glob("*.yml") if path.name != "engineering-harness.yml")
)
# SPEC-CIP-003, Terms: a retired name is governor, governor-transition or
# governance-migration. Two literals are exempt because WO-CIP-007 places
# "renaming scripts/validate_governor_transition.py or any script, module or
# test file" out of scope: the script's path, and the schema string it emits.
RETIRED_NAME = re.compile(r"governor|governance.migration", re.IGNORECASE)
RETIRED_NAME_EXEMPTIONS = (
    "scripts/validate_governor_transition.py",
    "se-harness-governor-transition-v1",
)
PIN_FORM = re.compile(r"^[\w.-]+/[\w./-]+@[0-9a-f]{40} # v\d+\.\d+\.\d+(?:\.post\d+)?$")


def _job_blocks(workflow: str) -> dict[str, str]:
    """Split the `jobs:` mapping into {job_id: block text} without a YAML parser."""

    body = workflow.split("\njobs:\n", 1)[1]
    names = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^  ([a-z][a-z0-9-]*):$", body)]
    blocks = {}
    for index, (start, name) in enumerate(names):
        end = names[index + 1][0] if index + 1 < len(names) else len(body)
        blocks[name] = body[start:end]
    return blocks


def _step_blocks(job: str) -> list[str]:
    """Split one job block into its step texts."""

    return re.split(r"(?m)^      - ", job)[1:]


class TriggerPolicyTests(unittest.TestCase):
    """REQ-CIP-001 / SPEC-CIP-001 CIP-TRG."""

    def test_each_candidate_evidence_workflow_runs_once_per_commit(self) -> None:
        for name, path in CANDIDATE_EVIDENCE_WORKFLOWS.items():
            with self.subTest(workflow=path.name):
                text = path.read_text(encoding="utf-8")
                head = text.split("\njobs:\n", 1)[0]
                self.assertIn("\non:\n  pull_request:\n  push:\n    branches:\n", head)
                push_block = head.split("  push:\n", 1)[1].split("\nconcurrency:", 1)[0]
                for line in PROTECTED_LINES:
                    self.assertIn(f"      - {line}\n", push_block, line)
                self.assertRegex(head, rf"(?m)^concurrency:\n  group: {name}-\$\{{\{{ github\.ref \}}\}}\n  cancel-in-progress: true$")
                # the header comment names the policy and the note that describes the workflow
                self.assertTrue(text.startswith("# "), "workflow header comment missing")
                self.assertIn("pull requests, and pushes to", text.split("\nname:", 1)[0])

    def test_release_workflows_do_not_cancel_in_progress(self) -> None:
        for filename in ("publish-pypi.yml", "release-candidate-replay.yml", "publish-dashboard-pages.yml"):
            with self.subTest(workflow=filename):
                text = (WORKFLOWS / filename).read_text(encoding="utf-8")
                self.assertIn("cancel-in-progress: false", text)

    def test_root_managed_copy_is_untouched(self) -> None:
        # The root engineering-harness.yml is the hash-locked copy of the released
        # governor, which carries WO-CIP-001's trigger policy; a work order changes
        # the standard template only, and the root follows on the next upgrade.
        # Since WO-ECP-003 the template carries the unconditional scope gate that
        # the released root does not, so the two are byte-identical only while
        # the root is the release that shipped the current template.
        from se_harness import __version__
        from se_harness.installer import tracked_content
        from se_harness.integrity import canonical_sha256

        root_path = WORKFLOWS / "engineering-harness.yml"
        root = root_path.read_text(encoding="utf-8")
        template = (REPOSITORY_ROOT / "templates/repository/standard/.github/workflows/engineering-harness.yml").read_text(encoding="utf-8")
        lock = json.loads((REPOSITORY_ROOT / ".engineering-harness.lock").read_bytes())
        evaluator_version = lock["evaluator"]["version"]
        entry = lock["files"][".github/workflows/engineering-harness.yml"]
        self.assertEqual(entry["sha256"], canonical_sha256(tracked_content(entry["mode"], root_path.read_bytes())))
        if evaluator_version == __version__:
            self.assertEqual(template.replace("{{HARNESS_VERSION}}", evaluator_version), root)
        else:
            self.assertIn("Enforce the work-order scope on the pull request's diff", template)
        self.assertIn("\non:\n  pull_request:\n  push:\n    branches:\n", root)
        self.assertIn("cancel-in-progress: true", root)

    def test_the_managed_workflow_enforces_scope_on_every_pull_request(self) -> None:
        # REQ-ECP-006 / ECP-GTE-003, -005, -007 and REQ-ECP-020 / ECP-SCP-006 to -009:
        # the scope check has no guard on a declared digest or on lifecycle state, no
        # early exit, reads the change set from Git and never from the body, and runs
        # the released evaluator; the handoff check and the digest comparison sit
        # behind the in_progress reading of the scope result.
        template = (REPOSITORY_ROOT / "templates/repository/standard/.github/workflows/engineering-harness.yml").read_text(encoding="utf-8")
        step = template.split("      - name: Enforce the work-order scope on the pull request's diff\n", 1)[1]
        step = step.split("      - name: ", 1)[0]
        self.assertIn("if: github.event_name == 'pull_request'", step)
        self.assertEqual(1, step.count("if: "))
        self.assertNotIn("exit 0", step)
        self.assertNotIn("--changed-path", step)
        self.assertNotIn("Verify a declared restitution digest", template)
        self.assertIn('--from-git "$HARNESS_BASE_SHA"', step)
        self.assertIn('git fetch --depth=1 origin "$HARNESS_BASE_SHA"', step)
        self.assertIn('"$RUNNER_TEMP/se-harness-env/bin/python" -I -m se_harness check .', step)
        self.assertIn("QGP-G4I-PATHS", step)
        self.assertIn("--checkpoint scope", step)
        self.assertLess(step.index("--checkpoint scope"), step.index("--checkpoint handoff"))
        self.assertLess(step.index("--checkpoint scope"), step.index("in_progress"))
        self.assertLess(step.index('if [ "$in_progress" != "yes" ]'), step.index("--checkpoint handoff"))
        self.assertLess(step.index("--checkpoint handoff"), step.index("does not match the recomputed result_sha256"))
        self.assertIn("was bound at handoff and is not recomputed after completion", step)
        self.assertIn("The scope check did not complete", step)
        self.assertIn("select-work-order --event", step)
        self.assertNotIn("github.head_ref", step)
        self.assertNotIn("secrets.", step)
        self.assertLess(step.index("--from-git"), step.index("restitution-digest"))
        self.assertIn("does not match the recomputed result_sha256", step)
        seed = (REPOSITORY_ROOT / "templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed").read_text(encoding="utf-8")
        self.assertIn("fails on any path of the diff outside the work order's declared scope, whatever the work order's lifecycle state", seed)
        self.assertNotIn("reviewers remain accountable for confirming that the diff stays within its scope", seed)

    def test_the_managed_lane_selects_from_the_live_pull_request_body(self) -> None:
        # REQ-ECP-026 / ECP-LPB-001 to -004 and -006 (WO-ECP-021): the lane
        # fetches the pull request from the API during the run, reduces it to
        # one event-shaped file, and selects every declaration from that file,
        # so a corrected body is honoured by a re-run without a new push.
        template = CANDIDATE_EVIDENCE_WORKFLOWS["engineering-harness"].read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read\n  pull-requests: read\n", template)

        step = template.split("      - name: Read the live pull-request body\n", 1)[1]
        step = step.split("      - name: ", 1)[0]
        self.assertIn("if: github.event_name == 'pull_request'", step)
        self.assertIn("PULL_REQUEST_NUMBER: ${{ github.event.pull_request.number }}", step)
        self.assertIn('"$GITHUB_API_URL/repos/$GITHUB_REPOSITORY/pulls/$PULL_REQUEST_NUMBER"', step)
        self.assertIn("curl --fail", step)
        self.assertIn("Authorization: Bearer $GH_TOKEN", step)
        self.assertIn('"$RUNNER_TEMP/se-harness-env/bin/python" - "$RUNNER_TEMP/pull-request.json" "$RUNNER_TEMP/live-event.json"', step)
        self.assertIn('json.dump({"pull_request": {"body": pull_request.get("body")}}', step)
        self.assertNotIn("${{ github.event.pull_request.body", step)

        # ECP-LPB-004: both selections read the live file; the stored payload
        # is gone from the template, and the fetch precedes the selection.
        self.assertEqual(2, template.count('select-work-order --event "$RUNNER_TEMP/live-event.json"'))
        self.assertNotIn("GITHUB_EVENT_PATH", template)
        self.assertLess(
            template.index("- name: Install the exact released evaluator"),
            template.index("- name: Read the live pull-request body"),
        )
        self.assertLess(
            template.index("- name: Read the live pull-request body"),
            template.index("- name: Select the pull-request work order"),
        )

        # ECP-LPB-006: the change set and the guards keep their trigger-context
        # inputs; nothing the body carries becomes an input of check.
        self.assertIn("HARNESS_BASE_SHA: ${{ github.event.pull_request.base.sha }}", template)
        self.assertIn('git fetch --depth=1 origin "$HARNESS_BASE_SHA"', template)


class OneBuildPerWorkflowTests(unittest.TestCase):
    """REQ-CIP-002 / SPEC-CIP-001 CIP-ART."""

    def setUp(self) -> None:
        self.text = CANDIDATE_EVIDENCE_WORKFLOWS["candidate-evidence"].read_text(encoding="utf-8")
        self.jobs = _job_blocks(self.text)

    def test_only_candidate_source_builds_and_every_consumer_verifies_the_handover(self) -> None:
        builders = [name for name, block in self.jobs.items() if "pip wheel" in block or "python -m build" in block]
        self.assertEqual(["candidate-source"], builders)
        source = self.jobs["candidate-source"]
        self.assertIn("sha256sum -- *.whl > SHA256SUMS", source)
        self.assertIn("name: candidate-wheel-non-promotable-${{ github.sha }}", source)
        for consumer, check in (
            ("candidate-package", "sha256sum --check --strict SHA256SUMS"),
            ("upgrade-rehearsal", "Get-FileHash -Algorithm SHA256 -LiteralPath $wheel.FullName"),
        ):
            with self.subTest(job=consumer):
                block = self.jobs[consumer]
                self.assertIn("name: candidate-wheel-non-promotable-${{ github.sha }}", block)
                self.assertIn(check, block)
                self.assertNotIn("git archive", block)

    def test_integration_package_keeps_its_own_deterministic_double_build(self) -> None:
        # SPEC-IPK-001 rule 1: the integration package applies a local-version
        # overlay and builds twice for byte equality; those bytes are a different
        # distribution from the candidate wheel and are built by the script, not
        # by the workflow. Recorded as a deviation from CIP-ART in WO-CIP-001.
        block = self.jobs["integration-package-build"]
        self.assertIn("build_integration_package.py", block)
        self.assertNotIn("pip wheel", block)

    def test_reconcile_and_retain_only_jobs(self) -> None:
        # WO-CIP-007 (CIP-ONE-012): the rehearsal job, its artifact, its needs entry
        # and its output references all read upgrade-rehearsal.
        self.assertNotIn("governance-migration-reconcile", self.jobs)
        rehearsal = self.jobs["upgrade-rehearsal"]
        self.assertIn("outputs:\n      Linux: ${{ steps.digest.outputs.Linux }}\n      Windows: ${{ steps.digest.outputs.Windows }}", rehearsal)
        self.assertIn("name: upgrade-rehearsal-${{ matrix.platform }}", rehearsal)
        build = self.jobs["integration-package-build"]
        self.assertIn("Require one cross-platform upgrade rehearsal semantic result", build)
        self.assertIn("REHEARSAL_DIGEST_LINUX: ${{ needs.upgrade-rehearsal.outputs.Linux }}", build)
        self.assertIn("      - upgrade-rehearsal\n", build)
        # SPEC-IPK-001 rule 5 keeps the retention job downstream of every matrix member
        self.assertIn("integration-package-retain", self.jobs)
        self.assertEqual(
            ["candidate-source", "candidate-package", "upgrade-rehearsal",
             "integration-package-build", "integration-package-verify", "integration-package-retain"],
            list(self.jobs),
        )

    def test_the_double_rehearsal_per_platform_is_kept(self) -> None:
        # REQ-REB-017's acceptance example runs the rehearsal twice per platform.
        rehearsal = self.jobs["upgrade-rehearsal"]
        self.assertEqual(2, rehearsal.count("-m repository_tools.upgrade_rehearsal"))


class RehearsalDiagnosticBoundaryTests(unittest.TestCase):
    def test_diagnostics_are_read_only_and_retained_without_changing_replay_gates(self):
        job = _job_blocks((WORKFLOWS / "candidate-evidence.yml").read_text(encoding="utf-8"))["upgrade-rehearsal"]
        steps = _step_blocks(job)
        diagnostic = next(step for step in steps if "name: Observe the rehearsal runtime" in step)
        self.assertIn("Get-MpComputerStatus -ErrorAction Stop", diagnostic)
        self.assertIn("Get-MpPreference -ErrorAction Stop", diagnostic)
        self.assertIn("RealTimeProtectionEnabled", diagnostic)
        self.assertIn("DisableRealtimeMonitoring", diagnostic)
        self.assertIn("ExclusionPath", diagnostic)
        self.assertEqual(2, diagnostic.count("availability = 'unavailable'"))
        self.assertNotRegex(diagnostic, r"(?i)(?:Set|Add|Remove)-Mp\w+|Stop-Service|Get-ChildItem\s+Env:")
        self.assertIn("Join-Path $env:RUNNER_TEMP 'upgrade-rehearsal-runtime.json'", diagnostic)
        replay = next(step for step in steps if "name: Rehearse the real predecessor-to-successor" in step)
        self.assertEqual(2, replay.count("python -m repository_tools.upgrade_rehearsal"))
        self.assertEqual(2, replay.count(" --timings"))
        self.assertEqual(2, replay.count(" --workspace $env:RUNNER_TEMP"))
        self.assertIn("if ($firstResult.semantic_sha256 -ne $secondResult.semantic_sha256)", replay)
        self.assertIn("if ($firstResult.overall_result -ne 'pass' -or $secondResult.overall_result -ne 'pass')", replay)
        retention = next(step for step in steps if "name: Retain the bounded upgrade rehearsal evidence" in step)
        self.assertIn("if: always()", retention)
        for filename in ("upgrade-rehearsal-result.json", "upgrade-rehearsal-timing.json", "upgrade-rehearsal-runtime.json"):
            self.assertIn(filename, retention)


class PredecessorDerivationTests(unittest.TestCase):
    """REQ-CIP-006 / SPEC-CIP-001 CIP-PRE."""

    REPOSITORY_OWNED = (WORKFLOWS / "candidate-evidence.yml", WORKFLOWS / "predecessor-evaluator-assessment.yml")

    def test_every_consumed_job_output_is_declared_in_the_consumers_needs(self) -> None:
        # Found by the hosted run of PR #172 (WO-CIP-003): needs.<job>.outputs.* resolve to
        # empty strings unless <job> is in the consumer's needs, and the workflow's guards
        # then refuse to run. Corrected under WO-CIP-002.
        for path in sorted(WORKFLOWS.glob("*.yml")):
            text = path.read_text(encoding="utf-8")
            if "\njobs:\n" not in text:
                continue
            for job, block in _job_blocks(text).items():
                declared: set[str] = set()
                match = re.search(r"(?m)^    needs:[ \t]*(.*)$", block)
                if match:
                    inline = match.group(1).strip()
                    if inline.startswith("["):
                        declared = {item.strip() for item in inline.strip("[]").split(",") if item.strip()}
                    elif inline:
                        declared = {inline}
                    else:
                        for line in block[match.end():].split("\n")[1:]:
                            if not line.startswith("      - "):
                                break
                            declared.add(line[8:].strip())
                for consumed in set(re.findall(r"needs\.([a-z_-]+)\.(?:outputs|result)", block)):
                    with self.subTest(workflow=path.name, job=job, consumed=consumed):
                        self.assertIn(consumed, declared)

    def test_facts_come_from_the_lock(self) -> None:
        from repository_tools.evaluator_facts import derive, released_evaluator_archive

        lock = json.loads((REPOSITORY_ROOT / ".engineering-harness.lock").read_bytes())["evaluator"]
        facts = derive(REPOSITORY_ROOT)
        self.assertEqual(lock["version"], facts.version)
        # WO-HUP-007: the lock's archive pair is null for an index install (REQ-REB-028);
        # the wheel then comes from the one released record binding that version.
        if lock["archive_name"] is None and lock["archive_sha256"] is None:
            expected_wheel, expected_wheel_sha256 = released_evaluator_archive(REPOSITORY_ROOT, lock["version"])
        else:
            expected_wheel, expected_wheel_sha256 = lock["archive_name"], lock["archive_sha256"]
        self.assertEqual(expected_wheel, facts.wheel)
        self.assertEqual(expected_wheel_sha256, facts.wheel_sha256)
        self.assertEqual(lock["payload_sha256"], facts.payload_sha256)
        # WO-REB-031 (SPEC-REB-016 REB-BFH-002): no legacy acceptance-contract
        # fact exists; the derivation exports version, wheel, digests and the
        # candidate version only.
        self.assertFalse(hasattr(facts, "acceptance_contract_sha256"))
        lines = facts.github_output_lines().splitlines()
        self.assertFalse(any(line.startswith("acceptance_contract") for line in lines), lines)
        self.assertIn(f"wheel_sha256={facts.wheel_sha256}", lines)
        # WO-ECP-010: no scenario fact exists any more; a version bump needs none.
        self.assertFalse(any(line.startswith("scenario") for line in lines), lines)

    def test_null_archive_pair_is_supplied_by_exactly_one_released_record(self) -> None:
        """WO-HUP-007: an index-installed root has no archive pair; the released record binding
        the evaluator version supplies it, and zero or several such records fail closed."""
        from repository_tools.evaluator_facts import PredecessorFactsError, derive, released_evaluator_archive

        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            self._copy_repository_declarations(root)
            lock_path = root / ".engineering-harness.lock"
            lock = json.loads(lock_path.read_bytes())
            version = lock["evaluator"]["version"]
            lock["evaluator"]["archive_name"] = None
            lock["evaluator"]["archive_sha256"] = None
            lock_path.write_bytes(json.dumps(lock, indent=2).encode("utf-8"))
            wheel, wheel_sha256 = released_evaluator_archive(root, version)
            self.assertEqual(f"se_harness-{version}-py3-none-any.whl", wheel)
            facts = derive(root)
            self.assertEqual((wheel, wheel_sha256), (facts.wheel, facts.wheel_sha256))
            records = [
                path for path in (root / "docs/engineering").rglob("RLS-*.md")
                if f'version = "{version}"' in path.read_text(encoding="utf-8")
                and 'status = "released"' in path.read_text(encoding="utf-8")
            ]
            self.assertEqual(1, len(records))
            duplicate = records[0].with_name("RLS-DUP-999.md")
            duplicate.write_bytes(records[0].read_bytes())
            with self.assertRaises(PredecessorFactsError) as caught:
                derive(root)
            self.assertIn("PRE014", str(caught.exception))
            duplicate.unlink()
            records[0].unlink()
            with self.assertRaises(PredecessorFactsError) as caught:
                derive(root)
            self.assertIn("PRE014", str(caught.exception))
            self.assertIn("found none", str(caught.exception))

    def test_no_predecessor_literal_remains_in_the_repository_owned_workflows(self) -> None:
        for path in self.REPOSITORY_OWNED:
            with self.subTest(workflow=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(re.search(r"[0-9a-f]{64}", text.replace("actions/", "")), "a digest literal remains")
                # version literals: the pinned build tools are not evaluator facts
                versions = {m.group(0) for m in re.finditer(r"\b\d+\.\d+\.\d+(?:\.post\d+)?\b", text)}
                self.assertEqual(set(), {v for v in versions if v in {"0.6.0", "0.7.0", "0.7.1", "0.8.0", "0.9.0", "0.10.0"}}, versions)

    def test_workflow_derives_once_and_consumers_take_the_outputs(self) -> None:
        text = (WORKFLOWS / "candidate-evidence.yml").read_text(encoding="utf-8")
        jobs = _job_blocks(text)
        self.assertEqual(1, text.count("repository_tools.evaluator_facts derive"))
        self.assertIn("repository_tools.evaluator_facts derive", jobs["candidate-source"])
        for output in ("predecessor_version", "predecessor_wheel_sha256"):
            self.assertIn(f"{output}: ${{{{ steps.predecessor.outputs.", jobs["candidate-source"])
        self.assertIn("needs.candidate-source.outputs.predecessor_wheel_sha256", jobs["upgrade-rehearsal"])
        self.assertIn("throw 'predecessor facts were not derived by candidate-source'", jobs["upgrade-rehearsal"])

    def _copy_repository_declarations(self, root: Path) -> None:
        for relative in (".engineering-harness.toml", ".engineering-harness.lock", "pyproject.toml"):
            shutil.copy(REPOSITORY_ROOT / relative, root / relative)
        # WO-HUP-007: a root adopted from an index install records no archive pair;
        # derive then reads the released record that binds the evaluator version.
        for record in (REPOSITORY_ROOT / "docs/engineering").rglob("RLS-*.md"):
            relative = record.relative_to(REPOSITORY_ROOT)
            (root / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(record, root / relative)

    def test_a_version_bump_needs_no_scenario(self) -> None:
        # WO-ECP-010: derive no longer requires a hand-authored migration scenario for
        # the predecessor-to-candidate pair (issue #210, acceptance criterion 3).
        from repository_tools.evaluator_facts import derive

        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            self._copy_repository_declarations(root)
            pyproject = root / "pyproject.toml"
            declared = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]["version"]
            # WO-HUP-009: bump past the declared root rather than to a literal, so the
            # fixture stays a bump whatever version the lock names.
            root_version = tomllib.loads((root / ".engineering-harness.toml").read_text(encoding="utf-8"))["harness"]["tool_version"]
            major, minor, _patch = (int(part) for part in root_version.split("."))
            bumped = f"{major}.{minor + 1}.0"
            pyproject.write_text(pyproject.read_text(encoding="utf-8").replace(f'version = "{declared}"', f'version = "{bumped}"', 1), encoding="utf-8")
            self.assertEqual(bumped, derive(root).candidate_version)
            completed = subprocess.run(
                [sys.executable, "-m", "repository_tools.evaluator_facts", "derive", "--repository", str(root)],
                capture_output=True, text=True, cwd=REPOSITORY_ROOT,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertIn(f'"candidate_version":"{bumped}"', completed.stdout)

    def test_disagreeing_root_declarations_fail_closed(self) -> None:
        from repository_tools.evaluator_facts import PredecessorFactsError, derive

        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            self._copy_repository_declarations(root)
            toml = root / ".engineering-harness.toml"
            lock_version = json.loads((root / ".engineering-harness.lock").read_bytes())["evaluator"]["version"]
            toml.write_text(toml.read_text(encoding="utf-8").replace(f'tool_version = "{lock_version}"', 'tool_version = "0.5.0"'), encoding="utf-8")
            with self.assertRaises(PredecessorFactsError) as caught:
                derive(root)
            self.assertIn("PRE007", str(caught.exception))

    def test_repository_tools_stay_standard_library_only(self) -> None:
        # repository_tools may not widen its pinned import crossing into se_harness
        # (tests/test_interpreter_safety.py); the rehearsal and the facts both hold to it.
        for relative in ("repository_tools/evaluator_facts.py", "repository_tools/upgrade_rehearsal.py"):
            source = (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")
            imported = [line.split()[1] for line in source.splitlines() if line.startswith(("import ", "from "))]
            self.assertNotIn("se_harness", imported, relative)
            self.assertFalse(any(name.startswith("se_harness.") for name in imported), relative)


class QualificationDefinitionTests(unittest.TestCase):
    """REQ-CIP-003 and REQ-CIP-005 / SPEC-CIP-001 CIP-QLF and CIP-LEG (WO-CIP-002)."""

    def setUp(self) -> None:
        self.definition = (WORKFLOWS / "release-qualification.yml").read_text(encoding="utf-8")
        self.rehearsal = (WORKFLOWS / "publication-rehearsal.yml").read_text(encoding="utf-8")
        self.release = (WORKFLOWS / "publish-pypi.yml").read_text(encoding="utf-8")
        self.pages = (WORKFLOWS / "pages-publication.yml").read_text(encoding="utf-8")
        self.dashboard = (WORKFLOWS / "publish-dashboard-pages.yml").read_text(encoding="utf-8")

    def test_one_definition_is_invoked_by_the_rehearsal_and_the_release(self) -> None:
        self.assertIn("\non:\n  workflow_call:\n", self.definition)
        self.assertEqual(2, self.rehearsal.count("uses: ./.github/workflows/release-qualification.yml"))
        self.assertEqual(1, self.release.count("uses: ./.github/workflows/release-qualification.yml"))
        self.assertIn("mode: candidate", self.rehearsal)
        self.assertIn("mode: release-record", self.rehearsal)
        self.assertIn("mode: release-record", self.release)
        self.assertIn("require_status: ${{ needs.select.outputs.status }}", self.rehearsal)
        self.assertIn("default_ref: refs/remotes/origin/main", self.rehearsal)
        self.assertIn("publish_release.py select-rehearsal-record", self.rehearsal)
        # WO-CIP-006 (SPEC-CIP-002 CIP-REH-003): a pull request reads the records at its base.
        self.assertIn("if: github.event_name == 'pull_request'", self.rehearsal)
        self.assertIn('git fetch --no-tags --depth=1 origin "+refs/heads/$BASE_REF:refs/remotes/origin/$BASE_REF"', self.rehearsal)
        self.assertIn("BASE_REF: ${{ github.event_name == 'pull_request' && format('refs/remotes/origin/{0}', github.base_ref) || '' }}", self.rehearsal)
        self.assertIn('--base-ref "$BASE_REF"', self.rehearsal)
        self.assertNotIn("matrix", self.rehearsal)
        for absent in ("rehearse_publication", "publication_rehearsal_mechanics", "check-divergence", "PyYAML", "windows-2022"):
            self.assertNotIn(absent, self.rehearsal)

    def test_the_definition_runs_the_scale_tests_at_full_size(self) -> None:
        # WO-TST-003 (REQ-TST-002, TST-SCL 2): the release qualification sets the marker.
        self.assertIn("SE_HARNESS_TEST_SCALE: full", self.definition)
        self.assertIn("python -m unittest discover -s tests -p 'test_*.py'", self.definition)

    def test_the_definition_holds_no_authority(self) -> None:
        head = self.definition.split("\njobs:\n", 1)[0]
        self.assertIn("\npermissions:\n  contents: read\n", head)
        self.assertNotIn("secrets", self.definition)
        for absent in ("environment:", "id-token: write", "contents: write", "gh release", "git push", "pypa/"):
            self.assertNotIn(absent, self.definition)
        self.assertIn("Prove the qualification left no checkout change", self.definition)

    def test_release_runs_one_schema_leg_and_one_pages_definition(self) -> None:
        for absent in ("legacy-schema-1", "recipe-schema-2", "matrix.mode", "runs-on: ${{ matrix.os }}", "pages_build", "pages_deploy"):
            self.assertNotIn(absent, self.release)
        self.assertEqual(1, self.release.count("uses: ./.github/workflows/pages-publication.yml"))
        self.assertEqual(1, self.dashboard.count("uses: ./.github/workflows/pages-publication.yml"))
        self.assertIn("\non:\n  workflow_call:\n", self.pages)
        self.assertNotIn("steps:", self.dashboard)

    def test_each_shared_helper_is_defined_once(self) -> None:
        scripts = sorted((REPOSITORY_ROOT / ".github/scripts").glob("*.py"))
        definitions: dict[str, list[str]] = {}
        for script in scripts + [REPOSITORY_ROOT / "repository_tools/json_bytes.py"]:
            for name in re.findall(r"(?m)^def (\w+)\(", script.read_text(encoding="utf-8")):
                definitions.setdefault(name, []).append(script.name)
        # wrappers in the scripts delegate to repository_tools.json_bytes; the logic lives there
        for helper in ("_duplicate_rejecting_object", "_reject_duplicate_keys", "_loads_json", "sha256_bytes"):
            self.assertNotIn(helper, [n for n in definitions if any(s != "json_bytes.py" for s in definitions[n]) and n == helper])
        for script in scripts:
            text = script.read_text(encoding="utf-8")
            self.assertNotIn("object_pairs_hook", text, script.name)
            self.assertNotIn("def sha256_file(path: Path) -> str:\n    digest", text, script.name)
        reconcile = (REPOSITORY_ROOT / ".github/scripts/reconcile_maintenance_branch.py").read_text(encoding="utf-8")
        self.assertNotIn("urlopen", reconcile)
        self.assertIn('["gh", "api", "--include"', reconcile)
        release = (REPOSITORY_ROOT / ".github/scripts/publish_release.py").read_text(encoding="utf-8")
        self.assertNotIn("classify-pypi", release)
        self.assertIn("select-rehearsal-record", release)

    def test_rehearsal_record_selection(self) -> None:
        module = load_module(REPOSITORY_ROOT / ".github" / "scripts" / "publish_release.py", "release_orchestration_test_module")

        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            releases = root / "docs/engineering/release-x/releases"
            releases.mkdir(parents=True)

            def record(identifier: str, version: str, status: str, schema: int) -> None:
                (releases / f"{identifier}.md").write_text(
                    f'+++\nid = "{identifier}"\ntype = "release_record"\nstatus = "{status}"\nversion = "{version}"\n[distribution]\nschema = {schema}\n+++\n# {identifier}\n',
                    encoding="utf-8",
                )

            self.assertEqual("", module.select_rehearsal_record(root, None)["release_record"])
            record("RLS-X-001", "0.6.0", "released", 1)
            self.assertEqual("", module.select_rehearsal_record(root, None)["release_record"])
            record("RLS-X-002", "0.7.0", "ready", 2)
            record("RLS-X-003", "0.7.1", "released", 2)
            record("RLS-X-004", "0.8.0", "rejected", 2)
            selection = module.select_rehearsal_record(root, None)
            self.assertEqual(("RLS-X-003", "released"), (selection["release_record"], selection["status"]))
            self.assertEqual("ready", module.select_rehearsal_record(root, "RLS-X-002")["status"])
            with self.assertRaises(module.ReleaseError):
                module.select_rehearsal_record(root, "RLS-X-001")

    def test_rehearsal_record_selection_reads_the_base_ref_when_given(self) -> None:
        # WO-CIP-006 (SPEC-CIP-002 CIP-REH-001, -002, -004): with a base ref the candidates are
        # the records committed at that ref, never the checkout; without it the checkout as before.
        import subprocess

        module = load_module(REPOSITORY_ROOT / ".github" / "scripts" / "publish_release.py", "release_orchestration_test_module")

        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            releases = root / "docs/engineering/release-x/releases"
            releases.mkdir(parents=True)

            def record(identifier: str, version: str, status: str) -> None:
                (releases / f"{identifier}.md").write_text(
                    f'+++\nid = "{identifier}"\ntype = "release_record"\nstatus = "{status}"\nversion = "{version}"\n[distribution]\nschema = 2\n+++\n# {identifier}\n',
                    encoding="utf-8",
                )

            init_repository(root)
            record("RLS-X-003", "0.7.1", "released")
            git(root, "add", "-A")
            git(root, "commit", "-q", "-m", "base")
            git(root, "update-ref", "refs/remotes/origin/main", "HEAD")
            record("RLS-X-005", "0.8.0", "ready")  # the pull request's own record, uncommitted on the base

            base = module.select_rehearsal_record(root, None, "refs/remotes/origin/main")
            self.assertEqual(("RLS-X-003", "released"), (base["release_record"], base["status"]))
            self.assertIn("refs/remotes/origin/main", base["reason"])
            tree = module.select_rehearsal_record(root, None)
            self.assertEqual("RLS-X-005", tree["release_record"])
            with self.assertRaises(module.ReleaseError):
                module.select_rehearsal_record(root, "RLS-X-005", "refs/remotes/origin/main")
            with self.assertRaises(module.ReleaseError):
                module.select_rehearsal_record(root, None, "refs/remotes/origin/nowhere")
            # The command surface carries the option (the workflow calls it, not the function).
            completed = subprocess.run(
                [sys.executable, str(REPOSITORY_ROOT / ".github/scripts/publish_release.py"), "select-rehearsal-record",
                 "--repository", str(root), "--release-record", "", "--base-ref", "refs/remotes/origin/main"],
                capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertIn("RLS-X-003", completed.stdout + completed.stderr)


class PipelineHygieneTests(unittest.TestCase):
    """REQ-CIP-008 and REQ-CIP-009 / SPEC-CIP-003 (WO-CIP-007), CIP-ONE-016."""

    def setUp(self) -> None:
        self.texts = {path.name: path.read_text(encoding="utf-8") for path in REPOSITORY_OWNED}

    def test_the_qualification_definition_qualifies_and_tests_release_records_only(self) -> None:
        # CIP-ONE-001: candidate mode replays the recipe; the qualification, the
        # suite and the smoke run under the release-record guard only.
        qualify = _job_blocks(self.texts["release-qualification.yml"])["qualify"]
        for command in ("qualify complete-candidate", "unittest discover", "-m se_harness --help"):
            with self.subTest(command=command):
                holding = [step for step in _step_blocks(qualify) if command in step]
                self.assertEqual(1, len(holding), command)
                self.assertIn("if: inputs.mode == 'release-record'", holding[0])
        replay = [step for step in _step_blocks(qualify) if "release_build replay" in step]
        self.assertEqual(1, len(replay))
        self.assertNotIn("if: inputs.mode == 'release-record'", replay[0])

    def test_candidate_source_is_the_only_lane_that_qualifies_and_tests_a_pull_request(self) -> None:
        # CIP-ONE-002: one qualification and one suite run per pull-request commit.
        jobs = _job_blocks(self.texts["candidate-evidence.yml"])
        for command in ("qualify complete-candidate", "scripts/run_tests.py"):
            with self.subTest(command=command):
                holders = [name for name, block in jobs.items() if command in block]
                self.assertEqual(["candidate-source"], holders)
                self.assertEqual(1, self.texts["candidate-evidence.yml"].count(command))
        for name, text in self.texts.items():
            if name in {"candidate-evidence.yml", "release-qualification.yml"}:
                continue
            with self.subTest(workflow=name):
                for command in ("qualify complete-candidate", "run_tests.py", "unittest discover"):
                    self.assertNotIn(command, text, command)

    def test_no_step_restates_a_check_a_script_already_performs(self) -> None:
        # CIP-ONE-003 and CIP-ONE-004: the script holds the one definition of the
        # forbidden wheel members and of the retired command surface.
        package = _job_blocks(self.texts["candidate-evidence.yml"])["candidate-package"]
        self.assertIn("check_portable_release_surface.py --wheel", package)
        self.assertRegex(package, r"check_portable_release_surface\.py\" \\\n\s+--harnessctl ")
        self.assertNotIn("zipfile", package)
        self.assertNotIn("forbidden", package)
        self.assertNotIn("--help | grep", package)
        self.assertNotIn("--help | ", package)

    def test_one_python_version_string(self) -> None:
        # CIP-ONE-005: publish-pypi.yml may hold it in PYTHON_VERSION; every other
        # occurrence is the literal "3.11".
        for name, text in self.texts.items():
            with self.subTest(workflow=name):
                values = re.findall(r"(?m)^\s+(?:\"python-version\"|python-version): (.+)$", text)
                allowed = {'"3.11"'}
                if name == "publish-pypi.yml":
                    allowed.add("${{ env.PYTHON_VERSION }}")
                    self.assertIn('PYTHON_VERSION: "3.11"', text)
                else:
                    self.assertNotIn("PYTHON_VERSION", text)
                self.assertEqual(set(), set(values) - allowed, values)

    def test_every_public_action_takes_the_pin_form(self) -> None:
        # CIP-ONE-006: a full commit digest and the exact tag it was peeled from.
        for name, text in self.texts.items():
            for line in re.findall(r"(?m)^\s+(?:- )?uses: (.+)$", text):
                with self.subTest(workflow=name, uses=line):
                    if line.startswith("./.github/workflows/"):
                        continue
                    self.assertRegex(line, PIN_FORM)
        # one digest per action within a file: no file names two generations at once
        for name, text in self.texts.items():
            pins: dict[str, set[str]] = {}
            for line in re.findall(r"(?m)^\s+(?:- )?uses: ([\w.-]+/[\w./-]+)@([0-9a-f]{40})", text):
                pins.setdefault(line[0], set()).add(line[1])
            for action, digests in pins.items():
                with self.subTest(workflow=name, action=action):
                    self.assertEqual(1, len(digests), digests)

    def test_the_integration_build_toolchain_is_stated_once(self) -> None:
        # CIP-ONE-007: one env block read by the install and by the expectations.
        build = _job_blocks(self.texts["candidate-evidence.yml"])["integration-package-build"]
        for variable in ("INTEGRATION_BUILD_VERSION", "INTEGRATION_SETUPTOOLS_VERSION", "INTEGRATION_WHEEL_VERSION"):
            with self.subTest(variable=variable):
                self.assertRegex(build, rf"(?m)^      {variable}: \S+$")
                self.assertEqual(3, build.count(variable), variable)
        self.assertIn('"build==$INTEGRATION_BUILD_VERSION"', build)
        self.assertIn('--expect-build-version "$INTEGRATION_BUILD_VERSION"', build)
        for literal in ("1.2.2.post1", "75.8.0", "0.45.1"):
            with self.subTest(literal=literal):
                self.assertEqual(1, build.count(literal), literal)

    def test_every_pages_deployment_queues_behind_one_group(self) -> None:
        # CIP-ONE-008: whichever caller invokes the definition.
        deploy = _job_blocks(self.texts["pages-publication.yml"])["deploy"]
        self.assertIn("    concurrency:\n      group: se-harness-pages-deploy\n      cancel-in-progress: false\n", deploy)

    def test_the_payload_digest_is_probed_only_where_the_evaluator_may_predate_it(self) -> None:
        # CIP-ONE-009 and CIP-ONE-010.
        release = self.texts["publish-pypi.yml"]
        self.assertIn('--evaluator-payload-sha256 "$EVALUATOR_PAYLOAD_SHA256"', release)
        self.assertNotIn("identity --help", release)
        pages = self.texts["pages-publication.yml"]
        self.assertIn("identity --help", pages)
        probe = pages.split("identity --help", 1)[0].rsplit("- name:", 1)[1]
        self.assertIn("governance root", probe)

    def test_no_retired_name_survives_in_a_repository_owned_workflow(self) -> None:
        # CIP-ONE-011 and CIP-ONE-012.
        for name, text in self.texts.items():
            with self.subTest(workflow=name):
                stripped = text
                for exemption in RETIRED_NAME_EXEMPTIONS:
                    stripped = stripped.replace(exemption, "")
                found = RETIRED_NAME.search(stripped)
                self.assertIsNone(found, found.group(0) if found else "")
        assessment = self.texts["predecessor-evaluator-assessment.yml"]
        self.assertIn("name: Predecessor Evaluator Assessment\n", assessment)
        self.assertIn("  predecessor-evaluator-assessment:\n", assessment)
        self.assertIn("name: predecessor-evaluator-assessment\n", assessment)

    def test_every_repository_owned_workflow_carries_a_header_comment(self) -> None:
        # CIP-ONE-017 with SPEC-CIP-001 CIP-DOC 4: purpose, trigger policy, note.
        for name, text in self.texts.items():
            with self.subTest(workflow=name):
                header = text.split("\nname:", 1)[0]
                self.assertTrue(text.startswith("# "), "workflow header comment missing")
                self.assertIn("docs/notes/", header)
                self.assertIn("Trigger policy", header)


if __name__ == "__main__":
    unittest.main()


class DefinitionNamesTests(unittest.TestCase):
    """REQ-CIP-010 / SPEC-CIP-004 CIP-AMD-004 (WO-CIP-008): in the body of every artifact under
    the domain's architecture and requirements, the retired job name survives only inside an
    amendment record. Two front-matter fields name it as retired and are pinned as such: the
    measure of REQ-CIP-009 and the source and measure of REQ-CIP-010."""

    DIRECTORIES = (
        "docs/engineering/ci-pipeline/architecture",
        "docs/engineering/ci-pipeline/requirements",
    )
    FRONT_MATTER_MENTIONS = {"REQ-CIP-009", "REQ-CIP-010"}

    def test_the_old_job_name_occurs_only_inside_an_amendment_record(self) -> None:
        offenders: list[str] = []
        explained: set[str] = set()
        front_matter_mentions: set[str] = set()
        for directory in self.DIRECTORIES:
            for path in sorted((REPOSITORY_ROOT / directory).rglob("*.md")):
                text = path.read_text(encoding="utf-8")
                front_matter, body = text.split("+++", 2)[1:]
                if "governance-migration" in front_matter:
                    front_matter_mentions.add(path.stem)
                first_body_line = text[: len(text) - len(body)].count("\n") + 1
                inside_amendment = False
                for number, line in enumerate(body.splitlines(), first_body_line):
                    if line.startswith("## "):
                        inside_amendment = line.strip() == "## Amendment record"
                    if "governance-migration" in line:
                        if inside_amendment:
                            explained.add(path.stem)
                        else:
                            offenders.append(f"{path.relative_to(REPOSITORY_ROOT).as_posix()}:{number}")
        self.assertEqual([], offenders)
        # CIP-AMD-001 and CIP-AMD-002: the two definitions WO-CIP-007 left explain the rename.
        self.assertEqual({"ARCH-CIP-001", "REQ-CIP-002"}, explained)
        self.assertEqual(self.FRONT_MATTER_MENTIONS, front_matter_mentions)

class EvaluatorFactsFrontMatterTests(unittest.TestCase):
    """WO-ECP-027 (ECP-COR-017): a CRLF checkout yields the same release-record metadata as LF."""

    def test_crlf_front_matter_parses_like_lf(self) -> None:
        from repository_tools.evaluator_facts import _front_matter

        body = '+++\nid = "RLS-TST-001"\nversion = "0.16.0"\nstatus = "released"\n+++\n\n# Record\n'
        with tempfile.TemporaryDirectory() as scratch:
            lf = Path(scratch) / "lf.md"
            crlf = Path(scratch) / "crlf.md"
            bom = Path(scratch) / "bom.md"
            lf.write_bytes(body.encode("utf-8"))
            crlf.write_bytes(body.replace("\n", "\r\n").encode("utf-8"))
            bom.write_bytes(b"\xef\xbb\xbf" + body.encode("utf-8"))
            expected = {"id": "RLS-TST-001", "version": "0.16.0", "status": "released"}
            self.assertEqual(expected, _front_matter(lf))
            self.assertEqual(expected, _front_matter(crlf))
            self.assertEqual(expected, _front_matter(bom))
