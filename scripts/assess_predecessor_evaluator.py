#!/usr/bin/env python3
"""Assess an exact candidate with the contract-bound predecessor evaluator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from repository_tools.predecessor_assessment import (
    PredecessorAssessmentError,
    assess_predecessor_evaluator,
)
from repository_tools.predecessor_preparation import PredecessorPreparationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--candidate-commit", required=True)
    parser.add_argument("--release-contract", required=True)
    parser.add_argument("--evaluator-python", type=Path, required=True)
    parser.add_argument("--evaluator-entry-point", type=Path, required=True)
    parser.add_argument("--evaluator-wheel", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = assess_predecessor_evaluator(
            args.repository,
            candidate_commit=args.candidate_commit,
            release_contract_id=args.release_contract,
            evaluator_python=args.evaluator_python,
            evaluator_entry_point=args.evaluator_entry_point,
            evaluator_wheel=args.evaluator_wheel,
            output=args.output,
            apply=args.apply,
        )
    except (OSError, ValueError, PredecessorAssessmentError, PredecessorPreparationError) as exc:
        if args.json:
            print(json.dumps({"applied": False, "error": str(exc), "passed": False}, sort_keys=True))
        else:
            print(f"predecessor evaluator assessment: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({**result.to_dict(), "passed": True}, sort_keys=True))
    else:
        action = "retained" if result.applied else "planned"
        print(
            f"predecessor evaluator assessment: {action}: "
            f"candidate={result.source_commit} | "
            f"evidence={result.assessment_evidence_path or '-'} | "
            f"sha256={result.assessment_evidence_sha256}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
