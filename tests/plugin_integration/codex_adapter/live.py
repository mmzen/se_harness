"""Retain one real Codex conversation; no credentials or fabricated host events."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).absolute().parent))
import fixture
import processes
import sanitize_output
from fixture import ROOT, CODEX, PYTHON, PROFILE, SCHEMAS, SANDBOX, host_argv, host_environment, sha, write
from processes import spawn, stop_owned_tree
from sanitize_output import sanitize_text, sanitize_value
from observer import ObservationStopped, received, schema_methods, active_bindings, loaded_payload, package_record
import observer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--package-record", type=Path, required=True)
    parser.add_argument("--inventory-only", action="store_true")
    parser.add_argument("--resume")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    destination = args.evidence.absolute()
    allowed = ROOT / "docs/engineering/plugin-integration/evidence/WO-PLG-005"
    if allowed not in destination.parents or destination.exists():
        parser.error("use a new WO-PLG-005 evidence directory")
    schema_sha256 = schema_methods(SCHEMAS / "ClientRequest.json")
    hooks_path = ROOT / "plugins/verity-plane/codex/hooks/hooks.json"
    definitions = json.loads(hooks_path.read_text(encoding="utf8"))
    hooks_sha256 = sha(hooks_path)
    package = package_record(args.package_record)
    package_is_current = (package["payload"]["hooks/hooks.json"] == hooks_sha256 and
            package["payload"]["scripts/codex-dispatch.py"] == sha(ROOT / "plugins/verity-plane/codex/dispatch.py"))
    if not package_is_current and not args.inventory_only:
        parser.error("checked package does not contain the current adapter bytes")
    source_sha256 = {str(path.relative_to(ROOT)): sha(path) for path in
        (Path(__file__), Path(fixture.__file__), Path(processes.__file__), Path(sanitize_output.__file__), Path(observer.__file__))}
    env = host_environment()
    status = subprocess.run(host_argv("login", "status"), env=env, capture_output=True, timeout=20)
    if status.returncode:
        parser.error("the selected disposable profile needs operator sign-in; no credentials copied")
    version = subprocess.run(host_argv("--version"), env=env, capture_output=True, timeout=15)
    if version.stdout.decode().strip() != "codex-cli 0.153.4":
        parser.error("actual host does not match the positively accepted profile")
    repo = SANDBOX / "repo with spaces"
    data = PROFILE / "codex/plugins/data/verity-plane-verity-plane-codex-fixture"
    targets = [repo / name for name in ("governed-target.txt", "outside-scope.txt", "café quoted ' target.txt")]
    def snapshot():
        return {p.name: {"sha256":sha(p), "bytes":p.read_text(encoding="utf8")} for p in targets}
    destination.mkdir(parents=True)
    records, errors = [], []
    before = snapshot()
    observation_start = (data / "observations.jsonl").stat().st_size if (data / "observations.jsonl").exists() else 0
    argv = host_argv("app-server", "--stdio")
    process = None
    started = time.monotonic()
    def stdout_reader():
        for line in process.stdout:
            try:
                value = json.loads(line)
            except ValueError:
                value = {"unparsed_stdout": line}
            if str(value.get("method", "")).startswith("account/"):
                value = {"method": value["method"], "capture_omission": "account fields excluded"}
            records.append({"received_monotonic": time.monotonic(), "message": sanitize_value(value)})
    def stderr_reader():
        errors.extend(sanitize_text(line) for line in process.stderr)
    readers = [threading.Thread(target=stdout_reader, daemon=True), threading.Thread(target=stderr_reader, daemon=True)]
    sequence = 0
    def send(value):
        received(records, len(records), lambda value: False)
        records.append({"sent_monotonic":time.monotonic(), "message":value})
        process.stdin.write(json.dumps(value) + "\n")
        process.stdin.flush()
    def wait(predicate, first=0, timeout=90):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            value = received(records, first, predicate)
            if value is not None:
                return value
            if process.poll() is not None:
                break
            time.sleep(.025)
        raise ObservationStopped("observer deadline or process exit before expected response")
    def request(method, params):
        nonlocal sequence
        sequence += 1
        identifier, first = sequence, len(records)
        send({"id":sequence, "method":method, "params":params})
        result = wait(lambda value: value.get("id") == identifier and "method" not in value, first, timeout=30)
        if "error" in result or "result" not in result:
            raise ObservationStopped("host request failed", result)
        return result
    outcome = {"argv":argv, "host_version":version.stdout.decode().strip(), "host_sha256":sha(CODEX),
               "before":before, "source_sha256":source_sha256, "schema_sha256":schema_sha256,
               "ordinary_profile": "read-only/on-request; this observer cannot request edits or setup",
               "profile": str(PROFILE), "credentials_copied":False,
               "checked_package":package, "package_record_sha256":sha(args.package_record),
               "package_matches_current_adapter":package_is_current}
    process = spawn(argv, cwd=repo, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, encoding="utf8", errors="replace")
    try:
        for reader in readers:
            reader.start()
        request("initialize", {"clientInfo":{"name":"verity-codex-adapter-acceptance", "version":"0.0.1"},
                               "capabilities":{"experimentalApi":True}})
        send({"method":"initialized", "params":{}})
        outcome["hooks"] = request("hooks/list", {"cwds":[str(repo)]})
        outcome["skills"] = request("skills/list", {"cwds":[str(repo)], "forceReload":True})
        if not package_is_current:
            raise ObservationStopped("inventory-only observation: historical package differs from current adapter; no thread started")
        outcome["active_bindings"] = active_bindings(outcome["hooks"], repo,
            PROFILE / "codex/plugins/cache/verity-plane-codex-fixture/verity-plane", definitions, hooks_sha256)
        cache_roots = {Path(hook["sourcePath"]).parent.parent for hook in outcome["active_bindings"]}
        if len(cache_roots) != 1:
            raise ObservationStopped("required hooks resolve to different installed payloads")
        cache_root = cache_roots.pop()
        outcome["loaded_payload"] = {"root":str(cache_root), "sha256":loaded_payload(cache_root, package["payload"])}
        if not args.inventory_only:
            params = {"cwd":str(repo), "sandbox":"read-only", "approvalPolicy":"on-request"}
            if args.resume:
                params["threadId"] = args.resume
            else:
                params["ephemeral"] = False
            result = request("thread/resume" if args.resume else "thread/start", params)
            thread = result.get("result", {}).get("thread", {}).get("id")
            outcome["thread_id"] = thread
            if thread:
                prompt = "Reply with READY only. Do not use tools or change files."
                outcome["prompt"] = prompt
                first = len(records)
                request("turn/start", {"threadId":thread, "input":[{"type":"text", "text":prompt}]})
                outcome["turn"] = wait(lambda value:value.get("method") == "turn/completed" and value.get("params", {}).get("threadId") == thread, first, timeout=120)
                if args.compact and outcome["turn"].get("method") == "turn/completed":
                    first = len(records)
                    request("thread/compact/start", {"threadId":thread})
                    outcome["compact"] = wait(lambda value:value.get("params", {}).get("threadId") == thread and
                        (value.get("method") == "thread/compacted" or value.get("method") == "item/completed" and
                         value.get("params", {}).get("item", {}).get("type") == "contextCompaction"), first)
                    first = len(records)
                    request("turn/start", {"threadId":thread, "input":[{"type":"text","text":"Reply READY only. No tools or changes."}]})
                    outcome["restored_turn"] = wait(lambda value:value.get("method") == "turn/completed" and value.get("params", {}).get("threadId") == thread, first)
                request("thread/read", {"threadId":thread, "includeTurns":True})
    except (ObservationStopped, OSError, ValueError) as error:
        outcome["observer_stopped"] = str(error)
        outcome["stop_detail"] = getattr(error, "detail", None)
    finally:
        try:
            process.stdin.close()
        except (OSError, BrokenPipeError):
            pass
        outcome["cleanup"] = stop_owned_tree(process)
        for reader in readers:
            if reader.ident is not None:
                reader.join(timeout=3)
        outcome.update(after=snapshot(), finished_monotonic=time.monotonic(), started_monotonic=started,
                       readers_complete=all(not reader.is_alive() for reader in readers))
        if (data / "observations.jsonl").is_file():
            with (data / "observations.jsonl").open("rb") as stream:
                stream.seek(observation_start)
                (destination / "dispatch.jsonl").write_bytes(stream.read())
        write(destination / "actions.txt", {"argv":argv, "prompt":outcome.get("prompt"), "source":str(Path(__file__))})
        write(destination / "transcript.json", records)
        write(destination / "stdout.txt", [entry for entry in records if "received_monotonic" in entry])
        (destination / "stderr.txt").write_text("".join(errors), encoding="utf8")
        write(destination / "observations.json", outcome)
        print(json.dumps({"evidence":str(destination), "thread_id":outcome.get("thread_id"),
                         "turn":outcome.get("turn"), "targets_unchanged":outcome["before"]==outcome["after"]}))


if __name__ == "__main__":
    main()
