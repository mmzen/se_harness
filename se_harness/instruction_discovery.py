"""Map evaluator-selected identifiers to released reading locations.

This catalogue owns no state, transition, gate or next-action selection.
Its versioned result is additive to the existing schema-2 workflow result.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Mapping


SCHEMA = "se-harness-instruction-discovery-v1"
CATALOG_PATH = Path(__file__).with_suffix(".json")


class DiscoveryError(ValueError):
    """The released instruction mapping is missing, incompatible or incomplete."""


def _location(value: Any) -> None:
    if not isinstance(value, dict) or not {"file", "heading"} <= value.keys():
        raise DiscoveryError("an instruction location requires a file and heading")
    file, heading = value["file"], value["heading"]
    if (not isinstance(file, str) or not file.endswith(".md")
            or "\\" in file or ":" in file or file.startswith("/")
            or any(part in {"", ".", ".."} for part in file.split("/"))
            or PurePosixPath(file).as_posix() != file):
        raise DiscoveryError("instruction file must be a normalized repository-relative Markdown path")
    if not isinstance(heading, str) or re.fullmatch(r"[a-z0-9_-]+", heading) is None:
        raise DiscoveryError("instruction heading must be an explicit Markdown anchor")


def _prerequisites(values: Any) -> None:
    if not isinstance(values, list):
        raise DiscoveryError("instruction prerequisites must be an array")
    for value in values:
        _location(value)
        if not isinstance(value.get("when"), str) or not value["when"].strip():
            raise DiscoveryError("each prerequisite must name its reading condition")


def load_catalog() -> dict[str, Any]:
    try:
        value = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        raise DiscoveryError("released instruction catalogue is unavailable") from exc
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        raise DiscoveryError("unsupported instruction discovery schema")
    _location(value.get("entry"))
    _prerequisites(value.get("shared_prerequisites"))
    if value.get("evaluator_only_inputs") != ["docs/engineering/WORKFLOW.json", "docs/engineering/QUALITY_GATES.json"]:
        raise DiscoveryError("instruction catalogue must identify the evaluator-only contracts")
    procedures = value.get("procedures")
    if not isinstance(procedures, dict) or not procedures:
        raise DiscoveryError("instruction catalogue has no procedure mapping")
    for pid, procedure in procedures.items():
        if not isinstance(pid, str) or not pid.startswith("PROC-") or not isinstance(procedure, dict):
            raise DiscoveryError("invalid procedure reading mapping")
        _location(procedure.get("location"))
        _prerequisites(procedure.get("prerequisites"))
        steps = procedure.get("steps")
        if not isinstance(steps, dict) or not steps:
            raise DiscoveryError(f"instruction catalogue has no steps for {pid}")
        for sid, step in steps.items():
            if not isinstance(sid, str) or not sid.startswith("STEP-") or not isinstance(step, dict):
                raise DiscoveryError("invalid typed-step reading mapping")
            _location(step.get("location"))
            _prerequisites(step.get("prerequisites"))
    return value


def validate_coverage(procedures: Mapping[str, Mapping[str, Any]]) -> None:
    mapped = load_catalog()["procedures"]
    if set(mapped) != set(procedures):
        raise DiscoveryError("procedure catalogue and instruction discovery version disagree")
    for pid, procedure in procedures.items():
        if set(mapped[pid]["steps"]) != {step["id"] for step in procedure["steps"]}:
            raise DiscoveryError(f"typed steps and instruction discovery version disagree for {pid}")


def locations() -> list[dict[str, Any]]:
    """All declared instruction references; not an unconditional reading list."""
    catalog = load_catalog()
    result = [catalog["entry"], *catalog["shared_prerequisites"]]
    for procedure in catalog["procedures"].values():
        result.extend([procedure["location"], *procedure["prerequisites"]])
        for step in procedure["steps"].values():
            result.extend([step["location"], *step["prerequisites"]])
    return result


def validate_collection(contents: Mapping[str, bytes]) -> None:
    """Check a planned or installed collection without running repository code."""
    for location in locations():
        file, heading = location["file"], location["heading"]
        raw = contents.get(file)
        if raw is None:
            raise DiscoveryError(f"required instruction file is missing: {file}")
        try:
            text = raw.decode("utf-8")
        except UnicodeError as exc:
            raise DiscoveryError(f"required instruction file is not UTF-8: {file}") from exc
        anchors = set()
        for title in re.findall(r"^#{1,6} (.+)$", text, re.MULTILINE):
            anchor = re.sub(r"[^\w\- ]", "", title.strip().lower()).replace(" ", "-")
            anchors.add(anchor)
        if heading not in anchors:
            raise DiscoveryError(f"required instruction heading is missing: {file}#{heading}")


def validate_delivery_evidence(path: Path | None, target: Path, entry: bytes, prior_lock: bytes) -> dict:
    """Check the binding of reviewed native traces before retiring old entries.

    A receipt is retained evidence, not independent proof of how a host ran.
    The upgrade reviewer must assess the named traces and configured host.
    """
    if path is None:
        raise DiscoveryError("legacy entry retirement requires --instruction-delivery-evidence; no files were written")
    from se_harness import __version__
    from se_harness.integrity import canonical_sha256, unique_object_hook
    path = path.expanduser().absolute()
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 1024 * 1024:
        raise DiscoveryError("instruction-delivery evidence must be a bounded regular JSON file")
    raw = path.read_bytes()
    try:
        value = json.loads(raw, object_pairs_hook=unique_object_hook(DiscoveryError))
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise DiscoveryError("invalid instruction-delivery evidence JSON") from exc
    expected = {"schema": "se-harness-native-instruction-delivery-v1",
                "repository": str(target.resolve()), "target_version": __version__,
                "prior_lock_sha256": canonical_sha256(prior_lock),
                "entry_sha256": canonical_sha256(entry)}
    if not isinstance(value, dict) or any(value.get(key) != wanted for key, wanted in expected.items()):
        raise DiscoveryError("instruction-delivery evidence does not bind this repository, prior lock and planned entry")
    if (value.get("host") not in {"codex", "claude"}
            or not isinstance(value.get("host_version"), str) or not value["host_version"].strip()):
        raise DiscoveryError("instruction-delivery evidence must name the observed host and version")
    events = value.get("events")
    if not isinstance(events, dict) or set(events) != {"startup", "compact"}:
        raise DiscoveryError("instruction-delivery evidence requires native startup and post-compaction events")
    for event, observed in events.items():
        if (not isinstance(observed, dict) or observed.get("origin") != "native-host"
                or observed.get("delivered_root_sha256") != expected["entry_sha256"]):
            raise DiscoveryError(f"{event} does not report native delivery of the planned root")
        trace_name, trace_hash = observed.get("trace"), observed.get("trace_sha256")
        if (not isinstance(trace_name, str) or not trace_name or "\\" in trace_name
                or ":" in trace_name or trace_name.startswith("/")
                or any(part in {"", ".", ".."} for part in trace_name.split("/"))):
            raise DiscoveryError(f"{event} trace must be relative to its evidence file")
        trace = path.parent / trace_name
        if (trace.resolve() != trace.absolute() or not trace.is_file()
                or trace.stat().st_size == 0 or trace.stat().st_size > 16 * 1024 * 1024):
            raise DiscoveryError(f"{event} native trace is missing, linked or oversized")
        if hashlib.sha256(trace.read_bytes()).hexdigest() != trace_hash:
            raise DiscoveryError(f"{event} native trace does not match its retained digest")
    return {**expected, "host": value["host"], "host_version": value["host_version"],
            "evidence_sha256": hashlib.sha256(raw).hexdigest()}


def describe(procedure: Mapping[str, Any], formal_artifact_ids: list[str]) -> dict[str, Any]:
    """Describe already selected identifiers without recomputing their meaning."""
    catalog = load_catalog()
    pid, sid = procedure.get("id"), procedure.get("current_step")
    mapped = catalog["procedures"].get(pid)
    if mapped is None or sid not in mapped["steps"]:
        raise DiscoveryError(f"no released reading location for {pid}/{sid}")
    for step in procedure.get("steps", []):
        if step.get("id") not in mapped["steps"]:
            raise DiscoveryError(f"no released reading location for {pid}/{step.get('id')}")
    return {
        "schema": SCHEMA,
        "status": "available",
        "agent_instructions": {
            "entry": copy.deepcopy(catalog["entry"]),
            "shared_prerequisites": copy.deepcopy(catalog["shared_prerequisites"]),
            "procedure": {"id": pid, **copy.deepcopy(mapped)},
            "current_step": {"id": sid, **copy.deepcopy(mapped["steps"][sid])},
        },
        "formal_artifact_ids": sorted(set(formal_artifact_ids)),
        "evaluator_only_inputs": list(catalog["evaluator_only_inputs"]),
    }
