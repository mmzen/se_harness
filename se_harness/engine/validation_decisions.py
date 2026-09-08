"""The decisions seam: decision assessments, work-order assurance, delegation and scope, decisions and risks.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any

from se_harness.codes import (
    E014,
    E015,
    E019,
    E020,
    E_DCM_001,
    E_DCM_002,
    E_DCM_003,
    E_DCM_005,
    E_ECP_001,
    E_RSK_001,
    E_RSK_002,
    E_RSK_003,
    E_RSK_004,
    E_RSK_005,
    W014,
    W_DCM_001,
    W_DCM_002,
    W_RSK_001,
)
from se_harness.workflow_contract import IMPLEMENTED_OR_LATER_STATUSES
from se_harness.engine.validation_authoring import sentences, specification_rules
from se_harness.engine.validation_core import (
    Artifact,
    Diagnostic,
    add_error,
    display_path,
    duplicate_strings,
    relation_targets,
)
from se_harness.engine.validation_lifecycle import grants_authority


DECISION_ASSESSMENT_OUTCOMES = {"adr_required", "no_significant_decision"}

DECISION_TRIGGERS = {
    "system-boundary",
    "responsibility-or-dependency-direction",
    "public-interface-or-protocol",
    "data-ownership-or-persistence",
    "security-privacy-or-trust-boundary",
    "deployment-or-operating-model",
    "concurrency-consistency-reliability-or-failure-strategy",
    "technology-framework-vendor-or-external-service",
    "material-performance-scalability-or-cost-tradeoff",
    "cross-cutting-policy",
    "difficult-to-reverse",
    "material-alternatives",
}


MAX_ASSESSMENT_RATIONALE_LENGTH = 2000

MAX_ASSESSOR_LENGTH = 128

WORK_ORDER_ASSURANCE_VALUES = {"required", "not_required"}

WORK_ORDER_ASSURANCE_FIELDS = {
    "commit_bound_verification",
    "rationale",
    "decided_by",
}


MAX_ASSURANCE_RATIONALE_LENGTH = 2000

MAX_ASSURANCE_DECIDER_LENGTH = 128

#: SPEC-DCM-001 rules 2 and 3: the decision kinds and the closed option set of a deviation.
DECISION_KINDS = ("question", "deviation")

DEVIATION_OPTIONS = frozenset({"amend", "supersede", "accept", "stop"})

DECISION_TERMINAL = frozenset({"decided", "withdrawn"})

#: SPEC-RSK-010 RSK-MGT-002 to RSK-MGT-005: the risk's declared fields, the closed
#: stage and category sets, and the five-by-five measurement.
RISK_REQUIRED_FIELDS = ("cause", "effect", "stage", "category", "likelihood", "impact", "score", "raised_by")

RISK_STAGES = frozenset({"definition", "architecture", "implementation", "verification", "release", "operation"})

RISK_CATEGORIES = frozenset({"safety", "security", "compliance", "process", "schedule", "quality"})

RISK_MEASUREMENT_RANGE = range(1, 6)

#: RSK-MGT-008: the retained end states; RSK-MGT-018: the states a disposition writes.
RISK_TERMINAL = frozenset({"accepted", "avoided", "mitigated", "withdrawn"})

RISK_DISPOSED = frozenset({"accepted", "avoided", "mitigating", "mitigated", "withdrawn"})

#: RSK-MGT-016 and RSK-MGT-020: the option of the paired decision and the risk state it names.
RISK_OPTION_TARGETS = {"accept": "accepted", "avoid": "avoided", "mitigate": "mitigating"}


def decision_assessment_state(artifact: Artifact) -> dict[str, Any]:
    """Return a deterministic, non-authoritative architecture assessment state."""

    raw = artifact.metadata.get("decision_assessment")
    if artifact.artifact_type != "architecture":
        return {
            "state": "invalid" if raw is not None else "not_applicable",
            "outcome": None,
            "triggers": [],
            "rationale": None,
            "assessed_by": None,
            "issues": ["decision_assessment is allowed only on architecture artifacts"] if raw is not None else [],
        }
    if raw is None:
        legacy = artifact.status in IMPLEMENTED_OR_LATER_STATUSES
        return {
            "state": "legacy_missing" if legacy else "missing",
            "outcome": None,
            "triggers": [],
            "rationale": None,
            "assessed_by": None,
            "issues": [] if legacy else ["architecture decision assessment is required"],
        }
    if not isinstance(raw, dict):
        return {
            "state": "invalid",
            "outcome": None,
            "triggers": [],
            "rationale": None,
            "assessed_by": None,
            "issues": ["decision_assessment must be a TOML table"],
        }

    issues: list[str] = []
    outcome_value = raw.get("outcome")
    outcome = outcome_value.strip() if isinstance(outcome_value, str) else None
    if outcome not in DECISION_ASSESSMENT_OUTCOMES:
        issues.append("decision_assessment outcome must be adr_required or no_significant_decision")

    triggers_value = raw.get("triggers")
    triggers: list[str] = []
    if not isinstance(triggers_value, list):
        issues.append("decision_assessment triggers must be an array")
    else:
        invalid_items = [item for item in triggers_value if not isinstance(item, str) or not item.strip()]
        if invalid_items:
            issues.append("decision_assessment triggers contain a non-string or empty value")
        triggers = [item.strip() for item in triggers_value if isinstance(item, str) and item.strip()]
        duplicates = duplicate_strings(triggers_value)
        if duplicates:
            issues.append(f"decision_assessment triggers contain duplicates: {', '.join(duplicates)}")
        unknown = sorted(set(triggers) - DECISION_TRIGGERS)
        if unknown:
            issues.append(f"decision_assessment triggers are unknown: {', '.join(unknown)}")

    rationale_value = raw.get("rationale")
    rationale = rationale_value.strip() if isinstance(rationale_value, str) else None
    if not rationale:
        issues.append("decision_assessment rationale must be a non-empty string")
    elif len(rationale) > MAX_ASSESSMENT_RATIONALE_LENGTH:
        issues.append(
            f"decision_assessment rationale exceeds {MAX_ASSESSMENT_RATIONALE_LENGTH} characters"
        )

    assessor_value = raw.get("assessed_by")
    assessed_by = assessor_value.strip() if isinstance(assessor_value, str) else None
    if not assessed_by:
        issues.append("decision_assessment assessed_by must be a non-empty string")
    elif len(assessed_by) > MAX_ASSESSOR_LENGTH:
        issues.append(f"decision_assessment assessed_by exceeds {MAX_ASSESSOR_LENGTH} characters")

    unknown_fields = sorted(set(raw) - {"outcome", "triggers", "rationale", "assessed_by"})
    if unknown_fields:
        issues.append(f"decision_assessment contains unknown fields: {', '.join(unknown_fields)}")
    if outcome == "adr_required" and not triggers:
        issues.append("adr_required decision assessment must declare at least one trigger")
    if outcome == "no_significant_decision" and triggers:
        issues.append("no_significant_decision assessment must not declare triggers")

    return {
        "state": "invalid" if issues else "valid",
        "outcome": outcome,
        "triggers": sorted(set(triggers)),
        "rationale": rationale,
        "assessed_by": assessed_by,
        "issues": issues,
    }


def work_order_assurance_state(artifact: Artifact) -> dict[str, Any]:
    """Return the explicit commit-bound assurance classification for a work order."""

    raw = artifact.metadata.get("assurance")
    if artifact.artifact_type != "work_order":
        return {
            "state": "invalid" if raw is not None else "not_applicable",
            "commit_bound_verification": None,
            "rationale": None,
            "decided_by": None,
            "issues": ["assurance is allowed only on work-order artifacts"] if raw is not None else [],
        }
    if raw is None:
        return {
            "state": "missing",
            "commit_bound_verification": None,
            "rationale": None,
            "decided_by": None,
            "issues": [],
        }
    if not isinstance(raw, dict):
        return {
            "state": "invalid",
            "commit_bound_verification": None,
            "rationale": None,
            "decided_by": None,
            "issues": ["assurance must be a TOML table"],
        }

    issues: list[str] = []
    classification_value = raw.get("commit_bound_verification")
    classification = (
        classification_value.strip()
        if isinstance(classification_value, str)
        else None
    )
    if classification not in WORK_ORDER_ASSURANCE_VALUES:
        issues.append(
            "assurance commit_bound_verification must be required or not_required"
        )

    rationale_value = raw.get("rationale")
    rationale = rationale_value.strip() if isinstance(rationale_value, str) else None
    if not rationale:
        issues.append("assurance rationale must be a non-empty string")
    elif len(rationale) > MAX_ASSURANCE_RATIONALE_LENGTH:
        issues.append(
            f"assurance rationale exceeds {MAX_ASSURANCE_RATIONALE_LENGTH} characters"
        )

    decider_value = raw.get("decided_by")
    decided_by = decider_value.strip() if isinstance(decider_value, str) else None
    if not decided_by:
        issues.append("assurance decided_by must be a non-empty string")
    elif len(decided_by) > MAX_ASSURANCE_DECIDER_LENGTH:
        issues.append(
            f"assurance decided_by exceeds {MAX_ASSURANCE_DECIDER_LENGTH} characters"
        )

    unknown_fields = sorted(set(raw) - WORK_ORDER_ASSURANCE_FIELDS)
    if unknown_fields:
        issues.append(f"assurance contains unknown fields: {', '.join(unknown_fields)}")

    return {
        "state": "invalid" if issues else "valid",
        "commit_bound_verification": classification,
        "rationale": rationale,
        "decided_by": decided_by,
        "issues": issues,
    }


def validate_work_order_assurance(
    artifacts: list[Artifact],
    report_root: Path,
) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    for artifact in artifacts:
        assurance = work_order_assurance_state(artifact)
        for issue in assurance["issues"]:
            add_error(
                errors,
                artifact,
                report_root,
                E019,
                issue,
                plane="governance",
            )
        if (
            artifact.artifact_type == "work_order"
            and assurance["state"] == "missing"
            and artifact.status in {"approved", "in_progress"}
        ):
            add_error(
                errors,
                artifact,
                report_root,
                E019,
                "approved or in-progress work order requires an explicit assurance classification",
                plane="governance",
            )
    return errors


def _execution_scope_path_issue(value: object) -> str | None:
    if not isinstance(value, str) or not value or len(value) > 4096:
        return "path must be non-empty text of at most 4096 characters"
    if re.search(r"[\x00-\x1f\x7f]", value):
        return "path contains a control character"
    if "\\" in value or ":" in value or any(token in value for token in ("*", "?", "[", "]")):
        return "path contains an alternate separator, drive/URI marker, or wildcard"
    directory = value.endswith("/")
    candidate = value[:-1] if directory else value
    if not candidate or candidate.startswith("/"):
        return "path is empty or absolute"
    parts = PurePosixPath(candidate).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        return "path contains an empty or dot component"
    reserved = {"CON", "PRN", "AUX", "NUL"} | {
        f"{prefix}{index}" for prefix in ("COM", "LPT") for index in range(1, 10)
    }
    for part in parts:
        if part.endswith((".", " ")) or part.rstrip(". ").split(".", 1)[0].upper() in reserved:
            return "path contains a reserved device or trailing dot/space component"
    normalized = PurePosixPath(*parts).as_posix() + ("/" if directory else "")
    if normalized != value:
        return "path is not normalized"
    return None


def validate_work_order_delegation(
    artifacts: list[Artifact],
    report_root: Path,
) -> list[Diagnostic]:
    """SPEC-ECP-006 ECP-DLG-001: `[delegation]` carries exactly `class = "execution"` on a work order."""

    errors: list[Diagnostic] = []
    for artifact in artifacts:
        table = artifact.metadata.get("delegation")
        if table is None:
            continue
        if artifact.artifact_type != "work_order":
            add_error(errors, artifact, report_root, E_ECP_001, "delegation is allowed only on work-order artifacts", plane="governance")
            continue
        if not isinstance(table, dict) or set(table) != {"class"}:
            add_error(errors, artifact, report_root, E_ECP_001, "delegation must contain exactly class", plane="governance")
            continue
        if table.get("class") != "execution":
            add_error(errors, artifact, report_root, E_ECP_001, f"delegation.class must be \"execution\", not {table.get('class')!r}", plane="governance")
    return errors


def validate_work_order_execution_scope(
    artifacts: list[Artifact],
    report_root: Path,
) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    for artifact in artifacts:
        if artifact.artifact_type != "work_order":
            continue
        table = artifact.metadata.get("execution_scope")
        if table is None:
            # Compatibility: the validator cannot infer whether an active work
            # order predates this contract. Checkpoint evaluation treats an
            # absent scope as not assessable; authoring templates require it for
            # new or resumed implementation.
            continue
        if not isinstance(table, dict) or set(table) != {"paths"}:
            add_error(
                errors,
                artifact,
                report_root,
                E020,
                "execution_scope must contain only paths",
                plane="governance",
            )
            continue
        paths = table.get("paths")
        if not isinstance(paths, list) or not paths:
            add_error(
                errors,
                artifact,
                report_root,
                E020,
                "execution_scope.paths must be a non-empty array",
                plane="governance",
            )
            continue
        folded: dict[str, str] = {}
        for value in paths:
            issue = _execution_scope_path_issue(value)
            if issue is not None:
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E020,
                    f"invalid execution scope path {value!r}: {issue}",
                    plane="governance",
                )
                continue
            key = value.casefold()
            if key in folded:
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E020,
                    f"duplicate or case-ambiguous execution scope path: {value!r}",
                    plane="governance",
                )
            folded[key] = value
    return errors


def validate_decision_assessments(
    artifacts: list[Artifact],
    report_root: Path,
) -> tuple[list[Diagnostic], list[Diagnostic]]:
    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    active_decisions_by_architecture: dict[str, set[str]] = {}
    for decision in artifacts:
        if decision.artifact_type != "adr" or not grants_authority(decision.artifact_type, decision.status):
            continue
        for architecture_id in relation_targets(decision, "decides"):
            active_decisions_by_architecture.setdefault(architecture_id, set()).add(decision.artifact_id)

    for artifact in artifacts:
        assessment = decision_assessment_state(artifact)
        if artifact.artifact_type != "architecture":
            for issue in assessment["issues"]:
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E014,
                    issue,
                    plane="governance",
                )
            continue

        state = assessment["state"]
        if state in {"missing", "invalid"}:
            for issue in assessment["issues"]:
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E014,
                    issue,
                    plane="governance",
                )
            continue
        deciding = active_decisions_by_architecture.get(artifact.artifact_id, set())
        if state == "legacy_missing":
            warnings.append(
                Diagnostic(
                    display_path(artifact.path, report_root),
                    W014,
                    "completed legacy architecture has no decision_assessment; migrate during the compatibility window",
                    "maintenance",
                )
            )
            if not deciding:
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E015,
                    "completed legacy architecture without decision_assessment requires an active deciding ADR",
                    plane="governance",
                )
            continue
        if (
            grants_authority(artifact.artifact_type, artifact.status)
            and assessment["outcome"] == "adr_required"
            and not deciding
        ):
            add_error(
                errors,
                artifact,
                report_root,
                E015,
                "adr_required architecture has no active ADR whose decides relation targets it",
                plane="governance",
            )
    return errors, warnings


def _decision_against(artifact: Artifact) -> tuple[str, str] | None:
    value = artifact.metadata.get("against")
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"([A-Z][A-Z0-9-]*-\d{3})#([A-Za-z0-9._-]+)", value.strip())
    return (match.group(1), match.group(2)) if match else None


def _decision_options(artifact: Artifact) -> list[dict[str, str]]:
    raw = artifact.metadata.get("options")
    if not isinstance(raw, list):
        return []
    return [
        {"id": item["id"], "label": item["label"]}
        for item in raw
        if isinstance(item, dict) and isinstance(item.get("id"), str) and isinstance(item.get("label"), str)
    ]


def standing_deviations(artifacts: list[Artifact]) -> dict[str, list[str]]:
    """Artifact id -> accepted deviations standing on it (SPEC-DCM-001 rule 9).

    An accepted deviation stands on the specification it departs from, on every
    work order it concerns, and on every verification or release record whose
    covered work includes one of those work orders, until a later decided
    deviation against the same rule chose `amend` or `supersede`.
    """

    closed_rules: set[str] = set()
    accepted: list[Artifact] = []
    for artifact in artifacts:
        if artifact.artifact_type != "decision" or artifact.metadata.get("kind") != "deviation":
            continue
        disposition = artifact.metadata.get("disposition")
        option = disposition.get("option") if isinstance(disposition, dict) else None
        reference = _decision_against(artifact)
        if artifact.status != "decided" or reference is None:
            continue
        if option in {"amend", "supersede"}:
            closed_rules.add(f"{reference[0]}#{reference[1]}")
        elif option == "accept":
            accepted.append(artifact)
    standing: dict[str, set[str]] = defaultdict(set)
    for artifact in accepted:
        reference = _decision_against(artifact)
        assert reference is not None
        if f"{reference[0]}#{reference[1]}" in closed_rules:
            continue
        standing[reference[0]].add(artifact.artifact_id)
        relations = artifact.metadata.get("relations", {})
        concerned = relations.get("concerns", []) if isinstance(relations, dict) else []
        work_orders = {item for item in concerned if isinstance(item, str) and item.startswith("WO-")}
        for work_order in work_orders:
            standing[work_order].add(artifact.artifact_id)
        for record in artifacts:
            if record.artifact_type not in {"verification_record", "release_record"}:
                continue
            record_relations = record.metadata.get("relations", {})
            if not isinstance(record_relations, dict):
                continue
            covered = set()
            for relation in ("verifies_work_order", "releases_work"):
                values = record_relations.get(relation, [])
                covered.update(item for item in values if isinstance(item, str)) if isinstance(values, list) else None
            if covered & work_orders:
                standing[record.artifact_id].add(artifact.artifact_id)
    return {key: sorted(value) for key, value in sorted(standing.items())}


def _check_deviation_fields(
    artifact: Artifact,
    reference: tuple[str, str] | None,
    option_ids: list[str],
    catalog: dict[str, Artifact],
    errors: list[Diagnostic],
    report_root: Path,
) -> None:
    """Check a deviation's departed rule reference, observed fact and option set."""
    if reference is None:
        add_error(errors, artifact, report_root, E_DCM_002, "a deviation names the departed rule as against = \"ARTIFACT-ID#rule\"", plane="structure")
    elif reference[0] not in catalog:
        add_error(errors, artifact, report_root, E_DCM_001, f"deviation departs from unknown artifact '{reference[0]}'", plane="governance")
    elif catalog[reference[0]].artifact_type != "specification":
        add_error(errors, artifact, report_root, E_DCM_001, f"a deviation departs from a specification, not a {catalog[reference[0]].artifact_type}", plane="governance")
    elif reference[1] not in {identifier for identifier, _ in specification_rules(catalog[reference[0]].body) if identifier}:
        # SPEC-TCM-006 TCM-RFS-020: the fragment names a rule identifier the specification defines.
        add_error(errors, artifact, report_root, E_DCM_005,
            f"deviation departs from '{reference[0]}#{reference[1]}', which names no rule identifier of {reference[0]}", plane="governance")
    if not isinstance(artifact.metadata.get("observed"), str) or not str(artifact.metadata.get("observed")).strip():
        add_error(errors, artifact, report_root, E_DCM_002, "a deviation records the observed fact in 'observed'", plane="structure")
    if option_ids and (not set(option_ids).issubset(DEVIATION_OPTIONS) or "stop" not in option_ids):
        add_error(errors, artifact, report_root, E_DCM_002, "a deviation's options are drawn from amend, supersede, accept, stop and include stop", plane="structure")


def _check_decision_disposition(
    artifact: Artifact,
    kind: Any,
    option_ids: list[str],
    reference: tuple[str, str] | None,
    catalog: dict[str, Artifact],
    released_versions: set[str],
    accepted_by_rule: dict[str, list[str]],
    errors: list[Diagnostic],
    warnings: list[Diagnostic],
    report_root: Path,
) -> None:
    """Check a decision's [disposition] table against its status, options and accepted-deviation revisit."""
    disposition = artifact.metadata.get("disposition")
    events = artifact.metadata.get("lifecycle_events")
    if artifact.status in DECISION_TERMINAL or artifact.status == "deferred":
        if not isinstance(disposition, dict):
            add_error(errors, artifact, report_root, E_DCM_003, f"a {artifact.status} decision carries a [disposition] table written by the transition", plane="governance")
        else:
            if not isinstance(events, list) or not events:
                add_error(errors, artifact, report_root, E_DCM_003, "a disposition without a lifecycle event was written by hand", plane="governance")
            option = disposition.get("option")
            if artifact.status == "decided" and option not in option_ids:
                add_error(errors, artifact, report_root, E_DCM_003, f"disposition option '{option}' is not a declared option", plane="governance")
            for key in ("decided_by", "decided_at", "reason", "label"):
                if not isinstance(disposition.get(key), str) or not disposition[key].strip():
                    add_error(errors, artifact, report_root, E_DCM_003, f"disposition field '{key}' must be a non-empty string", plane="governance")
            if artifact.status == "deferred" and (not isinstance(disposition.get("scope"), list) or not disposition.get("revisit")):
                add_error(errors, artifact, report_root, E_DCM_003, "a deferred decision records its scope and its revisit trigger", plane="governance")
            if artifact.status == "decided" and kind == "deviation" and option == "accept":
                revisit = disposition.get("revisit")
                if not isinstance(revisit, str) or not revisit.strip():
                    add_error(errors, artifact, report_root, E_DCM_003, "an accepted deviation records its revisit trigger", plane="governance")
                elif reference is not None:
                    rule = f"{reference[0]}#{reference[1]}"
                    accepted_by_rule[rule].append(artifact.artifact_id)
                    if any(f"v{version}" in revisit or version in revisit for version in released_versions):
                        warnings.append(Diagnostic(
                            display_path(catalog[reference[0]].path, report_root) if reference[0] in catalog else display_path(artifact.path, report_root),
                            W_DCM_001,
                            f"accepted deviation {artifact.artifact_id} against {rule} is past its revisit '{revisit}'; amend or supersede the rule, or accept again with a new trigger",
                            "maintenance",
                        ))
    elif isinstance(disposition, dict) and artifact.status == "open":
        add_error(errors, artifact, report_root, E_DCM_003, "an open decision carries no disposition", plane="governance")


def validate_decisions(artifacts: list[Artifact], report_root: Path) -> tuple[list[Diagnostic], list[Diagnostic]]:
    """SPEC-DCM-001 rules 2-4, 6, 8, 10: decision fields, options, relations, dispositions, revisits."""

    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    catalog = {artifact.artifact_id: artifact for artifact in artifacts if artifact.artifact_id != "<unknown>"}
    accepted_by_rule: dict[str, list[str]] = defaultdict(list)
    released_versions = {
        str(artifact.metadata.get("version"))
        for artifact in artifacts
        if artifact.artifact_type == "release_record" and artifact.status == "released" and artifact.metadata.get("version")
    }
    for artifact in artifacts:
        if artifact.artifact_type != "decision":
            continue
        kind = artifact.metadata.get("kind")
        if kind not in DECISION_KINDS:
            add_error(errors, artifact, report_root, E_DCM_002, "decision kind must be question or deviation", plane="structure")
            continue
        for key in ("question", "raised_by", "recommendation"):
            if not isinstance(artifact.metadata.get(key), str) or not str(artifact.metadata.get(key)).strip():
                add_error(errors, artifact, report_root, E_DCM_002, f"decision field '{key}' must be a non-empty string", plane="structure")
        options = _decision_options(artifact)
        option_ids = [item["id"] for item in options]
        if len(options) < 2 or len(set(option_ids)) != len(option_ids):
            add_error(errors, artifact, report_root, E_DCM_002, "a decision declares at least two options with distinct ids and labels", plane="structure")
        recommendation = artifact.metadata.get("recommendation")
        if isinstance(recommendation, str) and option_ids and recommendation not in option_ids:
            add_error(errors, artifact, report_root, E_DCM_002, f"recommendation '{recommendation}' is not a declared option", plane="structure")
        reference = _decision_against(artifact)
        if kind == "deviation":
            _check_deviation_fields(artifact, reference, option_ids, catalog, errors, report_root)
        relations = artifact.metadata.get("relations", {})
        relations = relations if isinstance(relations, dict) else {}
        blocked = relations.get("blocks", []) if isinstance(relations.get("blocks"), list) else []
        concerned = relations.get("concerns", []) if isinstance(relations.get("concerns"), list) else []
        if not blocked:
            add_error(errors, artifact, report_root, E_DCM_001, "a decision blocks at least one artifact", plane="governance")
        for target in blocked:
            if isinstance(target, str) and target not in concerned:
                add_error(errors, artifact, report_root, E_DCM_001, f"blocked artifact '{target}' is not also in concerns", plane="governance")
        _check_decision_disposition(artifact, kind, option_ids, reference, catalog, released_versions, accepted_by_rule, errors, warnings, report_root)
    for rule, decisions in sorted(accepted_by_rule.items()):
        if len(decisions) >= 2:
            target = catalog.get(rule.split("#", 1)[0])
            warnings.append(Diagnostic(
                display_path(target.path, report_root) if target is not None else rule,
                W_DCM_002,
                f"{len(decisions)} accepted deviations stand against {rule} ({', '.join(decisions)}); the rule, not the implementations, is probably wrong",
                "maintenance",
            ))
    return errors, warnings


def _check_risk_measurement(
    artifact: Artifact,
    metadata: dict[str, Any],
    errors: list[Diagnostic],
    report_root: Path,
) -> None:
    """Check the risk measurement: likelihood, impact and score are integers and score is their product."""
    measurement: dict[str, int] = {}
    for field_name in ("likelihood", "impact", "score"):
        value = metadata.get(field_name)
        if value is None:
            add_error(errors, artifact, report_root, E_RSK_001, f"risk field '{field_name}' is missing", plane="structure")
        elif type(value) is not int:
            add_error(errors, artifact, report_root, E_RSK_002, f"risk field '{field_name}' must be an integer, not {value!r}", plane="structure")
        elif field_name != "score" and value not in RISK_MEASUREMENT_RANGE:
            add_error(errors, artifact, report_root, E_RSK_002, f"risk field '{field_name}' must be from 1 to 5, not {value}", plane="structure")
        else:
            measurement[field_name] = value
    if {"likelihood", "impact", "score"} <= set(measurement):
        product = measurement["likelihood"] * measurement["impact"]
        if measurement["score"] != product:
            add_error(errors, artifact, report_root, E_RSK_002,
                f"risk field 'score' is {measurement['score']}; likelihood {measurement['likelihood']} times impact {measurement['impact']} is {product}", plane="structure")


def _check_risk_pairing(
    artifact: Artifact,
    concerned: dict[str, list[Artifact]],
    errors: list[Diagnostic],
    report_root: Path,
) -> None:
    """Check that a raised risk is answered by exactly one pending decision blocking what it threatens."""
    threatens = artifact.relations.get("threatens", [])
    threatened = {item for item in threatens if isinstance(item, str)} if isinstance(threatens, list) else set()
    if artifact.status == "raised":
        pending = [item for item in concerned.get(artifact.artifact_id, []) if item.status in {"open", "deferred"}]
        if not pending:
            add_error(errors, artifact, report_root, E_RSK_003,
                f"raised risk {artifact.artifact_id} is named in concerns by no open or deferred decision; raise it again with "
                f"harnessctl raise-risk --with-decision, or create a decision that names it in concerns and blocks exactly the artifacts it threatens",
                plane="governance")
        elif len(pending) > 1:
            names = ", ".join(sorted(item.artifact_id for item in pending))
            add_error(errors, artifact, report_root, E_RSK_003,
                f"raised risk {artifact.artifact_id} is named in concerns by {len(pending)} pending decisions ({names}); exactly one answers it", plane="governance")
        else:
            blocks = pending[0].relations.get("blocks", [])
            blocked = {item for item in blocks if isinstance(item, str)} if isinstance(blocks, list) else set()
            if blocked != threatened:
                add_error(errors, artifact, report_root, E_RSK_004,
                    f"{pending[0].artifact_id} blocks {sorted(blocked)} but {artifact.artifact_id} threatens {sorted(threatened)}; the two sets must be equal",
                    plane="governance")


def _check_risk_disposition(
    artifact: Artifact,
    metadata: dict[str, Any],
    concerned: dict[str, list[Artifact]],
    released_versions: set[str],
    errors: list[Diagnostic],
    warnings: list[Diagnostic],
    report_root: Path,
) -> None:
    """Check a disposed risk's [disposition] table and an accepted risk's revisit trigger."""
    disposition = metadata.get("disposition")
    events = metadata.get("lifecycle_events")
    expected_option = {"accepted": "accept", "avoided": "avoid", "mitigating": "mitigate", "mitigated": "mitigate", "withdrawn": "withdrawn"}
    if artifact.status in RISK_DISPOSED - {"withdrawn"} or (artifact.status == "withdrawn" and isinstance(disposition, dict)):
        if not isinstance(disposition, dict):
            add_error(errors, artifact, report_root, E_RSK_005,
                f"a {artifact.status} risk carries a [disposition] table written by harnessctl decide", plane="governance")
        else:
            if not isinstance(events, list) or not events:
                add_error(errors, artifact, report_root, E_RSK_005, "a disposition without a lifecycle event was written by hand", plane="governance")
            option = disposition.get("option")
            if option != expected_option[artifact.status]:
                add_error(errors, artifact, report_root, E_RSK_005,
                    f"disposition option '{option}' does not name the state {artifact.status}", plane="governance")
            for field_name in ("decided_by", "decided_at", "reason", "label"):
                if not isinstance(disposition.get(field_name), str) or not disposition[field_name].strip():
                    add_error(errors, artifact, report_root, E_RSK_005, f"disposition field '{field_name}' must be a non-empty string", plane="governance")
            revisit = disposition.get("revisit")
            if artifact.status == "accepted":
                if not isinstance(revisit, str) or not revisit.strip():
                    add_error(errors, artifact, report_root, E_RSK_005, "an accepted risk records its revisit trigger", plane="governance")
                elif any(f"v{version}" in revisit or version in revisit for version in released_versions) and not any(
                    item.status in {"open", "deferred"} for item in concerned.get(artifact.artifact_id, [])
                ):
                    warnings.append(Diagnostic(
                        display_path(artifact.path, report_root),
                        W_RSK_001,
                        f"accepted risk {artifact.artifact_id} is past its revisit '{revisit}' and no pending decision concerns it; raise it again or accept it again with a new trigger",
                        "maintenance",
                    ))
    elif isinstance(disposition, dict):
        add_error(errors, artifact, report_root, E_RSK_005, f"a {artifact.status} risk carries no disposition", plane="governance")


def validate_risks(artifacts: list[Artifact], report_root: Path) -> tuple[list[Diagnostic], list[Diagnostic]]:
    """SPEC-RSK-010 rules 2 to 6, 12, 13 and 18 to 20: risk fields, the measurement, the pairing, the answer."""

    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    released_versions = {
        str(artifact.metadata.get("version"))
        for artifact in artifacts
        if artifact.artifact_type == "release_record" and artifact.status == "released" and artifact.metadata.get("version")
    }
    concerned: dict[str, list[Artifact]] = defaultdict(list)
    for decision in artifacts:
        if decision.artifact_type != "decision":
            continue
        concerns = decision.relations.get("concerns", [])
        for target in concerns if isinstance(concerns, list) else []:
            if isinstance(target, str):
                concerned[target].append(decision)
    for artifact in artifacts:
        if artifact.artifact_type != "risk":
            continue
        metadata = artifact.metadata
        for field_name in ("cause", "effect", "stage", "category", "raised_by"):
            value = metadata.get(field_name)
            if not isinstance(value, str) or not value.strip():
                add_error(errors, artifact, report_root, E_RSK_001, f"risk field '{field_name}' must be a non-empty string", plane="structure")
        for field_name, allowed in (("stage", RISK_STAGES), ("category", RISK_CATEGORIES)):
            value = metadata.get(field_name)
            if isinstance(value, str) and value.strip() and value not in allowed:
                add_error(errors, artifact, report_root, E_RSK_001,
                    f"risk field '{field_name}' must name one of {', '.join(sorted(allowed))}, not '{value}'", plane="structure")
        for field_name in ("cause", "effect"):
            value = metadata.get(field_name)
            if isinstance(value, str) and len(sentences(value)) > 1:
                add_error(errors, artifact, report_root, E_RSK_001, f"risk field '{field_name}' must be one sentence", plane="structure")
        for field_name in ("question", "options", "recommendation", "decided_by"):
            # ARCH-RSK-010 conformance check 3: the answer lives on the paired decision.
            if field_name in metadata:
                add_error(errors, artifact, report_root, E_RSK_001,
                    f"risk declares the decision field '{field_name}'; the question, the options and the decider live on the paired decision", plane="structure")
        _check_risk_measurement(artifact, metadata, errors, report_root)
        _check_risk_pairing(artifact, concerned, errors, report_root)
        _check_risk_disposition(artifact, metadata, concerned, released_versions, errors, warnings, report_root)
        if artifact.status in {"mitigating", "mitigated"}:
            mitigated_by = artifact.relations.get("mitigated_by", [])
            if not isinstance(mitigated_by, list) or not mitigated_by:
                add_error(errors, artifact, report_root, E_RSK_005, f"a {artifact.status} risk names its mitigating work orders in mitigated_by", plane="governance")
        if artifact.status == "avoided":
            avoided_by = artifact.relations.get("avoided_by", [])
            if not isinstance(avoided_by, list) or len(avoided_by) != 1:
                add_error(errors, artifact, report_root, E_RSK_005, "an avoided risk names one ADR or one decision in avoided_by", plane="governance")
    return errors, warnings
