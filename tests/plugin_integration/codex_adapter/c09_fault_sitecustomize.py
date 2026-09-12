"""WO-PLG-005 C09 fault fixture; never install in an ordinary evaluator.

Copied as sitecustomize.py ONLY into the separately owned C09 runtime. Imports
for identity, doctor, dispatcher and shared scripts are deliberate no-ops. The
one exact final evaluator argv in an adjacent, reviewed plan selects the fault.
No target file is opened or changed here. This is injected runtime behavior,
not a released evaluator or a supported production environment.
"""
import hashlib
import json
import os
from pathlib import Path
import sys
import time

MODES = ("failed", "interrupted", "stalled")
STALL_SECONDS = 90
CONFIG_NAME = "c09-fault-config.json"


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


def selected(config, argv, executable, prefix, cwd):
    """Pure complete-array selector, with no substring or marker exemption."""
    return (config.get("schema") == "verity-c09-fault-v1" and config.get("case") in MODES and
            config.get("stall_seconds") == STALL_SECONDS and
            argv == config.get("selector") and executable == config.get("python") and
            prefix == config.get("runtime") and cwd == config.get("cwd"))


def creation_filetime(handle):
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    values = [wintypes.FILETIME() for _ in range(4)]
    if not kernel.GetProcessTimes(handle, *(ctypes.byref(value) for value in values)):
        raise ctypes.WinError(ctypes.get_last_error())
    return (values[0].dwHighDateTime << 32) | values[0].dwLowDateTime


def self_record(role, config_hash):
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    return {"role": role, "config_sha256": config_hash, "pid": os.getpid(), "ppid": os.getppid(),
            "creation_filetime": creation_filetime(kernel.GetCurrentProcess()),
            "argv": list(sys.orig_argv), "python": sys.executable, "prefix": sys.prefix,
            "cwd": os.getcwd(), "observed_monotonic": time.monotonic(), "observed_time_ns": time.time_ns()}


def retain(path, value):
    # Atomic, exclusive publication; no partially written marker is observable.
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("xb") as stream:
        stream.write(encoded(value) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.rename(path)  # Windows refuses an existing destination.


def configuration():
    runtime = Path(__file__).absolute().parents[2]
    path = runtime / CONFIG_NAME
    if not path.exists():
        return None
    raw = path.read_bytes()
    config = decode(raw)
    if (not isinstance(config, dict) or config.get("runtime") != str(runtime) or
            config.get("source_sha256") != digest(Path(__file__).read_bytes())):
        raise ValueError("fixture runtime/source mismatch")
    expected = {"schema", "case", "runtime", "python", "cwd", "selector", "stall_seconds",
                "source_sha256", "marker_directory", "one_edit_plan_sha256"}
    if set(config) != expected:
        raise ValueError("unknown/missing fixture configuration")
    marker = Path(config["marker_directory"])
    # The runner creates one fresh direct child of this C09 runtime for each run.
    if marker.parent != runtime or not marker.name.startswith("markers-") or not marker.is_dir():
        raise ValueError("marker directory is not owned by this C09 runtime")
    for current in (runtime, marker, path, Path(__file__)):
        if current.is_symlink() or getattr(current.lstat(), "st_file_attributes", 0) & 0x400:
            raise ValueError("linked fault fixture refused")
    return config, digest(raw)


def descendant(config, config_hash):
    expected = [config["python"], "-I", "-B", str(Path(__file__).absolute()), "--descendant", config_hash]
    if (list(sys.orig_argv) != expected or sys.executable != config["python"] or
            sys.prefix != config["runtime"] or os.getcwd() != config["cwd"]):
        raise ValueError("unexpected descendant invocation")
    retain(Path(config["marker_directory"]) / "descendant.json", self_record("descendant", config_hash))
    time.sleep(STALL_SECONDS)


def activate(config, config_hash):
    if not selected(config, list(sys.orig_argv), sys.executable, sys.prefix, os.getcwd()):
        return False
    import subprocess
    markers = Path(config["marker_directory"])
    child_argv = [config["python"], "-I", "-B", str(Path(__file__).absolute()), "--descendant", config_hash]
    # The shared handler assigned this evaluator to its Job Object while still
    # suspended. The child inherits that containment; no breakaway is requested.
    child = subprocess.Popen(child_argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, cwd=config["cwd"])
    record = self_record("evaluator", config_hash)
    record.update(child_pid=child.pid, child_creation_filetime=creation_filetime(int(child._handle)),
                  child_argv=child_argv, fault_case=config["case"], stall_seconds=STALL_SECONDS)
    deadline = time.monotonic() + 1
    while not (markers / "descendant.json").exists():
        if child.poll() is not None or time.monotonic() >= deadline:
            raise RuntimeError("fault descendant did not become observable")
        time.sleep(.005)
    record["fault_ready_monotonic"] = time.monotonic()
    retain(markers / "evaluator.json", record)
    if config["case"] == "failed":
        os._exit(3)
    # Interrupted waits for the external observer's verified handle termination.
    # Stalled is killed only by the unchanged handler's inner deadline.
    time.sleep(STALL_SECONDS)
    os._exit(4)  # Natural completion is NOT a successful fault observation.


def main():
    value = configuration()
    if value is None:
        return
    config, config_hash = value
    if __name__ == "__main__":
        descendant(config, config_hash)
    else:
        activate(config, config_hash)


if __name__ in ("sitecustomize", "__main__"):
    try:
        main()
    except BaseException:
        # site.py can swallow import exceptions. Never fall through into a real
        # evaluator after a selected fixture/configuration failure.
        os._exit(97)
