"""Strict loaders and indexes for executable workflow policy."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable, Mapping


WORKFLOW_SCHEMA = "se-harness-workflow-v2"
QUALITY_GATES_SCHEMA = "se-harness-quality-gates-v1"
STEP_KINDS = {"command", "decision", "reference"}
PARAMETER_CARDINALITIES = {"one", "zero_or_one", "one_or_more"}
PARAMETER_TYPES = {"artifact_id", "actor", "path", "path_list", "status", "text"}
CHECKPOINTS = {"start", "pre-action", "transition", "handoff"}
EVALUATORS = {
    "artifact_status",
    "change_set_complete",
    "changed_paths_within_scope",
    "execution_scope_declared",
    "formal_graph_valid",
    "repository_integrity",
    "review_evidence_available",
    "review_preflight_ready",
    "start_preflight_ready",
}
_PLACEHOLDER = re.compile(r"\{([a-z][a-z0-9_]*)\}")
_ID_PATTERNS = {
    "workflow": re.compile(r"^WFL-[A-Z0-9-]+$"),
    "procedure": re.compile(r"^PROC-[A-Z0-9-]+$"),
    "step": re.compile(r"^STEP-[A-Z0-9-]+$"),
    "gate": re.compile(r"^QG-[A-Z0-9-]+$"),
    "predicate": re.compile(r"^QGP-[A-Z0-9-]+$"),
}


class ContractError(RuntimeError):
    """Machine policy is malformed, ambiguous, or cannot resolve."""


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load(path: Path, schema: str) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
        if len(raw) > 2_000_000:
            raise ContractError(f"machine policy exceeds 2 MB: {path}")
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_object)
    except ContractError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ContractError(f"cannot load machine policy {path}: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema") != schema:
        raise ContractError(f"{path} must use schema {schema}")
    return value


def load_workflow_contract(path: Path | None = None) -> dict[str, Any]:
    return _load(path or Path(__file__).with_name("workflow_contract.json"), WORKFLOW_SCHEMA)


def load_quality_gate_contract(path: Path | None = None) -> dict[str, Any]:
    return _load(path or Path(__file__).with_name("quality_gates_contract.json"), QUALITY_GATES_SCHEMA)


def _identifier(kind: str, value: object) -> str:
    if not isinstance(value, str) or _ID_PATTERNS[kind].fullmatch(value) is None:
        raise ContractError(f"invalid {kind} ID: {value!r}")
    return value


def _unique(items: Iterable[Mapping[str, Any]], kind: str) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    folded: dict[str, str] = {}
    for item in items:
        if not isinstance(item, Mapping):
            raise ContractError(f"{kind} registry entries must be objects")
        identifier = _identifier(kind, item.get("id"))
        key = identifier.casefold()
        if identifier in result or key in folded:
            raise ContractError(f"duplicate or case-ambiguous {kind} ID: {identifier}")
        result[identifier] = item
        folded[key] = identifier
    return result


def _strings(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ContractError(f"{label} must be an array of strings")
    return value


def _validate_parameters(procedure: Mapping[str, Any]) -> set[str]:
    parameters = procedure.get("parameters")
    if not isinstance(parameters, list):
        raise ContractError(f"procedure {procedure.get('id')} parameters must be an array")
    names: set[str] = set()
    for parameter in parameters:
        if not isinstance(parameter, Mapping) or set(parameter) != {"name", "type", "cardinality", "source"}:
            raise ContractError(f"procedure {procedure.get('id')} has an invalid parameter")
        name = parameter.get("name")
        if not isinstance(name, str) or re.fullmatch(r"[a-z][a-z0-9_]*", name) is None or name in names:
            raise ContractError(f"procedure {procedure.get('id')} has a duplicate or invalid parameter")
        if parameter.get("type") not in PARAMETER_TYPES:
            raise ContractError(f"procedure {procedure.get('id')} parameter {name} has an unknown type")
        if parameter.get("cardinality") not in PARAMETER_CARDINALITIES:
            raise ContractError(f"procedure {procedure.get('id')} parameter {name} has an unknown cardinality")
        if not isinstance(parameter.get("source"), str) or not parameter["source"]:
            raise ContractError(f"procedure {procedure.get('id')} parameter {name} has no source")
        names.add(name)
    return names


def _validate_placeholders(value: object, parameters: set[str], label: str) -> None:
    if isinstance(value, str):
        unknown = set(_PLACEHOLDER.findall(value)) - parameters
        if unknown:
            raise ContractError(f"{label} has unknown placeholder(s): {', '.join(sorted(unknown))}")
    elif isinstance(value, list):
        for item in value:
            _validate_placeholders(item, parameters, label)


def _validate_procedures(workflow: Mapping[str, Any], gate_ids: set[str]) -> dict[str, Mapping[str, Any]]:
    raw = workflow.get("procedures")
    if not isinstance(raw, list):
        raise ContractError("workflow procedures must be an array")
    procedures = _unique(raw, "procedure")
    references: dict[str, list[str]] = {identifier: [] for identifier in procedures}
    for procedure_id, procedure in procedures.items():
        parameters = _validate_parameters(procedure)
        steps = procedure.get("steps")
        if not isinstance(steps, list) or not steps or len(steps) > 64:
            raise ContractError(f"procedure {procedure_id} must contain 1 to 64 steps")
        step_ids: set[str] = set()
        for step in steps:
            if not isinstance(step, Mapping):
                raise ContractError(f"procedure {procedure_id} step must be an object")
            step_id = _identifier("step", step.get("id"))
            if step_id in step_ids:
                raise ContractError(f"procedure {procedure_id} has duplicate step {step_id}")
            step_ids.add(step_id)
            kind = step.get("kind")
            if kind not in STEP_KINDS:
                raise ContractError(f"procedure {procedure_id} step {step_id} has unknown kind")
            common = {"id", "kind", "gate_ids", "effects", "non_effects"}
            if kind == "command":
                allowed = common | {"argv"}
                argv = step.get("argv")
                if not isinstance(argv, list) or not argv or not all(isinstance(item, str) for item in argv):
                    raise ContractError(f"procedure {procedure_id} command {step_id} requires argv")
                _validate_placeholders(argv, parameters, f"procedure {procedure_id} command {step_id}")
            elif kind == "decision":
                allowed = common | {"decision_right", "role", "artifact", "outcomes", "response", "decision"}
                if not isinstance(step.get("decision_right"), str) or not str(step["decision_right"]).startswith("DR-"):
                    raise ContractError(f"procedure {procedure_id} decision {step_id} has no decision right")
                if not isinstance(step.get("role"), str) or not step["role"]:
                    raise ContractError(f"procedure {procedure_id} decision {step_id} has no role")
                outcomes = _strings(step.get("outcomes"), f"procedure {procedure_id} decision outcomes")
                if not outcomes:
                    raise ContractError(f"procedure {procedure_id} decision {step_id} has no outcomes")
                _validate_placeholders(step.get("artifact"), parameters, f"procedure {procedure_id} decision {step_id}")
                _validate_placeholders(step.get("response"), parameters, f"procedure {procedure_id} decision {step_id}")
            else:
                if "action_id" in step:
                    raise ContractError(
                        f"procedure {procedure_id} reference {step_id} declares action_id, "
                        "a withdrawn reference form; a reference step declares procedure_id only"
                    )
                target = step.get("procedure_id")
                if not isinstance(target, str):
                    raise ContractError(f"procedure {procedure_id} reference {step_id} must declare a procedure ID")
                allowed = common | {"procedure_id"}
                references[procedure_id].append(target)
            if set(step) != allowed:
                raise ContractError(f"procedure {procedure_id} step {step_id} has invalid fields")
            for field in ("gate_ids", "effects", "non_effects"):
                values = _strings(step.get(field), f"procedure {procedure_id} step {step_id} {field}")
                if field == "gate_ids":
                    unknown = set(values) - gate_ids
                    if unknown:
                        raise ContractError(f"procedure {procedure_id} step {step_id} references unknown gate {sorted(unknown)[0]}")
                else:
                    _validate_placeholders(values, parameters, f"procedure {procedure_id} step {step_id} {field}")
    for source, targets in references.items():
        for target in targets:
            if target not in procedures:
                raise ContractError(f"procedure {source} references unknown procedure {target}")

    def visit(identifier: str, stack: tuple[str, ...]) -> None:
        if identifier in stack:
            raise ContractError("procedure reference cycle: " + " -> ".join((*stack, identifier)))
        if len(stack) >= 8:
            raise ContractError(f"procedure reference depth exceeds 8 at {identifier}")
        for target in references[identifier]:
            visit(target, (*stack, identifier))

    for procedure_id in procedures:
        visit(procedure_id, ())
    return procedures


def validate_contracts(
    workflow: Mapping[str, Any],
    quality_gates: Mapping[str, Any],
) -> tuple[dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    allowed_workflow = {
        "schema", "normative_language", "handoff_fields", "restitution_fields", "transitions", "failure", "recommendations", "procedures"
    }
    if set(workflow) != allowed_workflow:
        raise ContractError("workflow contract contains unknown or missing top-level fields")
    if workflow.get("restitution_fields") != [
        "outcome",
        "done",
        "not_done",
        "blocked_by",
        "current_lifecycle_state",
        "decision_required",
        "next",
        "command_or_response",
        "alternatives",
    ]:
        raise ContractError("workflow restitution fields are not canonical")
    if set(quality_gates) != {"schema", "aggregation", "gates"}:
        raise ContractError("quality-gate contract contains unknown or missing top-level fields")
    if quality_gates.get("aggregation") != ["fail", "not_assessable", "pass"]:
        raise ContractError("quality-gate aggregation must be fail > not_assessable > pass")
    gates_raw = quality_gates.get("gates")
    if not isinstance(gates_raw, list):
        raise ContractError("quality gates must be an array")
    gates = _unique(gates_raw, "gate")
    predicates: dict[str, Mapping[str, Any]] = {}
    for gate_id, gate in gates.items():
        if set(gate) != {"id", "checkpoints", "predicates"}:
            raise ContractError(f"gate {gate_id} has invalid fields")
        checkpoints = set(_strings(gate.get("checkpoints"), f"gate {gate_id} checkpoints"))
        if not checkpoints or not checkpoints.issubset(CHECKPOINTS):
            raise ContractError(f"gate {gate_id} has invalid checkpoints")
        raw_predicates = gate.get("predicates")
        if not isinstance(raw_predicates, list) or not raw_predicates:
            raise ContractError(f"gate {gate_id} has no predicates")
        local = _unique(raw_predicates, "predicate")
        for predicate_id, predicate in local.items():
            if predicate_id in predicates:
                raise ContractError(f"duplicate predicate ID: {predicate_id}")
            allowed = {"id", "evaluator", "required_evidence", "statuses"}
            if not set(predicate).issubset(allowed) or not {"id", "evaluator", "required_evidence"}.issubset(predicate):
                raise ContractError(f"predicate {predicate_id} has invalid fields")
            if predicate.get("evaluator") not in EVALUATORS:
                raise ContractError(f"predicate {predicate_id} has unknown evaluator")
            evidence = predicate.get("required_evidence")
            if not isinstance(evidence, list) or not evidence or not all(isinstance(item, Mapping) and item for item in evidence):
                raise ContractError(f"predicate {predicate_id} requires evidence descriptors")
            if "statuses" in predicate:
                _strings(predicate["statuses"], f"predicate {predicate_id} statuses")
            predicates[predicate_id] = predicate
    procedures = _validate_procedures(workflow, set(gates))
    rules_raw = workflow.get("recommendations")
    if not isinstance(rules_raw, list) or not rules_raw:
        raise ContractError("workflow recommendations must be a non-empty array")
    rules = _unique(rules_raw, "workflow")
    if list(rules)[-1] != "WFL-DEFAULT-REVIEW":
        raise ContractError("WFL-DEFAULT-REVIEW must be the final workflow rule")
    for rule_id, rule in [*rules.items(), (str(workflow.get("failure", {}).get("id")), workflow.get("failure", {}))]:
        if not isinstance(rule, Mapping):
            raise ContractError(f"workflow rule {rule_id} must be an object")
        procedure_id = rule.get("procedure_id")
        if procedure_id not in procedures:
            raise ContractError(f"workflow rule {rule_id} references unknown procedure {procedure_id}")
        unknown_gates = set(_strings(rule.get("gate_ids"), f"workflow rule {rule_id} gate_ids")) - set(gates)
        if unknown_gates:
            raise ContractError(f"workflow rule {rule_id} references unknown gate {sorted(unknown_gates)[0]}")
        alternatives = rule.get("alternative_procedure_ids", [])
        unknown_procedures = set(_strings(alternatives, f"workflow rule {rule_id} alternatives")) - set(procedures)
        if unknown_procedures:
            raise ContractError(f"workflow rule {rule_id} references unknown alternative {sorted(unknown_procedures)[0]}")
    return rules, procedures, gates


def load_validated_contracts() -> tuple[dict[str, Any], dict[str, Any], dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    workflow = load_workflow_contract()
    quality = load_quality_gate_contract()
    rules, procedures, gates = validate_contracts(workflow, quality)
    return workflow, quality, rules, procedures, gates


def contract_match(value: str, accepted: object) -> bool:
    return isinstance(accepted, list) and ("*" in accepted or value in accepted)


def select_rule(
    rules: Mapping[str, Mapping[str, Any]],
    primary: Any,
    *,
    related: Iterable[Any] = (),
    target: str | None = None,
) -> tuple[Mapping[str, Any], dict[str, str]]:
    status = target or primary.status
    context = {
        "artifact_id": primary.artifact_id,
        "status": status,
        "successor_id": "the declared successor",
    }
    successors = primary.relations.get("superseded_by", [])
    if isinstance(successors, list) and successors:
        context["successor_id"] = str(sorted(str(item) for item in successors)[0])
    related_items = sorted(related, key=lambda item: item.artifact_id)
    for rule in rules.values():
        selector = rule.get("selector")
        if not isinstance(selector, Mapping):
            raise ContractError(f"workflow rule {rule.get('id')} has an invalid selector")
        if not contract_match(primary.artifact_type, selector.get("artifact_types")):
            continue
        if not contract_match(status, selector.get("statuses")):
            continue
        related_type = selector.get("related_artifact_type")
        if related_type is not None:
            candidates = [
                item for item in related_items
                if item.artifact_type == related_type
                and contract_match(item.status, selector.get("related_statuses"))
            ]
            if not candidates:
                continue
            context["related_id"] = candidates[0].artifact_id
            context["related_status"] = candidates[0].status
        return rule, context
    raise ContractError(f"no workflow rule for {primary.artifact_type}:{status}")
