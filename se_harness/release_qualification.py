"""Typed, provenance-bound qualification for release workflow roles."""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import unquote, urlparse

from se_harness import __version__, interpreter_safety
from se_harness.candidate_acceptance import assess_candidate_wheel
from se_harness.evaluator_identity import (
    EvaluatorIdentityError,
    installed_evaluator_identity,
    wheel_payload_sha256,
)
from se_harness.installer import HarnessError, template_root
from se_harness.integrity import IntegrityError, parse_lock
from se_harness.preflight import inspect_installation
from se_harness.runtime_identity import (
    COMMIT_PATTERN,
    SHA256_PATTERN,
    inspect_runtime_identity,
)


QUALIFICATION_SCHEMA = "se-harness-release-qualification-v1"
AUTHORITY = "evidence-only; no lifecycle or external action authorized"
OPERATIONS = (
    "released-root",
    "predecessor-view",
    "complete-candidate",
    "candidate-package",
    "public-install",
)
INDEPENDENCE = {
    "released-root": "released-evaluator",
    "predecessor-view": "external-predecessor",
    "complete-candidate": "candidate-controlled",
    "candidate-package": "released-verifier",
    "public-install": "public-install-observation",
}
MAX_COMMAND_OUTPUT_BYTES = 4 * 1024 * 1024
MAX_WHEEL_BYTES = 100 * 1024 * 1024
VERSION_PATTERN = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:[A-Za-z0-9.+-]*)?")


@dataclass(frozen=True)
class QualificationCheck:
    id: str
    passed: bool
    subject: str
    message: str


@dataclass(frozen=True)
class QualificationResult:
    operation: str
    independence: str
    evaluator: dict[str, Any]
    target: dict[str, Any]
    checks: tuple[QualificationCheck, ...]
    passed: bool
    completion: str = "completed"
    schema: str = QUALIFICATION_SCHEMA
    authority: str = AUTHORITY

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "operation": self.operation,
            "completion": self.completion,
            "passed": self.passed,
            "independence": self.independence,
            "evaluator": self.evaluator,
            "target": self.target,
            "checks": [asdict(item) for item in self.checks],
            "authority": self.authority,
        }

    def canonical_bytes(self) -> bytes:
        return (
            json.dumps(self.to_dict(), ensure_ascii=True, indent=2, sort_keys=True)
            + "\n"
        ).encode("utf-8")


def _canonical_compact(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
        + "\n"
    ).encode("utf-8")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _identified(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result["identity_sha256"] = _sha256(_canonical_compact(value))
    return result


def _check(check_id: str, passed: bool, subject: str, message: str) -> QualificationCheck:
    return QualificationCheck(check_id, passed, subject, message)


def _result(
    operation: str,
    *,
    evaluator: dict[str, Any],
    target: dict[str, Any],
    checks: list[QualificationCheck],
) -> QualificationResult:
    if operation not in INDEPENDENCE:
        raise HarnessError("qualification operation is unsupported")
    return QualificationResult(
        operation=operation,
        independence=INDEPENDENCE[operation],
        evaluator=_identified(evaluator),
        target=_identified(target),
        checks=tuple(checks),
        passed=bool(checks) and all(item.passed for item in checks),
    )


def failed_qualification(
    operation: str,
    *,
    code: str,
    subject: str,
    message: str,
) -> QualificationResult:
    """Return a bounded failure when role execution cannot establish identity."""

    selected = operation if operation in INDEPENDENCE else "complete-candidate"
    return _result(
        selected,
        evaluator={"role": INDEPENDENCE[selected], "status": "unbound"},
        target={"kind": selected, "status": "unbound"},
        checks=[_check(code, False, subject, _bounded_message(message))],
    )


def _bounded_message(message: str) -> str:
    lines = message.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    normalized = lines[0] if lines else "qualification failed without a diagnostic"
    for path, replacement in (
        (Path.cwd(), "<ROOT>"),
        (Path(sys.prefix), "<EVALUATOR>"),
        (Path(tempfile.gettempdir()), "<TEMP>"),
    ):
        for value in {str(path), path.as_posix()}:
            normalized = normalized.replace(value, replacement)
    normalized = re.sub(r"(?i)\b[a-z]:[\\/][^\s,;]+", "<PATH>", normalized)
    normalized = re.sub(r"(?<![A-Za-z0-9.])/(?:[^\s,;]+)", "<PATH>", normalized)
    return normalized[:400]


def render_qualification(result: QualificationResult) -> str:
    lines = [
        f"Release qualification: {'PASS' if result.passed else 'FAIL'}",
        f"Operation: {result.operation}",
        f"Independence: {result.independence}",
        f"Evaluator: {result.evaluator['identity_sha256']}",
        f"Target: {result.target['identity_sha256']}",
        "Checks:",
    ]
    lines.extend(
        f"- {'PASS' if item.passed else 'FAIL'} {item.id} {item.subject}: {item.message}"
        for item in result.checks
    )
    lines.append(f"Authority: {result.authority}")
    return "\n".join(lines) + "\n"


def write_qualification_result(
    path: Path,
    result: QualificationResult,
    *,
    forbidden_roots: tuple[Path, ...] = (),
) -> None:
    """Publish complete canonical bytes through an exclusive same-directory link."""

    lexical = Path(os.path.abspath(path.expanduser()))
    if lexical.name in {"", ".", ".."}:
        raise HarnessError("qualification output name is invalid")
    try:
        parent = lexical.parent.resolve(strict=True)
    except OSError as exc:
        raise HarnessError("qualification output parent is unavailable") from exc
    if not parent.is_dir() or parent.is_symlink():
        raise HarnessError("qualification output parent must be an ordinary directory")
    destination = parent / lexical.name
    for root in forbidden_roots:
        try:
            destination.relative_to(root.resolve(strict=True))
        except (OSError, ValueError):
            continue
        raise HarnessError("qualification output must be outside the inspected repository")
    if destination.exists() or destination.is_symlink():
        raise HarnessError("qualification output already exists")
    fd, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(result.canonical_bytes())
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary_name, destination)
        except FileExistsError as exc:
            raise HarnessError("qualification output already exists") from exc
        except OSError as exc:
            raise HarnessError("qualification output could not be published atomically") from exc
    finally:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass


def _safe_environment() -> dict[str, str]:
    selected = {
        name: value
        for name, value in os.environ.items()
        if name.upper()
        in {
            "COMSPEC",
            "HOME",
            "LANG",
            "LC_ALL",
            "PATH",
            "PATHEXT",
            "SYSTEMROOT",
            "TEMP",
            "TMP",
            "WINDIR",
        }
    }
    selected["PYTHONNOUSERSITE"] = "1"
    selected.pop("PYTHONPATH", None)
    return selected


def _run(
    command: list[str],
    *,
    cwd: Path,
    timeout: int = 180,
) -> subprocess.CompletedProcess[bytes]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=_safe_environment(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise HarnessError("qualification subprocess could not complete") from exc
    if len(completed.stdout) > MAX_COMMAND_OUTPUT_BYTES or len(completed.stderr) > MAX_COMMAND_OUTPUT_BYTES:
        raise HarnessError("qualification subprocess output exceeds the byte limit")
    return completed


def _ordinary_root(path: Path) -> Path:
    try:
        root = path.expanduser().resolve(strict=True)
    except OSError as exc:
        raise HarnessError("qualification target does not exist") from exc
    if not root.is_dir() or root.is_symlink():
        raise HarnessError("qualification target must be an ordinary directory")
    return root


def _git(root: Path, *arguments: str) -> bytes:
    executable = shutil.which("git")
    if executable is None:
        raise HarnessError("Git is required for repository qualification")
    completed = _run([executable, "-C", str(root), *arguments], cwd=root)
    if completed.returncode != 0:
        raise HarnessError(f"Git observation failed: {' '.join(arguments[:2])}")
    return completed.stdout


def _repository_snapshot(root: Path) -> dict[str, str]:
    if not (root / ".git").exists():
        return {"kind": "directory", "state_sha256": _sha256(b"not-a-git-worktree\n")}
    head = _git(root, "rev-parse", "--verify", "HEAD^{commit}").decode("ascii").strip()
    tree = _git(root, "rev-parse", "--verify", "HEAD^{tree}").decode("ascii").strip()
    status = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    diff = _git(root, "diff", "--binary", "--no-ext-diff", "HEAD", "--")
    return {
        "kind": "git-worktree",
        "head": head,
        "tree": tree,
        "status_sha256": _sha256(status),
        "diff_sha256": _sha256(diff),
    }


def _tracked_clean(root: Path) -> bool:
    status = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=no")
    return not status


def _validator_report(root: Path) -> dict[str, Any]:
    validator = template_root() / "scripts" / "validate_engineering_artifacts.py"
    if not validator.is_file():
        raise HarnessError("installed engineering validator is unavailable")
    completed = _run(
        [sys.executable, "-B", str(validator), "--root", str(root), "--json"],
        cwd=root,
    )
    try:
        value = json.loads(completed.stdout.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise HarnessError("installed engineering validator returned invalid JSON") from exc
    if not isinstance(value, dict):
        raise HarnessError("installed engineering validator returned an invalid report")
    value["_returncode"] = completed.returncode
    return value


def _validation_check(root: Path, check_id: str) -> QualificationCheck:
    report = _validator_report(root)
    passed = report.get("valid") is True and report.get("_returncode") == 0
    errors = report.get("errors")
    warnings = report.get("warnings")
    artifact_count = report.get("artifact_count")
    if not isinstance(artifact_count, int):
        artifacts = report.get("artifacts")
        artifact_count = len(artifacts) if isinstance(artifacts, list) else 0
    return _check(
        check_id,
        passed,
        "engineering-graph",
        f"artifacts={artifact_count}; errors={len(errors) if isinstance(errors, list) else 0}; warnings={len(warnings) if isinstance(warnings, list) else 0}",
    )


def _runtime_summary(identity: Any, role: str) -> dict[str, Any]:
    value = {
        "role": role,
        "distribution": "se-harness",
        "version": identity.harness_version,
        "isolated_python": identity.isolated_python,
        "user_site_enabled": identity.user_site_enabled,
        "pythonpath_present": identity.pythonpath_present,
    }
    for name in (
        "candidate_commit",
        "evaluator_payload_manifest",
        "evaluator_payload_sha256",
        "evaluator_archive_name",
        "evaluator_archive_sha256",
    ):
        observed = getattr(identity, name, None)
        if observed is not None:
            value[name] = observed
    entry_point = getattr(identity, "entry_point_origin", None)
    if isinstance(entry_point, str):
        try:
            raw = Path(entry_point).read_bytes()
        except OSError:
            pass
        else:
            value["entry_point_sha256"] = _sha256(raw)
    diagnostics = getattr(identity, "diagnostics", ())
    value["diagnostics"] = [
        {
            "code": str(getattr(item, "code", "RID000")),
            "subject": str(getattr(item, "subject", "runtime")),
            "message": _bounded_message(str(getattr(item, "message", "identity mismatch"))),
        }
        for item in diagnostics
    ]
    return value


def _installed_entry_point() -> Path:
    root = Path(sys.prefix)
    candidates = (
        root / "Scripts" / "harnessctl.exe",
        root / "Scripts" / "harnessctl",
        root / "bin" / "harnessctl",
    )
    available = [item for item in candidates if item.is_file()]
    if len(available) != 1:
        raise HarnessError("installed harnessctl entry point is unavailable or ambiguous")
    return available[0]


def _load_lock(root: Path) -> dict[str, Any]:
    try:
        raw = (root / ".engineering-harness.lock").read_text(encoding="utf-8")
        value = parse_lock(raw)
    except (OSError, UnicodeError, IntegrityError, json.JSONDecodeError) as exc:
        raise HarnessError("target root lock is unavailable or invalid") from exc
    if not isinstance(value, dict):
        raise HarnessError("target root lock is invalid")
    return value


def qualify_released_root(root: Path) -> QualificationResult:
    selected = _ordinary_root(root)
    before = _repository_snapshot(selected)
    checks: list[QualificationCheck] = []
    lock = _load_lock(selected)
    evaluator_lock = lock.get("evaluator")
    if not isinstance(evaluator_lock, dict):
        raise HarnessError("target root lock has no evaluator identity")
    version = evaluator_lock.get("version")
    payload = evaluator_lock.get("payload_sha256")
    archive = evaluator_lock.get("archive_sha256")
    if not isinstance(version, str) or not isinstance(payload, str) or not isinstance(archive, str):
        raise HarnessError("target root evaluator identity is incomplete")
    entry_point = _installed_entry_point()
    identity = inspect_runtime_identity(
        role="released-evaluator",
        expected_version=version,
        expected_root=Path(sys.prefix),
        checkout_root=selected,
        evaluator_payload_sha256=payload,
        evaluator_wheel_sha256=archive,
        entry_point=entry_point,
        require_isolated_python=True,
        require_entry_point=True,
    )
    checks.append(
        _check(
            "RR001",
            identity.passed,
            "released-evaluator",
            "runtime matches the target root lock" if identity.passed else "runtime does not match the target root lock",
        )
    )
    if identity.passed:
        managed = inspect_installation(selected)
        checks.append(
            _check(
                "RR002",
                bool(managed) and all(item.passed for item in managed),
                "managed-root",
                f"{sum(item.passed for item in managed)}/{len(managed)} managed checks passed",
            )
        )
        checks.append(_validation_check(selected, "RR003"))
    else:
        checks.extend(
            [
                _check("RR002", False, "managed-root", "not run after evaluator identity failure"),
                _check("RR003", False, "engineering-graph", "not run after evaluator identity failure"),
            ]
        )
    after = _repository_snapshot(selected)
    checks.append(_check("RR004", before == after, "repository-state", "target state is unchanged" if before == after else "target state changed"))
    target = {
        "kind": "released-root",
        "lock_schema": lock.get("schema"),
        "lock_sha256": _sha256((selected / ".engineering-harness.lock").read_bytes()),
        **{name: value for name, value in before.items() if name in {"head", "tree"}},
    }
    return _result(
        "released-root",
        evaluator=_runtime_summary(identity, "released-evaluator"),
        target=target,
        checks=checks,
    )


def qualify_complete_candidate(root: Path, *, candidate_commit: str) -> QualificationResult:
    selected = _ordinary_root(root)
    if COMMIT_PATTERN.fullmatch(candidate_commit) is None:
        raise HarnessError("candidate commit must be one full lowercase Git object ID")
    before = _repository_snapshot(selected)
    observed_commit = _git(selected, "rev-parse", "--verify", "HEAD^{commit}").decode("ascii").strip()
    identity = inspect_runtime_identity(
        role="candidate-source",
        expected_version=__version__,
        expected_root=selected,
        checkout_root=selected,
        candidate_commit=candidate_commit,
    )
    tracked_clean = _tracked_clean(selected)
    checks = [
        _check("CC001", identity.passed, "candidate-runtime", "candidate runtime is bound to the checkout" if identity.passed else "candidate runtime identity failed"),
        _check("CC002", observed_commit == candidate_commit and tracked_clean, "candidate-commit", "HEAD and tracked tree match the candidate" if observed_commit == candidate_commit and tracked_clean else "HEAD or tracked tree differs from the candidate"),
    ]
    if all(item.passed for item in checks):
        checks.append(_validation_check(selected, "CC003"))
    else:
        checks.append(_check("CC003", False, "engineering-graph", "not run after candidate identity failure"))
    after = _repository_snapshot(selected)
    checks.append(_check("CC004", before == after, "repository-state", "target state is unchanged" if before == after else "target state changed"))
    return _result(
        "complete-candidate",
        evaluator=_runtime_summary(identity, "candidate-source"),
        target={
            "kind": "complete-candidate",
            "commit": observed_commit,
            "tree": before.get("tree"),
        },
        checks=checks,
    )


def qualify_candidate_package(
    wheel: Path,
    *,
    candidate_commit: str,
    candidate_wheel_sha256: str,
    verifier_wheel_sha256: str,
    checkout_root: Path | None = None,
) -> QualificationResult:
    selected_wheel = wheel.expanduser().resolve()
    boundary = checkout_root.expanduser().resolve() if checkout_root is not None else selected_wheel.parent
    entry_point = _installed_entry_point()
    identity = inspect_runtime_identity(
        role="released-evaluator",
        expected_version=__version__,
        expected_root=Path(sys.prefix),
        checkout_root=boundary,
        evaluator_wheel_sha256=verifier_wheel_sha256,
        entry_point=entry_point,
        require_isolated_python=True,
        require_entry_point=True,
    )
    checks = [
        _check("CP001", identity.passed, "released-verifier", "released verifier identity is exact and isolated" if identity.passed else "released verifier identity failed"),
    ]
    manifest = None
    if identity.passed:
        try:
            manifest = assess_candidate_wheel(
                selected_wheel,
                candidate_commit=candidate_commit,
                candidate_wheel_sha256=candidate_wheel_sha256,
                verifier_wheel_sha256=verifier_wheel_sha256,
                checkout_root=checkout_root,
            )
        except HarnessError as exc:
            checks.append(_check("CP002", False, "candidate-wheel", _bounded_message(str(exc))))
        else:
            checks.append(_check("CP002", True, "candidate-wheel", f"{len(manifest.scenarios)} released-verifier scenarios passed"))
    else:
        checks.append(_check("CP002", False, "candidate-wheel", "not run after verifier identity failure"))
    target = {
        "kind": "candidate-package",
        "commit": candidate_commit,
        "wheel_sha256": candidate_wheel_sha256,
    }
    if manifest is not None:
        target["version"] = manifest.candidate_version
        target["acceptance_contract_sha256"] = manifest.contract_sha256
    return _result(
        "candidate-package",
        evaluator=_runtime_summary(identity, "released-verifier"),
        target=target,
        checks=checks,
    )


def _external_evaluator_files(evaluator_python: Path, root: Path) -> tuple[Path, Path]:
    try:
        entry = interpreter_safety.evaluate(evaluator_python, checkout_root=root)
    except interpreter_safety.InterpreterSafetyRefusal as refusal:
        raise HarnessError(
            f"external predecessor interpreter is refused by {refusal.case}: {refusal.detail}"
        ) from refusal
    except interpreter_safety.InterpreterSafetyError as exc:
        raise HarnessError(f"external predecessor interpreter cannot be evaluated: {exc}") from exc
    evaluator_root = entry.environment_root
    entry_candidates = (
        evaluator_root / "Scripts" / "harnessctl.exe",
        evaluator_root / "Scripts" / "harnessctl",
        evaluator_root / "bin" / "harnessctl",
    )
    entry_points = [item for item in entry_candidates if item.is_file()]
    if len(entry_points) != 1:
        raise HarnessError("external predecessor entry point is unavailable or ambiguous")
    direct_urls = list(evaluator_root.glob("Lib/site-packages/se_harness-*.dist-info/direct_url.json"))
    direct_urls.extend(evaluator_root.glob("lib/python*/site-packages/se_harness-*.dist-info/direct_url.json"))
    if len(direct_urls) != 1:
        raise HarnessError("external predecessor wheel provenance is unavailable or ambiguous")
    try:
        value = json.loads(direct_urls[0].read_text(encoding="utf-8"))
        url = value["url"]
    except (OSError, UnicodeError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise HarnessError("external predecessor wheel provenance is invalid") from exc
    parsed = urlparse(url)
    if parsed.scheme != "file":
        raise HarnessError("external predecessor was not installed from a local exact wheel")
    wheel = Path(unquote(parsed.path))
    if os.name == "nt" and wheel.as_posix().startswith("/") and re.match(r"/[A-Za-z]:", wheel.as_posix()):
        wheel = Path(wheel.as_posix()[1:])
    try:
        wheel = wheel.resolve(strict=True)
    except OSError as exc:
        raise HarnessError("external predecessor source wheel is unavailable") from exc
    if not wheel.is_file():
        raise HarnessError("external predecessor source wheel is invalid")
    return entry_points[0].resolve(strict=True), wheel


def qualify_predecessor_view(
    root: Path,
    *,
    release_record_id: str,
    evaluator_python: Path,
    view_output: Path | None = None,
) -> QualificationResult:
    selected = _ordinary_root(root)
    before = _repository_snapshot(selected)
    entry_point, evaluator_wheel = _external_evaluator_files(evaluator_python, selected)
    try:
        from repository_tools.predecessor_publication import (
            PredecessorPublicationError,
            validate_predecessor_publication,
        )
    except ImportError as exc:
        raise HarnessError("the fixed predecessor-view service is unavailable") from exc
    try:
        plan = validate_predecessor_publication(
            selected,
            release_record_id=release_record_id,
            evaluator_python=evaluator_python,
            evaluator_entry_point=entry_point,
            evaluator_wheel=evaluator_wheel,
            output=None,
            view_output=view_output,
        )
    except PredecessorPublicationError as exc:
        checks = [_check("PV001", False, "predecessor-view", _bounded_message(str(exc)))]
        after = _repository_snapshot(selected)
        checks.append(_check("PV002", before == after, "repository-state", "target state is unchanged" if before == after else "target state changed"))
        return _result(
            "predecessor-view",
            evaluator={"role": "external-predecessor", "status": "rejected"},
            target={"kind": "predecessor-view", "release_record": release_record_id},
            checks=checks,
        )
    after = _repository_snapshot(selected)
    checks = [
        _check("PV001", True, "predecessor-view", f"current={plan.current_artifact_count}; predecessor={plan.predecessor_artifact_count}"),
        _check("PV002", before == after and plan.source_unchanged, "repository-state", "source and view inputs are unchanged" if before == after and plan.source_unchanged else "source state changed"),
    ]
    return _result(
        "predecessor-view",
        evaluator={
            "role": "external-predecessor",
            "version": plan.evaluator_version,
            "archive_name": plan.evaluator_archive_name,
            "archive_sha256": plan.evaluator_archive_sha256,
            "payload_sha256": plan.evaluator_payload_sha256,
        },
        target={
            "kind": "predecessor-view",
            "view_manifest_schema": plan.schema,
            "release_record": plan.release_record,
            "release_contract": plan.release_contract,
            "version": plan.version,
            "source_commit": plan.source_commit,
            "source_tree": plan.source_tree,
            "git_object_format": plan.git_object_format,
            "candidate_commit": plan.candidate_commit,
            "excluded_paths_sha256": plan.sparse_spec_sha256,
            "omitted_history_sha256": _sha256(
                _canonical_compact([asdict(item) for item in plan.omitted_history])
            ),
            "observation_sha256": plan.observation_sha256,
        },
        checks=checks,
    )


def _front_matter(path: Path) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    except (OSError, UnicodeError):
        return None
    lines = text.splitlines()
    if not lines or lines[0] != "+++":
        return None
    try:
        end = lines.index("+++", 1)
        value = tomllib.loads("\n".join(lines[1:end]))
    except (ValueError, tomllib.TOMLDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _release_record(root: Path, artifact_id: str) -> tuple[Path, dict[str, Any]]:
    matches: list[tuple[Path, dict[str, Any]]] = []
    engineering = root / "docs" / "engineering"
    for path in engineering.rglob("*.md") if engineering.is_dir() else ():
        value = _front_matter(path)
        if value is not None and value.get("id") == artifact_id:
            matches.append((path, value))
    if len(matches) != 1 or matches[0][1].get("type") != "release_record":
        raise HarnessError("released record is unavailable or ambiguous")
    return matches[0]


def _wheel_metadata(wheel: Path) -> tuple[str, str]:
    try:
        raw = wheel.read_bytes()
    except OSError as exc:
        raise HarnessError("public wheel is unavailable") from exc
    if len(raw) > MAX_WHEEL_BYTES:
        raise HarnessError("public wheel exceeds the byte limit")
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            names = [item for item in archive.namelist() if item.endswith(".dist-info/METADATA")]
            if len(names) != 1:
                raise HarnessError("public wheel metadata is unavailable or ambiguous")
            metadata = archive.read(names[0]).decode("utf-8")
    except (OSError, UnicodeError, zipfile.BadZipFile) as exc:
        raise HarnessError("public wheel is not a valid archive") from exc
    package_names = [line.partition(":")[2].strip() for line in metadata.splitlines() if line.startswith("Name:")]
    versions = [line.partition(":")[2].strip() for line in metadata.splitlines() if line.startswith("Version:")]
    if len(package_names) != 1 or package_names[0].lower().replace("_", "-") != "se-harness" or len(versions) != 1:
        raise HarnessError("public wheel does not identify one se-harness distribution")
    if VERSION_PATTERN.fullmatch(versions[0]) is None:
        raise HarnessError("public wheel version is invalid")
    return versions[0], _sha256(raw)


def qualify_public_install(
    root: Path,
    *,
    release_record_id: str,
    public_wheel: Path,
    public_wheel_sha256: str,
    payload_sha256: str,
) -> QualificationResult:
    selected = _ordinary_root(root)
    before = _repository_snapshot(selected)
    if SHA256_PATTERN.fullmatch(public_wheel_sha256) is None or SHA256_PATTERN.fullmatch(payload_sha256) is None:
        raise HarnessError("public wheel and payload digests must be lowercase SHA-256 values")
    _, record = _release_record(selected, release_record_id)
    distribution = record.get("distribution")
    version = record.get("version")
    if record.get("status") != "released" or not isinstance(distribution, dict) or not isinstance(version, str):
        raise HarnessError("public-install requires one released distribution record")
    selected_wheel = public_wheel.expanduser().resolve()
    wheel_version, observed_wheel_sha256 = _wheel_metadata(selected_wheel)
    try:
        installed = installed_evaluator_identity()
        wheel_payload = wheel_payload_sha256(selected_wheel, wheel_version)
    except EvaluatorIdentityError as exc:
        raise HarnessError("installed public evaluator identity is unavailable") from exc
    expected_wheel_name = distribution.get("wheel")
    expected_wheel_sha256 = distribution.get("wheel_sha256")
    wheel_ok = (
        wheel_version == version == installed.version == __version__
        and selected_wheel.name == expected_wheel_name == installed.archive_name
        and observed_wheel_sha256 == public_wheel_sha256 == expected_wheel_sha256 == installed.archive_sha256
    )
    payload_ok = installed.payload_sha256 == payload_sha256 == wheel_payload
    module = Path(__file__).resolve()
    templates = template_root().resolve()
    contaminated = False
    for path in (module, templates):
        try:
            path.relative_to(selected)
        except ValueError:
            continue
        contaminated = True
    entry = _installed_entry_point()
    try:
        entry.resolve(strict=True).relative_to(Path(sys.prefix).resolve(strict=True))
    except (OSError, ValueError):
        entry_ok = False
    else:
        entry_ok = True
    version_smoke = _run([str(entry), "--version"], cwd=selected)
    qualify_smoke = _run([str(entry), "qualify", "--help"], cwd=selected)
    behavior_ok = (
        version_smoke.returncode == 0
        and version_smoke.stdout.decode("utf-8", errors="replace").strip() == version
        and qualify_smoke.returncode == 0
        and all(operation.encode("ascii") in qualify_smoke.stdout for operation in OPERATIONS)
    )
    checks = [
        _check("PI001", wheel_ok, "public-wheel", "released wheel, record, and installed archive agree" if wheel_ok else "released wheel, record, or installed archive differs"),
        _check("PI002", payload_ok, "installed-payload", "wheel and installed payload digests agree" if payload_ok else "wheel or installed payload digest differs"),
        _check("PI003", entry_ok and not contaminated, "installed-runtime", "entry point and resources are isolated from source" if entry_ok and not contaminated else "entry point or resources are contaminated"),
        _check("PI004", behavior_ok, "public-cli", "installed version and qualification surface passed" if behavior_ok else "installed CLI behavior differs"),
    ]
    after = _repository_snapshot(selected)
    checks.append(_check("PI005", before == after, "repository-state", "target state is unchanged" if before == after else "target state changed"))
    return _result(
        "public-install",
        evaluator={
            "role": "public-install",
            "distribution": "se-harness",
            "version": installed.version,
            "archive_name": installed.archive_name,
            "archive_sha256": installed.archive_sha256,
            "payload_manifest": installed.payload_manifest,
            "payload_sha256": installed.payload_sha256,
            "entry_point_sha256": _sha256(entry.read_bytes()),
        },
        target={
            "kind": "public-install",
            "release_record": release_record_id,
            "version": version,
            "commit": record.get("commit"),
            "wheel_sha256": observed_wheel_sha256,
        },
        checks=checks,
    )


QUALIFIERS: dict[str, Callable[..., QualificationResult]] = {
    "released-root": qualify_released_root,
    "predecessor-view": qualify_predecessor_view,
    "complete-candidate": qualify_complete_candidate,
    "candidate-package": qualify_candidate_package,
    "public-install": qualify_public_install,
}
