from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from se_harness.agent_contract import (
    AUTONOMY_ENVELOPE_SCHEMA,
    AUTONOMY_ENVELOPE_V2_SCHEMA,
    DELEGATION_SCHEMA,
    PACKET_V1_SCHEMA,
    PROFILE_SCHEMA,
    RECEIPT_SCHEMA,
    REPOSITORY_OBSERVATION_SCHEMA,
    AgentContractError,
    ReceiptExpectations,
    assess_admission,
    canonical_json_bytes,
    construct_envelope_candidate,
    construct_repository_state_binding,
    narrow_autonomy_envelope,
    parse_agent_contract_catalog_bytes,
    parse_contract_bytes,
    project_decision_packet,
    render_decision_packet,
    validate_contract,
    validate_execution_receipt,
    validate_logical_execution_profile,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CATALOG = REPOSITORY_ROOT / "se_harness/agent_contract.json"
VECTORS = REPOSITORY_ROOT / "tests/fixtures/agentic_execution/contracts/canonical-vectors.json"
PHASE1_VECTORS = REPOSITORY_ROOT / "tests/fixtures/agentic_execution/canonical_vectors.json"
PHASE4_VECTORS = (
    REPOSITORY_ROOT
    / "tests/fixtures/agentic_execution/phase4/authority/canonical-vectors.json"
)


def load_vectors() -> dict[str, object]:
    return json.loads(VECTORS.read_text(encoding="utf-8"))


def decision_source() -> tuple[dict[str, object], dict[str, object]]:
    source = {
        "schema": "se-harness-workflow-result-v2",
        "operation": {"kind": "focus", "outcome": "completed"},
        "selection": {"primary": "WO-TST-001", "artifacts": ["WO-TST-001"]},
        "scope": {
            "mode": "selected",
            "governing": ["REQ-TST-001"],
            "dependencies": [],
            "declared_paths": ["docs/"],
            "changed_paths": [],
            "change_set_complete": False,
        },
        "compliance": {
            "checkpoint": "pre-action",
            "workflow_rule_id": "WFL-TST-DECIDE",
            "procedure_id": "PROC-TST-001",
            "status": "pass",
            "gates": [
                {
                    "id": "QG-TST-001",
                    "status": "pass",
                    "predicates": [
                        {
                            "id": "evidence-present",
                            "status": "pass",
                            "evidence": [{"kind": "artifact", "reference": "REQ-TST-001"}],
                            "message": "Required evidence is present.",
                        }
                    ],
                }
            ],
        },
        "procedure": {
            "id": "PROC-TST-001",
            "current_step": "STEP-TST-DECIDE",
            "steps": [
                {
                    "id": "STEP-TST-DECIDE",
                    "kind": "decision",
                    "gate_ids": ["QG-TST-001"],
                    "effects": ["The work order may become implemented."],
                    "non_effects": ["The decision does not verify or release the work."],
                    "decision_right": "DR-WO-COMPLETE",
                    "role": "engineering-owner",
                    "artifact": "WO-TST-001",
                    "decision": "whether implementation evidence is complete",
                    "outcomes": ["implemented", "continue", "reject"],
                    "response": "Mark WO-TST-001 implemented.",
                }
            ],
        },
        "state": {
            "before": [{"id": "WO-TST-001", "status": "in_progress"}],
            "after": [{"id": "WO-TST-001", "status": "in_progress"}],
        },
        "findings": {"scoped_blockers": [], "repository_blockers": [], "unrelated_count": 0},
        "mutation": {"writes": []},
        "restitution": {
            "outcome": "completed",
            "done": ["Implementation evidence was evaluated."],
            "not_done": [],
            "blocked_by": [],
            "current_lifecycle_state": ["WO-TST-001 is in_progress."],
            "decision_required": {
                "decision_right": "DR-WO-COMPLETE",
                "role": "engineering-owner",
                "artifact": "WO-TST-001",
                "decision": "whether implementation evidence is complete",
                "outcomes": ["implemented", "continue", "reject"],
            },
            "next": {
                "procedure_id": "PROC-TST-001",
                "step_id": "STEP-TST-DECIDE",
                "action": "Decide whether the implementation is complete",
            },
            "command_or_response": {"kind": "response", "value": "Mark WO-TST-001 implemented."},
            "alternatives": [],
        },
    }
    context = {
        "schema": "se-harness-decision-packet-context-v1",
        "repository": "fixture-repository",
        "candidate_commit": "1" * 40,
        "evaluator_payload_sha256": "2" * 64,
        "evidence": [{"kind": "verification", "path": "docs/evidence.json", "sha256": "3" * 64}],
        "assumptions": ["The supplied repository identity is current."],
        "residual_uncertainty": ["Real-world actor identity is not authenticated."],
        "preview": {
            "kind": "none",
            "artifact": None,
            "from_status": None,
            "to_status": None,
            "action": None,
            "target": None,
        },
        "alternatives": [],
        "safe_to_defer": True,
    }
    return source, context


def phase2_receipt(envelope_sha256: str, state_before: str) -> dict[str, object]:
    return {
        "schema": RECEIPT_SCHEMA,
        "selection": {
            "repository": "fixture-repository",
            "artifact": "WO-TST-001",
            "autonomy_envelope_sha256": envelope_sha256,
        },
        "execution": {
            "profiles": ["implementer"],
            "skills": [
                {"name": "harness-orient", "version": "1.0.0", "portable_core_sha256": "4" * 64}
            ],
            "operations": [
                {
                    "id": "read-contract",
                    "status": "passed",
                    "exit_code": 0,
                    "arguments_sha256": "5" * 64,
                    "output_sha256": "6" * 64,
                    "evidence_path": "docs/evidence.json",
                }
            ],
            "worker_results": [
                {
                    "id": "worker-1",
                    "profile": "implementer",
                    "status": "completed",
                    "operation_ids": ["read-contract"],
                    "changed_paths": ["docs/evidence.json"],
                    "evidence": [
                        {"kind": "verification", "path": "docs/evidence.json", "sha256": "7" * 64}
                    ],
                }
            ],
        },
        "effects": {
            "changed_paths": ["docs/evidence.json"],
            "evidence": [{"kind": "verification", "path": "docs/evidence.json", "sha256": "7" * 64}],
            "state_before": [{"kind": "repository-state", "sha256": state_before}],
            "state_after": [{"kind": "repository-state", "sha256": "8" * 64}],
        },
        "validation": {
            "evaluator": {"identity": "fixture evaluator", "version": "0.6.0", "payload_sha256": "9" * 64},
            "gates": [],
            "outcome": "completed",
            "deviations": [],
            "residual_uncertainty": ["Receipt evidence cannot authenticate a real-world actor."],
        },
    }


class CatalogAndParsingTests(unittest.TestCase):
    def test_catalog_is_canonical_closed_and_reference_complete(self) -> None:
        raw = CATALOG.read_bytes()
        catalog = parse_agent_contract_catalog_bytes(raw)

        self.assertEqual(raw, catalog.canonical_bytes)
        self.assertRegex(catalog.sha256, r"^[0-9a-f]{64}$")
        self.assertEqual(11, len(catalog.value["schemas"]))
        self.assertEqual([f"AEXCON{index:03d}" for index in range(1, 19)], [item["code"] for item in catalog.value["diagnostics"]])
        definitions = catalog.value["definitions"]
        names = {item["name"] for item in definitions}
        references = {item["root"] for item in catalog.value["schemas"]}
        for definition in definitions:
            references.update(field["type"] for field in definition["fields"])
            references.update(definition["variants"])
            references.update(
                item
                for item in (definition["element"], definition["key_type"], definition["value_type"])
                if item is not None
            )
        self.assertEqual(set(), references - names)
        self.assertEqual(set(), names - references)

        pretty = json.dumps(catalog.value, indent=2).encode("utf-8")
        with self.assertRaisesRegex(AgentContractError, "AEXCON009"):
            parse_agent_contract_catalog_bytes(pretty)

        tampered = copy.deepcopy(catalog.value)
        next(item for item in tampered["definitions"] if item["name"] == "boolean")["maximum"] = 1
        tampered_bytes = canonical_json_bytes(tampered)
        with self.assertRaisesRegex(AgentContractError, "AEXCON009"):
            parse_agent_contract_catalog_bytes(tampered_bytes)

    def test_parser_rejects_duplicate_unknown_float_bom_utf8_and_size(self) -> None:
        envelope = load_vectors()["autonomy_envelope"]["value"]
        raw = json.dumps(envelope, separators=(",", ":")).encode("utf-8")
        duplicate = raw.replace(b'{"schema":', b'{"schema":"se-harness-autonomy-envelope-v1","schema":', 1)
        cases = (
            (duplicate, "AEXCON003"),
            (b'{"schema":"unknown-v1"}', "AEXCON004"),
            (b'{"schema":1.5}', "AEXCON006"),
            (b"\xef\xbb\xbf{}", "AEXCON001"),
            (b"\xff", "AEXCON001"),
            (b" " * 1_048_577, "AEXCON002"),
        )
        for value, code in cases:
            with self.subTest(code=code):
                with self.assertRaisesRegex(AgentContractError, code):
                    parse_contract_bytes(value)

        unknown = copy.deepcopy(envelope)
        unknown["authority"] = "invented"
        with self.assertRaisesRegex(AgentContractError, "AEXCON005"):
            validate_contract(unknown)

    def test_phase4_contract_vectors_are_canonical_and_v1_remains_distinct(self) -> None:
        vectors = json.loads(PHASE4_VECTORS.read_text(encoding="utf-8"))
        expected = {
            "delegation": DELEGATION_SCHEMA,
            "repository_observation": REPOSITORY_OBSERVATION_SCHEMA,
            "autonomy_envelope_v2": AUTONOMY_ENVELOPE_V2_SCHEMA,
        }
        for name, schema in expected.items():
            with self.subTest(name=name):
                vector = vectors[name]
                document = validate_contract(vector["value"], expected_schema=schema)
                self.assertEqual(vector["canonical"].encode("utf-8"), document.canonical_bytes)
                self.assertEqual(vector["sha256"], document.sha256)
        with self.assertRaisesRegex(AgentContractError, "AEXCON004"):
            validate_contract(
                vectors["autonomy_envelope_v2"]["value"],
                expected_schema=AUTONOMY_ENVELOPE_SCHEMA,
            )
        invalid_time = copy.deepcopy(vectors["delegation"]["value"])
        invalid_time["valid_until"] = "2030-13-01T00:00:00Z"
        with self.assertRaisesRegex(AgentContractError, "AEXCON007"):
            validate_contract(invalid_time)
        excessive = copy.deepcopy(vectors["autonomy_envelope_v2"]["value"])
        excessive["authority"]["not_after"] = "2026-01-01T00:05:01Z"
        with self.assertRaisesRegex(AgentContractError, "AEXCON007"):
            validate_contract(excessive)

    def test_portable_paths_fail_closed(self) -> None:
        envelope = load_vectors()["autonomy_envelope"]["value"]
        invalid = (
            "/absolute.txt",
            "../escape.txt",
            "a/./b",
            "a//b",
            "a\\b",
            "C:/drive.txt",
            "https://example.invalid/x",
            "wild*.txt",
            "NUL.txt",
            "trailing-dot./x",
        )
        for candidate in invalid:
            with self.subTest(candidate=candidate):
                value = copy.deepcopy(envelope)
                value["delegation"]["path_scope"] = [candidate]
                value["evidence"]["required_paths"] = []
                with self.assertRaisesRegex(AgentContractError, "AEXCON008"):
                    validate_contract(value)


class RepositoryAndEnvelopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.vectors = load_vectors()

    def test_independent_worktree_binding_envelope_and_profile_vectors(self) -> None:
        for name in ("worktree", "repository_state_binding", "autonomy_envelope", "logical_profile"):
            with self.subTest(name=name):
                vector = self.vectors[name]
                document = validate_contract(vector["value"])
                self.assertEqual(vector["canonical"].encode("utf-8"), document.canonical_bytes)
                self.assertEqual(vector["sha256"], document.sha256)

        worktree = copy.deepcopy(self.vectors["worktree"]["value"])
        worktree["entries"].reverse()
        binding = construct_repository_state_binding(
            worktree,
            self.vectors["repository_state_binding"]["value"]["governance"],
        )
        self.assertEqual(self.vectors["repository_state_binding"]["sha256"], binding.sha256)

        envelope = copy.deepcopy(self.vectors["autonomy_envelope"]["value"])
        for name in ("operations", "path_scope", "execution_profiles", "stop_before"):
            envelope["delegation"][name].reverse()
        envelope["delegation"]["retry_limits"] = dict(
            reversed(list(envelope["delegation"]["retry_limits"].items()))
        )
        self.assertEqual(self.vectors["autonomy_envelope"]["sha256"], validate_contract(envelope).sha256)

    def test_worktree_rejects_invalid_combinations_and_case_collisions(self) -> None:
        value = copy.deepcopy(self.vectors["worktree"]["value"])
        value["entries"][0]["worktree_sha256"] = "0" * 64
        with self.assertRaisesRegex(AgentContractError, "AEXCON007"):
            validate_contract(value)

        value = copy.deepcopy(self.vectors["worktree"]["value"])
        collision = copy.deepcopy(value["entries"][1])
        collision["path"] = "SCRIPT.SH"
        value["entries"].append(collision)
        with self.assertRaisesRegex(AgentContractError, "AEXCON008"):
            validate_contract(value)

    def test_worktree_uses_observation_bound_without_relaxing_ordinary_arrays(self) -> None:
        value = {
            "schema": "se-harness-worktree-state-v1",
            "git_object_format": "sha1",
            "head": "1" * 40,
            "tree": "2" * 40,
            "entries": [
                {
                    "path": f"files/{index:04d}.txt",
                    "index_mode": None,
                    "index_object_id": None,
                    "worktree_kind": "regular",
                    "worktree_mode": "100644",
                    "worktree_sha256": hashlib.sha256(str(index).encode("ascii")).hexdigest(),
                    "worktree_object_id": None,
                }
                for index in range(1_025)
            ],
        }
        self.assertEqual(1_025, len(validate_contract(value).value["entries"]))
        with self.assertRaisesRegex(AgentContractError, "AEXCON002"):
            canonical_json_bytes(list(range(1_025)))

    def test_constructor_intersects_scope_and_parent_narrowing_is_monotonic(self) -> None:
        binding = self.vectors["repository_state_binding"]["value"]
        maximum = self.vectors["autonomy_envelope"]["value"]
        request = {
            "delegation": {
                "asserted_by": "engineering-owner",
                "operations": ["external-action", "read-contract"],
                "path_scope": ["docs/", "other/"],
                "execution_profiles": ["implementer", "unplanned"],
                "max_parallel_writers": 2,
                "retry_limits": {"external-action": 3, "read-contract": 2},
                "stop_before": ["accountable-decision-required", "action-time-authorization-required"],
            },
            "evidence": {"required_receipt": True, "required_paths": ["docs/evidence.json"]},
        }
        managed = {"delegation": maximum["delegation"], "evidence": maximum["evidence"]}
        constructed = construct_envelope_candidate(
            state_binding=binding,
            evaluator_payload_sha256="9" * 64,
            procedure_id="PROC-TST-001",
            request=request,
            managed_scope=managed,
            parent=maximum,
            parent_sha256=self.vectors["autonomy_envelope"]["sha256"],
        )

        self.assertEqual("constructed", constructed.outcome)
        self.assertEqual(["read-contract"], constructed.envelope.value["delegation"]["operations"])
        self.assertEqual(["docs/"], constructed.envelope.value["delegation"]["path_scope"])
        self.assertEqual(["implementer"], constructed.envelope.value["delegation"]["execution_profiles"])
        self.assertEqual(1, constructed.envelope.value["delegation"]["max_parallel_writers"])
        self.assertEqual({"read-contract": 0}, constructed.envelope.value["delegation"]["retry_limits"])
        self.assertEqual(
            {"operations", "path_scope", "execution_profiles", "max_parallel_writers", "retry_limits"},
            set(constructed.narrowing),
        )
        self.assertNotIn("derived", constructed.outcome)
        self.assertEqual("WO-TST-001", constructed.selected_work_order)
        self.assertEqual("PROC-TST-001", constructed.procedure_id)
        self.assertEqual("d" * 64, constructed.formal_snapshot_sha256)

        base = constructed.envelope.value
        cases = []

        wider = copy.deepcopy(base)
        wider["delegation"]["operations"].append("write-evidence")
        wider["delegation"]["retry_limits"]["write-evidence"] = 1
        cases.append(("operation", wider, "AEXCON010"))

        wider = copy.deepcopy(base)
        wider["delegation"]["path_scope"] = ["docs/", "outside.txt"]
        cases.append(("path", wider, "AEXCON010"))

        wider = copy.deepcopy(base)
        wider["delegation"]["execution_profiles"].append("reader")
        cases.append(("profile", wider, "AEXCON010"))

        wider = copy.deepcopy(base)
        wider["delegation"]["max_parallel_writers"] = 2
        cases.append(("writer", wider, "AEXCON010"))

        wider = copy.deepcopy(base)
        wider["delegation"]["retry_limits"]["read-contract"] = 1
        cases.append(("retry", wider, "AEXCON010"))

        wider = copy.deepcopy(base)
        wider["evidence"]["required_paths"] = []
        cases.append(("evidence", wider, "AEXCON010"))

        wider = copy.deepcopy(base)
        wider["selection"]["repository_state"] = "0" * 64
        cases.append(("identity", wider, "AEXCON011"))

        wider = copy.deepcopy(base)
        wider["delegation"]["asserted_by"] = "different-actor"
        cases.append(("actor", wider, "AEXCON012"))

        for label, value, code in cases:
            with self.subTest(label=label):
                with self.assertRaisesRegex(AgentContractError, code):
                    narrow_autonomy_envelope(base, value)

    def test_admission_denial_and_staleness_do_not_reach_effect_sentinel(self) -> None:
        envelope = self.vectors["autonomy_envelope"]["value"]
        envelope_sha = self.vectors["autonomy_envelope"]["sha256"]
        state_sha = self.vectors["repository_state_binding"]["sha256"]
        calls: list[str] = []

        def caller_side_effect(result: object) -> None:
            if result.outcome == "admissible":
                calls.append("effect")

        admissible = assess_admission(
            envelope,
            envelope_sha256=envelope_sha,
            expected_current_repository_state=state_sha,
            operation="read-contract",
            target_paths=["docs/input.json"],
            execution_profile="implementer",
            requested_writers=0,
            retry_ordinal=0,
            evidence_paths=["docs/evidence.json"],
            stop_boundary="routine-read-only",
        )
        self.assertEqual("admissible", admissible.outcome)
        self.assertIn("not admitted", " ".join(admissible.non_effects).lower())

        baseline = {
            "operation": "read-contract",
            "target_paths": ["docs/input.json"],
            "execution_profile": "implementer",
            "requested_writers": 0,
            "retry_ordinal": 0,
            "evidence_paths": ["docs/evidence.json"],
            "stop_boundary": "routine-read-only",
        }
        denial_cases = {
            "operation": {"operation": "unplanned-operation"},
            "path": {"target_paths": ["outside.txt"]},
            "profile": {"execution_profile": "unplanned"},
            "writers": {"requested_writers": 2},
            "retry": {"retry_ordinal": 1},
            "evidence": {"evidence_paths": []},
            "stop": {"stop_boundary": "accountable-decision-required"},
        }
        denied_results = []
        for label, changes in denial_cases.items():
            with self.subTest(label=label):
                arguments = {**baseline, **changes}
                denied = assess_admission(
                    envelope,
                    envelope_sha256=envelope_sha,
                    expected_current_repository_state=state_sha,
                    **arguments,
                )
                self.assertEqual("denied", denied.outcome)
                denied_results.append(denied)
        stale = assess_admission(
            envelope,
            envelope_sha256="0" * 64,
            expected_current_repository_state=state_sha,
            operation="read-contract",
            target_paths=["docs/input.json"],
            execution_profile="implementer",
            requested_writers=0,
            retry_ordinal=0,
            evidence_paths=["docs/evidence.json"],
            stop_boundary="routine-read-only",
        )
        for denied in denied_results:
            caller_side_effect(denied)
        caller_side_effect(stale)
        self.assertEqual("stale", stale.outcome)
        self.assertEqual("AEXCON012", denied_results[-1].diagnostics[0]["code"])
        self.assertEqual([], calls)


class PacketReceiptAndProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.vectors = load_vectors()

    def test_decision_packet_projection_is_lossless_and_render_order_is_fixed(self) -> None:
        source, context = decision_source()
        packet = project_decision_packet(source, context)

        self.assertEqual("se-harness-decision-packet-v2", packet.value["schema"])
        self.assertEqual("WO-TST-001", packet.value["context"]["selected_artifact"])
        self.assertEqual("in_progress", packet.value["context"]["lifecycle_state"])
        self.assertEqual(source["compliance"]["gates"], packet.value["assessment"]["gates"])
        self.assertEqual(context["evidence"], packet.value["assessment"]["evidence"])
        self.assertEqual(source["procedure"]["steps"][0]["effects"], packet.value["effect"]["effects"])
        self.assertEqual(source["restitution"]["command_or_response"], packet.value["handoff"]["command_or_suggested_response"])

        rendered = render_decision_packet(packet.value)
        headings = [section.splitlines()[0] for section in rendered.strip().split("\n\n")]
        self.assertEqual(
            [
                "Decision", "Subject", "Accountable role", "Current lifecycle state", "Scope",
                "Procedure", "Recommendation", "Alternatives", "Identity", "Gates", "Evidence",
                "Findings", "Assumptions", "Residual uncertainty", "Preview", "Effects",
                "Non-effects", "Safe to defer", "Command or response",
            ],
            headings,
        )

        v1 = copy.deepcopy(packet.value)
        v1["schema"] = PACKET_V1_SCHEMA
        del v1["context"]
        v1["effect"]["preview"] = {}
        self.assertEqual(PACKET_V1_SCHEMA, validate_contract(v1).value["schema"])

    def test_projection_rejects_missing_decision_state_drift_and_incomplete_context(self) -> None:
        source, context = decision_source()
        source["restitution"]["decision_required"] = None
        with self.assertRaisesRegex(AgentContractError, "AEXCON014"):
            project_decision_packet(source, context)

        source, context = decision_source()
        source["state"]["after"][0]["status"] = "implemented"
        with self.assertRaisesRegex(AgentContractError, "AEXCON014"):
            project_decision_packet(source, context)

        source, context = decision_source()
        context["alternatives"] = [
            {
                "summary": "An alternative absent from the workflow result.",
                "procedure_id": "PROC-TST-ALT",
                "decision_right": "DR-WO-COMPLETE",
                "subject": "WO-TST-001",
                "required_accountable_role": "engineering-owner",
                "recommendation": "Continue implementation",
                "command_or_suggested_response": {"kind": "response", "value": "Continue."},
                "effects": [],
                "non_effects": [],
            }
        ]
        with self.assertRaisesRegex(AgentContractError, "AEXCON014"):
            project_decision_packet(source, context)

    def test_receipt_requires_exact_independent_plan_coverage_and_rejects_authority(self) -> None:
        envelope_sha = self.vectors["autonomy_envelope"]["sha256"]
        state_before = self.vectors["repository_state_binding"]["sha256"]
        receipt = phase2_receipt(envelope_sha, state_before)
        expectations = ReceiptExpectations(
            profiles=("implementer",),
            skill_names=("harness-orient",),
            operation_ids=("read-contract",),
            worker_ids=("worker-1",),
            changed_paths=("docs/evidence.json",),
            evidence=(("verification", "docs/evidence.json", "7" * 64),),
            state_before=(("repository-state", state_before),),
            state_after=(("repository-state", "8" * 64),),
            autonomy_envelope_sha256=envelope_sha,
            evaluator_payload_sha256="9" * 64,
        )
        document = validate_execution_receipt(receipt, expectations)
        self.assertEqual(RECEIPT_SCHEMA, document.value["schema"])

        incomplete = copy.deepcopy(expectations)
        object.__setattr__(incomplete, "worker_ids", ("worker-1", "worker-2"))
        with self.assertRaisesRegex(AgentContractError, "AEXCON015"):
            validate_execution_receipt(receipt, incomplete)

        authority = copy.deepcopy(receipt)
        authority["authority"] = {"accountable_role": "engineering-owner"}
        with self.assertRaisesRegex(AgentContractError, "AEXCON016"):
            validate_execution_receipt(authority)

        hidden_failure = copy.deepcopy(receipt)
        hidden_failure["execution"]["operations"][0]["status"] = "failed"
        with self.assertRaisesRegex(AgentContractError, "AEXCON015"):
            validate_execution_receipt(hidden_failure)

    def test_phase1_receipt_bytes_and_portable_core_identity_remain_compatible(self) -> None:
        vectors = json.loads(PHASE1_VECTORS.read_text(encoding="utf-8"))
        receipt = vectors["receipt"]
        document = validate_execution_receipt(receipt["value"])
        self.assertEqual(receipt["canonical"].encode("utf-8"), document.canonical_bytes)
        self.assertEqual(receipt["sha256"], document.sha256)

        from se_harness.skill_contract import build_skill_manifest

        skill_root = REPOSITORY_ROOT / "templates/repository/standard/.agents/skills/harness-orient"
        manifest = build_skill_manifest(skill_root)
        self.assertEqual(vectors["portable_core"]["manifest_sha256"], manifest.sha256)

    def test_logical_profiles_are_non_authoritative_provider_neutral_and_fallback_safe(self) -> None:
        profile = self.vectors["logical_profile"]["value"]
        document = validate_logical_execution_profile(profile, accountable_roles={"assurance-owner"})
        self.assertEqual(PROFILE_SCHEMA, document.value["schema"])
        self.assertTrue(document.value["single_agent_fallback"])

        with self.assertRaisesRegex(AgentContractError, "AEXCON017"):
            validate_logical_execution_profile(profile, accountable_roles={"implementer"})

        provider_bound = copy.deepcopy(profile)
        provider_bound["runtime_characteristics"] = ["codex-workspace"]
        with self.assertRaisesRegex(AgentContractError, "AEXCON017"):
            validate_logical_execution_profile(provider_bound)

        missing_stop = copy.deepcopy(profile)
        missing_stop["prohibited_decisions"] = ["accountable-decision-required"]
        with self.assertRaisesRegex(AgentContractError, "AEXCON017"):
            validate_logical_execution_profile(missing_stop)


if __name__ == "__main__":
    unittest.main()
