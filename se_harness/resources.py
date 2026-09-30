"""Resolve the selected evaluator's resources without repository copies.

Resource IDs retain their familiar relative names. Local paths are query output,
never portable selection or workflow-result identity. The wheel payload is the
only resource manifest; there is no second registry or fallback search.
"""
from __future__ import annotations

import json
import re
import stat
import sys
import sysconfig
import tomllib
from pathlib import Path, PurePosixPath
from typing import Any

from se_harness import __version__
from se_harness.evaluator_identity import (
    EvaluatorIdentityError, canonical_payload_manifest, installed_evaluator_identity,
)
from se_harness.integrity import (
    EXTERNAL_RESOURCE_LAYOUT, IntegrityError, raw_sha256, unique_object_hook,
    validate_lock,
)


SCHEMA = "se-harness-resources-v1"
TEMPLATE_PREFIX = "templates/repository/standard/"
ENTRY = "ENGINEERING_HARNESS.md"
CONFIG = ".engineering-harness.toml"
LOCK = ".engineering-harness.lock"


class ResourceError(IntegrityError):
    """A selected resource cannot be returned safely."""


def _safe_path(path: Path) -> Path:
    """Check before resolving, including Windows junctions and linked parents."""
    path = path.absolute()
    for item in (path, *path.parents):
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ResourceError(f"resource input is linked: {item}")
    return path


def _read(path: Path, *, limit: int = 16 * 1024 * 1024) -> bytes:
    try:
        path = _safe_path(path)
        if not path.is_file() or path.stat().st_size > limit:
            raise ResourceError(f"resource input is missing or oversized: {path}")
        raw = path.read_bytes()
        if len(raw) > limit:
            raise ResourceError(f"resource input is oversized: {path}")
        return raw
    except OSError as exc:
        raise ResourceError(f"cannot read resource input: {path}") from exc


def _lock(raw: bytes) -> dict[str, Any]:
    try:
        value = json.loads(raw, object_pairs_hook=unique_object_hook(
            lambda key: ResourceError(f"repeated selection field: {key}")))
        return validate_lock(value)
    except (ValueError, UnicodeError) as exc:
        raise ResourceError(f"invalid resource selection: {exc}") from exc


def uses_external_resources(repository: Path) -> bool:
    """Identify the layout, refusing malformed existing selection records."""
    config_path = _safe_path(repository / CONFIG)
    layout = None
    if config_path.exists():
        try:
            harness = tomllib.loads(_read(config_path).decode("utf-8-sig")).get("harness", {})
            layout = harness.get("resource_layout") if isinstance(harness, dict) else None
        except (ValueError, UnicodeError) as exc:
            raise ResourceError("invalid resource configuration") from exc
    path = _safe_path(repository / LOCK)
    if not path.exists():
        if layout is not None:
            raise ResourceError("external resource selection is missing its lock")
        return False
    selected_layout = _lock(_read(path)).get("resource_layout")
    if layout != selected_layout:
        raise ResourceError("configuration and lock resource layouts differ")
    return selected_layout == EXTERNAL_RESOURCE_LAYOUT


def _installed_resource_root() -> Path:
    # Deliberately no source-tree, cwd, plugin or adjacent-checkout fallback.
    prefix = Path(sys.prefix).absolute()
    module = _safe_path(Path(__file__))
    root = _safe_path(Path(sysconfig.get_path("data")) / "share/se-harness/templates/repository/standard")
    if not module.is_relative_to(prefix) or not root.is_relative_to(prefix) or not root.is_dir():
        raise ResourceError("external resources require an installed evaluator wheel outside the checkout")
    return root


def _resource_id(member: str) -> str | None:
    if not member.startswith(TEMPLATE_PREFIX):
        return None
    relative = member.removeprefix(TEMPLATE_PREFIX)
    if relative == ENTRY + ".tpl":
        return ENTRY
    if relative in {"docs/engineering/ARTIFACT_AUTHORING.md", "docs/engineering/WORKFLOW.json", "docs/engineering/QUALITY_GATES.json"}:
        return relative
    if relative.startswith(("docs/engineering/harness/", "docs/engineering/templates/")):
        return relative
    return None


class ResourceSet:
    """A validated selection snapshot, rechecked before returning bytes or writes."""

    def __init__(self, repository: Path):
        self.repository = _safe_path(repository)
        self._inputs = {name: _read(self.repository / name) for name in (CONFIG, LOCK)}
        self.lock = _lock(self._inputs[LOCK])
        if self.lock.get("resource_layout") != EXTERNAL_RESOURCE_LAYOUT:
            raise ResourceError("selected layout uses repository copies; use its installed instructions")
        try:
            self.config = tomllib.loads(self._inputs[CONFIG].decode("utf-8-sig"))
        except (ValueError, UnicodeError) as exc:
            raise ResourceError("invalid resource configuration") from exc
        harness = self.config.get("harness", {})
        if not isinstance(harness, dict) or harness.get("tool_version") != self.lock["tool_version"] or self.lock["tool_version"] != __version__:
            raise ResourceError("configuration, lock and running evaluator versions differ")
        if harness.get("resource_layout") != EXTERNAL_RESOURCE_LAYOUT:
            raise ResourceError("configuration and lock resource layouts differ")
        self.root = _installed_resource_root()
        if self.root.is_relative_to(self.repository) or Path(__file__).absolute().is_relative_to(self.repository):
            raise ResourceError("released resources must be outside the selected checkout")
        self.release = dict(self.lock["evaluator"])
        self._manifest = self._payload()
        self._verify_identity()
        self.members = {}
        for member in json.loads(self._manifest)["files"]:
            identifier = _resource_id(member["path"])
            if identifier is not None:
                path = self.root / member["path"].removeprefix(TEMPLATE_PREFIX)
                raw = _read(path)
                if len(raw) != member["bytes"] or raw_sha256(raw) != member["sha256"]:
                    raise ResourceError(f"resource differs from selected payload: {identifier}")
                self.members[identifier] = {**member, "local_path": path}
        from se_harness.artifact_layout import ARTIFACT_TEMPLATES
        required = {ENTRY, "docs/engineering/ARTIFACT_AUTHORING.md", "docs/engineering/WORKFLOW.json", "docs/engineering/QUALITY_GATES.json"}
        required.update("docs/engineering/templates/" + name for name in ARTIFACT_TEMPLATES.values())
        missing = required - self.members.keys()
        if missing:
            raise ResourceError(f"required resource is absent: {sorted(missing)[0]}")
        from se_harness.instruction_discovery import validate_collection
        validate_collection({key: _read(item["local_path"]) for key, item in self.members.items()})
        self.assert_current()

    def _verify_identity(self) -> None:
        try:
            observed = installed_evaluator_identity().to_lock()
        except EvaluatorIdentityError as exc:
            raise ResourceError(f"selected evaluator identity is unavailable: {exc}") from exc
        for field in ("version", "payload_manifest", "payload_sha256", "archive_name", "archive_sha256"):
            expected = self.release.get(field)
            if expected is not None and observed.get(field) != expected:
                raise ResourceError(f"selected evaluator {field} does not match installed resources")
        if raw_sha256(self._manifest) != self.release["payload_sha256"]:
            raise ResourceError("resource manifest does not match the selected payload")

    @staticmethod
    def _payload() -> bytes:
        try:
            return canonical_payload_manifest()
        except EvaluatorIdentityError as exc:
            raise ResourceError(f"selected payload is unavailable: {exc}") from exc

    def assert_current(self) -> None:
        for name, raw in self._inputs.items():
            if _read(self.repository / name) != raw:
                raise ResourceError(f"resource selection changed during the operation: {name}")
        if self._payload() != self._manifest:
            raise ResourceError("selected evaluator resources changed during the operation")

    def _path(self, identifier: str) -> Path:
        if (not isinstance(identifier, str) or "\\" in identifier or ":" in identifier
                or identifier.startswith("/") or any(part in {"", ".", ".."} for part in identifier.split("/"))
                or PurePosixPath(identifier).as_posix() != identifier):
            raise ResourceError("resource ID must be a normalized relative path")
        if identifier not in self.members:
            raise ResourceError(f"unknown selected resource: {identifier}")
        return self.members[identifier]["local_path"]

    def path(self, identifier: str) -> Path:
        path = self._path(identifier)
        self._read_member(identifier)
        self.assert_current()
        return path

    def _read_member(self, identifier: str) -> bytes:
        raw = _read(self._path(identifier))
        if raw_sha256(raw) != self.members[identifier]["sha256"]:
            raise ResourceError(f"selected resource changed: {identifier}")
        return raw

    def read(self, identifier: str) -> bytes:
        raw = self._read_member(identifier)
        self.assert_current()
        return raw

    def _describe(self, identifier: str) -> dict[str, Any]:
        raw = self._read_member(identifier)
        return {"resource": identifier, "path": str(self._path(identifier)),
                "sha256": raw_sha256(raw), "bytes": len(raw),
                "headings": [re.sub(r"[^\w\- ]", "", value.strip().lower()).replace(" ", "-")
                             for value in re.findall(r"^#{1,6} (.+)$", raw.decode("utf-8"), re.M)]}

    def query(self, identifier: str | None = None, *, content: bool = False) -> dict[str, Any]:
        if content and identifier is None:
            raise ResourceError("--content requires one --resource; bulk instruction injection is unsupported")
        result = {"schema": SCHEMA, "resource_layout": EXTERNAL_RESOURCE_LAYOUT,
                  "release": self.release, "resources": [self._describe(key) for key in ([identifier] if identifier is not None else sorted(self.members))]}
        if content:
            text = self._read_member(identifier).decode("utf-8")
            if identifier == ENTRY:
                project = self.config["harness"].get("project_name", self.repository.name)
                if not isinstance(project, str) or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._ -]{0,127}", project) is None:
                    raise ResourceError("project name must use 1-128 safe letters, numbers, spaces, dots, underscores or hyphens")
                text = text.replace("{{PROJECT_NAME}}", project).replace("{{HARNESS_VERSION}}", __version__)
            result["content"] = text
            result["content_sha256"] = raw_sha256(text.encode("utf-8"))
        self.assert_current()
        return result
