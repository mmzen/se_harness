#!/usr/bin/env python3
"""Validate repository-owned SE Harness distribution provenance."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from repository_tools.release_distribution import (
    ReleaseDistributionError,
    read_release_record,
    release_record_paths,
    validate_record_distribution,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--require-record", action="append", default=[])
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repository = args.root.resolve()
    required = set(args.require_record)
    found: set[str] = set()
    validated = 0
    errors: list[str] = []
    try:
        paths = list(release_record_paths(repository))
    except ReleaseDistributionError as exc:
        print(f"SE Harness release distribution validation: FAIL\n- {exc}", file=sys.stderr)
        return 1
    for path in paths:
        try:
            metadata, _text, _lines, _closing = read_release_record(path)
        except ReleaseDistributionError:
            continue
        if metadata.get("type") != "release_record":
            continue
        artifact_id = metadata.get("id")
        is_required = isinstance(artifact_id, str) and artifact_id in required
        if is_required:
            found.add(artifact_id)
        try:
            if validate_record_distribution(repository, path, required=is_required):
                validated += 1
        except ReleaseDistributionError as exc:
            errors.append(str(exc))
    missing = sorted(required - found)
    errors.extend(f"required release record is missing: {item}" for item in missing)
    if errors:
        print("SE Harness release distribution validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "SE Harness release distribution validation: PASS "
        f"({validated} distribution-bearing record{'s' if validated != 1 else ''})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
