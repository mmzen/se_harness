"""No-network disposable rehearsal for bounded evaluator-deadlock recovery."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Mapping


REHEARSAL_SCHEMA = "se-harness-evaluator-recovery-rehearsal-v1"
COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.!+\-]{0,127}")
PUBLICATION_CREDENTIALS = frozenset(
    {
        "ACTIONS_ID_TOKEN_REQUEST_TOKEN",
        "AWS_SECRET_ACCESS_KEY",
        "AZURE_CLIENT_SECRET",
        "GITHUB_TOKEN",
        "GOOGLE_APPLICATION_CREDENTIALS",
        "PYPI_API_TOKEN",
        "TWINE_PASSWORD",
    }
)
STANDARD_WORKFLOWS = (
    ".github/workflows/candidate-evidence.yml",
    ".github/workflows/engineering-harness.yml",
    ".github/workflows/publish-pypi.yml",
)


class RecoveryRehearsalError(RuntimeError):
    """The rehearsal cannot preserve its disposable safety boundary."""


def _canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"), key=lambda item: item.as_posix())
        if path.is_file() and not path.is_symlink()
    }


def _transaction(root: Path, replacements: Mapping[str, bytes], *, fail_after: int | None = None) -> None:
    snapshot = {
        root / relative: (root / relative).read_bytes() if (root / relative).is_file() else None
        for relative in sorted(replacements)
    }
    try:
        for index, relative in enumerate(sorted(replacements), start=1):
            _atomic_write(root / relative, replacements[relative])
            if fail_after is not None and index == fail_after:
                raise OSError("injected interrupted migration")
    except BaseException as exc:
        failures: list[str] = []
        for path, original in reversed(tuple(snapshot.items())):
            try:
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    _atomic_write(path, original)
            except OSError as rollback_error:
                failures.append(f"{path.name}:{type(rollback_error).__name__}")
        if failures:
            raise RecoveryRehearsalError(
                "rehearsal rollback was incomplete: " + ", ".join(failures)
            ) from exc
        raise


def _create_archive(path: Path, *, commit: str, version: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = _canonical(
        {
            "candidate_commit": commit,
            "payload": "synthetic-released-evaluator",
            "version": version,
        }
    )
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as archive:
        member = zipfile.ZipInfo("se_harness_rehearsal/identity.json", date_time=(1980, 1, 1, 0, 0, 0))
        member.external_attr = 0o100644 << 16
        archive.writestr(member, manifest)
    return _sha256(path.read_bytes())


def _verify_archive(path: Path, expected_sha256: str) -> None:
    if not path.is_file() or path.is_symlink() or _sha256(path.read_bytes()) != expected_sha256:
        raise RecoveryRehearsalError("simulated public archive identity mismatch")
    try:
        with zipfile.ZipFile(path) as archive:
            if archive.namelist() != ["se_harness_rehearsal/identity.json"]:
                raise RecoveryRehearsalError("simulated public archive member set is not exact")
            json.loads(archive.read(archive.namelist()[0]))
    except (json.JSONDecodeError, OSError, zipfile.BadZipFile) as exc:
        raise RecoveryRehearsalError("simulated public archive is invalid") from exc


def _require_external_origin(origin: Path, operational_repository: Path) -> None:
    try:
        origin.resolve().relative_to(operational_repository.resolve())
    except ValueError:
        return
    raise RecoveryRehearsalError("candidate checkout contamination was rejected")


def run_recovery_rehearsal(
    output: Path,
    *,
    operational_repository: Path,
    candidate_commit: str,
    target_version: str,
    environment: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Execute a synthetic recovery and retain one canonical factual report."""

    repository = operational_repository.expanduser().resolve()
    requested_destination = output.expanduser()
    if requested_destination.is_symlink():
        raise RecoveryRehearsalError("rehearsal output must not be a symlink")
    destination = requested_destination.resolve()
    if not repository.is_dir():
        raise RecoveryRehearsalError("operational repository must be an existing directory")
    try:
        destination.relative_to(repository)
    except ValueError:
        pass
    else:
        raise RecoveryRehearsalError("rehearsal output must be outside the operational repository")
    if destination.exists() and (
        not destination.is_dir() or any(destination.iterdir())
    ):
        raise RecoveryRehearsalError("rehearsal output must be absent or empty and must not be a symlink")
    if COMMIT_PATTERN.fullmatch(candidate_commit) is None:
        raise RecoveryRehearsalError("candidate selection must be one full immutable commit")
    if VERSION_PATTERN.fullmatch(target_version) is None:
        raise RecoveryRehearsalError("target evaluator version is invalid")
    selected_environment = os.environ if environment is None else environment
    present_credentials = sorted(PUBLICATION_CREDENTIALS & set(selected_environment))
    if present_credentials:
        raise RecoveryRehearsalError(
            "production credential signals are forbidden during rehearsal: "
            + ", ".join(present_credentials)
        )

    destination.mkdir(parents=True, exist_ok=True)
    candidate_root = destination / "candidate"
    archive_name = f"se_harness-{target_version.replace('-', '_')}-py3-none-any.whl"
    archive = candidate_root / archive_name
    archive_sha256 = _create_archive(archive, commit=candidate_commit, version=target_version)
    publication = destination / "simulated-publication" / archive_name
    _atomic_write(publication, archive.read_bytes())
    _verify_archive(publication, archive_sha256)

    external_environment = destination / "external-evaluator"
    installed_archive = external_environment / archive_name
    _atomic_write(installed_archive, publication.read_bytes())
    _require_external_origin(installed_archive, repository)
    _verify_archive(installed_archive, archive_sha256)

    negative_results: list[dict[str, Any]] = []
    try:
        _require_external_origin(repository / "candidate-wheel.whl", repository)
    except RecoveryRehearsalError:
        negative_results.append({"case": "candidate-contamination", "result": "rejected"})
    try:
        _verify_archive(publication, "0" * 64)
    except RecoveryRehearsalError:
        negative_results.append({"case": "stale-or-mismatched-identity", "result": "rejected"})
    negative_results.append(
        {
            "automatic": False,
            "case": "conflicting-chains",
            "ids": ["RLS-REHEARSAL-001", "RLS-REHEARSAL-002"],
            "result": "stopped-for-accountable-disposition",
        }
    )

    standard_root = destination / "standard-root"
    prior_evaluator = {
        "archive_name": "se_harness-0.5.0-py3-none-any.whl",
        "archive_sha256": "1" * 64,
        "payload_manifest": "se-harness-installed-payload-v1",
        "payload_sha256": "2" * 64,
        "version": "0.5.0",
    }
    target_evaluator = {
        "archive_name": archive_name,
        "archive_sha256": archive_sha256,
        "payload_manifest": "se-harness-installed-payload-v1",
        "payload_sha256": _sha256(_canonical({"archive_sha256": archive_sha256})),
        "version": target_version,
    }
    prior_lock = {"schema": 3, "tool_version": "0.5.0", "evaluator": prior_evaluator, "files": {}}
    target_lock = {"schema": 3, "tool_version": target_version, "evaluator": target_evaluator, "files": {}}
    _atomic_write(standard_root / ".engineering-harness.toml", b'[harness]\ntool_version = "0.5.0"\n')
    _atomic_write(standard_root / ".engineering-harness.lock", _canonical(prior_lock))
    replacements = {
        ".engineering-harness.lock": _canonical(target_lock),
        ".engineering-harness.toml": (
            f'[harness]\ntool_version = "{target_version}"\n'.encode("utf-8")
        ),
        **{
            workflow: b"# restored standard workflow\n"
            for workflow in STANDARD_WORKFLOWS
        },
    }
    before_interruption = _snapshot(standard_root)
    interrupted = False
    try:
        _transaction(standard_root, replacements, fail_after=2)
    except OSError:
        interrupted = True
    rollback_exact = interrupted and _snapshot(standard_root) == before_interruption
    if not rollback_exact:
        raise RecoveryRehearsalError("interrupted migration did not restore the exact prior root")
    _transaction(standard_root, replacements)

    restored_lock = json.loads((standard_root / ".engineering-harness.lock").read_bytes())
    workflows_restored = all((standard_root / path).is_file() for path in STANDARD_WORKFLOWS)
    absence_invariants = not any(
        (standard_root / path).exists()
        for path in (".self-hosting", ".github/workflows/recovery-publisher.yml")
    )
    passed = (
        restored_lock.get("evaluator") == target_evaluator
        and workflows_restored
        and absence_invariants
        and rollback_exact
        and len(negative_results) == 3
    )
    report = {
        "schema": REHEARSAL_SCHEMA,
        "result": "pass" if passed else "fail",
        "fixture": "local-immutable-archive-and-simulated-publication",
        "inputs": {
            "candidate_commit": candidate_commit,
            "target_version": target_version,
            "archive_name": archive_name,
            "archive_sha256": archive_sha256,
        },
        "stages": [
            {"name": "immutable-selection", "result": "pass"},
            {"name": "isolated-local-build", "result": "pass"},
            {"name": "simulated-publication", "result": "pass"},
            {"name": "external-install-proof", "result": "pass"},
            {"name": "interrupted-root-transaction", "result": "rolled-back"},
            {"name": "bounded-root-transaction", "result": "pass"},
            {"name": "standard-control-restoration", "result": "pass" if passed else "fail"},
        ],
        "negative_cases": negative_results,
        "resulting_standard_root_identity": target_evaluator,
        "restoration": {
            "absence_invariants": absence_invariants,
            "normal_evaluator_workflow": workflows_restored,
            "normal_candidate_workflow": workflows_restored,
            "normal_publisher": workflows_restored,
            "rollback_exact": rollback_exact,
        },
        "external_actions": {
            "credentials": False,
            "network": False,
            "publication": False,
            "release": False,
            "tag": False,
            "deployment": False,
        },
        "authority": (
            "This disposable rehearsal grants no incident, lifecycle, release, publication, "
            "deployment, or standard-root mutation authority."
        ),
    }
    _atomic_write(destination / "rehearsal-report.json", _canonical(report))
    if not passed:
        raise RecoveryRehearsalError("recovery rehearsal did not restore every standard control")
    return report
