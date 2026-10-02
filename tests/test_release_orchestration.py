from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from copy import deepcopy
from dataclasses import replace, asdict
from unittest import mock
from pathlib import Path, PurePosixPath

from repository_tools import release_distribution as DISTRIBUTION
from repository_tools.release_distribution import (
    BUNDLE_SCHEMA,
    BUNDLE_SCHEMA_V2,
    ReleaseDistributionError,
    bind_distribution,
    checksum_manifest_bytes,
    create_manifest,
    read_bundle_manifest,
    validate_distribution_block,
    validate_record_distribution,
)
from tests.git_support import git
from tests.root_identity_support import load_module
from tests.artifact_support import write
from tests import test_dashboard_publication as dashboard_tests


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / ".github" / "scripts" / "publish_release.py"
RELEASE = load_module(SCRIPT_PATH, "release_orchestration_test_module")

MANIFEST_SCRIPT = REPOSITORY_ROOT / "scripts" / "create_release_bundle_manifest.py"
POLICY_SCRIPT = REPOSITORY_ROOT / "scripts" / "validate_release_distributions.py"
MANIFEST = load_module(MANIFEST_SCRIPT, "release_manifest_test_module")

SURFACE_SCRIPT = REPOSITORY_ROOT / "scripts" / "check_portable_release_surface.py"
SURFACE = load_module(SURFACE_SCRIPT, "portable_release_surface_test_module")


def distribution_values(version: str = "1.2.3") -> dict[str, object]:
    wheel_hash = "1" * 64
    sdist_hash = "2" * 64
    checksum_hash = hashlib.sha256(
        checksum_manifest_bytes(version, wheel_hash, sdist_hash)
    ).hexdigest()
    return {
        "schema": 1,
        "kind": "python-wheel-sdist",
        "source_date_epoch": 1710000000,
        "wheel": f"se_harness-{version}-py3-none-any.whl",
        "wheel_sha256": wheel_hash,
        "sdist": f"se_harness-{version}.tar.gz",
        "sdist_sha256": sdist_hash,
        "checksums": "SHA256SUMS",
        "checksums_sha256": checksum_hash,
        "source_manifest_sha256": "3" * 64,
    }


def plan() -> object:
    values = distribution_values()
    return RELEASE.ReleasePlan(
        schema="se-harness-release-plan/v2",
        repository="mmzen/se_harness",
        release_record="RLS-TST-001",
        release_record_path="docs/engineering/releases/RLS-TST-001.md",
        governance_commit="a" * 40,
        candidate_commit="b" * 40,
        git_object_format="sha1",
        version="1.2.3",
        tag="v1.2.3",
        released_at="2026-08-18T10:00:00Z",
        release_contract="REL-TST-001",
        verification_records=("VREC-TST-001",),
        released_work=("WO-TST-001",),
        source_date_epoch=values["source_date_epoch"],
        wheel=values["wheel"],
        wheel_sha256=values["wheel_sha256"],
        sdist=values["sdist"],
        sdist_sha256=values["sdist_sha256"],
        checksums=values["checksums"],
        checksums_sha256=values["checksums_sha256"],
        source_manifest_sha256=values["source_manifest_sha256"],
    )


class ReleaseArtifactDiscoveryTests(unittest.TestCase):
    """WO-RLO-009: real Git histories distinguish records from retained copies."""

    def setUp(self) -> None:
        self.fixture = dashboard_tests.GitReleaseFixture()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.root = self.fixture.root
        self.distribution = distribution_values()
        self.distribution["source_date_epoch"] = int(git(self.root, "show", "-s", "--format=%ct", self.fixture.candidate))
        self.distribution["source_manifest_sha256"] = DISTRIBUTION.source_manifest_sha256(self.root, self.fixture.candidate)
        self.record = self.fixture.release_record("RLS-TST-001").replace(
            "\n+++\n", "\n[distribution]\n" + "\n".join(
                f"{key} = {json.dumps(value)}" for key, value in self.distribution.items()
            ) + "\n+++\n", 1,
        )
        self.write_live_records()
        self.fixture.commit("add publication provenance")

    def write_live_records(self) -> None:
        write(self.root / self.fixture.record_path, self.record)
        for artifact_id, artifact_type in (
            ("VREC-TST-001", "verification_record"),
            ("WO-TST-001", "work_order"),
            ("REL-TST-001", "release_contract"),
        ):
            write(self.root / f"docs/engineering/release/{artifact_id}.md", self.artifact(artifact_id, artifact_type))

    def artifact(self, artifact_id: str, artifact_type: str) -> str:
        return (f'+++\nid = "{artifact_id}"\ntype = "{artifact_type}"\nstatus = "verified"\n'
                f'commit = "{self.fixture.candidate}"\ngit_object_format = "sha1"\n+++\n')

    def resolve(self):
        return RELEASE.resolve_plan(self.root, "RLS-TST-001", "refs/heads/main")

    def test_maintenance_tag_correction_preserves_distribution_and_evidence(self) -> None:
        self.fixture.maintenance_history(include_tag=False)
        self.distribution["source_date_epoch"] = int(git(self.root, "show", "-s", "--format=%ct", self.fixture.candidate))
        self.distribution["source_manifest_sha256"] = DISTRIBUTION.source_manifest_sha256(self.root, self.fixture.candidate)
        self.record = self.fixture.release_record("RLS-TST-001").replace(
            "\n+++\n", "\n[distribution]\n" + "\n".join(
                f"{key} = {json.dumps(value)}" for key, value in self.distribution.items()
            ) + "\n+++\n", 1,
        )
        complete = self.record
        self.record = self.record.replace('tag = "v1.2.3"\n', "")
        self.write_live_records()
        self.fixture.commit("retain distribution before tag correction")
        git(self.root, "update-ref", "refs/heads/main", "HEAD")
        with self.assertRaisesRegex(RELEASE.ReleaseError, "must declare version and tag"):
            self.resolve()
        self.record = complete
        self.write_live_records()
        self.fixture.commit("record authorized tag correction")
        corrected = git(self.root, "rev-parse", "HEAD")
        git(self.root, "update-ref", "refs/heads/main", corrected)
        result = self.resolve()
        self.assertEqual(corrected, result.governance_commit)
        self.assertEqual(self.fixture.candidate, result.candidate_commit)
        self.assertEqual(self.fixture.evaluator_evidence_sha256, result.evaluator_evidence_sha256)
        self.assertEqual(self.distribution["wheel_sha256"], result.wheel_sha256)
        self.assertEqual(self.distribution["sdist_sha256"], result.sdist_sha256)
        page = RELEASE.dashboard.resolve_release(self.root, "v1.2.3", default_ref="refs/heads/main")
        self.assertEqual(result.governance_commit, page.governance_commit)

    def test_plugin_owned_governance_resolves_the_same_bound_release(self) -> None:
        lock = json.loads(git(self.root, "show", f"{self.fixture.governance}:.engineering-harness.lock"))
        lock.update(schema=4, skill_ownership={"provider": "plugin"})
        git(self.root, "checkout", "-b", "plugin-governance", self.fixture.candidate)
        write(self.root / ".engineering-harness.lock", json.dumps(lock))
        write(self.root / self.fixture.evaluator_evidence_path, self.fixture.evaluator_evidence)
        self.write_live_records()
        self.fixture.commit("integrate release with plugin-owned evaluator")
        governance = git(self.root, "rev-parse", "HEAD")
        git(self.root, "update-ref", "refs/heads/main", governance)
        for result in (self.resolve(), RELEASE.dashboard.resolve_release(
                self.root, "v1.2.3", default_ref="refs/heads/main")):
            self.assertEqual(governance, result.governance_commit)
            self.assertEqual(self.fixture.candidate, result.candidate_commit)
            self.assertEqual(self.fixture.evaluator_evidence_sha256, result.evaluator_evidence_sha256)
        self.assertEqual(self.distribution["wheel_sha256"], self.resolve().wheel_sha256)

    def test_path_boundary_matches_the_validator_without_substring_exclusions(self) -> None:
        from se_harness.engine.validation_core import EXCLUDED_DIRECTORY_NAMES, _is_excluded

        excluded = {"templates", "evidence", ".git", ".idea", "target", "node_modules"}
        self.assertEqual(excluded, EXCLUDED_DIRECTORY_NAMES)
        artifact_root = Path("docs/engineering")
        for directory in excluded:
            for path in (f"docs/engineering/{directory}/record.md",
                         f"docs/engineering/domain/nested/{directory}/record.md"):
                with self.subTest(path=path):
                    self.assertFalse(RELEASE.dashboard._is_artifact_path(path))
                    self.assertTrue(_is_excluded(Path(path), artifact_root))
        for path in ("docs/engineering/flat.md", "docs/engineering/evidence.md",
                     "docs/engineering/domain/evidence-backed/VREC-EVD-001.md",
                     "docs/engineering/domain/mytemplates/record.md"):
            with self.subTest(path=path):
                self.assertTrue(RELEASE.dashboard._is_artifact_path(path))
                self.assertFalse(_is_excluded(Path(path), artifact_root))
        for path in ("docs/engineering-other/record.md", "other/docs/engineering/record.md",
                     "docs/engineering/record.json", "docs/engineering/record.MD"):
            with self.subTest(path=path):
                self.assertFalse(RELEASE.dashboard._is_artifact_path(path))

    def test_excluded_front_matter_is_not_parsed_and_live_evd_ids_remain_visible(self) -> None:
        from se_harness.engine.validation_core import discover_candidate_files

        for directory in ("templates", "evidence", ".idea", "target", "node_modules"):
            base = self.root / f"docs/engineering/domain/{directory}/nested"
            write(base / "copy.md", self.record)
            write(base / "bad.md", '+++\ntype = "release_record"\ninvalid = [\n+++\n')
        live = "docs/engineering/domain/evidence-backed/VREC-EVD-001.md"
        write(self.root / live, self.artifact("VREC-EVD-001", "verification_record"))
        self.fixture.commit("retain copies and malformed test inputs")
        head = git(self.root, "rev-parse", "HEAD")
        expected_paths = sorted(path.relative_to(self.root).as_posix() for path in
                                discover_candidate_files(self.root / "docs/engineering"))
        self.assertEqual(expected_paths, RELEASE.dashboard._tree_markdown_paths(self.root, head))
        catalog = RELEASE._catalog_at(self.root, head)
        self.assertEqual(live, catalog["VREC-EVD-001"][0])
        self.assertEqual(5, len(catalog))
        self.assertEqual(self.fixture.candidate, self.resolve().candidate_commit)

    def test_duplicate_live_catalog_ids_still_refuse(self) -> None:
        duplicate = self.root / "docs/engineering/other/duplicate.md"
        for artifact_id, artifact_type in (("VREC-TST-001", "verification_record"),
                                          ("WO-TST-001", "work_order"),
                                          ("RLS-TST-001", "release_record")):
            with self.subTest(artifact_id=artifact_id):
                write(self.root / "docs/engineering/other/evidence/copy.md", self.artifact(artifact_id, artifact_type))
                write(duplicate, self.artifact(artifact_id, artifact_type))
                self.fixture.commit("duplicate live artifact")
                with self.assertRaisesRegex(RELEASE.ReleaseError, "duplicate artifact ID.*" + artifact_id):
                    RELEASE._catalog_at(self.root, git(self.root, "rev-parse", "HEAD"))

    def test_duplicate_live_release_selection_and_malformed_live_metadata_refuse(self) -> None:
        duplicate = self.root / "docs/engineering/other/releases/duplicate.md"
        write(duplicate, self.record)
        self.fixture.commit("duplicate live release")
        with self.assertRaisesRegex(RELEASE.ReleaseError, "found 2"):
            self.resolve()
        write(duplicate, '+++\ntype = "release_record"\ninvalid = [\n+++\n')
        self.fixture.commit("malformed live record")
        with self.assertRaises(RELEASE.dashboard.PublicationError):
            self.resolve()

    def test_evidence_before_and_after_release_does_not_select_the_history(self) -> None:
        lock = git(self.root, "show", f"{self.fixture.governance}:.engineering-harness.lock")
        git(self.root, "checkout", "-b", "evidence-first", self.fixture.candidate)
        evidence_path = self.root / "docs/engineering/release/evidence/early.md"
        write(evidence_path, self.record)
        self.fixture.commit("retain a released-looking test input before the real record")
        write(self.root / ".engineering-harness.lock", lock + "\n")
        write(self.root / self.fixture.evaluator_evidence_path, self.fixture.evaluator_evidence)
        self.write_live_records()
        self.fixture.commit("integrate real release")
        real_governance = git(self.root, "rev-parse", "HEAD")
        write(evidence_path, self.record + "\nLater observation.\n")
        self.fixture.commit("change the retained copy")
        git(self.root, "update-ref", "refs/heads/main", "HEAD")
        for resolved in (self.resolve(), RELEASE.dashboard.resolve_release(
                self.root, "v1.2.3", default_ref="refs/heads/main")):
            self.assertEqual(real_governance, resolved.governance_commit)
            self.assertEqual(self.fixture.record_path, resolved.release_record_path)

    def test_bound_evidence_is_still_read_and_missing_or_corrupt_bytes_refuse(self) -> None:
        self.assertEqual(self.fixture.evaluator_evidence_sha256, self.resolve().evaluator_evidence_sha256)
        sidecar = self.root / self.fixture.evaluator_evidence_path
        write(sidecar, "{}\n")
        self.fixture.commit("corrupt explicit evidence")
        with self.assertRaisesRegex(RELEASE.dashboard.PublicationError, "evaluator evidence digest differs"):
            self.resolve()
        sidecar.unlink()
        self.fixture.commit("remove explicit evidence")
        with self.assertRaisesRegex(RELEASE.dashboard.PublicationError, "evaluator evidence is unavailable"):
            self.resolve()

    def test_working_tree_edits_do_not_change_committed_resolution(self) -> None:
        expected = self.resolve()
        write(self.root / self.fixture.record_path, "+++\ninvalid = [\n+++\n")
        write(self.root / "docs/engineering/other/duplicate.md", self.record)
        self.assertEqual(expected, self.resolve())

    def test_rehearsal_selector_ignores_evidence_only_records(self) -> None:
        rehearsal_copy = self.record.replace("schema = 1", "schema = 2")
        for status in ("ready", "released"):
            with self.subTest(status=status):
                write(self.root / "docs/engineering/evidence/releases/RLS-TST-999.md",
                      rehearsal_copy.replace('status = "released"', f'status = "{status}"'))
                self.fixture.commit("retain a rehearsable-looking record")
                for ref in (None, "refs/heads/main"):
                    result = RELEASE.select_rehearsal_record(self.root, None, ref)
                    self.assertEqual("", result["release_record"])
                    with self.assertRaisesRegex(RELEASE.ReleaseError, "not a ready or released"):
                        RELEASE.select_rehearsal_record(self.root, "RLS-TST-001", ref)


class DistributionManifestTests(unittest.TestCase):
    def test_portable_wheel_checker_accepts_clean_and_rejects_repository_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            clean = root / "clean.whl"
            with zipfile.ZipFile(clean, "w") as archive:
                archive.writestr("se_harness/cli.py", "print('portable')\n")
                for member in sorted(
                    SURFACE.REQUIRED_QUALIFICATION_MEMBERS
                    | SURFACE.REQUIRED_INTERPRETER_SAFETY_MEMBERS
                ):
                    archive.writestr(member, "{}\n" if member.endswith(".json") else "# portable\n")
            SURFACE.inspect_wheel(clean)

            leaked = root / "leaked.whl"
            with zipfile.ZipFile(leaked, "w") as archive:
                for member in sorted(
                    SURFACE.REQUIRED_QUALIFICATION_MEMBERS
                    | SURFACE.REQUIRED_INTERPRETER_SAFETY_MEMBERS
                ):
                    archive.writestr(member, "{}\n" if member.endswith(".json") else "# portable\n")
                archive.writestr("repository_tools/release_distribution.py", "repository policy\n")
            with self.assertRaisesRegex(SURFACE.SurfaceError, "leaked into wheel"):
                SURFACE.inspect_wheel(leaked)

    def test_active_repository_checker_rejects_retired_evaluator_contracts(self) -> None:
        SURFACE.inspect_repository(REPOSITORY_ROOT)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow = root / ".github" / "workflows" / "publish.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text("steps:\n  - run: harnessctl identity --role governor\n", encoding="utf-8")
            with self.assertRaisesRegex(SURFACE.SurfaceError, "retired specialized lifecycle"):
                SURFACE.inspect_repository(root)

            operator_note = root / "docs" / "notes" / "operator.md"
            operator_note.parent.mkdir(parents=True)
            workflow.unlink()
            operator_note.write_text("Use the retired governor role.\n", encoding="utf-8")
            with self.assertRaisesRegex(SURFACE.SurfaceError, "retired specialized lifecycle"):
                SURFACE.inspect_repository(root)

    def test_manifest_producer_hashes_exact_files_and_candidate_tree(self) -> None:
        commit = git(REPOSITORY_ROOT, "-c", f"safe.directory={REPOSITORY_ROOT.as_posix()}", "rev-parse", "HEAD")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "se_harness-1.2.3-py3-none-any.whl"
            sdist = root / "se_harness-1.2.3.tar.gz"
            wheel.write_bytes(b"wheel")
            sdist.write_bytes(b"sdist")
            with mock.patch.dict(
                "os.environ",
                {
                    "GIT_CONFIG_COUNT": "1",
                    "GIT_CONFIG_KEY_0": "safe.directory",
                    "GIT_CONFIG_VALUE_0": REPOSITORY_ROOT.as_posix(),
                },
                clear=False,
            ):
                result = MANIFEST.create_manifest(
                    REPOSITORY_ROOT,
                    commit,
                    "1.2.3",
                    wheel,
                    sdist,
                    build_recipe=PurePosixPath("release/build-recipe.json"),
                )
        # WO-CIP-007 (SPEC-CIP-003 CIP-ONE-013): every manifest this producer
        # writes binds the candidate's recipe and is schema-2.
        self.assertEqual(BUNDLE_SCHEMA_V2, result["schema"])
        self.assertEqual("release/build-recipe.json", result["build_recipe"])
        self.assertEqual(hashlib.sha256(b"wheel").hexdigest(), result["wheel_sha256"])
        self.assertRegex(result["source_manifest_sha256"], r"\A[0-9a-f]{64}\Z")

    def test_manifest_producer_refuses_to_write_a_schema_1_bundle(self) -> None:
        # SPEC-CIP-003 CIP-ONE-013: there is no writer of a schema-1 bundle manifest.
        # The command refuses before any Git call, and the function refuses the
        # keyword its caller could still pass as None.
        completed = subprocess.run(
            [
                sys.executable,
                str(MANIFEST_SCRIPT),
                "--commit", "0" * 40,
                "--version", "1.2.3",
                "--wheel", "se_harness-1.2.3-py3-none-any.whl",
                "--sdist", "se_harness-1.2.3.tar.gz",
                "--output", "bundle.json",
            ],
            capture_output=True,
            text=True,
            cwd=REPOSITORY_ROOT,
        )
        self.assertEqual(2, completed.returncode, completed.stdout + completed.stderr)
        self.assertIn("--build-recipe", completed.stderr)
        self.assertFalse((REPOSITORY_ROOT / "bundle.json").exists())
        with self.assertRaisesRegex(ReleaseDistributionError, "build recipe"):
            create_manifest(
                REPOSITORY_ROOT,
                "0" * 40,
                "1.2.3",
                REPOSITORY_ROOT / "se_harness-1.2.3-py3-none-any.whl",
                REPOSITORY_ROOT / "se_harness-1.2.3.tar.gz",
                build_recipe=None,
            )

    def test_complete_block_is_valid_and_historical_absence_is_separate(self) -> None:
        result = validate_distribution_block(distribution_values(), "1.2.3")
        self.assertEqual("se_harness-1.2.3-py3-none-any.whl", result.wheel)
        with self.assertRaisesRegex(ReleaseDistributionError, "TOML table"):
            validate_distribution_block(None, "1.2.3")

    def test_partial_unsafe_and_noncanonical_blocks_fail(self) -> None:
        partial = distribution_values()
        partial.pop("sdist_sha256")
        with self.assertRaisesRegex(ReleaseDistributionError, "complete"):
            validate_distribution_block(partial, "1.2.3")
        unsafe = distribution_values()
        unsafe["wheel"] = "../se_harness-1.2.3-py3-none-any.whl"
        with self.assertRaisesRegex(ReleaseDistributionError, "basename"):
            validate_distribution_block(unsafe, "1.2.3")
        wrong = distribution_values()
        wrong["checksums_sha256"] = "0" * 64
        with self.assertRaisesRegex(ReleaseDistributionError, "canonical"):
            validate_distribution_block(wrong, "1.2.3")

    def test_bundle_manifest_binds_version_commit_epoch_and_checksum_bytes(self) -> None:
        values = distribution_values()
        payload = {
            "schema": BUNDLE_SCHEMA,
            "version": "1.2.3",
            "commit": "a" * 40,
            "git_object_format": "sha1",
            **{key: value for key, value in values.items() if key not in {"schema", "kind"}},
            "checksums_content": checksum_manifest_bytes("1.2.3", "1" * 64, "2" * 64).decode("utf-8"),
        }
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bundle.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            result = read_bundle_manifest(
                path,
                version="1.2.3",
                commit="a" * 40,
                git_object_format="sha1",
                source_date_epoch=1710000000,
            )
            self.assertEqual("2" * 64, result.sdist_sha256)
            payload["version"] = "1.2.4"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ReleaseDistributionError, "version"):
                read_bundle_manifest(
                    path,
                    version="1.2.3",
                    commit="a" * 40,
                    git_object_format="sha1",
                    source_date_epoch=1710000000,
                )

    def _binding_repository(self, root: Path) -> tuple[str, dict[str, object], Path]:
        git(root, "init", "-q")
        git(root, "config", "user.name", "Harness Test")
        git(root, "config", "user.email", "harness@example.invalid")
        (root / "source.txt").write_text("candidate\n", encoding="utf-8")
        (root / "release").mkdir()
        shutil.copyfile(REPOSITORY_ROOT / "release" / "build-recipe.json", root / "release" / "build-recipe.json")
        shutil.copyfile(REPOSITORY_ROOT / "release" / "build-toolchain.lock", root / "release" / "build-toolchain.lock")
        git(root, "add", "source.txt", "release")
        git(root, "commit", "-q", "-m", "candidate")
        commit = git(root, "rev-parse", "HEAD")
        wheel = root / "se_harness-1.2.3-py3-none-any.whl"
        sdist = root / "se_harness-1.2.3.tar.gz"
        wheel.write_bytes(b"wheel")
        sdist.write_bytes(b"sdist")
        manifest = create_manifest(
            root,
            commit,
            "1.2.3",
            wheel,
            sdist,
            build_recipe=PurePosixPath("release/build-recipe.json"),
        )
        manifest_path = root / "bundle.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        record = root / "docs/engineering/product/releases/RLS-TST-001.md"
        record.parent.mkdir(parents=True)
        record.write_text(
            f'''+++
id = "RLS-TST-001"
type = "release_record"
title = "Release candidate 1.2.3"
status = "ready"
owners = ["release-owner"]
created = "2026-08-18"
updated = "2026-08-18"
version = "1.2.3"
commit = "{commit}"
git_object_format = "sha1"
released_at = "2026-08-18T10:00:00Z"
authorized_by = "release-owner"
tag = "v1.2.3"

[relations]
satisfies = ["REL-TST-001"]
includes_verification = ["VREC-TST-001"]
releases_work = ["WO-TST-001"]
+++

# Release Record Candidate
''',
            encoding="utf-8",
            newline="\n",
        )
        return commit, manifest, record

    def test_repository_binder_is_exact_replayable_and_preserves_core_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _commit, manifest, record = self._binding_repository(root)
            before = record.read_text(encoding="utf-8")
            path, distribution, changed = bind_distribution(
                root,
                record.relative_to(root),
                Path("bundle.json"),
            )
            self.assertEqual(record, path)
            self.assertTrue(changed)
            self.assertEqual(manifest["wheel_sha256"], distribution.wheel_sha256)
            after = record.read_text(encoding="utf-8")
            self.assertIn("[distribution]", after)
            for core_line in (
                'status = "ready"',
                f"commit = \"{manifest['commit']}\"",
                'tag = "v1.2.3"',
                'satisfies = ["REL-TST-001"]',
            ):
                self.assertIn(core_line, before)
                self.assertIn(core_line, after)
            replay = bind_distribution(root, record.relative_to(root), Path("bundle.json"))
            self.assertFalse(replay[2])
            self.assertEqual(after, record.read_text(encoding="utf-8"))

    def test_repository_binder_rejects_mismatch_and_atomic_replace_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _commit, manifest, record = self._binding_repository(root)
            original = record.read_bytes()
            manifest["version"] = "1.2.4"
            (root / "bundle.json").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ReleaseDistributionError, "version"):
                bind_distribution(root, record.relative_to(root), Path("bundle.json"))
            self.assertEqual(original, record.read_bytes())

            manifest["version"] = "1.2.3"
            (root / "bundle.json").write_text(json.dumps(manifest), encoding="utf-8")
            with mock.patch.object(DISTRIBUTION.os, "replace", side_effect=OSError("injected")):
                with self.assertRaisesRegex(ReleaseDistributionError, "atomically"):
                    bind_distribution(root, record.relative_to(root), Path("bundle.json"))
            self.assertEqual(original, record.read_bytes())
            self.assertEqual([], list(record.parent.glob(f".{record.name}.*")))

    def test_repository_binder_rejects_wrong_tree_identity_and_non_ready_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _commit, manifest, record = self._binding_repository(root)
            original = record.read_bytes()
            manifest["source_manifest_sha256"] = "0" * 64
            (root / "bundle.json").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ReleaseDistributionError, "candidate tree"):
                bind_distribution(root, record.relative_to(root), Path("bundle.json"))
            self.assertEqual(original, record.read_bytes())

            manifest["source_manifest_sha256"] = create_manifest(
                root,
                manifest["commit"],
                "1.2.3",
                root / "se_harness-1.2.3-py3-none-any.whl",
                root / "se_harness-1.2.3.tar.gz",
                build_recipe=PurePosixPath("release/build-recipe.json"),
            )["source_manifest_sha256"]
            (root / "bundle.json").write_text(json.dumps(manifest), encoding="utf-8")
            record.write_text(
                record.read_text(encoding="utf-8").replace('status = "ready"', 'status = "released"'),
                encoding="utf-8",
                newline="\n",
            )
            released = record.read_bytes()
            with self.assertRaisesRegex(ReleaseDistributionError, "ready"):
                bind_distribution(root, record.relative_to(root), Path("bundle.json"))
            self.assertEqual(released, record.read_bytes())

    def test_repository_binder_rejects_manifest_identity_matrix_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _commit, manifest, record = self._binding_repository(root)
            original = record.read_bytes()
            cases = (
                ("commit", "0" * 40, "commit"),
                ("source_date_epoch", int(manifest["source_date_epoch"]) + 1, "epoch"),
                ("wheel", "../se_harness-1.2.3-py3-none-any.whl", "basename"),
                ("checksums_content", "not canonical\n", "canonical"),
                ("build_recipe_sha256", "0" * 64, "candidate tree"),
            )
            for field, value, message in cases:
                with self.subTest(field=field):
                    changed = dict(manifest)
                    changed[field] = value
                    (root / "bundle.json").write_text(json.dumps(changed), encoding="utf-8")
                    with self.assertRaisesRegex(ReleaseDistributionError, message):
                        bind_distribution(root, record.relative_to(root), Path("bundle.json"))
                    self.assertEqual(original, record.read_bytes())

            (root / "bundle.json").write_text(
                '{"schema":"se-harness-release-bundle/v1","schema":"duplicate"}',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ReleaseDistributionError, "duplicate key"):
                bind_distribution(root, record.relative_to(root), Path("bundle.json"))
            self.assertEqual(original, record.read_bytes())

    def test_schema_1_is_historical_released_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            git(root, "init", "-q")
            git(root, "config", "user.name", "Harness Test")
            git(root, "config", "user.email", "harness@example.invalid")
            (root / "source.txt").write_text("historical\n", encoding="utf-8", newline="\n")
            # WO-CIP-007 (CIP-ONE-013): the producer always binds a recipe, so even
            # this historical-record fixture carries one; what is historical here is
            # the record's own [distribution] schema = 1 block, not the manifest.
            (root / "release").mkdir()
            shutil.copyfile(REPOSITORY_ROOT / "release" / "build-recipe.json", root / "release" / "build-recipe.json")
            shutil.copyfile(REPOSITORY_ROOT / "release" / "build-toolchain.lock", root / "release" / "build-toolchain.lock")
            git(root, "add", "source.txt", "release")
            git(root, "commit", "-q", "-m", "historical")
            commit = git(root, "rev-parse", "HEAD")
            wheel = root / "se_harness-1.2.3-py3-none-any.whl"
            sdist = root / "se_harness-1.2.3.tar.gz"
            wheel.write_bytes(b"wheel")
            sdist.write_bytes(b"sdist")
            manifest = create_manifest(
                root,
                commit,
                "1.2.3",
                wheel,
                sdist,
                build_recipe=PurePosixPath("release/build-recipe.json"),
            )
            distribution = validate_distribution_block(
                {
                    "schema": 1,
                    "kind": "python-wheel-sdist",
                    **{
                        key: manifest[key]
                        for key in (
                            "source_date_epoch", "wheel", "wheel_sha256", "sdist", "sdist_sha256",
                            "checksums", "checksums_sha256", "source_manifest_sha256",
                        )
                    },
                },
                "1.2.3",
            )
            record = root / "docs/engineering/releases/RLS-TST-001.md"
            record.parent.mkdir(parents=True)
            record.write_text(
                "+++\n"
                'id = "RLS-TST-001"\n'
                'type = "release_record"\n'
                'status = "released"\n'
                'version = "1.2.3"\n'
                f'commit = "{commit}"\n'
                'git_object_format = "sha1"\n\n'
                f"{distribution.toml()}\n"
                "+++\n",
                encoding="utf-8",
                newline="\n",
            )
            self.assertTrue(validate_record_distribution(root, record, required=True))
            record.write_text(
                record.read_text(encoding="utf-8").replace('status = "released"', 'status = "ready"'),
                encoding="utf-8",
                newline="\n",
            )
            with self.assertRaisesRegex(ReleaseDistributionError, "historical released"):
                validate_record_distribution(root, record, required=True)

    def test_repository_binder_rejects_partial_existing_state_and_unsafe_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _commit, _manifest, record = self._binding_repository(root)
            partial = record.read_text(encoding="utf-8").replace(
                "[relations]",
                "[distribution]\nschema = 1\n\n[relations]",
            )
            record.write_text(partial, encoding="utf-8", newline="\n")
            original = record.read_bytes()
            with self.assertRaisesRegex(ReleaseDistributionError, "complete"):
                bind_distribution(root, record.relative_to(root), Path("bundle.json"))
            self.assertEqual(original, record.read_bytes())
            with self.assertRaisesRegex(ReleaseDistributionError, "repository-relative"):
                bind_distribution(root, record, Path("bundle.json"))
            self.assertEqual(original, record.read_bytes())

    def test_repository_policy_validator_rechecks_bound_candidate_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _commit, manifest, record = self._binding_repository(root)
            bind_distribution(root, record.relative_to(root), Path("bundle.json"))
            self.assertTrue(validate_record_distribution(root, record, required=True))
            text = record.read_text(encoding="utf-8")
            record.write_text(
                text.replace(str(manifest["source_manifest_sha256"]), "0" * 64, 1),
                encoding="utf-8",
                newline="\n",
            )
            with self.assertRaisesRegex(ReleaseDistributionError, "candidate tree"):
                validate_record_distribution(root, record, required=True)

    def test_repository_policy_cli_requires_selected_record_distribution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _commit, _manifest, record = self._binding_repository(root)
            command = [
                sys.executable,
                str(POLICY_SCRIPT),
                "--root",
                str(root),
                "--require-record",
                "RLS-TST-001",
            ]
            missing = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(1, missing.returncode)
            self.assertIn("no distribution provenance", missing.stderr)
            bind_distribution(root, record.relative_to(root), Path("bundle.json"))
            exact = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(0, exact.returncode, exact.stderr)
            self.assertIn("PASS (1 distribution-bearing record)", exact.stdout)


class ReleaseStateTests(unittest.TestCase):
    def test_exact_bundle_and_any_extra_file_are_distinguished(self) -> None:
        selected = plan()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / selected.wheel).write_bytes(b"wheel")
            (root / selected.sdist).write_bytes(b"sdist")
            selected = RELEASE.ReleasePlan(
                **{
                    **RELEASE.asdict(selected),
                    "verification_records": selected.verification_records,
                    "released_work": selected.released_work,
                    "wheel_sha256": hashlib.sha256(b"wheel").hexdigest(),
                    "sdist_sha256": hashlib.sha256(b"sdist").hexdigest(),
                    "checksums_sha256": hashlib.sha256(
                        checksum_manifest_bytes(
                            selected.version,
                            hashlib.sha256(b"wheel").hexdigest(),
                            hashlib.sha256(b"sdist").hexdigest(),
                        )
                    ).hexdigest(),
                }
            )
            (root / selected.checksums).write_bytes(
                checksum_manifest_bytes(selected.version, selected.wheel_sha256, selected.sdist_sha256)
            )
            self.assertEqual("exact", RELEASE.verify_bundle(selected, root)["state"])
            (root / "unexpected.txt").write_text("no", encoding="utf-8")
            with self.assertRaisesRegex(RELEASE.ReleaseError, "file set"):
                RELEASE.verify_bundle(selected, root)

    def test_github_required_assets_allow_partial_drafts_and_unrelated_attachments(self) -> None:
        selected = plan()
        assets = [
            {"name": selected.wheel, "digest": f"sha256:{selected.wheel_sha256}"},
            {"name": selected.sdist, "digest": f"sha256:{selected.sdist_sha256}"},
            {"name": selected.checksums, "digest": f"sha256:{selected.checksums_sha256}"},
        ]
        metadata = {"tagName": selected.tag, "isDraft": True, "isPrerelease": False, "assets": assets}
        result = RELEASE.classify_github(selected, metadata)
        self.assertEqual("exact", result["state"])
        self.assertTrue(result["draft"])
        metadata["assets"] = []
        self.assertEqual("partial", RELEASE.classify_github(selected, metadata)["state"])
        metadata["assets"] = assets[:1]
        partial = RELEASE.classify_github(selected, metadata)
        self.assertEqual("partial", partial["state"])
        self.assertEqual(sorted([selected.sdist, selected.checksums]), partial["missing"])
        metadata["assets"] = assets + [{"name": "screenshot.png"}]
        self.assertEqual("exact", RELEASE.classify_github(selected, metadata)["state"])
        metadata["assets"][0] = {"name": selected.wheel, "digest": "sha256:" + "0" * 64}
        self.assertEqual("mismatched", RELEASE.classify_github(selected, metadata)["state"])

    def make_github_bundle(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        root = Path(scratch.name)
        selected = plan()
        wheel_hash, sdist_hash = hashlib.sha256(b"wheel").hexdigest(), hashlib.sha256(b"sdist").hexdigest()
        checksums = checksum_manifest_bytes(selected.version, wheel_hash, sdist_hash)
        selected = RELEASE.ReleasePlan(**{**RELEASE.asdict(selected), "wheel_sha256": wheel_hash,
            "sdist_sha256": sdist_hash, "checksums_sha256": hashlib.sha256(checksums).hexdigest()})
        for name, content in [(selected.wheel, b"wheel"), (selected.sdist, b"sdist"), (selected.checksums, checksums)]:
            (root / name).write_bytes(content)
        metadata = {"tagName": selected.tag, "isDraft": True, "isPrerelease": False,
                    "assets": [{"name": selected.wheel, "digest": "sha256:" + wheel_hash}, {"name": "screenshot.png"}]}
        return root, selected, metadata

    def test_interrupted_upload_resumes_only_missing_assets(self) -> None:
        root, selected, metadata = self.make_github_bundle()
        uploaded = []
        interrupted = False
        def upload(argv, **kwargs):
            nonlocal interrupted
            self.assertEqual(["gh", "release", "upload", selected.tag], argv[:4])
            self.assertNotIn("--clobber", argv)
            path = Path(argv[4])
            if path.name == selected.sdist and not interrupted:
                interrupted = True
                return subprocess.CompletedProcess(argv, 1, "", "interrupted")
            uploaded.append(path.name)
            metadata["assets"].append({"name": path.name, "digest": "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()})
            return subprocess.CompletedProcess(argv, 0, "", "")
        with mock.patch.object(RELEASE.subprocess, "run", side_effect=upload):
            with self.assertRaisesRegex(RELEASE.ReleaseError, "upload failed"):
                RELEASE.resume_github(selected, root, metadata)
            self.assertEqual([selected.checksums], uploaded)
            self.assertEqual([selected.sdist], RELEASE.resume_github(selected, root, metadata)["uploaded"])
            metadata["isDraft"] = False
            self.assertEqual([], RELEASE.resume_github(selected, root, metadata)["uploaded"])
        self.assertEqual([selected.checksums, selected.sdist], uploaded)

    def test_resume_refuses_published_partial_or_conflicting_required_asset(self) -> None:
        root, selected, metadata = self.make_github_bundle()
        with mock.patch.object(RELEASE.subprocess, "run") as upload:
            metadata["isDraft"] = False
            with self.assertRaisesRegex(RELEASE.ReleaseError, "unpublished draft"):
                RELEASE.resume_github(selected, root, metadata)
            metadata["isDraft"] = True
            metadata["assets"][0]["digest"] = "sha256:" + "0" * 64
            with self.assertRaisesRegex(RELEASE.ReleaseError, "mismatched"):
                RELEASE.resume_github(selected, root, metadata)
            upload.assert_not_called()

    def test_result_keeps_stages_and_denies_lifecycle_authority(self) -> None:
        stages = {"resolution": {"state": "exact"}, "github": {"state": "failed"}}
        result = RELEASE.release_result(plan(), stages)
        self.assertEqual("se-harness-release-result/v1", result["schema"])
        self.assertEqual("not_run", result["stages"]["pypi"]["state"])
        self.assertIn("no formal lifecycle transition", result["authority"])


class CompleteReleaseTests(unittest.TestCase):
    """ONE02/04/05/06/07: inert Git payloads and an independently fixed provider model."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.value = json.loads((REPOSITORY_ROOT/'tests/fixtures/release_delivery/complete-release/plan.json').read_text())
        self.envelope = {'plan': self.value, 'sha256': 'f'*64, 'decided_by': 'Example human',
                         'decision_reference': 'synthetic approval only', 'path': 'plan.json', 'review_commit': 'a'*40}
        self.selected = replace(plan(), schema='se-harness-release-plan/v3', complete_delivery=self.envelope)
        self.latest = 'v1.2.2'
        self.last = 'd'*40
        self.market = 'd'*40
        self.calls = []
        self.pushes = []
        self.ready = {'status': 'ready_for_markers', 'plan_sha256': 'f'*64}

    def request(self, method, path, payload):
        self.calls.append((method, path, payload))
        suffix = path.split('/repos/mmzen/se_harness/', 1)[1]
        values = {
            'releases/tags/v1.2.3': {'id': 7, 'tag_name': 'v1.2.3', 'draft': False, 'prerelease': False},
            'releases/latest': {'tag_name': self.latest} if self.latest else None,
            'git/ref/tags/last': {'ref':'refs/tags/last','object':{'type':'commit','sha':self.last}} if self.last else None,
            'git/ref/heads/plugin-marketplace': {'ref':'refs/heads/plugin-marketplace','object':{'type':'commit','sha':self.market}} if self.market else None,
            'environments/pypi': {'protection_rules':[{'type':'branch_policy'}],
                                  'deployment_branch_policy':{'protected_branches':False,'custom_branch_policies':True}},
            'environments/pypi/deployment-branch-policies': {'branch_policies':[{'name':'main','type':'branch'}]},
        }
        if method == 'PATCH' and suffix == 'releases/7':
            self.assertEqual({'make_latest':'true'}, payload)
            self.latest = 'v1.2.3'
            return RELEASE.maintenance.ApiResponse(200, {})
        self.assertEqual('GET', method)
        self.assertIn(suffix, values)
        value = values[suffix]
        return RELEASE.maintenance.ApiResponse(404 if value is None else 200, value)

    def push(self, ref, target, expected, moving):
        self.pushes.append((ref,target,expected,moving))
        if ref == 'refs/tags/last':
            self.assertEqual(self.last, expected)
            self.assertTrue(moving)
            self.last = target
        else:
            self.assertEqual('refs/heads/plugin-marketplace', ref)
            self.assertEqual(self.market, expected)
            self.assertFalse(moving)
            self.market = target

    def make_marketplace(self):
        git(self.root, 'init', '-b', 'main')
        git(self.root, 'config', 'user.name', 'Fixture')
        git(self.root, 'config', 'user.email', 'fixture@example.invalid')
        write(self.root/'old.txt', 'previous marketplace')
        git(self.root, 'add', '.')
        git(self.root, 'commit', '-m', 'previous marketplace')
        parent = git(self.root, 'rev-parse', 'HEAD')
        (self.root/'old.txt').unlink()
        files = {}
        wheel = b'inert approved wheel fixture'
        wheel_hash = hashlib.sha256(wheel).hexdigest()
        for host, label in [('codex','codex'),('claude','claude-code')]:
            prefix = f'packages/{host}/verity-plane/'
            for path, raw in [(prefix+'packages/'+self.selected.wheel,wheel), (prefix+'assembly-inventory.json', (host+' inventory').encode())]:
                target = self.root/path
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(raw)
                files[path] = hashlib.sha256(raw).hexdigest()
            self.value['surfaces'][1]['expected'][label+'_content_sha256'] = files[prefix+'assembly-inventory.json']
        identity = {'name':'verity-plane','plugin_version':'0.2.1','source':{'revision':self.selected.candidate_commit},
                    'evaluator':{'version':'1.2.3','candidate_commit':self.selected.candidate_commit,'archive_sha256':wheel_hash},'files':files}
        raw = json.dumps(identity).encode()
        (self.root/'PACKAGE-IDENTITY.json').write_bytes(raw)
        git(self.root,'add','.')
        git(self.root,'commit','-m','prepared inert payload')
        target = git(self.root,'rev-parse','HEAD')
        self.value['complete_release']['marketplace'] = {'parent':parent,'commit':target,
               'tree':git(self.root,'rev-parse','HEAD^{tree}'),'identity_sha256':hashlib.sha256(raw).hexdigest()}
        self.value['surfaces'][1]['expected']['public_revision'] = target
        self.selected = replace(self.selected,wheel_sha256=wheel_hash)
        self.market = parent
        public = self.root/self.selected.wheel
        public.write_bytes(wheel)
        return public

    def test_marketplace_promotes_approved_bytes_then_replays_without_writing(self):
        public = self.make_marketplace()
        result = RELEASE.promote_marketplace(self.root,self.selected,public,self.request,self.push,apply=True)
        self.assertEqual('exact',result['state'])
        self.assertEqual(1,len(self.pushes))
        RELEASE.promote_marketplace(self.root,self.selected,public,self.request,self.push,apply=True)
        self.assertEqual(1,len(self.pushes))
        public.write_bytes(b'different public wheel')
        with self.assertRaisesRegex(RELEASE.ReleaseError,'public wheel'):
            RELEASE.promote_marketplace(self.root,self.selected,public,self.request,self.push,apply=True)
        self.assertEqual(1,len(self.pushes))

    def test_marketplace_ref_conflict_and_uncertain_write_are_not_repeated(self):
        public = self.make_marketplace()
        self.market = 'e'*40
        with self.assertRaisesRegex(RELEASE.ReleaseError,'unexpected ref'):
            RELEASE.promote_marketplace(self.root,self.selected,public,self.request,self.push,apply=True)
        self.assertFalse(self.pushes)
        self.market = self.value['complete_release']['marketplace']['parent']
        def interrupted(*args):
            self.push(*args)
            raise OSError('transport lost after remote accepted write')
        with self.assertRaises(OSError):
            RELEASE.promote_marketplace(self.root,self.selected,public,self.request,interrupted,apply=True)
        RELEASE.promote_marketplace(self.root,self.selected,public,self.request,self.push,apply=True)
        self.assertEqual(1,len(self.pushes))

    def test_changed_parent_inventory_and_extra_file_refuse_without_remote_writes(self):
        public = self.make_marketplace()
        for field in ('parent','tree','identity_sha256'):
            original = self.value['complete_release']['marketplace'][field]
            self.value['complete_release']['marketplace'][field] = '0'*len(original)
            with self.assertRaises(RELEASE.ReleaseError):
                RELEASE.promote_marketplace(self.root,self.selected,public,self.request,self.push,apply=True)
            self.value['complete_release']['marketplace'][field] = original
        self.assertFalse(self.calls)
        self.assertFalse(self.pushes)

    def test_markers_wait_for_all_checks_and_reject_legacy(self):
        self.market = 'c'*40
        for assessment in ({'status':'incomplete','plan_sha256':'f'*64}, {'status':'ready_for_markers','plan_sha256':'0'*64}):
            with self.assertRaisesRegex(RELEASE.ReleaseError,'incomplete'):
                RELEASE.promote_markers(self.selected,assessment,self.request,self.push,apply=True)
        with self.assertRaisesRegex(RELEASE.ReleaseError,'no complete-release'):
            RELEASE.promote_markers(plan(),self.ready,self.request,self.push,apply=True)
        self.assertFalse(self.calls)
        self.assertFalse(self.pushes)

    def test_marker_resume_after_each_boundary_keeps_one_approval(self):
        self.market = 'c'*40
        # Crash after latest changes: the next run must leave latest alone.
        def interrupted(ref, target, expected, moving):
            raise OSError('last not written')
        with self.assertRaises(OSError):
            RELEASE.promote_markers(self.selected,self.ready,self.request,interrupted,apply=True)
        self.assertEqual('v1.2.3',self.latest)
        result = RELEASE.promote_markers(self.selected,self.ready,self.request,self.push,apply=True)
        self.assertEqual(('exact','exact'),(result['latest'],result['last']))
        RELEASE.promote_markers(self.selected,self.ready,self.request,self.push,apply=True)
        self.assertEqual(1,len([c for c in self.calls if c[0]=='PATCH']))
        self.assertEqual(1,len(self.pushes))

    def test_marker_conflict_unknown_or_moved_marketplace_stops_before_writes(self):
        self.market = 'c'*40
        for key in ('latest','last','market'):
            old = getattr(self,key)
            setattr(self,key,'e'*40)
            with self.assertRaises(RELEASE.ReleaseError):
                RELEASE.promote_markers(self.selected,self.ready,self.request,self.push,apply=True)
            setattr(self,key,old)
        def unknown(*args): return RELEASE.maintenance.ApiResponse(503,{})
        with self.assertRaisesRegex(RELEASE.ReleaseError,'unknown result'):
            RELEASE.promote_markers(self.selected,self.ready,unknown,self.push,apply=True)
        self.assertFalse(self.pushes)
        self.assertFalse([c for c in self.calls if c[0]=='PATCH'])

    def test_provider_control_changes_do_not_become_approval_prompts(self):
        self.assertEqual('main',RELEASE.controls_snapshot(self.request)['allowed_ref'])
        original = self.request
        def guarded(method,path,payload):
            response = original(method,path,payload)
            if path.endswith('/pypi'):
                response.payload['protection_rules'].append({'type':'required_reviewers','reviewers':[{'type':'User','id':1}]})
            return response
        with self.assertRaisesRegex(RELEASE.ReleaseError,'activation is not ready'):
            RELEASE.controls_snapshot(guarded)
        self.assertFalse([c for c in self.calls if c[0]!='GET'])

    def test_unknown_github_state_is_not_absence(self):
        for tag_only in (True,False):
            for status in (401,403,429,500,503):
                with self.subTest(tag_only=tag_only,status=status):
                    request=lambda *args: RELEASE.maintenance.ApiResponse(status,{})
                    with self.assertRaisesRegex(RELEASE.ReleaseError,'unknown result'):
                        RELEASE.observe_github(self.selected,request,tag_only=tag_only)
        request=lambda *args: RELEASE.maintenance.ApiResponse(404,{})
        self.assertEqual({'state':'absent'},RELEASE.observe_github(self.selected,request,tag_only=True))
        self.assertEqual({'absent':True},RELEASE.observe_github(self.selected,request))

    def test_legacy_plan_read_and_new_result_never_infer_full_delivery(self):
        old = asdict(plan())
        old.pop('complete_delivery')
        path = self.root/'old-plan.json'
        path.write_text(json.dumps(old))
        self.assertIsNone(RELEASE.read_plan(path).complete_delivery)
        old['complete_delivery'] = self.envelope
        path.write_text(json.dumps(old))
        with self.assertRaisesRegex(RELEASE.ReleaseError,'legacy'):
            RELEASE.read_plan(path)
        result = RELEASE.release_result(self.selected,{n:{'state':'exact'} for n in ('resolution','qualification','github','pypi','pages','public_install')})
        self.assertEqual('incomplete',result['delivery'])
        self.assertEqual('not_run',result['stages']['marketplace']['state'])

    def test_only_the_recorded_decision_can_change_in_integration(self):
        git(self.root,'init','-b','main')
        git(self.root,'config','user.name','Fixture')
        git(self.root,'config','user.email','fixture@example.invalid')
        path = self.value['complete_release']['integration']['decision_paths'][0]
        ready = '+++\nid="RLS-TST-001"\nstatus="ready"\nversion="1.2.3"\n+++\n\nFixed body\n'
        write(self.root/path,ready)
        git(self.root,'add','.')
        git(self.root,'commit','-m','reviewed content')
        base = git(self.root,'rev-parse','HEAD')
        released = ready.replace('status="ready"','status="released"').replace('\n+++\n','\n[[lifecycle_events]]\nfrom="ready"\nto="released"\ndecided_by="Example human"\n+++\n')
        write(self.root/path,released)
        git(self.root,'add','.')
        git(self.root,'commit','-m','record decision')
        head = git(self.root,'rev-parse','HEAD')
        self.assertEqual([path],RELEASE.verify_integration(self.root,base,head,self.envelope))
        write(self.root/path,released.replace('1.2.3','1.2.4'))
        git(self.root,'add','.')
        git(self.root,'commit','-m','wrong version')
        with self.assertRaisesRegex(RELEASE.ReleaseError,'accepted artifact content'):
            RELEASE.verify_integration(self.root,base,git(self.root,'rev-parse','HEAD'),self.envelope)

    def test_resolver_binds_one_real_git_review_and_refuses_later_plan_changes(self):
        fixture = dashboard_tests.GitReleaseFixture()
        fixture.setUp()
        self.addCleanup(fixture.tearDown)
        self.selected = replace(self.selected,candidate_commit=fixture.candidate)
        self.make_marketplace()
        market = self.value['complete_release']['marketplace']
        git(fixture.root,'fetch',str(self.root),market['commit'])
        lock = git(fixture.root,'show',fixture.governance+':.engineering-harness.lock')
        git(fixture.root,'checkout','-b','complete-route',fixture.candidate)
        write(fixture.root/'.engineering-harness.lock',lock)
        write(fixture.root/fixture.evaluator_evidence_path,fixture.evaluator_evidence)
        value = self.value
        value['release']['wheel_sha256'] = self.selected.wheel_sha256
        value['complete_release']['candidate_commit'] = fixture.candidate
        value['complete_release']['integration']['decision_paths'] = [fixture.record_path]
        value['complete_release']['documentation'] = {'README.md':hashlib.sha256(b'candidate\n').hexdigest()}
        value['surfaces'][0]['expected']['wheel_sha256'] = self.selected.wheel_sha256
        value['surfaces'][1]['expected'].update(source_commit=fixture.candidate,wheel_sha256=self.selected.wheel_sha256)
        value['surfaces'][2]['expected']['commit'] = fixture.candidate
        value['surfaces'][4]['expected']['last'] = fixture.candidate
        readiness = {'candidate_commit':fixture.candidate,'controls_ready':True,'qualification':'passed','verification_records':['VREC-TST-001']}
        readiness_raw = json.dumps(readiness)+'\n'
        value['complete_release']['readiness']['sha256'] = hashlib.sha256(readiness_raw.encode()).hexdigest()
        write(fixture.root/value['complete_release']['readiness']['path'],readiness_raw)
        plan_path = 'docs/engineering/example/evidence/release/plan.json'
        raw = json.dumps(value)+'\n'
        write(fixture.root/plan_path,raw)
        distribution = distribution_values()
        distribution.update(wheel_sha256=self.selected.wheel_sha256,
           checksums_sha256=hashlib.sha256(checksum_manifest_bytes('1.2.3',self.selected.wheel_sha256,distribution['sdist_sha256'])).hexdigest(),
           source_date_epoch=int(git(fixture.root,'show','-s','--format=%ct',fixture.candidate)),
           source_manifest_sha256=DISTRIBUTION.source_manifest_sha256(fixture.root,fixture.candidate))
        ready = fixture.release_record('RLS-TST-001').replace('status = "released"','status = "ready"')
        ready = ready.replace('\n+++\n','\n[distribution]\n'+'\n'.join(f'{k} = {json.dumps(v)}' for k,v in distribution.items())+'\n+++\n',1)
        write(fixture.root/fixture.record_path,ready)
        for artifact_id, artifact_type in [('REL-TST-001','release_contract'),('WO-TST-001','work_order'),('VREC-TST-001','verification_record')]:
            extra = '\n[delivery]\nroute="complete-release"\n' if artifact_type=='release_contract' else ''
            write(fixture.root/f'docs/engineering/example/{artifact_id}.md',f'+++\nid="{artifact_id}"\ntype="{artifact_type}"\nstatus="verified"\ncommit="{fixture.candidate}"\ngit_object_format="sha1"\n{extra}+++\n')
        fixture.commit('prepared and reviewed complete package')
        review = git(fixture.root,'rev-parse','HEAD')
        binding = {'plan':plan_path,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'decided_by':'Example human',
                   'decision_reference':'synthetic fixture approval','review_commit':review}
        released = ready.replace('status = "ready"','status = "released"').replace('authorized_by = "release-owner"', 'authorized_by = "Example human"').replace('\n+++\n',
            '\n[delivery]\n'+'\n'.join(f'{k}={json.dumps(v)}' for k,v in binding.items())+
            '\n[[lifecycle_events]]\nfrom="ready"\nto="released"\ndecided_by="Example human"\n+++\n',1)
        write(fixture.root/fixture.record_path,released)
        fixture.commit('apply one complete release decision')
        git(fixture.root,'update-ref','refs/heads/main','HEAD')
        resolved = RELEASE.resolve_plan(fixture.root,'RLS-TST-001','refs/heads/main')
        self.assertEqual('se-harness-release-plan/v3',resolved.schema)
        self.assertEqual(binding['sha256'],resolved.complete_delivery['sha256'])
        self.assertEqual(market['commit'],resolved.complete_delivery['plan']['complete_release']['marketplace']['commit'])
        (fixture.root/plan_path).write_bytes((' '+raw).encode())
        fixture.commit('unauthorized byte change after approval')
        git(fixture.root,'update-ref','refs/heads/main','HEAD')
        with self.assertRaisesRegex(RELEASE.ReleaseError,'plan digest differs'):
            RELEASE.resolve_plan(fixture.root,'RLS-TST-001','refs/heads/main')


class ReleaseWorkflowPolicyTests(unittest.TestCase):
    """The lane definitions and the resolver script read as text (TST-HYG-011): SPEC-REB-013 rules 4
    to 6 fix the publication, Pages and dashboard-publisher surfaces, SPEC-DPG-001 rule 8 the Pages
    definition."""

    @classmethod
    def setUpClass(cls) -> None:
        workflows = REPOSITORY_ROOT / ".github" / "workflows"
        cls.workflow = (workflows / "publish-pypi.yml").read_text(encoding="utf-8")
        cls.pages = (workflows / "publish-dashboard-pages.yml").read_text(encoding="utf-8")
        cls.qualification = (workflows / "release-qualification.yml").read_text(encoding="utf-8")
        cls.pages_definition = (workflows / "pages-publication.yml").read_text(encoding="utf-8")
        cls.resolver = (REPOSITORY_ROOT / ".github" / "scripts" / "publish_release.py").read_text(encoding="utf-8")

    def test_normal_workflow_has_one_main_only_input_and_stable_publisher_identity(self) -> None:
        self.assertIn("      release_record:\n", self.workflow)
        self.assertEqual(1, self.workflow.count("        required: true\n"))
        self.assertNotIn("      tag:\n", self.workflow)
        self.assertIn("github.ref == 'refs/heads/main'", self.workflow)
        self.assertIn("      name: pypi\n", self.workflow)
        self.assertIn("pypa/gh-action-pypi-publish@dc37677b2e1c63e2034f94d8a5b11f265b73ba33", self.workflow)

    def test_complete_delivery_is_explicit_and_never_executes_candidate_with_credentials(self):
        market = self.workflow.split('  marketplace:\n',1)[1].split('  observe:\n',1)[0]
        finish = self.workflow.split('  complete_delivery:\n',1)[1]
        self.assertIn("needs.resolve.outputs.complete_delivery == 'true'",market)
        self.assertIn('needs: [resolve, pypi]',market)
        self.assertIn('ref: main',market)
        self.assertIn('--stage marketplace --public-wheel',market)
        for forbidden in ('pip install','check-stage','build_plugin_marketplace','id-token: write','secrets.'):
            self.assertNotIn(forbidden,market)
        self.assertIn("needs.observe.outputs.public_result == 'success'",finish)
        self.assertIn('--stage markers --apply',finish)
        self.assertIn('--stage report',finish)

    def test_candidate_and_privileged_jobs_are_separate(self) -> None:
        # WO-CIP-002: the qualification is one reusable definition invoked here and by the
        # rehearsal; the release workflow's qualify job is a caller with no steps of its own.
        qualify = self.workflow.split("  qualify:\n", 1)[1].split("  github_release:\n", 1)[0]
        github = self.workflow.split("  github_release:\n", 1)[1].split("  pypi:\n", 1)[0]
        pypi = self.workflow.split("  pypi:\n", 1)[1].split("  pages:\n", 1)[0]
        pages = self.workflow.split("  pages:\n", 1)[1].split("  observe:\n", 1)[0]
        self.assertIn("uses: ./.github/workflows/release-qualification.yml", qualify)
        self.assertIn("mode: release-record", qualify)
        self.assertIn("require_status: released", qualify)
        self.assertIn("default_ref: refs/heads/main", qualify)
        for absent in ("steps:", "matrix", "runs-on", "legacy-schema-1", "windows-2022", "contents: write", "id-token: write"):
            self.assertNotIn(absent, qualify)
        definition = self.qualification
        self.assertIn("  workflow_call:\n", definition)
        self.assertIn("python -m se_harness qualify complete-candidate .", definition)
        self.assertIn('--candidate-commit "$CANDIDATE_COMMIT"', definition)
        self.assertIn("complete-candidate-qualification.json", definition)
        self.assertIn('git worktree add --detach "$RUNNER_TEMP/candidate-checkout" "$CANDIDATE_COMMIT"', definition)
        self.assertIn("python scripts/replay_release_build.py", definition)
        self.assertIn('--require-status "$REQUIRE_STATUS"', definition)
        self.assertIn("python -m repository_tools.release_build replay", definition)
        self.assertIn("release qualification is defined for schema-2 (recipe-bound) records only", definition)
        for absent in ("python -m build", "pip install", "normalize_sdist.py", "cygpath", "contents: write", "id-token: write", "secrets", "environment:"):
            self.assertNotIn(absent, definition)
        self.assertEqual(2, definition.count("contents: read"))
        self.assertIn("contents: write", github)
        self.assertNotIn("git archive", github)
        self.assertNotIn("actions/checkout", pypi)
        self.assertNotIn("python -m build", pypi)
        self.assertNotIn("skip-existing", pypi)
        self.assertEqual(1, pypi.count("id-token: write"))
        self.assertIn("uses: ./.github/workflows/pages-publication.yml", pages)
        self.assertIn("uses: ./.github/workflows/pages-publication.yml", self.pages)
        self.assertNotIn("pages_build", self.workflow)
        self.assertEqual(1, self.pages_definition.count('mkdir "$RUNNER_TEMP/generation-snapshot"'))

    def test_repository_policy_is_explicit_and_imported_only_from_trusted_main(self) -> None:
        self.assertIn("Check out trusted main history", self.workflow)
        self.assertIn("python scripts/validate_release_distributions.py", self.workflow)
        self.assertIn("--require-record \"$RELEASE_RECORD\"", self.workflow)
        self.assertIn(
            "from repository_tools.release_distribution import",
            self.resolver,
        )
        self.assertNotIn("from se_harness.release_distribution import", self.resolver)
        self.assertGreaterEqual(self.workflow.count("--release-record"), 2)

    def test_the_publication_path_has_no_predecessor_view_adapter(self) -> None:
        # WO-REB-028: the predecessor-bootstrap release path is retired. No lane names a
        # deleted script, the retired qualification operation, or its evidence artifact.
        combined = self.workflow + self.pages + self.pages_definition + self.qualification
        for absent in (
            "scripts/validate_predecessor_publication_view.py",
            "qualify predecessor-view",
            "predecessor-view-qualification.json",
            "predecessor-publication-result.json",
            "--view-output",
            "--evaluator-entry-point",
            "--evaluator-python",
            '--evaluator-wheel "$RUNNER_TEMP/$EVALUATOR_WHEEL"',
            "pages-predecessor-view",
            # WO-REB-029: the generation snapshot no longer borrows the retired name for
            # its temporary directory, so no lane mentions the retired name at all.
            "predecessor-view",
        ):
            with self.subTest(absent=absent):
                self.assertEqual(0, combined.count(absent))
        # SPEC-REB-013 rule 5: the generation snapshot is the complete governance snapshot,
        # materialized unconditionally at the path the generator invocation names.
        step = self.pages_definition.split(
            "      - name: Materialize the complete governance snapshot for generation", 1
        )[1].split("      - name: ", 1)[0]
        self.assertIn('git -C "$GITHUB_WORKSPACE" worktree add --detach', step)
        self.assertIn('mkdir "$RUNNER_TEMP/generation-snapshot"', step)
        for absent in ("RELEASE_RECORD", "if [", "sparse", "--omit"):
            with self.subTest(absent=absent):
                self.assertNotIn(absent, step)

    def test_public_observation_uses_the_typed_public_install_role(self) -> None:
        combined = self.workflow + self.pages + self.pages_definition
        observe = self.workflow.split("  observe:\n", 1)[1]
        self.assertIn("qualify public-install", observe)
        self.assertIn("--public-wheel-sha256 \"$WHEEL_SHA256\"", observe)
        self.assertIn("--payload-sha256 \"$payload_sha256\"", observe)
        self.assertIn("public-install-qualification.json", observe)
        self.assertNotIn('harnessctl" validate', observe)
        # WO-HUP-017 (SPEC-HUP-017 HUP-ADP-015): the generator is the proven released evaluator's
        # dashboard over the generation snapshot, the form SPEC-DPG-001 rule 8 admits.
        self.assertIn(
            '"$RUNNER_TEMP/evaluator-env/bin/python" -I -m se_harness dashboard',
            self.pages_definition,
        )
        self.assertNotIn(
            'python "$RUNNER_TEMP/generation-snapshot/governance/scripts/generate_harness_dashboard.py"',
            self.pages_definition,
        )
        self.assertNotIn(
            'python "$RUNNER_TEMP/governance/scripts/generate_harness_dashboard.py"',
            combined,
        )
        self.assertNotIn('evaluator-env/bin/harnessctl" validate "$GITHUB_WORKSPACE"', combined)
        self.assertNotIn('evaluator-env/bin/harnessctl" validate "$RUNNER_TEMP/governance"', combined)
        for forbidden in ("--omit", "--expected-error"):
            self.assertNotIn(forbidden, combined)

    def test_pages_recovery_is_main_only_and_has_no_release_event(self) -> None:
        self.assertNotIn("  release:\n", self.pages)
        self.assertNotIn("      release_tag:\n", self.pages)
        self.assertIn("      release_record:\n", self.pages)
        self.assertIn("      governance_commit:\n", self.pages)
        self.assertIn("github.ref == 'refs/heads/main'", self.pages)


if __name__ == "__main__":
    unittest.main()
