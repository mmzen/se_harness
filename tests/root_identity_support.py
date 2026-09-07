"""Identity-aware location of the evaluator's scripts (WO-HUP-017, SPEC-HUP-017 HUP-ADP-016).

Until the 0.15.0 root the released evaluator installed eight hash-locked copies of its
scripts under `scripts/`; since the 0.16.0 root (`SPEC-DST-025`) it installs none and
runs them from inside the package. A test that read a root copy reads it only when the
lock names it, and otherwise the engine copy the candidate carries.
"""
import json
from pathlib import Path

from se_harness.installer import ENGINE_ROOT

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def lock() -> dict:
    return json.loads((REPOSITORY_ROOT / ".engineering-harness.lock").read_text(encoding="utf-8"))


def root_manages_scripts() -> bool:
    return any(
        path.startswith("scripts/") and entry.get("mode") == "managed"
        for path, entry in lock()["files"].items()
    )


def evaluator_scripts_dir() -> Path:
    """The directory holding the evaluator's scripts this root runs: the root copies or the engine."""
    return REPOSITORY_ROOT / "scripts" if root_manages_scripts() else ENGINE_ROOT


def root_copy(relative: str) -> Path | None:
    """The root copy of `relative` when the lock names it, else None."""
    return REPOSITORY_ROOT / relative if relative in lock()["files"] else None


def committed_copies(root_relative: str, engine_relative: str) -> tuple[str, ...]:
    """Every committed copy of one evaluator file: the engine copy, plus the root copy when the lock names it."""
    copies = [engine_relative]
    if root_copy(root_relative) is not None:
        copies.insert(0, root_relative)
    return tuple(copies)
