"""The lifecycle seam: the registry the validator reads, the common metadata pass and the lifecycle-event pass.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from types import MappingProxyType

from se_harness.artifact_layout import ID_PATTERN
from se_harness.codes import E002, E003, E004, E006, E014
from se_harness.workflow_contract import LifecycleState, lifecycle_family, load_lifecycle_registry
from se_harness.engine.validation_core import (
    Artifact,
    Diagnostic,
    ISO_DATE_PATTERN,
    TYPE_PREFIX,
    add_error,
    display_path,
    require_non_empty_string,
    require_non_empty_string_list,
)


LifecycleStatePolicy = LifecycleState


WORKFLOW_LIFECYCLES = load_lifecycle_registry()


WORKFLOW_TRANSITIONS = MappingProxyType({
    family: MappingProxyType(
        {state: frozenset(row.transitions_to) for state, row in states.items()}
    )
    for family, states in WORKFLOW_LIFECYCLES.items()
})


ACTIVE_COVERAGE_STATUSES = frozenset({
    state
    for family in ("definition", "work_order")
    for state, row in WORKFLOW_LIFECYCLES[family].items()
    if row.grants_authority
})


def _lifecycle_policy(artifact_type: str, status: str) -> LifecycleStatePolicy | None:
    return WORKFLOW_LIFECYCLES[lifecycle_family(artifact_type)].get(status)


def grants_authority(artifact_type: str, status: str) -> bool:
    row = _lifecycle_policy(artifact_type, status)
    return bool(row and row.grants_authority)


def reserves_version(status: str) -> bool:
    row = WORKFLOW_LIFECYCLES["release_record"].get(status)
    return bool(row and row.reserves_version)


def active_record_status(artifact_type: str, status: str) -> bool:
    """Return whether a VREC/RLS is a live proposal or grants authority."""

    row = _lifecycle_policy(artifact_type, status)
    return bool(row and (row.transitionable or row.grants_authority))


def validate_common_metadata(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    seen: dict[str, Artifact] = {}

    for artifact in artifacts:
        artifact_id = require_non_empty_string(artifact, "id", errors, report_root)
        artifact_type = require_non_empty_string(artifact, "type", errors, report_root)
        require_non_empty_string(artifact, "title", errors, report_root)
        status = require_non_empty_string(artifact, "status", errors, report_root)
        require_non_empty_string_list(artifact, "owners", errors, report_root)
        created = require_non_empty_string(artifact, "created", errors, report_root)
        updated = require_non_empty_string(artifact, "updated", errors, report_root)

        if artifact_id is not None:
            if not ID_PATTERN.fullmatch(artifact_id):
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E002,
                    f"id '{artifact_id}' must use uppercase letters/digits/hyphens and end in a three-digit sequence",
                    plane="structure",
                )
            previous = seen.get(artifact_id)
            if previous is not None:
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E003,
                    f"duplicate id '{artifact_id}' also declared in {display_path(previous.path, report_root)}",
                    plane="structure",
                )
            else:
                seen[artifact_id] = artifact

        if artifact_type is not None:
            expected_prefix = TYPE_PREFIX.get(artifact_type)
            if expected_prefix is None:
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E002,
                    f"unknown artifact type '{artifact_type}'",
                    plane="structure",
                )
            elif artifact_id is not None and not artifact_id.startswith(expected_prefix):
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E004,
                    f"id '{artifact_id}' must start with '{expected_prefix}' for type '{artifact_type}'",
                    plane="structure",
                )

        if (
            status is not None
            and artifact_type is not None
            and status not in WORKFLOW_LIFECYCLES[lifecycle_family(artifact_type)]
        ):
            add_error(
                errors,
                artifact,
                report_root,
                E002,
                f"status '{status}' is not declared for {lifecycle_family(artifact_type)} artifacts",
                plane="structure",
            )

        for field_name, field_value in (("created", created), ("updated", updated)):
            if field_value is not None and not ISO_DATE_PATTERN.fullmatch(field_value):
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E002,
                    f"field '{field_name}' must use YYYY-MM-DD",
                    plane="structure",
                )

        relations = artifact.metadata.get("relations", {})
        if not isinstance(relations, dict):
            add_error(
                errors,
                artifact,
                report_root,
                E006,
                "field 'relations' must be a TOML table",
                plane="structure",
            )

    return errors


def validate_lifecycle_events(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    """Validate append-only decision events when the new contract is present.

    Historical artifacts without events remain valid. Once an event exists, its
    chain and any target-specific decision fields must be internally consistent.
    """

    errors: list[Diagnostic] = []
    for artifact in artifacts:
        events = artifact.metadata.get("lifecycle_events")
        if events is None:
            continue
        if not isinstance(events, list) or not events:
            add_error(
                errors, artifact, report_root, E014,
                "field 'lifecycle_events' must be a non-empty array of tables when present",
                plane="governance",
            )
            continue
        previous_to: str | None = None
        previous_at: str | None = None
        valid_events: list[dict[str, str]] = []
        family = lifecycle_family(artifact.artifact_type)
        for index, event in enumerate(events):
            if not isinstance(event, dict):
                add_error(
                    errors, artifact, report_root, E014,
                    f"lifecycle event {index + 1} must be a TOML table",
                    plane="governance",
                )
                continue
            values: dict[str, str] = {}
            for key in ("from", "to", "decided_at", "decided_by"):
                value = event.get(key)
                if not isinstance(value, str) or not value.strip():
                    add_error(
                        errors, artifact, report_root, E014,
                        f"lifecycle event {index + 1} field '{key}' must be a non-empty string",
                        plane="governance",
                    )
                else:
                    values[key] = value.strip()
            reason = event.get("reason")
            if reason is not None and (not isinstance(reason, str) or not reason.strip()):
                add_error(
                    errors, artifact, report_root, E014,
                    f"lifecycle event {index + 1} field 'reason' must be a non-empty string when present",
                    plane="governance",
                )
            decided_at = values.get("decided_at")
            if decided_at is not None:
                try:
                    datetime.strptime(decided_at, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    add_error(
                        errors, artifact, report_root, E014,
                        f"lifecycle event {index + 1} field 'decided_at' must use a valid YYYY-MM-DDTHH:MM:SSZ timestamp",
                        plane="governance",
                    )
                if previous_at is not None and decided_at < previous_at:
                    add_error(
                        errors, artifact, report_root, E014,
                        "lifecycle events must be ordered chronologically",
                        plane="governance",
                    )
                previous_at = decided_at
            source = values.get("from")
            target = values.get("to")
            if source is not None and target is not None:
                if target not in WORKFLOW_TRANSITIONS.get(family, {}).get(source, set()):
                    add_error(
                        errors, artifact, report_root, E014,
                        f"lifecycle event {index + 1} contains unsupported transition {source} -> {target}",
                        plane="governance",
                    )
                if previous_to is not None and source != previous_to:
                    add_error(
                        errors, artifact, report_root, E014,
                        f"lifecycle event {index + 1} starts at '{source}' instead of previous target '{previous_to}'",
                        plane="governance",
                    )
                previous_to = target
            if len(values) == 4:
                valid_events.append(values)
        if previous_to is not None and previous_to != artifact.status:
            add_error(
                errors, artifact, report_root, E014,
                f"last lifecycle event target '{previous_to}' must equal artifact status '{artifact.status}'",
                plane="governance",
            )
        if not valid_events:
            continue
        latest = valid_events[-1]
        expected_fields: tuple[str, str] | None = None
        if artifact.artifact_type == "verification_record" and latest["to"] == "verified":
            expected_fields = ("verified_at", "verified_by")
        elif artifact.artifact_type == "release_record" and latest["to"] == "released":
            expected_fields = ("released_at", "authorized_by")
        elif latest["to"] == "rejected":
            expected_fields = ("rejected_at", "rejected_by")
            reason = events[-1].get("reason") if isinstance(events[-1], dict) else None
            if not isinstance(reason, str) or not reason.strip():
                add_error(
                    errors, artifact, report_root, E014,
                    "rejection lifecycle event requires a non-empty reason",
                    plane="governance",
                )
            if artifact.metadata.get("rejection_reason") != reason:
                add_error(
                    errors, artifact, report_root, E014,
                    "field 'rejection_reason' must equal the rejection lifecycle event reason",
                    plane="governance",
                )
        elif artifact.artifact_type == "verification_record" and latest["to"] == "superseded":
            expected_fields = ("superseded_at", "supersession_authorized_by")
            reason = events[-1].get("reason") if isinstance(events[-1], dict) else None
            successors = artifact.relations.get("superseded_by", [])
            if not isinstance(reason, str) or successors != [reason]:
                add_error(
                    errors, artifact, report_root, E014,
                    "supersession lifecycle event reason must equal the single superseded_by target",
                    plane="governance",
                )
        if expected_fields is not None:
            timestamp_field, actor_field = expected_fields
            legacy_decision_record = (
                artifact.artifact_type in {"verification_record", "release_record"}
                and "prepared_at" not in artifact.metadata
                and latest["to"] in {"verified", "released"}
            )
            if not legacy_decision_record and artifact.metadata.get(timestamp_field) != latest["decided_at"]:
                add_error(
                    errors, artifact, report_root, E014,
                    f"field '{timestamp_field}' must equal the latest lifecycle decision timestamp",
                    plane="governance",
                )
            if not legacy_decision_record and artifact.metadata.get(actor_field) != latest["decided_by"]:
                add_error(
                    errors, artifact, report_root, E014,
                    f"field '{actor_field}' must equal the latest lifecycle decision actor",
                    plane="governance",
                )
    return errors
