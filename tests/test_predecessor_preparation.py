from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from repository_tools import predecessor_preparation as PREPARATION


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load test module: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


CANDIDATE_VALIDATOR = load_module(
    "predecessor_preparation_candidate_validator",
    REPOSITORY_ROOT / "templates/repository/standard/scripts/validate_engineering_artifacts.py",
)
PUBLICATION = load_module(
    "predecessor_preparation_publication",
    REPOSITORY_ROOT / ".github/scripts/publish_dashboard.py",
)


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class PredecessorPreparationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        temporary = Path(self.temporary.name)
        self.root = temporary / "repository"
        self.root.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Harness Test")
        self.git("config", "user.email", "harness-test@example.invalid")
        self.write("README.md", b"candidate\n")
        self.commit("candidate")
        self.candidate = self.git("rev-parse", "HEAD")

        self.lock_bytes = (
            json.dumps(
                {
                    "schema": 2,
                    "tool_version": "0.5.0",
                    "hash_algorithm": "sha256",
                    "hash_mode": "utf8-text-lf-v1",
                    "files": {},
                },
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        self.write(".engineering-harness.toml", b'[harness]\ntool_version = "0.5.0"\n')
        self.write(".engineering-harness.lock", self.lock_bytes)
        self.history_evidence = b'{"retained":true}\n'
        self.history_evidence_path = (
            "docs/engineering/release/evidence/RLS-TST-001-evaluator.json"
        )
        self.write(self.history_evidence_path, self.history_evidence)
        archive_bytes = b"exact released evaluator wheel\n"
        self.archive_sha = sha256(archive_bytes)

        self.write(
            "docs/engineering/release/release/REL-TST-001.md",
            self.contract("REL-TST-001", "RLS-TST-001", "rejected"),
        )
        self.write(
            "docs/engineering/release/releases/RLS-TST-001.md",
            self.rejected_record(),
        )
        self.write(
            "docs/engineering/release/release/REL-TST-002.md",
            self.contract("REL-TST-002", "RLS-TST-002", "approved"),
        )
        self.write(
            "docs/engineering/release/work-orders/WO-TST-001.md",
            self.artifact(
                "WO-TST-001",
                "work_order",
                "implemented",
                {"implements": ["REQ-TST-001"]},
            ),
        )
        self.write(
            "docs/engineering/release/verification-records/VREC-TST-002.md",
            self.verification_record(),
        )
        self.commit("governance")
        self.source = self.git("rev-parse", "HEAD")

        evaluator = temporary / "released-evaluator"
        self.python = evaluator / "Scripts" / "python.exe"
        self.entry_point = evaluator / "Scripts" / "harnessctl.exe"
        self.wheel = temporary / "se_harness-0.5.0-py3-none-any.whl"
        for path, payload in (
            (self.python, b"python\n"),
            (self.entry_point, b"harnessctl\n"),
            (self.wheel, archive_bytes),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        self.real_run = PREPARATION._run

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return completed.stdout.strip()

    def commit(self, message: str) -> None:
        self.git("add", ".")
        self.git("commit", "-m", message)

    def write(self, relative: str, payload: bytes) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)

    @staticmethod
    def artifact(
        artifact_id: str,
        artifact_type: str,
        status: str,
        relations: dict[str, list[str]],
        extra: str = "",
    ) -> bytes:
        relation_lines = "\n".join(
            f"{name} = {json.dumps(values)}" for name, values in relations.items()
        )
        return f'''+++
id = "{artifact_id}"
type = "{artifact_type}"
title = "{artifact_id}"
status = "{status}"
owners = ["release-owner"]
created = "2026-08-22"
updated = "2026-08-22"
{extra}

[relations]
{relation_lines}
+++

# {artifact_id}
'''.encode("utf-8")

    def contract(self, contract_id: str, record_id: str, status: str) -> bytes:
        extra = f'''[bootstrap]
schema = "se-harness-release-bootstrap-v1"
release_record = "{record_id}"
version = "1.2.3"
from_lock_schema = 2
from_lock_tool_version = "0.5.0"
from_lock_sha256 = "{sha256(self.lock_bytes)}"
evaluator_version = "0.5.0"
evaluator_archive_name = "se_harness-0.5.0-py3-none-any.whl"
evaluator_archive_sha256 = "{self.archive_sha}"'''
        return self.artifact(
            contract_id,
            "release_contract",
            status,
            {"gates": ["WO-TST-001"]},
            extra,
        )

    def rejected_record(self) -> bytes:
        extra = f'''version = "1.2.3"
commit = "{self.candidate}"
git_object_format = "sha1"
released_at = "2026-08-21T12:00:00Z"
authorized_by = "release-owner"
tag = "v1.2.3"
preparation_schema = "se-harness-predecessor-bootstrap-v1"
evaluator_evidence_path = "{self.history_evidence_path}"
evaluator_evidence_sha256 = "{sha256(self.history_evidence)}"
rejected_at = "2026-08-21T12:30:00Z"
rejected_by = "release-owner"
rejection_reason = "retained failure"'''
        return self.artifact(
            "RLS-TST-001",
            "release_record",
            "rejected",
            {
                "satisfies": ["REL-TST-001"],
                "includes_verification": ["VREC-TST-001"],
                "releases_work": ["WO-TST-001"],
            },
            extra,
        )

    def verification_record(self) -> bytes:
        extra = f'''commit = "{self.candidate}"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-21T13:00:00Z"
artifact_snapshot_sha256 = "{'a' * 64}"
evidence_paths = ["docs/engineering/release/evidence/WO-TST-001-check.md"]'''
        return self.artifact(
            "VREC-TST-002",
            "verification_record",
            "verified",
            {
                "verifies_work_order": ["WO-TST-001"],
                "conforms_to": ["VER-TST-001"],
            },
            extra,
        )

    def arguments(self) -> dict[str, object]:
        return {
            "record_id": "RLS-TST-002",
            "release_contract_id": "REL-TST-002",
            "verification_record_ids": ["VREC-TST-002"],
            "work_order_ids": ["WO-TST-001"],
            "version": "1.2.3",
            "authorized_by": "release-owner",
            "tag": "v1.2.3",
            "evaluator_python": self.python,
            "evaluator_entry_point": self.entry_point,
            "evaluator_wheel": self.wheel,
        }

    def fake_run(
        self,
        command: list[str],
        *,
        cwd: Path,
        input_bytes: bytes | None = None,
        timeout: int = PREPARATION.MAX_PROCESS_SECONDS,
    ) -> subprocess.CompletedProcess[bytes]:
        if "prepare-release" not in command:
            return self.real_run(command, cwd=cwd, input_bytes=input_bytes, timeout=timeout)
        output = command[command.index("--output") + 1]
        record = cwd / output
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_bytes(
            self.artifact(
                "RLS-TST-002",
                "release_record",
                "ready",
                {
                    "satisfies": ["REL-TST-002"],
                    "includes_verification": ["VREC-TST-002"],
                    "releases_work": ["WO-TST-001"],
                },
                f'''version = "1.2.3"
commit = "{self.candidate}"
git_object_format = "sha1"
released_at = "2026-08-21T14:00:00Z"
authorized_by = "release-owner"
tag = "v1.2.3"''',
            )
        )
        return subprocess.CompletedProcess(command, 0, b"", b"")

    def operation_patches(self):
        return (
            mock.patch.object(PREPARATION, "_candidate_validation"),
            mock.patch.object(
                PREPARATION.bootstrap,
                "_run_released_evaluator",
                return_value={"schema": "se-harness-runtime-identity-v2"},
            ),
            mock.patch.object(
                PREPARATION.bootstrap, "_installed_payload", return_value="c" * 64
            ),
            mock.patch.object(
                PREPARATION.bootstrap, "_wheel_payload", return_value="c" * 64
            ),
            mock.patch.object(PREPARATION, "_run", side_effect=self.fake_run),
        )

    def run_operation(self, *, apply: bool):
        operation = (
            PREPARATION.apply_predecessor_release
            if apply
            else PREPARATION.plan_predecessor_release
        )
        first, second, third, fourth, fifth = self.operation_patches()
        with first, second, third, fourth, fifth:
            return operation(self.root, **self.arguments())

    def test_plan_is_read_only_and_apply_imports_exact_two_path_view(self) -> None:
        plan = self.run_operation(apply=False)
        self.assertFalse(plan.applied)
        self.assertEqual(self.source, plan.source_commit)
        self.assertEqual(self.candidate, plan.candidate_commit)
        self.assertEqual(
            ["release_contract", "release_record"],
            sorted(item.artifact_type for item in plan.omitted_history),
        )
        self.assertFalse((self.root / plan.release_record_path).exists())
        self.assertFalse((self.root / plan.preparation_view_evidence_path).exists())
        self.assertEqual("", self.git("status", "--porcelain", "--untracked-files=all"))

        result = self.run_operation(apply=True)
        self.assertTrue(result.applied)
        self.assertTrue((self.root / result.release_record_path).is_file())
        evidence_path = self.root / result.preparation_view_evidence_path
        evidence_raw = evidence_path.read_bytes()
        self.assertEqual(result.preparation_view_evidence_sha256, sha256(evidence_raw))
        evidence = json.loads(evidence_raw)
        self.assertEqual(2, len(evidence["view"]["omitted_history"]))
        self.assertEqual(
            [
                "docs/engineering/release/release/REL-TST-001.md",
                "docs/engineering/release/releases/RLS-TST-001.md",
            ],
            [item["path"] for item in evidence["view"]["omitted_history"]],
        )
        replay = self.run_operation(apply=True)
        self.assertTrue(replay.applied)
        self.assertFalse(replay.changed)
        self.assertEqual(result.preparation_view_evidence_sha256, replay.preparation_view_evidence_sha256)

    def test_candidate_validator_binds_canonical_evidence_and_exact_command(self) -> None:
        result = self.run_operation(apply=True)
        artifacts, parse_errors = CANDIDATE_VALIDATOR.load_artifacts(
            self.root / "docs" / "engineering", self.root
        )
        self.assertEqual([], parse_errors)
        active = next(item for item in artifacts if item.artifact_id == "RLS-TST-002")
        contract = next(item for item in artifacts if item.artifact_id == "REL-TST-002")
        findings: list = []
        CANDIDATE_VALIDATOR._validate_predecessor_view_evidence(
            active,
            artifacts,
            findings,
            self.root,
            required=True,
            bootstrap_contract=contract.metadata["bootstrap"],
        )
        self.assertEqual([], findings)

        evidence_path = self.root / result.preparation_view_evidence_path
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        arguments = evidence["command"]["arguments"]
        arguments[arguments.index("--work-order") + 1] = "WO-TST-999"
        changed = (
            json.dumps(evidence, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
            + "\n"
        ).encode("utf-8")
        evidence_path.write_bytes(changed)
        active.metadata["preparation_view_evidence_sha256"] = sha256(changed)
        findings = []
        CANDIDATE_VALIDATOR._validate_predecessor_view_evidence(
            active,
            artifacts,
            findings,
            self.root,
            required=True,
            bootstrap_contract=contract.metadata["bootstrap"],
        )
        self.assertTrue(any("exact RLS preparation scope" in item.message for item in findings))

    def test_publication_replay_recomputes_view_and_predecessor_output_from_git(self) -> None:
        result = self.run_operation(apply=True)
        self.commit("integrate prepared record")
        head = self.git("rev-parse", "HEAD")
        record_path = result.release_record_path
        metadata = PUBLICATION._metadata_at(self.root, head, record_path)
        contract = PUBLICATION._metadata_at(
            self.root,
            head,
            "docs/engineering/release/release/REL-TST-002.md",
        )
        assert metadata is not None and contract is not None
        PUBLICATION._validated_preparation_view(
            self.root,
            head,
            record_path,
            metadata,
            contract["bootstrap"],
        )

        evidence_path = self.root / result.preparation_view_evidence_path
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        arguments = evidence["command"]["arguments"]
        arguments[arguments.index("--work-order") + 1] = "WO-TST-999"
        changed = (
            json.dumps(evidence, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
            + "\n"
        ).encode("utf-8")
        evidence_path.write_bytes(changed)
        record = self.root / record_path
        record.write_bytes(
            record.read_bytes().replace(
                result.preparation_view_evidence_sha256.encode("ascii"),
                sha256(changed).encode("ascii"),
            )
        )
        self.commit("tamper preparation command")
        head = self.git("rev-parse", "HEAD")
        metadata = PUBLICATION._metadata_at(self.root, head, record_path)
        assert metadata is not None
        with self.assertRaisesRegex(
            PUBLICATION.PublicationError,
            "command differs from the exact release scope",
        ):
            PUBLICATION._validated_preparation_view(
                self.root,
                head,
                record_path,
                metadata,
                contract["bootstrap"],
            )

    def test_partial_destination_and_second_write_failure_leave_no_new_pair(self) -> None:
        evidence_path = (
            self.root
            / "docs/engineering/release/evidence/RLS-TST-002-preparation-view.json"
        )
        evidence_path.write_bytes(b"occupied\n")
        self.commit("occupied destination")
        with self.assertRaisesRegex(
            PREPARATION.PredecessorPreparationError,
            "destination already exists or is partial",
        ):
            self.run_operation(apply=False)
        record_path = self.root / "docs/engineering/release/releases/RLS-TST-002.md"
        self.assertFalse(record_path.exists())
        self.assertEqual(b"occupied\n", evidence_path.read_bytes())

    def test_payload_mismatch_and_extra_sparse_omission_fail_without_outputs(self) -> None:
        patches = self.operation_patches()
        with patches[0], patches[1], mock.patch.object(
            PREPARATION.bootstrap, "_installed_payload", return_value="c" * 64
        ), mock.patch.object(
            PREPARATION.bootstrap, "_wheel_payload", return_value="d" * 64
        ), patches[4]:
            with self.assertRaisesRegex(
                PREPARATION.PredecessorPreparationError,
                "installed payload differs",
            ):
                PREPARATION.plan_predecessor_release(self.root, **self.arguments())
        self.assertFalse(
            (self.root / "docs/engineering/release/releases/RLS-TST-002.md").exists()
        )

        original_sparse = PREPARATION._sparse_spec

        def extra_sparse(history):
            return original_sparse(history) + b"!/README.md\n"

        patches = self.operation_patches()
        with patches[0], patches[1], patches[2], patches[3], patches[4], mock.patch.object(
            PREPARATION, "_sparse_spec", side_effect=extra_sparse
        ):
            with self.assertRaisesRegex(
                PREPARATION.PredecessorPreparationError,
                "omitted an unexpected path",
            ):
                PREPARATION.plan_predecessor_release(self.root, **self.arguments())
        self.assertFalse(
            (
                self.root
                / "docs/engineering/release/evidence/RLS-TST-002-preparation-view.json"
            ).exists()
        )

    def test_apply_rolls_back_evidence_when_record_exclusive_create_fails(self) -> None:
        real_open = PREPARATION.os.open
        calls = 0

        def failing_open(path, flags, mode=0o777):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected record creation failure")
            return real_open(path, flags, mode)

        first, second, third, fourth, fifth = self.operation_patches()
        with first, second, third, fourth, fifth, mock.patch.object(
            PREPARATION.os, "open", side_effect=failing_open
        ):
            with self.assertRaisesRegex(
                PREPARATION.PredecessorPreparationError,
                "injected record creation failure",
            ):
                PREPARATION.apply_predecessor_release(self.root, **self.arguments())
        self.assertFalse(
            (self.root / "docs/engineering/release/releases/RLS-TST-002.md").exists()
        )
        self.assertFalse(
            (
                self.root
                / "docs/engineering/release/evidence/RLS-TST-002-preparation-view.json"
            ).exists()
        )
        self.assertEqual("", self.git("status", "--porcelain", "--untracked-files=all"))

    def test_apply_detects_source_change_between_writes_and_rolls_back(self) -> None:
        real_open = PREPARATION.os.open
        calls = 0
        history_path = self.root / "docs/engineering/release/releases/RLS-TST-001.md"

        def changing_open(path, flags, mode=0o777):
            nonlocal calls
            calls += 1
            descriptor = real_open(path, flags, mode)
            if calls == 1:
                history_path.write_bytes(history_path.read_bytes() + b"changed\n")
            return descriptor

        first, second, third, fourth, fifth = self.operation_patches()
        with first, second, third, fourth, fifth, mock.patch.object(
            PREPARATION.os, "open", side_effect=changing_open
        ):
            with self.assertRaisesRegex(
                PREPARATION.PredecessorPreparationError,
                "tracked source changed after predecessor preparation",
            ):
                PREPARATION.apply_predecessor_release(self.root, **self.arguments())
        self.assertFalse(
            (self.root / "docs/engineering/release/releases/RLS-TST-002.md").exists()
        )
        self.assertFalse(
            (
                self.root
                / "docs/engineering/release/evidence/RLS-TST-002-preparation-view.json"
            ).exists()
        )


if __name__ == "__main__":
    unittest.main()
