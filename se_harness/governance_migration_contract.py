"""Strict contract and scenario parsing for governance migration rehearsals."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping


CONTRACT_SCHEMA = "se-harness-governance-migration-v1"
RESULT_SCHEMA = "se-harness-governance-migration-result-v1"
STAGE_ORDER = (
    "prepare",
    "validate-complete",
    "reject",
    "replace",
    "assess",
    "release-plan",
    "publish-plan",
    "render",
    "adopt",
)
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
IDENTIFIER_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}")
ARTIFACT_PATTERN = re.compile(r"[A-Z][A-Z0-9]*-[A-Z0-9]+-[0-9]{3}")
VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.!+\-]{0,127}")
TIMESTAMP_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


class MigrationContractError(ValueError):
    """A migration contract or scenario is incomplete, ambiguous, or noncanonical."""


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise MigrationContractError(f"MIG101: duplicate JSON key: {key}")
        result[key] = value
    return result


def _parse_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MigrationContractError(f"MIG102: {label} must be UTF-8") from exc
    try:
        value = json.loads(text, object_pairs_hook=_unique_object)
    except json.JSONDecodeError as exc:
        raise MigrationContractError(f"MIG103: invalid {label} JSON: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise MigrationContractError(f"MIG104: {label} root must be an object")
    return value


def _exact_keys(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    missing = expected - set(value)
    unknown = set(value) - expected
    if missing:
        raise MigrationContractError(f"MIG105: {label} is missing field: {sorted(missing)[0]}")
    if unknown:
        raise MigrationContractError(f"MIG106: {label} has unknown field: {sorted(unknown)[0]}")


def _strings(value: Any, label: str, *, sorted_unique: bool = True) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise MigrationContractError(f"MIG107: {label} must be an array of non-empty strings")
    if len(set(value)) != len(value):
        raise MigrationContractError(f"MIG108: {label} contains a duplicate")
    if sorted_unique and value != sorted(value):
        raise MigrationContractError(f"MIG109: {label} must be sorted")
    return value


def _identifier(value: Any, label: str, pattern: re.Pattern[str] = IDENTIFIER_PATTERN) -> str:
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        raise MigrationContractError(f"MIG110: invalid {label}")
    return value


def _sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_PATTERN.fullmatch(value) is None:
        raise MigrationContractError(f"MIG111: invalid {label} SHA-256")
    return value


def _package_path() -> Path:
    return Path(__file__).with_name("governance_migration_contract.json")


def load_migration_contract(path: Path | None = None) -> dict[str, Any]:
    selected = path or _package_path()
    try:
        raw = selected.read_bytes()
    except OSError as exc:
        raise MigrationContractError(f"MIG112: cannot read migration contract: {exc}") from exc
    contract = _parse_json(raw, "migration contract")
    _validate_contract(contract)
    return contract


def migration_contract_bytes(path: Path | None = None) -> bytes:
    selected = path or _package_path()
    try:
        raw = selected.read_bytes()
    except OSError as exc:
        raise MigrationContractError(f"MIG112: cannot read migration contract: {exc}") from exc
    _validate_contract(_parse_json(raw, "migration contract"))
    return raw


def _validate_contract(contract: Mapping[str, Any]) -> None:
    _exact_keys(
        contract,
        {
            "accountable_roles",
            "adapters",
            "capabilities",
            "credential_signals",
            "decision_types",
            "external_actions",
            "limits",
            "result_schema",
            "schema",
            "stage_order",
            "stages",
            "technical_roles",
        },
        "migration contract",
    )
    if contract["schema"] != CONTRACT_SCHEMA or contract["result_schema"] != RESULT_SCHEMA:
        raise MigrationContractError("MIG113: unsupported migration contract or result schema")
    if contract["stage_order"] != list(STAGE_ORDER):
        raise MigrationContractError("MIG114: migration stage catalog or order differs from v1")
    technical_roles = set(_strings(contract["technical_roles"], "technical roles"))
    accountable_roles = set(_strings(contract["accountable_roles"], "accountable roles"))
    external_actions = _strings(contract["external_actions"], "external actions")
    credentials = _strings(contract["credential_signals"], "credential signals")
    if any(not item.isupper() for item in credentials):
        raise MigrationContractError("MIG115: credential signals must be uppercase names")

    stages = contract["stages"]
    if not isinstance(stages, dict) or set(stages) != set(STAGE_ORDER):
        raise MigrationContractError("MIG116: stage definitions must exactly cover the v1 catalog")
    for stage_id in STAGE_ORDER:
        stage = stages[stage_id]
        if not isinstance(stage, dict):
            raise MigrationContractError(f"MIG117: stage {stage_id} must be an object")
        _exact_keys(
            stage,
            {"accountable_decision", "permitted_mutations", "technical_roles", "views"},
            f"stage {stage_id}",
        )
        roles = set(_strings(stage["technical_roles"], f"stage {stage_id} technical roles"))
        if not roles or not roles <= technical_roles:
            raise MigrationContractError(f"MIG118: stage {stage_id} has an invalid technical role")
        _strings(stage["views"], f"stage {stage_id} views")
        _strings(stage["permitted_mutations"], f"stage {stage_id} permitted mutations")
        decision = stage["accountable_decision"]
        if decision is not None and not isinstance(decision, str):
            raise MigrationContractError(f"MIG119: stage {stage_id} decision type is invalid")

    decisions = contract["decision_types"]
    if not isinstance(decisions, dict) or set(decisions) != {"adopt", "reject"}:
        raise MigrationContractError("MIG120: decision catalog must contain only adopt and reject")
    for decision_id, decision in decisions.items():
        if not isinstance(decision, dict):
            raise MigrationContractError(f"MIG121: decision {decision_id} must be an object")
        _exact_keys(decision, {"accountable_role", "permitted_effect"}, f"decision {decision_id}")
        if decision["accountable_role"] not in accountable_roles:
            raise MigrationContractError(f"MIG122: decision {decision_id} has an invalid accountable role")
        _identifier(decision["permitted_effect"], f"decision {decision_id} permitted effect")
    for stage_id, stage in stages.items():
        decision = stage["accountable_decision"]
        if decision is not None and decision not in decisions:
            raise MigrationContractError(f"MIG123: stage {stage_id} references an unknown decision")

    capabilities = contract["capabilities"]
    if not isinstance(capabilities, dict) or not capabilities:
        raise MigrationContractError("MIG124: capability catalog must be a non-empty object")
    for capability, operations in capabilities.items():
        _identifier(capability, "capability")
        selected = set(_strings(operations, f"capability {capability} operations"))
        if not selected <= set(STAGE_ORDER):
            raise MigrationContractError(f"MIG125: capability {capability} names an unknown operation")

    adapters = contract["adapters"]
    if not isinstance(adapters, dict) or not adapters:
        raise MigrationContractError("MIG126: adapter catalog must be a non-empty object")
    for adapter_id, adapter in adapters.items():
        _identifier(adapter_id, "adapter ID")
        if not isinstance(adapter, dict):
            raise MigrationContractError(f"MIG127: adapter {adapter_id} must be an object")
        _exact_keys(
            adapter,
            {"implementation_path", "implementation_sha256", "stages", "view"},
            f"adapter {adapter_id}",
        )
        implementation = _identifier(adapter["implementation_path"], f"adapter {adapter_id} implementation")
        if implementation != "governance_migration.py":
            raise MigrationContractError(f"MIG128: adapter {adapter_id} implementation is not packaged")
        _sha256(adapter["implementation_sha256"], f"adapter {adapter_id} implementation")
        adapter_stages = set(_strings(adapter["stages"], f"adapter {adapter_id} stages"))
        if not adapter_stages <= set(STAGE_ORDER):
            raise MigrationContractError(f"MIG129: adapter {adapter_id} names an unknown stage")
        view = _identifier(adapter["view"], f"adapter {adapter_id} view")
        if any(view not in stages[stage_id]["views"] for stage_id in adapter_stages):
            raise MigrationContractError(f"MIG130: adapter {adapter_id} view is invalid for its stage")

    limits = contract["limits"]
    if not isinstance(limits, dict):
        raise MigrationContractError("MIG131: limits must be an object")
    _exact_keys(limits, {"max_child_output_bytes", "max_scenario_bytes", "subprocess_timeout_seconds"}, "limits")
    if any(type(value) is not int or value < 1 for value in limits.values()):
        raise MigrationContractError("MIG132: migration limits must be positive integers")
    if not external_actions:
        raise MigrationContractError("MIG133: external action refusal catalog must not be empty")


def _validate_proposal(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MigrationContractError(f"MIG134: {label} must be an object")
    _exact_keys(
        value,
        {"artifact_id", "evaluator_evidence", "release_contract_id", "schema", "status", "version"},
        label,
    )
    _identifier(value["artifact_id"], f"{label} artifact ID", ARTIFACT_PATTERN)
    _identifier(value["release_contract_id"], f"{label} release-contract ID", ARTIFACT_PATTERN)
    if not isinstance(value["version"], str) or VERSION_PATTERN.fullmatch(value["version"]) is None:
        raise MigrationContractError(f"MIG135: {label} version is invalid")
    if type(value["schema"]) is not int or value["schema"] not in {2, 3}:
        raise MigrationContractError(f"MIG136: {label} schema must be 2 or 3")
    if type(value["evaluator_evidence"]) is not bool or value["status"] != "ready":
        raise MigrationContractError(f"MIG137: {label} must be a ready proposal with explicit evidence presence")
    return value


def _validate_decision(value: Any, contract: Mapping[str, Any], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MigrationContractError(f"MIG138: {label} must be an object")
    _exact_keys(
        value,
        {"accountable_role", "artifact_id", "decided_at", "id", "permitted_effect", "sha256", "type"},
        label,
    )
    _identifier(value["id"], f"{label} ID")
    _identifier(value["artifact_id"], f"{label} artifact ID", ARTIFACT_PATTERN)
    if value["type"] not in contract["decision_types"]:
        raise MigrationContractError(f"MIG139: {label} has an unknown decision type")
    declared = contract["decision_types"][value["type"]]
    if value["accountable_role"] != declared["accountable_role"]:
        raise MigrationContractError(f"MIG140: {label} accountable role differs from the contract")
    if value["permitted_effect"] != declared["permitted_effect"]:
        raise MigrationContractError(f"MIG141: {label} effect differs from the contract")
    if not isinstance(value["decided_at"], str) or TIMESTAMP_PATTERN.fullmatch(value["decided_at"]) is None:
        raise MigrationContractError(f"MIG142: {label} timestamp must be canonical UTC seconds")
    expected = sha256_bytes(canonical_json({key: item for key, item in value.items() if key != "sha256"}))
    if _sha256(value["sha256"], f"{label} fixture") != expected:
        raise MigrationContractError(f"MIG143: {label} fixture digest mismatch")
    return value


def load_migration_scenario(path: Path, contract: Mapping[str, Any]) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise MigrationContractError(f"MIG144: cannot read migration scenario: {exc}") from exc
    if len(raw) > contract["limits"]["max_scenario_bytes"]:
        raise MigrationContractError("MIG145: migration scenario exceeds the bounded size")
    scenario = _parse_json(raw, "migration scenario")
    if raw != canonical_json(scenario):
        raise MigrationContractError("MIG146: migration scenario is not canonical UTF-8/LF JSON")
    _validate_scenario(scenario, contract)
    return scenario, raw


def _validate_scenario(scenario: Mapping[str, Any], contract: Mapping[str, Any]) -> None:
    _exact_keys(
        scenario,
        {
            "adapters",
            "capabilities",
            "decisions",
            "description",
            "fixture",
            "fixture_sha256",
            "runtime_expectations",
            "scenario_id",
            "schema",
            "stages",
            "versions",
        },
        "migration scenario",
    )
    if scenario["schema"] != CONTRACT_SCHEMA:
        raise MigrationContractError("MIG147: scenario schema differs from the packaged contract")
    _identifier(scenario["scenario_id"], "scenario ID")
    if not isinstance(scenario["description"], str) or not scenario["description"].strip() or len(scenario["description"]) > 512:
        raise MigrationContractError("MIG148: scenario description is invalid")

    versions = scenario["versions"]
    if not isinstance(versions, dict):
        raise MigrationContractError("MIG149: scenario versions must be an object")
    _exact_keys(versions, {"predecessor", "successor"}, "scenario versions")
    for role in ("predecessor", "successor"):
        if not isinstance(versions[role], str) or VERSION_PATTERN.fullmatch(versions[role]) is None:
            raise MigrationContractError(f"MIG150: invalid {role} version")
    if versions["predecessor"] == versions["successor"]:
        raise MigrationContractError("MIG151: predecessor and successor versions must differ")

    runtime_expectations = scenario["runtime_expectations"]
    if not isinstance(runtime_expectations, dict):
        raise MigrationContractError("MIG174: runtime expectations must be an object")
    _exact_keys(runtime_expectations, {"predecessor", "successor"}, "runtime expectations")
    for role in ("predecessor", "successor"):
        expectation = runtime_expectations[role]
        if not isinstance(expectation, dict):
            raise MigrationContractError(f"MIG175: {role} runtime expectation must be an object")
        _exact_keys(expectation, {"archive_name", "archive_sha256", "version"}, f"{role} runtime expectation")
        if expectation["version"] != versions[role]:
            raise MigrationContractError(f"MIG176: {role} runtime expectation version differs")
        name = expectation["archive_name"]
        digest = expectation["archive_sha256"]
        if (name is None) != (digest is None):
            raise MigrationContractError(f"MIG177: {role} archive name and digest must appear together")
        if name is not None:
            expected_name = f"se_harness-{versions[role].replace('-', '_')}-py3-none-any.whl"
            if name != expected_name:
                raise MigrationContractError(f"MIG178: {role} archive name differs from its version")
            _sha256(digest, f"{role} archive")
    if scenario["scenario_id"].startswith("historical-") and runtime_expectations["predecessor"]["archive_sha256"] is None:
        raise MigrationContractError("MIG179: historical scenario must pin the released predecessor archive")

    capabilities = scenario["capabilities"]
    if not isinstance(capabilities, dict):
        raise MigrationContractError("MIG152: scenario capabilities must be an object")
    _exact_keys(capabilities, {"predecessor", "successor_required"}, "scenario capabilities")
    known = set(contract["capabilities"])
    for label in ("predecessor", "successor_required"):
        selected = set(_strings(capabilities[label], f"scenario {label} capabilities"))
        if not selected <= known:
            raise MigrationContractError(f"MIG153: scenario {label} names an unknown capability")

    fixture = scenario["fixture"]
    if not isinstance(fixture, dict):
        raise MigrationContractError("MIG154: scenario fixture must be an object")
    _exact_keys(
        fixture,
        {
            "initial_proposal",
            "predecessor_accepts_rejected",
            "replacement_proposal",
            "simulated_publication_sha256",
        },
        "scenario fixture",
    )
    initial = _validate_proposal(fixture["initial_proposal"], "initial proposal")
    replacement = _validate_proposal(fixture["replacement_proposal"], "replacement proposal")
    if initial["artifact_id"] == replacement["artifact_id"] or initial["release_contract_id"] == replacement["release_contract_id"]:
        raise MigrationContractError("MIG155: replacement must use distinct proposal and contract IDs")
    if initial["version"] != replacement["version"] or initial["version"] != versions["successor"]:
        raise MigrationContractError("MIG156: both proposals must target the declared successor version")
    if type(fixture["predecessor_accepts_rejected"]) is not bool:
        raise MigrationContractError("MIG157: rejected-state support must be boolean")
    _sha256(fixture["simulated_publication_sha256"], "simulated publication")
    expected_fixture = sha256_bytes(canonical_json(fixture))
    if _sha256(scenario["fixture_sha256"], "fixture") != expected_fixture:
        raise MigrationContractError("MIG158: fixture digest mismatch")

    decisions = scenario["decisions"]
    if not isinstance(decisions, list) or len(decisions) != 2:
        raise MigrationContractError("MIG159: scenario requires exactly rejection and adoption fixtures")
    decision_map: dict[str, dict[str, Any]] = {}
    type_map: dict[str, dict[str, Any]] = {}
    for index, decision in enumerate(decisions):
        selected = _validate_decision(decision, contract, f"decision fixture {index + 1}")
        if selected["id"] in decision_map or selected["type"] in type_map:
            raise MigrationContractError("MIG160: decision fixtures contain a duplicate ID or type")
        decision_map[selected["id"]] = selected
        type_map[selected["type"]] = selected
    if set(type_map) != {"adopt", "reject"}:
        raise MigrationContractError("MIG161: scenario decision fixtures must cover reject and adopt")
    if type_map["reject"]["artifact_id"] != initial["artifact_id"]:
        raise MigrationContractError("MIG162: rejection fixture does not select the initial proposal")
    if type_map["adopt"]["artifact_id"] != replacement["artifact_id"]:
        raise MigrationContractError("MIG163: adoption fixture does not select the replacement")

    declared_adapters = _strings(scenario["adapters"], "scenario adapters")
    if not set(declared_adapters) <= set(contract["adapters"]):
        raise MigrationContractError("MIG164: scenario names an unknown adapter")
    stages = scenario["stages"]
    if not isinstance(stages, list) or len(stages) != len(STAGE_ORDER):
        raise MigrationContractError("MIG165: scenario must contain exactly nine stages")
    if [item.get("id") if isinstance(item, dict) else None for item in stages] != list(STAGE_ORDER):
        raise MigrationContractError("MIG166: scenario stages are missing, duplicated, or reordered")
    used_adapters: set[str] = set()
    for stage in stages:
        stage_id = stage["id"]
        _exact_keys(stage, {"adapter", "decision_fixture", "id", "technical_role", "view"}, f"scenario stage {stage_id}")
        rule = contract["stages"][stage_id]
        if stage["technical_role"] not in rule["technical_roles"]:
            raise MigrationContractError(f"MIG167: stage {stage_id} substitutes an unauthorized technical role")
        if stage["view"] not in rule["views"]:
            raise MigrationContractError(f"MIG168: stage {stage_id} substitutes an unauthorized view")
        expected_decision = rule["accountable_decision"]
        fixture_id = stage["decision_fixture"]
        if expected_decision is None:
            if fixture_id is not None:
                raise MigrationContractError(f"MIG169: stage {stage_id} cannot infer an accountable decision")
        elif not isinstance(fixture_id, str) or fixture_id not in decision_map or decision_map[fixture_id]["type"] != expected_decision:
            raise MigrationContractError(f"MIG170: stage {stage_id} lacks its exact accountable decision fixture")
        adapter_id = stage["adapter"]
        if adapter_id is not None:
            if adapter_id not in contract["adapters"] or adapter_id not in declared_adapters:
                raise MigrationContractError(f"MIG171: stage {stage_id} uses an undeclared adapter")
            adapter = contract["adapters"][adapter_id]
            if stage_id not in adapter["stages"] or stage["view"] != adapter["view"]:
                raise MigrationContractError(f"MIG172: stage {stage_id} adapter binding differs from the contract")
            used_adapters.add(adapter_id)
    if sorted(used_adapters) != declared_adapters:
        raise MigrationContractError("MIG173: scenario declares an unused adapter")


def classify_migration(scenario: Mapping[str, Any], contract: Mapping[str, Any]) -> dict[str, Any]:
    predecessor = set(scenario["capabilities"]["predecessor"])
    required = set(scenario["capabilities"]["successor_required"])
    missing = sorted(required - predecessor)
    affected = sorted(
        {
            operation
            for capability in missing
            for operation in contract["capabilities"][capability]
        }
    )
    return {
        "affected_operations": affected,
        "missing_capabilities": missing,
        "outcome": "migration-required" if missing else "compatible",
    }
