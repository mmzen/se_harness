"""Read-only installed-harness and work-order readiness checks."""

from __future__ import annotations

import importlib.util
import json
import platform
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable

from se_harness.installer import (
    CONFIG_NAME,
    LOCK_NAME,
    HarnessError,
    ensure_target,
    load_lock,
    plan_install,
    safe_destination,
    template_files,
    template_root,
    tracked_content,
)
from se_harness.integrity import IntegrityError, canonical_text_equal, compare_lock_entry
from se_harness.self_hosting import load_governor_descriptor
from se_harness.self_hosting_policy import PROTECTED_CONTROL_PATHS, classify_self_hosting


PREFLIGHT_SCHEMA = "se-harness-preflight-v1"
WORK_ORDER_PATTERN = re.compile(r"^WO-[A-Z][A-Z0-9-]*-\d{3}$")
START_STATUSES = {"approved", "in_progress"}
REVIEW_STATUSES = START_STATUSES | {"implemented", "verified", "released"}
ACTIVE_CHAIN_STATUSES = REVIEW_STATUSES
AUTHORITY_BOUNDARY = (
    "Preflight is derived, read-only evidence. It does not approve artifacts, "
    "authorize a diff, verify work, release software, commit, push, tag, publish, or deploy."
)
REQUIRED_PATHS = (
    "AGENTS.md",
    "CLAUDE.md",
    "ENGINEERING_HARNESS.md",
    "docs/engineering/REPOSITORY_CONTEXT.md",
    "docs/engineering/README.md",
    "docs/engineering/WORKFLOW.md",
    "docs/engineering/DECISION_RIGHTS.md",
    "docs/engineering/QUALITY_GATES.md",
    "docs/engineering/TRACEABILITY.md",
    "scripts/validate_engineering_artifacts.py",
    "scripts/generate_harness_dashboard.py",
    "scripts/harness_explorer/index.template.html",
)
POLICY_PATHS = (
    "ENGINEERING_HARNESS.md",
    "docs/engineering/REPOSITORY_CONTEXT.md",
    "docs/engineering/README.md",
    "docs/engineering/WORKFLOW.md",
    "docs/engineering/DECISION_RIGHTS.md",
    "docs/engineering/QUALITY_GATES.md",
    "docs/engineering/TRACEABILITY.md",
)
CONTEXT_FIELDS = (
    ("Repository purpose", "repository_purpose"),
    ("Primary users or operators", "primary_users_or_operators"),
    ("Accountable repository owners", "accountable_repository_owners"),
    ("Setup", "setup"),
    ("Build", "build"),
    ("Test", "test"),
    ("Lint or format", "lint_or_format"),
    ("Additional required verification", "additional_required_verification"),
    ("Entry points", "entry_points"),
    ("Major components and responsibilities", "major_components_and_responsibilities"),
    ("External services or dependencies", "external_services_or_dependencies"),
    ("Generated paths", "generated_paths"),
    ("Restricted or sensitive paths", "restricted_or_sensitive_paths"),
    ("Files requiring specialized review", "files_requiring_specialized_review"),
    ("Local conventions not captured elsewhere", "local_conventions"),
)
COMMAND_KEYS = {
    "Setup": "setup",
    "Build": "build",
    "Test": "test",
    "Lint or format": "lint_or_format",
    "Additional required verification": "additional_required_verification",
}
UNRESOLVED_CONTEXT = re.compile(r"^TODO(?:\[[A-Za-z0-9-]+\])?$")
_VALIDATOR_MODULE: ModuleType | None = None
@dataclass(frozen=True, order=True)
class InstallationCheck:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True, order=True)
class PreflightDiagnostic:
    code: str
    path: str
    message: str


@dataclass(frozen=True)
class PreflightReport:
    ready: bool
    phase: str
    work_order: dict[str, str]
    diagnostics: tuple[PreflightDiagnostic, ...]
    reading_manifest: tuple[str, ...]
    repository_commands: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": PREFLIGHT_SCHEMA,
            "ready": self.ready,
            "phase": self.phase,
            "work_order": self.work_order,
            "diagnostics": [asdict(item) for item in self.diagnostics],
            "reading_manifest": list(self.reading_manifest),
            "repository_commands": self.repository_commands,
            "authority_boundary": AUTHORITY_BOUNDARY,
        }


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def inspect_installation(target: Path) -> list[InstallationCheck]:
    """Return deterministic read-only installation and managed-integrity checks."""

    target = ensure_target(target, must_exist=True)
    classification = classify_self_hosting(target)
    self_hosting = classification.enabled
    checks: list[InstallationCheck] = [
        InstallationCheck("python", sys.version_info >= (3, 11), platform.python_version()),
        InstallationCheck("config", (target / CONFIG_NAME).is_file(), CONFIG_NAME),
        InstallationCheck("lock", (target / LOCK_NAME).is_file(), LOCK_NAME),
    ]
    if classification.kind == "ambiguous":
        checks.append(InstallationCheck("self-hosting-classification", False, classification.detail))
    if self_hosting:
        try:
            governor = load_governor_descriptor(target)
            checks.append(
                InstallationCheck(
                    "self-hosting-governor",
                    True,
                    f"{governor.version} {governor.sha256}",
                )
            )
        except HarnessError as exc:
            checks.append(InstallationCheck("self-hosting-governor", False, str(exc)))
    for relative in REQUIRED_PATHS:
        checks.append(InstallationCheck(relative, (target / relative).is_file(), "required"))

    claude_path = target / "CLAUDE.md"
    if claude_path.is_file():
        try:
            import_count = sum(
                line.strip() == "@AGENTS.md"
                for line in claude_path.read_text(encoding="utf-8").splitlines()
            )
            checks.append(
                InstallationCheck(
                    "claude-import",
                    import_count == 1,
                    "@AGENTS.md" if import_count == 1 else f"expected one standalone import; found {import_count}",
                )
            )
        except (OSError, UnicodeError) as exc:
            checks.append(InstallationCheck("claude-import", False, str(exc)))

    lock_path = target / LOCK_NAME
    if not lock_path.is_file():
        return sorted(checks)

    try:
        lock = load_lock(target)
        changes, _ = plan_install(target, project_name=None, mode="upgrade")
        desired_by_path = {item.path: item for item in changes}
        expected_by_path = {item.target.as_posix(): item for item in template_files()}
        lock_files = lock.get("files", {})

        for relative, template in sorted(expected_by_path.items()):
            entry = lock_files.get(relative)
            if not isinstance(entry, dict):
                checks.append(InstallationCheck(f"lock-entry:{relative}", False, "missing"))
                continue
            if entry.get("mode") != template.mode:
                checks.append(
                    InstallationCheck(
                        f"lock-entry:{relative}",
                        False,
                        f"mode {entry.get('mode')!r}; expected {template.mode!r}",
                    )
                )
                continue
            path = safe_destination(target, Path(relative))
            if template.mode == "seed":
                expected_state = entry.get("state")
                present = path.is_file()
                passed = present if expected_state == "present" else not path.exists()
                checks.append(
                    InstallationCheck(
                        f"seed:{relative}",
                        passed,
                        str(expected_state) if passed else "state mismatch",
                    )
                )
                continue
            if not path.is_file():
                checks.append(InstallationCheck(f"managed:{relative}", False, "missing"))
                continue
            current = tracked_content(template.mode, path.read_bytes())
            if current is None:
                checks.append(InstallationCheck(f"managed:{relative}", False, "managed fragment missing"))
                continue
            desired_change = desired_by_path.get(relative)
            desired = (
                tracked_content(template.mode, desired_change.desired)
                if desired_change is not None
                else None
            )
            result = compare_lock_entry(lock, entry, current, desired=desired)
            passed = result != "mismatch"
            detail = {
                "exact": "unchanged (legacy exact)",
                "canonical": "unchanged",
                "legacy-canonical": "legacy canonical match; upgrade recommended",
                "mismatch": "customized",
            }[result]
            checks.append(InstallationCheck(f"managed:{relative}", passed, detail))
            if desired is not None and not (
                self_hosting and relative in PROTECTED_CONTROL_PATHS
            ):
                distribution_match = canonical_text_equal(current, desired)
                checks.append(
                    InstallationCheck(
                        f"distribution:{relative}",
                        distribution_match,
                        "matches distribution" if distribution_match else "differs from distribution template",
                    )
                )
            elif desired is not None:
                checks.append(
                    InstallationCheck(
                        f"distribution:{relative}",
                        True,
                        "repository-specific self-hosting control",
                    )
                )

        for relative in sorted(set(lock_files) - set(expected_by_path)):
            safe_destination(target, Path(relative))
            checks.append(InstallationCheck(f"lock-extra:{relative}", False, "not in standard template"))
    except (OSError, UnicodeError, IntegrityError, HarnessError, AttributeError) as exc:
        checks.append(InstallationCheck("lock-schema", False, str(exc)))
    return sorted(checks)


def _load_validator_module() -> ModuleType:
    global _VALIDATOR_MODULE
    if _VALIDATOR_MODULE is not None:
        return _VALIDATOR_MODULE
    path = template_root() / "scripts" / "validate_engineering_artifacts.py"
    if not path.is_file():
        raise HarnessError(f"missing distribution validator: {path}")
    module_name = "_se_harness_distribution_validator"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise HarnessError(f"cannot load distribution validator: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    _VALIDATOR_MODULE = module
    return module


def _parse_context(path: Path) -> tuple[dict[str, str], list[PreflightDiagnostic]]:
    diagnostics: list[PreflightDiagnostic] = []
    values: dict[str, list[str]] = {label: [] for label, _ in CONTEXT_FIELDS}
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return {}, [PreflightDiagnostic("C001", path.as_posix(), f"cannot read repository context: {exc}")]
    for line in text.splitlines():
        for label, _ in CONTEXT_FIELDS:
            prefix = f"- {label}:"
            if line.startswith(prefix):
                values[label].append(line[len(prefix) :].strip())

    resolved: dict[str, str] = {}
    for label, key in CONTEXT_FIELDS:
        matches = values[label]
        if not matches:
            diagnostics.append(PreflightDiagnostic("C002", path.as_posix(), f"missing context field: {label}"))
            continue
        if len(matches) > 1:
            diagnostics.append(PreflightDiagnostic("C003", path.as_posix(), f"duplicate context field: {label}"))
            continue
        value = matches[0]
        if not value or UNRESOLVED_CONTEXT.fullmatch(value):
            diagnostics.append(PreflightDiagnostic("C004", path.as_posix(), f"unresolved context field: {label}"))
            continue
        resolved[key] = value
    return resolved, diagnostics


def _targets(artifact: Any, relation: str) -> list[str]:
    value = artifact.relations.get(relation, [])
    return sorted(item for item in value if isinstance(item, str)) if isinstance(value, list) else []


def _unique_paths(items: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return tuple(result)


def run_preflight(target: Path, *, work_order_id: str, phase: str = "start") -> PreflightReport:
    """Evaluate implementation or review readiness without mutating the repository."""

    root = ensure_target(target, must_exist=True)
    if phase not in {"start", "review"}:
        raise HarnessError("preflight phase must be start or review")
    diagnostics: list[PreflightDiagnostic] = []
    for check in inspect_installation(root):
        if not check.passed:
            diagnostics.append(PreflightDiagnostic("I001", check.name, check.detail))

    context_path = root / "docs" / "engineering" / "REPOSITORY_CONTEXT.md"
    context_values, context_diagnostics = _parse_context(context_path)
    diagnostics.extend(
        PreflightDiagnostic(item.code, _relative(context_path, root), item.message)
        for item in context_diagnostics
    )

    artifacts: list[Any] = []
    validator: ModuleType | None = None
    try:
        validator = _load_validator_module()
        validation = validator.validate_repository(root)
        artifacts = list(validation.artifacts)
        diagnostics.extend(
            PreflightDiagnostic(f"A-{item.code}", item.path, item.message)
            for item in validation.errors
        )
    except Exception as exc:
        diagnostics.append(PreflightDiagnostic("A001", "docs/engineering", f"validator unavailable: {exc}"))

    work_order: Any | None = None
    work_order_summary = {"id": work_order_id, "status": "unknown", "path": ""}
    if WORK_ORDER_PATTERN.fullmatch(work_order_id) is None:
        diagnostics.append(PreflightDiagnostic("W001", work_order_id, "invalid work-order ID"))
    else:
        matches = [item for item in artifacts if item.artifact_id == work_order_id]
        if not matches:
            diagnostics.append(PreflightDiagnostic("W002", work_order_id, "unknown work-order ID"))
        elif len(matches) > 1:
            diagnostics.append(PreflightDiagnostic("W003", work_order_id, "work-order ID is not unique"))
        else:
            candidate = matches[0]
            work_order_summary = {
                "id": candidate.artifact_id,
                "status": candidate.status,
                "path": _relative(candidate.path, root),
            }
            if candidate.artifact_type != "work_order":
                diagnostics.append(PreflightDiagnostic("W004", work_order_id, "selected artifact is not a work order"))
            else:
                work_order = candidate
                allowed = START_STATUSES if phase == "start" else REVIEW_STATUSES
                if candidate.status not in allowed:
                    expected = ", ".join(sorted(allowed))
                    diagnostics.append(
                        PreflightDiagnostic(
                            "W005",
                            work_order_summary["path"],
                            f"status {candidate.status!r} is not eligible for {phase}; expected one of {expected}",
                        )
                    )

    catalog = {item.artifact_id: item for item in artifacts}

    def require_targets(source: Any, relation: str, allowed_types: set[str]) -> list[Any]:
        targets = _targets(source, relation)
        if not targets:
            diagnostics.append(
                PreflightDiagnostic(
                    "W010",
                    _relative(source.path, root),
                    f"required relation {relation!r} is empty",
                )
            )
        result: list[Any] = []
        for artifact_id in targets:
            target_artifact = catalog.get(artifact_id)
            if target_artifact is None:
                diagnostics.append(PreflightDiagnostic("W011", artifact_id, f"missing target of {relation!r}"))
                continue
            if target_artifact.artifact_type not in allowed_types:
                diagnostics.append(
                    PreflightDiagnostic(
                        "W012",
                        _relative(target_artifact.path, root),
                        f"{relation!r} targets type {target_artifact.artifact_type!r}",
                    )
                )
                continue
            if target_artifact.status not in ACTIVE_CHAIN_STATUSES:
                diagnostics.append(
                    PreflightDiagnostic(
                        "W013",
                        _relative(target_artifact.path, root),
                        f"governing artifact {artifact_id} is not active",
                    )
                )
            result.append(target_artifact)
        return result

    requirements: list[Any] = []
    specifications: list[Any] = []
    architectures: list[Any] = []
    decisions: list[Any] = []
    verifications: list[Any] = []
    capabilities: list[Any] = []
    intents: list[Any] = []
    if work_order is not None:
        requirements = require_targets(work_order, "implements", {"requirement"})
        specifications = require_targets(work_order, "specifications", {"specification"})
        architecture_items = require_targets(work_order, "architecture", {"architecture", "adr"})
        architectures = [item for item in architecture_items if item.artifact_type == "architecture"]
        decisions = [item for item in architecture_items if item.artifact_type == "adr"]
        verifications = require_targets(work_order, "verification", {"verification"})
        if not architectures:
            diagnostics.append(PreflightDiagnostic("W014", work_order_summary["path"], "no architecture is selected"))

        for requirement in requirements:
            capabilities.extend(require_targets(requirement, "derives_from", {"capability"}))
        for capability in list({item.artifact_id: item for item in capabilities}.values()):
            intents.extend(require_targets(capability, "derives_from", {"intent"}))

        requirement_ids = {item.artifact_id for item in requirements}
        coverage = {
            "specification": set().union(*(_targets(item, "specifies") for item in specifications))
            if specifications
            else set(),
            "verification": set().union(*(_targets(item, "verifies") for item in verifications))
            if verifications
            else set(),
        }
        for coverage_type, covered in coverage.items():
            missing = sorted(requirement_ids - covered)
            if missing:
                diagnostics.append(
                    PreflightDiagnostic(
                        "W016",
                        work_order_summary["path"],
                        f"{coverage_type} coverage is missing {', '.join(missing)}",
                    )
                )
        selected_architecture_ids = {item.artifact_id for item in architectures}
        selected_specification_ids = {item.artifact_id for item in specifications}
        for decision in decisions:
            if not selected_architecture_ids.intersection(_targets(decision, "decides")):
                diagnostics.append(
                    PreflightDiagnostic(
                        "W017",
                        _relative(decision.path, root),
                        "ADR does not decide a selected architecture",
                    )
                )
        if validator is not None:
            for architecture in architectures:
                traceability = validator.architecture_traceability_state(architecture, catalog)
                if traceability["state"] in {"typed", "dual_declared"}:
                    relevant = bool(
                        selected_specification_ids.intersection(traceability["conforms_to"])
                    )
                elif traceability["state"] == "legacy_requirement_trace":
                    relevant = bool(requirement_ids.intersection(traceability["legacy_targets"]))
                elif traceability["state"] == "legacy_specification_trace":
                    relevant = bool(
                        selected_specification_ids.intersection(traceability["legacy_targets"])
                    )
                else:
                    relevant = True
                if not relevant:
                    diagnostics.append(
                        PreflightDiagnostic(
                            "W021",
                            _relative(architecture.path, root),
                            f"selected architecture {architecture.artifact_id} is unrelated to selected specifications or requirements",
                        )
                    )

            for architecture in artifacts:
                if (
                    architecture.artifact_type != "architecture"
                    or architecture.status not in ACTIVE_CHAIN_STATUSES
                    or architecture.artifact_id in selected_architecture_ids
                ):
                    continue
                traceability = validator.architecture_traceability_state(architecture, catalog)
                if traceability["state"] in {"typed", "dual_declared"}:
                    applicable = bool(requirement_ids.intersection(traceability["addresses"]))
                elif traceability["state"] == "legacy_requirement_trace":
                    applicable = bool(requirement_ids.intersection(traceability["legacy_targets"]))
                elif traceability["state"] == "legacy_specification_trace":
                    applicable = bool(
                        selected_specification_ids.intersection(traceability["legacy_targets"])
                    )
                else:
                    applicable = False
                if applicable:
                    diagnostics.append(
                        PreflightDiagnostic(
                            "W022",
                            _relative(architecture.path, root),
                            f"applicable architecture {architecture.artifact_id} is not selected by the work order",
                        )
                    )

            active_decisions = [
                item for item in decisions if item.status in ACTIVE_CHAIN_STATUSES
            ]
            for architecture in architectures:
                assessment = validator.decision_assessment_state(architecture)
                selected_deciding = [
                    decision
                    for decision in active_decisions
                    if architecture.artifact_id in _targets(decision, "decides")
                ]
                if assessment["state"] in {"missing", "invalid"}:
                    details = "; ".join(assessment["issues"]) or "invalid decision assessment"
                    diagnostics.append(
                        PreflightDiagnostic(
                            "W020",
                            _relative(architecture.path, root),
                            f"architecture {architecture.artifact_id} has no valid decision assessment: {details}",
                        )
                    )
                elif assessment["state"] == "legacy_missing" and not selected_deciding:
                    diagnostics.append(
                        PreflightDiagnostic(
                            "W019",
                            _relative(architecture.path, root),
                            f"legacy architecture {architecture.artifact_id} has no selected active deciding ADR",
                        )
                    )
                elif assessment["outcome"] == "adr_required" and not selected_deciding:
                    diagnostics.append(
                        PreflightDiagnostic(
                            "W018",
                            _relative(architecture.path, root),
                            f"adr_required architecture {architecture.artifact_id} has no selected active deciding ADR",
                        )
                    )

    artifact_order = (
        sorted({item.artifact_id: item for item in intents}.values(), key=lambda item: item.artifact_id)
        + sorted({item.artifact_id: item for item in capabilities}.values(), key=lambda item: item.artifact_id)
        + sorted(requirements, key=lambda item: item.artifact_id)
        + sorted(specifications, key=lambda item: item.artifact_id)
        + sorted(architectures, key=lambda item: item.artifact_id)
        + sorted(decisions, key=lambda item: item.artifact_id)
        + sorted(verifications, key=lambda item: item.artifact_id)
        + ([work_order] if work_order is not None else [])
    )
    manifest = _unique_paths(
        list(POLICY_PATHS) + [_relative(item.path, root) for item in artifact_order]
    )
    commands = {
        COMMAND_KEYS[label]: context_values[key]
        for label, key in CONTEXT_FIELDS
        if label in COMMAND_KEYS and key in context_values
    }
    ordered_diagnostics = tuple(sorted(set(diagnostics)))
    return PreflightReport(
        ready=not ordered_diagnostics,
        phase=phase,
        work_order=work_order_summary,
        diagnostics=ordered_diagnostics,
        reading_manifest=manifest,
        repository_commands=dict(sorted(commands.items())),
    )


def render_preflight(report: PreflightReport) -> str:
    status = "PASS" if report.ready else "FAIL"
    lines = [
        f"Harness preflight: {status}",
        f"Phase: {report.phase}",
        f"Work order: {report.work_order['id']} ({report.work_order['status']})",
    ]
    if report.diagnostics:
        lines.extend(["", "Diagnostics:"])
        lines.extend(
            f"- [{item.code}] {item.path}: {item.message}"
            for item in report.diagnostics
        )
    if report.reading_manifest:
        lines.extend(["", "Reading manifest:"])
        lines.extend(f"- {path}" for path in report.reading_manifest)
    if report.repository_commands:
        lines.extend(["", "Repository commands:"])
        lines.extend(f"- {key}: {value}" for key, value in report.repository_commands.items())
    lines.extend(["", f"Authority boundary: {AUTHORITY_BOUNDARY}"])
    return "\n".join(lines)


def render_preflight_json(report: PreflightReport) -> str:
    return json.dumps(report.to_dict(), indent=2, sort_keys=True)
