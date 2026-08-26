#!/usr/bin/env python3
"""Resolve, reconcile, and report the deterministic SE Harness release last mile."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
REPOSITORY_ROOT = SCRIPT_DIRECTORY.parents[1]
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

import publish_dashboard as dashboard
from repository_tools.json_bytes import pretty_json_bytes, read_json_object, sha256_file
from repository_tools.release_build import load_build_recipe_at
from repository_tools.release_distribution import ReleaseDistribution, validate_distribution_block


RESULT_SCHEMA = "se-harness-release-result/v1"
RELEASE_RECORD_PATTERN = re.compile(r"RLS-[A-Z0-9-]+-[0-9]{3}")
STAGE_STATES = frozenset({"not_run", "absent", "exact", "partial", "mismatched", "created", "failed"})


class ReleaseError(RuntimeError):
    """A release orchestration invariant failed."""


@dataclass(frozen=True)
class ReleasePlan:
    schema: str
    repository: str
    release_record: str
    release_record_path: str
    governance_commit: str
    candidate_commit: str
    git_object_format: str
    version: str
    tag: str
    released_at: str
    release_contract: str
    verification_records: tuple[str, ...]
    released_work: tuple[str, ...]
    source_date_epoch: int
    wheel: str
    wheel_sha256: str
    sdist: str
    sdist_sha256: str
    checksums: str
    checksums_sha256: str
    source_manifest_sha256: str
    distribution_schema: int = 1
    build_recipe_schema: str | None = None
    build_recipe: str | None = None
    build_recipe_sha256: str | None = None
    evaluator_evidence_path: str | None = None
    evaluator_evidence_sha256: str | None = None


def _json_bytes(value: Any) -> bytes:
    return pretty_json_bytes(value)


def _read_json(path: Path) -> dict[str, Any]:
    return read_json_object(path, error=ReleaseError)


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_json_bytes(value))


def _sha256_file(path: Path) -> str:
    return sha256_file(path, error=ReleaseError, label=f"release file {path}")


def _run_git(repository: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=False,
        capture_output=True,
    )
    if check and completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", "replace").strip() or "Git command failed"
        raise ReleaseError(detail)
    return completed


def _git_text(repository: Path, *arguments: str) -> str:
    return _run_git(repository, *arguments).stdout.decode("utf-8", "strict").strip()


def _relations(metadata: dict[str, Any], name: str, *, exactly_one: bool = False) -> tuple[str, ...]:
    relations = metadata.get("relations")
    value = relations.get(name) if isinstance(relations, dict) else None
    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item for item in value):
        raise ReleaseError(f"release record relation {name} must be a non-empty string array")
    normalized = tuple(sorted(value))
    if len(set(normalized)) != len(normalized):
        raise ReleaseError(f"release record relation {name} contains duplicates")
    if exactly_one and len(normalized) != 1:
        raise ReleaseError(f"release record relation {name} must contain exactly one artifact")
    return normalized


def _catalog_at(repository: Path, commit: str) -> dict[str, tuple[str, dict[str, Any]]]:
    catalog: dict[str, tuple[str, dict[str, Any]]] = {}
    for path in dashboard._tree_markdown_paths(repository, commit):
        metadata = dashboard._metadata_at(repository, commit, path)
        if metadata is None:
            continue
        artifact_id = metadata.get("id")
        if not isinstance(artifact_id, str):
            continue
        if artifact_id in catalog:
            raise ReleaseError(f"duplicate artifact ID at trusted main head: {artifact_id}")
        catalog[artifact_id] = (path, metadata)
    return catalog


def _integration_commit(
    repository: Path,
    default_head: str,
    binding: dict[str, str],
) -> tuple[str, str]:
    commits = [
        line.strip().lower()
        for line in _git_text(
            repository,
            "log",
            "--first-parent",
            "--reverse",
            "--format=%H",
            '-G^status[[:space:]]*=[[:space:]]*"released"[[:space:]]*$',
            default_head,
            "--",
            "docs/engineering",
        ).splitlines()
        if line.strip()
    ]
    for commit in commits:
        parent_result = _run_git(repository, "rev-parse", "--verify", f"{commit}^1", check=False)
        parent = parent_result.stdout.decode("utf-8", "replace").strip().lower() if parent_result.returncode == 0 else None
        matching_paths = [
            path
            for path in dashboard._changed_markdown_paths(repository, parent, commit)
            if dashboard._same_release_binding(dashboard._metadata_at(repository, commit, path), binding)
        ]
        if len(matching_paths) > 1:
            raise ReleaseError("released record binding is duplicated in one main-history commit")
        if matching_paths:
            return commit, matching_paths[0]
    raise ReleaseError("released record has no first-parent integration commit")


def _source_manifest_sha256(repository: Path, candidate: str) -> str:
    payload = _run_git(repository, "ls-tree", "-r", "-z", "--full-tree", candidate).stdout
    if not payload:
        raise ReleaseError("candidate source manifest is empty")
    return hashlib.sha256(payload).hexdigest()


def resolve_plan(
    repository: Path,
    release_record: str,
    default_ref: str = "refs/remotes/origin/main",
) -> ReleasePlan:
    repository = repository.resolve()
    if RELEASE_RECORD_PATTERN.fullmatch(release_record) is None:
        raise ReleaseError("release_record must be a canonical RLS identifier")
    if default_ref not in dashboard.DEFAULT_REFS:
        raise ReleaseError("default ref must identify main")
    object_format = dashboard._git_object_format(repository)
    default_head = dashboard._resolve_commit(repository, default_ref)
    selected = [
        (path, metadata)
        for path, metadata in dashboard._release_records_at(repository, default_head)
        if metadata.get("id") == release_record
    ]
    if len(selected) != 1:
        raise ReleaseError(f"expected exactly one {release_record} at main head; found {len(selected)}")
    _, metadata = selected[0]
    version = metadata.get("version")
    tag = metadata.get("tag")
    if not isinstance(version, str) or not isinstance(tag, str):
        raise ReleaseError("released record must declare version and tag")
    binding = dashboard._validated_release_record(metadata, selected[0][0], tag)
    if tag != f"v{version}" or binding["object_format"] != object_format:
        raise ReleaseError("released record version, tag, or object format is inconsistent")
    candidate = binding["candidate"]
    if dashboard._resolve_commit(repository, candidate) != candidate:
        raise ReleaseError("candidate commit does not resolve exactly")
    governance_commit, record_path = _integration_commit(repository, default_head, binding)
    evaluator_binding = dashboard._validated_evaluator_binding(
        repository,
        default_head,
        metadata,
        lock_commit=governance_commit,
    )
    catalog = _catalog_at(repository, default_head)
    verification_records = _relations(metadata, "includes_verification")
    released_work = _relations(metadata, "releases_work")
    release_contract = _relations(metadata, "satisfies", exactly_one=True)[0]
    for verification_id in verification_records:
        item = catalog.get(verification_id)
        if item is None or item[1].get("type") != "verification_record":
            raise ReleaseError(f"included verification record is missing: {verification_id}")
        verification = item[1]
        if verification.get("status") not in {"verified", "released"}:
            raise ReleaseError(f"included verification record is not assured: {verification_id}")
        if verification.get("commit") != candidate or verification.get("git_object_format") != object_format:
            raise ReleaseError(f"verification record candidate differs from the RLS: {verification_id}")
    try:
        distribution = validate_distribution_block(metadata.get("distribution"), version)
    except Exception as exc:
        raise ReleaseError(f"release record has no usable distribution provenance: {exc}") from exc
    epoch_text = _git_text(repository, "show", "-s", "--format=%ct", candidate)
    if not epoch_text.isdigit() or int(epoch_text) != distribution.source_date_epoch:
        raise ReleaseError("distribution epoch differs from candidate commit time")
    source_manifest = _source_manifest_sha256(repository, candidate)
    if source_manifest != distribution.source_manifest_sha256:
        raise ReleaseError("distribution source manifest differs from the candidate tree")
    if distribution.schema == 2:
        try:
            recipe = load_build_recipe_at(
                repository,
                candidate,
                path=distribution.build_recipe or "",
                expected_sha256=distribution.build_recipe_sha256,
            )
        except (OSError, RuntimeError) as exc:
            raise ReleaseError(f"distribution build recipe differs from the candidate tree: {exc}") from exc
        if recipe.value["schema"] != distribution.build_recipe_schema:
            raise ReleaseError("distribution build recipe schema differs from the candidate tree")
    released_at = metadata.get("released_at")
    if not isinstance(released_at, str) or not released_at:
        raise ReleaseError("released record has no released_at timestamp")
    return ReleasePlan(
        schema="se-harness-release-plan/v2",
        repository=dashboard.EXPECTED_REPOSITORY,
        release_record=release_record,
        release_record_path=record_path,
        governance_commit=governance_commit,
        candidate_commit=candidate,
        git_object_format=object_format,
        version=version,
        tag=tag,
        released_at=released_at,
        release_contract=release_contract,
        verification_records=verification_records,
        released_work=released_work,
        source_date_epoch=distribution.source_date_epoch,
        wheel=distribution.wheel,
        wheel_sha256=distribution.wheel_sha256,
        sdist=distribution.sdist,
        sdist_sha256=distribution.sdist_sha256,
        checksums=distribution.checksums,
        checksums_sha256=distribution.checksums_sha256,
        source_manifest_sha256=distribution.source_manifest_sha256,
        distribution_schema=distribution.schema,
        build_recipe_schema=distribution.build_recipe_schema,
        build_recipe=distribution.build_recipe,
        build_recipe_sha256=distribution.build_recipe_sha256,
        evaluator_evidence_path=evaluator_binding["path"],
        evaluator_evidence_sha256=evaluator_binding["sha256"],
    )


def read_plan(path: Path) -> ReleasePlan:
    value = _read_json(path)
    fields = set(ReleasePlan.__dataclass_fields__)
    if set(value) != fields:
        raise ReleaseError("release plan field set is not canonical")
    if value.get("schema") != "se-harness-release-plan/v2":
        raise ReleaseError("release plan schema must be se-harness-release-plan/v2")
    for key in ("verification_records", "released_work"):
        if not isinstance(value.get(key), list):
            raise ReleaseError(f"release plan {key} must be an array")
        value[key] = tuple(value[key])
    try:
        return ReleasePlan(**value)
    except TypeError as exc:
        raise ReleaseError("release plan has invalid field types") from exc


def verify_bundle(plan: ReleasePlan, directory: Path) -> dict[str, Any]:
    expected = {plan.wheel, plan.sdist, plan.checksums}
    try:
        actual = {item.name for item in directory.iterdir() if item.is_file()}
    except OSError as exc:
        raise ReleaseError("release bundle directory is not readable") from exc
    if actual != expected:
        raise ReleaseError(f"release bundle file set differs: expected {sorted(expected)}, found {sorted(actual)}")
    hashes = {
        plan.wheel: _sha256_file(directory / plan.wheel),
        plan.sdist: _sha256_file(directory / plan.sdist),
        plan.checksums: _sha256_file(directory / plan.checksums),
    }
    expected_hashes = {
        plan.wheel: plan.wheel_sha256,
        plan.sdist: plan.sdist_sha256,
        plan.checksums: plan.checksums_sha256,
    }
    if hashes != expected_hashes:
        raise ReleaseError("release bundle hashes differ from the released record")
    expected_manifest = (
        f"{plan.wheel_sha256}  {plan.wheel}\n"
        f"{plan.sdist_sha256}  {plan.sdist}\n"
    ).encode("utf-8")
    if (directory / plan.checksums).read_bytes() != expected_manifest:
        raise ReleaseError("SHA256SUMS bytes are not canonical")
    return {"state": "exact", "files": sorted(expected), "hashes": hashes}


def verify_build_manifest(plan: ReleasePlan, value: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "schema": f"se-harness-release-bundle/v{plan.distribution_schema}",
        "version": plan.version,
        "commit": plan.candidate_commit,
        "git_object_format": plan.git_object_format,
        "source_date_epoch": plan.source_date_epoch,
        "wheel": plan.wheel,
        "wheel_sha256": plan.wheel_sha256,
        "sdist": plan.sdist,
        "sdist_sha256": plan.sdist_sha256,
        "checksums": plan.checksums,
        "checksums_sha256": plan.checksums_sha256,
        "checksums_content": (
            f"{plan.wheel_sha256}  {plan.wheel}\n"
            f"{plan.sdist_sha256}  {plan.sdist}\n"
        ),
        "source_manifest_sha256": plan.source_manifest_sha256,
    }
    if plan.distribution_schema == 2:
        expected.update(
            {
                "build_recipe_schema": plan.build_recipe_schema,
                "build_recipe": plan.build_recipe,
                "build_recipe_sha256": plan.build_recipe_sha256,
            }
        )
    if value != expected:
        differing = sorted(key for key in set(value) | set(expected) if value.get(key) != expected.get(key))
        raise ReleaseError(f"rebuilt distribution manifest differs from the released record: {', '.join(differing)}")
    return {"state": "exact", "source_manifest_sha256": plan.source_manifest_sha256}


REHEARSAL_STATUSES = frozenset({"ready", "released"})


def _version_key(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split("."))


def select_rehearsal_record(repository: Path, requested: str | None) -> dict[str, Any]:
    """Choose the record the publication rehearsal qualifies in release-record mode.

    Candidates are ready or released records whose distribution is schema 2 (recipe-bound):
    the one release-qualification definition replays a bound recipe, so a schema-1 record
    has no rehearsal subject. An explicitly requested record must be one of them; otherwise
    the newest by version is chosen, and an empty selection is a legitimate outcome that the
    caller reports rather than a failure.
    """

    import tomllib

    candidates: list[tuple[tuple[int, ...], str, str]] = []
    for path in sorted((repository / "docs/engineering").glob("*/releases/RLS-*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("+++\n") or "\n+++\n" not in text[4:]:
            continue
        try:
            front = tomllib.loads(text[4:].split("\n+++\n", 1)[0])
        except tomllib.TOMLDecodeError as exc:
            raise ReleaseError(f"invalid release record front matter: {path}") from exc
        status = front.get("status")
        distribution = front.get("distribution")
        version = front.get("version")
        if status not in REHEARSAL_STATUSES or not isinstance(distribution, dict) or distribution.get("schema") != 2:
            continue
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            continue
        candidates.append((_version_key(version), str(front.get("id")), str(status)))
    by_id = {identifier: status for _, identifier, status in candidates}
    if requested:
        if requested not in by_id:
            raise ReleaseError(
                f"{requested} is not a ready or released schema-2 record; rehearsable records: {sorted(by_id) or 'none'}"
            )
        return {"release_record": requested, "status": by_id[requested], "reason": "requested"}
    if not candidates:
        return {"release_record": "", "status": "", "reason": "no ready or released schema-2 record exists; only the candidate is rehearsed"}
    _, identifier, status = max(candidates)
    return {"release_record": identifier, "status": status, "reason": "newest ready or released schema-2 record"}


def classify_github(plan: ReleasePlan, metadata: dict[str, Any]) -> dict[str, Any]:
    if metadata.get("absent") is True:
        return {"state": "absent", "draft": None, "files": []}
    if metadata.get("tagName") != plan.tag or metadata.get("isPrerelease") is not False:
        return {"state": "mismatched", "draft": metadata.get("isDraft"), "files": []}
    assets = metadata.get("assets")
    if not isinstance(assets, list):
        raise ReleaseError("GitHub Release metadata must contain an assets array")
    expected = {plan.wheel: plan.wheel_sha256, plan.sdist: plan.sdist_sha256, plan.checksums: plan.checksums_sha256}
    observed: dict[str, str] = {}
    for asset in assets:
        if not isinstance(asset, dict) or not isinstance(asset.get("name"), str):
            return {"state": "mismatched", "draft": metadata.get("isDraft"), "files": []}
        digest = asset.get("digest")
        if not isinstance(digest, str) or not digest.startswith("sha256:"):
            return {"state": "mismatched", "draft": metadata.get("isDraft"), "files": sorted(observed)}
        observed[asset["name"]] = digest.removeprefix("sha256:")
    if any(name not in expected for name in observed) or any(observed.get(name) not in {None, digest} for name, digest in expected.items()):
        state = "mismatched"
    elif observed == expected:
        state = "exact"
    else:
        state = "partial"
    return {"state": state, "draft": metadata.get("isDraft"), "files": sorted(observed)}


def release_notes(plan: ReleasePlan) -> str:
    work = ", ".join(f"`{item}`" for item in plan.released_work)
    records = ", ".join(f"`{item}`" for item in plan.verification_records)
    return (
        f"# SE Harness {plan.version}\n\n"
        f"Released from candidate `{plan.candidate_commit}` under `{plan.release_record}`.\n\n"
        f"Verification: {records}\n\nReleased work: {work}\n\n"
        f"Install with `python -m pip install se-harness=={plan.version}`.\n"
    )


def release_result(plan: ReleasePlan, stages: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for name in ("resolution", "qualification", "github", "pypi", "pages", "public_install"):
        value = stages.get(name, {"state": "not_run"})
        if not isinstance(value, dict) or value.get("state") not in STAGE_STATES:
            raise ReleaseError(f"result stage {name} has an invalid state")
        normalized[name] = value
    return {
        "schema": RESULT_SCHEMA,
        "authority": "derived operational evidence; no formal lifecycle transition",
        "release": asdict(plan),
        "stages": normalized,
    }


def _github_outputs(path: Path, value: dict[str, Any]) -> None:
    lines = []
    for key, item in sorted(value.items()):
        if isinstance(item, (tuple, list, dict)):
            text = json.dumps(item, separators=(",", ":"), sort_keys=True)
        elif isinstance(item, bool):
            text = str(item).lower()
        elif item is None:
            text = ""
        else:
            text = str(item)
        if "\n" in text or "\r" in text:
            raise ReleaseError(f"GitHub output contains a line break: {key}")
        lines.append(f"{key}={text}\n")
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.writelines(lines)


def _emit(value: Any, output: Path | None, github_output: Path | None) -> None:
    payload = asdict(value) if hasattr(value, "__dataclass_fields__") else value
    if output is not None:
        _write_json(output, payload)
    if github_output is not None:
        if not isinstance(payload, dict):
            raise ReleaseError("GitHub outputs require an object")
        _github_outputs(github_output, payload)
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    resolve = commands.add_parser("resolve")
    resolve.add_argument("--repository", type=Path, required=True)
    resolve.add_argument("--release-record", required=True)
    resolve.add_argument("--default-ref", default="refs/remotes/origin/main")
    resolve.add_argument("--output", type=Path)
    resolve.add_argument("--github-output", type=Path)
    verify = commands.add_parser("verify-bundle")
    verify.add_argument("--plan", type=Path, required=True)
    verify.add_argument("--directory", type=Path, required=True)
    verify.add_argument("--output", type=Path)
    build_manifest = commands.add_parser("verify-build-manifest")
    build_manifest.add_argument("--plan", type=Path, required=True)
    build_manifest.add_argument("--manifest", type=Path, required=True)
    build_manifest.add_argument("--output", type=Path)
    select = commands.add_parser("select-rehearsal-record")
    select.add_argument("--repository", type=Path, required=True)
    select.add_argument("--release-record", default="")
    select.add_argument("--github-output", type=Path)
    select.add_argument("--summary", type=Path)
    github = commands.add_parser("classify-github")
    github.add_argument("--plan", type=Path, required=True)
    github.add_argument("--metadata", type=Path, required=True)
    github.add_argument("--output", type=Path)
    github.add_argument("--github-output", type=Path)
    notes = commands.add_parser("notes")
    notes.add_argument("--plan", type=Path, required=True)
    notes.add_argument("--output", type=Path, required=True)
    result = commands.add_parser("result")
    result.add_argument("--plan", type=Path, required=True)
    result.add_argument("--stages", type=Path, required=True)
    result.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        if args.command == "resolve":
            _emit(resolve_plan(args.repository, args.release_record, args.default_ref), args.output, args.github_output)
        elif args.command == "verify-bundle":
            _emit(verify_bundle(read_plan(args.plan), args.directory), args.output, None)
        elif args.command == "verify-build-manifest":
            _emit(verify_build_manifest(read_plan(args.plan), _read_json(args.manifest)), args.output, None)
        elif args.command == "select-rehearsal-record":
            selection = select_rehearsal_record(args.repository, args.release_record or None)
            if args.github_output is not None:
                with args.github_output.open("a", encoding="utf-8", newline="\n") as stream:
                    stream.write(f"release_record={selection['release_record']}\nstatus={selection['status']}\n")
            if args.summary is not None:
                with args.summary.open("a", encoding="utf-8", newline="\n") as stream:
                    stream.write(f"- Release-record rehearsal subject: `{selection['release_record'] or 'none'}` ({selection['reason']})\n")
            sys.stdout.write(_json_bytes(selection).decode("utf-8"))
        elif args.command == "classify-github":
            _emit(classify_github(read_plan(args.plan), _read_json(args.metadata)), args.output, args.github_output)
        elif args.command == "notes":
            args.output.write_text(release_notes(read_plan(args.plan)), encoding="utf-8", newline="\n")
        elif args.command == "result":
            _write_json(args.output, release_result(read_plan(args.plan), _read_json(args.stages)))
        else:  # pragma: no cover
            raise ReleaseError(f"unsupported command: {args.command}")
        return 0
    except (OSError, ReleaseError, dashboard.PublicationError) as exc:
        print(f"release orchestration: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
