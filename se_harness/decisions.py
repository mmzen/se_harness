"""The decision artifact: disposition of a pending decision (SPEC-DCM-001).

A decision (`DEC-`) blocks the transitions of the artifacts it names while it
is `open`. The accountable role disposes it with one declared option; the
tool records the option identifier, its label, the role, the time and the
verbatim reason as the decision's `[disposition]` table and lifecycle event.
`deferred` needs a scope of admitted transitions and a revisit trigger;
`accept` on a deviation needs a revisit trigger. Every rule here is
SPEC-DCM-001 rules 2 to 8; the gate that reads the result is
`decision_gate_clear` in `workflow_compliance`.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

from se_harness.installer import HarnessError

DECISION_KINDS = ("question", "deviation")
DEVIATION_OPTIONS = ("amend", "supersede", "accept", "stop")
BLOCKABLE_TYPES = frozenset({"requirement", "specification", "verification", "architecture", "adr", "work_order"})
OPTION_ID = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
#: `ARTIFACT-ID:FROM-TO`, the transition a deferral admits.
SCOPE_ENTRY = re.compile(r"^([A-Z][A-Z0-9-]*-\d{3}):([a-z_]+)-([a-z_]+)$")
DISPOSITION_FIELDS = ("option", "label", "decided_by", "decided_at", "reason", "revisit", "scope")


def decision_table(artifact: Any) -> Mapping[str, Any]:
    """The decision's own front-matter fields (top level, no table)."""

    return artifact.metadata if isinstance(artifact.metadata, Mapping) else {}


def declared_options(artifact: Any) -> list[dict[str, str]]:
    raw = decision_table(artifact).get("options")
    options: list[dict[str, str]] = []
    if not isinstance(raw, list):
        return options
    for item in raw:
        if isinstance(item, Mapping) and isinstance(item.get("id"), str) and isinstance(item.get("label"), str):
            options.append({"id": item["id"], "label": item["label"]})
    return options


def against_reference(artifact: Any) -> tuple[str, str] | None:
    """(artifact id, rule reference) from a deviation's `against`, or None."""

    value = decision_table(artifact).get("against")
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"([A-Z][A-Z0-9-]*-\d{3})#([A-Za-z0-9._-]+)", value.strip())
    if match is None:
        return None
    return match.group(1), match.group(2)


def deferral_scope(artifact: Any) -> tuple[str, ...]:
    disposition = decision_table(artifact).get("disposition")
    if not isinstance(disposition, Mapping):
        return ()
    raw = disposition.get("scope")
    if not isinstance(raw, list):
        return ()
    return tuple(item for item in raw if isinstance(item, str))


def scope_admits(scope: tuple[str, ...], artifact_id: str, source: str, target: str) -> bool:
    return f"{artifact_id}:{source}-{target}" in scope


def _owners(artifact: Any) -> set[str]:
    owners = artifact.metadata.get("owners") if isinstance(artifact.metadata, Mapping) else None
    return {item for item in owners if isinstance(item, str)} if isinstance(owners, list) else set()


def deciding_roles(decision: Any, catalog: Mapping[str, Any]) -> set[str]:
    """The roles that hold DR-DECISION-DISPOSE for this decision (SPEC-DCM-001 rule 7).

    A deviation is disposed by the owners named on the specification it departs
    from; a question by the owners named on the artifacts it blocks. A work
    order among the blocked artifacts adds the engineering owner, who holds its
    decision rights.
    """

    relations = decision.relations if isinstance(getattr(decision, "relations", None), Mapping) else {}
    if decision_table(decision).get("kind") == "deviation":
        reference = against_reference(decision)
        target = catalog.get(reference[0]) if reference else None
        return _owners(target) if target is not None else set()
    roles: set[str] = set()
    for target_id in relations.get("blocks", []) if isinstance(relations.get("blocks"), list) else []:
        target = catalog.get(target_id)
        if target is None:
            continue
        roles.update(_owners(target))
        if target.artifact_type == "work_order":
            roles.add("engineering-owner")
    return roles


def validate_disposition_request(
    decision: Any,
    catalog: Mapping[str, Any],
    *,
    target: str,
    option: str | None,
    actor: str,
    reason: str | None,
    revisit: str | None,
    scope: tuple[str, ...],
) -> dict[str, str | list[str]]:
    """Check one disposition request and return the `[disposition]` fields to write."""

    if decision.artifact_type != "decision":
        raise HarnessError(f"{decision.artifact_id} is not a decision")
    if decision.status not in {"open", "deferred"}:
        raise HarnessError(f"decision {decision.artifact_id} is {decision.status}; only an open or deferred decision is disposed")
    roles = deciding_roles(decision, catalog)
    if actor not in roles:
        holders = ", ".join(sorted(roles)) if roles else "no role (the decision blocks nothing readable)"
        raise HarnessError(
            f"DR-DECISION-DISPOSE: {decision.artifact_id} is disposed by {holders}, not {actor}"
        )
    if not reason or not reason.strip():
        raise HarnessError(f"disposing {decision.artifact_id} requires --reason with the verbatim answer")
    fields: dict[str, str | list[str]] = {"decided_by": actor, "reason": reason}
    if target == "withdrawn":
        fields["option"] = "withdrawn"
        fields["label"] = "The question no longer applies."
        return fields
    if target == "deferred":
        if not scope:
            raise HarnessError(f"deferring {decision.artifact_id} requires --scope ARTIFACT-ID:FROM-TO for every admitted transition")
        for entry in scope:
            match = SCOPE_ENTRY.fullmatch(entry)
            if match is None:
                raise HarnessError(f"deferral scope entry is not ARTIFACT-ID:FROM-TO: {entry}")
            blocked = decision.relations.get("blocks", []) if isinstance(decision.relations, Mapping) else []
            if match.group(1) not in blocked:
                raise HarnessError(f"deferral scope names {match.group(1)}, which {decision.artifact_id} does not block")
        if not revisit or not revisit.strip():
            raise HarnessError(f"deferring {decision.artifact_id} requires --revisit naming a release, a date, or an artifact state")
        fields["option"] = "deferred"
        fields["label"] = "Deferred with a scope of admitted transitions."
        fields["scope"] = list(scope)
        fields["revisit"] = revisit
        return fields
    options = {item["id"]: item["label"] for item in declared_options(decision)}
    if option is None or option not in options:
        declared = ", ".join(sorted(options)) or "none declared"
        raise HarnessError(f"decision {decision.artifact_id} declares options {declared}; --option must name one")
    fields["option"] = option
    fields["label"] = options[option]
    if decision_table(decision).get("kind") == "deviation" and option == "accept":
        if not revisit or not revisit.strip():
            raise HarnessError(f"accepting the deviation {decision.artifact_id} requires --revisit; acceptance is time-bounded")
        fields["revisit"] = revisit
    elif revisit:
        fields["revisit"] = revisit
    return fields


def dispose_decision(
    repository: Path,
    decision_id: str,
    *,
    option: str | None,
    actor: str,
    reason: str | None,
    defer: bool = False,
    withdraw: bool = False,
    scope: tuple[str, ...] = (),
    revisit: str | None = None,
    apply: bool = False,
) -> Any:
    """Plan or apply one disposition through the atomic transition path."""

    from se_harness.workflow import plan_transition

    if defer and withdraw:
        raise HarnessError("--defer and --withdraw are exclusive")
    if withdraw:
        target = "withdrawn"
    elif defer:
        target = "deferred"
    else:
        target = "decided"
    request = {
        "target": target,
        "option": option,
        "revisit": revisit,
        "scope": tuple(scope),
    }
    return plan_transition(
        repository,
        {decision_id: target},
        {decision_id: actor},
        {decision_id: reason} if reason is not None else {},
        apply=apply,
        dispositions={decision_id: request},
    )
