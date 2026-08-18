"""Validate deterministic Python release distribution manifests."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from se_harness.installer import HarnessError


BUNDLE_SCHEMA = "se-harness-release-bundle/v1"
DISTRIBUTION_SCHEMA = 1
DISTRIBUTION_KIND = "python-wheel-sdist"
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
COMMIT_PATTERNS = {
    "sha1": re.compile(r"[0-9a-f]{40}"),
    "sha256": re.compile(r"[0-9a-f]{64}"),
}
SAFE_BASENAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,199}")
BUNDLE_KEYS = frozenset(
    {
        "schema",
        "version",
        "commit",
        "git_object_format",
        "source_date_epoch",
        "wheel",
        "wheel_sha256",
        "sdist",
        "sdist_sha256",
        "checksums",
        "checksums_sha256",
        "checksums_content",
        "source_manifest_sha256",
    }
)
DISTRIBUTION_KEYS = frozenset(
    {
        "schema",
        "kind",
        "source_date_epoch",
        "wheel",
        "wheel_sha256",
        "sdist",
        "sdist_sha256",
        "checksums",
        "checksums_sha256",
        "source_manifest_sha256",
    }
)


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

    def toml(self) -> str:
        values = self.as_metadata()
        return "\n".join(
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
    return (
        f"{wheel_sha256}  {wheel}\n"
        f"{sdist_sha256}  {sdist}\n"
    ).encode("utf-8")


def expected_distribution_names(version: str) -> tuple[str, str]:
    return (
        f"se_harness-{version}-py3-none-any.whl",
        f"se_harness-{version}.tar.gz",
    )


def _duplicate_safe_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise HarnessError(f"distribution manifest contains duplicate key: {key}")
        result[key] = value
    return result


def _sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_PATTERN.fullmatch(value) is None:
        raise HarnessError(f"{label} must be 64 lowercase hexadecimal characters")
    return value


def _safe_basename(value: Any, label: str) -> str:
    if not isinstance(value, str) or SAFE_BASENAME_PATTERN.fullmatch(value) is None:
        raise HarnessError(f"{label} must be a safe ASCII basename")
    if Path(value).name != value or value in {".", ".."}:
        raise HarnessError(f"{label} must be a safe basename")
    return value


def validate_distribution_block(value: Any, version: str) -> ReleaseDistribution:
    if not isinstance(value, dict):
        raise HarnessError("distribution must be a TOML table")
    keys = set(value)
    if keys != DISTRIBUTION_KEYS:
        missing = sorted(DISTRIBUTION_KEYS - keys)
        extra = sorted(keys - DISTRIBUTION_KEYS)
        detail = []
        if missing:
            detail.append(f"missing {', '.join(missing)}")
        if extra:
            detail.append(f"unexpected {', '.join(extra)}")
        raise HarnessError(f"distribution block must be complete ({'; '.join(detail)})")
    if value.get("schema") != DISTRIBUTION_SCHEMA:
        raise HarnessError("distribution schema must be 1")
    if value.get("kind") != DISTRIBUTION_KIND:
        raise HarnessError(f"distribution kind must be {DISTRIBUTION_KIND}")
    epoch = value.get("source_date_epoch")
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 1:
        raise HarnessError("distribution source_date_epoch must be a positive integer")
    wheel = _safe_basename(value.get("wheel"), "distribution wheel")
    sdist = _safe_basename(value.get("sdist"), "distribution sdist")
    checksums = _safe_basename(value.get("checksums"), "distribution checksums")
    expected_wheel, expected_sdist = expected_distribution_names(version)
    if wheel != expected_wheel or sdist != expected_sdist:
        raise HarnessError("distribution filenames do not match the release version")
    if checksums != "SHA256SUMS":
        raise HarnessError("distribution checksums filename must be SHA256SUMS")
    wheel_hash = _sha256(value.get("wheel_sha256"), "distribution wheel_sha256")
    sdist_hash = _sha256(value.get("sdist_sha256"), "distribution sdist_sha256")
    checksums_hash = _sha256(value.get("checksums_sha256"), "distribution checksums_sha256")
    expected_checksums_hash = hashlib.sha256(
        checksum_manifest_bytes(version, wheel_hash, sdist_hash)
    ).hexdigest()
    if checksums_hash != expected_checksums_hash:
        raise HarnessError("distribution checksums_sha256 does not identify canonical SHA256SUMS bytes")
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
        raise HarnessError(f"cannot read distribution manifest: {path}") from exc
    if len(payload) > 128 * 1024:
        raise HarnessError("distribution manifest is too large")
    try:
        value = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=_duplicate_safe_object,
        )
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise HarnessError("distribution manifest must be valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise HarnessError("distribution manifest must be a JSON object")
    keys = set(value)
    if keys != BUNDLE_KEYS:
        missing = sorted(BUNDLE_KEYS - keys)
        extra = sorted(keys - BUNDLE_KEYS)
        detail = []
        if missing:
            detail.append(f"missing {', '.join(missing)}")
        if extra:
            detail.append(f"unexpected {', '.join(extra)}")
        raise HarnessError(f"distribution manifest fields are invalid ({'; '.join(detail)})")
    if value.get("schema") != BUNDLE_SCHEMA:
        raise HarnessError(f"distribution manifest schema must be {BUNDLE_SCHEMA}")
    if value.get("version") != version:
        raise HarnessError("distribution manifest version does not match the release")
    if value.get("git_object_format") != git_object_format:
        raise HarnessError("distribution manifest Git object format does not match the candidate")
    commit_pattern = COMMIT_PATTERNS.get(git_object_format)
    manifest_commit = value.get("commit")
    if (
        commit_pattern is None
        or not isinstance(manifest_commit, str)
        or commit_pattern.fullmatch(manifest_commit) is None
        or manifest_commit != commit
    ):
        raise HarnessError("distribution manifest commit does not match the candidate")
    if value.get("source_date_epoch") != source_date_epoch:
        raise HarnessError("distribution manifest epoch does not match the candidate commit")
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
        raise HarnessError("distribution manifest checksums_content is not canonical")
    return distribution
