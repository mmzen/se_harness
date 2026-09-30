"""Plan and apply the single standard harness template safely."""

from __future__ import annotations

import json
import re
import sysconfig
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Iterable, Literal

from se_harness import __version__
from se_harness.evaluator_identity import EvaluatorIdentityError, installed_evaluator_identity
from se_harness.integrity import (
    HASH_ALGORITHM,
    HASH_MODE,
    EXTERNAL_RESOURCE_LAYOUT,
    LOCK_SCHEMA,
    IntegrityError,
    atomic_write_bytes,
    canonical_json_bytes,
    canonical_sha256,
    canonical_text,
    canonical_text_equal,
    compare_lock_entry,
    parse_lock,
    pretty_json_bytes,
    read_toml,
    raw_sha256,
)


LOCK_NAME = ".engineering-harness.lock"
CONFIG_NAME = ".engineering-harness.toml"
BEGIN_MARKER = "<!-- se-harness:begin -->"
END_MARKER = "<!-- se-harness:end -->"
ATTRIBUTE_BEGIN_MARKER = "# se-harness:begin"
ATTRIBUTE_END_MARKER = "# se-harness:end"
FRAGMENT_TARGETS = {
    "gitattributes.fragment": ".gitattributes",
    "gitignore.fragment": ".gitignore",
}
SEED_SUFFIX = ".seed"
MACHINE_POLICY = frozenset({"ENGINEERING_HARNESS.md", "docs/engineering/WORKFLOW.json", "docs/engineering/QUALITY_GATES.json"})
INSTRUCTION_PREFIX = "docs/engineering/harness/"
RETIRED_ENTRIES = frozenset({"AGENTS.md", "CLAUDE.md"})
# Only the supported 0.18.0 upgrade converts full guides to these pointers.
# They are not templates and are never created by a fresh installation.
RETIRED_GUIDES = {
    "OPERATING_CARD.md": ("Operating card", ("CONTINUE.md",)),
    "DECISION_RIGHTS.md": ("Decision rights", ("AUTHORITY.md",)),
    "QUALITY_GATES.md": ("Quality gates", ("RESULTS.md",)),
    "WORKFLOW.md": ("Workflow", ("CONTINUE.md", "RECORD_STATE.md", "RESULTS.md")),
    "TRACEABILITY.md": ("Traceability", ("ARTIFACTS.md", "DEFINITION_LINKS.md", "WORK_AND_EVIDENCE.md")),
    "TECHNICAL_COMMUNICATION.md": ("Technical communication", ("COMMUNICATION.md",)),
}


def _legacy_guide_pointer(name: str) -> bytes:
    title, destinations = RETIRED_GUIDES[name]
    lines = [f"# {title}", "",
             "Compatibility pointer. The current instructions are in the following files;",
             "this file contains no additional policy. Read only the section selected by",
             "the root router or the evaluator result.", "",
             *(f"- [{destination}](harness/{destination})" for destination in destinations), ""]
    return "\n".join(lines).encode("utf-8")


def _retired_guide_changes(target: Path, lock: dict, replacements: set[str],
                           migration: dict) -> list[Change]:
    """Preserve leaving owner seeds; classify supported old full guides first."""
    legacy = lock.get("tool_version") == migration.get("source_version")
    result = []
    for name in RETIRED_GUIDES:
        relative = "docs/engineering/" + name
        destination = safe_destination(target, Path(relative))
        current = destination.read_bytes() if destination.exists() else None
        if relative not in lock.get("files", {}) and not legacy:
            continue
        if not legacy or current is None:
            result.append(Change(relative, "unchanged", "seed", current or b"", current))
            continue
        desired = _legacy_guide_pointer(name)
        if current == desired:
            action = "unchanged"
        elif relative in replacements or canonical_sha256(current) == migration.get("editable_guides", {}).get(relative):
            action = "update"
        else:
            action = "customized"
        result.append(Change(relative, action, "seed", desired, current))
    return result


def _managed(path: Path) -> bool:
    return path.as_posix() in MACHINE_POLICY or path.as_posix().startswith(INSTRUCTION_PREFIX)


class HarnessError(RuntimeError):
    """A bounded installation or configuration error."""


@dataclass(frozen=True)
class TemplateFile:
    source: Path
    target: Path
    mode: str



#: ECP-PRM-013: the installer's closed value sets, typed.
InstallMode = Literal["init", "upgrade"]
ChangeAction = Literal["add", "update", "adopt", "remove", "customized", "conflict", "integrate", "unchanged", "preserve"]

@dataclass(frozen=True)
class Change:
    path: str
    action: ChangeAction
    mode: str
    desired: bytes
    current: bytes | None


#: SPEC-DST-025 DST-ENG-003, DST-ENG-004: the evaluator's own scripts ship inside
#: the package and are resolved from here, never from the target repository, the
#: working directory or a ``share/`` prefix.
ENGINE_ROOT = Path(__file__).resolve().parent / "engine"


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
    from se_harness.resources import _safe_path
    _safe_path(path.expanduser())
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
    return canonical_text(text).encode("utf-8")  # ECP-PRM-010


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
            target = relative.with_name(name[:-4])
            result.append(TemplateFile(source, target, "managed" if _managed(target) else "seed"))
        else:
            result.append(TemplateFile(source, relative, "managed" if _managed(relative) else "seed"))
    return result


def template_files() -> list[TemplateFile]:
    """Return the deterministic standard-template manifest."""

    return _templates()


def effective_template_files(lock: dict) -> list[TemplateFile]:
    """Use the one ownership resolver for every installed inventory consumer."""

    from se_harness.skill_ownership import effective_templates

    return effective_templates(_templates(), lock)


#: SPEC-DST-027 DST-MWF-006: the Git dot-files read a line as a pattern unless it
#: starts with a hash, so their managed block takes the hash-prefixed pair; the
#: Markdown fragments keep the HTML comments. ``_extract_block`` accepts both
#: pairs, so an upgrade of a block written with the other pair rewrites only the
#: block (DST-MWF-007).
HASH_MARKER_TARGETS = frozenset({Path(".gitattributes"), Path(".gitignore")})


def _block(fragment: bytes, target: Path) -> bytes:
    content = fragment.decode("utf-8").strip()
    if target in HASH_MARKER_TARGETS:
        return f"{ATTRIBUTE_BEGIN_MARKER}\n{content}\n{ATTRIBUTE_END_MARKER}\n".encode("utf-8")
    return f"{BEGIN_MARKER}\n{content}\n{END_MARKER}\n".encode("utf-8")


def _extract_block(content: bytes) -> bytes | None:
    detected: list[tuple[bytes, bytes]] = []
    for begin_text, end_text in (
        (BEGIN_MARKER, END_MARKER),
        (ATTRIBUTE_BEGIN_MARKER, ATTRIBUTE_END_MARKER),
    ):
        begin_marker = begin_text.encode("utf-8")
        end_marker = end_text.encode("utf-8")
        begin_count = content.count(begin_marker)
        end_count = content.count(end_marker)
        if begin_count == 0 and end_count == 0:
            continue
        if begin_count != 1 or end_count != 1:
            raise HarnessError("managed integration markers are incomplete or duplicated")
        detected.append((begin_marker, end_marker))
    if not detected:
        return None
    if len(detected) != 1:
        raise HarnessError("managed integration markers are incomplete or duplicated")
    begin_marker, end_marker = detected[0]
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
        start = current.find(existing)
        end = start + len(existing)
        return current[:start] + desired_block + current[end:]
    separator = b"" if current.endswith((b"\n", b"\r\n")) else b"\n"
    return current + separator + b"\n" + desired_block


def safe_destination(root: Path, relative: Path) -> Path:
    if relative.is_absolute() or ".." in relative.parts:
        raise HarnessError(f"template destination escapes the target: {relative}")
    root = root.resolve()
    probe = root
    for part in relative.parts[:-1]:
        probe = probe / part
        if probe.is_symlink() or (probe.exists() and getattr(probe.lstat(), "st_file_attributes", 0) & 0x400):
            raise HarnessError(f"refusing to traverse a symlinked directory: {probe}")
    unresolved_destination = root / relative
    if unresolved_destination.is_symlink() or (unresolved_destination.exists() and getattr(unresolved_destination.lstat(), "st_file_attributes", 0) & 0x400):
        raise HarnessError(f"refusing to replace a symlink: {unresolved_destination}")
    destination = unresolved_destination.resolve()
    try:
        destination.relative_to(root)
    except ValueError as exc:
        raise HarnessError(f"template destination escapes the target: {relative}") from exc
    return destination


def _load_lock(target: Path) -> dict:
    lock_path = target / LOCK_NAME
    if not lock_path.exists():
        return {"schema": LOCK_SCHEMA, "tool_version": None, "files": {}}
    try:
        value = parse_lock(lock_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, IntegrityError) as exc:
        raise HarnessError(f"cannot read {LOCK_NAME}: {exc}") from exc
    return value


def load_lock(target: Path) -> dict:
    """Load and validate a supported standard managed-file lock."""

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


def _updated_config(current: bytes, version: str) -> bytes:
    """An explicit upgrade updates the selected version and keeps owner settings."""
    text = current.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    section = re.search(r"(?ms)^\[harness\][ \t]*(?:\#.*)?$.*?(?=^\[|\Z)", text)
    if section is None:
        raise HarnessError("use --replace-file .engineering-harness.toml to replace a config without a [harness] section")
    value, count = re.subn(r"(?m)^(tool_version[ \t]*=[ \t]*).*$", lambda match: match[1] + '"' + version + '"', section[0])
    if count != 1:
        raise HarnessError("the [harness] section must identify one tool_version")
    return (text[:section.start()] + value + text[section.end():]).encode("utf-8")


INTEGRATIONS = {
    "git": (".gitattributes",),
    "ci": (".github/workflows/engineering-harness.yml", ".gitignore"),
    "pr": (".github/PULL_REQUEST_TEMPLATE.md",),
}


def _resource_config(current: bytes | None, variables: dict[str, str]) -> bytes:
    if current is None:
        current = _render((template_root() / (CONFIG_NAME + ".tpl")).read_bytes(), variables)
    updated = _updated_config(current, __version__)
    text = updated.decode("utf-8")
    if not re.search(r"(?m)^resource_layout\s*=", text):
        text = re.sub(r"(?m)^(\[harness\][^\n]*\n)",
                      lambda m: m[0] + f'resource_layout = "{EXTERNAL_RESOURCE_LAYOUT}"\n', text, count=1)
    return text.encode("utf-8")


def _replacement_resources(target: Path, config: bytes, lock: dict) -> bytes:
    """Validate proposed selection outside the checkout through the shared resolver."""
    from se_harness.resources import ResourceSet
    with tempfile.TemporaryDirectory(prefix="se-harness-selection-") as directory:
        preview = Path(directory)
        (preview / CONFIG_NAME).write_bytes(config)
        (preview / LOCK_NAME).write_bytes(pretty_json_bytes(lock, ensure_ascii=True))
        selected = ResourceSet(preview)
        if selected.root.is_relative_to(target):
            raise HarnessError("replacement resources must be outside the target repository")
        entry = selected.query("ENGINEERING_HARNESS.md", content=True)["content"].encode("utf-8")
        selected.assert_current()
        return entry


def _prior_templates(wheel: Path, lock: dict, variables: dict[str, str]) -> dict[str, tuple[str, bytes]]:
    """Read stock bytes from the exact prior wheel; never execute prior package code."""
    from se_harness.evaluator_identity import wheel_payload_sha256
    from se_harness.resources import _read
    raw = _read(wheel, limit=100 * 1024 * 1024)
    identity = lock["evaluator"]
    if identity.get("archive_sha256") and raw_sha256(raw) != identity["archive_sha256"]:
        raise HarnessError("prior wheel archive differs from the selected lock")
    prefix = f'se_harness-{lock["tool_version"]}.data/data/share/se-harness/templates/repository/standard/'
    old_variables = {**variables, "HARNESS_VERSION": lock["tool_version"]}
    result = {}
    fragments = {**FRAGMENT_TARGETS, "AGENTS.md.fragment": "AGENTS.md", "CLAUDE.md.fragment": "CLAUDE.md"}
    # Hash and inspect one bounded snapshot, even if the source wheel changes.
    with tempfile.TemporaryDirectory(prefix="se-harness-prior-wheel-") as directory:
        snapshot = Path(directory) / wheel.name
        snapshot.write_bytes(raw)
        if wheel_payload_sha256(snapshot, lock["tool_version"]) != identity["payload_sha256"]:
            raise HarnessError("prior wheel payload differs from the selected lock")
        with zipfile.ZipFile(snapshot) as archive:
            for name in archive.namelist():
                if not name.startswith(prefix) or name.endswith("/"):
                    continue
                relative = Path(name.removeprefix(prefix))
                mode = "managed" if _managed(relative) else "seed"
                if relative.name in fragments:
                    relative, mode = Path(fragments[relative.name]), "fragment"
                elif relative.suffix in {".tpl", ".seed"}:
                    relative = relative.with_suffix("")
                    mode = "managed" if _managed(relative) else "seed"
                result[relative.as_posix()] = (mode, _render(archive.read(name), old_variables))
    return result


def plan_install(
    target: Path, *, project_name: str | None, mode: str,
    adoption_report: bytes | None = None, replace_files: Iterable[str] = (),
    external_resources: bool = False, integrations: Iterable[str] = (),
    retire_files: Iterable[str] = (), prior_wheel: Path | None = None,
) -> tuple[list[Change], dict]:
    """Default new installations are minimal; legacy layout migration is explicit."""
    if mode not in {"init", "upgrade"}:
        raise HarnessError(f"unknown installation mode {mode!r}; expected init or upgrade")
    integrations, retire_files, replace_files = tuple(integrations), tuple(retire_files), tuple(replace_files)
    target = ensure_target(target, must_exist=mode == "upgrade")
    old = _load_lock(target)
    selected_external = old.get("resource_layout") == EXTERNAL_RESOURCE_LAYOUT
    minimal = selected_external or external_resources or (mode == "init" and old.get("tool_version") is None)
    if not minimal:
        if integrations or retire_files or prior_wheel:
            raise HarnessError("legacy integrations are already installed; select --external-resources to migrate")
        return _plan_legacy_install(target, project_name=project_name, mode=mode,
                                    adoption_report=adoption_report, replace_files=replace_files)
    if replace_files or adoption_report:
        raise HarnessError("minimal installation does not replace owner files or generate an adoption report")
    if set(integrations) - INTEGRATIONS.keys():
        raise HarnessError("unknown repository integration")
    config_path = safe_destination(target, Path(CONFIG_NAME))
    current_config = config_path.read_bytes() if config_path.exists() else None
    if current_config is not None and old.get("tool_version") is None:
        raise HarnessError("configuration exists without its selected lock; no files were written")
    harness = read_toml(config_path).get("harness", {}) if current_config else {}
    if current_config and (not isinstance(harness, dict) or harness.get("tool_version") != old["tool_version"]
                           or harness.get("resource_layout") != old.get("resource_layout")):
        raise HarnessError("configuration and lock selections differ")
    variables = _variables(target, project_name or harness.get("project_name"), harness.get("installed_at"))
    config = _resource_config(current_config, variables)
    if selected_external and harness.get("tool_version") == __version__:
        config = current_config
    identity = installed_evaluator_identity().to_lock()
    lock = {"schema": 5, "resource_layout": EXTERNAL_RESOURCE_LAYOUT,
            "tool_version": __version__, "hash_algorithm": HASH_ALGORITHM, "hash_mode": HASH_MODE,
            "evaluator": identity, "files": {}}
    _replacement_resources(target, config, lock)
    if selected_external and mode == "init" and old["evaluator"] != identity:
        raise HarnessError("init cannot change an existing evaluator selection; use upgrade")
    changes = [Change(CONFIG_NAME, "add" if current_config is None else "unchanged" if config == current_config else "update",
                      "seed", config, current_config)]
    old_files = old.get("files", {})
    available_integrations = {path for paths in INTEGRATIONS.values() for path in paths}
    if selected_external and set(old_files) - available_integrations:
        raise HarnessError("external selection contains an unsupported repository integration")
    requested_integrations = {path for name in integrations for path in INTEGRATIONS[name]}
    integration_paths = set(requested_integrations)
    # Existing integration files remain selected; migration does not add new integrations.
    integration_paths.update(set(old_files) & available_integrations)
    templates = {item.target.as_posix(): item for item in _templates()}
    for relative in sorted(integration_paths):
        item = templates[relative]
        destination = safe_destination(target, Path(relative))
        current = destination.read_bytes() if destination.exists() else None
        rendered = _render(item.source.read_bytes(), variables)
        desired = _merge_block(current, _block(rendered, item.target)) if item.mode == "fragment" else rendered
        mode_value = item.mode
        action = "add" if current is None else "unchanged" if canonical_text_equal(current, desired) else "conflict"
        if current is None and item.mode == "seed" and relative in old_files and relative not in requested_integrations:
            # Removing an owner seed is an owner choice, not installation damage.
            desired, action = b"", "unchanged"
        elif current is not None and item.mode == "seed":
            # Optional seed files become owner content at installation.
            desired, action = current, "unchanged"
        elif current is not None and item.mode == "fragment" and _extract_block(current) is None:
            action = "integrate"
        elif current is not None and compare_lock_entry(old_files.get(relative, {}), tracked_content(item.mode, current) or b"") == "canonical":
            action = "update" if current != desired else "unchanged"
        changes.append(Change(relative, action, mode_value, desired, current))
        lock["files"][relative] = ({"mode": "seed", "state": "removed" if current is None and action == "unchanged" else "present"} if item.mode == "seed"
                                   else {"mode": item.mode, "sha256": canonical_sha256(tracked_content(item.mode, desired))})
    retire = set(retire_files)
    migrating = old.get("tool_version") is not None and not selected_external
    if prior_wheel is not None and not migrating:
        raise HarnessError("--prior-wheel is only for an explicit legacy resource migration")
    if retire and not migrating:
        raise HarnessError("--retire-file is only for an explicit legacy resource migration")
    if migrating:
        if prior_wheel is None:
            raise HarnessError("resource migration requires --prior-wheel for stock-file recognition")
        stock = _prior_templates(prior_wheel, old, variables)
        eligible = {path for path, entry in old_files.items()
                    if entry["mode"] == "seed" and path != CONFIG_NAME and path not in integration_paths}
        if retire - eligible:
            raise HarnessError("--retire-file must name a prior editable seed: " + ", ".join(sorted(retire - eligible)))
        for relative, old_entry in sorted(old_files.items()):
            if relative == CONFIG_NAME or relative in integration_paths:
                continue
            destination = safe_destination(target, Path(relative))
            current = destination.read_bytes() if destination.exists() else None
            if current is None:
                continue
            mode_value = old_entry["mode"]
            resource_seed = relative == "docs/engineering/ARTIFACT_AUTHORING.md" or relative.startswith("docs/engineering/templates/")
            if mode_value == "seed" and not resource_seed and relative not in retire:
                changes.append(Change(relative, "preserve", mode_value, current, current))
                continue
            known = stock.get(relative)
            tracked = current if mode_value == "seed" else tracked_content(mode_value, current)
            expected = _block(known[1], Path(relative)) if known and mode_value == "fragment" else known[1] if known else None
            recognized = expected is not None and tracked is not None and canonical_text_equal(tracked, expected)
            if mode_value != "seed":
                recognized = recognized and compare_lock_entry(old_entry, tracked or b"") == "canonical"
            action = "customized" if not recognized else "remove" if mode_value != "seed" or relative in retire else "preserve"
            desired = current
            if action == "remove":
                desired = current.replace(tracked, b"", 1) if mode_value == "fragment" else b""
            changes.append(Change(relative, action, mode_value, desired, current))
    lock_bytes = pretty_json_bytes(lock, ensure_ascii=True)
    lock_path = safe_destination(target, Path(LOCK_NAME))
    old_bytes = lock_path.read_bytes() if lock_path.exists() else None
    changes.append(Change(LOCK_NAME, "add" if old_bytes is None else "unchanged" if old_bytes == lock_bytes else "update",
                          "selection", lock_bytes, old_bytes))
    if mode == "init" and any(item.action == "update" and item.path != LOCK_NAME for item in changes):
        raise HarnessError("init cannot update an existing installation; use upgrade")
    return sorted(changes, key=lambda item: item.path), old


def _plan_legacy_install(
    target: Path,
    *,
    project_name: str | None,
    mode: str,
    adoption_report: bytes | None = None,
    replace_files: Iterable[str] = (),
) -> tuple[list[Change], dict]:
    # ECP-INS-004: two modes, "init" (installation into any target) and
    # "upgrade". A target with content is installed into, not refused.
    if mode not in {"init", "upgrade"}:
        raise HarnessError(f"unknown installation mode {mode!r}; expected init or upgrade")
    target = ensure_target(target, must_exist=(mode == "upgrade"))
    old_lock = _load_lock(target) if target.exists() else {"schema": LOCK_SCHEMA, "tool_version": None, "files": {}}
    installed_at = None
    configured_project_name = None
    harness_config = {}
    config_path = target / CONFIG_NAME
    if config_path.exists():
        try:
            harness_config = read_toml(config_path).get("harness", {})  # ECP-PRM-011: the one reader
            installed_at = harness_config.get("installed_at") if isinstance(harness_config, dict) else None
            configured_project_name = harness_config.get("project_name") if isinstance(harness_config, dict) else None
        except IntegrityError:
            installed_at = None
    variables = _variables(target, project_name or configured_project_name, installed_at)
    changes: list[Change] = []
    replacements = {Path(path).as_posix() for path in replace_files}
    templates = effective_template_files(old_lock)
    editable = {item.target.as_posix() for item in templates if item.mode == "seed"}
    old_files = old_lock.get("files", {})
    from se_harness.instruction_discovery import load_catalog, validate_collection
    migration = load_catalog().get("migration", {})
    legacy_guides = migration.get("editable_guides", {})
    if mode == "upgrade" and old_lock.get("tool_version") == migration.get("source_version"):
        editable.update("docs/engineering/" + name for name in RETIRED_GUIDES
                        if safe_destination(target, Path("docs/engineering/" + name)).is_file())
    if replacements - editable:
        raise HarnessError("--replace-file must name a seeded file: " + ", ".join(sorted(replacements - editable)))

    for item in templates:
        destination = safe_destination(target, item.target)
        current = destination.read_bytes() if destination.exists() else None
        rendered = _render(item.source.read_bytes(), variables)
        desired = _merge_block(current, _block(rendered, item.target)) if item.mode == "fragment" else rendered
        relative = item.target.as_posix()
        old_entry = old_files.get(relative, {}) if isinstance(old_files.get(relative, {}), dict) else {}

        if item.mode == "seed":
            if relative in replacements:
                action = "update" if current is not None and current != desired else ("add" if current is None else "unchanged")
            elif current is None:
                action = "unchanged" if old_entry.get("mode") == "seed" else "add"
            elif relative == CONFIG_NAME and mode == "upgrade" and harness_config.get("tool_version") != __version__:
                desired = _updated_config(current, __version__)
                action = "update"
            elif relative in legacy_guides and not canonical_text_equal(current, desired):
                # A retained explanatory guide becomes a pointer, never a second
                # current policy. Customized owner seeds need an explicit choice.
                recognized = (old_lock.get("tool_version") == migration.get("source_version")
                              and canonical_sha256(current) == legacy_guides[relative])
                action = "update" if mode == "upgrade" and recognized else "customized"
            else:
                action = "unchanged" if old_entry.get("mode") == "seed" else "adopt"
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
                elif mode == "init":
                    action = "conflict"
                else:
                    try:
                        match = compare_lock_entry(old_entry, current_block)
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
            elif mode == "init":
                action = "conflict"
            else:
                try:
                    match = compare_lock_entry(old_entry, current)
                except IntegrityError as exc:
                    raise HarnessError(f"invalid managed text at {relative}: {exc}") from exc
                action = "update" if match != "mismatch" else "customized"
        changes.append(Change(relative, action, item.mode, desired, current))

    if mode == "upgrade":
        changes.extend(_retired_guide_changes(target, old_lock, replacements, migration))
        changes.extend(_plan_leaving_set(target, old_lock, old_files))

    # Check the replacement entry and every mapped action before any old entry
    # can be retired. Atomic apply installs this complete collection before
    # removing fragments. Native host qualification is a separate release check.
    planned = {item.path: (item.current if item.action in {"unchanged", "adopt", "customized", "conflict"}
                          else item.desired) for item in changes}
    if not any(item.action in {"customized", "conflict"} for item in changes):
        validate_collection({path: raw for path, raw in planned.items() if raw is not None})

    if adoption_report is not None:
        relative = "docs/engineering/ADOPTION_REPORT.md"
        destination = safe_destination(target, Path(relative))
        current = destination.read_bytes() if destination.exists() else None
        action = "add" if current is None else ("unchanged" if current == adoption_report else "conflict")
        changes.append(Change(relative, action, "generated", adoption_report, current))

    return sorted(changes, key=lambda item: item.path), old_lock


def _plan_leaving_set(target: Path, old_lock: dict, old_files: dict) -> list[Change]:
    """Classify prior-lock managed paths that left the managed set.

    A byte-identical copy plans as ``remove``; a differing copy plans as
    ``customized`` and blocks the apply like an in-set customization. Seed
    entries are owner-owned from installation, and a path with no file on
    disk retires silently: both simply leave the written lock. An empty
    ``desired`` on a ``remove`` means the file is deleted; a fragment whose
    owner content remains carries that remainder as ``desired``.
    """

    managed_targets = {item.target.as_posix() for item in effective_template_files(old_lock)}
    from se_harness.instruction_discovery import load_catalog
    migration = load_catalog().get("migration", {})
    changes: list[Change] = []
    for relative in sorted(set(old_files) - managed_targets):
        old_entry = old_files.get(relative)
        if not isinstance(old_entry, dict):
            continue
        old_mode = old_entry.get("mode")
        if old_mode not in {"managed", "fragment"}:
            continue
        destination = safe_destination(target, Path(relative))
        if not destination.is_file():
            continue
        current = destination.read_bytes()
        tracked = tracked_content(str(old_mode), current)
        if tracked is None:
            continue
        try:
            match = compare_lock_entry(old_entry, tracked)
        except IntegrityError as exc:
            raise HarnessError(f"invalid managed text at {relative}: {exc}") from exc
        if match == "mismatch":
            changes.append(Change(relative, "customized", str(old_mode), current, current))
            continue
        if relative in RETIRED_ENTRIES:
            recognized = (old_mode == "fragment"
                          and old_lock.get("tool_version") == migration.get("source_version")
                          and canonical_sha256(tracked) == migration.get("fragments", {}).get(relative))
            if not recognized:
                changes.append(Change(relative, "customized", str(old_mode), current, current))
                continue
        if old_mode == "fragment":
            start = current.find(tracked)
            remainder = current[:start] + current[start + len(tracked) :]
            desired = remainder  # Whitespace is owner content too.
        else:
            desired = b""
        changes.append(Change(relative, "remove", str(old_mode), desired, current))
    return changes


# ECP-PRM-008: the installer's five writes go through integrity's one atomic writer.
_atomic_write = atomic_write_bytes


def _prune_empty_directories(directory: Path, root: Path) -> None:
    """Remove directories a deletion left empty, ascending no further than root."""

    root = root.resolve()
    directory = directory.resolve()
    while directory != root and root in directory.parents:
        try:
            if any(directory.iterdir()):
                return
            directory.rmdir()
        except OSError:
            return
        directory = directory.parent


def _restore_snapshot(snapshot: dict[Path, bytes | None]) -> list[str]:
    failures: list[str] = []
    for destination, original in reversed(tuple(snapshot.items())):
        try:
            if original is None:
                destination.unlink(missing_ok=True)
            else:
                _atomic_write(destination, original)
        except (OSError, RuntimeError) as exc:
            failures.append(f"{destination}: {type(exc).__name__}: {exc}")
    return failures


UPGRADE_EVIDENCE_SCHEMA = "se-harness-evaluator-upgrade-evidence-v1"


def validate_upgrade_evidence_path(path: Path) -> PurePosixPath:
    """Require repository-relative JSON evidence below docs/engineering/.../evidence/."""

    if path.is_absolute() or ".." in path.parts:
        raise HarnessError("upgrade evidence path must be repository-relative")
    normalized = PurePosixPath(path.as_posix())
    if (
        len(normalized.parts) < 4
        or normalized.parts[:2] != ("docs", "engineering")
        or "evidence" not in normalized.parts[2:-1]
        or normalized.suffix != ".json"
    ):
        raise HarnessError("upgrade evidence must be a JSON path below docs/engineering/.../evidence/")
    return normalized


def _upgrade_evidence_bytes(
    *,
    prior_lock_sha256: str,
    old_lock: dict,
    lock: dict,
    changes: list[Change],
) -> bytes:
    # SPEC-REB-012 rule 4: the same canonical document as before, minus the
    # retired work-order packet fields, which are carried as null.
    changed = [item for item in changes if item.action in {"add", "integrate", "update", "remove"}]
    value = {
        "schema": UPGRADE_EVIDENCE_SCHEMA,
        "work_order": None,
        "authorization_path": None,
        "scope": "standard-root-only",
        "authorized_by": None,
        "prior": {
            "lock_sha256": prior_lock_sha256,
            "lock_match": None,
            "tool_version": old_lock.get("tool_version"),
            "evaluator": old_lock.get("evaluator"),
        },
        "target": lock.get("evaluator"),
        "plan": [
            {"action": item.action, "mode": item.mode, "path": item.path}
            for item in changed
        ],
        "transaction": {
            "atomic": True,
            "outcome": "applied",
            "rollback": "pre-write snapshot restored on any failed write or postcondition",
        },
        "postconditions": {
            "lock_matches_target": True,
            "no_op_replay": True,
            "product_release_performed": False,
            "external_action_performed": False,
        },
        "authority": (
            "This evidence records a bounded repository transaction. It does not verify work, "
            "authorize a release, publish, tag, deploy, or grant incident authority."
        ),
    }
    return canonical_json_bytes(value, ensure_ascii=True)  # ECP-PRM-006, ECP-PRM-007


def apply_changes(
    target: Path,
    changes: Iterable[Change],
    old_lock: dict,
    *,
    allow_updates: bool,
    evidence_output: Path | None = None,
    replace_files: Iterable[str] = (),
    instruction_delivery_evidence: Path | None = None,
    external_resources: bool = False,
    integrations: Iterable[str] = (),
    retire_files: Iterable[str] = (),
    prior_wheel: Path | None = None,
) -> dict:
    changes = list(changes)
    integrations, retire_files, replace_files = tuple(integrations), tuple(retire_files), tuple(replace_files)
    selection = next((item for item in changes if item.path == LOCK_NAME and item.mode == "selection"), None)
    if selection is not None:
        config = next(item.desired for item in changes if item.path == CONFIG_NAME)
        replacement_entry = _replacement_resources(target, config, json.loads(selection.desired))
        # Fresh plans also bind every observed destination. No overwrite after preview.
        for item in changes:
            path = safe_destination(target, Path(item.path))
            observed = path.read_bytes() if path.exists() else None
            if observed != item.current:
                raise HarnessError("installation plan changed before apply; no files were written")
    transition = False
    target_identity = None
    prior_lock_sha256: str | None = None
    if allow_updates:
        refreshed_changes, refreshed_lock = plan_install(
            target,
            project_name=None,
            mode="upgrade",
            replace_files=replace_files,
            external_resources=external_resources,
            integrations=integrations,
            retire_files=retire_files,
            prior_wheel=prior_wheel,
        )
        if old_lock != refreshed_lock or changes != refreshed_changes:
            raise HarnessError("upgrade plan or installed root changed before apply; no files were written")
        from se_harness import mutation_guard

        authority = mutation_guard.require_mutation_authority(
            target,
            operation="upgrade-apply",
            allow_upgrade_transition=True,
        )
        transition = bool(getattr(authority, "transition", False))
        target_identity = getattr(authority, "target_identity", None)
        lock_file = target / LOCK_NAME
        if lock_file.is_file():
            # ECP-PRM-022: the lock's digest under the mode its hash-bound class declares.
            from se_harness.hash_bound import HashBoundError, declared_digest

            try:
                prior_lock_sha256 = declared_digest(LOCK_NAME, lock_file.read_bytes())
            except HashBoundError as exc:
                raise HarnessError(f"cannot hash the prior lock: {exc}") from exc
        # REQ-LRE-003 (the evaluator-evidence floor, owner decision of
        # 2026-08-30): a released record without evaluator evidence is not
        # assessed, so an identity transition enumerates nothing, refuses
        # nothing and declares nothing on unbound records' account.
    elif old_lock.get("tool_version") is not None or (target / CONFIG_NAME).exists():
        # Init and first adoption have no installed authority to prove. A direct
        # API call against an already-installed root is an ordinary mutation,
        # even when its caller disables managed-file updates.
        from se_harness import mutation_guard

        mutation_guard.require_mutation_authority(
            target,
            operation="installed-root-apply",
        )
    blocking = {"conflict", "customized"}
    if any(item.action in blocking for item in changes):
        raise HarnessError("installation has conflicts or customizations; no files were written")
    if allow_updates and any(item.action == "remove" and item.path in RETIRED_ENTRIES | {"ENGINEERING_HARNESS.md"} for item in changes):
        from se_harness.instruction_discovery import validate_delivery_evidence
        entry = replacement_entry if selection is not None else next(item.desired for item in changes if item.path == "ENGINEERING_HARNESS.md")
        validate_delivery_evidence(instruction_delivery_evidence, target, entry, (target / LOCK_NAME).read_bytes())
    target.mkdir(parents=True, exist_ok=True)

    safe_actions = {"add", "integrate"}
    if allow_updates:
        safe_actions.add("update")
    destinations = {
        item.path: safe_destination(target, Path(item.path))
        for item in changes
        if item.action in safe_actions and item.path != LOCK_NAME
    }
    # Removals execute only inside an update-allowing transaction; a plan
    # applied without update authority keeps the prior lock entries so the
    # root never records a retirement it did not perform.
    removals = {
        item.path: (safe_destination(target, Path(item.path)), item.desired)
        for item in changes
        if item.action == "remove" and allow_updates
    }
    evidence_destination: Path | None = None
    if allow_updates and evidence_output is not None:
        evidence_relative = validate_upgrade_evidence_path(evidence_output)
        evidence_destination = safe_destination(target, Path(evidence_relative.as_posix()))
        if evidence_destination in destinations.values() or any(
            evidence_destination == destination for destination, _ in removals.values()
        ):
            raise HarnessError("upgrade evidence path overlaps a managed destination")
        if evidence_destination.exists():
            raise HarnessError("upgrade evidence output already exists; no files were written")
    lock_path = safe_destination(target, Path(LOCK_NAME))
    snapshot: dict[Path, bytes | None] = {
        destination: destination.read_bytes() if destination.is_file() else None
        for destination in destinations.values()
    }
    for destination, _ in removals.values():
        snapshot.setdefault(destination, destination.read_bytes() if destination.is_file() else None)
    snapshot[lock_path] = lock_path.read_bytes() if lock_path.is_file() else None
    if evidence_destination is not None:
        snapshot[evidence_destination] = (
            evidence_destination.read_bytes() if evidence_destination.is_file() else None
        )

    try:
        for item in changes:
            destination = destinations.get(item.path)
            if destination is not None:
                _atomic_write(destination, item.desired)
        for destination, desired in removals.values():
            if desired:
                # A fragment whose owner content remains keeps that remainder.
                _atomic_write(destination, desired)
            else:
                destination.unlink(missing_ok=True)
                _prune_empty_directories(destination.parent, target)

        files: dict[str, dict[str, str]] = {}
        old_files = old_lock.get("files", {}) if isinstance(old_lock.get("files"), dict) else {}
        for item in changes:
            destination = target / item.path
            if item.action == "preserve" or item.path == LOCK_NAME:
                continue
            if item.action == "customized":
                if item.path in old_files:
                    files[item.path] = old_files[item.path]
                continue
            if item.action == "remove":
                if item.path not in removals and item.path in old_files:
                    files[item.path] = old_files[item.path]
                continue
            if item.mode == "seed":
                if item.path in {"docs/engineering/" + name for name in RETIRED_GUIDES}:
                    # Retired seeds remain owner files, including a just-migrated
                    # 0.18.0 pointer. Neither these files nor their absence is
                    # part of the new installation's tracked template inventory.
                    continue
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
                    digest = canonical_sha256(tracked)
                except IntegrityError as exc:
                    raise HarnessError(f"invalid managed text at {item.path}: {exc}") from exc
                files[item.path] = {"mode": item.mode, "sha256": digest}

        lock = {"schema": LOCK_SCHEMA, "tool_version": __version__, "files": dict(sorted(files.items()))}
        if old_lock.get("schema") == 4:
            lock["schema"] = 4
            lock["skill_ownership"] = old_lock["skill_ownership"]
        if selection is not None:
            lock = json.loads(selection.desired)
        lock["hash_algorithm"] = HASH_ALGORITHM
        lock["hash_mode"] = HASH_MODE
        try:
            lock["evaluator"] = installed_evaluator_identity().to_lock()
        except EvaluatorIdentityError as exc:
            raise HarnessError(f"cannot identify the installed evaluator payload: {exc}") from exc
        if target_identity is not None:
            if lock.get("evaluator") != target_identity.to_lock():
                raise HarnessError(
                    "installed evaluator identity changed after the authority check; no files were retained"
                )
        lock_bytes = pretty_json_bytes(lock, ensure_ascii=True)  # ECP-PRM-006: the same bytes as before
        if not lock_path.exists() or lock_path.read_bytes() != lock_bytes:
            _atomic_write(lock_path, lock_bytes)
        if selection is not None:
            from se_harness.resources import ResourceSet
            ResourceSet(target).assert_current()
        if transition:
            replay, replay_lock = plan_install(target, project_name=None, mode="upgrade")
            if replay_lock != lock or any(item.action != "unchanged" for item in replay):
                raise HarnessError("upgrade postcondition failed: replay is not a no-op")
        if evidence_destination is not None:
            _atomic_write(
                evidence_destination,
                _upgrade_evidence_bytes(
                    prior_lock_sha256=prior_lock_sha256 or "",
                    old_lock=old_lock,
                    lock=lock,
                    changes=changes,
                ),
            )
        return lock
    except BaseException as exc:
        rollback_failures = _restore_snapshot(snapshot)
        if rollback_failures:
            details = "; ".join(rollback_failures)
            raise HarnessError(f"installation transaction failed and rollback was incomplete: {details}") from exc
        raise


def format_plan(changes: Iterable[Change]) -> str:
    changes = list(changes)
    lines = [f"{item.action:10} {item.path}" for item in changes if item.action != "unchanged"]
    unchanged = sum(item.action == "unchanged" for item in changes)
    lines.append(f"summary: {len(changes)} files, {unchanged} unchanged")
    return "\n".join(lines)
