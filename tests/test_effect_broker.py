from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

from se_harness.agent_contract import canonical_sha256, validate_contract
from se_harness.agent_contract import canonical_json_bytes
from se_harness.change_bundle import construct_change_bundle
from se_harness.effect_broker import (
    EffectBrokerError,
    apply_change_bundle,
    parse_effect_receipt_bytes,
    recover_effect_transaction,
    validate_effect_receipt,
)
from se_harness.repository_state import EvaluatorIdentity
from se_harness.runtime_state import (
    EFFECT_JOURNAL_SCHEMA,
    MAX_EFFECT_JOURNAL_BYTES,
    RuntimeStateError,
    RuntimeStateStore,
)


class EffectBrokerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.target = self.base / "target"
        self.baseline = self.base / "baseline"
        self.proposed = self.base / "proposed"
        self.objects = self.base / "objects"
        self.runtime = self.base / "runtime"
        for path in (self.target, self.baseline, self.proposed):
            path.mkdir()
        self._write(self.target, "files/delete.txt", b"delete")
        self._write(self.target, "files/replace.txt", b"before")
        self._write(self.baseline, "files/delete.txt", b"delete")
        self._write(self.baseline, "files/replace.txt", b"before")
        self._write(self.proposed, "files/replace.txt", b"after")
        self._write(self.proposed, "files/nested/create.txt", b"created")
        self.evaluator = EvaluatorIdentity("se-harness", "0.7.0", "3" * 64, "4" * 64)
        self.store = RuntimeStateStore(self.runtime, self.target)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @staticmethod
    def _write(root: Path, relative: str, content: bytes) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def _reset_effect_fixture(self) -> None:
        for path in (
            self.target,
            self.baseline,
            self.proposed,
            self.objects,
            self.runtime,
        ):
            if path.exists():
                for item in path.rglob("*"):
                    if item.is_file():
                        item.chmod(0o600)
                shutil.rmtree(path)
        for path in (self.target, self.baseline, self.proposed):
            path.mkdir()
        self._write(self.target, "files/delete.txt", b"delete")
        self._write(self.target, "files/replace.txt", b"before")
        self._write(self.baseline, "files/delete.txt", b"delete")
        self._write(self.baseline, "files/replace.txt", b"before")
        self._write(self.proposed, "files/replace.txt", b"after")
        self._write(self.proposed, "files/nested/create.txt", b"created")
        self.store = RuntimeStateStore(self.runtime, self.target)

    def _manifest(self) -> str:
        values = [
            {
                "path": path.relative_to(self.target).as_posix(),
                "sha256": __import__("hashlib").sha256(path.read_bytes()).hexdigest(),
                "size": path.stat().st_size,
            }
            for path in sorted(self.target.rglob("*"), key=lambda item: item.as_posix())
            if path.is_file()
        ]
        return canonical_sha256(values)

    def _observation(self):
        return validate_contract(
            {
                "schema": "se-harness-repository-observation-v1",
                "repository": "a" * 64,
                "evaluator": self.evaluator.as_dict(),
                "git": {
                    "object_format": "sha1",
                    "head": "b" * 40,
                    "symbolic_ref": "refs/heads/main",
                    "index_entries_sha256": "c" * 64,
                    "tracked_worktree_sha256": "d" * 64,
                    "untracked_nonignored_sha256": "e" * 64,
                    "conflicts": False,
                    "submodules": False,
                },
                "governance": {
                    "managed_lock_sha256": "f" * 64,
                    "formal_snapshot_sha256": "1" * 64,
                    "workflow_contract_sha256": "2" * 64,
                    "decision_rights_sha256": "3" * 64,
                    "work_order": "WO-AEX-006",
                    "work_order_sha256": "4" * 64,
                    "work_order_status": "in_progress",
                },
                "filesystem": {
                    "platform_family": "windows",
                    "case_sensitive": False,
                    "regular_file_manifest_sha256": self._manifest(),
                    "unsupported_object_count": 0,
                },
                "previous_receipt_sha256": None,
            }
        )

    def _envelope(self, observation, nonce: str):
        return validate_contract(
            {
                "schema": "se-harness-autonomy-envelope-v2",
                "selection": {
                    "work_order": "WO-AEX-006",
                    "work_order_sha256": "4" * 64,
                    "repository_state": observation.sha256,
                    "evaluator_payload_sha256": self.evaluator.payload_sha256,
                },
                "delegation": {
                    "asserted_by": "engineering-owner",
                    "operations": ["change-bundle-apply"],
                    "path_scope": ["files/"],
                    "execution_profiles": ["implementer"],
                    "max_parallel_writers": 1,
                    "retry_limits": {"change-bundle-apply": 0},
                    "stop_before": [
                        "accountable-decision-required",
                        "action-time-authorization-required",
                    ],
                },
                "evidence": {"required_receipt": True, "required_paths": []},
                "authority": {
                    "decision_right": None,
                    "delegate": "worker",
                    "execution_profile": "implementer",
                    "delegation_sha256": "5" * 64,
                    "work_order_sha256": "4" * 64,
                    "expected_repository_state": observation.sha256,
                    "previous_receipt_sha256": None,
                    "nonce": nonce,
                    "issued_at": "2026-08-25T10:00:00Z",
                    "not_after": "2026-08-25T10:05:00Z",
                    "retry_ordinal": 0,
                },
            }
        )

    def _inputs(self, nonce: str = "6" * 32):
        before = self._observation()
        envelope = self._envelope(before, nonce)
        bundle = construct_change_bundle(
            baseline_workspace=self.baseline,
            proposed_workspace=self.proposed,
            object_store=self.objects,
            work_order="WO-AEX-006",
            envelope_sha256=envelope.sha256,
            repository_state_before=before.sha256,
            intended_deletions=("files/delete.txt",),
        )
        session = self.store.start_session(
            before.value["repository"],
            "test operator",
            started_at="2026-08-25T10:00:00Z",
        )
        return before, envelope, bundle, session

    def _apply(self, envelope, bundle, session, **overrides):
        values = {
            "repository": self.target,
            "bundle_bytes": bundle.bundle.canonical_bytes,
            "object_store": self.objects,
            "envelope": envelope,
            "current_delegation_sha256": "5" * 64,
            "evaluator": self.evaluator,
            "runtime_store": self.store,
            "session": session,
            "gates_passed": True,
            "now": lambda: datetime(2026, 8, 25, 10, 0, 1, tzinfo=UTC),
            "observer": lambda *_args, **_kwargs: self._observation(),
            "authority_guard": lambda *_args, **_kwargs: SimpleNamespace(
                identity=SimpleNamespace(
                    evaluator_payload_sha256=self.evaluator.payload_sha256
                )
            ),
            "transaction_id_factory": lambda: "7" * 32,
        }
        values.update(overrides)
        return apply_change_bundle(**values)

    def test_create_replace_delete_commit_and_exact_receipt(self) -> None:
        _, envelope, bundle, session = self._inputs()
        result = self._apply(envelope, bundle, session)
        self.assertEqual("committed", result.outcome)
        self.assertEqual(b"after", (self.target / "files/replace.txt").read_bytes())
        self.assertEqual(b"created", (self.target / "files/nested/create.txt").read_bytes())
        self.assertFalse((self.target / "files/delete.txt").exists())
        self.assertEqual("committed", json.loads(result.journal_path.read_bytes())["state"])
        self.assertEqual(result.receipt.sha256, validate_effect_receipt(result.receipt.value).sha256)
        self.assertEqual(
            result.receipt.sha256,
            parse_effect_receipt_bytes(result.receipt.canonical_bytes).sha256,
        )
        self.assertEqual(
            ["files/delete.txt", "files/nested/create.txt", "files/replace.txt"],
            [item["path"] for item in result.receipt.value["entries"]],
        )
        self.assertNotIn("authority", result.receipt.value)
        self.assertIsNone(self.store.read_effect_journal(session.repository_id))
        self.store.close_session(session)

    def test_independent_canonical_receipt_reference_vector_is_exact(self) -> None:
        vector_path = (
            Path(__file__).resolve().parents[1]
            / "tests/fixtures/agentic_execution/phase4/broker/canonical-vectors.json"
        )
        vector = json.loads(vector_path.read_text(encoding="utf-8"))["receipt"]
        receipt = parse_effect_receipt_bytes(vector["canonical"].encode("utf-8"))
        self.assertEqual(vector["sha256"], receipt.sha256)
        self.assertEqual(vector["canonical"].encode("utf-8"), receipt.canonical_bytes)

    def test_oversized_effect_journal_is_rejected_before_persistence(self) -> None:
        session = self.store.start_session("a" * 64, "journal-bound-test")
        accepted = {
            "schema": EFFECT_JOURNAL_SCHEMA,
            "repository_id": session.repository_id,
            "session_id": session.session_id,
            "transaction_id": "b" * 32,
            "state": "rolled-back",
            "padding": ["x" * 4_096 for _ in range(300)],
        }
        accepted_bytes = canonical_json_bytes(
            accepted, maximum_bytes=MAX_EFFECT_JOURNAL_BYTES
        )
        self.assertGreater(len(accepted_bytes), 1_048_576)
        self.assertLess(len(accepted_bytes), MAX_EFFECT_JOURNAL_BYTES)
        self.store.begin_effect_transaction(session, accepted)
        self.assertEqual(
            accepted,
            self.store.read_effect_journal(session.repository_id),
        )
        self.store.archive_effect_transaction(session, "b" * 32)

        journal = {
            "schema": EFFECT_JOURNAL_SCHEMA,
            "repository_id": session.repository_id,
            "session_id": session.session_id,
            "transaction_id": "a" * 32,
            "padding": ["x" * 4_096 for _ in range(1_024)],
        }
        encoded = canonical_json_bytes(
            journal, maximum_bytes=MAX_EFFECT_JOURNAL_BYTES + 65_536
        )
        self.assertGreater(len(encoded), MAX_EFFECT_JOURNAL_BYTES)
        try:
            with self.assertRaisesRegex(RuntimeStateError, "AEXRT002"):
                self.store.begin_effect_transaction(session, journal)
            self.assertIsNone(self.store.read_effect_journal(session.repository_id))
        finally:
            self.store.close_session(session)

    def test_injected_apply_failure_restores_exact_prior_state(self) -> None:
        before_bytes = {
            path.relative_to(self.target).as_posix(): path.read_bytes()
            for path in self.target.rglob("*")
            if path.is_file()
        }
        _, envelope, bundle, session = self._inputs("8" * 32)

        def fail(stage: str) -> None:
            if stage.startswith("after-apply:"):
                raise OSError("injected apply fault")

        with self.assertRaisesRegex(EffectBrokerError, "prior state was restored"):
            self._apply(envelope, bundle, session, fault=fail)
        after_bytes = {
            path.relative_to(self.target).as_posix(): path.read_bytes()
            for path in self.target.rglob("*")
            if path.is_file()
        }
        self.assertEqual(before_bytes, after_bytes)
        self.assertIsNone(self.store.read_effect_journal(session.repository_id))
        self.store.close_session(session)

    def test_every_in_process_fault_phase_restores_prior_state(self) -> None:
        stages = (
            "before-journal",
            "after-journal-prepared",
            "after-parent:files/nested",
            "after-temp:files/nested/create.txt",
            "after-temp:files/replace.txt",
            "after-apply:files/delete.txt",
            "after-apply:files/nested/create.txt",
            "after-apply:files/replace.txt",
            "before-result-observation",
            "before-receipt",
            "before-commit",
        )
        for index, selected in enumerate(stages, start=1):
            with self.subTest(stage=selected):
                if index > 1:
                    self._reset_effect_fixture()
                before_manifest = self._manifest()
                _, envelope, bundle, session = self._inputs(f"{index:032x}")

                def fail(stage: str) -> None:
                    if stage == selected:
                        raise OSError(f"injected fault at {selected}")

                try:
                    with self.assertRaisesRegex(
                        EffectBrokerError, "prior state was restored"
                    ):
                        self._apply(envelope, bundle, session, fault=fail)
                    self.assertEqual(before_manifest, self._manifest())
                    self.assertIsNone(
                        self.store.read_effect_journal(session.repository_id)
                    )
                    self.assertFalse(list(self.runtime.rglob("receipt.json")))
                finally:
                    self.store.close_session(session)

    def test_post_commit_fault_requires_recovery_then_returns_exact_result(self) -> None:
        _, envelope, bundle, session = self._inputs("7" * 32)

        def fail(stage: str) -> None:
            if stage == "after-journal-commit":
                raise OSError("injected post-commit finalization fault")

        with self.assertRaisesRegex(EffectBrokerError, "AEXEFF013"):
            self._apply(envelope, bundle, session, fault=fail)
        journal = self.store.read_effect_journal(session.repository_id)
        self.assertEqual("committed", journal["state"])
        recovered = recover_effect_transaction(
            self.target, runtime_store=self.store, session=session
        )
        self.assertEqual("recovered-result", recovered.outcome)
        self.assertIsNotNone(recovered.receipt)
        self.assertEqual(b"after", (self.target / "files/replace.txt").read_bytes())
        self.store.close_session(session)
        next_session = self.store.start_session(
            session.repository_id, "post-recovery operator"
        )
        self.store.close_session(next_session)

    def test_interruption_leaves_journal_and_restart_recovers_prior(self) -> None:
        before_manifest = self._manifest()
        _, envelope, bundle, session = self._inputs("9" * 32)

        def interrupt(stage: str) -> None:
            if stage.startswith("after-apply:"):
                raise SystemExit("simulated process termination")

        with self.assertRaises(SystemExit):
            self._apply(envelope, bundle, session, fault=interrupt)
        self.assertIsNotNone(self.store.read_effect_journal(session.repository_id))
        recovered = recover_effect_transaction(
            self.target, runtime_store=self.store, session=session
        )
        self.assertEqual("recovered-prior", recovered.outcome)
        self.assertEqual(before_manifest, self._manifest())
        self.assertIsNone(self.store.read_effect_journal(session.repository_id))
        self.store.close_session(session)

    def test_interruption_at_each_noncommitted_durable_phase_recovers_prior(self) -> None:
        stages = (
            "after-journal-prepared",
            "after-apply:files/delete.txt",
            "after-apply:files/nested/create.txt",
            "after-apply:files/replace.txt",
            "before-receipt",
        )
        for index, selected in enumerate(stages, start=16):
            with self.subTest(stage=selected):
                if index > 16:
                    self._reset_effect_fixture()
                before_manifest = self._manifest()
                _, envelope, bundle, session = self._inputs(f"{index:032x}")

                def interrupt(stage: str) -> None:
                    if stage == selected:
                        raise SystemExit(f"simulated termination at {selected}")

                try:
                    with self.assertRaises(SystemExit):
                        self._apply(envelope, bundle, session, fault=interrupt)
                    self.assertIsNotNone(
                        self.store.read_effect_journal(session.repository_id)
                    )
                    recovered = recover_effect_transaction(
                        self.target,
                        runtime_store=self.store,
                        session=session,
                    )
                    self.assertEqual("recovered-prior", recovered.outcome)
                    self.assertEqual(before_manifest, self._manifest())
                    self.assertIsNone(
                        self.store.read_effect_journal(session.repository_id)
                    )
                finally:
                    self.store.close_session(session)

    def test_process_exit_releases_locks_and_new_store_recovers_journal(self) -> None:
        script = """
import hashlib
import os
import sys
from pathlib import Path
from se_harness.agent_contract import canonical_sha256
from se_harness.effect_broker import _manifest_sha256, _snapshot
from se_harness.runtime_state import EFFECT_JOURNAL_SCHEMA, RuntimeStateStore

target, runtime = Path(sys.argv[1]), Path(sys.argv[2])
store = RuntimeStateStore(runtime, target)
session = store.start_session("a" * 64, "test operator", started_at="2026-08-25T10:00:00Z")
nonce = "c" * 32
store.consume_nonce(
    session,
    nonce=nonce,
    envelope_sha256="d" * 64,
    repository_state_sha256="e" * 64,
    admitted_at="2026-08-25T10:00:01Z",
)
transaction = "f" * 32
manifest = _manifest_sha256(_snapshot(target))
plan = {
    "bundle_sha256": "1" * 64,
    "envelope_sha256": "d" * 64,
    "entries": [],
    "prior_manifest_sha256": manifest,
    "expected_manifest_sha256": manifest,
    "created_parents": [],
    "temporaries": [],
}
store.effect_material_directory(session, transaction)
with store.effect_lock(session):
    store.begin_effect_transaction(
        session,
        {
            "schema": EFFECT_JOURNAL_SCHEMA,
            "repository_id": "a" * 64,
            "session_id": session.session_id,
            "transaction_id": transaction,
            "state": "prepared",
            "bundle_sha256": "1" * 64,
            "envelope_sha256": "d" * 64,
            "nonce_sha256": hashlib.sha256(nonce.encode("ascii")).hexdigest(),
            "work_order": "WO-AEX-006",
            "state_before": "e" * 64,
            "state_after": None,
            "previous_receipt_sha256": None,
            "entries": [],
            "prior_manifest_sha256": manifest,
            "expected_manifest_sha256": manifest,
            "plan_sha256": canonical_sha256(plan),
            "created_parents": [],
            "temporaries": [],
            "applied": [],
            "receipt_sha256": None,
            "uncertain_paths": [],
            "started_at": "2026-08-25T10:00:01Z",
        },
    )
    os._exit(0)
"""
        completed = subprocess.run(
            [sys.executable, "-c", script, str(self.target), str(self.runtime)],
            cwd=Path(__file__).resolve().parents[1],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(0, completed.returncode, completed.stderr.decode("utf-8"))
        resumed_store = RuntimeStateStore(self.runtime, self.target)
        resumed = resumed_store.resume_session("a" * 64, "test operator")
        with resumed_store.effect_lock(resumed):
            pass
        recovered = recover_effect_transaction(
            self.target, runtime_store=resumed_store, session=resumed
        )
        self.assertEqual("recovered-prior", recovered.outcome)
        resumed_store.close_session(resumed)

    def test_corrupt_recovery_material_stops_for_human_recovery(self) -> None:
        _, envelope, bundle, session = self._inputs("d" * 32)

        def interrupt(stage: str) -> None:
            if stage == "after-apply:files/delete.txt":
                raise SystemExit("simulated process termination")

        with self.assertRaises(SystemExit):
            self._apply(envelope, bundle, session, fault=interrupt)
        backups = list(self.runtime.rglob("backups/*"))
        self.assertTrue(backups)
        deleted_digest = __import__("hashlib").sha256(b"delete").hexdigest()
        backup = next(path for path in backups if path.name == deleted_digest)
        backup.chmod(0o600)
        backup.write_bytes(b"corrupt")
        with self.assertRaisesRegex(EffectBrokerError, "AEXEFF014"):
            recover_effect_transaction(
                self.target, runtime_store=self.store, session=session
            )
        journal = self.store.read_effect_journal(session.repository_id)
        self.assertEqual("human-recovery-stop", journal["state"])
        self.store.close_session(session)
        with self.assertRaisesRegex(Exception, "AEXRT006"):
            self.store.start_session(
                "a" * 64,
                "test operator",
                started_at="2026-08-25T10:00:02Z",
            )

    def test_interruption_after_journal_commit_recovers_exact_receipt(self) -> None:
        _, envelope, bundle, session = self._inputs("1" * 32)

        def interrupt(stage: str) -> None:
            if stage == "after-journal-commit":
                raise SystemExit("simulated post-commit termination")

        with self.assertRaises(SystemExit):
            self._apply(envelope, bundle, session, fault=interrupt)
        recovered = recover_effect_transaction(
            self.target, runtime_store=self.store, session=session
        )
        self.assertEqual("recovered-result", recovered.outcome)
        self.assertIsNotNone(recovered.receipt)
        self.assertEqual(
            recovered.receipt.sha256,
            json.loads(recovered.journal_path.read_bytes())["receipt_sha256"],
        )
        self.assertEqual(b"after", (self.target / "files/replace.txt").read_bytes())
        self.store.close_session(session)

    def test_identity_scope_and_managed_denials_consume_nonce_without_write(self) -> None:
        before_manifest = self._manifest()
        _, envelope, bundle, session = self._inputs("a" * 32)
        value = copy.deepcopy(bundle.bundle.value)
        value["identity"]["repository_state_before"] = "0" * 64
        bad_bytes = (
            json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n"
        ).encode("utf-8")
        with self.assertRaisesRegex(EffectBrokerError, "AEXEFF004"):
            self._apply(
                envelope,
                bundle,
                session,
                bundle_bytes=bad_bytes,
            )
        self.assertEqual(before_manifest, self._manifest())
        self.store.close_session(session)

    def test_scope_and_managed_deny_paths_stop_before_target_write(self) -> None:
        before = self._observation()
        envelope = self._envelope(before, "2" * 32)
        self._write(self.proposed, "outside.txt", b"outside")
        bundle = construct_change_bundle(
            baseline_workspace=self.baseline,
            proposed_workspace=self.proposed,
            object_store=self.objects,
            work_order="WO-AEX-006",
            envelope_sha256=envelope.sha256,
            repository_state_before=before.sha256,
            intended_deletions=("files/delete.txt",),
        )
        session = self.store.start_session(before.value["repository"], "scope-test")
        try:
            with self.assertRaisesRegex(EffectBrokerError, "outside scope"):
                self._apply(envelope, bundle, session)
            self.assertFalse((self.target / "outside.txt").exists())
            self.assertIsNone(self.store.read_effect_journal(session.repository_id))
        finally:
            self.store.close_session(session)

        self._reset_effect_fixture()
        before = self._observation()
        value = copy.deepcopy(self._envelope(before, "3" * 32).value)
        value["delegation"]["path_scope"] = [".git/", "files/"]
        envelope = validate_contract(value)
        self._write(self.proposed, ".git/config", b"proposed git metadata")
        bundle = construct_change_bundle(
            baseline_workspace=self.baseline,
            proposed_workspace=self.proposed,
            object_store=self.objects,
            work_order="WO-AEX-006",
            envelope_sha256=envelope.sha256,
            repository_state_before=before.sha256,
            intended_deletions=("files/delete.txt",),
        )
        session = self.store.start_session(before.value["repository"], "deny-test")
        try:
            with self.assertRaisesRegex(EffectBrokerError, "managed-denied"):
                self._apply(envelope, bundle, session)
            self.assertFalse((self.target / ".git").exists())
            self.assertIsNone(self.store.read_effect_journal(session.repository_id))
        finally:
            self.store.close_session(session)

    def test_hard_link_alias_in_target_stops_before_journal(self) -> None:
        os.link(
            self.target / "files/replace.txt",
            self.target / "files/replace-alias.txt",
        )
        before_manifest = self._manifest()
        _, envelope, bundle, session = self._inputs("4" * 32)
        try:
            with self.assertRaisesRegex(EffectBrokerError, "AEXEFF006"):
                self._apply(envelope, bundle, session)
            self.assertEqual(before_manifest, self._manifest())
            self.assertIsNone(self.store.read_effect_journal(session.repository_id))
        finally:
            self.store.close_session(session)

    def test_preexisting_planned_temporary_is_preserved_and_rejected(self) -> None:
        transaction = "9" * 32
        temporary = self.target / "files" / f".se-harness-{transaction}-2.tmp"
        temporary.write_bytes(b"user-owned collision")
        before_manifest = self._manifest()
        _, envelope, bundle, session = self._inputs("8" * 32)
        try:
            with self.assertRaisesRegex(EffectBrokerError, "AEXEFF009"):
                self._apply(
                    envelope,
                    bundle,
                    session,
                    transaction_id_factory=lambda: transaction,
                )
            self.assertEqual(b"user-owned collision", temporary.read_bytes())
            self.assertEqual(before_manifest, self._manifest())
            self.assertIsNone(self.store.read_effect_journal(session.repository_id))
        finally:
            self.store.close_session(session)

    @unittest.skipUnless(os.name == "nt", "Windows locked-file replacement case")
    def test_locked_destination_rolls_back_prior_entries_on_windows(self) -> None:
        before_manifest = self._manifest()
        _, envelope, bundle, session = self._inputs("9" * 32)
        handle = (self.target / "files/replace.txt").open("rb")
        try:
            with self.assertRaisesRegex(EffectBrokerError, "AEXEFF010"):
                self._apply(envelope, bundle, session)
            self.assertEqual(before_manifest, self._manifest())
            self.assertEqual(
                b"before", (self.target / "files/replace.txt").read_bytes()
            )
            self.assertIsNone(self.store.read_effect_journal(session.repository_id))
        finally:
            handle.close()
            self.store.close_session(session)

    def test_direct_write_during_preflight_is_detected_and_not_receipted(self) -> None:
        _, envelope, bundle, session = self._inputs("e" * 32)
        calls = 0

        def observer(*_args, **_kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                self._write(self.target, "outside.txt", b"direct worker write")
            return self._observation()

        with self.assertRaisesRegex(EffectBrokerError, "AEXEFF007"):
            self._apply(envelope, bundle, session, observer=observer)
        self.assertEqual(b"before", (self.target / "files/replace.txt").read_bytes())
        self.assertEqual(b"delete", (self.target / "files/delete.txt").read_bytes())
        self.assertFalse((self.target / "files/nested/create.txt").exists())
        self.assertIsNone(self.store.read_effect_journal(session.repository_id))
        self.store.close_session(session)

    def test_result_observer_and_receipt_validation_failures_roll_back(self) -> None:
        before_manifest = self._manifest()
        _, envelope, bundle, session = self._inputs("5" * 32)
        calls = 0

        def failing_observer(*_args, **_kwargs):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("injected result observation failure")
            return self._observation()

        try:
            with self.assertRaisesRegex(
                EffectBrokerError, "prior state was restored"
            ):
                self._apply(
                    envelope,
                    bundle,
                    session,
                    observer=failing_observer,
                )
            self.assertEqual(before_manifest, self._manifest())
            self.assertIsNone(self.store.read_effect_journal(session.repository_id))
        finally:
            self.store.close_session(session)

        self._reset_effect_fixture()
        before_manifest = self._manifest()
        _, envelope, bundle, session = self._inputs("6" * 32)
        try:
            with self.assertRaisesRegex(EffectBrokerError, "AEXEFF015"):
                self._apply(
                    envelope,
                    bundle,
                    session,
                    evidence=({"unexpected": "field"},),
                )
            self.assertEqual(before_manifest, self._manifest())
            self.assertIsNone(self.store.read_effect_journal(session.repository_id))
            self.assertFalse(list(self.runtime.rglob("receipt.json")))
        finally:
            self.store.close_session(session)

    def test_receipt_rejects_authority_fields_and_writer_lock_is_exclusive(self) -> None:
        _, envelope, bundle, session = self._inputs("b" * 32)
        with self.store.effect_lock(session):
            with self.assertRaisesRegex(Exception, "AEXRT011"):
                with self.store.effect_lock(session):
                    pass
        result = self._apply(envelope, bundle, session)
        attacked = copy.deepcopy(result.receipt.value)
        attacked["authority"] = {"approved": True}
        with self.assertRaisesRegex(EffectBrokerError, "AEXEFF015"):
            validate_effect_receipt(attacked)
        self.store.close_session(session)

    def test_checksum_mismatched_journal_blocks_recovery(self) -> None:
        _, envelope, bundle, session = self._inputs("f" * 32)

        def interrupt(stage: str) -> None:
            if stage == "after-journal-prepared":
                raise SystemExit("simulated process termination")

        with self.assertRaises(SystemExit):
            self._apply(envelope, bundle, session, fault=interrupt)
        journal_path = next(self.runtime.rglob("effect-journal.json"))
        value = json.loads(journal_path.read_bytes())
        value["bundle_sha256"] = "0" * 64
        journal_path.write_bytes(canonical_json_bytes(value))
        with self.assertRaisesRegex(EffectBrokerError, "AEXEFF014"):
            recover_effect_transaction(
                self.target, runtime_store=self.store, session=session
            )
        self.store.close_session(session)


if __name__ == "__main__":
    unittest.main()
