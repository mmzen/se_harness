"""Run the fixed C01/C02/C03/C06/C08 helper matrix; no model decisions."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from boundary_runner import sha, snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--only-brief", action="store_true", help="Repeat only changed brief-core cases and boundary calibration")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    settings = json.loads(args.settings.read_text())
    here = Path(__file__).resolve().parent
    shutil.copytree(here, output / "driver-source", ignore=shutil.ignore_patterns("__pycache__"))
    wrong = output / "wrong-payload-repository"
    if not args.only_brief:
        shutil.copytree(settings["target"], wrong)
        before_wrong = snapshot(wrong)
        lock_path = wrong / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text())
        original_payload = lock["evaluator"]["payload_sha256"]
        lock["evaluator"]["payload_sha256"] = "0" * 64
        lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf8")
        (output / "wrong-payload-fixture-setup.json").write_text(json.dumps({
            "classification": "Direct negative helper fixture only, not skill trust selection; no source managed lock changed",
            "source": settings["target"], "target": str(wrong), "original_payload": original_payload, "injected_payload": "0" * 64,
            "before": before_wrong, "after": snapshot(wrong)}, indent=2) + "\n")
    cases = []
    for canary in ("write", "network", "credential", "spawn", "lifecycle"):
        cases.append(("C08-calibrate-" + canary, ["--canary", canary, "--expect-exit", "1" if canary == "lifecycle" else "73"]))
    cases += [
        ("C01-selected", ["--helper", "orient", "--expect-exit", "0"]),
        ("C02-preflight", ["--helper", "orient", "--preflight", "start", "--expect-exit", "0"]),
        ("C03-version", ["--helper", "orient", "--expected-version", "0.15.0", "--expect-exit", "2", "--expect-code", "AEXORI013"]),
        ("C03-root", ["--helper", "orient", "--expected-root", str(output / "wrong-evaluator-root"), "--expect-exit", "2", "--expect-code", "AEXORI022"]),
        ("C03-payload", ["--helper", "orient", "--target", str(wrong), "--expect-exit", "2", "--expect-code", "AEXORI022"]),
    ]
    for name, code in (("valid", None), ("wrong-digest", "TCM006"), ("reversed-spans", "TCM007"), ("altered-output", "TCM010")):
        argv = ["--helper", "brief", "--request-json", str(here / "fixtures" / ("brief-" + name + ".json")), "--expect-exit", "2" if code else "0"]
        if code:
            argv.extend(["--expect-code", code])
        cases.append(("C06-" + name, argv))
    if args.only_brief:
        cases = [(name, argv) for name, argv in cases if name.startswith(("C06-", "C08-"))]
    summary = {"classification": "Fixed helper/calibration matrix, not independent instruction behavior", "settings_sha256": sha(args.settings),
               "driver_source_sha256": snapshot(output / "driver-source"), "cases": [], "passed": False}
    try:
        for name, suffix in cases:
            target = output / name
            argv = [settings["python"], "-I", "-B", str(here / "boundary_runner.py"), "--settings", str(args.settings.resolve()), "--output", str(target), *suffix]
            try:
                result = subprocess.run(argv, capture_output=True, timeout=300)
            except (OSError, subprocess.TimeoutExpired) as exc:
                (output / (name + "-driver.json")).write_text(json.dumps({"argv": argv, "exit_code": None,
                    "execution_error": {"type": type(exc).__name__, "message": str(exc)},
                    "stdout": (getattr(exc, "stdout", None) or b"").decode("utf8", "replace"),
                    "stderr": (getattr(exc, "stderr", None) or b"").decode("utf8", "replace")}, indent=2) + "\n")
                raise
            (output / (name + "-driver.json")).write_text(json.dumps({"argv": argv, "exit_code": result.returncode,
                "stdout": result.stdout.decode("utf8", "replace"), "stderr": result.stderr.decode("utf8", "replace")}, indent=2) + "\n")
            observation = json.loads((target / "observations.json").read_text())
            if result.returncode != 0 or not observation["passed"]:
                raise AssertionError("Retained helper case failed: " + name)
            stdout = (target / "stdout.txt").read_text()
            if name in {"C01-selected", "C02-preflight", "C03-version", "C03-root", "C03-payload"}:
                value = json.loads(stdout)
                receipt = value["execution_receipt"]
                assert value["schema"] == "se-harness-orientation-result-v1"
                assert receipt["schema"] == "se-harness-execution-receipt-v1"
                assert receipt["effects"]["changed_paths"] == receipt["execution"]["worker_results"] == []
                operations = [r["id"] for r in receipt["execution"]["operations"]]
                if name == "C03-version":
                    assert operations == ["version"] and value["outcome"] == "blocked"
                elif name.startswith("C03"):
                    assert operations == ["version", "identity"] and value["outcome"] == "blocked"
                else:
                    assert value["outcome"] in {"completed", "degraded"}
                    assert operations == ["version", "identity", "capability-help", "doctor", "validate-json", "inspect-json", "focus-help", "focus-json"] + (["preflight"] if name == "C02-preflight" else [])
                    if name == "C01-selected":
                        assert value["preflight"] == {"status": "not_requested"}
                    else:
                        assert value["preflight"]["ready"] is True
            elif name == "C06-valid":
                value = json.loads(stdout)
                fixed = json.loads((here / "fixtures/brief-valid.json").read_text())
                assert value["outcome"] == "completed" and value["source_sha256"] == fixed["source_sha256"]
                assert value["protected_binding_count"] == len(fixed["protected_spans"])
            summary["cases"].append({"case": name, "passed": True, "exit_code": observation["exit_code"], "observations_sha256": sha(target / "observations.json")})
            print(json.dumps(summary["cases"][-1]), flush=True)
        summary["passed"] = True
    except BaseException as exc:
        summary["failure"] = {"type": type(exc).__name__, "message": str(exc)}
        raise
    finally:
        (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf8")


if __name__ == "__main__":
    main()
