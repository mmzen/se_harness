"""C11 lost active PreToolUse binding across a fresh native host/session.

Default is a pure preview. Execution requires the exact independently reviewed
plan hash. Ready activation precedes one native enabled=false setting; the
original trust hashes, inline commands, package, runtime and edit gate stay intact.
This is neither same-process hot reload nor literal guard-file/shell deletion.
"""
import argparse
import base64
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import tomllib

HERE = Path(__file__).absolute().parent
sys.path.insert(0, str(HERE))
import c05_runner as prior
import edit_observer as edit
import fixture
import observer
from c08_runner import ordinary, file_hash, digest, encoded, read_json, replace_binding

PLUGIN, SESSION_KEY, TOOL_KEY, TRUST = prior.PLUGIN, prior.SESSION_KEY, prior.TOOL_KEY, prior.TRUST
NORMAL_VALIDATOR = observer.active_bindings
PHASES = ("ready", "lost", "restored")
AFTER = "WO-PLG-005 C11 lost active binding effect\n"
LIMIT = ("Binding disappearance across a fresh host/session after proven readiness; "
         "not same-process hot reload, literal guard-file deletion or OS shell-start failure. "
         "The missing required binding is unqualified regardless of target effects.")


def disable_pre_tool(raw):
    """Preserve owner bytes and change only the exact native PreToolUse flag."""
    original = tomllib.loads(raw.decode("utf-8-sig"))
    for key, trusted in TRUST.items():
        item = original.get("hooks", {}).get("state", {}).get(key, {})
        if item.get("trusted_hash") != trusted or item.get("enabled", True) is not True:
            raise ValueError("both original hooks must be enabled with pinned trust hashes")
    lines = raw.splitlines(keepends=True)
    header = ('[hooks.state."' + TOOL_KEY + '"]').encode()
    indices = [i for i, line in enumerate(lines) if line.rstrip(b"\r\n") == header]
    if len(indices) != 1 or not lines[indices[0]].endswith(b"\n"):
        raise ValueError("one exact native PreToolUse table header with line ending required")
    start = indices[0]
    end = next((i for i in range(start + 1, len(lines)) if lines[i].lstrip().startswith(b"[")), len(lines))
    enabled = [i for i in range(start + 1, end) if re.match(rb"\s*enabled\s*=", lines[i])]
    if len(enabled) > 1:
        raise ValueError("ambiguous enabled setting")
    if enabled:
        index = enabled[0]
        lines[index], count = re.subn(rb"^(\s*enabled\s*=\s*)true(\s*(?:#.*)?(?:\r?\n)?)$", rb"\g<1>false\g<2>", lines[index])
        if count != 1:
            raise ValueError("unsupported enabled spelling")
    else:
        lines.insert(start + 1, b"enabled = false" + (b"\r\n" if lines[start].endswith(b"\r\n") else b"\n"))
    selected = b"".join(lines)
    expected = copy.deepcopy(original)
    expected["hooks"]["state"][TOOL_KEY]["enabled"] = False
    if tomllib.loads(selected.decode("utf-8-sig")) != expected:
        raise ValueError("config changed beyond the selected enabled flag")
    return selected


def paths():
    return prior.paths()


def build_plan(destination, package_path, context=None):
    context = context or paths()
    destination, package_path = ordinary(destination), ordinary(package_path, file=True)
    allowed = context["root"] / "docs/engineering/plugin-integration/evidence/WO-PLG-005/C11"
    if allowed not in destination.parents or destination.exists():
        raise ValueError("fresh C11 evidence directory required")
    config = ordinary(context["config"], file=True)
    original = config.read_bytes()
    selected = disable_pre_tool(original)
    for name in ("config.c11-disabled.tmp", "config.c11-restored.tmp"):
        if ordinary(config.with_name(name)).exists():
            raise ValueError("prior C11 config transaction remains; inspect before retry")
    if read_json(context["binding"]) != fixture.binding(context["repo"], context["runner_python"].parent.parent):
        raise ValueError("ordinary accepted shared016 binding required, with no fault runtime")
    package = read_json(package_path)
    hooks = context["root"] / "plugins/verity-plane/codex/hooks/hooks.json"
    dispatch = hooks.parent.parent / "dispatch.py"
    if (package.get("archive_sha256") != prior.boundary.PACKAGE_SHA or
            package["payload"].get("hooks/hooks.json") != file_hash(hooks) or
            package["payload"].get("scripts/codex-dispatch.py") != file_hash(dispatch)):
        raise ValueError("exact checked current package04 required")
    single = edit.Plan(context["repo"], {"schema":"verity-one-edit-v1", "target":"governed-target.txt",
        "before_utf8":edit.ordinary_file(context["repo"] / "governed-target.txt").decode("utf8"), "after_utf8":AFTER})
    single.read_before()
    stop = ordinary(context["repo"].parent / ("STOP-C11-binding-" + digest(str(destination).encode())[:16]))
    if stop.exists():
        raise ValueError("fresh external stop marker required")
    agents = ordinary(context["repo"] / "AGENTS.md", file=True).read_bytes()
    begin, end = b"<!-- se-harness:begin -->", b"<!-- se-harness:end -->"
    if agents.count(begin) != 1 or agents.count(end) != 1 or agents.index(begin) >= agents.index(end):
        raise ValueError("one exact managed gate required")
    body = (b"AGENTS.md managed gate:\n" + agents[agents.index(begin):agents.index(end) + len(end)] +
            b"\n\nENGINEERING_HARNESS.md:\n" + ordinary(context["repo"] / "ENGINEERING_HARNESS.md", file=True).read_bytes())
    inputs = [*prior.boundary.source_paths(context), Path(prior.__file__), Path(__file__), Path(edit.__file__),
              package_path, hooks, dispatch, context["binding"], context["runner_python"], context["host"], context["schema"],
              *[context["schema"].parent / name for name in edit.SCHEMA_PINS],
              context["root"] / "docs/engineering/plugin-integration/evidence/WO-PLG-005/preparation/accepted-profile/identity.json",
              context["root"] / "docs/engineering/plugin-integration/evidence/WO-PLG-005/C02/startup-01/transcript.json",
              *[context["repo"] / name for name in ("AGENTS.md", "ENGINEERING_HARNESS.md", ".engineering-harness.lock", ".engineering-harness.toml")]]
    return {"schema":"verity-c11-binding-loss-plan-v1", "evidence":str(destination), "config_path":str(config),
        "config_before_base64":base64.b64encode(original).decode(), "config_before_sha256":digest(original),
        "config_disabled_base64":base64.b64encode(selected).decode(), "config_disabled_sha256":digest(selected),
        "config_change":{"key":TOOL_KEY, "enabled":False, "trusted_hash_unchanged":TRUST[TOOL_KEY]},
        "fixed_input_sha256":{str(path):file_hash(path) for path in inputs},
        "repo":str(context["repo"]), "cache":str(ordinary(context["cache"])), "hooks_path":str(hooks), "hooks_sha256":file_hash(hooks),
        "package_record":str(package_path), "package_record_sha256":file_hash(package_path), "package_payload":package["payload"],
        "python":str(context["runner_python"]), "observer_script":str(Path(__file__)), "stop_marker":str(stop),
        "targets_before_sha256":{name:digest(edit.ordinary_file(context["repo"] / name)) for name in edit.TARGETS},
        "one_edit_plan":single.value, "one_edit_plan_sha256":digest(encoded(single.value)), "prompt":single.prompt(),
        "ready_prompt":prior.PROMPT, "expected_governance_body_base64":base64.b64encode(body).decode(),
        "expected_governance_body_sha256":digest(body), "ordinary_profile":"read-only/on-request; unchanged exact one-edit approval gate",
        "sequence":["ready native activation and owned cleanup", "disable only PreToolUse", "fresh native one-edit activation and owned cleanup",
                    "restore exact original config", "fresh active native inventory only"],
        "limits":LIMIT, "literal_os_shell_start_failure":{"status":"unavailable",
            "reason":"Owned C09 shell captures show an absolute system PowerShell executable. No safe accepted-route OS launch-failure injection was demonstrated; a synthetic exit127 would not prove OS launch failure."}}


def inactive_bindings(response, repo, cache, definitions, hooks_sha256):
    selected = [hook for group in response.get("result", {}).get("data", []) for hook in group.get("hooks", []) if hook.get("pluginId") == PLUGIN]
    for event, key, enabled in (("sessionStart", SESSION_KEY, True), ("preToolUse", TOOL_KEY, False)):
        matching = [hook for hook in selected if hook.get("eventName") == event]
        if len(matching) != 1 or any(matching[0].get(field) != value for field, value in
                (("key",key), ("trustStatus","trusted"), ("currentHash",TRUST[key]))) or matching[0].get("enabled") is not enabled:
            raise observer.ObservationStopped("actual C11 native enabled/trust/currentHash differs from plan")
    try:
        NORMAL_VALIDATOR(response, repo, cache, definitions, hooks_sha256)
    except observer.ObservationStopped as error:
        rejection = str(error)
    else:
        raise observer.ObservationStopped("normal validator unexpectedly accepted missing active PreToolUse")
    comparison = copy.deepcopy(response)
    for group in comparison["result"]["data"]:
        for hook in group["hooks"]:
            if hook.get("key") == TOOL_KEY:
                hook["enabled"] = True
    checked = NORMAL_VALIDATOR(comparison, repo, cache, definitions, hooks_sha256)
    actual = [{**hook, "enabled":False} if hook["key"] == TOOL_KEY else hook for hook in checked]
    return actual, {"normal_validator_rejected":rejection, "qualified":False,
        "comparison_only":"Only copied PreToolUse enabled set true for remaining validation. Original hooks/list, trust/currentHash, command/payload and returned disabled entry remain actual.",
        "actual_session_start_enabled":True, "actual_pre_tool_use_enabled":False}


def target_snapshot(plan):
    return {name:digest(edit.ordinary_file(Path(plan["repo"]) / name)) for name in edit.TARGETS}


def check_inputs(plan, phase):
    if phase not in PHASES:
        raise ValueError("unknown phase")
    for path, expected in plan["fixed_input_sha256"].items():
        if file_hash(path) != expected:
            raise ValueError("fixed input changed after review: " + path)
    if file_hash(plan["config_path"]) != plan["config_disabled_sha256" if phase == "lost" else "config_before_sha256"]:
        raise ValueError("native config differs from the planned phase")
    if phase != "restored" and target_snapshot(plan) != plan["targets_before_sha256"]:
        raise ValueError("target changed before the one authorized edit")
    if phase == "restored":
        # The exact observed target effect is retained, never silently reset.
        observed_after = read_json(Path(plan["evidence"]) / "lost/observations.json")["after"]
        if target_snapshot(plan) != observed_after:
            raise ValueError("target drift since lost-binding observation")
    if Path(plan["stop_marker"]).exists():
        raise ValueError("operator stop marker exists")


def observe(plan, phase):
    expected = paths()
    if (expected["root"] / "docs/engineering/plugin-integration/evidence/WO-PLG-005/C11" not in ordinary(plan["evidence"]).parents or
            any(Path(plan[key]) != expected[name] for key, name in (("config_path","config"), ("repo","repo"), ("cache","cache"), ("python","runner_python"))) or
            Path(plan["observer_script"]) != Path(__file__) or Path(plan["stop_marker"]).parent != expected["repo"].parent):
        raise ValueError("private plan leaves exact accepted disposable paths")
    check_inputs(plan, phase)
    destination = Path(plan["evidence"]) / phase
    if phase == "lost":
        edit_path = Path(plan["evidence"]) / "one-edit-plan.json"
        if file_hash(edit_path) != plan["one_edit_plan_sha256"] or read_json(edit_path) != plan["one_edit_plan"]:
            raise ValueError("exact reviewed edit plan changed")
        normal, validation = observer.active_bindings, []
        def validate(*args):
            actual, record = inactive_bindings(*args)
            validation.append(record)
            return actual
        try:
            observer.active_bindings = validate
            return edit.main(["--plan",str(edit_path), "--approved-plan-sha256",plan["one_edit_plan_sha256"],
                "--package-record",plan["package_record"], "--evidence",str(destination), "--stop-marker",plan["stop_marker"], "--run"])
        finally:
            observer.active_bindings = normal
            if destination.is_dir():
                (destination / "c11-comparison.json").write_bytes(encoded({"phase":phase, "checks":validation, "plan_sha256":digest(encoded(plan))}))
    import live
    original_argv = sys.argv
    try:
        sys.argv = [str(Path(live.__file__)), "--evidence",str(destination), "--package-record",plan["package_record"]]
        if phase == "restored":
            sys.argv.append("--inventory-only")
        live.main()
        return 0
    finally:
        sys.argv = original_argv


def startup_context(plan, observed, transcript, dispatch):
    """Require the actual correlated complete native context, not diagnostic text."""
    thread = observed["thread_id"]
    starts, completions = [], []
    for i, row in enumerate(transcript):
        message, params = row["message"], row["message"].get("params", {})
        if "received_monotonic" not in row or params.get("threadId") != thread or params.get("run", {}).get("eventName") != "sessionStart":
            continue
        if message.get("method") == "hook/started":
            starts.append((i, row))
        elif message.get("method") == "hook/completed":
            completions.append((i, row))
    if len(starts) != 1 or len(completions) != 1:
        raise ValueError("one actual startup hook sequence required")
    a, first = starts[0]; b, last = completions[0]
    start, finish = first["message"]["params"], last["message"]["params"]
    run = finish["run"]
    if (a >= b or start.get("turnId") != finish.get("turnId") or start["run"].get("id") != run.get("id") or
            run.get("status") != "completed" or run.get("executionMode") != "sync"):
        raise ValueError("startup completion is not the correlated synchronous receipt")
    body = base64.b64decode(plan["expected_governance_body_base64"], validate=True).decode("utf8")
    contexts = [item.get("text") for item in run.get("entries", []) if item.get("kind") == "context"]
    ending = "END VERIFIED GOVERNANCE " + plan["expected_governance_body_sha256"] + "; complete context delivered."
    sessions = [row for row in dispatch if len(row.get("argv", [])) > 3 and
                Path(row["argv"][3]) == Path(observed["loaded_payload"]["root"]) / "scripts/session-context.py"]
    if len(sessions) != 1:
        raise ValueError("one actual SessionStart dispatcher record required")
    response = json.loads(sessions[0]["stdout"])["hookSpecificOutput"]
    if (len(contexts) != 1 or not isinstance(contexts[0], str) or body not in contexts[0] or ending not in contexts[0] or
            response.get("hookEventName") != "SessionStart" or response.get("additionalContext") != contexts[0] or sessions[0].get("exit_status") != 0):
        raise ValueError("full native startup bytes do not match successful shared context")
    return {"context_sha256":digest(contexts[0].encode()), "context_bytes":len(contexts[0].encode()),
            "received_monotonic":last["received_monotonic"], "thread_id":thread, "turn_id":finish.get("turnId"), "receipt_index":b}


def replay_edit(plan, observed, transcript):
    """Read-only replay; the actual observer's approval implementation is unchanged."""
    gate = edit.EditGate(edit.Plan(plan["repo"], plan["one_edit_plan"]))
    gate.thread, gate.turn, gate.turn_requested = observed["thread_id"], observed["turn_id"], True
    approvals = []
    for row in transcript:
        message = row["message"]
        if "received_monotonic" in row:
            gate.observe(message)
        elif "sent_monotonic" in row and "result" in message:
            if gate.pending is None or message != {"id":gate.pending["id"], "result":{"decision":"accept"}}:
                raise ValueError("sent approval differs from the exact pending one-edit request")
            gate.validate_changes(gate.changes)
            approvals.append(message)
            # Replay only: no read_before() on the now changed target, no output.
            gate.accepted, gate.pending = True, None
    if not gate.done or not gate.item_done or gate.pending or len(approvals) != 1 or gate.completed_file_items != 1:
        raise ValueError("complete correlated one-edit effect was not observed; absence is not refusal")
    after = dict(plan["targets_before_sha256"])
    after[plan["one_edit_plan"]["target"]] = digest(gate.plan.after)
    if (observed.get("before") != plan["targets_before_sha256"] or observed.get("after") != after or
            observed.get("acceptance_sent") is not True or observed.get("completed_file_change_items") != 1 or
            observed.get("target_actual_sha256") != digest(gate.plan.after)):
        raise ValueError("native edit receipt and independent target hashes disagree")
    return {"observed_completed_native_file_changes":1, "exact_target_sha256":digest(gate.plan.after),
            "targets_after_sha256":after, "hook_refusal_observed":False, "enforcement":"failed; exact effect occurred without active PreToolUse", "qualified":False}


def native_result(plan, phase):
    folder = Path(plan["evidence"]) / phase
    observed, transcript = read_json(folder / "observations.json"), read_json(folder / "transcript.json")
    if (observed.get("readers_complete") is not True or observed.get("cleanup", {}).get("active_processes") != 0 or
            observed.get("cleanup", {}).get("descendant_cleanup_unconfirmed") is True or observed.get("observer_stopped") or observed.get("cleanup_error")):
        raise ValueError("native observation or owned cleanup incomplete; no effect inference")
    inventories = [row["message"] for row in transcript if "received_monotonic" in row and
                   isinstance(row["message"].get("result", {}).get("data"), list) and
                   any("hooks" in group for group in row["message"]["result"]["data"])]
    if len(inventories) != 1:
        raise ValueError("one native hooks/list response required")
    arguments = (inventories[0], Path(plan["repo"]), Path(plan["cache"]), read_json(plan["hooks_path"]), plan["hooks_sha256"])
    inventory, validation = inactive_bindings(*arguments) if phase == "lost" else (NORMAL_VALIDATOR(*arguments), None)
    if (any(hook.get("currentHash") != TRUST[hook["key"]] for hook in inventory) or
            observed.get("active_bindings") != inventory or observed.get("loaded_payload", {}).get("sha256") != plan["package_payload"] or
            observed.get("package_record_sha256") != plan["package_record_sha256"] or
            {str(Path(hook["sourcePath"]).parent.parent) for hook in inventory} != {observed["loaded_payload"]["root"]}):
        raise ValueError("actual trust/currentHash or loaded package differs from reviewed inputs")
    sent = [row["message"] for row in transcript if "sent_monotonic" in row]
    starts = [row for row in sent if row.get("method") == "thread/start"]
    turns = [row for row in sent if row.get("method") == "turn/start"]
    result = {"phase":phase, "inventory_validation":validation, "cleanup":observed["cleanup"], "payload_matches":True}
    if phase == "restored":
        if starts or turns or observed.get("thread_id") or observed.get("before") != observed.get("after"):
            raise ValueError("restoration must be inventory only, with unchanged targets")
        result["targets_after_sha256"] = {name:value["sha256"] for name,value in observed["after"].items()}
        return {**result, "matches_expected":True}
    if (len(starts) != 1 or len(turns) != 1 or starts[0].get("params") != edit.thread_params(Path(plan["repo"])) or
            turns[0].get("params", {}).get("threadId") != observed.get("thread_id") or
            turns[0]["params"].get("input") != [{"type":"text", "text":plan["prompt"] if phase == "lost" else prior.PROMPT}]):
        raise ValueError("one exact ordinary native thread and authorized prompt required")
    responses = [row["message"] for row in transcript if "received_monotonic" in row and
                 row["message"].get("id") == starts[0].get("id") and "method" not in row["message"]]
    if len(responses) != 1 or edit.check_thread(responses[0]["result"], Path(plan["repo"])) != observed["thread_id"]:
        raise ValueError("actual native thread response is missing or has different permissions")
    if phase == "lost" and responses[0]["result"] != observed["effective_thread"]:
        raise ValueError("retained effective thread differs from actual response")
    dispatch = [json.loads(line) for line in (folder / "dispatch.jsonl").read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    result["startup"] = startup_context(plan, observed, transcript, dispatch)
    if any(row["message"].get("params", {}).get("run", {}).get("eventName") == "preToolUse" for row in transcript if "received_monotonic" in row) or any("--refusal-mode" in row.get("argv", []) for row in dispatch):
        raise ValueError("unexpected before-tool hook invocation in ready-only or disabled phase")
    if phase == "lost":
        if observed.get("observation_complete") is not True:
            raise ValueError("one-edit observation incomplete")
        file_events = [i for i,row in enumerate(transcript) if "received_monotonic" in row and
                       (row["message"].get("params", {}).get("item", {}).get("type") == "fileChange" or
                        row["message"].get("method") == "item/fileChange/requestApproval")]
        if (result["startup"]["turn_id"] != observed["turn_id"] or not file_events or
                result["startup"]["receipt_index"] >= min(file_events)):
            raise ValueError("normal startup must precede the exact one-edit fault attempt")
        result["effect"] = replay_edit(plan, observed, transcript)
    else:
        completions = [row["message"] for row in transcript if "received_monotonic" in row and row["message"].get("method") == "turn/completed"]
        if (len(completions) != 1 or completions[0] != observed.get("turn") or
                completions[0]["params"].get("threadId") != observed["thread_id"] or
                completions[0]["params"]["turn"].get("id") != result["startup"]["turn_id"] or
                completions[0]["params"]["turn"].get("status") != "completed" or completions[0]["params"]["turn"].get("error") is not None or
                observed["before"] != observed["after"] or {name:value["sha256"] for name,value in observed["before"].items()} != plan["targets_before_sha256"] or
                any("id" in row["message"] and "method" in row["message"] for row in transcript if "received_monotonic" in row) or
                any(row["message"].get("params", {}).get("item", {}).get("type") not in (None,"userMessage","agentMessage","reasoning") for row in transcript)):
            raise ValueError("normal ready activation did not complete without tools/effects")
    return {**result, "matches_expected":True}


def invoke(plan, phase):
    from processes import spawn, stop_owned_tree
    destination = Path(plan["evidence"])
    argv = [plan["python"], "-I", "-B", plan["observer_script"], "--observe-phase",phase,
            "--plan",str(destination / "plan.json"), "--run", "--approved-plan-sha256",digest(encoded(plan))]
    result = {"argv":argv, "started_monotonic":time.monotonic()}
    process = None
    try:
        with (destination / (phase + "-stdout.txt")).open("xb") as stdout, (destination / (phase + "-stderr.txt")).open("xb") as stderr:
            process = spawn(argv, cwd=Path(plan["repo"]).parent, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr)
            deadline = time.monotonic() + edit.DEADLINE_SECONDS + 20
            while process.poll() is None:
                if time.monotonic() >= deadline or Path(plan["stop_marker"]).exists():
                    raise TimeoutError("outer deadline/operator stop; not a hook refusal")
                time.sleep(.02)
            result["returncode"] = process.returncode
    except BaseException as error:
        result["error"] = type(error).__name__ + ": " + str(error)
    finally:
        if process is not None:
            try:
                result["outer_cleanup"] = stop_owned_tree(process)
            except BaseException as error:
                result["cleanup_error"] = type(error).__name__ + ": " + str(error)
        result["finished_monotonic"] = time.monotonic()
        (destination / (phase + "-launch.json")).write_bytes(encoded(result))
    return result


def cleanup_confirmed(result):
    return (result.get("outer_cleanup", {}).get("active_processes") == 0 and
            result.get("outer_cleanup", {}).get("descendant_cleanup_unconfirmed") is not True and not result.get("cleanup_error"))


def execute(plan, run_observer=None):
    run_observer = run_observer or invoke
    check_inputs(plan, "ready")
    destination = ordinary(plan["evidence"])
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "plan.json").write_bytes(encoded(plan))
    (destination / "one-edit-plan.json").write_bytes(encoded(plan["one_edit_plan"]))
    (destination / "actions.txt").write_bytes(encoded({"plan_sha256":digest(encoded(plan)), "sequence":plan["sequence"], "limits":LIMIT}))
    original, selected = (base64.b64decode(plan[key], validate=True) for key in ("config_before_base64", "config_disabled_base64"))
    outcome = {"observation_complete":False, "qualified":False, "conclusion":"unavailable", "limits":LIMIT, "phases":{}, "started_monotonic":time.monotonic()}
    intent, safe_cleanup = {}, True
    try:
        safe_cleanup = False
        outcome["phases"]["ready"] = run_observer(plan, "ready")
        safe_cleanup = cleanup_confirmed(outcome["phases"]["ready"])
        outcome["ready_assessment"] = native_result(plan, "ready")
        if not safe_cleanup or outcome["phases"]["ready"].get("returncode") != 0 or outcome["phases"]["ready"].get("error"):
            raise ValueError("ready phase failed; no binding mutation")
        check_inputs(plan, "ready")
        intent["write_started"] = True
        try:
            replace_binding(Path(plan["config_path"]), original, selected, "config.c11-disabled.tmp")
        except ValueError:
            intent["replace_rejected"] = True
            raise
        intent["write_completed"] = True
        outcome["disabled_monotonic"] = time.monotonic()
        outcome["disabled_config_sha256"] = file_hash(plan["config_path"])
        (destination / "fault-setup.json").write_bytes(encoded({"config_sha256":outcome["disabled_config_sha256"], "change":plan["config_change"],
            "disabled_monotonic":outcome["disabled_monotonic"], "prior_ready":outcome["ready_assessment"], "prior_owned_cleanup":outcome["phases"]["ready"]["outer_cleanup"]}))
        safe_cleanup = False
        outcome["phases"]["lost"] = run_observer(plan, "lost")
        safe_cleanup = cleanup_confirmed(outcome["phases"]["lost"])
        outcome["lost_assessment"] = native_result(plan, "lost")
        if not safe_cleanup or outcome["phases"]["lost"].get("returncode") != 0 or outcome["phases"]["lost"].get("error"):
            raise ValueError("lost-binding native observation incomplete")
        a, b = outcome["ready_assessment"]["startup"], outcome["lost_assessment"]["startup"]
        if (a["thread_id"] == b["thread_id"] or not a["received_monotonic"] < outcome["phases"]["ready"]["finished_monotonic"] <=
                outcome["disabled_monotonic"] <= outcome["phases"]["lost"]["started_monotonic"] < b["received_monotonic"]):
            raise ValueError("fresh activation chronology not proven")
        outcome["observation_complete"] = True
    except BaseException as error:
        outcome["error"] = type(error).__name__ + ": " + str(error)
    finally:
        restoration = {"config_restored":False, "inventory_confirmed":False, "write_intent":intent}
        try:
            config = ordinary(plan["config_path"], file=True)
            current = config.read_bytes()
            if current == selected and intent.get("write_started") and not intent.get("replace_rejected"):
                replace_binding(config, selected, original, "config.c11-restored.tmp")
                restoration["reconciled_exact_bytes_after_interrupt"] = not intent.get("write_completed", False)
            elif current != original:
                raise ValueError("config differs from original or attributable selected bytes; preserve for inspection")
            restoration["config_restored"] = config.read_bytes() == original
        except BaseException as error:
            restoration["config_error"] = type(error).__name__ + ": " + str(error)
        if safe_cleanup and restoration["config_restored"] and "lost" in outcome["phases"]:
            try:
                check_inputs(plan, "restored")
                outcome["phases"]["restored"] = run_observer(plan, "restored")
                restoration["assessment"] = native_result(plan, "restored")
                restoration["inventory_confirmed"] = (cleanup_confirmed(outcome["phases"]["restored"]) and
                    outcome["phases"]["restored"].get("returncode") == 0 and not outcome["phases"]["restored"].get("error"))
                restoration["config_restored"] = file_hash(plan["config_path"]) == plan["config_before_sha256"]
            except BaseException as error:
                restoration["inventory_error"] = type(error).__name__ + ": " + str(error)
        else:
            restoration["inventory_not_run"] = "No completed lost observer with confirmed outer cleanup, or exact config not restored."
        try:
            outcome["targets_after_sha256"] = target_snapshot(plan)
            expected_after = outcome.get("lost_assessment", {}).get("effect", {}).get("targets_after_sha256")
            outcome["final_targets_match_observed_effect"] = (outcome["targets_after_sha256"] == expected_after ==
                restoration.get("assessment", {}).get("targets_after_sha256"))
        except BaseException as error:
            outcome["final_snapshot_error"] = str(error)
        restoration["complete"] = restoration["config_restored"] and restoration["inventory_confirmed"]
        outcome["restoration"] = restoration
        outcome["observation_complete"] = (outcome["observation_complete"] and restoration["complete"] and
            outcome.get("final_targets_match_observed_effect") is True and not outcome.get("error"))
        outcome["conclusion"] = "negative-case observation complete; enforcement failed/unqualified" if outcome["observation_complete"] else "unavailable; no refusal or effect inference"
        outcome["finished_monotonic"] = time.monotonic()
        (destination / "observations.json").write_bytes(encoded(outcome))
    return outcome


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--package-record", type=Path)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--approved-plan-sha256")
    parser.add_argument("--observe-phase", choices=PHASES, help=argparse.SUPPRESS)
    parser.add_argument("--plan", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        if args.observe_phase:
            if not args.run or not args.plan or args.evidence or args.package_record:
                raise ValueError("private phase requires exactly one retained reviewed plan")
            plan = read_json(args.plan.absolute())
            if digest(encoded(plan)) != args.approved_plan_sha256:
                raise ValueError("exact reviewed private plan hash required")
            return observe(plan, args.observe_phase)
        if args.plan or not args.evidence or not args.package_record:
            raise ValueError("fresh evidence and exact package record required")
        plan = build_plan(args.evidence.absolute(), args.package_record.absolute())
        plan_sha = digest(encoded(plan))
        if not args.run:
            # ASCII JSON escapes preserve Unicode paths on Windows pipe encodings.
            print(json.dumps({"mode":"preflight-only; no mutation or process", "plan_sha256":plan_sha, "plan":plan}, ensure_ascii=True, indent=2))
            return 0
        if plan_sha != args.approved_plan_sha256:
            raise ValueError("exact independently reviewed current plan hash required")
        return 0 if execute(plan)["observation_complete"] else 1
    except (OSError, ValueError, KeyError, edit.Stop, observer.ObservationStopped) as error:
        print(json.dumps({"preflight_or_observer_failed":str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
