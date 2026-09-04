#!/usr/bin/env python3
"""Validate specification-driven engineering artifacts.

The validator intentionally uses only the Python 3.11+ standard library so it can
run before the repository's normal toolchain is available.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Iterable

try:
    import tomllib
except ModuleNotFoundError as exc:  # pragma: no cover - version guard
    raise SystemExit("Python 3.11 or later is required (missing tomllib).") from exc

_LAYOUT_PATH = Path(__file__).with_name("artifact_layout_registry.py")
_LAYOUT_SPEC = importlib.util.spec_from_file_location("_se_harness_artifact_layout_registry", _LAYOUT_PATH)
if _LAYOUT_SPEC is None or _LAYOUT_SPEC.loader is None:
    raise RuntimeError(f"cannot load artifact layout registry: {_LAYOUT_PATH}")
_LAYOUT = importlib.util.module_from_spec(_LAYOUT_SPEC)
_LAYOUT_SPEC.loader.exec_module(_LAYOUT)
ARTIFACT_DIRECTORIES = _LAYOUT.ARTIFACT_DIRECTORIES
ARTIFACT_PREFIXES = _LAYOUT.ARTIFACT_PREFIXES
artifact_domain_from_relative_path = _LAYOUT.artifact_domain_from_relative_path
canonical_artifact_relative_path = _LAYOUT.canonical_artifact_relative_path
common_artifact_domain = _LAYOUT.common_artifact_domain
repository_record_relative_path = _LAYOUT.repository_record_relative_path


TAXONOMY_VERSION = "se-harness-validation-taxonomy-v1"
VALIDATION_PLANES = ("structure", "governance", "policy", "maintenance")

TYPE_PREFIX = {**ARTIFACT_PREFIXES, "risk_acceptance": "RISK-"}

ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9-]*-\d{3}$")
EVIDENCE_WORK_ORDER_PATTERN = re.compile(
    r"^(WO-(?:[A-Z0-9-]*-)?\d{3})(?:-|\.|$)"
)
ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
EVALUATOR_EVIDENCE_SCHEMA = "se-harness-evaluator-evidence-v1"
EVALUATOR_PAYLOAD_MANIFEST = "se-harness-installed-payload-v1"
EVALUATOR_EVIDENCE_MAX_BYTES = 64 * 1024
EVALUATOR_ORIGIN_PATTERN = re.compile(r"^<evaluator-root>(?:/[A-Za-z0-9._+()@ -]+)*$")
EVALUATOR_VERSION_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.!+\-]{0,127}$")
# The legacy release-evidence declaration mechanism (SPEC-LRE-001) was retired
# under WO-LRE-002 (the evaluator-evidence floor, owner decision of 2026-08-30):
# a released record carrying neither evaluator-evidence field is not assessed.
# The diagnostic code W024 is retired and stays reserved, never reused.
GIT_COMMIT_PATTERNS = {
    "sha1": re.compile(r"^[0-9a-f]{40}$"),
    "sha256": re.compile(r"^[0-9a-f]{64}$"),
}

RELEASABLE_WORK_STATUSES = {
    "implemented",
    "verified",
    "released",
}


@dataclass(frozen=True)
class LifecycleStatePolicy:
    transitions_to: tuple[str, ...]
    grants_authority: bool
    reserves_version: bool
    transitionable: bool
    must_remain_visible: bool
    predecessor_adapter: str


_LIFECYCLE_FAMILIES = {"definition", "work_order", "verification_record", "release_record", "decision"}
_LIFECYCLE_FIELDS = {
    "transitions_to",
    "grants_authority",
    "reserves_version",
    "transitionable",
    "must_remain_visible",
    "predecessor_adapter",
}
_PREDECESSOR_ADAPTER_VALUES = {"none", "required"}
_STATE_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")


def _workflow_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise RuntimeError(f"managed workflow contract contains duplicate JSON key: {key}")
        value[key] = item
    return value


def _load_workflow_lifecycles() -> MappingProxyType:
    path = Path(__file__).resolve().parent.parent / "docs" / "engineering" / "WORKFLOW.json"
    try:
        raw = path.read_bytes()
        if len(raw) > 2_000_000:
            raise RuntimeError(f"managed workflow contract exceeds 2 MB: {path}")
        contract = json.loads(raw.decode("utf-8"), object_pairs_hook=_workflow_object)
    except RuntimeError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot load managed workflow contract: {path}") from exc
    if not isinstance(contract, dict) or contract.get("schema") != "se-harness-workflow-v4":
        raise RuntimeError("managed workflow contract has an unsupported schema")
    source = contract.get("lifecycles")
    if not isinstance(source, dict) or set(source) != _LIFECYCLE_FAMILIES:
        raise RuntimeError("managed workflow contract must declare exactly the five lifecycle families")
    lifecycles: dict[str, dict[str, LifecycleStatePolicy]] = {}
    for family in sorted(_LIFECYCLE_FAMILIES):
        raw_states = source.get(family)
        if not isinstance(raw_states, dict) or not raw_states:
            raise RuntimeError(f"managed workflow lifecycle family {family} must contain states")
        states: dict[str, LifecycleStatePolicy] = {}
        for current, raw_row in raw_states.items():
            if not isinstance(current, str) or _STATE_NAME_PATTERN.fullmatch(current) is None:
                raise RuntimeError(f"managed workflow lifecycle family {family} has an invalid state")
            if not isinstance(raw_row, dict) or set(raw_row) != _LIFECYCLE_FIELDS:
                raise RuntimeError(f"managed workflow lifecycle {family}:{current} has invalid fields")
            targets = raw_row.get("transitions_to")
            if (
                not isinstance(targets, list)
                or not all(isinstance(target, str) and _STATE_NAME_PATTERN.fullmatch(target) for target in targets)
                or len(targets) != len(set(targets))
            ):
                raise RuntimeError(f"managed workflow lifecycle {family}:{current} has invalid transitions_to")
            boolean_fields = (
                "grants_authority",
                "reserves_version",
                "transitionable",
                "must_remain_visible",
            )
            if any(type(raw_row.get(field)) is not bool for field in boolean_fields):
                raise RuntimeError(f"managed workflow lifecycle {family}:{current} has a non-boolean property")
            adapter = raw_row.get("predecessor_adapter")
            if adapter not in _PREDECESSOR_ADAPTER_VALUES:
                raise RuntimeError(f"managed workflow lifecycle {family}:{current} has invalid predecessor_adapter")
            if raw_row["transitionable"] != bool(targets):
                raise RuntimeError(
                    f"managed workflow lifecycle {family}:{current} transitionable disagrees with transitions_to"
                )
            if not raw_row["must_remain_visible"]:
                raise RuntimeError(f"managed workflow lifecycle {family}:{current} must remain visible")
            if family != "release_record" and raw_row["reserves_version"]:
                raise RuntimeError(f"managed workflow lifecycle {family}:{current} cannot reserve a version")
            states[current] = LifecycleStatePolicy(
                transitions_to=tuple(targets),
                grants_authority=raw_row["grants_authority"],
                reserves_version=raw_row["reserves_version"],
                transitionable=raw_row["transitionable"],
                must_remain_visible=raw_row["must_remain_visible"],
                predecessor_adapter=adapter,
            )
        for current, row in states.items():
            unknown = set(row.transitions_to) - set(states)
            if unknown:
                raise RuntimeError(
                    f"managed workflow lifecycle {family}:{current} targets unknown state {sorted(unknown)[0]}"
                )
        lifecycles[family] = MappingProxyType(states)
    return MappingProxyType(lifecycles)


WORKFLOW_LIFECYCLES = _load_workflow_lifecycles()
WORKFLOW_TRANSITIONS = MappingProxyType({
    family: MappingProxyType(
        {state: frozenset(row.transitions_to) for state, row in states.items()}
    )
    for family, states in WORKFLOW_LIFECYCLES.items()
})
ALLOWED_STATUSES = frozenset({
    state
    for states in WORKFLOW_LIFECYCLES.values()
    for state in states
})
ACTIVE_COVERAGE_STATUSES = frozenset({
    state
    for family in ("definition", "work_order")
    for state, row in WORKFLOW_LIFECYCLES[family].items()
    if row.grants_authority
})


def _lifecycle_family(artifact_type: str) -> str:
    return artifact_type if artifact_type in {"work_order", "verification_record", "release_record", "decision"} else "definition"


def _lifecycle_policy(artifact_type: str, status: str) -> LifecycleStatePolicy | None:
    return WORKFLOW_LIFECYCLES[_lifecycle_family(artifact_type)].get(status)


def _grants_authority(artifact_type: str, status: str) -> bool:
    row = _lifecycle_policy(artifact_type, status)
    return bool(row and row.grants_authority)


def _reserves_version(status: str) -> bool:
    row = WORKFLOW_LIFECYCLES["release_record"].get(status)
    return bool(row and row.reserves_version)


def _active_record_status(artifact_type: str, status: str) -> bool:
    """Return whether a VREC/RLS is a live proposal or grants authority."""

    row = _lifecycle_policy(artifact_type, status)
    return bool(row and (row.transitionable or row.grants_authority))
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
LEGACY_ARCHITECTURE_STATUSES = {"implemented", "verified", "released"}
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
EXCLUDED_DIRECTORY_NAMES = {"templates", "evidence", ".git", ".idea", "target", "node_modules"}

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
}

#: SPEC-DCM-001 rules 2 and 3: the decision kinds and the closed option set of a deviation.
DECISION_KINDS = ("question", "deviation")
DEVIATION_OPTIONS = frozenset({"amend", "supersede", "accept", "stop"})
DECISION_TERMINAL = frozenset({"decided", "withdrawn"})


AUTHORING_OPENERS = ("THE SYSTEM SHALL", "WHEN ", "WHILE ", "IF ", "WHERE ")
AUTHORING_NAMED_SUBJECT = re.compile(r"^THE [A-Z][A-Za-z0-9 _-]{0,60} SHALL\b")
#: SPEC-TCM-003 TCM-RFR-003: the reader-first budgets, counted with code spans removed.
AUTHORING_STATEMENT_LIMIT = 30  # words
AUTHORING_BODY_LIMIT = 250  # words
AUTHORING_WHY_WORD_LIMIT = 120
AUTHORING_WHY_SENTENCE_LIMIT = 5
AUTHORING_SENTENCE_LIMIT = 25  # words
AUTHORING_CODE_IDENTIFIER_LIMIT = 3
AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT = 2
#: SPEC-TCM-004 TCM-RFI-002 to TCM-RFI-004: the reader-first intent budgets and the
#: acceptance vocabulary that marks a success-measure row as an acceptance check.
INTENT_OUTCOME_LIMIT = 30  # words
INTENT_BODY_LIMIT = 200  # words
INTENT_PROBLEM_WORD_LIMIT = 120
INTENT_PROBLEM_SENTENCE_LIMIT = 5
INTENT_CODE_IDENTIFIER_LIMIT = 2
_REPOSITORY_PATH_SPAN = re.compile(r"`[^`\s]*/[^`\s]*\.[A-Za-z0-9]{1,6}(?::\d+(?:-\d+)?)?`")
_LINE_RANGE_SPAN = re.compile(r"`[^`]*:\d+(?:-\d+)?`")
_ACCEPTANCE_VOCABULARY = re.compile(
    r"\b(CI|tests?|validator|validate|verification|implementation review|acceptance run|regression run|transaction)\b", re.I
)
_CODE_SPAN = re.compile(r"`[^`]*`")
_FENCE = re.compile(r"```.*?```", re.S)
_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'\-]*")
_SENTENCE_END = re.compile(r"[.!?](?:\s|$)")
_EVALUATION_EVENT = re.compile(r"^WHEN\s+[^,]*\b(is validated|is evaluated|is checked|runs|is run)\b[^,]*,", re.I)


def _prose(text: str) -> str:
    return _CODE_SPAN.sub(" ", _FENCE.sub(" ", text))


def _word_count(text: str) -> int:
    return len(_WORD.findall(_prose(text)))


def _sentences(text: str) -> list[str]:
    prose = " ".join(line.strip() for line in _prose(text).split("\n") if line.strip() and not line.strip().startswith(("|", "#", "**Given", "**When", "**Then")))
    return [item.strip() for item in _SENTENCE_END.split(prose) if item.strip()]


def _body_sections(body: str) -> dict[str, str]:
    """Second-level headings to their text, fenced code removed."""
    sections: dict[str, str] = {}
    current = ""
    for line in _FENCE.sub(" ", body.replace("\r\n", "\n")).split("\n"):
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, "")
        elif current:
            sections[current] += line + "\n"
    return sections
VERIFICATION_METHODS = ("test", "analysis", "inspection", "demonstration")
REQUIREMENT_PRIORITIES = ("must", "should", "could")


def validate_authoring(artifacts: list[Artifact], report_root: Path) -> tuple[list[Diagnostic], list[Diagnostic], list[Diagnostic]]:
    """Requirement-writing rules: statement shape signals, vocabulary, and optional attributes (SPEC-AUT-001).

    The statement and vocabulary signals are advisories (SPEC-AUT-002, AUT-ADV-001):
    they help the author of a draft and are raised only while the requirement is in
    `draft` (AUT-ADV-002). Errors and warnings are unchanged.
    """

    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    advisories: list[Diagnostic] = []
    catalog = {artifact.artifact_id for artifact in artifacts if artifact.artifact_id != "<unknown>"}
    for artifact in artifacts:
        if artifact.artifact_type == "intent":
            intent_errors, intent_advisories = _intent_authoring(artifact, report_root)
            errors.extend(intent_errors)
            advisories.extend(intent_advisories)
            continue
        if artifact.artifact_type != "requirement":
            continue
        draft = artifact.status == "draft"
        statement = artifact.metadata.get("statement")
        if isinstance(statement, str) and statement.strip() and draft:
            text = statement.strip()
            opener_ok = text.startswith(AUTHORING_OPENERS) or AUTHORING_NAMED_SUBJECT.match(text) is not None
            if text.startswith("IF ") and " THEN " not in text:
                opener_ok = False
            if not opener_ok:
                advisories.append(Diagnostic(_display_path(artifact.path, report_root), "W-AUT-001",
                    "statement does not open with one of the five shapes (THE SYSTEM SHALL, WHEN, WHILE, IF ... THEN, WHERE)", "maintenance"))
            shall_count = len(re.findall(r"\bSHALL\b", text))
            if shall_count > 1:
                advisories.append(Diagnostic(_display_path(artifact.path, report_root), "W-AUT-002",
                    f"statement carries {shall_count} SHALL obligations; one requirement states one obligation", "maintenance"))
            statement_words = _word_count(text)
            if statement_words > AUTHORING_STATEMENT_LIMIT:
                advisories.append(Diagnostic(_display_path(artifact.path, report_root), "W-AUT-003",
                    f"statement is {statement_words} words; the budget is {AUTHORING_STATEMENT_LIMIT}", "maintenance"))
            if _EVALUATION_EVENT.match(text) and " AND " not in text.split(",", 1)[0].upper():
                advisories.append(Diagnostic(_display_path(artifact.path, report_root), "W-AUT-010",
                    "statement opens WHEN on an event of evaluation with no other condition; an invariant reads THE SYSTEM SHALL", "maintenance"))
        if draft:
            advisories.extend(_reader_first_advisories(artifact, report_root))
        method = artifact.metadata.get("verification_method")
        if isinstance(method, str):
            if method.strip() and draft:
                advisories.append(Diagnostic(_display_path(artifact.path, report_root), "W-AUT-004",
                    "verification_method is a free-text string; the closed vocabulary is an array of test, analysis, inspection, demonstration", "maintenance"))
        elif isinstance(method, list):
            if not method or len(method) > len(VERIFICATION_METHODS) or len(set(method)) != len(method) or any(item not in VERIFICATION_METHODS for item in method):
                _add_error(errors, artifact, report_root, "E-AUT-001",
                    f"verification_method must list 1-4 distinct values from {', '.join(VERIFICATION_METHODS)}", plane="structure")
        notes = artifact.metadata.get("verification_notes")
        if notes is not None and (not isinstance(notes, str) or not notes.strip()):
            _add_error(errors, artifact, report_root, "E-AUT-002", "verification_notes must be a non-empty string when present", plane="structure")
        priority = artifact.metadata.get("priority")
        if priority is not None and priority not in REQUIREMENT_PRIORITIES:
            _add_error(errors, artifact, report_root, "E-AUT-002", f"priority must be one of {', '.join(REQUIREMENT_PRIORITIES)}", plane="structure")
        source = artifact.metadata.get("source")
        if source is not None:
            if not isinstance(source, str) or not source.strip():
                _add_error(errors, artifact, report_root, "E-AUT-002", "source must be a non-empty string when present", plane="structure")
            elif ID_PATTERN.fullmatch(source.strip()) is not None and source.strip() not in catalog:
                _add_error(errors, artifact, report_root, "E-AUT-002", f"source names an unknown artifact '{source.strip()}'", plane="structure")
        measure = artifact.metadata.get("measure")
        if measure is not None and (not isinstance(measure, str) or not measure.strip()):
            _add_error(errors, artifact, report_root, "E-AUT-002", "measure must be a non-empty string when present", plane="structure")
    return errors, warnings, advisories


def _reader_first_advisories(artifact: Artifact, report_root: Path) -> list[Diagnostic]:
    """SPEC-TCM-003 TCM-RFR-003: the body budgets of a requirement draft, advisories only."""

    body = artifact.body if isinstance(artifact.body, str) else ""
    path = _display_path(artifact.path, report_root)
    found: list[Diagnostic] = []
    body_words = _word_count(body)
    if body_words > AUTHORING_BODY_LIMIT:
        found.append(Diagnostic(path, "W-AUT-005", f"body is {body_words} words; the budget is {AUTHORING_BODY_LIMIT}", "maintenance"))
    sections = _body_sections(body)
    why = sections.get("Why")
    if why is not None:
        why_words = _word_count(why)
        why_sentences = len(_sentences(why))
        if why_words > AUTHORING_WHY_WORD_LIMIT or why_sentences > AUTHORING_WHY_SENTENCE_LIMIT:
            found.append(Diagnostic(path, "W-AUT-006",
                f"Why is {why_words} words in {why_sentences} sentences; the budget is {AUTHORING_WHY_WORD_LIMIT} words or {AUTHORING_WHY_SENTENCE_LIMIT} sentences", "maintenance"))
    longest = max((len(_WORD.findall(sentence)) for sentence in _sentences(body)), default=0)
    if longest > AUTHORING_SENTENCE_LIMIT:
        found.append(Diagnostic(path, "W-AUT-007", f"a body sentence is {longest} words; the budget is {AUTHORING_SENTENCE_LIMIT}", "maintenance"))
    identifiers = len(_CODE_SPAN.findall(_FENCE.sub(" ", body)))
    if identifiers > AUTHORING_CODE_IDENTIFIER_LIMIT:
        found.append(Diagnostic(path, "W-AUT-008",
            f"body cites {identifiers} code identifiers; the budget is {AUTHORING_CODE_IDENTIFIER_LIMIT}, the rest belongs in the specification", "maintenance"))
    plain = sections.get("In plain words")
    if body.strip() and plain is None:
        found.append(Diagnostic(path, "W-AUT-009", "body has no In plain words section; the reader-first shape opens with one or two plain sentences", "maintenance"))
    elif plain is not None and (not plain.strip() or len(_sentences(plain)) > AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT):
        found.append(Diagnostic(path, "W-AUT-009",
            f"In plain words has {len(_sentences(plain))} sentences; the budget is {AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT}", "maintenance"))
    return found


def _success_measure_rows(section: str) -> list[list[str]] | None:
    """The data rows of a Success measures table as cell lists; None when the table is malformed."""

    rows: list[list[str]] = []
    header_seen = False
    for line in section.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not header_seen:
            header_seen = True
            continue
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        if len(cells) < 4:
            return None
        rows.append(cells)
    return rows


def _intent_authoring(artifact: Artifact, report_root: Path) -> tuple[list[Diagnostic], list[Diagnostic]]:
    """SPEC-TCM-004 TCM-RFI-002 to TCM-RFI-004: the outcome field and the intent draft advisories."""

    errors: list[Diagnostic] = []
    found: list[Diagnostic] = []
    outcome = artifact.metadata.get("outcome")
    if outcome is not None and (not isinstance(outcome, str) or not outcome.strip()):
        _add_error(errors, artifact, report_root, "E-AUT-002", "outcome must be a non-empty string when present", plane="structure")
    if artifact.status != "draft":
        return errors, found
    path = _display_path(artifact.path, report_root)
    if not isinstance(outcome, str) or not outcome.strip():
        found.append(Diagnostic(path, "W-AUT-011", "intent has no outcome; one sentence names who can do or observe what after delivery", "maintenance"))
    else:
        outcome_words = _word_count(outcome)
        if outcome_words > INTENT_OUTCOME_LIMIT:
            found.append(Diagnostic(path, "W-AUT-011", f"outcome is {outcome_words} words; the budget is {INTENT_OUTCOME_LIMIT}", "maintenance"))
        outcome_spans = len(_CODE_SPAN.findall(outcome))
        if outcome_spans:
            found.append(Diagnostic(path, "W-AUT-011", f"outcome cites {outcome_spans} code identifiers; the outcome names no solution", "maintenance"))
    body = artifact.body if isinstance(artifact.body, str) else ""
    body_words = _word_count(body)
    if body_words > INTENT_BODY_LIMIT:
        found.append(Diagnostic(path, "W-AUT-005", f"body is {body_words} words; the budget is {INTENT_BODY_LIMIT}", "maintenance"))
    sections = _body_sections(body)
    problem = sections.get("Problem")
    if problem is not None:
        problem_words = _word_count(problem)
        problem_sentences = len(_sentences(problem))
        if problem_words > INTENT_PROBLEM_WORD_LIMIT or problem_sentences > INTENT_PROBLEM_SENTENCE_LIMIT:
            found.append(Diagnostic(path, "W-AUT-012",
                f"Problem is {problem_words} words in {problem_sentences} sentences; the budget is {INTENT_PROBLEM_WORD_LIMIT} words or {INTENT_PROBLEM_SENTENCE_LIMIT} sentences", "maintenance"))
    longest = max((len(_WORD.findall(sentence)) for sentence in _sentences(body)), default=0)
    if longest > AUTHORING_SENTENCE_LIMIT:
        found.append(Diagnostic(path, "W-AUT-007", f"a body sentence is {longest} words; the budget is {AUTHORING_SENTENCE_LIMIT}", "maintenance"))
    unfenced = _FENCE.sub(" ", body)
    identifiers = len(_CODE_SPAN.findall(unfenced))
    if identifiers > INTENT_CODE_IDENTIFIER_LIMIT:
        found.append(Diagnostic(path, "W-AUT-008",
            f"body cites {identifiers} code identifiers; the budget is {INTENT_CODE_IDENTIFIER_LIMIT}, the evidence belongs in a note, an RCA or an ADR", "maintenance"))
    citations = len({span for span in _CODE_SPAN.findall(unfenced) if _REPOSITORY_PATH_SPAN.fullmatch(span) or _LINE_RANGE_SPAN.fullmatch(span)})
    if citations:
        found.append(Diagnostic(path, "W-AUT-015",
            f"body cites {citations} repository paths or source line ranges; evidence is cited by link to a note, an RCA or an ADR, not quoted", "maintenance"))
    plain = sections.get("In plain words")
    if body.strip() and plain is None:
        found.append(Diagnostic(path, "W-AUT-009", "body has no In plain words section; the reader-first shape opens with one or two plain sentences", "maintenance"))
    elif plain is not None and (not plain.strip() or len(_sentences(plain)) > AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT):
        found.append(Diagnostic(path, "W-AUT-009",
            f"In plain words has {len(_sentences(plain))} sentences; the budget is {AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT}", "maintenance"))
    measures = sections.get("Success measures")
    if measures is not None:
        rows = _success_measure_rows(measures)
        if not rows:
            found.append(Diagnostic(path, "W-AUT-014", "Success measures has no row; a success measure is what an operator can count or time after delivery", "maintenance"))
        else:
            for cells in rows:
                match = _ACCEPTANCE_VOCABULARY.search(cells[3])
                if match is not None:
                    found.append(Diagnostic(path, "W-AUT-013",
                        f"success measure '{cells[0]}' is observed by {match.group(0)}; an acceptance check belongs in the verification contract", "maintenance"))
    return errors, found


def evidence_work_order_keys(evidence_path: str) -> tuple[str, ...]:
    """Extract exact work-order keys from a normalized repository path."""
    parts = PurePosixPath(evidence_path).parts
    if not parts:
        return ()
    candidates = [parts[-1]]
    if "evidence" in parts:
        candidates.extend(parts[parts.index("evidence") + 1 :])
    keys = {
        match.group(1)
        for component in candidates
        if (match := EVIDENCE_WORK_ORDER_PATTERN.match(component)) is not None
    }
    return tuple(sorted(keys))


def evidence_path_is_keyed_to(evidence_path: str, work_order_id: str) -> bool:
    return work_order_id in evidence_work_order_keys(evidence_path)


@dataclass(frozen=True, order=True)
class Diagnostic:
    path: str
    code: str
    message: str
    plane: str

    def __post_init__(self) -> None:
        if self.plane not in VALIDATION_PLANES:
            raise ValueError(f"unknown validation plane: {self.plane!r}")


@dataclass
class Artifact:
    path: Path
    metadata: dict[str, Any]
    body: str

    @property
    def artifact_id(self) -> str:
        value = self.metadata.get("id")
        return value if isinstance(value, str) else "<unknown>"

    @property
    def artifact_type(self) -> str:
        value = self.metadata.get("type")
        return value if isinstance(value, str) else "<unknown>"

    @property
    def status(self) -> str:
        value = self.metadata.get("status")
        return value if isinstance(value, str) else "<unknown>"

    @property
    def relations(self) -> dict[str, Any]:
        value = self.metadata.get("relations", {})
        return value if isinstance(value, dict) else {}


@dataclass
class ValidationReport:
    artifacts: list[Artifact]
    errors: list[Diagnostic]
    warnings: list[Diagnostic]
    # SPEC-AUT-002 AUT-ADV-001: the advisory class, apart from errors and warnings.
    advisories: list[Diagnostic] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors

    def to_dict(self, root: Path) -> dict[str, Any]:
        def relative(path: Path) -> str:
            try:
                return path.resolve().relative_to(root.resolve()).as_posix()
            except ValueError:
                return path.as_posix()

        plane_counts = {
            plane: {
                "errors": sum(item.plane == plane for item in self.errors),
                "warnings": sum(item.plane == plane for item in self.warnings),
            }
            for plane in VALIDATION_PLANES
        }
        return {
            "taxonomy": TAXONOMY_VERSION,
            "valid": self.valid,
            "artifact_count": len(self.artifacts),
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "advisory_count": len(self.advisories),
            "errors": [asdict(item) for item in sorted(self.errors)],
            "warnings": [asdict(item) for item in sorted(self.warnings)],
            "advisories": [asdict(item) for item in sorted(self.advisories)],
            "plane_counts": plane_counts,
            "artifacts": [
                {
                    "id": artifact.artifact_id,
                    "type": artifact.artifact_type,
                    "status": artifact.status,
                    "path": relative(artifact.path),
                }
                for artifact in sorted(self.artifacts, key=lambda item: (item.artifact_id, item.path.as_posix()))
            ],
        }


def load_revision_policy(repository_root: Path) -> dict[str, bool]:
    defaults = {"required_for_verified_work": False, "required_for_release": False}
    path = repository_root / ".engineering-harness.toml"
    if not path.is_file():
        return defaults
    try:
        metadata = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return defaults
    policy = metadata.get("revision_provenance", {})
    if not isinstance(policy, dict):
        return defaults
    return {
        key: value if isinstance((value := policy.get(key)), bool) else default
        for key, default in defaults.items()
    }


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _is_excluded(path: Path, artifact_root: Path) -> bool:
    try:
        relative_parts = path.relative_to(artifact_root).parts
    except ValueError:
        relative_parts = path.parts
    return any(part in EXCLUDED_DIRECTORY_NAMES for part in relative_parts[:-1])


def discover_candidate_files(artifact_root: Path) -> list[Path]:
    if not artifact_root.exists():
        return []
    return sorted(
        path
        for path in artifact_root.rglob("*.md")
        if path.is_file() and not _is_excluded(path, artifact_root)
    )


def parse_formal_artifact(path: Path, report_root: Path) -> tuple[Artifact | None, Diagnostic | None]:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return None, Diagnostic(_display_path(path, report_root), "E001", f"cannot read artifact: {exc}", "structure")

    if not text.startswith("+++\n") and text != "+++":
        return None, None

    lines = text.splitlines()
    try:
        closing_index = lines.index("+++", 1)
    except ValueError:
        return None, Diagnostic(
            _display_path(path, report_root),
            "E001",
            "formal artifact starts TOML front matter but has no closing +++ delimiter",
            "structure",
        )

    front_matter_text = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :]).lstrip("\n")

    try:
        metadata = tomllib.loads(front_matter_text)
    except tomllib.TOMLDecodeError as exc:
        return None, Diagnostic(
            _display_path(path, report_root),
            "E001",
            f"invalid TOML front matter: {exc}",
            "structure",
        )

    if not isinstance(metadata, dict):
        return None, Diagnostic(
            _display_path(path, report_root),
            "E001",
            "front matter must be a TOML table",
            "structure",
        )

    return Artifact(path=path, metadata=metadata, body=body), None


def load_artifacts(artifact_root: Path, report_root: Path) -> tuple[list[Artifact], list[Diagnostic]]:
    artifacts: list[Artifact] = []
    errors: list[Diagnostic] = []
    for path in discover_candidate_files(artifact_root):
        artifact, error = parse_formal_artifact(path, report_root)
        if error is not None:
            errors.append(error)
        elif artifact is not None:
            artifacts.append(artifact)
    return artifacts, errors


def _add_error(
    errors: list[Diagnostic],
    artifact: Artifact,
    report_root: Path,
    code: str,
    message: str,
    *,
    plane: str,
) -> None:
    errors.append(Diagnostic(_display_path(artifact.path, report_root), code, message, plane))


def _require_non_empty_string(
    artifact: Artifact,
    field: str,
    errors: list[Diagnostic],
    report_root: Path,
    *,
    plane: str = "structure",
) -> str | None:
    value = artifact.metadata.get(field)
    if not isinstance(value, str) or not value.strip():
        _add_error(
            errors,
            artifact,
            report_root,
            "E002",
            f"field '{field}' must be a non-empty string",
            plane=plane,
        )
        return None
    return value.strip()


def _require_non_empty_string_list(
    artifact: Artifact,
    field: str,
    errors: list[Diagnostic],
    report_root: Path,
    *,
    code: str = "E002",
    container: dict[str, Any] | None = None,
    plane: str = "structure",
) -> list[str] | None:
    source = artifact.metadata if container is None else container
    value = source.get(field)
    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item.strip() for item in value):
        _add_error(
            errors,
            artifact,
            report_root,
            code,
            f"field '{field}' must be a non-empty array of strings",
            plane=plane,
        )
        return None
    return [item.strip() for item in value]


def _validate_git_identity(
    artifact: Artifact,
    errors: list[Diagnostic],
    report_root: Path,
) -> tuple[str | None, str | None]:
    commit = _require_non_empty_string(
        artifact, "commit", errors, report_root, plane="governance"
    )
    object_format = _require_non_empty_string(
        artifact, "git_object_format", errors, report_root, plane="governance"
    )
    if object_format is not None and object_format not in GIT_COMMIT_PATTERNS:
        _add_error(
            errors,
            artifact,
            report_root,
            "E009",
            "field 'git_object_format' must be 'sha1' or 'sha256'",
            plane="governance",
        )
    elif commit is not None and object_format is not None and not GIT_COMMIT_PATTERNS[object_format].fullmatch(commit):
        _add_error(
            errors,
            artifact,
            report_root,
            "E009",
            f"field 'commit' must be a full lowercase {object_format} Git object ID",
            plane="governance",
        )
    return commit, object_format


def _validate_timestamp(
    artifact: Artifact,
    field: str,
    errors: list[Diagnostic],
    report_root: Path,
) -> None:
    value = _require_non_empty_string(
        artifact, field, errors, report_root, plane="governance"
    )
    if value is not None:
        try:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            _add_error(
                errors,
                artifact,
                report_root,
                "E009",
                f"field '{field}' must use a valid YYYY-MM-DDTHH:MM:SSZ timestamp",
                plane="governance",
            )


def _validate_evidence_paths(
    artifact: Artifact,
    errors: list[Diagnostic],
    repository_root: Path,
) -> None:
    paths = _require_non_empty_string_list(
        artifact,
        "evidence_paths",
        errors,
        repository_root,
        plane="governance",
    )
    if paths is None:
        return
    resolved_root = repository_root.resolve()
    for raw_path in paths:
        relative = Path(raw_path)
        if relative.is_absolute() or "\\" in raw_path or any(part in {"", ".", ".."} for part in relative.parts):
            _add_error(
                errors,
                artifact,
                repository_root,
                "E012",
                f"evidence path must be a normalized repository-relative path: '{raw_path}'",
                plane="governance",
            )
            continue
        candidate = repository_root / relative
        probe = repository_root
        symlinked = False
        for part in relative.parts:
            probe = probe / part
            if probe.is_symlink():
                symlinked = True
                break
        try:
            resolved = candidate.resolve()
            resolved.relative_to(resolved_root)
        except (OSError, ValueError):
            _add_error(
                errors,
                artifact,
                repository_root,
                "E012",
                f"evidence path escapes the repository: '{raw_path}'",
                plane="governance",
            )
            continue
        if symlinked:
            _add_error(
                errors,
                artifact,
                repository_root,
                "E012",
                f"evidence path must not traverse a symlink: '{raw_path}'",
                plane="governance",
            )
        elif not candidate.is_file():
            _add_error(
                errors,
                artifact,
                repository_root,
                "E012",
                f"evidence path does not identify an existing file: '{raw_path}'",
                plane="governance",
            )


def _unique_evaluator_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate evaluator evidence field: {key}")
        value[key] = item
    return value


def _evaluator_binding_error(
    artifact: Artifact,
    errors: list[Diagnostic],
    repository_root: Path,
    message: str,
) -> None:
    _add_error(errors, artifact, repository_root, "E012", message, plane="governance")


def _valid_evaluator_origin(value: Any) -> bool:
    if not isinstance(value, str) or EVALUATOR_ORIGIN_PATTERN.fullmatch(value) is None:
        return False
    suffix = value.removeprefix("<evaluator-root>").removeprefix("/")
    return not suffix or all(part not in {"", ".", ".."} for part in suffix.split("/"))


def _validate_evaluator_evidence_binding(
    artifact: Artifact,
    errors: list[Diagnostic],
    repository_root: Path,
    *,
    required: bool,
    require_archive: bool = False,
    match_current_lock: bool = True,
) -> None:
    raw_path = artifact.metadata.get("evaluator_evidence_path")
    raw_digest = artifact.metadata.get("evaluator_evidence_sha256")
    if raw_path is None and raw_digest is None and not required:
        return
    if not isinstance(raw_path, str) or not raw_path:
        _evaluator_binding_error(
            artifact, errors, repository_root, "field 'evaluator_evidence_path' must be a non-empty string"
        )
        return
    if not isinstance(raw_digest, str) or SHA256_PATTERN.fullmatch(raw_digest) is None:
        _evaluator_binding_error(
            artifact,
            errors,
            repository_root,
            "field 'evaluator_evidence_sha256' must be a lowercase SHA-256 value",
        )
        return
    relative = Path(raw_path)
    if (
        relative.is_absolute()
        or "\\" in raw_path
        or any(part in {"", ".", ".."} for part in relative.parts)
        or relative.suffix != ".json"
        or relative.parts[:2] != ("docs", "engineering")
        or "evidence" not in relative.parts
    ):
        _evaluator_binding_error(
            artifact, errors, repository_root, "evaluator evidence path must be normalized and repository-relative"
        )
        return
    candidate = repository_root / relative
    probe = repository_root
    for part in relative.parts:
        probe = probe / part
        if probe.is_symlink():
            _evaluator_binding_error(
                artifact, errors, repository_root, "evaluator evidence path must not traverse a symlink"
            )
            return
    try:
        candidate.resolve().relative_to(repository_root.resolve())
        raw = candidate.read_bytes()
    except (OSError, ValueError):
        _evaluator_binding_error(
            artifact, errors, repository_root, "evaluator evidence path is unavailable or escapes the repository"
        )
        return
    if not raw or len(raw) > EVALUATOR_EVIDENCE_MAX_BYTES:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence size is invalid")
        return
    if hashlib.sha256(raw).hexdigest() != raw_digest:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence digest does not match its bytes")
        return
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_evaluator_object)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        _evaluator_binding_error(artifact, errors, repository_root, f"invalid evaluator evidence JSON: {exc}")
        return
    canonical = (json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
    if raw != canonical or not isinstance(value, dict):
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence bytes are not canonical")
        return
    if set(value) != {"schema", "role", "evaluator", "origins", "environment", "diagnostics"}:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence field set is not canonical")
        return
    evaluator = value.get("evaluator")
    origins = value.get("origins")
    environment = value.get("environment")
    if value.get("schema") != EVALUATOR_EVIDENCE_SCHEMA or value.get("role") != "released-evaluator":
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence schema or role is invalid")
        return
    if not isinstance(evaluator, dict) or set(evaluator) != {
        "version", "payload_manifest", "payload_sha256", "archive_name", "archive_sha256"
    }:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator identity field set is not canonical")
        return
    if evaluator.get("payload_manifest") != EVALUATOR_PAYLOAD_MANIFEST:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator payload manifest is unsupported")
        return
    evaluator_version = evaluator.get("version")
    if not isinstance(evaluator_version, str) or EVALUATOR_VERSION_PATTERN.fullmatch(evaluator_version) is None:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator version is invalid")
        return
    if not isinstance(evaluator.get("payload_sha256"), str) or SHA256_PATTERN.fullmatch(evaluator["payload_sha256"]) is None:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator payload digest is invalid")
        return
    archive_name = evaluator.get("archive_name")
    archive_sha256 = evaluator.get("archive_sha256")
    if (archive_name is None) != (archive_sha256 is None):
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator archive fields must appear together")
        return
    if archive_name is not None and (
        not isinstance(archive_name, str)
        or archive_name != f"se_harness-{evaluator_version.replace('-', '_')}-py3-none-any.whl"
        or not isinstance(archive_sha256, str)
        or SHA256_PATTERN.fullmatch(archive_sha256) is None
    ):
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator archive identity is invalid")
        return
    if require_archive and archive_name is None:
        _evaluator_binding_error(
            artifact,
            errors,
            repository_root,
            "release evaluator evidence requires an archive name and SHA-256",
        )
        return
    if not isinstance(origins, dict) or set(origins) != {
        "python_executable", "module", "distribution", "templates", "entry_point"
    } or any(not _valid_evaluator_origin(item) for item in origins.values()):
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator origins are not canonical")
        return
    expected_environment = {
        "isolated_python", "user_site_enabled", "pythonpath_present", "entry_point_resolved", "checkout_excluded"
    }
    if (
        not isinstance(environment, dict)
        or set(environment) != expected_environment
        or any(type(environment.get(field)) is not bool for field in expected_environment)
        or not environment.get("isolated_python")
        or environment.get("user_site_enabled")
        or environment.get("pythonpath_present")
        or not environment.get("entry_point_resolved")
        or not environment.get("checkout_excluded")
        or value.get("diagnostics") != []
    ):
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator environment proof is invalid")
        return
    if not match_current_lock:
        return
    try:
        lock = json.loads(
            (repository_root / ".engineering-harness.lock").read_text(encoding="utf-8"),
            object_pairs_hook=_unique_evaluator_object,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        _evaluator_binding_error(artifact, errors, repository_root, f"cannot read standard evaluator lock: {exc}")
        return
    expected_evaluator = lock.get("evaluator") if isinstance(lock, dict) and lock.get("schema") == 3 else None
    expected_fields = {"version", "payload_manifest", "payload_sha256", "archive_name", "archive_sha256"}
    if (
        not isinstance(expected_evaluator, dict)
        or set(expected_evaluator) - expected_fields
        or lock.get("tool_version") != expected_evaluator.get("version")
    ):
        _evaluator_binding_error(artifact, errors, repository_root, "standard evaluator lock identity is invalid")
        return
    normalized_expected = (
        {
            "version": expected_evaluator.get("version"),
            "payload_manifest": expected_evaluator.get("payload_manifest"),
            "payload_sha256": expected_evaluator.get("payload_sha256"),
            "archive_name": expected_evaluator.get("archive_name"),
            "archive_sha256": expected_evaluator.get("archive_sha256"),
        }
        if isinstance(expected_evaluator, dict)
        else None
    )
    if normalized_expected is None or evaluator != normalized_expected:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence differs from the standard lock")


def validate_common_metadata(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    seen: dict[str, Artifact] = {}

    for artifact in artifacts:
        artifact_id = _require_non_empty_string(artifact, "id", errors, report_root)
        artifact_type = _require_non_empty_string(artifact, "type", errors, report_root)
        _require_non_empty_string(artifact, "title", errors, report_root)
        status = _require_non_empty_string(artifact, "status", errors, report_root)
        _require_non_empty_string_list(artifact, "owners", errors, report_root)
        created = _require_non_empty_string(artifact, "created", errors, report_root)
        updated = _require_non_empty_string(artifact, "updated", errors, report_root)

        if artifact_id is not None:
            if not ID_PATTERN.fullmatch(artifact_id):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E002",
                    f"id '{artifact_id}' must use uppercase letters/digits/hyphens and end in a three-digit sequence",
                    plane="structure",
                )
            previous = seen.get(artifact_id)
            if previous is not None:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E003",
                    f"duplicate id '{artifact_id}' also declared in {_display_path(previous.path, report_root)}",
                    plane="structure",
                )
            else:
                seen[artifact_id] = artifact

        if artifact_type is not None:
            expected_prefix = TYPE_PREFIX.get(artifact_type)
            if expected_prefix is None:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E002",
                    f"unknown artifact type '{artifact_type}'",
                    plane="structure",
                )
            elif artifact_id is not None and not artifact_id.startswith(expected_prefix):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E004",
                    f"id '{artifact_id}' must start with '{expected_prefix}' for type '{artifact_type}'",
                    plane="structure",
                )

        if (
            status is not None
            and artifact_type is not None
            and status not in WORKFLOW_LIFECYCLES[_lifecycle_family(artifact_type)]
        ):
            _add_error(
                errors,
                artifact,
                report_root,
                "E002",
                f"status '{status}' is not declared for {_lifecycle_family(artifact_type)} artifacts",
                plane="structure",
            )

        for field_name, field_value in (("created", created), ("updated", updated)):
            if field_value is not None and not ISO_DATE_PATTERN.fullmatch(field_value):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E002",
                    f"field '{field_name}' must use YYYY-MM-DD",
                    plane="structure",
                )

        relations = artifact.metadata.get("relations", {})
        if not isinstance(relations, dict):
            _add_error(
                errors,
                artifact,
                report_root,
                "E006",
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
            _add_error(
                errors, artifact, report_root, "E014",
                "field 'lifecycle_events' must be a non-empty array of tables when present",
                plane="governance",
            )
            continue
        previous_to: str | None = None
        previous_at: str | None = None
        valid_events: list[dict[str, str]] = []
        family = _lifecycle_family(artifact.artifact_type)
        for index, event in enumerate(events):
            if not isinstance(event, dict):
                _add_error(
                    errors, artifact, report_root, "E014",
                    f"lifecycle event {index + 1} must be a TOML table",
                    plane="governance",
                )
                continue
            values: dict[str, str] = {}
            for field in ("from", "to", "decided_at", "decided_by"):
                value = event.get(field)
                if not isinstance(value, str) or not value.strip():
                    _add_error(
                        errors, artifact, report_root, "E014",
                        f"lifecycle event {index + 1} field '{field}' must be a non-empty string",
                        plane="governance",
                    )
                else:
                    values[field] = value.strip()
            reason = event.get("reason")
            if reason is not None and (not isinstance(reason, str) or not reason.strip()):
                _add_error(
                    errors, artifact, report_root, "E014",
                    f"lifecycle event {index + 1} field 'reason' must be a non-empty string when present",
                    plane="governance",
                )
            decided_at = values.get("decided_at")
            if decided_at is not None:
                try:
                    datetime.strptime(decided_at, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    _add_error(
                        errors, artifact, report_root, "E014",
                        f"lifecycle event {index + 1} field 'decided_at' must use a valid YYYY-MM-DDTHH:MM:SSZ timestamp",
                        plane="governance",
                    )
                if previous_at is not None and decided_at < previous_at:
                    _add_error(
                        errors, artifact, report_root, "E014",
                        "lifecycle events must be ordered chronologically",
                        plane="governance",
                    )
                previous_at = decided_at
            source = values.get("from")
            target = values.get("to")
            if source is not None and target is not None:
                if target not in WORKFLOW_TRANSITIONS.get(family, {}).get(source, set()):
                    _add_error(
                        errors, artifact, report_root, "E014",
                        f"lifecycle event {index + 1} contains unsupported transition {source} -> {target}",
                        plane="governance",
                    )
                if previous_to is not None and source != previous_to:
                    _add_error(
                        errors, artifact, report_root, "E014",
                        f"lifecycle event {index + 1} starts at '{source}' instead of previous target '{previous_to}'",
                        plane="governance",
                    )
                previous_to = target
            if len(values) == 4:
                valid_events.append(values)
        if previous_to is not None and previous_to != artifact.status:
            _add_error(
                errors, artifact, report_root, "E014",
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
                _add_error(
                    errors, artifact, report_root, "E014",
                    "rejection lifecycle event requires a non-empty reason",
                    plane="governance",
                )
            if artifact.metadata.get("rejection_reason") != reason:
                _add_error(
                    errors, artifact, report_root, "E014",
                    "field 'rejection_reason' must equal the rejection lifecycle event reason",
                    plane="governance",
                )
        elif artifact.artifact_type == "verification_record" and latest["to"] == "superseded":
            expected_fields = ("superseded_at", "supersession_authorized_by")
            reason = events[-1].get("reason") if isinstance(events[-1], dict) else None
            successors = artifact.relations.get("superseded_by", [])
            if not isinstance(reason, str) or successors != [reason]:
                _add_error(
                    errors, artifact, report_root, "E014",
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
                _add_error(
                    errors, artifact, report_root, "E014",
                    f"field '{timestamp_field}' must equal the latest lifecycle decision timestamp",
                    plane="governance",
                )
            if not legacy_decision_record and artifact.metadata.get(actor_field) != latest["decided_by"]:
                _add_error(
                    errors, artifact, report_root, "E014",
                    f"field '{actor_field}' must equal the latest lifecycle decision actor",
                    plane="governance",
                )
    return errors


def validate_type_specific_metadata(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    errors: list[Diagnostic] = []

    relation_requirements: dict[str, tuple[str, ...]] = {
        "capability": ("derives_from",),
        "requirement": ("derives_from",),
        "specification": ("specifies",),
        "architecture": (),
        "adr": ("decides",),
        "verification": ("verifies",),
        "work_order": ("implements", "specifications", "verification"),
        "release_contract": ("gates",),
        "verification_record": ("verifies_work_order", "conforms_to"),
        "release_record": ("satisfies", "includes_verification", "releases_work"),
        "operating_contract": ("assures",),
        "decision": ("concerns", "blocks"),
    }

    for artifact in artifacts:
        artifact_type = artifact.metadata.get("type")
        if not isinstance(artifact_type, str):
            continue

        if artifact_type == "requirement":
            statement = _require_non_empty_string(artifact, "statement", errors, report_root)
            if not isinstance(artifact.metadata.get("verification_method"), list):
                _require_non_empty_string(artifact, "verification_method", errors, report_root)
            if statement is not None and re.search(r"\bSHALL\b", statement) is None:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E005",
                    "requirement statement must contain normative keyword SHALL",
                    plane="structure",
                )

        if artifact_type == "verification_record":
            _validate_git_identity(artifact, errors, report_root)
            worktree_state = _require_non_empty_string(
                artifact, "worktree_state", errors, report_root, plane="governance"
            )
            if worktree_state is not None and worktree_state != "clean":
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E009",
                    "field 'worktree_state' must be 'clean'",
                    plane="governance",
                )
            prepared = "prepared_at" in artifact.metadata or "prepared_by" in artifact.metadata
            if prepared:
                _validate_timestamp(artifact, "prepared_at", errors, report_root)
                _require_non_empty_string(artifact, "prepared_by", errors, report_root, plane="governance")
            if artifact.status in {"verified", "released"}:
                _validate_timestamp(artifact, "verified_at", errors, report_root)
                if prepared:
                    _require_non_empty_string(artifact, "verified_by", errors, report_root, plane="governance")
            elif artifact.status == "superseded":
                if prepared:
                    for field_name in ("verified_at", "verified_by"):
                        if field_name in artifact.metadata:
                            _add_error(
                                errors, artifact, report_root, "E009",
                                f"prepared superseded verification_record must omit decision field '{field_name}'",
                                plane="governance",
                            )
                else:
                    _validate_timestamp(artifact, "verified_at", errors, report_root)
            snapshot_hash = _require_non_empty_string(
                artifact,
                "artifact_snapshot_sha256",
                errors,
                report_root,
                plane="governance",
            )
            if snapshot_hash is not None and not SHA256_PATTERN.fullmatch(snapshot_hash):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E009",
                    "field 'artifact_snapshot_sha256' must be a lowercase SHA-256 value",
                    plane="governance",
            )
            _validate_evidence_paths(artifact, errors, report_root)
            _validate_evaluator_evidence_binding(
                artifact,
                errors,
                report_root,
                required=False,
                match_current_lock=artifact.status == "ready",
            )
            if artifact.status not in WORKFLOW_LIFECYCLES["verification_record"]:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E009",
                    "verification_record status is not declared by the workflow lifecycle registry",
                    plane="governance",
                )
            if artifact.status == "ready" and prepared:
                for field_name in ("verified_at", "verified_by"):
                    if field_name in artifact.metadata:
                        _add_error(
                            errors, artifact, report_root, "E009",
                            f"ready verification_record must omit decision field '{field_name}'",
                            plane="governance",
                        )
            if artifact.status == "rejected":
                _validate_timestamp(artifact, "rejected_at", errors, report_root)
                _require_non_empty_string(artifact, "rejected_by", errors, report_root, plane="governance")
                _require_non_empty_string(artifact, "rejection_reason", errors, report_root, plane="governance")
            if artifact.status == "superseded":
                _validate_timestamp(artifact, "superseded_at", errors, report_root)
                _require_non_empty_string(artifact, "supersession_authorized_by", errors, report_root)
                successors = _require_non_empty_string_list(
                    artifact,
                    "superseded_by",
                    errors,
                    report_root,
                    code="E009",
                    container=artifact.relations,
                    plane="governance",
                )
                if successors is not None and len(successors) != 1:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E009",
                        "relation 'superseded_by' must contain exactly one verification record",
                        plane="governance",
                    )
            else:
                for field_name in ("superseded_at", "supersession_authorized_by"):
                    if field_name in artifact.metadata:
                        _add_error(
                            errors,
                            artifact,
                            report_root,
                            "E009",
                            f"field '{field_name}' is allowed only when verification_record status is superseded",
                            plane="governance",
                        )
                if "superseded_by" in artifact.relations:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E009",
                        "relation 'superseded_by' is allowed only when verification_record status is superseded",
                        plane="governance",
                    )

        if artifact_type == "release_record":
            _validate_git_identity(artifact, errors, report_root)
            release_version = _require_non_empty_string(
                artifact, "version", errors, report_root, plane="governance"
            )
            prepared = "prepared_at" in artifact.metadata or "prepared_by" in artifact.metadata
            if prepared:
                _validate_timestamp(artifact, "prepared_at", errors, report_root)
                _require_non_empty_string(artifact, "prepared_by", errors, report_root, plane="governance")
            authorized_by: str | None = None
            if artifact.status == "released":
                _validate_timestamp(artifact, "released_at", errors, report_root)
                authorized_by = _require_non_empty_string(
                    artifact, "authorized_by", errors, report_root, plane="governance"
                )
            owners = artifact.metadata.get("owners", [])
            if authorized_by is not None and isinstance(owners, list) and authorized_by not in owners:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E009",
                    "field 'authorized_by' must identify one of the record owners",
                    plane="governance",
                )
            tag = artifact.metadata.get("tag")
            if tag is not None and (not isinstance(tag, str) or not tag.strip()):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E009",
                    "field 'tag' must be a non-empty string when present",
                    plane="governance",
                )
            if artifact.status == "ready" and prepared:
                for field_name in ("released_at", "authorized_by"):
                    if field_name in artifact.metadata:
                        _add_error(
                            errors, artifact, report_root, "E009",
                            f"ready release_record must omit decision field '{field_name}'",
                            plane="governance",
                        )
            if artifact.status == "rejected":
                _validate_timestamp(artifact, "rejected_at", errors, report_root)
                _require_non_empty_string(artifact, "rejected_by", errors, report_root, plane="governance")
                _require_non_empty_string(artifact, "rejection_reason", errors, report_root, plane="governance")
            if artifact.status not in WORKFLOW_LIFECYCLES["release_record"]:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E009",
                    "release_record status is not declared by the workflow lifecycle registry",
                    plane="governance",
                )
            # REQ-LRE-003 (the evaluator-evidence floor, owner decision of
            # 2026-08-30, WO-LRE-002): a released record carrying neither
            # evidence field is not assessed against the binding. A partially
            # bound record keeps its existing error.
            unbound = (
                artifact.status == "released"
                and artifact.metadata.get("evaluator_evidence_path") is None
                and artifact.metadata.get("evaluator_evidence_sha256") is None
            )
            _validate_evaluator_evidence_binding(
                artifact,
                errors,
                report_root,
                required=not unbound,
                require_archive=True,
                match_current_lock=artifact.status == "ready",
            )

        if artifact_type == "work_order" and "architecture" in artifact.relations:
            _require_non_empty_string_list(
                artifact,
                "architecture",
                errors,
                report_root,
                code="E005",
                container=artifact.relations,
            )

        required_relations = relation_requirements.get(artifact_type, ())
        relations = artifact.metadata.get("relations", {})
        if not isinstance(relations, dict):
            continue
        for relation_name in required_relations:
            _require_non_empty_string_list(
                artifact,
                relation_name,
                errors,
                report_root,
                code="E005",
                container=relations,
            )

    return errors


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
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E006",
                    f"relation '{relation_name}' must be an array of artifact IDs",
                    plane="structure",
                )
                continue
            for target in targets:
                if not isinstance(target, str) or not target.strip():
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E006",
                        f"relation '{relation_name}' contains a non-string or empty target",
                        plane="structure",
                    )
                    continue
                if target == artifact.artifact_id:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E006",
                        f"artifact '{artifact.artifact_id}' must not reference itself via '{relation_name}'",
                        plane="structure",
                    )
                elif target not in catalog:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E006",
                        f"artifact '{artifact.artifact_id}' relation '{relation_name}' references unknown target '{target}'",
                        plane="structure",
                    )
                else:
                    allowed_types = RELATION_TARGET_TYPES.get((artifact.artifact_type, relation_name))
                    target_type = catalog[target].artifact_type
                    if allowed_types is not None and target_type not in allowed_types:
                        expected = ", ".join(sorted(allowed_types))
                        _add_error(
                            errors,
                            artifact,
                            report_root,
                            "E011",
                            f"relation '{relation_name}' target '{target}' must have type {expected}, found {target_type}",
                            plane="structure",
                        )
    return errors


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
            and _grants_authority(record.artifact_type, record.status)
            for work_order_id in _relation_targets(record, "verifies_work_order")
        }
        for work_order in artifacts:
            if (
                work_order.artifact_type == "work_order"
                and work_order.status in {"verified", "released"}
                and work_order.artifact_id not in verified_work
            ):
                _add_error(
                    errors,
                    work_order,
                    report_root,
                    "E010",
                    f"{work_order.status} work order requires coverage by a verified or released verification record",
                    plane="policy",
                )

    for artifact in artifacts:
        if artifact.artifact_type == "verification_record":
            for field_name in ("evidence_paths",):
                duplicates = _duplicate_strings(artifact.metadata.get(field_name))
                if duplicates:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E010",
                        f"field '{field_name}' contains duplicate values: {', '.join(duplicates)}",
                        plane="governance",
                    )
            for relation_name in ("verifies_work_order", "conforms_to", "superseded_by"):
                duplicates = _duplicate_strings(artifact.relations.get(relation_name))
                if duplicates:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E010",
                        f"relation '{relation_name}' contains duplicate targets: {', '.join(duplicates)}",
                        plane="governance",
                    )
            work_order_ids = _relation_targets(artifact, "verifies_work_order")
            verification_ids = _relation_targets(artifact, "conforms_to")
            declared_verification: set[str] = set()
            for work_order_id in work_order_ids:
                work_order = catalog.get(work_order_id)
                if work_order is None or work_order.artifact_type != "work_order":
                    continue
                declared_verification.update(_relation_targets(work_order, "verification"))
                if (
                    _active_record_status(artifact.artifact_type, artifact.status)
                    and not _grants_authority(work_order.artifact_type, work_order.status)
                ):
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E010",
                        f"active verification record requires active work order '{work_order_id}'",
                        plane="governance",
                    )
            for verification_id in verification_ids:
                verification = catalog.get(verification_id)
                if (
                    verification is not None
                    and verification.artifact_type == "verification"
                    and _active_record_status(artifact.artifact_type, artifact.status)
                    and not _grants_authority(verification.artifact_type, verification.status)
                ):
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E010",
                        f"active verification record requires active verification contract '{verification_id}'",
                        plane="governance",
                    )
            missing_verification = declared_verification - verification_ids
            extra_verification = verification_ids - declared_verification
            if missing_verification and (
                "prepared_at" in artifact.metadata or len(work_order_ids) > 1
            ):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"verification record is missing contracts declared by selected work: {', '.join(sorted(missing_verification))}",
                    plane="governance",
                )
            if extra_verification:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
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
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E010",
                        f"aggregate evidence is not keyed to work orders: {', '.join(uncovered)}",
                        plane="governance",
                    )
            if artifact.status == "superseded":
                successor_ids = sorted(_relation_targets(artifact, "superseded_by"))
                if len(successor_ids) == 1:
                    successor_id = successor_ids[0]
                    successor = catalog.get(successor_id)
                    if successor is not None and successor.artifact_type == "verification_record":
                        if not _grants_authority(successor.artifact_type, successor.status):
                            _add_error(
                                errors,
                                artifact,
                                report_root,
                                "E010",
                                f"superseding verification record '{successor_id}' must be verified or released",
                                plane="governance",
                            )
                        missing_work = work_order_ids - _relation_targets(successor, "verifies_work_order")
                        if missing_work:
                            _add_error(
                                errors,
                                artifact,
                                report_root,
                                "E010",
                                f"superseding verification record '{successor_id}' omits work orders: {', '.join(sorted(missing_work))}",
                                plane="governance",
                            )
            if artifact.artifact_id in supersession_cycle_nodes:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"verification supersession cycle detected among: {', '.join(sorted(supersession_cycle_nodes))}",
                    plane="governance",
                )

        if artifact.artifact_type != "release_record":
            continue
        for relation_name in ("satisfies", "includes_verification", "releases_work"):
            duplicates = _duplicate_strings(artifact.relations.get(relation_name))
            if duplicates:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"relation '{relation_name}' contains duplicate targets: {', '.join(duplicates)}",
                    plane="governance",
                )
        version = artifact.metadata.get("version")
        if _reserves_version(artifact.status) and isinstance(version, str) and version.strip():
            release_versions.setdefault(version.strip(), []).append(artifact)
        release_commit = artifact.metadata.get("commit")
        release_format = artifact.metadata.get("git_object_format")
        released_work = _relation_targets(artifact, "releases_work")
        for work_order_id in released_work:
            work_order = catalog.get(work_order_id)
            if (
                work_order is not None
                and work_order.artifact_type == "work_order"
                and _active_record_status(artifact.artifact_type, artifact.status)
                and work_order.status not in RELEASABLE_WORK_STATUSES
            ):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"active release record requires implemented, verified, or released work order '{work_order_id}'",
                    plane="governance",
                )
        verification_work: set[str] = set()
        for verification_id in _relation_targets(artifact, "includes_verification"):
            verification = catalog.get(verification_id)
            if verification is None or verification.artifact_type != "verification_record":
                continue
            if _active_record_status(verification.artifact_type, verification.status):
                verification_work.update(_relation_targets(verification, "verifies_work_order"))
            if _active_record_status(artifact.artifact_type, artifact.status) and verification.status == "superseded":
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"active release record must not include superseded verification record '{verification_id}'",
                    plane="governance",
                )
            if release_commit != verification.metadata.get("commit") or release_format != verification.metadata.get("git_object_format"):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"release commit does not match verification record '{verification_id}'",
                    plane="governance",
                )
            if (
                _grants_authority(artifact.artifact_type, artifact.status)
                and not _grants_authority(verification.artifact_type, verification.status)
            ):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"released record requires verified included record '{verification_id}'",
                    plane="governance",
                )
        missing_work = released_work - verification_work
        if missing_work:
            _add_error(
                errors,
                artifact,
                report_root,
                "E010",
                f"released work orders are not covered by included verification records: {', '.join(sorted(missing_work))}",
                plane="governance",
            )
        extra_work = verification_work - released_work
        if extra_work:
            _add_error(
                errors,
                artifact,
                report_root,
                "E010",
                f"included verification records cover work orders absent from the release: {', '.join(sorted(extra_work))}",
                plane="governance",
            )
        for contract_id in _relation_targets(artifact, "satisfies"):
            contract = catalog.get(contract_id)
            if contract is None or contract.artifact_type != "release_contract":
                continue
            if (
                _active_record_status(artifact.artifact_type, artifact.status)
                and not _grants_authority(contract.artifact_type, contract.status)
            ):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"active release record requires active release contract '{contract_id}'",
                    plane="governance",
                )
            ungated = released_work - _relation_targets(contract, "gates")
            if ungated:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"release contract '{contract_id}' does not gate work orders: {', '.join(sorted(ungated))}",
                    plane="governance",
                )

    for version, records in sorted(release_versions.items()):
        if len(records) < 2:
            continue
        record_ids = ", ".join(sorted(record.artifact_id for record in records))
        for record in records:
            _add_error(
                errors,
                record,
                report_root,
                "E010",
                f"duplicate release record version '{version}' among {record_ids}",
                plane="governance",
            )
    return errors


def _supersession_cycle_nodes(artifacts: list[Artifact]) -> set[str]:
    graph = {
        artifact.artifact_id: sorted(_relation_targets(artifact, "superseded_by"))
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


def _relation_targets(artifact: Artifact, relation_name: str) -> set[str]:
    value = artifact.relations.get(relation_name, [])
    if not isinstance(value, list):
        return set()
    return {item for item in value if isinstance(item, str)}


def _duplicate_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    strings = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in strings:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return sorted(duplicates)


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
            or work_order.status not in RELEASABLE_WORK_STATUSES
        ):
            continue
        for requirement_id in _relation_targets(work_order, "implements"):
            completed_work_by_requirement.setdefault(requirement_id, set()).add(
                work_order.artifact_id
            )

    verified_work = {
        work_order_id
        for record in artifacts
        if record.artifact_type == "verification_record"
        and _grants_authority(record.artifact_type, record.status)
        for work_order_id in _relation_targets(record, "verifies_work_order")
    }

    for contract in artifacts:
        if (
            contract.artifact_type != "operating_contract"
            or not _grants_authority(contract.artifact_type, contract.status)
        ):
            continue
        for requirement_id in sorted(_relation_targets(contract, "assures")):
            requirement = catalog.get(requirement_id)
            # Missing and wrong-type targets are owned by validate_relations.
            if requirement is None or requirement.artifact_type != "requirement":
                continue
            if not _grants_authority(requirement.artifact_type, requirement.status):
                _add_error(
                    errors,
                    contract,
                    report_root,
                    "E017",
                    f"active operating contract assures inactive requirement '{requirement_id}'",
                    plane="governance",
                )
                continue

            completed_work = completed_work_by_requirement.get(requirement_id, set())
            if not completed_work:
                _add_error(
                    errors,
                    contract,
                    report_root,
                    "E017",
                    f"active operating contract assures requirement '{requirement_id}' without completed implementing work",
                    plane="governance",
                )
                continue

            if require_verified_work and completed_work.isdisjoint(verified_work):
                _add_error(
                    errors,
                    contract,
                    report_root,
                    "E018",
                    f"active operating contract assures requirement '{requirement_id}' without a verified or released VREC covering completed implementing work",
                    plane="policy",
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
        duplicates = _duplicate_strings(raw)
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
        transitive_requirements.update(_relation_targets(specification, "specifies"))
        if (
            _grants_authority(artifact.artifact_type, artifact.status)
            and not _grants_authority(specification.artifact_type, specification.status)
        ):
            issues.append(
                f"active architecture conforms to inactive specification '{specification_id}'"
            )

    if _grants_authority(artifact.artifact_type, artifact.status):
        for requirement_id in addresses:
            requirement = catalog.get(requirement_id)
            if (
                requirement is not None
                and requirement.artifact_type == "requirement"
                and not _grants_authority(requirement.artifact_type, requirement.status)
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
    elif legacy_present and artifact.status in LEGACY_ARCHITECTURE_STATUSES:
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
            _add_error(
                errors,
                artifact,
                report_root,
                "E016",
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
                    _display_path(artifact.path, report_root),
                    "W015",
                    f"architecture uses deprecated constrains relation ({traceability['state']}); migrate through accountable governance",
                    "maintenance",
                )
            )
    return errors, warnings


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
        legacy = artifact.status in LEGACY_ARCHITECTURE_STATUSES
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
        duplicates = _duplicate_strings(triggers_value)
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
            _add_error(
                errors,
                artifact,
                report_root,
                "E019",
                issue,
                plane="governance",
            )
        if (
            artifact.artifact_type == "work_order"
            and assurance["state"] == "missing"
            and artifact.status in {"approved", "in_progress"}
        ):
            _add_error(
                errors,
                artifact,
                report_root,
                "E019",
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
            _add_error(errors, artifact, report_root, "E-ECP-001", "delegation is allowed only on work-order artifacts", plane="governance")
            continue
        if not isinstance(table, dict) or set(table) != {"class"}:
            _add_error(errors, artifact, report_root, "E-ECP-001", "delegation must contain exactly class", plane="governance")
            continue
        if table.get("class") != "execution":
            _add_error(errors, artifact, report_root, "E-ECP-001", f"delegation.class must be \"execution\", not {table.get('class')!r}", plane="governance")
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
            _add_error(
                errors,
                artifact,
                report_root,
                "E020",
                "execution_scope must contain only paths",
                plane="governance",
            )
            continue
        paths = table.get("paths")
        if not isinstance(paths, list) or not paths:
            _add_error(
                errors,
                artifact,
                report_root,
                "E020",
                "execution_scope.paths must be a non-empty array",
                plane="governance",
            )
            continue
        folded: dict[str, str] = {}
        for value in paths:
            issue = _execution_scope_path_issue(value)
            if issue is not None:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E020",
                    f"invalid execution scope path {value!r}: {issue}",
                    plane="governance",
                )
                continue
            key = value.casefold()
            if key in folded:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E020",
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
        if decision.artifact_type != "adr" or not _grants_authority(decision.artifact_type, decision.status):
            continue
        for architecture_id in _relation_targets(decision, "decides"):
            active_decisions_by_architecture.setdefault(architecture_id, set()).add(decision.artifact_id)

    for artifact in artifacts:
        assessment = decision_assessment_state(artifact)
        if artifact.artifact_type != "architecture":
            for issue in assessment["issues"]:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E014",
                    issue,
                    plane="governance",
                )
            continue

        state = assessment["state"]
        if state in {"missing", "invalid"}:
            for issue in assessment["issues"]:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E014",
                    issue,
                    plane="governance",
                )
            continue
        deciding = active_decisions_by_architecture.get(artifact.artifact_id, set())
        if state == "legacy_missing":
            warnings.append(
                Diagnostic(
                    _display_path(artifact.path, report_root),
                    "W014",
                    "completed legacy architecture has no decision_assessment; migrate during the compatibility window",
                    "maintenance",
                )
            )
            if not deciding:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E015",
                    "completed legacy architecture without decision_assessment requires an active deciding ADR",
                    plane="governance",
                )
            continue
        if (
            _grants_authority(artifact.artifact_type, artifact.status)
            and assessment["outcome"] == "adr_required"
            and not deciding
        ):
            _add_error(
                errors,
                artifact,
                report_root,
                "E015",
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
            _add_error(errors, artifact, report_root, "E-DCM-002", "decision kind must be question or deviation", plane="structure")
            continue
        for field in ("question", "raised_by", "recommendation"):
            if not isinstance(artifact.metadata.get(field), str) or not str(artifact.metadata.get(field)).strip():
                _add_error(errors, artifact, report_root, "E-DCM-002", f"decision field '{field}' must be a non-empty string", plane="structure")
        options = _decision_options(artifact)
        option_ids = [item["id"] for item in options]
        if len(options) < 2 or len(set(option_ids)) != len(option_ids):
            _add_error(errors, artifact, report_root, "E-DCM-002", "a decision declares at least two options with distinct ids and labels", plane="structure")
        recommendation = artifact.metadata.get("recommendation")
        if isinstance(recommendation, str) and option_ids and recommendation not in option_ids:
            _add_error(errors, artifact, report_root, "E-DCM-002", f"recommendation '{recommendation}' is not a declared option", plane="structure")
        reference = _decision_against(artifact)
        if kind == "deviation":
            if reference is None:
                _add_error(errors, artifact, report_root, "E-DCM-002", "a deviation names the departed rule as against = \"ARTIFACT-ID#rule\"", plane="structure")
            elif reference[0] not in catalog:
                _add_error(errors, artifact, report_root, "E-DCM-001", f"deviation departs from unknown artifact '{reference[0]}'", plane="governance")
            elif catalog[reference[0]].artifact_type != "specification":
                _add_error(errors, artifact, report_root, "E-DCM-001", f"a deviation departs from a specification, not a {catalog[reference[0]].artifact_type}", plane="governance")
            if not isinstance(artifact.metadata.get("observed"), str) or not str(artifact.metadata.get("observed")).strip():
                _add_error(errors, artifact, report_root, "E-DCM-002", "a deviation records the observed fact in 'observed'", plane="structure")
            if option_ids and (not set(option_ids).issubset(DEVIATION_OPTIONS) or "stop" not in option_ids):
                _add_error(errors, artifact, report_root, "E-DCM-002", "a deviation's options are drawn from amend, supersede, accept, stop and include stop", plane="structure")
        relations = artifact.metadata.get("relations", {})
        relations = relations if isinstance(relations, dict) else {}
        blocked = relations.get("blocks", []) if isinstance(relations.get("blocks"), list) else []
        concerned = relations.get("concerns", []) if isinstance(relations.get("concerns"), list) else []
        if not blocked:
            _add_error(errors, artifact, report_root, "E-DCM-001", "a decision blocks at least one artifact", plane="governance")
        for target in blocked:
            if isinstance(target, str) and target not in concerned:
                _add_error(errors, artifact, report_root, "E-DCM-001", f"blocked artifact '{target}' is not also in concerns", plane="governance")
        disposition = artifact.metadata.get("disposition")
        events = artifact.metadata.get("lifecycle_events")
        if artifact.status in DECISION_TERMINAL or artifact.status == "deferred":
            if not isinstance(disposition, dict):
                _add_error(errors, artifact, report_root, "E-DCM-003", f"a {artifact.status} decision carries a [disposition] table written by the transition", plane="governance")
            else:
                if not isinstance(events, list) or not events:
                    _add_error(errors, artifact, report_root, "E-DCM-003", "a disposition without a lifecycle event was written by hand", plane="governance")
                option = disposition.get("option")
                if artifact.status == "decided" and option not in option_ids:
                    _add_error(errors, artifact, report_root, "E-DCM-003", f"disposition option '{option}' is not a declared option", plane="governance")
                for field in ("decided_by", "decided_at", "reason", "label"):
                    if not isinstance(disposition.get(field), str) or not disposition[field].strip():
                        _add_error(errors, artifact, report_root, "E-DCM-003", f"disposition field '{field}' must be a non-empty string", plane="governance")
                if artifact.status == "deferred" and (not isinstance(disposition.get("scope"), list) or not disposition.get("revisit")):
                    _add_error(errors, artifact, report_root, "E-DCM-003", "a deferred decision records its scope and its revisit trigger", plane="governance")
                if artifact.status == "decided" and kind == "deviation" and option == "accept":
                    revisit = disposition.get("revisit")
                    if not isinstance(revisit, str) or not revisit.strip():
                        _add_error(errors, artifact, report_root, "E-DCM-003", "an accepted deviation records its revisit trigger", plane="governance")
                    elif reference is not None:
                        rule = f"{reference[0]}#{reference[1]}"
                        accepted_by_rule[rule].append(artifact.artifact_id)
                        if any(f"v{version}" in revisit or version in revisit for version in released_versions):
                            warnings.append(Diagnostic(
                                _display_path(catalog[reference[0]].path, report_root) if reference[0] in catalog else _display_path(artifact.path, report_root),
                                "W-DCM-001",
                                f"accepted deviation {artifact.artifact_id} against {rule} is past its revisit '{revisit}'; amend or supersede the rule, or accept again with a new trigger",
                                "maintenance",
                            ))
        elif isinstance(disposition, dict) and artifact.status == "open":
            _add_error(errors, artifact, report_root, "E-DCM-003", "an open decision carries no disposition", plane="governance")
    for rule, decisions in sorted(accepted_by_rule.items()):
        if len(decisions) >= 2:
            target = catalog.get(rule.split("#", 1)[0])
            warnings.append(Diagnostic(
                _display_path(target.path, report_root) if target is not None else rule,
                "W-DCM-002",
                f"{len(decisions)} accepted deviations stand against {rule} ({', '.join(decisions)}); the rule, not the implementations, is probably wrong",
                "maintenance",
            ))
    return errors, warnings


def validate_requirement_coverage(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    active_specs = [
        artifact
        for artifact in artifacts
        if artifact.artifact_type == "specification"
        and _grants_authority(artifact.artifact_type, artifact.status)
    ]
    active_verifications = [
        artifact
        for artifact in artifacts
        if artifact.artifact_type == "verification"
        and _grants_authority(artifact.artifact_type, artifact.status)
    ]

    specified = set().union(*(_relation_targets(item, "specifies") for item in active_specs)) if active_specs else set()
    verified = set().union(*(_relation_targets(item, "verifies") for item in active_verifications)) if active_verifications else set()

    for artifact in artifacts:
        if (
            artifact.artifact_type != "requirement"
            or not _grants_authority(artifact.artifact_type, artifact.status)
        ):
            continue
        if artifact.artifact_id not in specified:
            _add_error(
                errors,
                artifact,
                report_root,
                "E007",
                f"active requirement '{artifact.artifact_id}' has no active specification coverage",
                plane="governance",
            )
        if artifact.artifact_id not in verified:
            _add_error(
                errors,
                artifact,
                report_root,
                "E008",
                f"active requirement '{artifact.artifact_id}' has no active verification coverage",
                plane="governance",
            )

    return errors


def validate_canonical_layout(
    artifacts: list[Artifact],
    repository_root: Path,
    artifact_root: Path,
    errors: list[Diagnostic],
) -> list[Diagnostic]:
    canonical_root = repository_root / "docs" / "engineering"
    if artifact_root.resolve() != canonical_root.resolve():
        return []

    invalid_paths = {item.path for item in errors}
    id_counts = Counter(artifact.artifact_id for artifact in artifacts)
    catalog = {
        artifact.artifact_id: artifact
        for artifact in artifacts
        if artifact.artifact_id != "<unknown>" and id_counts[artifact.artifact_id] == 1
    }
    warnings: list[Diagnostic] = []

    for artifact in artifacts:
        actual = _display_path(artifact.path, repository_root)
        artifact_type = artifact.artifact_type
        artifact_id = artifact.artifact_id
        if (
            actual in invalid_paths
            or artifact_type not in ARTIFACT_DIRECTORIES
            or id_counts[artifact_id] != 1
            or ID_PATTERN.fullmatch(artifact_id) is None
            or not artifact_id.startswith(ARTIFACT_PREFIXES[artifact_type])
        ):
            continue

        if artifact_type in {"verification_record", "release_record"}:
            relation = "verifies_work_order" if artifact_type == "verification_record" else "releases_work"
            work_order_ids = sorted(_relation_targets(artifact, relation))
            work_order_paths: list[str] = []
            complete = bool(work_order_ids)
            for work_order_id in work_order_ids:
                work_order = catalog.get(work_order_id)
                if work_order is None or work_order.artifact_type != "work_order":
                    complete = False
                    break
                work_order_paths.append(_display_path(work_order.path, repository_root))
            if not complete:
                continue
            domain = common_artifact_domain(work_order_paths)
            expected = repository_record_relative_path(artifact_type, artifact_id, domain)
        else:
            domain = artifact_domain_from_relative_path(actual)
            if domain is None:
                continue
            expected = canonical_artifact_relative_path(domain, artifact_type, artifact_id)

        expected_text = expected.as_posix()
        if actual != expected_text:
            warnings.append(
                Diagnostic(
                    actual,
                    "W013",
                    f"artifact '{artifact_id}' is valid outside its canonical location; expected '{expected_text}'",
                    "maintenance",
                )
            )
    return sorted(set(warnings))


def validate_repository(repository_root: Path, artifact_root: Path | None = None) -> ValidationReport:
    repository_root = repository_root.resolve()
    selected_artifact_root = (artifact_root or repository_root / "docs" / "engineering").resolve()
    revision_policy = load_revision_policy(repository_root)

    artifacts, parse_errors = load_artifacts(selected_artifact_root, repository_root)
    errors = list(parse_errors)

    assessment_warnings: list[Diagnostic] = []
    traceability_warnings: list[Diagnostic] = []
    authoring_warnings: list[Diagnostic] = []
    decision_warnings: list[Diagnostic] = []
    if not selected_artifact_root.exists():
        errors.append(
            Diagnostic(
                _display_path(selected_artifact_root, repository_root),
                "E001",
                "artifact root does not exist",
                "structure",
            )
        )
    else:
        errors.extend(validate_common_metadata(artifacts, repository_root))
        errors.extend(validate_lifecycle_events(artifacts, repository_root))
        errors.extend(validate_type_specific_metadata(artifacts, repository_root))
        authoring_errors, authoring_warnings, authoring_advisories = validate_authoring(artifacts, repository_root)
        errors.extend(authoring_errors)
        errors.extend(validate_relations(artifacts, repository_root))
        traceability_errors, traceability_warnings = validate_architecture_traceability(
            artifacts,
            repository_root,
        )
        errors.extend(traceability_errors)
        assessment_errors, assessment_warnings = validate_decision_assessments(
            artifacts,
            repository_root,
        )
        errors.extend(assessment_errors)
        errors.extend(validate_work_order_assurance(artifacts, repository_root))
        errors.extend(validate_work_order_execution_scope(artifacts, repository_root))
        errors.extend(validate_work_order_delegation(artifacts, repository_root))
        decision_errors, decision_warnings = validate_decisions(artifacts, repository_root)
        errors.extend(decision_errors)
        errors.extend(
            validate_revision_consistency(
                artifacts,
                repository_root,
                require_verified_work=revision_policy["required_for_verified_work"],
            )
        )
        errors.extend(
            validate_operating_contract_readiness(
                artifacts,
                repository_root,
                require_verified_work=revision_policy["required_for_verified_work"],
            )
        )
        errors.extend(validate_requirement_coverage(artifacts, repository_root))

    warnings = [
        *assessment_warnings,
        *traceability_warnings,
        *authoring_warnings,
        *decision_warnings,
        *validate_canonical_layout(artifacts, repository_root, selected_artifact_root, errors),
    ]
    return ValidationReport(
        artifacts=artifacts,
        errors=sorted(set(errors)),
        warnings=sorted(set(warnings)),
        advisories=sorted(set(authoring_advisories)),
    )


def render_human(report: ValidationReport, *, show_advisories: bool = False) -> str:
    status = "PASS" if report.valid else "FAIL"
    plane_summary = " | ".join(
        f"{plane} E{sum(item.plane == plane for item in report.errors)}/W{sum(item.plane == plane for item in report.warnings)}"
        for plane in VALIDATION_PLANES
    )
    lines = [
        f"Engineering artifact validation: {status}",
        f"Artifacts: {len(report.artifacts)} | Errors: {len(report.errors)} | Warnings: {len(report.warnings)} | Advisories: {len(report.advisories)}",
        f"Planes: {plane_summary}",
    ]
    if report.errors:
        lines.append("")
        lines.append("Errors:")
        for diagnostic in sorted(report.errors):
            lines.append(
                f"- [{diagnostic.code}] [{diagnostic.plane}] {diagnostic.path}: {diagnostic.message}"
            )
    if report.warnings:
        lines.append("")
        lines.append("Warnings:")
        for diagnostic in sorted(report.warnings):
            lines.append(
                f"- [{diagnostic.code}] [{diagnostic.plane}] {diagnostic.path}: {diagnostic.message}"
            )
    if show_advisories and report.advisories:
        lines.append("")
        lines.append("Advisories:")
        for diagnostic in sorted(report.advisories):
            lines.append(
                f"- [{diagnostic.code}] [{diagnostic.plane}] {diagnostic.path}: {diagnostic.message}"
            )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate engineering artifact identity, relations, and coverage.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root (default: current directory).")
    parser.add_argument(
        "--artifact-root",
        type=Path,
        default=None,
        help="Artifact directory. Relative paths are resolved below --root; default: docs/engineering.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit a machine-readable JSON report.")
    parser.add_argument(
        "--advisories", action="store_true", dest="show_advisories",
        help="List the authoring advisories (W-AUT-*) after the warnings; the JSON report always carries them.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    repository_root = args.root.resolve()
    artifact_root = args.artifact_root
    if artifact_root is not None and not artifact_root.is_absolute():
        artifact_root = repository_root / artifact_root

    report = validate_repository(repository_root, artifact_root)
    if args.as_json:
        print(json.dumps(report.to_dict(repository_root), indent=2, sort_keys=True))
    else:
        print(render_human(report, show_advisories=args.show_advisories))
    return 0 if report.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
