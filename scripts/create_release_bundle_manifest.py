#!/usr/bin/env python3
"""Create the deterministic distribution manifest consumed by prepare-release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


BUNDLE_SCHEMA = "se-harness-release-bundle/v1"
COMMIT_LENGTHS = {"sha1": 40, "sha256": 64}
VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,63}")


class ManifestError(RuntimeError):
    """Release bundle input does not identify one exact candidate distribution."""


def _git(repository: Path, *arguments: str, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", "replace").strip() or "Git command failed"
        raise ManifestError(detail)
    return completed.stdout if binary else completed.stdout.decode("utf-8", "strict").strip()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ManifestError(f"cannot read distribution: {path}") from exc
    return digest.hexdigest()


def create_manifest(
    repository: Path,
    commit: str,
    version: str,
    wheel: Path,
    sdist: Path,
) -> dict[str, object]:
    repository = repository.resolve()
    if VERSION_PATTERN.fullmatch(version) is None:
        raise ManifestError("version contains unsupported characters")
    object_format = str(_git(repository, "rev-parse", "--show-object-format"))
    if object_format not in COMMIT_LENGTHS:
        raise ManifestError("unsupported Git object format")
    candidate = str(_git(repository, "rev-parse", "--verify", f"{commit}^{{commit}}")).lower()
    if len(candidate) != COMMIT_LENGTHS[object_format] or re.fullmatch(r"[0-9a-f]+", candidate) is None:
        raise ManifestError("candidate did not resolve to a full Git object ID")
    if commit.lower() != candidate:
        raise ManifestError("candidate commit must be supplied as a full exact object ID")
    expected_wheel = f"se_harness-{version}-py3-none-any.whl"
    expected_sdist = f"se_harness-{version}.tar.gz"
    if wheel.name != expected_wheel or sdist.name != expected_sdist:
        raise ManifestError("distribution filenames do not match the release version")
    if not wheel.is_file() or wheel.is_symlink() or not sdist.is_file() or sdist.is_symlink():
        raise ManifestError("wheel and sdist must be ordinary files")
    wheel_hash = _sha256_file(wheel)
    sdist_hash = _sha256_file(sdist)
    checksums_content = (
        f"{wheel_hash}  {expected_wheel}\n"
        f"{sdist_hash}  {expected_sdist}\n"
    )
    epoch = str(_git(repository, "show", "-s", "--format=%ct", candidate))
    if not epoch.isdigit() or int(epoch) < 1:
        raise ManifestError("candidate commit timestamp is invalid")
    tree_manifest = _git(repository, "ls-tree", "-r", "-z", "--full-tree", candidate, binary=True)
    assert isinstance(tree_manifest, bytes)
    if not tree_manifest:
        raise ManifestError("candidate source manifest is empty")
    return {
        "schema": BUNDLE_SCHEMA,
        "version": version,
        "commit": candidate,
        "git_object_format": object_format,
        "source_date_epoch": int(epoch),
        "wheel": expected_wheel,
        "wheel_sha256": wheel_hash,
        "sdist": expected_sdist,
        "sdist_sha256": sdist_hash,
        "checksums": "SHA256SUMS",
        "checksums_sha256": hashlib.sha256(checksums_content.encode("utf-8")).hexdigest(),
        "checksums_content": checksums_content,
        "source_manifest_sha256": hashlib.sha256(tree_manifest).hexdigest(),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--commit", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--sdist", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        manifest = create_manifest(args.repository, args.commit, args.version, args.wheel, args.sdist)
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
