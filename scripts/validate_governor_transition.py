#!/usr/bin/env python3
"""Plan and assess an exact, read-only repository-governor succession."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence


SCHEMA = "se-harness-governor-transition-v1"
EVIDENCE_SCHEMA = "se-harness-evaluator-upgrade-evidence-v1"
PAYLOAD_MANIFEST = "se-harness-installed-payload-v1"
SHA1 = re.compile(r"[0-9a-f]{40}")
SHA256 = re.compile(r"[0-9a-f]{64}")
ARTIFACT_ID = re.compile(r"WO-[A-Z][A-Z0-9]*-[0-9]{3}")
RELEASE_ID = re.compile(r"RLS-[A-Z][A-Z0-9]*-[0-9]{3}")
VERSION = re.compile(r"[0-9]+(?:\.[0-9]+){2}(?:[A-Za-z0-9.+-]*)?")
WHEEL_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.+-]*\.whl")
DEFAULT_BRANCH_REF = re.compile(r"refs/remotes/origin/[A-Za-z0-9._/-]+")
MAX_GIT_OUTPUT = 4 * 1024 * 1024
MAX_EVALUATOR_OUTPUT = 4 * 1024 * 1024


class GovernorTransitionError(RuntimeError):
    """The transition cannot be planned or assessed safely."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GovernorTransitionError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _canonical_lf(raw: bytes, label: str) -> bytes:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise GovernorTransitionError(f"{label} is not UTF-8") from exc
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GovernorTransitionError(f"{label} is not valid JSON") from exc
    if not isinstance(value, dict):
        raise GovernorTransitionError(f"{label} must be a JSON object")
    return value


def _run(
    command: Sequence[str],
    *,
    cwd: Path,
    env: Mapping[str, str] | None = None,
    timeout: int = 120,
    limit: int = MAX_GIT_OUTPUT,
) -> subprocess.CompletedProcess[bytes]:
    try:
        completed = subprocess.run(
            list(command),
            cwd=cwd,
            env=dict(env) if env is not None else None,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GovernorTransitionError(f"command could not complete: {command[0]}") from exc
    if len(completed.stdout) > limit or len(completed.stderr) > limit:
        raise GovernorTransitionError(f"command output exceeds the {limit}-byte limit")
    return completed


def _git(root: Path, *args: str, check: bool = True) -> bytes:
    completed = _run(["git", "-C", str(root), *args], cwd=root)
    if check and completed.returncode != 0:
        message = completed.stderr.decode("utf-8", errors="replace").strip()
        raise GovernorTransitionError(f"git {' '.join(args[:2])} failed: {message[:400]}")
    return completed.stdout


def _repository(value: str) -> Path:
    try:
        root = Path(value).resolve(strict=True)
    except OSError as exc:
        raise GovernorTransitionError("repository is unavailable") from exc
    if not root.is_dir() or not (root / ".git").exists():
        raise GovernorTransitionError("repository must be a Git checkout")
    return root


def _clean(root: Path) -> None:
    if _git(root, "status", "--porcelain=v1", "--untracked-files=all"):
        raise GovernorTransitionError("repository worktree must be clean")


def _object_format(root: Path) -> tuple[str, re.Pattern[str]]:
    value = _git(root, "rev-parse", "--show-object-format").decode("ascii").strip()
    if value == "sha1":
        return value, SHA1
    if value == "sha256":
        return value, SHA256
    raise GovernorTransitionError("unsupported Git object format")


def _full_commit(root: Path, value: str, pattern: re.Pattern[str], label: str) -> str:
    if pattern.fullmatch(value) is None:
        raise GovernorTransitionError(f"{label} must be one full lowercase commit ID")
    resolved = _git(root, "rev-parse", "--verify", f"{value}^{{commit}}").decode("ascii").strip()
    if resolved != value:
        raise GovernorTransitionError(f"{label} does not resolve exactly")
    return resolved


def _resolve_base(
    root: Path,
    head: str,
    supplied: str,
    default_branch_ref: str,
    pattern: re.Pattern[str],
) -> tuple[str, str]:
    value = supplied.strip().lower()
    zero = value and set(value) == {"0"} and len(value) in {40, 64}
    if value and not zero:
        base = _full_commit(root, value, pattern, "base revision")
        source = "event"
    else:
        if DEFAULT_BRANCH_REF.fullmatch(default_branch_ref) is None or ".." in default_branch_ref:
            raise GovernorTransitionError("default branch ref is invalid")
        ref = _git(root, "rev-parse", "--verify", f"{default_branch_ref}^{{commit}}").decode("ascii").strip()
        _full_commit(root, ref, pattern, "default branch revision")
        completed = _run(
            ["git", "-C", str(root), "merge-base", "--all", head, ref],
            cwd=root,
        )
        if completed.returncode != 0:
            raise GovernorTransitionError("default-branch merge base is unavailable")
        candidates = [line for line in completed.stdout.decode("ascii").splitlines() if line]
        if len(candidates) != 1:
            raise GovernorTransitionError("default-branch merge base is ambiguous")
        base = _full_commit(root, candidates[0], pattern, "merge-base revision")
        source = "merge-base"
    if base == head:
        raise GovernorTransitionError("base revision must differ from target HEAD")
    ancestor = _run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", base, head],
        cwd=root,
    )
    if ancestor.returncode != 0:
        raise GovernorTransitionError("base revision is not an ancestor of target HEAD")
    return base, source


def _blob(root: Path, revision: str, relative: str, label: str) -> bytes:
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts or str(path) != relative:
        raise GovernorTransitionError(f"{label} path is invalid")
    completed = _run(
        ["git", "-C", str(root), "show", f"{revision}:{relative}"],
        cwd=root,
    )
    if completed.returncode != 0:
        raise GovernorTransitionError(f"{label} is unavailable at {revision}")
    return completed.stdout


def _metadata(raw: bytes, label: str) -> dict[str, Any]:
    canonical = _canonical_lf(raw, label).decode("utf-8")
    lines = canonical.splitlines()
    if not lines or lines[0] != "+++":
        raise GovernorTransitionError(f"{label} has no TOML front matter")
    try:
        end = lines.index("+++", 1)
        value = tomllib.loads("\n".join(lines[1:end]))
    except (ValueError, tomllib.TOMLDecodeError) as exc:
        raise GovernorTransitionError(f"{label} front matter is invalid") from exc
    if not isinstance(value, dict):
        raise GovernorTransitionError(f"{label} metadata must be an object")
    return value


def _root_identity(root: Path, revision: str, label: str) -> dict[str, Any]:
    config_raw = _blob(root, revision, ".engineering-harness.toml", f"{label} configuration")
    lock_raw = _blob(root, revision, ".engineering-harness.lock", f"{label} lock")
    try:
        config = tomllib.loads(_canonical_lf(config_raw, f"{label} configuration").decode("utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise GovernorTransitionError(f"{label} configuration is invalid") from exc
    lock_canonical = _canonical_lf(lock_raw, f"{label} lock")
    lock_crlf = lock_canonical.decode("utf-8").replace("\n", "\r\n").encode("utf-8")
    lock = _json(lock_canonical, f"{label} lock")
    harness = config.get("harness") if isinstance(config, dict) else None
    version = harness.get("tool_version") if isinstance(harness, dict) else None
    if not isinstance(version, str) or VERSION.fullmatch(version) is None:
        raise GovernorTransitionError(f"{label} configured governor version is invalid")
    schema = lock.get("schema")
    if schema not in {2, 3} or lock.get("tool_version") != version:
        raise GovernorTransitionError(f"{label} configuration and lock disagree")
    if lock.get("hash_algorithm") != "sha256" or lock.get("hash_mode") != "utf8-text-lf-v1":
        raise GovernorTransitionError(f"{label} lock hash contract is unsupported")
    evaluator = lock.get("evaluator")
    if evaluator is not None and not isinstance(evaluator, dict):
        raise GovernorTransitionError(f"{label} evaluator identity is invalid")
    return {
        "commit": revision,
        "version": version,
        "lock_schema": schema,
        "lock_sha256": _sha256(lock_raw),
        "canonical_lock_sha256": _sha256(lock_canonical),
        "lock_materialization_sha256": {
            "git": _sha256(lock_raw),
            "lf": _sha256(lock_canonical),
            "crlf": _sha256(lock_crlf),
        },
        "evaluator": evaluator,
    }


def _evaluator(value: Any, label: str) -> dict[str, str | None]:
    """Validate an evaluator identity; the archive pair is either both strings or both null.

    A root adopted by the simple upgrade from an index install records no archive
    identity (REQ-REB-028, SPEC-REB-012 rule 1); version and installed-payload
    digest are the identity.
    """

    if not isinstance(value, dict) or set(value) != {
        "archive_name",
        "archive_sha256",
        "payload_manifest",
        "payload_sha256",
        "version",
    }:
        raise GovernorTransitionError(f"{label} field set is invalid")
    result = {key: value.get(key) for key in value}
    archive_recorded = result["archive_name"] is not None or result["archive_sha256"] is not None
    if (
        not isinstance(result["version"], str)
        or VERSION.fullmatch(result["version"]) is None
        or (
            archive_recorded
            and (
                not isinstance(result["archive_name"], str)
                or WHEEL_NAME.fullmatch(result["archive_name"]) is None
                or not isinstance(result["archive_sha256"], str)
                or SHA256.fullmatch(result["archive_sha256"]) is None
            )
        )
        or result["payload_manifest"] != PAYLOAD_MANIFEST
        or not isinstance(result["payload_sha256"], str)
        or SHA256.fullmatch(result["payload_sha256"]) is None
    ):
        raise GovernorTransitionError(f"{label} values are invalid")
    return {key: (None if item is None else str(item)) for key, item in result.items()}


def _released_distribution(
    root: Path, base_revision: str, target_version: str
) -> dict[str, str]:
    paths = _git(
        root,
        "ls-tree",
        "-r",
        "--name-only",
        base_revision,
        "--",
        "docs/engineering",
    ).decode("utf-8")
    matches: list[dict[str, str]] = []
    for relative in sorted(paths.splitlines()):
        path = PurePosixPath(relative)
        if path.suffix != ".md" or path.parent.name != "releases" or not path.name.startswith("RLS-"):
            continue
        metadata = _metadata(_blob(root, base_revision, relative, relative), relative)
        distribution = metadata.get("distribution")
        events = metadata.get("lifecycle_events")
        released = isinstance(events, list) and any(
            isinstance(event, dict)
            and event.get("from") == "ready"
            and event.get("to") == "released"
            and event.get("decided_by") == "release-owner"
            for event in events
        )
        record_id = metadata.get("id")
        if (
            metadata.get("type") != "release_record"
            or metadata.get("status") != "released"
            or metadata.get("version") != target_version
            or metadata.get("authorized_by") != "release-owner"
            or metadata.get("tag") != f"v{target_version}"
            or not released
            or not isinstance(record_id, str)
            or RELEASE_ID.fullmatch(record_id) is None
            or not isinstance(distribution, dict)
            or distribution.get("schema") not in {1, 2}
            or distribution.get("kind") != "python-wheel-sdist"
            or not isinstance(distribution.get("wheel"), str)
            or WHEEL_NAME.fullmatch(distribution["wheel"]) is None
            or not isinstance(distribution.get("wheel_sha256"), str)
            or SHA256.fullmatch(distribution["wheel_sha256"]) is None
        ):
            continue
        matches.append(
            {
                "id": record_id,
                "path": relative,
                "version": target_version,
                "tag": str(metadata["tag"]),
                "archive_name": str(distribution["wheel"]),
                "archive_sha256": str(distribution["wheel_sha256"]),
            }
        )
    if len(matches) != 1:
        raise GovernorTransitionError(
            "trusted base must contain exactly one released distribution for the target version"
        )
    return matches[0]


def _evidence_documents(root: Path, head: str) -> list[tuple[str, bytes]]:
    paths = _git(root, "ls-tree", "-r", "--name-only", head, "--", "docs/engineering").decode(
        "utf-8"
    )
    result: list[tuple[str, bytes]] = []
    for relative in sorted(paths.splitlines()):
        path = PurePosixPath(relative)
        if path.suffix != ".json" or path.parent.name != "evidence":
            continue
        raw = _blob(root, head, relative, relative)
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            continue
        if isinstance(value, dict) and value.get("schema") == EVIDENCE_SCHEMA:
            result.append((relative, raw))
    return result


def _select_transition(
    root: Path,
    head: str,
    base: Mapping[str, Any],
    target: Mapping[str, Any],
    trusted_release: Mapping[str, str],
) -> tuple[dict[str, Any], dict[str, str]]:
    """Select the one retained upgrade transaction that took the base root to the target root.

    The simple upgrade (SPEC-REB-012) binds no work order: the installed released
    evaluator's version and payload digest are its identity, and the transaction
    document it retains is the evidence. The target's archive pair must equal
    the trusted release's when recorded; an index install records none, and the
    trusted release then supplies the wheel the assessment installs.
    """

    target_evaluator = _evaluator(target.get("evaluator"), "target lock evaluator")
    if target_evaluator["version"] != trusted_release.get("version"):
        raise GovernorTransitionError("target evaluator version differs from the trusted base release record")
    if target_evaluator["archive_name"] is None:
        archive_source = "trusted-release"
        effective = dict(target_evaluator)
        effective["archive_name"] = trusted_release["archive_name"]
        effective["archive_sha256"] = trusted_release["archive_sha256"]
    else:
        archive_source = "lock"
        effective = dict(target_evaluator)
        if (
            target_evaluator["archive_name"] != trusted_release.get("archive_name")
            or target_evaluator["archive_sha256"] != trusted_release.get("archive_sha256")
        ):
            raise GovernorTransitionError(
                "target evaluator archive differs from the trusted base release record"
            )
    base_locks = set(base.get("lock_materialization_sha256", {}).values())
    matches: list[tuple[str, bytes, dict[str, Any]]] = []
    for relative, raw in _evidence_documents(root, head):
        value = _json(raw, "upgrade transaction evidence")
        if raw != _canonical_json(value):
            raise GovernorTransitionError("upgrade transaction evidence is not canonical JSON")
        prior = value.get("prior")
        transaction = value.get("transaction")
        postconditions = value.get("postconditions")
        work_order = value.get("work_order")
        if (
            value.get("scope") != "standard-root-only"
            or not isinstance(prior, dict)
            or prior.get("lock_sha256") not in base_locks
            or prior.get("tool_version") != base.get("version")
            or value.get("target") != target_evaluator
            or not isinstance(transaction, dict)
            or transaction.get("outcome") != "applied"
            or transaction.get("atomic") is not True
            or not isinstance(postconditions, dict)
            or postconditions.get("lock_matches_target") is not True
            or postconditions.get("no_op_replay") is not True
            or postconditions.get("external_action_performed") is not False
            or postconditions.get("product_release_performed") is not False
            or (work_order is not None and (not isinstance(work_order, str) or ARTIFACT_ID.fullmatch(work_order) is None))
        ):
            continue
        matches.append((relative, raw, value))
    if len(matches) != 1:
        raise GovernorTransitionError(
            "target must contain exactly one retained evaluator-upgrade evidence document matching base and target identities"
        )
    relative, raw, value = matches[0]
    transition = {
        "evidence_path": relative,
        "evidence_sha256": _sha256(raw),
        "work_order": value.get("work_order"),
        "archive_source": archive_source,
        "trusted_release": dict(trusted_release),
    }
    return transition, {key: str(item) for key, item in effective.items()}


def build_plan(
    repository: str,
    base_revision: str,
    default_branch_ref: str,
) -> dict[str, Any]:
    root = _repository(repository)
    _clean(root)
    object_format, pattern = _object_format(root)
    head_value = _git(root, "rev-parse", "--verify", "HEAD^{commit}").decode("ascii").strip()
    head = _full_commit(root, head_value, pattern, "target HEAD")
    base_commit, base_source = _resolve_base(
        root, head, base_revision, default_branch_ref, pattern
    )
    base = _root_identity(root, base_commit, "base")
    target = _root_identity(root, head, "target")
    transition = base["version"] != target["version"]
    if not transition:
        if (
            base["lock_sha256"] != target["lock_sha256"]
            or base["canonical_lock_sha256"] != target["canonical_lock_sha256"]
        ):
            raise GovernorTransitionError("same-version candidate changed the standard governor lock")
        upgrade: dict[str, Any] | None = None
    else:
        trusted_release = _released_distribution(root, base_commit, str(target["version"]))
        upgrade, target_evaluator = _select_transition(root, head, base, target, trusted_release)
        target["evaluator"] = target_evaluator
    return {
        "schema": SCHEMA,
        "phase": "plan",
        "passed": True,
        "applied": False,
        "transition_required": transition,
        "object_format": object_format,
        "base_source": base_source,
        "base": base,
        "target": target,
        "transition": upgrade,
        "diagnostics": [],
    }


def _external_file(value: str, root: Path, label: str) -> tuple[Path, Path]:
    path = Path(os.path.abspath(value))
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise GovernorTransitionError(f"{label} is unavailable") from exc
    for candidate in (path, resolved):
        try:
            candidate.relative_to(root)
        except ValueError:
            continue
        raise GovernorTransitionError(f"{label} must be outside the checkout")
    if not resolved.is_file():
        raise GovernorTransitionError(f"{label} must be an ordinary file")
    return path, resolved


def _evaluator_installation(
    python_value: str,
    entry_point_value: str,
    checkout_root: Path,
) -> tuple[Path, Path, Path]:
    python, _resolved_python = _external_file(
        python_value, checkout_root, "evaluator Python"
    )
    entry_point, resolved_entry_point = _external_file(
        entry_point_value, checkout_root, "evaluator entry point"
    )
    launcher_directory = python.parent
    evaluator_root = launcher_directory.parent
    if launcher_directory.name.casefold() not in {"bin", "scripts"}:
        raise GovernorTransitionError("evaluator Python has no virtual-environment layout")
    if entry_point.parent != launcher_directory:
        raise GovernorTransitionError("evaluator entry point is outside the evaluator installation")
    try:
        resolved_root = evaluator_root.resolve(strict=True)
        resolved_entry_point.relative_to(resolved_root)
    except (OSError, ValueError) as exc:
        raise GovernorTransitionError(
            "evaluator entry point is outside the evaluator installation"
        ) from exc
    return python, entry_point, evaluator_root


def _evaluator_environment() -> dict[str, str]:
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env["PYTHONNOUSERSITE"] = "1"
    env["PYTHONUTF8"] = "1"
    return env


def _evaluator_command(command: Sequence[str], root: Path) -> dict[str, Any]:
    completed = _run(
        command,
        cwd=root.parent,
        env=_evaluator_environment(),
        timeout=300,
        limit=MAX_EVALUATOR_OUTPUT,
    )
    return {
        "exit_code": completed.returncode,
        "stdout_sha256": _sha256(completed.stdout),
        "stderr_sha256": _sha256(completed.stderr),
        "stdout_bytes": len(completed.stdout),
        "stderr_bytes": len(completed.stderr),
    }


def assess(
    repository: str,
    base_revision: str,
    default_branch_ref: str,
    evaluator_python: str | None,
    evaluator_entry_point: str | None,
    evaluator_wheel: str | None,
) -> dict[str, Any]:
    plan = build_plan(repository, base_revision, default_branch_ref)
    root = _repository(repository)
    result = dict(plan)
    result["phase"] = "assessment"
    if not plan["transition_required"]:
        result["assessment"] = "not_applicable"
        result["commands"] = {}
        _clean(root)
        return result
    if not evaluator_python or not evaluator_entry_point or not evaluator_wheel:
        raise GovernorTransitionError("changed-version assessment requires exact evaluator paths")
    python, entry_point, evaluator_root = _evaluator_installation(
        evaluator_python, evaluator_entry_point, root
    )
    wheel, resolved_wheel = _external_file(evaluator_wheel, root, "evaluator wheel")
    expected = _evaluator(plan["target"].get("evaluator"), "planned target evaluator")
    if (
        wheel.name != expected["archive_name"]
        or _sha256(resolved_wheel.read_bytes()) != expected["archive_sha256"]
    ):
        raise GovernorTransitionError("evaluator wheel differs from the approved target identity")
    commands = {
        "identity": _evaluator_command(
            [
                str(python),
                "-I",
                "-m",
                "se_harness",
                "identity",
                "--role",
                "released-evaluator",
                "--expected-version",
                expected["version"],
                "--expected-root",
                str(evaluator_root),
                "--checkout-root",
                str(root),
                "--evaluator-payload-sha256",
                expected["payload_sha256"],
                "--evaluator-wheel-sha256",
                expected["archive_sha256"],
                "--entry-point",
                str(entry_point),
                "--require-isolated-python",
                "--require-entry-point",
            ],
            root,
        ),
        "doctor": _evaluator_command(
            [str(python), "-I", "-m", "se_harness", "doctor", str(root)], root
        ),
        "validate": _evaluator_command(
            [str(python), "-I", "-m", "se_harness", "validate", str(root), "--json"],
            root,
        ),
    }
    failed = [name for name, value in commands.items() if value["exit_code"] != 0]
    if failed:
        raise GovernorTransitionError(
            "target evaluator commands failed: " + ", ".join(sorted(failed))
        )
    _clean(root)
    result["assessment"] = "passed"
    result["commands"] = commands
    return result


def _output_path(value: str | None, root: Path) -> Path | None:
    if value is None:
        return None
    path = Path(os.path.abspath(value))
    try:
        path.relative_to(root)
    except ValueError:
        pass
    else:
        raise GovernorTransitionError("result output must be outside the checkout")
    if not path.parent.is_dir() or path.exists() and not path.is_file():
        raise GovernorTransitionError("result output destination is invalid")
    return path


def _render_human(value: Mapping[str, Any]) -> str:
    if value.get("passed") is not True:
        return f"Governor transition assessment: FAIL\nError: {value.get('error', 'unknown')}\n"
    return (
        "Governor transition assessment: PASS\n"
        f"Phase: {value.get('phase')}\n"
        f"Base: {value['base']['commit']} ({value['base']['version']})\n"
        f"Target: {value['target']['commit']} ({value['target']['version']})\n"
        f"Transition required: {str(value.get('transition_required')).lower()}\n"
        f"Assessment: {value.get('assessment', 'planned')}\n"
        "Authority: read-only observation; no approval, lifecycle, Git, publication, or deployment effect.\n"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Plan or assess one exact read-only repository-governor succession."
    )
    subparsers = parser.add_subparsers(dest="phase", required=True)
    for phase in ("plan", "assess"):
        command = subparsers.add_parser(phase)
        command.add_argument("--repository", default=".")
        command.add_argument("--base-revision", default="")
        command.add_argument(
            "--default-branch-ref", default="refs/remotes/origin/main"
        )
        command.add_argument("--output")
        command.add_argument("--json", action="store_true")
        if phase == "assess":
            command.add_argument("--evaluator-python")
            command.add_argument("--evaluator-entry-point")
            command.add_argument("--evaluator-wheel")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root: Path | None = None
    output: Path | None = None
    try:
        root = _repository(args.repository)
        output = _output_path(args.output, root)
        if args.phase == "plan":
            value = build_plan(args.repository, args.base_revision, args.default_branch_ref)
        else:
            value = assess(
                args.repository,
                args.base_revision,
                args.default_branch_ref,
                args.evaluator_python,
                args.evaluator_entry_point,
                args.evaluator_wheel,
            )
        code = 0
    except GovernorTransitionError as exc:
        value = {
            "schema": SCHEMA,
            "phase": getattr(args, "phase", None),
            "passed": False,
            "applied": False,
            "error": str(exc),
            "diagnostics": [],
        }
        code = 1
    raw = _canonical_json(value)
    if output is not None:
        try:
            output.write_bytes(raw)
        except OSError:
            value = {
                "schema": SCHEMA,
                "phase": getattr(args, "phase", None),
                "passed": False,
                "applied": False,
                "error": "result output could not be written",
                "diagnostics": [],
            }
            raw = _canonical_json(value)
            code = 1
    if args.json:
        sys.stdout.buffer.write(raw)
    else:
        sys.stdout.write(_render_human(value))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
