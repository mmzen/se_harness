from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

from se_harness.agent_contract import ReceiptExpectations, validate_contract
from se_harness.delegated_authority import (
    AuthorityRequest,
    DelegatedAuthorityError,
    DelegationPolicy,
    admit_fresh_envelope,
    derive_autonomy_envelope_v2,
    resolve_delegation,
    verify_receipt_state_chain,
)
from se_harness.repository_state import StableRepositoryObservation
from se_harness.runtime_state import RuntimeStateError, RuntimeStateStore
from tests.test_agent_contract import phase2_receipt


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VECTORS = (
    REPOSITORY_ROOT
    / "tests/fixtures/agentic_execution/phase4/authority/canonical-vectors.json"
)


def _policy() -> DelegationPolicy:
    return DelegationPolicy(
        decision_right_delegators={
            "DR-WO-START": frozenset({"engineering-owner"}),
            "DR-WO-COMPLETE": frozenset({"engineering-owner"}),
        },
        operations=frozenset({"change-bundle-apply", "delegated-work-order-start"}),
        execution_profiles=frozenset({"implementer"}),
        delegates=frozenset({"implementation-worker"}),
        operation_statuses={
            "change-bundle-apply": frozenset({"in_progress"}),
            "delegated-work-order-start": frozenset({"approved"}),
        },
    )


def _work_order(
    *,
    status: str = "in_progress",
    operation: str = "change-bundle-apply",
    valid_until: str = "2030-01-01T00:00:00Z",
    paths: tuple[str, ...] = ("docs/",),
) -> bytes:
    path_lines = ", ".join(json.dumps(item) for item in paths)
    return f"""+++
id = "WO-TST-002"
type = "work_order"
title = "Delegation fixture"
status = "{status}"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[execution_scope]
paths = ["docs/"]

[agentic_delegation]
schema = "se-harness-agentic-delegation-v1"
delegated_by = "engineering-owner"
delegate = "implementation-worker"
decision_rights = []
operations = ["{operation}"]
execution_profiles = ["implementer"]
paths = [{path_lines}]
required_evidence = [
  {{ kind = "verification", path = "docs/evidence.json" }},
]
valid_until = "{valid_until}"
max_retry = 1
max_parallel_writers = 1
child_delegation = false
stop_before = [
  "accountable-decision-required",
  "action-time-authorization-required",
]
+++

# Delegation fixture
""".encode("utf-8")


def _observation(work_order: bytes, *, previous: str | None = None):
    value = json.loads(VECTORS.read_text(encoding="utf-8"))["repository_observation"]["value"]
    value["governance"]["work_order_sha256"] = __import__("hashlib").sha256(work_order).hexdigest()
    value["governance"]["work_order_status"] = "in_progress"
    value["previous_receipt_sha256"] = previous
    return validate_contract(value)


def _request() -> AuthorityRequest:
    return AuthorityRequest(
        operation="change-bundle-apply",
        decision_right=None,
        delegate="implementation-worker",
        execution_profile="implementer",
        paths=("docs/",),
        required_evidence=(("verification", "docs/evidence.json"),),
        retry_ordinal=0,
    )


class DelegationAndEnvelopeTests(unittest.TestCase):
    def test_concurrent_nonce_replay_has_exactly_one_winner(self) -> None:
        with tempfile.TemporaryDirectory() as parent:
            target = Path(parent) / "target"
            target.mkdir()
            store = RuntimeStateStore(Path(parent) / "runtime", target)
            session = store.start_session(
                "1" * 64,
                "operator",
                started_at="2026-08-25T10:00:00Z",
            )

            def attempt() -> str:
                try:
                    store.consume_nonce(
                        session,
                        nonce="34" * 16,
                        envelope_sha256="2" * 64,
                        repository_state_sha256="3" * 64,
                        admitted_at="2026-08-25T10:00:01Z",
                    )
                    return "admitted"
                except RuntimeStateError as exc:
                    return exc.code

            with ThreadPoolExecutor(max_workers=2) as executor:
                outcomes = sorted(executor.map(lambda _: attempt(), range(2)))
            self.assertEqual(["AEXRT008", "admitted"], outcomes)
            store.close_session(session)

    def test_resolution_derivation_expiry_and_narrowing(self) -> None:
        raw = _work_order()
        resolved = resolve_delegation(raw, _policy())
        stable = StableRepositoryObservation(_observation(raw), 2, True)
        issued = datetime(2026, 8, 25, 10, 0, tzinfo=UTC)
        result = derive_autonomy_envelope_v2(
            stable_observation=stable,
            delegation=resolved,
            policy=_policy(),
            request=_request(),
            issued_at=issued,
            gates_passed=True,
            nonce_factory=lambda: "ab" * 16,
        )
        self.assertEqual("derived", result.outcome)
        self.assertEqual(
            "2026-08-25T10:05:00Z",
            result.envelope.value["authority"]["not_after"],
        )
        self.assertEqual(
            stable.document.sha256,
            result.envelope.value["authority"]["expected_repository_state"],
        )
        self.assertIn("No effect was admitted", " ".join(result.non_effects))

        shorter = derive_autonomy_envelope_v2(
            stable_observation=stable,
            delegation=resolved,
            policy=_policy(),
            request=_request(),
            issued_at=issued,
            managed_not_after=datetime(2026, 8, 25, 10, 1, tzinfo=UTC),
            gates_passed=True,
            nonce_factory=lambda: "cd" * 16,
        )
        self.assertEqual(
            "2026-08-25T10:01:00Z",
            shorter.envelope.value["authority"]["not_after"],
        )

    def test_delegation_and_request_widening_fail_closed(self) -> None:
        with self.assertRaisesRegex(DelegatedAuthorityError, "AEXAUTH005"):
            resolve_delegation(_work_order(operation="unknown-operation"), _policy())
        with self.assertRaisesRegex(DelegatedAuthorityError, "AEXAUTH004"):
            resolve_delegation(_work_order(paths=("docs/", "outside/")), _policy())

        raw = _work_order()
        resolved = resolve_delegation(raw, _policy())
        stable = StableRepositoryObservation(_observation(raw), 2, True)
        request = copy.deepcopy(_request())
        object.__setattr__(request, "paths", ("outside/",))
        with self.assertRaisesRegex(DelegatedAuthorityError, "AEXAUTH004"):
            derive_autonomy_envelope_v2(
                stable_observation=stable,
                delegation=resolved,
                policy=_policy(),
                request=request,
                issued_at=datetime(2026, 8, 25, tzinfo=UTC),
                gates_passed=True,
            )
        with self.assertRaisesRegex(DelegatedAuthorityError, "AEXAUTH009"):
            derive_autonomy_envelope_v2(
                stable_observation=stable,
                delegation=resolved,
                policy=_policy(),
                request=_request(),
                issued_at=datetime(2026, 8, 25, tzinfo=UTC),
                gates_passed=False,
            )
        dirty = StableRepositoryObservation(_observation(raw), 2, False)
        with self.assertRaisesRegex(DelegatedAuthorityError, "AEXAUTH014"):
            derive_autonomy_envelope_v2(
                stable_observation=dirty,
                delegation=resolved,
                policy=_policy(),
                request=_request(),
                issued_at=datetime(2026, 8, 25, tzinfo=UTC),
                gates_passed=True,
            )

    def test_external_runtime_admission_replay_revocation_and_recovery(self) -> None:
        raw = _work_order()
        resolved = resolve_delegation(raw, _policy())
        stable = StableRepositoryObservation(_observation(raw), 2, True)
        issued = datetime(2026, 8, 25, 10, 0, tzinfo=UTC)
        derived = derive_autonomy_envelope_v2(
            stable_observation=stable,
            delegation=resolved,
            policy=_policy(),
            request=_request(),
            issued_at=issued,
            gates_passed=True,
            nonce_factory=lambda: "ef" * 16,
        )
        with tempfile.TemporaryDirectory() as parent:
            target = Path(parent) / "target"
            target.mkdir()
            runtime = Path(parent) / "runtime"
            store = RuntimeStateStore(runtime, target)
            session = store.start_session(
                stable.document.value["repository"],
                "operator assertion",
                started_at="2026-08-25T10:00:00Z",
            )
            with self.assertRaisesRegex(RuntimeStateError, "AEXRT003"):
                store.start_session(
                    stable.document.value["repository"],
                    "second operator",
                    started_at="2026-08-25T10:00:00Z",
                )
            admitted = admit_fresh_envelope(
                envelope=derived.envelope,
                fresh_observation=stable.document,
                current_delegation_sha256=resolved.document.sha256,
                now=datetime(2026, 8, 25, 10, 0, 1, tzinfo=UTC),
                runtime_store=store,
                session=session,
                gates_passed=True,
            )
            self.assertEqual("admitted", admitted.outcome)
            with self.assertRaisesRegex(RuntimeStateError, "AEXRT008"):
                admit_fresh_envelope(
                    envelope=derived.envelope,
                    fresh_observation=stable.document,
                    current_delegation_sha256=resolved.document.sha256,
                    now=datetime(2026, 8, 25, 10, 0, 2, tzinfo=UTC),
                    runtime_store=store,
                    session=session,
                    gates_passed=True,
                )
            terminal = store.record_terminal(
                session,
                nonce="ef" * 16,
                outcome="failed-consumed",
                recorded_at="2026-08-25T10:00:03Z",
            )
            self.assertEqual("failed-consumed", terminal["outcome"])
            store.revoke_delegation(
                session,
                resolved.document.sha256,
                revoked_at="2026-08-25T10:00:04Z",
            )
            self.assertTrue(
                store.is_revoked(
                    stable.document.value["repository"], resolved.document.sha256
                )
            )
            store.mark_recovery_required(
                session,
                "interrupted effect",
                recorded_at="2026-08-25T10:00:05Z",
            )
            store.close_session(session)
            with self.assertRaisesRegex(RuntimeStateError, "AEXRT006"):
                store.start_session(
                    stable.document.value["repository"],
                    "operator",
                    started_at="2026-08-25T10:00:06Z",
                )
            store.acknowledge_recovery(
                stable.document.value["repository"],
                acknowledged_at="2026-08-25T10:00:07Z",
            )
            resumed = store.start_session(
                stable.document.value["repository"],
                "operator",
                started_at="2026-08-25T10:00:08Z",
            )
            store.close_session(resumed)
            if os.name != "nt":
                self.assertEqual(0o700, runtime.stat().st_mode & 0o777)
            with self.assertRaisesRegex(RuntimeStateError, "AEXRT005"):
                RuntimeStateStore(target / "runtime", target)

    def test_expiry_fresh_state_and_receipt_chain_are_exact(self) -> None:
        raw = _work_order()
        resolved = resolve_delegation(raw, _policy())
        stable = StableRepositoryObservation(_observation(raw), 2, True)
        issued = datetime(2026, 8, 25, 10, 0, tzinfo=UTC)
        derived = derive_autonomy_envelope_v2(
            stable_observation=stable,
            delegation=resolved,
            policy=_policy(),
            request=_request(),
            issued_at=issued,
            gates_passed=True,
            nonce_factory=lambda: "12" * 16,
        )
        changed = copy.deepcopy(stable.document.value)
        changed["filesystem"]["regular_file_manifest_sha256"] = "f" * 64
        with tempfile.TemporaryDirectory() as parent:
            target = Path(parent) / "target"
            target.mkdir()
            store = RuntimeStateStore(Path(parent) / "runtime", target)
            session = store.start_session(
                stable.document.value["repository"],
                "operator",
                started_at="2026-08-25T10:00:00Z",
            )
            with self.assertRaisesRegex(Exception, "AEXOBS010"):
                admit_fresh_envelope(
                    envelope=derived.envelope,
                    fresh_observation=validate_contract(changed),
                    current_delegation_sha256=resolved.document.sha256,
                    now=datetime(2026, 8, 25, 10, 0, 1, tzinfo=UTC),
                    runtime_store=store,
                    session=session,
                    gates_passed=True,
                )
            with self.assertRaisesRegex(DelegatedAuthorityError, "AEXAUTH012"):
                admit_fresh_envelope(
                    envelope=derived.envelope,
                    fresh_observation=stable.document,
                    current_delegation_sha256=resolved.document.sha256,
                    now=datetime(2026, 8, 25, 10, 5, tzinfo=UTC),
                    runtime_store=store,
                    session=session,
                    gates_passed=True,
                )
            store.close_session(session)

        after_value = copy.deepcopy(stable.document.value)
        after_value["previous_receipt_sha256"] = "d" * 64
        fresh_after = validate_contract(after_value)
        receipt = phase2_receipt(derived.envelope.sha256, stable.document.sha256)
        receipt["effects"]["state_after"][0]["sha256"] = fresh_after.sha256
        expectations = ReceiptExpectations(
            profiles=("implementer",),
            skill_names=("harness-orient",),
            operation_ids=("read-contract",),
            worker_ids=("worker-1",),
            changed_paths=("docs/evidence.json",),
            evidence=(("verification", "docs/evidence.json", "7" * 64),),
            state_before=(("repository-state", stable.document.sha256),),
            state_after=(("repository-state", fresh_after.sha256),),
            autonomy_envelope_sha256=derived.envelope.sha256,
            evaluator_payload_sha256="9" * 64,
        )
        verified = verify_receipt_state_chain(
            receipt=receipt,
            expectations=expectations,
            admitted_repository_state=stable.document.sha256,
            fresh_after=fresh_after,
        )
        self.assertRegex(verified.sha256, r"^[0-9a-f]{64}$")
        with self.assertRaisesRegex(DelegatedAuthorityError, "AEXAUTH014"):
            verify_receipt_state_chain(
                receipt=receipt,
                expectations=expectations,
                admitted_repository_state="0" * 64,
                fresh_after=fresh_after,
            )


if __name__ == "__main__":
    unittest.main()
