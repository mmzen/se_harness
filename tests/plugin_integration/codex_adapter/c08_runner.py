"""Preflight one C08 observation; --run requires the exact reviewed plan digest.

Only this fixture's binding and its owned interpreter may change. The existing
live observer owns native execution/cleanup. This wrapper is not a hook, an
evaluator, or a source of readiness. No native process is started by default.
"""
import argparse
import base64
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

CASES = ("missing", "runtime-ready", "removed", "wrong017")
PACKAGE_SHA = "a94185033507c3e3c65de890a6979c34048e6905ea6062a270d004b1b254c4c5"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf8")


def ordinary(path, *, file=False):
    path = Path(path)
    if not path.is_absolute() or ".." in path.parts or any(ord(c) < 32 for c in str(path)):
        raise ValueError("absolute path without traversal required")
    for parent in (path, *path.parents):
        if parent.exists() or parent.is_symlink():
            info = parent.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise ValueError("linked/reparse paths are not permitted")
    if file:
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError("ordinary single-link file required")
    return path


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result
    raw = ordinary(path, file=True).read_bytes()
    return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=pairs)


def paths():
    return {"root": fixture.ROOT, "repo": fixture.SANDBOX / "repo with spaces",
        "binding": fixture.PROFILE / "codex/plugins/data/verity-plane-verity-plane-codex-fixture/binding.json",
        "owned_runtime": fixture.SANDBOX / "C08 owned runtime 016",
        "missing_runtime": fixture.SANDBOX / "C08 never prepared runtime",
        "wrong_runtime": fixture.WORK / "se-harness-plugin-eval-017",
        "runner_python": fixture.PYTHON, "live_observer": HERE / "live.py"}


def file_hash(path):
    return digest(ordinary(path, file=True).read_bytes())


def source_paths(context):
    folder = context["live_observer"].parent
    probe = context["root"] / "tests/plugin_integration/codex_probe"
    return [context["live_observer"], folder / "fixture.py", folder / "observer.py",
            probe / "processes.py", probe / "probe.py", probe / "sanitize_output.py", Path(__file__)]


def build_plan(case, destination, package_record, ready_evidence=None, context=None):
    context = context or paths()
    destination, package_record = ordinary(destination), ordinary(package_record, file=True)
    allowed = context["root"] / "docs/engineering/plugin-integration/evidence/WO-PLG-005/C08"
    if allowed not in destination.parents or destination.exists():
        raise ValueError("fresh C08 evidence directory required")
    original = ordinary(context["binding"], file=True).read_bytes()
    selected = read_json(context["binding"])
    if not isinstance(selected, dict) or set(selected) != {"schema", "repo", "environment", "artifact", "capture", "profile", "decision"}:
        raise ValueError("unexpected original binding fields")
    if (selected["schema"] != "verity-codex-binding-v1" or selected["capture"] is not True or
            selected["repo"] != str(context["repo"]) or selected["artifact"] != "WO-PROBE-001" or
            selected["profile"] != {"host":"0.153.4", "os":"windows", "python":"3.14.6", "evaluator":"0.16.0"} or
            selected["decision"] != {"id":"DEC-PLG-001", "status":"decided", "option":"prove-supported-route"}):
        raise ValueError("original binding is not the accepted captured fixture")
    if ordinary(selected["environment"]) != context["runner_python"].parent.parent:
        raise ValueError("restore target must be the original shared accepted 016 selection")
    package = read_json(package_record)
    if not isinstance(package, dict) or package.get("archive_sha256") != PACKAGE_SHA:
        raise ValueError("exact checked package04 required")
    for name, source in (("hooks/hooks.json", "hooks/hooks.json"), ("scripts/codex-dispatch.py", "dispatch.py")):
        if package["payload"][name] != digest((context["root"] / "plugins/verity-plane/codex" / source).read_bytes()):
            raise ValueError("package differs from current adapter")
    for member in ("repo", "owned_runtime", "missing_runtime", "wrong_runtime", "runner_python", "live_observer"):
        ordinary(context[member], file=member in ("runner_python", "live_observer"))
    owned_python = ordinary(context["owned_runtime"] / "Scripts/python.exe", file=True)
    removed_python = ordinary(owned_python.with_name("python.c08-removed.exe"))
    if removed_python.exists():
        raise ValueError("owned removal destination already exists; inspect previous recovery first")
    if context["missing_runtime"].exists():
        raise ValueError("pre-setup runtime path must remain absent")
    ordinary(context["wrong_runtime"] / "Scripts/python.exe", file=True)
    if case not in CASES:
        raise ValueError("unknown C08 case")
    ready_binding = None
    if case == "removed":
        if ready_evidence is None:
            raise ValueError("literal removal requires the prior owned-runtime native readiness evidence")
        ready_evidence = ordinary(ready_evidence, file=True)
        if allowed not in ready_evidence.parents:
            raise ValueError("ready evidence must be inside C08")
        ready = read_json(ready_evidence)
        if (ready.get("case") != "runtime-ready" or ready.get("conclusion") != "pass" or
                ready.get("plan", {}).get("selected_environment") != str(context["owned_runtime"]) or
                ready.get("restoration", {}).get("complete") is not True or
                ready.get("plan", {}).get("owned_python_sha256") != file_hash(owned_python) or
                ready.get("assessment", {}).get("matches_expected") is not True):
            raise ValueError("prior evidence does not prove owned runtime readiness and restoration")
        ready_binding = {"path":str(ready_evidence), "sha256":digest(ready_evidence.read_bytes())}
    environment = context[{"missing":"missing_runtime", "runtime-ready":"owned_runtime",
                           "removed":"owned_runtime", "wrong017":"wrong_runtime"}[case]]
    changed = {**selected, "environment":str(environment)}
    repo = context["repo"]
    agents = ordinary(repo / "AGENTS.md", file=True).read_bytes()
    start, end = b"<!-- se-harness:begin -->", b"<!-- se-harness:end -->"
    if agents.count(start) != 1 or agents.count(end) != 1 or agents.index(start) >= agents.index(end):
        raise ValueError("one ordered complete managed gate required")
    gate = agents[agents.index(start):agents.index(end) + len(end)]
    router = ordinary(repo / "ENGINEERING_HARNESS.md", file=True).read_bytes()
    body = b"AGENTS.md managed gate:\n" + gate + b"\n\nENGINEERING_HARNESS.md:\n" + router
    body.decode("utf8")
    before_targets = {name:digest(ordinary(repo / name, file=True).read_bytes()) for name in
                      ("governed-target.txt", "outside-scope.txt", "café quoted ' target.txt")}
    fixed_inputs = [*source_paths(context), package_record, context["runner_python"], owned_python,
                    context["wrong_runtime"] / "Scripts/python.exe",
                    *[repo / name for name in ("AGENTS.md", "ENGINEERING_HARNESS.md", ".engineering-harness.lock", ".engineering-harness.toml")]]
    for temporary in ("binding.c08-selected.tmp", "binding.c08-restored.tmp"):
        candidate = ordinary(context["binding"].with_name(temporary))
        if candidate.exists():
            raise ValueError("binding transaction temporary exists; inspect previous recovery first")
    log = ordinary(context["binding"].with_name("observations.jsonl"))
    log_raw = ordinary(log, file=True).read_bytes() if log.exists() else b""
    plan = {"schema":"verity-c08-plan-v1", "case":case, "evidence":str(destination), "repo":str(repo),
        "binding_path":str(context["binding"]), "binding_before_base64":base64.b64encode(original).decode(),
        "binding_before_sha256":digest(original), "binding_selected":changed,
        "binding_selected_sha256":digest(encoded(changed)), "selected_environment":str(environment),
        "owned_runtime":str(context["owned_runtime"]), "owned_python":str(owned_python),
        "owned_python_sha256":digest(owned_python.read_bytes()), "removed_python":str(removed_python),
        "prior_ready_evidence":ready_binding, "targets_before_sha256":before_targets,
        "expected_body_base64":base64.b64encode(body).decode(), "expected_body_sha256":digest(body),
        "dispatch_audit":{"path":str(log), "before_bytes":len(log_raw), "before_sha256":digest(log_raw)},
        "expected_dispatch_count":0 if case in ("missing", "removed") else 1,
        "expected_result":"complete-context" if case == "runtime-ready" else "identity-unready" if case == "wrong017" else "setup-required",
        "argv":[str(context["runner_python"]), "-I", "-B", str(context["live_observer"]),
                "--package-record",str(package_record),"--evidence",str(destination / "live")],
        "fixed_input_sha256":{str(path):file_hash(path) for path in fixed_inputs},
        "package_payload":package["payload"], "package_record_sha256":file_hash(package_record),
        "payload":"Public managed gate/router, synthetic WO-PROBE-001 fixture and local paths; existing live.py sends its fixed READY-only prompt. No credential content is read by this runner.",
        "restoration":"finally: restore only our selected binding bytes to the exact original; restore only the checked owned interpreter rename; verify hashes. No shared environment/cache/security change."}
    return plan


def rename_owned(source, destination, owned_runtime, expected_sha256):
    source, destination, owned_runtime = ordinary(source, file=True), ordinary(destination), ordinary(owned_runtime)
    expected_parent = owned_runtime.resolve(strict=True) / "Scripts"
    if (source.resolve(strict=True).parent != expected_parent or destination.resolve(strict=False).parent != expected_parent or
            {source.name, destination.name} != {"python.exe", "python.c08-removed.exe"} or destination.exists()):
        raise ValueError("rename must remain between the two exact owned interpreter paths")
    if digest(source.read_bytes()) != expected_sha256:
        raise ValueError("owned interpreter bytes changed")
    source.rename(destination)


def replace_binding(binding, expected, replacement, temporary_name):
    """Keep partial writes away from binding.json; never overwrite another actor."""
    binding = ordinary(binding, file=True)
    temporary = ordinary(binding.with_name(temporary_name))
    if temporary.exists() or binding.read_bytes() != expected:
        raise ValueError("binding changed or transaction temporary already exists")
    created = False
    created_identity = None
    try:
        with temporary.open("xb") as stream:
            created = True
            created_identity = (os.fstat(stream.fileno()).st_dev, os.fstat(stream.fileno()).st_ino)
            stream.write(replacement)
            stream.flush()
            os.fsync(stream.fileno())
        ordinary(binding, file=True)
        if binding.read_bytes() != expected:
            raise ValueError("binding changed outside this run; preserve the other actor's bytes")
        os.replace(temporary, binding)
    finally:
        if created and temporary.exists():
            # This exact exclusive-created temporary is ours; no recursive cleanup.
            info = ordinary(temporary, file=True).stat()
            if (info.st_dev, info.st_ino) != created_identity:
                raise ValueError("transaction temporary replaced by another actor; preserve it")
            temporary.unlink()


def assess(plan):
    live = Path(plan["evidence"]) / "live"
    observed = read_json(live / "observations.json")
    transcript = read_json(live / "transcript.json")
    capture = live / "dispatch.jsonl"
    dispatch = [json.loads(line) for line in capture.read_text(encoding="utf8").splitlines()] if capture.exists() else []
    receipts = [row["message"]["params"]["run"] for row in transcript if
        "received_monotonic" in row and row.get("message", {}).get("method") == "hook/completed"
        and row["message"].get("params", {}).get("run", {}).get("eventName") == "sessionStart"]
    contexts = [entry["text"] for run in receipts for entry in run.get("entries", [])
                if entry.get("kind") == "context" and isinstance(entry.get("text"), str)]
    body = base64.b64decode(plan["expected_body_base64"])
    marker = "END VERIFIED GOVERNANCE " + plan["expected_body_sha256"] + "; complete context delivered.\n"
    is_ready = any(body in context.encode("utf8") and context.endswith(marker) for context in contexts)
    setup = any("Setup required" in context and "interpreter absent" in context and "no Python invoked" in context for context in contexts)
    unready = any(context.startswith("Verity Plane governance context is UNREADY.") for context in contexts)
    identity_checks = []
    for row in dispatch:
        if row.get("stderr"):
            for line in row["stderr"].splitlines():
                try:
                    identity_checks.extend(json.loads(line).get("checks", []))
                except (ValueError, AttributeError):
                    pass
    identity_prefix = [str(Path(plan["selected_environment"]) / "Scripts/python.exe"), "-I", "-B", "-m", "se_harness", "identity"]
    wrong_identity = any(row.get("argv", [])[:6] == identity_prefix and isinstance(row.get("result"), dict)
                         and row["result"].get("passed") is False
                         and row["result"].get("harness_version") == "0.17.0" for row in identity_checks)
    unchanged = (observed["before"] == observed["after"] and
                 {name:value["sha256"] for name, value in observed["before"].items()} == plan["targets_before_sha256"])
    payload = observed.get("loaded_payload") or {}
    source = Path(payload.get("root", ".")) / "hooks/hooks.json"
    requests = [row for row in transcript if "received_monotonic" in row and
                "id" in row.get("message", {}) and "method" in row["message"]]
    native_ok = (len(receipts) == 1 and len(contexts) == 1 and
                 all(run.get("status") == "completed" and run.get("sourcePath") == str(source) for run in receipts) and
                 observed.get("observer_stopped") is None and not requests and observed.get("readers_complete") is True and
                 observed.get("cleanup", {}).get("active_processes") == 0 and
                 payload.get("sha256") == plan["package_payload"] and
                 observed.get("package_record_sha256") == plan["package_record_sha256"])
    environment = Path(plan["selected_environment"])
    expected_argv = [str(environment / "Scripts/python.exe"), "-I", "-B",
        str(Path(payload.get("root", ".")) / "scripts/session-context.py"),
        "--repo", plan["repo"], "--environment", str(environment), "--version", "0.16.0",
        "--payload-sha256", "51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c",
        "--archive-sha256", "a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae",
        "--host", "codex", "--context-limit", "16000", "--read-limit", "0"]
    exact_argv = all(row.get("argv") == expected_argv for row in dispatch)
    prepared_contexts = [json.loads(row["stdout"])["hookSpecificOutput"]["additionalContext"]
                         for row in dispatch if row.get("status") == "handler-output-returned"]
    native_dispatch_match = bool(contexts) and all(context in prepared_contexts for context in contexts)
    audit = plan["dispatch_audit"]
    log = ordinary(audit["path"])
    log_raw = ordinary(log, file=True).read_bytes() if log.exists() else b""
    appended = log_raw[audit["before_bytes"]:]
    audit_valid = (digest(log_raw[:audit["before_bytes"]]) == audit["before_sha256"] and
                   appended == (capture.read_bytes() if capture.exists() else b""))
    exact_count = len(dispatch) == plan["expected_dispatch_count"]
    if plan["case"] in ("missing", "removed"):
        matched = setup and not is_ready and exact_count and not appended
    elif plan["case"] == "runtime-ready":
        matched = is_ready and exact_count and native_dispatch_match and all(row.get("exit_status") == 0 for row in dispatch)
    else:
        matched = unready and wrong_identity and not is_ready and not setup and exact_count and native_dispatch_match
    return {"native_receipts":receipts, "dispatch_count":len(dispatch), "complete_context":is_ready,
        "setup_required":setup, "unready":unready, "wrong_identity_observed":wrong_identity,
        "exact_argv":exact_argv, "expected_argv":expected_argv, "native_dispatch_match":native_dispatch_match,
        "dispatch_audit":{"valid":audit_valid, "appended_bytes":len(appended), "appended_sha256":digest(appended)},
        "targets_unchanged":unchanged, "cleanup":observed.get("cleanup"),
        "observer_stopped":observed.get("observer_stopped"), "matches_expected":bool(matched and native_ok and unchanged and exact_argv and audit_valid),
        "limits":"No dispatch capture for an absent absolute interpreter is the invocation audit; no claim about unrelated Python processes. Logical identity refusal is expected with shared handler exit zero."}


def execute(plan, observe=None):
    destination = ordinary(plan["evidence"])
    original = base64.b64decode(plan["binding_before_base64"], validate=True)
    selected = encoded(plan["binding_selected"])
    binding = ordinary(plan["binding_path"], file=True)
    if digest(binding.read_bytes()) != plan["binding_before_sha256"]:
        raise ValueError("binding changed after preflight")
    for path, expected in plan["fixed_input_sha256"].items():
        if file_hash(path) != expected:
            raise ValueError("fixed input changed after preflight: " + path)
    for name, expected in plan["targets_before_sha256"].items():
        if file_hash(Path(plan["repo"]) / name) != expected:
            raise ValueError("target changed after preflight: " + name)
    audit = plan["dispatch_audit"]
    log = ordinary(audit["path"])
    log_raw = ordinary(log, file=True).read_bytes() if log.exists() else b""
    if len(log_raw) != audit["before_bytes"] or digest(log_raw) != audit["before_sha256"]:
        raise ValueError("dispatch audit changed after preflight")
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "actions.txt").write_bytes(encoded(plan))
    (destination / "binding-before.raw.json").write_bytes(encoded({"sha256":digest(original),"encoding":"base64","bytes":base64.b64encode(original).decode()}))
    for name in ("stdout.txt", "stderr.txt"):
        (destination / name).write_bytes(b"")
    outcome = {"case":plan["case"], "plan":plan, "conclusion":"unavailable", "started_monotonic":time.monotonic()}
    removed = False
    try:
        replace_binding(binding, original, selected, "binding.c08-selected.tmp")
        if plan["case"] == "removed":
            rename_owned(plan["owned_python"], plan["removed_python"], plan["owned_runtime"], plan["owned_python_sha256"])
            removed = True
        outcome["fault_setup"] = {"binding_sha256":digest(binding.read_bytes()),
            "selected_python_exists":Path(plan["selected_environment"], "Scripts/python.exe").exists(), "owned_python_removed":removed}
        (destination / "fault-setup.json").write_bytes(encoded(outcome["fault_setup"]))
        if (outcome["fault_setup"]["binding_sha256"] != plan["binding_selected_sha256"] or
                outcome["fault_setup"]["selected_python_exists"] != (plan["case"] in ("runtime-ready", "wrong017"))):
            raise ValueError("fault setup differs from the reviewed plan; no observer started")
        result = observe(plan) if observe else subprocess.run(plan["argv"], cwd=fixture.ROOT, capture_output=True)
        (destination / "stdout.txt").write_bytes(result.stdout)
        (destination / "stderr.txt").write_bytes(result.stderr)
        outcome["observer_exit_status"] = result.returncode
        outcome["assessment"] = assess(plan)
        outcome["conclusion"] = "pass" if result.returncode == 0 and outcome["assessment"]["matches_expected"] else "fail"
    except BaseException as error:
        outcome["error"] = type(error).__name__ + ": " + str(error)
    finally:
        restoration = {"binding_restored":False, "owned_python_restored":False, "errors":[]}
        try:
            # Inspect actual state even if an interruption occurred between the
            # atomic rename and recording its completion in Python.
            if plan["case"] == "removed" and Path(plan["removed_python"]).exists():
                rename_owned(plan["removed_python"], plan["owned_python"], plan["owned_runtime"], plan["owned_python_sha256"])
            restoration["owned_python_sha256"] = digest(ordinary(plan["owned_python"], file=True).read_bytes())
            restoration["owned_python_restored"] = (restoration["owned_python_sha256"] == plan["owned_python_sha256"] and
                                                     not Path(plan["removed_python"]).exists())
        except (OSError, ValueError) as error:
            restoration["errors"].append("interpreter: " + str(error))
        try:
            current = ordinary(binding, file=True).read_bytes()
            if current == selected:
                replace_binding(binding, selected, original, "binding.c08-restored.tmp")
            elif current != original:
                raise ValueError("binding changed outside this run; do not overwrite another actor's bytes")
            restoration["binding_restored"] = file_hash(binding) == plan["binding_before_sha256"]
        except (OSError, ValueError) as error:
            restoration["errors"].append("binding: " + str(error))
        restoration["complete"] = restoration["binding_restored"] and restoration["owned_python_restored"] and restoration.get("owned_python_sha256") == plan["owned_python_sha256"]
        outcome["restoration"] = restoration
        if not restoration["complete"]:
            outcome["conclusion"] = "fail"
        outcome["finished_monotonic"] = time.monotonic()
        (destination / "observations.json").write_bytes(encoded(outcome))
    return outcome


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=CASES, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--package-record", type=Path, required=True)
    parser.add_argument("--ready-evidence", type=Path)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--approved-plan-sha256")
    args = parser.parse_args()
    try:
        plan = build_plan(args.case, args.evidence.absolute(), args.package_record.absolute(),
                          args.ready_evidence.absolute() if args.ready_evidence else None)
        plan_sha = digest(encoded(plan))
        if not args.run:
            print(json.dumps({"mode":"preflight; no mutation or process", "plan_sha256":plan_sha, "plan":plan},indent=2))
            return 0
        if args.approved_plan_sha256 != plan_sha:
            raise ValueError("exact independently reviewed plan digest required")
        result = execute(plan)
        print(json.dumps({"case":args.case,"conclusion":result["conclusion"],"restoration":result["restoration"]},indent=2))
        return 0 if result["conclusion"] == "pass" else 1
    except (ValueError, OSError, KeyError) as error:
        print(json.dumps({"preflight_failed":str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
