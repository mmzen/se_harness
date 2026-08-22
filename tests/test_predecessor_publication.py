from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

from repository_tools import predecessor_preparation as PREPARATION
from repository_tools import predecessor_publication as PUBLICATION
from repository_tools import release_bootstrap as BOOTSTRAP


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY_ROOT / "scripts" / "validate_predecessor_publication_view.py"


def valid_report(artifacts: int, warnings: int) -> dict[str, object]:
    return {
        "artifact_count": artifacts,
        "error_count": 0,
        "errors": [],
        "valid": True,
        "warning_count": warnings,
    }


class PredecessorPublicationTests(unittest.TestCase):
    def test_retained_rls_replays_one_exact_rejected_pair(self) -> None:
        root = PREPARATION._ordinary_root(REPOSITORY_ROOT)
        with PUBLICATION._isolated_process_environment(root):
            commit = PREPARATION._git_text(root, "rev-parse", "HEAD").lower()
            object_format = PREPARATION._git_text(root, "rev-parse", "--show-object-format").lower()
            record_path, record, catalog, contract = PUBLICATION._selected_release(
                root, commit, object_format, "RLS-SEH-012"
            )
            evaluator, evaluator_path, _evaluator_sha = PUBLICATION._validate_evaluator_evidence(
                root, commit, record, contract
            )
            evidence, history, evidence_path, _evidence_sha = PUBLICATION._validate_preparation_evidence(
                root,
                commit,
                object_format,
                record_path,
                record,
                catalog,
                contract,
            )

        self.assertEqual("0.5.0", evaluator["evaluator"]["version"])
        self.assertEqual("RLS-SEH-012", evidence["release"]["record"])
        self.assertEqual(
            [
                "docs/engineering/release-0-6-0/release/REL-SEH-008.md",
                "docs/engineering/release-0-6-0/releases/RLS-SEH-009.md",
            ],
            [item.path for item in history],
        )
        self.assertEqual({"release_contract", "release_record"}, {item.artifact_type for item in history})
        self.assertTrue(all(item.status == "rejected" for item in history))
        self.assertEqual(
            "docs/engineering/release-0-6-0/evidence/RLS-SEH-012-evaluator.json",
            evaluator_path,
        )
        self.assertEqual(
            "docs/engineering/release-0-6-0/evidence/RLS-SEH-012-preparation-view.json",
            evidence_path,
        )

    def test_dual_plane_orchestration_writes_canonical_host_free_observation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            root = parent / "repository"
            root.mkdir()
            (root / ".git").mkdir()
            evaluator_root = parent / "evaluator"
            python = evaluator_root / "bin" / "python"
            entry_point = evaluator_root / "bin" / "harnessctl"
            wheel = parent / "se_harness-0.5.0-py3-none-any.whl"
            for path in (python, entry_point, wheel):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"fixture\n")
            output = parent / "publication-observation.json"
            retained_view = parent / "retained-publication-view"
            commit = "a" * 40
            tree = "b" * 40
            candidate = "c" * 40
            history = (
                PREPARATION.HistoryDescriptor(
                    "REL-TST-001", "release_contract", "rejected", "docs/engineering/x/release/REL-TST-001.md", "d" * 40, 4, "1" * 64
                ),
                PREPARATION.HistoryDescriptor(
                    "RLS-TST-001", "release_record", "rejected", "docs/engineering/x/releases/RLS-TST-001.md", "e" * 40, 4, "2" * 64
                ),
            )
            sparse_spec = PREPARATION._sparse_spec(history)
            record = {
                "id": "RLS-TST-002",
                "status": "released",
                "version": "1.2.3",
                "commit": candidate,
                "tag": "v1.2.3",
            }
            contract = BOOTSTRAP.BootstrapContract(
                release_contract="REL-TST-002",
                release_record="RLS-TST-002",
                version="1.2.3",
                from_lock_schema=2,
                from_lock_tool_version="0.5.0",
                from_lock_sha256="3" * 64,
                evaluator_version="0.5.0",
                evaluator_archive_name=wheel.name,
                evaluator_archive_sha256="4" * 64,
            )
            current = valid_report(653, 50)
            predecessor = valid_report(651, 49)
            evaluator_evidence = {"evaluator": {"payload_sha256": "5" * 64}}
            preparation_evidence = {"source": {"commit": "f" * 40}}

            def create_view(_root: Path, _commit: str, _history: object, view_parent: Path):
                view = view_parent / "repository"
                view.mkdir()
                return view, sparse_spec

            def git_text(_root: Path, *arguments: str) -> str:
                if arguments[:1] == ("status",):
                    return ""
                if arguments == ("rev-parse", "HEAD"):
                    return commit
                raise AssertionError(arguments)

            with ExitStack() as stack:
                stack.enter_context(mock.patch.object(PREPARATION, "_ordinary_root", return_value=root))
                stack.enter_context(mock.patch.object(PREPARATION, "_candidate_validation", return_value=current))
                stack.enter_context(mock.patch.object(PREPARATION, "_source_identity", return_value=(commit, tree, "sha1")))
                stack.enter_context(
                    mock.patch.object(
                        PUBLICATION,
                        "_selected_release",
                        return_value=(root / "docs/engineering/x/releases/RLS-TST-002.md", record, {}, contract),
                    )
                )
                stack.enter_context(mock.patch.object(PUBLICATION, "_tag_identity", return_value="9" * 40))
                stack.enter_context(
                    mock.patch.object(
                        PUBLICATION,
                        "_validate_evaluator_evidence",
                        return_value=(evaluator_evidence, "docs/engineering/x/evidence/evaluator.json", "6" * 64),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        PUBLICATION,
                        "_validate_preparation_evidence",
                        return_value=(preparation_evidence, history, "docs/engineering/x/evidence/view.json", "7" * 64),
                    )
                )
                stack.enter_context(mock.patch.object(PREPARATION, "_ordinary_external_interpreter", return_value=python))
                stack.enter_context(mock.patch.object(PREPARATION, "_ordinary_external", side_effect=[entry_point, wheel]))
                stack.enter_context(mock.patch.object(BOOTSTRAP, "_sha256_file", return_value=contract.evaluator_archive_sha256))
                stack.enter_context(mock.patch.object(PREPARATION, "_create_view", side_effect=create_view))
                stack.enter_context(
                    mock.patch.object(
                        PUBLICATION,
                        "_run_predecessor",
                        return_value=(
                            {"schema": "se-harness-runtime-identity-v2"},
                            predecessor,
                            {"doctor": {"returncode": 0}, "identity": {"returncode": 0}, "validate": {"returncode": 0}},
                            "5" * 64,
                        ),
                    )
                )
                stack.enter_context(mock.patch.object(PREPARATION, "_git_text", side_effect=git_text))
                stack.enter_context(mock.patch.object(BOOTSTRAP, "_artifact_catalog", return_value={}))
                stack.enter_context(mock.patch.object(PREPARATION, "_derive_history", return_value=history))
                result = PUBLICATION.validate_predecessor_publication(
                    root,
                    release_record_id="RLS-TST-002",
                    evaluator_python=python,
                    evaluator_entry_point=entry_point,
                    evaluator_wheel=wheel,
                    output=output,
                    view_output=retained_view,
                )

            retained = output.read_bytes()
            value = json.loads(retained)
            self.assertEqual(retained, PUBLICATION._canonical_json(value))
            self.assertNotIn(str(parent), retained.decode("utf-8"))
            self.assertEqual(653, result.current_artifact_count)
            self.assertEqual(651, result.predecessor_artifact_count)
            self.assertTrue(result.source_unchanged)
            self.assertTrue(result.applied)
            self.assertTrue(result.retained_view)
            self.assertTrue(retained_view.is_dir())
            self.assertEqual(result.observation_sha256, PUBLICATION._sha256(retained))

    def test_changed_preparation_evidence_fails_before_predecessor_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            root.mkdir()
            (root / ".git").mkdir()
            contract = BOOTSTRAP.BootstrapContract(
                "REL-TST-002", "RLS-TST-002", "1.2.3", 2, "0.5.0", "1" * 64, "0.5.0", "se_harness-0.5.0-py3-none-any.whl", "2" * 64
            )
            record = {"id": "RLS-TST-002", "version": "1.2.3", "commit": "c" * 40, "tag": "v1.2.3", "status": "released"}
            runner = mock.Mock()
            with ExitStack() as stack:
                stack.enter_context(mock.patch.object(PREPARATION, "_ordinary_root", return_value=root))
                stack.enter_context(mock.patch.object(PREPARATION, "_candidate_validation", return_value=valid_report(10, 0)))
                stack.enter_context(mock.patch.object(PREPARATION, "_source_identity", return_value=("a" * 40, "b" * 40, "sha1")))
                stack.enter_context(mock.patch.object(PUBLICATION, "_selected_release", return_value=(root / "RLS-TST-002.md", record, {}, contract)))
                stack.enter_context(mock.patch.object(PUBLICATION, "_tag_identity", return_value="9" * 40))
                stack.enter_context(mock.patch.object(PUBLICATION, "_validate_evaluator_evidence", return_value=({"evaluator": {"payload_sha256": "3" * 64}}, "evaluator.json", "4" * 64)))
                stack.enter_context(mock.patch.object(PUBLICATION, "_validate_preparation_evidence", side_effect=PUBLICATION.PredecessorPublicationError("preparation-view evidence digest differs")))
                stack.enter_context(mock.patch.object(PUBLICATION, "_run_predecessor", runner))
                with self.assertRaisesRegex(PUBLICATION.PredecessorPublicationError, "digest differs"):
                    PUBLICATION.validate_predecessor_publication(
                        root,
                        release_record_id="RLS-TST-002",
                        evaluator_python=Path(temporary) / "python",
                        evaluator_entry_point=Path(temporary) / "harnessctl",
                        evaluator_wheel=Path(temporary) / contract.evaluator_archive_name,
                    )
            runner.assert_not_called()

    def test_credentials_and_alternate_git_configuration_fail_closed(self) -> None:
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "secret"}, clear=False):
            with self.assertRaisesRegex(PUBLICATION.PredecessorPublicationError, "credentials are forbidden"):
                PUBLICATION._reject_environment()
        with mock.patch.dict(os.environ, {"PYTHONPATH": "attacker-controlled"}, clear=True):
            with self.assertRaisesRegex(PUBLICATION.PredecessorPublicationError, "alternate Python"):
                PUBLICATION._reject_environment()
        with mock.patch.dict(os.environ, {"PYTHONPATH": ""}, clear=True):
            PUBLICATION._reject_environment()
        contaminated = {
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "url.https://example.invalid/.insteadOf",
            "GIT_CONFIG_VALUE_0": "https://github.com/",
        }
        with mock.patch.dict(os.environ, contaminated, clear=True):
            with self.assertRaisesRegex(PUBLICATION.PredecessorPublicationError, "safe.directory"):
                PUBLICATION._reject_environment()

    def test_output_must_be_external_absent_and_exclusive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            root = parent / "repository"
            root.mkdir()
            with self.assertRaisesRegex(PUBLICATION.PredecessorPublicationError, "outside the repository"):
                PUBLICATION._ordinary_output(root / "observation.json", root)

            output = parent / "observation.json"
            output.write_text("already present\n", encoding="utf-8")
            candidate = mock.Mock()
            with mock.patch.object(PREPARATION, "_ordinary_root", return_value=root), mock.patch.object(
                PREPARATION, "_candidate_validation", candidate
            ):
                with self.assertRaisesRegex(PUBLICATION.PredecessorPublicationError, "already exists"):
                    PUBLICATION.validate_predecessor_publication(
                        root,
                        release_record_id="RLS-TST-002",
                        evaluator_python=parent / "python",
                        evaluator_entry_point=parent / "harnessctl",
                        evaluator_wheel=parent / "evaluator.whl",
                        output=output,
                    )
            candidate.assert_not_called()

            with self.assertRaisesRegex(PUBLICATION.PredecessorPublicationError, "outside the repository"):
                PUBLICATION._ordinary_view_output(root / "publication-view", root)
            retained_view = parent / "publication-view"
            retained_view.mkdir()
            with self.assertRaisesRegex(PUBLICATION.PredecessorPublicationError, "already exists"):
                PUBLICATION._ordinary_view_output(retained_view, root)

    def test_cli_has_closed_inputs_and_json_failure(self) -> None:
        help_run = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertNotIn("--omit", help_run.stdout)
        self.assertNotIn("--expected-error", help_run.stdout)
        self.assertIn("--view-output", help_run.stdout)
        failed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--repository",
                str(REPOSITORY_ROOT / "missing-publication-repository"),
                "--release-record",
                "RLS-SEH-012",
                "--evaluator-python",
                "missing-python",
                "--evaluator-entry-point",
                "missing-entry-point",
                "--evaluator-wheel",
                "missing-wheel",
                "--json",
            ],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(1, failed.returncode)
        self.assertEqual("", failed.stderr)
        self.assertIn('"passed": false', failed.stdout)
        self.assertIn('"applied": false', failed.stdout)


if __name__ == "__main__":
    unittest.main()
