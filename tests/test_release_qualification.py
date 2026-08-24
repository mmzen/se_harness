from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from se_harness.cli import build_parser, main
from se_harness.installer import HarnessError
from se_harness.release_qualification import (
    AUTHORITY,
    INDEPENDENCE,
    OPERATIONS,
    QUALIFICATION_SCHEMA,
    QualificationCheck,
    QualificationResult,
    failed_qualification,
    qualify_candidate_package,
    qualify_complete_candidate,
    qualify_predecessor_view,
    qualify_public_install,
    qualify_released_root,
    write_qualification_result,
)


def runtime_identity(*, passed: bool, role: str, commit: str | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        passed=passed,
        harness_version="0.6.0",
        isolated_python=True,
        user_site_enabled=False,
        pythonpath_present=False,
        candidate_commit=commit,
        evaluator_payload_manifest="se-harness-installed-payload-v1" if role == "released-evaluator" else None,
        evaluator_payload_sha256="a" * 64 if role == "released-evaluator" else None,
        evaluator_archive_name="se_harness-0.6.0-py3-none-any.whl" if role == "released-evaluator" else None,
        evaluator_archive_sha256="b" * 64 if role == "released-evaluator" else None,
    )


class ReleaseQualificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)

    def result(self, operation: str = "complete-candidate") -> QualificationResult:
        return QualificationResult(
            operation=operation,
            independence=INDEPENDENCE[operation],
            evaluator={"role": INDEPENDENCE[operation], "identity_sha256": "a" * 64},
            target={"kind": operation, "identity_sha256": "b" * 64},
            checks=(QualificationCheck("T001", True, "fixture", "passed"),),
            passed=True,
        )

    def test_result_schema_is_closed_deterministic_and_non_authoritative(self) -> None:
        first = self.result()
        second = self.result()
        self.assertEqual(first.canonical_bytes(), second.canonical_bytes())
        value = json.loads(first.canonical_bytes())
        self.assertEqual(
            {"authority", "checks", "completion", "evaluator", "independence", "operation", "passed", "schema", "target"},
            set(value),
        )
        self.assertEqual(QUALIFICATION_SCHEMA, value["schema"])
        self.assertEqual(AUTHORITY, value["authority"])

    def test_result_output_is_exclusive_and_outside_the_target(self) -> None:
        target = self.root / "repository"
        target.mkdir()
        output = self.root / "qualification.json"
        write_qualification_result(output, self.result(), forbidden_roots=(target,))
        self.assertEqual(self.result().canonical_bytes(), output.read_bytes())
        with self.assertRaisesRegex(HarnessError, "already exists"):
            write_qualification_result(output, self.result(), forbidden_roots=(target,))
        with self.assertRaisesRegex(HarnessError, "outside"):
            write_qualification_result(target / "result.json", self.result(), forbidden_roots=(target,))

    def test_failure_result_bounds_paths_and_retains_no_authority(self) -> None:
        hostile = self.root / "private" / "candidate.txt"
        result = failed_qualification(
            "complete-candidate",
            code="T002",
            subject="fixture",
            message=f"cannot read {hostile}:\nsecret body",
        )
        raw = result.canonical_bytes().decode("utf-8")
        self.assertNotIn(str(self.root), raw)
        self.assertNotIn("secret body", raw)
        self.assertIn("<TEMP>", raw)
        self.assertFalse(result.passed)
        self.assertEqual(AUTHORITY, result.authority)

    def test_cli_has_five_closed_operations_and_rejects_cross_role_options(self) -> None:
        parser = build_parser()
        command_action = next(action for action in parser._actions if isinstance(getattr(action, "choices", None), dict))
        qualify = command_action.choices["qualify"]
        role_action = next(action for action in qualify._actions if isinstance(getattr(action, "choices", None), dict))
        self.assertEqual(set(OPERATIONS), set(role_action.choices))
        parsed = parser.parse_args(
            ["qualify", "complete-candidate", ".", "--candidate-commit", "a" * 40, "--json"]
        )
        self.assertEqual("complete-candidate", parsed.qualification_operation)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parser.parse_args(
                [
                    "qualify",
                    "complete-candidate",
                    ".",
                    "--candidate-commit",
                    "a" * 40,
                    "--public-wheel",
                    "x.whl",
                ]
            )

    def test_candidate_workflow_bootstrap_is_exact_legacy_evidence(self) -> None:
        workflow = (
            Path(__file__).resolve().parents[1]
            / ".github"
            / "workflows"
            / "candidate-evidence.yml"
        ).read_text(encoding="utf-8")
        required = (
            'RELEASED_VERIFIER_VERSION: "0.6.0"',
            'RELEASED_VERIFIER_WHEEL_SHA256: "2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7"',
            'RELEASED_VERIFIER_PAYLOAD_SHA256: "c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42"',
            'RELEASED_ACCEPTANCE_CONTRACT_SHA256: "a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75"',
            '"$RUNNER_TEMP/verifier-env/bin/python" -I -m se_harness accept-candidate',
            'value["schema"] == "se-harness-functional-acceptance-v1"',
            'assert "independence" not in value',
            'candidate-package-legacy-bootstrap-0.6.0',
        )
        self.assertTrue(all(value in workflow for value in required))
        self.assertNotIn("qualify candidate-package", workflow)
        for original, replacement in (
            ('RELEASED_VERIFIER_VERSION: "0.6.0"', 'RELEASED_VERIFIER_VERSION: "0.6.1"'),
            ("se-harness-functional-acceptance-v1", QUALIFICATION_SCHEMA),
            ("accept-candidate", "validate"),
        ):
            mutated = workflow.replace(original, replacement, 1)
            with self.subTest(original=original):
                self.assertFalse(all(value in mutated for value in required))

    @mock.patch("se_harness.release_qualification._validation_check")
    @mock.patch("se_harness.release_qualification.inspect_runtime_identity")
    @mock.patch("se_harness.release_qualification._tracked_clean", return_value=True)
    @mock.patch("se_harness.release_qualification._git")
    @mock.patch("se_harness.release_qualification._repository_snapshot")
    def test_complete_candidate_is_always_candidate_controlled(
        self,
        snapshot: mock.Mock,
        git: mock.Mock,
        _clean: mock.Mock,
        inspect: mock.Mock,
        validation: mock.Mock,
    ) -> None:
        repository = self.root / "candidate"
        repository.mkdir()
        commit = "c" * 40
        snapshot.return_value = {"kind": "git-worktree", "head": commit, "tree": "d" * 40}
        git.return_value = (commit + "\n").encode("ascii")
        inspect.return_value = runtime_identity(passed=True, role="candidate-source", commit=commit)
        validation.return_value = QualificationCheck("CC003", True, "engineering-graph", "passed")
        result = qualify_complete_candidate(repository, candidate_commit=commit)
        self.assertTrue(result.passed)
        self.assertEqual("candidate-controlled", result.independence)
        self.assertEqual(["CC001", "CC002", "CC003", "CC004"], [item.id for item in result.checks])

    @mock.patch("se_harness.release_qualification._repository_snapshot")
    @mock.patch("se_harness.release_qualification._load_lock")
    @mock.patch("se_harness.release_qualification._installed_entry_point")
    @mock.patch("se_harness.release_qualification.inspect_runtime_identity")
    @mock.patch("se_harness.release_qualification.inspect_installation")
    @mock.patch("se_harness.release_qualification._validation_check")
    def test_released_root_stops_before_validation_on_identity_failure(
        self,
        validation: mock.Mock,
        installation: mock.Mock,
        inspect: mock.Mock,
        entry_point: mock.Mock,
        load_lock: mock.Mock,
        snapshot: mock.Mock,
    ) -> None:
        repository = self.root / "root"
        repository.mkdir()
        (repository / ".engineering-harness.lock").write_text("{}\n", encoding="utf-8")
        snapshot.return_value = {"kind": "directory", "state_sha256": "a" * 64}
        entry_point.return_value = self.root / "harnessctl"
        load_lock.return_value = {
            "schema": 3,
            "evaluator": {
                "version": "0.6.0",
                "payload_sha256": "a" * 64,
                "archive_sha256": "b" * 64,
            },
        }
        inspect.return_value = runtime_identity(passed=False, role="released-evaluator")
        result = qualify_released_root(repository)
        self.assertFalse(result.passed)
        installation.assert_not_called()
        validation.assert_not_called()
        self.assertEqual(["RR001", "RR002", "RR003", "RR004"], [item.id for item in result.checks])

    @mock.patch("se_harness.release_qualification.assess_candidate_wheel")
    @mock.patch("se_harness.release_qualification._installed_entry_point")
    @mock.patch("se_harness.release_qualification.inspect_runtime_identity")
    def test_candidate_package_cannot_run_after_verifier_identity_failure(
        self,
        inspect: mock.Mock,
        entry_point: mock.Mock,
        acceptance: mock.Mock,
    ) -> None:
        wheel = self.root / "candidate.whl"
        wheel.write_bytes(b"candidate")
        entry_point.return_value = self.root / "harnessctl"
        inspect.return_value = runtime_identity(passed=False, role="released-evaluator")
        result = qualify_candidate_package(
            wheel,
            candidate_commit="c" * 40,
            candidate_wheel_sha256="d" * 64,
            verifier_wheel_sha256="e" * 64,
        )
        self.assertFalse(result.passed)
        acceptance.assert_not_called()
        self.assertEqual("released-verifier", result.independence)

    @mock.patch("repository_tools.predecessor_publication.validate_predecessor_publication")
    @mock.patch("se_harness.release_qualification._external_evaluator_files")
    @mock.patch("se_harness.release_qualification._repository_snapshot")
    def test_predecessor_view_wraps_the_fixed_service_and_preserves_claim_boundary(
        self,
        snapshot: mock.Mock,
        external: mock.Mock,
        validate: mock.Mock,
    ) -> None:
        repository = self.root / "repository"
        repository.mkdir()
        snapshot.return_value = {"kind": "directory", "state_sha256": "a" * 64}
        external.return_value = (self.root / "harnessctl", self.root / "predecessor.whl")
        validate.return_value = SimpleNamespace(
            schema="se-harness-predecessor-publication-view-v1",
            current_artifact_count=10,
            predecessor_artifact_count=8,
            source_unchanged=True,
            release_contract="REL-X-001",
            version="0.6.0",
            evaluator_version="0.5.0",
            evaluator_archive_name="se_harness-0.5.0-py3-none-any.whl",
            evaluator_archive_sha256="a" * 64,
            evaluator_payload_sha256="b" * 64,
            release_record="RLS-X-001",
            source_commit="c" * 40,
            source_tree="f" * 40,
            git_object_format="sha1",
            candidate_commit="d" * 40,
            sparse_spec_sha256="1" * 64,
            omitted_history=(),
            observation_sha256="e" * 64,
        )
        result = qualify_predecessor_view(
            repository,
            release_record_id="RLS-X-001",
            evaluator_python=self.root / "python",
        )
        self.assertTrue(result.passed)
        self.assertEqual("external-predecessor", result.independence)
        validate.assert_called_once()

    @mock.patch("se_harness.release_qualification._repository_snapshot")
    @mock.patch("se_harness.release_qualification._release_record")
    @mock.patch("se_harness.release_qualification._wheel_metadata")
    @mock.patch("se_harness.release_qualification.wheel_payload_sha256")
    @mock.patch("se_harness.release_qualification.installed_evaluator_identity")
    @mock.patch("se_harness.release_qualification._run")
    @mock.patch("se_harness.release_qualification._installed_entry_point")
    def test_public_install_binds_released_record_wheel_and_payload(
        self,
        entry_point: mock.Mock,
        run: mock.Mock,
        installed: mock.Mock,
        wheel_payload: mock.Mock,
        metadata: mock.Mock,
        release: mock.Mock,
        snapshot: mock.Mock,
    ) -> None:
        repository = self.root / "repository"
        repository.mkdir()
        wheel = self.root / "se_harness-0.6.0-py3-none-any.whl"
        wheel.write_bytes(b"wheel")
        launcher = self.root / "harnessctl"
        launcher.write_bytes(b"launcher")
        digest = "a" * 64
        payload = "b" * 64
        snapshot.return_value = {"kind": "directory", "state_sha256": "c" * 64}
        release.return_value = (
            repository / "RLS-X-001.md",
            {
                "status": "released",
                "version": "0.6.0",
                "commit": "d" * 40,
                "distribution": {"wheel": wheel.name, "wheel_sha256": digest},
            },
        )
        metadata.return_value = ("0.6.0", digest)
        installed.return_value = SimpleNamespace(
            version="0.6.0",
            archive_name=wheel.name,
            archive_sha256=digest,
            payload_manifest="se-harness-installed-payload-v1",
            payload_sha256=payload,
        )
        wheel_payload.return_value = payload
        entry_point.return_value = launcher
        run.side_effect = (
            SimpleNamespace(returncode=0, stdout=b"0.6.0\n", stderr=b""),
            SimpleNamespace(
                returncode=0,
                stdout=(" ".join(OPERATIONS) + "\n").encode("ascii"),
                stderr=b"",
            ),
        )
        with mock.patch("se_harness.release_qualification.sys.prefix", str(self.root)):
            result = qualify_public_install(
                repository,
                release_record_id="RLS-X-001",
                public_wheel=wheel,
                public_wheel_sha256=digest,
                payload_sha256=payload,
            )
        self.assertTrue(result.passed)
        self.assertEqual("public-install-observation", result.independence)

    @mock.patch("se_harness.cli.qualify_candidate_package")
    def test_accept_candidate_is_one_result_compatible_alias(self, qualify: mock.Mock) -> None:
        qualify.return_value = self.result("candidate-package")
        output = self.root / "result.json"
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(
                [
                    "accept-candidate",
                    "--wheel",
                    "candidate.whl",
                    "--candidate-commit",
                    "c" * 40,
                    "--candidate-wheel-sha256",
                    "d" * 64,
                    "--verifier-wheel-sha256",
                    "e" * 64,
                    "--output",
                    str(output),
                ]
            )
        self.assertEqual(0, code, stderr.getvalue())
        self.assertEqual(QUALIFICATION_SCHEMA, json.loads(output.read_text(encoding="utf-8"))["schema"])
        qualify.assert_called_once()


if __name__ == "__main__":
    unittest.main()
