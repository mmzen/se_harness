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
from urllib.parse import urlparse


EXPECTED_REPOSITORY = "mmzen/se_harness"
SNAPSHOT_SCHEMA = "harness-dashboard-snapshot-v1"
GENERATION_SCHEMA = "harness-dashboard-generation-v1"
PUBLICATION_SCHEMA = "se-harness-pages-publication-v1"
SOURCE_FILES = frozenset({"dashboard-data.json", "generation-summary.json", "index.html"})
PUBLISHED_FIXED_FILES = frozenset({*SOURCE_FILES, "publication-manifest.json"})
CONTENT_FILE_PATTERN = re.compile(r"content/(?P<sha256>[0-9a-f]{64})\.txt")
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
class GovernorDescriptor:
    version: str
    tag: str
    wheel: str
    url: str
    sha256: str
    selected_release_record: str
    selected_candidate_commit: str


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PublicationError(f"invalid JSON file: {path}") from exc
    if not isinstance(value, dict):
        raise PublicationError(f"JSON document must be an object: {path}")
    return value


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


def read_governor(repository: Path) -> GovernorDescriptor:
    path = repository.resolve() / ".self-hosting" / "governor.toml"
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise PublicationError("governance snapshot has no valid governor descriptor") from exc

    keys = (
        "version",
        "tag",
        "wheel",
        "url",
        "sha256",
        "selected_release_record",
        "selected_candidate_commit",
    )
    required = {key: raw.get(key) for key in keys}
    if any(not isinstance(value, str) or not value for value in required.values()):
        raise PublicationError("governor descriptor contains an empty or non-string field")
    version, tag, wheel, url, digest, record, candidate = (required[key] for key in keys)
    assert all(isinstance(value, str) for value in (version, tag, wheel, url, digest, record, candidate))

    if TAG_PATTERN.fullmatch(tag) is None or tag != f"v{version}":
        raise PublicationError("governor version and tag are inconsistent")
    if wheel != f"se_harness-{version}-py3-none-any.whl":
        raise PublicationError("governor wheel name is inconsistent with its version")
    if re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise PublicationError("governor wheel SHA-256 is invalid")
    if RELEASE_RECORD_PATTERN.fullmatch(record) is None:
        raise PublicationError("governor release-record ID is invalid")
    if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", candidate) is None:
        raise PublicationError("governor candidate commit is invalid")
    parsed = urlparse(url)
    expected_path = f"/mmzen/se_harness/releases/download/{tag}/{wheel}"
    if parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.path != expected_path:
        raise PublicationError("governor URL is outside the accepted GitHub release boundary")
    if parsed.params or parsed.query or parsed.fragment:
        raise PublicationError("governor URL must not contain parameters, a query, or a fragment")

    return GovernorDescriptor(
        version=version,
        tag=tag,
        wheel=wheel,
        url=url,
        sha256=digest,
        selected_release_record=record,
        selected_candidate_commit=candidate,
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
    entries = sorted(source.iterdir(), key=lambda path: path.name)
    top_level_names = {path.name for path in entries}
    allowed_top_level = {*SOURCE_FILES, "content"}
    missing = sorted(SOURCE_FILES - top_level_names)
    unexpected = sorted(top_level_names - allowed_top_level)
    if missing or unexpected:
        raise PublicationError(
            f"generated dashboard file set differs from the allowlist; missing={missing}, unexpected={unexpected}"
        )
    payload: dict[str, bytes] = {}
    for name in sorted(SOURCE_FILES):
        path = source / name
        if path.is_symlink() or not path.is_file():
            raise PublicationError(f"generated dashboard source is not a regular file: {name}")
        payload[name] = path.read_bytes()
    content_root = source / "content"
    if content_root.exists():
        if content_root.is_symlink() or not content_root.is_dir():
            raise PublicationError("generated dashboard content must be a real directory")
        for path in sorted(content_root.iterdir(), key=lambda item: item.name):
            relative = f"content/{path.name}"
            if (
                path.is_symlink()
                or not path.is_file()
                or CONTENT_FILE_PATTERN.fullmatch(relative) is None
            ):
                raise PublicationError(
                    f"generated dashboard content differs from the allowlist: {relative}"
                )
            payload[relative] = path.read_bytes()
    if sum(len(value) for value in payload.values()) > MAX_PAYLOAD_BYTES:
        raise PublicationError("generated dashboard exceeds the publication size boundary")
    return payload


def _validated_raw_content(
    snapshot: dict[str, Any],
    payload: dict[str, bytes],
) -> list[str]:
    documents = snapshot.get("evidence_documents", [])
    if not isinstance(documents, list):
        raise PublicationError("snapshot evidence_documents must be an array")
    expected: dict[str, bytes] = {}
    for document in documents:
        if not isinstance(document, dict):
            raise PublicationError("snapshot evidence document must be an object")
        if document.get("state") != "included":
            continue
        raw_path = document.get("raw_path")
        digest = document.get("sha256")
        markdown = document.get("markdown")
        observed_bytes = document.get("bytes")
        if not isinstance(raw_path, str) or CONTENT_FILE_PATTERN.fullmatch(raw_path) is None:
            raise PublicationError("included evidence document has an invalid raw path")
        if not isinstance(digest, str) or raw_path != f"content/{digest}.txt":
            raise PublicationError("included evidence document raw path differs from its digest")
        if not isinstance(markdown, str):
            raise PublicationError("included evidence document has no projected Markdown")
        encoded = markdown.encode("utf-8")
        if _sha256(encoded) != digest or observed_bytes != len(encoded):
            raise PublicationError("included evidence document content metadata is inconsistent")
        previous = expected.get(raw_path)
        if previous is not None and previous != encoded:
            raise PublicationError("included evidence documents collide on one raw path")
        expected[raw_path] = encoded
    actual_paths = sorted(name for name in payload if name.startswith("content/"))
    if set(actual_paths) != set(expected):
        raise PublicationError(
            "generated raw evidence set differs from the canonical snapshot"
        )
    for path, expected_bytes in expected.items():
        if payload[path] != expected_bytes:
            raise PublicationError(f"generated raw evidence differs from its snapshot: {path}")
    return actual_paths


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
        snapshot = json.loads(payload["dashboard-data.json"].decode("utf-8"))
        summary = json.loads(payload["generation-summary.json"].decode("utf-8"))
        generated_html = payload["index.html"].decode("utf-8")
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise PublicationError("generated dashboard output is not valid UTF-8/JSON") from exc
    if not isinstance(snapshot, dict) or snapshot.get("schema") != SNAPSHOT_SCHEMA:
        raise PublicationError("generated dashboard uses an unsupported snapshot schema")
    repository = snapshot.get("repository")
    if not isinstance(repository, dict) or repository.get("valid") is not True:
        raise PublicationError("generated dashboard does not describe a valid repository")
    if repository.get("name") != "governance" or repository.get("revision") != provenance.governance_commit:
        raise PublicationError("generated dashboard repository provenance is not the selected governance snapshot")
    if not isinstance(summary, dict) or summary.get("schema") != GENERATION_SCHEMA:
        raise PublicationError("generated dashboard uses an unsupported generation-summary schema")
    if summary.get("outcome") != "generated-valid" or summary.get("validator_error_count") != 0:
        raise PublicationError("generated dashboard summary is not valid")
    if summary.get("repository_revision") != provenance.governance_commit:
        raise PublicationError("generation summary revision differs from the governance snapshot")
    raw_content_paths = _validated_raw_content(snapshot, payload)

    snapshot_digest = _sha256(payload["dashboard-data.json"])
    generated_dashboard_digest = _sha256(payload["index.html"])
    if summary.get("snapshot_sha256") != snapshot_digest:
        raise PublicationError("generation summary snapshot hash is incorrect")
    if summary.get("dashboard_sha256") != generated_dashboard_digest:
        raise PublicationError("generation summary dashboard hash is incorrect")
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
        "raw_evidence_file_count": len(raw_content_paths),
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
        "snapshot_sha256": snapshot_digest,
        "generated_dashboard_sha256": generated_dashboard_digest,
        "published_dashboard_sha256": published_dashboard_digest,
        "generation_summary_sha256": _sha256(published_summary),
        "raw_evidence_files": raw_content_paths,
    }
    published_payload = {
        "dashboard-data.json": payload["dashboard-data.json"],
        "generation-summary.json": published_summary,
        "index.html": published_html,
        "publication-manifest.json": _json_bytes(manifest),
        **{path: payload[path] for path in raw_content_paths},
    }
    if set(published_payload) != {*PUBLISHED_FIXED_FILES, *raw_content_paths}:
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

    governor = subparsers.add_parser("governor", help="Validate a governance snapshot's governor descriptor.")
    governor.add_argument("--repository", type=Path, required=True)
    governor.add_argument("--output", type=Path)
    governor.add_argument("--github-output", type=Path)

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
        elif args.command == "governor":
            result = read_governor(args.repository)
            _write_result(result, args.output, args.github_output, prefix="governor_")
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
