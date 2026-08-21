#!/usr/bin/env python3
"""Plan or apply one contract-bound predecessor-evaluator evidence binding."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from repository_tools.release_bootstrap import (
    ReleaseBootstrapError,
    apply_bootstrap_binding,
    plan_bootstrap_binding,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--release-record", type=Path, required=True)
    parser.add_argument("--release-contract", type=Path, required=True)
    parser.add_argument("--evaluator-python", type=Path, required=True)
    parser.add_argument("--evaluator-entry-point", type=Path, required=True)
    parser.add_argument("--evaluator-wheel", type=Path, required=True)
    parser.add_argument("--apply", action="store_true", help="apply the exact planned binding")
    parser.add_argument("--json", action="store_true", help="emit canonical JSON output")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    operation = apply_bootstrap_binding if args.apply else plan_bootstrap_binding
    try:
        result = operation(
            args.repository,
            args.release_record,
            args.release_contract,
            args.evaluator_python,
            args.evaluator_entry_point,
            args.evaluator_wheel,
        )
    except (OSError, ReleaseBootstrapError, ValueError) as exc:
        if args.json:
            print(json.dumps({"applied": False, "error": str(exc), "passed": False}, sort_keys=True))
        else:
            print(f"release bootstrap binding: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({**result.to_dict(), "passed": True}, sort_keys=True))
    else:
        action = "applied" if args.apply and result.changed else "already exact" if args.apply else "planned"
        print(
            f"release bootstrap binding: {action}: {result.release_record_path} | "
            f"evidence={result.evaluator_evidence_path} | sha256={result.evaluator_evidence_sha256}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
