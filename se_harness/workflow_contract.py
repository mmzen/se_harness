"""Strict loaders and indexes for executable workflow policy."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping


WORKFLOW_SCHEMA = "se-harness-workflow-v4"
QUALITY_GATES_SCHEMA = "se-harness-quality-gates-v2"
RETIRED_QUALITY_GATES_SCHEMAS = frozenset({"se-harness-quality-gates-v1"})
#: Graph-structural transition checks (SPEC-ECP-005 Terms): properties of the
#: artifact graph shape alone, kept in Python and reported as predicates.
STRUCTURAL_CHECKS = frozenset({
    "QGS-EDGE",
    "QGS-ASSURANCE",
    "QGS-VREC-COVERAGE",
    "QGS-RLS-COVERAGE",
    "QGS-VERIFIED-INCLUSION",
    "QGS-SUCCESSOR",
})
BINDING_FIELDS = frozenset({"family", "target", "artifact_types", "predicates", "structural"})
STEP_KINDS = {"command", "decision", "reference"}
CORRECTIVE_KINDS = {"command", "escalation", "response"}
PARAMETER_CARDINALITIES = {"one", "zero_or_one", "one_or_more"}
PARAMETER_TYPES = {"artifact_id", "actor", "path", "path_list", "status", "text"}
CHECKPOINTS = {"start", "pre-action", "transition", "handoff", "scope"}
#: The prose a rule contributes to a schema-2 result (WO-ECP-005): what the
#: operation did and the lifecycle state it leaves. Every other restitution
#: field is derived from the bound procedure step.
RULE_RESTITUTION_FIELDS = frozenset({"done", "current_lifecycle_state"})
EVALUATORS = {
    "artifact_status",
    "authoring_ready",
    "release_unit_ready",
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
DEFINITION_TYPES = frozenset({
    "intent",
    "capability",
    "requirement",
    "specification",
    "architecture",
    "adr",
    "verification",
    "release_contract",
    "operating_contract",
})
LIFECYCLE_FAMILIES = frozenset(
    {"definition", "work_order", "verification_record", "release_record"}
)
LIFECYCLE_FIELDS = frozenset(
    {
        "transitions_to",
        "grants_authority",
        "reserves_version",
        "transitionable",
        "must_remain_visible",
        "predecessor_adapter",
    }
)
PREDECESSOR_ADAPTER_VALUES = frozenset({"none", "required"})
_STATE_NAME = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
AGENTIC_OPERATION_FIELDS = frozenset(
    {
        "id",
        "decision_right",
        "current_status",
        "result_status",
        "gate_ids",
        "procedure_id",
        "mutation_operation",
    }
)
#: The three delegated operations of the delegation class (SPEC-ECP-006 ECP-DLG-002);
#: the JSON key keeps its schema-v4 name `agentic_operations`.
DELEGATED_OPERATIONS = (
    ("delegated-work-order-start", "DR-WO-START", "approved", "in_progress", ("QG-G3-WORK-AUTHORIZATION",), "PROC-WO-START"),
    ("delegated-work-order-complete", "DR-WO-COMPLETE", "in_progress", "implemented", ("QG-G4-IMPLEMENTATION-EVIDENCE",), "PROC-WO-IMPLEMENT"),
    ("delegated-vrec-prepare", "DR-VREC-PREPARE", "implemented", "implemented", ("QG-G4-CANDIDATE-READY",), "PROC-WO-PREPARE-VREC"),
)


class ContractError(RuntimeError):
    """Machine policy is malformed, ambiguous, or cannot resolve."""


@dataclass(frozen=True)
class LifecycleState:
    """Validated semantics for one state in one artifact family."""

    transitions_to: tuple[str, ...]
    grants_authority: bool
    reserves_version: bool
    transitionable: bool
    must_remain_visible: bool
    predecessor_adapter: str


LifecycleRegistry = Mapping[str, Mapping[str, LifecycleState]]


def validate_lifecycle_registry(workflow: Mapping[str, Any]) -> LifecycleRegistry:
    """Return the strict, immutable lifecycle index from workflow policy."""

    raw = workflow.get("lifecycles")
    if not isinstance(raw, Mapping) or set(raw) != LIFECYCLE_FAMILIES:
        raise ContractError("workflow lifecycles must declare exactly the four artifact families")
    families: dict[str, Mapping[str, LifecycleState]] = {}
    for family in sorted(LIFECYCLE_FAMILIES):
        raw_states = raw.get(family)
        if not isinstance(raw_states, Mapping) or not raw_states:
            raise ContractError(f"workflow lifecycle family {family} must contain states")
        states: dict[str, LifecycleState] = {}
        for state, raw_row in raw_states.items():
            if not isinstance(state, str) or _STATE_NAME.fullmatch(state) is None:
                raise ContractError(f"workflow lifecycle family {family} has invalid state {state!r}")
            if not isinstance(raw_row, Mapping) or set(raw_row) != LIFECYCLE_FIELDS:
                raise ContractError(f"workflow lifecycle {family}:{state} has invalid fields")
            targets = raw_row.get("transitions_to")
            if (
                not isinstance(targets, list)
                or not all(isinstance(target, str) and _STATE_NAME.fullmatch(target) for target in targets)
                or len(targets) != len(set(targets))
            ):
                raise ContractError(f"workflow lifecycle {family}:{state} has invalid transitions_to")
            boolean_fields = (
                "grants_authority",
                "reserves_version",
                "transitionable",
                "must_remain_visible",
            )
            if any(type(raw_row.get(field)) is not bool for field in boolean_fields):
                raise ContractError(f"workflow lifecycle {family}:{state} has a non-boolean property")
            adapter = raw_row.get("predecessor_adapter")
            if adapter not in PREDECESSOR_ADAPTER_VALUES:
                raise ContractError(f"workflow lifecycle {family}:{state} has invalid predecessor_adapter")
            if raw_row["transitionable"] != bool(targets):
                raise ContractError(
                    f"workflow lifecycle {family}:{state} transitionable disagrees with transitions_to"
                )
            if not raw_row["must_remain_visible"]:
                raise ContractError(f"workflow lifecycle {family}:{state} must remain visible")
            if family != "release_record" and raw_row["reserves_version"]:
                raise ContractError(f"workflow lifecycle {family}:{state} cannot reserve a release version")
            states[state] = LifecycleState(
                transitions_to=tuple(targets),
                grants_authority=raw_row["grants_authority"],
                reserves_version=raw_row["reserves_version"],
                transitionable=raw_row["transitionable"],
                must_remain_visible=raw_row["must_remain_visible"],
                predecessor_adapter=adapter,
            )
        for state, row in states.items():
            unknown = set(row.transitions_to) - set(states)
            if unknown:
                raise ContractError(
                    f"workflow lifecycle {family}:{state} targets unknown state {sorted(unknown)[0]}"
                )
        families[family] = MappingProxyType(states)
    return MappingProxyType(families)


def load_lifecycle_registry(path: Path | None = None) -> LifecycleRegistry:
    """Load and validate the canonical lifecycle registry."""

    return validate_lifecycle_registry(load_workflow_contract(path))


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
    target = path or Path(__file__).with_name("quality_gates_contract.json")
    try:
        return _load(target, QUALITY_GATES_SCHEMA)
    except ContractError as exc:
        try:
            observed = json.loads(target.read_bytes().decode("utf-8")).get("schema")
        except Exception:  # noqa: BLE001 - the original error is the one to report
            raise exc from None
        if observed in RETIRED_QUALITY_GATES_SCHEMAS:
            raise ContractError(
                f"WEX-ECP-030: {target} uses retired schema {observed}; the transition bindings of "
                f"{QUALITY_GATES_SCHEMA} are required, upgrade the installed contract"
            ) from exc
        raise


def effective_checkpoints(gate: Mapping[str, Any], predicate: Mapping[str, Any]) -> frozenset[str]:
    """A predicate's own `checkpoints` when declared, else its gate's (ECP-KRN-009)."""

    declared = predicate.get("checkpoints")
    if declared is None:
        return frozenset(str(item) for item in gate.get("checkpoints", ()))
    return frozenset(str(item) for item in declared)


def transition_binding(
    quality_gates: Mapping[str, Any], family: str, artifact_type: str, target: str
) -> tuple[list[str], list[str]]:
    """Return (predicate ids, structural check ids) bound to one lifecycle edge."""

    for binding in quality_gates.get("transition_bindings", []):
        if binding.get("family") != family or binding.get("target") != target:
            continue
        types = binding.get("artifact_types")
        if types is not None and artifact_type not in types:
            continue
        return [str(item) for item in binding.get("predicates", [])], [str(item) for item in binding.get("structural", [])]
    raise ContractError(f"WEX-ECP-030: no transition binding for {family}:{artifact_type} -> {target}")


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


def _validate_corrective(
    step: Mapping[str, Any],
    gate_predicates: Mapping[str, list[str]],
    parameters: set[str],
    label: str,
) -> None:
    """Require one distinct corrective form per predicate of a gated command step (ADS-RST-001)."""

    expected = [
        predicate_id
        for gate_id in step.get("gate_ids", [])
        for predicate_id in gate_predicates.get(gate_id, [])
    ]
    corrective = step.get("corrective")
    if not expected:
        if corrective is not None:
            raise ContractError(f"WEX-ADS-001: {label} declares corrective forms without gates")
        return
    if not isinstance(corrective, Mapping):
        raise ContractError(f"WEX-ADS-001: {label} has no corrective forms for its gate predicates")
    if set(corrective) != set(expected):
        missing = sorted(set(expected) - set(corrective))
        extra = sorted(set(corrective) - set(expected))
        raise ContractError(
            f"WEX-ADS-001: {label} corrective forms do not cover its predicates "
            f"(missing {missing}, extra {extra})"
        )
    for predicate_id, form in corrective.items():
        if not isinstance(form, Mapping) or form.get("kind") not in CORRECTIVE_KINDS:
            raise ContractError(f"WEX-ADS-001: {label} corrective for {predicate_id} has an unknown kind")
        kind = form["kind"]
        if kind == "command":
            argv = form.get("argv")
            if set(form) != {"kind", "argv"} or not isinstance(argv, list) or not argv or not all(isinstance(item, str) for item in argv):
                raise ContractError(f"WEX-ADS-001: {label} corrective command for {predicate_id} requires argv")
            _validate_placeholders(argv, parameters, f"{label} corrective {predicate_id}")
            if argv == step.get("argv"):
                raise ContractError(f"WEX-ADS-001: {label} corrective for {predicate_id} repeats the evaluated command")
        elif kind == "escalation":
            right = form.get("decision_right")
            if set(form) != {"kind", "decision_right"} or not isinstance(right, str) or not right.startswith("DR-"):
                raise ContractError(f"WEX-ADS-001: {label} corrective escalation for {predicate_id} needs a decision right")
        else:
            value = form.get("value")
            if set(form) != {"kind", "value"} or not isinstance(value, str) or not value.strip():
                raise ContractError(f"WEX-ADS-001: {label} corrective response for {predicate_id} needs text")
            _validate_placeholders(value, parameters, f"{label} corrective {predicate_id}")


def _validate_procedures(
    workflow: Mapping[str, Any],
    gate_ids: set[str],
    gate_predicates: Mapping[str, list[str]] | None = None,
) -> dict[str, Mapping[str, Any]]:
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
                allowed = common | {"argv", "corrective"}
                argv = step.get("argv")
                if not isinstance(argv, list) or not argv or not all(isinstance(item, str) for item in argv):
                    raise ContractError(f"procedure {procedure_id} command {step_id} requires argv")
                _validate_placeholders(argv, parameters, f"procedure {procedure_id} command {step_id}")
                _validate_corrective(
                    step, gate_predicates or {}, parameters, f"procedure {procedure_id} command {step_id}"
                )
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
            if not set(step).issubset(allowed) or not common.issubset(step) or (kind == "command" and "argv" not in step):
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


def _validate_transition_bindings(
    workflow: Mapping[str, Any],
    quality_gates: Mapping[str, Any],
    gates: Mapping[str, Mapping[str, Any]],
    predicates: Mapping[str, Mapping[str, Any]],
) -> None:
    """Every lifecycle edge is bound to transition predicates or structural checks (ECP-KRN-009)."""

    raw = quality_gates.get("transition_bindings")
    if not isinstance(raw, list) or not raw:
        raise ContractError("WEX-ECP-030: quality-gate contract declares no transition bindings")
    owner: dict[str, str] = {}
    for gate_id, gate in gates.items():
        for predicate in gate["predicates"]:
            owner[str(predicate["id"])] = gate_id
    seen: set[tuple[str, str, str | None]] = set()
    bound: dict[tuple[str, str], set[str] | None] = {}
    for binding in raw:
        if not isinstance(binding, Mapping) or not {"family", "target", "predicates", "structural"}.issubset(binding) or not set(binding).issubset(BINDING_FIELDS):
            raise ContractError("WEX-ECP-030: transition binding has invalid fields")
        family = binding["family"]
        target = binding["target"]
        if family not in LIFECYCLE_FAMILIES or not isinstance(target, str) or _STATE_NAME.fullmatch(target) is None:
            raise ContractError(f"WEX-ECP-030: transition binding names unknown family or state {family}:{target}")
        types = binding.get("artifact_types")
        if types is not None:
            types = _strings(types, f"transition binding {family}:{target} artifact_types")
            if family != "definition" or not set(types).issubset(DEFINITION_TYPES):
                raise ContractError(f"WEX-ECP-030: transition binding {family}:{target} restricts artifact types it cannot")
        for predicate_id in _strings(binding["predicates"], f"transition binding {family}:{target} predicates"):
            gate_id = owner.get(predicate_id)
            if gate_id is None:
                raise ContractError(f"WEX-ECP-030: transition binding {family}:{target} names unknown predicate {predicate_id}")
            if "transition" not in effective_checkpoints(gates[gate_id], predicates[predicate_id]):
                raise ContractError(f"WEX-ECP-030: predicate {predicate_id} is bound to transition but does not declare that checkpoint")
        for structural in _strings(binding["structural"], f"transition binding {family}:{target} structural"):
            if structural not in STRUCTURAL_CHECKS:
                raise ContractError(f"WEX-ECP-030: transition binding {family}:{target} names unknown structural check {structural}")
        key = (family, target, None if types is None else ",".join(sorted(types)))
        if key in seen:
            raise ContractError(f"WEX-ECP-030: duplicate transition binding {family}:{target}")
        seen.add(key)
        covered = bound.setdefault((family, target), set())
        if types is None:
            bound[(family, target)] = None
        elif covered is not None:
            covered.update(types)
    registry = validate_lifecycle_registry(workflow)
    for family, states in registry.items():
        for source, row in states.items():
            for target in row.transitions_to:
                covered = bound.get((family, target), set())
                if covered is None:
                    continue
                if family != "definition" or not covered or not DEFINITION_TYPES.issubset(covered):
                    raise ContractError(
                        f"WEX-ECP-030: lifecycle edge {family}:{source} -> {target} has no transition binding"
                    )


def validate_contracts(
    workflow: Mapping[str, Any],
    quality_gates: Mapping[str, Any],
) -> tuple[dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    allowed_workflow = {
        "schema", "normative_language", "restitution_fields", "agentic_operations", "lifecycles", "failure", "recommendations", "procedures"
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
    validate_lifecycle_registry(workflow)
    if set(quality_gates) != {"schema", "aggregation", "gates", "transition_bindings"}:
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
            allowed = {"id", "evaluator", "required_evidence", "statuses", "checkpoints"}
            if not set(predicate).issubset(allowed) or not {"id", "evaluator", "required_evidence"}.issubset(predicate):
                raise ContractError(f"predicate {predicate_id} has invalid fields")
            if "checkpoints" in predicate:
                own = set(_strings(predicate["checkpoints"], f"predicate {predicate_id} checkpoints"))
                if not own or not own.issubset(checkpoints):
                    raise ContractError(f"predicate {predicate_id} declares checkpoints outside its gate")
            if predicate.get("evaluator") not in EVALUATORS:
                raise ContractError(f"predicate {predicate_id} has unknown evaluator")
            evidence = predicate.get("required_evidence")
            if not isinstance(evidence, list) or not evidence or not all(isinstance(item, Mapping) and item for item in evidence):
                raise ContractError(f"predicate {predicate_id} requires evidence descriptors")
            if "statuses" in predicate:
                _strings(predicate["statuses"], f"predicate {predicate_id} statuses")
            predicates[predicate_id] = predicate
    gate_predicates = {
        gate_id: [str(item["id"]) for item in gate["predicates"]] for gate_id, gate in gates.items()
    }
    _validate_transition_bindings(workflow, quality_gates, gates, predicates)
    procedures = _validate_procedures(workflow, set(gates), gate_predicates)
    raw_operations = workflow.get("agentic_operations")
    if not isinstance(raw_operations, list) or len(raw_operations) != len(DELEGATED_OPERATIONS):
        raise ContractError("workflow must declare exactly the three delegated operations")
    expected_operations = [item[0] for item in DELEGATED_OPERATIONS]
    if [item.get("id") for item in raw_operations if isinstance(item, Mapping)] != expected_operations:
        raise ContractError("workflow delegated operation order or identity is invalid")
    for raw, expected in zip(raw_operations, DELEGATED_OPERATIONS, strict=True):
        if not isinstance(raw, Mapping) or set(raw) != AGENTIC_OPERATION_FIELDS:
            raise ContractError("workflow delegated operation has invalid fields")
        operation, right, current, result, gate_ids, procedure_id = expected
        observed_gate_ids = tuple(
            _strings(raw.get("gate_ids"), f"agentic operation {operation} gate_ids")
        )
        if (
            raw.get("id") != operation
            or raw.get("decision_right") != right
            or raw.get("current_status") != current
            or raw.get("result_status") != result
            or observed_gate_ids != gate_ids
            or raw.get("procedure_id") != procedure_id
            or raw.get("mutation_operation") != operation
        ):
            raise ContractError(f"workflow delegated operation mapping is invalid: {operation}")
        if raw.get("procedure_id") not in procedures:
            raise ContractError(f"workflow delegated operation references unknown procedure: {operation}")
        unknown_gates = set(observed_gate_ids) - set(gates)
        if unknown_gates:
            raise ContractError(f"workflow Phase 4 operation references unknown gate {sorted(unknown_gates)[0]}")
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
        restitution = rule.get("restitution")
        if not isinstance(restitution, Mapping) or set(restitution) != RULE_RESTITUTION_FIELDS:
            raise ContractError(f"workflow rule {rule_id} must declare restitution done and current_lifecycle_state")
        for field in RULE_RESTITUTION_FIELDS:
            _strings(restitution.get(field), f"workflow rule {rule_id} restitution {field}")
    return rules, procedures, gates


def load_validated_contracts() -> tuple[dict[str, Any], dict[str, Any], dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    workflow = load_workflow_contract()
    quality = load_quality_gate_contract()
    rules, procedures, gates = validate_contracts(workflow, quality)
    return workflow, quality, rules, procedures, gates


OPERATING_CARD_LIMIT = 1024
OPERATING_CARD_PATH = "docs/engineering/OPERATING_CARD.md"
_CARD_STOP_CONDITIONS = (
    "managed integrity fails",
    "the formal graph is invalid",
    "no phase-eligible selected work order exists",
    "a required governing artifact or gate is missing",
    "a required check fails",
    "owner instructions conflict with the managed contract",
    "remediation would exceed the selected work order",
    "the action lacks its decision right or explicit authority",
)
_CARD_TRAPS = (
    "A PR body needs one standalone `Harness-Work-Order: WO-...` line with LF endings; CI reads the stored event.",
    "A VREC or RLS binds an earlier commit; it lives in a later governance commit and is never rewritten.",
    "Artifact IDs are shared across branches and sessions; check every ref before numbering.",
    "A `ready` VREC whose candidate leaves `HEAD` (rebase, merge below it) is orphaned; verify, reject, or succeed it.",
)


def render_operating_card(
    workflow: Mapping[str, Any] | None = None,
    quality_gates: Mapping[str, Any] | None = None,
) -> bytes:
    """Render the managed operating card from the machine contracts (ADS-RDM-002).

    The card is derived content: every line restates a contract value or a
    router rule. It is bounded to OPERATING_CARD_LIMIT bytes.
    """

    workflow = load_workflow_contract() if workflow is None else workflow
    quality_gates = load_quality_gate_contract() if quality_gates is None else quality_gates
    validate_contracts(workflow, quality_gates)
    lines = [
        "# Operating card",
        "",
        "Derived from `WORKFLOW.json` and `QUALITY_GATES.json`; `harnessctl` alone computes",
        "legality and the next step.",
        "",
        "## Stop when",
        "",
    ]
    lines.extend(f"- {item};" for item in _CARD_STOP_CONDITIONS)
    lines.extend(["", "Then report the failing rule, the unchanged state, and the corrective step.", "", "## Traps", ""])
    lines.extend(f"- {item}" for item in _CARD_TRAPS)
    lines.append("")
    rendered = "\n".join(lines).encode("utf-8")
    if len(rendered) > OPERATING_CARD_LIMIT:
        raise ContractError(f"WEX-ADS-003: operating card is {len(rendered)} bytes; limit is {OPERATING_CARD_LIMIT}")
    return rendered


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
