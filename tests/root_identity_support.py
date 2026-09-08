"""Identity-aware location of the evaluator's scripts (WO-HUP-017, SPEC-HUP-017 HUP-ADP-016).

Until the 0.15.0 root the released evaluator installed eight hash-locked copies of its
scripts under `scripts/`; since the 0.16.0 root (`SPEC-DST-025`) it installs none and
runs them from inside the package. A test that read a root copy reads it only when the
lock names it, and otherwise the engine copy the candidate carries.
"""
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

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


def load_module(path: Path, name: str) -> ModuleType:
    """Load one Python file as the module `name`, registered in `sys.modules` (SPEC-TST-002 TST-HYG-008).

    Registration keeps the module object unique per name, so exception classes
    and patched attributes are the same for every importer. A module already
    loaded from the same file is returned as is.
    """
    path = Path(path)
    existing = sys.modules.get(name)
    if existing is not None and getattr(existing, "__file__", None) == str(path):
        return existing
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path} as {name}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True  # a script loaded from a shipped tree leaves no __pycache__ behind
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    finally:
        sys.dont_write_bytecode = previous
    return module


# The engine's scripts import one another by bare name, in this order.
EVALUATOR_MODULES = (
    "artifact_layout_registry",
    "validate_engineering_artifacts",
    "generate_harness_dashboard",
    "inspect_engineering_artifacts",
)


def load_evaluator_module(name: str, *, alias: str | None = None, directory: Path | None = None) -> ModuleType:
    """The evaluator script `name` this root runs, loaded by path under its bare name.

    The scripts a module imports are loaded first under their bare names, so no
    test module puts a directory on `sys.path`. `alias` loads a second, distinct
    copy under another name; `directory` reads the scripts from another root.
    """
    scripts = Path(directory) if directory is not None else evaluator_scripts_dir()
    for dependency in EVALUATOR_MODULES:
        if dependency == name:
            break
        if dependency not in sys.modules and (scripts / f"{dependency}.py").is_file():
            load_module(scripts / f"{dependency}.py", dependency)
    return load_module(scripts / f"{name}.py", alias or name)
