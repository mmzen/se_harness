"""Rehearse the real root-evaluator handover: the successor's `upgrade --apply`.

`WO-ECP-010` (`REQ-ECP-012`, `SPEC-ECP-007` `ECP-PRD-008`; repository issue
#210). The operational checkout is never written. Its tracked tree is exported
to a throwaway directory whose lock is the released predecessor's, and then:

1. the predecessor evaluator's `doctor` must pass there (it owns the root);
2. the successor's `upgrade` is planned and applied with retained evidence;
3. the successor's `doctor` must pass and its `validate` must report no error
   other than `E012` on a `ready` record, the one consequence a root change
   has on records prepared under the previous evaluator;
4. the predecessor's `doctor` must now fail (it no longer owns the root);
5. the resulting lock must be schema 3 naming the successor's version and
   installed-payload digest.

The result's `semantic_sha256` is the canonical `utf8-text-lf-v1` digest of
the resulting lock, the value two runs and two platforms must agree on. The
module uses the standard library only, imports nothing from `se_harness`, and
opens no network connection; both evaluators run with `-I` from their own
environments with credential-bearing variables stripped.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import time
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

SCHEMA = "se-harness-upgrade-rehearsal-v1"
RESULT_NAME = "upgrade-rehearsal-result.json"
TIMING_NAME = "upgrade-rehearsal-timing.json"
LOCK_NAME = ".engineering-harness.lock"
TRANSACTION_EVIDENCE = "docs/engineering/evidence/upgrade-rehearsal-transaction.json"
#: The one validator error a root change legitimately produces: a `ready`
#: record binds the evaluator identity of the lock it was prepared under.
TOLERATED_ERROR = re.compile(r"^- \[E012\] .* evaluator evidence differs from the standard lock$")
ERROR_LINE = re.compile(r"^- \[E[0-9A-Z-]+\] ")
# The validator prints three numbers up to 0.11.0 and a fourth, `Advisories`, from
# 0.12.0 (SPEC-AUT-002 AUT-ADV-003); both forms are one summary line.
SUMMARY_LINE = re.compile(r"^Artifacts: (\d+) \| Errors: (\d+) \| Warnings: (\d+)(?: \| Advisories: (\d+))?$")
FAIL_LINE = re.compile(r"^FAIL ")
_SECRET = re.compile(r"(TOKEN|SECRET|PASSWORD|CREDENTIAL|_KEY$|^AWS_|^AZURE_|^GOOGLE_)", re.IGNORECASE)


class UpgradeRehearsalError(RuntimeError):
    """The rehearsal could not be set up; distinct from a failed rehearsal."""


@dataclass(frozen=True)
class Completed:
    exit_code: int
    stdout: str
    stderr: str


Runner = Callable[[Sequence[str], Path], Completed]


class RehearsalTiming:
    """Optional observations, separate from the handover result and its digest.

    Children of replay are sequential; sum them once and compare with replay.
    The remainder includes Python checks, output and measurement overhead.
    Boundary snapshots retain running stages if the process is interrupted.
    """

    def __init__(self, output: Path, clock: Callable[[], float] = time.perf_counter):
        self.output = output
        self.clock = clock
        self.data: dict[str, Any] = {
            "schema": "se-harness-upgrade-timing-v1", "complete": False,
            "identity": {key: os.environ.get(key) for key in (
                "GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "GITHUB_SHA", "GITHUB_JOB",
                "REHEARSAL_HEAD_SHA", "RUNNER_OS", "ImageOS", "ImageVersion",
            )},
            "stages": [], "diagnostic_errors": [],
        }

    def persist(self) -> None:
        try:
            temporary = self.output / (TIMING_NAME + ".tmp")
            temporary.write_text(json.dumps(self.data, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
            temporary.replace(self.output / TIMING_NAME)
        except OSError as exc:
            self.data["complete"] = False
            self.data["diagnostic_errors"].append(type(exc).__name__)

    def progress(self, text: str) -> None:
        try:
            print(f"upgrade timing: {text}", file=sys.stderr, flush=True)
        except OSError as exc:
            self.data["diagnostic_errors"].append(type(exc).__name__)

    @contextmanager
    def measure(self, identifier: str):
        entry = {"id": identifier, "parent": None if identifier == "replay" else "replay", "status": "running"}
        self.data["stages"].append(entry)
        self.persist()
        self.progress(f"start {identifier}")
        started = self.clock()
        try:
            yield entry
        except BaseException as exc:
            entry.update(status="error", error_type=type(exc).__name__)
            raise
        else:
            entry["status"] = "finished"
        finally:
            entry["elapsed_seconds"] = self.clock() - started
            self.progress(f"end {identifier}: {entry['elapsed_seconds']:.6f}s ({entry['status']})")
            self.persist()


def _measure(timing: RehearsalTiming | None, identifier: str):
    return timing.measure(identifier) if timing else nullcontext({})


@contextmanager
def _scratch(workspace: Path | None, timing: RehearsalTiming | None):
    # Keep TemporaryDirectory's original exception/cleanup behavior.
    temporary = tempfile.TemporaryDirectory(prefix="upgrade-rehearsal-", dir=str(workspace) if workspace else None)
    try:
        yield temporary.__enter__()
    finally:
        with _measure(timing, "scratch-cleanup"):
            temporary.__exit__(*sys.exc_info())


def _environment() -> dict[str, str]:
    environment = {
        key: value
        for key, value in os.environ.items()
        if not _SECRET.search(key) and key not in {"PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP"}
    }
    environment["PYTHONNOUSERSITE"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    return environment


RUN_TIMEOUT_SECONDS = 600


def run(argv: Sequence[str], cwd: Path) -> Completed:
    # ECP-COR-015: bounded; a timeout is a failed Completed, never a hang.
    try:
        completed = subprocess.run(
            list(argv), cwd=str(cwd), env=_environment(), capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=False, timeout=RUN_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return Completed(124, "", f"{argv[0]} timed out after {RUN_TIMEOUT_SECONDS} seconds")
    return Completed(completed.returncode, completed.stdout, completed.stderr)


def canonical_sha256(raw: bytes) -> str:
    """The `utf8-text-lf-v1` digest: UTF-8 text with every newline form as LF."""

    text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def export_tracked_tree(repository: Path, destination: Path, runner: Runner = run, *, timing: RehearsalTiming | None = None) -> None:
    """Copy the committed tree (never the working tree) into `destination` and commit it there."""

    with _measure(timing, "git-archive") as observation:
        archive = subprocess.run(
            ["git", "-c", "core.autocrlf=false", "archive", "--format=tar", "HEAD"],
            cwd=str(repository), capture_output=True, check=False, timeout=RUN_TIMEOUT_SECONDS,
        )
        if archive.returncode != 0:
            raise UpgradeRehearsalError(f"cannot export the tracked tree: {archive.stderr.decode('utf-8', 'replace').strip()}")
        observation["archive_bytes"] = len(archive.stdout)
    with _measure(timing, "archive-extraction") as observation:
        with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
            tar.extractall(destination, filter="data")
            if timing:
                members = tar.getmembers()
                observation.update(entries=len(members), files=sum(member.isfile() for member in members))
    for identifier, argv in (
        ("git-init", ["git", "init", "-q", "-b", "main"]),
        # These repositories are deleted immediately after the replay.
        # Automatic maintenance must not outlive the command that starts it.
        ("git-config-maintenance", ["git", "config", "maintenance.auto", "false"]),
        ("git-config-gc", ["git", "config", "gc.auto", "0"]),
        ("git-config-autocrlf", ["git", "config", "core.autocrlf", "false"]),
        ("git-config-email", ["git", "config", "user.email", "rehearsal@example.invalid"]),
        ("git-config-name", ["git", "config", "user.name", "upgrade rehearsal"]),
        ("git-config-signing", ["git", "config", "commit.gpgsign", "false"]),
        ("git-add", ["git", "add", "-A"]),
        ("git-commit", ["git", "commit", "-q", "-m", "exported tracked tree"]),
    ):
        with _measure(timing, identifier) as observation:
            completed = runner(argv, destination)
            observation["exit_code"] = completed.exit_code
            if completed.exit_code != 0:
                raise UpgradeRehearsalError(f"cannot prepare the throwaway repository: {' '.join(argv)}: {completed.stderr.strip()}")
    if timing:
        with timing.measure("git-storage-paths") as observation:
            completed = runner([
                "git", "rev-parse", "--path-format=absolute", "--absolute-git-dir",
                "--git-path", "index", "--git-path", "objects",
            ], destination)
            observation["exit_code"] = completed.exit_code
            paths = completed.stdout.strip().splitlines()
            if completed.exit_code != 0 or len(paths) != 3 or not all(Path(path).is_absolute() for path in paths):
                timing.data["diagnostic_errors"].append("git-storage-paths")
            else:
                timing.data["storage"].update(zip(("git_directory", "index_file", "object_directory"), paths))


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _evaluator(python: Path) -> list[str]:
    return [str(python), "-I", "-m", "se_harness"]


def _version(python: Path, runner: Runner, cwd: Path) -> str:
    completed = runner([*_evaluator(python), "--version"], cwd)
    version = completed.stdout.strip().splitlines()[-1].strip() if completed.stdout.strip() else ""
    if completed.exit_code != 0 or not re.fullmatch(r"[0-9]+(?:\.[0-9]+){2}(?:[A-Za-z0-9.+-]*)?", version):
        raise UpgradeRehearsalError(f"cannot read the evaluator version of {python}: {completed.stderr.strip()}")
    return version


def _validation_errors(stdout: str) -> tuple[list[str], list[str], dict[str, int] | None]:
    tolerated: list[str] = []
    other: list[str] = []
    summary: dict[str, int] | None = None
    for line in stdout.splitlines():
        line = line.rstrip()
        if TOLERATED_ERROR.match(line):
            tolerated.append(line)
        elif ERROR_LINE.match(line):
            other.append(line)
        match = SUMMARY_LINE.match(line)
        if match:
            summary = {"artifacts": int(match.group(1)), "errors": int(match.group(2)), "warnings": int(match.group(3))}
    return tolerated, other, summary


def rehearse(
    repository: Path,
    *,
    predecessor_python: Path,
    successor_python: Path,
    output: Path,
    runner: Runner = run,
    workspace: Path | None = None,
    timings: bool = False,
) -> dict[str, Any]:
    repository = repository.resolve()
    output = output.resolve()
    if output.exists() and any(output.iterdir()):
        raise UpgradeRehearsalError(f"output directory is not empty: {output}")
    if repository == output or repository in output.parents:
        raise UpgradeRehearsalError("the output directory must lie outside the operational repository")
    default_temp = Path(tempfile.gettempdir()).resolve()
    selected_workspace = workspace.resolve() if workspace is not None else default_temp
    if selected_workspace == repository or repository in selected_workspace.parents:
        raise UpgradeRehearsalError("the workspace must lie outside the operational repository")
    if not selected_workspace.is_dir():
        raise UpgradeRehearsalError("the workspace must be an existing directory")
    output.mkdir(parents=True, exist_ok=True)
    timing = RehearsalTiming(output) if timings else None
    if timing:
        timing.data["storage"] = {
            "selection": "explicit" if workspace is not None else "python-default",
            "python_default_temp": str(default_temp),
            "workspace_root": str(selected_workspace),
            "operational_repository": str(repository),
            "temp_environment": {key: os.environ.get(key) for key in ("TMPDIR", "TEMP", "TMP", "RUNNER_TEMP")},
        }
    try:
        with _measure(timing, "replay") as observation:
            result = _rehearse(repository, predecessor_python, successor_python, output, runner, selected_workspace, timing)
            observation["handover_result"] = result["overall_result"]
        if timing:
            timing.data["complete"] = not timing.data["diagnostic_errors"]
    finally:
        if timing:
            stages = timing.data["stages"]
            total = stages[0].get("elapsed_seconds") if stages else None
            if total is not None:
                timing.data["unaccounted_seconds"] = total - sum(stage.get("elapsed_seconds", 0) for stage in stages[1:])
            timing.persist()
    if timing and timing.data["diagnostic_errors"] and result["overall_result"] == "pass":
        raise UpgradeRehearsalError("handover passed but timing diagnostics are incomplete")
    return result


def _rehearse(repository, predecessor_python, successor_python, output, runner, workspace, timing):
    steps: list[dict[str, Any]] = []
    failure: str | None = None

    def step(identifier: str, argv: Sequence[str], cwd: Path, *, expect: str = "success") -> Completed:
        nonlocal failure
        with _measure(timing, identifier) as observation:
            completed = runner(argv, cwd)
            observation["exit_code"] = completed.exit_code
        succeeded = completed.exit_code == 0
        outcome = "pass" if expect == "any" or succeeded == (expect == "success") else "fail"
        steps.append({
            "id": identifier,
            "argv": [str(item).replace(str(cwd), "<copy>") for item in argv],
            "expect": expect,
            "exit_code": completed.exit_code,
            "stdout_sha256": _digest(completed.stdout),
            "stderr_sha256": _digest(completed.stderr),
            "outcome": outcome,
        })
        if outcome == "fail" and failure is None:
            failure = f"{identifier}: expected {expect}, exit code {completed.exit_code}: {(completed.stderr or completed.stdout).strip()[:400]}"
        return completed

    with _scratch(workspace, timing) as scratch:
        copy = Path(scratch) / "repository"
        copy.mkdir()
        if timing:
            timing.data["storage"].update(scratch_directory=str(Path(scratch).resolve()), repository_directory=str(copy.resolve()))
            timing.persist()
        export_tracked_tree(repository, copy, runner, timing=timing)
        with _measure(timing, "predecessor-version"):
            predecessor_version = _version(predecessor_python, runner, Path(scratch))
        with _measure(timing, "successor-version"):
            successor_version = _version(successor_python, runner, Path(scratch))
        result: dict[str, Any] = {
            "schema": SCHEMA,
            "predecessor": {"version": predecessor_version},
            "successor": {"version": successor_version},
            "steps": steps,
            "lock": None,
            "tolerated_diagnostics": [],
            "semantic_sha256": None,
            "overall_result": "fail",
            "failure": None,
        }
        if predecessor_version == successor_version:
            failure = f"the predecessor and successor are the same version {successor_version}; there is no handover to rehearse"
        else:
            prior_lock = json.loads((copy / LOCK_NAME).read_text(encoding="utf-8"))
            if prior_lock.get("evaluator", {}).get("version") != predecessor_version:
                failure = f"the exported lock names evaluator {prior_lock.get('evaluator', {}).get('version')}, not the predecessor {predecessor_version}"
        if failure is None:
            step("predecessor-doctor-before", [*_evaluator(predecessor_python), "doctor", str(copy)], Path(scratch))
        if failure is None:
            step("successor-upgrade-plan", [*_evaluator(successor_python), "upgrade", str(copy)], Path(scratch))
        if failure is None:
            (copy / TRANSACTION_EVIDENCE).parent.mkdir(parents=True, exist_ok=True)
            step(
                "successor-upgrade-apply",
                [*_evaluator(successor_python), "upgrade", str(copy), "--apply", "--evidence-output", TRANSACTION_EVIDENCE],
                Path(scratch),
            )
        if failure is None:
            step("successor-doctor-after", [*_evaluator(successor_python), "doctor", str(copy)], Path(scratch))
        if failure is None:
            completed = step("successor-validate-after", [*_evaluator(successor_python), "validate", str(copy)], Path(scratch), expect="any")
            tolerated, other, summary = _validation_errors(completed.stdout)
            result["tolerated_diagnostics"] = tolerated
            result["validation"] = summary
            if summary is None:
                failure = "successor-validate-after: no validation summary was printed"
            elif other:
                failure = f"successor-validate-after: {len(other)} error(s) beyond E012 on ready records: {other[0]}"
            elif summary["errors"] != len(tolerated):
                failure = f"successor-validate-after: {summary['errors']} error(s) reported, {len(tolerated)} tolerated"
        if failure is None:
            step("predecessor-doctor-after", [*_evaluator(predecessor_python), "doctor", str(copy)], Path(scratch), expect="failure")
        if failure is None:
            raw = (copy / LOCK_NAME).read_bytes()
            lock = json.loads(raw.decode("utf-8"))
            evaluator = lock.get("evaluator") if isinstance(lock.get("evaluator"), dict) else {}
            transaction = json.loads((copy / TRANSACTION_EVIDENCE).read_text(encoding="utf-8"))
            expected_payload = transaction.get("target", {}).get("payload_sha256")
            result["lock"] = {
                "schema": lock.get("schema"),
                "tool_version": lock.get("tool_version"),
                "evaluator": {"version": evaluator.get("version"), "payload_sha256": evaluator.get("payload_sha256")},
                "canonical_sha256": canonical_sha256(raw),
            }
            if lock.get("schema") != 3:
                failure = f"the resulting lock is schema {lock.get('schema')!r}, not 3"
            elif evaluator.get("version") != successor_version or lock.get("tool_version") != successor_version:
                failure = f"the resulting lock names {evaluator.get('version')!r}/{lock.get('tool_version')!r}, not the successor {successor_version}"
            elif not isinstance(evaluator.get("payload_sha256"), str) or evaluator.get("payload_sha256") != expected_payload:
                failure = "the resulting lock does not name the successor's installed-payload digest"
            else:
                result["semantic_sha256"] = result["lock"]["canonical_sha256"]
        result["failure"] = failure
        result["overall_result"] = "pass" if failure is None else "fail"
    (output / RESULT_NAME).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rehearse the successor's real upgrade --apply against a throwaway copy of the repository.")
    parser.add_argument("--repository", default=".", help="operational repository; never written")
    parser.add_argument("--predecessor-python", required=True, help="interpreter of the environment holding the released predecessor")
    parser.add_argument("--successor-python", required=True, help="interpreter of the environment holding the successor candidate")
    parser.add_argument("--output", required=True, help="absent or empty directory outside the repository for the result")
    parser.add_argument("--workspace", type=Path, help="existing directory outside the repository for disposable copies; defaults to Python's temporary directory")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    parser.add_argument("--timings", action="store_true", help="retain separate stage timings in --output and print progress to stderr")
    args = parser.parse_args(argv)
    try:
        result = rehearse(
            Path(args.repository),
            predecessor_python=Path(args.predecessor_python),
            successor_python=Path(args.successor_python),
            output=Path(args.output),
            workspace=args.workspace,
            timings=args.timings,
        )
    except UpgradeRehearsalError as exc:
        print(f"upgrade rehearsal: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(f"upgrade rehearsal: {result['overall_result'].upper()} ({result['predecessor']['version']} -> {result['successor']['version']})")
        if result["failure"]:
            print(f"failure: {result['failure']}")
        else:
            print(f"semantic_sha256: {result['semantic_sha256']}")
    return 0 if result["overall_result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
