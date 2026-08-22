from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from unittest import mock
from pathlib import Path

from repository_tools import release_distribution as DISTRIBUTION
from repository_tools.release_distribution import (
    BUNDLE_SCHEMA,
    ReleaseDistributionError,
    bind_distribution,
    checksum_manifest_bytes,
    create_manifest,
    read_bundle_manifest,
    validate_distribution_block,
    validate_record_distribution,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / ".github" / "scripts" / "publish_release.py"
SPEC = importlib.util.spec_from_file_location("release_orchestration_test_module", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load release orchestration module")
RELEASE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RELEASE
SPEC.loader.exec_module(RELEASE)

MANIFEST_SCRIPT = REPOSITORY_ROOT / "scripts" / "create_release_bundle_manifest.py"
POLICY_SCRIPT = REPOSITORY_ROOT / "scripts" / "validate_release_distributions.py"
MANIFEST_SPEC = importlib.util.spec_from_file_location("release_manifest_test_module", MANIFEST_SCRIPT)
if MANIFEST_SPEC is None or MANIFEST_SPEC.loader is None:
    raise RuntimeError("cannot load release manifest module")
MANIFEST = importlib.util.module_from_spec(MANIFEST_SPEC)
sys.modules[MANIFEST_SPEC.name] = MANIFEST
MANIFEST_SPEC.loader.exec_module(MANIFEST)

SURFACE_SCRIPT = REPOSITORY_ROOT / "scripts" / "check_portable_release_surface.py"
SURFACE_SPEC = importlib.util.spec_from_file_location("portable_release_surface_test_module", SURFACE_SCRIPT)
if SURFACE_SPEC is None or SURFACE_SPEC.loader is None:
    raise RuntimeError("cannot load portable release surface module")
SURFACE = importlib.util.module_from_spec(SURFACE_SPEC)
sys.modules[SURFACE_SPEC.name] = SURFACE
SURFACE_SPEC.loader.exec_module(SURFACE)


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
        schema="se-harness-release-plan/v1",
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


class DistributionManifestTests(unittest.TestCase):
    def test_portable_wheel_checker_accepts_clean_and_rejects_repository_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            clean = root / "clean.whl"
            with zipfile.ZipFile(clean, "w") as archive:
                archive.writestr("se_harness/cli.py", "print('portable')\n")
            SURFACE.inspect_wheel(clean)

            leaked = root / "leaked.whl"
            with zipfile.ZipFile(leaked, "w") as archive:
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
        commit = subprocess.run(
            ["git", "-c", f"safe.directory={REPOSITORY_ROOT.as_posix()}", "-C", str(REPOSITORY_ROOT), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
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
                result = MANIFEST.create_manifest(REPOSITORY_ROOT, commit, "1.2.3", wheel, sdist)
        self.assertEqual(BUNDLE_SCHEMA, result["schema"])
        self.assertEqual(hashlib.sha256(b"wheel").hexdigest(), result["wheel_sha256"])
        self.assertRegex(result["source_manifest_sha256"], r"\A[0-9a-f]{64}\Z")

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
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Harness Test"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "harness@example.invalid"], check=True)
        (root / "source.txt").write_text("candidate\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "source.txt"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "candidate"], check=True)
        commit = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        wheel = root / "se_harness-1.2.3-py3-none-any.whl"
        sdist = root / "se_harness-1.2.3.tar.gz"
        wheel.write_bytes(b"wheel")
        sdist.write_bytes(b"sdist")
        manifest = create_manifest(root, commit, "1.2.3", wheel, sdist)
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

    def test_pypi_absent_exact_partial_and_mismatch_are_explicit(self) -> None:
        selected = plan()
        self.assertEqual("absent", RELEASE.classify_pypi(selected, {"absent": True})["state"])
        exact = {
            "urls": [
                {"filename": selected.wheel, "digests": {"sha256": selected.wheel_sha256}},
                {"filename": selected.sdist, "digests": {"sha256": selected.sdist_sha256}},
            ]
        }
        self.assertEqual("exact", RELEASE.classify_pypi(selected, exact)["state"])
        self.assertEqual("partial", RELEASE.classify_pypi(selected, {"urls": exact["urls"][:1]})["state"])
        exact["urls"][0]["digests"]["sha256"] = "9" * 64
        self.assertEqual("mismatched", RELEASE.classify_pypi(selected, exact)["state"])

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
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = (REPOSITORY_ROOT / ".github" / "workflows" / "publish-pypi.yml").read_text(encoding="utf-8")
        cls.pages = (REPOSITORY_ROOT / ".github" / "workflows" / "publish-dashboard-pages.yml").read_text(encoding="utf-8")
        cls.resolver = (REPOSITORY_ROOT / ".github" / "scripts" / "publish_release.py").read_text(encoding="utf-8")

    def test_normal_workflow_has_one_main_only_input_and_stable_publisher_identity(self) -> None:
        self.assertIn("      release_record:\n", self.workflow)
        self.assertEqual(1, self.workflow.count("        required: true\n"))
        self.assertNotIn("      tag:\n", self.workflow)
        self.assertIn("github.ref == 'refs/heads/main'", self.workflow)
        self.assertIn("      name: pypi\n", self.workflow)
        self.assertIn("pypa/gh-action-pypi-publish@dc37677b2e1c63e2034f94d8a5b11f265b73ba33", self.workflow)

    def test_candidate_and_privileged_jobs_are_separate(self) -> None:
        qualify = self.workflow.split("  qualify:\n", 1)[1].split("  github_release:\n", 1)[0]
        github = self.workflow.split("  github_release:\n", 1)[1].split("  pypi:\n", 1)[0]
        pypi = self.workflow.split("  pypi:\n", 1)[1].split("  pages_build:\n", 1)[0]
        self.assertNotIn("contents: write", qualify)
        self.assertNotIn("id-token: write", qualify)
        self.assertIn("python -m se_harness validate .", qualify)
        self.assertNotIn("python scripts/validate_engineering_artifacts.py --root .", qualify)
        self.assertIn(
            'git worktree add --detach "$temp_root/candidate-checkout" "$CANDIDATE_COMMIT"',
            qualify,
        )
        self.assertIn('cd "$temp_root/candidate-checkout"', qualify)
        self.assertNotIn('cd "$RUNNER_TEMP/source-a"', qualify)
        self.assertNotIn("python -m se_harness doctor .", qualify)
        self.assertIn("runs-on: windows-2022", qualify)
        self.assertIn('python-version: "3.11.9"', qualify)
        self.assertEqual(4, qualify.count('temp_root="$(cygpath -u "$RUNNER_TEMP")"'))
        self.assertNotIn('"$RUNNER_TEMP/', qualify)
        self.assertIn('test_temp="$temp_root/candidate-test-temp"', qualify)
        self.assertIn('export TEMP="$(cygpath -w "$test_temp")"', qualify)
        self.assertIn('export TMP="$TEMP"', qualify)
        self.assertIn(
            "python -m pip install --disable-pip-version-check "
            "build==1.3.0 setuptools==84.0.0 wheel==0.48.0",
            qualify,
        )
        self.assertNotIn(
            "python -m pip install --disable-pip-version-check build==1.3.0\n",
            qualify,
        )
        self.assertIn("contents: write", github)
        self.assertNotIn("git archive", github)
        self.assertNotIn("actions/checkout", pypi)
        self.assertNotIn("python -m build", pypi)
        self.assertNotIn("skip-existing", pypi)
        self.assertEqual(1, pypi.count("id-token: write"))

    def test_repository_policy_is_explicit_and_imported_only_from_trusted_main(self) -> None:
        self.assertIn("Check out trusted main history", self.workflow)
        self.assertIn("python scripts/validate_release_distributions.py", self.workflow)
        self.assertIn("--require-record \"$RELEASE_RECORD\"", self.workflow)
        self.assertIn(
            "from repository_tools.release_distribution import",
            self.resolver,
        )
        self.assertNotIn("from se_harness.release_distribution import", self.resolver)
        self.assertGreaterEqual(self.workflow.count("--release-record"), 4)

    def test_all_publication_validation_points_use_one_predecessor_view_adapter(self) -> None:
        combined = self.workflow + self.pages
        self.assertEqual(3, combined.count("scripts/validate_predecessor_publication_view.py"))
        self.assertEqual(
            3,
            combined.count('python "$GITHUB_WORKSPACE/scripts/validate_predecessor_publication_view.py"'),
        )
        self.assertEqual(3, combined.count("--evaluator-entry-point"))
        self.assertEqual(3, combined.count('--evaluator-wheel "$RUNNER_TEMP/$EVALUATOR_WHEEL"'))
        self.assertEqual(5, combined.count("predecessor-publication-view.json"))
        self.assertEqual(5, combined.count("predecessor-publication-result.json"))
        self.assertEqual(3, combined.count("--json | tee"))
        self.assertEqual(2, combined.count("--view-output"))
        self.assertIn('mkdir "$RUNNER_TEMP/pages-predecessor-view"', self.workflow)
        self.assertIn('mkdir "$RUNNER_TEMP/predecessor-view"', self.pages)
        self.assertIn('--view-output "$RUNNER_TEMP/pages-predecessor-view/governance"', self.workflow)
        self.assertIn('--view-output "$RUNNER_TEMP/predecessor-view/governance"', self.pages)
        self.assertIn(
            'python "$RUNNER_TEMP/pages-predecessor-view/governance/scripts/generate_harness_dashboard.py"',
            self.workflow,
        )
        self.assertIn(
            'python "$RUNNER_TEMP/predecessor-view/governance/scripts/generate_harness_dashboard.py"',
            self.pages,
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
