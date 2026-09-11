"""Record one requested helper/calibration call; make no activation decisions."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root):
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob("*")) if p.is_file()}


def environment(settings):
    value = {key: os.environ[key] for key in ("SYSTEMROOT", "WINDIR", "SYSTEMDRIVE", "COMSPEC", "PATHEXT", "LANG", "LC_ALL") if key in os.environ}
    value.update({"PATH": os.pathsep.join((str(Path(settings["python"]).parent), str(Path(settings["git"]).parent))),
                  "HOME": settings["home"], "USERPROFILE": settings["home"], "TMP": settings["home"], "TEMP": settings["home"], "TMPDIR": settings["home"],
                  "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_COUNT": "2", "GIT_OPTIONAL_LOCKS": "0",
                  "GIT_CONFIG_KEY_0": "core.longpaths", "GIT_CONFIG_VALUE_0": "true", "GIT_CONFIG_KEY_1": "core.autocrlf", "GIT_CONFIG_VALUE_1": "false",
                  "GIT_ATTR_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0", "PYTHONDONTWRITEBYTECODE": "1"})
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--helper", choices=("orient", "brief"))
    parser.add_argument("--operation", choices=("version", "identity", "doctor"))
    parser.add_argument("--request-json", type=Path)
    parser.add_argument("--preflight", choices=("start",))
    parser.add_argument("--expected-version", default="0.16.0")
    parser.add_argument("--expected-root")
    parser.add_argument("--target", type=Path)
    parser.add_argument("--canary", choices=("write", "network", "credential", "spawn", "lifecycle"))
    parser.add_argument("--expect-exit", type=int, required=True)
    parser.add_argument("--expect-code")
    args = parser.parse_args()
    settings = json.loads(args.settings.read_text())
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    target = args.target.resolve() if args.target else Path(settings["target"])
    config = {**settings, "target": str(target), "audit_log": str(output / "audit.jsonl")}
    worker = Path(__file__).with_name("audit_worker.py").resolve()
    helper_paths = list(settings["helpers"].values())
    source_paths = [worker, Path(__file__).resolve(), args.settings.resolve()]
    for helper in helper_paths:
        source_paths.extend(p for p in Path(helper).parents[1].rglob("*") if p.is_file())
    if args.request_json:
        source_paths.append(args.request_json.resolve())
    source_hashes = {str(p): sha(p) for p in source_paths}
    for path, expected in settings["product_sha256"].items():
        if sha(Path(path)) != expected:
            raise ValueError("Frozen product source changed: " + path)
    config["source_sha256"] = source_hashes
    config["helpers"] = helper_paths
    config["read_roots"] = [*settings["read_roots"], str(target), str(output), str(Path(__file__).parent.resolve()), *helper_paths]
    config["read_roots"].extend(str(Path(p).parents[1]) for p in helper_paths)
    if args.request_json:
        config["read_roots"].append(str(args.request_json.resolve()))
    expected_root = args.expected_root or settings["environment"]
    lock = json.loads((target / ".engineering-harness.lock").read_text())
    identity = ["identity", "--role", "released-evaluator", "--expected-version", args.expected_version, "--expected-root", expected_root,
                "--checkout-root", str(target), "--require-isolated-python", "--evaluator-payload-sha256", lock["evaluator"]["payload_sha256"],
                "--evaluator-wheel-sha256", lock["evaluator"]["archive_sha256"]]
    config["evaluator_commands"] = [["--version"], identity, ["--help"], ["doctor", str(target)], ["validate", str(target), "--json"],
                                    ["inspect", str(target), "--json"], ["check", "--help"],
                                    ["check", str(target), "--artifact", "WO-ROF-001", "--json", "--result-schema", "2"],
                                    ["preflight", str(target), "--work-order", "WO-ROF-001", "--phase", "start", "--json"]]
    engine = Path(settings["engine"])
    config["engine_commands"] = [[str(engine / name), "--root", str(target), "--json"] for name in ("validate_engineering_artifacts.py", "inspect_engineering_artifacts.py")]
    git_args = [["rev-parse", "HEAD"], ["rev-parse", "--show-object-format"], ["remote", "get-url", "origin"], ["ls-files", "-z"],
                ["check-attr", "-z", "--stdin", "text", "eol"], ["status", "--porcelain", "--untracked-files=all"]]
    config["git_commands"] = [["-C", str(target), *argv] for argv in git_args]
    config_path = output / "boundary-config.json"
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf8")
    versions = output / "executed-source"
    versions.mkdir()
    for index, p in enumerate(source_paths):
        shutil.copyfile(p, versions / (str(index) + "-" + p.name))
    (versions / "source-map.json").write_text(json.dumps({str(index) + "-" + p.name: {"source": str(p), "sha256": sha(p)} for index, p in enumerate(source_paths)}, indent=2) + "\n")
    prefix = [settings["python"], "-I", "-B", str(worker), "--config", str(config_path)]
    if args.canary:
        argv = [*prefix, "--mode", "canary", "--", args.canary] if args.canary != "lifecycle" else [*prefix, "--mode", "evaluator", "--", "transition", str(target), "--apply"]
    elif args.operation:
        selected = {"version": ["--version"], "identity": identity, "doctor": ["doctor", str(target)]}[args.operation]
        argv = [*prefix, "--mode", "evaluator", "--", *selected]
    elif args.helper == "orient":
        launcher = [*prefix, "--mode", "evaluator", "--"]
        argv = [*prefix, "--mode", "helper", "--path", settings["helpers"]["orient"], "--", str(target),
                "--evaluator-launcher-json", json.dumps(launcher), "--expected-evaluator-version", args.expected_version,
                "--expected-evaluator-root", expected_root, "--artifact", "WO-ROF-001"]
        if args.preflight:
            argv.extend(["--preflight-phase", args.preflight])
    elif args.helper == "brief" and args.request_json:
        argv = [*prefix, "--mode", "helper", "--path", settings["helpers"]["brief"], "--", "--request-json", str(args.request_json.resolve())]
    else:
        parser.error("Select a helper/request or one calibration canary")
    before, started = snapshot(target), time.time()
    stdout = stderr = b""
    status = None
    error = None
    try:
        completed = subprocess.run(argv, cwd=output, env=environment(settings), capture_output=True, timeout=240)
        stdout, stderr, status = completed.stdout, completed.stderr, completed.returncode
    except (subprocess.TimeoutExpired, OSError) as exc:
        error = {"type": type(exc).__name__, "message": str(exc)}
        stdout, stderr = getattr(exc, "stdout", None) or b"", getattr(exc, "stderr", None) or b""
    after = snapshot(target)
    (output / "stdout.txt").write_bytes(stdout)
    (output / "stderr.txt").write_bytes(stderr)
    (output / "actions.txt").write_text(json.dumps(argv) + "\n", encoding="utf8")
    events = [json.loads(line) for line in (output / "audit.jsonl").read_text().splitlines()] if (output / "audit.jsonl").exists() else []
    denied = [row for row in events if row["kind"] == "denied"]
    try:
        result = json.loads(stdout)
    except ValueError:
        result = None
    codes = [result.get("code")] if isinstance(result, dict) else []
    if isinstance(result, dict) and "execution_receipt" in result:
        codes.extend(row.get("code") for row in result["execution_receipt"]["validation"]["deviations"])
    passed = status == args.expect_exit and before == after and error is None
    if args.expect_code:
        passed = passed and args.expect_code in codes
    passed = passed and (len(denied) == 1 and denied[0]["category"] == args.canary if args.canary else not denied)
    observation = {"classification": "One actual instrumented helper call or explicit calibration; no model activation/rendering decision", "argv": argv,
                   "started_unix": started, "duration_seconds": time.time() - started, "exit_code": status, "execution_error": error,
                   "expected_exit": args.expect_exit, "expected_code": args.expect_code, "observed_codes": codes, "before": before, "after": after,
                   "changed_paths": [p for p in sorted(before.keys() | after.keys()) if before.get(p) != after.get(p)], "denied_events": denied,
                   "boundary_entries": [row["role"] for row in events if row["kind"] == "boundary-enter"], "passed": bool(passed), "source_sha256": source_hashes}
    (output / "observations.json").write_text(json.dumps(observation, indent=2) + "\n", encoding="utf8")
    print(json.dumps({"output": str(output), "passed": bool(passed), "exit_code": status, "codes": codes, "denied": len(denied)}), flush=True)
    if stdout:
        sys.stdout.buffer.write(stdout)
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
