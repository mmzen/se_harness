"""Pure C09 fixture boundaries; no runtime creation, native process or API call."""
import copy
import base64
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).absolute().parent))
import c09_runner as runner
import c09_fault_sitecustomize as fault


class Plans(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        sandbox = root / "sandbox with spaces"
        repo = sandbox / "repo with spaces"
        repo.mkdir(parents=True)
        self.context = {"root": root / "checkout", "sandbox": sandbox, "repo": repo,
            "runtime": sandbox / runner.OWNED_NAME, "python": root / "shared016/Scripts/python.exe",
            "wheel": root / "wheel.whl", "evidence": root / "checkout/docs/engineering/plugin-integration/evidence/WO-PLG-005/C09",
            "capture": root / "capture.jsonl", "capture_observations": root / "observations.json",
            "package": root / "package.json", "binding": root / "data/binding.json",
            "observer": root / "observer.py", "runner": root / "runner.py", "fault_source": root / "fault.py"}
        for key in ("python", "wheel", "observer", "runner", "fault_source"):
            self.write(self.context[key], ("inert " + key).encode())
        self.addCleanup(patch.stopall)
        patch.object(runner, "WHEEL_SHA", runner.sha(self.context["wheel"])).start()
        patch.object(runner, "source_files", side_effect=lambda context: [context[name] for name in ("runner", "observer", "fault_source")]).start()
        self.binding = {"schema": "verity-codex-binding-v1", "repo": str(repo), "environment": str(self.context["python"].parent.parent),
            "artifact": "WO-PROBE-001", "capture": True,
            "profile": {"host": "0.153.4", "os": "windows", "python": "3.14.6", "evaluator": "0.16.0"},
            "decision": {"id": "DEC-PLG-001", "status": "decided", "option": "prove-supported-route"}}
        patch.object(runner.fixture, "binding", side_effect=lambda repo, env: copy.deepcopy(self.binding)).start()
        self.write(self.context["binding"], runner.encoded(self.binding))
        hooks = self.context["root"] / "plugins/verity-plane/codex/hooks/hooks.json"
        dispatch = self.context["root"] / "plugins/verity-plane/codex/dispatch.py"
        self.write(hooks, b"inert hooks")
        self.write(dispatch, b"inert dispatch")
        self.write(self.context["package"], runner.encoded({"archive_sha256": runner.PACKAGE_SHA,
            "payload": {"hooks/hooks.json": runner.sha(hooks), "scripts/codex-dispatch.py": runner.sha(dispatch)}}))
        self.argv = [str(self.context["python"]), "-I", "-B", "-m", "se_harness", "check", str(repo),
            "--artifact", "WO-PROBE-001", "--checkpoint", "pre-action", "--procedure", "PROC-WO-IMPLEMENT",
            "--changes-complete", "--changed-path", "governed-target.txt", "--json"]
        self.capture(self.argv)
        self.write(self.context["capture_observations"], runner.encoded({"observation_complete": True,
            "target_matches_expected_after": True, "completed_file_change_items": 1,
            "package": {"archive_sha256": runner.PACKAGE_SHA}}))
        for name in runner.edit.TARGETS:
            self.write(repo / name, b"old\n")
        self.write(repo / "AGENTS.md", b"<!-- se-harness:begin -->\npublic gate\n<!-- se-harness:end -->\n")
        self.write(repo / "ENGINEERING_HARNESS.md", b"public router\n")

    @staticmethod
    def write(path, raw):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    def capture(self, argv, extra=False):
        row = {"argv": ["--refusal-mode", "deny"], "stderr": json.dumps({"status": "checked",
            "checks": [{"argv": argv, "exit_status": 0}]})}
        raw = runner.encoded(row) + b"\n"
        self.write(self.context["capture"], raw * (2 if extra else 1))

    def inert_runtime(self):
        # These bytes are inert model inputs, never a virtualenv or executable.
        runtime = self.context["runtime"]
        self.write(runtime / "Scripts/python.exe", b"not executable")
        self.write(runtime / "Lib/site-packages/sitecustomize.py", self.context["fault_source"].read_bytes())
        self.write(runtime / runner.RUNTIME_RECORD, runner.encoded({"schema": "verity-c09-runtime-v1", "runtime": str(runtime),
            "wheel_sha256": runner.WHEEL_SHA, "source_sha256": runner.sha(self.context["fault_source"]),
            "normal_runtime_qualified": False, "files": runner.inventory(runtime)}))

    def test_setup_preview_never_spawns_creates_or_mutates(self):
        destination = self.context["evidence"] / "setup"
        before = self.context["binding"].read_bytes()
        with patch.object(runner, "paths", return_value=self.context), patch("subprocess.Popen") as spawn, \
                patch.object(runner, "execute_setup") as execute, patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(runner.main(["setup", "--evidence", str(destination)]), 0)
            plan = json.loads(output.getvalue())["plan"]
        self.assertFalse(destination.exists())
        self.assertFalse(self.context["runtime"].exists())
        self.assertEqual(self.context["binding"].read_bytes(), before)
        self.assertIn("--no-index", plan["commands"][1])
        self.assertIn("--no-deps", plan["commands"][1])
        self.assertIn("--isolated", plan["commands"][1])
        self.assertEqual(plan["commands"][1][-1], str(self.context["wheel"]))
        execute.assert_not_called()
        spawn.assert_not_called()

    def test_execution_rejects_missing_wrong_or_stale_plan_hash(self):
        destination = self.context["evidence"] / "setup"
        plan_sha = runner.digest(runner.encoded(runner.setup_plan(destination, self.context)))
        self.context["fault_source"].write_bytes(b"changed fixture source")
        with patch.object(runner, "paths", return_value=self.context), patch.object(runner, "execute_setup") as execute, \
                patch("sys.stderr", new_callable=io.StringIO):
            for extra in ([], ["--approved-plan-sha256", "0" * 64], ["--approved-plan-sha256", plan_sha]):
                with self.subTest(extra=extra), self.assertRaises(SystemExit):
                    runner.main(["setup", "--execute", "--evidence", str(destination), *extra])
        execute.assert_not_called()

    def test_captured_argv_must_be_unique_and_exact(self):
        for index in (0, 6, 8, 10, 12, 15):
            altered = self.argv.copy()
            altered[index] += "-different"
            self.capture(altered)
            with self.subTest(index=index), self.assertRaises(ValueError):
                runner.capture_argv(self.context)
        self.capture(self.argv, extra=True)
        with self.assertRaises(ValueError):
            runner.capture_argv(self.context)

    def test_old_dispatch_projection_blank_lines_do_not_change_exact_selector(self):
        raw = self.context["capture"].read_bytes()
        self.context["capture"].write_bytes(b" \r\n\r\n" + raw.replace(b"\n", b"\r\r\n") + b"\r\n")
        self.assertEqual(runner.capture_argv(self.context), self.argv)

    def test_shared_c08_and_repo_runtime_paths_are_never_owned(self):
        for forbidden in (self.context["python"].parent.parent, self.context["sandbox"] / "C08 owned runtime 016", self.context["repo"]):
            with self.subTest(path=forbidden), self.assertRaises(ValueError):
                runner.owned_runtime({**self.context, "runtime": forbidden})

    def test_run_preview_only_replaces_captured_interpreter_and_preserves_gate(self):
        self.inert_runtime()
        before = self.context["binding"].read_bytes()
        destination = self.context["evidence"] / "failed"
        with patch("subprocess.Popen") as spawn:
            plan = runner.run_plan("failed", destination, self.context)
        expected = self.argv.copy()
        expected[0] = str(self.context["runtime"] / "Scripts/python.exe")
        self.assertEqual(plan["fault_config"]["selector"], expected)
        self.assertEqual(plan["observer_argv"][3], str(self.context["observer"]))
        self.assertEqual(plan["one_edit_plan"]["target"], "governed-target.txt")
        self.assertEqual(plan["binding_before_sha256"], runner.digest(before))
        self.assertEqual(self.context["binding"].read_bytes(), before)
        self.assertFalse(Path(plan["fault_config_path"]).exists())
        self.assertFalse(Path(plan["marker_directory"]).exists())
        self.assertFalse(destination.exists())
        spawn.assert_not_called()

    def test_run_refuses_existing_fault_config_changed_runtime_and_binding(self):
        self.inert_runtime()
        config = self.context["runtime"] / fault.CONFIG_NAME
        self.write(config, b"leftover")
        with self.assertRaises(ValueError):
            runner.run_plan("failed", self.context["evidence"] / "failed", self.context)
        config.unlink()
        self.context["binding"].write_bytes(runner.encoded({**self.binding, "environment": "another"}))
        with self.assertRaises(ValueError):
            runner.run_plan("failed", self.context["evidence"] / "failed", self.context)
        self.context["binding"].write_bytes(runner.encoded(self.binding))
        (self.context["runtime"] / "Scripts/python.exe").write_bytes(b"changed")
        with self.assertRaises(ValueError):
            runner.run_plan("failed", self.context["evidence"] / "failed", self.context)

    def test_exact_binding_restore_never_overwrites_third_party_bytes(self):
        path = self.context["binding"]
        original = path.read_bytes()
        runner.replace_exact(path, original, b"our selection")
        path.write_bytes(b"another actor")
        with self.assertRaises(ValueError):
            runner.replace_exact(path, b"our selection", original)
        self.assertEqual(path.read_bytes(), b"another actor")

    def test_cleanup_failure_in_one_file_never_skips_the_other(self):
        binding = self.context["binding"]
        original = binding.read_bytes()
        config = self.context["sandbox"] / "inert-config.json"
        selected, config_raw = b"selected", b"exact config"
        intent = {"binding_write_started": True, "config_write_started": True}
        binding.write_bytes(b"other actor binding")
        config.write_bytes(config_raw)
        result = runner.restore_run_files(binding, original, selected, config, config_raw, intent)
        self.assertIn("binding_restoration_error", result)
        self.assertTrue(result["fault_config_removed"])
        self.assertEqual(binding.read_bytes(), b"other actor binding")
        binding.write_bytes(selected)
        config.write_bytes(b"other actor config")
        result = runner.restore_run_files(binding, original, selected, config, config_raw, intent)
        self.assertTrue(result["binding_restored"])
        self.assertIn("fault_config_cleanup_error", result)
        self.assertEqual(config.read_bytes(), b"other actor config")

    def test_completed_writes_are_reconciled_even_when_completion_flags_were_not_set(self):
        binding = self.context["binding"]
        original = binding.read_bytes()
        config = self.context["sandbox"] / "inert-config.json"
        selected, config_raw = b"selected", b"exact config"
        binding.write_bytes(selected)
        config.write_bytes(config_raw)
        result = runner.restore_run_files(binding, original, selected, config, config_raw,
            {"binding_write_started": True, "config_write_started": True})
        self.assertTrue(result["binding_restored"])
        self.assertTrue(result["fault_config_removed"])
        self.assertTrue(result["binding_reconciled_from_exact_bytes"])
        self.assertTrue(result["config_reconciled_from_exact_bytes"])

    def test_rejected_or_unattempted_creation_never_attributes_identical_foreign_bytes(self):
        binding = self.context["binding"]
        original = binding.read_bytes()
        config = self.context["sandbox"] / "inert-config.json"
        selected, config_raw = b"selected", b"exact config"
        for intent in ({}, {"config_write_started": True, "config_create_rejected": True,
                           "binding_write_started": True, "binding_replace_rejected": True}):
            binding.write_bytes(selected)
            config.write_bytes(config_raw)
            result = runner.restore_run_files(binding, original, selected, config, config_raw, intent)
            self.assertFalse(result["binding_restored"])
            self.assertFalse(result["fault_config_removed"])
            self.assertEqual(binding.read_bytes(), selected)
            self.assertEqual(config.read_bytes(), config_raw)

    def test_restore_interrupt_does_not_skip_exact_owned_config_cleanup(self):
        binding = self.context["binding"]
        original = binding.read_bytes()
        binding.write_bytes(b"selected")
        config = self.context["sandbox"] / "inert-config.json"
        config.write_bytes(b"exact config")
        with patch.object(runner, "replace_exact", side_effect=KeyboardInterrupt("injected cleanup interruption")):
            result = runner.restore_run_files(binding, original, b"selected", config, b"exact config",
                {"binding_write_started": True, "config_write_started": True})
        self.assertIn("KeyboardInterrupt", result["binding_restoration_error"])
        self.assertTrue(result["fault_config_removed"])


class FaultSelectors(unittest.TestCase):
    def setUp(self):
        self.config = {"schema": "verity-c09-fault-v1", "case": "failed", "stall_seconds": 90,
            "selector": ["X/python.exe", "-I", "-B", "-m", "se_harness", "check", "repo", "--json"],
            "python": "X/python.exe", "runtime": "X", "cwd": "parent"}

    def test_identity_doctor_script_and_other_check_never_select_fault(self):
        for argv in (["X/python.exe", "-I", "-B", "script.py"],
                     self.config["selector"][:5] + ["identity"], self.config["selector"][:5] + ["doctor"],
                     self.config["selector"] + ["--changed-path", "extra"]):
            with self.subTest(argv=argv):
                self.assertFalse(fault.selected(self.config, argv, "X/python.exe", "X", "parent"))
        self.assertTrue(fault.selected(self.config, self.config["selector"], "X/python.exe", "X", "parent"))
        for executable, prefix, cwd in (("Y/python.exe", "X", "parent"), ("X/python.exe", "Y", "parent"), ("X/python.exe", "X", "elsewhere")):
            self.assertFalse(fault.selected(self.config, self.config["selector"], executable, prefix, cwd))

    def test_nonselected_activation_does_not_spawn_or_sleep(self):
        with patch.object(fault.sys, "orig_argv", ["python", "-m", "se_harness", "identity"]), \
                patch("subprocess.Popen") as spawn, patch.object(fault.time, "sleep") as sleep:
            self.assertFalse(fault.activate(self.config, "hash"))
        spawn.assert_not_called()
        sleep.assert_not_called()

    def test_unmatched_marker_is_rejected_before_any_process_access(self):
        with patch.object(runner.ctypes, "WinDLL", create=True) as native:
            with self.assertRaises(ValueError):
                runner.interrupt_owned({"pid": 123, "role": "evaluator", "argv": ["wrong"]}, self.config, "hash", object())
        native.assert_not_called()

    def test_process_ownership_and_creation_are_checked_before_termination(self):
        marker = {"role": "evaluator", "config_sha256": "hash", "argv": self.config["selector"],
            "python": "X/python.exe", "prefix": "X", "cwd": "parent", "pid": 123, "creation_filetime": 10}
        for creation, member in ((11, True), (10, False), (10, True)):
            terminated = []
            class Call:
                def __init__(self, function): self.function = function
                def __call__(self, *args): return self.function(*args)
            def membership(handle, job, value):
                value._obj.value = member
                return True
            kernel = types.SimpleNamespace(OpenProcess=Call(lambda *args: 42), IsProcessInJob=Call(membership),
                TerminateProcess=Call(lambda *args: terminated.append(args) or True),
                WaitForSingleObject=Call(lambda *args: 0), CloseHandle=Call(lambda *args: True))
            with patch.object(runner.ctypes, "WinDLL", return_value=kernel, create=True), patch.object(fault, "creation_filetime", return_value=creation):
                if creation != 10 or not member:
                    with self.assertRaises(ValueError):
                        runner.interrupt_owned(marker, self.config, "hash", types.SimpleNamespace(handle=9))
                    self.assertEqual(terminated, [])
                else:
                    result = runner.interrupt_owned(marker, self.config, "hash", types.SimpleNamespace(handle=9))
                    self.assertTrue(result["owned_job_verified"])
                    self.assertEqual(terminated, [(42, 15)])

    def test_missing_native_refusal_never_passes_from_unchanged_target(self):
        observed = {"observation_complete": True, "cleanup": {"active_processes": 0}, "before": {"target": "same"},
                    "after": {"target": "same"}, "thread_id": "thread", "turn_id": "turn"}
        result = runner.assess({}, observed, [], [], {}, {})
        self.assertFalse(result["enforcement_observed"])
        self.assertFalse(result["qualified"])
        self.assertEqual(result["conclusion"], "unavailable")

    def test_three_fault_modes_publish_identity_before_exit_or_wait(self):
        class Exit(Exception): pass
        with tempfile.TemporaryDirectory() as folder:
            markers = Path(folder)
            (markers / "descendant.json").write_text("already observed")
            for mode in fault.MODES:
                config = {**self.config, "case": mode, "marker_directory": str(markers)}
                child = types.SimpleNamespace(pid=456, _handle=78, poll=lambda: None)
                actions = []
                def stop(code):
                    actions.append(("exit", code))
                    raise Exit()
                with patch.object(fault, "selected", return_value=True), patch("subprocess.Popen", return_value=child) as spawn, \
                        patch.object(fault, "self_record", return_value={"pid": 123, "creation_filetime": 10}), \
                        patch.object(fault, "creation_filetime", return_value=20), \
                        patch.object(fault, "retain", side_effect=lambda path, record: actions.append(("record", record))), \
                        patch.object(fault.time, "sleep", side_effect=lambda seconds: actions.append(("sleep", seconds))), \
                        patch.object(fault.os, "_exit", side_effect=stop):
                    with self.assertRaises(Exit):
                        fault.activate(config, "hash")
                self.assertEqual(actions[0][0], "record")
                self.assertEqual(actions[0][1]["fault_case"], mode)
                self.assertEqual(actions[0][1]["child_creation_filetime"], 20)
                self.assertEqual(actions[-1], ("exit", 3 if mode == "failed" else 4))
                self.assertEqual([action for action in actions if action[0] == "sleep"], [] if mode == "failed" else [("sleep", 90)])
                self.assertEqual(spawn.call_args.kwargs["stdout"], runner.subprocess.DEVNULL)
                self.assertEqual(spawn.call_args.kwargs["stderr"], runner.subprocess.DEVNULL)


class StrictAssessment(unittest.TestCase):
    def test_final_gate_requires_explicit_outer_cleanup_and_final_unchanged_snapshot(self):
        plan = {"targets_before_sha256": {"governed-target.txt": "before", "outside-scope.txt": "sentinel"}}
        outcome = {"observation_complete": True, "assessment": {"enforcement_observed": True},
            "binding_restored": True, "fault_config_removed": True, "runtime_inventory_restored": True,
            "outer_cleanup": {"active_processes": 0}, "targets_after_sha256": dict(plan["targets_before_sha256"])}
        self.assertTrue(runner.final_gates(outcome, plan))
        for change in ({"outer_cleanup": {}}, {"outer_cleanup": {"active_processes": 1}},
                       {"outer_cleanup": {"active_processes": 0, "descendant_cleanup_unconfirmed": True}},
                       {"targets_after_sha256": {"governed-target.txt": "changed", "outside-scope.txt": "sentinel"}},
                       {"targets_after_sha256": None}, {"binding_restored": False}):
            with self.subTest(change=change):
                self.assertFalse(runner.final_gates({**outcome, **change}, plan))

    def fixture(self):
        # Independently constructed protocol/effect observations, never a host.
        config = {"schema": "verity-c09-fault-v1", "case": "failed", "stall_seconds": 90,
            "selector": ["X/python.exe", "-I", "-B", "-m", "se_harness", "check"],
            "python": "X/python.exe", "runtime": "X", "cwd": "parent"}
        plan = {"repo": str(Path.cwd()), "runtime": "X", "runtime_python": "X/python.exe", "case": "failed",
            "one_edit_plan": {"schema": "verity-one-edit-v1", "target": "governed-target.txt", "before_utf8": "old\n", "after_utf8": "new\n"},
            "fault_config": config, "fault_config_sha256": "hash", "expected_governance_body_base64": base64.b64encode(b"body").decode(),
            "expected_governance_body_sha256": runner.digest(b"body"), "targets_before_sha256": {"governed-target.txt": runner.digest(b"old\n")}}
        observed = {"observation_complete": True, "cleanup": {"active_processes": 0}, "thread_id": "thread", "turn_id": "turn",
            "before": plan["targets_before_sha256"], "after": plan["targets_before_sha256"], "completed_file_change_items": 0,
            "native_hook_blocked": True, "acceptance_sent": False}
        change = {"path": "governed-target.txt", "kind": {"type": "update"}, "diff": "@@ -1 +1 @@\n-old\n+new\n"}
        def frame(method, params, timestamp):
            return {"message": {"method": method, "params": {"threadId": "thread", "turnId": "turn", **params}}, "received_monotonic": timestamp}
        reason = "Governed action refused: evaluator failed"
        transcript = [
            frame("turn/started", {"turn": {"id": "turn"}}, 7),
            frame("hook/completed", {"run": {"eventName": "sessionStart", "status": "completed", "entries": [{"kind": "context", "text": "body\nEND VERIFIED GOVERNANCE " + plan["expected_governance_body_sha256"] + "; complete context delivered."}]}}, 8),
            frame("item/started", {"item": {"type": "fileChange", "id": "edit", "status": "inProgress", "changes": [change]}}, 8.5),
            frame("hook/started", {"run": {"id": "hook", "eventName": "preToolUse"}}, 9),
            frame("hook/completed", {"run": {"id": "hook", "eventName": "preToolUse", "status": "blocked", "executionMode": "sync", "durationMs": 6000, "entries": [{"kind": "feedback", "text": reason}]}}, 15),
            frame("item/completed", {"item": {"type": "fileChange", "id": "edit", "status": "failed", "changes": [change]}}, 15.1),
            frame("turn/completed", {"turn": {"id": "turn"}}, 16)]
        identity = {"passed": True, "expected_root": "X", "python_executable": "X/python.exe", "python_version": "3.14.6",
            "harness_version": "0.16.0", "evaluator_payload_sha256": runner.PAYLOAD_SHA, "evaluator_archive_sha256": runner.WHEEL_SHA}
        final = {"argv": config["selector"], "pid": 123, "exit_status": 3, "resumed_monotonic": 10,
            "cleanup_started_monotonic": 12, "cleanup_finished_monotonic": 12.5,
            "cleanup": {"active_processes": 0, "before_cleanup": {"active_processes": 1}}}
        shared = {"checks": [{"argv": ["python", "-I", "-B", "-m", "se_harness", "identity"], "exit_status": 0, "result": identity},
            {"argv": ["python", "-I", "-B", "-m", "se_harness", "doctor"], "exit_status": 0, "result": {"checks": [{"passed": True}]}}, final],
            "inner_deadline_monotonic": 18, "response_written_monotonic": 13}
        row = {"argv": ["--refusal-mode", "deny"], "stderr": json.dumps(shared), "response_prepared_monotonic": 14,
            "stdout": json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}})}
        evaluator = {"role": "evaluator", "config_sha256": "hash", "argv": config["selector"], "python": "X/python.exe", "prefix": "X", "cwd": "parent",
            "fault_case": "failed", "pid": 124, "ppid": 123, "creation_filetime": 10, "observed_monotonic": 11,
            "fault_ready_monotonic": 11.5, "child_pid": 134, "child_argv": ["child"]}
        descendant = {"role": "descendant", "config_sha256": "hash", "pid": 135, "ppid": 134, "creation_filetime": 20, "argv": ["child"]}
        return plan, observed, transcript, [row], evaluator, descendant

    def test_complete_independent_fault_observations_pass_without_runtime_qualification(self):
        result = runner.assess(*self.fixture())
        self.assertEqual(result["conclusion"], "pass", result)
        self.assertTrue(result["enforcement_observed"])
        self.assertFalse(result["qualified"])

    def test_native_denial_without_file_item_has_only_the_specific_terminal_limit(self):
        values = self.fixture()
        plan, observed, transcript, dispatch, evaluator, descendant = values
        observed.update(observation_complete=False, readers_complete=True,
                        observer_stopped="turn ended without a complete correlated native file-change item")
        transcript[:] = [row for row in transcript if row["message"]["method"] not in ("item/started", "item/completed")]
        transcript[-1]["message"]["params"]["turn"].update(status="completed", error=None)
        result = runner.assess(*values)
        self.assertTrue(result["enforcement_observed"], result)
        self.assertTrue(result["native_observer_terminal_limited"])
        observed["observer_stopped"] = "external stop, fixed deadline or protocol-reader failure"
        result = runner.assess(*values)
        self.assertFalse(result["enforcement_observed"], result)

    def test_effect_context_wrong_path_late_denial_and_live_descendants_refuse_pass(self):
        for mode in ("effect", "other-path", "truncated-context", "late-denial", "child-alive", "cleanup-after-response", "wrong-argv", "false-identity"):
            values = self.fixture()
            plan, observed, transcript, dispatch, evaluator, descendant = values
            shared = json.loads(dispatch[0]["stderr"])
            if mode == "effect": observed["completed_file_change_items"] = 1
            if mode == "other-path": transcript[2]["message"]["params"]["item"]["changes"][0]["path"] = "outside-scope.txt"
            if mode == "truncated-context": transcript[1]["message"]["params"]["run"]["entries"][0]["text"] = "partial"
            if mode == "late-denial": transcript[4]["received_monotonic"] = 40
            if mode == "child-alive": shared["checks"][-1]["cleanup"]["active_processes"] = 1
            if mode == "cleanup-after-response": shared["checks"][-1]["cleanup_finished_monotonic"] = 14
            if mode == "wrong-argv": evaluator["argv"] = ["another"]
            if mode == "false-identity": shared["checks"][0]["result"]["python_version"] = "3.15.0"
            dispatch[0]["stderr"] = json.dumps(shared)
            with self.subTest(mode=mode):
                result = runner.assess(*values)
                self.assertFalse(result["enforcement_observed"], result)
                self.assertFalse(result["qualified"])


if __name__ == "__main__":
    unittest.main()
