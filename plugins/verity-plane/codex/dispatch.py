"""Codex transport and binding inputs; shared handlers own evaluator checks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).absolute().parent.parent
SHARED = ROOT / "scripts"
VERSION = "0.16.0"
HOST = "0.153.4"
PYTHON = (3, 14, 6)
ARCHIVE = "a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae"
PAYLOAD = "51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c"
TIMING = {"inner-timeout": 8, "host-timeout": 30, "startup-margin": 4,
          "cleanup-margin": 4, "output-margin": 2}
CONTEXT_LIMIT = 16000
COVERAGE = ("Only native apply_patch edits have this binding's evaluator coverage. "
            "Shell, continuing sessions, MCP and other tools are coverage gaps. "
            "Missing hooks or output prove no prevention; inspect effects before retry. "
            "Ordinary host permissions and already-authorized setup remain required/available.")


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate binding or event field")
        result[key] = value
    return result


def decode(raw):
    if len(raw) > 65536:
        raise ValueError("binding or event is too large")
    value = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique)
    if not isinstance(value, dict):
        raise ValueError("binding or event must be an object")
    return value


def ordinary(value):
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        raise ValueError("invalid absolute binding path")
    path = Path(value)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("binding paths must be absolute without traversal")
    for part in (path, *path.parents):
        if part.is_symlink() or (part.exists() and getattr(part.lstat(), "st_file_attributes", 0) & 0x400):
            raise ValueError("linked binding paths are unsupported")
    return path


def response(event_name, message):
    if event_name == "PreToolUse":
        specific = {"hookEventName": event_name, "permissionDecision": "deny",
                    "permissionDecisionReason": "UNREADY: " + message}
    else:
        specific = {"hookEventName": "SessionStart", "additionalContext": "UNREADY: " + message}
    return {"hookSpecificOutput": specific}


def arguments(binding, event, data, root=ROOT):
    if set(binding) != {"schema", "repo", "environment", "artifact", "profile", "decision", "capture"}:
        raise ValueError("missing or unknown binding fields; configure the selected fixture")
    if binding["schema"] != "verity-codex-binding-v1" or not isinstance(binding["capture"], bool):
        raise ValueError("unsupported binding schema or capture flag")
    if binding["profile"] != {"host": HOST, "os": "windows", "python": "3.14.6", "evaluator": VERSION}:
        raise ValueError("unsupported selected profile; DEC-PLG-001 has no positive route for it")
    if binding["decision"] != {"id": "DEC-PLG-001", "status": "decided", "option": "prove-supported-route"}:
        raise ValueError("no positively selected Codex route")
    repo, environment = ordinary(binding["repo"]), ordinary(binding["environment"])
    if repo == environment or repo in environment.parents or environment in repo.parents:
        raise ValueError("prepared environment must be outside the repository")
    python = environment / "Scripts/python.exe"
    ordinary(str(python))
    if not python.is_file():
        raise ValueError("setup required: selected interpreter is absent")
    if not isinstance(binding["artifact"], str) or not re.fullmatch(r"WO-[A-Z0-9]+-[0-9]+", binding["artifact"]):
        raise ValueError("select one work-order artifact")
    if event.get("cwd") != str(repo):
        # Path comparison handles the native slash spelling without widening roots.
        if not isinstance(event.get("cwd"), str) or ordinary(event["cwd"]) != repo:
            raise ValueError("event repository differs from explicit binding")
    name = event.get("hook_event_name")
    if name == "SessionStart" and event.get("source") in ("startup", "resume", "clear", "compact"):
        script = root / "scripts/session-context.py"
        extra = ["--context-limit", str(CONTEXT_LIMIT), "--read-limit", "0"]
    elif name == "PreToolUse" and event.get("tool_name") == "apply_patch":
        script = root / "scripts/check-tool-action.py"
        extra = ["--artifact", binding["artifact"], "--refusal-mode", "deny"]
        for key, value in TIMING.items():
            extra += ["--" + key, str(value)]
    else:
        raise ValueError("event has no supported handler mapping")
    ordinary(str(script))
    return [str(python), "-I", "-B", str(script), "--repo", str(repo),
            "--environment", str(environment), "--version", VERSION,
            "--payload-sha256", PAYLOAD, "--archive-sha256", ARCHIVE,
            "--host", "codex", *extra]


def validate_output(raw, event_name, exit_status):
    output = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique)
    if not isinstance(output, dict) or set(output) != {"hookSpecificOutput"}:
        raise ValueError("shared handler returned an unsupported envelope")
    specific = output["hookSpecificOutput"]
    if not isinstance(specific, dict) or exit_status or specific.get("hookEventName") != event_name:
        raise ValueError("shared handler failed or returned invalid output")
    if event_name == "SessionStart":
        valid = (set(specific) == {"hookEventName", "additionalContext"} and isinstance(specific["additionalContext"], str)
                 and bool(specific["additionalContext"].strip()))
    elif "permissionDecision" in specific:
        valid = (set(specific) == {"hookEventName", "permissionDecision", "permissionDecisionReason"} and
                 specific["permissionDecision"] == "deny" and isinstance(specific["permissionDecisionReason"], str) and
                 bool(specific["permissionDecisionReason"].strip()))
    else:
        valid = (set(specific) == {"hookEventName", "additionalContext"} and isinstance(specific.get("additionalContext"), str)
                 and bool(specific["additionalContext"].strip()))
    if not valid:
        raise ValueError("shared handler omitted its supported decision/context")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True)
    parser.add_argument("--event", required=True, choices=("SessionStart", "PreToolUse"))
    options = parser.parse_args()
    entered = time.monotonic()
    event, binding, capture, record = {}, {}, None, {"entered_monotonic": entered}
    raw = sys.stdin.buffer.read(65537)
    record["input_sha256"] = hashlib.sha256(raw).hexdigest()
    try:
        data = ordinary(options.data)
        config = ordinary(str(data / "binding.json"))
        binding = decode(config.read_bytes())
        if binding.get("capture") is True:
            capture = ordinary(str(data / "observations.jsonl"))
        event = decode(raw)
        if event.get("hook_event_name") != options.event:
            raise ValueError("event differs from the registered binding")
        if os.name != "nt" or sys.version_info[:3] != PYTHON:
            raise ValueError("unsupported operating system or Python profile")
        argv = arguments(binding, event, data)
        if not sys.flags.isolated or Path(sys.executable) != Path(argv[0]):
            raise ValueError("launch with the selected environment's absolute Python and -I")
        record.update(argv=argv, script_started_monotonic=time.monotonic())
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        environment.pop("PYTHONHOME", None)
        environment["PATH"] = str(Path(argv[0]).parent) + os.pathsep + environment.get("PATH", "")
        # The shared tool handler owns its process tree and inner deadline. The
        # host owns the outer deadline; no competing parent timeout is invented.
        result = subprocess.run(argv, input=raw, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                cwd=Path(binding["repo"]).parent, env=environment)
        record.update(script_finished_monotonic=time.monotonic(), exit_status=result.returncode,
                      stderr=result.stderr.decode("utf8", "replace"))
        output = validate_output(result.stdout, event["hook_event_name"], result.returncode)
        if event["hook_event_name"] == "SessionStart":
            output["systemMessage"] = COVERAGE
        record["status"] = "handler-output-returned"
    except (ValueError, OSError, KeyError, UnicodeError) as error:
        record.update(status="unready", error=str(error))
        output = response(options.event, str(error) + ". " + COVERAGE)
    record["response_prepared_monotonic"] = time.monotonic()
    encoded = (json.dumps(output, ensure_ascii=False) + "\n").encode("utf8")
    record["stdout"] = encoded.decode("utf8")
    # Opt-in local acceptance diagnostics, not a readiness cache or authority store.
    if capture is not None:
        try:
            with capture.open("a", encoding="utf8") as stream:
                stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError as error:
            output = response(options.event, "diagnostic capture failed: " + str(error))
            encoded = (json.dumps(output) + "\n").encode("utf8")
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()
    sys.stderr.write(json.dumps({key: value for key, value in record.items() if key != "stdout"}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
