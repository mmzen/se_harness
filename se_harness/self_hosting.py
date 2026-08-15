"""Repository-specific governor descriptor for developing se-harness itself."""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

from se_harness.installer import HarnessError, ensure_target, safe_destination
from se_harness.self_hosting_policy import DESCRIPTOR_PATH, classify_self_hosting


VERSION_PATTERN = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?")
RECORD_PATTERN = re.compile(r"RLS-[A-Z][A-Z0-9-]*-\d{3}")


@dataclass(frozen=True)
class GovernorDescriptor:
    version: str
    tag: str
    wheel: str
    url: str
    sha256: str
    selected_release_record: str
    selected_candidate_commit: str


def self_hosting_enabled(target: Path) -> bool:
    ensure_target(target, must_exist=True)
    return classify_self_hosting(target).enabled


def load_governor_descriptor(target: Path) -> GovernorDescriptor:
    root = ensure_target(target, must_exist=True)
    path = safe_destination(root, DESCRIPTOR_PATH)
    try:
        value = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise HarnessError(f"cannot read self-hosting governor descriptor: {exc}") from exc
    if value.get("schema") != 1:
        raise HarnessError("unsupported self-hosting governor descriptor schema")
    fields = {
        key: value.get(key)
        for key in (
            "version",
            "tag",
            "wheel",
            "url",
            "sha256",
            "selected_release_record",
            "selected_candidate_commit",
        )
    }
    if any(not isinstance(item, str) or not item for item in fields.values()):
        raise HarnessError("self-hosting governor descriptor fields must be non-empty strings")
    descriptor = GovernorDescriptor(**fields)  # type: ignore[arg-type]
    expected_wheel = f"se_harness-{descriptor.version}-py3-none-any.whl"
    expected_url = (
        "https://github.com/mmzen/se_harness/releases/download/"
        f"{descriptor.tag}/{descriptor.wheel}"
    )
    if VERSION_PATTERN.fullmatch(descriptor.version) is None:
        raise HarnessError("invalid self-hosting governor version")
    if descriptor.tag != f"v{descriptor.version}":
        raise HarnessError("self-hosting governor tag does not match its version")
    if descriptor.wheel != expected_wheel:
        raise HarnessError("self-hosting governor wheel does not match its version")
    if descriptor.url != expected_url:
        raise HarnessError("self-hosting governor URL is not the immutable release asset URL")
    if SHA256_PATTERN.fullmatch(descriptor.sha256) is None:
        raise HarnessError("invalid self-hosting governor SHA-256")
    if RECORD_PATTERN.fullmatch(descriptor.selected_release_record) is None:
        raise HarnessError("invalid selected governor release record")
    if COMMIT_PATTERN.fullmatch(descriptor.selected_candidate_commit) is None:
        raise HarnessError("invalid selected governor candidate commit")
    return descriptor
