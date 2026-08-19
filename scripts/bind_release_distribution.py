#!/usr/bin/env python3
"""Bind exact SE Harness distribution provenance to one ready release record."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from repository_tools.release_distribution import ReleaseDistributionError, bind_distribution


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--release-record", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        path, _distribution, changed = bind_distribution(
            args.repository, args.release_record, args.manifest
        )
    except (ReleaseDistributionError, OSError) as exc:
        print(f"release distribution binding: {exc}", file=sys.stderr)
        return 1
    state = "bound" if changed else "already exact"
    print(f"release distribution binding: {state}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
