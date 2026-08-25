"""Read-only installed-harness and work-order readiness checks."""

from __future__ import annotations

import importlib.util
import json
import platform
import re
import subprocess
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
from se_harness.hash_bound import assess as assess_hash_bound, is_git_worktree
from se_harness.integrity import IntegrityError, canonical_text_equal, compare_lock_entry


PREFLIGHT_SCHEMA = "se-harness-preflight-v2"
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
    "docs/engineering/README.md",
    "docs/engineering/WORKFLOW.md",
    "docs/engineering/WORKFLOW.json",
    "docs/engineering/DECISION_RIGHTS.md",
    "docs/engineering/QUALITY_GATES.md",
    "docs/engineering/QUALITY_GATES.json",
    "docs/engineering/TRACEABILITY.md",
    "docs/engineering/TECHNICAL_COMMUNICATION.md",
    "docs/engineering/OPERATING_CARD.md",
    "scripts/validate_engineering_artifacts.py",
    "scripts/generate_harness_dashboard.py",
    "scripts/harness_explorer/index.template.html",
)
READING_PATHS = (
    "ENGINEERING_HARNESS.md",
    "docs/engineering/OPERATING_CARD.md",
    "AGENTS.md",
)
POLICY_PATHS = (
    "ENGINEERING_HARNESS.md",
    "docs/engineering/OPERATING_CARD.md",
    "docs/engineering/README.md",
    "docs/engineering/WORKFLOW.md",
    "docs/engineering/WORKFLOW.json",
    "docs/engineering/DECISION_RIGHTS.md",
    "docs/engineering/QUALITY_GATES.md",
    "docs/engineering/QUALITY_GATES.json",
    "docs/engineering/TRACEABILITY.md",
    "docs/engineering/TECHNICAL_COMMUNICATION.md",
)
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
    assurance: dict[str, str]
    diagnostics: tuple[PreflightDiagnostic, ...]
    reading_manifest: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": PREFLIGHT_SCHEMA,
            "ready": self.ready,
            "phase": self.phase,
            "work_order": self.work_order,
            "assurance": self.assurance,
            "diagnostics": [asdict(item) for item in self.diagnostics],
            "reading_manifest": list(self.reading_manifest),
            "authority_boundary": AUTHORITY_BOUNDARY,
        }


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _hash_bound_checks(target: Path) -> list[InstallationCheck]:
    """Return the hash-bound checks in specified order, appended after the sorted set.

    The three names are part of the observable contract in the order
    declared, effective, consistent, which is not their alphabetical order, so
    they are appended rather than merged into the sorted list. A target that is
    not a Git working tree carries no tracked set to assess and emits none of
    them; every assessable condition, including an unusable Git, fails closed.
    """

    if not is_git_worktree(target):
        return []
    return [InstallationCheck(*result) for result in assess_hash_bound(target)]


def inspect_installation(target: Path) -> list[InstallationCheck]:
    """Return deterministic read-only installation and managed-integrity checks."""

    target = ensure_target(target, must_exist=True)
    checks: list[InstallationCheck] = [
        InstallationCheck("python", sys.version_info >= (3, 11), platform.python_version()),
        InstallationCheck("config", (target / CONFIG_NAME).is_file(), CONFIG_NAME),
        InstallationCheck("lock", (target / LOCK_NAME).is_file(), LOCK_NAME),
    ]
    for relative in REQUIRED_PATHS:
        checks.append(InstallationCheck(relative, (target / relative).is_file(), "required"))
    checks.append(risk_policy_check(target))

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
        return sorted(checks) + _hash_bound_checks(target)

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
            if desired is not None:
                distribution_match = canonical_text_equal(current, desired)
                checks.append(
                    InstallationCheck(
                        f"distribution:{relative}",
                        distribution_match,
                        "matches distribution" if distribution_match else "differs from distribution template",
                    )
                )
        for relative in sorted(set(lock_files) - set(expected_by_path)):
            safe_destination(target, Path(relative))
            checks.append(InstallationCheck(f"lock-extra:{relative}", False, "not in standard template"))
    except (OSError, UnicodeError, IntegrityError, HarnessError, AttributeError) as exc:
        checks.append(InstallationCheck("lock-schema", False, str(exc)))
    return sorted(checks) + _hash_bound_checks(target)


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


def _targets(artifact: Any, relation: str) -> list[str]:
    value = artifact.relations.get(relation, [])
    return sorted(item for item in value if isinstance(item, str)) if isinstance(value, list) else []


def risk_policy_check(target: Path) -> InstallationCheck:
    """C-RSK-001: the [risk] section of the installation file is absent or valid (RSK2-DOC-001)."""

    path = target / CONFIG_NAME
    if not path.is_file():
        return InstallationCheck("risk-policy", True, "C-RSK-001: no installation file; default acceptance level 1")
    try:
        import tomllib

        data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, ValueError) as exc:
        return InstallationCheck("risk-policy", False, f"C-RSK-001: cannot read {CONFIG_NAME}: {exc}")
    table = data.get("risk")
    if table is None:
        return InstallationCheck("risk-policy", True, "C-RSK-001: [risk] absent; default acceptance level 1")
    if not isinstance(table, dict) or not set(table).issubset({"acceptance_level", "scale", "release_requires_disposition"}):
        return InstallationCheck("risk-policy", False, "C-RSK-001: [risk] carries an unknown key")
    level = table.get("acceptance_level", 1)
    if type(level) is not int or not 1 <= level <= 25:
        return InstallationCheck("risk-policy", False, f"C-RSK-001: acceptance_level must be an integer 1-25, not {level!r}")
    if table.get("scale", "5x5") != "5x5":
        return InstallationCheck("risk-policy", False, "C-RSK-001: scale must be 5x5")
    if table.get("release_requires_disposition", True) is not True:
        return InstallationCheck("risk-policy", False, "C-RSK-001: release_requires_disposition must be true")
    return InstallationCheck("risk-policy", True, f"C-RSK-001: acceptance level {level}")


def _commit_is_ancestor(root: Path, commit: str, reference: str = "HEAD") -> bool | None:
    """True/False for Git ancestry; None when the question cannot be answered here."""

    if not is_git_worktree(root) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        return None
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", commit, reference],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode == 0:
        return True
    if completed.returncode == 1:
        return False
    return None


def orphaned_ready_records(root: Path, artifacts: Iterable[Any], work_order_id: str) -> list[str]:
    """W-ADS-002: ready verification records for the work order whose candidate left HEAD."""

    messages: list[str] = []
    for artifact in sorted(artifacts, key=lambda item: item.artifact_id):
        if artifact.artifact_type != "verification_record" or artifact.status != "ready":
            continue
        if work_order_id not in _targets(artifact, "verifies_work_order"):
            continue
        commit = artifact.metadata.get("commit")
        if not isinstance(commit, str):
            continue
        if _commit_is_ancestor(root, commit) is False:
            messages.append(
                f"{artifact.artifact_id} is ready and binds candidate {commit}, which is not an ancestor of HEAD; "
                "the only routes are verify, reject, or a successor record bound to a fresh commit"
            )
    return messages


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
    assurance_summary = {
        "commit_bound_verification": "unknown",
        "rationale": "",
        "decided_by": "",
    }
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
                if validator is not None:
                    assurance = validator.work_order_assurance_state(candidate)
                    if assurance["state"] == "valid":
                        assurance_summary = {
                            "commit_bound_verification": assurance["commit_bound_verification"],
                            "rationale": assurance["rationale"],
                            "decided_by": assurance["decided_by"],
                        }
                    else:
                        details = "; ".join(assurance["issues"])
                        if not details:
                            details = "assurance classification is missing"
                        diagnostics.append(
                            PreflightDiagnostic(
                                "W023",
                                work_order_summary["path"],
                                "selected work order requires an accountable explicit assurance decision: "
                                + details,
                            )
                        )
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

    def require_targets(
        source: Any,
        relation: str,
        allowed_types: set[str],
        *,
        required: bool = True,
    ) -> list[Any]:
        targets = _targets(source, relation)
        if required and not targets:
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
        architecture_items = require_targets(
            work_order,
            "architecture",
            {"architecture", "adr"},
            required=False,
        )
        architectures = [item for item in architecture_items if item.artifact_type == "architecture"]
        decisions = [item for item in architecture_items if item.artifact_type == "adr"]
        verifications = require_targets(work_order, "verification", {"verification"})

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

    if phase == "review" and work_order is not None:
        for message in orphaned_ready_records(root, artifacts, work_order.artifact_id):
            diagnostics.append(PreflightDiagnostic("W-ADS-002", work_order.artifact_id, message))

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
        list(READING_PATHS) + [_relative(item.path, root) for item in artifact_order]
    )
    ordered_diagnostics = tuple(sorted(set(diagnostics)))
    return PreflightReport(
        ready=not ordered_diagnostics,
        phase=phase,
        work_order=work_order_summary,
        assurance=assurance_summary,
        diagnostics=ordered_diagnostics,
        reading_manifest=manifest,
    )


def render_preflight(report: PreflightReport) -> str:
    status = "PASS" if report.ready else "FAIL"
    lines = [
        f"Harness preflight: {status}",
        f"Phase: {report.phase}",
        f"Work order: {report.work_order['id']} ({report.work_order['status']})",
        "",
        "Assurance classification:",
        f"- Commit-bound verification: {report.assurance['commit_bound_verification']}",
        f"- Decided by: {report.assurance['decided_by'] or 'unavailable'}",
        f"- Rationale: {report.assurance['rationale'] or 'unavailable'}",
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
    lines.extend(["", f"Authority boundary: {AUTHORITY_BOUNDARY}"])
    return "\n".join(lines)


def render_preflight_json(report: PreflightReport) -> str:
    return json.dumps(report.to_dict(), indent=2, sort_keys=True)
