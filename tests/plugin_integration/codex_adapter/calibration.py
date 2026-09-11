"""Retain local registered-shell C04/C07 checks without a native/API session."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).absolute().parent))
from fixture import ROOT, SANDBOX, PYTHON, binding, sha, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("C04", "C07"))
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    if not args.run.replace("-", "").isalnum():
        parser.error("use a simple fresh run name")
    evidence = ROOT / "docs/engineering/plugin-integration/evidence/WO-PLG-005" / args.case / args.run
    folder = SANDBOX / "registered shell calibration" / args.case / args.run
    if evidence.exists() or folder.exists():
        parser.error("fresh evidence and calibration paths required")
    folder.mkdir(parents=True)
    evidence.mkdir(parents=True)
    repo, plugin, data = folder / "repo with spaces", folder / "plugin with spaces", folder / "data with spaces"
    for path in (repo, plugin / "scripts", data):
        path.mkdir(parents=True)
    sentinel = folder / "helper-spawn.jsonl"
    sentinel_script = plugin / "scripts/codex-dispatch.py"
    sentinel_script.write_text(
        "import json,os,sys,time\nfrom pathlib import Path\n"
        "event=json.load(sys.stdin)\n"
        f"with Path({str(sentinel)!r}).open('a',encoding='utf8') as stream:\n"
        " stream.write(json.dumps({'pid':os.getpid(),'executable':sys.executable,'argv':sys.argv,'monotonic':time.monotonic()})+'\\n')\n"
        "print(json.dumps({'hookSpecificOutput':{'hookEventName':event['hook_event_name'],'additionalContext':'SENTINEL CALIBRATION ONLY; no production readiness result'}}))\n",
        encoding="utf8")
    selected = binding(repo, capture=False)
    definitions = json.loads((ROOT / "plugins/verity-plane/codex/hooks/hooks.json").read_text(encoding="utf8"))
    shell = str(Path(os.environ["SYSTEMROOT"]) / "System32/WindowsPowerShell/v1.0/powershell.exe")
    environment = os.environ.copy()
    environment.update(PLUGIN_DATA=str(data), PLUGIN_ROOT=str(plugin))
    original = {"hook_event_name":"PreToolUse", "cwd":str(repo), "tool_name":"apply_patch",
                "tool_input":{"command":"*** Begin Patch\n*** End Patch"}}
    sources = {"hooks/hooks.json": sha(ROOT / "plugins/verity-plane/codex/hooks/hooks.json"),
               "calibration.py":sha(Path(__file__)), "sentinel-dispatch.py":sha(sentinel_script),
               "selected-python":sha(PYTHON), "native-shell":sha(Path(shell))}
    formal_paths = sorted((ROOT / "docs/engineering/plugin-integration").glob("*/*.md"))
    def formal_snapshot():
        return {str(path.relative_to(ROOT)):sha(path) for path in formal_paths}
    before_states = formal_snapshot()
    runs = []
    def invoke(label, event, choice=selected, *, positive=False):
        raw = event if isinstance(event, bytes) else json.dumps(event, ensure_ascii=False).encode()
        kind = event.get("hook_event_name", "PreToolUse") if isinstance(event, dict) else "PreToolUse"
        command = definitions["hooks"][kind][0]["hooks"][0]["command"]
        argv = [shell, "-NoProfile", "-NonInteractive", "-Command", command]
        write(data / "binding.json", choice)
        log_before = sentinel.read_bytes() if sentinel.exists() else b""
        started = time.monotonic()
        result = subprocess.run(argv, input=raw, capture_output=True, env=environment, cwd=folder, timeout=15)
        finished = time.monotonic()
        log_after = sentinel.read_bytes() if sentinel.exists() else b""
        output = json.loads(result.stdout)
        specific = output.get("hookSpecificOutput", {})
        expected = "sentinel invoked" if positive else "deny/unready with unchanged helper-spawn log"
        correct = (result.returncode == 0 and (log_after != log_before if positive else
            log_after == log_before and specific.get("hookEventName") == kind and
            (specific.get("permissionDecision") == "deny" if kind == "PreToolUse" else
             "UNREADY" in specific.get("additionalContext", ""))))
        path = evidence / label
        path.mkdir()
        (path / "event.json.txt").write_bytes(raw)
        (path / "stdout.txt").write_bytes(result.stdout)
        (path / "stderr.txt").write_bytes(result.stderr)
        write(path / "actions.txt", {"argv":argv, "cwd":str(folder), "binding":choice,
            "plugin_root":str(plugin), "plugin_data":str(data), "input_path":"event.json.txt"})
        record = {"label":label, "expected":expected, "exit_status":result.returncode,
            "host_response_channel":"registered PowerShell command stdout; no model/app-server invoked",
            "response":output, "helper_spawn_log_before":log_before.decode(), "helper_spawn_log_after":log_after.decode(),
            "started_monotonic":started, "finished_monotonic":finished,
            "conclusion":"pass" if correct else "fail"}
        write(path / "observations.json", record)
        runs.append(record)
    invoke("positive-sentinel-before", original, positive=True)
    if args.case == "C04":
        missing = {key:value for key,value in original.items() if key != "cwd"}
        invoke("missing-required-cwd", missing)
        invoke("malformed-json", b"{")
        invoke("wrong-event-shape", b"[]")
        for label, tool in (("blank-tool", " "), ("object-tool", {}), ("array-tool", ["apply_patch"])):
            invoke(label, {**original, "tool_name":tool})
    else:
        variants = (("unaccepted-host", "profile", "host", "0.153.5"),
                    ("empty-host", "profile", "host", ""),
                    ("open-decision", "decision", "status", "open"),
                    ("excluded-route", "decision", "option", "exclude-codex"),
                    ("empty-positive-route", "decision", "option", ""))
        for label, section, field, value in variants:
            choice = copy.deepcopy(selected)
            choice[section][field] = value
            for kind in ("PreToolUse", "SessionStart"):
                event = {**original, "hook_event_name":kind, "source":"startup"}
                invoke(label + "-" + kind, event, choice)
    invoke("positive-sentinel-after", original, positive=True)
    after_states = formal_snapshot()
    (evidence / "helper-spawn.jsonl").write_bytes(sentinel.read_bytes())
    write(evidence / "state-before.json", before_states)
    write(evidence / "state-after.json", after_states)
    write(evidence / "actions.txt", {"argv":[str(PYTHON), "-I", "-B", str(Path(__file__)), args.case, "--run",args.run],
        "source_sha256":sources, "fixture":str(folder), "actions":[row["label"] for row in runs]})
    (evidence / "stdout.txt").write_text("".join(row["label"] + ": " + row["conclusion"] + "\n" for row in runs), encoding="utf8")
    (evidence / "stderr.txt").write_text("", encoding="utf8")
    write(evidence / "observations.json", {"case":args.case, "expected":"All negative inputs refuse before sentinel Python; positive controls prove the spawn audit is active.",
        "source_evidence":["actions.txt", "helper-spawn.jsonl", "state-before.json", "state-after.json", "per-input directories"],
        "observed":runs, "lifecycle_artifact_hashes_unchanged":before_states == after_states,
        "exit_status":0, "conclusion":"pass" if before_states == after_states and all(row["conclusion"] == "pass" for row in runs) else "fail",
        "limits":"Direct execution of the exact registered native shell commands with a sentinel dispatcher. No live model, native pending edit, actual production readiness, or broader supported profile is claimed."})
    print(json.dumps({"case":args.case,"evidence":str(evidence),"results":[row["conclusion"] for row in runs]}))


if __name__ == "__main__":
    main()
