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

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = REPOSITORY_ROOT / ".github/workflows"
TEMPLATE_WORKFLOWS = REPOSITORY_ROOT / "templates/repository/standard/.github/workflows"

CANDIDATE_EVIDENCE_WORKFLOWS = {
    "candidate-evidence": WORKFLOWS / "candidate-evidence.yml",
    "governor-transition": WORKFLOWS / "predecessor-evaluator-assessment.yml",
    "engineering-harness": TEMPLATE_WORKFLOWS / "engineering-harness.yml",
}
PROTECTED_LINES = ("main", '"release/**"', '"candidate/**"')


def _job_blocks(workflow: str) -> dict[str, str]:
    """Split the `jobs:` mapping into {job_id: block text} without a YAML parser."""

    body = workflow.split("\njobs:\n", 1)[1]
    names = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^  ([a-z][a-z0-9-]*):$", body)]
    blocks = {}
    for index, (start, name) in enumerate(names):
        end = names[index + 1][0] if index + 1 < len(names) else len(body)
        blocks[name] = body[start:end]
    return blocks


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
        # REQ-ECP-006 / ECP-GTE-001 to -005 and -007: the scope step has no guard
        # on a declared digest, no early exit on its absence, reads the change set
        # from Git and never from the body, and runs the released evaluator.
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
        self.assertIn("select-work-order --event", step)
        self.assertNotIn("github.head_ref", step)
        self.assertNotIn("secrets.", step)
        self.assertLess(step.index("--from-git"), step.index("restitution-digest"))
        self.assertIn("does not match the recomputed result_sha256", step)
        seed = (REPOSITORY_ROOT / "templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed").read_text(encoding="utf-8")
        self.assertIn("fails on any path of the diff outside the work order's declared scope", seed)
        self.assertNotIn("reviewers remain accountable for confirming that the diff stays within its scope", seed)


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
            ("governance-migration", "Get-FileHash -Algorithm SHA256 -LiteralPath $wheel.FullName"),
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
        self.assertNotIn("governance-migration-reconcile", self.jobs)
        migration = self.jobs["governance-migration"]
        self.assertIn("outputs:\n      Linux: ${{ steps.digest.outputs.Linux }}\n      Windows: ${{ steps.digest.outputs.Windows }}", migration)
        build = self.jobs["integration-package-build"]
        self.assertIn("Require one cross-platform migration semantic result", build)
        self.assertIn("MIGRATION_DIGEST_LINUX: ${{ needs.governance-migration.outputs.Linux }}", build)
        # SPEC-IPK-001 rule 5 keeps the retention job downstream of every matrix member
        self.assertIn("integration-package-retain", self.jobs)
        self.assertEqual(
            ["candidate-source", "candidate-package", "governance-migration",
             "integration-package-build", "integration-package-verify", "integration-package-retain"],
            list(self.jobs),
        )

    def test_the_double_rehearsal_per_platform_is_kept(self) -> None:
        # REQ-REB-017's acceptance example runs the rehearsal twice per platform.
        migration = self.jobs["governance-migration"]
        self.assertEqual(2, migration.count("-m repository_tools.upgrade_rehearsal"))


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

    def test_facts_come_from_the_lock_and_the_legacy_table(self) -> None:
        from repository_tools.evaluator_facts import LEGACY_ACCEPTANCE_CONTRACT_SHA256, derive, released_evaluator_archive

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
        # WO-HUP-008: a root that carries the qualify namespace (0.8.0 and later) has no
        # legacy accept-candidate contract; the fact is then None and the typed branch runs.
        self.assertEqual(LEGACY_ACCEPTANCE_CONTRACT_SHA256.get(facts.version), facts.acceptance_contract_sha256)
        lines = facts.github_output_lines().splitlines()
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
                self.assertEqual(set(), {v for v in versions if v in {"0.6.0", "0.7.0", "0.7.1", "0.8.0"}}, versions)

    def test_workflow_derives_once_and_consumers_take_the_outputs(self) -> None:
        text = (WORKFLOWS / "candidate-evidence.yml").read_text(encoding="utf-8")
        jobs = _job_blocks(text)
        self.assertEqual(1, text.count("repository_tools.evaluator_facts derive"))
        self.assertIn("repository_tools.evaluator_facts derive", jobs["candidate-source"])
        for output in ("predecessor_version", "predecessor_wheel_sha256"):
            self.assertIn(f"{output}: ${{{{ steps.predecessor.outputs.", jobs["candidate-source"])
        self.assertNotIn("migration_scenario", text)
        self.assertIn("needs.candidate-source.outputs.predecessor_acceptance_contract_sha256", jobs["candidate-package"])
        self.assertIn("needs.candidate-source.outputs.predecessor_wheel_sha256", jobs["governance-migration"])
        self.assertIn("throw 'predecessor facts were not derived by candidate-source'", jobs["governance-migration"])

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
            pyproject.write_text(pyproject.read_text(encoding="utf-8").replace(f'version = "{declared}"', 'version = "0.9.0"', 1), encoding="utf-8")
            self.assertEqual("0.9.0", derive(root).candidate_version)
            completed = subprocess.run(
                [sys.executable, "-m", "repository_tools.evaluator_facts", "derive", "--repository", str(root)],
                capture_output=True, text=True, cwd=REPOSITORY_ROOT,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertIn('"candidate_version":"0.9.0"', completed.stdout)

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

    def test_the_digest_declaration_and_its_script_are_gone(self) -> None:
        scripts = REPOSITORY_ROOT / ".github/scripts"
        self.assertFalse((scripts / "rehearse_publication.py").exists())
        self.assertFalse((scripts / "publication_rehearsal_mechanics.json").exists())
        self.assertFalse((REPOSITORY_ROOT / "tests/test_publication_rehearsal.py").exists())

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
        from tests.test_release_orchestration import RELEASE as module

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


if __name__ == "__main__":
    unittest.main()
