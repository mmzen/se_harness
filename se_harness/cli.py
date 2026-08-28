"""Command line entry point for the single-profile engineering harness."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from se_harness import __version__
from se_harness.agent_contract import AgentContractError
from se_harness.artifact_layout import create_artifact, scaffold_domain
from se_harness.change_bundle import ChangeBundleError
from se_harness.delegated_authority import DelegatedAuthorityError
from se_harness.delegated_workflow import (
    CompletionProof,
    DelegatedStop,
    DelegatedWorkflowError,
    EffectProof,
    LifecycleProof,
    candidate_commit_stop,
    delegated_change_bundle_apply,
    delegated_vrec_prepare,
    delegated_work_order_complete,
    delegated_work_order_start,
    phase4_operation_catalog,
)
from se_harness.installer import (
    HarnessError,
    apply_changes,
    ensure_target,
    format_plan,
    plan_install,
    template_root,
)
from se_harness.effect_broker import EffectBrokerError
from se_harness.github_ci import SelectionError, select_from_event
from se_harness.preflight import inspect_installation, render_preflight, render_preflight_json, run_preflight
from se_harness.provenance import capture_verification, prepare_release
from se_harness.renumber import (
    RenumberError,
    apply_renumber_plan,
    build_renumber_plan,
    render_human as render_renumber_human,
    render_human_error as render_renumber_human_error,
    render_json as render_renumber_json,
    render_json_error as render_renumber_json_error,
)
from se_harness.recovery_rehearsal import RecoveryRehearsalError, run_recovery_rehearsal
from se_harness.release_qualification import (
    failed_qualification,
    qualify_candidate_package,
    qualify_complete_candidate,
    qualify_public_install,
    qualify_released_root,
    render_qualification,
    write_qualification_result,
)
from se_harness.runtime_identity import inspect_runtime_identity, render_runtime_identity
from se_harness.repository_state import EvaluatorIdentity, RepositoryObservationError
from se_harness.runtime_state import RuntimeStateError, RuntimeStateStore
from se_harness.workflow_compliance import check_workflow
from se_harness.workflow_contract import ContractError
from se_harness.workflow_procedures import ProcedureError
from se_harness.workflow_result import (
    render_human as render_workflow_human_v2,
    render_json as render_workflow_json_v2,
)
from se_harness.workflow import (
    RepositoryWorkflowError,
    failed_result,
    focus,
    plan_transition,
    preparation_result,
)


def _scan_repository(target: Path) -> bytes:
    indicators = {
        "Rust": ["Cargo.toml"],
        "Python": ["pyproject.toml", "requirements.txt", "setup.py"],
        "JavaScript/TypeScript": ["package.json", "tsconfig.json"],
        "Java/JVM": ["pom.xml", "build.gradle", "build.gradle.kts"],
        ".NET": ["*.sln", "*.csproj"],
        "Go": ["go.mod"],
    }
    detected: list[str] = []
    for label, patterns in indicators.items():
        if any(any(target.glob(pattern)) for pattern in patterns):
            detected.append(label)
    ci = []
    for candidate in (".github/workflows", ".gitlab-ci.yml", "azure-pipelines.yml"):
        if (target / candidate).exists():
            ci.append(candidate)
    lines = [
        "# Engineering Harness Adoption Report",
        "",
        "> Generated inventory only. This report does not approve or infer product intent, requirements, architecture, or release authority.",
        "",
        "## Observed repository signals",
        "",
        f"- Repository: `{target.name}`",
        f"- Detected ecosystems: {', '.join(detected) if detected else 'none detected'}",
        f"- Existing CI entry points: {', '.join(ci) if ci else 'none detected'}",
        "",
        "## Human decisions required",
        "",
        "1. Record build, test, verification, ownership, and boundary facts in the owner-controlled region of `AGENTS.md`.",
        "2. Name the accountable owners for product intent, engineering, assurance, release, and operations.",
        "3. Create and approve the first intent-to-verification artifact chain using `docs/engineering/templates/`.",
        "4. Select one bounded approved work order before implementation begins.",
        "5. Add repository-specific formatter, linter, test, security, build, release, and operating checks to the verification contract.",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def _install(args: argparse.Namespace, mode: str) -> int:
    target = Path(args.target)
    report = _scan_repository(target.resolve()) if mode == "adopt" else None
    changes, old_lock = plan_install(target, project_name=args.project_name, mode=mode, adoption_report=report)
    print(format_plan(changes))
    if any(item.action == "conflict" for item in changes):
        print("conflicts must be resolved before installation; no files were written", file=sys.stderr)
        if any(
            item.action == "conflict"
            and item.path == ".github/workflows/engineering-harness.yml"
            for item in changes
        ):
            print(
                "preserve repository-specific CI under another workflow filename, then rerun installation",
                file=sys.stderr,
            )
        return 1
    if args.dry_run:
        return 0
    apply_changes(target.resolve(), changes, old_lock, allow_updates=False)
    print(f"installed se-harness {__version__} in {target.resolve()}")
    return 0


def _report_undeclared_legacy_releases(target: Path) -> None:
    """Notice, without refusing, the released records an apply would refuse over."""

    from se_harness.legacy_release_evidence import (
        DECLARATION_FIELD,
        LegacyReleaseEvidenceError,
        undeclared_legacy_releases,
    )

    try:
        undeclared = undeclared_legacy_releases(target)
    except LegacyReleaseEvidenceError as exc:
        print(f"cannot assess released records for evaluator evidence: {exc}", file=sys.stderr)
        return
    if not undeclared:
        return
    authority = "an approved work order"
    print(
        "notice: these released records predate evaluator-evidence enforcement and are "
        "not declared; applying an evaluator identity transition would be refused:",
        file=sys.stderr,
    )
    for identifier in undeclared:
        print(f"  {identifier}", file=sys.stderr)
    print(
        f"declare them in {authority} under [evaluator_upgrade].{DECLARATION_FIELD}",
        file=sys.stderr,
    )


def _upgrade(args: argparse.Namespace) -> int:
    target = ensure_target(Path(args.target), must_exist=True)
    changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
    print(format_plan(changes))
    if not args.apply:
        # REQ-LRE-002: report on the planning path what an apply would refuse, so the
        # operator learns it before the transaction rather than from a frozen gate.
        _report_undeclared_legacy_releases(target)
        return 0
    blocked = [item for item in changes if item.action == "customized"]
    if blocked:
        print("customized files require manual review; no files were written:", file=sys.stderr)
        for item in blocked:
            path = item.path
            print(f"  {path}", file=sys.stderr)
        if any(item.path == ".github/workflows/engineering-harness.yml" for item in blocked):
            print(
                "preserve repository-specific CI in a separate workflow and restore the managed destination before retrying",
                file=sys.stderr,
            )
        return 1
    apply_changes(
        target,
        changes,
        old_lock,
        allow_updates=True,
        evidence_output=Path(args.evidence_output) if args.evidence_output else None,
    )
    print(f"upgraded managed files to se-harness {__version__}")
    if args.evidence_output:
        print(f"retained evaluator-upgrade evidence at {args.evidence_output}")
    else:
        print("no transaction evidence retained; pass --evidence-output to keep it")
    return 0


def _rehearse_recovery(args: argparse.Namespace) -> int:
    output = Path(args.output)
    try:
        report = run_recovery_rehearsal(
            output,
            operational_repository=Path(args.repository),
            candidate_commit=args.candidate_commit,
            target_version=args.target_version,
        )
    except RecoveryRehearsalError as exc:
        raise HarnessError(str(exc)) from exc
    print(f"recovery rehearsal: {report['result'].upper()}")
    print(f"report: {(output.resolve() / 'rehearsal-report.json')}")
    return 0


def _distribution_script(script: str) -> Path:
    path = template_root() / "scripts" / script
    if not path.is_file():
        raise HarnessError(f"missing distribution script: {path}")
    return path


def _distribution_environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment["PYTHONNOUSERSITE"] = "1"
    return environment


def _run_distribution_script(
    target: Path,
    script: str,
    extra: list[str],
) -> int:
    target = ensure_target(target, must_exist=True)
    path = _distribution_script(script)
    completed = subprocess.run(
        [sys.executable, "-B", str(path), "--root", str(target), *extra],
        cwd=target,
        env=_distribution_environment(),
        check=False,
    )
    return completed.returncode


def _inspect_repository(args: argparse.Namespace) -> int:
    target = ensure_target(Path(args.target), must_exist=True)
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(_distribution_script("inspect_engineering_artifacts.py")),
            "--root",
            str(target),
            *(["--json"] if args.json else []),
        ],
        cwd=target,
        env=_distribution_environment(),
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout
    if completed.returncode == 0 and args.json:
        try:
            report = json.loads(output)
        except json.JSONDecodeError:
            pass
        else:
            report["mode"] = "repository_wide"
            report["selection"] = {"primary": None, "artifacts": []}
            output = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    elif completed.returncode == 0:
        output = output.replace("Harness inspection", "Harness inspection (repository_wide)", 1)
    print(output, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    return completed.returncode


def _doctor(args: argparse.Namespace) -> int:
    target = ensure_target(Path(args.target), must_exist=True)
    checks = inspect_installation(target)
    for check in checks:
        print(f"{'PASS' if check.passed else 'FAIL'} {check.name}: {check.detail}")
    validator = _distribution_script("validate_engineering_artifacts.py")
    if validator.is_file():
        completed = subprocess.run(
            [sys.executable, "-B", str(validator), "--root", str(target), "--json"],
            cwd=target,
            env=_distribution_environment(),
            check=False,
            capture_output=True,
            text=True,
        )
        try:
            report = json.loads(completed.stdout)
        except json.JSONDecodeError:
            report = {}
        for warning in report.get("warnings", []):
            if isinstance(warning, dict) and warning.get("code") == "W013":
                print(f"WARN {warning['code']}: {warning.get('path', '<unknown>')}: {warning.get('message', '')}")
    return 0 if all(item.passed for item in checks) else 1


def _preflight(args: argparse.Namespace) -> int:
    report = run_preflight(
        Path(args.target),
        work_order_id=args.work_order,
        phase=args.phase,
    )
    print(render_preflight_json(report) if args.json else render_preflight(report))
    return 0 if report.ready else 1


def _render_selected_result(result: dict, args: argparse.Namespace) -> str:
    return render_workflow_json_v2(result) if args.json else render_workflow_human_v2(result)


def _check(args: argparse.Namespace) -> int:
    if args.change_manifest and (args.changed_path or args.changes_complete):
        raise HarnessError(
            "WEX200: --change-manifest is mutually exclusive with --changed-path and --changes-complete"
        )
    try:
        result = check_workflow(
            Path(args.target),
            artifact_id=args.artifact,
            checkpoint=args.checkpoint,
            procedure_id=args.procedure,
            changed_paths=args.changed_path,
            changes_complete=args.changes_complete,
            change_manifest=Path(args.change_manifest) if args.change_manifest else None,
            pull_request_body=Path(args.pull_request_body) if args.pull_request_body else None,
            target=args.target_state,
        )
    except (HarnessError, ContractError, ProcedureError, ValueError) as exc:
        result = failed_result("check", args.artifact, str(exc), code="WEX210")
    print(render_workflow_json_v2(result) if args.json else render_workflow_human_v2(result), end="")
    return 0 if result["operation"]["outcome"] == "completed" else 1


def _select_work_order(args: argparse.Namespace) -> int:
    try:
        print(select_from_event(Path(args.event), field=args.field))
        return 0
    except SelectionError as exc:
        raise HarnessError(f"work-order selection: {exc}") from exc


def _capture_verification(args: argparse.Namespace) -> int:
    try:
        output = capture_verification(
            Path(args.target),
            record_id=args.record_id,
            work_order_ids=args.work_order,
            verification_ids=args.verification,
            evidence_paths=args.evidence,
            owner=args.owner,
            output=args.output,
            domain=args.domain,
        )
        result = preparation_result(Path(args.target), args.record_id, "capture-verification", output)
    except HarnessError as exc:
        result = failed_result("capture-verification", args.record_id, str(exc), code="WEX301")
        print(_render_selected_result(result, args), end="", file=sys.stdout if args.json else sys.stderr)
        return 2
    print(_render_selected_result(result, args), end="")
    return 0


def _prepare_release(args: argparse.Namespace) -> int:
    try:
        output = prepare_release(
            Path(args.target),
            record_id=args.record_id,
            release_contract_id=args.release_contract,
            verification_record_ids=args.verification_record,
            work_order_ids=args.work_order,
            version=args.release_version,
            authorized_by=args.authorized_by,
            tag=args.tag,
            output=args.output,
            domain=args.domain,
        )
        result = preparation_result(Path(args.target), args.record_id, "prepare-release", output)
    except HarnessError as exc:
        result = failed_result("prepare-release", args.record_id, str(exc), code="WEX401")
        print(_render_selected_result(result, args), end="", file=sys.stdout if args.json else sys.stderr)
        return 2
    print(_render_selected_result(result, args), end="")
    return 0


def _focus(args: argparse.Namespace) -> int:
    try:
        result = focus(
            Path(args.target),
            args.artifact,
            include_background=args.include_background,
        )
    except HarnessError as exc:
        result = failed_result(
            "focus",
            args.artifact,
            str(exc),
            code="WEX101",
            repository_blocker=isinstance(exc, RepositoryWorkflowError),
        )
    print(_render_selected_result(result, args), end="")
    return 0 if result["operation"]["outcome"] == "completed" else 1


def _assignments(values: list[str], label: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise HarnessError(f"{label} must use ID=VALUE")
        artifact_id, selected = value.split("=", 1)
        artifact_id = artifact_id.strip()
        selected = selected.strip()
        if not artifact_id or not selected:
            raise HarnessError(f"{label} must use a non-empty ID and value")
        if artifact_id in result:
            raise HarnessError(f"duplicate {label} for {artifact_id}")
        result[artifact_id] = selected
    return result


def _refusal_code(exc: Exception) -> str:
    """The identifier of the check that refused, else the operation's generic code (ECP-KRN-008)."""

    return str(getattr(exc, "predicate_id", "") or "WEX201")


def _transition(args: argparse.Namespace) -> int:
    primary: str | None = None
    try:
        transitions = _assignments(args.transitions, "--set")
        primary = sorted(transitions)[0] if transitions else None
        decisions = _assignments(args.decisions, "--decision")
        reasons = _assignments(args.reasons, "--reason")
        plan = plan_transition(
            Path(args.target),
            transitions,
            decisions,
            reasons,
            apply=args.apply,
        )
        result = plan.result
    except HarnessError as exc:
        result = failed_result(
            "transition",
            primary,
            str(exc),
            code=_refusal_code(exc),
            repository_blocker=isinstance(exc, RepositoryWorkflowError),
        )
    print(_render_selected_result(result, args), end="")
    return 0 if result["operation"]["outcome"] == "completed" else 1


def _scaffold_domain(args: argparse.Namespace) -> int:
    changes = scaffold_domain(
        Path(args.target),
        domain=args.domain,
        title=args.title,
        dry_run=args.dry_run,
    )
    for change in changes:
        print(f"{change.action:8} {change.path}")
    if args.dry_run:
        print("dry run: no files were written")
    else:
        print(f"canonical domain scaffold is available: docs/engineering/{args.domain}")
    return 0


def _create_artifact(args: argparse.Namespace) -> int:
    change = create_artifact(
        Path(args.target),
        domain=args.domain,
        artifact_type=args.artifact_type,
        artifact_id=args.artifact_id,
        dry_run=args.dry_run,
    )
    print(f"{change.action:8} {change.path}")
    if args.dry_run:
        print("dry run: no files were written")
    else:
        print("created an incomplete draft; complete accountable fields and run harnessctl validate before approval")
        if not args.quiet:
            from se_harness.artifact_layout import authoring_checklist

            bullets = authoring_checklist(Path(args.target), args.artifact_type)
            if bullets:
                print(f"authoring checklist for {args.artifact_type} (docs/engineering/ARTIFACT_AUTHORING.md):")
                for item in bullets:
                    print(f"- {item}")
    return 0


def _renumber_artifacts(args: argparse.Namespace) -> int:
    try:
        plan = build_renumber_plan(Path(args.target), args.mappings)
        if args.apply:
            plan = apply_renumber_plan(plan)
        print(
            render_renumber_json(plan, applied=args.apply)
            if args.json
            else render_renumber_human(plan, applied=args.apply)
        )
        return 0
    except RenumberError as exc:
        if args.json:
            print(render_renumber_json_error(exc))
        else:
            print(render_renumber_human_error(exc), file=sys.stderr)
        return 1


def _release_unit(args: argparse.Namespace) -> int:
    from se_harness.release_unit import (
        PACKAGED_SURFACE_PREFIXES,
        compare_with_contract,
        derive_release_unit,
        render_gates_toml,
        render_release_unit,
    )
    from se_harness.workflow import _catalog, _validation

    root = Path(args.target)
    _, report = _validation(root)
    catalog = _catalog(report)

    def lookup(work_order: str) -> tuple[str | None, bool | None]:
        artifact = catalog.get(work_order)
        if artifact is None:
            return None, None
        status = artifact.metadata.get("status")
        scope = artifact.metadata.get("execution_scope", {})
        paths = scope.get("paths", []) if isinstance(scope, dict) else []
        packaged = any(isinstance(item, str) and item.startswith(PACKAGED_SURFACE_PREFIXES) for item in paths)
        return (status if isinstance(status, str) else None), packaged

    unit = derive_release_unit(root, from_ref=args.from_ref, to_ref=args.to_ref, exempt=args.exempt or (), lookup=lookup)
    findings: list[str] = []
    if args.contract:
        contract = catalog.get(args.contract)
        if contract is None or contract.metadata.get("type") != "release_contract":
            raise HarnessError(f"{args.contract} is not a release contract in this repository")
        findings = compare_with_contract(unit, contract.metadata)
    if args.toml:
        print(render_gates_toml(unit), end="")
    elif args.json:
        value = unit.to_dict()
        if args.contract:
            value["contract"] = {"id": args.contract, "findings": findings}
        print(json.dumps(value, indent=2, sort_keys=True))
    else:
        print(render_release_unit(unit, findings if args.contract else None))
    return 0 if unit.complete and not findings else 1


def _identity(args: argparse.Namespace) -> int:
    report = inspect_runtime_identity(
        role=args.role,
        expected_version=args.expected_version,
        expected_root=Path(args.expected_root),
        checkout_root=Path(args.checkout_root) if args.checkout_root else None,
        candidate_commit=args.candidate_commit,
        evaluator_payload_sha256=args.evaluator_payload_sha256,
        evaluator_wheel_sha256=args.evaluator_wheel_sha256,
        entry_point=Path(args.entry_point) if args.entry_point else None,
        require_isolated_python=args.require_isolated_python,
        require_entry_point=args.require_entry_point,
    )
    print(render_runtime_identity(report))
    return 0 if report.passed else 1


def _qualify(args: argparse.Namespace) -> int:
    operation = args.qualification_operation
    forbidden_roots: tuple[Path, ...] = ()
    try:
        if operation == "released-root":
            root = Path(args.target)
            result = qualify_released_root(root)
            forbidden_roots = (root.expanduser().resolve(),)
        elif operation == "complete-candidate":
            root = Path(args.target)
            result = qualify_complete_candidate(
                root,
                candidate_commit=args.candidate_commit,
            )
            forbidden_roots = (root.expanduser().resolve(),)
        elif operation == "candidate-package":
            checkout = Path(args.checkout_root) if args.checkout_root else None
            result = qualify_candidate_package(
                Path(args.candidate_wheel),
                candidate_commit=args.candidate_commit,
                candidate_wheel_sha256=args.candidate_wheel_sha256,
                verifier_wheel_sha256=args.verifier_wheel_sha256,
                checkout_root=checkout,
            )
            forbidden_roots = (checkout.expanduser().resolve(),) if checkout is not None else ()
        elif operation == "public-install":
            root = Path(args.target)
            result = qualify_public_install(
                root,
                release_record_id=args.release_record,
                public_wheel=Path(args.public_wheel),
                public_wheel_sha256=args.public_wheel_sha256,
                payload_sha256=args.payload_sha256,
            )
            forbidden_roots = (root.expanduser().resolve(),)
        else:
            raise HarnessError("qualification operation is unsupported")
    except (HarnessError, OSError, ValueError) as exc:
        result = failed_qualification(
            operation,
            code="RQ001",
            subject="qualification-input",
            message=str(exc),
        )

    if args.output:
        try:
            write_qualification_result(
                Path(args.output),
                result,
                forbidden_roots=forbidden_roots,
            )
        except HarnessError as exc:
            result = failed_qualification(
                operation,
                code="RQ002",
                subject="qualification-output",
                message=str(exc),
            )
    if args.json:
        print(result.canonical_bytes().decode("utf-8"), end="")
    else:
        print(render_qualification(result), end="")
    return 0 if result.passed else 1


def _accept_candidate(args: argparse.Namespace) -> int:
    """Compatibility alias for the typed candidate-package operation."""

    args.qualification_operation = "candidate-package"
    args.candidate_wheel = args.wheel
    args.json = False
    return _qualify(args)


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON field: {key}")
        value[key] = item
    return value


def _bounded_json(path: str, label: str) -> object:
    source = Path(path)
    try:
        raw = source.read_bytes()
        if len(raw) > 2_000_000:
            raise ValueError("input exceeds 2 MB")
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_json_object)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise HarnessError(f"delegated workflow {label}: {exc}") from exc


def _json_array(path: str, label: str) -> list[dict[str, object]]:
    value = _bounded_json(path, label)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise HarnessError(f"delegated workflow {label} must be a JSON array of objects")
    return value


def _lifecycle_proof(path: str, label: str) -> LifecycleProof:
    value = _bounded_json(path, label)
    expected = {"receipt", "envelope", "before_observation", "after_observation"}
    if (
        not isinstance(value, dict)
        or set(value) != expected
        or any(not isinstance(value[item], dict) for item in expected)
    ):
        raise HarnessError(
            f"delegated workflow {label} must contain exactly receipt, envelope, "
            "before_observation, and after_observation objects"
        )
    return LifecycleProof(
        receipt=value["receipt"],
        envelope=value["envelope"],
        before_observation=value["before_observation"],
        after_observation=value["after_observation"],
    )


def _lifecycle_proof_value(result: object) -> dict[str, object]:
    return {
        "receipt": result.receipt.value,
        "envelope": result.envelope.value,
        "before_observation": result.before_observation.value,
        "after_observation": result.after_observation.value,
    }


def _delegated_evaluator(args: argparse.Namespace) -> EvaluatorIdentity:
    return EvaluatorIdentity(
        package=args.evaluator_package,
        version=args.evaluator_version,
        payload_sha256=args.evaluator_payload_sha256,
        launcher_sha256=args.evaluator_launcher_sha256,
    )


def _delegated_catalog(args: argparse.Namespace) -> int:
    value = [dict(item) for item in phase4_operation_catalog()]
    if args.json:
        print(json.dumps(value, indent=2, ensure_ascii=True) + "\n", end="")
    else:
        for item in value:
            print(
                f"{item['id']}: {item['current_status']} -> {item['result_status']} "
                f"({item['decision_right'] or 'started-work execution'})"
            )
    return 0


def _delegated_execute(args: argparse.Namespace) -> int:
    evaluator = _delegated_evaluator(args)
    root = Path(args.target)
    store = RuntimeStateStore(Path(args.runtime_root), root)
    start_gates = _json_array(args.start_gates, "start gates")
    effect_gates = _json_array(args.effect_gates, "effect gates")
    completion_gates = _json_array(args.completion_gates, "completion gates")
    prepare_gates = _json_array(args.prepare_gates, "preparation gates")
    tests = _json_array(args.tests, "tests")
    evidence = _json_array(args.evidence_bindings, "evidence bindings")
    effect_deviations = _json_array(args.effect_deviations, "effect deviations")
    completion_deviations = tuple(
        {
            "code": item.get("code"),
            "operation": "change-bundle-apply",
            "status": "completed",
            "message": item.get("message"),
            "evidence_path": None,
            "details_sha256": None,
        }
        for item in effect_deviations
    )
    start = delegated_work_order_start(
        root,
        work_order_id=args.work_order,
        delegate=args.delegate,
        execution_profile=args.execution_profile,
        gates=start_gates,
        evaluator=evaluator,
        runtime_store=store,
    )
    assert start.session is not None
    effect = delegated_change_bundle_apply(
        root,
        work_order_id=args.work_order,
        delegate=args.delegate,
        execution_profile=args.execution_profile,
        requested_paths=args.changed_path,
        baseline_workspace=Path(args.baseline_workspace),
        proposed_workspace=Path(args.proposed_workspace),
        object_store=Path(args.object_store),
        intended_deletions=args.delete_path,
        previous_receipt_sha256=start.receipt.sha256,
        gates=effect_gates,
        evidence=evidence,
        deviations=effect_deviations,
        evaluator=evaluator,
        runtime_store=store,
        session=start.session,
    )
    completion = delegated_work_order_complete(
        root,
        work_order_id=args.work_order,
        delegate=args.delegate,
        execution_profile=args.execution_profile,
        proof=CompletionProof(
            start=LifecycleProof(
                start.receipt,
                start.envelope,
                start.before_observation,
                start.after_observation,
            ),
            effects=(
                EffectProof(
                    effect.result.receipt,
                    effect.before_observation,
                    effect.after_observation,
                ),
            ),
            changed_paths=tuple(args.changed_path),
            tests=tuple(tests),
            gates=tuple(completion_gates),
            evidence=tuple(evidence),
            deviations=completion_deviations,
            residual_uncertainty=tuple(args.residual_uncertainty),
        ),
        evaluator=evaluator,
        runtime_store=store,
        session=start.session,
    )
    stop = candidate_commit_stop(
        work_order_id=args.work_order,
        repository=completion.receipt.value["selection"]["repository"],
        evaluator=evaluator,
        declared_paths=completion.workflow_result["scope"]["declared_paths"],
        changed_paths=completion.workflow_result["scope"]["changed_paths"],
        gates=prepare_gates,
        evidence=completion.receipt.value["effects"]["evidence"],
        residual_uncertainty=args.residual_uncertainty,
    )
    output = {
        "outcome": "completed-at-git-stop",
        "work_order": args.work_order,
        "start": {"result": start.workflow_result, "lifecycle_proof": _lifecycle_proof_value(start)},
        "effects": [{
            "receipt": effect.result.receipt.value,
            "envelope": effect.envelope.value,
            "before_observation": effect.before_observation.value,
            "after_observation": effect.after_observation.value,
            "bundle_sha256": effect.bundle.bundle.sha256,
        }],
        "completion": {
            "result": completion.workflow_result,
            "lifecycle_proof": _lifecycle_proof_value(completion),
        },
        "next": {"result": stop.workflow_result, "decision_packet": stop.decision_packet.value},
    }
    print(json.dumps(output, indent=2, ensure_ascii=True) + "\n", end="")
    return 0


def _delegated_prepare_vrec(args: argparse.Namespace) -> int:
    evaluator = _delegated_evaluator(args)
    root = Path(args.target)
    store = RuntimeStateStore(Path(args.runtime_root), root)
    result = delegated_vrec_prepare(
        root,
        work_order_id=args.work_order,
        record_id=args.record_id,
        verification_ids=args.verification,
        evidence_paths=args.evidence,
        owner=args.owner,
        output=args.output,
        domain=args.domain,
        delegate=args.delegate,
        execution_profile=args.execution_profile,
        gates=_json_array(args.gates, "preparation gates"),
        completion_proof=_lifecycle_proof(args.completion_proof, "completion proof"),
        evaluator=evaluator,
        runtime_store=store,
        residual_uncertainty=args.residual_uncertainty,
    )
    if isinstance(result, DelegatedStop):
        value = {"outcome": "stopped", "result": result.workflow_result, "decision_packet": result.decision_packet.value}
    else:
        value = {
            "outcome": "prepared",
            "record": result.record_path.relative_to(root.resolve()).as_posix(),
            "receipt": result.receipt.value,
            "result": result.workflow_result,
            "decision_packet": result.decision_packet.value,
        }
    print(json.dumps(value, indent=2, ensure_ascii=True) + "\n", end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="harnessctl", description="Install and operate the standard software-engineering harness.")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)

    for name in ("init", "adopt"):
        command = commands.add_parser(name, help=f"{name} the standard harness")
        command.add_argument("target", nargs="?", default=".")
        command.add_argument("--project-name")
        command.add_argument("--dry-run", action="store_true")
        command.set_defaults(handler=lambda args, selected=name: _install(args, selected))

    validate = commands.add_parser("validate", help="validate the repository artifact graph")
    validate.add_argument("target", nargs="?", default=".")
    validate.add_argument("--json", action="store_true")
    validate.set_defaults(handler=lambda args: _run_distribution_script(Path(args.target), "validate_engineering_artifacts.py", ["--json"] if args.json else []))

    inspect = commands.add_parser("inspect", help="inspect repository-wide attention and lifecycle queues")
    inspect.add_argument("target", nargs="?", default=".")
    inspect.add_argument("--json", action="store_true")
    inspect.set_defaults(handler=_inspect_repository)

    dashboard = commands.add_parser("dashboard", help="generate the repository Harness Explorer")
    dashboard.add_argument("target", nargs="?", default=".")
    dashboard.add_argument("--output")
    dashboard.set_defaults(handler=lambda args: _run_distribution_script(Path(args.target), "generate_harness_dashboard.py", ["--output", args.output] if args.output else []))

    doctor = commands.add_parser("doctor", help="check an installed harness")
    doctor.add_argument("target", nargs="?", default=".")
    doctor.set_defaults(handler=_doctor)

    preflight = commands.add_parser("preflight", help="check work-order implementation or review readiness")
    preflight.add_argument("target", nargs="?", default=".")
    preflight.add_argument("--work-order", required=True)
    preflight.add_argument("--phase", choices=("start", "review"), default="start")
    preflight.add_argument("--json", action="store_true")
    preflight.set_defaults(handler=_preflight)

    selected_focus = commands.add_parser("focus", help="project one selected WO, VREC, or RLS workflow scope")
    selected_focus.add_argument("target", nargs="?", default=".")
    selected_focus.add_argument("--artifact", required=True)
    selected_focus.add_argument("--json", action="store_true")
    selected_focus.add_argument("--include-background", action="store_true")
    selected_focus.set_defaults(handler=_focus)

    check = commands.add_parser("check", help="evaluate one selected workflow checkpoint and emit canonical restitution")
    check.add_argument("target", nargs="?", default=".")
    check.add_argument("--artifact", required=True, help="one selected WO, VREC, or RLS ID")
    check.add_argument(
        "--checkpoint", required=True, choices=("start", "pre-action", "transition", "handoff"),
        help="fixed stateless evaluation checkpoint",
    )
    check.add_argument(
        "--target", dest="target_state",
        help="target lifecycle state; required for and limited to the transition checkpoint",
    )
    check.add_argument(
        "--procedure",
        help="selected PROC ID; required for pre-action and limited to declared alternatives",
    )
    check.add_argument(
        "--changed-path", action="append", default=[],
        help="normalized repository-relative changed path; repeat for the declared set",
    )
    check.add_argument(
        "--changes-complete", action="store_true",
        help="assert that repeated changed paths are complete; this is evidence, not trusted proof",
    )
    check.add_argument(
        "--change-manifest",
        help="in-repository se-harness-change-set-v1 JSON; exclusive with changed-path options",
    )
    check.add_argument(
        "--pull-request-body",
        help="UTF-8 pull-request body file; reports W-ADS-001 when its work-order trailer carries a carriage return",
    )
    check.add_argument("--json", action="store_true", help="emit se-harness-workflow-result-v2 JSON")
    check.set_defaults(handler=_check)

    transition = commands.add_parser("transition", help="plan or atomically apply explicit lifecycle transitions")
    transition.add_argument("target", nargs="?", default=".")
    transition.add_argument("--set", required=True, action="append", dest="transitions", help="explicit ID=STATUS transition; repeat for packets")
    transition.add_argument("--decision", required=True, action="append", dest="decisions", help="ID=ACTOR assertion; repeat for every selected artifact")
    transition.add_argument("--reason", action="append", default=[], dest="reasons", help="ID=TEXT reason; required for rejection, or use successor VREC ID for supersession")
    transition.add_argument("--apply", action="store_true", help="apply the exact validated transaction; default is read-only planning")
    transition.add_argument("--json", action="store_true")
    transition.set_defaults(handler=_transition)

    select_work = commands.add_parser(
        "select-work-order",
        help="select one structured work-order field from a GitHub pull-request event",
    )
    select_work.add_argument("--event", required=True)
    select_work.add_argument(
        "--field", choices=("work-order", "restitution-digest"), default="work-order",
        help="declared field to select; restitution-digest prints empty text when absent",
    )
    select_work.set_defaults(handler=_select_work_order)

    upgrade = commands.add_parser("upgrade", help="plan or apply safe managed-file upgrades")
    upgrade.add_argument("target", nargs="?", default=".")
    upgrade.add_argument("--apply", action="store_true", help="apply safe changes; customized files remain untouched")
    upgrade.add_argument(
        "--evidence-output",
        help="optional repository JSON path below docs/engineering/.../evidence/ for the transaction evidence",
    )
    upgrade.set_defaults(handler=_upgrade)

    rehearse = commands.add_parser(
        "rehearse-recovery",
        help="run a no-network evaluator-recovery rehearsal in a disposable directory",
    )
    rehearse.add_argument("output", help="absent or empty directory outside the operational repository")
    rehearse.add_argument("--repository", default=".", help="operational repository that must remain unchanged")
    rehearse.add_argument("--candidate-commit", required=True, help="full synthetic immutable candidate commit")
    rehearse.add_argument("--target-version", default="999.0.0", help="synthetic target evaluator version")
    rehearse.set_defaults(handler=_rehearse_recovery)


    scaffold = commands.add_parser("scaffold-domain", help="safely create the canonical organization for one engineering domain")
    scaffold.add_argument("target", nargs="?", default=".")
    scaffold.add_argument("--domain", required=True)
    scaffold.add_argument("--title")
    scaffold.add_argument("--dry-run", action="store_true")
    scaffold.set_defaults(handler=_scaffold_domain)

    create = commands.add_parser("create-artifact", help="create one incomplete draft from the canonical artifact template")
    create.add_argument("target", nargs="?", default=".")
    create.add_argument("--domain", required=True)
    create.add_argument("--type", required=True, dest="artifact_type")
    create.add_argument("--id", required=True, dest="artifact_id")
    create.add_argument("--dry-run", action="store_true")
    create.add_argument("--quiet", action="store_true", help="do not print the authoring checklist after creation")
    create.set_defaults(handler=_create_artifact)

    renumber = commands.add_parser(
        "renumber-artifacts",
        help="plan or apply explicit structured artifact renumbering",
    )
    renumber.add_argument("target", nargs="?", default=".")
    renumber.add_argument(
        "--map",
        required=True,
        action="append",
        dest="mappings",
        metavar="OLD=NEW",
        help="explicit type-compatible identifier mapping; repeat for a set",
    )
    renumber.add_argument("--json", action="store_true")
    renumber.add_argument(
        "--apply",
        action="store_true",
        help="apply the validated structured changes and path moves",
    )
    renumber.set_defaults(handler=_renumber_artifacts)

    release_unit = commands.add_parser(
        "release-unit", help="derive a release unit's work-order census from the commits between the previous release tag and a candidate commit"
    )
    release_unit.add_argument("target", nargs="?", default=".")
    release_unit.add_argument("--from", dest="from_ref", required=True, help="the previous release tag")
    release_unit.add_argument("--to", dest="to_ref", required=True, help="the candidate commit or ref")
    release_unit.add_argument("--exempt", action="append", help="full commit id on the first-parent path that carries no trailer by owner decision; repeatable")
    release_unit.add_argument("--contract", help="a release contract to compare with; E-CIP-001 findings fail the command")
    release_unit.add_argument("--json", action="store_true", help="emit the canonical JSON census")
    release_unit.add_argument("--toml", action="store_true", help="emit only the gates array ready to paste into a contract")
    release_unit.set_defaults(handler=_release_unit)

    identity = commands.add_parser("identity", help="emit and verify one evaluator or candidate runtime identity")
    identity.add_argument("--role", required=True, choices=("released-evaluator", "candidate-source", "candidate-package"))
    identity.add_argument("--expected-version", required=True)
    identity.add_argument("--expected-root", required=True)
    identity.add_argument("--checkout-root")
    identity.add_argument("--candidate-commit")
    identity.add_argument("--evaluator-payload-sha256")
    identity.add_argument("--evaluator-wheel-sha256")
    identity.add_argument("--entry-point")
    identity.add_argument("--require-isolated-python", action="store_true")
    identity.add_argument("--require-entry-point", action="store_true")
    identity.set_defaults(handler=_identity)

    qualify = commands.add_parser(
        "qualify",
        help="run one typed, provenance-bound release qualification operation",
    )
    qualification = qualify.add_subparsers(
        dest="qualification_operation",
        required=True,
    )

    def qualification_output(command: argparse.ArgumentParser) -> None:
        command.add_argument(
            "--output",
            help="external absent path for the canonical qualification result",
        )
        command.add_argument("--json", action="store_true")
        command.set_defaults(handler=_qualify)

    released_root = qualification.add_parser(
        "released-root",
        help="qualify a repository with the released evaluator that owns its root lock",
    )
    released_root.add_argument("target", nargs="?", default=".")
    qualification_output(released_root)

    complete_candidate = qualification.add_parser(
        "complete-candidate",
        help="qualify the complete candidate graph as candidate-controlled evidence",
    )
    complete_candidate.add_argument("target", nargs="?", default=".")
    complete_candidate.add_argument("--candidate-commit", required=True)
    qualification_output(complete_candidate)

    candidate_package = qualification.add_parser(
        "candidate-package",
        help="qualify an exact candidate wheel from an isolated released verifier",
    )
    candidate_package.add_argument("--candidate-wheel", required=True)
    candidate_package.add_argument("--candidate-commit", required=True)
    candidate_package.add_argument("--candidate-wheel-sha256", required=True)
    candidate_package.add_argument("--verifier-wheel-sha256", required=True)
    candidate_package.add_argument("--checkout-root")
    qualification_output(candidate_package)

    public_install = qualification.add_parser(
        "public-install",
        help="qualify an exact public wheel and the clean environment installed from it",
    )
    public_install.add_argument("target", nargs="?", default=".")
    public_install.add_argument("--release-record", required=True)
    public_install.add_argument("--public-wheel", required=True)
    public_install.add_argument("--public-wheel-sha256", required=True)
    public_install.add_argument("--payload-sha256", required=True)
    qualification_output(public_install)

    accept = commands.add_parser(
        "accept-candidate",
        help="compatibility alias for qualify candidate-package",
    )
    accept.add_argument("--wheel", required=True)
    accept.add_argument("--candidate-commit", required=True)
    accept.add_argument("--candidate-wheel-sha256", required=True)
    accept.add_argument("--verifier-wheel-sha256", required=True)
    accept.add_argument("--checkout-root")
    accept.add_argument("--output", required=True)
    accept.set_defaults(handler=_accept_candidate)

    capture = commands.add_parser("capture-verification", help="prepare a ready commit-bound verification record")
    capture.add_argument("target", nargs="?", default=".")
    capture.add_argument("--id", required=True, dest="record_id")
    capture.add_argument("--work-order", required=True, action="append", help="work order to verify; repeat for aggregate candidates")
    capture.add_argument("--verification", required=True, action="append", help="applicable verification contract; repeat for aggregate candidates")
    capture.add_argument("--evidence", required=True, action="append", help="retained evidence path; repeat for aggregate candidates")
    capture.add_argument("--owner", default="quality-owner", help="preparation actor and record owner; does not verify the record")
    capture.add_argument("--output")
    capture.add_argument("--domain", help="place the record in an explicit engineering domain")
    capture.add_argument("--json", action="store_true", help="emit the canonical workflow result as JSON")
    capture.set_defaults(handler=_capture_verification)

    delegated = commands.add_parser(
        "delegated-workflow",
        help="run the closed Phase 4 delegated workflow through the exact evaluator",
    )
    delegated_commands = delegated.add_subparsers(dest="delegated_operation", required=True)

    delegated_catalog = delegated_commands.add_parser(
        "catalog",
        help="inspect the closed managed Phase 4 operation catalog",
    )
    delegated_catalog.add_argument("--json", action="store_true")
    delegated_catalog.set_defaults(handler=_delegated_catalog)

    def delegated_identity(command: argparse.ArgumentParser) -> None:
        command.add_argument("--runtime-root", required=True, help="external non-overlapping runtime-state directory")
        command.add_argument("--evaluator-package", required=True)
        command.add_argument("--evaluator-version", required=True)
        command.add_argument("--evaluator-payload-sha256", required=True)
        command.add_argument("--evaluator-launcher-sha256", required=True)
        command.add_argument("--work-order", required=True)
        command.add_argument("--delegate", default="implementation-worker")
        command.add_argument("--execution-profile", default="implementer")
        command.add_argument("--residual-uncertainty", action="append", default=[])

    delegated_execute = delegated_commands.add_parser(
        "execute",
        help="start, apply one brokered bundle, complete, and stop before Git",
    )
    delegated_execute.add_argument("target", nargs="?", default=".")
    delegated_identity(delegated_execute)
    delegated_execute.add_argument("--baseline-workspace", required=True)
    delegated_execute.add_argument("--proposed-workspace", required=True)
    delegated_execute.add_argument("--object-store", required=True)
    delegated_execute.add_argument("--changed-path", action="append", required=True)
    delegated_execute.add_argument("--delete-path", action="append", default=[])
    delegated_execute.add_argument("--start-gates", required=True)
    delegated_execute.add_argument("--effect-gates", required=True)
    delegated_execute.add_argument("--completion-gates", required=True)
    delegated_execute.add_argument("--prepare-gates", required=True)
    delegated_execute.add_argument("--tests", required=True)
    delegated_execute.add_argument("--evidence-bindings", required=True)
    delegated_execute.add_argument("--effect-deviations", required=True)
    delegated_execute.set_defaults(handler=_delegated_execute)

    delegated_prepare = delegated_commands.add_parser(
        "prepare-vrec",
        help="prepare one undecided ready VREC from an existing clean candidate",
    )
    delegated_prepare.add_argument("target", nargs="?", default=".")
    delegated_identity(delegated_prepare)
    delegated_prepare.add_argument("--id", required=True, dest="record_id")
    delegated_prepare.add_argument("--verification", action="append", required=True)
    delegated_prepare.add_argument("--evidence", action="append", required=True)
    delegated_prepare.add_argument("--owner", default="quality-owner")
    delegated_prepare.add_argument("--output", required=True)
    delegated_prepare.add_argument("--domain", required=True)
    delegated_prepare.add_argument("--gates", required=True)
    delegated_prepare.add_argument("--completion-proof", required=True)
    delegated_prepare.set_defaults(handler=_delegated_prepare_vrec)

    release = commands.add_parser("prepare-release", help="prepare a ready commit-bound release record")
    release.add_argument("target", nargs="?", default=".")
    release.add_argument("--id", required=True, dest="record_id")
    release.add_argument("--release-contract", required=True)
    release.add_argument("--verification-record", required=True, action="append", help="included verification record; repeat for aggregate releases")
    release.add_argument("--work-order", required=True, action="append", help="released work order; repeat for aggregate releases")
    release.add_argument("--version", required=True, dest="release_version")
    release.add_argument(
        "--authorized-by",
        required=True,
        help="retained compatibility name for the preparation actor and owner; does not authorize release",
    )
    release.add_argument("--tag")
    release.add_argument("--output")
    release.add_argument("--domain", help="place the record in an explicit engineering domain")
    release.add_argument("--json", action="store_true", help="emit the canonical workflow result as JSON")
    release.set_defaults(handler=_prepare_release)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        return int(args.handler(args))
    except (
        AgentContractError,
        ChangeBundleError,
        ContractError,
        DelegatedAuthorityError,
        DelegatedWorkflowError,
        EffectBrokerError,
        HarnessError,
        RepositoryObservationError,
        RuntimeStateError,
    ) as exc:
        print(f"harnessctl: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
