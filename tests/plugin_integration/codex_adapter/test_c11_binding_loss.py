"""Pure C11 binding-loss boundaries; all mutations use temporary fake fixtures."""
import base64
import copy
import json
from pathlib import Path
import sys
import time
import tomllib
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).absolute().parent))
import c11_binding_loss as runner
import test_c05_runner as fixtures


class BindingLossTests(unittest.TestCase):
    def setUp(self):
        helper = fixtures.C05RunnerTests()
        helper.setUp()
        self.addCleanup(helper.doCleanups)
        self.helper, self.context, self.put = helper, helper.context, helper.put
        self.destination = helper.root / "docs/engineering/plugin-integration/evidence/WO-PLG-005/C11/lost-01"
        self.original, self.package, self.loaded = helper.original, helper.package, helper.loaded
        self.put(self.context["repo"] / "AGENTS.md", b"owner text\r\n<!-- se-harness:begin -->\npublic synthetic gate\n<!-- se-harness:end -->\n")
        for path in [*[self.context["schema"].parent / name for name in runner.edit.SCHEMA_PINS],
                     helper.root / "docs/engineering/plugin-integration/evidence/WO-PLG-005/preparation/accepted-profile/identity.json",
                     helper.root / "docs/engineering/plugin-integration/evidence/WO-PLG-005/C02/startup-01/transcript.json"]:
            self.put(path,b"synthetic fixed input; never execute")

    def plan(self):
        return runner.build_plan(self.destination, self.package, self.context)

    def hooks(self, lost):
        result = self.helper.hooks(True)
        for hook in result["result"]["data"][0]["hooks"]:
            if hook["eventName"] == "preToolUse":
                hook["enabled"] = not lost
        return result

    def inventory_check(self, response):
        return runner.inactive_bindings(response, self.context["repo"], self.context["cache"], self.helper.definitions, self.helper.payload["hooks/hooks.json"])

    def native_records(self, plan, phase):
        started = time.monotonic()
        folder, transcript = Path(plan["evidence"]) / phase, []
        def send(value):
            transcript.append({"sent_monotonic":time.monotonic(), "message":value})
        def receive(value):
            transcript.append({"received_monotonic":time.monotonic(), "message":value})
        hooks = self.hooks(phase == "lost")
        send({"id":"inventory", "method":"hooks/list", "params":{"cwds":[plan["repo"]]}})
        receive({"id":"inventory", **hooks})
        arguments = (hooks, self.context["repo"], self.context["cache"], self.helper.definitions, self.helper.payload["hooks/hooks.json"])
        inventory = runner.inactive_bindings(*arguments)[0] if phase == "lost" else runner.NORMAL_VALIDATOR(*arguments)
        snapshot = runner.target_snapshot(plan)
        target_values = {name:{"sha256":sha, "bytes":"synthetic"} for name,sha in snapshot.items()}
        observed = {"active_bindings":inventory, "loaded_payload":{"root":str(self.loaded), "sha256":plan["package_payload"]},
            "package_record_sha256":plan["package_record_sha256"], "before":target_values, "after":target_values,
            "cleanup":{"active_processes":0}, "readers_complete":True}
        dispatch = []
        if phase != "restored":
            thread, turn = phase + "-thread", phase + "-turn"
            observed["thread_id"] = thread
            effective = {"thread":{"id":thread}, "cwd":plan["repo"], "sandbox":{"type":"readOnly", "networkAccess":False},
                "approvalPolicy":"on-request", "approvalsReviewer":"user", "runtimeWorkspaceRoots":[plan["repo"]], "activePermissionProfile":None}
            send({"id":"thread-start", "method":"thread/start", "params":runner.edit.thread_params(Path(plan["repo"]))})
            receive({"id":"thread-start", "result":effective})
            send({"id":"turn-start", "method":"turn/start", "params":{"threadId":thread, "input":[{"type":"text", "text":plan["prompt"] if phase == "lost" else runner.prior.PROMPT}]}})
            receive({"method":"turn/started", "params":{"threadId":thread, "turn":{"id":turn}}})
            body = base64.b64decode(plan["expected_governance_body_base64"]).decode()
            context = "READY synthetic test\n" + body + "\nEND VERIFIED GOVERNANCE " + plan["expected_governance_body_sha256"] + "; complete context delivered."
            run = {"id":"session-hook", "eventName":"sessionStart", "status":"inProgress", "executionMode":"sync", "entries":[]}
            receive({"method":"hook/started", "params":{"threadId":thread, "turnId":turn, "run":copy.deepcopy(run)}})
            run.update(status="completed", entries=[{"kind":"context", "text":context}])
            receive({"method":"hook/completed", "params":{"threadId":thread, "turnId":turn, "run":run}})
            dispatch = [{"argv":[plan["python"], "-I", "-B", str(self.loaded / "scripts/session-context.py")], "exit_status":0,
                "stdout":runner.encoded({"hookSpecificOutput":{"hookEventName":"SessionStart", "additionalContext":context}}).decode()}]
            if phase == "lost":
                value = plan["one_edit_plan"]
                changes = [{"path":value["target"], "kind":{"type":"update"}, "diff":"@@ -1 +1 @@\n-" + value["before_utf8"] + "+" + value["after_utf8"]}]
                item = {"id":"edit-item", "type":"fileChange", "status":"inProgress", "changes":changes}
                receive({"method":"item/started", "params":{"threadId":thread, "turnId":turn, "item":copy.deepcopy(item)}})
                receive({"id":"one-approval", "method":"item/fileChange/requestApproval", "params":{
                    "threadId":thread, "turnId":turn, "itemId":"edit-item", "startedAtMs":1}})
                send({"id":"one-approval", "result":{"decision":"accept"}})
                self.put(Path(plan["repo"]) / value["target"], value["after_utf8"].encode())
                item["status"] = "completed"
                receive({"method":"item/completed", "params":{"threadId":thread, "turnId":turn, "item":item}})
                observed.update(before=snapshot, after=runner.target_snapshot(plan), observation_complete=True, effective_thread=effective,
                    turn_id=turn, acceptance_sent=True, completed_file_change_items=1, target_actual_sha256=runner.digest(value["after_utf8"].encode()))
            completed = {"method":"turn/completed", "params":{"threadId":thread, "turn":{"id":turn, "status":"completed", "error":None}}}
            receive(completed)
            observed["turn"] = completed
        self.put(folder / "observations.json", runner.encoded(observed))
        self.put(folder / "transcript.json", runner.encoded(transcript))
        # Deliberate empty projection lines match historical CRCRLF captures.
        self.put(folder / "dispatch.jsonl", b"\r\r\n".join(json.dumps(row).encode() for row in dispatch) + b"\r\r\n")
        return {"returncode":0, "started_monotonic":started, "finished_monotonic":time.monotonic(), "outer_cleanup":{"active_processes":0}}

    def test_only_pretool_flag_changes_preserving_bom_comments_and_crlf(self):
        selected = runner.disable_pre_tool(self.original)
        self.assertEqual(selected.replace(b"enabled = false\r\n", b"", 1), self.original)
        before, after = (tomllib.loads(raw.decode("utf-8-sig")) for raw in (self.original, selected))
        before["hooks"]["state"][runner.TOOL_KEY]["enabled"] = False
        self.assertEqual(before, after)
        header = ('[hooks.state."' + runner.TOOL_KEY + '"]\r\n').encode()
        original = self.original.replace(header, header + b"enabled = true # preserve comment\r\n")
        self.assertEqual(runner.disable_pre_tool(original), original.replace(b"true # preserve comment", b"false # preserve comment"))

    def test_wrong_trust_disabled_or_noncanonical_header_rejected(self):
        for raw in (self.original.replace(runner.TRUST[runner.TOOL_KEY].encode(), b"wrong"), runner.disable_pre_tool(self.original),
                    self.original.replace(('"' + runner.TOOL_KEY + '"').encode(), ("'" + runner.TOOL_KEY + "'").encode())):
            with self.subTest(raw=raw[-50:]), self.assertRaises(ValueError):
                runner.disable_pre_tool(raw)

    def test_inactive_inventory_retains_actual_disabled_native_record(self):
        response = self.hooks(True)
        original = copy.deepcopy(response)
        actual, comparison = self.inventory_check(response)
        self.assertEqual(response, original)
        self.assertFalse(next(h for h in actual if h["key"] == runner.TOOL_KEY)["enabled"])
        self.assertTrue(next(h for h in actual if h["key"] == runner.SESSION_KEY)["enabled"])
        self.assertFalse(comparison["qualified"])
        self.assertIn("disabled", comparison["normal_validator_rejected"])

    def test_inactive_inventory_still_rejects_command_trust_and_other_hook_drift(self):
        for index, field, value in ((0,"enabled",False), (1,"enabled",True), (1,"command","wrong"),
                (1,"currentHash","wrong"), (0,"trustStatus","untrusted")):
            response = self.hooks(True)
            response["result"]["data"][0]["hooks"][index][field] = value
            with self.subTest(field=field), self.assertRaises(runner.observer.ObservationStopped):
                self.inventory_check(response)
        response = self.hooks(True)
        response["result"]["data"][0]["hooks"].append({"pluginId":"other", "enabled":True})
        with self.assertRaises(runner.observer.ObservationStopped):
            self.inventory_check(response)

    def test_pure_default_and_exact_review_hash_gate(self):
        with patch.object(runner.subprocess, "Popen", side_effect=AssertionError("native forbidden")):
            plan = self.plan()
        self.assertEqual(self.context["config"].read_bytes(), self.original)
        self.assertFalse(self.destination.exists())
        argv = ["--evidence",str(self.destination), "--package-record",str(self.package)]
        for extra, code in (([],0), (["--run"],2), (["--run","--approved-plan-sha256","0"*64],2)):
            with patch.object(runner,"paths",return_value=self.context), patch.object(runner,"execute",side_effect=AssertionError("native forbidden")), patch("builtins.print"):
                self.assertEqual(runner.main(argv + extra), code)
        self.assertEqual(plan["config_change"]["key"], runner.TOOL_KEY)

    def test_ready_then_restart_effect_then_exact_restore_and_native_inventory(self):
        plan, phases = self.plan(), []
        def invoke(value, phase):
            phases.append(phase)
            expected = runner.disable_pre_tool(self.original) if phase == "lost" else self.original
            self.assertEqual(self.context["config"].read_bytes(), expected)
            return self.native_records(value, phase)
        result = runner.execute(plan, invoke)
        self.assertEqual(phases, ["ready", "lost", "restored"])
        self.assertTrue(result["observation_complete"], result)
        self.assertFalse(result["qualified"])
        self.assertIn("enforcement failed/unqualified", result["conclusion"])
        self.assertTrue(result["restoration"]["complete"])
        self.assertEqual(self.context["config"].read_bytes(), self.original)
        self.assertEqual((self.context["repo"] / "governed-target.txt").read_bytes(), runner.AFTER.encode())

    def test_missing_ready_capture_never_disables_or_launches_second_host(self):
        phases = []
        def fail(plan, phase):
            phases.append(phase)
            return {"returncode":1, "outer_cleanup":{"active_processes":0}}
        result = runner.execute(self.plan(), fail)
        self.assertEqual(phases,["ready"])
        self.assertEqual(self.context["config"].read_bytes(), self.original)
        self.assertFalse(result["observation_complete"])

    def test_interrupt_after_exact_write_restores_before_completed_flag(self):
        replace, phases = runner.replace_binding, []
        def interrupted(path, before, after, temporary):
            replace(path,before,after,temporary)
            if temporary == "config.c11-disabled.tmp":
                raise KeyboardInterrupt("after exact write")
        def invoke(plan, phase):
            phases.append(phase)
            return self.native_records(plan,phase)
        with patch.object(runner,"replace_binding",side_effect=interrupted):
            result = runner.execute(self.plan(),invoke)
        self.assertEqual(phases,["ready"])
        self.assertEqual(self.context["config"].read_bytes(),self.original)
        self.assertTrue(result["restoration"]["reconciled_exact_bytes_after_interrupt"])

    def test_foreign_config_is_never_overwritten(self):
        phases = []
        def invoke(plan,phase):
            phases.append(phase)
            if phase == "lost":
                self.context["config"].write_bytes(b"foreign actor")
                raise RuntimeError("foreign drift")
            return self.native_records(plan,phase)
        result = runner.execute(self.plan(),invoke)
        self.assertEqual(phases,["ready","lost"])
        self.assertEqual(self.context["config"].read_bytes(),b"foreign actor")
        self.assertFalse(result["restoration"]["config_restored"])

    def test_rejected_replace_does_not_claim_another_actors_identical_bytes(self):
        def rejected(path,before,after,temporary):
            path.write_bytes(after)  # Synthetic concurrent actor, not this transaction.
            raise ValueError("precondition rejected")
        with patch.object(runner,"replace_binding",side_effect=rejected):
            result = runner.execute(self.plan(),self.native_records)
        self.assertFalse(result["restoration"]["config_restored"])
        self.assertEqual(self.context["config"].read_bytes(),runner.disable_pre_tool(self.original))

    def test_unconfirmed_outer_cleanup_prevents_further_native_run(self):
        phases = []
        def invoke(plan,phase):
            phases.append(phase)
            result = self.native_records(plan,phase)
            if phase == "lost":
                result["outer_cleanup"] = {"active_processes":1}
            return result
        result = runner.execute(self.plan(),invoke)
        self.assertEqual(phases,["ready","lost"])
        self.assertTrue(result["restoration"]["config_restored"])
        self.assertFalse(result["observation_complete"])

    def test_final_target_drift_cannot_pass_from_earlier_effect(self):
        def invoke(plan,phase):
            result = self.native_records(plan,phase)
            if phase == "restored":
                (self.context["repo"] / "outside-scope.txt").write_bytes(b"later unrelated effect\n")
            return result
        result = runner.execute(self.plan(),invoke)
        self.assertFalse(result["final_targets_match_observed_effect"])
        self.assertFalse(result["observation_complete"])

    def test_ready_uses_actual_correlated_thread_response_without_outcome_thread_field(self):
        plan = self.plan()
        self.native_records(plan,"ready")
        path = self.destination / "ready/observations.json"
        self.assertNotIn("thread",runner.read_json(path))
        self.assertTrue(runner.native_result(plan,"ready")["matches_expected"])
        path = self.destination / "ready/transcript.json"
        transcript = runner.read_json(path)
        transcript = [row for row in transcript if not (row["message"].get("id") == "thread-start" and "received_monotonic" in row)]
        self.put(path,runner.encoded(transcript))
        with self.assertRaisesRegex(ValueError,"thread response"):
            runner.native_result(plan,"ready")

    def test_incomplete_or_wrong_context_and_payload_do_not_prove_ready(self):
        plan = self.plan()
        for variant in ("context","payload","cleanup"):
            self.native_records(plan,"ready")
            if variant == "context":
                path = self.destination / "ready/transcript.json"
                data = runner.read_json(path)
                for row in data:
                    if row["message"].get("method") == "hook/completed":
                        row["message"]["params"]["run"]["entries"][0]["text"] = "READY"
            else:
                path = self.destination / "ready/observations.json"
                data = runner.read_json(path)
                if variant == "payload":
                    data["loaded_payload"]["sha256"] = {}
                else:
                    data["cleanup"]["active_processes"] = 1
            self.put(path,runner.encoded(data))
            with self.subTest(variant=variant),self.assertRaises(ValueError):
                runner.native_result(plan,"ready")

    def test_missing_edit_or_wrong_exact_effect_never_becomes_refusal(self):
        plan = self.plan()
        for variant in ("missing-accept","wrong-target","wrong-hash","pretool-hook","late-startup"):
            self.put(self.context["repo"] / "governed-target.txt",plan["one_edit_plan"]["before_utf8"].encode())
            self.native_records(plan,"lost")
            if variant == "wrong-hash":
                path = self.destination / "lost/observations.json"
                data = runner.read_json(path)
                data["after"]["governed-target.txt"] = plan["targets_before_sha256"]["governed-target.txt"]
            else:
                path = self.destination / "lost/transcript.json"
                data = runner.read_json(path)
                if variant == "missing-accept":
                    data = [row for row in data if not ("sent_monotonic" in row and "result" in row["message"])]
                elif variant == "wrong-target":
                    for row in data:
                        item = row["message"].get("params",{}).get("item",{})
                        if item.get("type") == "fileChange":
                            item["changes"][0]["path"] = "outside-scope.txt"
                elif variant == "pretool-hook":
                    data.append({"received_monotonic":time.monotonic(),"message":{"method":"hook/completed","params":{"run":{"eventName":"preToolUse"}}}})
                else:
                    startup = [row for row in data if row["message"].get("method") == "hook/completed"]
                    data = [row for row in data if row not in startup] + startup
            self.put(path,runner.encoded(data))
            with self.subTest(variant=variant),self.assertRaises((ValueError,runner.edit.Stop)):
                runner.native_result(plan,"lost")

    def test_private_entry_rejects_foreign_profile_without_native_import(self):
        with self.assertRaisesRegex(ValueError,"exact accepted disposable"):
            runner.observe(self.plan(),"ready")


if __name__ == "__main__":
    unittest.main()
