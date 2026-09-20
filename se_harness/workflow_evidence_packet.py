"""Explicit check capture, legacy attachments and retained handoff results."""

from __future__ import annotations

import json
import base64
import hashlib
import re
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from se_harness._process import ProcessError, run, run_git
from se_harness.codes import CodedError, WEX_ECP_010, WEX_ECP_011
from se_harness.integrity import atomic_create_bytes, atomic_write_bytes, pretty_json_bytes, canonical_text_bytes
from se_harness.installer import HarnessError, safe_destination


OBSERVATION_SCHEMA = "se-harness-check-observation-v1"
OBSERVATION_OUTCOMES = ("success", "failure", "not_run", "unavailable", "not_applicable")


def required_checks(artifact: Any, catalog: Mapping[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    """Read required outcomes from VER metadata, never infer them from an attachment."""
    result = {}
    for identifier in artifact.relations.get("verification", []):
        verification = catalog.get(identifier)
        checks = verification.metadata.get("checks") if verification else None
        if not isinstance(checks, list) or not checks:
            raise CodedError(WEX_ECP_010, f"{identifier} has no declared checks; attachment availability is not an assessment")
        for check in checks:
            if not isinstance(check, dict) or not isinstance(check.get("id"), str) or not check["id"].strip():
                raise CodedError(WEX_ECP_010, f"{identifier} has an invalid check declaration")
            key = (identifier, check["id"])
            if key in result or check.get("method") not in {"test", "inspection", "analysis", "demonstration"}:
                raise CodedError(WEX_ECP_010, f"{identifier} has a duplicate check or unsupported method")
            command = check.get("command")
            if check["method"] == "test" and (
                not isinstance(command, list) or not command
                or not all(isinstance(arg, str) and arg for arg in command)
            ):
                raise CodedError(WEX_ECP_010, f"{identifier}#{check['id']} requires exact command arguments")
            if check["method"] != "test" and command is not None:
                raise CodedError(WEX_ECP_010, f"{identifier}#{check['id']} is a manual check, not a command")
            result[key] = check
    if not result:
        raise CodedError(WEX_ECP_010, "No verification checks are declared for this work order")
    return result


def observation_inputs(root: Path, artifact: Any, report: Any) -> str:
    """Reuse the selected snapshot and bind the installed policy inputs as well."""
    from se_harness.workflow_change_set import formal_snapshot_digest
    digest = hashlib.sha256(formal_snapshot_digest(root, report.artifacts, [artifact.artifact_id]).encode())
    for relative in (".engineering-harness.toml", ".engineering-harness.lock", "ENGINEERING_HARNESS.md",
                     "docs/engineering/WORKFLOW.json", "docs/engineering/QUALITY_GATES.json"):
        path = safe_destination(root, Path(relative))
        digest.update(relative.encode() + b"\0" + canonical_text_bytes(path.read_bytes()))
    return digest.hexdigest()


def capture_check_observation(root: Path, artifact: Any, report: Any, *, verification: str,
                              check_id: str, command: list[str] | None = None,
                              outcome: str | None = None, assessor: str | None = None,
                              reason: str | None = None, output_ref: str | None = None) -> tuple[str, dict[str, Any]]:
    """Explicitly retain one observation; existing observations are never rebound."""
    from se_harness import __version__
    from se_harness.gate_source import authorize_delegated_right
    from se_harness.workflow_change_set import normalize_path, execution_scope, path_is_admitted
    catalog = {item.artifact_id: item for item in report.artifacts}
    if artifact.status != "in_progress":
        raise CodedError(WEX_ECP_010, "Check capture requires an in-progress work order")
    authorize_delegated_right(root, work_order_metadata=artifact.metadata,
                             work_order_path=artifact.path, right="DR-WO-COMPLETE")
    checks = required_checks(artifact, catalog)
    selected = checks.get((verification, check_id))
    if selected is None:
        raise CodedError(WEX_ECP_010, "The selected check is not declared by this work order's verification contract")
    directory = evidence_packet_path(root, artifact, "handoff").parent
    relative_directory = directory.relative_to(root).as_posix() + "/"
    if not path_is_admitted(relative_directory + "observation.json", execution_scope(artifact)):
        raise CodedError(WEX_ECP_010, f"Observation output directory is outside approved scope: {relative_directory}")
    before = observation_inputs(root, artifact, report)
    try:
        identity = run_git(root, "rev-parse", "HEAD")
        candidate = identity.stdout.decode().strip() if identity.returncode == 0 else None
    except ProcessError:
        candidate = None
    record = {"schema": OBSERVATION_SCHEMA, "artifact": artifact.artifact_id,
              "verification": verification, "check": check_id, "method": selected["method"],
              "observed_at": datetime.now(timezone.utc).isoformat(), "candidate_commit": candidate,
              "input_sha256": before, "origin": "local-command" if command else "local-assessment",
              "checker": {"version": __version__, "python": sys.executable,
                          "module": str(Path(__file__).resolve()),
                          "module_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
              "command": command, "exit_code": None, "outcome": outcome,
              "assessor": assessor, "reason": reason, "output_ref": output_ref}
    if command is not None:
        if selected["method"] != "test" or command != selected["command"] or outcome is not None:
            raise CodedError(WEX_ECP_010, "Use the exact declared test command; its outcome is observed, not supplied")
        try:
            completed = run(command, cwd=root, timeout=3600)
            record.update(exit_code=completed.returncode,
                          outcome="success" if completed.returncode == 0 else "failure",
                          stdout=base64.b64encode(completed.stdout).decode(),
                          stderr=base64.b64encode(completed.stderr).decode())
        except ProcessError as exc:
            record.update(outcome="unavailable", reason=str(exc))
    else:
        if outcome not in OBSERVATION_OUTCOMES or not assessor or not reason:
            raise CodedError(WEX_ECP_010, "A manual observation requires outcome, assessor and reason")
        if selected["method"] == "test" and outcome in {"success", "failure"}:
            raise CodedError(WEX_ECP_010, "Test success or failure must come from the declared command run")
        if outcome == "not_applicable" and reason != selected.get("not_applicable_reason"):
            raise CodedError(WEX_ECP_010, "Not applicable requires the reason declared in the verification contract")
        if outcome in {"success", "failure"} and not output_ref:
            raise CodedError(WEX_ECP_010, "Manual assessment requires a retained output reference")
    if output_ref:
        relative = normalize_path(output_ref)
        output = safe_destination(root, Path(relative))
        if not output.is_file() or not output.read_bytes().strip():
            raise CodedError(WEX_ECP_010, "The assessment output reference is unavailable or empty")
        record.update(output_ref=relative, output_sha256=hashlib.sha256(output.read_bytes()).hexdigest())
    # Reparse governing files after a command, so edited contract bytes cannot reuse
    # the pre-run catalog. The observation remains useful failure evidence.
    from se_harness.repository_graph import validated_repository
    try:
        _, latest_report = validated_repository(root)
        latest = {item.artifact_id: item for item in latest_report.artifacts}.get(artifact.artifact_id)
        unchanged = latest is not None and observation_inputs(root, latest, latest_report) == before
    except (HarnessError, OSError, ValueError):
        unchanged = False
    if not unchanged:
        record.update(outcome="unavailable", reason="Relevant inputs changed while the observation was captured")
    content = pretty_json_bytes(record, ensure_ascii=True)
    filename = "observation-" + hashlib.sha256(content).hexdigest() + ".json"
    path = safe_destination(root, directory.relative_to(root) / filename)
    atomic_create_bytes(path, content,
        exists=lambda: CodedError(WEX_ECP_010, "Observation already exists; it was not overwritten"),
        failed=lambda detail: CodedError(WEX_ECP_010, f"Cannot retain observation: {detail}"))
    return path.relative_to(root).as_posix(), record


EVIDENCE_HEADER_KEYS = ("artifact", "checkpoint", "formal_snapshot_sha256", "rebound_at")

_HEADER_OPEN = b"```toml\n"

_HEADER_CLOSE = b"\n```\n"

RFC3339_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def parse_evidence_header(data: bytes) -> tuple[dict[str, str] | None, bytes]:
    """Split a packet into its machine header and retained body (ECP-EVD-002, -004).

    Returns `(None, data)` when no fenced TOML block starts at byte offset 0.
    A block that starts there but is not valid TOML with the four required
    header keys raises `WEX-ECP-010`.
    """

    if not data.startswith(_HEADER_OPEN):
        return None, data
    end = data.find(_HEADER_CLOSE, len(_HEADER_OPEN))
    if end < 0:
        raise CodedError(WEX_ECP_010, "the evidence packet header fence is not closed")
    raw = data[len(_HEADER_OPEN):end]
    try:
        parsed = tomllib.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise CodedError(WEX_ECP_010, f"the evidence packet header is not valid TOML: {exc}") from exc
    if not set(EVIDENCE_HEADER_KEYS) <= set(parsed) or not all(isinstance(value, str) for value in parsed.values()):
        raise CodedError(WEX_ECP_010, "the evidence packet header must carry "
            + ", ".join(EVIDENCE_HEADER_KEYS)
        )
    return parsed, data[end + len(_HEADER_CLOSE):]


def render_evidence_header(fields: Mapping[str, str]) -> bytes:
    lines = [f"{key if re.fullmatch(r'[A-Za-z0-9_-]+', key) else json.dumps(key)} = {json.dumps(value, ensure_ascii=False)}" for key, value in fields.items()]
    return _HEADER_OPEN + "\n".join(lines).encode("utf-8") + _HEADER_CLOSE


def evidence_packet_path(root: Path, artifact: Any, checkpoint: str) -> Path:
    """`DOMAIN/evidence/WO-ID/WO-ID-CHECKPOINT.md` (ECP-EVD-001)."""

    from se_harness.artifact_layout import artifact_domain_from_relative_path

    # ECP-HST-001 (issue #254): the resolver's text guard rejects a backslash, and
    # a WindowsPath renders with them; hand it the POSIX form of the evaluator's own path.
    domain = artifact_domain_from_relative_path(artifact.path.relative_to(root).as_posix())
    if domain is None:
        raise CodedError(WEX_ECP_010, f"{artifact.artifact_id} is not under a domain directory")
    return root / "docs" / "engineering" / domain / "evidence" / artifact.artifact_id / f"{artifact.artifact_id}-{checkpoint}.md"


def line_ending_conversion(root: Path, relative: str) -> str | None:
    """The attribute rule that would convert this path's line endings, if any (ECP-EVD-006)."""

    if not (root / ".git").exists():
        return None
    try:
        completed = run_git(root, "check-attr", "-z", "text", "eol", "--", relative, timeout=60, error=ProcessError)
    except ProcessError:
        return None
    if completed.returncode != 0:
        return None
    fields = completed.stdout.split(b"\0")
    values: dict[str, str] = {}
    for index in range(0, len(fields) - 2, 3):
        values[fields[index + 1].decode("utf-8", "replace")] = fields[index + 2].decode("utf-8", "replace")
    text, eol = values.get("text", "unspecified"), values.get("eol", "unspecified")
    if text in {"set", "auto"} and eol != "lf":
        return f"text={text} eol={eol}"
    return None


def rebind_handoff_packet(root: Path, artifact: Any, snapshot: str, now: str) -> str | None:
    """Rebind an existing handoff packet header to the current snapshot (ECP-SBH-001 to -003).

    Returns the packet's repository-relative path when the header was rewritten,
    None when there is nothing to move: no packet, no machine header (the legacy
    grace still reads it), or a header already bound to `snapshot`. A missing
    packet is never created; `harnessctl evidence` stays the authoring command.
    """

    path = evidence_packet_path(root, artifact, "handoff")
    if not path.exists():
        return None
    relative = path.relative_to(root).as_posix()
    if path.is_symlink() or not path.is_file():
        raise CodedError(WEX_ECP_010, f"{relative} is not an ordinary file")
    existing, body = parse_evidence_header(path.read_bytes())
    if existing is None:
        return None
    if existing["artifact"] != artifact.artifact_id or existing["checkpoint"] != "handoff":
        raise CodedError(WEX_ECP_010, f"{relative} is the packet of {existing['artifact']} at {existing['checkpoint']}, "
            f"not {artifact.artifact_id} at handoff"
        )
    if existing["formal_snapshot_sha256"] == snapshot:
        return None
    conversion = line_ending_conversion(root, relative)
    if conversion is not None:
        raise CodedError(WEX_ECP_011, f"a .gitattributes rule would convert line endings of {relative} ({conversion})")
    header = {
        **existing,
        "artifact": artifact.artifact_id,
        "checkpoint": "handoff",
        "formal_snapshot_sha256": snapshot,
        "rebound_at": now,
    }
    try:
        atomic_write_bytes(path, render_evidence_header(header) + body)  # ECP-PRM-008
    except OSError as exc:
        raise CodedError(WEX_ECP_010, f"cannot write the evidence packet: {exc}") from exc
    return relative


def retain_handoff_result(root: Path, artifact: Any, result: Mapping[str, Any]) -> str:
    """Retain a completed Git-derived handoff result beside the packet (ECP-PRB-002, amended)."""

    path = evidence_packet_path(root, artifact, "handoff").with_name("handoff.json")
    try:
        atomic_write_bytes(path, pretty_json_bytes(result, ensure_ascii=True))  # ECP-PRM-006, ECP-PRM-008
    except OSError as exc:
        raise CodedError(WEX_ECP_010, f"cannot retain the handoff result: {exc}") from exc
    return path.relative_to(root).as_posix()
