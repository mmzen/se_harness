"""C10/C11 native-output fault plans. Preview is the default; no host is spawned.

A distinct intentionally instrumented runtime replaces only the disposable
binding selection. Registered guard, cache, trust and one-edit gate are unchanged.
No observation qualifies this fault runtime or exercises a lifecycle decision.
"""
import argparse
import base64
import ctypes
from ctypes import wintypes
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).absolute().parent
sys.path.insert(0, str(HERE))
import fixture
import edit_observer as edit
import c09_runner as prior
import c10_c11_fault_sitecustomize as fault
from c08_runner import ordinary, file_hash, replace_binding

OWNED_NAME = "C10 C11 isolated output fault runtime 016"
RECORD = "c10-c11-runtime.json"
encoded, digest, decode = fault.encoded, fault.digest, fault.decode


def read(path):
    return decode(ordinary(path, file=True).read_bytes())


def retain(path, value):
    with path.open("xb") as stream:
        stream.write(encoded(value) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())


def paths():
    evidence = fixture.ROOT / "docs/engineering/plugin-integration/evidence/WO-PLG-005"
    return {"root":fixture.ROOT, "repo":fixture.SANDBOX / "repo with spaces", "sandbox":fixture.SANDBOX,
        "runtime":fixture.SANDBOX / OWNED_NAME, "python":fixture.PYTHON,
        "wheel":fixture.WORK / "plugin-evaluator-wheels/se_harness-0.16.0-py3-none-any.whl",
        "package":evidence / "preparation/package-04/package.json", "evidence":evidence,
        "shell_capture":evidence / "C09/failed-01/native-shells.json",
        "native_control":evidence / "C09/failed-01/live/observations.json",
        "binding":fixture.PROFILE / "codex/plugins/data/verity-plane-verity-plane-codex-fixture/binding.json",
        "profile_config":fixture.PROFILE / "codex/config.toml",
        "fault_source":HERE / "c10_c11_fault_sitecustomize.py", "runner":Path(__file__).absolute()}


def windows_argv(command):
    parse = ctypes.windll.shell32.CommandLineToArgvW
    parse.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_int)]
    parse.restype = ctypes.POINTER(wintypes.LPWSTR)
    free = ctypes.windll.kernel32.LocalFree
    free.argtypes = [ctypes.c_void_p]
    count = ctypes.c_int()
    pointer = parse(command, ctypes.byref(count))
    if not pointer:
        raise ValueError("captured Windows command line could not be decoded")
    try:
        return [pointer[i] for i in range(count.value)]
    finally:
        free(pointer)


def native_guard_selection(capture, definitions, parse=windows_argv):
    """Match retained native shell arrays to both exact registered guard bodies."""
    if capture.get("status") != "observed" or capture.get("errors"):
        raise ValueError("complete eligible native shell capture required")
    found = {}
    for row in capture.get("records", []):
        if (row.get("owned_job_verified") is not True or row.get("raw_command_line_retained") is not True or
                row.get("selector_eligible") is not True or digest(row["command_line"].encode("utf-16-le")) != row.get("command_line_utf16le_sha256")):
            raise ValueError("native shell identity or raw command proof unavailable")
        argv = parse(row["command_line"])
        if len(argv) != 4 or argv[1:3] != ["-NoProfile", "-Command"] or Path(argv[0]) != Path(row["executable"]):
            raise ValueError("actual shell argument form differs from the observed accepted route")
        for event in ("SessionStart", "PreToolUse"):
            command = definitions["hooks"][event][0]["hooks"][0]
            if argv[3] == command["command"] and command["timeout"] == 30:
                if event in found:
                    raise ValueError("ambiguous duplicate native guard capture")
                found[event] = {"argv":argv, "pid":row["pid"], "creation_filetime":row["creation_filetime"],
                    "command_line_utf16le_sha256":row["command_line_utf16le_sha256"]}
    if set(found) != {"SessionStart", "PreToolUse"}:
        raise ValueError("both exact native guard commands must be demonstrated")
    return found


def inventory(runtime):
    result = {}
    for path in runtime.rglob("*"):
        name = path.relative_to(runtime).as_posix()
        ordinary(path)
        if path.is_file() and name != RECORD and not name.startswith("markers-"):
            result[name] = file_hash(path)
    return result


def base_plan(action, destination, context):
    runtime = ordinary(context["runtime"])
    if runtime != ordinary(context["sandbox"]) / OWNED_NAME:
        raise ValueError("only the exact distinct C10/C11-owned runtime is permitted")
    protected = [context["root"], context["repo"], context["python"].parent.parent,
        context["sandbox"] / "C08 owned runtime 016", context["sandbox"] / prior.OWNED_NAME,
        context["root"].parent / "se-harness-plugin-eval-017"]
    if any(runtime == item or runtime in item.parents or item in runtime.parents for item in protected):
        raise ValueError("output fault runtime overlaps a protected tree")
    destination = ordinary(destination)
    if context["evidence"] not in destination.parents or destination.exists():
        raise ValueError("fresh WO005 evidence directory required")
    if file_hash(context["wheel"]) != prior.WHEEL_SHA:
        raise ValueError("pinned offline 016 wheel required")
    package = read(context["package"])
    hooks = context["root"] / "plugins/verity-plane/codex/hooks/hooks.json"
    if (package.get("archive_sha256") != prior.PACKAGE_SHA or package["payload"]["hooks/hooks.json"] != file_hash(hooks) or
        package["payload"]["scripts/codex-dispatch.py"] != file_hash(context["root"] / "plugins/verity-plane/codex/dispatch.py")):
        raise ValueError("unchanged checked package04 required")
    native = read(context["native_control"])
    loaded = ordinary(native["loaded_payload"]["root"])
    if native["loaded_payload"]["sha256"] != package["payload"]:
        raise ValueError("actual loaded payload control differs from package04")
    guards = native_guard_selection(read(context["shell_capture"]), read(hooks))
    inputs = [context["runner"], context["fault_source"], Path(prior.__file__), Path(edit.__file__),
        Path(fixture.__file__), HERE / "c08_runner.py", HERE / "observer.py",
        context["root"] / "tests/plugin_integration/codex_probe/processes.py",
        context["root"] / "tests/plugin_integration/codex_probe/probe.py",
        context["root"] / "tests/plugin_integration/codex_probe/sanitize_output.py",
        context["python"], context["wheel"], context["package"], context["shell_capture"], context["native_control"],
        context["profile_config"], hooks, loaded / "scripts/codex-dispatch.py"]
    return {"schema":"verity-c10-c11-plan-v1", "action":action, "evidence":str(destination),
        "runtime":str(runtime), "runtime_python":str(runtime / "Scripts/python.exe"), "runner_python":str(context["python"]),
        "repo":str(context["repo"]), "package_record":str(context["package"]), "package_payload":package["payload"],
        "plugin_root":str(loaded), "plugin_data":str(context["binding"].parent), "native_guard_control":guards,
        "profile_config_path":str(context["profile_config"]), "profile_config_sha256":file_hash(context["profile_config"]),
        "fixed_input_sha256":{str(path):file_hash(path) for path in inputs},
        "runtime_qualified":False, "boundary":"Intentionally instrumented dispatcher startup; no normal-runtime or new-profile qualification.",
        "guard_start_failure":"Not tested by this route. A launched fixture exit97 is not missing native shell/guard or interpreter removal."}


def setup_plan(destination, context=None):
    context = context or paths()
    plan = base_plan("setup", destination, context)
    runtime, python = Path(plan["runtime"]), Path(plan["runtime_python"])
    if runtime.exists():
        raise ValueError("setup requires a never-created distinct runtime")
    plan.update(commands=[
        [str(context["python"]), "-I", "-B", "-m", "venv", str(runtime)],
        [str(python), "-I", "-B", "-m", "pip", "--isolated", "install", "--no-index", "--no-deps", "--no-cache-dir", "--disable-pip-version-check", str(context["wheel"])],
        prior.identity_argv(context, python, runtime),
        [str(python), "-I", "-B", "-m", "se_harness", "doctor", str(context["repo"]), "--json"]],
        cwd=str(context["repo"].parent), fault_source=str(context["fault_source"]),
        fault_destination=str(runtime / "Lib/site-packages/sitecustomize.py"),
        setup_order="Offline fresh venv/wheel, actual identity+doctor, then inactive instrumentation and inventory. No host or binding change.")
    return plan


def runtime_record(context):
    runtime = ordinary(context["runtime"])
    record = read(runtime / RECORD)
    if (record.get("schema") != "verity-c10-c11-runtime-v1" or record.get("runtime") != str(runtime) or
        record.get("runtime_qualified") is not False or record.get("source_sha256") != file_hash(context["fault_source"]) or
        record.get("wheel_sha256") != prior.WHEEL_SHA or record.get("files") != inventory(runtime)):
        raise ValueError("distinct output fault runtime differs from its successful setup record")
    return record


def run_plan(case, destination, context=None):
    context = context or paths()
    if case not in fault.MODES:
        raise ValueError("one explicit C10/C11 output fault is required")
    if context["evidence"] / ("C10" if case == "hang" else "C11") not in Path(destination).parents:
        raise ValueError("use the matching C10 or C11 evidence subtree")
    plan = base_plan("run", destination, context)
    runtime_record(context)
    runtime = Path(plan["runtime"])
    config_path = runtime / fault.CONFIG_NAME
    if config_path.exists() or context["binding"].with_name("binding.c10-c11.tmp").exists():
        raise ValueError("previous fault transaction remains; inspect before retry")
    original = ordinary(context["binding"], file=True).read_bytes()
    binding = decode(original.decode("utf-8-sig").encode("utf8"))
    if binding != fixture.binding(context["repo"], context["python"].parent.parent):
        raise ValueError("ordinary shared-016 binding must be restored before this case")
    one_edit = edit.Plan(context["repo"], {"schema":"verity-one-edit-v1", "target":"governed-target.txt",
        "before_utf8":edit.ordinary_file(context["repo"] / "governed-target.txt").decode("utf8"),
        "after_utf8":"WO-PLG-005 " + ("C10 " if case == "hang" else "C11 ") + case + " exact observed effect\n"})
    one_edit.read_before()
    raw_edit = encoded(one_edit.value)
    run_id = digest(encoded({"case":case,"evidence":str(destination)}))[:20]
    markers = runtime / ("markers-" + run_id)
    stop = context["sandbox"] / ("STOP-C10-C11-" + run_id)
    if markers.exists() or stop.exists():
        raise ValueError("fresh marker and external stop paths required")
    selector = [plan["runtime_python"], "-I", "-B", str(Path(plan["plugin_root"]) / "scripts/codex-dispatch.py"),
        "--data", plan["plugin_data"], "--event", "PreToolUse"]
    config = {"schema":"verity-native-output-fault-v1", "case":case, "runtime":str(runtime), "python":plan["runtime_python"],
        "cwd":plan["repo"], "selector":selector, "stall_seconds":fault.STALL_SECONDS,
        "source_sha256":file_hash(context["fault_source"]), "marker_directory":str(markers),
        "one_edit_plan_sha256":digest(raw_edit), "one_edit_plan":one_edit.value,
        "plugin_root":plan["plugin_root"], "plugin_data":plan["plugin_data"]}
    agents = edit.ordinary_file(context["repo"] / "AGENTS.md")
    begin, end = b"<!-- se-harness:begin -->", b"<!-- se-harness:end -->"
    if agents.count(begin) != 1 or agents.count(end) != 1 or agents.index(begin) >= agents.index(end):
        raise ValueError("complete ordered managed gate required")
    body = b"AGENTS.md managed gate:\n" + agents[agents.index(begin):agents.index(end)+len(end)] + b"\n\nENGINEERING_HARNESS.md:\n" + edit.ordinary_file(context["repo"] / "ENGINEERING_HARNESS.md")
    plan.update(case=case, binding_path=str(context["binding"]), binding_before_base64=base64.b64encode(original).decode(),
        binding_before_sha256=digest(original), selected_binding={**binding,"environment":str(runtime)},
        fault_config=config, fault_config_sha256=digest(encoded(config)), fault_config_path=str(config_path),
        marker_directory=str(markers), stop_marker=str(stop), runtime_record_sha256=file_hash(runtime / RECORD),
        one_edit_plan=one_edit.value, one_edit_plan_sha256=digest(raw_edit), prompt=one_edit.prompt(),
        targets_before_sha256={name:digest(edit.ordinary_file(context["repo"] / name)) for name in edit.TARGETS},
        targets_expected_after_sha256={name:digest(one_edit.after if name == one_edit.value["target"] else edit.ordinary_file(context["repo"] / name)) for name in edit.TARGETS},
        expected_governance_body_base64=base64.b64encode(body).decode(), expected_governance_body_sha256=digest(body),
        observer_argv=[str(context["python"]), "-I", "-B", str(Path(edit.__file__)), "--plan",str(Path(destination)/"one-edit-plan.json"),
            "--approved-plan-sha256",digest(raw_edit), "--package-record",str(context["package"]),
            "--evidence",str(Path(destination)/"live"), "--stop-marker",str(stop), "--run"],
        selector_origin="Exact native guard source expanded against actual loaded package root and explicit selected binding; the injected process's actual full argv/cwd/PLUGIN_ROOT/PLUGIN_DATA marker must corroborate it before any fault counts.",
        expected="Full normal SessionStart context; exact dispatcher fault; actual native timeout/output receipt and independent effect/cleanup observations. No denial is inferred from observer cancellation.")
    return plan


def check_inputs(plan):
    for path, expected in plan["fixed_input_sha256"].items():
        if file_hash(path) != expected:
            raise ValueError("reviewed input changed: " + path)


def execute_setup(plan):
    check_inputs(plan)
    runtime, destination = Path(plan["runtime"]), Path(plan["evidence"])
    if runtime.exists() or destination.exists():
        raise ValueError("fresh setup paths changed")
    destination.mkdir(parents=True)
    retain(destination / "actions.txt", plan)
    result = {"complete":False,"runtime_qualified":False}
    try:
        for index, argv in enumerate(plan["commands"]):
            folder = destination / ("command-" + str(index))
            folder.mkdir()
            child = subprocess.run(argv, cwd=plan["cwd"], capture_output=True, timeout=120)
            retain(folder / "command.json", {"argv":argv, "exit_status":child.returncode})
            (folder / "stdout.txt").write_bytes(child.stdout)
            (folder / "stderr.txt").write_bytes(child.stderr)
            if child.returncode:
                raise ValueError("offline setup failed; retain partial owned runtime")
            if index == 2:
                identity = decode(child.stdout)
                if (identity.get("passed") is not True or identity.get("harness_version") != "0.16.0" or
                    identity.get("python_version") != "3.14.6" or identity.get("python_executable") != plan["runtime_python"] or
                    identity.get("expected_root") != plan["runtime"] or identity.get("evaluator_payload_sha256") != prior.PAYLOAD_SHA or
                    identity.get("evaluator_archive_sha256") != prior.WHEEL_SHA):
                    raise ValueError("actual owned identity differs")
            if index == 3:
                checks = decode(child.stdout).get("checks")
                if not checks or any(row.get("passed") is not True for row in checks):
                    raise ValueError("ordinary doctor failed before instrumentation")
        source, target = Path(plan["fault_source"]), ordinary(plan["fault_destination"])
        with target.open("xb") as stream:
            stream.write(source.read_bytes())
        record = {"schema":"verity-c10-c11-runtime-v1", "runtime":str(runtime), "runtime_qualified":False,
            "wheel_sha256":prior.WHEEL_SHA, "source_sha256":file_hash(source), "files":inventory(runtime)}
        retain(runtime / RECORD, record)
        result.update(complete=True, runtime_record_sha256=file_hash(runtime / RECORD))
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)
    retain(destination / "observations.json", result)
    return 0 if result["complete"] else 1


def restore(binding, original, selected, config_path, config_raw, intent):
    result = {"binding_restored":False,"fault_config_removed":False}
    try:
        current = ordinary(binding, file=True).read_bytes()
        if current == selected and intent.get("binding_started") and not intent.get("binding_rejected"):
            replace_binding(binding, selected, original, "binding.c10-c11.tmp")
        elif current != original:
            raise ValueError("binding drift preserved; no overwrite")
        result["binding_restored"] = binding.read_bytes() == original
    except BaseException as error:
        result["binding_restoration_error"] = type(error).__name__ + ": " + str(error)
    try:
        if config_path.exists():
            if not intent.get("config_write_started") or intent.get("config_create_rejected") or ordinary(config_path, file=True).read_bytes() != config_raw:
                raise ValueError("unattributed config drift preserved")
            config_path.unlink()
        result["fault_config_removed"] = not config_path.exists()
    except BaseException as error:
        result["fault_config_cleanup_error"] = type(error).__name__ + ": " + str(error)
    return result


def assess(plan, native, transcript, marker, output=None):
    config = plan["fault_config"]
    exact_fault = (marker.get("config_sha256") == plan["fault_config_sha256"] and
        fault.selected(config, marker.get("argv"), marker.get("python"), marker.get("prefix"), marker.get("cwd"), marker.get("plugin_root"), marker.get("plugin_data")) and
        marker.get("case") == plan["case"] and marker.get("dispatcher_source_executed") is False and
        marker.get("shared_handler_started") is False and marker.get("role") == "pre-tool-dispatcher")
    raw = bytes.fromhex(marker["input_hex"])
    event = decode(raw)
    exact_fault = (exact_fault and len(raw) <= 65536 and digest(raw) == marker.get("input_sha256") and
        event == marker.get("native_input") and config["one_edit_plan"] == plan["one_edit_plan"] and
        digest(encoded(config["one_edit_plan"])) == plan["one_edit_plan_sha256"] and fault.patch_matches(config, event) and
        event.get("hook_event_name") == "PreToolUse" and event.get("tool_name") == "apply_patch" and
        Path(event.get("cwd", "")) == Path(plan["repo"]))
    receipts = [row for row in transcript if "received_monotonic" in row and row.get("message", {}).get("method") == "hook/completed"]
    tools = [row for row in receipts if row["message"].get("params", {}).get("run", {}).get("eventName") == "preToolUse" and
        row["message"]["params"].get("threadId") == native.get("thread_id") and row["message"]["params"].get("turnId") == native.get("turn_id")]
    session_rows = [row for row in receipts if row["message"].get("params", {}).get("run", {}).get("eventName") == "sessionStart" and
        row["message"]["params"].get("threadId") == native.get("thread_id")]
    sessions = [row["message"]["params"]["run"] for row in session_rows]
    body = base64.b64decode(plan["expected_governance_body_base64"])
    end = b"END VERIFIED GOVERNANCE " + plan["expected_governance_body_sha256"].encode() + b"; complete context delivered.\n"
    context_ready = len(sessions) == 1 and sessions[0].get("status") == "completed" and any(
        body in entry.get("text", "").encode("utf8") and entry.get("text", "").encode("utf8").endswith(end)
        for entry in sessions[0].get("entries", []) if entry.get("kind") == "context")
    run = tools[0]["message"]["params"]["run"] if len(tools) == 1 else {}
    source = str(Path(plan["plugin_root"]) / "hooks/hooks.json")
    native_receipt = len(tools) == 1 and run.get("sourcePath") == source and run.get("status") in ("completed", "failed", "blocked", "stopped")
    starts = [row for row in transcript if "received_monotonic" in row and row.get("message", {}).get("method") == "hook/started" and
        row["message"].get("params", {}).get("threadId") == native.get("thread_id") and
        row["message"]["params"].get("turnId") == native.get("turn_id") and
        row["message"]["params"].get("run", {}).get("id") == run.get("id") and
        row["message"]["params"].get("run", {}).get("eventName") == "preToolUse" and
        row["message"]["params"].get("run", {}).get("sourcePath") == source]
    interval = tools[0]["received_monotonic"] - starts[0]["received_monotonic"] if len(tools) == len(starts) == 1 else None
    ordered = (bool(run.get("id")) and len(starts) == len(tools) == len(session_rows) == 1 and
        sessions[0].get("sourcePath") == source and session_rows[0]["received_monotonic"] < starts[0]["received_monotonic"] <=
        marker.get("started_monotonic", -1) <= tools[0]["received_monotonic"])
    timeout_reported = any("timeout" in entry.get("text", "").lower() or "timed out" in entry.get("text", "").lower() for entry in run.get("entries", []))
    if plan["case"] == "hang":
        mode_observed = timeout_reported and run.get("durationMs", 0) >= 30000 and interval is not None and interval >= 30
    else:
        expected = fault.output_bytes(plan["case"])
        mode_observed = (bool(output) and output.get("stdout_hex") == expected.hex() and output.get("stdout_sha256") == digest(expected) and
            output.get("exit_status") == 0 and len(tools) == 1 and marker.get("started_monotonic", -1) <=
            output.get("finished_monotonic", -1) <= tools[0]["received_monotonic"])
    before, after = plan["targets_before_sha256"], native.get("after")
    effects_bounded = native.get("before") == before and after in (before, plan["targets_expected_after_sha256"])
    effect_count = int(after == plan["targets_expected_after_sha256"]) if effects_bounded else None
    completed_updates = [row for row in transcript if "received_monotonic" in row and row.get("message", {}).get("method") == "item/completed" and
        row["message"].get("params", {}).get("threadId") == native.get("thread_id") and row["message"]["params"].get("turnId") == native.get("turn_id") and
        row["message"]["params"].get("item", {}).get("type") == "fileChange" and row["message"]["params"]["item"].get("status") == "completed"]
    if effect_count == 1:
        effects_bounded = (native.get("acceptance_sent") is True and native.get("completed_file_change_items") == 1 and
            len(completed_updates) == len(tools) == 1 and tools[0]["received_monotonic"] <= native.get("acceptance_sent_monotonic", -1) <= completed_updates[0]["received_monotonic"])
    elif effect_count == 0:
        effects_bounded = native.get("acceptance_sent") is False and native.get("completed_file_change_items") == 0 and not completed_updates
    hash_effect_count = effect_count
    effect_count = effect_count if effects_bounded else None
    blocking_control = native_receipt and run.get("status") == "blocked" and native.get("native_hook_blocked") is True and effect_count == 0
    allowed_stop = (native.get("observation_complete") is True and native.get("observer_stopped") is None) or (
        native.get("observation_complete") is False and native.get("observer_stopped") == "turn ended without a complete correlated native file-change item")
    complete = (exact_fault and native_receipt and ordered and mode_observed and context_ready and effects_bounded and allowed_stop and
        native.get("readers_complete") is True and native.get("cleanup", {}).get("active_processes") == 0 and
        native.get("cleanup", {}).get("descendant_cleanup_unconfirmed") is not True and
        not any(native.get(name) for name in ("cleanup_error", "late_stop", "snapshot_error", "dispatch_capture_error")))
    return {"observation_complete":bool(complete), "runtime_qualified":False, "exact_fault_observed":bool(exact_fault),
        "native_receipt":run, "native_timeout_reported":timeout_reported, "fault_mode_observed":bool(mode_observed),
        "ordered_native_and_fault_events":bool(ordered), "observed_hook_interval_seconds":interval,
        "native_completed_update_count":native.get("completed_file_change_items"), "native_acceptance_sent":native.get("acceptance_sent"),
        "full_session_context":context_ready, "effects_bounded":effects_bounded, "actual_effect_count":effect_count,
        "hash_derived_effect_count":hash_effect_count,
        "native_blocking_control_observed":bool(blocking_control),
        "supported_handler_denial_observed":False, "required_native_refusal_observed":False,
        "enforcement_result":"unqualified: no supported handler refusal observed",
        "limits":"Fault completion is distinct from host acceptance and from actual target effects. Observer cancellation never substitutes for hook refusal."}


def final_gates(outcome, plan):
    return (outcome.get("observation_complete") is True and outcome.get("outer_cleanup", {}).get("active_processes") == 0 and
        outcome.get("outer_cleanup", {}).get("descendant_cleanup_unconfirmed") is not True and
        outcome.get("binding_restored") is True and outcome.get("fault_config_removed") is True and
        outcome.get("runtime_inventory_restored") is True and outcome.get("profile_config_unchanged") is True and
        outcome.get("targets_after_sha256") == outcome.get("native_after_sha256") and
        outcome.get("targets_after_sha256") in (plan["targets_before_sha256"], plan["targets_expected_after_sha256"]) and
        outcome.get("natural_fault_return") is False and
        not any(outcome.get(name) for name in ("error", "cleanup_error", "binding_restoration_error", "fault_config_cleanup_error", "capture_or_assessment_error")))


def execute_run(plan):
    from processes import spawn, stop_owned_tree
    check_inputs(plan)
    runtime, destination = Path(plan["runtime"]), Path(plan["evidence"])
    binding, config_path = Path(plan["binding_path"]), Path(plan["fault_config_path"])
    original = base64.b64decode(plan["binding_before_base64"], validate=True)
    selected, config_raw = encoded(plan["selected_binding"]), encoded(plan["fault_config"])
    if (destination.exists() or config_path.exists() or binding.read_bytes() != original or
        file_hash(runtime / RECORD) != plan["runtime_record_sha256"] or read(runtime / RECORD)["files"] != inventory(runtime)):
        raise ValueError("reviewed binding/runtime/destination changed")
    for name, expected in plan["targets_before_sha256"].items():
        if digest(edit.ordinary_file(Path(plan["repo"])/name)) != expected:
            raise ValueError("independent target snapshot changed")
    destination.mkdir(parents=True)
    retain(destination / "actions.txt", plan)
    retain(destination / "binding-before.raw.json", {"encoding":"base64", "bytes":plan["binding_before_base64"], "sha256":plan["binding_before_sha256"]})
    (destination / "one-edit-plan.json").write_bytes(encoded(plan["one_edit_plan"]))
    markers, process, intent = Path(plan["marker_directory"]), None, {}
    outcome = {"observation_complete":False,"runtime_qualified":False,"case":plan["case"],"started_monotonic":time.monotonic()}
    try:
        markers.mkdir()
        prior.write_fault_config(config_path, config_raw, intent)
        intent["binding_started"] = True
        try:
            replace_binding(binding, original, selected, "binding.c10-c11.tmp")
        except ValueError:
            intent["binding_rejected"] = True
            raise
        with (destination / "stdout.txt").open("xb") as stdout, (destination / "stderr.txt").open("xb") as stderr:
            process = spawn(plan["observer_argv"], cwd=Path(plan["repo"]).parent, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr)
            deadline = time.monotonic() + edit.DEADLINE_SECONDS + 15
            while process.poll() is None:
                if time.monotonic() >= deadline or Path(plan["stop_marker"]).exists():
                    raise TimeoutError("outer observation deadline/stop; not native hook refusal")
                time.sleep(.025)
            outcome["observer_exit_status"] = process.returncode
    except BaseException as error:
        outcome["error"] = type(error).__name__ + ": " + str(error)
    finally:
        if process is not None:
            try:
                outcome["outer_cleanup"] = stop_owned_tree(process)
            except BaseException as error:
                outcome["cleanup_error"] = type(error).__name__ + ": " + str(error)
        outcome.update(restore(binding, original, selected, config_path, config_raw, intent))
        try:
            outcome["runtime_inventory_restored"] = read(runtime / RECORD)["files"] == inventory(runtime)
            outcome["profile_config_after_sha256"] = file_hash(plan["profile_config_path"])
            outcome["profile_config_unchanged"] = outcome["profile_config_after_sha256"] == plan["profile_config_sha256"]
            outcome["targets_after_sha256"] = {name:digest(edit.ordinary_file(Path(plan["repo"])/name)) for name in edit.TARGETS}
            for name in ("dispatcher.json", "output.json", "natural-timeout.json", "rejected-input.json"):
                if (markers/name).is_file():
                    retain(destination/name, read(markers/name))
            if "error" not in outcome:
                native = read(destination/"live/observations.json")
                outcome["native_after_sha256"] = native.get("after")
                outcome["assessment"] = assess(plan, native, read(destination/"live/transcript.json"),
                    read(destination/"dispatcher.json"), read(destination/"output.json") if plan["case"] != "hang" else None)
                outcome["observation_complete"] = outcome["assessment"]["observation_complete"]
            outcome["natural_fault_return"] = (destination/"natural-timeout.json").exists()
            outcome["observation_complete"] = final_gates(outcome, plan)
        except BaseException as error:
            outcome["capture_or_assessment_error"] = type(error).__name__ + ": " + str(error)
            outcome["observation_complete"] = False
        outcome["finished_monotonic"] = time.monotonic()
        outcome["conclusion"] = (outcome.get("assessment", {}).get("enforcement_result", "unavailable; no refusal/effect inference")
            if outcome["observation_complete"] else "unavailable; no refusal/effect inference")
        retain(destination / "observations.json", outcome)
    # Zero means the negative observation is complete, never that the route passed.
    return 0 if outcome["observation_complete"] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "run"))
    parser.add_argument("--case", choices=fault.MODES)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--approved-plan-sha256")
    args = parser.parse_args()
    try:
        if args.action == "setup" and args.case:
            raise ValueError("setup does not select an active fault")
        plan = setup_plan(args.evidence.absolute()) if args.action == "setup" else run_plan(args.case, args.evidence.absolute())
        plan_sha = digest(encoded(plan))
        if not args.execute:
            print(json.dumps({"mode":"preflight only; no fixture or process change", "plan_sha256":plan_sha, "plan":plan},indent=2))
            return 0
        if args.approved_plan_sha256 != plan_sha:
            raise ValueError("exact separately reviewed plan hash required")
        return execute_setup(plan) if args.action == "setup" else execute_run(plan)
    except (ValueError, OSError, KeyError, edit.Stop) as error:
        print(json.dumps({"preflight_failed":str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
