#!/usr/bin/env python3
"""Run the unittest suite across worker processes with one aggregated verdict.

`WO-TST-001` (`REQ-TST-001`, `SPEC-TST-001` TST-RUN, `ADR-TST-001`). Repository-
owned, standard library only. Discovery is `unittest`'s; the unit of scheduling
is the test class; classes are ordered longest-first from the timings recorded
by the previous run (`target/test-timings.json`, derived output), else by test
count; each class runs in a worker process through `unittest.TextTestRunner`;
the results are aggregated into one report in `unittest`'s form and one exit
code. `--workers 1` runs the same classes in this process, in the same order,
and equals `python -m unittest discover -s tests -p "test_*.py"` in its pass,
fail, error and skip sets. That serial command stays the canonical reference.

    python scripts/run_tests.py [--workers N] [--scale full|reduced]
"""

from __future__ import annotations

import argparse
import concurrent.futures
import io
import json
import multiprocessing
import os
import sys
import time
import traceback
import unittest
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TIMINGS = REPOSITORY_ROOT / "target" / "test-timings.json"
SCALE_VARIABLE = "SE_HARNESS_TEST_SCALE"
TIMINGS_SCHEMA = "se-harness-test-timings-v1"


@dataclass
class ClassResult:
    name: str
    tests_run: int = 0
    failures: list[tuple[str, str]] = field(default_factory=list)
    errors: list[tuple[str, str]] = field(default_factory=list)
    skipped: list[tuple[str, str]] = field(default_factory=list)
    expected_failures: int = 0
    unexpected_successes: list[str] = field(default_factory=list)
    elapsed: float = 0.0


@dataclass(frozen=True)
class Plan:
    start_dir: str
    pattern: str
    root_dir: str
    scale: str


def _collect_classes(suite: unittest.TestSuite, classes: dict[str, int], load_errors: dict[str, str]) -> None:
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            _collect_classes(item, classes, load_errors)
            continue
        if isinstance(item, unittest.loader._FailedTest):  # type: ignore[attr-defined]
            load_errors[item.id()] = str(getattr(item, "_exception", "load error"))
            continue
        name = f"{type(item).__module__}.{type(item).__qualname__}"
        classes[name] = classes.get(name, 0) + 1


def _put_repository_first(plan: Plan) -> None:
    """`python -m unittest` runs with the repository root first on sys.path; a script in scripts/ does not.

    Without this, `se_harness` can resolve to another checkout's editable install.
    """

    for entry in (plan.start_dir, plan.root_dir):
        if entry in sys.path:
            sys.path.remove(entry)
        sys.path.insert(0, entry)


def _forget_stale_test_modules(start_dir: str, pattern: str) -> None:
    """Drop cached top-level modules matching the pattern that do not live under start_dir."""

    import fnmatch

    prefix = str(Path(start_dir).resolve())
    for name, module in list(sys.modules.items()):
        location = getattr(module, "__file__", None)
        if "." in name or not isinstance(location, str) or not fnmatch.fnmatch(name + ".py", pattern):
            continue
        if not str(Path(location).resolve()).startswith(prefix):
            del sys.modules[name]


def discover_classes(plan: Plan) -> tuple[dict[str, int], dict[str, str]]:
    """Return {class name: test count} and {failed load id: message}."""

    # `tests/` is a namespace package: discovery puts the start directory on sys.path and names
    # classes `module.Class`, exactly as `python -m unittest discover -s tests` does.
    _put_repository_first(plan)
    _forget_stale_test_modules(plan.start_dir, plan.pattern)  # a stale module cache must not stand in for the files on disk
    loader = unittest.TestLoader()  # a fresh loader: the shared one remembers its first top-level directory
    suite = loader.discover(plan.start_dir, pattern=plan.pattern)
    classes: dict[str, int] = {}
    load_errors: dict[str, str] = {}
    _collect_classes(suite, classes, load_errors)
    return classes, load_errors


def load_timings(path: Path) -> dict[str, float]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(value, dict) or value.get("schema") != TIMINGS_SCHEMA:
        return {}
    classes = value.get("classes")
    return {k: float(v) for k, v in classes.items() if isinstance(v, (int, float))} if isinstance(classes, dict) else {}


def save_timings(path: Path, results: Iterable[ClassResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema": TIMINGS_SCHEMA, "classes": {r.name: round(r.elapsed, 3) for r in results}}
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def order_classes(classes: dict[str, int], timings: dict[str, float]) -> list[str]:
    return sorted(classes, key=lambda name: (-timings.get(name, 0.0), -classes[name], name))


def run_class(arguments: tuple[str, dict[str, str]]) -> dict[str, Any]:
    """Worker entry: run one test class in this process and return a serialisable result."""

    name, plan_values = arguments
    plan = Plan(**plan_values)
    previous_directory = os.getcwd()
    os.chdir(plan.root_dir)
    _put_repository_first(plan)
    _forget_stale_test_modules(plan.start_dir, plan.pattern)
    os.environ[SCALE_VARIABLE] = plan.scale
    result = ClassResult(name=name)
    started = time.perf_counter()
    try:
        suite = unittest.TestLoader().loadTestsFromName(name)
        outcome = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
        result.tests_run = outcome.testsRun
        result.failures = [(test.id(), text) for test, text in outcome.failures]
        result.errors = [(test.id(), text) for test, text in outcome.errors]
        result.skipped = [(test.id(), reason) for test, reason in outcome.skipped]
        result.expected_failures = len(outcome.expectedFailures)
        result.unexpected_successes = [test.id() for test in outcome.unexpectedSuccesses]
    except BaseException:  # a class that cannot be loaded or a runner crash is an error, never a silent drop
        result.errors = [(name, traceback.format_exc())]
    finally:
        os.chdir(previous_directory)
    result.elapsed = time.perf_counter() - started
    return asdict(result)


def _from_dict(value: dict[str, Any]) -> ClassResult:
    return ClassResult(
        name=value["name"],
        tests_run=value["tests_run"],
        failures=[tuple(item) for item in value["failures"]],
        errors=[tuple(item) for item in value["errors"]],
        skipped=[tuple(item) for item in value["skipped"]],
        expected_failures=value["expected_failures"],
        unexpected_successes=list(value["unexpected_successes"]),
        elapsed=value["elapsed"],
    )


def run(plan: Plan, *, workers: int, timings_path: Path | None, stream=None) -> tuple[int, list[ClassResult]]:
    stream = stream or sys.stdout
    classes, load_errors = discover_classes(plan)
    order = order_classes(classes, load_timings(timings_path) if timings_path else {})
    tasks = [(name, asdict(plan)) for name in order]
    started = time.perf_counter()
    results: list[ClassResult] = []
    if workers <= 1:
        for task in tasks:
            try:
                results.append(_from_dict(run_class(task)))
            except Exception as exc:  # the runner itself failed on this class: an error, never a silent drop
                results.append(ClassResult(name=task[0], errors=[(task[0], f"worker died: {exc!r}")]))
    else:
        # ProcessPoolExecutor workers are not daemonic, so a test of this runner can itself run it.
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        pending = {}
        try:
            pending = {executor.submit(run_class, task): task[0] for task in tasks}
            for future in concurrent.futures.as_completed(pending):
                name = pending[future]
                try:
                    results.append(_from_dict(future.result()))
                except Exception as exc:  # a worker that died takes its class down as an error
                    results.append(ClassResult(name=name, errors=[(name, f"worker died: {exc!r}")]))
        finally:
            executor.shutdown(wait=True)  # every worker has exited before the caller's directories are removed
    wall = time.perf_counter() - started
    for identifier, message in load_errors.items():
        results.append(ClassResult(name=identifier, errors=[(identifier, message)]))

    tests_run = sum(r.tests_run for r in results)
    failures = [item for r in results for item in r.failures]
    errors = [item for r in results for item in r.errors]
    skipped = [item for r in results for item in r.skipped]
    unexpected = [item for r in results for item in r.unexpected_successes]
    for kind, items in (("FAIL", failures), ("ERROR", errors)):
        for identifier, text in items:
            print(f"{'=' * 70}\n{kind}: {identifier}\n{'-' * 70}\n{text}", file=stream)
    print(f"{'-' * 70}\nRan {tests_run} tests in {wall:.3f}s ({len(classes)} classes, {workers} worker{'s' if workers != 1 else ''})\n", file=stream)
    details = []
    if failures:
        details.append(f"failures={len(failures)}")
    if errors:
        details.append(f"errors={len(errors)}")
    if skipped:
        details.append(f"skipped={len(skipped)}")
    if unexpected:
        details.append(f"unexpected successes={len(unexpected)}")
    verdict = "FAILED" if failures or errors or unexpected else "OK"
    print(f"{verdict}{' (' + ', '.join(details) + ')' if details else ''}", file=stream)
    if timings_path:
        save_timings(timings_path, (r for r in results if r.name in classes))
    return (1 if verdict == "FAILED" else 0), results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1), help="worker processes (1 = serial, in this process)")
    parser.add_argument("--start-dir", default="tests")
    parser.add_argument("--pattern", default="test_*.py")
    parser.add_argument("--root-dir", default=str(REPOSITORY_ROOT), help="working directory of the workers")
    parser.add_argument("--timings", default=str(DEFAULT_TIMINGS), help="timings file read for ordering and rewritten after the run; '' disables")
    parser.add_argument("--scale", choices=("full", "reduced"), default="reduced", help=f"sets {SCALE_VARIABLE} for the workers")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.workers < 1:
        print("--workers must be at least 1", file=sys.stderr)
        return 2
    root = str(Path(args.root_dir).resolve())
    start = str((Path(root) / args.start_dir).resolve()) if not Path(args.start_dir).is_absolute() else args.start_dir
    plan = Plan(start_dir=start, pattern=args.pattern, root_dir=root, scale=args.scale)
    code, _ = run(plan, workers=args.workers, timings_path=Path(args.timings) if args.timings else None)
    return code


if __name__ == "__main__":
    multiprocessing.freeze_support()
    raise SystemExit(main())
