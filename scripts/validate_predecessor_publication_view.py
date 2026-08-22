#!/usr/bin/env python3
"""Validate publication with current semantics and an exact predecessor view."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from repository_tools.predecessor_preparation import PredecessorPreparationError
from repository_tools.predecessor_publication import (
    PredecessorPublicationError,
    validate_predecessor_publication,
)
from repository_tools.release_bootstrap import ReleaseBootstrapError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--release-record", dest="release_record_id", required=True)
    parser.add_argument("--evaluator-python", type=Path, required=True)
    parser.add_argument("--evaluator-entry-point", type=Path, required=True)
    parser.add_argument("--evaluator-wheel", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = validate_predecessor_publication(
            args.repository,
            release_record_id=args.release_record_id,
            evaluator_python=args.evaluator_python,
            evaluator_entry_point=args.evaluator_entry_point,
            evaluator_wheel=args.evaluator_wheel,
            output=args.output,
        )
    except (
        OSError,
        ValueError,
        PredecessorPreparationError,
        PredecessorPublicationError,
        ReleaseBootstrapError,
    ) as exc:
        if args.json:
            print(json.dumps({"applied": False, "error": str(exc), "passed": False}, sort_keys=True))
        else:
            print(f"predecessor publication validation: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({**result.to_dict(), "passed": True}, sort_keys=True))
    else:
        print(
            "predecessor publication validation: passed: "
            f"release={result.release_record} | current={result.current_artifact_count} | "
            f"view={result.predecessor_artifact_count} | sha256={result.observation_sha256}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
