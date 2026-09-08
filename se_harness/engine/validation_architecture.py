"""The architecture seam: relations, traceability and requirement coverage.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from se_harness.codes import E006, E007, E008, E011, E016, W015
from se_harness.workflow_contract import IMPLEMENTED_OR_LATER_STATUSES
from se_harness.engine.validation_core import (
    Artifact,
    Diagnostic,
    add_error,
    display_path,
    duplicate_strings,
    relation_targets,
)
from se_harness.engine.validation_lifecycle import grants_authority


RELATION_TARGET_TYPES: dict[tuple[str, str], set[str]] = {
    ("architecture", "addresses"): {"requirement"},
    ("architecture", "conforms_to"): {"specification"},
    ("architecture", "constrains"): {"requirement", "specification"},
    ("operating_contract", "assures"): {"requirement"},
    ("verification_record", "verifies_work_order"): {"work_order"},
    ("verification_record", "conforms_to"): {"verification"},
    ("verification_record", "superseded_by"): {"verification_record"},
    ("release_record", "satisfies"): {"release_contract"},
    ("release_record", "includes_verification"): {"verification_record"},
    ("release_record", "releases_work"): {"work_order"},
    ("decision", "blocks"): {"requirement", "specification", "verification", "architecture", "adr", "work_order"},
    ("decision", "produces"): {"requirement", "specification", "verification", "architecture", "adr", "work_order"},
    ("risk", "mitigated_by"): {"work_order"},
    ("risk", "avoided_by"): {"adr", "decision"},
}


def validate_relations(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    catalog = {
        artifact.artifact_id: artifact
        for artifact in artifacts
        if artifact.artifact_id != "<unknown>"
    }

    for artifact in artifacts:
        relations = artifact.metadata.get("relations", {})
        if not isinstance(relations, dict):
            continue
        for relation_name, targets in sorted(relations.items()):
            if not isinstance(targets, list):
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E006,
                    f"relation '{relation_name}' must be an array of artifact IDs",
                    plane="structure",
                )
                continue
            for target in targets:
                if not isinstance(target, str) or not target.strip():
                    add_error(
                        errors,
                        artifact,
                        report_root,
                        E006,
                        f"relation '{relation_name}' contains a non-string or empty target",
                        plane="structure",
                    )
                    continue
                if target == artifact.artifact_id:
                    add_error(
                        errors,
                        artifact,
                        report_root,
                        E006,
                        f"artifact '{artifact.artifact_id}' must not reference itself via '{relation_name}'",
                        plane="structure",
                    )
                elif target not in catalog:
                    add_error(
                        errors,
                        artifact,
                        report_root,
                        E006,
                        f"artifact '{artifact.artifact_id}' relation '{relation_name}' references unknown target '{target}'",
                        plane="structure",
                    )
                else:
                    allowed_types = RELATION_TARGET_TYPES.get((artifact.artifact_type, relation_name))
                    target_type = catalog[target].artifact_type
                    if allowed_types is not None and target_type not in allowed_types:
                        expected = ", ".join(sorted(allowed_types))
                        add_error(
                            errors,
                            artifact,
                            report_root,
                            E011,
                            f"relation '{relation_name}' target '{target}' must have type {expected}, found {target_type}",
                            plane="structure",
                        )
    return errors


def architecture_traceability_state(
    artifact: Artifact,
    catalog: dict[str, Artifact],
) -> dict[str, Any]:
    """Return deterministic typed or compatibility architecture traceability."""

    if artifact.artifact_type != "architecture":
        return {
            "state": "not_applicable",
            "addresses": [],
            "conforms_to": [],
            "transitive_requirements": [],
            "missing_from_conforming_specifications": [],
            "legacy_targets": [],
            "issues": [],
        }

    relations = artifact.relations
    issues: list[str] = []

    def values(name: str, *, required: bool) -> list[str]:
        raw = relations.get(name)
        if raw is None:
            if required:
                issues.append(f"architecture relation '{name}' is required")
            return []
        if not isinstance(raw, list):
            issues.append(f"architecture relation '{name}' must be an array")
            return []
        invalid = [item for item in raw if not isinstance(item, str) or not item.strip()]
        if invalid:
            issues.append(f"architecture relation '{name}' contains a non-string or empty target")
        clean = [item.strip() for item in raw if isinstance(item, str) and item.strip()]
        duplicates = duplicate_strings(raw)
        if duplicates:
            issues.append(f"architecture relation '{name}' contains duplicates: {', '.join(duplicates)}")
        if required and not clean:
            issues.append(f"architecture relation '{name}' must not be empty")
        return sorted(set(clean))

    typed_present = "addresses" in relations or "conforms_to" in relations
    legacy_present = "constrains" in relations
    addresses = values("addresses", required=typed_present)
    conforms_to = values("conforms_to", required=typed_present)
    legacy_targets = values("constrains", required=legacy_present)

    transitive_requirements: set[str] = set()
    for specification_id in conforms_to:
        specification = catalog.get(specification_id)
        if specification is None or specification.artifact_type != "specification":
            continue
        transitive_requirements.update(relation_targets(specification, "specifies"))
        if (
            grants_authority(artifact.artifact_type, artifact.status)
            and not grants_authority(specification.artifact_type, specification.status)
        ):
            issues.append(
                f"active architecture conforms to inactive specification '{specification_id}'"
            )

    if grants_authority(artifact.artifact_type, artifact.status):
        for requirement_id in addresses:
            requirement = catalog.get(requirement_id)
            if (
                requirement is not None
                and requirement.artifact_type == "requirement"
                and not grants_authority(requirement.artifact_type, requirement.status)
            ):
                issues.append(
                    f"active architecture addresses inactive requirement '{requirement_id}'"
                )

    missing = sorted(set(addresses) - transitive_requirements)
    if typed_present and missing:
        issues.append(
            "addressed requirements are not specified by a conforming specification: "
            + ", ".join(missing)
        )

    state = "typed"
    if typed_present:
        if legacy_present:
            for target_id in legacy_targets:
                target = catalog.get(target_id)
                if target is None:
                    continue
                if target.artifact_type == "requirement" and target_id not in addresses:
                    issues.append(
                        f"legacy requirement target '{target_id}' is absent from addresses"
                    )
                elif target.artifact_type == "specification" and target_id not in conforms_to:
                    issues.append(
                        f"legacy specification target '{target_id}' is absent from conforms_to"
                    )
                elif target.artifact_type not in {"requirement", "specification"}:
                    issues.append(
                        f"legacy target '{target_id}' has unsupported type '{target.artifact_type}'"
                    )
            state = "dual_declared"
    elif legacy_present and artifact.status in IMPLEMENTED_OR_LATER_STATUSES:
        target_types = {
            catalog[target_id].artifact_type
            for target_id in legacy_targets
            if target_id in catalog
        }
        if target_types == {"requirement"}:
            state = "legacy_requirement_trace"
        elif target_types == {"specification"}:
            state = "legacy_specification_trace"
        else:
            state = "legacy_ambiguous"
            issues.append(
                "completed legacy architecture constrains relation must target only requirements or only specifications"
            )
    else:
        state = "missing_typed_relations"
        issues.append(
            "new or ongoing architecture requires typed addresses and conforms_to relations"
        )

    if issues:
        state = "invalid"
    return {
        "state": state,
        "addresses": addresses,
        "conforms_to": conforms_to,
        "transitive_requirements": sorted(transitive_requirements),
        "missing_from_conforming_specifications": missing,
        "legacy_targets": legacy_targets,
        "issues": sorted(set(issues)),
    }


def validate_architecture_traceability(
    artifacts: list[Artifact],
    report_root: Path,
) -> tuple[list[Diagnostic], list[Diagnostic]]:
    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    catalog = {
        artifact.artifact_id: artifact
        for artifact in artifacts
        if artifact.artifact_id != "<unknown>"
    }
    for artifact in artifacts:
        if artifact.artifact_type != "architecture":
            continue
        traceability = architecture_traceability_state(artifact, catalog)
        for issue in traceability["issues"]:
            add_error(
                errors,
                artifact,
                report_root,
                E016,
                issue,
                plane="governance",
            )
        if traceability["state"] in {
            "dual_declared",
            "legacy_requirement_trace",
            "legacy_specification_trace",
        }:
            warnings.append(
                Diagnostic(
                    display_path(artifact.path, report_root),
                    W015,
                    f"architecture uses deprecated constrains relation ({traceability['state']}); migrate through accountable governance",
                    "maintenance",
                )
            )
    return errors, warnings


def validate_requirement_coverage(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    active_specs = [
        artifact
        for artifact in artifacts
        if artifact.artifact_type == "specification"
        and grants_authority(artifact.artifact_type, artifact.status)
    ]
    active_verifications = [
        artifact
        for artifact in artifacts
        if artifact.artifact_type == "verification"
        and grants_authority(artifact.artifact_type, artifact.status)
    ]

    specified = set().union(*(relation_targets(item, "specifies") for item in active_specs)) if active_specs else set()
    verified = set().union(*(relation_targets(item, "verifies") for item in active_verifications)) if active_verifications else set()

    for artifact in artifacts:
        if (
            artifact.artifact_type != "requirement"
            or not grants_authority(artifact.artifact_type, artifact.status)
        ):
            continue
        if artifact.artifact_id not in specified:
            add_error(
                errors,
                artifact,
                report_root,
                E007,
                f"active requirement '{artifact.artifact_id}' has no active specification coverage",
                plane="governance",
            )
        if artifact.artifact_id not in verified:
            add_error(
                errors,
                artifact,
                report_root,
                E008,
                f"active requirement '{artifact.artifact_id}' has no active verification coverage",
                plane="governance",
            )

    return errors
