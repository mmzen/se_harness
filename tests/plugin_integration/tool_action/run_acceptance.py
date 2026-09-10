"""VER-PLG-008: real released checks and independently observed fixture effects."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCRIPT = ROOT / "plugins/verity-plane/common/scripts/check-tool-action.py"
VERSION = "0.17.0"
PAYLOAD = "dd48b16b69d90a04412f458c756876ec22a687c99282075e69d0f58316c43405"
ARCHIVE = "305c7cbc79f87baa76ea3bea939b134999f9cad3bfdfa0b4c9c2fd2d9caacced"
PROBE = ROOT / "docs/engineering/plugin-integration/evidence/WO-PLG-003/20260909-live/readiness-fixture-inputs/synthetic-inputs"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def denied(stdout):
    try:
        value = json.loads(stdout)["hookSpecificOutput"]
        return (value["hookEventName"] == "PreToolUse" and value["permissionDecision"] == "deny"
                and isinstance(value["permissionDecisionReason"], str) and bool(value["permissionDecisionReason"]))
    except (ValueError, KeyError, TypeError):
        return False


def alive(pid):
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32)]
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    handle = kernel.OpenProcess(0x1000, False, pid)
    if not handle:
        return False
    try:
        code = ctypes.c_uint32()
        if not kernel.GetExitCodeProcess(handle, ctypes.byref(code)):
            raise OSError("cannot independently inspect the fixture child")
        return code.value == 259
    finally:
        kernel.CloseHandle(handle)


class Acceptance:
    def __init__(self, args):
        assert os.name == "nt", "this acceptance profile exercises owned Windows Job Objects"
        self.space, self.out = Path(args.sandbox).resolve(), Path(args.evidence).resolve()
        self.python = Path(args.evaluator).absolute()
        self.environment = self.python.parent.parent
        self.space.mkdir(parents=True, exist_ok=False)
        self.out.mkdir(parents=True, exist_ok=False)
        self.base = self.space / "baseline"
        run = subprocess.run([str(self.python), "-I", "-B", "-m", "se_harness", "init", str(self.base),
                              "--project-name", "tool-fixture", "--json"], cwd=self.space, capture_output=True)
        (self.out / "init.stdout.json").write_bytes(run.stdout)
        (self.out / "init.stderr.txt").write_bytes(run.stderr)
        assert run.returncode == 0, "released fixture initialization failed"
        for source in PROBE.rglob("*.md.txt"):
            destination = self.base / source.relative_to(PROBE).as_posix().removesuffix(".txt")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())
        wo = self.base / "docs/engineering/readiness-probe/work-orders/WO-PROBE-001.md"
        wo.write_text(wo.read_text().replace('status = "approved"', 'status = "in_progress"', 1), encoding="utf8")
        (self.base / "governed-target.txt").write_text("initial fixture target\n")
        (self.base / "outside-scope.txt").write_text("outside fixture scope\n")
        self.rows = []
        (self.out / "identities.json").write_text(json.dumps({
            "os": platform.platform(), "python": sys.version, "evaluator": VERSION,
            "payload_sha256": PAYLOAD, "archive_sha256": ARCHIVE,
            "handler_sha256": sha(SCRIPT), "session_dependency_sha256": sha(SCRIPT.with_name("session-context.py")),
            "runner_sha256": sha(Path(__file__)), "fault_invoke_sha256": sha(HERE / "fault_invoke.py"),
            "fault_worker_sha256": sha(HERE / "fault_worker.py"),
            "profile": "captured Codex/Claude protocols on Windows; no native host qualification",
            "timing": {"inner": 4, "startup_margin": 1, "cleanup_margin": 2, "output_margin": 1, "host": 10}}, indent=2))

    def prepare(self, repo):
        argv = [str(self.python), "-I", "-B", "-m", "se_harness", "evidence", str(repo),
                "--artifact", "WO-PROBE-001", "--checkpoint", "pre-action", "--json"]
        run = subprocess.run(argv, cwd=self.space, capture_output=True)
        self.actions.append({"fixture_preparation": argv, "exit_status": run.returncode})
        self.stdout.append(run.stdout)
        self.stderr.append(run.stderr)
        assert run.returncode == 0, "could not prepare existing pre-action fixture evidence"

    def event(self, repo, host="claude", path="governed-target.txt"):
        if host == "claude":
            tool, data = "Write", {"file_path": str(repo / path), "content": "fixture effect\n"}
        else:
            tool = "apply_patch"
            data = {"command": "*** Begin Patch\n*** Update File: " + path + "\n@@\n-initial fixture target\n+fixture effect\n*** End Patch"}
        return {"hook_event_name": "PreToolUse", "cwd": str(repo), "tool_name": tool,
                "tool_use_id": "fixed-captured-fixture-id", "tool_input": data}

    def invoke(self, repo, *, host="claude", path="governed-target.txt", event=None, artifact="WO-PROBE-001",
               fault=None, refusal="deny", inner=4):
        args = ["--repo", str(repo), "--environment", str(self.environment), "--version", VERSION,
                "--payload-sha256", PAYLOAD, "--archive-sha256", ARCHIVE, "--host", host,
                "--artifact", artifact, "--refusal-mode", refusal, "--inner-timeout", str(inner),
                "--startup-margin", "1", "--cleanup-margin", "2", "--output-margin", "1", "--host-timeout", "10"]
        if fault:
            argv = [str(self.python), "-I", "-B", str(HERE / "fault_invoke.py"), str(SCRIPT), fault,
                    str(repo / "fault-observation"), *args]
        else:
            argv = [str(self.python), "-I", "-B", str(SCRIPT), *args]
        event = self.event(repo, host, path) if event is None else event
        raw = event if isinstance(event, bytes) else json.dumps(event).encode()
        start = time.monotonic()
        run = subprocess.run(argv, cwd=self.space, input=raw, capture_output=True, timeout=10)
        self.actions.append({"argv": argv, "event": raw.decode("utf8", "replace"), "exit_status": run.returncode,
                             "host_started_monotonic": start, "host_received_monotonic": time.monotonic()})
        self.stdout.append(run.stdout)
        self.stderr.append(run.stderr)
        record = json.loads(run.stderr)
        self.receipt = (run.stdout, record)
        return run.stdout, record

    def effect(self, target, stdout, *, observed=True):
        # A declared fail-open protocol fixture, outside the handler's logs.
        before, count = sha(target), 0
        refusal = observed and denied(stdout)
        if not refusal:
            target.write_bytes(target.read_bytes() + b"observed fixture effect\n")
            count = 1
        result = {"before_sha256": before, "after_sha256": sha(target), "effect_count": count,
                  "refusal_received": refusal, "inspected_at_monotonic": time.monotonic(),
                  "qualification": "refusal-observed" if refusal else "unqualified-missing-required-refusal"}
        self.effects.append(result)
        return result

    def case(self, number, callback):
        folder, repo = self.out / number, self.space / number
        folder.mkdir()
        shutil.copytree(self.base, repo)
        self.actions, self.stdout, self.stderr, self.effects = [], [], [], []
        outcome = {"case": number, "conclusion": "fail"}
        try:
            self.prepare(repo)
            callback(repo)
            outcome["conclusion"] = "pass"
        except Exception as error:
            outcome["failure"] = type(error).__name__ + ": " + str(error)
        outcome.update(effects=self.effects, fixture_injection="declared by actions; no live-host result inferred")
        (folder / "actions.txt").write_text(json.dumps(self.actions, indent=2), encoding="utf8")
        (folder / "stdout.txt").write_bytes(b"\n".join(self.stdout))
        (folder / "stderr.txt").write_bytes(b"\n".join(self.stderr))
        (folder / "observations.json").write_text(json.dumps(outcome, indent=2), encoding="utf8")
        self.rows.append({key: value for key, value in outcome.items() if key not in ("effects", "fixture_injection")})
        print(json.dumps(self.rows[-1]), flush=True)

    def c01(self, repo):
        for host in ("codex", "claude"):
            stdout, record = self.invoke(repo, host=host)
            assert record["status"] == "checked", record.get("error")
            action = record["action"]
            argv = record["checks"][-1]["argv"]
            assert action["paths"] == ["governed-target.txt"] and action["checkpoint"] == "pre-action"
            assert argv[argv.index("--artifact") + 1] == "WO-PROBE-001"
            assert argv[argv.index("--procedure") + 1] == "PROC-WO-IMPLEMENT"
            result = self.effect(repo / "governed-target.txt", stdout)
            assert result["effect_count"] == 1
            assert record["checks"][-1]["finished_monotonic"] < result["inspected_at_monotonic"]

    def c02(self, repo):
        for host in ("codex", "claude"):
            stdout, record = self.invoke(repo, host=host, path="outside-scope.txt")
            assert denied(stdout) and len(record["checks"]) == 3
            result = self.effect(repo / "outside-scope.txt", stdout)
            assert result["effect_count"] == 0 and result["before_sha256"] == result["after_sha256"]

    def c03(self, repo):
        for mode in ("failed", "stalled", "interrupted"):
            stdout, record = self.invoke(repo, fault=mode)
            assert denied(stdout) and len(record["checks"]) == 3
            child = record["checks"][-1]
            cleanup = child["cleanup"]
            # Windows venv launchers add processes; every observed process must exit.
            assert cleanup["active_processes"] == 0 and cleanup["total_processes"] >= 2
            assert cleanup["exited_processes"] == cleanup["total_processes"]
            assert child["exit_status"] is not None
            assert child["cleanup_finished_monotonic"] < record["inner_deadline_monotonic"] + 2
            assert record["response_written_monotonic"] < record["host_deadline_monotonic"]
            receipt = self.actions[-1]
            assert receipt["host_received_monotonic"] < receipt["host_started_monotonic"] + 10
            assert self.effect(repo / "governed-target.txt", stdout)["effect_count"] == 0
            pids = json.loads((repo / "fault-observation/pids.json").read_text())
            assert not any(alive(pid) for pid in pids.values())
            self.actions.append({"mode": mode, "independent_processes": {str(pid): "exited" for pid in pids.values()},
                                 "partial_write_sha256": sha(repo / "fault-observation/partial-check.txt"),
                                 "partial_write_retained": True})

    def c04(self, repo):
        for event in (b"{", {"hook_event_name": "PreToolUse"},
                      {**self.event(repo), "tool_name": "Bash", "tool_input": {"command": "write target; run another command"}}):
            stdout, record = self.invoke(repo, event=event)
            assert denied(stdout) and record["coverage"] == "unavailable"
            assert self.effect(repo / "governed-target.txt", stdout)["effect_count"] == 0

    def c05(self, repo):
        event = {**self.event(repo), "tool_name": "Bash", "tool_input": {"command": "unmapped write"}}
        stdout, record = self.invoke(repo, refusal="report-only", event=event)
        assert record["status"] == "unenforced" and not record["checks"]
        assert self.effect(repo / "governed-target.txt", stdout)["effect_count"] == 1

    def c06(self, repo):
        first, baseline = self.invoke(repo)
        assert baseline["status"] == "checked"
        second, changed = self.invoke(repo, artifact="WO-PROBE-OTHER")
        assert denied(second) and len(changed["checks"]) == 3
        assert "WO-PROBE-OTHER" in changed["checks"][-1]["argv"]
        third, path = self.invoke(repo, path="outside-scope.txt")
        assert denied(third) and "outside-scope.txt" in path["checks"][-1]["argv"]
        fourth, checkpoint = self.invoke(repo, event={**self.event(repo), "checkpoint": "scope"})
        assert denied(fourth) and checkpoint["coverage"] == "unavailable"
        self.actions.append({"checkpoint_override": "Refused as unmapped; events cannot replace the required pre-action check with a weaker scope-only check."})
        for output in (second, third, fourth):
            assert self.effect(repo / "governed-target.txt", output)["effect_count"] == 0

    def c07(self, repo):
        for event in ({**self.event(repo), "tool_input": {"file_path": "../escape.txt", "content": "x"}},
                      {**self.event(repo), "tool_name": "Bash", "recursion_marker": "skip", "tool_input": {"command": "write"}},
                      {**self.event(repo), "tool_name": "write_stdin", "tool_input": {"session_id": 17, "chars": "write"}}):
            stdout, record = self.invoke(repo, event=event)
            assert denied(stdout)
            assert self.effect(repo / "governed-target.txt", stdout)["effect_count"] == 0
        # A tool which never emits an event cannot be stopped by this handler.
        escaped = self.effect(repo / "governed-target.txt", b"", observed=False)
        assert escaped["effect_count"] == 1 and "unqualified" in escaped["qualification"]

    def c08(self, repo):
        start = time.monotonic()
        try:
            subprocess.run([str(self.python), "-I", "-c", "import time; time.sleep(30)"],
                           capture_output=True, timeout=.25)
        except subprocess.TimeoutExpired:
            self.actions.append({"host_timeout_injection": "stand-in handler never responds", "timeout_seconds": .25,
                                 "elapsed_seconds": time.monotonic() - start, "refusal_observed": False})
        else:
            raise AssertionError("host timeout not observed")
        assert self.effect(repo / "governed-target.txt", b"")["effect_count"] == 1

    def c09(self, repo):
        for mode in ("missing-interpreter", "guard-removed-after-success", "invalid-output", "empty-output"):
            if mode == "missing-interpreter":
                try:
                    subprocess.run([str(self.space / "missing-python.exe")], capture_output=True)
                except FileNotFoundError:
                    raw = b""
            elif mode == "guard-removed-after-success":
                good, record = self.invoke(repo)
                assert record["status"] == "checked"
                run = subprocess.run([str(self.python), "-I", str(self.space / "removed-guard.py")], capture_output=True)
                assert run.returncode != 0
                raw = run.stdout
                self.stderr.append(run.stderr)
            else:
                code = "print('{}')" if mode == "invalid-output" else "pass"
                run = subprocess.run([str(self.python), "-I", "-c", code], capture_output=True)
                raw = run.stdout
            self.actions.append({"missing_refusal_variant": mode, "raw_output": raw.decode("utf8"), "actual_effect_inspection": True})
            assert self.effect(repo / "governed-target.txt", raw)["effect_count"] == 1

    def c10(self, repo):
        for inner in (6, 7):
            stdout, record = self.invoke(repo, inner=inner)
            assert denied(stdout) and not record["checks"]
            assert "margins" in record["error"]
            assert self.effect(repo / "governed-target.txt", stdout)["effect_count"] == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("evaluator", "sandbox", "evidence"):
        parser.add_argument("--" + name, required=True)
    tests = Acceptance(parser.parse_args())
    for number in range(1, 11):
        tests.case(f"C{number:02}", getattr(tests, f"c{number:02}"))
    (tests.out / "summary.json").write_text(json.dumps(tests.rows, indent=2))
    return int(any(row["conclusion"] != "pass" for row in tests.rows))


if __name__ == "__main__":
    raise SystemExit(main())
