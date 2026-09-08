"""The evidence-packet seam (SPEC-ECP-024 ECP-ENG-019): the header, the packet path, the handoff rebind and the retained result; the writer stays with the evaluator.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any, Mapping

from se_harness._process import ProcessError, run_git
from se_harness.codes import CodedError, WEX_ECP_010, WEX_ECP_011
from se_harness.integrity import atomic_write_bytes, pretty_json_bytes


EVIDENCE_HEADER_KEYS = ("artifact", "checkpoint", "formal_snapshot_sha256", "rebound_at")

_HEADER_OPEN = b"```toml\n"

_HEADER_CLOSE = b"\n```\n"

RFC3339_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def parse_evidence_header(data: bytes) -> tuple[dict[str, str] | None, bytes]:
    """Split a packet into its machine header and retained body (ECP-EVD-002, -004).

    Returns `(None, data)` when no fenced TOML block starts at byte offset 0.
    A block that starts there but is not valid TOML with exactly the four
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
    if set(parsed) != set(EVIDENCE_HEADER_KEYS) or not all(isinstance(parsed[key], str) for key in EVIDENCE_HEADER_KEYS):
        raise CodedError(WEX_ECP_010, "the evidence packet header must carry exactly "
            + ", ".join(EVIDENCE_HEADER_KEYS)
        )
    return {key: parsed[key] for key in EVIDENCE_HEADER_KEYS}, data[end + len(_HEADER_CLOSE):]


def render_evidence_header(fields: Mapping[str, str]) -> bytes:
    lines = [f'{key} = "{fields[key]}"' for key in EVIDENCE_HEADER_KEYS]
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
