"""Observe released readiness on synthetic WO-PROBE-001; never decide authority."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

VERSION = "0.16.0"
ARCHIVE = "a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae"
PAYLOAD = "51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c"
MAX_INPUT = 65536
MAX_OUTPUT = 524288
MAX_CONTEXT = 262144
MAX_RECORD = 3 * 1024 * 1024
UNREADY = "CODEX_PROBE_READY_003: Setup or fixture checks required. No readiness or authority is asserted."


def parse_event(raw):
    if len(raw) > MAX_INPUT:
        raise ValueError("Hook input exceeds the observation limit")
    event = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(event, dict) or not isinstance(event.get("cwd"), str):
        raise ValueError("Hook input must identify its fixture cwd")
    if not Path(event["cwd"]).is_absolute():
        raise ValueError("Fixture cwd must be absolute")
    return event


def run_check(arguments, cwd):
    argv = [sys.executable, "-I", "-m", "se_harness", *arguments]
    start = time.monotonic()
    try:
        result = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=20)
        stdout, stderr = result.stdout, result.stderr
        exit_status, timed_out = result.returncode, False
    except subprocess.TimeoutExpired as error:
        stdout, stderr = error.stdout or b"", error.stderr or b""
        exit_status, timed_out = None, True
    truncated = len(stdout) > MAX_OUTPUT or len(stderr) > MAX_OUTPUT
    stdout = stdout[:MAX_OUTPUT].decode("utf-8", "replace")
    stderr = stderr[:MAX_OUTPUT].decode("utf-8", "replace")
    try:
        parsed = json.loads(stdout) if not truncated else None
    except ValueError:
        parsed = None
    return {"argv": argv, "exit_status": exit_status, "timed_out": timed_out,
            "output_truncated": truncated, "duration_seconds": round(time.monotonic()-start, 4),
            "stdout": stdout, "stderr": stderr, "result": parsed}


def succeeded(result):
    return (result.get("exit_status") == 0 and result.get("timed_out") is False
            and result.get("output_truncated") is False
            and isinstance(result.get("result"), dict))


def read_manifest(repo, manifest):
    if (not isinstance(manifest, list) or not manifest or len(manifest) > 64
            or any(not isinstance(name, str) for name in manifest)):
        raise ValueError("Expected a bounded nonempty released reading manifest")
    files, parts, total = [], [], 0
    for relative in manifest:
        path = (repo / relative).resolve()
        path.relative_to(repo)
        with path.open("rb") as stream:
            source = stream.read(MAX_CONTEXT + 1)
        total += len(source)
        if total > MAX_CONTEXT:
            raise ValueError("Fixture manifest exceeds the observation limit")
        text = source.decode("utf-8")
        files.append({"path": relative, "sha256": hashlib.sha256(source).hexdigest(),
                      "bytes": len(source), "text": text})
        parts.append("FILE: " + relative + "\n" + text)
    return files, "\n\n".join(parts)


def observe(event, run=run_check):
    repo = Path(event["cwd"]).resolve()
    observation = {"timestamp": time.time(), "event": event.get("hook_event_name"),
                   "source": event.get("source"), "cwd": str(repo),
                   "python": sys.executable, "prefix": sys.prefix,
                   "work_order": "WO-PROBE-001", "probe_only": True,
                   "governance_readiness": False, "production_readiness_claim": False,
                   "readiness_source": "Released preflight of synthetic inputs; no decision right exercised.",
                   "context": UNREADY, "checks": {}}
    checks = observation["checks"]
    checks["identity"] = run([
        "identity", "--role", "released-evaluator", "--expected-version", VERSION,
        "--expected-root", sys.prefix, "--checkout-root", str(repo),
        "--require-isolated-python", "--entry-point", str(Path(sys.prefix) / "Scripts/harnessctl.exe"),
        "--require-entry-point", "--evaluator-payload-sha256", PAYLOAD,
        "--evaluator-wheel-sha256", ARCHIVE, "--json"], repo.parent)
    if not succeeded(checks["identity"]) or checks["identity"]["result"].get("passed") is not True:
        return observation
    for name, arguments in (
        ("doctor", ["doctor", str(repo), "--json"]),
        ("preflight", ["preflight", str(repo), "--work-order", "WO-PROBE-001", "--phase", "start", "--json"]),
        ("check", ["check", str(repo), "--artifact", "WO-PROBE-001", "--json"]),
    ):
        checks[name] = run(arguments, repo.parent)
    if not all(succeeded(result) for result in checks.values()):
        return observation
    if checks["preflight"]["result"].get("ready") is not True:
        return observation
    try:
        files, payload = read_manifest(repo, checks["check"]["result"].get("context", {}).get("reading_manifest"))
    except (OSError, ValueError, TypeError) as error:
        observation["manifest_error"] = type(error).__name__ + ": " + str(error)[:200]
        return observation
    observation["manifest_files"] = files
    observation["manifest_payload_sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    observation["governance_readiness"] = True
    observation["context"] = (
        "CODEX_PROBE_READY_003: Released preflight ready=true for disposable synthetic WO-PROBE-001. "
        "No real approval, lifecycle transition or production authority is recorded by this observation.\n\n" + payload)
    observation["context_sha256"] = hashlib.sha256(observation["context"].encode("utf-8")).hexdigest()
    return observation


def output_context(observation):
    return observation["context"] if observation.get("event") == "SessionStart" else None


def main():
    event = parse_event(sys.stdin.buffer.read(MAX_INPUT + 1))
    observation = observe(event)
    encoded = json.dumps(observation, ensure_ascii=False).encode("utf-8")
    if len(encoded) > MAX_RECORD:
        raise ValueError("Readiness observation exceeds the record limit")
    data = Path(os.environ["PLUGIN_DATA"])
    data.mkdir(parents=True, exist_ok=True)
    with (data / "runtime-readiness-observations.jsonl").open("ab") as stream:
        stream.write(encoded + b"\n")
    context = output_context(observation)
    if context is not None:
        sys.stdout.buffer.write(context.encode("utf-8") + b"\n")


if __name__ == "__main__":
    main()
