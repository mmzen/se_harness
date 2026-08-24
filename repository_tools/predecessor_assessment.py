"""Hosted assessment of an exact candidate by the immutable predecessor.

Released 0.5.0 cannot parse the complete rejected-history graph.  This module
retains that exact refusal, derives the same closed two-artifact view used by
predecessor preparation, and runs fixed predecessor checks inside the view.
Candidate validation remains responsible for the complete graph.
"""

from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from repository_tools import interpreter_safety
from repository_tools import predecessor_preparation as preparation
from repository_tools import release_bootstrap as bootstrap


EVIDENCE_SCHEMA = "se-harness-predecessor-assessment-view-v1"
MAX_COMMAND_OUTPUT_BYTES = 4 * 1024 * 1024
MAX_DASHBOARD_FILES = 4096
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
OUTPUT_NAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,126}\.json")
WINDOWS_RESERVED_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{index}" for index in range(1, 10)}
    | {f"LPT{index}" for index in range(1, 10)}
)
EXPECTED_LEGACY_ERROR = {
    "code": "E009",
    "message": "release_record status must be ready or released",
    "path": "docs/engineering/release-0-6-0/releases/RLS-SEH-009.md",
    "plane": "governance",
}


class PredecessorAssessmentError(RuntimeError):
    """A hosted predecessor assessment observation violates the contract."""


@dataclass(frozen=True)
class AssessmentPlan:
    schema: str
    source_commit: str
    source_tree: str
    git_object_format: str
    release_contract: str
    version: str
    evaluator_version: str
    evaluator_archive_name: str
    evaluator_archive_sha256: str
    evaluator_payload_sha256: str
    omitted_history: tuple[preparation.HistoryDescriptor, ...]
    sparse_spec_sha256: str
    legacy_artifact_count: int
    legacy_warning_count: int
    candidate_artifact_count: int
    candidate_warning_count: int
    predecessor_artifact_count: int
    predecessor_warning_count: int
    dashboard_manifest_sha256: str
    assessment_evidence_sha256: str
    assessment_evidence_path: str | None
    changed: bool
    applied: bool

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["omitted_history"] = [asdict(item) for item in self.omitted_history]
        return value


def _canonical_json(value: Any) -> bytes:
    return preparation._canonical_json(value)


def _sha256(value: bytes) -> str:
    return preparation._sha256(value)


def _bounded_output(result: Any, label: str) -> None:
    if len(result.stdout) > MAX_COMMAND_OUTPUT_BYTES or len(result.stderr) > MAX_COMMAND_OUTPUT_BYTES:
        raise PredecessorAssessmentError(f"{label} output exceeds the byte limit")


def _run_command(command: list[str], *, cwd: Path) -> Any:
    """Run one released-evaluator command through an adapter-local seam."""

    return preparation._run(command, cwd=cwd)


def _safe_interpreter(
    path: Path,
    label: str,
    *,
    checkout_root: Path | None = None,
    declared_root: Path | None = None,
) -> interpreter_safety.SafeEntryPoint:
    """Accept an external interpreter through the declared safety rule."""

    try:
        return interpreter_safety.evaluate(
            path, checkout_root=checkout_root, declared_root=declared_root
        )
    except interpreter_safety.InterpreterSafetyRefusal as refusal:
        raise PredecessorAssessmentError(
            f"{label} is refused by {refusal.case}: {refusal.detail}"
        ) from refusal
    except interpreter_safety.InterpreterSafetyError as exc:
        raise PredecessorAssessmentError(f"{label} cannot be evaluated: {exc}") from exc


def _released_identity(
    root: Path,
    evaluator_python: Path,
    evaluator_entry_point: Path,
    contract: bootstrap.BootstrapContract,
) -> tuple[dict[str, Any], list[str], Any]:
    """Prove released runtime identity without requiring a full-graph validation."""

    safe = _safe_interpreter(
        evaluator_python, "released-evaluator interpreter", checkout_root=root
    )
    evaluator_root = safe.environment_root
    if not bootstrap._within(evaluator_entry_point, evaluator_root):
        raise PredecessorAssessmentError(
            "released-evaluator entry point is outside the interpreter environment"
        )
    arguments = [
        "-I",
        "-m",
        "se_harness",
        "identity",
        "--role",
        "released-evaluator",
        "--expected-version",
        contract.evaluator_version,
        "--expected-root",
        str(evaluator_root),
        "--checkout-root",
        str(root),
        "--entry-point",
        str(evaluator_entry_point),
        "--require-isolated-python",
        "--require-entry-point",
    ]
    result = _run_command([str(safe.entry_point), *arguments], cwd=root)
    identity = _json_report(result, "released-evaluator identity")
    required = {
        "schema",
        "passed",
        "role",
        "python_executable",
        "harness_version",
        "module_origin",
        "distribution_origin",
        "template_origin",
        "entry_point_origin",
        "expected_root",
        "checkout_root",
        "candidate_commit",
        "isolated_python",
        "user_site_enabled",
        "pythonpath_present",
        "diagnostics",
    }
    if result.returncode != 0 or not required.issubset(identity):
        raise PredecessorAssessmentError("released-evaluator identity proof is incomplete")
    if (
        identity.get("schema") not in bootstrap.RUNTIME_IDENTITY_SCHEMAS
        or identity.get("passed") is not True
        or identity.get("role") != "released-evaluator"
        or identity.get("harness_version") != contract.evaluator_version
        or identity.get("candidate_commit") is not None
        or identity.get("isolated_python") is not True
        or identity.get("user_site_enabled") is not False
        or identity.get("pythonpath_present") is not False
        or identity.get("diagnostics") != []
    ):
        raise PredecessorAssessmentError("released-evaluator identity proof is not acceptable")
    exact_paths = {
        "python_executable": safe.entry_point,
        "entry_point_origin": evaluator_entry_point,
        "expected_root": evaluator_root,
        "checkout_root": root,
    }
    for field, expected in exact_paths.items():
        value = identity.get(field)
        try:
            if field == "python_executable" and isinstance(value, str):
                observed = Path(os.path.abspath(value))
                expected_path = Path(os.path.abspath(expected))
            else:
                observed = Path(value).resolve(strict=True) if isinstance(value, str) else None
                expected_path = expected.resolve(strict=True)
        except OSError:
            observed = None
            expected_path = None
        if observed != expected_path:
            raise PredecessorAssessmentError(f"released-evaluator identity {field} differs")
    reported_facts = {
        "python_entry_is_link": safe.entry_is_link,
        "python_binary_position": safe.binary_position,
        "python_binary_sha256": safe.binary_sha256,
    }
    for field, expected_fact in reported_facts.items():
        if field in identity and identity[field] != expected_fact:
            raise PredecessorAssessmentError(f"released-evaluator identity {field} differs")
    for field in ("module_origin", "distribution_origin", "template_origin"):
        value = identity.get(field)
        if not isinstance(value, str) or not bootstrap._within(Path(value), evaluator_root):
            raise PredecessorAssessmentError(
                f"released-evaluator {field} is outside its environment"
            )
        if bootstrap._within(Path(value), root):
            raise PredecessorAssessmentError(
                f"released-evaluator {field} resolves inside the checkout"
            )
    return identity, arguments, result


def _normalize_interpreter_origin(path: Path, evaluator_root: Path) -> str:
    """Normalize a verified interpreter without dereferencing its venv link.

    The declared rule owns the decision, so the origin recorded in evidence is
    exactly the entry point the boundary accepted and never its resolved
    system binary.
    """

    safe = _safe_interpreter(
        path, "released-evaluator interpreter origin", declared_root=evaluator_root
    )
    relative = safe.entry_point.relative_to(Path(os.path.abspath(evaluator_root)))
    return f"<evaluator-root>/{relative.as_posix()}"


def _identity_evidence(
    identity: dict[str, Any],
    arguments: list[str],
    result: Any,
    *,
    checkout_root: Path,
    checkout_marker: str,
    evaluator_root: Path,
) -> dict[str, Any]:
    normalized = dict(identity)
    normalized["checkout_root"] = checkout_marker
    normalized["expected_root"] = "<evaluator-root>"
    normalized["python_executable"] = _normalize_interpreter_origin(
        Path(identity["python_executable"]), evaluator_root
    )
    for field in (
        "module_origin",
        "distribution_origin",
        "template_origin",
        "entry_point_origin",
    ):
        normalized[field] = bootstrap._normalize_origin(Path(identity[field]), evaluator_root)
    normalized_arguments = [
        checkout_marker if item == str(checkout_root) else "<evaluator-root>"
        if item == str(evaluator_root)
        else bootstrap._normalize_origin(Path(item), evaluator_root)
        if item == str(identity["entry_point_origin"])
        else item
        for item in arguments
    ]
    replacements = {checkout_root: checkout_marker, evaluator_root: "<evaluator-root>"}
    return {
        "arguments": normalized_arguments,
        "report_sha256": _sha256(_canonical_json(normalized)),
        "returncode": result.returncode,
        "stderr_sha256": _sha256(_normalized_output(result.stderr, replacements)),
    }


def _normalized_output(raw: bytes, replacements: dict[Path, str]) -> bytes:
    text = raw.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n")
    ordered = sorted(replacements.items(), key=lambda item: len(str(item[0])), reverse=True)
    for path, marker in ordered:
        values = {str(path), path.as_posix(), str(path).replace("\\", "/")}
        for value in sorted(values, key=len, reverse=True):
            text = text.replace(value, marker)
    return text.encode("utf-8")


def _json_report(result: Any, label: str) -> dict[str, Any]:
    _bounded_output(result, label)
    try:
        value = json.loads(result.stdout.decode("utf-8"), object_pairs_hook=bootstrap._unique_object)
    except (UnicodeError, json.JSONDecodeError, bootstrap.ReleaseBootstrapError) as exc:
        raise PredecessorAssessmentError(f"{label} returned invalid JSON") from exc
    if not isinstance(value, dict):
        raise PredecessorAssessmentError(f"{label} returned a non-object report")
    return value


def _report_counts(report: dict[str, Any], label: str) -> tuple[int, int, int]:
    values = tuple(report.get(name) for name in ("artifact_count", "error_count", "warning_count"))
    if any(type(value) is not int or value < 0 for value in values):
        raise PredecessorAssessmentError(f"{label} count fields are invalid")
    return values  # type: ignore[return-value]


def _validate_candidate_report(report: dict[str, Any], label: str) -> tuple[int, int]:
    artifact_count, error_count, warning_count = _report_counts(report, label)
    if report.get("valid") is not True or error_count != 0 or report.get("errors") != []:
        raise PredecessorAssessmentError(f"{label} is not valid")
    return artifact_count, warning_count


def _validate_legacy_report(report: dict[str, Any]) -> tuple[int, int]:
    artifact_count, error_count, warning_count = _report_counts(report, "legacy validation")
    if (
        report.get("valid") is not False
        or error_count != 1
        or report.get("errors") != [EXPECTED_LEGACY_ERROR]
    ):
        raise PredecessorAssessmentError("legacy full-checkout refusal differs from exact E009")
    plane_counts = report.get("plane_counts")
    if not isinstance(plane_counts, dict):
        raise PredecessorAssessmentError("legacy validation plane counts are invalid")
    for plane in ("structure", "governance", "policy", "maintenance"):
        value = plane_counts.get(plane)
        if not isinstance(value, dict) or type(value.get("errors")) is not int:
            raise PredecessorAssessmentError("legacy validation plane counts are invalid")
        expected = 1 if plane == "governance" else 0
        if value.get("errors") != expected:
            raise PredecessorAssessmentError("legacy validation has an unexpected error plane")
    return artifact_count, warning_count


def _dashboard_manifest(root: Path) -> tuple[list[dict[str, Any]], str]:
    if not root.is_dir() or bootstrap._path_has_link(root):
        raise PredecessorAssessmentError("predecessor dashboard output is unavailable or linked")
    entries: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        if path.is_dir():
            continue
        relative = path.relative_to(root).as_posix()
        if not path.is_file() or bootstrap._path_has_link(path, root):
            raise PredecessorAssessmentError(f"predecessor dashboard contains an unsafe path: {relative}")
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise PredecessorAssessmentError(
                f"predecessor dashboard output cannot be read: {relative}"
            ) from exc
        if relative == "generation-summary.json":
            try:
                summary = json.loads(
                    raw.decode("utf-8"), object_pairs_hook=bootstrap._unique_object
                )
            except (UnicodeError, json.JSONDecodeError, bootstrap.ReleaseBootstrapError) as exc:
                raise PredecessorAssessmentError(
                    "predecessor dashboard generation summary is invalid"
                ) from exc
            if (
                not isinstance(summary, dict)
                or summary.get("schema") != "harness-dashboard-generation-v2"
                or summary.get("outcome") != "generated-valid"
                or not isinstance(summary.get("generated_at"), str)
                or type(summary.get("elapsed_ms")) is not int
                or summary["elapsed_ms"] < 0
            ):
                raise PredecessorAssessmentError(
                    "predecessor dashboard generation summary is invalid"
                )
            summary["generated_at"] = "<generated-at>"
            summary["elapsed_ms"] = 0
            raw = _canonical_json(summary)
        entries.append({"bytes": len(raw), "path": relative, "sha256": _sha256(raw)})
        if len(entries) > MAX_DASHBOARD_FILES:
            raise PredecessorAssessmentError("predecessor dashboard file count exceeds the limit")
    required = {"dashboard-manifest.json", "generation-summary.json", "index.html"}
    if not required.issubset(item["path"] for item in entries):
        raise PredecessorAssessmentError("predecessor dashboard output is incomplete")
    digest = _sha256(
        _canonical_json(
            {
                "files": entries,
                "normalization": {
                    "generation-summary.json": ["elapsed_ms", "generated_at"]
                },
                "schema": "se-harness-dashboard-tree-v1",
            }
        )
    )
    return entries, digest


def _external_output(path: Path, root: Path) -> Path:
    try:
        parent = path.parent.resolve(strict=True)
    except OSError as exc:
        raise PredecessorAssessmentError("assessment evidence parent does not exist") from exc
    if not parent.is_dir() or bootstrap._path_has_link(parent):
        raise PredecessorAssessmentError("assessment evidence parent must be ordinary and unlinked")
    candidate = parent / path.name
    if (
        OUTPUT_NAME_PATTERN.fullmatch(path.name) is None
        or path.stem.upper() in WINDOWS_RESERVED_NAMES
        or path.name.endswith((".", " "))
    ):
        raise PredecessorAssessmentError("assessment evidence name is invalid")
    try:
        candidate.relative_to(root)
    except ValueError:
        return candidate
    raise PredecessorAssessmentError("assessment evidence must be outside the source checkout")


def _write_exclusive(path: Path, payload: bytes) -> None:
    descriptor: int | None = None
    created = False
    try:
        descriptor = _open_exclusive(path)
        created = True
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = None
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        if descriptor is not None:
            os.close(descriptor)
        if created:
            try:
                path.unlink()
            except OSError:
                pass
        raise PredecessorAssessmentError(f"cannot create assessment evidence: {exc}") from exc


def _open_exclusive(path: Path) -> int:
    """Open one assessment output through an adapter-local test seam."""

    return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)


def assess_predecessor_evaluator(
    repository: Path,
    *,
    candidate_commit: str,
    release_contract_id: str,
    evaluator_python: Path,
    evaluator_entry_point: Path,
    evaluator_wheel: Path,
    output: Path | None = None,
    apply: bool = False,
) -> AssessmentPlan:
    """Run fixed predecessor checks in the exact view and optionally retain JSON."""

    root = preparation._ordinary_root(repository)
    present_credentials = sorted(PUBLICATION_CREDENTIALS & set(os.environ))
    if present_credentials:
        raise PredecessorAssessmentError(
            "production credential signals are forbidden during predecessor assessment: "
            + ", ".join(present_credentials)
        )
    if apply and output is None:
        raise PredecessorAssessmentError("apply requires an external assessment evidence path")
    output_path = _external_output(output, root) if output is not None else None
    if output_path is not None and output_path.exists():
        raise PredecessorAssessmentError("assessment evidence destination already exists")
    candidate_before = preparation._candidate_validation(root)
    source_commit, source_tree, object_format = preparation._source_identity(root)
    if candidate_commit.lower() != source_commit:
        raise PredecessorAssessmentError("candidate commit differs from the exact source HEAD")
    catalog = bootstrap._artifact_catalog(root)
    _contract_path, contract_metadata = preparation._artifact(
        catalog, release_contract_id, "release_contract"
    )
    try:
        contract = bootstrap.parse_bootstrap_contract(contract_metadata)
    except bootstrap.ReleaseBootstrapError as exc:
        raise PredecessorAssessmentError(str(exc)) from exc
    history = preparation._derive_history(
        root, catalog, contract.version, source_commit, object_format
    )
    interpreter = preparation._safe_interpreter(
        evaluator_python, "evaluator interpreter", root
    )
    python = interpreter.entry_point
    evaluator_root = interpreter.environment_root
    entry_point = preparation._ordinary_external(
        evaluator_entry_point, "evaluator entry point", root
    )
    wheel = preparation._ordinary_external(evaluator_wheel, "evaluator wheel", root)
    if (
        wheel.name != contract.evaluator_archive_name
        or bootstrap._sha256_file(wheel) != contract.evaluator_archive_sha256
    ):
        raise PredecessorAssessmentError("evaluator wheel differs from the assessment contract")

    try:
        bootstrap._validate_old_root(root, contract)
        root_identity, root_identity_arguments, root_identity_run = _released_identity(
            root, python, entry_point, contract
        )
        installed_payload = bootstrap._installed_payload(root_identity, evaluator_root)
        wheel_payload = bootstrap._wheel_payload(wheel, contract.evaluator_version)
    except (OSError, bootstrap.ReleaseBootstrapError) as exc:
        raise PredecessorAssessmentError(str(exc)) from exc
    if installed_payload != wheel_payload:
        raise PredecessorAssessmentError(
            "released-evaluator installed payload differs from the exact public wheel"
        )

    legacy_doctor_arguments = ["-I", "-m", "se_harness", "doctor", "."]
    legacy_doctor = _run_command(
        [str(python), *legacy_doctor_arguments], cwd=root
    )
    _bounded_output(legacy_doctor, "legacy doctor")
    if legacy_doctor.returncode != 0:
        raise PredecessorAssessmentError("legacy full-checkout doctor did not pass")
    legacy_validate_arguments = ["-I", "-m", "se_harness", "validate", ".", "--json"]
    legacy_validate = _run_command(
        [str(python), *legacy_validate_arguments], cwd=root
    )
    legacy_report = _json_report(legacy_validate, "legacy validation")
    if legacy_validate.returncode != 1:
        raise PredecessorAssessmentError("legacy full-checkout validation did not fail exactly")
    legacy_artifacts, legacy_warnings = _validate_legacy_report(legacy_report)

    with tempfile.TemporaryDirectory(prefix="se-harness-predecessor-assessment-") as temporary:
        parent = Path(temporary)
        view, sparse_spec = preparation._create_view(root, source_commit, history, parent)
        dashboard = parent / "dashboard"
        try:
            bootstrap._validate_old_root(view, contract)
            view_identity, view_identity_arguments, view_identity_run = _released_identity(
                view, python, entry_point, contract
            )
        except bootstrap.ReleaseBootstrapError as exc:
            raise PredecessorAssessmentError(str(exc)) from exc
        if view_identity.get("schema") != root_identity.get("schema"):
            raise PredecessorAssessmentError("released-evaluator identity schema changed in the view")

        doctor_arguments = ["-I", "-m", "se_harness", "doctor", "."]
        doctor = _run_command([str(python), *doctor_arguments], cwd=view)
        _bounded_output(doctor, "predecessor doctor")
        if doctor.returncode != 0:
            raise PredecessorAssessmentError("released-evaluator doctor failed in the exact view")

        validate_arguments = ["-I", "-m", "se_harness", "validate", ".", "--json"]
        validate = _run_command([str(python), *validate_arguments], cwd=view)
        view_report = _json_report(validate, "predecessor validation")
        if validate.returncode != 0:
            raise PredecessorAssessmentError("released-evaluator validation failed in the exact view")
        predecessor_artifacts, predecessor_warnings = _validate_candidate_report(
            view_report, "predecessor view"
        )

        dashboard_arguments = [
            "-I",
            "-m",
            "se_harness",
            "dashboard",
            ".",
            "--output",
            "<assessment-output>/dashboard",
        ]
        dashboard_run = _run_command(
            [
                str(python),
                "-I",
                "-m",
                "se_harness",
                "dashboard",
                ".",
                "--output",
                str(dashboard),
            ],
            cwd=view,
        )
        _bounded_output(dashboard_run, "predecessor dashboard")
        if dashboard_run.returncode != 0:
            raise PredecessorAssessmentError("released-evaluator dashboard failed in the exact view")
        dashboard_entries, dashboard_digest = _dashboard_manifest(dashboard)

        replacements = {
            root: "<candidate-root>",
            view: "<assessment-view>",
            dashboard: "<assessment-output>/dashboard",
            evaluator_root: "<evaluator-root>",
        }
        command_evidence = {
            "identity": _identity_evidence(
                view_identity,
                view_identity_arguments,
                view_identity_run,
                checkout_root=view,
                checkout_marker="<assessment-view>",
                evaluator_root=evaluator_root,
            ),
            "doctor": {
                "arguments": doctor_arguments,
                "returncode": doctor.returncode,
                "stderr_sha256": _sha256(_normalized_output(doctor.stderr, replacements)),
                "stdout_sha256": _sha256(_normalized_output(doctor.stdout, replacements)),
            },
            "validate": {
                "arguments": validate_arguments,
                "report_sha256": _sha256(_canonical_json(view_report)),
                "returncode": validate.returncode,
            },
            "dashboard": {
                "arguments": dashboard_arguments,
                "manifest_sha256": dashboard_digest,
                "returncode": dashboard_run.returncode,
                "stderr_sha256": _sha256(
                    _normalized_output(dashboard_run.stderr, replacements)
                ),
                "stdout_sha256": _sha256(
                    _normalized_output(dashboard_run.stdout, replacements)
                ),
            },
        }

    candidate_after = preparation._candidate_validation(root)
    final_commit, final_tree, final_format = preparation._source_identity(root)
    if (final_commit, final_tree, final_format) != (source_commit, source_tree, object_format):
        raise PredecessorAssessmentError("source identity changed during predecessor assessment")
    candidate_artifacts, candidate_warnings = _validate_candidate_report(
        candidate_before, "candidate validation"
    )
    after_artifacts, after_warnings = _validate_candidate_report(
        candidate_after, "candidate replay"
    )
    if (
        _canonical_json(candidate_before) != _canonical_json(candidate_after)
        or (after_artifacts, after_warnings) != (candidate_artifacts, candidate_warnings)
    ):
        raise PredecessorAssessmentError("complete candidate validation changed during assessment")

    evidence_value = {
        "candidate": {
            "artifact_count": candidate_artifacts,
            "commit": source_commit,
            "git_object_format": object_format,
            "report_sha256": _sha256(_canonical_json(candidate_before)),
            "tree": source_tree,
            "warning_count": candidate_warnings,
        },
        "commands": command_evidence,
        "contract": {
            "id": release_contract_id,
            "release_record": contract.release_record,
            "version": contract.version,
        },
        "evaluator": {
            "archive_name": contract.evaluator_archive_name,
            "archive_sha256": contract.evaluator_archive_sha256,
            "payload_sha256": installed_payload,
            "runtime_identity_schema": root_identity.get("schema"),
            "version": contract.evaluator_version,
        },
        "legacy_full_checkout": {
            "artifact_count": legacy_artifacts,
            "diagnostic": EXPECTED_LEGACY_ERROR,
            "doctor": {
                "arguments": legacy_doctor_arguments,
                "returncode": legacy_doctor.returncode,
                "stderr_sha256": _sha256(
                    _normalized_output(legacy_doctor.stderr, {root: "<candidate-root>"})
                ),
                "stdout_sha256": _sha256(
                    _normalized_output(legacy_doctor.stdout, {root: "<candidate-root>"})
                ),
            },
            "identity": _identity_evidence(
                root_identity,
                root_identity_arguments,
                root_identity_run,
                checkout_root=root,
                checkout_marker="<candidate-root>",
                evaluator_root=evaluator_root,
            ),
            "report_sha256": _sha256(_canonical_json(legacy_report)),
            "validate_arguments": legacy_validate_arguments,
            "warning_count": legacy_warnings,
        },
        "schema": EVIDENCE_SCHEMA,
        "view": {
            "dashboard_bytes": sum(item["bytes"] for item in dashboard_entries),
            "dashboard_file_count": len(dashboard_entries),
            "dashboard_manifest_sha256": dashboard_digest,
            "omitted_history": [asdict(item) for item in history],
            "sparse_spec_sha256": _sha256(sparse_spec),
            "validation_artifact_count": predecessor_artifacts,
            "validation_warning_count": predecessor_warnings,
        },
    }
    evidence_bytes = _canonical_json(evidence_value)
    if len(evidence_bytes) > preparation.MAX_EVIDENCE_BYTES:
        raise PredecessorAssessmentError("assessment evidence exceeds the byte limit")
    evidence_digest = _sha256(evidence_bytes)

    if apply:
        assert output_path is not None
        _write_exclusive(output_path, evidence_bytes)

    return AssessmentPlan(
        schema=EVIDENCE_SCHEMA,
        source_commit=source_commit,
        source_tree=source_tree,
        git_object_format=object_format,
        release_contract=release_contract_id,
        version=contract.version,
        evaluator_version=contract.evaluator_version,
        evaluator_archive_name=contract.evaluator_archive_name,
        evaluator_archive_sha256=contract.evaluator_archive_sha256,
        evaluator_payload_sha256=installed_payload,
        omitted_history=history,
        sparse_spec_sha256=_sha256(sparse_spec),
        legacy_artifact_count=legacy_artifacts,
        legacy_warning_count=legacy_warnings,
        candidate_artifact_count=candidate_artifacts,
        candidate_warning_count=candidate_warnings,
        predecessor_artifact_count=predecessor_artifacts,
        predecessor_warning_count=predecessor_warnings,
        dashboard_manifest_sha256=dashboard_digest,
        assessment_evidence_sha256=evidence_digest,
        assessment_evidence_path=(
            f"<external-assessment-output>/{output_path.name}"
            if output_path is not None
            else None
        ),
        changed=apply,
        applied=apply,
    )
