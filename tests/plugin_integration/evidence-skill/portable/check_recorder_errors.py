"""Exercise only recorder error retention with real local disposable processes.

These probes do not represent evaluator or model behavior. No evaluator results
are substituted: a small process prints, writes a sentinel, and optionally waits.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf8", newline="\n")


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not sys.flags.isolated:
        parser.error("Use provided Python with -I")
    here, output = Path(__file__).resolve().parent, args.output.resolve()
    if output.is_relative_to(here) or here.is_relative_to(output):
        parser.error("Use a fresh disposable output outside the source")
    output.mkdir(parents=True, exist_ok=False)
    python = str(Path(sys.executable).absolute())
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    summary = {"classification": "Recorder fault probes only; no evaluator/model/lifecycle behavior",
               "platform": platform.platform(), "python": sys.version,
               "runner_sha256": sha(Path(__file__)), "sources": {}, "cases": []}
    for name in ("run_replay.py", "run_external_replay.py", Path(__file__).name):
        source = here / name
        snapshot = output / "source" / name
        snapshot.parent.mkdir(exist_ok=True)
        snapshot.write_bytes(source.read_bytes())
        summary["sources"][name] = sha(snapshot)
    try:
        for external in (False, True):
            for fault in ("timeout", "missing-executable", "normal"):
                name = ("external-" if external else "repository-") + fault
                root = output / name
                bundle, run_output = root / "bundle", root / "run"
                bundle.mkdir(parents=True)
                target = "{external}/external-control-calibration" if external else "{repo}"
                script = (
                    "from pathlib import Path; import sys,time; "
                    "p=Path(sys.argv[-1]); p.mkdir(parents=True,exist_ok=True); "
                )
                if external:
                    script += (
                        "(p/'invocations.jsonl').write_text('{}\\n',encoding='utf8'); "
                        "(p/'effects.jsonl').write_text('{}\\n',encoding='utf8'); "
                        "(p/'remote-refs.json').write_text('{\"probe\":true}\\n',encoding='utf8'); "
                    )
                    changed = ["effects.jsonl", "invocations.jsonl", "remote-refs.json"]
                else:
                    script += "(p/'sentinel.txt').write_text('observed\\n',encoding='utf8'); "
                    changed = ["sentinel.txt"]
                script += "print('probe-stdout',flush=True); print('probe-stderr',file=sys.stderr,flush=True); "
                script += "time.sleep(30)" if fault == "timeout" else "sys.exit(0)"
                command = ["{python}", "-I", "-B", "-c", script]
                if fault == "missing-executable":
                    command = [str(root / "absent-probe-executable")]
                    changed = []
                command += (["--control-dir", target] if external else [target])
                record = {"label": "probe", "argv": command, "stdin": None,
                          "expected_exit": 0, "expected_changed_paths": changed,
                          "expected_state": None, "original_sha256": hashlib.sha256(name.encode()).hexdigest()}
                assets = {}
                if external:
                    original = {"candidate": "1" * 40, "evidence": {"fixture.txt": "2" * 64}}
                    write_json(bundle / "candidate-inputs.json", original)
                    write_json(bundle / "external-case-inputs.json", {})
                    write_json(bundle / "external-control-gate-failure/gates.json", {})
                    for item in ("allowlist.json", "gates.json", "remote-refs.json", "registry.json"):
                        write_json(bundle / "external-input-base" / item, {})
                    for item in ("invocations.jsonl", "effects.jsonl"):
                        (bundle / "external-input-base" / item).write_bytes(b"")
                    native = root / "native"
                    write_json(native / "candidate-inputs-linux.json", original)
                    (native / "release-repository").mkdir()
                    for item in bundle.rglob("*"):
                        if item.is_file():
                            assets[item.relative_to(bundle).as_posix()] = sha(item)
                    runner = here / "run_external_replay.py"
                    extra = ["--replay-root", str(native)]
                    result_file = run_output / "summary.json"
                else:
                    runner = here / "run_replay.py"
                    extra = ["--batch", "probe"]
                    result_file = run_output / "probe.json"
                write_json(bundle / "manifest.json", {"classification": summary["classification"],
                                                        "assets": assets, "records": [record]})
                argv = [python, "-I", "-B", str(runner), "--bundle", str(bundle),
                        "--output", str(run_output), "--command-timeout", "2", *extra]
                result = subprocess.run(argv, cwd=root, env=env, capture_output=True, timeout=15)
                write_json(root / "process.json", {"argv": argv, "cwd": str(root), "exit_code": result.returncode,
                                                    "stdout": result.stdout.decode("utf8", "replace"),
                                                    "stderr": result.stderr.decode("utf8", "replace")})
                trace = json.loads((run_output / "trace/probe.json").read_text(encoding="utf8"))
                batch = json.loads(result_file.read_text(encoding="utf8"))
                expected_error = {"timeout": "TimeoutExpired", "missing-executable": "FileNotFoundError"}.get(fault)
                check(trace["original_record_sha256"] == record["original_sha256"], name + ": original binding")
                check(trace["argv"] and trace["cwd"] == str(run_output), name + ": invocation retention")
                check(trace["duration_seconds"] > 0 and trace["started_unix"] > 0, name + ": timing retention")
                check(trace["changed_paths"] == changed, name + ": observed mutations")
                check(trace["before"] != trace["after"] if changed else trace["before"] == trace["after"],
                      name + ": after snapshot")
                check(batch["passed"] is (fault == "normal"), name + ": batch outcome")
                check((result.returncode == 0) is (fault == "normal"), name + ": runner exit")
                if expected_error:
                    check(trace["exit_code"] is None and trace["error"]["type"] == expected_error,
                          name + ": unknown child exit and real error")
                    check(trace["timed_out"] is (fault == "timeout"), name + ": timeout classification")
                    check(batch["failure"]["type"] == expected_error, name + ": failed batch retention")
                else:
                    check(trace["exit_code"] == 0 and "error" not in trace, name + ": normal control")
                expected_stdout = "probe-stdout" if fault != "missing-executable" else ""
                expected_stderr = "probe-stderr" if fault != "missing-executable" else ""
                check(trace["stdout"].strip() == expected_stdout, name + ": stdout retention")
                check(trace["stderr"].strip() == expected_stderr, name + ": stderr retention")
                if external:
                    expected_delta = int(fault != "missing-executable")
                    check(trace["dispatch_delta"] == expected_delta and trace["simulated_effect_delta"] == expected_delta,
                          name + ": effect deltas")
                    check(trace["local_before"] == trace["local_after"], name + ": local snapshot")
                summary["cases"].append({"case": name, "passed": True, "expected_error": expected_error,
                                          "trace": str(run_output / "trace/probe.json"),
                                          "trace_sha256": sha(run_output / "trace/probe.json")})
        summary["passed"] = True
    except Exception as error:
        summary["passed"] = False
        summary["failure"] = {"type": type(error).__name__, "message": str(error)}
        raise
    finally:
        write_json(output / "summary.json", summary)
        print(json.dumps({"passed": summary.get("passed"), "cases": len(summary["cases"]), "output": str(output)}))


if __name__ == "__main__":
    main()
