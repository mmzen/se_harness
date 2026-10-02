"""Read-only coverage of a proposed file list (SPEC-KIS-004)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping

from se_harness.codes import CodedError, WEX200
from se_harness.installer import HarnessError, safe_destination
from se_harness.workflow_evidence_packet import evidence_packet_path
from se_harness.workflow_change_set import (
    declared_change_set,
    execution_scope,
    normalize_path,
    own_record_paths,
    path_is_admitted,
    validate_changed_targets,
)


def assess_planned_paths(
    root: Path, primary: Any, catalog: Mapping[str, Any], paths: Iterable[str],
) -> dict[str, Any]:
    """Reuse admission without treating a plan as observed change evidence."""
    proposed = declared_change_set(paths, complete=False)
    if not proposed.paths:
        raise CodedError(WEX200, "planned paths must contain at least one file")
    validate_changed_targets(root, proposed)
    for path in proposed.paths:
        if safe_destination(root, Path(path)).is_dir():
            raise CodedError(WEX200, f"planned path must name a file: {path!r}")
    result: dict[str, Any] = {
        "planned_paths": sorted(proposed.paths),
        "coverage": "invalid",
        "explicit_matches": [],
        "automatic_matches": [],
        "uncovered_paths": [],
        "invalid_declarations": [],
        "impact_analysis": "not_assessed",
    }
    try:
        declared = execution_scope(primary)
        for entry in declared:
            safe_destination(root, Path(entry.rstrip("/")))
        own_path = normalize_path(primary.path.relative_to(root).as_posix())
        packet_directory = evidence_packet_path(root, primary, "handoff").parent.relative_to(root).as_posix() + "/"
        safe_destination(root, Path(packet_directory.rstrip("/")))
        records = own_record_paths(root, catalog, primary.artifact_id)
        automatic = declared_change_set((own_path, *records), complete=False)
        validate_changed_targets(root, automatic)
    except (HarnessError, ValueError) as exc:
        result["invalid_declarations"].append(str(exc))
        return result
    for path in result["planned_paths"]:
        entry = next((item for item in declared if path_is_admitted(path, (item,))), None)
        if entry is not None:
            result["explicit_matches"].append({"path": path, "scope_entry": entry})
        elif path in automatic.paths:
            result["automatic_matches"].append({
                "path": path,
                "rule": "own-work-order" if path == own_path else "linked-record-or-evaluator-evidence",
                "work_order": primary.artifact_id,
            })
        elif path_is_admitted(path, (packet_directory,)):
            result["automatic_matches"].append({
                "path": path,
                "rule": "work-order-evidence-directory",
                "work_order": primary.artifact_id,
                "scope_entry": packet_directory,
            })
        else:
            result["uncovered_paths"].append(path)
    result["coverage"] = "uncovered" if result["uncovered_paths"] else "covered"
    return result
