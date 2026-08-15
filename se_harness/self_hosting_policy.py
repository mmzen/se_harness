"""Dependency-light classification for the se-harness implementation checkout."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CONFIG_PATH = Path(".engineering-harness.toml")
DESCRIPTOR_PATH = Path(".self-hosting/governor.toml")
WORKFLOW_PATH = Path(".github/workflows/engineering-harness.yml")
SELF_HOSTING_ROLE = "implementation-repository"
PROTECTED_CONTROL_PATHS = frozenset(
    {
        CONFIG_PATH.as_posix(),
        WORKFLOW_PATH.as_posix(),
    }
)


@dataclass(frozen=True)
class SelfHostingClassification:
    """One fail-closed repository-role decision."""

    kind: str
    detail: str
    config: dict[str, Any] | None = None

    @property
    def enabled(self) -> bool:
        return self.kind == "self-hosting"


def _toml(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.is_file():
        return None, None
    try:
        value = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        return None, str(exc)
    return value, None


def classify_self_hosting(target: Path) -> SelfHostingClassification:
    """Classify consumer, exact implementation repository, or ambiguity.

    Repository content is untrusted. A partial self-hosting signal therefore
    blocks upgrade instead of silently falling back to consumer behavior.
    """

    root = target.expanduser().resolve()
    config, config_error = _toml(root / CONFIG_PATH)
    project, project_error = _toml(root / "pyproject.toml")
    package_signal = (root / "se_harness" / "__init__.py").is_file()
    descriptor_signal = (root / DESCRIPTOR_PATH).exists()
    project_section = project.get("project") if isinstance(project, dict) else None
    project_signal = (
        isinstance(project_section, dict)
        and project_section.get("name") == "se-harness"
        and package_signal
    )
    self_hosting_section = config.get("self_hosting") if isinstance(config, dict) else None
    declaration_signal = self_hosting_section is not None
    any_signal = declaration_signal or descriptor_signal or project_signal

    if config_error is not None:
        return SelfHostingClassification("ambiguous", f"invalid {CONFIG_PATH.as_posix()}: {config_error}")
    if project_error is not None and (declaration_signal or descriptor_signal or package_signal):
        return SelfHostingClassification("ambiguous", f"invalid pyproject.toml: {project_error}", config)
    if not any_signal:
        return SelfHostingClassification("consumer", "no self-hosting signal", config)
    if not isinstance(self_hosting_section, dict):
        return SelfHostingClassification("ambiguous", "self-hosting signals exist without a complete declaration", config)
    if self_hosting_section.get("role") != SELF_HOSTING_ROLE:
        return SelfHostingClassification("ambiguous", "unsupported or missing self-hosting role", config)
    if self_hosting_section.get("governor_descriptor") != DESCRIPTOR_PATH.as_posix():
        return SelfHostingClassification("ambiguous", "self-hosting governor descriptor path is not exact", config)
    if not project_signal:
        return SelfHostingClassification("ambiguous", "self-hosting project identity or source layout is incomplete", config)
    if not (root / DESCRIPTOR_PATH).is_file():
        return SelfHostingClassification("ambiguous", "self-hosting governor descriptor is missing", config)
    if not (root / WORKFLOW_PATH).is_file():
        return SelfHostingClassification("ambiguous", "self-hosting workflow is missing", config)
    return SelfHostingClassification("self-hosting", "exact implementation repository", config)
