"""The repository graph the workflow reads (SPEC-ECP-024 ECP-ENG-020): one validation, the artifact catalog, the selected scope of a primary artifact and the classification of its diagnostics.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from se_harness.codes import E001, E003, WEX200
from se_harness.decisions import against_reference
from se_harness.engine import validate_engineering_artifacts as _validator_module
from se_harness.engine.validation_core import relation_targets
from se_harness.installer import HarnessError, safe_destination


PRIMARY_TYPES = {"work_order", "verification_record", "release_record", "decision"}
#: The codes that make a repository unevaluable for any selected scope (ECP-KRN-004).
REPOSITORY_ERROR_CODES = {E001, E003}


class RepositoryWorkflowError(HarnessError):
    """The repository cannot be evaluated at all: the validator or its identities failed."""


def validated_repository(root: Path) -> tuple[Any, Any]:
    try:
        validator = _validator_module  # ECP-ENG-003: imported, never loaded by path
        return validator, validator.validate_repository(root)
    except HarnessError as exc:
        raise RepositoryWorkflowError(str(exc)) from exc


def artifact_catalog(report: Any) -> dict[str, Any]:
    catalog: dict[str, Any] = {}
    duplicates: set[str] = set()
    folded: dict[str, str] = {}
    case_collisions: set[str] = set()
    for artifact in report.artifacts:
        if artifact.artifact_id in catalog:
            duplicates.add(artifact.artifact_id)
        key = artifact.artifact_id.casefold()
        previous = folded.get(key)
        if previous is not None and previous != artifact.artifact_id:
            case_collisions.update((previous, artifact.artifact_id))
        folded[key] = artifact.artifact_id
        catalog[artifact.artifact_id] = artifact
    if duplicates:
        raise RepositoryWorkflowError(f"formal artifact IDs are not unique: {', '.join(sorted(duplicates))}")
    if case_collisions:
        raise RepositoryWorkflowError(
            "formal artifact IDs are not unique under case-insensitive comparison: "
            + ", ".join(sorted(case_collisions, key=lambda item: (item.casefold(), item)))
        )
    return catalog


def inverse_targets(catalog: Mapping[str, Any], target_id: str, relation: str, artifact_type: str) -> set[str]:
    return {
        item.artifact_id
        for item in catalog.values()
        if item.artifact_type == artifact_type and target_id in relation_targets(item, relation)
    }


def work_scope(catalog: Mapping[str, Any], work_order: Any) -> tuple[set[str], set[str]]:
    governing = set().union(
        relation_targets(work_order, "implements"),
        relation_targets(work_order, "specifications"),
        relation_targets(work_order, "architecture"),
        relation_targets(work_order, "verification"),
    )
    requirements = {
        item for item in governing if item in catalog and catalog[item].artifact_type == "requirement"
    }
    capabilities: set[str] = set()
    for requirement_id in requirements:
        capabilities.update(relation_targets(catalog[requirement_id], "derives_from"))
    governing.update(capabilities)
    for capability_id in capabilities:
        if capability_id in catalog:
            governing.update(relation_targets(catalog[capability_id], "derives_from"))
    vrecs = inverse_targets(catalog, work_order.artifact_id, "verifies_work_order", "verification_record")
    releases = inverse_targets(catalog, work_order.artifact_id, "releases_work", "release_record")
    return governing, vrecs | releases


def project_scope(catalog: Mapping[str, Any], primary: Any) -> tuple[set[str], set[str]]:
    if primary.artifact_type == "work_order":
        return work_scope(catalog, primary)
    if primary.artifact_type == "verification_record":
        governing = relation_targets(primary, "conforms_to")
        work = relation_targets(primary, "verifies_work_order")
        governing.update(work)
        dependencies: set[str] = set()
        for work_id in work:
            if work_id in catalog:
                upstream, _ = work_scope(catalog, catalog[work_id])
                governing.update(upstream)
        dependencies.update(inverse_targets(catalog, primary.artifact_id, "includes_verification", "release_record"))
        return governing, dependencies
    if primary.artifact_type == "release_record":
        governing = set().union(
            relation_targets(primary, "satisfies"),
            relation_targets(primary, "includes_verification"),
            relation_targets(primary, "releases_work"),
        )
        for work_id in relation_targets(primary, "releases_work"):
            if work_id in catalog:
                upstream, _ = work_scope(catalog, catalog[work_id])
                governing.update(upstream)
        return governing, set()
    if primary.artifact_type == "decision":
        governing = set().union(relation_targets(primary, "concerns"), relation_targets(primary, "blocks"), relation_targets(primary, "produces"))
        reference = against_reference(primary)
        if reference is not None:
            governing.add(reference[0])
        return governing, set()
    raise HarnessError("check accepts only WO, VREC, RLS, or DEC artifacts")


def diagnostic_payload(item: Any) -> dict[str, str]:
    return {
        "code": item.code,
        "path": item.path,
        "message": item.message,
        "plane": item.plane,
    }


def classify_diagnostics(report: Any, catalog: Mapping[str, Any], primary: Any, root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    """Split a report's errors into the selected scope, the repository blockers and the unrelated count (ECP-KRN-004)."""

    if primary.artifact_type in PRIMARY_TYPES:
        governing, dependencies = project_scope(catalog, primary)
    else:
        # A definition's selected scope is itself (transition checkpoint, ECP-KRN-004).
        governing, dependencies = set(), set()
    scope_paths = {
        catalog[identifier].path.resolve()
        for identifier in governing | dependencies | {primary.artifact_id}
        if identifier in catalog
    }
    scoped: list[dict[str, Any]] = []
    repository: list[dict[str, Any]] = []
    unrelated = 0
    for item in report.errors:
        diagnostic = diagnostic_payload(item)
        if item.code in REPOSITORY_ERROR_CODES:
            repository.append(diagnostic)
            continue
        try:
            candidate = safe_destination(root, Path(item.path)).resolve()
        except HarnessError:
            repository.append({**diagnostic, "code": WEX200})
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
