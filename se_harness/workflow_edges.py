"""The lifecycle edges (SPEC-ECP-024 ECP-ENG-019): the registry the workflow reads, the edge check with its refusal, the revision policy reader and the graph-structural checks bound to a transition.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

from se_harness.codes import CodedError, WEX_ECP_030
from se_harness.decisions import validate_disposition_request
from se_harness.engine.validation_core import relation_targets
from se_harness.installer import HarnessError
from se_harness.integrity import IntegrityError, read_toml
from se_harness.risks import validate_risk_edge
from se_harness.workflow_contract import (
    lifecycle_family,
    load_validated_contracts,
    load_workflow_contract,
    transition_binding,
    validate_lifecycle_registry,
)


WORKFLOW_CONTRACT = load_workflow_contract()

LIFECYCLE_REGISTRY = validate_lifecycle_registry(WORKFLOW_CONTRACT)

# Compatibility projection for callers that only need transition edges.  The
# lifecycle registry remains the sole policy source.
TRANSITIONS: dict[str, dict[str, set[str]]] = {
    family: {
        source: set(row.transitions_to)
        for source, row in states.items()
    }
    for family, states in LIFECYCLE_REGISTRY.items()
}


_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


class PreconditionError(HarnessError):
    """A refused transition, labelled by the check that refused it (ECP-KRN-008)."""

    def __init__(self, predicate_id: str, message: str) -> None:
        super().__init__(message)
        self.predicate_id = predicate_id
        # ECP-PRM-017: the two attributes of a coded refusal; the wire form stays the bare message,
        # the CLI labelling it with the predicate.
        self.code = predicate_id
        self.message = message


def _assertion(value: str, label: str, *, limit: int) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit or _CONTROL.search(value):
        raise HarnessError(f"{label} must be non-empty, single-line text of at most {limit} characters")
    return value.strip()


def grants_authority(family: str, status: str) -> bool:
    row = LIFECYCLE_REGISTRY.get(family, {}).get(status)
    return bool(row and row.grants_authority)


def revision_policy(root: Path) -> dict[str, bool]:
    # ECP-PRM-011: the one configuration reader; an unreadable file is the policy's default.
    path = root / ".engineering-harness.toml"
    if not path.is_file():
        return {"required_for_verified_work": False, "required_for_release": False}
    try:
        data = read_toml(path)
    except IntegrityError:
        return {"required_for_verified_work": False, "required_for_release": False}
    table = data.get("revision_provenance", {})
    return {
        name: bool(table.get(name, False)) if isinstance(table, dict) else False
        for name in ("required_for_verified_work", "required_for_release")
    }


def validate_edge(
    root: Path,
    artifact: Any,
    target: str,
    actor: str,
    reason: str | None,
    catalog: Mapping[str, Any] | None = None,
    disposition: Mapping[str, Any] | None = None,
    policy: Mapping[str, bool] | None = None,
) -> Mapping[str, Any] | None:
    family = lifecycle_family(artifact.artifact_type)
    row = LIFECYCLE_REGISTRY.get(family, {}).get(artifact.status)
    if row is None or target not in row.transitions_to:
        raise PreconditionError("QGS-EDGE", f"transition {artifact.artifact_id}: {artifact.status} -> {target} is not allowed")
    _assertion(actor, f"decision actor for {artifact.artifact_id}", limit=128)
    if artifact.artifact_type == "decision":
        # SPEC-DCM-001 rules 6 to 8: a decision is disposed through `decide`, which
        # supplies the option, the scope and the revisit the transition records;
        # without them only the lifecycle edge is checked (the planner refuses).
        if disposition is None:
            return None
        if reason is not None:
            _assertion(reason, f"reason for {artifact.artifact_id}", limit=2000)
        return validate_disposition_request(
            artifact,
            catalog or {},
            target=target,
            option=disposition.get("option"),
            actor=actor,
            reason=reason,
            revisit=disposition.get("revisit"),
            scope=tuple(disposition.get("scope") or ()),
        )
    if artifact.artifact_type == "risk":
        # SPEC-RSK-010 RSK-MGT-016 to RSK-MGT-021: a raised risk moves only through the
        # decision that names it; `decide` supplies the option the transition copies.
        if reason is not None:
            _assertion(reason, f"reason for {artifact.artifact_id}", limit=2000)
        return validate_risk_edge(artifact, catalog or {}, target=target, actor=actor, reason=reason, disposition=disposition)
    if target in {"rejected", "superseded"}:
        if reason is None:
            detail = "successor VREC ID" if target == "superseded" else "rejection reason"
            raise HarnessError(f"transition {artifact.artifact_id} to {target} requires --reason with a {detail}")
        _assertion(reason, f"reason for {artifact.artifact_id}", limit=2000)
    elif reason is not None:
        _assertion(reason, f"reason for {artifact.artifact_id}", limit=2000)
    if policy is None:
        policy = revision_policy(root)  # ECP-PRM-011: the planner passes its one reading
    if family == "work_order" and artifact.status in {"implemented", "verified"}:
        setting = "required_for_verified_work" if target == "verified" else "required_for_release"
        if not policy[setting]:
            raise PreconditionError("QGS-EDGE", f"work order transition to {target} is not enabled by revision provenance policy")
    return None


def _structural(predicate_id: str, status: str, message: str, artifact_id: str) -> dict[str, Any]:
    return {
        "id": predicate_id,
        "status": status,
        "evidence": [{"kind": "artifact", "reference": artifact_id}],
        "message": message,
    }


def structural_precondition_results(
    root: Path,
    catalog: Mapping[str, Any],
    proposed_catalog: Mapping[str, Any],
    artifact: Any,
    target: str,
    reason: str | None,
    policy: Mapping[str, bool] | None = None,
) -> list[dict[str, Any]]:
    """Evaluate the graph-structural checks bound to one edge (ECP-KRN-005).

    These are properties of the artifact graph shape alone; every other
    precondition is a gate predicate in `QUALITY_GATES.json`. Each check is
    reported as a `QGS-` predicate so a refusal names it.
    """

    _, quality, _, _, _ = load_validated_contracts()
    _, structural_ids = transition_binding(quality, lifecycle_family(artifact.artifact_type), artifact.artifact_type, target)
    artifact_id = artifact.artifact_id
    results: list[dict[str, Any]] = []
    for check in structural_ids:
        if check == "QGS-EDGE":
            family = lifecycle_family(artifact.artifact_type)
            row = LIFECYCLE_REGISTRY.get(family, {}).get(artifact.status)
            if row is None or target not in row.transitions_to:
                results.append(_structural(check, "fail", f"transition {artifact_id}: {artifact.status} -> {target} is not allowed", artifact_id))
                continue
            if policy is None:
                policy = revision_policy(root)
            if family == "work_order" and artifact.status in {"implemented", "verified"}:
                setting = "required_for_verified_work" if target == "verified" else "required_for_release"
                if not policy[setting]:
                    results.append(_structural(check, "fail", f"work order transition to {target} is not enabled by revision provenance policy", artifact_id))
                    continue
            results.append(_structural(check, "pass", f"{artifact.status} -> {target} is a declared lifecycle edge for {artifact_id}.", artifact_id))
        elif check == "QGS-ASSURANCE":
            assurance = artifact.metadata.get("assurance")
            if not isinstance(assurance, dict) or assurance.get("commit_bound_verification") not in {"required", "not_required"}:
                results.append(_structural(check, "fail", f"work order {artifact_id} requires a complete assurance classification before approval", artifact_id))
            else:
                results.append(_structural(check, "pass", f"{artifact_id} classifies commit-bound verification as {assurance['commit_bound_verification']}.", artifact_id))
        elif check == "QGS-VREC-COVERAGE":
            covered = [
                item for item in proposed_catalog.values()
                if item.artifact_type == "verification_record"
                and grants_authority("verification_record", item.status)
                and artifact_id in relation_targets(item, "verifies_work_order")
            ]
            if covered:
                results.append(_structural(check, "pass", f"{artifact_id} is covered by eligible verification record {sorted(item.artifact_id for item in covered)[0]}.", artifact_id))
            else:
                results.append(_structural(check, "fail", f"work order {artifact_id} has no direct eligible verification record", artifact_id))
        elif check == "QGS-RLS-COVERAGE":
            covered = [
                item for item in proposed_catalog.values()
                if item.artifact_type == "release_record"
                and grants_authority("release_record", item.status)
                and artifact_id in relation_targets(item, "releases_work")
            ]
            if covered:
                results.append(_structural(check, "pass", f"{artifact_id} is released by {sorted(item.artifact_id for item in covered)[0]}.", artifact_id))
            else:
                results.append(_structural(check, "fail", f"work order {artifact_id} has no direct released release record", artifact_id))
        elif check == "QGS-VERIFIED-INCLUSION":
            missing = [
                vrec_id for vrec_id in sorted(relation_targets(artifact, "includes_verification"))
                if vrec_id not in proposed_catalog
                or not grants_authority("verification_record", proposed_catalog[vrec_id].status)
            ]
            if missing:
                results.append(_structural(check, "fail", f"release record {artifact_id} requires verified VREC {missing[0]}", artifact_id))
            else:
                results.append(_structural(check, "pass", f"Every verification record {artifact_id} includes is verified.", artifact_id))
        elif check == "QGS-SUCCESSOR":
            successor_id = reason
            successor = proposed_catalog.get(successor_id) if successor_id else None
            if successor_id is None:
                results.append(_structural(check, "not_assessable", f"supersession of {artifact_id} names no successor VREC", artifact_id))
            elif successor is None or successor.artifact_type != "verification_record":
                results.append(_structural(check, "fail", f"supersession successor is not a VREC: {successor_id}", artifact_id))
            elif not grants_authority("verification_record", successor.status):
                results.append(_structural(check, "fail", f"supersession successor {successor_id} must be verified or released", artifact_id))
            elif not relation_targets(artifact, "verifies_work_order").issubset(relation_targets(successor, "verifies_work_order")):
                results.append(_structural(check, "fail", f"supersession successor {successor_id} does not preserve work coverage", artifact_id))
            else:
                results.append(_structural(check, "pass", f"{successor_id} is an eligible successor preserving the coverage of {artifact_id}.", artifact_id))
        else:  # pragma: no cover - the loader rejects unknown structural ids
            raise CodedError(WEX_ECP_030, f"unknown structural check {check}")
    return results
