#!/usr/bin/env python3
"""Build and verify non-promotable, commit-addressed integration packages."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import unicodedata
import venv
import zipfile
from email import policy
from email.parser import BytesParser
from typing import Any, Sequence

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from repository_tools import json_bytes  # noqa: E402
from repository_tools.json_bytes import sha256_bytes  # noqa: E402,F401

SCHEMA = "se-harness-integration-package-v1"
DISTRIBUTION_KIND = "integration-package"
MANIFEST_NAME = "integration-manifest.json"
CHECKSUM_NAME = "SHA256SUMS"
MAX_PAYLOAD_FILE = 128 * 1024 * 1024
MAX_MANIFEST = 1024 * 1024
MAX_ARCHIVE_MEMBER = 128 * 1024 * 1024
MAX_ARCHIVE_TOTAL = 512 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 10_000
MAX_WHEEL_MEMBERS = 20_000
MAX_WHEEL_EXPANDED = 512 * 1024 * 1024
COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?")
BASE_VERSION_PATTERN = re.compile(
    r"(?:[1-9][0-9]*!)?[0-9]+(?:\.[0-9]+)*"
    r"(?:(?:a|b|rc)[0-9]+)?(?:\.post[0-9]+)?(?:\.dev[0-9]+)?"
)
REPOSITORY_PATTERN = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
HASH_PATTERN = re.compile(r"[0-9a-f]{64}")
RESERVED_WINDOWS_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}
TOP_LEVEL_FIELDS = {
    "base_version",
    "build",
    "channel",
    "commit",
    "distribution_kind",
    "event",
    "overlays",
    "promotable",
    "pull_request",
    "ref",
    "repository",
    "retention_days",
    "run",
    "schema",
    "version",
    "wheel",
}
BUILD_FIELDS = {"build", "python", "setuptools", "source_date_epoch", "wheel"}
RUN_FIELDS = {"attempt", "id", "workflow"}
WHEEL_FIELDS = {"filename", "sha256", "size"}
OVERLAY_FIELDS = {"after_sha256", "before_sha256", "path"}
OVERLAY_PATHS = ("pyproject.toml", "se_harness/__init__.py")


class IntegrationPackageError(RuntimeError):
    """An integration-package invariant failed."""


def canonical_json_bytes(value: Any) -> bytes:
    return json_bytes.canonical_json_bytes(value, error=IntegrationPackageError)


def sha256_file(path: Path) -> str:
    return json_bytes.sha256_file(path, error=IntegrationPackageError, label=path.name)


def parse_json_object(raw: bytes) -> dict[str, Any]:
    return json_bytes.parse_json_object(raw, error=IntegrationPackageError, label="manifest", max_bytes=MAX_MANIFEST)


def _require_exact_fields(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        unknown = sorted(actual - expected)
        detail = []
        if missing:
            detail.append("missing=" + ",".join(missing))
        if unknown:
            detail.append("unknown=" + ",".join(unknown))
        raise IntegrationPackageError(f"{label} fields are invalid ({'; '.join(detail)})")


def _require_string(value: Any, label: str, *, maximum: int = 512) -> str:
    if not isinstance(value, str) or not value or len(value) > maximum:
        raise IntegrationPackageError(f"{label} must be a non-empty bounded string")
    if any(
        ord(character) < 32 or ord(character) == 127 or 0xD800 <= ord(character) <= 0xDFFF
        for character in value
    ):
        raise IntegrationPackageError(f"{label} contains a control character")
    return value


def _require_positive_integer(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise IntegrationPackageError(f"{label} must be a positive integer")
    return value


def validate_commit(value: str) -> str:
    if COMMIT_PATTERN.fullmatch(value) is None:
        raise IntegrationPackageError("commit must be 40 or 64 lowercase hexadecimal characters")
    return value


def validate_base_version(value: str) -> str:
    if BASE_VERSION_PATTERN.fullmatch(value) is None:
        raise IntegrationPackageError("base version is not an accepted public PEP 440 version")
    if "+" in value:
        raise IntegrationPackageError("base version must not contain a local-version segment")
    return value


def derive_identity(
    base_version: str,
    commit: str,
    event: str,
    ref: str,
    pull_request: int | None,
) -> tuple[str, str, int]:
    base_version = validate_base_version(base_version)
    commit = validate_commit(commit)
    if event == "push":
        if ref != "refs/heads/main" or pull_request is not None:
            raise IntegrationPackageError("push integration packages require refs/heads/main and no pull request")
        channel = "main"
        retention_days = 14
    elif event == "pull_request":
        if isinstance(pull_request, bool) or not isinstance(pull_request, int) or pull_request <= 0:
            raise IntegrationPackageError("pull_request event requires a positive pull-request number")
        if ref != f"refs/pull/{pull_request}/merge":
            raise IntegrationPackageError("pull-request ref does not match the pull-request number")
        channel = f"pr{pull_request}"
        retention_days = 3
    else:
        raise IntegrationPackageError("event must be push or pull_request")
    return channel, f"{base_version}+{channel}.g{commit[:12]}", retention_days


def _portable_path(value: str, *, directory: bool = False) -> str:
    if directory and value.endswith("/"):
        value = value[:-1]
    if not value or len(value) > 512 or value.startswith("/") or "\\" in value:
        raise IntegrationPackageError(f"unsafe portable path: {value!r}")
    if any(
        ord(character) < 32 or ord(character) == 127 or 0xD800 <= ord(character) <= 0xDFFF
        for character in value
    ):
        raise IntegrationPackageError("portable path contains a control character")
    raw_parts = value.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        raise IntegrationPackageError(f"unsafe portable path: {value!r}")
    path = PurePosixPath(*raw_parts)
    if path.is_absolute():
        raise IntegrationPackageError(f"unsafe portable path: {value!r}")
    for part in path.parts:
        if len(part) > 255 or part.endswith((".", " ")) or ":" in part:
            raise IntegrationPackageError(f"non-portable path segment: {part!r}")
        device = part.split(".", 1)[0].upper()
        if device in RESERVED_WINDOWS_NAMES:
            raise IntegrationPackageError(f"reserved path segment: {part!r}")
    return path.as_posix()


def _portable_identity(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def _run(
    arguments: Sequence[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        list(arguments),
        cwd=cwd,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        if len(detail) > 4000:
            detail = detail[:4000] + "..."
        raise IntegrationPackageError(
            f"command failed ({arguments[0]} exit {completed.returncode}): {detail or 'no diagnostic'}"
        )
    return completed


def _run_bytes(arguments: Sequence[str], *, cwd: Path | None = None) -> bytes:
    completed = subprocess.run(list(arguments), cwd=cwd, check=False, capture_output=True)
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", "replace").strip()
        if len(detail) > 4000:
            detail = detail[:4000] + "..."
        raise IntegrationPackageError(
            f"command failed ({arguments[0]} exit {completed.returncode}): {detail or 'no diagnostic'}"
        )
    return completed.stdout


def _git_text(repository: Path, *arguments: str) -> str:
    return _run(["git", "-C", str(repository), *arguments]).stdout.strip()


def validate_repository(repository: Path, commit: str) -> tuple[Path, int]:
    repository = repository.resolve(strict=True)
    top = Path(_git_text(repository, "rev-parse", "--show-toplevel")).resolve(strict=True)
    if top != repository:
        raise IntegrationPackageError("repository must be the exact Git worktree root")
    resolved = _git_text(repository, "rev-parse", "--verify", f"{commit}^{{commit}}").lower()
    if resolved != commit:
        raise IntegrationPackageError("commit does not resolve exactly in the selected repository")
    timestamp_text = _git_text(repository, "show", "-s", "--format=%ct", commit)
    try:
        timestamp = int(timestamp_text)
    except ValueError as exc:
        raise IntegrationPackageError("commit timestamp is invalid") from exc
    if timestamp <= 0:
        raise IntegrationPackageError("commit timestamp must be positive")
    return repository, timestamp


def create_git_archive(repository: Path, commit: str, destination: Path) -> None:
    if destination.exists():
        raise IntegrationPackageError("archive destination already exists")
    _run(
        [
            "git",
            "-C",
            str(repository),
            "archive",
            "--format=tar",
            f"--output={destination}",
            commit,
        ]
    )
    if not destination.is_file() or destination.is_symlink():
        raise IntegrationPackageError("Git did not produce one regular archive")


def extract_safe_archive(archive_path: Path, destination: Path) -> None:
    if destination.exists():
        raise IntegrationPackageError("archive extraction destination already exists")
    if not archive_path.is_file() or archive_path.is_symlink() or archive_path.stat().st_size > MAX_ARCHIVE_TOTAL:
        raise IntegrationPackageError("archive must be one bounded regular file")
    destination.mkdir(parents=True)
    try:
        with tarfile.open(archive_path, mode="r:") as archive:
            members = archive.getmembers()
            if not members or len(members) > MAX_ARCHIVE_MEMBERS:
                raise IntegrationPackageError("archive member count is invalid")
            planned: list[tuple[tarfile.TarInfo, str]] = []
            identities: set[str] = set()
            total_size = 0
            for member in members:
                if not (member.isdir() or member.isreg()):
                    raise IntegrationPackageError(f"archive contains a link or special member: {member.name}")
                portable = _portable_path(member.name, directory=member.isdir())
                identity = _portable_identity(portable)
                if identity in identities:
                    raise IntegrationPackageError(f"archive contains a duplicate portable path: {portable}")
                identities.add(identity)
                if member.isreg():
                    if member.size < 0 or member.size > MAX_ARCHIVE_MEMBER:
                        raise IntegrationPackageError(f"archive member size is invalid: {portable}")
                    total_size += member.size
                    if total_size > MAX_ARCHIVE_TOTAL:
                        raise IntegrationPackageError("archive expanded size exceeds the limit")
                planned.append((member, portable))

            for member, portable in planned:
                target = destination.joinpath(*PurePosixPath(portable).parts)
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    if not target.is_dir() or target.is_symlink():
                        raise IntegrationPackageError(f"archive directory is unsafe: {portable}")
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                source = archive.extractfile(member)
                if source is None:
                    raise IntegrationPackageError(f"cannot read archive member: {portable}")
                with source, target.open("xb") as handle:
                    shutil.copyfileobj(source, handle, length=1024 * 1024)
                target.chmod(0o755 if member.mode & 0o111 else 0o644)
    except (OSError, tarfile.TarError) as exc:
        raise IntegrationPackageError("cannot safely extract Git archive") from exc

    for required in OVERLAY_PATHS:
        path = destination.joinpath(*PurePosixPath(required).parts)
        if not path.is_file() or path.is_symlink():
            raise IntegrationPackageError(f"archive is missing required regular file: {required}")


def regular_tree_manifest(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    identities: set[str] = set()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        portable = _portable_path(relative, directory=path.is_dir())
        identity = _portable_identity(portable)
        if identity in identities:
            raise IntegrationPackageError(f"tree contains a duplicate portable path: {portable}")
        identities.add(identity)
        if path.is_symlink():
            raise IntegrationPackageError(f"tree contains a symbolic link: {portable}")
        if path.is_dir():
            continue
        if not path.is_file() or path.stat().st_size > MAX_ARCHIVE_MEMBER:
            raise IntegrationPackageError(f"tree contains an invalid file: {portable}")
        result[portable] = sha256_file(path)
    return result


def _replace_declared_version(path: Path, *, project_file: bool, replacement: str) -> tuple[str, str, str]:
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise IntegrationPackageError(f"version declaration is not regular UTF-8 text: {path.name}") from exc
    if raw.startswith(b"\xef\xbb\xbf"):
        raise IntegrationPackageError("version declaration must not contain a UTF-8 BOM")

    section: str | None = None
    matches: list[tuple[int, str, str, str]] = []
    lines = text.splitlines(keepends=True)
    section_pattern = re.compile(r"^[ \t]*\[([^]\r\n]+)\][ \t]*(?:#.*)?(?:\r?\n)?$")
    name = "version" if project_file else "__version__"
    assignment = re.compile(
        rf'^(?P<prefix>[ \t]*{re.escape(name)}[ \t]*=[ \t]*")'
        r'(?P<value>[^"\r\n]+)(?P<suffix>"[ \t]*(?:#.*)?)(?P<eol>\r?\n)?$'
    )
    for index, line in enumerate(lines):
        heading = section_pattern.fullmatch(line)
        if heading:
            section = heading.group(1).strip()
            continue
        match = assignment.fullmatch(line)
        if match and (not project_file or section == "project"):
            matches.append((index, match.group("prefix"), match.group("suffix"), match.group("eol") or ""))
            old_value = match.group("value")
    if len(matches) != 1:
        raise IntegrationPackageError(f"expected exactly one declared {name} assignment")
    index, prefix, suffix, ending = matches[0]
    lines[index] = f"{prefix}{replacement}{suffix}{ending}"
    updated = "".join(lines).encode("utf-8")
    path.write_bytes(updated)
    return old_value, sha256_bytes(raw), sha256_bytes(updated)


def apply_version_overlay(export: Path, integration_version: str) -> tuple[str, list[dict[str, str]]]:
    pyproject = export / "pyproject.toml"
    package_init = export / "se_harness" / "__init__.py"
    pyproject_version, py_before, py_after = _replace_declared_version(
        pyproject,
        project_file=True,
        replacement=integration_version,
    )
    init_version, init_before, init_after = _replace_declared_version(
        package_init,
        project_file=False,
        replacement=integration_version,
    )
    if pyproject_version != init_version:
        raise IntegrationPackageError("committed version declarations do not agree")
    validate_base_version(pyproject_version)
    return pyproject_version, [
        {"path": OVERLAY_PATHS[0], "before_sha256": py_before, "after_sha256": py_after},
        {"path": OVERLAY_PATHS[1], "before_sha256": init_before, "after_sha256": init_after},
    ]


def installed_build_versions(
    expected_build: str,
    expected_setuptools: str,
    expected_wheel: str,
) -> dict[str, str]:
    expected = {
        "build": expected_build,
        "setuptools": expected_setuptools,
        "wheel": expected_wheel,
    }
    actual: dict[str, str] = {}
    for distribution, wanted in expected.items():
        try:
            observed = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError as exc:
            raise IntegrationPackageError(f"required build tool is not installed: {distribution}") from exc
        if observed != wanted:
            raise IntegrationPackageError(
                f"build tool version mismatch for {distribution}: expected {wanted}, observed {observed}"
            )
        actual[distribution] = observed
    return actual


def build_wheel(export: Path, output: Path, source_date_epoch: int) -> Path:
    output.mkdir(parents=True)
    environment = os.environ.copy()
    environment["SOURCE_DATE_EPOCH"] = str(source_date_epoch)
    environment["PYTHONHASHSEED"] = "0"
    environment["PYTHONNOUSERSITE"] = "1"
    environment["PYTHONPATH"] = ""
    _run(
        [
            sys.executable,
            "-m",
            "build",
            "--wheel",
            "--no-isolation",
            "--outdir",
            str(output),
            str(export),
        ],
        cwd=export.parent,
        env=environment,
    )
    wheels = [path for path in output.iterdir() if path.is_file() and not path.is_symlink() and path.suffix == ".whl"]
    if len(wheels) != 1 or len(list(output.iterdir())) != 1:
        raise IntegrationPackageError("each build must produce exactly one regular wheel")
    return wheels[0]


def validate_wheel(path: Path, expected_version: str) -> None:
    if not path.is_file() or path.is_symlink() or path.stat().st_size > MAX_PAYLOAD_FILE:
        raise IntegrationPackageError("wheel is not one bounded regular file")
    stem = path.name.removesuffix(".whl")
    parts = stem.rsplit("-", 3)
    if len(parts) != 4 or parts[1:] != ["py3", "none", "any"]:
        raise IntegrationPackageError("wheel must have the py3-none-any tag")
    if parts[0] != f"se_harness-{expected_version}":
        raise IntegrationPackageError("wheel filename does not match the integration version")
    try:
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            if not infos or len(infos) > MAX_WHEEL_MEMBERS:
                raise IntegrationPackageError("wheel member count is invalid")
            identities: set[str] = set()
            expanded = 0
            metadata_names: list[str] = []
            wheel_names: list[str] = []
            for info in infos:
                portable = _portable_path(info.filename, directory=info.is_dir())
                identity = _portable_identity(portable)
                if identity in identities:
                    raise IntegrationPackageError(f"wheel contains a duplicate portable path: {portable}")
                identities.add(identity)
                mode = (info.external_attr >> 16) & 0xFFFF
                if stat.S_IFMT(mode) == stat.S_IFLNK:
                    raise IntegrationPackageError("wheel contains a symbolic link")
                if info.file_size < 0 or info.file_size > MAX_PAYLOAD_FILE:
                    raise IntegrationPackageError("wheel member size is invalid")
                expanded += info.file_size
                if expanded > MAX_WHEEL_EXPANDED:
                    raise IntegrationPackageError("wheel expanded size exceeds the limit")
                if portable.endswith(".dist-info/METADATA"):
                    metadata_names.append(portable)
                if portable.endswith(".dist-info/WHEEL"):
                    wheel_names.append(portable)
            if len(metadata_names) != 1 or len(wheel_names) != 1:
                raise IntegrationPackageError("wheel must contain one METADATA and one WHEEL document")
            metadata_root = metadata_names[0].removesuffix("/METADATA")
            if wheel_names[0].removesuffix("/WHEEL") != metadata_root:
                raise IntegrationPackageError("wheel metadata documents use different dist-info roots")
            if metadata_root != f"se_harness-{expected_version}.dist-info":
                raise IntegrationPackageError("dist-info directory does not match the integration version")
            metadata = BytesParser(policy=policy.default).parsebytes(archive.read(metadata_names[0]))
            if metadata.get("Name") != "se-harness" or metadata.get("Version") != expected_version:
                raise IntegrationPackageError("wheel METADATA identity does not match")
            wheel_text = archive.read(wheel_names[0]).decode("utf-8", "strict")
            wheel_headers = BytesParser(policy=policy.default).parsebytes(wheel_text.encode("utf-8"))
            if wheel_headers.get("Root-Is-Purelib", "").lower() != "true":
                raise IntegrationPackageError("wheel is not pure Python")
            if "py3-none-any" not in wheel_headers.get_all("Tag", []):
                raise IntegrationPackageError("wheel metadata is missing py3-none-any")
    except IntegrationPackageError:
        raise
    except (OSError, UnicodeError, zipfile.BadZipFile, KeyError) as exc:
        raise IntegrationPackageError("wheel archive is invalid") from exc


def _validate_manifest(value: dict[str, Any]) -> None:
    _require_exact_fields(value, TOP_LEVEL_FIELDS, "manifest")
    if value["schema"] != SCHEMA or value["distribution_kind"] != DISTRIBUTION_KIND:
        raise IntegrationPackageError("manifest schema or distribution kind is invalid")
    if value["promotable"] is not False:
        raise IntegrationPackageError("integration package must declare promotable=false")
    base = validate_base_version(_require_string(value["base_version"], "base_version"))
    commit = validate_commit(_require_string(value["commit"], "commit"))
    event = _require_string(value["event"], "event")
    ref = _require_string(value["ref"], "ref")
    pull_request = value["pull_request"]
    if pull_request is not None and (isinstance(pull_request, bool) or not isinstance(pull_request, int)):
        raise IntegrationPackageError("pull_request must be null or an integer")
    channel, version, retention = derive_identity(base, commit, event, ref, pull_request)
    if value["channel"] != channel or value["version"] != version or value["retention_days"] != retention:
        raise IntegrationPackageError("manifest identity or retention does not match its inputs")
    repository = _require_string(value["repository"], "repository")
    if REPOSITORY_PATTERN.fullmatch(repository) is None:
        raise IntegrationPackageError("repository must be an owner/name slug")

    build = value["build"]
    if not isinstance(build, dict):
        raise IntegrationPackageError("build must be an object")
    _require_exact_fields(build, BUILD_FIELDS, "build")
    for field in ("build", "python", "setuptools", "wheel"):
        _require_string(build[field], f"build.{field}")
    _require_positive_integer(build["source_date_epoch"], "build.source_date_epoch")

    run = value["run"]
    if not isinstance(run, dict):
        raise IntegrationPackageError("run must be an object")
    _require_exact_fields(run, RUN_FIELDS, "run")
    _require_positive_integer(run["id"], "run.id")
    _require_positive_integer(run["attempt"], "run.attempt")
    _require_string(run["workflow"], "run.workflow")

    overlays = value["overlays"]
    if not isinstance(overlays, list) or len(overlays) != 2:
        raise IntegrationPackageError("overlays must contain exactly two entries")
    observed_paths: list[str] = []
    for index, overlay in enumerate(overlays):
        if not isinstance(overlay, dict):
            raise IntegrationPackageError("overlay entry must be an object")
        _require_exact_fields(overlay, OVERLAY_FIELDS, f"overlay[{index}]")
        observed_paths.append(_portable_path(_require_string(overlay["path"], "overlay.path")))
        for name in ("before_sha256", "after_sha256"):
            digest = _require_string(overlay[name], f"overlay.{name}")
            if HASH_PATTERN.fullmatch(digest) is None:
                raise IntegrationPackageError("overlay digest is invalid")
        if overlay["before_sha256"] == overlay["after_sha256"]:
            raise IntegrationPackageError("version overlay did not change its declared file")
    if tuple(observed_paths) != OVERLAY_PATHS:
        raise IntegrationPackageError("overlay paths or ordering are invalid")

    wheel = value["wheel"]
    if not isinstance(wheel, dict):
        raise IntegrationPackageError("wheel must be an object")
    _require_exact_fields(wheel, WHEEL_FIELDS, "wheel")
    filename = _portable_path(_require_string(wheel["filename"], "wheel.filename"))
    if "/" in filename or not filename.endswith(".whl"):
        raise IntegrationPackageError("wheel filename is invalid")
    digest = _require_string(wheel["sha256"], "wheel.sha256")
    if HASH_PATTERN.fullmatch(digest) is None:
        raise IntegrationPackageError("wheel digest is invalid")
    _require_positive_integer(wheel["size"], "wheel.size")


def checksum_bytes(files: dict[str, bytes]) -> bytes:
    lines = [f"{sha256_bytes(files[name])}  {name}\n" for name in sorted(files)]
    return "".join(lines).encode("ascii")


def verify_payload(
    payload: Path,
    *,
    expected_commit: str | None = None,
    expected_repository: str | None = None,
    expected_event: str | None = None,
    expected_ref: str | None = None,
    expected_pull_request: int | None = None,
    expected_run_id: int | None = None,
    expected_run_attempt: int | None = None,
    expected_workflow: str | None = None,
    expected_retention_days: int | None = None,
) -> dict[str, Any]:
    lexical_payload = payload.absolute()
    if lexical_payload.is_symlink():
        raise IntegrationPackageError("payload directory must not be a symbolic link")
    payload = lexical_payload.resolve(strict=True)
    if not payload.is_dir():
        raise IntegrationPackageError("payload must be one regular directory")
    entries = list(payload.iterdir())
    if any(not path.is_file() or path.is_symlink() for path in entries):
        raise IntegrationPackageError("payload contains a directory, link, or special file")
    names = {path.name for path in entries}
    wheel_names = sorted(name for name in names if name.endswith(".whl"))
    if len(wheel_names) != 1 or names != {MANIFEST_NAME, CHECKSUM_NAME, wheel_names[0]}:
        raise IntegrationPackageError("payload must contain exactly one wheel, manifest, and checksum file")
    for path in entries:
        if path.stat().st_size > MAX_PAYLOAD_FILE:
            raise IntegrationPackageError(f"payload file exceeds size limit: {path.name}")

    manifest_path = payload / MANIFEST_NAME
    manifest_raw = manifest_path.read_bytes()
    manifest = parse_json_object(manifest_raw)
    _validate_manifest(manifest)
    if canonical_json_bytes(manifest) != manifest_raw:
        raise IntegrationPackageError("manifest is not canonical compact UTF-8/LF JSON")
    wheel_name = manifest["wheel"]["filename"]
    if wheel_name != wheel_names[0]:
        raise IntegrationPackageError("manifest wheel filename does not match payload inventory")
    wheel_path = payload / wheel_name
    if wheel_path.stat().st_size != manifest["wheel"]["size"]:
        raise IntegrationPackageError("wheel size does not match manifest")
    if sha256_file(wheel_path) != manifest["wheel"]["sha256"]:
        raise IntegrationPackageError("wheel digest does not match manifest")
    validate_wheel(wheel_path, manifest["version"])
    expected_checksums = checksum_bytes({MANIFEST_NAME: manifest_raw, wheel_name: wheel_path.read_bytes()})
    if (payload / CHECKSUM_NAME).read_bytes() != expected_checksums:
        raise IntegrationPackageError("SHA256SUMS is noncanonical or does not match payload bytes")

    expected_pairs = {
        "commit": expected_commit,
        "repository": expected_repository,
        "event": expected_event,
        "ref": expected_ref,
        "pull_request": expected_pull_request,
        "retention_days": expected_retention_days,
    }
    for field, expected in expected_pairs.items():
        if expected is not None and manifest[field] != expected:
            raise IntegrationPackageError(f"manifest {field} does not match workflow expectation")
    run_pairs = {
        "id": expected_run_id,
        "attempt": expected_run_attempt,
        "workflow": expected_workflow,
    }
    for field, expected in run_pairs.items():
        if expected is not None and manifest["run"][field] != expected:
            raise IntegrationPackageError(f"manifest run.{field} does not match workflow expectation")
    return manifest


def _prepare_output(output: Path, wheel: Path, manifest: dict[str, Any]) -> None:
    output = output.absolute()
    if output.exists() or output.is_symlink():
        raise IntegrationPackageError("output payload path already exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.parent / f".{output.name}.tmp-{os.getpid()}-{secrets.token_hex(4)}"
    temporary.mkdir()
    try:
        destination_wheel = temporary / wheel.name
        shutil.copyfile(wheel, destination_wheel)
        manifest_raw = canonical_json_bytes(manifest)
        (temporary / MANIFEST_NAME).write_bytes(manifest_raw)
        (temporary / CHECKSUM_NAME).write_bytes(
            checksum_bytes({MANIFEST_NAME: manifest_raw, wheel.name: destination_wheel.read_bytes()})
        )
        verify_payload(temporary)
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def build_integration_package(args: argparse.Namespace) -> dict[str, Any]:
    commit = validate_commit(args.commit)
    repository, source_date_epoch = validate_repository(args.repository, commit)
    output = args.output.absolute().resolve(strict=False)
    if output == repository or repository in output.parents:
        raise IntegrationPackageError("integration payload output must remain outside the candidate checkout")
    if REPOSITORY_PATTERN.fullmatch(args.repository_slug) is None:
        raise IntegrationPackageError("repository slug must be owner/name")
    _require_positive_integer(args.run_id, "run id")
    _require_positive_integer(args.run_attempt, "run attempt")
    _require_string(args.workflow, "workflow")
    tool_versions = installed_build_versions(
        args.expect_build_version,
        args.expect_setuptools_version,
        args.expect_wheel_version,
    )
    with tempfile.TemporaryDirectory(prefix="se-harness-integration-build-") as temporary_name:
        temporary = Path(temporary_name)
        archive = temporary / "candidate.tar"
        create_git_archive(repository, commit, archive)
        exports = (temporary / "export-a", temporary / "export-b")
        for export in exports:
            extract_safe_archive(archive, export)
        baseline_a = regular_tree_manifest(exports[0])
        baseline_b = regular_tree_manifest(exports[1])
        if baseline_a != baseline_b:
            raise IntegrationPackageError("independent exact-commit exports differ")

        first_declared = _replace_declared_version_preview(exports[0])
        channel, integration_version, required_retention = derive_identity(
            first_declared,
            commit,
            args.event,
            args.ref,
            args.pull_request,
        )
        if args.retention_days != required_retention:
            raise IntegrationPackageError("requested retention does not match the event channel")
        overlay_a = apply_version_overlay(exports[0], integration_version)
        overlay_b = apply_version_overlay(exports[1], integration_version)
        if overlay_a != overlay_b or overlay_a[0] != first_declared:
            raise IntegrationPackageError("independent version overlays are not identical")
        for export, baseline in zip(exports, (baseline_a, baseline_b), strict=True):
            updated = regular_tree_manifest(export)
            changed = sorted(
                path
                for path in set(baseline) | set(updated)
                if baseline.get(path) != updated.get(path)
            )
            if changed != list(OVERLAY_PATHS):
                raise IntegrationPackageError("version overlay changed a path outside its declared boundary")

        wheel_a = build_wheel(exports[0], temporary / "dist-a", source_date_epoch)
        wheel_b = build_wheel(exports[1], temporary / "dist-b", source_date_epoch)
        if wheel_a.name != wheel_b.name:
            raise IntegrationPackageError("independent wheel filenames differ")
        first_bytes = wheel_a.read_bytes()
        second_bytes = wheel_b.read_bytes()
        if first_bytes != second_bytes:
            raise IntegrationPackageError("independent wheel builds are not byte-identical")
        validate_wheel(wheel_a, integration_version)
        wheel_digest = sha256_bytes(first_bytes)
        manifest: dict[str, Any] = {
            "schema": SCHEMA,
            "distribution_kind": DISTRIBUTION_KIND,
            "promotable": False,
            "repository": args.repository_slug,
            "commit": commit,
            "event": args.event,
            "ref": args.ref,
            "pull_request": args.pull_request,
            "channel": channel,
            "base_version": first_declared,
            "version": integration_version,
            "retention_days": required_retention,
            "build": {
                "python": platform.python_version(),
                "build": tool_versions["build"],
                "setuptools": tool_versions["setuptools"],
                "wheel": tool_versions["wheel"],
                "source_date_epoch": source_date_epoch,
            },
            "run": {
                "id": args.run_id,
                "attempt": args.run_attempt,
                "workflow": args.workflow,
            },
            "overlays": overlay_a[1],
            "wheel": {
                "filename": wheel_a.name,
                "size": len(first_bytes),
                "sha256": wheel_digest,
            },
        }
        _validate_manifest(manifest)
        _prepare_output(output, wheel_a, manifest)
        return verify_payload(output)


def _replace_declared_version_preview(export: Path) -> str:
    values: list[str] = []
    pyproject = (export / "pyproject.toml").read_text(encoding="utf-8")
    section: str | None = None
    for line in pyproject.splitlines():
        heading = re.fullmatch(r"[ \t]*\[([^]]+)\][ \t]*(?:#.*)?", line)
        if heading:
            section = heading.group(1).strip()
            continue
        match = re.fullmatch(r'[ \t]*version[ \t]*=[ \t]*"([^"\r\n]+)"[ \t]*(?:#.*)?', line)
        if match and section == "project":
            values.append(match.group(1))
    init_text = (export / "se_harness" / "__init__.py").read_text(encoding="utf-8")
    values.extend(
        match.group(1)
        for line in init_text.splitlines()
        if (match := re.fullmatch(r'[ \t]*__version__[ \t]*=[ \t]*"([^"\r\n]+)"[ \t]*(?:#.*)?', line))
    )
    if len(values) != 2 or len(set(values)) != 1:
        raise IntegrationPackageError("committed version declarations are absent, ambiguous, or mismatched")
    return validate_base_version(values[0])


def repository_snapshot(repository: Path) -> str:
    repository = repository.resolve(strict=True)
    names_raw = _run_bytes(
        ["git", "-C", str(repository), "ls-files", "--cached", "--others", "--exclude-standard", "-z"]
    )
    digest = hashlib.sha256()
    names = [name for name in names_raw.split(b"\0") if name]
    for raw_name in sorted(names):
        name = os.fsdecode(raw_name)
        portable = _portable_path(name.replace(os.sep, "/"))
        path = repository.joinpath(*PurePosixPath(portable).parts)
        digest.update(raw_name + b"\0")
        if path.is_symlink():
            digest.update(b"link\0" + os.fsencode(os.readlink(path)) + b"\0")
        elif path.is_file():
            digest.update(b"file\0" + bytes.fromhex(sha256_file(path)))
        else:
            raise IntegrationPackageError(f"repository snapshot path is not a file: {portable}")
    refs = _run_bytes(["git", "-C", str(repository), "show-ref", "--head"])
    status_output = _run_bytes(
        ["git", "-C", str(repository), "status", "--porcelain=v1", "--untracked-files=all"]
    )
    digest.update(b"refs\0" + refs + b"status\0" + status_output)
    return digest.hexdigest()


def _isolated_environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment["PYTHONNOUSERSITE"] = "1"
    environment["PYTHONPATH"] = ""
    return environment


def _canonical_existing_directory(path: str | os.PathLike[str]) -> Path:
    """Resolve aliases such as Windows 8.3 names before creating a venv."""
    resolved = Path(os.path.realpath(os.fspath(path), strict=True))
    if not resolved.is_dir():
        raise IntegrationPackageError(f"temporary root is not a directory: {resolved}")
    return resolved


def install_test(payload: Path, checkout: Path, expected: dict[str, Any]) -> dict[str, Any]:
    manifest = verify_payload(payload, **expected)
    checkout = checkout.resolve(strict=True)
    before = repository_snapshot(checkout)
    with tempfile.TemporaryDirectory(prefix="se-harness-integration-install-") as temporary_name:
        temporary = _canonical_existing_directory(temporary_name)
        environment_root = temporary / "environment"
        venv.EnvBuilder(with_pip=True, clear=False).create(environment_root)
        if os.name == "nt":
            python = environment_root / "Scripts" / "python.exe"
            harnessctl = environment_root / "Scripts" / "harnessctl.exe"
        else:
            python = environment_root / "bin" / "python"
            harnessctl = environment_root / "bin" / "harnessctl"
        wheel = payload.resolve(strict=True) / manifest["wheel"]["filename"]
        environment = _isolated_environment()
        _run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-index",
                "--no-deps",
                str(wheel),
            ],
            cwd=temporary,
            env=environment,
        )
        identity = _run(
            [
                str(python),
                "-I",
                "-c",
                "import importlib.metadata as m, se_harness; "
                "print(m.version('se-harness')); print(se_harness.__version__)",
            ],
            cwd=temporary,
            env=environment,
        ).stdout.splitlines()
        if identity != [manifest["version"], manifest["version"]]:
            raise IntegrationPackageError("installed distribution and imported versions do not match manifest")
        entry_version = _run([str(harnessctl), "--version"], cwd=temporary, env=environment).stdout.strip()
        if manifest["version"] not in entry_version:
            raise IntegrationPackageError("harnessctl --version does not match manifest")

        target = temporary / "disposable-target"
        module = [str(python), "-I", "-m", "se_harness"]
        _run([*module, "init", str(target), "--project-name", "IntegrationPackage"], cwd=temporary, env=environment)
        _run([*module, "doctor", str(target)], cwd=temporary, env=environment)
        _run([*module, "validate", str(target)], cwd=temporary, env=environment)
        _run([*module, "upgrade", str(target), "--apply"], cwd=temporary, env=environment)
        _run([*module, "doctor", str(target)], cwd=temporary, env=environment)
        _run([*module, "validate", str(target)], cwd=temporary, env=environment)
    after = repository_snapshot(checkout)
    if before != after:
        raise IntegrationPackageError("installed-package verification changed the candidate checkout")
    return {
        "schema": "se-harness-integration-install-result-v1",
        "commit": manifest["commit"],
        "version": manifest["version"],
        "wheel_sha256": manifest["wheel"]["sha256"],
        "platform": platform.system(),
        "checkout_sha256": before,
        "result": "pass",
    }


def _add_expected_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--payload", type=Path, required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--expected-repository", required=True)
    parser.add_argument("--expected-event", choices=("push", "pull_request"), required=True)
    parser.add_argument("--expected-ref", required=True)
    parser.add_argument("--expected-pull-request", type=int)
    parser.add_argument("--expected-run-id", type=int, required=True)
    parser.add_argument("--expected-run-attempt", type=int, required=True)
    parser.add_argument("--expected-workflow", required=True)
    parser.add_argument("--expected-retention-days", type=int, required=True)


def _expected_arguments(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "expected_commit": args.expected_commit,
        "expected_repository": args.expected_repository,
        "expected_event": args.expected_event,
        "expected_ref": args.expected_ref,
        "expected_pull_request": args.expected_pull_request,
        "expected_run_id": args.expected_run_id,
        "expected_run_attempt": args.expected_run_attempt,
        "expected_workflow": args.expected_workflow,
        "expected_retention_days": args.expected_retention_days,
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build", help="build two identical wheels and create one verified payload")
    build.add_argument("--repository", type=Path, required=True)
    build.add_argument("--repository-slug", required=True)
    build.add_argument("--commit", required=True)
    build.add_argument("--event", choices=("push", "pull_request"), required=True)
    build.add_argument("--ref", required=True)
    build.add_argument("--pull-request", type=int)
    build.add_argument("--workflow", required=True)
    build.add_argument("--run-id", type=int, required=True)
    build.add_argument("--run-attempt", type=int, required=True)
    build.add_argument("--retention-days", type=int, required=True)
    build.add_argument("--expect-build-version", required=True)
    build.add_argument("--expect-setuptools-version", required=True)
    build.add_argument("--expect-wheel-version", required=True)
    build.add_argument("--output", type=Path, required=True)

    verify = commands.add_parser("verify", help="independently verify one retained payload")
    _add_expected_arguments(verify)
    install = commands.add_parser("install-test", help="verify and install into a disposable environment")
    _add_expected_arguments(install)
    install.add_argument("--checkout", type=Path, required=True)
    return root


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "build":
            result = build_integration_package(args)
            summary = {
                "schema": SCHEMA,
                "commit": result["commit"],
                "version": result["version"],
                "wheel": result["wheel"],
                "output": str(args.output),
                "result": "pass",
            }
        elif args.command == "verify":
            result = verify_payload(args.payload, **_expected_arguments(args))
            summary = {
                "schema": SCHEMA,
                "commit": result["commit"],
                "version": result["version"],
                "wheel_sha256": result["wheel"]["sha256"],
                "result": "pass",
            }
        else:
            summary = install_test(args.payload, args.checkout, _expected_arguments(args))
    except (IntegrationPackageError, OSError) as exc:
        print(f"integration-package: error: {exc}", file=sys.stderr)
        return 2
    print(canonical_json_bytes(summary).decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
