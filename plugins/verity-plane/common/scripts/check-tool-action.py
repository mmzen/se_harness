"""Map supported file edits to released checks and synchronous host responses."""
import time
ENTERED = time.monotonic()
import argparse
import ctypes
from ctypes import wintypes
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys

_spec = importlib.util.spec_from_file_location("verity_session_context", Path(__file__).with_name("session-context.py"))
session = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(session)


class CoverageError(ValueError):
    pass


class WindowsJob:
    """Contain a suspended child before resuming it; never clean by process name."""
    def __init__(self):
        self.kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        k = self.kernel
        k.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        k.CreateJobObjectW.restype = wintypes.HANDLE
        k.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        k.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        k.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        k.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p,
                                               wintypes.DWORD, ctypes.c_void_p]
        k.CloseHandle.argtypes = [wintypes.HANDLE]
        k.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        k.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        k.Thread32First.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
        k.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
        k.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        k.OpenThread.restype = wintypes.HANDLE
        k.ResumeThread.argtypes = [wintypes.HANDLE]
        k.ResumeThread.restype = wintypes.DWORD

        class BasicLimit(ctypes.Structure):
            _fields_ = [("process_time", ctypes.c_longlong), ("job_time", ctypes.c_longlong),
                        ("flags", wintypes.DWORD), ("min_working", ctypes.c_size_t),
                        ("max_working", ctypes.c_size_t), ("active_limit", wintypes.DWORD),
                        ("affinity", ctypes.c_size_t), ("priority", wintypes.DWORD),
                        ("scheduling", wintypes.DWORD)]
        class ExtendedLimit(ctypes.Structure):
            _fields_ = [("basic", BasicLimit), ("io", ctypes.c_ulonglong * 6),
                        ("process_memory", ctypes.c_size_t), ("job_memory", ctypes.c_size_t),
                        ("peak_process", ctypes.c_size_t), ("peak_job", ctypes.c_size_t)]
        self.handle = k.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = ExtendedLimit()
        limits.basic.flags = 0x2000  # KILL_ON_JOB_CLOSE; no breakaway flags.
        if not k.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            self.close()
            raise ctypes.WinError(ctypes.get_last_error())

    def attach_and_resume(self, process):
        if not self.kernel.AssignProcessToJobObject(self.handle, wintypes.HANDLE(int(process._handle))):
            raise ctypes.WinError(ctypes.get_last_error())
        class ThreadEntry(ctypes.Structure):
            _fields_ = [("size", wintypes.DWORD), ("usage", wintypes.DWORD),
                        ("thread_id", wintypes.DWORD), ("process_id", wintypes.DWORD),
                        ("base_priority", wintypes.LONG), ("delta_priority", wintypes.LONG),
                        ("flags", wintypes.DWORD)]
        snapshot = self.kernel.CreateToolhelp32Snapshot(4, 0)
        if snapshot == wintypes.HANDLE(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            entry = ThreadEntry(size=ctypes.sizeof(ThreadEntry))
            found = self.kernel.Thread32First(snapshot, ctypes.byref(entry))
            while found:
                if entry.process_id == process.pid:
                    thread = self.kernel.OpenThread(2, False, entry.thread_id)
                    if not thread:
                        raise ctypes.WinError(ctypes.get_last_error())
                    try:
                        if self.kernel.ResumeThread(thread) == 0xFFFFFFFF:
                            raise ctypes.WinError(ctypes.get_last_error())
                    finally:
                        self.kernel.CloseHandle(thread)
                    return
                found = self.kernel.Thread32Next(snapshot, ctypes.byref(entry))
            raise OSError("suspended evaluator has no observable primary thread")
        finally:
            self.kernel.CloseHandle(snapshot)

    def accounting(self):
        class Accounting(ctypes.Structure):
            _fields_ = [("times", ctypes.c_longlong * 4), ("faults", wintypes.DWORD),
                        ("total", wintypes.DWORD), ("active", wintypes.DWORD),
                        ("terminated", wintypes.DWORD)]
        info = Accounting()
        if not self.kernel.QueryInformationJobObject(self.handle, 1, ctypes.byref(info), ctypes.sizeof(info), None):
            raise ctypes.WinError(ctypes.get_last_error())
        return {"total_processes": info.total, "active_processes": info.active,
                "exited_processes": info.total - info.active}

    def finish(self, deadline):
        before = self.accounting()
        if not self.kernel.TerminateJobObject(self.handle, 1):
            raise ctypes.WinError(ctypes.get_last_error())
        while time.monotonic() < deadline:
            after = self.accounting()
            if after["active_processes"] == 0:
                return {"before_cleanup": before, **after, "method": "owned Windows Job Object"}
            time.sleep(.005)
        raise TimeoutError("evaluator tree cleanup could not be confirmed within its margin")

    def close(self):
        if self.handle:
            self.kernel.CloseHandle(self.handle)
            self.handle = None


class Deadline:
    """One invocation budget, including collection and response reserve."""
    def __init__(self, config, entered=ENTERED):
        values = [config.inner_timeout, config.host_timeout, config.startup_margin,
                  config.cleanup_margin, config.output_margin]
        if any(not math.isfinite(value) or value <= 0 for value in values):
            raise CoverageError("timing budgets must be finite and positive")
        if sum((config.inner_timeout, config.startup_margin, config.cleanup_margin,
                config.output_margin)) >= config.host_timeout:
            raise CoverageError("inner timeout plus startup/cleanup/output margins must be below host timeout")
        self.entered = entered
        self.inner_end = entered + config.inner_timeout
        self.cleanup_end = self.inner_end + config.cleanup_margin
        self.output_end = self.cleanup_end + config.output_margin
        self.host_end = entered + config.host_timeout - config.startup_margin
        self.records = []

    def remaining(self):
        value = self.inner_end - time.monotonic()
        if value <= 0:
            raise TimeoutError("shared evaluator deadline expired")
        return value

    def run(self, argv, cwd, environment):
        self.remaining()
        if os.name != "nt":
            raise CoverageError("process-tree cleanup is qualified by these fixtures on Windows only")
        job, process = WindowsJob(), None
        record = {"argv": argv, "started_monotonic": time.monotonic(),
                  "inner_deadline_monotonic": self.inner_end, "exit_status": None,
                  "result": None, "stderr": ""}
        failure = None
        try:
            # CREATE_SUSPENDED makes containment precede any evaluator execution.
            process = subprocess.Popen(argv, cwd=cwd, env=environment, stdin=subprocess.DEVNULL,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=0x4)
            record["pid"] = process.pid
            job.attach_and_resume(process)
            record["resumed_monotonic"] = time.monotonic()
            try:
                stdout, stderr = process.communicate(timeout=self.remaining())
            except subprocess.TimeoutExpired:
                failure = "inner evaluator deadline expired"
                stdout, stderr = b"", b""
            record["cleanup_started_monotonic"] = time.monotonic()
            record["cleanup"] = job.finish(self.cleanup_end)
            stdout, stderr = process.communicate(timeout=max(.001, self.cleanup_end - time.monotonic()))
            record["exit_status"] = process.returncode
            record["cleanup_finished_monotonic"] = time.monotonic()
            if record["cleanup"]["before_cleanup"]["active_processes"] and failure is None:
                failure = "evaluator left active descendants after returning"
            if len(stdout) > session.MAX_RESULT or len(stderr) > session.MAX_RESULT:
                failure = "evaluator output exceeds the result limit"
            else:
                record["stderr"] = stderr.decode("utf-8", "replace")
                try:
                    record["result"] = session.decode(stdout, session.MAX_RESULT)
                except (ValueError, UnicodeError):
                    failure = failure or "evaluator did not return complete JSON"
            if process.returncode != 0:
                failure = failure or "evaluator failed"
        except (OSError, TimeoutError) as error:
            failure = type(error).__name__ + ": " + str(error)
            if process is not None and "cleanup" not in record:
                record["cleanup_unconfirmed"] = True
        finally:
            # The kill-on-close backstop also covers attach/resume/collection errors.
            job.close()
            if process is not None and process.poll() is None:
                try:
                    process.kill()
                    process.wait(timeout=max(.001, self.cleanup_end - time.monotonic()))
                except (OSError, subprocess.TimeoutExpired):
                    record["cleanup_unconfirmed"] = True
            record["finished_monotonic"] = time.monotonic()
            if failure:
                record["error"] = failure
            self.records.append(record)
        if failure:
            raise session.Blocked(failure + "; inspect any partial evaluator writes before retry", self.records)
        self.remaining()
        return record


def mapped_path(repo, name):
    if (not isinstance(name, str) or not name or name != name.strip() or
            any(ord(char) < 32 or ord(char) == 127 for char in name)):
        raise CoverageError("file path is missing or ambiguous")
    if os.name != "nt" and "\\" in name:
        raise CoverageError("alternate path separator is unsupported")
    raw = Path(name)
    path = raw if raw.is_absolute() else repo / raw
    session.ordinary(path)
    try:
        relative = path.relative_to(repo).as_posix()
    except ValueError as error:
        raise CoverageError("target is outside the configured repository") from error
    if not relative or ":" in relative:
        raise CoverageError("invalid target or alternate data stream")
    if path.exists() and (not path.is_file() or path.stat().st_nlink > 1):
        raise CoverageError("linked or non-file edit target is unsupported")
    return relative


def patch_paths(command):
    """Read a closed subset of native apply_patch syntax, never shell text."""
    if not isinstance(command, str):
        raise CoverageError("apply_patch requires tool_input.command")
    lines = command.splitlines()
    if not lines or lines[0] != "*** Begin Patch" or lines[-1] != "*** End Patch":
        raise CoverageError("unmapped patch envelope or shell wrapper")
    paths, mode, body = [], None, False
    for line in lines[1:-1]:
        if line.startswith(("*** Add File: ", "*** Update File: ", "*** Delete File: ")):
            if mode in ("add", "update") and not body:
                raise CoverageError("empty patch operation")
            mode = line[4:].split(" ", 1)[0].lower()
            paths.append(line.split(": ", 1)[1])
            body = mode == "delete"
        elif line.startswith("*** Move to: ") and mode == "update" and not body:
            paths.append(line[len("*** Move to: "):])
        elif mode == "add" and line.startswith("+"):
            body = True
        elif mode == "update" and (line == "@@" or line.startswith("@@ ") or
                                   line.startswith(("+", "-", " ")) or line == "*** End of File"):
            body = True
        else:
            raise CoverageError("unsupported or ambiguous patch operation")
    if not paths or not body or len(paths) > 128:
        raise CoverageError("empty or oversized patch path set")
    return paths


def map_action(config, event):
    repo = session.ordinary(config.repo)
    if (event.get("hook_event_name") != "PreToolUse" or
            not isinstance(event.get("cwd"), str) or session.ordinary(event["cwd"]) != repo):
        raise CoverageError("unsupported event or repository mismatch")
    if any(key in event for key in ("checkpoint", "procedure", "changed_paths", "skip_check")):
        raise CoverageError("event cannot override the fixed edit checkpoint or declared effects")
    data, tool = event.get("tool_input"), event.get("tool_name")
    if not isinstance(data, dict):
        raise CoverageError("tool_input must be an object")
    if config.host == "codex" and tool == "apply_patch":
        if set(data) != {"command"}:
            raise CoverageError("unsupported patch input fields")
        names = patch_paths(data.get("command"))
    elif config.host == "claude" and tool in ("Write", "Edit"):
        required = {"file_path", "content"} if tool == "Write" else {"file_path", "old_string", "new_string"}
        allowed = required | ({"replace_all"} if tool == "Edit" else set())
        if (set(data) - allowed or not required.issubset(data) or
                any(not isinstance(data[key], str) for key in required) or
                ("replace_all" in data and not isinstance(data["replace_all"], bool))):
            raise CoverageError("malformed file-edit inputs")
        names = [data["file_path"]]
    else:
        raise CoverageError("unmapped tool; shell commands, continuing sessions, MCP and other tools need separate coverage")
    paths = sorted(set(mapped_path(repo, name) for name in names))
    return {"tool": tool, "paths": paths, "checkpoint": "pre-action", "procedure": "PROC-WO-IMPLEMENT"}


def response(denied, message, refusal_capable=True):
    if not refusal_capable:
        return {"systemMessage": "UNENFORCED: " + message +
                " Inspect actual effects before retry. This route is unqualified for governed automation."}
    output = {"hookEventName": "PreToolUse"}
    if denied:
        output.update(permissionDecision="deny", permissionDecisionReason=message)
    else:
        output["additionalContext"] = message  # Never override host permissions with "allow".
    return {"hookSpecificOutput": output}


def assess(config, event, budget):
    if config.refusal_mode != "deny":
        raise CoverageError("binding cannot enforce refusal; no governance-check success is claimed")
    action = map_action(config, event)
    sources, checks = session.verify(config, budget.run)
    repo, _, python, _ = session.runtime_paths(config)
    argv = [str(python), "-I", "-B", "-m", "se_harness", "check", str(repo),
            "--artifact", config.artifact, "--checkpoint", action["checkpoint"],
            "--procedure", action["procedure"], "--changes-complete"]
    for path in action["paths"]:
        argv.extend(["--changed-path", path])
    argv.append("--json")
    result = budget.run(argv, repo.parent, session.evaluator_environment(python))
    data = result["result"] or {}
    if not checked_result(data, config.artifact):
        raise session.Blocked("current pre-action checkpoint refused; retain its corrective step", budget.records)
    if session.snapshot(repo) != sources or map_action(config, event) != action:
        raise session.Blocked("installation or paths changed during checking; retry fresh checks", budget.records)
    budget.remaining()
    return action


def checked_result(data, artifact):
    return (data.get("schema") == "se-harness-workflow-result-v2" and all(
        isinstance(data.get(section), dict) and data[section].get(key) == expected
        for section, key, expected in (("operation", "outcome", "completed"),
                                      ("compliance", "status", "pass"),
                                      ("selection", "primary", artifact))))


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise CoverageError("invalid binding configuration: " + message)


def main():
    config, budget = None, None
    record = {"status": "denied", "coverage": "unavailable", "checks": [], "entered_monotonic": ENTERED}
    try:
        parser = Parser(description=__doc__)
        session.add_runtime_arguments(parser)
        parser.add_argument("--host", choices=("codex", "claude"), required=True)
        parser.add_argument("--artifact", required=True)
        parser.add_argument("--refusal-mode", choices=("deny", "report-only"), default="deny")
        for key in ("inner-timeout", "host-timeout", "startup-margin", "cleanup-margin", "output-margin"):
            parser.add_argument("--" + key, type=float, required=True)
        config = parser.parse_args()
        budget = Deadline(config)
        _, environment, python, _ = session.runtime_paths(config)
        if not sys.flags.isolated or Path(sys.executable) != python or Path(sys.prefix) != environment:
            raise CoverageError("invoke the prepared environment's absolute Python with -I")
        if not config.artifact.startswith("WO-") or len(config.artifact) > 80:
            raise CoverageError("select one work-order artifact")
        event = session.decode(sys.stdin.buffer.read(session.MAX_INPUT + 1))
        action = assess(config, event, budget)
        record.update(status="checked", coverage="mapped", action=action)
        message = "Current evaluator checks passed for " + config.artifact + ". Host permissions and accountable decisions remain required."
    except (CoverageError, session.Blocked, ValueError, OSError, TimeoutError, UnicodeError) as error:
        record["error"] = str(error)
        message = "Governed action refused: " + str(error)
    if budget:
        record.update(checks=budget.records, inner_deadline_monotonic=budget.inner_end,
                      host_deadline_monotonic=budget.host_end, response_prepared_monotonic=time.monotonic())
        if time.monotonic() >= budget.output_end:
            record.update(status="denied", coverage="unqualified-timeout")
            message = "Response margin expired; inspect actual effects before retry. No timely enforcement claim."
    capable = config is not None and config.refusal_mode == "deny"
    if not capable:
        record.update(status="unenforced", coverage="unqualified")
    record["effect_inspection_required_on_missing_response"] = True
    result = response(record["status"] != "checked", message, capable)
    # Return the small host decision first; verbose evidence must not consume its margin.
    try:
        sys.stdout.buffer.write((json.dumps(result, ensure_ascii=False) + "\n").encode("utf-8"))
        sys.stdout.buffer.flush()
        record["response_written_monotonic"] = time.monotonic()
        sys.stderr.buffer.write((json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8"))
    except OSError:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
