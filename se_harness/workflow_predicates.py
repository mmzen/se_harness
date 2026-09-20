"""The predicate seam (SPEC-ECP-024 ECP-ENG-019): the checkpoint context and the predicates that read the repository rather than the context alone.
"""

from __future__ import annotations

import re
import json
import hashlib
import base64
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from se_harness import front_matter
from se_harness.codes import CodedError, E_DCM_004, WEX200
from se_harness.installer import HarnessError, safe_destination
from se_harness.integrity import canonical_text
from se_harness.workflow_contract import Checkpoint
from se_harness.workflow_change_set import ChangeSet, normalize_path
from se_harness.workflow_evidence_packet import (
    OBSERVATION_SCHEMA, evidence_packet_path, observation_inputs, required_checks,
)


@dataclass
class CheckpointContext:
    root: Path
    artifact: Any
    catalog: Mapping[str, Any]
    scoped_errors: list[dict[str, Any]]
    repository_errors: list[dict[str, Any]]
    unrelated_count: int
    declared_scope: tuple[str, ...]
    admitted_scope: tuple[str, ...]
    change_set: ChangeSet
    checkpoint: Checkpoint  # ECP-PRM-013
    formal_snapshot_sha256: str
    target: str | None = None
    #: ECP-ENG-010: the validation this checkpoint was built from, so no predicate validates again.
    report: Any = None


def review_evidence(context: CheckpointContext) -> tuple[str, str]:
    if context.artifact.artifact_type != "work_order":
        return "pass", "Work-order implementation evidence does not apply to this artifact type."
    # Attachments remain ordinary files. Availability does not establish an outcome.
    references = context.artifact.metadata.get("evidence_paths")
    if references is not None:
        if not isinstance(references, list) or not references:
            return "not_assessable", "evidence_paths must list at least one repository file."
        for reference in references:
            try:
                relative = normalize_path(reference)
                path = safe_destination(context.root, Path(relative))
                path.resolve(strict=True).relative_to(context.root.resolve())
                if not path.is_file() or not path.read_bytes().strip():
                    return "not_assessable", f"Evidence {relative} is missing or empty."
            except (HarnessError, OSError, ValueError) as exc:
                return "not_assessable", f"Cannot read evidence {reference!r}: {exc}"
    try:
        checks = required_checks(context.artifact, context.catalog)
        current = observation_inputs(context.root, context.artifact, context.report)
        directory = evidence_packet_path(context.root, context.artifact, "handoff").parent
        records: dict[tuple[str, str], list[tuple[str, dict[str, Any]]]] = {}
        for path in sorted(directory.glob("observation-*.json")):
            safe = safe_destination(context.root, path.relative_to(context.root))
            raw = safe.read_bytes()
            if path.name != "observation-" + hashlib.sha256(raw).hexdigest() + ".json":
                return "fail", f"Retained observation changed: {path.relative_to(context.root).as_posix()}."
            item = json.loads(raw)
            if not isinstance(item, dict) or item.get("schema") != OBSERVATION_SCHEMA:
                return "not_assessable", "Unreadable check observation."
            if item.get("artifact") != context.artifact.artifact_id:
                return "fail", "Observation names a different work order."
            key = (item.get("verification"), item.get("check"))
            if key in checks:
                records.setdefault(key, []).append((path.relative_to(context.root).as_posix(), item))
        assessed = []
        for key, check in checks.items():
            label = "#".join(key)
            candidates = records.get(key, [])
            if not candidates:
                return "not_assessable", f"{label}: not_run; capture its required observation with harnessctl evidence."
            if any(not isinstance(item.get("observed_at"), str) for _, item in candidates):
                return "not_assessable", f"{label}: observation time is unavailable."
            candidates.sort(key=lambda pair: pair[1]["observed_at"])
            relative, item = candidates[-1]
            if len(candidates) > 1 and candidates[-2][1]["observed_at"] == item["observed_at"]:
                return "not_assessable", f"{label}: latest observation is ambiguous."
            if item.get("input_sha256") != current:
                return "not_assessable", f"{label}: stale observation at {relative}; relevant inputs changed."
            checker = item.get("checker")
            if (item.get("method") != check["method"] or not isinstance(checker, dict)
                    or not all(isinstance(checker.get(key), str) and checker[key].strip()
                               for key in ("version", "python", "module", "module_sha256"))):
                return "not_assessable", f"{label}: method or checker identity is unavailable."
            outcome = item.get("outcome")
            if outcome == "failure":
                return "fail", f"{label}: failure retained at {relative}."
            if outcome not in {"success", "not_applicable"}:
                return "not_assessable", f"{label}: {outcome or 'unavailable'} at {relative}."
            if outcome == "not_applicable":
                if (not check.get("not_applicable_reason") or item.get("reason") != check["not_applicable_reason"]
                        or item.get("origin") != "local-assessment" or not item.get("assessor")):
                    return "fail", f"{label}: not applicable is not supported by its contract."
            elif check["method"] == "test":
                if (item.get("command") != check["command"] or type(item.get("exit_code")) is not int
                        or item["exit_code"] != 0 or item.get("origin") != "local-command"):
                    return "fail", f"{label}: no successful run of the required command."
                # Successful captures retain both complete byte streams, including empty output.
                for stream in ("stdout", "stderr"):
                    base64.b64decode(item[stream], validate=True)
            elif (item.get("origin") != "local-assessment" or not item.get("assessor")
                  or not item.get("reason") or not item.get("output_ref")):
                return "not_assessable", f"{label}: responsible manual assessment is missing."
            if item.get("output_ref"):
                output = safe_destination(context.root, Path(normalize_path(item["output_ref"])))
                if not output.is_file() or hashlib.sha256(output.read_bytes()).hexdigest() != item.get("output_sha256"):
                    return "not_assessable", f"{label}: assessment output is unavailable or changed."
            assessed.append(f"{label}: {outcome} ({item.get('origin')}, {relative})")
        return "pass", "Assessed required checks: " + "; ".join(assessed) + ". Local observations do not establish independent assurance."
    except (HarnessError, OSError, ValueError, KeyError, TypeError) as exc:
        return "not_assessable", f"Cannot assess required evidence: {exc}"


def pull_request_body_findings(root: Path, body_path: Path) -> list[str]:
    """Check that a supplied pull-request body is readable and selects one work order."""

    from se_harness.github_ci import MAX_EVENT_BYTES, SelectionError, select_work_orders

    try:
        with body_path.open("rb") as handle:
            raw = handle.read(MAX_EVENT_BYTES + 1)
    except OSError as exc:
        raise CodedError(WEX200, f"cannot read pull-request body: {exc}") from exc
    if len(raw) > MAX_EVENT_BYTES:
        raise CodedError(WEX200, "pull-request body exceeds the size limit")
    try:
        body = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CodedError(WEX200, "pull-request body must be UTF-8") from exc
    try:
        select_work_orders(body)
    except SelectionError as exc:
        return [str(exc)]
    return []


_PLACEHOLDER = re.compile(r"<[A-Za-z][^>\n]{2,80}>")

_FENCE = re.compile(r"```.*?```", re.DOTALL)

_INLINE_CODE = re.compile(r"`[^`\n]*`")

_DECISION_LINE = re.compile(r"^-?\s*`?DEC-(?:[A-Z0-9]+-)*\d{3}`?(?:\s*\((?:open|deferred|decided|withdrawn)\))?\.?$")


def authoring_ready(artifact: Any, root: Path | None = None, catalog: Mapping[str, Any] | None = None) -> tuple[str, str]:
    """Refuse unfinished content or decisions; leave writing style to the author."""

    try:
        text = artifact.path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return "not_assessable", f"{artifact.artifact_id} cannot be read: {exc}"
    prose = _INLINE_CODE.sub("", _FENCE.sub("", canonical_text(text)))  # ECP-PRM-010
    # the template's five shape comments live in the front matter; markdown headings stay
    split = front_matter.partition(prose)  # ECP-PRM-005: line-anchored on the normalized text
    if split is not None:
        head, body = split
        head = "\n".join(line for line in head.split("\n") if not line.lstrip().startswith("#"))
        prose = head + "\n+++\n" + body
    match = _PLACEHOLDER.search(prose)
    if match is not None:
        return "fail", f"{artifact.artifact_id} still carries the template placeholder {match.group(0)}."
    # the section is read with its inline code intact: the ids are written as `DEC-...`
    lines = _FENCE.sub("", canonical_text(text)).split("\n")
    for index, line in enumerate(lines):
        if line.strip() == "## Open decisions":
            body_lines = []
            for item in lines[index + 1:]:
                if item.startswith("## "):
                    break
                if item.strip():
                    body_lines.append(item.strip())
            body = body_lines[0] if body_lines else ""
            # SPEC-DCM-001 rule 11: the section reads None, or lists decision ids.
            if body not in {"None", "None."} and not all(_DECISION_LINE.fullmatch(line) for line in body_lines):
                return "fail", (
                    f"{E_DCM_004}: {artifact.artifact_id} has an open decision written as prose: {body[:120]} "
                    f"(the Open decisions section reads exactly None, or lists DEC- identifiers)"
                )
            break
    if artifact.artifact_type == "requirement":
        statement = artifact.metadata.get("statement")
        if not isinstance(statement, str) or not statement.strip():
            return "fail", f"{artifact.artifact_id} needs a non-empty statement."
        sections = front_matter.body_sections(artifact.body)
        acceptance = [sections.get("Examples"), sections.get("Acceptance"), sections.get("Acceptance criteria"),
                      artifact.metadata.get("measure"), artifact.metadata.get("verification_notes")]
        linked = [item.body for item in (catalog or {}).values()
                  if item.artifact_type == "verification" and artifact.artifact_id in item.relations.get("verifies", [])]
        if not any(isinstance(item, str) and item.strip() for item in acceptance + linked):
            return "fail", f"{artifact.artifact_id} needs an acceptance condition: add an example, measure, verification notes or a linked verification contract."
    return "pass", f"{artifact.artifact_id} has no unfinished content or unresolved decision text."



def blocking_decisions(catalog: Mapping[str, Any], artifact: Any, target: str | None) -> list[Any]:
    """Decisions that block `artifact` now (SPEC-DCM-001 rule 5).

    An `open` decision naming the artifact in `blocks` always blocks. A
    `deferred` one blocks unless its scope admits the requested transition;
    without a requested transition it does not block.
    """

    from se_harness.decisions import deferral_scope, scope_admits

    hits: list[Any] = []
    for candidate in catalog.values():
        if getattr(candidate, "artifact_type", None) != "decision":
            continue
        relations = candidate.relations if isinstance(getattr(candidate, "relations", None), Mapping) else {}
        blocked = relations.get("blocks", [])
        if not isinstance(blocked, list) or artifact.artifact_id not in blocked:
            continue
        if candidate.status == "open":
            hits.append(candidate)
        elif candidate.status == "deferred" and target is not None:
            if not scope_admits(deferral_scope(candidate), artifact.artifact_id, artifact.status, target):
                hits.append(candidate)
    return sorted(hits, key=lambda item: item.artifact_id)


def decision_gate_clear(context: CheckpointContext) -> tuple[str, str]:
    """QGP-*-DECISION: no open or unscoped deferred decision blocks the selected artifact."""

    from se_harness.decisions import declared_options, deciding_roles

    hits = blocking_decisions(context.catalog, context.artifact, context.target)
    if not hits:
        return "pass", f"No open decision blocks {context.artifact.artifact_id}."
    first = hits[0]
    question = str(first.metadata.get("question") or "").strip()
    options = "; ".join(f"{item['id']}: {item['label']}" for item in declared_options(first)) or "none declared"
    roles = ", ".join(sorted(deciding_roles(first, context.catalog))) or "the owner of the blocked artifact"
    return "fail", (
        f"{first.artifact_id} is {first.status} and blocks {context.artifact.artifact_id}: {question} "
        f"Options: {options}. Decider: {roles}. "
        f"Next: harnessctl decide . --artifact {first.artifact_id} --option OPTION-ID --decision ROLE --reason TEXT"
    )


def release_unit_ready(artifact: Any, root: Path, catalog: Mapping[str, Any]) -> tuple[str, str]:
    """Compatibility evaluator: trailer history informs the owner, not release authority."""
    return "pass", "Commit-trailer census is advisory. Approve release scope and verify the final candidate explicitly."
