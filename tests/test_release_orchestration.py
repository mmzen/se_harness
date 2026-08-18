from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from se_harness.installer import HarnessError
from se_harness.release_distribution import (
    BUNDLE_SCHEMA,
    checksum_manifest_bytes,
    read_bundle_manifest,
    validate_distribution_block,
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
MANIFEST_SPEC = importlib.util.spec_from_file_location("release_manifest_test_module", MANIFEST_SCRIPT)
if MANIFEST_SPEC is None or MANIFEST_SPEC.loader is None:
    raise RuntimeError("cannot load release manifest module")
MANIFEST = importlib.util.module_from_spec(MANIFEST_SPEC)
sys.modules[MANIFEST_SPEC.name] = MANIFEST
MANIFEST_SPEC.loader.exec_module(MANIFEST)


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
    def test_manifest_producer_hashes_exact_files_and_candidate_tree(self) -> None:
        commit = subprocess.run(
            ["git", "-C", str(REPOSITORY_ROOT), "rev-parse", "HEAD"],
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
            result = MANIFEST.create_manifest(REPOSITORY_ROOT, commit, "1.2.3", wheel, sdist)
        self.assertEqual(BUNDLE_SCHEMA, result["schema"])
        self.assertEqual(hashlib.sha256(b"wheel").hexdigest(), result["wheel_sha256"])
        self.assertRegex(result["source_manifest_sha256"], r"\A[0-9a-f]{64}\Z")

    def test_complete_block_is_valid_and_historical_absence_is_separate(self) -> None:
        result = validate_distribution_block(distribution_values(), "1.2.3")
        self.assertEqual("se_harness-1.2.3-py3-none-any.whl", result.wheel)
        with self.assertRaisesRegex(HarnessError, "TOML table"):
            validate_distribution_block(None, "1.2.3")

    def test_partial_unsafe_and_noncanonical_blocks_fail(self) -> None:
        partial = distribution_values()
        partial.pop("sdist_sha256")
        with self.assertRaisesRegex(HarnessError, "complete"):
            validate_distribution_block(partial, "1.2.3")
        unsafe = distribution_values()
        unsafe["wheel"] = "../se_harness-1.2.3-py3-none-any.whl"
        with self.assertRaisesRegex(HarnessError, "basename"):
            validate_distribution_block(unsafe, "1.2.3")
        wrong = distribution_values()
        wrong["checksums_sha256"] = "0" * 64
        with self.assertRaisesRegex(HarnessError, "canonical"):
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
            with self.assertRaisesRegex(HarnessError, "version"):
                read_bundle_manifest(
                    path,
                    version="1.2.3",
                    commit="a" * 40,
                    git_object_format="sha1",
                    source_date_epoch=1710000000,
                )


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
        self.assertIn("contents: write", github)
        self.assertNotIn("git archive", github)
        self.assertNotIn("actions/checkout", pypi)
        self.assertNotIn("python -m build", pypi)
        self.assertNotIn("skip-existing", pypi)
        self.assertEqual(1, pypi.count("id-token: write"))

    def test_pages_recovery_is_main_only_and_has_no_release_event(self) -> None:
        self.assertNotIn("  release:\n", self.pages)
        self.assertNotIn("      release_tag:\n", self.pages)
        self.assertIn("      release_record:\n", self.pages)
        self.assertIn("      governance_commit:\n", self.pages)
        self.assertIn("github.ref == 'refs/heads/main'", self.pages)


if __name__ == "__main__":
    unittest.main()
