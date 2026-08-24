#!/usr/bin/env python3
"""Create deterministic SE Harness release-bundle evidence for repository binding."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from repository_tools.release_distribution import (
    ReleaseDistributionError as ManifestError,
    create_manifest,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--commit", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--sdist", type=Path, required=True)
    parser.add_argument(
        "--build-recipe",
        type=PurePosixPath,
        help="candidate-relative canonical recipe; omit only for historical schema-1 replay",
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        manifest = create_manifest(
            args.repository,
            args.commit,
            args.version,
            args.wheel,
            args.sdist,
            build_recipe=args.build_recipe,
        )
        payload = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.output.with_name(f".{args.output.name}.tmp")
        temporary.write_bytes(payload)
        temporary.replace(args.output)
        print(f"release bundle manifest: {args.output}")
        return 0
    except (ManifestError, OSError) as exc:
        print(f"release bundle manifest: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
