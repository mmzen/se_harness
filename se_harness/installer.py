"""Plan and apply the single standard harness template safely."""

from __future__ import annotations

import json
import os
import re
import sysconfig
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

from se_harness import __version__
from se_harness.integrity import (
    HASH_ALGORITHM,
    HASH_MODE,
    LOCK_SCHEMA,
    IntegrityError,
    canonical_text_equal,
    compare_lock_entry,
    digest_for_schema,
    parse_lock,
    raw_sha256,
)


LOCK_NAME = ".engineering-harness.lock"
CONFIG_NAME = ".engineering-harness.toml"
BEGIN_MARKER = "<!-- se-harness:begin -->"
END_MARKER = "<!-- se-harness:end -->"
FRAGMENT_TARGETS = {
    "AGENTS.md.fragment": "AGENTS.md",
    "CLAUDE.md.fragment": "CLAUDE.md",
    "gitignore.fragment": ".gitignore",
}
SEED_SUFFIX = ".seed"


class HarnessError(RuntimeError):
    """A bounded installation or configuration error."""


@dataclass(frozen=True)
class TemplateFile:
    source: Path
    target: Path
    mode: str


@dataclass(frozen=True)
class Change:
    path: str
    action: str
    mode: str
    desired: bytes
    current: bytes | None


def sha256(value: bytes) -> str:
    """Retain the legacy raw-byte helper for schema-1 compatibility."""

    return raw_sha256(value)


def template_root() -> Path:
    candidates = [
        Path(__file__).resolve().parent.parent / "templates" / "repository" / "standard",
        Path(sysconfig.get_path("data")) / "share" / "se-harness" / "templates" / "repository" / "standard",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()
    raise HarnessError("the standard template could not be located")


def ensure_target(path: Path, *, must_exist: bool) -> Path:
    target = path.expanduser().resolve()
    if must_exist and not target.is_dir():
        raise HarnessError(f"target repository does not exist: {target}")
    if target.exists() and not target.is_dir():
        raise HarnessError(f"target is not a directory: {target}")
    return target


def _render(raw: bytes, variables: dict[str, str]) -> bytes:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HarnessError("template files must be UTF-8") from exc
    for key, value in variables.items():
        text = text.replace("{{" + key + "}}", value)
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def _templates() -> list[TemplateFile]:
    root = template_root()
    result: list[TemplateFile] = []
    source_files = (
        item
        for item in root.rglob("*")
        if item.is_file()
        and "__pycache__" not in item.parts
        and item.suffix.lower() not in {".pyc", ".pyo"}
    )
    for source in sorted(source_files, key=lambda item: item.as_posix()):
        relative = source.relative_to(root)
        name = relative.name
        if name in FRAGMENT_TARGETS:
            result.append(TemplateFile(source, Path(FRAGMENT_TARGETS[name]), "fragment"))
        elif name.endswith(SEED_SUFFIX):
            result.append(TemplateFile(source, relative.with_name(name[: -len(SEED_SUFFIX)]), "seed"))
        elif name.endswith(".tpl"):
            result.append(TemplateFile(source, relative.with_name(name[:-4]), "managed"))
        else:
            result.append(TemplateFile(source, relative, "managed"))
    return result


def _block(fragment: bytes) -> bytes:
    content = fragment.decode("utf-8").strip()
    return f"{BEGIN_MARKER}\n{content}\n{END_MARKER}\n".encode("utf-8")


def _extract_block(content: bytes) -> bytes | None:
    begin_marker = BEGIN_MARKER.encode("utf-8")
    end_marker = END_MARKER.encode("utf-8")
    begin_count = content.count(begin_marker)
    end_count = content.count(end_marker)
    if begin_count == 0 and end_count == 0:
        return None
    if begin_count != 1 or end_count != 1:
        raise HarnessError("managed integration markers are incomplete or duplicated")
    start = content.find(begin_marker)
    end = content.find(end_marker)
    if start < 0 or end < start:
        raise HarnessError("managed integration markers are out of order")
    end += len(end_marker)
    if end < len(content) and content[end : end + 2] == b"\r\n":
        end += 2
    elif end < len(content) and content[end : end + 1] == b"\n":
        end += 1
    return content[start:end]


def tracked_content(mode: str, content: bytes) -> bytes | None:
    if mode == "fragment":
        return _extract_block(content)
    if mode == "managed":
        return content
    return None


def _merge_block(current: bytes | None, desired_block: bytes) -> bytes:
    if current is None or not current.strip():
        return desired_block
    existing = _extract_block(current)
    if existing is not None:
        start = current.find(BEGIN_MARKER.encode("utf-8"))
        end = start + len(existing)
        return current[:start] + desired_block + current[end:]
    separator = b"" if current.endswith((b"\n", b"\r\n")) else b"\n"
    return current + separator + b"\n" + desired_block


def safe_destination(root: Path, relative: Path) -> Path:
    destination = (root / relative).resolve()
    try:
        destination.relative_to(root)
    except ValueError as exc:
        raise HarnessError(f"template destination escapes the target: {relative}") from exc
    probe = root
    for part in relative.parts[:-1]:
        probe = probe / part
        if probe.exists() and probe.is_symlink():
            raise HarnessError(f"refusing to traverse a symlinked directory: {probe}")
    if destination.exists() and destination.is_symlink():
        raise HarnessError(f"refusing to replace a symlink: {destination}")
    return destination


def _load_lock(target: Path) -> dict:
    lock_path = target / LOCK_NAME
    if not lock_path.exists():
        return {"schema": 1, "tool_version": None, "files": {}}
    try:
        value = parse_lock(lock_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, IntegrityError) as exc:
        raise HarnessError(f"cannot read {LOCK_NAME}: {exc}") from exc
    return value


def load_lock(target: Path) -> dict:
    """Load and validate a schema-1 or schema-2 managed-file lock."""

    return _load_lock(target)


def _variables(target: Path, project_name: str | None, installed_at: str | None = None) -> dict[str, str]:
    selected_name = project_name or target.name
    if not isinstance(selected_name, str) or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._ -]{0,127}", selected_name) is None:
        raise HarnessError("project name must use 1-128 letters, numbers, spaces, dots, underscores, or hyphens")
    selected_date = installed_at if isinstance(installed_at, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", installed_at) else date.today().isoformat()
    return {
        "PROJECT_NAME": selected_name,
        "HARNESS_VERSION": __version__,
        "INSTALL_DATE": selected_date,
    }


def plan_install(
    target: Path,
    *,
    project_name: str | None,
    mode: str,
    adoption_report: bytes | None = None,
) -> tuple[list[Change], dict]:
    target = ensure_target(target, must_exist=(mode != "init"))
    if mode == "init" and target.exists() and any(target.iterdir()):
        raise HarnessError("init requires an empty or absent directory; use adopt for an existing repository")
    old_lock = _load_lock(target) if target.exists() else {"schema": 1, "tool_version": None, "files": {}}
    installed_at = None
    configured_project_name = None
    config_path = target / CONFIG_NAME
    if config_path.exists():
        try:
            import tomllib

            harness_config = tomllib.loads(config_path.read_text(encoding="utf-8")).get("harness", {})
            installed_at = harness_config.get("installed_at")
            configured_project_name = harness_config.get("project_name")
        except (OSError, ValueError):
            installed_at = None
    variables = _variables(target, project_name or configured_project_name, installed_at)
    changes: list[Change] = []
    old_files = old_lock.get("files", {})

    for item in _templates():
        destination = safe_destination(target, item.target)
        current = destination.read_bytes() if destination.exists() else None
        rendered = _render(item.source.read_bytes(), variables)
        desired = _merge_block(current, _block(rendered)) if item.mode == "fragment" else rendered
        relative = item.target.as_posix()
        old_entry = old_files.get(relative, {}) if isinstance(old_files.get(relative, {}), dict) else {}

        if item.mode == "seed":
            # Seed files become repository-owned as soon as they are installed.
            # A prior lock entry remembers intentional removal and prevents later
            # upgrades from recreating the file.
            action = "add" if current is None and old_entry.get("mode") != "seed" else "unchanged"
        elif current is None:
            action = "add"
        elif current == desired:
            action = "unchanged"
        elif item.mode == "fragment":
            current_block = _extract_block(current)
            desired_block = _extract_block(desired)
            if desired_block is None:
                raise HarnessError(f"rendered managed fragment is missing markers: {relative}")
            if current_block is None:
                action = "integrate"
            else:
                try:
                    desired_match = canonical_text_equal(current_block, desired_block)
                except IntegrityError as exc:
                    raise HarnessError(f"invalid managed text at {relative}: {exc}") from exc
                if desired_match:
                    action = "unchanged"
                elif mode in {"init", "adopt"}:
                    action = "conflict"
                else:
                    try:
                        match = compare_lock_entry(old_lock, old_entry, current_block, desired=desired_block)
                    except IntegrityError as exc:
                        raise HarnessError(f"invalid managed text at {relative}: {exc}") from exc
                    action = "update" if match != "mismatch" else "customized"
        else:
            try:
                desired_match = canonical_text_equal(current, desired)
            except IntegrityError as exc:
                raise HarnessError(f"invalid managed text at {relative}: {exc}") from exc
            if desired_match:
                action = "unchanged"
            elif mode in {"init", "adopt"}:
                action = "conflict"
            else:
                try:
                    match = compare_lock_entry(old_lock, old_entry, current, desired=desired)
                except IntegrityError as exc:
                    raise HarnessError(f"invalid managed text at {relative}: {exc}") from exc
                action = "update" if match != "mismatch" else "customized"
        changes.append(Change(relative, action, item.mode, desired, current))

    if adoption_report is not None:
        relative = "docs/engineering/ADOPTION_REPORT.md"
        destination = safe_destination(target, Path(relative))
        current = destination.read_bytes() if destination.exists() else None
        action = "add" if current is None else ("unchanged" if current == adoption_report else "conflict")
        changes.append(Change(relative, action, "generated", adoption_report, current))

    return sorted(changes, key=lambda item: item.path), old_lock


def apply_changes(target: Path, changes: Iterable[Change], old_lock: dict, *, allow_updates: bool) -> dict:
    target.mkdir(parents=True, exist_ok=True)
    changes = list(changes)
    blocking = {"conflict"} if not allow_updates else set()
    if any(item.action in blocking for item in changes):
        raise HarnessError("installation has conflicts; no files were written")

    safe_actions = {"add", "integrate"}
    if allow_updates:
        safe_actions.add("update")
    for item in changes:
        if item.action not in safe_actions:
            continue
        destination = safe_destination(target, Path(item.path))
        destination.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(item.desired)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, destination)
        finally:
            if os.path.exists(temporary_name):
                os.unlink(temporary_name)

    files: dict[str, dict[str, str]] = {}
    old_files = old_lock.get("files", {}) if isinstance(old_lock.get("files"), dict) else {}
    legacy_customized = any(item.action == "customized" and item.path in old_files for item in changes)
    output_schema = 1 if old_lock.get("schema") == 1 and legacy_customized else LOCK_SCHEMA
    for item in changes:
        destination = target / item.path
        if item.action == "customized":
            if item.path in old_files:
                files[item.path] = old_files[item.path]
            continue
        if item.mode == "seed":
            files[item.path] = {
                "mode": "seed",
                "state": "present" if destination.is_file() else "removed",
            }
            continue
        if not destination.exists() or item.mode == "generated":
            continue
        content = destination.read_bytes()
        tracked = tracked_content(item.mode, content)
        if tracked is not None:
            try:
                digest = digest_for_schema(tracked, output_schema, item.mode)
            except IntegrityError as exc:
                raise HarnessError(f"invalid managed text at {item.path}: {exc}") from exc
            files[item.path] = {"mode": item.mode, "sha256": digest}

    lock = {"schema": output_schema, "tool_version": __version__, "files": dict(sorted(files.items()))}
    if output_schema == LOCK_SCHEMA:
        lock["hash_algorithm"] = HASH_ALGORITHM
        lock["hash_mode"] = HASH_MODE
    lock_bytes = (json.dumps(lock, indent=2, sort_keys=True) + "\n").encode("utf-8")
    lock_path = target / LOCK_NAME
    fd, temporary_name = tempfile.mkstemp(prefix=f".{LOCK_NAME}.", dir=target)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(lock_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, lock_path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)
    return lock


def format_plan(changes: Iterable[Change]) -> str:
    changes = list(changes)
    lines = [f"{item.action:10} {item.path}" for item in changes if item.action != "unchanged"]
    unchanged = sum(item.action == "unchanged" for item in changes)
    lines.append(f"summary: {len(changes)} files, {unchanged} unchanged")
    return "\n".join(lines)
