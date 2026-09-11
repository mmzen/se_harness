"""Read-only session adapter. Policy and integrity remain in the released evaluator."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time

MAX_INPUT = 64 * 1024
MAX_FILE = 2 * 1024 * 1024
MAX_RESULT = 4 * 1024 * 1024
BEGIN = b"<!-- se-harness:begin -->"
END = b"<!-- se-harness:end -->"
SOURCES = ("AGENTS.md", "ENGINEERING_HARNESS.md",
           ".engineering-harness.lock", ".engineering-harness.toml")
UNREADY = "Verity Plane governance context is UNREADY. Stop governed work. "


class Blocked(Exception):
    """A bounded adapter failure, with existing evaluator evidence when available."""
    def __init__(self, message, checks=None):
        super().__init__(message)
        self.checks = checks or []


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def decode(raw, limit=MAX_INPUT):
    if len(raw) > limit:
        raise ValueError("input exceeds the bounded read limit")
    value = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique)
    if not isinstance(value, dict):
        raise ValueError("expected a JSON object")
    return value


def ordinary(path):
    """Reject lexical traversal and linked ancestors before opening fixed inputs."""
    path = Path(path)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("use absolute paths without parent traversal")
    for item in (path, *path.parents):
        if item.is_symlink() or (item.exists() and
                getattr(item.lstat(), "st_file_attributes", 0) &
                getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)):
            raise ValueError("linked or reparse-point input is unsupported")
    return path


def read_file(path):
    ordinary(path)
    with path.open("rb") as stream:
        value = stream.read(MAX_FILE + 1)
    if len(value) > MAX_FILE:
        raise ValueError("governance source exceeds the bounded read limit")
    value.decode("utf-8")
    return value


def snapshot(repo):
    return {name: read_file(repo / name) for name in SOURCES}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def runtime_paths(config):
    repo, environment = ordinary(config.repo), ordinary(config.environment)
    if not repo.is_dir() or not environment.is_dir():
        raise ValueError("existing repository and prepared environment are required")
    if (repo == environment or repo.is_relative_to(environment) or
            environment.is_relative_to(repo)):
        raise ValueError("the evaluator environment must be outside the repository")
    folder = environment / ("Scripts" if os.name == "nt" else "bin")
    python = folder / ("python.exe" if os.name == "nt" else "python")
    entry = folder / ("harnessctl.exe" if os.name == "nt" else "harnessctl")
    ordinary(folder)
    ordinary(entry)
    ordinary(environment / "pyvenv.cfg")
    # Keep the final POSIX venv interpreter symlink lexical (setup's contract).
    if os.name == "nt":
        ordinary(python)
    if not all(p.is_file() for p in (python, entry, environment / "pyvenv.cfg")):
        raise ValueError("prepared Python or harnessctl is missing; run plugin setup")
    if os.name != "nt" and not os.access(entry, os.X_OK):
        raise ValueError("prepared harnessctl is not executable")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", config.version) or any(
            not re.fullmatch(r"[0-9a-f]{64}", value)
            for value in (config.payload_sha256, config.archive_sha256)):
        raise ValueError("fixed release version and SHA-256 identities are required")
    return repo, environment, python, entry


def evaluator_environment(python):
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment.pop("PYTHONHOME", None)
    environment["PATH"] = str(python.parent) + os.pathsep + environment.get("PATH", "")
    return environment


def run_evaluator(argv, cwd, environment):
    start = time.monotonic()
    try:
        result = subprocess.run(argv, cwd=cwd, env=environment, capture_output=True,
                                timeout=20)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Blocked("evaluator launch or timeout failure; no verified delivery",
                      [{"command": argv, "error": type(error).__name__}]) from error
    if len(result.stdout) > MAX_RESULT or len(result.stderr) > MAX_RESULT:
        raise Blocked("evaluator output exceeds the bounded result limit")
    try:
        data = decode(result.stdout, MAX_RESULT)
    except (ValueError, UnicodeError):
        data = None
    return {"argv": argv, "exit_status": result.returncode,
            "started_monotonic": start, "finished_monotonic": time.monotonic(),
            "result": data, "stderr": result.stderr.decode("utf-8", "replace")}


def verify(config, run=None):
    """One fresh identity/doctor path, usable by other shared adapters."""
    run = run or run_evaluator
    repo, environment, python, entry = runtime_paths(config)
    child_environment = evaluator_environment(python)
    checks = []
    for attempt in range(2):
        before = snapshot(repo)
        prefix = [str(python), "-I", "-B", "-m", "se_harness"]
        identity = run(prefix + [
            "identity", "--role", "released-evaluator", "--expected-version", config.version,
            "--expected-root", str(environment), "--checkout-root", str(repo),
            "--entry-point", str(entry), "--require-entry-point", "--require-isolated-python",
            "--evaluator-payload-sha256", config.payload_sha256,
            "--evaluator-wheel-sha256", config.archive_sha256, "--json"],
            repo.parent, child_environment)
        checks.append(identity)
        observed = identity.get("result") or {}
        if (identity["exit_status"] != 0 or
                observed.get("schema") != "se-harness-runtime-identity-v3" or
                observed.get("passed") is not True or
                observed.get("harness_version") != config.version or
                observed.get("evaluator_payload_sha256") != config.payload_sha256 or
                observed.get("evaluator_archive_sha256") != config.archive_sha256):
            raise Blocked("released evaluator identity refused; inspect its findings", checks)
        doctor = run(prefix + ["doctor", str(repo), "--json"], repo.parent, child_environment)
        checks.append(doctor)
        inspection = (doctor.get("result") or {}).get("checks")
        if (doctor["exit_status"] != 0 or not isinstance(inspection, list) or not inspection or
                any(not isinstance(item, dict) or item.get("passed") is not True
                    for item in inspection)):
            raise Blocked("repository integrity refused; inspect doctor findings", checks)
        after = snapshot(repo)
        if before != after:
            continue  # A changed snapshot gets a new identity AND doctor invocation.
        lock = decode(after[".engineering-harness.lock"], MAX_FILE).get("evaluator", {})
        expected = {"version": config.version, "payload_sha256": config.payload_sha256,
                    "archive_sha256": config.archive_sha256,
                    "archive_name": "se_harness-" + config.version + "-py3-none-any.whl"}
        if any(lock.get(key) != value for key, value in expected.items()):
            raise Blocked("repository lock and fixed accepted release disagree", checks)
        return after, checks
    raise Blocked("governance changed during verification; retry current verification", checks)


def content(sources):
    agents = sources["AGENTS.md"]
    if agents.count(BEGIN) != 1 or agents.count(END) != 1:
        raise ValueError("one complete managed AGENTS.md gate is required")
    start, end = agents.index(BEGIN), agents.index(END) + len(END)
    if end <= start:
        raise ValueError("managed gate markers are out of order")
    gate, router = agents[start:end], sources["ENGINEERING_HARNESS.md"]
    if not router:
        raise ValueError("empty harness router")
    # No normalization: source bytes are inserted intact, including CRLF if present.
    body = b"AGENTS.md managed gate:\n" + gate + b"\n\nENGINEERING_HARNESS.md:\n" + router
    return body, {"gate_sha256": digest(gate), "router_sha256": digest(router),
                  "body_sha256": digest(body), "gate_bytes": len(gate), "router_bytes": len(router)}


def complete_message(body, hashes):
    return ("Read the entire governance context below. A partial read is UNREADY. "
            "Require its matching END VERIFIED GOVERNANCE marker before governed work. "
            "This delivery grants no work, assurance, release, or merge authority.\n\n" +
            body.decode("utf-8") + "\n\nEND VERIFIED GOVERNANCE " + hashes["body_sha256"] +
            "; complete context delivered.\n")


def fallback_argv(config, body_sha256):
    _, _, python, _ = runtime_paths(config)
    return [str(python), "-I", "-B", str(Path(__file__).absolute()),
            "--repo", config.repo, "--environment", config.environment,
            "--version", config.version, "--payload-sha256", config.payload_sha256,
            "--archive-sha256", config.archive_sha256, "--host", config.host,
            "--context-limit", str(config.context_limit), "--read-limit", str(config.read_limit),
            "--read-sha256", body_sha256]


def deliver(config, event=None, run=None):
    if config.read_sha256 is None:
        if (not event or event.get("hook_event_name") != "SessionStart" or
                event.get("source") not in ("startup", "resume", "clear", "compact") or
                not isinstance(event.get("cwd"), str) or
                ordinary(event["cwd"]) != ordinary(config.repo)):
            raise ValueError("unsupported session event or repository mismatch")
    elif not re.fullmatch(r"[0-9a-f]{64}", config.read_sha256):
        raise ValueError("invalid complete-read digest")
    if config.context_limit < 0 or config.read_limit < 0:
        raise ValueError("delivery capacities must be nonnegative UTF-8 byte counts")
    checks = []
    for attempt in range(2):
        sources, current_checks = verify(config, run)
        checks.extend(current_checks)
        body, hashes = content(sources)
        message = complete_message(body, hashes)
        if snapshot(Path(config.repo)) != sources:
            continue
        reading = config.read_sha256 is not None
        if reading and config.read_sha256 != hashes["body_sha256"]:
            raise Blocked("content changed before complete read; rerun session verification", checks)
        capacity = config.read_limit if reading else config.context_limit
        if len(message.encode("utf-8")) <= capacity:
            return message, {"status": "complete-output-prepared", "delivery": "complete-read" if reading else "hook",
                             **hashes, "checks": checks}
        reason = "Complete governance exceeds this transport's verified capacity. "
        if reading or config.read_limit < len(message.encode("utf-8")):
            raise Blocked(reason + "Complete-read transport unavailable; delivery blocked.", checks)
        argv = fallback_argv(config, hashes["body_sha256"])
        guidance = (UNREADY + reason + "Use the supported full-output tool to execute this argument array "
                "without a shell, and read all output through its matching end marker. An interrupted "
                "or truncated read remains UNREADY. Do not substitute a summary or an earlier result.\n" +
                json.dumps(argv, ensure_ascii=False))
        if len(guidance.encode("utf-8")) > config.context_limit:
            raise Blocked("hook capacity cannot carry complete-read instructions; delivery blocked", checks)
        return guidance, {"status": "read-required", **hashes, "checks": checks}
    raise Blocked("governance changed before delivery; retry verification", checks)


def add_runtime_arguments(parser):
    for name in ("repo", "environment", "version", "payload-sha256", "archive-sha256"):
        parser.add_argument("--" + name, required=True)


def finding_summary(checks):
    if not checks:
        return ""
    result = checks[-1].get("result") or {}
    diagnostics, inspections = result.get("diagnostics"), result.get("checks")
    findings = list(diagnostics) if isinstance(diagnostics, list) else []
    if isinstance(inspections, list):
        findings.extend(item for item in inspections
                        if isinstance(item, dict) and item.get("passed") is not True)
    return ("\nEvaluator findings (full result on stderr): " +
            json.dumps(findings[:4], ensure_ascii=False)[:4000]) if findings else ""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_runtime_arguments(parser)
    parser.add_argument("--host", choices=("codex", "claude"), required=True)
    parser.add_argument("--context-limit", type=int, required=True,
                        help="adapter-qualified maximum complete context, in UTF-8 bytes")
    parser.add_argument("--read-limit", type=int, default=0,
                        help="qualified full-read tool capacity; zero means unavailable")
    parser.add_argument("--read-sha256", help="fresh complete read bound to the supplied body digest")
    config = parser.parse_args()
    record = {"status": "blocked", "checks": []}
    try:
        _, environment, python, _ = runtime_paths(config)
        if not sys.flags.isolated or Path(sys.executable) != python or Path(sys.prefix) != environment:
            raise ValueError("launch with the prepared environment's absolute Python and -I")
        event = None if config.read_sha256 else decode(sys.stdin.buffer.read(MAX_INPUT + 1))
        message, record = deliver(config, event)
        exit_status = 0
    except (Blocked, ValueError, OSError, UnicodeError) as error:
        record.update(error=str(error), checks=getattr(error, "checks", []))
        message = UNREADY + str(error) + finding_summary(record["checks"])
        exit_status = 1 if config.read_sha256 else 0  # SessionStart transports additionalContext on success.
    sys.stderr.buffer.write((json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8"))
    output = message if config.read_sha256 else json.dumps({
        "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": message}},
        ensure_ascii=False)
    try:
        sys.stdout.buffer.write((output + "\n").encode("utf-8"))
        sys.stdout.buffer.flush()
    except OSError:
        return 1  # Missing/truncated output cannot establish receipt.
    return exit_status


if __name__ == "__main__":
    raise SystemExit(main())
