"""C10/C11 output fault fixture for one separately owned disposable runtime.

Identity, doctor, SessionStart and all shared handlers are inactive selections.
Only the full pinned PreToolUse dispatcher argv, interpreter, prefix and cwd
select a fault before dispatch starts. No target/cache/profile file is changed.
"""
import hashlib
import json
import os
from pathlib import Path
import sys
import time

MODES = ("hang", "empty", "truncated")
CONFIG_NAME = "c10-c11-fault-config.json"
STALL_SECONDS = 90


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False).encode("utf8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def decode(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate fixture field")
            result[key] = value
        return result
    return json.loads(raw.decode("utf8"), object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError("nonfinite number")))


def selected(config, argv, executable, prefix, cwd, plugin_root, plugin_data):
    return (config.get("schema") == "verity-native-output-fault-v1" and config.get("case") in MODES and
        config.get("stall_seconds") == STALL_SECONDS and argv == config.get("selector") and
        executable == config.get("python") and prefix == config.get("runtime") and cwd == config.get("cwd") and
        plugin_root == config.get("plugin_root") and plugin_data == config.get("plugin_data"))


def configuration():
    runtime = Path(__file__).absolute().parents[2]
    path = runtime / CONFIG_NAME
    if not path.exists():
        return None
    raw = path.read_bytes()
    config = decode(raw)
    expected = {"schema", "case", "runtime", "python", "cwd", "selector", "stall_seconds",
        "source_sha256", "marker_directory", "one_edit_plan_sha256", "one_edit_plan", "plugin_root", "plugin_data"}
    if (not isinstance(config, dict) or set(config) != expected or config["runtime"] != str(runtime) or
            config["source_sha256"] != digest(Path(__file__).read_bytes()) or
            digest(encoded(config.get("one_edit_plan"))) != config.get("one_edit_plan_sha256")):
        raise ValueError("fixture runtime/source/config mismatch")
    marker = Path(config["marker_directory"])
    if marker.parent != runtime or not marker.name.startswith("markers-") or not marker.is_dir():
        raise ValueError("marker directory is not the owned runtime's fresh direct child")
    for path in (runtime, marker, path, Path(__file__)):
        for current in (path, *path.parents):
            if current.is_symlink() or (current.exists() and getattr(current.lstat(), "st_file_attributes", 0) & 0x400):
                raise ValueError("linked fixture refused")
    return config, digest(raw)


def retain(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("xb") as stream:
        stream.write(encoded(value) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.rename(path)


def self_record(config_sha):
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    values = [wintypes.FILETIME() for _ in range(4)]
    if not kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(value) for value in values)):
        raise ctypes.WinError(ctypes.get_last_error())
    created = (values[0].dwHighDateTime << 32) | values[0].dwLowDateTime
    return {"role":"pre-tool-dispatcher", "pid":os.getpid(), "ppid":os.getppid(), "creation_filetime":created,
        "argv":list(sys.orig_argv), "python":sys.executable, "prefix":sys.prefix, "cwd":os.getcwd(),
        "config_sha256":config_sha, "started_monotonic":time.monotonic(), "started_time_ns":time.time_ns()}


def output_bytes(case):
    if case == "empty":
        return b""
    if case == "truncated":
        return b'{"hookSpecificOutput":'
    raise ValueError("this mode has no completed output")


def patch_matches(config, event):
    """One complete native update, independently bounded by reviewed before/after."""
    planned = config.get("one_edit_plan") or {}
    data = event.get("tool_input")
    if not isinstance(data, dict) or set(data) != {"command"} or not isinstance(data["command"], str):
        return False
    lines = data["command"].splitlines()
    if len(lines) < 6 or lines[0] != "*** Begin Patch" or lines[-1] != "*** End Patch" or not lines[1].startswith("*** Update File: "):
        return False
    target = lines[1][len("*** Update File: "):].replace("\\", "/")
    expected = planned.get("target")
    allowed = (expected, (Path(config["cwd"]) / expected).as_posix()) if isinstance(expected, str) else ()
    if target not in allowed or lines[2] != "@@":
        return False
    before, after = planned.get("before_utf8"), planned.get("after_utf8")
    if not isinstance(before, str) or not isinstance(after, str) or before == after:
        return False
    return lines[3:-1] == ["-" + line for line in before.splitlines()] + ["+" + line for line in after.splitlines()]


def activate(config, config_sha):
    if not selected(config, list(sys.orig_argv), sys.executable, sys.prefix, os.getcwd(),
                    os.environ.get("PLUGIN_ROOT"), os.environ.get("PLUGIN_DATA")):
        return False
    markers = Path(config["marker_directory"])
    raw = sys.stdin.buffer.read(65537)
    try:
        event = decode(raw)
        if (len(raw) > 65536 or not isinstance(event, dict) or event.get("hook_event_name") != "PreToolUse" or
                event.get("tool_name") != "apply_patch" or Path(event.get("cwd", "")) != Path(config["cwd"]) or
                not patch_matches(config, event)):
            raise ValueError("selected event/patch is outside the exact supported synthetic update")
    except (ValueError, TypeError, UnicodeError) as error:
        rejected = self_record(config_sha)
        rejected.update(role="selected-dispatcher-input-rejected", fault_activated=False,
            reason=type(error).__name__ + ": " + str(error), input_hex=raw.hex(), input_sha256=digest(raw),
            input_bytes=len(raw), capture_may_be_truncated=len(raw)>65536)
        retain(markers / "rejected-input.json", rejected)
        raise
    # This is the actual selected dispatcher process, before its source executes.
    # No evaluator/handler inner deadline has started. The unchanged native guard
    # and host own the 30s outer behavior; the external observer owns final cleanup.
    record = self_record(config_sha)
    record.update(case=config["case"], stall_seconds=STALL_SECONDS,
                  dispatcher_source_executed=False, shared_handler_started=False,
                  input_sha256=digest(raw), input_bytes=len(raw), input_hex=raw.hex(), native_input=event,
                  plugin_root=os.environ.get("PLUGIN_ROOT"), plugin_data=os.environ.get("PLUGIN_DATA"))
    retain(markers / "dispatcher.json", record)
    if config["case"] == "hang":
        time.sleep(STALL_SECONDS)
        retain(markers / "natural-timeout.json", {"finished_monotonic":time.monotonic(), "slept_seconds":STALL_SECONDS})
        os._exit(96)  # Natural return does not prove the native 30s timeout acted.
    output = output_bytes(config["case"])
    sys.stdout.buffer.write(output)
    sys.stdout.buffer.flush()
    retain(markers / "output.json", {"stdout_hex":output.hex(), "stdout_sha256":digest(output),
        "exit_status":0, "finished_monotonic":time.monotonic()})
    # Exit zero prevents PowerShell's unchanged LASTEXITCODE guard from replacing
    # the observed missing/invalid bytes with a script-failure denial.
    os._exit(0)


def main():
    value = configuration()
    if value is not None:
        activate(*value)


if __name__ == "sitecustomize":
    try:
        main()
    except BaseException:
        # site.py can swallow import exceptions; a bad selected fixture must not
        # fall through into an accidental real dispatcher or evaluator run.
        os._exit(97)
