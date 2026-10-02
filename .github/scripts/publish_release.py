#!/usr/bin/env python3
"""Resolve, reconcile, and report the deterministic SE Harness release last mile."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
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
import reconcile_maintenance_branch as maintenance
from scripts import check_release_delivery as delivery
from repository_tools.json_bytes import pretty_json_bytes, read_json_object, parse_json_object, sha256_file
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
    complete_delivery: dict[str, Any] | None = None


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
            '-G^(status[[:space:]]*=[[:space:]]*"released"[[:space:]]*$|tag[[:space:]]*=)',
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
    plan = ReleasePlan(
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
    envelope = resolve_complete_delivery(repository, default_head, metadata, catalog, plan)
    if envelope is not None:
        from dataclasses import replace
        plan = replace(plan, schema="se-harness-release-plan/v3", complete_delivery=envelope)
    return plan


def read_plan(path: Path) -> ReleasePlan:
    value = _read_json(path)
    if value.get("schema") == "se-harness-release-plan/v2":
        if value.get("complete_delivery") is not None:
            raise ReleaseError("legacy release plan cannot carry complete delivery")
        value.setdefault("complete_delivery", None)
    fields = set(ReleasePlan.__dataclass_fields__)
    if set(value) != fields:
        raise ReleaseError("release plan field set is not canonical")
    if value.get("schema") not in {"se-harness-release-plan/v2", "se-harness-release-plan/v3"}:
        raise ReleaseError("unsupported release plan schema")
    if value["schema"] == "se-harness-release-plan/v3" and not isinstance(value.get("complete_delivery"), dict):
        raise ReleaseError("complete release plan requires a bound delivery envelope")
    for key in ("verification_records", "released_work"):
        if not isinstance(value.get(key), list):
            raise ReleaseError(f"release plan {key} must be an array")
        value[key] = tuple(value[key])
    try:
        return ReleasePlan(**value)
    except TypeError as exc:
        raise ReleaseError("release plan has invalid field types") from exc


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ReleaseError(message)


def _blob(repository: Path, commit: str, path: str) -> bytes:
    delivery.repository_path(path, "committed input")
    entry = _run_git(repository, "ls-tree", "-z", commit, "--", path).stdout
    _require(entry.startswith(b"100644 blob ") or entry.startswith(b"100755 blob "), "input must be a regular committed file: " + path)
    raw = _run_git(repository, "show", commit + ":" + path).stdout
    _require(len(raw) <= 64 * 1024 * 1024, "committed input exceeds 64 MiB")
    return raw


def _json_blob(repository: Path, commit: str, path: str) -> tuple[dict, bytes]:
    raw = _blob(repository, commit, path)
    _require(len(raw) <= delivery.MAX_JSON_BYTES, "JSON input exceeds 2 MiB")
    value = parse_json_object(raw, error=ReleaseError, label=path, max_bytes=delivery.MAX_JSON_BYTES)
    return value, raw


def verify_marketplace(repository: Path, plan: ReleasePlan, value: dict) -> dict:
    """Inspect inert Git blobs; never execute the staged package."""
    market = value["complete_release"]["marketplace"]
    commit = market["commit"]
    _require(_git_text(repository, "rev-parse", commit + "^{tree}") == market["tree"], "marketplace tree differs")
    _require(_git_text(repository, "show", "-s", "--format=%P", commit) == market["parent"], "marketplace must have exactly the expected parent")
    identity, raw = _json_blob(repository, commit, "PACKAGE-IDENTITY.json")
    _require(hashlib.sha256(raw).hexdigest() == market["identity_sha256"], "marketplace identity digest differs")
    expected = next(s["expected"] for s in value["surfaces"] if s["id"] == "marketplace")
    _require(identity.get("plugin_version") == expected["plugin_version"] and identity.get("name") == "verity-plane", "plugin identity differs")
    _require(identity.get("source", {}).get("revision") == plan.candidate_commit, "plugin source differs")
    evaluator = identity.get("evaluator", {})
    _require(evaluator.get("archive_sha256") == plan.wheel_sha256 and evaluator.get("version") == plan.version
             and evaluator.get("candidate_commit") == plan.candidate_commit, "plugin evaluator provenance differs")
    files = identity.get("files")
    _require(isinstance(files, dict) and bool(files), "marketplace inventory missing")
    entries = _run_git(repository, "ls-tree", "-r", "-z", "--full-tree", commit).stdout.split(b"\0")
    paths = set()
    for entry in filter(None, entries):
        header, raw_path = entry.split(b"\t", 1)
        _require(header.startswith(b"100644 blob ") or header.startswith(b"100755 blob "), "marketplace has linked or non-file content")
        paths.add(raw_path.decode("utf-8"))
    _require(paths == set(files) | {"PACKAGE-IDENTITY.json"}, "marketplace file set differs")
    for name, digest in files.items():
        delivery.digest_value(digest, "marketplace file digest")
        _require(hashlib.sha256(_blob(repository, commit, name)).hexdigest() == digest, "marketplace file differs: " + name)
    for host, label in (("codex", "codex"), ("claude", "claude-code")):
        prefix = "packages/" + host + "/verity-plane/"
        _require(files.get(prefix + "packages/" + plan.wheel) == plan.wheel_sha256, "bundled wheel differs")
        # The receipt uses the native inventory byte digest as its content identity.
        _require(files.get(prefix + "assembly-inventory.json") == expected[label + "_content_sha256"], "native inventory digest differs")
    return {"state": "exact", "commit": commit, "tree": market["tree"], "identity_sha256": market["identity_sha256"]}


def verify_integration(repository: Path, base: str, head: str, envelope: dict, *, receipts: bool = False) -> list[str]:
    """Check the reviewed derivation, not just an allowlist of filenames."""
    value = envelope["plan"]
    scope = value["complete_release"]["integration"]
    _require(_run_git(repository, "merge-base", "--is-ancestor", base, head, check=False).returncode == 0, "integration base is not an ancestor")
    paths = _run_git(repository, "diff", "--name-only", "--no-renames", "-z", base, head).stdout.decode().strip("\0").split("\0")
    paths = [p for p in paths if p]
    allowed = scope["receipt_paths" if receipts else "decision_paths"]
    _require(set(paths) <= set(allowed), "integration contains unapproved paths")
    for path in paths:
        if receipts:
            receipt, _ = _json_blob(repository, head, path)
            _require(receipt.get("plan_sha256") == envelope["sha256"] and
                     receipt.get("release_record") == value["release"]["record"] and
                     receipt.get("candidate_commit") == value["complete_release"]["candidate_commit"], "receipt binding differs")
            continue
        old = _blob(repository, base, path).decode("utf-8").split("+++", 2)
        new = _blob(repository, head, path).decode("utf-8").split("+++", 2)
        _require(len(old) == len(new) == 3 and old[0] == new[0] and old[2] == new[2], "decision integration changes artifact body")
        before, after = tomllib.loads(old[1]), tomllib.loads(new[1])
        events = after.get("lifecycle_events", [])
        prior = before.get("lifecycle_events", [])
        _require(len(events) == len(prior) + 1 and events[:-1] == prior, "decision history is not one appended event")
        event = events[-1]
        _require(event.get("from") == before.get("status") and event.get("to") == after.get("status") == "released"
                 and event.get("decided_by") == envelope["decided_by"], "decision event differs from reviewed human")
        if after.get("type") == "release_record":
            _require(after.get("authorized_by") == envelope["decided_by"], "release authorization actor differs")
            before.pop("authorized_by", None)
            after.pop("authorized_by", None)
        for metadata in (before, after):
            for field in ("status", "updated", "released_at", "lifecycle_events", "delivery"):
                metadata.pop(field, None)
        _require(before == after, "decision integration changes accepted artifact content")
    return paths


def resolve_complete_delivery(repository: Path, head: str, record: dict, catalog: dict, plan: ReleasePlan) -> dict | None:
    binding = record.get("delivery")
    contract = catalog.get(plan.release_contract)
    route = contract[1].get("delivery", {}).get("route") if contract else None
    if binding is None and route is None:
        return None
    _require(route == "complete-release" and isinstance(binding, dict), "release contract and RLS must both select complete-release")
    _require(set(binding) == {"plan", "sha256", "decided_by", "decision_reference", "review_commit"}, "RLS delivery binding field set differs")
    delivery.commit_value(binding["review_commit"], "delivery.review_commit")
    for key in ("decided_by", "decision_reference"):
        delivery.text_value(binding[key], "delivery." + key)
    value, raw = _json_blob(repository, head, binding["plan"])
    _require(hashlib.sha256(raw).hexdigest() == binding["sha256"], "approved delivery plan digest differs")
    _require(value.get("schema") == delivery.COMPLETE_PLAN_SCHEMA, "complete-release needs delivery plan v2")
    surfaces = delivery.validate_plan(value)
    _require(value["release"] == {"contract": plan.release_contract, "record": plan.release_record,
                                "version": plan.version, "wheel_sha256": plan.wheel_sha256}, "delivery plan release identity differs")
    _require(value["complete_release"]["candidate_commit"] == plan.candidate_commit, "delivery candidate differs")
    _require(value["review"]["by"] == binding["decided_by"], "delivery reviewer differs from recorded human")
    events = [e for e in record.get("lifecycle_events", []) if e.get("to") == "released"]
    _require(len(events) == 1 and events[0].get("decided_by") == binding["decided_by"], "complete approval is not bound to the release decision")
    ready = value["complete_release"]["readiness"]
    readiness, readiness_raw = _json_blob(repository, head, ready["path"])
    _require(hashlib.sha256(readiness_raw).hexdigest() == ready["sha256"], "readiness receipt digest differs")
    _require(readiness.get("candidate_commit") == plan.candidate_commit and readiness.get("controls_ready") is True
             and readiness.get("qualification") == "passed" and
             set(readiness.get("verification_records", [])) <= set(plan.verification_records)
             and bool(readiness.get("verification_records")), "required preparation or controls not ready")
    envelope = {**binding, "path": binding["plan"], "plan": value}
    base = binding["review_commit"]
    _require(_blob(repository, base, binding["plan"]) == raw, "reviewed plan was not frozen at integration base")
    verify_integration(repository, base, plan.governance_commit, envelope)
    _require(plan.release_record_path in value["complete_release"]["integration"]["decision_paths"], "release decision path not selected")
    doc_commit = surfaces["documentation"]["expected"]["commit"]
    _require(_run_git(repository, "merge-base", "--is-ancestor", doc_commit, plan.governance_commit, check=False).returncode == 0,
             "approved documentation is not integrated")
    for path, digest in value["complete_release"]["documentation"].items():
        for ref in (doc_commit, plan.governance_commit, head):
            _require(hashlib.sha256(_blob(repository, ref, path)).hexdigest() == digest, "approved documentation differs: " + path)
    verify_marketplace(repository, plan, value)
    return envelope


def _api(request, method: str, suffix: str, payload=None, *, absent=False):
    response = request(method, "/repos/" + dashboard.EXPECTED_REPOSITORY + "/" + suffix, payload)
    if absent and response.status == 404:
        return None
    _require(response.status in {200, 201}, f"{method} {suffix}: unknown result (HTTP {response.status}); inspect before retry")
    return response.payload


def controls_snapshot(request) -> dict:
    environment = _api(request, "GET", "environments/pypi")
    branches = _api(request, "GET", "environments/pypi/deployment-branch-policies")
    reviewers = [r for r in environment.get("protection_rules", []) if r.get("type") == "required_reviewers"]
    _require(not any(r.get("reviewers") for r in reviewers), "pypi still requires a separate reviewer; activation is not ready")
    _require(environment.get("deployment_branch_policy") == {"protected_branches": False, "custom_branch_policies": True}, "pypi ref controls differ")
    rules = branches.get("branch_policies", [])
    _require(len(rules) == 1 and rules[0].get("name") == "main" and rules[0].get("type") == "branch", "pypi must allow only main")
    return {"pypi_reviewer": "not required", "allowed_ref": "main"}


def classify_ref(actual: str | None, expected_parent: str | None, target: str) -> str:
    if actual == target:
        return "exact"
    if actual == expected_parent:
        return "absent" if actual is None else "partial"
    raise ReleaseError("unexpected ref movement; approved parent no longer matches")


def observe_github(plan: ReleasePlan, request, *, tag_only=False) -> dict:
    """Only an explicit 404 is absent. Transport/auth/provider failures stop writes."""
    if tag_only:
        value = _api(request, "GET", "git/ref/tags/" + plan.tag, absent=True)
        if value is None:
            return {"state": "absent"}
        _require(value.get("ref") == "refs/tags/" + plan.tag, "version ref differs")
        obj = value.get("object", {})
        if obj.get("type") == "tag":
            obj = _api(request, "GET", "git/tags/" + str(obj.get("sha"))).get("object", {})
        _require(obj.get("type") == "commit" and obj.get("sha") == plan.candidate_commit, "immutable version tag differs")
        return {"state": "exact"}
    value = _api(request, "GET", "releases/tags/" + plan.tag, absent=True)
    if value is None:
        return {"absent": True}
    return {"tagName": value.get("tag_name"), "isDraft": value.get("draft"),
            "isPrerelease": value.get("prerelease"), "assets": value.get("assets")}


def _remote_ref(request, ref: str) -> str | None:
    value = _api(request, "GET", "git/ref/" + ref, absent=True)
    if value is None:
        return None
    _require(value.get("ref") == "refs/" + ref and value.get("object", {}).get("type") in {"commit", "tag"}, "malformed remote ref")
    sha = value["object"]["sha"]
    delivery.commit_value(sha, "remote ref")
    return sha  # Keep the tag object ID for the compare-and-swap lease.


def _push_ref(repository: Path, ref: str, target: str, expected: str | None, token: str, *, moving_tag=False) -> None:
    """Only fixed destinations. Marketplace is fast-forward; last uses an exact lease."""
    _require(ref in {"refs/heads/plugin-marketplace", "refs/tags/last"}, "unsupported push target")
    env = os.environ.copy()
    count = int(env.get("GIT_CONFIG_COUNT", "0"))
    auth = base64.b64encode(("x-access-token:" + token).encode()).decode()
    env.update({"GIT_CONFIG_COUNT": str(count + 2), f"GIT_CONFIG_KEY_{count}": "http.https://github.com/.extraheader",
                f"GIT_CONFIG_VALUE_{count}": "AUTHORIZATION: basic " + auth,
                f"GIT_CONFIG_KEY_{count+1}": "credential.helper", f"GIT_CONFIG_VALUE_{count+1}": ""})
    args = ["git", "-C", str(repository), "push"]
    if moving_tag:
        args.append("--force-with-lease=" + ref + ":" + (expected or ""))
    args += ["https://github.com/mmzen/se_harness.git", target + ":" + ref]
    cp = subprocess.run(args, env=env, capture_output=True, timeout=90)
    _require(cp.returncode == 0, "ref push did not confirm success; inspect remote before retry")


def promote_marketplace(repository: Path, plan: ReleasePlan, public_wheel: Path, request, push, *, apply=False) -> dict:
    _require(plan.complete_delivery is not None, "no complete-release authority for marketplace")
    _require(public_wheel.name == plan.wheel and _sha256_file(public_wheel) == plan.wheel_sha256, "public wheel differs from approved wheel")
    value = plan.complete_delivery["plan"]
    verified = verify_marketplace(repository, plan, value)
    market = value["complete_release"]["marketplace"]
    state = classify_ref(_remote_ref(request, "heads/plugin-marketplace"), market["parent"], market["commit"])
    if state != "exact" and apply:
        push("refs/heads/plugin-marketplace", market["commit"], market["parent"], False)
        _require(_remote_ref(request, "heads/plugin-marketplace") == market["commit"], "marketplace write is not confirmed")
        state = "exact"
    return {**verified, "state": state, "applied": apply, "plan_sha256": plan.complete_delivery["sha256"]}


def assess_committed_delivery(repository: Path, head: str, plan: ReleasePlan, *, before_markers=False) -> dict:
    _require(plan.complete_delivery is not None, "legacy release has no complete-delivery grant")
    envelope = plan.complete_delivery
    value = envelope["plan"]["complete_release"]
    with tempfile.TemporaryDirectory(prefix="release-readback-") as temporary:
        root = Path(temporary)
        names = _run_git(repository, "ls-tree", "-r", "--name-only", "-z", head, "--", value["evidence_root"]).stdout.decode().split("\0")
        for name in filter(None, names):
            raw = _blob(repository, head, name)
            destination = root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw)
        plan_path = root / "frozen-plan.json"
        plan_path.write_bytes(_blob(repository, head, envelope["path"]))
        observations = root / "observations.json"
        observations.write_bytes(_blob(repository, head, value["observations"]))
        result, _ = delivery.assess(plan_path, observations, root / value["evidence_root"],
                                    governance_commit=plan.governance_commit, before_markers=before_markers)
    return result


def promote_markers(plan: ReleasePlan, assessment: dict, request, push, *, apply=False) -> dict:
    _require(plan.complete_delivery is not None, "no complete-release authority for markers")
    _require(assessment.get("status") == "ready_for_markers" and
             assessment.get("plan_sha256") == plan.complete_delivery["sha256"], "required public checks are incomplete; markers unchanged")
    marker = plan.complete_delivery["plan"]["complete_release"]["markers"]
    _require(_remote_ref(request, "heads/plugin-marketplace") == plan.complete_delivery["plan"]["complete_release"]["marketplace"]["commit"], "public marketplace moved before marker promotion")
    release = _api(request, "GET", "releases/tags/" + plan.tag)
    _require(release.get("tag_name") == plan.tag and release.get("draft") is False and release.get("prerelease") is False, "version release is not final")
    latest = _api(request, "GET", "releases/latest", absent=True)
    latest_tag = latest.get("tag_name") if latest else None
    latest_state = classify_ref(latest_tag, marker["previous_latest"], plan.tag)
    last = _remote_ref(request, "tags/last")
    last_state = classify_ref(last, marker["previous_last"], plan.candidate_commit)
    if apply:
        if latest_state != "exact":
            _api(request, "PATCH", "releases/" + str(release["id"]), {"make_latest": "true"})
        if last_state != "exact":
            push("refs/tags/last", plan.candidate_commit, marker["previous_last"], True)
        observed_latest = _api(request, "GET", "releases/latest")
        _require(observed_latest.get("tag_name") == plan.tag and _remote_ref(request, "tags/last") == plan.candidate_commit, "marker write not confirmed")
        latest_state = last_state = "exact"
    return {"latest": latest_state, "last": last_state, "applied": apply, "plan_sha256": plan.complete_delivery["sha256"]}


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


def _checkout_release_records(repository: Path) -> list[dict[str, Any]]:
    """Front matter of every release record in the checkout tree."""

    import tomllib

    fronts: list[dict[str, Any]] = []
    for path in sorted((repository / "docs/engineering").glob("*/releases/RLS-*.md")):
        if not dashboard._is_artifact_path(path.relative_to(repository).as_posix()):
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("+++\n") or "\n+++\n" not in text[4:]:
            continue
        try:
            fronts.append(tomllib.loads(text[4:].split("\n+++\n", 1)[0]))
        except tomllib.TOMLDecodeError as exc:
            raise ReleaseError(f"invalid release record front matter: {path}") from exc
    return fronts


def select_rehearsal_record(repository: Path, requested: str | None, base_ref: str | None = None) -> dict[str, Any]:
    """Choose the record the publication rehearsal qualifies in release-record mode.

    Candidates are ready or released records whose distribution is schema 2 (recipe-bound):
    the one release-qualification definition replays a bound recipe, so a schema-1 record
    has no rehearsal subject. An explicitly requested record must be one of them; otherwise
    the newest by version is chosen, and an empty selection is a legitimate outcome that the
    caller reports rather than a failure.

    With `base_ref` (CIP-REH-001, WO-CIP-006) the candidates are the records at that ref's
    commit, read from the Git tree exactly as the resolver reads them, so a pull request
    rehearses a record its base branch already holds; the checkout is not consulted.
    """

    if base_ref:
        try:
            base_head = dashboard._resolve_commit(repository, base_ref)
            fronts = [metadata for _, metadata in dashboard._release_records_at(repository, base_head)]
        except dashboard.PublicationError as exc:
            raise ReleaseError(f"cannot read release records at {base_ref}: {exc}") from exc
        where = f" at {base_ref}"
    else:
        fronts = _checkout_release_records(repository)
        where = ""

    candidates: list[tuple[tuple[int, ...], str, str]] = []
    for front in fronts:
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
                f"{requested} is not a ready or released schema-2 record{where}; rehearsable records: {sorted(by_id) or 'none'}"
            )
        return {"release_record": requested, "status": by_id[requested], "reason": "requested"}
    if not candidates:
        return {"release_record": "", "status": "", "reason": f"no ready or released schema-2 record exists{where}; only the candidate is rehearsed"}
    _, identifier, status = max(candidates)
    return {"release_record": identifier, "status": status, "reason": f"newest ready or released schema-2 record{where}"}


# Shared trigger policy for both rehearsal legs (WO-KIS-005).
PUBLICATION_INPUTS = {
    ".github/scripts/publish_release.py", ".github/scripts/publish_dashboard.py",
    ".github/scripts/reconcile_maintenance_branch.py",
    ".github/workflows/publication-rehearsal.yml", ".github/workflows/release-qualification.yml",
    ".github/workflows/release-candidate-replay.yml", ".github/workflows/publish-pypi.yml",
    ".github/workflows/pages-publication.yml", ".github/workflows/publish-dashboard-pages.yml",
    "repository_tools/release_distribution.py", "repository_tools/json_bytes.py",
    "repository_tools/evaluator_facts.py", "se_harness/release_qualification.py",
}
BUILD_INPUTS = {
    "pyproject.toml", "MANIFEST.in", "repository_tools/release_build.py",
    "scripts/bind_release_distribution.py", "scripts/create_release_bundle_manifest.py",
    "scripts/normalize_sdist.py", "scripts/replay_release_build.py",
    "scripts/check_portable_release_surface.py", "scripts/validate_release_distributions.py",
    "scripts/build_plugin_archives.py",
    "repository_tools/plugin_distribution.py", "se_harness/candidate_acceptance.py",
    "tests/test_ci_pipeline.py", "tests/test_release_orchestration.py",
    "tests/test_release_build.py", "tests/test_release_qualification.py",
    "tests/test_pypi_publishing.py", "tests/test_release_evidence_audit.py",
}


def rehearsal_changes(paths: Iterable[str], *, explicit: bool = False) -> dict[str, Any]:
    changed = set(paths)
    publication = explicit or bool(changed & PUBLICATION_INPUTS)
    candidate = publication or bool(changed & BUILD_INPUTS) or any(p.startswith("release/") for p in changed)
    return {"candidate": candidate, "record": publication,
            "reason": "explicit release preparation" if explicit else
            ("build or publication inputs changed" if candidate else "skipped: no build or publication inputs changed")}


def select_rehearsals(repository: Path, event: dict[str, Any], event_name: str, requested: str = "") -> dict[str, Any]:
    base_ref = None
    if event_name == "workflow_dispatch":
        decision = rehearsal_changes((), explicit=True)
    else:
        if event_name == "pull_request":
            base_ref = event["pull_request"]["base"]["sha"]
        elif event_name == "push":
            base_ref = event["before"]
        else:
            raise ReleaseError(f"unsupported rehearsal event: {event_name}")
        if not isinstance(base_ref, str) or re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", base_ref) is None:
            raise ReleaseError("rehearsal base must be a full Git object ID")
        # A new branch has no previous commit: inspect all its paths.
        arguments = ("ls-tree", "-r", "--name-only", "-z", "HEAD") if set(base_ref) == {"0"} else (
            "diff", "--name-only", "--no-renames", "-z", base_ref, "HEAD", "--")
        paths = _run_git(repository, *arguments).stdout.decode("utf-8").rstrip("\0").split("\0")
        decision = rehearsal_changes(paths)
    record = {"release_record": "", "status": ""}
    if decision["record"]:
        record = select_rehearsal_record(repository, requested or None, base_ref if event_name == "pull_request" else None)
    return {**record, **decision}


def classify_github(plan: ReleasePlan, metadata: dict[str, Any]) -> dict[str, Any]:
    if metadata.get("absent") is True:
        return {"state": "absent", "draft": None, "files": []}
    if metadata.get("tagName") != plan.tag or metadata.get("isPrerelease") is not False or not isinstance(metadata.get("isDraft"), bool):
        return {"state": "mismatched", "draft": metadata.get("isDraft"), "files": []}
    assets = metadata.get("assets")
    if not isinstance(assets, list):
        raise ReleaseError("GitHub Release metadata must contain an assets array")
    expected = {plan.wheel: plan.wheel_sha256, plan.sdist: plan.sdist_sha256, plan.checksums: plan.checksums_sha256}
    observed: dict[str, str] = {}
    for asset in assets:
        if not isinstance(asset, dict) or not isinstance(asset.get("name"), str):
            return {"state": "mismatched", "draft": metadata.get("isDraft"), "files": []}
        if asset["name"] not in expected:
            continue
        digest = asset.get("digest")
        if asset["name"] in observed or not isinstance(digest, str) or digest != "sha256:" + expected[asset["name"]]:
            return {"state": "mismatched", "draft": metadata.get("isDraft"), "files": sorted(observed), "conflict": asset["name"]}
        observed[asset["name"]] = digest.removeprefix("sha256:")
    missing = sorted(expected.keys() - observed.keys())
    return {"state": "partial" if missing else "exact", "draft": metadata["isDraft"],
            "files": sorted(observed), "missing": missing}


def resume_github(plan: ReleasePlan, directory: Path, metadata: dict[str, Any]) -> dict[str, Any]:
    """Upload only missing required assets of a matching unpublished draft."""
    verify_bundle(plan, directory)
    state = classify_github(plan, metadata)
    if state["state"] == "exact":
        return {"uploaded": []}
    if state["state"] != "partial" or state["draft"] is not True:
        detail = f" ({state['conflict']})" if "conflict" in state else ""
        raise ReleaseError(f"GitHub Release is {state['state']}{detail}; only a matching unpublished draft can resume")
    for name in state["missing"]:
        result = subprocess.run(["gh", "release", "upload", plan.tag, str(directory / name), "--repo", plan.repository],
                                capture_output=True, text=True)
        if result.returncode:
            raise ReleaseError(f"upload failed for {name}: {result.stderr.strip()}")
    return {"uploaded": state["missing"]}


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
    names = ("resolution", "qualification", "github", "pypi", "pages", "public_install")
    if plan.complete_delivery is not None:
        names += ("marketplace", "documentation", "public_routes", "release_markers", "receipts")
    for name in names:
        value = stages.get(name, {"state": "not_run"})
        if not isinstance(value, dict) or value.get("state") not in STAGE_STATES:
            raise ReleaseError(f"result stage {name} has an invalid state")
        normalized[name] = value
    result = {
        "schema": RESULT_SCHEMA,
        "authority": "derived operational evidence; no formal lifecycle transition",
        "release": asdict(plan),
        "stages": normalized,
    }
    if plan.complete_delivery is not None:
        result["delivery"] = "complete" if all(v["state"] == "exact" for v in normalized.values()) else "incomplete"
        result["authorization"] = {"decided_by": plan.complete_delivery["decided_by"], "decision_reference": plan.complete_delivery["decision_reference"], "plan_sha256": plan.complete_delivery["sha256"]}
    return result


def _github_outputs(path: Path, value: dict[str, Any]) -> None:
    lines = []
    for key, item in sorted(value.items()):
        if key == "complete_delivery":
            item = item is not None
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
    if isinstance(value, ReleasePlan) and value.complete_delivery is None:
        payload.pop("complete_delivery", None)
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
    select.add_argument("--base-ref", default=None, help="read the records at this ref (a pull request's base) instead of the checkout")
    rehearsals = commands.add_parser("select-rehearsals")
    rehearsals.add_argument("--repository", type=Path, required=True)
    rehearsals.add_argument("--event", type=Path, required=True)
    rehearsals.add_argument("--event-name", required=True)
    rehearsals.add_argument("--release-record", default="")
    rehearsals.add_argument("--github-output", type=Path)
    rehearsals.add_argument("--summary", type=Path)
    resume = commands.add_parser("resume-github")
    resume.add_argument("--plan", type=Path, required=True)
    resume.add_argument("--directory", type=Path, required=True)
    resume.add_argument("--metadata", type=Path, required=True)
    github = commands.add_parser("classify-github")
    github.add_argument("--plan", type=Path, required=True)
    github.add_argument("--metadata", type=Path, required=True)
    github.add_argument("--output", type=Path)
    github.add_argument("--github-output", type=Path)
    for name in ("observe-github", "observe-tag"):
        observe = commands.add_parser(name)
        observe.add_argument("--plan", type=Path, required=True)
        observe.add_argument("--output", type=Path, required=True)
    notes = commands.add_parser("notes")
    notes.add_argument("--plan", type=Path, required=True)
    notes.add_argument("--output", type=Path, required=True)
    result = commands.add_parser("result")
    result.add_argument("--plan", type=Path, required=True)
    result.add_argument("--stages", type=Path, required=True)
    result.add_argument("--output", type=Path, required=True)
    complete = commands.add_parser("continue-delivery", help="Resolve the existing complete approval from trusted main")
    complete.add_argument("--repository", type=Path, required=True)
    complete.add_argument("--release-record", required=True)
    complete.add_argument("--stage", choices=("controls", "marketplace", "markers", "report"), required=True)
    complete.add_argument("--public-wheel", type=Path)
    complete.add_argument("--apply", action="store_true")
    complete.add_argument("--output", type=Path, required=True)
    integration = commands.add_parser("check-integration", help="Read-only comparison with an already reviewed decision envelope")
    integration.add_argument("--repository", type=Path, required=True)
    integration.add_argument("--envelope", type=Path, required=True)
    integration.add_argument("--base", required=True)
    integration.add_argument("--head", required=True)
    integration.add_argument("--receipts", action="store_true")
    integration.add_argument("--output", type=Path)
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
            selection = select_rehearsal_record(args.repository, args.release_record or None, args.base_ref or None)
            if args.github_output is not None:
                with args.github_output.open("a", encoding="utf-8", newline="\n") as stream:
                    stream.write(f"release_record={selection['release_record']}\nstatus={selection['status']}\n")
            if args.summary is not None:
                with args.summary.open("a", encoding="utf-8", newline="\n") as stream:
                    stream.write(f"- Release-record rehearsal subject: `{selection['release_record'] or 'none'}` ({selection['reason']})\n")
            sys.stdout.write(_json_bytes(selection).decode("utf-8"))
        elif args.command == "select-rehearsals":
            selection = select_rehearsals(args.repository, _read_json(args.event), args.event_name, args.release_record)
            _emit(selection, None, args.github_output)
            if args.summary is not None:
                with args.summary.open("a", encoding="utf-8", newline="\n") as stream:
                    stream.write(f"- Rehearsals: {selection['reason']}. Candidate: {selection['candidate']}; older record: {selection['release_record'] or 'skipped'}.\n")
        elif args.command == "resume-github":
            _emit(resume_github(read_plan(args.plan), args.directory, _read_json(args.metadata)), None, None)
        elif args.command == "classify-github":
            _emit(classify_github(read_plan(args.plan), _read_json(args.metadata)), args.output, args.github_output)
        elif args.command in {"observe-github", "observe-tag"}:
            request = maintenance.github_request(os.environ.get("GH_TOKEN", ""))
            _emit(observe_github(read_plan(args.plan), request, tag_only=args.command == "observe-tag"), args.output, None)
        elif args.command == "notes":
            args.output.write_text(release_notes(read_plan(args.plan)), encoding="utf-8", newline="\n")
        elif args.command == "result":
            _write_json(args.output, release_result(read_plan(args.plan), _read_json(args.stages)))
        elif args.command == "check-integration":
            envelope = _read_json(args.envelope)
            _emit({"paths": verify_integration(args.repository, args.base, args.head, envelope, receipts=args.receipts),
                   "claim": "Diff check only; does not authenticate a grant or merge a PR."}, args.output, None)
        elif args.command == "continue-delivery":
            plan = resolve_plan(args.repository, args.release_record)
            _require(plan.complete_delivery is not None, "legacy release requires its original action-specific authority")
            request = maintenance.github_request(os.environ.get("GH_TOKEN", ""))
            push = lambda ref, target, expected, moving: _push_ref(args.repository, ref, target, expected,
                       os.environ.get("GH_TOKEN", ""), moving_tag=moving)
            if args.stage == "controls":
                value = controls_snapshot(request)
            elif args.stage == "marketplace":
                _require(args.public_wheel is not None, "independently downloaded public wheel is required")
                controls_snapshot(request)
                value = promote_marketplace(args.repository, plan, args.public_wheel, request, push, apply=args.apply)
            else:
                head = _git_text(args.repository, "rev-parse", "refs/remotes/origin/main")
                value = assess_committed_delivery(args.repository, head, plan, before_markers=args.stage == "markers")
                if args.stage == "markers":
                    # Retain incomplete evidence before refusing the affected write.
                    _write_json(args.output, value)
                    value = promote_markers(plan, value, request, push, apply=args.apply)
            _emit(value, args.output, None)
            if args.stage == "report" and value.get("status") != "complete":
                return 1
        else:  # pragma: no cover
            raise ReleaseError(f"unsupported command: {args.command}")
        return 0
    except (OSError, ValueError, ReleaseError, dashboard.PublicationError, maintenance.MaintenanceBranchError) as exc:
        print(f"release orchestration: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
