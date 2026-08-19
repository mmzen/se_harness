#!/usr/bin/env python3
"""Prove that a candidate wheel or installed CLI excludes repository release policy."""

from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path


FORBIDDEN_CONTENT = (
    b"--distribution-manifest",
    b"python-wheel-sdist",
    b"SHA256SUMS",
)
MAX_MEMBER_SIZE = 16 * 1024 * 1024
MAX_MEMBER_COUNT = 4096
MAX_TOTAL_SIZE = 128 * 1024 * 1024


class SurfaceError(RuntimeError):
    """A portable candidate exposes SE Harness repository release policy."""


def inspect_wheel(path: Path) -> None:
    if not path.is_file() or path.is_symlink():
        raise SurfaceError("wheel must be an ordinary file")
    try:
        with zipfile.ZipFile(path) as archive:
            hits: list[str] = []
            members = archive.infolist()
            if len(members) > MAX_MEMBER_COUNT:
                raise SurfaceError("wheel contains too many members")
            total_size = sum(member.file_size for member in members)
            if total_size > MAX_TOTAL_SIZE:
                raise SurfaceError("wheel expands beyond the inspection limit")
            for member in members:
                name = member.filename
                if name == "se_harness/release_distribution.py" or name.startswith(
                    "repository_tools/"
                ):
                    hits.append(name)
                    continue
                if member.is_dir():
                    continue
                if member.file_size > MAX_MEMBER_SIZE:
                    raise SurfaceError(f"wheel member is too large to inspect: {name}")
                content = archive.read(member)
                if any(term in content for term in FORBIDDEN_CONTENT):
                    hits.append(name)
    except (KeyError, OSError, RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        raise SurfaceError(f"cannot inspect wheel: {path}") from exc
    if hits:
        raise SurfaceError("repository release policy leaked into wheel: " + ", ".join(hits))


def inspect_harnessctl(path: Path) -> None:
    if not path.is_file() or path.is_symlink():
        raise SurfaceError("harnessctl must be an ordinary file")
    try:
        completed = subprocess.run(
            [str(path), "prepare-release", "--help"],
            check=False,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise SurfaceError("installed harnessctl help could not be inspected") from exc
    if completed.returncode != 0:
        raise SurfaceError("installed harnessctl prepare-release help failed")
    if FORBIDDEN_CONTENT[0] in completed.stdout + completed.stderr:
        raise SurfaceError("repository distribution option leaked into installed harnessctl")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path)
    parser.add_argument("--harnessctl", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.wheel is None and args.harnessctl is None:
        print("portable release surface: at least one input is required", file=sys.stderr)
        return 2
    try:
        if args.wheel is not None:
            inspect_wheel(args.wheel)
        if args.harnessctl is not None:
            inspect_harnessctl(args.harnessctl)
    except SurfaceError as exc:
        print(f"portable release surface: FAIL: {exc}", file=sys.stderr)
        return 1
    print("portable release surface: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
