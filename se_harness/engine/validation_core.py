"""The validator's core (SPEC-ECP-024 ECP-ENG-017): the artifact and diagnostic types, the loaders and the helpers every seam shares.
"""

from __future__ import annotations

import tomllib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from se_harness.artifact_layout import ARTIFACT_PREFIXES
from se_harness.codes import E001, E002


TAXONOMY_VERSION = "se-harness-validation-taxonomy-v1"


VALIDATION_PLANES = ("structure", "governance", "policy", "maintenance")


TYPE_PREFIX = dict(ARTIFACT_PREFIXES)


ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


EXCLUDED_DIRECTORY_NAMES = {"templates", "evidence", ".git", ".idea", "target", "node_modules"}


@dataclass(frozen=True, order=True)
class Diagnostic:
    path: str
    code: str
    message: str
    plane: str

    def __post_init__(self) -> None:
        if self.plane not in VALIDATION_PLANES:
            raise ValueError(f"unknown validation plane: {self.plane!r}")


@dataclass
class Artifact:
    path: Path
    metadata: dict[str, Any]
    body: str

    @property
    def artifact_id(self) -> str:
        value = self.metadata.get("id")
        return value if isinstance(value, str) else "<unknown>"

    @property
    def artifact_type(self) -> str:
        value = self.metadata.get("type")
        return value if isinstance(value, str) else "<unknown>"

    @property
    def status(self) -> str:
        value = self.metadata.get("status")
        return value if isinstance(value, str) else "<unknown>"

    @property
    def relations(self) -> dict[str, Any]:
        value = self.metadata.get("relations", {})
        return value if isinstance(value, dict) else {}


def load_revision_policy(repository_root: Path) -> dict[str, bool]:
    defaults = {"required_for_verified_work": False, "required_for_release": False}
    path = repository_root / ".engineering-harness.toml"
    if not path.is_file():
        return defaults
    try:
        metadata = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return defaults
    policy = metadata.get("revision_provenance", {})
    if not isinstance(policy, dict):
        return defaults
    return {
        key: value if isinstance((value := policy.get(key)), bool) else default
        for key, default in defaults.items()
    }


def display_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _is_excluded(path: Path, artifact_root: Path) -> bool:
    try:
        relative_parts = path.relative_to(artifact_root).parts
    except ValueError:
        relative_parts = path.parts
    return any(part in EXCLUDED_DIRECTORY_NAMES for part in relative_parts[:-1])


def discover_candidate_files(artifact_root: Path) -> list[Path]:
    if not artifact_root.exists():
        return []
    return sorted(
        path
        for path in artifact_root.rglob("*.md")
        if path.is_file() and not _is_excluded(path, artifact_root)
    )


def parse_formal_artifact(path: Path, report_root: Path) -> tuple[Artifact | None, Diagnostic | None]:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return None, Diagnostic(display_path(path, report_root), E001, f"cannot read artifact: {exc}", "structure")

    if not text.startswith("+++\n") and text != "+++":
        return None, None

    lines = text.splitlines()
    try:
        closing_index = lines.index("+++", 1)
    except ValueError:
        return None, Diagnostic(
            display_path(path, report_root),
            E001,
            "formal artifact starts TOML front matter but has no closing +++ delimiter",
            "structure",
        )

    front_matter_text = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :]).lstrip("\n")

    try:
        metadata = tomllib.loads(front_matter_text)
    except tomllib.TOMLDecodeError as exc:
        return None, Diagnostic(
            display_path(path, report_root),
            E001,
            f"invalid TOML front matter: {exc}",
            "structure",
        )

    if not isinstance(metadata, dict):
        return None, Diagnostic(
            display_path(path, report_root),
            E001,
            "front matter must be a TOML table",
            "structure",
        )

    return Artifact(path=path, metadata=metadata, body=body), None


def load_artifacts(artifact_root: Path, report_root: Path) -> tuple[list[Artifact], list[Diagnostic]]:
    artifacts: list[Artifact] = []
    errors: list[Diagnostic] = []
    for path in discover_candidate_files(artifact_root):
        artifact, error = parse_formal_artifact(path, report_root)
        if error is not None:
            errors.append(error)
        elif artifact is not None:
            artifacts.append(artifact)
    return artifacts, errors


def add_error(
    errors: list[Diagnostic],
    artifact: Artifact,
    report_root: Path,
    code: str,
    message: str,
    *,
    plane: str,
) -> None:
    errors.append(Diagnostic(display_path(artifact.path, report_root), code, message, plane))


def require_non_empty_string(
    artifact: Artifact,
    field: str,
    errors: list[Diagnostic],
    report_root: Path,
    *,
    plane: str = "structure",
) -> str | None:
    value = artifact.metadata.get(field)
    if not isinstance(value, str) or not value.strip():
        add_error(
            errors,
            artifact,
            report_root,
            E002,
            f"field '{field}' must be a non-empty string",
            plane=plane,
        )
        return None
    return value.strip()


def require_non_empty_string_list(
    artifact: Artifact,
    field: str,
    errors: list[Diagnostic],
    report_root: Path,
    *,
    code: str = E002,
    container: dict[str, Any] | None = None,
    plane: str = "structure",
) -> list[str] | None:
    source = artifact.metadata if container is None else container
    value = source.get(field)
    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item.strip() for item in value):
        add_error(
            errors,
            artifact,
            report_root,
            code,
            f"field '{field}' must be a non-empty array of strings",
            plane=plane,
        )
        return None
    return [item.strip() for item in value]


def relation_targets(artifact: Artifact, relation_name: str) -> set[str]:
    value = artifact.relations.get(relation_name, [])
    if not isinstance(value, list):
        return set()
    return {item for item in value if isinstance(item, str)}


def duplicate_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    strings = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in strings:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return sorted(duplicates)
