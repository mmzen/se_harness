"""Command line entry point for the single-profile engineering harness."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from se_harness import __version__
from se_harness.installer import (
    HarnessError,
    apply_changes,
    ensure_target,
    format_plan,
    plan_install,
)
from se_harness.preflight import inspect_installation, render_preflight, render_preflight_json, run_preflight
from se_harness.provenance import capture_verification, prepare_release


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
    customized = [item.path for item in changes if item.action == "customized"]
    if customized:
        print("customized files were preserved and require manual review; no files were written:", file=sys.stderr)
        for path in customized:
            print(f"  {path}", file=sys.stderr)
        return 1
    apply_changes(target, changes, old_lock, allow_updates=True)
    print(f"upgraded managed files to se-harness {__version__}")
    return 0


def _run_repository_script(target: Path, script: str, extra: list[str]) -> int:
    target = ensure_target(target, must_exist=True)
    path = target / "scripts" / script
    if not path.is_file():
        raise HarnessError(f"missing managed script: {path}")
    completed = subprocess.run([sys.executable, str(path), "--root", str(target), *extra], check=False)
    return completed.returncode


def _doctor(args: argparse.Namespace) -> int:
    target = ensure_target(Path(args.target), must_exist=True)
    checks = inspect_installation(target)
    for check in checks:
        print(f"{'PASS' if check.passed else 'FAIL'} {check.name}: {check.detail}")
    return 0 if all(item.passed for item in checks) else 1


def _preflight(args: argparse.Namespace) -> int:
    report = run_preflight(
        Path(args.target),
        work_order_id=args.work_order,
        phase=args.phase,
    )
    print(render_preflight_json(report) if args.json else render_preflight(report))
    return 0 if report.ready else 1


def _capture_verification(args: argparse.Namespace) -> int:
    output = capture_verification(
        Path(args.target),
        record_id=args.record_id,
        work_order_ids=args.work_order,
        verification_ids=args.verification,
        evidence_paths=args.evidence,
        owner=args.owner,
        output=args.output,
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
    )
    print(f"prepared ready release record: {output}")
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
    validate.set_defaults(handler=lambda args: _run_repository_script(Path(args.target), "validate_engineering_artifacts.py", ["--json"] if args.json else []))

    dashboard = commands.add_parser("dashboard", help="generate the repository Harness Explorer")
    dashboard.add_argument("target", nargs="?", default=".")
    dashboard.add_argument("--output")
    dashboard.set_defaults(handler=lambda args: _run_repository_script(Path(args.target), "generate_harness_dashboard.py", ["--output", args.output] if args.output else []))

    doctor = commands.add_parser("doctor", help="check an installed harness")
    doctor.add_argument("target", nargs="?", default=".")
    doctor.set_defaults(handler=_doctor)

    preflight = commands.add_parser("preflight", help="check work-order implementation or review readiness")
    preflight.add_argument("target", nargs="?", default=".")
    preflight.add_argument("--work-order", required=True)
    preflight.add_argument("--phase", choices=("start", "review"), default="start")
    preflight.add_argument("--json", action="store_true")
    preflight.set_defaults(handler=_preflight)

    upgrade = commands.add_parser("upgrade", help="plan or apply safe managed-file upgrades")
    upgrade.add_argument("target", nargs="?", default=".")
    upgrade.add_argument("--apply", action="store_true", help="apply safe changes; customized files remain untouched")
    upgrade.set_defaults(handler=_upgrade)

    capture = commands.add_parser("capture-verification", help="prepare a ready commit-bound verification record")
    capture.add_argument("target", nargs="?", default=".")
    capture.add_argument("--id", required=True, dest="record_id")
    capture.add_argument("--work-order", required=True, action="append", help="work order to verify; repeat for aggregate candidates")
    capture.add_argument("--verification", required=True, action="append", help="applicable verification contract; repeat for aggregate candidates")
    capture.add_argument("--evidence", required=True, action="append", help="retained evidence path; repeat for aggregate candidates")
    capture.add_argument("--owner", default="quality-owner")
    capture.add_argument("--output")
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
