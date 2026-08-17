"""Command line entry point for the single-profile engineering harness."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from se_harness import __version__
from se_harness.artifact_layout import create_artifact, scaffold_domain
from se_harness.candidate_acceptance import assess_candidate_wheel, write_acceptance_manifest
from se_harness.installer import (
    HarnessError,
    apply_changes,
    ensure_target,
    format_plan,
    plan_install,
    template_root,
)
from se_harness.governor_reconciliation import (
    apply_governor_reconciliation,
    format_reconciliation_plan,
    plan_governor_reconciliation,
)
from se_harness.github_ci import SelectionError, select_from_event
from se_harness.preflight import inspect_installation, render_preflight, render_preflight_json, run_preflight
from se_harness.provenance import capture_verification, prepare_release
from se_harness.runtime_identity import inspect_runtime_identity, render_runtime_identity


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
        "1. Curate `docs/engineering/REPOSITORY_CONTEXT.md` with owner-confirmed purpose, commands, architecture, and constraints.",
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


def _upgrade(args: argparse.Namespace) -> int:
    target = ensure_target(Path(args.target), must_exist=True)
    changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
    print(format_plan(changes))
    if not args.apply:
        return 0
    blocked = [item for item in changes if item.action in {"customized", "protected-mismatch"}]
    if blocked:
        print("customized or protected files require manual review; no files were written:", file=sys.stderr)
        for item in blocked:
            path = item.path
            print(f"  {path}", file=sys.stderr)
        if any(item.path == ".github/workflows/engineering-harness.yml" for item in blocked):
            print(
                "preserve repository-specific CI in a separate workflow and restore the managed destination before retrying",
                file=sys.stderr,
            )
        return 1
    apply_changes(target, changes, old_lock, allow_updates=True)
    print(f"upgraded managed files to se-harness {__version__}")
    return 0


def _reconcile_governor(args: argparse.Namespace) -> int:
    target = ensure_target(Path(args.target), must_exist=True)
    plan = plan_governor_reconciliation(
        target,
        version=args.target_version,
        commit=args.target_commit,
        release_record=args.target_release_record,
        sha256=args.target_sha256,
        work_order=args.work_order,
        wheel_path=Path(args.target_wheel) if args.target_wheel else None,
        decisions=args.decisions,
    )
    print(format_reconciliation_plan(plan))
    if not args.apply:
        return 1 if plan.blocked else 0
    if plan.blocked:
        print("governor reconciliation requires explicit resolution; no files were written", file=sys.stderr)
        return 1
    apply_governor_reconciliation(target, plan)
    print(f"reconciled self-hosting controls to published governor {args.target_version}")
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


def _select_work_order(args: argparse.Namespace) -> int:
    try:
        print(select_from_event(Path(args.event)))
        return 0
    except SelectionError as exc:
        raise HarnessError(f"work-order selection: {exc}") from exc


def _capture_verification(args: argparse.Namespace) -> int:
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
    print(f"prepared ready verification record: {output}")
    return 0


def _prepare_release(args: argparse.Namespace) -> int:
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
    print(f"prepared ready release record: {output}")
    return 0


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
    return 0


def _identity(args: argparse.Namespace) -> int:
    report = inspect_runtime_identity(
        role=args.role,
        expected_version=args.expected_version,
        expected_root=Path(args.expected_root),
        checkout_root=Path(args.checkout_root) if args.checkout_root else None,
        candidate_commit=args.candidate_commit,
        governor_wheel_sha256=args.governor_wheel_sha256,
        entry_point=Path(args.entry_point) if args.entry_point else None,
        require_isolated_python=args.require_isolated_python,
        require_entry_point=args.require_entry_point,
    )
    print(render_runtime_identity(report))
    return 0 if report.passed else 1


def _accept_candidate(args: argparse.Namespace) -> int:
    manifest = assess_candidate_wheel(
        Path(args.wheel),
        candidate_commit=args.candidate_commit,
        candidate_wheel_sha256=args.candidate_wheel_sha256,
        verifier_wheel_sha256=args.governor_wheel_sha256,
        checkout_root=Path(args.checkout_root) if args.checkout_root else None,
    )
    output = Path(args.output)
    write_acceptance_manifest(output, manifest)
    print(
        f"candidate acceptance passed: {len(manifest.scenarios)} scenarios; "
        f"manifest {output.expanduser().resolve()}"
    )
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

    inspect = commands.add_parser("inspect", help="inspect repository attention and lifecycle queues")
    inspect.add_argument("target", nargs="?", default=".")
    inspect.add_argument("--json", action="store_true")
    inspect.set_defaults(
        handler=lambda args: _run_distribution_script(
            Path(args.target),
            "inspect_engineering_artifacts.py",
            ["--json"] if args.json else [],
        )
    )

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

    select_work = commands.add_parser(
        "select-work-order",
        help="select one structured work-order field from a GitHub pull-request event",
    )
    select_work.add_argument("--event", required=True)
    select_work.set_defaults(handler=_select_work_order)

    upgrade = commands.add_parser("upgrade", help="plan or apply safe managed-file upgrades")
    upgrade.add_argument("target", nargs="?", default=".")
    upgrade.add_argument("--apply", action="store_true", help="apply safe changes; customized files remain untouched")
    upgrade.set_defaults(handler=_upgrade)

    reconcile = commands.add_parser(
        "reconcile-governor",
        help="plan or apply an authorized transition to an exact published self-hosting governor",
    )
    reconcile.add_argument("target", nargs="?", default=".")
    reconcile.add_argument("--to", required=True, dest="target_version")
    reconcile.add_argument("--target-commit", required=True)
    reconcile.add_argument("--target-release-record", required=True)
    reconcile.add_argument("--target-sha256", required=True)
    reconcile.add_argument("--target-wheel", help="use an exact local wheel after SHA-256 verification")
    reconcile.add_argument("--work-order", required=True)
    reconcile.add_argument(
        "--set",
        action="append",
        default=[],
        dest="decisions",
        metavar="DOTTED.PATH=TOML_VALUE",
        help="supply one explicitly governed repository-policy value; repeat as needed",
    )
    reconcile.add_argument("--apply", action="store_true", help="apply the complete recoverable control transaction")
    reconcile.set_defaults(handler=_reconcile_governor)

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
    create.set_defaults(handler=_create_artifact)

    identity = commands.add_parser("identity", help="emit and verify one self-hosting runtime identity")
    identity.add_argument("--role", required=True, choices=("governor", "candidate-source", "candidate-package"))
    identity.add_argument("--expected-version", required=True)
    identity.add_argument("--expected-root", required=True)
    identity.add_argument("--checkout-root")
    identity.add_argument("--candidate-commit")
    identity.add_argument("--governor-wheel-sha256")
    identity.add_argument("--entry-point")
    identity.add_argument("--require-isolated-python", action="store_true")
    identity.add_argument("--require-entry-point", action="store_true")
    identity.set_defaults(handler=_identity)

    accept = commands.add_parser(
        "accept-candidate",
        help="run the released verifier-owned black-box contract against an exact candidate wheel",
    )
    accept.add_argument("--wheel", required=True)
    accept.add_argument("--candidate-commit", required=True)
    accept.add_argument("--candidate-wheel-sha256", required=True)
    accept.add_argument("--governor-wheel-sha256", required=True)
    accept.add_argument("--checkout-root")
    accept.add_argument("--output", required=True)
    accept.set_defaults(handler=_accept_candidate)

    capture = commands.add_parser("capture-verification", help="prepare a ready commit-bound verification record")
    capture.add_argument("target", nargs="?", default=".")
    capture.add_argument("--id", required=True, dest="record_id")
    capture.add_argument("--work-order", required=True, action="append", help="work order to verify; repeat for aggregate candidates")
    capture.add_argument("--verification", required=True, action="append", help="applicable verification contract; repeat for aggregate candidates")
    capture.add_argument("--evidence", required=True, action="append", help="retained evidence path; repeat for aggregate candidates")
    capture.add_argument("--owner", default="quality-owner")
    capture.add_argument("--output")
    capture.add_argument("--domain", help="place the record in an explicit engineering domain")
    capture.set_defaults(handler=_capture_verification)

    release = commands.add_parser("prepare-release", help="prepare a ready commit-bound release record")
    release.add_argument("target", nargs="?", default=".")
    release.add_argument("--id", required=True, dest="record_id")
    release.add_argument("--release-contract", required=True)
    release.add_argument("--verification-record", required=True, action="append", help="included verification record; repeat for aggregate releases")
    release.add_argument("--work-order", required=True, action="append", help="released work order; repeat for aggregate releases")
    release.add_argument("--version", required=True, dest="release_version")
    release.add_argument("--authorized-by", required=True)
    release.add_argument("--tag")
    release.add_argument("--output")
    release.add_argument("--domain", help="place the record in an explicit engineering domain")
    release.set_defaults(handler=_prepare_release)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        return int(args.handler(args))
    except HarnessError as exc:
        print(f"harnessctl: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
