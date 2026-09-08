"""The revision seam: revision consistency and operating-contract readiness.
"""

from __future__ import annotations

from pathlib import Path

from se_harness.codes import E010, E017, E018
from se_harness.workflow_contract import IMPLEMENTED_OR_LATER_STATUSES
from se_harness.engine.validation_core import (
    Artifact,
    Diagnostic,
    add_error,
    duplicate_strings,
    relation_targets,
)
from se_harness.engine.validation_evidence import evidence_path_is_keyed_to
from se_harness.engine.validation_lifecycle import active_record_status, grants_authority, reserves_version


def _check_verification_record(
    artifact: Artifact,
    catalog: dict[str, Artifact],
    supersession_cycle_nodes: set[str],
    errors: list[Diagnostic],
    report_root: Path,
) -> None:
    """Check one verification record: duplicates, work and contract links, evidence keying, supersession."""
    for field_name in ("evidence_paths",):
        duplicates = duplicate_strings(artifact.metadata.get(field_name))
        if duplicates:
            add_error(
                errors,
                artifact,
                report_root,
                E010,
                f"field '{field_name}' contains duplicate values: {', '.join(duplicates)}",
                plane="governance",
            )
    for relation_name in ("verifies_work_order", "conforms_to", "superseded_by"):
        duplicates = duplicate_strings(artifact.relations.get(relation_name))
        if duplicates:
            add_error(
                errors,
                artifact,
                report_root,
                E010,
                f"relation '{relation_name}' contains duplicate targets: {', '.join(duplicates)}",
                plane="governance",
            )
    work_order_ids = relation_targets(artifact, "verifies_work_order")
    verification_ids = relation_targets(artifact, "conforms_to")
    declared_verification: set[str] = set()
    for work_order_id in work_order_ids:
        work_order = catalog.get(work_order_id)
        if work_order is None or work_order.artifact_type != "work_order":
            continue
        declared_verification.update(relation_targets(work_order, "verification"))
        if (
            active_record_status(artifact.artifact_type, artifact.status)
            and not grants_authority(work_order.artifact_type, work_order.status)
        ):
            add_error(
                errors,
                artifact,
                report_root,
                E010,
                f"active verification record requires active work order '{work_order_id}'",
                plane="governance",
            )
    for verification_id in verification_ids:
        verification = catalog.get(verification_id)
        if (
            verification is not None
            and verification.artifact_type == "verification"
            and active_record_status(artifact.artifact_type, artifact.status)
            and not grants_authority(verification.artifact_type, verification.status)
        ):
            add_error(
                errors,
                artifact,
                report_root,
                E010,
                f"active verification record requires active verification contract '{verification_id}'",
                plane="governance",
            )
    missing_verification = declared_verification - verification_ids
    extra_verification = verification_ids - declared_verification
    if missing_verification and (
        "prepared_at" in artifact.metadata or len(work_order_ids) > 1
    ):
        add_error(
            errors,
            artifact,
            report_root,
            E010,
            f"verification record is missing contracts declared by selected work: {', '.join(sorted(missing_verification))}",
            plane="governance",
        )
    if extra_verification:
        add_error(
            errors,
            artifact,
            report_root,
            E010,
            f"verification record includes contracts not declared by selected work: {', '.join(sorted(extra_verification))}",
            plane="governance",
        )
    if len(work_order_ids) > 1:
        evidence_paths = artifact.metadata.get("evidence_paths", [])
        normalized_paths = [item for item in evidence_paths if isinstance(item, str)] if isinstance(evidence_paths, list) else []
        uncovered = [
            work_order_id
            for work_order_id in sorted(work_order_ids)
            if not any(evidence_path_is_keyed_to(path, work_order_id) for path in normalized_paths)
        ]
        if uncovered:
            add_error(
                errors,
                artifact,
                report_root,
                E010,
                f"aggregate evidence is not keyed to work orders: {', '.join(uncovered)}",
                plane="governance",
            )
    if artifact.status == "superseded":
        successor_ids = sorted(relation_targets(artifact, "superseded_by"))
        if len(successor_ids) == 1:
            successor_id = successor_ids[0]
            successor = catalog.get(successor_id)
            if successor is not None and successor.artifact_type == "verification_record":
                if not grants_authority(successor.artifact_type, successor.status):
                    add_error(
                        errors,
                        artifact,
                        report_root,
                        E010,
                        f"superseding verification record '{successor_id}' must be verified or released",
                        plane="governance",
                    )
                missing_work = work_order_ids - relation_targets(successor, "verifies_work_order")
                if missing_work:
                    add_error(
                        errors,
                        artifact,
                        report_root,
                        E010,
                        f"superseding verification record '{successor_id}' omits work orders: {', '.join(sorted(missing_work))}",
                        plane="governance",
                    )
    if artifact.artifact_id in supersession_cycle_nodes:
        add_error(
            errors,
            artifact,
            report_root,
            E010,
            f"verification supersession cycle detected among: {', '.join(sorted(supersession_cycle_nodes))}",
            plane="governance",
        )


def _check_release_record(
    artifact: Artifact,
    catalog: dict[str, Artifact],
    release_versions: dict[str, list[Artifact]],
    errors: list[Diagnostic],
    report_root: Path,
) -> None:
    """Check one release record: duplicate relations, version reservation, released work, included records, contracts."""
    for relation_name in ("satisfies", "includes_verification", "releases_work"):
        duplicates = duplicate_strings(artifact.relations.get(relation_name))
        if duplicates:
            add_error(
                errors,
                artifact,
                report_root,
                E010,
                f"relation '{relation_name}' contains duplicate targets: {', '.join(duplicates)}",
                plane="governance",
            )
    version = artifact.metadata.get("version")
    if reserves_version(artifact.status) and isinstance(version, str) and version.strip():
        release_versions.setdefault(version.strip(), []).append(artifact)
    release_commit = artifact.metadata.get("commit")
    release_format = artifact.metadata.get("git_object_format")
    released_work = relation_targets(artifact, "releases_work")
    for work_order_id in released_work:
        work_order = catalog.get(work_order_id)
        if (
            work_order is not None
            and work_order.artifact_type == "work_order"
            and active_record_status(artifact.artifact_type, artifact.status)
            and work_order.status not in IMPLEMENTED_OR_LATER_STATUSES
        ):
            add_error(
                errors,
                artifact,
                report_root,
                E010,
                f"active release record requires implemented, verified, or released work order '{work_order_id}'",
                plane="governance",
            )
    verification_work: set[str] = set()
    for verification_id in relation_targets(artifact, "includes_verification"):
        verification = catalog.get(verification_id)
        if verification is None or verification.artifact_type != "verification_record":
            continue
        if active_record_status(verification.artifact_type, verification.status):
            verification_work.update(relation_targets(verification, "verifies_work_order"))
        if active_record_status(artifact.artifact_type, artifact.status) and verification.status == "superseded":
            add_error(
                errors,
                artifact,
                report_root,
                E010,
                f"active release record must not include superseded verification record '{verification_id}'",
                plane="governance",
            )
        if release_commit != verification.metadata.get("commit") or release_format != verification.metadata.get("git_object_format"):
            add_error(
                errors,
                artifact,
                report_root,
                E010,
                f"release commit does not match verification record '{verification_id}'",
                plane="governance",
            )
        if (
            grants_authority(artifact.artifact_type, artifact.status)
            and not grants_authority(verification.artifact_type, verification.status)
        ):
            add_error(
                errors,
                artifact,
                report_root,
                E010,
                f"released record requires verified included record '{verification_id}'",
                plane="governance",
            )
    missing_work = released_work - verification_work
    if missing_work:
        add_error(
            errors,
            artifact,
            report_root,
            E010,
            f"released work orders are not covered by included verification records: {', '.join(sorted(missing_work))}",
            plane="governance",
        )
    extra_work = verification_work - released_work
    if extra_work:
        add_error(
            errors,
            artifact,
            report_root,
            E010,
            f"included verification records cover work orders absent from the release: {', '.join(sorted(extra_work))}",
            plane="governance",
        )
    for contract_id in relation_targets(artifact, "satisfies"):
        contract = catalog.get(contract_id)
        if contract is None or contract.artifact_type != "release_contract":
            continue
        if (
            active_record_status(artifact.artifact_type, artifact.status)
            and not grants_authority(contract.artifact_type, contract.status)
        ):
            add_error(
                errors,
                artifact,
                report_root,
                E010,
                f"active release record requires active release contract '{contract_id}'",
                plane="governance",
            )
        ungated = released_work - relation_targets(contract, "gates")
        if ungated:
            add_error(
                errors,
                artifact,
                report_root,
                E010,
                f"release contract '{contract_id}' does not gate work orders: {', '.join(sorted(ungated))}",
                plane="governance",
            )


def validate_revision_consistency(
    artifacts: list[Artifact],
    report_root: Path,
    *,
    require_verified_work: bool = False,
) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    catalog = {artifact.artifact_id: artifact for artifact in artifacts if artifact.artifact_id != "<unknown>"}
    release_versions: dict[str, list[Artifact]] = {}
    supersession_cycle_nodes = _supersession_cycle_nodes(artifacts)

    if require_verified_work:
        verified_work = {
            work_order_id
            for record in artifacts
            if record.artifact_type == "verification_record"
            and grants_authority(record.artifact_type, record.status)
            for work_order_id in relation_targets(record, "verifies_work_order")
        }
        for work_order in artifacts:
            if (
                work_order.artifact_type == "work_order"
                and work_order.status in {"verified", "released"}
                and work_order.artifact_id not in verified_work
            ):
                add_error(
                    errors,
                    work_order,
                    report_root,
                    E010,
                    f"{work_order.status} work order requires coverage by a verified or released verification record",
                    plane="policy",
                )

    for artifact in artifacts:
        if artifact.artifact_type == "verification_record":
            _check_verification_record(artifact, catalog, supersession_cycle_nodes, errors, report_root)

        if artifact.artifact_type != "release_record":
            continue
        _check_release_record(artifact, catalog, release_versions, errors, report_root)

    for version, records in sorted(release_versions.items()):
        if len(records) < 2:
            continue
        record_ids = ", ".join(sorted(record.artifact_id for record in records))
        for record in records:
            add_error(
                errors,
                record,
                report_root,
                E010,
                f"duplicate release record version '{version}' among {record_ids}",
                plane="governance",
            )
    return errors


def _supersession_cycle_nodes(artifacts: list[Artifact]) -> set[str]:
    graph = {
        artifact.artifact_id: sorted(relation_targets(artifact, "superseded_by"))
        for artifact in artifacts
        if artifact.artifact_type == "verification_record"
    }
    state: dict[str, int] = {}
    cycle_nodes: set[str] = set()

    for start in sorted(graph):
        if state.get(start, 0) != 0:
            continue
        path = [start]
        positions = {start: 0}
        frames = [(start, 0)]
        state[start] = 1
        while frames:
            node, successor_index = frames[-1]
            successors = graph.get(node, [])
            if successor_index >= len(successors):
                frames.pop()
                path.pop()
                positions.pop(node, None)
                state[node] = 2
                continue
            successor = successors[successor_index]
            frames[-1] = (node, successor_index + 1)
            if successor not in graph:
                continue
            successor_state = state.get(successor, 0)
            if successor_state == 0:
                state[successor] = 1
                positions[successor] = len(path)
                path.append(successor)
                frames.append((successor, 0))
            elif successor_state == 1:
                cycle_nodes.update(path[positions[successor] :])
    return cycle_nodes


def validate_operating_contract_readiness(
    artifacts: list[Artifact],
    report_root: Path,
    *,
    require_verified_work: bool = False,
) -> list[Diagnostic]:
    """Validate the implementation path behind each active OPS assurance claim."""

    errors: list[Diagnostic] = []
    catalog = {
        artifact.artifact_id: artifact
        for artifact in artifacts
        if artifact.artifact_id != "<unknown>"
    }
    completed_work_by_requirement: dict[str, set[str]] = {}
    for work_order in artifacts:
        if (
            work_order.artifact_type != "work_order"
            or work_order.status not in IMPLEMENTED_OR_LATER_STATUSES
        ):
            continue
        for requirement_id in relation_targets(work_order, "implements"):
            completed_work_by_requirement.setdefault(requirement_id, set()).add(
                work_order.artifact_id
            )

    verified_work = {
        work_order_id
        for record in artifacts
        if record.artifact_type == "verification_record"
        and grants_authority(record.artifact_type, record.status)
        for work_order_id in relation_targets(record, "verifies_work_order")
    }

    for contract in artifacts:
        if (
            contract.artifact_type != "operating_contract"
            or not grants_authority(contract.artifact_type, contract.status)
        ):
            continue
        for requirement_id in sorted(relation_targets(contract, "assures")):
            requirement = catalog.get(requirement_id)
            # Missing and wrong-type targets are owned by validate_relations.
            if requirement is None or requirement.artifact_type != "requirement":
                continue
            if not grants_authority(requirement.artifact_type, requirement.status):
                add_error(
                    errors,
                    contract,
                    report_root,
                    E017,
                    f"active operating contract assures inactive requirement '{requirement_id}'",
                    plane="governance",
                )
                continue

            completed_work = completed_work_by_requirement.get(requirement_id, set())
            if not completed_work:
                add_error(
                    errors,
                    contract,
                    report_root,
                    E017,
                    f"active operating contract assures requirement '{requirement_id}' without completed implementing work",
                    plane="governance",
                )
                continue

            if require_verified_work and completed_work.isdisjoint(verified_work):
                add_error(
                    errors,
                    contract,
                    report_root,
                    E018,
                    f"active operating contract assures requirement '{requirement_id}' without a verified or released VREC covering completed implementing work",
                    plane="policy",
                )

    return errors
