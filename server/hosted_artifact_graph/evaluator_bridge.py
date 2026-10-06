"""Trusted adapter entry point, executed only by the isolated released Python.

All parsing, relation rules, allocation and work selection come from that release.
The service never imports candidate repository modules into this process.
"""
from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

from se_harness.engine.validation_core import load_artifacts
from se_harness.engine.validate_engineering_artifacts import validate_repository
from se_harness.evaluator_identity import installed_evaluator_identity
from se_harness.installer import plan_install, apply_changes


def main():
    action = sys.argv[1]
    if action == "identity":
        return installed_evaluator_identity().to_lock()
    root = Path(sys.argv[2])
    if action == "select":
        changes, lock = plan_install(root, project_name="hosted-artifact-poc", mode="upgrade")
        result = apply_changes(root, changes, lock, allow_updates=True)
        return {"selected": installed_evaluator_identity().to_lock()}
    if action == "catalog":
        artifacts, errors = load_artifacts(root / "docs/engineering", root)
        # A failed parse has no usable catalog. Preserve the released errors
        # without carrying every unrelated record into the client refusal.
        if errors:
            artifacts = []
        return {"errors": [asdict(e) for e in errors], "artifacts": [
            {"id": a.artifact_id, "type": a.artifact_type, "status": a.status,
             "path": a.path.relative_to(root).as_posix(), "metadata": a.metadata,
             "relations": a.relations} for a in artifacts]}
    if action == "validate":
        return validate_repository(root).to_dict(root)
    raise ValueError("Unsupported trusted adapter operation")


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, default=str, allow_nan=False))
