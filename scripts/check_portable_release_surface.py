#!/usr/bin/env python3
"""Prove that a candidate wheel or installed CLI excludes repository release policy."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import zipfile
from pathlib import Path


FORBIDDEN_CONTENT = (
    b"--distribution-manifest",
    b"python-wheel-sdist",
    b"SHA256SUMS",
)
FORBIDDEN_MEMBERS = frozenset(
    {
        "se_harness/governor_reconciliation.py",
        "se_harness/self_hosting.py",
        "se_harness/self_hosting_policy.py",
    }
)
FORBIDDEN_MEMBER_PREFIXES = ("share/se-harness/self-hosting/",)
FORBIDDEN_CLI = (b"reconcile-governor", b"--governor-wheel-sha256", b"--role governor")
FORBIDDEN_ACTIVE_CONTENT = (
    b"publish_dashboard.py governor",
    b"--role governor",
    b"--governor-wheel-sha256",
    b"def read_governor",
    b"class GovernorDescriptor",
    b'prefix="governor_"',
    b"id: governor",
    b"steps.governor",
    b"GOVERNOR_",
    b"governor-env",
)
FORBIDDEN_ACTIVE_PATHS = frozenset(
    {
        ".github/workflows/self-hosting-governor.yml",
        ".self-hosting/governor.toml",
        "se_harness/governor_reconciliation.py",
        "se_harness/self_hosting.py",
        "se_harness/self_hosting_policy.py",
    }
)
ACTIVE_ROOTS = (
    ".github/workflows",
    ".github/scripts",
    "scripts",
    "se_harness",
    "templates/repository/standard",
)
ACTIVE_SCAN_ALLOWLIST = frozenset({"scripts/check_portable_release_surface.py"})
CURRENT_OPERATOR_ROOTS = ("README.md", "docs/notes")
RETIRED_OPERATOR_TERM = re.compile(rb"\bgovernor\b", re.IGNORECASE)
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
                if (
                    name == "se_harness/release_distribution.py"
                    or name in FORBIDDEN_MEMBERS
                    or name.startswith(("repository_tools/", *FORBIDDEN_MEMBER_PREFIXES))
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
                elif any(term in content for term in FORBIDDEN_ACTIVE_CONTENT):
                    hits.append(name)
    except (KeyError, OSError, RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        raise SurfaceError(f"cannot inspect wheel: {path}") from exc
    if hits:
        raise SurfaceError("repository release policy leaked into wheel: " + ", ".join(hits))


def inspect_harnessctl(path: Path) -> None:
    if not path.is_file() or path.is_symlink():
        raise SurfaceError("harnessctl must be an ordinary file")
    try:
        commands = (
            [str(path), "--help"],
            [str(path), "prepare-release", "--help"],
            [str(path), "identity", "--help"],
        )
        completed = [
            subprocess.run(command, check=False, capture_output=True, timeout=30)
            for command in commands
        ]
    except (OSError, subprocess.SubprocessError) as exc:
        raise SurfaceError("installed harnessctl help could not be inspected") from exc
    if any(item.returncode != 0 for item in completed):
        raise SurfaceError("installed harnessctl help inspection failed")
    output = b"\n".join(item.stdout + item.stderr for item in completed)
    if FORBIDDEN_CONTENT[0] in output:
        raise SurfaceError("repository distribution option leaked into installed harnessctl")
    if any(term in output for term in FORBIDDEN_CLI):
        raise SurfaceError("retired specialized lifecycle leaked into installed harnessctl")


def inspect_repository(path: Path) -> None:
    root = path.expanduser().resolve()
    if not root.is_dir():
        raise SurfaceError("repository must be an existing directory")
    hits: list[str] = []
    for relative in sorted(FORBIDDEN_ACTIVE_PATHS):
        if (root / relative).exists():
            hits.append(relative)
    for active_root in ACTIVE_ROOTS:
        directory = root / active_root
        if not directory.is_dir():
            continue
        for candidate in sorted(directory.rglob("*"), key=lambda item: item.as_posix()):
            if not candidate.is_file() or candidate.is_symlink():
                continue
            relative = candidate.relative_to(root).as_posix()
            if relative in ACTIVE_SCAN_ALLOWLIST or "__pycache__" in candidate.parts:
                continue
            try:
                content = candidate.read_bytes()
            except OSError as exc:
                raise SurfaceError(f"cannot inspect active repository surface: {relative}") from exc
            if len(content) > MAX_MEMBER_SIZE:
                raise SurfaceError(f"active repository surface is too large to inspect: {relative}")
            if any(term in content for term in FORBIDDEN_ACTIVE_CONTENT):
                hits.append(relative)
    for operator_root in CURRENT_OPERATOR_ROOTS:
        selected = root / operator_root
        candidates = [selected] if selected.is_file() else sorted(selected.rglob("*.md")) if selected.is_dir() else []
        for candidate in candidates:
            if not candidate.is_file() or candidate.is_symlink():
                continue
            relative = candidate.relative_to(root).as_posix()
            try:
                content = candidate.read_bytes()
            except OSError as exc:
                raise SurfaceError(f"cannot inspect current operator surface: {relative}") from exc
            if len(content) > MAX_MEMBER_SIZE:
                raise SurfaceError(f"current operator surface is too large to inspect: {relative}")
            if RETIRED_OPERATOR_TERM.search(content):
                hits.append(relative)
    if hits:
        raise SurfaceError("retired specialized lifecycle is active in: " + ", ".join(sorted(set(hits))))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path)
    parser.add_argument("--harnessctl", type=Path)
    parser.add_argument("--repository", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.wheel is None and args.harnessctl is None and args.repository is None:
        print("portable release surface: at least one input is required", file=sys.stderr)
        return 2
    try:
        if args.wheel is not None:
            inspect_wheel(args.wheel)
        if args.harnessctl is not None:
            inspect_harnessctl(args.harnessctl)
        if args.repository is not None:
            inspect_repository(args.repository)
    except SurfaceError as exc:
        print(f"portable release surface: FAIL: {exc}", file=sys.stderr)
        return 1
    print("portable release surface: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
