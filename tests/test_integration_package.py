from __future__ import annotations

import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock
import zipfile


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY_ROOT / ".github" / "scripts" / "build_integration_package.py"
FIXTURES = REPOSITORY_ROOT / "tests" / "fixtures" / "integration_package"
WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "candidate-evidence.yml"
MODULE_NAME = "se_harness_integration_package_script"
SPEC = importlib.util.spec_from_file_location(MODULE_NAME, SCRIPT)
assert SPEC is not None and SPEC.loader is not None
integration = importlib.util.module_from_spec(SPEC)
sys.modules[MODULE_NAME] = integration
SPEC.loader.exec_module(integration)


def canonical(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True) + "\n"
    ).encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


class IntegrationPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.commit = "1cdc75259da8156e93ad8c32110ee196296b8cea"
        self.version = "0.6.0+main.g1cdc75259da8"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def make_wheel(self, directory: Path, version: str | None = None) -> Path:
        version = version or self.version
        directory.mkdir(parents=True, exist_ok=True)
        wheel = directory / f"se_harness-{version}-py3-none-any.whl"
        dist_info = f"se_harness-{version}.dist-info"
        with zipfile.ZipFile(wheel, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("se_harness/__init__.py", f'__version__ = "{version}"\n')
            archive.writestr(
                f"{dist_info}/METADATA",
                "Metadata-Version: 2.1\n"
                "Name: se-harness\n"
                f"Version: {version}\n"
                "Requires-Python: >=3.11\n\n",
            )
            archive.writestr(
                f"{dist_info}/WHEEL",
                "Wheel-Version: 1.0\n"
                "Generator: independent-test-fixture\n"
                "Root-Is-Purelib: true\n"
                "Tag: py3-none-any\n\n",
            )
            archive.writestr(f"{dist_info}/RECORD", "")
        return wheel

    def manifest_for(self, wheel: Path) -> dict[str, object]:
        wheel_raw = wheel.read_bytes()
        return {
            "schema": "se-harness-integration-package-v1",
            "distribution_kind": "integration-package",
            "promotable": False,
            "repository": "mmzen/se_harness",
            "commit": self.commit,
            "event": "push",
            "ref": "refs/heads/main",
            "pull_request": None,
            "channel": "main",
            "base_version": "0.6.0",
            "version": self.version,
            "retention_days": 14,
            "build": {
                "python": "3.11.11",
                "build": "1.2.2.post1",
                "setuptools": "75.8.0",
                "wheel": "0.45.1",
                "source_date_epoch": 1_700_000_000,
            },
            "run": {"id": 32716711655, "attempt": 1, "workflow": "SE Harness Candidate Evidence"},
            "overlays": [
                {"path": "pyproject.toml", "before_sha256": "a" * 64, "after_sha256": "b" * 64},
                {
                    "path": "se_harness/__init__.py",
                    "before_sha256": "c" * 64,
                    "after_sha256": "d" * 64,
                },
            ],
            "wheel": {"filename": wheel.name, "size": len(wheel_raw), "sha256": digest(wheel_raw)},
        }

    def make_payload(self) -> tuple[Path, dict[str, object]]:
        payload = self.root / "payload"
        wheel = self.make_wheel(payload)
        manifest = self.manifest_for(wheel)
        manifest_raw = canonical(manifest)
        (payload / "integration-manifest.json").write_bytes(manifest_raw)
        checksums = "".join(
            f"{digest(raw)}  {name}\n"
            for name, raw in sorted(
                {
                    "integration-manifest.json": manifest_raw,
                    wheel.name: wheel.read_bytes(),
                }.items()
            )
        ).encode("ascii")
        (payload / "SHA256SUMS").write_bytes(checksums)
        return payload, manifest

    def test_verifier_owned_identity_vectors(self) -> None:
        document = json.loads((FIXTURES / "canonical_vectors.json").read_text(encoding="utf-8"))
        self.assertEqual("se-harness-integration-package-test-v1", document["schema"])
        for vector in document["vectors"]:
            channel, version, retention = integration.derive_identity(
                vector["base_version"],
                vector["commit"],
                vector["event"],
                vector["ref"],
                vector["pull_request"],
            )
            self.assertEqual(vector["channel"], channel)
            self.assertEqual(vector["version"], version)
            self.assertEqual(vector["retention_days"], retention)
        sha256_commit = "a" * 64
        channel, version, retention = integration.derive_identity(
            "0.7.0rc1", sha256_commit, "push", "refs/heads/main", None
        )
        self.assertEqual(("main", "0.7.0rc1+main.gaaaaaaaaaaaa", 14), (channel, version, retention))

    def test_identity_rejects_ambiguous_event_version_and_commit_inputs(self) -> None:
        cases = [
            ("0.6.0+already.local", self.commit, "push", "refs/heads/main", None),
            ("0.6.0", self.commit.upper(), "push", "refs/heads/main", None),
            ("0.6.0", self.commit[:-1], "push", "refs/heads/main", None),
            ("0.6.0", self.commit, "push", "refs/heads/feature", None),
            ("0.6.0", self.commit, "push", "refs/heads/main", 1),
            ("0.6.0", self.commit, "pull_request", "refs/pull/1/merge", 0),
            ("0.6.0", self.commit, "pull_request", "refs/pull/2/merge", 1),
            ("0.6.0", self.commit, "workflow_dispatch", "refs/heads/main", None),
        ]
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(integration.IntegrationPackageError):
                    integration.derive_identity(*case)

    def test_overlay_changes_only_the_two_declared_assignments(self) -> None:
        export = self.root / "export"
        (export / "se_harness").mkdir(parents=True)
        pyproject_before = (
            "[build-system]\n"
            'requires = ["setuptools>=68"]\n\n'
            "[project]\n"
            'name = "se-harness"\n'
            'version = "0.6.0"\n\n'
            "[tool.example]\n"
            'version = "owner-controlled"\n'
        )
        init_before = '__version__ = "0.6.0"\nOTHER = "0.6.0"\n'
        (export / "pyproject.toml").write_text(pyproject_before, encoding="utf-8")
        (export / "se_harness" / "__init__.py").write_text(init_before, encoding="utf-8")

        base, overlays = integration.apply_version_overlay(export, self.version)

        self.assertEqual("0.6.0", base)
        self.assertEqual(["pyproject.toml", "se_harness/__init__.py"], [item["path"] for item in overlays])
        pyproject_after = (export / "pyproject.toml").read_text(encoding="utf-8")
        init_after = (export / "se_harness" / "__init__.py").read_text(encoding="utf-8")
        self.assertIn(f'version = "{self.version}"', pyproject_after)
        self.assertIn('version = "owner-controlled"', pyproject_after)
        self.assertEqual(f'__version__ = "{self.version}"\nOTHER = "0.6.0"\n', init_after)
        self.assertNotEqual(overlays[0]["before_sha256"], overlays[0]["after_sha256"])
        self.assertNotEqual(overlays[1]["before_sha256"], overlays[1]["after_sha256"])
        before_paths = set(integration.regular_tree_manifest(export))
        self.assertEqual({"pyproject.toml", "se_harness/__init__.py"}, before_paths)

    def test_overlay_rejects_mismatch_missing_and_duplicate_declarations(self) -> None:
        cases = [
            ('[project]\nversion = "0.6.0"\n', '__version__ = "0.6.1"\n'),
            ('[project]\nname = "se-harness"\n', '__version__ = "0.6.0"\n'),
            (
                '[project]\nversion = "0.6.0"\nversion = "0.6.0"\n',
                '__version__ = "0.6.0"\n',
            ),
        ]
        for index, (pyproject, package_init) in enumerate(cases):
            export = self.root / f"invalid-overlay-{index}"
            (export / "se_harness").mkdir(parents=True)
            (export / "pyproject.toml").write_text(pyproject, encoding="utf-8")
            (export / "se_harness" / "__init__.py").write_text(package_init, encoding="utf-8")
            with self.subTest(index=index):
                with self.assertRaises(integration.IntegrationPackageError):
                    integration.apply_version_overlay(export, self.version)

    def write_tar(self, path: Path, members: list[tuple[str, bytes | str]]) -> None:
        with tarfile.open(path, "w") as archive:
            for name, value in members:
                member = tarfile.TarInfo(name)
                if value == "symlink":
                    member.type = tarfile.SYMTYPE
                    member.linkname = "target"
                    archive.addfile(member)
                else:
                    assert isinstance(value, bytes)
                    member.size = len(value)
                    archive.addfile(member, io.BytesIO(value))

    def test_safe_archive_extracts_regular_portable_members(self) -> None:
        archive = self.root / "valid.tar"
        self.write_tar(
            archive,
            [
                ("pyproject.toml", b'[project]\nversion = "0.6.0"\n'),
                ("se_harness/__init__.py", b'__version__ = "0.6.0"\n'),
                ("README.md", b"candidate\n"),
            ],
        )
        destination = self.root / "valid-export"
        integration.extract_safe_archive(archive, destination)
        self.assertEqual(b"candidate\n", (destination / "README.md").read_bytes())

    def test_safe_archive_rejects_traversal_links_duplicates_and_reserved_names(self) -> None:
        invalid_members = {
            "traversal": [("../escape", b"bad")],
            "dot": [("source/./file", b"bad")],
            "backslash": [("source\\file", b"bad")],
            "absolute": [("/absolute", b"bad")],
            "symlink": [("link", "symlink")],
            "case-collision": [("README.md", b"one"), ("readme.md", b"two")],
            "device": [("source/CON.txt", b"bad")],
        }
        for label, members in invalid_members.items():
            archive = self.root / f"{label}.tar"
            destination = self.root / f"{label}-export"
            self.write_tar(archive, members)
            with self.subTest(label=label):
                with self.assertRaises(integration.IntegrationPackageError):
                    integration.extract_safe_archive(archive, destination)
                self.assertFalse(any(destination.rglob("*")))

    def test_payload_verification_is_strict_and_binds_workflow_identity(self) -> None:
        payload, manifest = self.make_payload()
        result = integration.verify_payload(
            payload,
            expected_commit=self.commit,
            expected_repository="mmzen/se_harness",
            expected_event="push",
            expected_ref="refs/heads/main",
            expected_run_id=32716711655,
            expected_run_attempt=1,
            expected_workflow="SE Harness Candidate Evidence",
            expected_retention_days=14,
        )
        self.assertEqual(manifest, result)
        with self.assertRaises(integration.IntegrationPackageError):
            integration.verify_payload(payload, expected_commit="f" * 40)

        (payload / "unexpected.txt").write_text("unexpected", encoding="utf-8")
        with self.assertRaises(integration.IntegrationPackageError):
            integration.verify_payload(payload)

    def test_verify_cli_rechecks_the_complete_workflow_binding(self) -> None:
        payload, _ = self.make_payload()
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(SCRIPT),
                "verify",
                "--payload",
                str(payload),
                "--expected-commit",
                self.commit,
                "--expected-repository",
                "mmzen/se_harness",
                "--expected-event",
                "push",
                "--expected-ref",
                "refs/heads/main",
                "--expected-run-id",
                "32716711655",
                "--expected-run-attempt",
                "1",
                "--expected-workflow",
                "SE Harness Candidate Evidence",
                "--expected-retention-days",
                "14",
            ],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual("pass", summary["result"])
        self.assertEqual(self.commit, summary["commit"])
        self.assertEqual(self.version, summary["version"])

    def test_payload_rejects_tampered_wheel_manifest_and_checksums(self) -> None:
        payload, manifest = self.make_payload()
        wheel = payload / str(manifest["wheel"]["filename"])
        wheel.write_bytes(wheel.read_bytes() + b"tampered")
        with self.assertRaises(integration.IntegrationPackageError):
            integration.verify_payload(payload)

        payload, manifest = self.make_payload_in(self.root / "second")
        manifest["promotable"] = True
        (payload / "integration-manifest.json").write_bytes(canonical(manifest))
        with self.assertRaises(integration.IntegrationPackageError):
            integration.verify_payload(payload)

        payload, _ = self.make_payload_in(self.root / "third")
        checksum = payload / "SHA256SUMS"
        checksum.write_bytes(checksum.read_bytes().replace(b"a", b"b", 1))
        with self.assertRaises(integration.IntegrationPackageError):
            integration.verify_payload(payload)

    def make_payload_in(self, root: Path) -> tuple[Path, dict[str, object]]:
        previous = self.root
        try:
            self.root = root
            return self.make_payload()
        finally:
            self.root = previous

    def test_manifest_parser_rejects_duplicate_keys_bom_and_noncanonical_bytes(self) -> None:
        with self.assertRaises(integration.IntegrationPackageError):
            integration.parse_json_object(b'{"schema":"one","schema":"two"}\n')
        with self.assertRaises(integration.IntegrationPackageError):
            integration.parse_json_object(b"\xef\xbb\xbf{}\n")

        payload, manifest = self.make_payload()
        raw = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
        (payload / "integration-manifest.json").write_bytes(raw)
        wheel = payload / str(manifest["wheel"]["filename"])
        (payload / "SHA256SUMS").write_bytes(
            "".join(
                f"{digest(value)}  {name}\n"
                for name, value in sorted(
                    {"integration-manifest.json": raw, wheel.name: wheel.read_bytes()}.items()
                )
            ).encode("ascii")
        )
        with self.assertRaises(integration.IntegrationPackageError):
            integration.verify_payload(payload)

    def test_wheel_rejects_wrong_metadata_tag_and_member_paths(self) -> None:
        wrong = self.root / "wrong"
        wrong.mkdir()
        wheel = wrong / f"se_harness-{self.version}-py3-none-any.whl"
        dist_info = f"se_harness-{self.version}.dist-info"
        with zipfile.ZipFile(wheel, "w") as archive:
            archive.writestr(f"{dist_info}/METADATA", f"Name: se-harness\nVersion: {self.version}\n\n")
            archive.writestr(
                f"{dist_info}/WHEEL",
                "Wheel-Version: 1.0\nRoot-Is-Purelib: false\nTag: cp311-cp311-win_amd64\n\n",
            )
        with self.assertRaises(integration.IntegrationPackageError):
            integration.validate_wheel(wheel, self.version)

        traversal = wrong / f"se_harness-{self.version}-py3-none-any.whl"
        with zipfile.ZipFile(traversal, "w") as archive:
            archive.writestr("../escape", "bad")
            archive.writestr(f"{dist_info}/METADATA", f"Name: se-harness\nVersion: {self.version}\n\n")
            archive.writestr(
                f"{dist_info}/WHEEL",
                "Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n\n",
            )
        with self.assertRaises(integration.IntegrationPackageError):
            integration.validate_wheel(traversal, self.version)

    def test_output_is_exclusive_and_never_overwrites_owner_content(self) -> None:
        source = self.root / "source"
        wheel = self.make_wheel(source)
        manifest = self.manifest_for(wheel)
        output = self.root / "owner-output"
        output.mkdir()
        marker = output / "owner.txt"
        marker.write_text("keep", encoding="utf-8")
        with self.assertRaises(integration.IntegrationPackageError):
            integration._prepare_output(output, wheel, manifest)
        self.assertEqual("keep", marker.read_text(encoding="utf-8"))

    def test_install_root_expands_windows_short_path_before_virtualenv(self) -> None:
        alias = r"C:\Users\RUNNER~1\AppData\Local\Temp\integration"
        expected = self.root.resolve()
        with mock.patch.object(integration.os.path, "realpath", return_value=str(expected)) as realpath:
            actual = integration._canonical_existing_directory(alias)
        self.assertEqual(expected, actual)
        realpath.assert_called_once_with(alias, strict=True)

    def test_workflow_has_qualified_three_stage_non_release_lane(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for job in (
            "integration-package-build",
            "integration-package-verify",
            "integration-package-retain",
        ):
            self.assertRegex(workflow, rf"(?m)^  {job}:$")
        lane = workflow.split("  integration-package-build:\n", 1)[1]
        self.assertIn("needs:", lane)
        for prerequisite in (
            "candidate-source",
            "candidate-package",
            "governance-migration",
        ):
            self.assertIn(f"      - {prerequisite}\n", lane)
        # WO-CIP-001: the cross-platform migration reconciliation is the lane's
        # first step, not a job of its own.
        self.assertNotIn("governance-migration-reconcile", workflow)
        self.assertIn("needs.governance-migration.outputs.Linux", lane)
        self.assertIn("needs.governance-migration.outputs.Windows", lane)
        actions = {
            "actions/checkout": "11bd71901bbe5b1630ceea73d27597364c9af683",
            "actions/setup-python": "a26af69be951a213d495a4c3e4e4022e16d87065",
            "actions/upload-artifact": "ea165f8d65b6e75b540449e92b4886f43607fa02",
            "actions/download-artifact": "d3f86a106a0bac45b974a628896c90dbdf5c8093",
        }
        for action, commit in actions.items():
            self.assertIn(f"uses: {action}@{commit}", lane)
        self.assertNotRegex(lane, r"uses: actions/[a-z-]+@v[0-9]")
        self.assertIn("build==1.2.2.post1 setuptools==75.8.0 wheel==0.45.1", lane)
        self.assertIn("integration-package-staging-${{ github.sha }}", lane)
        self.assertIn("se-harness-integration-${{ github.sha }}", lane)
        self.assertIn("retention-days: 1", lane)
        self.assertIn("github.event_name == 'pull_request'", lane)
        self.assertIn("github.ref == 'refs/heads/main'", lane)
        self.assertIn("runs-on: ${{ matrix.runner }}", lane)
        self.assertIn("runner: ubuntu-latest", lane)
        self.assertIn("runner: windows-latest", lane)
        self.assertIn("install-test", lane)
        self.assertIn("--no-index", SCRIPT.read_text(encoding="utf-8"))
        self.assertNotIn("contents: write", workflow)
        self.assertNotIn("workflow_dispatch:", workflow)
        for forbidden in ("pypi", "github release", "create-release", "git tag", "secrets."):
            self.assertNotIn(forbidden, lane.lower())

    def test_operator_documentation_covers_safe_install_and_authority_boundary(self) -> None:
        guide = (REPOSITORY_ROOT / "docs" / "notes" / "integration-packages.md").read_text(encoding="utf-8")
        for required in (
            "gh run download",
            "SHA256SUMS",
            "--no-index --no-deps",
            "promotable",
            "14 days",
            "3 days",
            "disposable",
            "governing evaluator",
            "pip install --upgrade se-harness",
        ):
            self.assertIn(required, guide)
        self.assertIn("integration-packages.md", (REPOSITORY_ROOT / "docs" / "notes" / "README.md").read_text(encoding="utf-8"))
        self.assertIn("integration packages", (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8").lower())


if __name__ == "__main__":
    unittest.main()
