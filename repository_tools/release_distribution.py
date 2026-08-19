"""Repository-owned SE Harness distribution provenance and binding policy."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


BUNDLE_SCHEMA = "se-harness-release-bundle/v1"
DISTRIBUTION_SCHEMA = 1
DISTRIBUTION_KIND = "python-wheel-sdist"
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,63}")
COMMIT_PATTERNS = {
    "sha1": re.compile(r"[0-9a-f]{40}"),
    "sha256": re.compile(r"[0-9a-f]{64}"),
}
SAFE_BASENAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,199}")
BUNDLE_KEYS = frozenset(
    {
        "schema", "version", "commit", "git_object_format", "source_date_epoch",
        "wheel", "wheel_sha256", "sdist", "sdist_sha256", "checksums",
        "checksums_sha256", "checksums_content", "source_manifest_sha256",
    }
)
DISTRIBUTION_KEYS = frozenset(
    {
        "schema", "kind", "source_date_epoch", "wheel", "wheel_sha256", "sdist",
        "sdist_sha256", "checksums", "checksums_sha256", "source_manifest_sha256",
    }
)


class ReleaseDistributionError(RuntimeError):
    """Repository distribution input violates the SE Harness release policy."""


@dataclass(frozen=True)
class ReleaseDistribution:
    source_date_epoch: int
    wheel: str
    wheel_sha256: str
    sdist: str
    sdist_sha256: str
    checksums: str
    checksums_sha256: str
    source_manifest_sha256: str

    def as_metadata(self) -> dict[str, Any]:
        return {
            "schema": DISTRIBUTION_SCHEMA,
            "kind": DISTRIBUTION_KIND,
            "source_date_epoch": self.source_date_epoch,
            "wheel": self.wheel,
            "wheel_sha256": self.wheel_sha256,
            "sdist": self.sdist,
            "sdist_sha256": self.sdist_sha256,
            "checksums": self.checksums,
            "checksums_sha256": self.checksums_sha256,
            "source_manifest_sha256": self.source_manifest_sha256,
        }

    def toml(self, newline: str = "\n") -> str:
        values = self.as_metadata()
        return newline.join(
            [
                "[distribution]",
                f'schema = {values["schema"]}',
                f'kind = "{values["kind"]}"',
                f'source_date_epoch = {values["source_date_epoch"]}',
                f'wheel = "{values["wheel"]}"',
                f'wheel_sha256 = "{values["wheel_sha256"]}"',
                f'sdist = "{values["sdist"]}"',
                f'sdist_sha256 = "{values["sdist_sha256"]}"',
                f'checksums = "{values["checksums"]}"',
                f'checksums_sha256 = "{values["checksums_sha256"]}"',
                f'source_manifest_sha256 = "{values["source_manifest_sha256"]}"',
            ]
        )


def checksum_manifest_bytes(version: str, wheel_sha256: str, sdist_sha256: str) -> bytes:
    wheel, sdist = expected_distribution_names(version)
    return f"{wheel_sha256}  {wheel}\n{sdist_sha256}  {sdist}\n".encode("utf-8")


def expected_distribution_names(version: str) -> tuple[str, str]:
    if not isinstance(version, str) or VERSION_PATTERN.fullmatch(version) is None:
        raise ReleaseDistributionError("version contains unsupported characters")
    return f"se_harness-{version}-py3-none-any.whl", f"se_harness-{version}.tar.gz"


def _duplicate_safe_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReleaseDistributionError(f"distribution manifest contains duplicate key: {key}")
        result[key] = value
    return result


def _sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_PATTERN.fullmatch(value) is None:
        raise ReleaseDistributionError(f"{label} must be 64 lowercase hexadecimal characters")
    return value


def _safe_basename(value: Any, label: str) -> str:
    if not isinstance(value, str) or SAFE_BASENAME_PATTERN.fullmatch(value) is None:
        raise ReleaseDistributionError(f"{label} must be a safe ASCII basename")
    if Path(value).name != value or value in {".", ".."}:
        raise ReleaseDistributionError(f"{label} must be a safe basename")
    return value


def validate_distribution_block(value: Any, version: str) -> ReleaseDistribution:
    if not isinstance(value, dict):
        raise ReleaseDistributionError("distribution must be a TOML table")
    keys = set(value)
    if keys != DISTRIBUTION_KEYS:
        missing = sorted(DISTRIBUTION_KEYS - keys)
        extra = sorted(keys - DISTRIBUTION_KEYS)
        detail = []
        if missing:
            detail.append(f"missing {', '.join(missing)}")
        if extra:
            detail.append(f"unexpected {', '.join(extra)}")
        raise ReleaseDistributionError(f"distribution block must be complete ({'; '.join(detail)})")
    if value.get("schema") != DISTRIBUTION_SCHEMA:
        raise ReleaseDistributionError("distribution schema must be 1")
    if value.get("kind") != DISTRIBUTION_KIND:
        raise ReleaseDistributionError(f"distribution kind must be {DISTRIBUTION_KIND}")
    epoch = value.get("source_date_epoch")
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 1:
        raise ReleaseDistributionError("distribution source_date_epoch must be a positive integer")
    wheel = _safe_basename(value.get("wheel"), "distribution wheel")
    sdist = _safe_basename(value.get("sdist"), "distribution sdist")
    checksums = _safe_basename(value.get("checksums"), "distribution checksums")
    expected_wheel, expected_sdist = expected_distribution_names(version)
    if wheel != expected_wheel or sdist != expected_sdist:
        raise ReleaseDistributionError("distribution filenames do not match the release version")
    if checksums != "SHA256SUMS":
        raise ReleaseDistributionError("distribution checksums filename must be SHA256SUMS")
    wheel_hash = _sha256(value.get("wheel_sha256"), "distribution wheel_sha256")
    sdist_hash = _sha256(value.get("sdist_sha256"), "distribution sdist_sha256")
    checksums_hash = _sha256(value.get("checksums_sha256"), "distribution checksums_sha256")
    expected_checksums_hash = hashlib.sha256(
        checksum_manifest_bytes(version, wheel_hash, sdist_hash)
    ).hexdigest()
    if checksums_hash != expected_checksums_hash:
        raise ReleaseDistributionError(
            "distribution checksums_sha256 does not identify canonical SHA256SUMS bytes"
        )
    return ReleaseDistribution(
        source_date_epoch=epoch,
        wheel=wheel,
        wheel_sha256=wheel_hash,
        sdist=sdist,
        sdist_sha256=sdist_hash,
        checksums=checksums,
        checksums_sha256=checksums_hash,
        source_manifest_sha256=_sha256(
            value.get("source_manifest_sha256"), "distribution source_manifest_sha256"
        ),
    )


def read_bundle_manifest(
    path: Path,
    *,
    version: str,
    commit: str,
    git_object_format: str,
    source_date_epoch: int,
) -> ReleaseDistribution:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise ReleaseDistributionError(f"cannot read distribution manifest: {path}") from exc
    if len(payload) > 128 * 1024:
        raise ReleaseDistributionError("distribution manifest is too large")
    try:
        value = json.loads(payload.decode("utf-8"), object_pairs_hook=_duplicate_safe_object)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ReleaseDistributionError("distribution manifest must be valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise ReleaseDistributionError("distribution manifest must be a JSON object")
    keys = set(value)
    if keys != BUNDLE_KEYS:
        missing = sorted(BUNDLE_KEYS - keys)
        extra = sorted(keys - BUNDLE_KEYS)
        detail = []
        if missing:
            detail.append(f"missing {', '.join(missing)}")
        if extra:
            detail.append(f"unexpected {', '.join(extra)}")
        raise ReleaseDistributionError(
            f"distribution manifest fields are invalid ({'; '.join(detail)})"
        )
    if value.get("schema") != BUNDLE_SCHEMA:
        raise ReleaseDistributionError(f"distribution manifest schema must be {BUNDLE_SCHEMA}")
    if value.get("version") != version:
        raise ReleaseDistributionError("distribution manifest version does not match the release")
    if value.get("git_object_format") != git_object_format:
        raise ReleaseDistributionError(
            "distribution manifest Git object format does not match the candidate"
        )
    commit_pattern = COMMIT_PATTERNS.get(git_object_format)
    manifest_commit = value.get("commit")
    if (
        commit_pattern is None
        or not isinstance(manifest_commit, str)
        or commit_pattern.fullmatch(manifest_commit) is None
        or manifest_commit != commit
    ):
        raise ReleaseDistributionError("distribution manifest commit does not match the candidate")
    if value.get("source_date_epoch") != source_date_epoch:
        raise ReleaseDistributionError("distribution manifest epoch does not match the candidate commit")
    metadata = {
        "schema": DISTRIBUTION_SCHEMA,
        "kind": DISTRIBUTION_KIND,
        "source_date_epoch": value.get("source_date_epoch"),
        "wheel": value.get("wheel"),
        "wheel_sha256": value.get("wheel_sha256"),
        "sdist": value.get("sdist"),
        "sdist_sha256": value.get("sdist_sha256"),
        "checksums": value.get("checksums"),
        "checksums_sha256": value.get("checksums_sha256"),
        "source_manifest_sha256": value.get("source_manifest_sha256"),
    }
    distribution = validate_distribution_block(metadata, version)
    expected_content = checksum_manifest_bytes(
        version, distribution.wheel_sha256, distribution.sdist_sha256
    ).decode("utf-8")
    if value.get("checksums_content") != expected_content:
        raise ReleaseDistributionError("distribution manifest checksums_content is not canonical")
    return distribution


def _run_git(repository: Path, *arguments: str, binary: bool = False) -> str | bytes:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=False,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ReleaseDistributionError("Git command failed to start") from exc
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", "replace").strip() or "Git command failed"
        raise ReleaseDistributionError(detail)
    return completed.stdout if binary else completed.stdout.decode("utf-8", "strict").strip()


def source_manifest_sha256(repository: Path, commit: str) -> str:
    payload = _run_git(repository, "ls-tree", "-r", "-z", "--full-tree", commit, binary=True)
    assert isinstance(payload, bytes)
    if not payload:
        raise ReleaseDistributionError("candidate source manifest is empty")
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ReleaseDistributionError(f"cannot read distribution: {path}") from exc
    return digest.hexdigest()


def create_manifest(
    repository: Path,
    commit: str,
    version: str,
    wheel: Path,
    sdist: Path,
) -> dict[str, object]:
    repository = repository.resolve()
    expected_wheel, expected_sdist = expected_distribution_names(version)
    object_format = str(_run_git(repository, "rev-parse", "--show-object-format"))
    commit_pattern = COMMIT_PATTERNS.get(object_format)
    if commit_pattern is None:
        raise ReleaseDistributionError("unsupported Git object format")
    candidate = str(_run_git(repository, "rev-parse", "--verify", f"{commit}^{{commit}}")).lower()
    if commit_pattern.fullmatch(candidate) is None or commit.lower() != candidate:
        raise ReleaseDistributionError("candidate commit must be supplied as a full exact object ID")
    if wheel.name != expected_wheel or sdist.name != expected_sdist:
        raise ReleaseDistributionError("distribution filenames do not match the release version")
    if not wheel.is_file() or wheel.is_symlink() or not sdist.is_file() or sdist.is_symlink():
        raise ReleaseDistributionError("wheel and sdist must be ordinary files")
    wheel_hash = _sha256_file(wheel)
    sdist_hash = _sha256_file(sdist)
    checksums_content = checksum_manifest_bytes(version, wheel_hash, sdist_hash).decode("utf-8")
    epoch = str(_run_git(repository, "show", "-s", "--format=%ct", candidate))
    if not epoch.isdigit() or int(epoch) < 1:
        raise ReleaseDistributionError("candidate commit timestamp is invalid")
    return {
        "schema": BUNDLE_SCHEMA,
        "version": version,
        "commit": candidate,
        "git_object_format": object_format,
        "source_date_epoch": int(epoch),
        "wheel": expected_wheel,
        "wheel_sha256": wheel_hash,
        "sdist": expected_sdist,
        "sdist_sha256": sdist_hash,
        "checksums": "SHA256SUMS",
        "checksums_sha256": hashlib.sha256(checksums_content.encode("utf-8")).hexdigest(),
        "checksums_content": checksums_content,
        "source_manifest_sha256": source_manifest_sha256(repository, candidate),
    }


def _safe_repository_file(repository: Path, supplied: Path, label: str) -> Path:
    if supplied.is_absolute() or ".." in supplied.parts:
        raise ReleaseDistributionError(f"{label} must be repository-relative")
    candidate = repository / supplied
    if candidate.is_symlink():
        raise ReleaseDistributionError(f"{label} must not be a symbolic link")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(repository)
    except (OSError, ValueError) as exc:
        raise ReleaseDistributionError(f"{label} must resolve inside the repository") from exc
    if not resolved.is_file():
        raise ReleaseDistributionError(f"{label} must be an ordinary file")
    return resolved


def read_release_record(path: Path) -> tuple[dict[str, Any], str, list[str], int]:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise ReleaseDistributionError(f"cannot read release record: {path}") from exc
    if len(payload) > 1024 * 1024:
        raise ReleaseDistributionError("release record is too large")
    if payload.startswith(b"\xef\xbb\xbf"):
        raise ReleaseDistributionError("release record must use UTF-8 without a byte-order mark")
    try:
        text = payload.decode("utf-8")
    except UnicodeError as exc:
        raise ReleaseDistributionError("release record must use UTF-8") from exc
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "+++":
        raise ReleaseDistributionError("release record has no TOML front matter")
    closing = next((index for index, line in enumerate(lines[1:], 1) if line.strip() == "+++"), -1)
    if closing < 0:
        raise ReleaseDistributionError("release record front matter is not closed")
    try:
        metadata = tomllib.loads("".join(lines[1:closing]))
    except tomllib.TOMLDecodeError as exc:
        raise ReleaseDistributionError(f"release record metadata is invalid: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ReleaseDistributionError("release record metadata must be a TOML table")
    return metadata, text, lines, closing


def _atomic_replace(path: Path, payload: bytes) -> None:
    mode = stat.S_IMODE(path.stat().st_mode)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary_name, mode)
        os.replace(temporary_name, path)
    except OSError as exc:
        raise ReleaseDistributionError(f"cannot replace release record atomically: {exc}") from exc
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def bind_distribution(
    repository: Path,
    release_record: Path,
    manifest: Path,
) -> tuple[Path, ReleaseDistribution, bool]:
    try:
        root = repository.resolve(strict=True)
    except OSError as exc:
        raise ReleaseDistributionError("repository does not exist") from exc
    record_path = _safe_repository_file(root, release_record, "release record")
    manifest_path = _safe_repository_file(root, manifest, "distribution manifest")
    metadata, _text, lines, closing = read_release_record(record_path)
    if metadata.get("type") != "release_record" or metadata.get("status") != "ready":
        raise ReleaseDistributionError("distribution binding requires one ready release_record")
    version = metadata.get("version")
    commit = metadata.get("commit")
    object_format = metadata.get("git_object_format")
    if not isinstance(version, str) or VERSION_PATTERN.fullmatch(version) is None:
        raise ReleaseDistributionError("release record version is invalid")
    pattern = COMMIT_PATTERNS.get(object_format)
    if not isinstance(commit, str) or pattern is None or pattern.fullmatch(commit) is None:
        raise ReleaseDistributionError("release record candidate identity is invalid")
    epoch_text = str(_run_git(root, "show", "-s", "--format=%ct", commit))
    if not epoch_text.isdigit():
        raise ReleaseDistributionError("candidate commit timestamp is invalid")
    distribution = read_bundle_manifest(
        manifest_path,
        version=version,
        commit=commit,
        git_object_format=object_format,
        source_date_epoch=int(epoch_text),
    )
    if source_manifest_sha256(root, commit) != distribution.source_manifest_sha256:
        raise ReleaseDistributionError(
            "distribution manifest source identity does not match the candidate tree"
        )
    existing = metadata.get("distribution")
    if existing is not None:
        current = validate_distribution_block(existing, version)
        if current != distribution:
            raise ReleaseDistributionError("release record contains conflicting distribution provenance")
        return record_path, distribution, False
    relation_index = next(
        (index for index, line in enumerate(lines[1:closing], 1) if line.strip() == "[relations]"),
        -1,
    )
    if relation_index < 0:
        raise ReleaseDistributionError("release record has no relations table")
    newline = "\r\n" if lines[0].endswith("\r\n") else "\n"
    insertion = distribution.toml(newline) + newline * 2
    updated = "".join(lines[:relation_index]) + insertion + "".join(lines[relation_index:])
    _atomic_replace(record_path, updated.encode("utf-8"))
    return record_path, distribution, True


def validate_record_distribution(repository: Path, path: Path, *, required: bool = False) -> bool:
    metadata, _text, _lines, _closing = read_release_record(path)
    if metadata.get("type") != "release_record":
        return False
    value = metadata.get("distribution")
    if value is None:
        if required:
            raise ReleaseDistributionError(f"release record has no distribution provenance: {path}")
        return False
    version = metadata.get("version")
    commit = metadata.get("commit")
    object_format = metadata.get("git_object_format")
    if not isinstance(version, str):
        raise ReleaseDistributionError(f"release record version is invalid: {path}")
    pattern = COMMIT_PATTERNS.get(object_format)
    if not isinstance(commit, str) or pattern is None or pattern.fullmatch(commit) is None:
        raise ReleaseDistributionError(f"release record candidate identity is invalid: {path}")
    distribution = validate_distribution_block(value, version)
    epoch_text = str(_run_git(repository, "show", "-s", "--format=%ct", commit))
    if not epoch_text.isdigit() or int(epoch_text) != distribution.source_date_epoch:
        raise ReleaseDistributionError(f"distribution epoch differs from candidate commit: {path}")
    if source_manifest_sha256(repository, commit) != distribution.source_manifest_sha256:
        raise ReleaseDistributionError(f"distribution source manifest differs from candidate tree: {path}")
    return True


def release_record_paths(repository: Path) -> Iterable[Path]:
    root = repository / "docs" / "engineering"
    if not root.is_dir():
        raise ReleaseDistributionError("repository has no docs/engineering directory")
    for path in sorted(root.rglob("*.md")):
        if path.is_file() and not path.is_symlink():
            yield path
