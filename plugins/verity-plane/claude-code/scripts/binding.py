"""Describe a selected Claude binding; does not install or claim qualification."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

PROFILE = {"decision": "DEC-PLG-002:prove-supported-route", "host_version": "2.1.266",
           "python_version": "3.14.6", "version": "0.16.0",
           "payload_sha256": "51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c",
           "archive_sha256": "a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae"}
BUDGET = {"host_timeout": 60, "inner_timeout": 35, "startup_margin": 5,
          "cleanup_margin": 5, "output_margin": 5}
SKILLS = ("setup", "change", "evidence", "harness-orient", "harness-operator-brief")


def hooks(guard):
    result = {}
    for event in ("SessionStart", "PreToolUse"):
        command = guard
        if event == "PreToolUse":
            command = command.replace("$kind = 'SessionStart'", "$kind = 'PreToolUse'", 1)
            command = command.replace("$covered = $false", "$covered = $true", 1)
        result[event] = [{"hooks": [{"type": "command", "shell": "powershell",
                                    "command": command, "timeout": BUDGET["host_timeout"]}]}]
    return {"hooks": result}


def assess_binding(config, loaded, observed, decision):
    """Static eligibility only. Live receipt/refusal/effects are separate evidence."""
    errors = []
    expected_hooks = hooks((Path(__file__).resolve().parents[1] / 'hooks/guard.txt').read_text(encoding='utf8'))
    if loaded != expected_hooks:
        errors.append('loaded commands, matchers or registration differ from this adapter')
    if decision != "DEC-PLG-002:prove-supported-route":
        errors.append("no positive compatibility decision")
    expected = {"host": "2.1.266", "os": "Windows", "python": "3.14.6", "evaluator": "0.16.0"}
    if observed != expected:
        errors.append("unaccepted observed profile")
    if any(config.get(k) != v for k, v in {**PROFILE, **BUDGET, "context_limit": 32768, "read_limit": 0}.items()):
        errors.append("unsupported binding configuration")
    for event in ("SessionStart", "PreToolUse"):
        entries = loaded.get("hooks", {}).get(event, [])
        if len(entries) != 1 or len(entries[0].get("hooks", [])) != 1:
            errors.append("missing or ambiguous " + event + " binding")
            continue
        hook = entries[0]["hooks"][0]
        if hook.get("type") != "command" or hook.get("shell") != "powershell" or hook.get("timeout") != BUDGET["host_timeout"] or hook.get("async", False):
            errors.append("unsupported " + event + " execution mode/budget")
    return {"eligible_for_live_assessment": not errors, "qualified": False,
            "reasons": errors, "note": "Configuration eligibility does not prove host receipt or enforcement."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repo", "environment", "claude", "artifact"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    repo, environment, host = (Path(getattr(args, n)).absolute() for n in ("repo", "environment", "claude"))
    if not repo.is_dir() or not environment.is_dir() or not host.is_file():
        parser.error("select existing repository, private environment and Claude executable")
    version = subprocess.run([str(host), "--version"], capture_output=True, text=True, timeout=10)
    if version.returncode or version.stdout.strip() != "2.1.266 (Claude Code)":
        parser.error("Claude version is outside the accepted profile")
    value = {"schema": "verity-plane-claude-binding-v1", **PROFILE, **BUDGET,
             "repo": str(repo), "environment": str(environment), "host_executable": str(host),
             "host_sha256": hashlib.sha256(host.read_bytes()).hexdigest(), "artifact": args.artifact,
             "context_limit": 32768, "read_limit": 0}
    print(json.dumps(value, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
