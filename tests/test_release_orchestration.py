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

    def test_github_exact_draft_is_replayable_but_partial_is_not(self) -> None:
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
        self.assertEqual("partial", RELEASE.classify_github(selected, metadata)["state"])

    def test_result_keeps_stages_and_denies_lifecycle_authority(self) -> None:
        stages = {"resolution": {"state": "exact"}, "github": {"state": "failed"}}
        result = RELEASE.release_result(plan(), stages)
        self.assertEqual("se-harness-release-result/v1", result["schema"])
        self.assertEqual("not_run", result["stages"]["pypi"]["state"])
        self.assertIn("no formal lifecycle transition", result["authority"])


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
