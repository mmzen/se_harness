#!/usr/bin/env python3
"""Plan or apply one contract-bound predecessor-compatible RLS preparation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from repository_tools.predecessor_preparation import (
    PredecessorPreparationError,
    apply_predecessor_release,
    plan_predecessor_release,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--release-record", dest="record_id", required=True)
    parser.add_argument("--release-contract", required=True)
    parser.add_argument("--verification-record", action="append", required=True)
    parser.add_argument("--work-order", action="append", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--authorized-by", required=True)
    parser.add_argument("--tag")
    parser.add_argument("--evaluator-python", type=Path, required=True)
    parser.add_argument("--evaluator-entry-point", type=Path, required=True)
    parser.add_argument("--evaluator-wheel", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    operation = apply_predecessor_release if args.apply else plan_predecessor_release
    try:
        result = operation(
            args.repository,
            record_id=args.record_id,
            release_contract_id=args.release_contract,
            verification_record_ids=args.verification_record,
            work_order_ids=args.work_order,
            version=args.version,
            authorized_by=args.authorized_by,
            tag=args.tag,
            evaluator_python=args.evaluator_python,
            evaluator_entry_point=args.evaluator_entry_point,
            evaluator_wheel=args.evaluator_wheel,
        )
    except (OSError, ValueError, PredecessorPreparationError) as exc:
        if args.json:
            print(json.dumps({"applied": False, "error": str(exc), "passed": False}, sort_keys=True))
        else:
            print(f"predecessor release preparation: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({**result.to_dict(), "passed": True}, sort_keys=True))
    else:
        action = "applied" if result.applied else "planned"
        print(
            f"predecessor release preparation: {action}: {result.release_record_path} | "
            f"view-evidence={result.preparation_view_evidence_path} | "
            f"sha256={result.preparation_view_evidence_sha256}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
