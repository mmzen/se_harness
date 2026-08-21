#!/usr/bin/env python3
"""Resolve and package the repository-specific SE Harness Pages demonstration."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


EXPECTED_REPOSITORY = "mmzen/se_harness"
BUNDLE_SCHEMA = "harness-dashboard-bundle-v2"
BOOTSTRAP_SCHEMA = "harness-dashboard-bootstrap-v2"
GENERATION_SCHEMA = "harness-dashboard-generation-v2"
PUBLICATION_SCHEMA = "se-harness-pages-publication-v1"
SOURCE_FILES = frozenset({"dashboard-manifest.json", "generation-summary.json", "index.html"})
PUBLISHED_FIXED_FILES = frozenset({*SOURCE_FILES, "publication-manifest.json"})
CONTENT_FILE_PATTERN = re.compile(r"content/(?P<sha256>[0-9a-f]{64})\.txt")
RESOURCE_FILE_PATTERN = re.compile(
    r"(?:data/(?:summary|topology|readiness|artifacts)/[0-9a-f]{64}\.json|content/[0-9a-f]{64}\.txt)"
)
BOOTSTRAP_PATTERN = re.compile(
    r'<script id="harness-dashboard-bootstrap" type="application/json">(?P<payload>.*?)</script>',
    re.DOTALL,
)
TAG_PATTERN = re.compile(r"v(?P<version>0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
RELEASE_RECORD_PATTERN = re.compile(r"RLS-[A-Z0-9]+-[0-9]{3}")
HEX_PATTERN = re.compile(r"[0-9a-f]+")
DEFAULT_REFS = frozenset({"refs/heads/main", "refs/remotes/origin/main"})
MAX_PAYLOAD_BYTES = 100 * 1024 * 1024
WORKSPACE_MARKER = '<div class="workspace">'


class PublicationError(RuntimeError):
    """A bounded publication invariant failed."""


@dataclass(frozen=True)
class ReleaseProvenance:
    repository: str
    tag: str
    version: str
    release_record: str
    release_record_path: str
    candidate_commit: str
    git_object_format: str
    governance_commit: str
    default_head: str


@dataclass(frozen=True)
class EvaluatorDescriptor:
    version: str
    tag: str
    wheel: str
    url: str
    sha256: str
    payload_manifest: str
    payload_sha256: str


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise PublicationError(f"JSON object contains duplicate key: {key}")
        value[key] = item
    return value


def _loads_json_bytes(payload: bytes, *, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise PublicationError(f"invalid UTF-8/JSON document: {label}") from exc
    if not isinstance(value, dict):
        raise PublicationError(f"JSON document must be an object: {label}")
    return value


def _read_json(path: Path) -> dict[str, Any]:
    try:
        return _loads_json_bytes(path.read_bytes(), label=str(path))
    except OSError as exc:
        raise PublicationError(f"invalid JSON file: {path}") from exc


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_json_bytes(value))


def _run_git(repository: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "git command failed"
        raise PublicationError(detail)
    return completed


def _resolve_commit(repository: Path, revision: str) -> str:
    completed = _run_git(repository, "rev-parse", "--verify", f"{revision}^{{commit}}")
    value = completed.stdout.strip().lower()
    if not HEX_PATTERN.fullmatch(value):
        raise PublicationError(f"Git did not resolve a full commit for {revision}")
    return value


def _git_object_format(repository: Path) -> str:
    value = _run_git(repository, "rev-parse", "--show-object-format").stdout.strip().lower()
    if value not in {"sha1", "sha256"}:
        raise PublicationError(f"unsupported Git object format: {value or 'unavailable'}")
    return value


def _object_length(object_format: str) -> int:
    return 40 if object_format == "sha1" else 64


def _validate_full_commit(value: str, object_format: str, label: str) -> str:
    clean = value.strip().lower()
    if len(clean) != _object_length(object_format) or not HEX_PATTERN.fullmatch(clean):
        raise PublicationError(f"{label} must be a full {object_format} commit ID")
    return clean


def _parse_front_matter(text: str, source: str) -> dict[str, Any] | None:
    lines = text.splitlines()
    if not lines or lines[0] != "+++":
        return None
    try:
        end = lines.index("+++", 1)
    except ValueError as exc:
        raise PublicationError(f"unterminated TOML front matter in {source}") from exc
    try:
        metadata = tomllib.loads("\n".join(lines[1:end]))
    except tomllib.TOMLDecodeError as exc:
        raise PublicationError(f"invalid TOML front matter in {source}: {exc}") from exc
    return metadata


def _text_at(repository: Path, commit: str, path: str) -> str | None:
    completed = _run_git(repository, "show", f"{commit}:{path}", check=False)
    if completed.returncode != 0:
        return None
    return completed.stdout


def _metadata_at(repository: Path, commit: str, path: str) -> dict[str, Any] | None:
    text = _text_at(repository, commit, path)
    return None if text is None else _parse_front_matter(text, f"{commit}:{path}")


def _tree_markdown_paths(repository: Path, commit: str) -> list[str]:
    output = _run_git(
        repository,
        "ls-tree",
        "-r",
        "--name-only",
        "--full-tree",
        commit,
        "--",
        "docs/engineering",
    ).stdout
    return sorted(
        line.strip()
        for line in output.splitlines()
        if line.strip().endswith(".md") and line.strip().startswith("docs/engineering/")
    )


def _release_records_at(repository: Path, commit: str) -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    completed = _run_git(
        repository,
        "grep",
        "-l",
        "release_record",
        commit,
        "--",
        "docs/engineering",
        check=False,
    )
    if completed.returncode not in {0, 1}:
        detail = completed.stderr.strip() or "unable to inspect release-record candidates"
        raise PublicationError(detail)
    prefix = f"{commit}:"
    candidate_paths = sorted(
        line[len(prefix) :].strip()
        for line in completed.stdout.splitlines()
        if line.startswith(prefix) and line[len(prefix) :].strip().endswith(".md")
    )
    for path in candidate_paths:
        metadata = _metadata_at(repository, commit, path)
        if metadata is not None and metadata.get("type") == "release_record":
            records.append((path, metadata))
    return records


def _changed_markdown_paths(repository: Path, parent: str | None, commit: str) -> list[str]:
    if parent is None:
        return _tree_markdown_paths(repository, commit)
    output = _run_git(
        repository,
        "diff",
        "--name-only",
        "--diff-filter=ACMRT",
        parent,
        commit,
        "--",
        "docs/engineering",
    ).stdout
    return sorted(
        line.strip()
        for line in output.splitlines()
        if line.strip().endswith(".md") and line.strip().startswith("docs/engineering/")
    )


def _validated_release_record(metadata: dict[str, Any], path: str, tag: str) -> dict[str, str]:
    record_id = metadata.get("id")
    version = metadata.get("version")
    status = metadata.get("status")
    candidate = metadata.get("commit")
    object_format = metadata.get("git_object_format")
    recorded_tag = metadata.get("tag")
    if not isinstance(record_id, str) or RELEASE_RECORD_PATTERN.fullmatch(record_id) is None:
        raise PublicationError(f"invalid release-record ID in {path}")
    if status != "released":
        raise PublicationError(f"release record {record_id} is not released")
    if not isinstance(version, str) or TAG_PATTERN.fullmatch(f"v{version}") is None:
        raise PublicationError(f"release record {record_id} has an invalid version")
    if recorded_tag != tag or tag != f"v{version}":
        raise PublicationError(f"release record {record_id} does not match tag {tag}")
    if object_format not in {"sha1", "sha256"}:
        raise PublicationError(f"release record {record_id} has an unsupported object format")
    if not isinstance(candidate, str):
        raise PublicationError(f"release record {record_id} has no candidate commit")
    candidate = _validate_full_commit(candidate, object_format, f"candidate commit for {record_id}")
    return {
        "id": record_id,
        "version": version,
        "candidate": candidate,
        "object_format": object_format,
        "tag": tag,
    }


def _same_release_binding(metadata: dict[str, Any] | None, expected: dict[str, str]) -> bool:
    return bool(
        metadata
        and metadata.get("type") == "release_record"
        and metadata.get("status") == "released"
        and metadata.get("id") == expected["id"]
        and metadata.get("version") == expected["version"]
        and metadata.get("commit") == expected["candidate"]
        and metadata.get("git_object_format") == expected["object_format"]
        and metadata.get("tag") == expected["tag"]
    )


def resolve_release(
    repository: Path,
    tag: str,
    release_record: str | None = None,
    governance_commit: str | None = None,
    default_ref: str = "refs/remotes/origin/main",
) -> ReleaseProvenance:
    repository = repository.resolve()
    if not (repository / ".git").exists():
        raise PublicationError("repository must be a Git worktree")
    if TAG_PATTERN.fullmatch(tag) is None:
        raise PublicationError("release tag must match vMAJOR.MINOR.PATCH")
    if release_record is not None and RELEASE_RECORD_PATTERN.fullmatch(release_record) is None:
        raise PublicationError("release-record input has an invalid ID")
    if default_ref not in DEFAULT_REFS:
        raise PublicationError("default ref must identify the repository main integration branch")

    object_format = _git_object_format(repository)
    default_head = _resolve_commit(repository, default_ref)
    candidates: list[tuple[str, dict[str, Any]]] = []
    for path, metadata in _release_records_at(repository, default_head):
        if metadata.get("status") == "released" and metadata.get("tag") == tag:
            if release_record is None or metadata.get("id") == release_record:
                candidates.append((path, metadata))
    if len(candidates) != 1:
        raise PublicationError(f"expected exactly one released record for {tag}; found {len(candidates)}")

    record_path, metadata = candidates[0]
    binding = _validated_release_record(metadata, record_path, tag)
    if binding["object_format"] != object_format:
        raise PublicationError("release-record object format differs from the repository")
    if release_record is not None and binding["id"] != release_record:
        raise PublicationError("resolved release record differs from the requested record")

    tag_commit = _resolve_commit(repository, f"refs/tags/{tag}")
    if tag_commit != binding["candidate"]:
        raise PublicationError("Git tag target differs from the released candidate commit")

    transition_commits = [
        line.strip().lower()
        for line in _run_git(
            repository,
            "log",
            "--first-parent",
            "--reverse",
            "--format=%H",
            '-G^status[[:space:]]*=[[:space:]]*"released"[[:space:]]*$',
            default_head,
            "--",
            "docs/engineering",
        ).stdout.splitlines()
        if line.strip()
    ]
    selected: str | None = None
    selected_path: str | None = None
    for commit in transition_commits:
        parent_result = _run_git(repository, "rev-parse", "--verify", f"{commit}^1", check=False)
        parent = parent_result.stdout.strip().lower() if parent_result.returncode == 0 else None
        matching_paths = [
            path
            for path in _changed_markdown_paths(repository, parent, commit)
            if _same_release_binding(_metadata_at(repository, commit, path), binding)
        ]
        if len(matching_paths) > 1:
            raise PublicationError("released record binding is duplicated in one main-history commit")
        if matching_paths:
            selected = commit
            selected_path = matching_paths[0]
            break
    if selected is None:
        raise PublicationError("released record has no integrating commit on main first-parent history")
    assert selected_path is not None

    selected = _validate_full_commit(selected, object_format, "governance commit")
    if governance_commit is not None:
        requested = _validate_full_commit(governance_commit, object_format, "manual governance commit")
        if _resolve_commit(repository, requested) != requested:
            raise PublicationError("manual governance commit does not resolve exactly")
        if requested != selected:
            raise PublicationError("manual governance commit is not the release integration commit")

    return ReleaseProvenance(
        repository=EXPECTED_REPOSITORY,
        tag=tag,
        version=binding["version"],
        release_record=binding["id"],
        release_record_path=selected_path,
        candidate_commit=binding["candidate"],
        git_object_format=object_format,
        governance_commit=selected,
        default_head=default_head,
    )


def read_evaluator(repository: Path) -> EvaluatorDescriptor:
    root = repository.resolve()
    if (root / ".self-hosting" / "governor.toml").exists():
        raise PublicationError("governance snapshot contains a retired active evaluator descriptor")
    config_path = root / ".engineering-harness.toml"
    lock_path = root / ".engineering-harness.lock"
    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise PublicationError("governance snapshot has no valid standard configuration") from exc
    lock = _read_json(lock_path)
    harness = config.get("harness")
    if not isinstance(harness, dict):
        raise PublicationError("standard configuration has no harness table")
    configured_version = harness.get("tool_version")
    if not isinstance(configured_version, str) or not configured_version:
        raise PublicationError("standard configuration has no valid tool version")
    if lock.get("schema") != 3:
        raise PublicationError("publication requires a schema-3 standard evaluator lock")
    if lock.get("hash_algorithm") != "sha256" or lock.get("hash_mode") != "utf8-text-lf-v1":
        raise PublicationError("standard evaluator lock uses unsupported integrity semantics")
    evaluator = lock.get("evaluator")
    if not isinstance(evaluator, dict):
        raise PublicationError("standard evaluator lock has no evaluator identity")
    allowed = {
        "version",
        "payload_manifest",
        "payload_sha256",
        "archive_name",
        "archive_sha256",
    }
    unknown = set(evaluator) - allowed
    if unknown:
        raise PublicationError(f"standard evaluator lock has unknown field: {sorted(unknown)[0]}")
    version = evaluator.get("version")
    payload_manifest = evaluator.get("payload_manifest")
    payload_sha256 = evaluator.get("payload_sha256")
    wheel = evaluator.get("archive_name")
    digest = evaluator.get("archive_sha256")
    if not all(isinstance(value, str) and value for value in (version, payload_manifest, payload_sha256, wheel, digest)):
        raise PublicationError("publication requires complete standard evaluator archive identity")
    assert all(isinstance(value, str) for value in (version, payload_manifest, payload_sha256, wheel, digest))
    if lock.get("tool_version") != version or configured_version != version:
        raise PublicationError("standard configuration, lock, and evaluator versions differ")
    tag = f"v{version}"
    if TAG_PATTERN.fullmatch(tag) is None:
        raise PublicationError("standard evaluator version is not publication-compatible")
    if payload_manifest != "se-harness-installed-payload-v1":
        raise PublicationError("standard evaluator payload manifest is unsupported")
    if re.fullmatch(r"[0-9a-f]{64}", payload_sha256) is None:
        raise PublicationError("standard evaluator payload SHA-256 is invalid")
    if wheel != f"se_harness-{version.replace('-', '_')}-py3-none-any.whl":
        raise PublicationError("standard evaluator wheel name is inconsistent with its version")
    if re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise PublicationError("standard evaluator wheel SHA-256 is invalid")
    url = f"https://github.com/mmzen/se_harness/releases/download/{tag}/{wheel}"

    return EvaluatorDescriptor(
        version=version,
        tag=tag,
        wheel=wheel,
        url=url,
        sha256=digest,
        payload_manifest=payload_manifest,
        payload_sha256=payload_sha256,
    )


def verify_github_release(path: Path, expected_tag: str) -> None:
    metadata = _read_json(path)
    if metadata.get("tagName") != expected_tag:
        raise PublicationError("GitHub Release tag differs from the requested tag")
    if metadata.get("isDraft") is not False:
        raise PublicationError("GitHub Release must not be a draft")
    if metadata.get("isPrerelease") is not False:
        raise PublicationError("prerelease dashboards are outside this publication workflow")


def _validated_provenance(path: Path) -> ReleaseProvenance:
    payload = _read_json(path)
    try:
        provenance = ReleaseProvenance(**payload)
    except TypeError as exc:
        raise PublicationError("publication provenance has missing or unexpected fields") from exc
    if provenance.repository != EXPECTED_REPOSITORY:
        raise PublicationError("publication provenance identifies another repository")
    if TAG_PATTERN.fullmatch(provenance.tag) is None or provenance.tag != f"v{provenance.version}":
        raise PublicationError("publication provenance has an invalid release tag")
    if RELEASE_RECORD_PATTERN.fullmatch(provenance.release_record) is None:
        raise PublicationError("publication provenance has an invalid release-record ID")
    _validate_full_commit(provenance.candidate_commit, provenance.git_object_format, "publication candidate commit")
    _validate_full_commit(provenance.governance_commit, provenance.git_object_format, "publication governance commit")
    return provenance


def _source_payload(source: Path) -> dict[str, bytes]:
    if not source.is_dir() or source.is_symlink():
        raise PublicationError("generated dashboard source must be a real directory")
    payload: dict[str, bytes] = {}
    for path in sorted(source.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(source).as_posix()
        if path.is_symlink():
            raise PublicationError(f"generated dashboard source contains a symbolic link: {relative}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise PublicationError(f"generated dashboard source is not a regular file: {relative}")
        payload[relative] = path.read_bytes()
    if sum(len(value) for value in payload.values()) > MAX_PAYLOAD_BYTES:
        raise PublicationError("generated dashboard exceeds the publication size boundary")
    return payload


def _descriptor(value: Any, *, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PublicationError(f"{label} must be an object")
    path = value.get("path")
    digest = value.get("sha256")
    size = value.get("bytes")
    role = value.get("role")
    schema = value.get("schema")
    if (
        not isinstance(path, str)
        or RESOURCE_FILE_PATTERN.fullmatch(path) is None
        or not isinstance(digest, str)
        or not re.fullmatch(r"[0-9a-f]{64}", digest)
        or not isinstance(size, int)
        or isinstance(size, bool)
        or size < 0
        or not isinstance(role, str)
        or not role
        or not isinstance(schema, str)
        or not schema
    ):
        raise PublicationError(f"{label} is invalid")
    if Path(path).stem != digest:
        raise PublicationError(f"{label} path differs from its digest")
    return value


def _validated_bundle(manifest: dict[str, Any], payload: dict[str, bytes]) -> list[str]:
    if manifest.get("schema") != BUNDLE_SCHEMA:
        raise PublicationError("generated dashboard uses an unsupported bundle schema")
    repository = manifest.get("repository")
    if not isinstance(repository, dict) or repository.get("valid") is not True:
        raise PublicationError("generated dashboard does not describe a valid repository")
    resources = manifest.get("resources")
    if not isinstance(resources, list):
        raise PublicationError("bundle resources must be an array")
    declared: dict[str, dict[str, Any]] = {}
    for index, candidate in enumerate(resources):
        descriptor = _descriptor(candidate, label=f"bundle resource {index}")
        path = descriptor["path"]
        role = descriptor["role"]
        schema = descriptor["schema"]
        accepted = {
            "summary": ("harness-dashboard-summary-v2", "data/summary/"),
            "topology": ("harness-dashboard-topology-v2", "data/topology/"),
            "readiness": ("harness-dashboard-readiness-v2", "data/readiness/"),
            "artifact": ("harness-dashboard-artifact-v2", "data/artifacts/"),
            "evidence": ("utf8-markdown-v1", "content/"),
        }.get(role)
        if accepted is None or schema != accepted[0] or not path.startswith(accepted[1]):
            raise PublicationError(f"bundle resource role, schema, or path is unsupported: {path}")
        if path in declared:
            raise PublicationError(f"bundle resource path is duplicated: {path}")
        declared[path] = descriptor
    expected_files = {*SOURCE_FILES, *declared}
    if set(payload) != expected_files:
        missing = sorted(expected_files - set(payload))
        unexpected = sorted(set(payload) - expected_files)
        raise PublicationError(
            f"generated dashboard file set differs from its manifest; missing={missing}, unexpected={unexpected}"
        )
    for path, descriptor in declared.items():
        content = payload[path]
        if len(content) != descriptor["bytes"] or _sha256(content) != descriptor["sha256"]:
            raise PublicationError(f"bundle resource differs from its descriptor: {path}")
        if descriptor["schema"] == "utf8-markdown-v1":
            try:
                content.decode("utf-8")
            except UnicodeError as exc:
                raise PublicationError(f"evidence resource is not UTF-8: {path}") from exc
            if descriptor["role"] != "evidence" or CONTENT_FILE_PATTERN.fullmatch(path) is None:
                raise PublicationError(f"evidence resource role or path is invalid: {path}")
            continue
        try:
            value = _loads_json_bytes(content, label=path)
        except PublicationError as exc:
            raise PublicationError(f"JSON resource is invalid: {path}") from exc
        if not isinstance(value, dict) or value.get("schema") != descriptor["schema"]:
            raise PublicationError(f"JSON resource schema differs from its descriptor: {path}")
        if descriptor["role"] == "artifact":
            artifact_id = descriptor.get("artifact_id")
            artifact = value.get("artifact")
            if (
                not isinstance(artifact_id, str)
                or not isinstance(artifact, dict)
                or artifact.get("id") != artifact_id
            ):
                raise PublicationError(f"artifact resource identity is invalid: {path}")
    entrypoints = manifest.get("entrypoints")
    if not isinstance(entrypoints, dict):
        raise PublicationError("bundle entrypoints must be an object")
    for role in ("summary", "topology", "readiness"):
        descriptor = _descriptor(entrypoints.get(role), label=f"bundle {role} entrypoint")
        if descriptor.get("role") != role or declared.get(descriptor["path"]) != descriptor:
            raise PublicationError(f"bundle {role} entrypoint is not declared exactly")
    return sorted(declared)


def _validated_bootstrap(generated_html: str, manifest_bytes: bytes, revision: str) -> None:
    matches = list(BOOTSTRAP_PATTERN.finditer(generated_html))
    if len(matches) != 1:
        raise PublicationError("generated dashboard has no unique bootstrap descriptor")
    try:
        bootstrap = json.loads(
            matches[0].group("payload"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except json.JSONDecodeError as exc:
        raise PublicationError("generated dashboard bootstrap is invalid JSON") from exc
    expected = {
        "path": "dashboard-manifest.json",
        "bytes": len(manifest_bytes),
        "sha256": _sha256(manifest_bytes),
    }
    if (
        not isinstance(bootstrap, dict)
        or bootstrap.get("schema") != BOOTSTRAP_SCHEMA
        or bootstrap.get("bundle_schema") != BUNDLE_SCHEMA
        or bootstrap.get("repository_revision") != revision
        or bootstrap.get("manifest") != expected
    ):
        raise PublicationError("generated dashboard bootstrap differs from its manifest")


def _demonstration_notice(provenance: ReleaseProvenance) -> str:
    release_url = f"https://github.com/{EXPECTED_REPOSITORY}/releases/tag/{provenance.tag}"
    return (
        '<aside role="note" aria-label="SE Harness demonstration notice" '
        'style="margin:12px 28px 0;padding:10px 14px;border:1px solid #bfdbfe;'
        'background:#eff6ff;color:#1e3a8a;font:13px/1.45 system-ui,sans-serif">'
        '<strong>SE Harness development demonstration.</strong> '
        'This public Explorer is a derived, read-only view; repository artifacts and accountable '
        'human decisions remain authoritative. Included artifact bodies and retained evidence are public. '
        f'<a href="{html.escape(release_url, quote=True)}">Release {html.escape(provenance.tag)}</a> '
        f'uses candidate <code>{html.escape(provenance.candidate_commit[:12])}</code> and governance '
        f'snapshot <code>{html.escape(provenance.governance_commit[:12])}</code>.'
        "</aside>"
    )


def package_dashboard(source: Path, destination: Path, provenance_path: Path) -> dict[str, Any]:
    provenance = _validated_provenance(provenance_path)
    payload = _source_payload(source.resolve())
    try:
        bundle_manifest = _loads_json_bytes(payload["dashboard-manifest.json"], label="dashboard-manifest.json")
        summary = _loads_json_bytes(payload["generation-summary.json"], label="generation-summary.json")
        generated_html = payload["index.html"].decode("utf-8")
    except (KeyError, UnicodeError) as exc:
        raise PublicationError("generated dashboard output is not valid UTF-8/JSON") from exc
    if not isinstance(bundle_manifest, dict):
        raise PublicationError("generated dashboard manifest must be an object")
    resource_paths = _validated_bundle(bundle_manifest, payload)
    repository = bundle_manifest.get("repository")
    if repository.get("name") != "governance" or repository.get("revision") != provenance.governance_commit:
        raise PublicationError("generated dashboard repository provenance is not the selected governance snapshot")
    if repository.get("git_object_format") != provenance.git_object_format:
        raise PublicationError("generated dashboard Git object format differs from release provenance")
    if not isinstance(summary, dict) or summary.get("schema") != GENERATION_SCHEMA:
        raise PublicationError("generated dashboard uses an unsupported generation-summary schema")
    if summary.get("outcome") != "generated-valid" or summary.get("validator_error_count") != 0:
        raise PublicationError("generated dashboard summary is not valid")
    if summary.get("repository_revision") != provenance.governance_commit:
        raise PublicationError("generation summary revision differs from the governance snapshot")

    manifest_digest = _sha256(payload["dashboard-manifest.json"])
    generated_dashboard_digest = _sha256(payload["index.html"])
    if summary.get("bundle_schema") != BUNDLE_SCHEMA or summary.get("manifest_sha256") != manifest_digest:
        raise PublicationError("generation summary bundle manifest hash is incorrect")
    if summary.get("dashboard_sha256") != generated_dashboard_digest:
        raise PublicationError("generation summary dashboard hash is incorrect")
    if summary.get("resource_count") != len(resource_paths):
        raise PublicationError("generation summary resource count is incorrect")
    _validated_bootstrap(generated_html, payload["dashboard-manifest.json"], provenance.governance_commit)
    if generated_html.count(WORKSPACE_MARKER) != 1:
        raise PublicationError("generated dashboard has no unique publication notice boundary")

    published_html = generated_html.replace(
        WORKSPACE_MARKER,
        WORKSPACE_MARKER + _demonstration_notice(provenance),
        1,
    ).encode("utf-8")
    published_dashboard_digest = _sha256(published_html)
    summary["dashboard_sha256"] = published_dashboard_digest
    summary["publication"] = {
        "schema": PUBLICATION_SCHEMA,
        "derived_non_authoritative": True,
        "release_tag": provenance.tag,
        "release_record": provenance.release_record,
        "candidate_commit": provenance.candidate_commit,
        "governance_commit": provenance.governance_commit,
        "generated_dashboard_sha256": generated_dashboard_digest,
        "published_dashboard_sha256": published_dashboard_digest,
        "resource_file_count": len(resource_paths),
        "raw_evidence_file_count": sum(1 for path in resource_paths if path.startswith("content/")),
    }
    published_summary = _json_bytes(summary)
    manifest = {
        "schema": PUBLICATION_SCHEMA,
        "repository": provenance.repository,
        "derived_non_authoritative": True,
        "release_tag": provenance.tag,
        "version": provenance.version,
        "release_record": provenance.release_record,
        "candidate_commit": provenance.candidate_commit,
        "governance_commit": provenance.governance_commit,
        "bundle_manifest_sha256": manifest_digest,
        "generated_dashboard_sha256": generated_dashboard_digest,
        "published_dashboard_sha256": published_dashboard_digest,
        "generation_summary_sha256": _sha256(published_summary),
        "resource_files": resource_paths,
    }
    published_payload = {
        "dashboard-manifest.json": payload["dashboard-manifest.json"],
        "generation-summary.json": published_summary,
        "index.html": published_html,
        "publication-manifest.json": _json_bytes(manifest),
        **{path: payload[path] for path in resource_paths},
    }
    if set(published_payload) != {*PUBLISHED_FIXED_FILES, *resource_paths}:
        raise PublicationError("internal publication payload differs from the allowlist")

    destination = destination.resolve()
    if destination.exists():
        raise PublicationError("publication destination must not already exist")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent))
    try:
        for name, content in published_payload.items():
            target = temporary.joinpath(*name.split("/"))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        temporary.replace(destination)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return manifest


def _append_github_outputs(path: Path, values: dict[str, Any], prefix: str = "") -> None:
    lines: list[str] = []
    for key, value in sorted(values.items()):
        if not isinstance(value, (str, int, bool)):
            continue
        text = str(value).lower() if isinstance(value, bool) else str(value)
        if "\n" in text or "\r" in text:
            raise PublicationError(f"GitHub output {key} contains a line break")
        lines.append(f"{prefix}{key}={text}\n")
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.writelines(lines)


def _write_result(value: Any, output: Path | None, github_output: Path | None, prefix: str = "") -> None:
    payload = asdict(value) if hasattr(value, "__dataclass_fields__") else value
    if output is not None:
        _write_json(output, payload)
    if github_output is not None:
        if not isinstance(payload, dict):
            raise PublicationError("GitHub outputs require an object result")
        _append_github_outputs(github_output, payload, prefix)
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve = subparsers.add_parser("resolve", help="Resolve immutable release and governance provenance.")
    resolve.add_argument("--repository", type=Path, required=True)
    resolve.add_argument("--tag", required=True)
    resolve.add_argument("--release-record")
    resolve.add_argument("--governance-commit")
    resolve.add_argument("--default-ref", default="refs/remotes/origin/main")
    resolve.add_argument("--output", type=Path)
    resolve.add_argument("--github-output", type=Path)

    evaluator = subparsers.add_parser("evaluator", help="Resolve a governance snapshot's standard evaluator identity.")
    evaluator.add_argument("--repository", type=Path, required=True)
    evaluator.add_argument("--output", type=Path)
    evaluator.add_argument("--github-output", type=Path)

    github_release = subparsers.add_parser(
        "verify-github-release",
        help="Verify bounded GitHub Release metadata returned by gh.",
    )
    github_release.add_argument("--metadata", type=Path, required=True)
    github_release.add_argument("--tag", required=True)

    package = subparsers.add_parser("package", help="Prepare the exact public Pages payload.")
    package.add_argument("--source", type=Path, required=True)
    package.add_argument("--destination", type=Path, required=True)
    package.add_argument("--provenance", type=Path, required=True)
    package.add_argument("--output", type=Path)
    package.add_argument("--github-output", type=Path)

    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        if args.command == "resolve":
            result = resolve_release(
                args.repository,
                args.tag,
                release_record=args.release_record,
                governance_commit=args.governance_commit,
                default_ref=args.default_ref,
            )
            _write_result(result, args.output, args.github_output)
        elif args.command == "evaluator":
            result = read_evaluator(args.repository)
            _write_result(result, args.output, args.github_output, prefix="evaluator_")
        elif args.command == "verify-github-release":
            verify_github_release(args.metadata, args.tag)
            print(f"GitHub Release metadata: PASS | tag={args.tag}")
        elif args.command == "package":
            result = package_dashboard(args.source, args.destination, args.provenance)
            _write_result(result, args.output, args.github_output)
        else:  # pragma: no cover - argparse owns this boundary
            raise PublicationError(f"unsupported command: {args.command}")
        return 0
    except (OSError, PublicationError, subprocess.SubprocessError) as exc:
        print(f"dashboard publication: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
