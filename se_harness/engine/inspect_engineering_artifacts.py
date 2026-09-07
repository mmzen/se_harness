#!/usr/bin/env python3
"""Render deterministic, read-only repository attention from existing harness evidence."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from itertools import groupby
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from generate_harness_dashboard import (
    GenerationError,
    SNAPSHOT_SCHEMA,
    generate_snapshot,
)
from validate_engineering_artifacts import (
    TAXONOMY_VERSION,
    VALIDATION_PLANES,
    ValidationReport,
    work_order_assurance_state,
)


INSPECTION_SCHEMA = "se-harness-inspection-v2"

#: SPEC-TCM-003 TCM-RFR-008: the repository-owned glossary and the vocabulary report.
GLOSSARY_RELATIVE = "GLOSSARY.md"
VOCABULARY_DEFAULT_THRESHOLD = 50
VOCABULARY_MINIMUM_THRESHOLD = 30
VOCABULARY_MAXIMUM_THRESHOLD = 100
#: Harness terms are defined once in the managed instructions the distribution
#: ships; they are excluded from the report so only project terms are named.
#: This list ships as exclusions, never as definitions.
HARNESS_TERMS = frozenset({
    "artifact", "artifacts", "intent", "capability", "capabilities", "requirement", "requirements",
    "specification", "specifications", "architecture", "adr", "verification", "contract", "contracts",
    "operating", "release", "releases", "record", "records", "work", "order", "orders", "lifecycle",
    "transition", "transitions", "status", "draft", "approved", "implemented", "verified", "released",
    "rejected", "ready", "superseded", "withdrawn", "deferred", "decided", "decision", "decisions",
    "right", "rights", "gate", "gates", "predicate", "predicates", "checkpoint", "checkpoints",
    "handoff", "evidence", "packet", "scope", "restitution", "projection", "check", "preflight",
    "validate", "validation", "validator", "harness", "harnessctl", "managed", "lock", "owner", "owners",
    "accountable", "delegation", "delegated", "executor", "relation", "relations", "domain", "domains",
    "template", "templates", "advisory", "advisories", "warning", "warnings", "error", "errors",
    "diagnostic", "diagnostics", "explorer", "dashboard", "inspect", "inspection", "amendment",
    "supersede", "reason", "role", "roles", "owner", "repository", "pull", "request",
})
#: Common English, so the report is about vocabulary and not grammar.
ENGLISH_STOPWORDS = frozenset("""
a about above after again against all also always am an and any are as at be because been before being
below between both but by can could did do does doing down during each either every few for from further
had has have having he her here hers herself him himself his how i if in into is it its itself just least
less let like may me might more most much must my myself never no nor not now of off on once one only or
other our ours ourselves out over own per same shall she should since so some still such than that the
their theirs them themselves then there these they this those through to too under until up upon us very
was we were what when where whether which while who whom why will with within without would you your yours
yourself yourselves given then when normal failure example examples trigger response behavior plain words
why none section sections file files path paths name names new old first second last next same different
exact exactly state states required requires require existing exists exist complete completes completed
remain remains remaining test tests testing source sources implementation implementations expected observed
current later earlier retained retain named single change changes changed add added adds remove removed
before after without within every each one two three
""".split())
#: The report names at most this many undefined terms, most frequent first, and counts the rest.
VOCABULARY_REPORT_LIMIT = 25
_TOKEN = re.compile(r"[a-z][a-z-]{2,}")
_INLINE_CODE = re.compile(r"`[^`]*`")
_FENCED_CODE = re.compile(r"```.*?```", re.S)
#: An entry opens with its term in bold, the period inside or just after the span.
_GLOSSARY_ENTRY = re.compile(r"^\*\*([^*]+?)\.?\*\*[.:]?(?=\s)", re.M)
SEVERITIES = ("error", "warning", "info")
SEVERITY_ORDER = {value: index for index, value in enumerate(SEVERITIES)}
QUEUE_SUGGESTION_CATALOG = {
    "assurance-review": (
        "review-assurance-decision",
        "assurance-owner",
        "Review retained evidence and record or withhold the accountable verification decision.",
    ),
    "release-review": (
        "review-release-decision",
        "release-owner",
        "Review the verified candidate and release controls and record or withhold the release decision.",
    ),
    "accountable-review": (
        "review-accountable-decision",
        "artifact-owner",
        "Identify the accountable owner and review the ready artifact without assuming an outcome.",
    ),
    "dispose-decision": (
        "dispose-pending-decision",
        "artifact-owner",
        "Answer the pending decision with one declared option through harnessctl decide; the artifacts it blocks wait until then.",
    ),
    "complete-definition": (
        "complete-or-dispose-definition",
        "artifact-owner",
        "Complete the definition or explicitly dispose of it through an allowed governed state.",
    ),
    "start-authorized-work": (
        "start-bounded-work",
        "engineering-owner",
        "Run start preflight and begin only the approved scope.",
    ),
    "continue-authorized-work": (
        "continue-bounded-work",
        "engineering-owner",
        "Continue only the authorized scope and retain work-order-keyed evidence.",
    ),
    "prepare-commit-bound-verification": (
        "prepare-commit-bound-verification",
        "engineering-owner",
        "After retaining the selected work in one clean candidate commit, prepare a ready verification record for explicit accountable review.",
    ),
}
FINDING_SUGGESTION_CATALOG = {
    "W-HEX-001": (
        "retain-work-order-evidence",
        "engineering-owner",
        "Retain evidence keyed to the implemented work order and reassess the observation.",
    ),
    "W-HEX-002": (
        "review-governing-scope",
        "engineering-owner",
        "Review inactive governing references before continuing active work.",
    ),
    "W-HEX-003": (
        "reassess-dependent-artifact",
        "artifact-owner",
        "Reassess the older source against its newer declared dependency or parent.",
    ),
    "W-HEX-004": (
        "review-relation-cycle",
        "technical-owner",
        "Determine whether the declared cycle is intentional and correct unintended edges through governed work.",
    ),
    "W-HEX-005": (
        "review-unlinked-artifact",
        "artifact-owner",
        "Declare the applicable relation or explicitly dispose of an artifact that is no longer applicable.",
    ),
    "W-HEX-006": (
        "deduplicate-relation",
        "artifact-owner",
        "Remove an unintended repeated relation through governed work.",
    ),
    "W-REV-002": (
        "review-release-provenance",
        "release-owner",
        "Reconcile the released work claim with an eligible commit-bound release record.",
    ),
    "W-REV-003": (
        "restore-candidate-availability",
        "repository-owner",
        "Make the declared candidate commit available for assessment without changing its recorded identity.",
    ),
    "W-REV-004": (
        "review-verification-supersession",
        "assurance-owner",
        "Assess explicit supersession against one eligible verified or released successor; do not transition automatically.",
    ),
    "W-REB-001": (
        "review-competing-release-proposals",
        "release-owner",
        "Review same-version release proposals and record an accountable disposition without automatic selection.",
    ),
    "W-REB-002": (
        "review-overlapping-verification-candidates",
        "assurance-owner",
        "Review overlapping ready verification candidates and govern any supersession explicitly.",
    ),
    "W-REB-003": (
        "review-competing-release-contracts",
        "release-owner",
        "Review competing release contracts and proposals without changing either chain automatically.",
    ),
}


class InspectionError(RuntimeError):
    """The existing snapshot cannot be projected into the inspection contract."""


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise InspectionError(f"{label} must be an object")
    return value


def _mapping_list(value: Any, label: str) -> list[Mapping[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(item, Mapping) for item in value):
        raise InspectionError(f"{label} must be an array of objects")
    return list(value)


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise InspectionError(f"{label} must be text")
    return value


def _text_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise InspectionError(f"{label} must be an array of text values")
    return list(value)


def _display(value: Any) -> str:
    """Preserve Unicode while escaping terminal control characters and newlines."""

    return json.dumps(str(value), ensure_ascii=False)[1:-1]


def _queue_entry(artifact: Mapping[str, Any], action: str) -> dict[str, Any]:
    return {
        "id": _text(artifact.get("id"), "artifact id"),
        "type": _text(artifact.get("type"), "artifact type"),
        "title": _text(artifact.get("title"), "artifact title"),
        "status": _text(artifact.get("status"), "artifact status"),
        "owners": sorted(_text_list(artifact.get("owners", []), "artifact owners")),
        "path": _text(artifact.get("path"), "artifact path"),
        "action": action,
    }


def _ready_action(artifact_type: str) -> str:
    if artifact_type == "verification_record":
        return "assurance-review"
    if artifact_type == "release_record":
        return "release-review"
    return "accountable-review"


def _queue_sort(item: Mapping[str, Any]) -> tuple[str, str]:
    return str(item.get("id", "")), str(item.get("path", ""))


def _finding_copy(item: Mapping[str, Any]) -> dict[str, Any]:
    severity = _text(item.get("severity"), "finding severity")
    if severity not in SEVERITY_ORDER:
        raise InspectionError(f"unknown finding severity: {severity!r}")
    return {
        "rule": _text(item.get("rule"), "finding rule"),
        "severity": severity,
        "message": _text(item.get("message"), "finding message"),
        "artifacts": sorted(_text_list(item.get("artifacts", []), "finding artifacts")),
        "paths": sorted(_text_list(item.get("paths", []), "finding paths")),
        "evidence": sorted(_text_list(item.get("evidence", []), "finding evidence")),
        "authority": _text(item.get("authority"), "finding authority"),
    }


def _finding_sort(item: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        SEVERITY_ORDER[str(item["severity"])],
        str(item["rule"]),
        tuple(item["artifacts"]),
        tuple(item["paths"]),
        str(item["message"]),
    )


def _suggestion(
    source_kind: str,
    source_id: str,
    subjects: Iterable[str],
    definition: tuple[str, str, str],
) -> dict[str, Any]:
    action, accountable_role, message = definition
    return {
        "source_kind": source_kind,
        "source_id": source_id,
        "subjects": sorted(set(subjects)),
        "action": action,
        "message": message,
        "accountable_role": accountable_role,
        "automatic": False,
    }


def _suggestion_sort(item: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        str(item["source_kind"]),
        str(item["source_id"]),
        str(item["action"]),
        tuple(item["subjects"]),
        str(item["accountable_role"]),
        str(item["message"]),
    )


def _build_suggestions(
    queues: Mapping[str, Sequence[Mapping[str, Any]]],
    findings: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    suggestions: list[dict[str, Any]] = []
    for queue_name in (
        "decision_required",
        "definition_pending",
        "active_work",
        "assurance_pending",
    ):
        for item in queues[queue_name]:
            action = _text(item.get("action"), "queue action")
            definition = QUEUE_SUGGESTION_CATALOG.get(action)
            if definition is None:
                raise InspectionError(f"unknown queue suggestion action: {action!r}")
            suggestions.append(
                _suggestion(
                    "queue",
                    queue_name,
                    [_text(item.get("id"), "queue artifact id")],
                    definition,
                )
            )

    for item in findings:
        if item.get("severity") != "warning" or item.get("authority") != "derived":
            continue
        rule = _text(item.get("rule"), "finding rule")
        definition = FINDING_SUGGESTION_CATALOG.get(rule)
        if definition is None:
            continue
        suggestions.append(
            _suggestion(
                "finding",
                rule,
                _text_list(item.get("artifacts", []), "finding artifacts"),
                definition,
            )
        )
    return sorted(suggestions, key=_suggestion_sort)


def _diagnostic_plane_counts(
    snapshot_diagnostics: Sequence[Mapping[str, Any]],
    validation_report: ValidationReport | None,
) -> tuple[int, int, dict[str, dict[str, int]]]:
    counts = {
        plane: {"errors": 0, "warnings": 0}
        for plane in VALIDATION_PLANES
    }
    error_count = 0
    warning_count = 0

    if validation_report is not None:
        diagnostics = [
            *((item, "error") for item in validation_report.errors),
            *((item, "warning") for item in validation_report.warnings),
        ]
        for diagnostic, severity in diagnostics:
            plane = diagnostic.plane
            if plane not in counts:
                raise InspectionError(f"unknown validation plane: {plane!r}")
            key = "errors" if severity == "error" else "warnings"
            counts[plane][key] += 1
            if severity == "error":
                error_count += 1
            else:
                warning_count += 1
        return error_count, warning_count, counts

    for item in snapshot_diagnostics:
        severity = _text(item.get("severity"), "diagnostic severity")
        plane = _text(item.get("plane"), "diagnostic plane")
        if plane not in counts:
            raise InspectionError(f"unknown validation plane: {plane!r}")
        if severity == "error":
            error_count += 1
            counts[plane]["errors"] += 1
        elif severity == "warning":
            warning_count += 1
            counts[plane]["warnings"] += 1
        else:
            raise InspectionError(f"unknown diagnostic severity: {severity!r}")
    return error_count, warning_count, counts


def _corpus_words(artifacts: Iterable[Any]) -> Counter[str]:
    """Word counts over statements and bodies, code removed, lowercased."""

    counts: Counter[str] = Counter()
    for artifact in artifacts:
        metadata = getattr(artifact, "metadata", None)
        statement = metadata.get("statement") if isinstance(metadata, Mapping) else None
        body = getattr(artifact, "body", "")
        text = " ".join(part for part in (statement if isinstance(statement, str) else "", body if isinstance(body, str) else "") if part)
        text = _INLINE_CODE.sub(" ", _FENCED_CODE.sub(" ", text))
        for token in _TOKEN.findall(text.lower()):
            token = token.strip("-")
            if len(token) >= 3 and token not in ENGLISH_STOPWORDS:
                counts[token] += 1
    return counts


def _glossary_entries(text: str) -> list[str]:
    """The entry heads of a glossary page: the bold term opening each entry."""

    return [match.group(1).strip() for match in _GLOSSARY_ENTRY.finditer(text)]


def _entry_keys(entry: str) -> set[str]:
    """Lowercase words a corpus token may match for one entry, including an abbreviation."""

    keys: set[str] = set()
    head = entry.split(" versus ")[0]
    for part in re.split(r"[(),/]", head):
        part = part.strip().lower()
        if not part:
            continue
        keys.add(part)
        for word in _TOKEN.findall(part):
            if word not in ENGLISH_STOPWORDS:
                keys.add(word)
    return keys


def build_vocabulary_report(
    root: Path,
    validation_report: ValidationReport | None,
    threshold: int = VOCABULARY_DEFAULT_THRESHOLD,
) -> dict[str, Any]:
    """SPEC-TCM-003 TCM-RFR-008: frequent project terms without an entry, entries without a term.

    Read-only and deterministic. Harness terms and common English are excluded;
    a missing glossary is reported once and is not an error.
    """

    if not (VOCABULARY_MINIMUM_THRESHOLD <= threshold <= VOCABULARY_MAXIMUM_THRESHOLD):
        raise InspectionError(
            f"vocabulary threshold must be between {VOCABULARY_MINIMUM_THRESHOLD} and {VOCABULARY_MAXIMUM_THRESHOLD}"
        )
    glossary_path = Path(root) / GLOSSARY_RELATIVE
    present = glossary_path.is_file()
    entries: list[str] = []
    readable = True
    if present:
        try:
            entries = _glossary_entries(glossary_path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError):
            readable = False
    counts = _corpus_words(validation_report.artifacts if validation_report is not None else ())
    defined: set[str] = set()
    for entry in entries:
        defined |= _entry_keys(entry)
    undefined_all = [
        {"term": term, "count": count}
        for term, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        if count >= threshold and term not in HARNESS_TERMS and term not in defined
    ]
    undefined = undefined_all[:VOCABULARY_REPORT_LIMIT]
    omitted = len(undefined_all) - len(undefined)
    stale = sorted(
        entry for entry in entries
        if not any(counts.get(key, 0) > 0 for key in _entry_keys(entry) if " " not in key)
        and not any(" ".join(_TOKEN.findall(key)) and all(counts.get(word, 0) > 0 for word in _TOKEN.findall(key)) for key in _entry_keys(entry) if " " in key)
    )
    notes: list[str] = []
    if not present:
        notes.append(f"{GLOSSARY_RELATIVE} is absent; the harness seeds it at installation and this repository writes it")
    elif not readable:
        notes.append(f"{GLOSSARY_RELATIVE} could not be read as UTF-8 text")
    return {
        "glossary_path": GLOSSARY_RELATIVE,
        "present": present,
        "entry_count": len(entries),
        "threshold": threshold,
        "undefined_frequent_terms": undefined,
        "undefined_frequent_terms_omitted": omitted,
        "stale_entries": [{"term": entry} for entry in stale],
        "notes": notes,
        "authority": "derived",
    }


def build_inspection(
    snapshot: Mapping[str, Any],
    validation_report: ValidationReport | None = None,
    vocabulary: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    snapshot = _mapping(snapshot, "snapshot")
    if snapshot.get("schema") != SNAPSHOT_SCHEMA:
        raise InspectionError(
            f"snapshot schema must be {SNAPSHOT_SCHEMA!r}"
        )

    repository = dict(_mapping(snapshot.get("repository"), "snapshot repository"))
    valid = repository.get("valid")
    if not isinstance(valid, bool):
        raise InspectionError("repository validity must be boolean")

    artifacts = _mapping_list(snapshot.get("artifacts"), "snapshot artifacts")
    relations = _mapping_list(snapshot.get("relations"), "snapshot relations")
    diagnostics = _mapping_list(snapshot.get("diagnostics"), "snapshot diagnostics")
    findings = sorted(
        (_finding_copy(item) for item in _mapping_list(snapshot.get("findings"), "snapshot findings")),
        key=_finding_sort,
    )

    decision_required: list[dict[str, Any]] = []
    definition_pending: list[dict[str, Any]] = []
    active_work: list[dict[str, Any]] = []
    assurance_pending: list[dict[str, Any]] = []
    assurance_by_id: dict[str, Mapping[str, Any]] = {}
    if validation_report is not None:
        assurance_by_id = {
            artifact.artifact_id: work_order_assurance_state(artifact)
            for artifact in validation_report.artifacts
            if artifact.artifact_type == "work_order"
        }

    artifact_by_id = {
        _text(artifact.get("id"), "artifact id"): artifact
        for artifact in artifacts
    }
    actively_covered_work: set[str] = set()
    for relation in relations:
        if (
            relation.get("relation") != "verifies_work_order"
            or relation.get("authority") != "declared"
        ):
            continue
        source_id = _text(relation.get("source"), "relation source")
        target_id = _text(relation.get("target"), "relation target")
        source = artifact_by_id.get(source_id)
        if source is None:
            continue
        if (
            source.get("type") == "verification_record"
            and source.get("status") in {"ready", "verified", "released"}
        ):
            actively_covered_work.add(target_id)

    for artifact in artifacts:
        artifact_id = _text(artifact.get("id"), "artifact id")
        artifact_type = _text(artifact.get("type"), "artifact type")
        status = _text(artifact.get("status"), "artifact status")
        if status == "ready":
            decision_required.append(_queue_entry(artifact, _ready_action(artifact_type)))
        if artifact_type == "decision" and status in {"open", "deferred"}:
            decision_required.append(_queue_entry(artifact, "dispose-decision"))
        if status == "draft":
            definition_pending.append(_queue_entry(artifact, "complete-definition"))
        if artifact_type == "work_order" and status in {"approved", "in_progress"}:
            action = "start-authorized-work" if status == "approved" else "continue-authorized-work"
            active_work.append(_queue_entry(artifact, action))
        assurance = assurance_by_id.get(artifact_id)
        if (
            artifact_type == "work_order"
            and status == "implemented"
            and assurance is not None
            and assurance.get("state") == "valid"
            and assurance.get("commit_bound_verification") == "required"
            and artifact_id not in actively_covered_work
        ):
            assurance_pending.append(
                _queue_entry(artifact, "prepare-commit-bound-verification")
            )

    error_count, warning_count, plane_counts = _diagnostic_plane_counts(
        diagnostics,
        validation_report,
    )
    finding_counts = Counter(str(item["severity"]) for item in findings)

    repository_projection = {
        "name": repository.get("name"),
        "revision": repository.get("revision"),
        "artifact_root": repository.get("artifact_root"),
    }
    for key, value in repository_projection.items():
        if value is not None and not isinstance(value, str):
            raise InspectionError(f"repository {key} must be text or null")

    queues = {
        "decision_required": sorted(decision_required, key=_queue_sort),
        "definition_pending": sorted(definition_pending, key=_queue_sort),
        "active_work": sorted(active_work, key=_queue_sort),
        "assurance_pending": sorted(assurance_pending, key=_queue_sort),
    }
    return {
        "schema": INSPECTION_SCHEMA,
        "authority": "derived",
        "producer": "repository-local",
        "repository": repository_projection,
        "validation": {
            "valid": valid,
            "taxonomy": TAXONOMY_VERSION,
            "error_count": error_count,
            "warning_count": warning_count,
            "plane_counts": plane_counts,
        },
        "summary": {
            "artifact_count": len(artifacts),
            "relation_count": len(relations),
            "finding_count": len(findings),
            "findings_by_severity": {
                severity: finding_counts.get(severity, 0)
                for severity in SEVERITIES
            },
        },
        "queues": queues,
        "findings": findings,
        "vocabulary": dict(vocabulary) if vocabulary is not None else None,
        "suggestions": _build_suggestions(queues, findings),
    }


def serialize_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _render_queue(label: str, entries: Sequence[Mapping[str, Any]]) -> list[str]:
    lines = [f"{label} ({len(entries)}):"]
    if not entries:
        lines.append("- none")
        return lines
    for item in entries:
        lines.append(
            f"- {_display(item['id'])} [{_display(item['status'])}] "
            f"{_display(item['action'])}: {_display(item['title'])} "
            f"({_display(item['path'])})"
        )
    return lines


def _render_findings(findings: Sequence[Mapping[str, Any]]) -> list[str]:
    if not findings:
        return ["- none"]
    lines: list[str] = []
    group_key = lambda item: (
        SEVERITY_ORDER[str(item.get("severity", ""))],
        str(item.get("rule", "")),
        str(item.get("authority", "")),
    )
    for _, grouped in groupby(sorted(findings, key=group_key), key=group_key):
        items = list(grouped)
        first = items[0]
        prefix = (
            f"- [{_display(str(first.get('severity', '')).upper())}] "
            f"{_display(first.get('rule', ''))} "
            f"({_display(first.get('authority', ''))}): "
        )
        artifacts = sorted(
            {
                artifact
                for item in items
                for artifact in item.get("artifacts", [])
                if isinstance(artifact, str)
            }
        )
        shown = artifacts[:8]
        artifact_suffix = ""
        if shown:
            artifact_suffix = " [" + ", ".join(_display(value) for value in shown)
            if len(artifacts) > len(shown):
                artifact_suffix += f", +{len(artifacts) - len(shown)} more"
            artifact_suffix += "]"
        if len(items) == 1:
            lines.append(prefix + _display(first.get("message", "")) + artifact_suffix)
        else:
            lines.append(prefix + f"{len(items)} observations" + artifact_suffix)
    return lines


def _render_suggestions(suggestions: Sequence[Mapping[str, Any]]) -> list[str]:
    if not suggestions:
        return ["- none"]
    lines: list[str] = []
    group_key = lambda item: (
        str(item.get("source_kind", "")),
        str(item.get("source_id", "")),
        str(item.get("action", "")),
        str(item.get("accountable_role", "")),
        str(item.get("message", "")),
    )
    for _, grouped in groupby(sorted(suggestions, key=group_key), key=group_key):
        items = list(grouped)
        first = items[0]
        subjects = sorted(
            {
                subject
                for item in items
                for subject in item.get("subjects", [])
                if isinstance(subject, str)
            }
        )
        shown = subjects[:8]
        subject_suffix = ""
        if shown:
            subject_suffix = " [" + ", ".join(_display(value) for value in shown)
            if len(subjects) > len(shown):
                subject_suffix += f", +{len(subjects) - len(shown)} more"
            subject_suffix += "]"
        observation = ""
        if len(items) > 1:
            observation = f" Repeated for {len(items)} source observations."
        lines.append(
            f"- {_display(first.get('source_id', ''))} -> "
            f"{_display(first.get('action', ''))} "
            f"({_display(first.get('accountable_role', ''))}): "
            f"{_display(first.get('message', ''))}{observation}{subject_suffix}"
        )
    return lines


def _render_vocabulary(vocabulary: Mapping[str, Any] | None) -> list[str]:
    if vocabulary is None:
        return []
    lines = ["", "Vocabulary (derived, informational):"]
    for note in vocabulary.get("notes", []):
        lines.append(f"- {note}")
    undefined = vocabulary.get("undefined_frequent_terms", [])
    stale = vocabulary.get("stale_entries", [])
    lines.append(
        f"- {vocabulary.get('entry_count', 0)} glossary entries in {vocabulary.get('glossary_path')}; "
        f"threshold {vocabulary.get('threshold')} occurrences"
    )
    if undefined:
        omitted = vocabulary.get("undefined_frequent_terms_omitted", 0)
        lines.append("- frequent project terms without an entry: " + ", ".join(f"{item['term']} ({item['count']})" for item in undefined) + (f"; and {omitted} more above the threshold" if omitted else ""))
    else:
        lines.append("- every project term above the threshold has an entry")
    if stale:
        lines.append("- entries whose term appears in no artifact: " + ", ".join(item["term"] for item in stale))
    return lines


def render_human(report: Mapping[str, Any]) -> str:
    report = _mapping(report, "inspection report")
    validation = _mapping(report.get("validation"), "inspection validation")
    summary = _mapping(report.get("summary"), "inspection summary")
    repository = _mapping(report.get("repository"), "inspection repository")
    queues = _mapping(report.get("queues"), "inspection queues")
    plane_counts = _mapping(validation.get("plane_counts"), "inspection plane counts")
    findings_by_severity = _mapping(
        summary.get("findings_by_severity"),
        "inspection severity counts",
    )
    findings = _mapping_list(report.get("findings"), "inspection findings")
    suggestions = _mapping_list(report.get("suggestions"), "inspection suggestions")

    revision = repository.get("revision") or "unavailable"
    lines = [
        "Harness inspection",
        f"Repository: {_display(repository.get('name') or 'unknown')} @ {_display(revision)}",
        f"Formal validation: {'PASS' if validation.get('valid') is True else 'FAIL'}",
        (
            f"Graph: {summary.get('artifact_count')} artifacts | "
            f"{summary.get('relation_count')} relations | "
            f"{summary.get('finding_count')} findings"
        ),
        (
            "Planes: "
            + " | ".join(
                f"{plane} E{_mapping(plane_counts.get(plane), f'{plane} counts').get('errors')}"
                f"/W{_mapping(plane_counts.get(plane), f'{plane} counts').get('warnings')}"
                for plane in VALIDATION_PLANES
            )
        ),
        (
            "Finding severity: "
            + " | ".join(
                f"{severity} {findings_by_severity.get(severity)}"
                for severity in SEVERITIES
            )
        ),
        "",
    ]
    lines.extend(
        _render_queue(
            "Decision required",
            _mapping_list(queues.get("decision_required"), "decision queue"),
        )
    )
    lines.append("")
    lines.extend(
        _render_queue(
            "Definitions pending",
            _mapping_list(queues.get("definition_pending"), "definition queue"),
        )
    )
    lines.append("")
    lines.extend(
        _render_queue(
            "Active work",
            _mapping_list(queues.get("active_work"), "active work queue"),
        )
    )
    lines.append("")
    lines.extend(
        _render_queue(
            "Assurance pending",
            _mapping_list(queues.get("assurance_pending"), "assurance pending queue"),
        )
    )
    lines.extend(["", f"Findings ({len(findings)}):"])
    lines.extend(_render_findings(findings))
    lines.extend(["", f"Suggested next steps ({len(suggestions)}):"])
    lines.extend(_render_suggestions(suggestions))
    lines.extend(
        [
            "",
            "Authority: repository-local, derived observation. "
            "Inspection does not validate by exit status, approve, authorize, verify, release, or remediate.",
        ]
    )
    lines.extend(_render_vocabulary(report.get("vocabulary")))
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect existing validation, lifecycle, and Explorer observations."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--vocabulary-threshold",
        type=int,
        default=VOCABULARY_DEFAULT_THRESHOLD,
        help=f"occurrences from which a project term without a glossary entry is reported ({VOCABULARY_MINIMUM_THRESHOLD}-{VOCABULARY_MAXIMUM_THRESHOLD})",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        snapshot, validation_report, _ = generate_snapshot(Path(args.root))
        vocabulary = build_vocabulary_report(Path(args.root), validation_report, args.vocabulary_threshold)
        report = build_inspection(snapshot, validation_report, vocabulary)
        if args.json:
            sys.stdout.write(serialize_json(report))
        else:
            sys.stdout.write(render_human(report))
        return 0
    except (GenerationError, InspectionError, OSError, ValueError) as exc:
        print(f"inspection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
