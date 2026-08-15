"""Plan and apply published-governor control reconciliation."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import re
import shutil
import tempfile
import tomllib
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from se_harness import __version__
from se_harness.installer import HarnessError, LOCK_NAME, ensure_target, load_lock, safe_destination
from se_harness.integrity import HASH_ALGORITHM, HASH_MODE, LOCK_SCHEMA, canonical_sha256, canonical_text_equal, compare_lock_entry
from se_harness.preflight import run_preflight
from se_harness.self_hosting import COMMIT_PATTERN, RECORD_PATTERN, SHA256_PATTERN, VERSION_PATTERN, GovernorDescriptor, load_governor_descriptor
from se_harness.self_hosting_policy import CONFIG_PATH, DESCRIPTOR_PATH, PROTECTED_CONTROL_PATHS, WORKFLOW_PATH, classify_self_hosting


MIGRATION_PROTOCOL = 1
MIGRATION_DATA = "governor-migration.toml"
WORKFLOW_TEMPLATE = "engineering-harness.yml.tpl"
REUSABLE_WORKFLOW = "self-hosting-governor.yml"
TRANSACTION_PATH = Path(".self-hosting/.reconcile-governor-transaction")
RECONCILIATION_PATHS = (
    DESCRIPTOR_PATH,
    CONFIG_PATH,
    WORKFLOW_PATH,
    Path(LOCK_NAME),
)
OWNERSHIPS = {"release-managed", "repository-identity", "repository-policy"}
FIELD_TYPES = {"string": str, "boolean": bool, "integer": int}
FIELD_PATH = re.compile(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+")
MAX_WHEEL_BYTES = 100 * 1024 * 1024


@dataclass(frozen=True)
class TargetRelease:
    version: str
    commit: str
    release_record: str
    wheel: str
    url: str
    sha256: str
    migration: dict[str, Any]
    workflow_template: bytes
    reusable_workflow: bytes


@dataclass(frozen=True)
class ReconciliationChange:
    path: str
    action: str
    detail: str
    current: bytes | None
    desired: bytes | None


@dataclass(frozen=True)
class ReconciliationPlan:
    current_governor: GovernorDescriptor
    target_release: TargetRelease
    work_order: str
    changes: tuple[ReconciliationChange, ...]

    @property
    def blocked(self) -> bool:
        return any(item.action in {"conflict", "decision-required"} for item in self.changes)


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _release_url(version: str, wheel: str) -> str:
    return f"https://github.com/mmzen/se_harness/releases/download/v{version}/{wheel}"


def self_hosting_template_root() -> Path:
    import sysconfig

    candidates = (
        Path(__file__).resolve().parent.parent / "self_hosting",
        Path(sysconfig.get_path("data")) / "share/se-harness/self-hosting",
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()
    raise HarnessError("self-hosting release material could not be located")


def _within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _assert_current_governor(target: Path) -> GovernorDescriptor:
    classification = classify_self_hosting(target)
    if not classification.enabled:
        raise HarnessError(f"reconcile-governor requires the exact implementation repository: {classification.detail}")
    descriptor = load_governor_descriptor(target)
    if descriptor.version != __version__:
        raise HarnessError(
            "reconcile-governor must execute from the currently selected released governor "
            f"{descriptor.version}; running {__version__}"
        )
    if _within(Path(__file__), target):
        raise HarnessError("reconcile-governor refuses candidate source from the implementation checkout")
    lock = load_lock(target)
    files = lock.get("files", {})
    for relative in sorted(PROTECTED_CONTROL_PATHS):
        entry = files.get(relative)
        path = safe_destination(target, Path(relative))
        if not isinstance(entry, dict) or entry.get("mode") != "managed" or not path.is_file():
            raise HarnessError(f"protected control lacks accepted integrity: {relative}")
        if compare_lock_entry(lock, entry, path.read_bytes()) == "mismatch":
            raise HarnessError(f"protected control differs from accepted integrity: {relative}")
    return descriptor


def _wheel_member(archive: zipfile.ZipFile, suffix: str) -> bytes:
    matches = [name for name in archive.namelist() if name.replace("\\", "/").endswith(suffix)]
    if len(matches) != 1:
        raise HarnessError(f"target wheel must contain exactly one {suffix}")
    info = archive.getinfo(matches[0])
    if info.file_size > 1_000_000:
        raise HarnessError(f"target release data is too large: {suffix}")
    return archive.read(info)


def _metadata_version(archive: zipfile.ZipFile) -> str:
    metadata = _wheel_member(archive, ".dist-info/METADATA").decode("utf-8")
    versions = [line.partition(":")[2].strip() for line in metadata.splitlines() if line.startswith("Version:")]
    if len(versions) != 1:
        raise HarnessError("target wheel has ambiguous distribution version metadata")
    return versions[0]


def _acquire_target_wheel(version: str, expected_sha256: str, supplied: Path | None) -> tuple[Path, bool]:
    wheel = f"se_harness-{version}-py3-none-any.whl"
    if supplied is not None:
        path = supplied.expanduser().resolve()
        if path.name != wheel or not path.is_file():
            raise HarnessError(f"target wheel must be an exact local file named {wheel}")
        return path, False
    temporary = tempfile.NamedTemporaryFile(prefix="se-harness-target-", suffix=".whl", delete=False)
    temporary.close()
    path = Path(temporary.name)
    try:
        request = urllib.request.Request(_release_url(version, wheel), headers={"User-Agent": "se-harness-governor"})
        with urllib.request.urlopen(request, timeout=30) as response, path.open("wb") as output:  # noqa: S310 - exact HTTPS origin is constructed above
            if response.geturl() and not response.geturl().startswith("https://"):
                raise HarnessError("target wheel download left HTTPS")
            total = 0
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_WHEEL_BYTES:
                    raise HarnessError("target governor wheel exceeds the bounded download size")
                output.write(chunk)
    except Exception:
        path.unlink(missing_ok=True)
        raise
    return path, True


def load_target_release(
    *,
    version: str,
    commit: str,
    release_record: str,
    sha256: str,
    wheel_path: Path | None,
) -> TargetRelease:
    if VERSION_PATTERN.fullmatch(version) is None:
        raise HarnessError("invalid target governor version")
    if COMMIT_PATTERN.fullmatch(commit) is None:
        raise HarnessError("target governor commit must be a full Git object ID")
    if RECORD_PATTERN.fullmatch(release_record) is None:
        raise HarnessError("invalid target governor release record")
    if SHA256_PATTERN.fullmatch(sha256) is None:
        raise HarnessError("target governor wheel SHA-256 must be lowercase and complete")
    wheel = f"se_harness-{version}-py3-none-any.whl"
    path, cleanup = _acquire_target_wheel(version, sha256, wheel_path)
    try:
        if path.stat().st_size > MAX_WHEEL_BYTES:
            raise HarnessError("target governor wheel exceeds the bounded archive size")
        raw = path.read_bytes()
        if _sha256(raw) != sha256:
            raise HarnessError("target governor wheel SHA-256 mismatch")
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                if _metadata_version(archive) != version:
                    raise HarnessError("target wheel metadata version does not match --to")
                prefix = "share/se-harness/self-hosting/"
                migration_bytes = _wheel_member(archive, prefix + MIGRATION_DATA)
                workflow_template = _wheel_member(archive, prefix + WORKFLOW_TEMPLATE)
                reusable_workflow = _wheel_member(archive, prefix + REUSABLE_WORKFLOW)
        except (OSError, UnicodeError, zipfile.BadZipFile, tomllib.TOMLDecodeError) as exc:
            raise HarnessError(f"cannot inspect target governor wheel: {exc}") from exc
        try:
            migration = tomllib.loads(migration_bytes.decode("utf-8"))
        except (UnicodeError, tomllib.TOMLDecodeError) as exc:
            raise HarnessError(f"invalid target migration contract: {exc}") from exc
        if migration.get("protocol") != MIGRATION_PROTOCOL:
            raise HarnessError("current governor does not understand the target migration protocol")
        if migration.get("workflow_role") != "implementation-repository":
            raise HarnessError("target release does not declare the self-hosting workflow role")
        _validate_reusable_workflow(reusable_workflow)
        return TargetRelease(
            version=version,
            commit=commit,
            release_record=release_record,
            wheel=wheel,
            url=_release_url(version, wheel),
            sha256=sha256,
            migration=migration,
            workflow_template=workflow_template,
            reusable_workflow=reusable_workflow,
        )
    finally:
        if cleanup:
            path.unlink(missing_ok=True)


def _validate_reusable_workflow(value: bytes) -> None:
    try:
        text = value.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HarnessError("self-hosting reusable workflow must be UTF-8") from exc
    required = (
        "workflow_call:",
        "  governor:",
        "  candidate-source:",
        "  candidate-package:",
        "needs: governor",
        "needs: candidate-source",
        "accept-candidate",
    )
    if any(item not in text for item in required):
        raise HarnessError("target self-hosting workflow is missing a required assurance plane")
    if "pull_request_target" in text or re.search(r"(?m)^\s*contents:\s*write\s*$", text):
        raise HarnessError("target self-hosting workflow requests a prohibited authority boundary")


def _parse_decisions(values: Iterable[str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for item in values:
        path, separator, literal = item.partition("=")
        if not separator or FIELD_PATH.fullmatch(path) is None or path in result:
            raise HarnessError("--set requires one unique dotted.path=TOML_VALUE")
        try:
            parsed = tomllib.loads(f"value = {literal}\n")["value"]
        except (tomllib.TOMLDecodeError, KeyError) as exc:
            raise HarnessError(f"invalid TOML value for {path}") from exc
        result[path] = parsed
    return result


def _lookup(root: dict[str, Any], path: str) -> tuple[bool, Any]:
    current: Any = root
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    return True, current


def _assign(root: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    current = root
    for part in parts[:-1]:
        child = current.setdefault(part, {})
        if not isinstance(child, dict):
            raise HarnessError(f"configuration path collides with a scalar: {path}")
        current = child
    current[parts[-1]] = value


def _leaf_paths(value: dict[str, Any], prefix: str = "") -> set[str]:
    result: set[str] = set()
    for key, item in value.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(item, dict):
            result.update(_leaf_paths(item, path))
        else:
            result.add(path)
    return result


def _toml_scalar(value: Any) -> str:
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        return str(value)
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return "[" + ", ".join(json.dumps(item, ensure_ascii=False) for item in value) + "]"
    raise HarnessError(f"unsupported reconciled TOML value type: {type(value).__name__}")


def _render_toml(value: dict[str, Any]) -> bytes:
    lines: list[str] = []

    def render_table(table: dict[str, Any], path: tuple[str, ...]) -> None:
        scalars = [(key, item) for key, item in table.items() if not isinstance(item, dict)]
        children = [(key, item) for key, item in table.items() if isinstance(item, dict)]
        if path:
            if lines and lines[-1] != "":
                lines.append("")
            lines.append("[" + ".".join(path) + "]")
        for key, item in scalars:
            lines.append(f"{key} = {_toml_scalar(item)}")
        for key, child in children:
            render_table(child, (*path, key))

    render_table(value, ())
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def _migrate_configuration(current_bytes: bytes, migration: dict[str, Any], target_version: str, decisions: dict[str, Any]) -> tuple[bytes | None, list[str]]:
    try:
        current = tomllib.loads(current_bytes.decode("utf-8"))
    except (UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise HarnessError(f"cannot parse current self-hosting configuration: {exc}") from exc
    rules = migration.get("fields")
    if not isinstance(rules, list) or not rules:
        raise HarnessError("target migration contract has no field ownership rules")
    extensions = migration.get("extension_namespaces", [])
    if not isinstance(extensions, list) or any(not isinstance(item, str) or not item for item in extensions):
        raise HarnessError("target migration extension namespaces are invalid")
    known: set[str] = set()
    result: dict[str, Any] = {}
    required: list[str] = []
    for rule in rules:
        if not isinstance(rule, dict):
            raise HarnessError("target migration field rule must be an object")
        path = rule.get("path")
        ownership = rule.get("ownership")
        declared_type = rule.get("type")
        if not isinstance(path, str) or FIELD_PATH.fullmatch(path) is None or path in known:
            raise HarnessError("target migration field paths must be unique dotted names")
        if ownership not in OWNERSHIPS:
            raise HarnessError(f"invalid ownership for {path}")
        if declared_type not in FIELD_TYPES:
            raise HarnessError(f"invalid or missing field type for {path}")
        known.add(path)
        present, current_value = _lookup(current, path)
        if ownership == "release-managed":
            if path in decisions:
                raise HarnessError(f"release-managed field cannot be supplied through --set: {path}")
            source = rule.get("source")
            if source == "target-version":
                selected = target_version
            elif "value" in rule:
                if source is not None:
                    raise HarnessError(f"unsupported release-managed source for {path}")
                selected = rule["value"]
            else:
                raise HarnessError(f"release-managed field has no target value: {path}")
        elif path in decisions:
            selected = decisions[path]
        elif present:
            selected = current_value
        elif "default" in rule:
            selected = rule["default"]
        else:
            required.append(path)
            continue
        expected_type = FIELD_TYPES[str(declared_type)]
        if expected_type is bool:
            valid_type = type(selected) is bool
        elif expected_type is int:
            valid_type = type(selected) is int
        else:
            valid_type = isinstance(selected, expected_type)
        if not valid_type:
            raise HarnessError(f"reconciled value has the wrong type for {path}")
        _toml_scalar(selected)
        _assign(result, path, selected)
    unused = sorted(set(decisions) - known)
    if unused:
        raise HarnessError(f"unknown reconciliation decision: {unused[0]}")
    unknown = sorted(
        path
        for path in _leaf_paths(current) - known
        if not any(path == prefix or path.startswith(prefix + ".") for prefix in extensions)
    )
    if unknown:
        raise HarnessError(f"current configuration has an unowned field: {unknown[0]}")
    for prefix in extensions:
        present, extension = _lookup(current, prefix)
        if present:
            _assign(result, prefix, extension)
    return (None if required else _render_toml(result)), required


def _render_workflow(template: bytes, descriptor: GovernorDescriptor, candidate_version: str) -> bytes:
    try:
        text = template.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HarnessError("self-hosting workflow template must be UTF-8") from exc
    variables = {
        "GOVERNOR_VERSION": descriptor.version,
        "GOVERNOR_TAG": descriptor.tag,
        "GOVERNOR_WHEEL": descriptor.wheel,
        "GOVERNOR_URL": descriptor.url,
        "GOVERNOR_WHEEL_SHA256": descriptor.sha256,
        "GOVERNOR_COMMIT": descriptor.selected_candidate_commit,
        "GOVERNOR_RELEASE_RECORD": descriptor.selected_release_record,
        "CANDIDATE_VERSION": candidate_version,
    }
    for key, value in variables.items():
        text = text.replace("{{" + key + "}}", value)
    if "{{" in text or "}}" in text:
        raise HarnessError("self-hosting workflow template contains unresolved variables")
    value = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    if "pull_request_target" in text or "contents: write" in text:
        raise HarnessError("rendered self-hosting workflow crosses the authority boundary")
    expected_use = f"mmzen/se_harness/.github/workflows/self-hosting-governor.yml@{descriptor.selected_candidate_commit}"
    if expected_use not in text:
        raise HarnessError("rendered workflow is not pinned to the selected governor commit")
    return value


def _descriptor_bytes(target: TargetRelease) -> bytes:
    values = {
        "schema": 1,
        "version": target.version,
        "tag": f"v{target.version}",
        "wheel": target.wheel,
        "url": target.url,
        "sha256": target.sha256,
        "selected_release_record": target.release_record,
        "selected_candidate_commit": target.commit,
    }
    lines = [f"schema = {values['schema']}"]
    lines.extend(f"{key} = {json.dumps(value)}" for key, value in values.items() if key != "schema")
    return ("\n".join(lines) + "\n").encode("utf-8")


def _load_current_workflow_template() -> bytes:
    path = self_hosting_template_root() / WORKFLOW_TEMPLATE
    try:
        return path.read_bytes()
    except OSError as exc:
        raise HarnessError(f"cannot read current self-hosting workflow contract: {exc}") from exc


def _candidate_version(config_bytes: bytes) -> str:
    try:
        value = tomllib.loads(config_bytes.decode("utf-8"))["harness"]["tool_version"]
    except (UnicodeError, tomllib.TOMLDecodeError, KeyError, TypeError) as exc:
        raise HarnessError("current configuration has no valid harness.tool_version") from exc
    if not isinstance(value, str) or VERSION_PATTERN.fullmatch(value) is None:
        raise HarnessError("current configuration has an invalid harness.tool_version")
    return value


def _change(path: Path, current: bytes | None, desired: bytes | None, *, blocked: str | None = None) -> ReconciliationChange:
    if blocked is not None:
        return ReconciliationChange(path.as_posix(), blocked, blocked, current, desired)
    if current is not None and desired is not None and canonical_text_equal(current, desired):
        return ReconciliationChange(path.as_posix(), "unchanged", "matches target", current, desired)
    return ReconciliationChange(path.as_posix(), "update", "authorized target state", current, desired)


def plan_governor_reconciliation(
    target: Path,
    *,
    version: str,
    commit: str,
    release_record: str,
    sha256: str,
    work_order: str,
    wheel_path: Path | None = None,
    decisions: Iterable[str] = (),
) -> ReconciliationPlan:
    target = ensure_target(target, must_exist=True)
    _recover_transaction(target)
    current_governor = _assert_current_governor(target)
    report = run_preflight(target, work_order_id=work_order, phase="start")
    if not report.ready:
        detail = report.diagnostics[0].message if report.diagnostics else "unknown preflight failure"
        raise HarnessError(f"reconcile-governor work-order preflight failed: {detail}")
    target_release = load_target_release(
        version=version,
        commit=commit,
        release_record=release_record,
        sha256=sha256,
        wheel_path=wheel_path,
    )
    current_config = safe_destination(target, CONFIG_PATH).read_bytes()
    current_workflow = safe_destination(target, WORKFLOW_PATH).read_bytes()
    expected_current_workflow = _render_workflow(
        _load_current_workflow_template(), current_governor, _candidate_version(current_config)
    )
    workflow_conflict = not canonical_text_equal(current_workflow, expected_current_workflow)
    parsed_decisions = _parse_decisions(decisions)
    desired_config, required = _migrate_configuration(
        current_config, target_release.migration, target_release.version, parsed_decisions
    )
    desired_descriptor = _descriptor_bytes(target_release)
    target_descriptor = GovernorDescriptor(
        version=target_release.version,
        tag=f"v{target_release.version}",
        wheel=target_release.wheel,
        url=target_release.url,
        sha256=target_release.sha256,
        selected_release_record=target_release.release_record,
        selected_candidate_commit=target_release.commit,
    )
    desired_workflow = _render_workflow(
        target_release.workflow_template, target_descriptor, target_release.version
    )
    old_lock = load_lock(target)
    desired_lock: bytes | None = None
    if desired_config is not None and not workflow_conflict:
        lock = copy.deepcopy(old_lock)
        lock["schema"] = LOCK_SCHEMA
        lock["hash_algorithm"] = HASH_ALGORITHM
        lock["hash_mode"] = HASH_MODE
        lock["tool_version"] = target_release.version
        files = lock.setdefault("files", {})
        files[CONFIG_PATH.as_posix()] = {"mode": "managed", "sha256": canonical_sha256(desired_config)}
        files[WORKFLOW_PATH.as_posix()] = {"mode": "managed", "sha256": canonical_sha256(desired_workflow)}
        lock["governor"] = {
            "version": target_release.version,
            "commit": target_release.commit,
            "release_record": target_release.release_record,
            "wheel_sha256": target_release.sha256,
            "migration_protocol": MIGRATION_PROTOCOL,
        }
        desired_lock = (json.dumps(lock, indent=2, sort_keys=True) + "\n").encode("utf-8")
    changes = [
        _change(DESCRIPTOR_PATH, safe_destination(target, DESCRIPTOR_PATH).read_bytes(), desired_descriptor),
        _change(
            CONFIG_PATH,
            current_config,
            desired_config,
            blocked="decision-required" if required else None,
        ),
        _change(
            WORKFLOW_PATH,
            current_workflow,
            desired_workflow,
            blocked="conflict" if workflow_conflict else None,
        ),
        _change(Path(LOCK_NAME), safe_destination(target, Path(LOCK_NAME)).read_bytes(), desired_lock),
    ]
    if required:
        changes[1] = ReconciliationChange(
            CONFIG_PATH.as_posix(),
            "decision-required",
            ", ".join(sorted(required)),
            current_config,
            None,
        )
    return ReconciliationPlan(current_governor, target_release, work_order, tuple(changes))


def format_reconciliation_plan(plan: ReconciliationPlan) -> str:
    lines = [
        f"current governor: {plan.current_governor.version} {plan.current_governor.sha256}",
        f"target governor:  {plan.target_release.version} {plan.target_release.sha256}",
    ]
    lines.extend(f"{item.action:18} {item.path} ({item.detail})" for item in plan.changes)
    lines.append("authority: mechanical reconciliation only; accountable promotion remains separate")
    return "\n".join(lines)


def _write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        handle.write(value)
        handle.flush()
        os.fsync(handle.fileno())


def _recover_transaction(target: Path) -> None:
    transaction = safe_destination(target, TRANSACTION_PATH)
    manifest_path = transaction / "manifest.json"
    if not manifest_path.is_file():
        if transaction.exists():
            raise HarnessError("incomplete governor transaction has no recovery manifest")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        paths = manifest["paths"]
        if not isinstance(paths, list):
            raise ValueError("paths")
        for index, relative in reversed(list(enumerate(paths))):
            if relative not in {item.as_posix() for item in RECONCILIATION_PATHS}:
                raise ValueError("path")
            destination = safe_destination(target, Path(relative))
            backup = transaction / "backup" / str(index)
            absent = transaction / "absent" / str(index)
            if backup.is_file():
                _write_bytes(destination, backup.read_bytes())
            elif absent.is_file():
                destination.unlink(missing_ok=True)
            else:
                raise ValueError("backup")
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise HarnessError(f"cannot recover interrupted governor reconciliation: {exc}") from exc
    shutil.rmtree(transaction)


def apply_governor_reconciliation(target: Path, plan: ReconciliationPlan) -> None:
    target = ensure_target(target, must_exist=True)
    if plan.blocked:
        raise HarnessError("governor reconciliation is blocked; no files were written")
    desired = {Path(item.path): item.desired for item in plan.changes}
    if set(desired) != set(RECONCILIATION_PATHS) or any(value is None for value in desired.values()):
        raise HarnessError("governor reconciliation has an invalid write set")
    for item in plan.changes:
        destination = safe_destination(target, Path(item.path))
        current = destination.read_bytes() if destination.is_file() else None
        if current != item.current:
            raise HarnessError(f"governor reconciliation input changed after planning: {item.path}")
    transaction = safe_destination(target, TRANSACTION_PATH)
    if transaction.exists():
        _recover_transaction(target)
    transaction.mkdir(parents=True)
    paths = [item.as_posix() for item in RECONCILIATION_PATHS]
    try:
        for index, relative in enumerate(RECONCILIATION_PATHS):
            destination = safe_destination(target, relative)
            if destination.is_file():
                _write_bytes(transaction / "backup" / str(index), destination.read_bytes())
            else:
                _write_bytes(transaction / "absent" / str(index), b"")
            _write_bytes(transaction / "staged" / str(index), desired[relative])  # type: ignore[arg-type]
        _write_bytes(
            transaction / "manifest.json",
            (json.dumps({"schema": 1, "paths": paths}, sort_keys=True) + "\n").encode("utf-8"),
        )
        for index, relative in enumerate(RECONCILIATION_PATHS):
            destination = safe_destination(target, relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(transaction / "staged" / str(index), destination)
        shutil.rmtree(transaction)
    except Exception as exc:
        try:
            _recover_transaction(target)
        except HarnessError as recovery:
            raise HarnessError(f"governor reconciliation failed and recovery is required: {recovery}") from exc
        raise HarnessError(f"governor reconciliation failed; prior state restored: {exc}") from exc
