"""Capture native hook notifications during a disposable demo replay."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import queue
import subprocess
import sys
import threading
import time
import uuid

import run_demo


SOURCE_THREAD = "01a0e37f-a778-7b71-a39b-93a898d33f6f"
PROBE = """This is an instruction-delivery probe. Do not read files or call tools.
Use only the current delivered instruction context. Return only JSON:
instruction_file_path = the complete path after 'SE Harness instruction source:',
including the filename; harness_version = the version after 'Selected release:';
entry_sha256 = the 64 characters after 'entry SHA-256:', excluding the period;
final_heading = the last heading in that file without Markdown heading markers;
delivery_gap = true only when a required value was not delivered.
Return null for missing values. Do not infer values or compute a digest."""


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads(Path(__file__).with_name("prepared-demo.json").read_text())
    base = Path(manifest["demo"])
    project = Path(manifest["roots"]["codex"]["repository"])
    root_path = project / "ENGINEERING_HARNESS.md"
    root = root_path.read_text(encoding="utf-8")
    expected = manifest["roots"]["codex"]["root_sha256"]
    if hashlib.sha256(root.encode()).hexdigest() != expected:
        raise RuntimeError("Selected demo root differs from its expected digest.")
    protected = [root_path, project / ".engineering-harness.toml", project / ".engineering-harness.lock"]
    before = {str(p): digest(p) for p in protected}
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = Path(__file__).parent / "observations" / ("codex-hooks-" + stamp + "-" + uuid.uuid4().hex[:6])
    out.mkdir(parents=True)
    stream = (out / "native-events.jsonl").open("w", encoding="utf-8")
    print("Capture: " + str(out.resolve()), flush=True)
    env = run_demo.child_env(base, "codex")
    executable = manifest["host_executables"]["codex"]
    version = subprocess.check_output([executable, "--version"], cwd=project, env=env, text=True).strip()
    proc = subprocess.Popen([executable, "--enable", "hooks", "app-server", "--listen", "stdio://"],
        cwd=project, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", bufsize=1)
    inbox = queue.Queue()
    notes = []
    def read_stdout():
        for line in proc.stdout:
            try: inbox.put(json.loads(line))
            except json.JSONDecodeError: inbox.put({"capture_error": "App-server emitted invalid JSON."})
        inbox.put({"capture_error": "App-server output closed."})
    def read_stderr():
        for line in proc.stderr:
            # Retain counts, not arbitrary transport diagnostics or credentials.
            notes.append({"stderr_line_received": True})
    threading.Thread(target=read_stdout, daemon=True).start()
    threading.Thread(target=read_stderr, daemon=True).start()
    phase = "initialize"
    request_id = 0
    recorded = []
    report = {"status": "running", "source_thread": SOURCE_THREAD,
        "surface": "Codex native app-server over stdio; ephemeral fork of the CLI demo",
        "host_version": version, "platform": "Windows", "output": str(out.resolve()),
        "instruction_file_path": str(root_path), "expected_entry_sha256": expected}
    def save():
        (out / "observation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    def record(value):
        entry = {"captured_at": dt.datetime.now(dt.timezone.utc).isoformat(), "phase": phase, **value}
        recorded.append(entry)
        stream.write(json.dumps(entry, ensure_ascii=False) + "\n")
        stream.flush()
    def send(value):
        proc.stdin.write(json.dumps(value) + "\n")
        proc.stdin.flush()
    def receive(timeout):
        value = inbox.get(timeout=timeout)
        if "capture_error" in value:
            raise RuntimeError(value["capture_error"])
        method = value.get("method", "")
        if method and "id" in value:
            # Never bypass hook trust or grant an action from the capture client.
            send({"id": value["id"], "error": {"code": -32000, "message": "Demo capture does not grant approvals."}})
            raise RuntimeError("Native host requested operator input: " + method)
        params = value.get("params", {})
        if method.startswith("hook/"):
            record({"notification": value})
            run = params.get("run", {})
            print(method + " " + str(run.get("eventName")) + " " + str(run.get("status")) + " (" + phase + ")", flush=True)
        elif method in {"item/started", "item/completed"}:
            item = params.get("item", {})
            if item.get("type") == "contextCompaction":
                record({"notification": value})
                print(method + " contextCompaction (" + phase + ")", flush=True)
            elif item.get("type") == "agentMessage" and method == "item/completed":
                record({"notification": value})
        elif method in {"turn/started", "turn/completed"}:
            turn = params.get("turn", {})
            record({"notification": {"method": method, "params": {
                "threadId": params.get("threadId"),
                "turn": {k: turn.get(k) for k in ("id", "status", "error")}}}})
            print(method + " " + str(turn.get("status")) + " (" + phase + ")", flush=True)
        elif method in {"error", "warning", "configWarning"}:
            record({"notification": value})
        return value
    def rpc(method, params, timeout=90):
        nonlocal request_id
        request_id += 1
        ident = request_id
        record({"request": {"id": ident, "method": method, "params": params}})
        send({"id": ident, "method": method, "params": params})
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            value = receive(max(0.1, deadline-time.monotonic()))
            if value.get("id") == ident and "method" not in value:
                if "error" in value:
                    raise RuntimeError(method + ": " + json.dumps(value["error"]))
                return value["result"]
        raise RuntimeError("Timeout waiting for " + method)
    def wait_turn(thread_id, timeout=240):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            value = receive(max(0.1, deadline-time.monotonic()))
            params = value.get("params", {})
            if value.get("method") == "turn/completed" and params.get("threadId") == thread_id:
                if params["turn"]["status"] != "completed":
                    raise RuntimeError("Demo turn did not complete: " + json.dumps(params["turn"].get("error")))
                return
        raise RuntimeError("Timeout waiting for turn completion.")
    try:
        save()
        rpc("initialize", {"clientInfo": {"name": "se_harness_demo_capture", "title": "SE Harness demo capture", "version": "0.1.0"},
            "capabilities": {"experimentalApi": True}})
        send({"method": "initialized", "params": {}})
        phase = "fork"
        fork = rpc("thread/fork", {"threadId": SOURCE_THREAD, "ephemeral": True,
            "excludeTurns": True, "cwd": str(project), "sandbox": "read-only"})
        thread_id = fork["thread"]["id"]
        report["replay_thread"] = thread_id
        report["ephemeral"] = True
        report["model"] = fork.get("model")
        save()
        print("Ephemeral replay: " + thread_id, flush=True)
        phase = "before_compaction"
        rpc("turn/start", {"threadId": thread_id, "input": [{"type": "text", "text": PROBE}]})
        wait_turn(thread_id)
        phase = "compaction"
        rpc("thread/compact/start", {"threadId": thread_id})
        wait_turn(thread_id, timeout=300)
        phase = "after_compaction"
        rpc("turn/start", {"threadId": thread_id, "input": [{"type": "text", "text": PROBE}]})
        wait_turn(thread_id)
        hook_runs = []
        for entry in recorded:
            event = entry.get("notification", {})
            if event.get("method") != "hook/completed":
                continue
            run = event["params"]["run"]
            if run.get("eventName") != "sessionStart" or run.get("source") != "plugin":
                continue
            matching = [e["text"] for e in run.get("entries", []) if e.get("kind") == "context" and e.get("text", "").endswith(root)]
            hook_runs.append({"phase": entry["phase"], "id": run["id"],
                "eventName": run["eventName"], "source": run["source"], "sourcePath": run["sourcePath"],
                "status": run["status"], "startedAt": run["startedAt"], "completedAt": run.get("completedAt"),
                "complete_root_matches": bool(matching), "entry_sha256": expected if matching else None})
        report["hook_runs"] = hook_runs
        passing = [r for r in hook_runs if r["phase"] in {"compaction", "after_compaction"}
            and r["status"] == "completed" and r["complete_root_matches"]]
        if not passing:
            raise RuntimeError("No successful matching sessionStart callback captured after compaction request.")
        report["protected_demo_inputs_unchanged"] = all(digest(p) == before[str(p)] for p in protected)
        if not report["protected_demo_inputs_unchanged"]:
            raise RuntimeError("Protected demo inputs changed during capture.")
        report["status"] = "captured"
        report["limits"] = "Native app-server replay; earlier CLI session remains a separate observation. No formal verification acceptance or lifecycle transition."
        save()
        print(json.dumps(report, indent=2), flush=True)
        return 0
    except Exception as error:
        report["status"] = "incomplete"
        report["error"] = str(error) or type(error).__name__
        save()
        print("STOP: " + report["error"], flush=True)
        return 1
    finally:
        proc.stdin.close()
        try: proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.terminate()
            proc.wait(timeout=10)
        report["stderr_lines_received"] = len(notes)
        save()
        stream.close()


if __name__ == "__main__":
    raise SystemExit(main())
