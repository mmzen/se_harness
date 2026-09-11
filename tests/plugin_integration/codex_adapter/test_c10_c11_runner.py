"""Pure synthetic output-fault boundaries; never install or start a host."""
import base64
import copy
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).absolute().parent))
import c10_c11_runner as runner
import c10_c11_fault_sitecustomize as fault


class OutputFaultTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.repo, self.runtime = self.root / "repo", self.root / "owned"
        self.one_edit = {"schema":"verity-one-edit-v1", "target":"governed-target.txt", "before_utf8":"before\r\n", "after_utf8":"after\n"}
        self.config = {"schema":"verity-native-output-fault-v1", "case":"empty", "runtime":str(self.runtime),
            "python":str(self.runtime / "Scripts/python.exe"), "cwd":str(self.repo),
            "selector":[str(self.runtime / "Scripts/python.exe"), "-I", "-B", str(self.root / "cache/scripts/codex-dispatch.py"), "--data",str(self.root / "data"),"--event","PreToolUse"],
            "stall_seconds":90, "plugin_root":str(self.root / "cache"), "plugin_data":str(self.root / "data"),
            "one_edit_plan":self.one_edit, "one_edit_plan_sha256":fault.digest(fault.encoded(self.one_edit))}
        self.event = {"hook_event_name":"PreToolUse", "tool_name":"apply_patch", "cwd":str(self.repo),
            "tool_input":{"command":"*** Begin Patch\n*** Update File: governed-target.txt\n@@\n-before\n+after\n*** End Patch\n"}}

    def selected(self, config=None, **changes):
        config = config or self.config
        values = {"argv":config["selector"], "executable":config["python"], "prefix":config["runtime"],
            "cwd":config["cwd"], "plugin_root":config["plugin_root"], "plugin_data":config["plugin_data"]}
        values.update(changes)
        return fault.selected(config, **values)

    def case(self, mode="empty", effect=False, blocked=False):
        config = {**self.config, "case":mode}
        raw = fault.encoded(self.event)
        before = {name:"before-"+name for name in runner.edit.TARGETS}
        after = {**before, "governed-target.txt":"after"}
        body = b"complete synthetic context"
        plan = {"case":mode, "fault_config":config,"fault_config_sha256":fault.digest(fault.encoded(config)),
            "one_edit_plan":self.one_edit,"one_edit_plan_sha256":fault.digest(fault.encoded(self.one_edit)),
            "repo":str(self.repo),"plugin_root":config["plugin_root"],"targets_before_sha256":before,"targets_expected_after_sha256":after,
            "expected_governance_body_base64":base64.b64encode(body).decode(),"expected_governance_body_sha256":fault.digest(body)}
        marker = {"role":"pre-tool-dispatcher","pid":123,"creation_filetime":456,"config_sha256":plan["fault_config_sha256"],
            "argv":config["selector"],"python":config["python"],"prefix":config["runtime"],"cwd":config["cwd"],
            "plugin_root":config["plugin_root"],"plugin_data":config["plugin_data"],"case":mode,
            "dispatcher_source_executed":False,"shared_handler_started":False,"input_hex":raw.hex(),
            "input_sha256":fault.digest(raw),"native_input":self.event,"started_monotonic":2.1}
        native = {"thread_id":"t","turn_id":"u","before":before,"after":after if effect else before,
            "acceptance_sent":effect,"completed_file_change_items":1 if effect else 0,"native_hook_blocked":blocked,
            "observation_complete":True,
            "readers_complete":True,"cleanup":{"active_processes":0},"acceptance_sent_monotonic":33 if effect else None}
        context = body.decode()+"END VERIFIED GOVERNANCE "+fault.digest(body)+"; complete context delivered.\n"
        session = {"eventName":"sessionStart","status":"completed","sourcePath":str(self.root / "cache/hooks/hooks.json"),"entries":[{"kind":"context","text":context}]}
        tool = {"eventName":"preToolUse","status":"blocked" if blocked else "failed" if mode=="hang" else "completed",
            "id":"hook-1","sourcePath":str(self.root / "cache/hooks/hooks.json"),"durationMs":30010 if mode=="hang" else 12,
            "entries":[{"kind":"error","text":"Command timed out"}] if mode=="hang" else []}
        transcript = [{"received_monotonic":1,"message":{"method":"hook/completed","params":{"threadId":"t","run":session}}},
            {"received_monotonic":32,"message":{"method":"hook/completed","params":{"threadId":"t","turnId":"u","run":tool}}}]
        transcript.append({"received_monotonic":2,"message":{"method":"hook/started","params":{"threadId":"t","turnId":"u","run":{**tool,"status":"running"}}}})
        if effect:transcript.append({"received_monotonic":34,"message":{"method":"item/completed","params":{"threadId":"t","turnId":"u","item":{"type":"fileChange","status":"completed"}}}})
        output = None if mode=="hang" else {"stdout_hex":fault.output_bytes(mode).hex(),"stdout_sha256":fault.digest(fault.output_bytes(mode)),"exit_status":0,"finished_monotonic":2.2}
        return plan,native,transcript,marker,output

    def test_only_full_dispatcher_argv_and_plugin_environment_select(self):
        self.assertTrue(self.selected())
        for values in ({"argv":self.config["selector"][:-1]+["SessionStart"]}, {"argv":[self.config["python"],"-I","-B","-m","se_harness","identity"]},
                       {"cwd":str(self.repo.parent)}, {"prefix":"other"}, {"plugin_root":"other"}, {"plugin_data":"other"}):
            with self.subTest(values=values):
                self.assertFalse(self.selected(**values))

    def test_patch_requires_exact_target_and_full_before_after(self):
        self.assertTrue(fault.patch_matches(self.config,self.event))
        for old,new in (("governed-target.txt","outside-scope.txt"),("-before","-other"),("+after","+other"),("@@\n","@@ extra\n"),("*** End Patch","*** Delete File: outside-scope.txt\n*** End Patch")):
            event=copy.deepcopy(self.event)
            event["tool_input"]["command"]=event["tool_input"]["command"].replace(old,new)
            with self.subTest(new=new):self.assertFalse(fault.patch_matches(self.config,event))

    def test_duplicate_json_and_unknown_output_mode_rejected(self):
        with self.assertRaises(ValueError):fault.decode(b'{"case":"empty","case":"hang"}')
        with self.assertRaises(ValueError):fault.output_bytes("hang")
        self.assertEqual(fault.output_bytes("empty"),b"")
        self.assertEqual(fault.output_bytes("truncated"),b'{"hookSpecificOutput":')

    def test_empty_or_invalid_can_record_one_actual_fail_open_effect(self):
        for mode in ("empty","truncated"):
            result=runner.assess(*self.case(mode,effect=True))
            self.assertTrue(result["observation_complete"])
            self.assertEqual(result["actual_effect_count"],1)
            self.assertFalse(result["required_native_refusal_observed"])
            self.assertIn("unqualified",result["enforcement_result"])

    def test_host_blocked_status_is_not_supported_handler_denial(self):
        result=runner.assess(*self.case("empty",blocked=True))
        self.assertTrue(result["native_blocking_control_observed"])
        self.assertFalse(result["supported_handler_denial_observed"])
        self.assertFalse(result["required_native_refusal_observed"])

    def test_hang_requires_explicit_host_timeout_and_full_duration(self):
        values=self.case("hang")
        self.assertTrue(runner.assess(*values)["observation_complete"])
        values[2][1]["message"]["params"]["run"]["entries"]=[]
        self.assertFalse(runner.assess(*values)["observation_complete"])
        values=self.case("hang")
        values[2][1]["message"]["params"]["run"]["durationMs"]=25000
        self.assertFalse(runner.assess(*values)["observation_complete"])

    def test_wrong_patch_and_no_native_receipt_do_not_count(self):
        values=self.case()
        values[3]["native_input"]={**self.event,"tool_name":"Bash"}
        self.assertFalse(runner.assess(*values)["observation_complete"])
        values=self.case()
        values[2].pop(1)
        self.assertFalse(runner.assess(*values)["observation_complete"])

    def test_effect_without_one_edit_acceptance_is_unavailable(self):
        values=self.case(effect=True)
        values[1]["acceptance_sent"]=False
        self.assertFalse(runner.assess(*values)["observation_complete"])

    def test_zero_hash_change_conflicting_with_completed_effect_is_unavailable(self):
        values=self.case()
        values[1]["completed_file_change_items"]=1
        values[1]["acceptance_sent"]=True
        result=runner.assess(*values)
        self.assertFalse(result["observation_complete"])
        self.assertIsNone(result["actual_effect_count"])
        self.assertEqual(result["hash_derived_effect_count"],0)

    def test_incomplete_observer_and_unconfirmed_cleanup_are_unavailable(self):
        values=self.case()
        values[1]["observation_complete"]=False
        self.assertFalse(runner.assess(*values)["observation_complete"])
        values[1]["observer_stopped"]="turn ended without a complete correlated native file-change item"
        self.assertTrue(runner.assess(*values)["observation_complete"])
        values[1]["cleanup"]["descendant_cleanup_unconfirmed"]=True
        self.assertFalse(runner.assess(*values)["observation_complete"])

    def test_stale_marker_or_session_thread_and_missing_started_receipt_rejected(self):
        values=self.case()
        values[3]["started_monotonic"]=.5
        self.assertFalse(runner.assess(*values)["observation_complete"])
        values=self.case()
        values[2][0]["message"]["params"]["threadId"]="another-thread"
        self.assertFalse(runner.assess(*values)["observation_complete"])
        values=self.case()
        values[2].pop(2)
        self.assertFalse(runner.assess(*values)["observation_complete"])
        values=self.case(effect=True)
        values[1]["after"]={**values[1]["after"],"outside-scope.txt":"changed"}
        self.assertFalse(runner.assess(*values)["observation_complete"])

    def test_final_cleanup_config_and_native_after_are_independent_gates(self):
        plan=self.case()[0]
        outcome={"observation_complete":True,"outer_cleanup":{"active_processes":0},"binding_restored":True,
            "fault_config_removed":True,"runtime_inventory_restored":True,"profile_config_unchanged":True,
            "targets_after_sha256":plan["targets_before_sha256"],"native_after_sha256":plan["targets_before_sha256"],"natural_fault_return":False}
        self.assertTrue(runner.final_gates(outcome,plan))
        for key,value in (("outer_cleanup",{"descendant_cleanup_unconfirmed":True}),("profile_config_unchanged",False),
                          ("native_after_sha256",plan["targets_expected_after_sha256"]),("natural_fault_return",True),
                          ("outer_cleanup",{"active_processes":0,"descendant_cleanup_unconfirmed":True}),("cleanup_error","failed")):
            with self.subTest(key=key):self.assertFalse(runner.final_gates({**outcome,key:value},plan))

    def test_rejected_binding_replace_cannot_restore_another_actors_bytes(self):
        binding=self.root/"binding.json"
        binding.write_bytes(b"selected")
        config=self.root/"fault.json"
        config.write_bytes(b"ours")
        result=runner.restore(binding,b"original",b"selected",config,b"ours",{"binding_started":True,"binding_rejected":True,"config_write_started":True})
        self.assertFalse(result["binding_restored"])
        self.assertEqual(binding.read_bytes(),b"selected")
        self.assertTrue(result["fault_config_removed"])

    def test_interrupted_attributable_binding_publication_restores_exact_bytes(self):
        binding=self.root/"binding.json"
        binding.write_bytes(b"selected")
        result=runner.restore(binding,b"original\r\n",b"selected",self.root/"absent-config",b"config",{"binding_started":True})
        self.assertTrue(result["binding_restored"])
        self.assertEqual(binding.read_bytes(),b"original\r\n")


if __name__ == "__main__":
    unittest.main()
