"""C05 inactive SessionStart observation. Default: preflight, no mutation/process.

Only the accepted disposable profile's exact SessionStart enabled flag changes.
The trusted hash, plugin/cache payload, binding and host permissions do not change.
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
import c08_runner as boundary
import fixture
import observer
from c08_runner import ordinary, file_hash, digest, encoded, read_json, replace_binding

PLUGIN = "verity-plane@verity-plane-codex-fixture"
SESSION_KEY = PLUGIN + ":hooks/hooks.json:session_start:0:0"
TOOL_KEY = PLUGIN + ":hooks/hooks.json:pre_tool_use:0:0"
TRUST = {SESSION_KEY:"sha256:3d24ebbb6f1df466e491ac2738c5895b5bef36d63c5ed24be257517d59c56ab3",
         TOOL_KEY:"sha256:f39cf9eac1e46f8bc70dc5b6c60e1ba1b4ce51a15affbc3210a0a70cac8821cb"}
PROMPT = "Reply with READY only. Do not use tools or change files."


def disable_session_start(raw):
    """Change one native TOML table without serializing unrelated owner bytes."""
    original = tomllib.loads(raw.decode("utf-8-sig"))
    state = original.get("hooks", {}).get("state", {})
    for key, trusted in TRUST.items():
        entry = state.get(key)
        if (not isinstance(entry, dict) or entry.get("trusted_hash") != trusted or
                entry.get("enabled", True) is not True):
            raise ValueError("both original candidate hooks must be enabled with their pinned trust hashes")
    header = ('[hooks.state."' + SESSION_KEY + '"]').encode()
    lines = raw.splitlines(keepends=True)
    indices = [i for i, line in enumerate(lines) if line.rstrip(b"\r\n") == header]
    if len(indices) != 1:
        raise ValueError("one exact native SessionStart table header required")
    start = indices[0]
    if not lines[start].endswith(b"\n"):
        raise ValueError("native table header requires its original line ending")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].lstrip().startswith(b"[")), len(lines))
    enabled = [i for i in range(start + 1, end) if re.match(rb"\s*enabled\s*=", lines[i])]
    if len(enabled) > 1:
        raise ValueError("ambiguous enabled setting")
    if enabled:
        index = enabled[0]
        changed, count = re.subn(rb"^(\s*enabled\s*=\s*)true(\s*(?:#.*)?(?:\r?\n)?)$", rb"\g<1>false\g<2>", lines[index])
        if count != 1:
            raise ValueError("unsupported enabled spelling; no config change")
        lines[index] = changed
    else:
        newline = b"\r\n" if lines[start].endswith(b"\r\n") else b"\n"
        lines.insert(start + 1, b"enabled = false" + newline)
    selected = b"".join(lines)
    expected = copy.deepcopy(original)
    expected["hooks"]["state"][SESSION_KEY]["enabled"] = False
    if tomllib.loads(selected.decode("utf-8-sig")) != expected:
        raise ValueError("config transformation changed more than the selected enabled flag")
    return selected


def paths():
    result = boundary.paths()
    result.update(config=fixture.PROFILE / "codex/config.toml", host=fixture.CODEX,
                  schema=fixture.SCHEMAS / "ClientRequest.json",
                  cache=fixture.PROFILE / "codex/plugins/cache/verity-plane-codex-fixture/verity-plane")
    return result


def build_plan(destination, package_path, context=None):
    context = context or paths()
    destination, package_path = ordinary(destination), ordinary(package_path, file=True)
    allowed = context["root"] / "docs/engineering/plugin-integration/evidence/WO-PLG-005/C05"
    if allowed not in destination.parents or destination.exists():
        raise ValueError("fresh C05 evidence directory required")
    config = ordinary(context["config"], file=True)
    original = config.read_bytes()
    selected = disable_session_start(original)
    for name in ("config.c05-disabled.tmp", "config.c05-restored.tmp"):
        if ordinary(config.with_name(name)).exists():
            raise ValueError("prior config transaction temporary exists; inspect recovery first")
    binding = read_json(context["binding"])
    expected_binding = {"schema":"verity-codex-binding-v1", "repo":str(context["repo"]),
        "environment":str(context["runner_python"].parent.parent), "artifact":"WO-PROBE-001", "capture":True,
        "profile":{"host":"0.153.4", "os":"windows", "python":"3.14.6", "evaluator":"0.16.0"},
        "decision":{"id":"DEC-PLG-001", "status":"decided", "option":"prove-supported-route"}}
    if binding != expected_binding:
        raise ValueError("original accepted captured shared-016 binding required")
    package = read_json(package_path)
    if package.get("archive_sha256") != boundary.PACKAGE_SHA:
        raise ValueError("exact checked package04 required")
    hooks = context["root"] / "plugins/verity-plane/codex/hooks/hooks.json"
    dispatch = context["root"] / "plugins/verity-plane/codex/dispatch.py"
    if package["payload"]["hooks/hooks.json"] != file_hash(hooks) or package["payload"]["scripts/codex-dispatch.py"] != file_hash(dispatch):
        raise ValueError("current adapter differs from checked package")
    inputs = [*boundary.source_paths(context), Path(__file__), package_path, hooks, dispatch,
              context["binding"], context["runner_python"], context["host"], context["schema"],
              *[context["repo"] / name for name in ("AGENTS.md", "ENGINEERING_HARNESS.md", ".engineering-harness.lock", ".engineering-harness.toml")]]
    log = ordinary(context["binding"].with_name("observations.jsonl"))
    log_raw = ordinary(log, file=True).read_bytes() if log.exists() else b""
    return {"schema":"verity-c05-plan-v1", "evidence":str(destination), "config_path":str(config),
        "config_before_base64":base64.b64encode(original).decode(), "config_before_sha256":digest(original),
        "config_disabled_base64":base64.b64encode(selected).decode(), "config_disabled_sha256":digest(selected),
        "config_change":{"key":SESSION_KEY, "enabled":False, "trusted_hash_unchanged":TRUST[SESSION_KEY]},
        "fixed_input_sha256":{str(path):file_hash(path) for path in inputs},
        "repo":str(context["repo"]), "cache":str(ordinary(context["cache"])),
        "hooks_path":str(hooks), "hooks_sha256":file_hash(hooks),
        "package_record":str(package_path), "package_record_sha256":file_hash(package_path), "package_payload":package["payload"],
        "python":str(context["runner_python"]), "observer_script":str(Path(__file__)),
        "targets_before_sha256":{name:file_hash(context["repo"] / name) for name in
            ("governed-target.txt", "outside-scope.txt", "café quoted ' target.txt")},
        "dispatch_audit":{"path":str(log), "before_bytes":len(log_raw), "before_sha256":digest(log_raw)},
        "prompt":PROMPT, "ordinary_profile":"read-only/on-request; abort every server request",
        "expected":"actual disabled SessionStart, unchanged trusted PreToolUse, identical loaded payload; no SessionStart receipt or dispatch, no target change; restore exact config then confirm native active inventory",
        "logical_failure_reference":"C08/wrong017 observes identity failure as exit-0 UNREADY; it is not a shared-script nonzero claim."}


def inactive_bindings(response, repo, cache, definitions, hooks_sha256):
    """Validate the real disabled entry before a documented comparison-only copy."""
    groups = response.get("result", {}).get("data", [])
    selected = [hook for group in groups for hook in group.get("hooks", []) if hook.get("pluginId") == PLUGIN]
    session = [hook for hook in selected if hook.get("eventName") == "sessionStart"]
    tool = [hook for hook in selected if hook.get("eventName") == "preToolUse"]
    if len(session) != 1 or len(tool) != 1:
        raise observer.ObservationStopped("C05 requires both unique actual candidate entries")
    for hook, key, enabled in ((session[0], SESSION_KEY, False), (tool[0], TOOL_KEY, True)):
        if (hook.get("key") != key or hook.get("enabled") is not enabled or
                hook.get("trustStatus") != "trusted" or hook.get("currentHash") != TRUST[key]):
            raise observer.ObservationStopped("C05 actual enabled/trust/hash state differs from the exact plan", hook)
    try:
        observer.active_bindings(response, repo, cache, definitions, hooks_sha256)
    except observer.ObservationStopped as error:
        normal_rejection = str(error)
    else:
        raise observer.ObservationStopped("normal validator unexpectedly accepted an inactive required hook")
    comparison = copy.deepcopy(response)
    for group in comparison["result"]["data"]:
        for hook in group["hooks"]:
            if hook.get("key") == SESSION_KEY:
                hook["enabled"] = True
    checked = observer.active_bindings(comparison, repo, cache, definitions, hooks_sha256)
    # Return the actual disabled state. No copied native record replaces evidence.
    checked = [{**hook, "enabled":False} if hook["key"] == SESSION_KEY else hook for hook in checked]
    return checked, {"normal_validator_rejected":normal_rejection,
        "comparison_only":"One copied enabled field was set true solely to reuse all other normal inventory checks; original hooks/list and returned enabled=false remain retained.",
        "actual_session_start_enabled":False, "actual_pre_tool_use_enabled":True}


def check_inputs(plan, phase):
    for path, expected in plan["fixed_input_sha256"].items():
        if file_hash(path) != expected:
            raise ValueError("fixed input changed after preflight: " + path)
    for name, expected in plan["targets_before_sha256"].items():
        if file_hash(Path(plan["repo"]) / name) != expected:
            raise ValueError("target changed after preflight: " + name)
    expected = plan["config_disabled_sha256"] if phase == "disabled" else plan["config_before_sha256"]
    if file_hash(plan["config_path"]) != expected:
        raise ValueError("config differs from the exact planned phase")


def observe(plan, phase):
    """Private child entry: existing native observer, one explicit C05 validator."""
    expected = paths()
    allowed = expected["root"] / "docs/engineering/plugin-integration/evidence/WO-PLG-005/C05"
    if (allowed not in ordinary(plan["evidence"]).parents or
            Path(plan["config_path"]) != expected["config"] or Path(plan["repo"]) != expected["repo"] or
            Path(plan["cache"]) != expected["cache"] or Path(plan["python"]) != expected["runner_python"] or
            Path(plan["observer_script"]) != Path(__file__)):
        raise ValueError("private observer plan leaves the exact accepted disposable paths")
    check_inputs(plan, phase)
    import live
    destination = Path(plan["evidence"]) / phase
    normal_validator = live.active_bindings
    original_argv = sys.argv
    validation = []
    def validate(*args):
        actual, record = inactive_bindings(*args)
        validation.append(record)
        return actual
    try:
        if phase == "disabled":
            live.active_bindings = validate
        sys.argv = [str(Path(live.__file__)), "--evidence", str(destination), "--package-record", plan["package_record"]]
        if phase == "restored":
            sys.argv.append("--inventory-only")
        live.main()
    finally:
        live.active_bindings = normal_validator
        sys.argv = original_argv
        if destination.is_dir():
            (destination / "c05-comparison.json").write_bytes(encoded({"phase":phase, "checks":validation,
                "runner_sha256":file_hash(Path(__file__)), "plan_sha256":digest(encoded(plan))}))


def native_result(plan, phase):
    folder = Path(plan["evidence"]) / phase
    observed = read_json(folder / "observations.json")
    transcript = read_json(folder / "transcript.json")
    definitions = read_json(plan["hooks_path"])
    arguments = (observed["hooks"], Path(plan["repo"]), Path(plan["cache"]), definitions, plan["hooks_sha256"])
    if phase == "disabled":
        inventory, validation = inactive_bindings(*arguments)
    else:
        inventory = validation = observer.active_bindings(*arguments)
    if phase == "restored" and any(hook.get("currentHash") != TRUST.get(hook.get("key")) for hook in inventory):
        raise observer.ObservationStopped("restored native trust hash differs from the original accepted binding")
    requests = [row for row in transcript if "received_monotonic" in row and
                "id" in row.get("message", {}) and "method" in row["message"]]
    session_receipts = [row for row in transcript if "received_monotonic" in row and
        row.get("message", {}).get("method") in ("hook/started", "hook/completed") and
        row["message"].get("params", {}).get("run", {}).get("eventName") == "sessionStart"]
    sent = [row["message"] for row in transcript if "sent_monotonic" in row]
    starts = [row for row in sent if row.get("method") == "thread/start"]
    turns = [row for row in sent if row.get("method") == "turn/start"]
    target_match = (observed["before"] == observed["after"] and
        {name:value["sha256"] for name, value in observed["before"].items()} == plan["targets_before_sha256"])
    capture = folder / "dispatch.jsonl"
    dispatch = capture.read_bytes() if capture.exists() else b""
    log = Path(plan["dispatch_audit"]["path"])
    log_raw = ordinary(log, file=True).read_bytes() if log.exists() else b""
    audit_matches = len(log_raw) == plan["dispatch_audit"]["before_bytes"] and digest(log_raw) == plan["dispatch_audit"]["before_sha256"]
    payload_matches = (observed.get("loaded_payload", {}).get("sha256") == plan["package_payload"] and
                       observed.get("package_record_sha256") == plan["package_record_sha256"] and
                       {str(Path(hook["sourcePath"]).parent.parent) for hook in inventory} == {observed.get("loaded_payload", {}).get("root")})
    completed = (observed.get("turn") or {}).get("params", {}).get("turn", {})
    completions = [row["message"] for row in transcript if "received_monotonic" in row and
        row.get("message", {}).get("method") == "turn/completed" and
        row["message"].get("params", {}).get("threadId") == observed.get("thread_id")]
    tool_items = [row for row in transcript if row.get("message", {}).get("method") in ("item/started", "item/completed") and
        row["message"].get("params", {}).get("item", {}).get("type") not in ("userMessage", "agentMessage", "reasoning")]
    if phase == "disabled":
        phase_matches = (len(starts) == len(turns) == 1 and starts[0].get("params") == {
            "cwd":plan["repo"], "sandbox":"read-only", "approvalPolicy":"on-request", "ephemeral":False} and
            turns[0].get("params", {}).get("input") == [{"type":"text", "text":PROMPT}] and
            len(completions) == 1 and completions[0] == observed.get("turn") and
            completed.get("status") == "completed" and completed.get("error") is None and not tool_items)
    else:
        phase_matches = not starts and not turns and not observed.get("thread_id")
    passed = (phase_matches and not requests and not session_receipts and not dispatch and audit_matches and
        payload_matches and target_match and observed.get("observer_stopped") is None and
        observed.get("readers_complete") is True and observed.get("cleanup", {}).get("active_processes") == 0)
    return {"phase":phase, "matches_expected":bool(passed), "inventory_validation":validation,
        "session_receipt_count":len(session_receipts), "dispatch_bytes":len(dispatch), "dispatch_audit_unchanged":audit_matches,
        "targets_unchanged":target_match, "payload_matches":payload_matches, "cleanup":observed.get("cleanup"),
        "unexpected_server_requests":requests, "unexpected_tool_items":tool_items,
        "observer_stopped":observed.get("observer_stopped"), "native_turn_status":completed.get("status"),
        "interpretation":"The disabled hook supplies no context and no successful governance check. READY is only a requested model reply, never a readiness verdict."}


def invoke(plan, phase):
    argv = [plan["python"], "-I", "-B", plan["observer_script"], "--observe-phase", phase,
        "--plan", str(Path(plan["evidence"]) / "plan.json"), "--run", "--approved-plan-sha256", digest(encoded(plan))]
    return subprocess.run(argv, cwd=fixture.ROOT, capture_output=True)


def execute(plan, run_observer=None):
    run_observer = run_observer or invoke
    check_inputs(plan, "restored")
    log = Path(plan["dispatch_audit"]["path"])
    log_raw = ordinary(log, file=True).read_bytes() if log.exists() else b""
    if digest(log_raw) != plan["dispatch_audit"]["before_sha256"] or len(log_raw) != plan["dispatch_audit"]["before_bytes"]:
        raise ValueError("dispatch log changed after preflight")
    destination = ordinary(plan["evidence"])
    destination.mkdir(parents=True, exist_ok=False)
    original = base64.b64decode(plan["config_before_base64"], validate=True)
    disabled = base64.b64decode(plan["config_disabled_base64"], validate=True)
    (destination / "plan.json").write_bytes(encoded(plan))
    (destination / "actions.txt").write_bytes(encoded({"plan_sha256":digest(encoded(plan)), "operation":plan["config_change"],
        "sequence":["atomic config disable", "disabled native observation", "exact config restoration", "restored native inventory only"]}))
    (destination / "config-before.raw.json").write_bytes(encoded({"sha256":digest(original), "encoding":"base64", "bytes":plan["config_before_base64"]}))
    for name in ("stdout.txt", "stderr.txt", "restored-stdout.txt", "restored-stderr.txt"):
        (destination / name).write_bytes(b"")
    outcome = {"plan":plan, "conclusion":"unavailable", "started_monotonic":time.monotonic()}
    safe_cleanup = False
    try:
        replace_binding(Path(plan["config_path"]), original, disabled, "config.c05-disabled.tmp")
        outcome["fault_setup"] = {"actual_config_sha256":file_hash(plan["config_path"]), "only_enabled_changed":disable_session_start(original) == disabled}
        (destination / "fault-setup.json").write_bytes(encoded(outcome["fault_setup"]))
        result = run_observer(plan, "disabled")
        (destination / "stdout.txt").write_bytes(result.stdout)
        (destination / "stderr.txt").write_bytes(result.stderr)
        outcome["disabled_exit_status"] = result.returncode
        native = read_json(destination / "disabled/observations.json")
        safe_cleanup = native.get("cleanup", {}).get("active_processes") == 0 and native.get("readers_complete") is True
        outcome["disabled_assessment"] = native_result(plan, "disabled")
        outcome["conclusion"] = "pass" if result.returncode == 0 and outcome["disabled_assessment"]["matches_expected"] else "fail"
    except BaseException as error:
        outcome["error"] = type(error).__name__ + ": " + str(error)
    finally:
        restoration = {"config_restored":False, "inventory_confirmed":False}
        try:
            config = ordinary(plan["config_path"], file=True)
            current = config.read_bytes()
            if current == disabled:
                replace_binding(config, disabled, original, "config.c05-restored.tmp")
            elif current != original:
                raise ValueError("config changed outside this run; preserve the other actor's bytes")
            restoration["config_restored"] = file_hash(config) == plan["config_before_sha256"]
            if safe_cleanup and restoration["config_restored"]:
                result = run_observer(plan, "restored")
                (destination / "restored-stdout.txt").write_bytes(result.stdout)
                (destination / "restored-stderr.txt").write_bytes(result.stderr)
                restoration["inventory_exit_status"] = result.returncode
                restoration["inventory_assessment"] = native_result(plan, "restored")
                restoration["inventory_confirmed"] = result.returncode == 0 and restoration["inventory_assessment"]["matches_expected"]
                restoration["config_restored"] = file_hash(config) == plan["config_before_sha256"]
            else:
                restoration["inventory_not_run"] = "Disabled observer lacks confirmed owned cleanup, or config restoration failed; no further native process."
        except BaseException as error:
            restoration["error"] = type(error).__name__ + ": " + str(error)
        restoration["complete"] = restoration["config_restored"] and restoration["inventory_confirmed"]
        outcome["restoration"] = restoration
        if not restoration["complete"]:
            outcome["conclusion"] = "fail"
        outcome["finished_monotonic"] = time.monotonic()
        (destination / "observations.json").write_bytes(encoded(outcome))
    return outcome


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--package-record", type=Path)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--approved-plan-sha256")
    parser.add_argument("--observe-phase", choices=("disabled", "restored"), help=argparse.SUPPRESS)
    parser.add_argument("--plan", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        if args.observe_phase:
            if not args.run or not args.plan or args.evidence or args.package_record:
                raise ValueError("private observer requires one retained reviewed plan and explicit run")
            plan = read_json(args.plan.absolute())
            if args.approved_plan_sha256 != digest(encoded(plan)):
                raise ValueError("exact reviewed private observer plan required")
            observe(plan, args.observe_phase)
            return 0
        if args.plan or not args.evidence or not args.package_record:
            raise ValueError("evidence and checked package record required")
        plan = build_plan(args.evidence.absolute(), args.package_record.absolute())
        plan_sha256 = digest(encoded(plan))
        if not args.run:
            print(json.dumps({"mode":"preflight; no mutation or process", "plan_sha256":plan_sha256, "plan":plan}, indent=2))
            return 0
        if args.approved_plan_sha256 != plan_sha256:
            raise ValueError("exact independently reviewed plan digest required")
        result = execute(plan)
        print(json.dumps({"conclusion":result["conclusion"], "restoration":result["restoration"]}, indent=2))
        return 0 if result["conclusion"] == "pass" else 1
    except (ValueError, OSError, KeyError, observer.ObservationStopped) as error:
        print(json.dumps({"preflight_or_observer_failed":str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
