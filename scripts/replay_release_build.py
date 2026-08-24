#!/usr/bin/env python3
"""Replay one recipe-bound release record without changing its accepted hashes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from repository_tools.release_build import BuildRecipeError, canonical_json_bytes, replay_build
from repository_tools.release_distribution import (
    DISTRIBUTION_SCHEMA_V2,
    ReleaseDistributionError,
    read_release_record,
    release_record_paths,
    validate_distribution_block,
    validate_record_distribution,
)


def _selected_record(repository: Path, artifact_id: str) -> tuple[Path, dict[str, object]]:
    matches: list[tuple[Path, dict[str, object]]] = []
    for path in release_record_paths(repository):
        try:
            metadata, _text, _lines, _closing = read_release_record(path)
        except ReleaseDistributionError:
            continue
        if metadata.get("type") == "release_record" and metadata.get("id") == artifact_id:
            matches.append((path, metadata))
    if len(matches) != 1:
        raise ReleaseDistributionError(
            f"expected exactly one release record {artifact_id}; found {len(matches)}"
        )
    return matches[0]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--release-record", required=True)
    parser.add_argument("--require-status", choices=("ready", "released"), required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    return parser


def main() -> int:
    arguments = build_parser().parse_args()
    try:
        repository = arguments.repository.resolve(strict=True)
        record_path, metadata = _selected_record(repository, arguments.release_record)
        if metadata.get("status") != arguments.require_status:
            raise ReleaseDistributionError(
                f"{arguments.release_record} must be {arguments.require_status}"
            )
        validate_record_distribution(repository, record_path, required=True)
        version = metadata.get("version")
        commit = metadata.get("commit")
        if not isinstance(version, str) or not isinstance(commit, str):
            raise ReleaseDistributionError("release record version or candidate is invalid")
        distribution = validate_distribution_block(metadata.get("distribution"), version)
        if distribution.schema != DISTRIBUTION_SCHEMA_V2:
            raise ReleaseDistributionError(
                "recipe replay requires distribution schema 2; schema 1 is legacy-only"
            )
        result = replay_build(
            repository,
            commit,
            version,
            arguments.output_directory,
            recipe_path=distribution.build_recipe or "",
            recipe_sha256=distribution.build_recipe_sha256,
            expected_wheel_sha256=distribution.wheel_sha256,
            expected_sdist_sha256=distribution.sdist_sha256,
        )
        result["release_record"] = arguments.release_record
        arguments.result.parent.mkdir(parents=True, exist_ok=True)
        temporary = arguments.result.with_name(f".{arguments.result.name}.tmp")
        temporary.write_bytes(canonical_json_bytes(result))
        temporary.replace(arguments.result)
        print(f"release build replay: PASS ({arguments.release_record})")
        return 0
    except (BuildRecipeError, ReleaseDistributionError, OSError, ValueError) as exc:
        try:
            arguments.result.parent.mkdir(parents=True, exist_ok=True)
            arguments.result.write_bytes(
                canonical_json_bytes(
                    {
                        "schema": "se-harness-release-build-replay/v1",
                        "authority": "technical replay evidence only; no lifecycle or external-action authority",
                        "state": "failed",
                        "release_record": arguments.release_record,
                        "failure_class": type(exc).__name__,
                    }
                )
            )
        except OSError:
            pass
        print(f"release build replay: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
