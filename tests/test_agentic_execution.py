from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from pathlib import PurePosixPath

from se_harness.skill_contract import (
    _validate_component,
    CONTRACT_SCHEMA,
    CONTRACT_SCHEMA_V2,
    CONTRACT_SCHEMA_V3,
    MANIFEST_SCHEMA,
    SkillContractError,
    build_skill_manifest,
    canonical_json_bytes,
    load_skill_contract,
    parse_skill_contract_bytes,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPOSITORY_ROOT / "templates/repository/standard/.agents/skills/harness-orient"
SKILLS_ROOT = REPOSITORY_ROOT / "templates/repository/standard/.agents/skills"
PHASE3_ROOTS = {
    name: SKILLS_ROOT / name
    for name in (
        "harness-draft-change",
        "harness-execute-work-order",
        "harness-prepare-assurance",
    )
}
OPERATOR_BRIEF_ROOT = SKILLS_ROOT / "harness-operator-brief"
OPERATOR_BRIEF = OPERATOR_BRIEF_ROOT / "scripts/check_brief.py"
TECHNICAL_COMMUNICATION_CORPUS = REPOSITORY_ROOT / "tests/fixtures/technical_communication/review_corpus.json"
ORIENT = SKILL_ROOT / "scripts/orient.py"
FAKE_EVALUATOR = REPOSITORY_ROOT / "tests/fixtures/agentic_execution/fake_evaluator.py"
VECTORS = REPOSITORY_ROOT / "tests/fixtures/agentic_execution/canonical_vectors.json"
PHASE3_VECTORS = REPOSITORY_ROOT / "tests/fixtures/agentic_execution/phase3/portable_vectors.json"
PHASE4_SKILL_VECTORS = REPOSITORY_ROOT / "tests/fixtures/agentic_execution/phase4/skills/portable-vectors.json"
PHASE4_SKILL_CASES = REPOSITORY_ROOT / "tests/fixtures/agentic_execution/phase4/skills/client-cases.json"
HOST_SURFACE_VECTORS = REPOSITORY_ROOT / "tests/fixtures/agentic_execution/host_activation/expected_surfaces.json"
CLAUDE_SKILLS_ROOT = REPOSITORY_ROOT / "templates/repository/standard/.claude/skills"
ALL_SKILL_NAMES = {"harness-orient", *PHASE3_ROOTS}


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file()
    }


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    prior = sys.dont_write_bytecode
    prior_module = sys.modules.get(name)
    sys.modules[name] = module
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = prior
        if prior_module is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = prior_module
    return module


class Phase4DelegationTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_script(
            "_phase4_candidate_validator",
            REPOSITORY_ROOT
            / "templates/repository/standard/scripts/validate_engineering_artifacts.py",
        )

    def artifact(self, table: dict[str, object]):
        return self.validator.Artifact(
            path=REPOSITORY_ROOT / "docs/engineering/work-orders/WO-TST-002.md",
            metadata={
                "id": "WO-TST-002",
                "type": "work_order",
                "status": "approved",
                "execution_scope": {"paths": ["docs/", "se_harness/runtime.py"]},
                "agentic_delegation": table,
            },
            body="# Fixture\n",
        )

    @staticmethod
    def declaration() -> dict[str, object]:
        return {
            "schema": "se-harness-agentic-delegation-v1",
            "delegated_by": "engineering-owner",
            "delegate": "implementation-worker",
            "decision_rights": ["DR-WO-START"],
            "operations": ["change-bundle-apply"],
            "execution_profiles": ["implementer"],
            "paths": ["docs/"],
            "required_evidence": [
                {"kind": "verification", "path": "docs/evidence.json"}
            ],
            "valid_until": "2030-01-01T00:00:00Z",
            "max_retry": 1,
            "max_parallel_writers": 1,
            "child_delegation": False,
            "stop_before": [
                "accountable-decision-required",
                "action-time-authorization-required",
            ],
        }

    def test_candidate_template_and_validator_accept_exact_optional_delegation(self) -> None:
        template = (
            REPOSITORY_ROOT
            / "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md"
        ).read_text(encoding="utf-8")
        self.assertIn('[agentic_delegation]', template)
        self.assertIn('schema = "se-harness-agentic-delegation-v1"', template)
        self.assertIn('child_delegation = false', template)
        errors = self.validator.validate_agentic_delegations(
            [self.artifact(self.declaration())], REPOSITORY_ROOT
        )
        self.assertEqual([], errors)

    def test_candidate_validator_rejects_unknown_fields_widening_and_stop_removal(self) -> None:
        cases = {}
        value = self.declaration()
        value["invented"] = True
        cases["unknown"] = value
        value = self.declaration()
        value["paths"] = ["outside/"]
        cases["path"] = value
        value = self.declaration()
        value["stop_before"] = ["accountable-decision-required"]
        cases["stop"] = value
        value = self.declaration()
        value["required_evidence"] = [{"kind": "verification", "path": "outside.json"}]
        cases["evidence"] = value
        value = self.declaration()
        value["max_parallel_writers"] = 2
        cases["writers"] = value
        value = self.declaration()
        value["child_delegation"] = True
        cases["child"] = value
        for label, table in cases.items():
            with self.subTest(label=label):
                errors = self.validator.validate_agentic_delegations(
                    [self.artifact(table)], REPOSITORY_ROOT
                )
                self.assertTrue(errors)
                self.assertEqual({"E021"}, {item.code for item in errors})


class SkillContractTests(unittest.TestCase):
    def test_canonical_harness_orient_contract_and_manifest_validate(self) -> None:
        contract = load_skill_contract(SKILL_ROOT / "skill-contract.json")
        manifest = build_skill_manifest(SKILL_ROOT)
        vectors = json.loads(VECTORS.read_text(encoding="utf-8"))

        self.assertEqual(CONTRACT_SCHEMA, contract.value["schema"])
        self.assertEqual("harness-orient", contract.name)
        self.assertEqual("read-only", contract.value["mutation_class"])
        self.assertFalse(contract.value["delegation"]["allowed"])
        self.assertFalse(contract.value["evidence"]["target_retention"])
        self.assertEqual(MANIFEST_SCHEMA, manifest.value["schema"])
        self.assertEqual(
            ["SKILL.md", "scripts/orient.py", "skill-contract.json"],
            [item["path"] for item in manifest.value["files"]],
        )
        self.assertRegex(manifest.sha256, r"^[0-9a-f]{64}$")
        self.assertEqual(vectors["portable_core"]["files"], manifest.value["files"])
        self.assertEqual(vectors["portable_core"]["manifest_sha256"], manifest.sha256)

    def test_contract_rejects_duplicate_and_unknown_fields(self) -> None:
        raw = (SKILL_ROOT / "skill-contract.json").read_bytes()
        duplicate = raw.replace(b'{\n  "schema":', b'{\n  "schema": "se-harness-skill-contract-v1",\n  "schema":', 1)
        with self.assertRaisesRegex(SkillContractError, "SKC002"):
            parse_skill_contract_bytes(duplicate)

        value = json.loads(raw)
        value["authority"] = "invented"
        with self.assertRaisesRegex(SkillContractError, "SKC006"):
            parse_skill_contract_bytes(json.dumps(value).encode("utf-8"))

    def test_contract_rejects_authority_delegation_and_target_retention(self) -> None:
        original = json.loads((SKILL_ROOT / "skill-contract.json").read_text(encoding="utf-8"))
        cases = (
            ("mutation", lambda value: value.__setitem__("mutation_class", "write"), "SKC013"),
            ("delegation", lambda value: value["delegation"].__setitem__("allowed", True), "SKC018"),
            ("retention", lambda value: value["evidence"].__setitem__("target_retention", True), "SKC019"),
        )
        for label, mutate, code in cases:
            with self.subTest(label=label):
                value = json.loads(json.dumps(original))
                mutate(value)
                with self.assertRaisesRegex(SkillContractError, code):
                    parse_skill_contract_bytes(json.dumps(value).encode("utf-8"))

    def test_closed_phase4_contracts_and_manifests_validate(self) -> None:
        expected = {
            "harness-draft-change": ("draft-writing", ["draft-create", "draft-revise", "planning-note-write"]),
            "harness-execute-work-order": (
                "governed-mutation",
                ["implementation-write", "test-execution", "evidence-write"],
            ),
            "harness-prepare-assurance": ("governed-mutation", ["verification-record-prepare"]),
        }
        for name, root in PHASE3_ROOTS.items():
            with self.subTest(skill=name):
                contract = load_skill_contract(root / "skill-contract.json")
                manifest = build_skill_manifest(root)
                self.assertEqual(CONTRACT_SCHEMA_V3, contract.value["schema"])
                self.assertEqual(name, contract.name)
                self.assertEqual(expected[name][0], contract.value["mutation_class"])
                self.assertEqual(expected[name][1], contract.value["effects"]["permitted"])
                self.assertEqual([], contract.value["effects"]["lifecycle_transitions"])
                self.assertFalse(contract.value["client"]["direct_target_writes"])
                self.assertEqual("evaluator", contract.value["client"]["bundle_owner"])
                self.assertEqual("evaluator", contract.value["client"]["target_writer"])
                self.assertEqual("required", contract.value["client"]["canonical_restitution"])
                self.assertEqual("se-harness-workflow-v4", contract.value["client"]["workflow_schema"])
                self.assertTrue(contract.value["activation"]["explicit"])
                self.assertFalse(contract.value["activation"]["implicit"])
                self.assertFalse(contract.value["delegation"]["allowed"])
                self.assertEqual("single-agent", contract.value["delegation"]["fallback"])
                self.assertEqual(
                    sorted(["SKILL.md", "agents/openai.yaml", next(item for item in [
                        "scripts/guard.py", "scripts/check_scope.py", "scripts/check_prepare.py"
                    ] if (root / item).exists()), "skill-contract.json"]),
                    sorted(item["path"] for item in manifest.value["files"]),
                )
                self.assertEqual("2.0.0", contract.value["version"])
                self.assertEqual(
                    b"policy:\n  allow_implicit_invocation: false\n",
                    (root / "agents/openai.yaml").read_bytes(),
                )

    def test_retained_phase3_vectors_are_preserved_and_orientation_is_byte_exact(self) -> None:
        phase3 = json.loads(PHASE3_VECTORS.read_text(encoding="utf-8"))
        phase4 = json.loads(PHASE4_SKILL_VECTORS.read_text(encoding="utf-8"))
        self.assertEqual("se-harness-phase3-portable-vectors-v1", phase3["schema"])
        self.assertEqual("se-harness-phase4-skill-vectors-v1", phase4["schema"])
        for name in PHASE3_ROOTS:
            with self.subTest(skill=name):
                self.assertEqual(phase3["skills"][name], phase4["skills"][name]["previous"])
        expected = phase4["orientation"]
        contract = load_skill_contract(SKILL_ROOT / "skill-contract.json")
        self.assertEqual(expected["schema"], contract.value["schema"])
        self.assertEqual(expected["manifest_sha256"], build_skill_manifest(SKILL_ROOT).sha256)
        self.assertEqual(
            expected["contract_sha256"],
            hashlib.sha256(canonical_json_bytes(contract.value)).hexdigest(),
        )

    def test_current_writing_cores_match_phase4_vectors(self) -> None:
        vectors = json.loads(PHASE4_SKILL_VECTORS.read_text(encoding="utf-8"))
        for name, identities in vectors["skills"].items():
            with self.subTest(skill=name):
                expected = identities["current"]
                root = SKILLS_ROOT / name
                contract = load_skill_contract(root / "skill-contract.json")
                self.assertEqual(expected["schema"], contract.value["schema"])
                self.assertEqual(expected["version"], contract.version)
                self.assertEqual(expected["manifest_sha256"], build_skill_manifest(root).sha256)
                self.assertEqual(
                    expected["contract_sha256"],
                    hashlib.sha256(canonical_json_bytes(contract.value)).hexdigest(),
                )
                self.assertEqual(expected["interface_operation"], contract.value["client"]["interface_operation"])
                self.assertEqual(expected["operation_catalog"], contract.value["client"]["operation_catalog"])

    def test_phase4_contracts_reject_implicit_activation_direct_write_and_authority(self) -> None:
        original = json.loads(
            (PHASE3_ROOTS["harness-draft-change"] / "skill-contract.json").read_text(encoding="utf-8")
        )
        cases = (
            ("implicit", lambda value: value["activation"].__setitem__("implicit", True), "SKC033"),
            (
                "transition",
                lambda value: value["effects"]["lifecycle_transitions"].append("draft-to-approved"),
                "SKC038",
            ),
            ("direct-write", lambda value: value["client"].__setitem__("direct_target_writes", True), "SKC036"),
            ("writer", lambda value: value["client"].__setitem__("target_writer", "provider"), "SKC036"),
            ("authority", lambda value: value.__setitem__("authority", "engineering-owner"), "SKC006"),
            ("delegation", lambda value: value["delegation"].__setitem__("allowed", True), "SKC018"),
        )
        for label, mutate, code in cases:
            with self.subTest(label=label):
                value = json.loads(json.dumps(original))
                mutate(value)
                with self.assertRaisesRegex(SkillContractError, code):
                    parse_skill_contract_bytes(json.dumps(value).encode("utf-8"))

    def test_closed_operator_brief_contract_and_three_file_core_validate(self) -> None:
        contract = load_skill_contract(OPERATOR_BRIEF_ROOT / "skill-contract.json")
        manifest = build_skill_manifest(OPERATOR_BRIEF_ROOT)
        self.assertEqual(CONTRACT_SCHEMA_V2, contract.value["schema"])
        self.assertEqual("harness-operator-brief", contract.name)
        self.assertEqual("1.0.0", contract.version)
        self.assertEqual("read-only", contract.value["mutation_class"])
        self.assertEqual(["inline-brief-render"], contract.value["effects"]["permitted"])
        self.assertEqual("none", contract.value["effects"]["path_source"])
        self.assertEqual([], contract.value["effects"]["lifecycle_transitions"])
        self.assertEqual(["version", "identity", "doctor"], contract.value["evaluator"]["required_operations"])
        self.assertEqual([], contract.value["evaluator"]["optional_operations"])
        self.assertEqual({"allowed": False, "fallback": "single-agent"}, contract.value["delegation"])
        self.assertFalse(contract.value["evidence"]["target_retention"])
        self.assertEqual([], contract.value["evidence"]["required_retained_kinds"])
        self.assertEqual(
            ["SKILL.md", "scripts/check_brief.py", "skill-contract.json"],
            sorted(item["path"] for item in manifest.value["files"]),
        )

    def test_operator_brief_contract_rejects_open_or_authoritative_variants(self) -> None:
        original = json.loads((OPERATOR_BRIEF_ROOT / "skill-contract.json").read_text(encoding="utf-8"))
        cases = (
            ("implicit", lambda value: value["activation"].__setitem__("implicit", True), "SKC023"),
            ("write", lambda value: value.__setitem__("mutation_class", "governed-mutation"), "SKC022"),
            (
                "transition",
                lambda value: value["effects"]["lifecycle_transitions"].append("approved-to-in-progress"),
                "SKC027",
            ),
            ("network", lambda value: value["effects"].__setitem__("prohibited", []), "SKC027"),
            ("retention", lambda value: value["evidence"].__setitem__("target_retention", True), "SKC028"),
            ("open-input", lambda value: value["inputs"].append(
                {"name": "arbitrary-operation", "required": False, "type": "bounded-text"}
            ), "SKC024"),
        )
        for label, mutate, code in cases:
            with self.subTest(label=label):
                value = json.loads(json.dumps(original))
                mutate(value)
                with self.assertRaisesRegex(SkillContractError, code):
                    parse_skill_contract_bytes(json.dumps(value).encode("utf-8"))

    def test_operator_brief_activation_declares_required_non_matches(self) -> None:
        contract = load_skill_contract(OPERATOR_BRIEF_ROOT / "skill-contract.json").value
        non_matches = " ".join(contract["activation"]["must_not_match"]).lower()
        for term in ("orient", "artifact", "work order", "assurance", "lifecycle", "git", "release", "network"):
            with self.subTest(term=term):
                self.assertIn(term, non_matches)
        self.assertTrue(contract["activation"]["explicit"])
        self.assertFalse(contract["activation"]["implicit"])
    def test_repository_host_surfaces_bind_one_canonical_core_per_name(self) -> None:
        vectors = json.loads(HOST_SURFACE_VECTORS.read_text(encoding="utf-8"))
        self.assertEqual("se-harness-host-surface-vectors-v2", vectors["schema"])
        self.assertEqual(ALL_SKILL_NAMES, set(vectors["skills"]))
        self.assertEqual(
            ALL_SKILL_NAMES,
            {path.name for path in CLAUDE_SKILLS_ROOT.iterdir() if path.is_dir()},
        )
        for name, expected in sorted(vectors["skills"].items()):
            with self.subTest(skill=name):
                adapter = CLAUDE_SKILLS_ROOT / name / "SKILL.md"
                self.assertEqual(["SKILL.md"], [path.name for path in adapter.parent.iterdir()])
                raw = adapter.read_text(encoding="utf-8")
                front, body = raw.removeprefix("---\n").split("\n---\n", 1)
                self.assertIn(f"name: {name}\n", front + "\n")
                self.assertIn("adapter-schema: se-harness-host-adapter-v1", front)
                self.assertIn(f"canonical-name: {name}", front)
                self.assertIn(f"canonical-path: {expected['canonical_path']}", front)
                self.assertEqual(
                    expected["claude_disable_model_invocation"] is True,
                    "disable-model-invocation: true" in front,
                )
                self.assertIn("non-authoritative Claude Code discovery adapter", body)
                self.assertIn(f"${{CLAUDE_PROJECT_DIR}}/{expected['canonical_path']}", body)
                self.assertIn("Read the complete canonical `SKILL.md`", body)
                self.assertIn("yield entirely to the canonical procedure", body)
                for forbidden in (
                    "allowed-tools:", "disallowed-tools:", "model:", "context:",
                    "agent:", "hooks:", "http://", "https://", "$(`", "scripts/",
                ):
                    self.assertNotIn(forbidden, raw)

                canonical = PurePosixPath(f".agents/skills/{name}")
                self.assertFalse(canonical.is_absolute())
                self.assertNotIn("..", canonical.parts)
                contract = load_skill_contract(SKILLS_ROOT / name / "skill-contract.json")
                self.assertEqual(name, contract.name)
                self.assertEqual(expected["contract_schema"], contract.value["schema"])
                self.assertEqual(expected["contract_version"], contract.version)
                self.assertEqual(
                    expected["interface_operation"],
                    contract.value.get("client", {}).get("interface_operation"),
                )
                policy = expected["codex_policy_path"]
                self.assertEqual(policy is not None, (SKILLS_ROOT / name / (policy or "agents/openai.yaml")).exists())

    def test_host_surfaces_fail_static_binding_checks_for_hostile_changes(self) -> None:
        source = (CLAUDE_SKILLS_ROOT / "harness-draft-change/SKILL.md").read_text(encoding="utf-8")
        attacks = {
            "wrong-schema": source.replace("se-harness-host-adapter-v1", "unknown-adapter"),
            "wrong-name": source.replace("canonical-name: harness-draft-change", "canonical-name: harness-orient"),
            "traversal": source.replace(
                ".agents/skills/harness-draft-change", "../.agents/skills/harness-draft-change"
            ),
            "absolute": source.replace(
                ".agents/skills/harness-draft-change", "/.agents/skills/harness-draft-change"
            ),
            "permission": source.replace("metadata:\n", "allowed-tools: Bash\nmetadata:\n"),
            "remote": source + "\nhttps://example.invalid/skill\n",
        }
        required = (
            "adapter-schema: se-harness-host-adapter-v1",
            "canonical-name: harness-draft-change",
            "canonical-path: .agents/skills/harness-draft-change",
            "disable-model-invocation: true",
        )
        forbidden = ("allowed-tools:", "http://", "https://", "../", "canonical-path: /")
        for label, raw in attacks.items():
            with self.subTest(attack=label):
                self.assertTrue(any(item not in raw for item in required) or any(item in raw for item in forbidden))


class Phase4EvaluatorClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.draft = load_script(
            "phase4_draft_guard", PHASE3_ROOTS["harness-draft-change"] / "scripts/guard.py"
        )
        cls.execute = load_script(
            "phase4_execute_guard", PHASE3_ROOTS["harness-execute-work-order"] / "scripts/check_scope.py"
        )
        cls.assurance = load_script(
            "phase4_assurance_guard", PHASE3_ROOTS["harness-prepare-assurance"] / "scripts/check_prepare.py"
        )
        cls.brief = load_script(
            "technical_communication_brief_check", OPERATOR_BRIEF
        )

    @staticmethod
    def catalog() -> list[dict[str, str]]:
        return [
            {"id": item}
            for item in (
                "delegated-work-order-start",
                "change-bundle-apply",
                "delegated-work-order-complete",
                "delegated-vrec-prepare",
            )
        ]

    @staticmethod
    def evaluator_request(operation: str) -> dict[str, object]:
        return {
            "schema": "se-harness-evaluator-client-request-v1",
            "arguments": ["delegated-workflow", operation, ".", "--work-order", "WO-AEX-008"],
            "delegation_sha256": "a" * 64,
        }

    @staticmethod
    def execution_result(work_order: str, *, with_effect: bool = True) -> dict[str, object]:
        return {
            "outcome": "completed-at-git-stop",
            "work_order": work_order,
            "start": {"lifecycle_proof": {}},
            "effects": [{"receipt": {}}] if with_effect else [],
            "completion": {"lifecycle_proof": {}},
            "next": {"decision_packet": {}},
        }

    def test_client_case_vector_covers_all_phase4_skill_stops_and_successes(self) -> None:
        value = json.loads(PHASE4_SKILL_CASES.read_text(encoding="utf-8"))
        self.assertEqual("se-harness-phase4-skill-client-cases-v1", value["schema"])
        self.assertEqual("se-harness-workflow-v4", value["workflow_schema"])
        self.assertTrue(value["single_agent"])
        self.assertFalse(value["direct_target_writes"])
        self.assertEqual(
            {
                "implicit-writing-nonactivation",
                "unavailable-public-0-6-evaluator",
                "invalid-delegation",
                "active-session-conflict",
                "direct-target-write-attempt",
                "valid-sequential-bundle-and-completion",
                "commit-bound-vrec-missing-commit",
                "prepared-vrec-assurance-stop",
            },
            {item["id"] for item in value["cases"]},
        )
        self.assertTrue({"direct-target-write", "git-mutation", "assurance-decision"}.issubset(value["prohibited"]))

    def test_draft_client_invokes_only_evaluator_after_closed_checks(self) -> None:
        request = {
            "schema": "se-harness-evaluator-client-request-v1",
            "explicit_skill": "harness-draft-change",
            "workflow_schema": "se-harness-workflow-v4",
            "interface_operation": "delegated-workflow-execute",
            "direct_target_write": False,
            "work_order": "WO-AEX-008",
            "state": "approved",
            "effect_class": "draft-create",
            "planned_paths": ["docs/engineering/example/requirements/REQ-EX-001.md"],
            "allowed_paths": ["docs/engineering/example/requirements/REQ-EX-001.md"],
            "revisions": {},
            "evaluator_request": self.evaluator_request("execute"),
        }
        calls: list[tuple[str, ...]] = []
        result = self.draft.invoke_draft_client(
            request,
            catalog=self.catalog,
            client=lambda arguments: calls.append(arguments) or self.execution_result("WO-AEX-008", with_effect=False),
        )
        self.assertEqual("se-harness-evaluator-client-result-v1", result["schema"])
        self.assertEqual("completed-at-git-stop", result["outcome"])
        self.assertEqual([tuple(request["evaluator_request"]["arguments"])], calls)

        for label, mutate in (
            ("implicit", lambda value: value.__setitem__("explicit_skill", "")),
            ("direct", lambda value: value.__setitem__("direct_target_write", True)),
            ("escape", lambda value: value.__setitem__("planned_paths", ["../outside.md"])),
            ("scope", lambda value: value.__setitem__("planned_paths", ["README.md"])),
            ("state", lambda value: value.__setitem__("revisions", {"REQ-EX-001": "approved"})),
            ("delegation", lambda value: value["evaluator_request"].__setitem__("delegation_sha256", "invalid")),
        ):
            with self.subTest(label=label):
                rejected = json.loads(json.dumps(request))
                mutate(rejected)
                calls.clear()
                with self.assertRaises(self.draft.DraftGuardError):
                    self.draft.invoke_draft_client(
                        rejected,
                        catalog=self.catalog,
                        client=lambda arguments: calls.append(arguments),
                    )
                self.assertEqual([], calls)
        with self.assertRaisesRegex(self.draft.DraftGuardError, "AEXDRF014"):
            self.draft.invoke_draft_client(
                request,
                catalog=lambda: [],
                client=lambda arguments: calls.append(arguments),
            )
        self.assertEqual([], calls)

    def test_work_order_client_requires_approved_scope_and_exact_phase4_catalog(self) -> None:
        base = {
            "schema": "se-harness-evaluator-client-request-v1",
            "explicit_skill": "harness-execute-work-order",
            "workflow_schema": "se-harness-workflow-v4",
            "interface_operation": "delegated-workflow-execute",
            "direct_target_write": False,
            "work_order": "WO-AEX-008",
            "state": "approved",
            "effect_class": "implementation-write",
            "planned_paths": ["se_harness/skill_contract.py"],
            "execution_scope": ["se_harness/skill_contract.py", "tests/fixtures/agentic_execution/phase4/"],
            "evaluator_request": self.evaluator_request("execute"),
        }
        calls: list[tuple[str, ...]] = []
        result = self.execute.invoke_work_order_client(
            base,
            catalog=self.catalog,
            client=lambda arguments: calls.append(arguments) or self.execution_result("WO-AEX-008"),
        )
        self.assertEqual("se-harness-evaluator-client-result-v1", result["schema"])
        self.assertEqual(1, len(calls))

        for state in ("draft", "in_progress", "implemented", "verified", "rejected"):
            rejected = {**base, "state": state}
            calls.clear()
            with self.subTest(state=state), self.assertRaises(self.execute.ScopeGuardError):
                self.execute.invoke_work_order_client(
                    rejected, catalog=self.catalog, client=lambda arguments: calls.append(arguments)
                )
            self.assertEqual([], calls)
        for hostile in ("../escape.py", "/absolute.py", "file://host/path", "tests/*.py", "README.md"):
            rejected = {**base, "planned_paths": [hostile]}
            calls.clear()
            with self.subTest(path=hostile), self.assertRaises(self.execute.ScopeGuardError):
                self.execute.invoke_work_order_client(
                    rejected, catalog=self.catalog, client=lambda arguments: calls.append(arguments)
                )
            self.assertEqual([], calls)
        for label, rejected in (
            ("direct", {**base, "direct_target_write": True}),
            ("catalog", base),
        ):
            calls.clear()
            selected_catalog = (lambda: []) if label == "catalog" else self.catalog
            with self.subTest(label=label), self.assertRaises(self.execute.ScopeGuardError):
                self.execute.invoke_work_order_client(
                    rejected, catalog=selected_catalog, client=lambda arguments: calls.append(arguments)
                )
            self.assertEqual([], calls)

    def test_public_0_6_interface_without_delegated_workflow_stops_before_client(self) -> None:
        environment = {**os.environ, "AEX_FAKE_VERSION": "0.6.0", "AEX_FAKE_MODE": "healthy"}
        help_result = subprocess.run(
            [sys.executable, "-B", str(FAKE_EVALUATOR), "--help"],
            capture_output=True,
            text=True,
            check=True,
            env=environment,
        )
        self.assertNotIn("delegated-workflow", help_result.stdout)
        request = {
            "schema": "se-harness-evaluator-client-request-v1",
            "explicit_skill": "harness-execute-work-order",
            "workflow_schema": "se-harness-workflow-v4",
            "interface_operation": "delegated-workflow-execute",
            "direct_target_write": False,
            "work_order": "WO-AEX-008",
            "state": "approved",
            "effect_class": "implementation-write",
            "planned_paths": ["se_harness/skill_contract.py"],
            "execution_scope": ["se_harness/skill_contract.py"],
            "evaluator_request": self.evaluator_request("execute"),
        }
        calls: list[tuple[str, ...]] = []
        with self.assertRaisesRegex(self.execute.ScopeGuardError, "AEXEXE012"):
            self.execute.invoke_work_order_client(
                request,
                catalog=lambda: [],
                client=lambda arguments: calls.append(arguments),
            )
        self.assertEqual([], calls)
    def test_assurance_client_stops_for_git_or_returns_prepared_record(self) -> None:
        request = {
            "schema": "se-harness-evaluator-client-request-v1",
            "explicit_skill": "harness-prepare-assurance",
            "workflow_schema": "se-harness-workflow-v4",
            "interface_operation": "delegated-workflow-prepare-vrec",
            "direct_target_write": False,
            "work_order": "WO-AEX-008",
            "state": "implemented",
            "record_id": "VREC-AEX-008",
            "record_destination": "docs/engineering/agentic-execution/verification-records/VREC-AEX-008.md",
            "candidate_commit": None,
            "record_exists": False,
            "preparation_actor": "engineering-owner",
            "completion_proof": {"operation": "delegated-work-order-complete"},
            "evaluator_request": self.evaluator_request("prepare-vrec"),
        }
        calls: list[tuple[str, ...]] = []
        stopped = self.assurance.invoke_assurance_client(
            request,
            catalog=self.catalog,
            client=lambda arguments: calls.append(arguments) or {
                "outcome": "stopped", "result": {}, "decision_packet": {"next": "authorize-git"}
            },
        )
        self.assertEqual("stopped", stopped["outcome"])
        prepared = self.assurance.invoke_assurance_client(
            {**request, "candidate_commit": "b" * 40},
            catalog=self.catalog,
            client=lambda arguments: {
                "outcome": "prepared",
                "record": request["record_destination"],
                "receipt": {},
                "result": {},
                "decision_packet": {"next": "independent-assurance"},
            },
        )
        self.assertEqual("prepared", prepared["outcome"])

        for label, change in (
            ("actor", {"preparation_actor": ""}),
            ("collision", {"record_exists": True}),
            ("implicit", {"explicit_skill": ""}),
            ("direct", {"direct_target_write": True}),
            ("proof", {"completion_proof": {}}),
        ):
            rejected = {**request, **change}
            calls.clear()
            with self.subTest(label=label), self.assertRaises(self.assurance.AssuranceGuardError):
                self.assurance.invoke_assurance_client(
                    rejected, catalog=self.catalog, client=lambda arguments: calls.append(arguments)
                )
            self.assertEqual([], calls)

    def brief_request(
        self,
        source: str,
        protected: list[tuple[str, str]],
        *,
        rendered: str | None = None,
    ) -> dict[str, object]:
        output = source if rendered is None else rendered
        source_spans = []
        output_bindings = []
        source_cursor = 0
        output_cursor = 0
        for index, (token, kind) in enumerate(protected):
            source_character = source.index(token, source_cursor)
            output_character = output.index(token, output_cursor)
            source_start = len(source[:source_character].encode("utf-8"))
            source_end = source_start + len(token.encode("utf-8"))
            output_start = len(output[:output_character].encode("utf-8"))
            output_end = output_start + len(token.encode("utf-8"))
            digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
            span_id = f"span-{index + 1}"
            source_spans.append({
                "id": span_id,
                "kind": kind,
                "start": source_start,
                "end": source_end,
                "sha256": digest,
            })
            output_bindings.append({
                "id": span_id,
                "start": output_start,
                "end": output_end,
                "sha256": digest,
            })
            source_cursor = source_character + len(token)
            output_cursor = output_character + len(token)
        return {
            "explicit_skill": "harness-operator-brief",
            "profile": "operator-communication",
            "source_kind": "bounded-technical-text",
            "source_text": source,
            "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
            "protected_spans": source_spans,
            "rendered_text": output,
            "bindings": output_bindings,
            "changed_paths": [],
        }

    def test_brief_checker_preserves_unicode_source_bytes_and_reports_zero_changes(self) -> None:
        source = "Décision: WO-EX-001. Run harnessctl focus . --artifact WO-EX-001."
        rendered = "Next action. " + source
        request = self.brief_request(
            source,
            [
                ("WO-EX-001", "identifier"),
                ("harnessctl focus . --artifact WO-EX-001", "command"),
            ],
            rendered=rendered,
        )
        result = self.brief.validate_brief(request)
        self.assertEqual("completed", result["outcome"])
        self.assertEqual("operator-communication", result["profile"])
        self.assertEqual(2, result["protected_binding_count"])
        self.assertEqual([], result["changed_paths"])

    def test_brief_checker_fails_closed_on_source_span_output_and_effect_changes(self) -> None:
        request = self.brief_request(
            "Use WO-EX-002 at version 0.6.0.",
            [("WO-EX-002", "identifier"), ("0.6.0", "version")],
            rendered="Outcome: Use WO-EX-002 at version 0.6.0.",
        )
        cases = (
            ("source-digest", lambda value: value.__setitem__("source_sha256", "0" * 64), "TCM006"),
            (
                "overlap",
                lambda value: value["protected_spans"][1].__setitem__(
                    "start", value["protected_spans"][0]["end"] - 1
                ),
                "TCM007",
            ),
            (
                "output-byte",
                lambda value: value.__setitem__("rendered_text", value["rendered_text"].replace("0.6.0", "0.6.1")),
                "TCM010",
            ),
            ("changed-path", lambda value: value.__setitem__("changed_paths", ["README.md"]), "TCM012"),
            ("unknown-field", lambda value: value.__setitem__("authority", "assurance-owner"), "TCM002"),
        )
        for label, mutate, code in cases:
            with self.subTest(label=label):
                changed = json.loads(json.dumps(request))
                mutate(changed)
                with self.assertRaisesRegex(self.brief.BriefCheckError, code):
                    self.brief.validate_brief(changed)

    def test_canonical_restitution_block_is_returned_alone(self) -> None:
        source = "Outcome\nCompleted.\n\nCurrent lifecycle state\n- WO-EX-003 is approved."
        exact = self.brief_request(source, [(source, "canonical-restitution-block")])
        self.assertEqual("completed", self.brief.validate_brief(exact)["outcome"])
        surrounded = self.brief_request(
            source,
            [(source, "canonical-restitution-block")],
            rendered="Summary:\n" + source,
        )
        with self.assertRaisesRegex(self.brief.BriefCheckError, "TCM013"):
            self.brief.validate_brief(surrounded)

    def test_protected_partition_property_rejects_each_changed_binding(self) -> None:
        source = "alpha beta gamma delta"
        tokens = [(token, "established-terminology") for token in source.split()]
        request = self.brief_request(source, tokens, rendered="Outcome: " + source)
        self.brief.validate_brief(request)
        for index in range(len(tokens)):
            changed = json.loads(json.dumps(request))
            binding = changed["bindings"][index]
            binding["sha256"] = "0" * 64
            with self.subTest(index=index), self.assertRaisesRegex(self.brief.BriefCheckError, "TCM010"):
                self.brief.validate_brief(changed)

    def test_review_corpus_covers_operator_artifact_safety_and_terms(self) -> None:
        corpus = json.loads(TECHNICAL_COMMUNICATION_CORPUS.read_text(encoding="utf-8"))
        self.assertEqual("se-harness-technical-communication-review-corpus-v1", corpus["schema"])
        self.assertEqual("5/10", corpus["target_expertise"])
        self.assertGreaterEqual(len(corpus["cases"]), 11)
        profiles = [item["profile"] for item in corpus["cases"]]
        self.assertGreaterEqual(profiles.count("operator-communication"), 4)
        self.assertGreaterEqual(profiles.count("technical-artifact-writing"), 5)
        ids = {item["id"] for item in corpus["cases"]}
        self.assertTrue({"operator-current-decision", "operator-blocked", "operator-exact-output",
                         "operator-no-current-state", "safety-qualification", "project-term"}.issubset(ids))
        expected_fields = {"actor", "action", "condition", "force", "qualification", "result"}
        for item in corpus["cases"]:
            self.assertEqual(expected_fields, set(item["expected"]))
            for token in item["protected_tokens"]:
                self.assertIn(token, item["source"])

    def test_canonical_json_is_stable_and_rejects_floats(self) -> None:
        self.assertEqual(b'{"a":1,"z":[true,null]}\n', canonical_json_bytes({"z": [True, None], "a": 1}))
        with self.assertRaisesRegex(SkillContractError, "SKC003"):
            canonical_json_bytes({"not_allowed": 1.25})

    def test_independent_canonical_receipt_vector_matches_exact_bytes_and_digest(self) -> None:
        vector = json.loads(VECTORS.read_text(encoding="utf-8"))["receipt"]
        encoded = canonical_json_bytes(vector["value"])
        self.assertEqual(vector["canonical"].encode("utf-8"), encoded)
        self.assertEqual(vector["sha256"], hashlib.sha256(encoded).hexdigest())

    def test_manifest_normalizes_line_endings_and_detects_content_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first"
            second = Path(temporary) / "second"
            shutil.copytree(SKILL_ROOT, first)
            shutil.copytree(SKILL_ROOT, second)
            for path in second.rglob("*"):
                if path.is_file():
                    path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))

            baseline = build_skill_manifest(first)
            self.assertEqual(baseline.sha256, build_skill_manifest(second).sha256)
            (second / "SKILL.md").write_bytes((second / "SKILL.md").read_bytes() + b"changed\r\n")
            self.assertNotEqual(baseline.sha256, build_skill_manifest(second).sha256)

    def test_manifest_rejects_missing_required_invalid_utf8_and_reserved_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "skill"
            shutil.copytree(SKILL_ROOT, root)
            (root / "SKILL.md").unlink()
            with self.assertRaisesRegex(SkillContractError, "SKM008"):
                build_skill_manifest(root)

            shutil.copy2(SKILL_ROOT / "SKILL.md", root / "SKILL.md")
            invalid = root / "invalid.txt"
            invalid.write_bytes(b"\xff")
            with self.assertRaisesRegex(SkillContractError, "SKM007"):
                build_skill_manifest(root)
            invalid.unlink()

            # A reserved device basename is not creatable on every Windows image. On
            # hosted windows-2022 the write succeeds against the device itself and leaves
            # nothing to enumerate, so the manifest never sees the entry and this branch
            # asserted a refusal that could not be reached. The enumeration path is
            # exercised only where the entry is a real file; the refusal itself is
            # asserted on every platform by
            # test_reserved_path_components_are_refused_on_every_platform.
            reserved = root / "NUL.txt"
            try:
                reserved.write_text("reserved\n", encoding="utf-8")
            except OSError:
                enumerated = False
            else:
                enumerated = reserved.name in {entry.name for entry in root.iterdir()}
            if enumerated:
                with self.assertRaisesRegex(SkillContractError, "SKM003"):
                    build_skill_manifest(root)

    def test_reserved_path_components_are_refused_on_every_platform(self) -> None:
        """Filesystem-independent, mirroring `AgentContractTests.test_portable_paths_fail_closed`.

        `VER-AEX-001` requires reserved-name paths to be exercised. Driving that through
        the filesystem only exercises it where a reserved basename can exist as a file,
        which excludes the hosted Windows image the release orchestrator qualifies on.
        """

        for component in ("NUL.txt", "nul", "CON", "PRN.md", "aux.json", "COM1.py", "lpt9.yaml"):
            with self.subTest(component=component):
                with self.assertRaisesRegex(SkillContractError, "SKM003"):
                    _validate_component(component)
        for component in ("openai.yaml", "SKILL.md", "skill-contract.json", "nullable.py"):
            with self.subTest(component=component):
                self.assertIsNone(_validate_component(component))

    @unittest.skipIf(os.name == "nt", "creating an unprivileged symlink is not portable on Windows")
    def test_manifest_rejects_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "skill"
            shutil.copytree(SKILL_ROOT, root)
            (root / "linked").symlink_to(root / "SKILL.md")
            with self.assertRaisesRegex(SkillContractError, "SKM005"):
                build_skill_manifest(root)

    @unittest.skipIf(os.name == "nt", "Windows cannot create the hostile portable names")
    def test_manifest_rejects_case_collisions_and_alternate_separators(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "skill"
            shutil.copytree(SKILL_ROOT, root)
            (root / "Case.txt").write_text("one\n", encoding="utf-8")
            (root / "case.txt").write_text("two\n", encoding="utf-8")
            with self.assertRaisesRegex(SkillContractError, "SKM004"):
                build_skill_manifest(root)
            (root / "Case.txt").unlink()
            (root / "case.txt").unlink()
            (root / "alternate\\separator.txt").write_text("unsafe\n", encoding="utf-8")
            with self.assertRaisesRegex(SkillContractError, "SKM003"):
                build_skill_manifest(root)


class HarnessOrientBlackBoxTests(unittest.TestCase):
    def invoke(
        self,
        target: Path,
        *,
        mode: str = "healthy",
        version: str = "0.6.0",
        artifact: str | None = None,
        preflight_phase: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        launcher = json.dumps([sys.executable, "-B", str(FAKE_EVALUATOR)])
        command = [
            sys.executable,
            "-B",
            str(ORIENT),
            str(target),
            "--evaluator-launcher-json",
            launcher,
            "--expected-evaluator-version",
            version,
            "--expected-evaluator-root",
            str(Path(sys.prefix)),
        ]
        if artifact is not None:
            command.extend(["--artifact", artifact])
        if preflight_phase is not None:
            command.extend(["--preflight-phase", preflight_phase])
        environment = os.environ.copy()
        environment["AEX_FAKE_MODE"] = mode
        environment["AEX_FAKE_VERSION"] = version
        return subprocess.run(command, capture_output=True, text=True, check=False, env=environment)

    def make_target(self, parent: Path) -> Path:
        target = parent / "repository"
        (target / ".git/refs/heads").mkdir(parents=True)
        (target / ".git/HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
        (target / ".git/refs/heads/main").write_text("a" * 40 + "\n", encoding="utf-8")
        (target / "README.md").write_text("fixture\n", encoding="utf-8")
        return target

    def test_healthy_selected_orientation_is_deterministic_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            before = snapshot(target)
            first = self.invoke(target, artifact="WO-TST-001")
            after = snapshot(target)

            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(before, after)
            result = json.loads(first.stdout)
            self.assertEqual("completed", result["outcome"])
            self.assertEqual("in_progress", result["selected"]["lifecycle_state"])
            self.assertEqual("fixture-repository", result["repository"]["name"])
            receipt = result["execution_receipt"]
            self.assertEqual([], receipt["effects"]["changed_paths"])
            self.assertEqual(receipt["effects"]["state_before"], receipt["effects"]["state_after"])
            self.assertEqual(["single-agent-orientation"], receipt["execution"]["profiles"])
            self.assertEqual([], receipt["execution"]["worker_results"])
            self.assertEqual(
                hashlib.sha256(canonical_json_bytes(receipt)).hexdigest(),
                result["execution_receipt_sha256"],
            )

    def test_candidate_source_content_and_repository_secret_are_not_governing_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            (target / "se_harness").mkdir()
            (target / "se_harness/__init__.py").write_text('__version__ = "999.0.0"\n', encoding="utf-8")
            (target / "private.txt").write_text("credential=do-not-expose\n", encoding="utf-8")
            completed = self.invoke(target)

            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertNotIn("999.0.0", completed.stdout)
            self.assertNotIn("do-not-expose", completed.stdout)
            result = json.loads(completed.stdout)
            self.assertEqual({"governing": False, "status": "not_assessed"}, result["candidate_source"])
            self.assertEqual("0.6.0", result["released_evaluator"]["version"])

    def test_exact_0_5_without_focus_degrades_only_selected_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            completed = self.invoke(target, mode="no-focus", version="0.5.0", artifact="WO-TST-001")

            self.assertEqual(0, completed.returncode, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual("degraded", result["outcome"])
            self.assertEqual("not_assessable", result["selected"]["status"])
            self.assertEqual("passed", result["integrity"]["outcome"])
            self.assertTrue(result["validation"]["valid"])
            operation_ids = [item["id"] for item in result["execution_receipt"]["execution"]["operations"]]
            self.assertNotIn("focus-json", operation_ids)
            self.assertIn(
                {"code": "AEXORI030", "operation": "focus-json", "status": "not_assessable"},
                result["execution_receipt"]["validation"]["deviations"],
            )

    def test_required_identity_failure_blocks_before_integrity_and_preserves_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            before = snapshot(target)
            completed = self.invoke(target, mode="identity-fail")

            self.assertEqual(2, completed.returncode)
            self.assertEqual(before, snapshot(target))
            result = json.loads(completed.stdout)
            self.assertEqual("blocked", result["outcome"])
            self.assertEqual(
                ["version", "identity"],
                [item["id"] for item in result["execution_receipt"]["execution"]["operations"]],
            )

    def test_invalid_graph_blocks_before_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            completed = self.invoke(target, mode="invalid-graph")

            self.assertEqual(2, completed.returncode)
            result = json.loads(completed.stdout)
            self.assertEqual("blocked", result["outcome"])
            self.assertFalse(result["validation"]["valid"])
            operation_ids = [item["id"] for item in result["execution_receipt"]["execution"]["operations"]]
            self.assertIn("validate-json", operation_ids)
            self.assertNotIn("inspect-json", operation_ids)

    def test_malformed_required_json_fails_and_large_output_is_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            malformed = self.invoke(target, mode="malformed-validation")
            self.assertEqual(2, malformed.returncode)
            malformed_result = json.loads(malformed.stdout)
            self.assertEqual("failed", malformed_result["outcome"])
            self.assertIn("AEXORI021", malformed.stdout)

            large = self.invoke(target, mode="large-output")
            self.assertEqual(2, large.returncode)
            large_result = json.loads(large.stdout)
            self.assertEqual("blocked", large_result["outcome"])
            self.assertLess(len(large.stdout), 50_000)

    def test_managed_integrity_diagnostic_redacts_secret_and_host_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            completed = self.invoke(target, mode="doctor-fail")

            self.assertEqual(2, completed.returncode)
            result = json.loads(completed.stdout)
            rendered = json.dumps(result, sort_keys=True)
            self.assertNotIn("top-secret", rendered)
            self.assertNotIn(str(target), rendered)
            self.assertIn("secret=<redacted>", rendered)

    def test_preflight_is_explicit_and_cannot_be_rendered_as_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            completed = self.invoke(
                target,
                mode="preflight-blocked",
                artifact="WO-TST-001",
                preflight_phase="review",
            )

            self.assertEqual(2, completed.returncode)
            result = json.loads(completed.stdout)
            self.assertEqual("blocked", result["outcome"])
            self.assertFalse(result["preflight"]["ready"])
            self.assertNotIn("approved", completed.stdout.lower())

    def test_preflight_rejects_non_work_order_selection_without_running_evaluator(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            completed = self.invoke(target, artifact="REQ-TST-001", preflight_phase="start")

            self.assertEqual(2, completed.returncode)
            result = json.loads(completed.stdout)
            self.assertEqual([], result["execution_receipt"]["execution"]["operations"])
            self.assertEqual("blocked", result["outcome"])

    def test_unsupported_old_evaluator_and_missing_launcher_block_without_target_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            before = snapshot(target)
            old = self.invoke(target, version="0.4.9")
            self.assertEqual(2, old.returncode)
            self.assertEqual([], json.loads(old.stdout)["execution_receipt"]["execution"]["operations"])

            command = [
                sys.executable,
                "-B",
                str(ORIENT),
                str(target),
                "--evaluator-launcher-json",
                json.dumps([str(Path(temporary) / "missing-evaluator")]),
                "--expected-evaluator-version",
                "0.6.0",
                "--expected-evaluator-root",
                str(Path(temporary) / "missing-root"),
            ]
            missing = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(2, missing.returncode)
            self.assertEqual("blocked", json.loads(missing.stdout)["outcome"])
            self.assertEqual(before, snapshot(target))


if __name__ == "__main__":
    unittest.main()
