"""Test-only calibrated CPython boundary; executes unchanged trusted sources.

Not a production security sandbox. Native code/Git internals are outside Python
audit coverage. The parent supplies immutable exact argv and read roots.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--mode", choices=("helper", "evaluator", "engine", "canary"), required=True)
    parser.add_argument("--path")
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not sys.flags.isolated or not sys.dont_write_bytecode:
        parser.error("Use the verified Python with -I -B")
    config_path = Path(args.config).resolve()
    config = json.loads(config_path.read_text())
    command = args.arguments[1:] if args.arguments[:1] == ["--"] else args.arguments
    for path, expected in config["source_sha256"].items():
        if hashlib.sha256(Path(path).read_bytes()).hexdigest() != expected:
            raise ValueError("Boundary source input mismatch: " + path)
    fd = os.open(config["audit_log"], os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    role = args.mode

    def log(kind, **fields):
        row = {"kind": kind, "pid": os.getpid(), "role": role, "time_ns": time.time_ns(), **fields}
        os.write(fd, (json.dumps(row, ensure_ascii=True, default=lambda value: os.fspath(value) if isinstance(value, os.PathLike) else repr(value)) + "\n").encode())

    def deny(category, event, detail):
        log("denied", category=category, event=event, detail=detail)
        raise PermissionError("TEST_BOUNDARY_DENIED:" + category)

    roots = [Path(path).resolve() for path in config["read_roots"]]
    credential = Path(config["synthetic_credential"]).resolve()
    prefix = [config["python"], "-I", "-B", str(Path(__file__).resolve()), "--config", str(config_path)]
    evaluator_prefix = [*prefix, "--mode", "evaluator", "--"]
    process_map = {}
    for argv in config["evaluator_commands"]:
        actual = (*evaluator_prefix, *argv)
        process_map[actual] = (list(actual), "evaluator")
    for argv in config["engine_commands"]:
        original = (config["python"], "-B", *argv)
        actual = [*prefix, "--mode", "engine", "--path", argv[0], "--", *argv[1:]]
        process_map[original] = (actual, "engine")
    for argv in config["git_commands"]:
        process_map[tuple(["git", *argv])] = ([config["git"], *argv], "git-readonly")
        process_map[tuple([config["git"], *argv])] = ([config["git"], *argv], "git-readonly")
    approved_effective = {tuple(value[0]) for value in process_map.values()}
    approved_windows = {subprocess.list2cmdline(value) for value in approved_effective}
    mutation_events = {"os.remove", "os.rename", "os.mkdir", "os.rmdir", "os.chmod", "os.chown", "os.utime", "os.link", "os.symlink", "os.truncate", "shutil.copyfile", "shutil.copymode", "shutil.copystat"}

    def audit(event, values):
        if event == "open":
            name, mode, flags = values
            if isinstance(name, int):
                return
            path = Path(os.fsdecode(name)).resolve()
            if path == credential:
                deny("credential", event, str(path))
            if isinstance(mode, str) and any(c in mode for c in "wax+") or isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                # DEVNULL is used only as stdin by the unchanged helper.
                if path != Path(os.devnull).resolve():
                    deny("write", event, str(path))
            if path != Path(os.devnull).resolve() and not any(path == root or path.is_relative_to(root) for root in roots):
                deny("read-outside-fixture", event, str(path))
        elif event.startswith("socket."):
            deny("network", event, repr(values))
        elif event in mutation_events:
            deny("write", event, repr(values))
        elif event in {"os.system", "os.exec", "os.posix_spawn", "os.fork", "os.forkpty", "pty.spawn"}:
            deny("spawn", event, repr(values))
        elif event == "subprocess.Popen":
            executable, argv, cwd, environment = values
            accepted = tuple(argv) in approved_effective if isinstance(argv, (list, tuple)) else os.name == "nt" and isinstance(argv, str) and argv in approved_windows
            if not accepted:
                deny("spawn", event, repr(argv))
            log("allowed-process", argv=list(argv) if isinstance(argv, (list, tuple)) else argv, cwd=cwd)

    original_popen, original_run = subprocess.Popen, subprocess.run

    def controlled_popen(argv, *positional, **kwargs):
        if kwargs.get("shell") or kwargs.get("executable") or not isinstance(argv, (list, tuple)):
            deny("spawn", "subprocess.Popen-wrapper", repr(argv))
        selected = process_map.get(tuple(argv))
        if selected is None:
            deny("spawn", "subprocess.Popen-wrapper", list(argv))
        effective, category = selected
        log("process-binding", original_argv=list(argv), effective_argv=effective, category=category)
        return original_popen(effective, *positional, **kwargs)

    def controlled_run(*positional, **kwargs):
        argv = positional[0] if positional else kwargs.get("args")
        try:
            result = original_run(*positional, **kwargs)
        except BaseException as exc:
            log("process-error", argv=argv, exception=type(exc).__name__, message=str(exc))
            raise
        def output(value):
            return value.decode("utf8", "replace") if isinstance(value, bytes) else value
        log("process-result", argv=argv, exit_code=result.returncode, stdout=output(result.stdout), stderr=output(result.stderr))
        return result

    sys.addaudithook(audit)
    subprocess.Popen, subprocess.run = controlled_popen, controlled_run
    log("boundary-enter", argv=sys.argv, isolated=sys.flags.isolated, bytecode_disabled=sys.dont_write_bytecode)
    if role == "helper":
        if args.path not in config["helpers"]:
            deny("helper", "entry", args.path)
        sys.argv = [args.path, *command]
        runpy.run_path(args.path, run_name="__main__")
    elif role == "engine":
        if [args.path, *command] not in config["engine_commands"]:
            deny("engine", "entry", [args.path, *command])
        sys.path.insert(0, str(Path(args.path).parent))
        sys.argv = [args.path, *command]
        runpy.run_path(args.path, run_name="__main__")
    elif role == "evaluator":
        if command not in config["evaluator_commands"]:
            deny("lifecycle", "evaluator-entry", command)
        sys.argv = ["se_harness", *command]
        runpy.run_module("se_harness", run_name="__main__", alter_sys=True)
    else:
        try:
            if command == ["write"]:
                Path(config["target"], "boundary-must-not-exist").write_text("denied")
            elif command == ["network"]:
                import socket
                socket.socket()
            elif command == ["credential"]:
                credential.read_bytes()
            elif command == ["spawn"]:
                subprocess.run([config["python"], "-I", "-B", "-c", "print('unexpected worker')"])
            else:
                raise ValueError("Unknown calibration")
        except PermissionError:
            print(json.dumps({"canary": command, "denied": True}))
            raise SystemExit(73)
        raise AssertionError("Boundary canary unexpectedly succeeded")


if __name__ == "__main__":
    main()
