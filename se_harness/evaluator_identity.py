"""Canonical identity for one installed SE Harness evaluator payload."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import re
import sysconfig
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from se_harness import __version__


PAYLOAD_MANIFEST = "se-harness-installed-payload-v1"
MAX_FILE_BYTES = 16 * 1024 * 1024
MAX_FILE_COUNT = 4096
MAX_PAYLOAD_BYTES = 128 * 1024 * 1024
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
WHEEL_PATTERN = re.compile(r"se_harness-(?P<version>[A-Za-z0-9_.!+]+)-py3-none-any\.whl")


class EvaluatorIdentityError(ValueError):
    """The installed evaluator payload cannot be identified safely."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise EvaluatorIdentityError(f"installed evaluator PEP 610 metadata repeats field: {key}")
        value[key] = item
    return value


@dataclass(frozen=True)
class InstalledEvaluatorIdentity:
    version: str
    payload_manifest: str
    payload_sha256: str
    archive_name: str | None = None
    archive_sha256: str | None = None

    def to_lock(self) -> dict[str, str]:
        value = {
            "version": self.version,
            "payload_manifest": self.payload_manifest,
            "payload_sha256": self.payload_sha256,
        }
        if self.archive_name is not None and self.archive_sha256 is not None:
            value["archive_name"] = self.archive_name
            value["archive_sha256"] = self.archive_sha256
        return value


def expected_wheel_name(version: str) -> str:
    return f"se_harness-{version.replace('-', '_')}-py3-none-any.whl"


def validate_wheel_name(name: str, version: str) -> bool:
    return WHEEL_PATTERN.fullmatch(name) is not None and name == expected_wheel_name(version)


def _template_root() -> Path:
    package_parent = Path(__file__).resolve().parent.parent
    candidates = (
        package_parent / "templates" / "repository" / "standard",
        Path(sysconfig.get_path("data"))
        / "share"
        / "se-harness"
        / "templates"
        / "repository"
        / "standard",
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()
    raise EvaluatorIdentityError("the standard evaluator templates could not be located")


def _payload_files() -> list[tuple[str, Path]]:
    roots = (
        ("se_harness", Path(__file__).resolve().parent),
        ("templates/repository/standard", _template_root()),
    )
    files: list[tuple[str, Path]] = []
    for prefix, root in roots:
        for path in root.rglob("*"):
            if path.is_symlink():
                raise EvaluatorIdentityError("the installed evaluator payload contains a symlink")
            if (
                not path.is_file()
                or "__pycache__" in path.parts
                or path.suffix.lower() in {".pyc", ".pyo"}
            ):
                continue
            relative = path.relative_to(root).as_posix()
            files.append((f"{prefix}/{relative}", path))
    files.sort(key=lambda item: item[0])
    if not files or len(files) > MAX_FILE_COUNT:
        raise EvaluatorIdentityError("the installed evaluator payload has an invalid file count")
    return files


def canonical_payload_manifest() -> bytes:
    entries: list[dict[str, Any]] = []
    total = 0
    for relative, path in sorted(_payload_files(), key=lambda item: item[0]):
        try:
            content = path.read_bytes()
        except OSError as exc:
            raise EvaluatorIdentityError(f"cannot read installed evaluator payload member: {relative}") from exc
        if len(content) > MAX_FILE_BYTES:
            raise EvaluatorIdentityError(f"installed evaluator payload member is too large: {relative}")
        total += len(content)
        if total > MAX_PAYLOAD_BYTES:
            raise EvaluatorIdentityError("the installed evaluator payload exceeds the byte limit")
        entries.append(
            {
                "bytes": len(content),
                "path": relative,
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    value = {"files": entries, "schema": PAYLOAD_MANIFEST}
    return (json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")


def installed_payload_sha256() -> str:
    return hashlib.sha256(canonical_payload_manifest()).hexdigest()


def _direct_url_archive() -> tuple[str, str] | None:
    try:
        distribution = importlib.metadata.distribution("se-harness")
    except importlib.metadata.PackageNotFoundError:
        return None
    distribution_root = Path(distribution.locate_file("")).resolve()
    try:
        Path(__file__).resolve().relative_to(distribution_root)
    except ValueError:
        return None
    raw = distribution.read_text("direct_url.json")
    if raw is None:
        return None
    try:
        value = json.loads(raw, object_pairs_hook=_unique_object)
    except json.JSONDecodeError as exc:
        raise EvaluatorIdentityError("installed evaluator has malformed PEP 610 metadata") from exc
    if not isinstance(value, dict) or "archive_info" not in value:
        return None
    archive = value.get("archive_info")
    url = value.get("url")
    if not isinstance(archive, dict) or not isinstance(url, str):
        raise EvaluatorIdentityError("installed evaluator has invalid PEP 610 archive metadata")
    hashes = archive.get("hashes")
    digest = hashes.get("sha256") if isinstance(hashes, dict) else None
    legacy_hash = archive.get("hash")
    legacy_digest = (
        legacy_hash.removeprefix("sha256=")
        if isinstance(legacy_hash, str) and legacy_hash.startswith("sha256=")
        else None
    )
    if digest is not None and legacy_digest is not None and digest != legacy_digest:
        raise EvaluatorIdentityError("installed evaluator PEP 610 SHA-256 values disagree")
    if digest is None:
        digest = legacy_digest
    if not isinstance(digest, str) or SHA256_PATTERN.fullmatch(digest) is None:
        raise EvaluatorIdentityError("installed evaluator PEP 610 metadata has no valid SHA-256")
    parsed = urlparse(url)
    name = Path(unquote(parsed.path)).name
    if not validate_wheel_name(name, __version__):
        raise EvaluatorIdentityError("installed evaluator PEP 610 wheel name is inconsistent with its version")
    return name, digest


def installed_evaluator_identity() -> InstalledEvaluatorIdentity:
    archive = _direct_url_archive()
    return InstalledEvaluatorIdentity(
        version=__version__,
        payload_manifest=PAYLOAD_MANIFEST,
        payload_sha256=installed_payload_sha256(),
        archive_name=archive[0] if archive is not None else None,
        archive_sha256=archive[1] if archive is not None else None,
    )
