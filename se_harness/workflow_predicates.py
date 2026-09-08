"""The predicate seam (SPEC-ECP-024 ECP-ENG-019): the checkpoint context and the predicates that read the repository rather than the context alone.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from se_harness import front_matter
from se_harness.codes import CodedError, E_CIP_001, E_DCM_004, WEX200, W_ECP_002
from se_harness.installer import HarnessError
from se_harness.integrity import canonical_text
from se_harness.workflow_contract import Checkpoint
from se_harness.workflow_change_set import ChangeSet
from se_harness.workflow_evidence_packet import parse_evidence_header


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
    evidence_root = context.root / "docs" / "engineering"
    candidates = [
        path for path in evidence_root.rglob("*")
        if path.is_file()
        and "evidence" in path.parts
        and any(part.startswith(context.artifact.artifact_id) for part in path.parts[path.parts.index("evidence") + 1 :])
    ]
    binding = f"formal_snapshot_sha256: {context.formal_snapshot_sha256}"
    # The handoff checkpoint is the one that retains evidence; a transition to
    # implemented accepts the handoff-bound document for the same snapshot, so
    # the transition can never pass on weaker evidence than check evaluated.
    checkpoint = "handoff" if context.checkpoint == "transition" else context.checkpoint
    legacy: str | None = None
    for path in sorted(candidates):
        try:
            data = path.read_bytes()
        except OSError:
            continue
        relative = path.relative_to(context.root).as_posix()
        # ECP-EVD-005: the machine header is read through the TOML parser, never by substring.
        try:
            header, _ = parse_evidence_header(data)
        except HarnessError:
            header = None
        if header is not None:
            if (
                header["artifact"] == context.artifact.artifact_id
                and header["checkpoint"] == checkpoint
                and header["formal_snapshot_sha256"] == context.formal_snapshot_sha256
            ):
                return "pass", f"Fresh retained evidence is bound at {relative}."
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeError:
            continue
        if (
            legacy is None
            and f"artifact: {context.artifact.artifact_id}" in text
            and f"checkpoint: {checkpoint}" in text
            and binding in text
        ):
            legacy = relative
    if legacy is not None:
        # Compatibility for one release: substring-bound packets still pass, named by W-ECP-002.
        return "pass", (
            f"Fresh retained evidence is bound at {legacy}. {W_ECP_002}: the packet carries no machine header; "
            f"migrate it with harnessctl evidence . --artifact {context.artifact.artifact_id} --checkpoint {checkpoint}."
        )
    return "not_assessable", (
        f"No readable evidence for {context.artifact.artifact_id}, checkpoint {checkpoint}, "
        f"and formal snapshot {context.formal_snapshot_sha256} is available."
    )


def pull_request_body_findings(root: Path, body_path: Path) -> list[str]:
    """Report W-ADS-001 for a pull-request body whose trailer carries a carriage return."""

    from se_harness.github_ci import MAX_EVENT_BYTES, carriage_return_trailer_offsets

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
    return [
        (
            f"the Harness-Work-Order line ends with a carriage return at byte offset {offset}; "
            "write the body with LF line endings (newline=\"\\n\" in Python, or core.autocrlf=false) before pushing"
        )
        for offset in carriage_return_trailer_offsets(body)
    ]


_PLACEHOLDER = re.compile(r"<[A-Za-z][^>\n]{2,80}>")

_FENCE = re.compile(r"```.*?```", re.DOTALL)

_INLINE_CODE = re.compile(r"`[^`\n]*`")

_DECISION_LINE = re.compile(r"^-?\s*`?DEC-(?:[A-Z0-9]+-)*\d{3}`?(?:\s*\((?:open|deferred|decided|withdrawn)\))?\.?$")


def authoring_ready(artifact: Any) -> tuple[str, str]:
    """AUT-GTE-001: no leftover template placeholder, and Open decisions closed."""

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
    return "pass", f"{artifact.artifact_id} carries no placeholder and no open decision."


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
    """CIP-RLU: a release contract that names a candidate commit declares the census the history yields.

    A contract without `candidate_commit` is the retained allow-list form and passes. A contract
    with one is re-measured with `se_harness.release_unit`; every `E-CIP-001` finding fails it.
    An unavailable history (no git, no tag) is `not_assessable`, never a pass.
    """

    metadata = artifact.metadata
    if artifact.artifact_type != "release_contract":
        return "not_assessable", f"{artifact.artifact_id} is not a release contract."
    candidate = metadata.get("candidate_commit")
    if not isinstance(candidate, str) or not candidate:
        return "pass", f"{artifact.artifact_id} declares no candidate_commit; the allow-list form is not re-measured."
    previous_tag = metadata.get("previous_release_tag")
    if not isinstance(previous_tag, str) or not previous_tag:
        return "fail", f"{E_CIP_001}: {artifact.artifact_id} names candidate_commit but no previous_release_tag."
    section = metadata.get("release_unit", {})
    exemptions = section.get("untraced_exemptions", []) if isinstance(section, dict) else []
    if not isinstance(exemptions, list) or not all(isinstance(item, str) for item in exemptions):
        return "fail", f"{E_CIP_001}: {artifact.artifact_id} release_unit.untraced_exemptions must be an array of full commit ids."
    from se_harness.release_unit import PACKAGED_SURFACE_PREFIXES, compare_with_contract, derive_release_unit

    def lookup(work_order: str) -> tuple[str | None, bool | None]:
        entry = catalog.get(work_order)
        if entry is None:
            return None, None
        status = entry.metadata.get("status")
        scope = entry.metadata.get("execution_scope", {})
        paths = scope.get("paths", []) if isinstance(scope, dict) else []
        packaged = any(isinstance(item, str) and item.startswith(PACKAGED_SURFACE_PREFIXES) for item in paths)
        return (status if isinstance(status, str) else None), packaged

    try:
        unit = derive_release_unit(root, from_ref=previous_tag, to_ref=candidate, exempt=exemptions, lookup=lookup)
    except HarnessError as exc:
        return "not_assessable", f"{artifact.artifact_id}: the release unit cannot be derived here: {exc}"
    findings = compare_with_contract(unit, metadata)
    if findings:
        return "fail", f"{artifact.artifact_id}: " + " ".join(findings)
    return "pass", f"{artifact.artifact_id} gates equal the census derived over {previous_tag}..{unit.to_commit[:12]} ({len(unit.gates)} work orders)."
