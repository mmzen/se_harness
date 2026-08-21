"""Stateless selected-scope workflow checkpoint evaluation."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Mapping

from se_harness.installer import HarnessError, ensure_target, safe_destination
from se_harness.preflight import run_preflight
from se_harness.workflow_contract import (
    ContractError,
    load_validated_contracts,
    select_rule,
)
from se_harness.workflow_procedures import (
    ProcedureError,
    command_or_response,
    decision_required,
    resolve_procedure,
    select_current_step,
)
from se_harness.workflow_result import build_result


CHANGE_SET_SCHEMA = "se-harness-change-set-v1"
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}
_REPOSITORY_ERROR_CODES = {"E001", "E003"}


@dataclass(frozen=True)
class ChangeSet:
    paths: tuple[str, ...]
    complete: bool
    source: str


@dataclass
class CheckpointContext:
    root: Path
    artifact: Any
    report: Any
    catalog: Mapping[str, Any]
    scoped_errors: list[dict[str, Any]]
    repository_errors: list[dict[str, Any]]
    unrelated_count: int
    declared_scope: tuple[str, ...]
    change_set: ChangeSet
    checkpoint: str
    formal_snapshot_sha256: str


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise HarnessError(f"WEX200: duplicate JSON key in change manifest: {key}")
        result[key] = value
    return result


def normalize_path(value: object, *, directory_allowed: bool = False) -> str:
    if not isinstance(value, str) or not value or len(value) > 4096:
        raise HarnessError("WEX200: path must be non-empty UTF-8 text of at most 4096 characters")
    if _CONTROL.search(value) or "\\" in value or ":" in value or any(token in value for token in ("*", "?", "[", "]")):
        raise HarnessError(f"WEX200: path is not a normalized repository path: {value!r}")
    directory = value.endswith("/")
    if directory and not directory_allowed:
        raise HarnessError(f"WEX200: changed path must name a file or component: {value!r}")
    candidate = value[:-1] if directory else value
    if not candidate or candidate.startswith("/") or candidate.startswith("//"):
        raise HarnessError(f"WEX200: absolute or empty path is forbidden: {value!r}")
    parts = PurePosixPath(candidate).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise HarnessError(f"WEX200: dot or empty path component is forbidden: {value!r}")
    for part in parts:
        stem = part.rstrip(". ").split(".", 1)[0].upper()
        if stem in _RESERVED or part.endswith((".", " ")):
            raise HarnessError(f"WEX200: reserved path component is forbidden: {value!r}")
    normalized = PurePosixPath(*parts).as_posix() + ("/" if directory else "")
    if normalized != value:
        raise HarnessError(f"WEX200: path is not normalized: {value!r}")
    return normalized


def _unique_paths(values: Iterable[object], *, directory_allowed: bool) -> tuple[str, ...]:
    result: list[str] = []
    folded: dict[str, str] = {}
    for value in values:
        path = normalize_path(value, directory_allowed=directory_allowed)
        key = path.casefold()
        if key in folded:
            raise HarnessError(f"WEX200: duplicate or case-ambiguous path: {path!r}")
        folded[key] = path
        result.append(path)
    return tuple(result)


def parse_change_manifest(root: Path, manifest: Path) -> ChangeSet:
    raw = manifest.as_posix()
    if manifest.is_absolute():
        try:
            candidate = manifest.resolve(strict=True)
            candidate.relative_to(root)
        except (OSError, ValueError) as exc:
            raise HarnessError("WEX200: change manifest must remain inside the repository") from exc
    else:
        normalized = normalize_path(raw)
        candidate = safe_destination(root, Path(normalized))
        try:
            candidate = candidate.resolve(strict=True)
            candidate.relative_to(root)
        except (OSError, ValueError) as exc:
            raise HarnessError("WEX200: change manifest cannot resolve safely") from exc
    if candidate.is_symlink() or not candidate.is_file():
        raise HarnessError("WEX200: change manifest must be one ordinary file")
    try:
        data = candidate.read_bytes()
        if len(data) > 10_000_000:
            raise HarnessError("WEX200: change manifest exceeds 10 MB")
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs)
    except HarnessError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise HarnessError(f"WEX200: invalid change manifest: {exc}") from exc
    if not isinstance(value, dict) or set(value) != {"schema", "complete", "paths"}:
        raise HarnessError("WEX200: change manifest fields must be schema, complete, and paths")
    if value.get("schema") != CHANGE_SET_SCHEMA or not isinstance(value.get("complete"), bool):
        raise HarnessError("WEX200: change manifest schema or completeness value is invalid")
    if not isinstance(value.get("paths"), list):
        raise HarnessError("WEX200: change manifest paths must be an array")
    return ChangeSet(
        paths=_unique_paths(value["paths"], directory_allowed=False),
        complete=value["complete"],
        source=candidate.relative_to(root).as_posix(),
    )


def declared_change_set(paths: Iterable[str], *, complete: bool) -> ChangeSet:
    return ChangeSet(
        paths=_unique_paths(paths, directory_allowed=False),
        complete=bool(complete),
        source="arguments",
    )


def _validate_changed_targets(root: Path, change_set: ChangeSet) -> None:
    for value in change_set.paths:
        candidate = safe_destination(root, Path(value))
        if not candidate.exists() and not candidate.is_symlink():
            continue
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError) as exc:
            raise HarnessError(f"WEX200: changed path escapes the repository: {value}") from exc


def execution_scope(artifact: Any) -> tuple[str, ...]:
    table = artifact.metadata.get("execution_scope")
    if not isinstance(table, dict) or set(table) != {"paths"} or not isinstance(table.get("paths"), list):
        raise HarnessError(f"WEX200: {artifact.artifact_id} has no valid [execution_scope].paths declaration")
    paths = _unique_paths(table["paths"], directory_allowed=True)
    if not paths:
        raise HarnessError(f"WEX200: {artifact.artifact_id} execution scope is empty")
    return paths


def path_is_admitted(path: str, scope: Iterable[str]) -> bool:
    return any(
        path.startswith(entry) if entry.endswith("/") else path == entry
        for entry in scope
    )


def formal_snapshot_digest(root: Path, artifacts: Iterable[Any]) -> str:
    digest = hashlib.sha256()
    for artifact in sorted(artifacts, key=lambda item: item.path.relative_to(root).as_posix()):
        relative = artifact.path.relative_to(root).as_posix().encode("utf-8")
        content = artifact.path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def _diagnostic(item: Any) -> dict[str, Any]:
    return {"code": item.code, "path": item.path, "message": item.message, "plane": item.plane}


def _classify(report: Any, catalog: Mapping[str, Any], primary: Any, root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    from se_harness.workflow import project_scope

    governing, dependencies = project_scope(catalog, primary)
    scope_paths = {
        catalog[identifier].path.resolve()
        for identifier in governing | dependencies | {primary.artifact_id}
        if identifier in catalog
    }
    scoped: list[dict[str, Any]] = []
    repository: list[dict[str, Any]] = []
    unrelated = 0
    for item in report.errors:
        diagnostic = _diagnostic(item)
        if item.code in _REPOSITORY_ERROR_CODES:
            repository.append(diagnostic)
            continue
        try:
            candidate = safe_destination(root, Path(item.path)).resolve()
        except HarnessError:
            repository.append({**diagnostic, "code": "WEX200"})
            continue
        if candidate in scope_paths:
            scoped.append(diagnostic)
        else:
            unrelated += 1
    for item in report.warnings:
        try:
            selected = safe_destination(root, Path(item.path)).resolve() in scope_paths
        except HarnessError:
            selected = False
        if not selected:
            unrelated += 1
    return scoped, repository, unrelated


def _preflight_status(context: CheckpointContext, phase: str) -> tuple[str, str]:
    if context.artifact.artifact_type != "work_order":
        return "pass", f"{phase} preflight does not apply to {context.artifact.artifact_type}."
    report = run_preflight(context.root, work_order_id=context.artifact.artifact_id, phase=phase)
    lock_files: set[str] = set()
    try:
        lock = json.loads((context.root / ".engineering-harness.lock").read_text(encoding="utf-8"))
        if isinstance(lock, dict) and isinstance(lock.get("files"), dict):
            lock_files = {str(path) for path in lock["files"]}
    except (OSError, UnicodeError, json.JSONDecodeError):
        pass

    def lifecycle_relevant(item: Any) -> bool:
        path = str(item.path)
        if item.code == "I001" and path.startswith("distribution:"):
            return False
        candidate = path.removeprefix("lock-entry:")
        if item.code == "I001" and item.message in {"missing", "required"} and candidate not in lock_files:
            # Candidate templates may add managed paths while the released root
            # installation intentionally remains on its lock-recorded version.
            return False
        return True

    relevant = [item for item in report.diagnostics if lifecycle_relevant(item)]
    if relevant:
        return "fail", relevant[0].message
    return "pass", f"Released-installation {phase} preflight inputs are ready."


def _review_evidence(context: CheckpointContext) -> tuple[str, str]:
    if context.artifact.artifact_type != "work_order":
        return "pass", "Work-order implementation evidence does not apply to this artifact type."
    evidence_root = context.root / "docs" / "engineering"
    candidates = [
        path for path in evidence_root.rglob("*")
        if path.is_file()
        and "evidence" in path.parts
        and any(part.startswith(context.artifact.artifact_id) for part in path.parts[path.parts.index("evidence") + 1 :])
    ]
    binding = f"formal_snapshot_sha256: {context.formal_snapshot_sha256}"
    for path in sorted(candidates):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if (
            f"artifact: {context.artifact.artifact_id}" in text
            and f"checkpoint: {context.checkpoint}" in text
            and binding in text
        ):
            return "pass", f"Fresh retained evidence is bound at {path.relative_to(context.root).as_posix()}."
    return "not_assessable", (
        f"No readable evidence for {context.artifact.artifact_id}, checkpoint {context.checkpoint}, "
        f"and formal snapshot {context.formal_snapshot_sha256} is available."
    )


def _evaluate(name: str, predicate: Mapping[str, Any], context: CheckpointContext) -> tuple[str, str]:
    if name == "artifact_status":
        statuses = predicate.get("statuses", [])
        if context.artifact.status in statuses:
            return "pass", f"{context.artifact.artifact_id} status is {context.artifact.status}."
        return "fail", f"{context.artifact.artifact_id} status {context.artifact.status} is not one of {', '.join(statuses)}."
    if name == "formal_graph_valid":
        if context.scoped_errors:
            return "fail", f"Selected graph validation failed: {context.scoped_errors[0]['message']}"
        return "pass", "The selected formal graph is valid."
    if name == "repository_integrity":
        if context.repository_errors:
            return "fail", f"Repository integrity failed: {context.repository_errors[0]['message']}"
        return "pass", "No repository-integrity blocker prevents selected evaluation."
    if name == "execution_scope_declared":
        if context.declared_scope:
            return "pass", f"{context.artifact.artifact_id} declares {len(context.declared_scope)} normalized scope path(s)."
        return "not_assessable", f"{context.artifact.artifact_id} has no assessable execution scope."
    if name == "change_set_complete":
        if context.change_set.complete:
            return "pass", "The caller explicitly asserted that the declared change set is complete."
        return "not_assessable", "Change-set completeness was not asserted; absence of undeclared changes cannot be inferred."
    if name == "changed_paths_within_scope":
        if not context.change_set.complete:
            return "not_assessable", "Changed-path scope cannot pass without an explicit completeness assertion."
        outside = [path for path in context.change_set.paths if not path_is_admitted(path, context.declared_scope)]
        if outside:
            return "fail", f"WEX201: changed path is outside execution scope: {outside[0]}"
        return "pass", f"All {len(context.change_set.paths)} declared changed path(s) are within execution scope."
    if name == "start_preflight_ready":
        return _preflight_status(context, "start")
    if name == "review_preflight_ready":
        return _preflight_status(context, "review")
    if name == "review_evidence_available":
        return _review_evidence(context)
    raise ContractError(f"unknown predicate evaluator {name}")


def _aggregate(statuses: Iterable[str]) -> str:
    values = set(statuses)
    if "fail" in values:
        return "fail"
    if "not_assessable" in values:
        return "not_assessable"
    return "pass"


def _evidence(descriptors: Iterable[Mapping[str, Any]], artifact_id: str, checkpoint: str) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for descriptor in descriptors:
        result.append(
            {
                "kind": str(descriptor.get("kind", "result")),
                "reference": str(descriptor.get("reference", "")).replace("{artifact_id}", artifact_id).replace("{checkpoint}", checkpoint),
            }
        )
    return result


def _gate_results(
    gate_ids: Iterable[str],
    gates: Mapping[str, Mapping[str, Any]],
    context: CheckpointContext,
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for gate_id in gate_ids:
        gate = gates[gate_id]
        if context.checkpoint not in gate["checkpoints"]:
            raise HarnessError(
                f"WEX210: gate {gate_id} does not apply at checkpoint {context.checkpoint}"
            )
        predicates: list[dict[str, Any]] = []
        for predicate in gate["predicates"]:
            status, message = _evaluate(predicate["evaluator"], predicate, context)
            predicates.append(
                {
                    "id": predicate["id"],
                    "status": status,
                    "evidence": _evidence(predicate["required_evidence"], context.artifact.artifact_id, context.checkpoint),
                    "message": message,
                }
            )
        result.append({"id": gate_id, "status": _aggregate(item["status"] for item in predicates), "predicates": predicates})
    return result


def check_workflow(
    repository: Path,
    *,
    artifact_id: str,
    checkpoint: str,
    procedure_id: str | None = None,
    changed_paths: Iterable[str] = (),
    changes_complete: bool = False,
    change_manifest: Path | None = None,
) -> dict[str, Any]:
    if checkpoint not in {"start", "pre-action", "handoff"}:
        raise HarnessError("WEX210: public check checkpoint must be start, pre-action, or handoff")
    root = ensure_target(repository, must_exist=True)
    workflow_contract, _, rules, procedures, gates = load_validated_contracts()
    from se_harness.workflow import _catalog, _validation, project_scope

    _, report = _validation(root)
    try:
        catalog = _catalog(report)
    except HarnessError as exc:
        raise HarnessError(f"WEX210: {exc}") from exc
    primary = catalog.get(artifact_id)
    if primary is None:
        raise HarnessError(f"WEX210: unknown artifact ID: {artifact_id}")
    if primary.artifact_type not in {"work_order", "verification_record", "release_record"}:
        raise HarnessError("WEX210: check accepts only WO, VREC, or RLS artifacts")
    governing, dependencies = project_scope(catalog, primary)
    related = [catalog[item] for item in dependencies if item in catalog]
    rule, rule_context = select_rule(rules, primary, related=related)
    selected_procedure = str(rule["procedure_id"])
    alternatives = list(rule.get("alternative_procedure_ids", []))
    if checkpoint == "pre-action" and procedure_id is None:
        raise HarnessError("WEX220: --procedure is required for pre-action")
    if procedure_id is not None:
        if procedure_id not in {selected_procedure, *alternatives}:
            raise HarnessError(f"WEX220: procedure {procedure_id} is not selected by workflow rule {rule['id']}")
        selected_procedure = procedure_id
    change_set = (
        parse_change_manifest(root, change_manifest)
        if change_manifest is not None
        else declared_change_set(changed_paths, complete=changes_complete)
    )
    _validate_changed_targets(root, change_set)
    scoped, repository_errors, unrelated = _classify(report, catalog, primary, root)
    try:
        scope = execution_scope(primary) if primary.artifact_type == "work_order" else ()
    except HarnessError:
        scope = ()
    context = CheckpointContext(
        root=root,
        artifact=primary,
        report=report,
        catalog=catalog,
        scoped_errors=scoped,
        repository_errors=repository_errors,
        unrelated_count=unrelated,
        declared_scope=scope,
        change_set=change_set,
        checkpoint=checkpoint,
        formal_snapshot_sha256=formal_snapshot_digest(root, report.artifacts),
    )
    gate_ids = list(rule["gate_ids"])
    resolved = resolve_procedure(
        procedures,
        selected_procedure,
        {
            "artifact_id": artifact_id,
            "status": primary.status,
            "changed_paths": list(change_set.paths),
            **rule_context,
        },
    )
    if checkpoint == "pre-action":
        first = resolved["steps"][0]
        gate_ids = list(dict.fromkeys([*gate_ids, *first.get("gate_ids", [])]))
    gate_results = _gate_results(gate_ids, gates, context)
    compliance_status = _aggregate([item["status"] for item in gate_results] or ["pass"])
    passed = compliance_status == "pass" and not scoped and not repository_errors
    outcome = "completed" if passed else "blocked"
    current_step = select_current_step(resolved, checkpoint=checkpoint, passed=passed)
    predicate_blockers = [
        f"{predicate['id']}: {predicate['message']}"
        for gate in gate_results
        for predicate in gate["predicates"]
        if predicate["status"] != "pass"
    ]
    finding_blockers = [
        f"{item['code']}: {item['message']}"
        for item in [*repository_errors, *scoped]
    ]
    blockers = [*predicate_blockers, *finding_blockers]
    action = (
        str(current_step.get("decision", "Provide the required decision"))
        if current_step["kind"] == "decision"
        else "Run the bound command"
        if current_step["kind"] == "command"
        else "Follow the bound reference"
    )
    restitution = {
        "outcome": outcome,
        "done": [f"Evaluated {checkpoint} compliance for {artifact_id}."],
        "not_done": [] if passed else [f"The {checkpoint} checkpoint did not pass."],
        "blocked_by": blockers,
        "current_lifecycle_state": [f"{artifact_id} is {primary.status}."],
        "decision_required": decision_required(current_step) if passed else None,
        "next": {"procedure_id": selected_procedure, "step_id": current_step["id"], "action": action},
        "command_or_response": command_or_response(current_step),
        "alternatives": [f"Use complete alternative procedure {identifier}." for identifier in alternatives],
    }
    return build_result(
        operation="check",
        outcome=outcome,
        primary=artifact_id,
        artifacts=[artifact_id],
        governing=governing,
        dependencies=dependencies,
        declared_paths=scope,
        changed_paths=change_set.paths,
        change_set_complete=change_set.complete,
        compliance={
            "checkpoint": checkpoint,
            "workflow_rule_id": rule["id"],
            "procedure_id": selected_procedure,
            "status": compliance_status if not (scoped or repository_errors) else "fail",
            "gates": gate_results,
            "formal_snapshot_sha256": context.formal_snapshot_sha256,
            "change_set_source": change_set.source,
        },
        procedure={"id": selected_procedure, "current_step": current_step["id"], "steps": resolved["steps"]},
        restitution=restitution,
        before=[{"id": artifact_id, "status": primary.status}],
        after=[{"id": artifact_id, "status": primary.status}],
        scoped_blockers=scoped,
        repository_blockers=repository_errors,
        unrelated_count=unrelated,
    )


def focus_schema2(
    repository: Path,
    *,
    artifact_id: str,
    include_background: bool = False,
) -> dict[str, Any]:
    """Project selected focus through the v2 rule and procedure registries."""

    root = ensure_target(repository, must_exist=True)
    _, _, rules, procedures, _ = load_validated_contracts()
    from se_harness.workflow import _catalog, _validation, focus, project_scope

    legacy = focus(root, artifact_id, include_background=include_background)
    _, report = _validation(root)
    catalog = _catalog(report)
    primary = catalog[artifact_id]
    governing, dependencies = project_scope(catalog, primary)
    related = [catalog[item] for item in dependencies if item in catalog]
    rule, rule_context = select_rule(rules, primary, related=related)
    resolved = resolve_procedure(
        procedures,
        str(rule["procedure_id"]),
        {"artifact_id": artifact_id, "status": primary.status, **rule_context},
    )
    step = resolved["steps"][0]
    legacy_findings = legacy["findings"]
    blockers = [
        *legacy_findings["repository_blockers"],
        *legacy_findings["scoped_blockers"],
    ]
    blocked = legacy["operation"]["outcome"] != "completed"
    handoff = legacy["handoff"]
    alternatives = list(rule.get("alternative_procedure_ids", []))
    scope = ()
    if primary.artifact_type == "work_order":
        try:
            scope = execution_scope(primary)
        except HarnessError:
            scope = ()
    restitution = {
        "outcome": "blocked" if blocked else "completed",
        "done": [str(item) for item in handoff.get("completed", [])],
        "not_done": ["The selected focus operation remains incomplete."] if blocked else [],
        "blocked_by": [f"{item.get('code', 'WEX')}: {item.get('message', '')}" for item in blockers],
        "current_lifecycle_state": [str(item) for item in handoff.get("current_lifecycle_state", [])],
        "decision_required": decision_required(step) if not blocked else None,
        "next": {
            "procedure_id": rule["procedure_id"],
            "step_id": step["id"],
            "action": str(step.get("decision", "Run the bound command" if step["kind"] == "command" else "Follow the bound reference")),
        },
        "command_or_response": command_or_response(step),
        "alternatives": [f"Use complete alternative procedure {identifier}." for identifier in alternatives],
    }
    unrelated_count = sum(
        int(item.get("count", 0))
        for item in legacy_findings.get("background_summary", [])
        if isinstance(item, Mapping)
    )
    return build_result(
        operation="focus",
        outcome="blocked" if blocked else "completed",
        primary=artifact_id,
        artifacts=[artifact_id],
        governing=governing,
        dependencies=dependencies,
        declared_paths=scope,
        changed_paths=[],
        change_set_complete=False,
        compliance={
            "checkpoint": "pre-action",
            "workflow_rule_id": rule["id"],
            "procedure_id": rule["procedure_id"],
            "status": "fail" if blocked else "not_assessable",
            "gates": [],
        },
        procedure={"id": rule["procedure_id"], "current_step": step["id"], "steps": resolved["steps"]},
        restitution=restitution,
        before=legacy["state"]["before"],
        after=legacy["state"]["after"],
        scoped_blockers=legacy_findings["scoped_blockers"],
        repository_blockers=legacy_findings["repository_blockers"],
        unrelated_count=unrelated_count,
    )


def ensure_governed_checkpoint(
    repository: Path,
    artifact_ids: Iterable[str],
    *,
    report: Any | None = None,
    catalog: Mapping[str, Any] | None = None,
) -> None:
    """Fail closed on contract or repository-integrity damage before a mutation."""

    root = ensure_target(repository, must_exist=True)
    try:
        load_validated_contracts()
    except ContractError as exc:
        raise HarnessError(f"WEX210: invalid machine policy: {exc}") from exc
    from se_harness.workflow import _catalog, _validation

    if report is None:
        _, report = _validation(root)
    if catalog is None:
        catalog = _catalog(report)
    for artifact_id in artifact_ids:
        if artifact_id not in catalog:
            raise HarnessError(f"WEX210: unknown governed artifact {artifact_id}")
    repository_errors = [item for item in report.errors if item.code in _REPOSITORY_ERROR_CODES]
    if repository_errors:
        raise HarnessError(f"WEX210: repository integrity prevents governed action: {repository_errors[0].message}")
