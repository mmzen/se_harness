"""Replace disposable repository skills with the installed plugin's skills.

Remove the old copies, then save the provider. If interrupted, run it again.
Plugin installation belongs to the host.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil
from typing import Any, Iterable

from se_harness.integrity import (
    IntegrityError, atomic_write_bytes, canonical_sha256, pretty_json_bytes,
)


class OwnershipError(IntegrityError):
    """The selected repository or replacement plugin cannot be used."""


CATALOG = frozenset(json.loads(
    Path(__file__).with_name("skill_ownership_contract.json").read_text(encoding="utf-8")
)["catalog"])
SKILLS = ("harness-orient", "harness-operator-brief")
SKILL_DIRECTORIES = tuple(f"{host}/skills/{skill}" for host in (".agents", ".claude") for skill in SKILLS)
DISCOVERY_PATHS = CATALOG | {".claude/skills/harness-operator-brief/SKILL.md"}
LOCK_NAME = ".engineering-harness.lock"


def catalog_paths() -> frozenset[str]:
    return CATALOG


def validate_ownership_binding(value: Any) -> dict:
    """The portable record selects a provider; it does not pin plugin contents."""
    if not isinstance(value, dict) or value.get("provider") != "plugin":
        raise OwnershipError("skill ownership must select the plugin provider")
    return value


def effective_templates(templates: Iterable[Any], lock: dict) -> list[Any]:
    items = list(templates)
    if lock.get("schema") == 4:
        validate_ownership_binding(lock.get("skill_ownership"))
        return [item for item in items if item.target.as_posix() not in CATALOG]
    return items


def _destination(root: Path, relative: str) -> Path:
    # Fixed harness paths only. A linked parent must not redirect deletion or
    # restoration into another skill or repository.
    path = root / relative
    if path.resolve() != path or not path.resolve().is_relative_to(root):
        raise OwnershipError(f"remove the linked skill path before switching provider: {path}")
    return path


def _check_plugin(plugin_root: Path | None) -> None:
    if plugin_root is None:
        raise OwnershipError("plugin ownership requires --plugin-root")
    root = Path(plugin_root).expanduser().resolve()
    manifests = [root / host / "plugin.json" for host in (".codex-plugin", ".claude-plugin")]
    manifest = next((path for path in manifests if path.is_file()), None)
    if manifest is None:
        raise OwnershipError(f"plugin manifest missing: {root}")
    try:
        plugin = json.loads(manifest.read_text(encoding="utf-8-sig"))
    except (ValueError, UnicodeError) as exc:
        raise OwnershipError(f"invalid plugin manifest: {manifest}") from exc
    if not isinstance(plugin, dict) or plugin.get("name") != "verity-plane":
        raise OwnershipError("select the verity-plane plugin")
    for relative in sorted(CATALOG):
        if not relative.startswith(".agents/"):
            continue
        path = root / relative.removeprefix(".agents/")
        if not path.is_file() or path.stat().st_size == 0:
            raise OwnershipError(f"replacement skill missing or empty: {path}")


def _prepare(target: Path, provider: str, plugin_root: Path | None) -> tuple[Path, dict, dict[str, bytes], dict]:
    from se_harness.installer import ensure_target, load_lock, template_files

    if provider not in {"plugin", "repository"}:
        raise OwnershipError("provider must be plugin or repository")
    root = ensure_target(target, must_exist=True)
    if not _destination(root, LOCK_NAME).is_file():
        raise OwnershipError("initialize the repository before switching its skill provider")
    lock = load_lock(root)
    after = {**lock, "files": dict(lock["files"])}
    writes = {}
    changes = []
    if provider == "plugin":
        _check_plugin(plugin_root)
        plugin = Path(plugin_root).expanduser().resolve()
        for relative in SKILL_DIRECTORIES:
            path = _destination(root, relative)
            if plugin == path or plugin.is_relative_to(path):
                raise OwnershipError("replacement plugin is inside a skill directory being removed")
            if path.exists():
                changes.append({"path": relative, "action": "remove"})
        after.update(schema=4, skill_ownership={"provider": "plugin"})
        for path in CATALOG:
            after["files"].pop(path, None)
    else:
        if plugin_root is not None:
            raise OwnershipError("repository ownership does not use --plugin-root")
        after["schema"] = 3
        after.pop("skill_ownership", None)
        for item in template_files():
            path = item.target.as_posix()
            if path not in CATALOG:
                continue
            destination = _destination(root, path)
            raw = item.source.read_bytes()
            after["files"][path] = {"mode": "managed", "sha256": canonical_sha256(raw)}
            if not destination.is_file() or destination.read_bytes() != raw:
                writes[path] = raw
                changes.append({"path": path, "action": "replace"})
    if after != lock:
        _destination(root, LOCK_NAME)
        changes.append({"path": LOCK_NAME, "action": "update"})
    result = {
        "schema": "se-harness-command-result-v1", "command": "skill-ownership",
        "outcome": "planned" if changes else "unchanged", "passed": True,
        "provider": provider, "target": str(root), "changes": changes, "written": False,
    }
    return root, after, writes, result


def plan_skill_ownership(target: Path, *, provider: str, plugin_root: Path | None = None) -> dict:
    return _prepare(target, provider, plugin_root)[3]


def apply_skill_ownership(target: Path, *, provider: str, plugin_root: Path | None = None) -> dict:
    """Apply current inputs. Partial deletions or writes are completed on retry."""
    root, lock, writes, result = _prepare(target, provider, plugin_root)
    for change in result["changes"]:
        path = _destination(root, change["path"])
        if change["action"] == "remove":
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink(missing_ok=True)
        elif change["path"] != LOCK_NAME:
            path.parent.mkdir(parents=True, exist_ok=True)
            atomic_write_bytes(path, writes[change["path"]])
    if any(change["path"] == LOCK_NAME for change in result["changes"]):
        atomic_write_bytes(root / LOCK_NAME, pretty_json_bytes(lock, ensure_ascii=True))
    if result["changes"]:
        result.update(outcome="applied", written=True)
    return result
