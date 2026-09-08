"""A per-session cache of freshly initialised standard repositories for test fixtures.

`WO-TST-002` (`REQ-TST-003`, `SPEC-TST-001` TST-FIX). `harnessctl init` writes
61 files with durable atomic writes and costs about 0.57 seconds; about three
hundred tests ran it in `setUp`. `standard_repository()` runs it once per
project name per test process and hands out `shutil.copytree` copies, which
are byte-identical to a direct `init` (asserted by `tests/test_fixture_support.py`)
and cost a few hundredths of a second. Fixtures that assert on `init` itself
keep calling `init` directly.
"""

from __future__ import annotations

import atexit
import contextlib
import io
import os
import shutil
import tempfile
from pathlib import Path

from tests.cli_support import invoke

_SESSION: tempfile.TemporaryDirectory | None = None
_CACHE: dict[str, Path] = {}
_INITIALISATIONS: list[str] = []


def _session_root() -> Path:
    global _SESSION
    if _SESSION is None or not Path(_SESSION.name).is_dir():
        _SESSION = tempfile.TemporaryDirectory(prefix="se-harness-fixture-cache-")
        atexit.register(_SESSION.cleanup)
        _CACHE.clear()
    return Path(_SESSION.name)


def _initialise(project_name: str) -> Path:
    """One real `init` per project name per process; re-run if the cache directory has gone."""

    cached = _CACHE.get(project_name)
    if cached is not None and cached.is_dir():
        return cached
    target = _session_root() / f"repository-{len(_INITIALISATIONS) + 1}"  # monotonic: a re-initialised name never collides
    code, output, errors = invoke("init", str(target), "--project-name", project_name)
    if code != 0:
        raise RuntimeError(f"fixture init failed for {project_name!r} with exit code {code}: {errors.strip() or output.strip()}")
    _CACHE[project_name] = target
    _INITIALISATIONS.append(project_name)
    return target


def standard_repository(destination: Path, project_name: str = "Fixture") -> Path:
    """Copy a freshly initialised standard repository into `destination` (created or empty)."""

    destination = Path(destination)
    if destination.exists() and any(destination.iterdir()):
        raise RuntimeError(f"fixture destination is not empty: {destination}")
    shutil.copytree(_initialise(project_name), destination, dirs_exist_ok=True)
    return destination


def initialisations() -> tuple[str, ...]:
    """The project names initialised so far in this process, in order (for the cache test)."""

    return tuple(_INITIALISATIONS)


def scale_sizes() -> tuple[int, ...]:
    """REQ-TST-002: the 1,000-artifact size runs only under SE_HARNESS_TEST_SCALE=full."""

    return (100, 500, 1000) if os.environ.get("SE_HARNESS_TEST_SCALE") == "full" else (100, 500)
