"""One Git launcher for tests (SPEC-TST-002 TST-HYG-005).

Every Git launch in the suite goes through `run_git`, `git` or
`init_repository`: UTF-8 output, a fixture identity given by environment so no
repository needs it configured, and commit signing turned off so a
signing-enabled workstation runs the suite unchanged.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

IDENTITY = {
    "GIT_AUTHOR_NAME": "Fixture",
    "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
    "GIT_COMMITTER_NAME": "Fixture",
    "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
}


def git_available() -> bool:
    return shutil.which("git") is not None


def run_git(
    root: Path | str,
    *arguments: str,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    """Run `git -C root ...` with the fixture identity and signing off; the one launch site of the suite."""
    return subprocess.run(
        ["git", "-C", str(root), "-c", "commit.gpgsign=false", *arguments],
        capture_output=True,
        check=check,
        env={**os.environ, **IDENTITY, **(env or {})},
    )


def git(
    root: Path | str,
    *arguments: str,
    check: bool = True,
    binary: bool = False,
    env: dict[str, str] | None = None,
) -> str | bytes:
    """Stripped UTF-8 stdout of `git -C root ...`, or the raw bytes when `binary`."""
    completed = run_git(root, *arguments, check=check, env=env)
    if binary:
        return completed.stdout
    return completed.stdout.decode("utf-8", errors="replace").strip()


def init_repository(root: Path | str, *, branch: str = "main") -> None:
    """Initialise an empty repository at `root` with a fixture identity and deterministic text handling."""
    git(root, "init", "-q", "-b", branch)
    git(root, "config", "user.email", IDENTITY["GIT_AUTHOR_EMAIL"])
    git(root, "config", "user.name", IDENTITY["GIT_AUTHOR_NAME"])
    git(root, "config", "core.autocrlf", "false")
    git(root, "config", "commit.gpgsign", "false")
