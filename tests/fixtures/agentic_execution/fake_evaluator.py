"""Verifier-owned public-command fake for harness-orient black-box tests."""

from __future__ import annotations

import json
import os
import sys


MODE = os.environ.get("AEX_FAKE_MODE", "healthy")
VERSION = os.environ.get("AEX_FAKE_VERSION", "0.6.0")


def emit(value: object) -> None:
    print(json.dumps(value, ensure_ascii=True, sort_keys=True))


def main() -> int:
    arguments = sys.argv[1:]
    if arguments == ["--version"]:
        print(VERSION)
        return 0
    if arguments == ["--help"]:
        commands = ["identity", "doctor", "validate", "inspect", "preflight"]
        if MODE != "no-check":
            commands.append("check")
        print("commands:")
        for command in commands:
            print(f"  {command}  fake public command")
        return 0
    if not arguments:
        return 2
    command = arguments[0]
    if command == "identity":
        if MODE == "identity-fail":
            print("identity mismatch", file=sys.stderr)
            return 1
        print("Runtime identity: PASS")
        return 0
    if command == "doctor":
        if MODE == "large-output":
            print("x" * (2 * 1024 * 1024))
            return 0
        if MODE == "doctor-fail":
            print("FAIL managed-integrity: secret=top-secret", file=sys.stderr)
            return 1
        print("PASS managed-integrity: installed content matches")
        return 0
    if command == "validate":
        if MODE == "malformed-validation":
            print("not-json")
            return 1
        valid = MODE != "invalid-graph"
        emit(
            {
                "artifact_count": 3,
                "error_count": 0 if valid else 1,
                "errors": [] if valid else [{"code": "E-FAKE", "message": "invalid fixture graph"}],
                "valid": valid,
                "warning_count": 0,
                "warnings": [],
            }
        )
        return 0 if valid else 1
    if command == "inspect":
        emit(
            {
                "queues": {
                    "active_work": [],
                    "assurance_pending": [],
                    "decision_required": [
                        {
                            "action": "decide-definition",
                            "id": "REQ-TST-001",
                            "owners": ["requirements-steward"],
                        }
                    ],
                    "definition_pending": [],
                },
                "repository": {"name": "fixture-repository"},
                "schema": "se-harness-inspection-v2",
                "summary": {"artifact_count": 3, "finding_count": 2, "relation_count": 2},
            }
        )
        return 0
    if command == "check":
        if "--help" in arguments:
            print("usage: check --artifact ARTIFACT [--checkpoint NAME] --json")
            return 0
        artifact = arguments[arguments.index("--artifact") + 1]
        emit(
            {
                "findings": {"repository_blockers": [], "scoped_blockers": [], "unrelated_count": 2},
                "operation": {"kind": "check", "outcome": "completed"},
                "restitution": {
                    "command_or_response": {
                        "argv": ["harnessctl", "check", ".", "--artifact", artifact, "--checkpoint", "handoff"],
                        "kind": "command",
                    },
                    "decision_required": None,
                    "next": {"action": "Run the bound command"},
                },
                "schema": "se-harness-workflow-result-v2",
                "scope": {
                    "declared_paths": ["src/"],
                    "dependencies": [],
                    "governing": ["REQ-TST-001"],
                },
                "state": {"before": [{"id": artifact, "status": "in_progress"}]},
            }
        )
        return 0
    if command == "preflight":
        ready = MODE != "preflight-blocked"
        emit({"phase": arguments[arguments.index("--phase") + 1], "ready": ready, "work_order": arguments[arguments.index("--work-order") + 1]})
        return 0 if ready else 1
    print(f"unsupported fake command: {command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
