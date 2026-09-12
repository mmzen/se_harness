"""C09 disposable fault setup/observation, defaulting to a pure plan preview.

Both --execute actions require the hash of their complete current preview. The
ordinary one-edit observer runs unchanged in its own process. No native hook,
plugin package/cache, ordinary profile setting, or shared evaluator is edited.
Only one selected binding is temporarily pointed at this distinct fault runtime.
Native observations and injected faults never grant work or qualification.
"""
import argparse
import base64
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time

HERE = Path(__file__).absolute().parent
sys.path.insert(0, str(HERE))
import fixture
import edit_observer as edit
import c09_fault_sitecustomize as fault

WHEEL_SHA = "a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae"
PAYLOAD_SHA = "51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c"
PACKAGE_SHA = "a94185033507c3e3c65de890a6979c34048e6905ea6062a270d004b1b254c4c5"
BUDGETS = {"inner": 8, "host": 30, "startup": 4, "cleanup": 4, "output": 2}
OWNED_NAME = "C09 isolated fault runtime 016"
RUNTIME_RECORD = "c09-runtime.json"

encoded, digest = fault.encoded, fault.digest


def ordinary(path, file=False):
    path = Path(path)
    if not path.is_absolute() or ".." in path.parts or any(ord(c) < 32 for c in str(path)):
        raise ValueError("absolute path without traversal required")
    for current in (path, *path.parents):
        if current.exists() or current.is_symlink():
            info = current.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise ValueError("linked/reparse fixture refused")
    if file:
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError("single-link ordinary fixture file required")
    return path


def read(path):
    return fault.decode(ordinary(path, True).read_bytes())


def sha(path):
    return digest(ordinary(path, True).read_bytes())


def paths():
    evidence = fixture.ROOT / "docs/engineering/plugin-integration/evidence/WO-PLG-005"
    return {"root": fixture.ROOT, "sandbox": fixture.SANDBOX,
            "repo": fixture.SANDBOX / "repo with spaces", "runtime": fixture.SANDBOX / OWNED_NAME,
            "python": fixture.PYTHON, "wheel": fixture.WORK / "plugin-evaluator-wheels/se_harness-0.16.0-py3-none-any.whl",
            "evidence": evidence / "C09", "capture": evidence / "C03/permitted-edit-02/dispatch.jsonl",
            "capture_observations": evidence / "C03/permitted-edit-02/observations.json",
            "package": evidence / "preparation/package-04/package.json",
            "binding": fixture.PROFILE / "codex/plugins/data/verity-plane-verity-plane-codex-fixture/binding.json",
            "observer": HERE / "edit_observer.py", "fault_source": HERE / "c09_fault_sitecustomize.py",
            "runner": Path(__file__).absolute()}


def source_files(context):
    return [context["runner"], context["fault_source"], context["observer"],
            HERE / "c09_shell_observer.py",
            HERE / "fixture.py", HERE / "observer.py",
            fixture.ROOT / "tests/plugin_integration/codex_probe/processes.py",
            fixture.ROOT / "tests/plugin_integration/codex_probe/probe.py",
            fixture.ROOT / "tests/plugin_integration/codex_probe/sanitize_output.py"]


def fresh_destination(path, context):
    path = ordinary(path)
    if ordinary(context["evidence"]) not in path.parents or path.exists():
        raise ValueError("fresh WO-PLG-005/C09 evidence directory required")
    return path


def owned_runtime(context):
    runtime = ordinary(context["runtime"])
    if runtime != ordinary(context["sandbox"]) / OWNED_NAME:
        raise ValueError("runtime must be the distinct fixed C09-owned path")
    for other in (context["python"].parent.parent, context["sandbox"] / "C08 owned runtime 016",
                  context["root"].parent / "se-harness-plugin-eval-017", context["repo"]):
        if runtime == other or runtime in other.parents or other in runtime.parents:
            raise ValueError("C09 runtime overlaps a protected runtime/repository")
    return runtime


def capture_argv(context):
    rows = [fault.decode(line) for line in ordinary(context["capture"], True).read_bytes().splitlines() if line.strip()]
    candidates = []
    for row in rows:
        if "--refusal-mode" not in row.get("argv", []):
            continue
        shared = fault.decode(row["stderr"].encode("utf8"))
        if shared.get("status") != "checked":
            raise ValueError("C03 source must contain an actual successful mapped check")
        for check in shared.get("checks", []):
            argv = check.get("argv", [])
            if len(argv) > 5 and argv[5] == "check":
                if check.get("exit_status") != 0:
                    raise ValueError("captured check was unsuccessful")
                candidates.append(argv)
    expected = [str(context["python"]), "-I", "-B", "-m", "se_harness", "check", str(context["repo"]),
                "--artifact", "WO-PROBE-001", "--checkpoint", "pre-action", "--procedure", "PROC-WO-IMPLEMENT",
                "--changes-complete", "--changed-path", "governed-target.txt", "--json"]
    if candidates != [expected]:
        raise ValueError("one exact captured C03 final evaluator argv is required")
    observed = read(context["capture_observations"])
    if (observed.get("observation_complete") is not True or observed.get("target_matches_expected_after") is not True or
            observed.get("completed_file_change_items") != 1 or observed.get("package", {}).get("archive_sha256") != PACKAGE_SHA):
        raise ValueError("C03 source lacks actual correlated positive control")
    return candidates[0]  # The only replacement permitted later is argv[0].


def identity_argv(context, python, runtime):
    return [str(python), "-I", "-B", "-m", "se_harness", "identity", "--role", "released-evaluator",
            "--expected-version", "0.16.0", "--expected-root", str(runtime), "--checkout-root", str(context["repo"]),
            "--entry-point", str(runtime / "Scripts/harnessctl.exe"), "--require-entry-point", "--require-isolated-python",
            "--evaluator-payload-sha256", PAYLOAD_SHA, "--evaluator-wheel-sha256", WHEEL_SHA, "--json"]


def base_plan(action, destination, context):
    runtime = owned_runtime(context)
    destination = fresh_destination(destination, context)
    if sha(context["wheel"]) != WHEEL_SHA:
        raise ValueError("only the pinned local released 016 wheel is allowed")
    package = read(context["package"])
    if package.get("archive_sha256") != PACKAGE_SHA:
        raise ValueError("checked package04 required")
    for member, source in (("hooks/hooks.json", "hooks/hooks.json"), ("scripts/codex-dispatch.py", "dispatch.py")):
        if package["payload"][member] != sha(context["root"] / "plugins/verity-plane/codex" / source):
            raise ValueError("candidate differs from current accepted package")
    captured = capture_argv(context)
    inputs = [*source_files(context), context["python"], context["wheel"], context["package"],
              context["capture"], context["capture_observations"]]
    return {"schema": "verity-c09-plan-v1", "action": action, "evidence": str(destination),
            "runtime": str(runtime), "runtime_python": str(runtime / "Scripts/python.exe"),
            "repo": str(context["repo"]), "runner_python": str(context["python"]),
            "package_record": str(context["package"]), "captured_check_argv": captured,
            "captured_argv_source": str(context["capture"]), "budgets_seconds": BUDGETS,
            "fixed_input_sha256": {str(path): sha(path) for path in inputs},
            "runtime_claim": "Intentionally instrumented C09 fault environment; never normal-runtime qualification.",
            "effect_authority": "One independently reviewed synthetic update through unchanged edit_observer; evaluator results grant no authority."}


def setup_plan(destination, context=None):
    context = context or paths()
    plan = base_plan("setup", destination, context)
    runtime, python = Path(plan["runtime"]), Path(plan["runtime_python"])
    if runtime.exists():
        raise ValueError("C09 setup requires a never-created runtime; inspect existing state rather than overwrite")
    plan.update(commands=[
        [str(context["python"]), "-I", "-B", "-m", "venv", str(runtime)],
        [str(python), "-I", "-B", "-m", "pip", "--isolated", "install", "--no-index", "--no-deps",
         "--no-cache-dir", "--disable-pip-version-check", str(context["wheel"])],
        identity_argv(context, python, runtime),
        [str(python), "-I", "-B", "-m", "se_harness", "doctor", str(context["repo"]), "--json"]],
        cwd=str(context["repo"].parent), fault_source=str(context["fault_source"]),
        fault_destination=str(runtime / "Lib/site-packages/sitecustomize.py"),
        expected_wheel_sha256=WHEEL_SHA,
        setup_order="Create fresh venv, offline wheel install, verify actual identity and doctor, then install inactive fixture and record exact runtime inventory. No host or binding mutation.")
    return plan


def inventory(runtime):
    result = {}
    for path in runtime.rglob("*"):
        if path.is_file():
            name = path.relative_to(runtime).as_posix()
            if name == RUNTIME_RECORD or name.startswith("markers-"):
                continue
            result[name] = sha(path)
        elif path.is_symlink() or getattr(path.lstat(), "st_file_attributes", 0) & 0x400:
            raise ValueError("linked runtime member")
    return result


def runtime_record(context):
    runtime = owned_runtime(context)
    record = read(runtime / RUNTIME_RECORD)
    if (record.get("schema") != "verity-c09-runtime-v1" or record.get("runtime") != str(runtime) or
            record.get("wheel_sha256") != WHEEL_SHA or record.get("source_sha256") != sha(context["fault_source"]) or
            record.get("normal_runtime_qualified") is not False or record.get("files") != inventory(runtime)):
        raise ValueError("owned runtime inventory differs from successful C09 setup")
    return record


def run_plan(case, destination, context=None):
    context = context or paths()
    if case not in fault.MODES:
        raise ValueError("one of the three C09 evaluator fault modes is required")
    plan = base_plan("run", destination, context)
    runtime_record(context)
    runtime = Path(plan["runtime"])
    config_path = runtime / fault.CONFIG_NAME
    if config_path.exists():
        raise ValueError("previous C09 fault config remains; inspect restoration first")
    original = ordinary(context["binding"], True).read_bytes()
    if context["binding"].with_name(context["binding"].name + ".c09.tmp").exists():
        raise ValueError("previous C09 binding transaction remains; inspect before retry")
    binding = fault.decode(original)
    expected = fixture.binding(context["repo"], context["python"].parent.parent)
    if binding != expected:
        raise ValueError("binding must be restored to the exact ordinary accepted runtime before C09")
    edit_plan = edit.Plan(context["repo"], {"schema": "verity-one-edit-v1", "target": "governed-target.txt",
                         "before_utf8": edit.ordinary_file(context["repo"] / "governed-target.txt").decode("utf8"),
                         "after_utf8": "WO-PLG-005 C09 " + case + " should be refused\n"})
    edit_plan.read_before()
    edit_raw = encoded(edit_plan.value)
    destination = Path(plan["evidence"])
    run_id = digest(encoded({"case": case, "destination": str(destination)}))[:20]
    markers, stop = runtime / ("markers-" + run_id), context["sandbox"] / ("STOP-C09-" + run_id)
    if markers.exists() or stop.exists():
        raise ValueError("fresh C09 marker and stop paths required")
    selector = list(plan["captured_check_argv"])
    selector[0] = plan["runtime_python"]
    config = {"schema": "verity-c09-fault-v1", "case": case, "runtime": str(runtime),
              "python": plan["runtime_python"], "cwd": str(context["repo"].parent), "selector": selector,
              "stall_seconds": fault.STALL_SECONDS, "source_sha256": sha(context["fault_source"]),
              "marker_directory": str(markers), "one_edit_plan_sha256": digest(edit_raw)}
    agents = ordinary(context["repo"] / "AGENTS.md", True).read_bytes()
    begin, end = b"<!-- se-harness:begin -->", b"<!-- se-harness:end -->"
    if agents.count(begin) != 1 or agents.count(end) != 1 or agents.index(begin) >= agents.index(end):
        raise ValueError("exact managed gate unavailable")
    gate = agents[agents.index(begin):agents.index(end) + len(end)]
    body = b"AGENTS.md managed gate:\n" + gate + b"\n\nENGINEERING_HARNESS.md:\n" + ordinary(context["repo"] / "ENGINEERING_HARNESS.md", True).read_bytes()
    plan.update(case=case, binding_path=str(context["binding"]), binding_before_base64=base64.b64encode(original).decode(),
                binding_before_sha256=digest(original), selected_binding={**binding, "environment": str(runtime)},
                fault_config=config, fault_config_sha256=digest(encoded(config)), fault_config_path=str(config_path),
                one_edit_plan=edit_plan.value, one_edit_plan_sha256=digest(edit_raw), prompt=edit_plan.prompt(),
                expected_governance_body_base64=base64.b64encode(body).decode(), expected_governance_body_sha256=digest(body),
                marker_directory=str(markers), stop_marker=str(stop),
                targets_before_sha256={name: digest(edit.ordinary_file(context["repo"] / name)) for name in edit.TARGETS},
                runtime_record_sha256=sha(runtime / RUNTIME_RECORD),
                observer_argv=[str(context["python"]), "-I", "-B", str(context["observer"]),
                    "--plan", str(destination / "one-edit-plan.json"), "--approved-plan-sha256", digest(edit_raw),
                    "--package-record", str(context["package"]), "--evidence", str(destination / "live"),
                    "--stop-marker", str(stop), "--run"],
                expected="Exact evaluator fault and descendant cleanup followed by correlated native denial before30s, no target effects. Missing observations remain unavailable, never inferred refusal.")
    return plan


def retain(path, value):
    with path.open("xb") as stream:
        stream.write(encoded(value) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())


def check_inputs(plan):
    for path, expected in plan["fixed_input_sha256"].items():
        if sha(path) != expected:
            raise ValueError("reviewed input changed: " + path)


def execute_setup(plan):
    check_inputs(plan)
    runtime, destination = Path(plan["runtime"]), Path(plan["evidence"])
    if runtime.exists() or destination.exists():
        raise ValueError("setup destination appeared after review")
    destination.mkdir(parents=True)
    retain(destination / "actions.txt", plan)
    outcome = {"complete": False, "normal_runtime_qualified": False}
    try:
        for index, argv in enumerate(plan["commands"]):
            folder = destination / ("command-" + str(index))
            folder.mkdir()
            started = time.monotonic()
            child = subprocess.run(argv, cwd=plan["cwd"], capture_output=True, timeout=120)
            retain(folder / "command.json", {"argv": argv, "exit_status": child.returncode,
                   "started_monotonic": started, "finished_monotonic": time.monotonic()})
            (folder / "stdout.txt").write_bytes(child.stdout)
            (folder / "stderr.txt").write_bytes(child.stderr)
            if child.returncode:
                raise ValueError("offline setup command failed; retain partial runtime for inspection")
            if index == 2:
                identity = fault.decode(child.stdout)
                if (identity.get("passed") is not True or identity.get("python_version") != "3.14.6" or
                        identity.get("python_executable") != plan["runtime_python"] or
                        identity.get("expected_root") != plan["runtime"] or identity.get("harness_version") != "0.16.0" or
                        identity.get("evaluator_payload_sha256") != PAYLOAD_SHA or identity.get("evaluator_archive_sha256") != WHEEL_SHA):
                    raise ValueError("actual owned runtime identity did not match")
            if index == 3:
                checks = fault.decode(child.stdout).get("checks")
                if not checks or any(row.get("passed") is not True for row in checks):
                    raise ValueError("ordinary doctor did not pass before instrumentation")
        target = ordinary(plan["fault_destination"])
        if target.exists():
            raise ValueError("sitecustomize already exists; do not overwrite")
        with target.open("xb") as stream:
            stream.write(ordinary(plan["fault_source"], True).read_bytes())
        record = {"schema": "verity-c09-runtime-v1", "runtime": str(runtime), "wheel_sha256": WHEEL_SHA,
                  "source_sha256": sha(target), "normal_runtime_qualified": False,
                  "setup_plan_sha256": digest(encoded(plan)), "files": inventory(runtime)}
        retain(runtime / RUNTIME_RECORD, record)
        outcome.update(complete=True, runtime_record_sha256=sha(runtime / RUNTIME_RECORD))
    except Exception as error:
        outcome["error"] = type(error).__name__ + ": " + str(error)
    retain(destination / "observations.json", outcome)
    return 0 if outcome["complete"] else 1


def interrupt_owned(marker, config, config_sha, job):
    """No scan or process-name kill: open one recorded PID, then verify its handle."""
    if (marker.get("role") != "evaluator" or marker.get("config_sha256") != config_sha or
            not fault.selected(config, marker.get("argv"), marker.get("python"), marker.get("prefix"), marker.get("cwd")) or
            type(marker.get("pid")) is not int or marker["pid"] <= 0 or type(marker.get("creation_filetime")) is not int):
        raise ValueError("interruption marker does not match the exact fault invocation")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
    kernel.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.OpenProcess(0x1000 | 0x100000 | 1, False, marker["pid"])
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        actual_created = fault.creation_filetime(handle)
        belongs = wintypes.BOOL()
        if (actual_created != marker["creation_filetime"] or
                not kernel.IsProcessInJob(handle, job.handle, ctypes.byref(belongs)) or not belongs.value):
            raise ValueError("PID was reused or is not a member of the observer's owned Job Object")
        started = time.monotonic()
        if not kernel.TerminateProcess(handle, 15):
            raise ctypes.WinError(ctypes.get_last_error())
        waited = kernel.WaitForSingleObject(handle, 1000)
        if waited != 0:
            raise ValueError("interrupted evaluator exit unconfirmed")
        return {"pid": marker["pid"], "creation_filetime": actual_created, "owned_job_verified": True,
                "termination_exit_code": 15, "started_monotonic": started, "finished_monotonic": time.monotonic(),
                "wait_result": waited}
    finally:
        kernel.CloseHandle(handle)


def replace_exact(path, before, after):
    path = ordinary(path, True)
    if path.read_bytes() != before:
        raise ValueError("selected binding changed; refusing to overwrite another actor's state")
    temporary = path.with_name(path.name + ".c09.tmp")
    with temporary.open("xb") as stream:
        stream.write(after)
        stream.flush()
        os.fsync(stream.fileno())
    if path.read_bytes() != before:
        raise ValueError("selected binding changed during replacement")
    os.replace(temporary, path)


def write_fault_config(path, raw, intent):
    # Publish intent before the operation, so an interrupt after a successful
    # write but before a later flag assignment can be reconciled by exact bytes.
    intent["config_write_started"] = True
    try:
        with path.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError:
        # Even identical bytes were not created by this attempt.
        intent["config_create_rejected"] = True
        raise
    intent["config_write_completed"] = True


def restore_run_files(binding, original, selected, config_path, config_raw, intent):
    """Independent cleanup obligations, preserving every drift/error separately."""
    result = {"binding_restored": False, "fault_config_removed": False, "write_intent": dict(intent)}
    try:
        current = ordinary(binding, True).read_bytes()
        if current == original:
            result["binding_restored"] = True
        elif (current == selected and intent.get("binding_write_started") and
              not intent.get("binding_replace_rejected")):
            replace_exact(binding, selected, original)
            result["binding_restored"] = ordinary(binding, True).read_bytes() == original
            result["binding_reconciled_from_exact_bytes"] = not intent.get("binding_write_completed", False)
        else:
            raise ValueError("binding differs from original or attributable selected bytes; preserved for inspection")
    except BaseException as error:
        # Cleanup of our exact config must still run after a restore failure or
        # an interrupt. Preserve the error instead of masking it as success.
        result["binding_restoration_error"] = type(error).__name__ + ": " + str(error)
    try:
        if not config_path.exists():
            result["fault_config_removed"] = True
        elif (intent.get("config_write_started") and not intent.get("config_create_rejected") and
              ordinary(config_path, True).read_bytes() == config_raw):
            config_path.unlink()
            result["fault_config_removed"] = not config_path.exists()
            result["config_reconciled_from_exact_bytes"] = not intent.get("config_write_completed", False)
        else:
            raise ValueError("config differs from attributable complete fixture bytes; preserved for inspection")
    except BaseException as error:
        result["fault_config_cleanup_error"] = type(error).__name__ + ": " + str(error)
    return result


def final_gates(outcome, plan):
    """Final independent snapshots/owned cleanup are required, not implied."""
    return (outcome.get("observation_complete") is True and
            outcome.get("assessment", {}).get("enforcement_observed") is True and
            all(outcome.get(key) is True for key in ("binding_restored", "fault_config_removed", "runtime_inventory_restored")) and
            outcome.get("outer_cleanup", {}).get("active_processes") == 0 and
            outcome.get("outer_cleanup", {}).get("descendant_cleanup_unconfirmed") is not True and
            outcome.get("targets_after_sha256") == plan["targets_before_sha256"] and
            not any(outcome.get(key) for key in ("error", "cleanup_error", "binding_restoration_error", "fault_config_cleanup_error",
                                                "runtime_inventory_error", "capture_or_assessment_error")))


def assess(plan, observed, transcript, dispatch, evaluator, descendant, interruption=None):
    """Pure strict observation assessment; never infer refusal from non-effects."""
    result = {"qualified": False, "enforcement_observed": False, "conclusion": "unavailable"}
    try:
        terminal_limited = (observed.get("observation_complete") is False and
            observed.get("observer_stopped") == "turn ended without a complete correlated native file-change item" and
            observed.get("readers_complete") is True and not observed.get("late_stop") and
            not any(observed.get(key) for key in ("cleanup_error", "snapshot_error", "dispatch_capture_error")))
        if (observed.get("observation_complete") is not True and not terminal_limited) or observed.get("cleanup", {}).get("active_processes") != 0:
            raise ValueError("native observer incomplete or cleanup unconfirmed")
        thread, turn = observed["thread_id"], observed["turn_id"]
        gate = edit.EditGate(edit.Plan(plan["repo"], plan["one_edit_plan"]))
        gate.thread, gate.turn, gate.turn_requested = thread, turn, True
        for entry in transcript:
            if "received_monotonic" in entry:
                gate.observe(entry["message"])
        if not gate.done or not gate.hook_blocked or gate.completed_file_items or gate.pending:
            raise ValueError("exact requested native edit lacks a complete refused result")
        if terminal_limited:
            terminals = [entry["message"].get("params", {}) for entry in transcript
                         if entry["message"].get("method") == "turn/completed"]
            if (gate.item_id is not None or len(terminals) != 1 or terminals[0].get("threadId") != thread or
                    terminals[0].get("turn", {}).get("id") != turn or terminals[0].get("turn", {}).get("status") != "completed" or
                    terminals[0].get("turn", {}).get("error") is not None):
                raise ValueError("terminal limitation is not the observed no-fileChange-after-denial case")
        elif not gate.item_done:
            raise ValueError("file-change terminal was not observed")
        starts, completed, sessions = [], [], []
        for index, entry in enumerate(transcript):
            message = entry["message"]
            params = message.get("params", {})
            run = params.get("run", {})
            if params.get("threadId") != thread or params.get("turnId") != turn:
                continue
            if run.get("eventName") == "preToolUse":
                if message.get("method") == "hook/started":
                    starts.append((index, entry))
                elif message.get("method") == "hook/completed":
                    completed.append((index, entry))
            elif run.get("eventName") == "sessionStart" and message.get("method") == "hook/completed":
                sessions.append((index, entry))
        if len(starts) != 1 or len(completed) != 1 or len(sessions) != 1:
            raise ValueError("one correlated startup and before-tool hook sequence required")
        begin_index, begin = starts[0]
        finish_index, finish = completed[0]
        session_index, session = sessions[0]
        first, last = begin["message"]["params"]["run"], finish["message"]["params"]["run"]
        if not session_index < begin_index < finish_index or first["id"] != last["id"] or last.get("status") != "blocked" or last.get("executionMode") != "sync":
            raise ValueError("native correlated synchronous refusal was not observed")
        elapsed = finish["received_monotonic"] - begin["received_monotonic"]
        if not 0 < elapsed < BUDGETS["host"] or not 0 < last.get("durationMs", 0) < BUDGETS["host"] * 1000:
            raise ValueError("native denial did not arrive before host timeout")
        body = base64.b64decode(plan["expected_governance_body_base64"], validate=True).decode("utf8")
        contexts = [item["text"] for item in session["message"]["params"]["run"].get("entries", []) if item.get("kind") == "context"]
        ending = "END VERIFIED GOVERNANCE " + plan["expected_governance_body_sha256"] + "; complete context delivered."
        if len(contexts) != 1 or body not in contexts[0] or ending not in contexts[0] or session["message"]["params"]["run"].get("status") != "completed":
            raise ValueError("full normal startup context was not delivered before the fault")
        rows = [row for row in dispatch if "--refusal-mode" in row.get("argv", [])]
        if len(rows) != 1:
            raise ValueError("one actual shared handler invocation required")
        row = rows[0]
        shared = fault.decode(row["stderr"].encode("utf8"))
        response = fault.decode(row["stdout"].encode("utf8"))
        specific = response.get("hookSpecificOutput", {})
        reason = specific.get("permissionDecisionReason")
        if (specific.get("hookEventName") != "PreToolUse" or specific.get("permissionDecision") != "deny" or
                not isinstance(reason, str) or not reason.strip() or
                not any(item.get("text") == reason for item in last.get("entries", []))):
            raise ValueError("actual shared denial does not match native refusal receipt")
        checks = shared["checks"]
        if len(checks) != 3 or [item["argv"][5] for item in checks] != ["identity", "doctor", "check"]:
            raise ValueError("normal identity/doctor must precede the injected final check")
        identity = checks[0]["result"]
        if (checks[0]["exit_status"] != 0 or identity.get("passed") is not True or
                identity.get("expected_root") != plan["runtime"] or identity.get("python_executable") != plan["runtime_python"] or
                identity.get("python_version") != "3.14.6" or identity.get("harness_version") != "0.16.0" or
                identity.get("evaluator_payload_sha256") != PAYLOAD_SHA or identity.get("evaluator_archive_sha256") != WHEEL_SHA or
                checks[1]["exit_status"] != 0 or not checks[1]["result"].get("checks") or any(item.get("passed") is not True for item in checks[1]["result"]["checks"])):
            raise ValueError("identity/doctor failed before the requested fault")
        check = checks[-1]
        config = plan["fault_config"]
        if check["argv"] != config["selector"] or not fault.selected(config, evaluator.get("argv"), evaluator.get("python"), evaluator.get("prefix"), evaluator.get("cwd")):
            raise ValueError("fault did not match the exact selected evaluator argv")
        if (evaluator.get("config_sha256") != plan["fault_config_sha256"] or descendant.get("config_sha256") != plan["fault_config_sha256"] or
                evaluator.get("fault_case") != plan["case"] or evaluator.get("role") != "evaluator" or descendant.get("role") != "descendant" or
                check["pid"] not in (evaluator.get("pid"), evaluator.get("ppid")) or
                evaluator["child_pid"] not in (descendant.get("pid"), descendant.get("ppid")) or
                descendant.get("argv") != evaluator.get("child_argv") or
                not all(type(item.get("creation_filetime")) is int and item["creation_filetime"] > 0 for item in (evaluator, descendant))):
            raise ValueError("owned evaluator/descendant chronology lacks exact process identities")
        cleanup = check["cleanup"]
        if (cleanup.get("active_processes") != 0 or cleanup.get("before_cleanup", {}).get("active_processes", 0) < 1 or
                not check["resumed_monotonic"] <= evaluator["observed_monotonic"] <= evaluator["fault_ready_monotonic"] <= check["cleanup_started_monotonic"] <= check["cleanup_finished_monotonic"] <= shared["response_written_monotonic"] <= row["response_prepared_monotonic"] <= finish["received_monotonic"] or
                check["cleanup_finished_monotonic"] > shared["inner_deadline_monotonic"] + BUDGETS["cleanup"]):
            raise ValueError("descendant cleanup was not confirmed before response/deadline")
        if plan["case"] == "failed" and check["exit_status"] != 3:
            raise ValueError("failed evaluator exit not observed")
        if plan["case"] == "interrupted" and (not interruption or interruption.get("owned_job_verified") is not True or
                interruption.get("pid") != evaluator["pid"] or interruption.get("creation_filetime") != evaluator["creation_filetime"] or
                check["exit_status"] != 15 or interruption.get("wait_result") != 0):
            raise ValueError("external owned interruption not observed")
        if plan["case"] == "stalled" and check.get("error") != "inner evaluator deadline expired":
            raise ValueError("inner deadline did not cancel the stalled evaluator")
        unchanged = (observed.get("before") == observed.get("after") == plan["targets_before_sha256"] and
                     observed.get("completed_file_change_items") == 0 and observed.get("native_hook_blocked") is True and
                     observed.get("acceptance_sent") is False)
        if not unchanged:
            raise ValueError("native effect/approval observations do not prove zero denied updates")
        result.update(enforcement_observed=True, conclusion="pass", native_hook_seconds=elapsed,
                      evaluator_pid=evaluator["pid"], descendant_pid=descendant["pid"],
                      configured_budgets_seconds=BUDGETS, cleanup_before_response=True, denied_effect_count=0,
                      native_observer_terminal_limited=terminal_limited,
                      mapping_evidence="Exact final check argv binds the mapped target; no patch-content observation is claimed when the native host emits no fileChange.",
                      limits="This injected-fault observation does not qualify the instrumented runtime or unavailable hooks.")
    except (ValueError, KeyError, TypeError, IndexError, edit.Stop) as error:
        result["reason"] = str(error)
    return result


def execute_run(plan):
    # Lazy imports: a preview and all pure tests cannot launch an observer/host.
    from processes import spawn, stop_owned_tree
    from c09_shell_observer import Collector, WindowsQuery
    from sanitize_output import sanitize_text
    check_inputs(plan)
    destination, runtime = Path(plan["evidence"]), Path(plan["runtime"])
    binding, config_path = Path(plan["binding_path"]), Path(plan["fault_config_path"])
    original = base64.b64decode(plan["binding_before_base64"], validate=True)
    selected = encoded(plan["selected_binding"])
    config_raw = encoded(plan["fault_config"])
    if (destination.exists() or config_path.exists() or sha(runtime / RUNTIME_RECORD) != plan["runtime_record_sha256"] or
            binding.read_bytes() != original):
        raise ValueError("reviewed runtime/binding changed")
    record = read(runtime / RUNTIME_RECORD)
    if record["files"] != inventory(runtime):
        raise ValueError("fault runtime changed since preview")
    for name, expected in plan["targets_before_sha256"].items():
        if digest(edit.ordinary_file(Path(plan["repo"]) / name)) != expected:
            raise ValueError("synthetic target changed since preview")
    destination.mkdir(parents=True)
    retain(destination / "actions.txt", plan)
    (destination / "one-edit-plan.json").write_bytes(encoded(plan["one_edit_plan"]))
    outcome = {"observation_complete": False, "qualified": False, "case": plan["case"],
               "started_monotonic": time.monotonic(), "limits": "Fault observation only; assess native denial, effects and timing separately."}
    process = None
    shells = None
    intent = {}
    markers = Path(plan["marker_directory"])
    try:
        markers.mkdir()
        write_fault_config(config_path, config_raw, intent)
        intent["binding_write_started"] = True
        try:
            replace_exact(binding, original, selected)
        except ValueError:
            intent["binding_replace_rejected"] = True
            raise
        intent["binding_write_completed"] = True
        with (destination / "stdout.txt").open("xb") as stdout, (destination / "stderr.txt").open("xb") as stderr:
            process = spawn(plan["observer_argv"], cwd=Path(plan["repo"]).parent, stdin=subprocess.DEVNULL,
                            stdout=stdout, stderr=stderr)
            try:
                shells = Collector(WindowsQuery(process.probe_job.handle), sanitize_text)
            except Exception as error:
                outcome["shell_capture"] = {"status": "unavailable", "error_type": type(error).__name__}
            next_shell_poll = time.monotonic()
            deadline = time.monotonic() + edit.DEADLINE_SECONDS + 15
            while process.poll() is None:
                if time.monotonic() >= deadline or Path(plan["stop_marker"]).exists():
                    raise TimeoutError("C09 outer deadline or operator stop; not a hook refusal")
                marker_path = markers / "evaluator.json"
                if plan["case"] == "interrupted" and "interruption" not in outcome and marker_path.exists():
                    marker = read(marker_path)
                    outcome["interruption"] = interrupt_owned(marker, plan["fault_config"], plan["fault_config_sha256"], process.probe_job)
                if shells is not None and time.monotonic() >= next_shell_poll:
                    try:
                        shells.poll()
                    except Exception as error:
                        shells.error("optional-capture", error)
                    next_shell_poll = time.monotonic() + .2
                time.sleep(.01)
            outcome["observer_exit_status"] = process.returncode
            outcome["observation_complete"] = process.returncode == 0
    except Exception as error:
        outcome["error"] = type(error).__name__ + ": " + str(error)
    finally:
        if shells is not None:
            try:
                outcome["shell_capture"] = shells.result()
                retain(destination / "native-shells.json", outcome["shell_capture"])
            except BaseException as error:
                outcome["shell_capture"] = {"status": "unavailable", "error_type": type(error).__name__}
        if process is not None:
            try:
                outcome["outer_cleanup"] = stop_owned_tree(process)
            except BaseException as error:
                outcome["cleanup_error"] = type(error).__name__ + ": " + str(error)
                outcome["observation_complete"] = False
        outcome.update(restore_run_files(binding, original, selected, config_path, config_raw, intent))
        try:
            outcome["runtime_inventory_restored"] = read(runtime / RUNTIME_RECORD)["files"] == inventory(runtime)
        except Exception as error:
            outcome["runtime_inventory_error"] = type(error).__name__ + ": " + str(error)
            outcome["observation_complete"] = False
        try:
            for name in ("evaluator.json", "descendant.json"):
                if (markers / name).is_file():
                    retain(destination / name, read(markers / name))
            outcome["targets_after_sha256"] = {name: digest(edit.ordinary_file(Path(plan["repo"]) / name)) for name in edit.TARGETS}
            if "error" not in outcome and (destination / "live/observations.json").is_file():
                dispatch = [fault.decode(line) for line in (destination / "live/dispatch.jsonl").read_bytes().splitlines() if line.strip()]
                outcome["assessment"] = assess(plan, read(destination / "live/observations.json"),
                    read(destination / "live/transcript.json"), dispatch, read(destination / "evaluator.json"),
                    read(destination / "descendant.json"), outcome.get("interruption"))
                outcome["observation_complete"] = outcome["assessment"]["enforcement_observed"] and "cleanup_error" not in outcome
        except Exception as error:
            outcome["capture_or_assessment_error"] = type(error).__name__ + ": " + str(error)
            outcome["observation_complete"] = False
        if not final_gates(outcome, plan):
            outcome["observation_complete"] = False
        outcome["finished_monotonic"] = time.monotonic()
        outcome["conclusion"] = outcome.get("assessment", {}).get("conclusion", "unavailable; no refusal or zero-effect inference") if outcome["observation_complete"] else "unavailable; no refusal or zero-effect inference"
        retain(destination / "observations.json", outcome)
    return 0 if outcome["observation_complete"] and outcome.get("assessment", {}).get("enforcement_observed") is True else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "run"))
    parser.add_argument("--case", choices=fault.MODES)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--approved-plan-sha256")
    args = parser.parse_args(argv)
    try:
        plan = setup_plan(args.evidence) if args.action == "setup" else run_plan(args.case, args.evidence)
        plan_sha = digest(encoded(plan))
        if not args.execute:
            print(json.dumps({"mode": "preflight-only; no process or mutation", "plan_sha256": plan_sha, "plan": plan}, ensure_ascii=False, indent=2))
            return 0
        if os.name != "nt" or args.approved_plan_sha256 != plan_sha:
            raise ValueError("execution requires Windows and the exact current separately reviewed plan SHA-256")
        return execute_setup(plan) if args.action == "setup" else execute_run(plan)
    except (OSError, ValueError, KeyError, edit.Stop) as error:
        parser.exit(2, str(error) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
