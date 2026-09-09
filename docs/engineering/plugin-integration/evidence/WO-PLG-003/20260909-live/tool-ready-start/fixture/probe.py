"""Disposable Codex host observations. Never uses the operator's auth/profile.

This is an investigation fixture, not a production plugin or governance gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import queue
import shutil
import subprocess
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from processes import close_owned_tree, spawn, stop_owned_tree


# A distinct inline native command, not evaluation of the refused .ps1 file.
INLINE_GUARD = (
    "$ErrorActionPreference='Stop'; $raw=[Console]::In.ReadToEnd(); $event=$raw|ConvertFrom-Json; "
    "$data=$env:PLUGIN_DATA; if(!$data){throw 'PLUGIN_DATA absent'}; "
    "New-Item -ItemType Directory -Path $data -Force|Out-Null; "
    "[ordered]@{event=$event.hook_event_name; source=$event.source; cwd=$event.cwd; "
    "plugin_data=$data; plugin_root=$env:PLUGIN_ROOT; timestamp=[DateTimeOffset]::UtcNow.ToString('o')} "
    "|ConvertTo-Json -Compress|Add-Content -LiteralPath (Join-Path $data 'inline-events.jsonl'); "
    "$pointer=Join-Path $data 'runtime-path.txt'; "
    "if(Test-Path -LiteralPath $pointer){$python=(Get-Content -LiteralPath $pointer -Raw).Trim(); "
    "if(Test-Path -LiteralPath $python -PathType Leaf){ "
    "$raw|& $python -I (Join-Path $env:PLUGIN_ROOT 'observe_runtime.py'); exit $LASTEXITCODE}}; "
    "if($event.hook_event_name -eq 'SessionStart'){ "
    "Write-Output 'CODEX_PROBE_INLINE_003: Setup required. Supplied Python 3.11+ with venv/ensurepip is required. "
    "No Python was invoked. This fixture is not governance-ready; do not perform governed writes.'}; exit 0"
)


def write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8", newline="\n")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def isolated_environment(home: Path) -> dict[str, str]:
    """Allow-list OS launch inputs; do not inherit account tokens or user config."""
    keys = ("SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "NUMBER_OF_PROCESSORS",
            "PROCESSOR_ARCHITECTURE")
    env = {k: os.environ[k] for k in keys if k in os.environ}
    windows = env.get("SYSTEMROOT", r"C:\Windows")
    env.update({
        "HOME": str(home), "USERPROFILE": str(home), "CODEX_HOME": str(home / "codex"),
        "APPDATA": str(home / "AppData" / "Roaming"),
        "LOCALAPPDATA": str(home / "AppData" / "Local"),
        "TEMP": str(home / "tmp"), "TMP": str(home / "tmp"),
        "PATH": os.pathsep.join((str(Path(windows) / "System32"),
                                 str(Path(windows) / "System32/WindowsPowerShell/v1.0"))),
        "NO_COLOR": "1", "TERM": "dumb",
    })
    return env


def run(argv: list[str], cwd: Path, env: dict[str, str], timeout: int = 30, input_text: str = "") -> dict:
    start = time.monotonic()
    process = spawn(argv, cwd=cwd, env=env, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                               encoding="utf-8", errors="replace")
    try:
        stdout, stderr = process.communicate(input_text, timeout=timeout)
        close_owned_tree(process)
        return dict(argv=argv, exit_status=process.returncode, stdout=stdout,
                    stderr=stderr, duration_seconds=round(time.monotonic()-start, 3),
                    timed_out=False)
    except subprocess.TimeoutExpired as error:
        def decoded(value):
            return value.decode("utf-8", "replace") if isinstance(value, bytes) else value or ""
        cleanup = stop_owned_tree(process)
        try:
            stdout, stderr = process.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            stdout, stderr = decoded(error.stdout), decoded(error.stderr)
            cleanup["descendant_cleanup_unconfirmed"] = True
            # Reader threads may still own pipe locks. Do not block on close.
        return dict(argv=argv, exit_status=None, stdout=stdout, stderr=stderr,
                    duration_seconds=round(time.monotonic()-start, 3), timed_out=True,
                    cleanup=cleanup)


def retain(directory: Path, name: str, result: dict) -> None:
    if (directory / f"{name}.json").exists():
        raise ValueError(f"Evidence already exists: {directory / name}; use a new output directory.")
    write(directory / f"{name}.json", json.dumps(result, indent=2)+"\n")
    write(directory / f"{name}.stdout.txt", result["stdout"])
    write(directory / f"{name}.stderr.txt", result["stderr"])


def inventory(root: Path) -> dict:
    """Metadata only; never read contents of normal-profile/auth files."""
    if not root.exists():
        return {"exists": False, "files": {}}
    return {"exists": True, "files": {
        str(p.relative_to(root)): {"size": p.stat().st_size, "mtime_ns": p.stat().st_mtime_ns}
        for p in root.rglob("*") if p.is_file()
    }}


def app_server(codex: Path, sandbox: Path, evidence: Path) -> None:
    """Use only methods/fields present in this executable's generated schema."""
    if (evidence / "app-server/transcript.json").exists():
        raise ValueError("App-server evidence already exists; use a new evidence directory.")
    schema_root = sandbox / "schemas"
    schemas = [schema_root / "ClientRequest.json", schema_root / "v1/InitializeParams.json",
               *[schema_root / "v2" / n for n in ("HooksListParams.json", "HooksListResponse.json",
                 "SkillsListParams.json", "ThreadStartParams.json", "ThreadResumeParams.json",
                 "ThreadCompactStartParams.json")]]
    write(evidence / "app-server/schema-digests.json", json.dumps(
        {str(p.relative_to(schema_root)): digest(p) for p in schemas}, indent=2)+"\n")
    env = isolated_environment(sandbox / "profile")
    process = spawn([str(codex), "app-server", "--stdio"], cwd=sandbox / "repo",
                               env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    incoming: queue.Queue = queue.Queue()
    records, errors = [], []
    def read_stdout():
        for line in process.stdout:
            try:
                value = json.loads(line)
            except ValueError:
                value = {"unparsed_stdout": line}
            records.append({"received_at": time.time(), "message": value})
            incoming.put(value)
    def read_stderr():
        errors.extend(process.stderr.readlines())
    readers = [threading.Thread(target=read_stdout, daemon=True),
               threading.Thread(target=read_stderr, daemon=True)]
    for reader in readers:
        reader.start()
    sequence = 0
    def request(method, params, timeout=12):
        nonlocal sequence
        sequence += 1
        msg = {"id": sequence, "method": method, "params": params}
        records.append({"sent_at": time.time(), "message": msg})
        process.stdin.write(json.dumps(msg)+"\n")
        process.stdin.flush()
        deadline = time.monotonic()+timeout
        while time.monotonic() < deadline:
            try:
                response = incoming.get(timeout=max(.01, deadline-time.monotonic()))
            except queue.Empty:
                break
            if response.get("id") == sequence:
                return response
        return {"id": sequence, "probe_timeout": True}
    try:
        request("initialize", {"clientInfo": {"name": "codex-compatibility-probe", "version": "0.0.1"},
                               "capabilities": {"experimentalApi": True}})
        process.stdin.write('{"method":"initialized","params":{}}\n')
        process.stdin.flush()
        request("hooks/list", {"cwds": [str(sandbox / "repo")]})
        request("skills/list", {"cwds": [str(sandbox / "repo")], "forceReload": True})
        started = request("thread/start", {"cwd": str(sandbox / "repo"), "sandbox": "read-only",
                                           "approvalPolicy": "on-request"})
        thread_id = started.get("result", {}).get("thread", {}).get("id")
        if thread_id:
            # This checks the actual endpoint; same-server resume is reported as such.
            request("thread/resume", {"threadId": thread_id, "cwd": str(sandbox / "repo")})
            request("thread/compact/start", {"threadId": thread_id})
            time.sleep(2)
    finally:
        process.stdin.close()
        cleanup = None
        try:
            process.wait(timeout=5)
            cleanup = stop_owned_tree(process)
        except subprocess.TimeoutExpired:
            cleanup = stop_owned_tree(process)
        for reader in readers:
            reader.join(timeout=2)
        write(evidence / "app-server/transcript.json", json.dumps(records, indent=2)+"\n")
        write(evidence / "app-server/stderr.txt", "".join(errors))
        write(evidence / "app-server/capture.json", json.dumps({
            "exit_status": process.returncode,
            "reader_complete": [not reader.is_alive() for reader in readers], "cleanup": cleanup
        }, indent=2)+"\n")
        print(json.dumps({"app_server_exit": process.returncode, "record_count": len(records)}))


def prepare(sandbox: Path, inline: bool = False) -> tuple[Path, Path, Path, dict[str, str]]:
    if sandbox.exists():
        raise ValueError("Use a new sandbox path for each run; previous evidence is preserved.")
    home, repo, marketplace = sandbox / "profile", sandbox / "repo", sandbox / "marketplace with spaces"
    env = isolated_environment(home)
    for name in ("CODEX_HOME", "APPDATA", "LOCALAPPDATA", "TEMP"):
        Path(env[name]).mkdir(parents=True, exist_ok=True)
    repo.mkdir(parents=True)
    write(repo / "AGENTS.md", "# Disposable Codex observation repository\n\n"
          "Fixture only. Do not change any path outside this disposable sandbox.\n")
    write(repo / "governed-target.txt", "unchanged sentinel\n")
    write(Path(env["CODEX_HOME"]) / "config.toml", 'cli_auth_credentials_store = "file"\n'
          'check_for_update_on_startup = false\n')
    plugin = marketplace / "plugins" / "codex-probe"
    write(plugin / ".codex-plugin/plugin.json", json.dumps({
        "name": "codex-probe", "version": "0.0.2" if inline else "0.0.1", "description": "Disposable compatibility observation",
        "skills": "./skills/", "hooks": "./hooks/hooks.json"}, indent=2)+"\n")
    write(plugin / "skills/setup/SKILL.md", "---\nname: setup\n"
          "description: Disposable Codex probe setup marker; no production authority.\n---\n\n"
          "Report CODEX_PROBE_SKILL_003. Do not install Python. If supplied Python is missing, "
          "older than 3.11, or lacks venv/ensurepip, report that prerequisite and stop setup. "
          "The fixture is not governance-ready. Never write governed-target.txt while unready.\n")
    shutil.copy2(Path(__file__).with_name("observe.ps1"), plugin / "observe.ps1")
    shutil.copy2(Path(__file__).with_name("observe_runtime.py"), plugin / "observe_runtime.py")
    command = 'powershell.exe -NoProfile -NonInteractive -File "${PLUGIN_ROOT}/observe.ps1"'
    if inline:
        command = 'powershell.exe -NoProfile -NonInteractive -Command "'+INLINE_GUARD+'"'
    hooks = {"SessionStart": [{"matcher": "startup|resume|clear|compact",
                              "hooks": [{"type": "command", "command": command, "timeout": 10}]}],
             "PreToolUse": [{"hooks": [{"type": "command", "command": command, "timeout": 10}]}]}
    write(plugin / "hooks/hooks.json", json.dumps({"hooks": hooks}, indent=2)+"\n")
    write(marketplace / ".agents/plugins/marketplace.json", json.dumps({
        "name": "codex-probe-local", "plugins": [{"name": "codex-probe",
        "source": {"source": "local", "path": "./plugins/codex-probe"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Productivity"}]}, indent=2)+"\n")
    return home, repo, marketplace, env


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", required=True, type=Path)
    parser.add_argument("--sandbox", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--schemas-only", action="store_true")
    parser.add_argument("--network-retry", action="store_true")
    parser.add_argument("--app-server", action="store_true")
    parser.add_argument("--local-only", action="store_true")
    parser.add_argument("--inline", action="store_true")
    args = parser.parse_args()
    sandbox, evidence = args.sandbox.resolve(), args.evidence.resolve()
    checkout = Path(__file__).resolve().parents[3]
    if sandbox == checkout or checkout in sandbox.parents:
        parser.error("Disposable host profiles must remain outside the checkout.")
    if sandbox == evidence or sandbox in evidence.parents or evidence in sandbox.parents:
        parser.error("Keep disposable host state separate from retained evidence.")
    if args.app_server:
        app_server(args.codex, sandbox, evidence)
        return
    if args.network_retry:
        result = run([str(args.codex), "exec", "--json", "--skip-git-repo-check",
                      "--sandbox", "read-only", "Report CODEX_PROBE_STARTUP_003. Do not use tools or write files."],
                     sandbox / "repo", isolated_environment(sandbox / "profile"), timeout=35)
        retain(evidence / "host-attempts", "exec-startup-network-retry", result)
        print(json.dumps(result, indent=2))
        return
    if args.schemas_only:
        env = isolated_environment(sandbox / "profile")
        result = run([str(args.codex), "app-server", "generate-json-schema", "--experimental",
                      "--out", str(sandbox / "schemas")], sandbox / "repo", env)
        retain(evidence / "host-attempts", "generate-schemas", result)
        print(result["exit_status"])
        return
    home, repo, marketplace, env = prepare(sandbox, inline=args.inline)
    metadata = {"host_executable": str(args.codex), "os": platform.platform(),
                "provided_python": sys.version, "probe_python": sys.executable,
                "fixture_sha256": {p.name: digest(p) for p in Path(__file__).parent.glob("*.py")},
                "sandbox": str(sandbox), "repository_before": inventory(repo),
                "auth_mode": "isolated file store; no credentials supplied", "started_at": time.time()}
    write(evidence / "environment.json", json.dumps(metadata, indent=2)+"\n")
    commands = [
        ("version", ["--version"]),
        ("marketplace-add", ["plugin", "marketplace", "add", str(marketplace), "--json"]),
        ("plugin-add", ["plugin", "add", "codex-probe@codex-probe-local", "--json"]),
        ("plugin-list", ["plugin", "list", "--json"]),
        ("prompt-input", ["debug", "prompt-input", "Use the setup skill; report its marker only."]),
        ("exec-startup", ["exec", "--json", "--skip-git-repo-check", "--sandbox", "read-only",
                          "Report CODEX_PROBE_STARTUP_003. Do not use tools or write files."]),
    ]
    for name, argv in commands:
        if args.local_only and name == "exec-startup":
            continue
        result = run([str(args.codex), *argv], repo, env, timeout=35)
        retain(evidence / "host-attempts", name, result)
        print(json.dumps({"step": name, "exit_status": result["exit_status"],
                          "timed_out": result["timed_out"], "duration": result["duration_seconds"]}), flush=True)
    write(evidence / "repository-after.json", json.dumps(inventory(repo), indent=2)+"\n")


if __name__ == "__main__":
    main()
