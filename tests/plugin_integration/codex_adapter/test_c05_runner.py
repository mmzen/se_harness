"""C05 synthetic boundaries; these fixtures never launch a native host."""
import base64
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).absolute().parent))
import c05_runner as runner


def config_bytes(enabled=b""):
    return (b'\xef\xbb\xbf# preserve owner bytes\r\nmodel = "synthetic"\r\n\r\n' +
        ('[hooks.state."' + runner.TOOL_KEY + '"]\r\ntrusted_hash = "' + runner.TRUST[runner.TOOL_KEY] + '"\r\n\r\n').encode() +
        ('[hooks.state."' + runner.SESSION_KEY + '"]\r\ntrusted_hash = "' + runner.TRUST[runner.SESSION_KEY] + '"\r\n').encode() + enabled +
        b'\r\n[unrelated]\r\nvalue = "keep me" # exact comment\r\n')


class C05RunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.context = {"root":self.root, "repo":self.root / "sandbox/repo with spaces",
            "binding":self.root / "profile/data/binding.json", "config":self.root / "profile/config.toml",
            "runner_python":self.root / "shared016/Scripts/python.exe",
            "live_observer":self.root / "tests/plugin_integration/codex_adapter/live.py",
            "host":self.root / "codex.exe", "schema":self.root / "ClientRequest.json", "cache":self.root / "cache/plugin"}
        self.destination = self.root / "docs/engineering/plugin-integration/evidence/WO-PLG-005/C05/disabled-01"
        self.package = self.root / "package04.json"
        self.original = config_bytes()
        self.put(self.context["config"], self.original)
        self.put(self.context["binding"], runner.encoded({"schema":"verity-codex-binding-v1", "repo":str(self.context["repo"]),
            "environment":str(self.context["runner_python"].parent.parent), "artifact":"WO-PROBE-001", "capture":True,
            "profile":{"host":"0.153.4", "os":"windows", "python":"3.14.6", "evaluator":"0.16.0"},
            "decision":{"id":"DEC-PLG-001", "status":"decided", "option":"prove-supported-route"}}))
        for name in ("governed-target.txt", "outside-scope.txt", "café quoted ' target.txt", "AGENTS.md", "ENGINEERING_HARNESS.md", ".engineering-harness.lock", ".engineering-harness.toml"):
            self.put(self.context["repo"] / name, b"synthetic unchanged\r\n")
        for path in [*runner.boundary.source_paths(self.context)[:-1], self.context["host"], self.context["runner_python"], self.context["schema"]]:
            self.put(path, b"synthetic; never execute")
        self.definitions = {"hooks":{
            "SessionStart":[{"matcher":"startup|resume|compact", "hooks":[{"command":"synthetic startup", "timeout":30}]}],
            "PreToolUse":[{"hooks":[{"command":"synthetic pretool", "timeout":30}]}]}}
        hooks = self.root / "plugins/verity-plane/codex/hooks/hooks.json"
        self.put(hooks, runner.encoded(self.definitions))
        dispatch = self.root / "plugins/verity-plane/codex/dispatch.py"
        self.put(dispatch, b"synthetic dispatcher")
        self.payload = {"hooks/hooks.json":runner.file_hash(hooks), "scripts/codex-dispatch.py":runner.file_hash(dispatch)}
        self.put(self.package, runner.encoded({"archive_sha256":runner.boundary.PACKAGE_SHA, "payload":self.payload}))
        self.loaded = self.context["cache"] / "package04"
        self.put(self.loaded / "hooks/hooks.json", hooks.read_bytes())

    @staticmethod
    def put(path, raw):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    def plan(self):
        return runner.build_plan(self.destination, self.package, self.context)

    def hooks(self, enabled=False):
        hooks = []
        for event, native, key, value in (("SessionStart", "sessionStart", runner.SESSION_KEY, enabled),
                                           ("PreToolUse", "preToolUse", runner.TOOL_KEY, True)):
            definition = self.definitions["hooks"][event][0]
            hooks.append({"eventName":native, "pluginId":runner.PLUGIN, "key":key,
                "enabled":value, "trustStatus":"trusted", "currentHash":runner.TRUST[key], "async":False,
                "handlerType":"command", "command":definition["hooks"][0]["command"], "timeoutSec":30,
                "matcher":definition.get("matcher"), "sourcePath":str(self.loaded / "hooks/hooks.json")})
        return {"result":{"data":[{"cwd":str(self.context["repo"]), "hooks":hooks, "errors":[], "warnings":[]}]}}

    def inventory_check(self, response):
        return runner.inactive_bindings(response, self.context["repo"], self.context["cache"], self.definitions, self.payload["hooks/hooks.json"])

    def native_records(self, plan, phase):
        folder = Path(plan["evidence"]) / phase
        snapshot = {name:{"sha256":sha,"bytes":"synthetic unchanged\n"} for name, sha in plan["targets_before_sha256"].items()}
        observed = {"hooks":self.hooks(phase == "restored"), "before":snapshot, "after":snapshot,
            "readers_complete":True, "cleanup":{"active_processes":0},
            "loaded_payload":{"root":str(self.loaded), "sha256":plan["package_payload"]},
            "package_record_sha256":plan["package_record_sha256"]}
        transcript = []
        if phase == "disabled":
            observed["thread_id"] = "synthetic-thread"
            observed["turn"] = {"method":"turn/completed", "params":{"threadId":"synthetic-thread", "turn":{"status":"completed", "error":None}}}
            transcript = [{"sent_monotonic":1, "message":{"method":"thread/start", "params":{
                "cwd":plan["repo"], "sandbox":"read-only", "approvalPolicy":"on-request", "ephemeral":False}}},
                {"sent_monotonic":2, "message":{"method":"turn/start", "params":{"threadId":"synthetic-thread",
                    "input":[{"type":"text", "text":runner.PROMPT}]}}},
                {"received_monotonic":3, "message":observed["turn"]}]
        self.put(folder / "observations.json", runner.encoded(observed))
        self.put(folder / "transcript.json", runner.encoded(transcript))
        self.put(folder / "dispatch.jsonl", b"")
        return subprocess.CompletedProcess([], 0, b"synthetic observer\n", b"")

    def test_config_preserves_every_original_byte_except_one_inserted_flag(self):
        original = config_bytes()
        selected = runner.disable_session_start(original)
        self.assertEqual(selected.replace(b"enabled = false\r\n", b"", 1), original)
        before, after = tomllib.loads(original.decode("utf-8-sig")), tomllib.loads(selected.decode("utf-8-sig"))
        before["hooks"]["state"][runner.SESSION_KEY]["enabled"] = False
        self.assertEqual(before, after)

    def test_existing_true_token_preserves_comments_bom_and_crlf(self):
        original = config_bytes(b"enabled  =  true # preserve comment\r\n")
        selected = runner.disable_session_start(original)
        self.assertEqual(selected, original.replace(b"true # preserve comment", b"false # preserve comment"))

    def test_disabled_or_changed_trust_and_ambiguous_table_rejected(self):
        for raw in (config_bytes(b"enabled = false\r\n"), config_bytes().replace(runner.TRUST[runner.TOOL_KEY].encode(), b"wrong"),
                    config_bytes().replace(('"' + runner.SESSION_KEY + '"').encode(), ("'" + runner.SESSION_KEY + "'").encode())):
            with self.subTest(raw=raw[-60:]), self.assertRaises(ValueError):
                runner.disable_session_start(raw)

    def test_inactive_inventory_is_actual_and_normal_rejection_retained(self):
        response = self.hooks()
        original = copy.deepcopy(response)
        actual, validation = self.inventory_check(response)
        self.assertEqual(response, original)
        self.assertFalse(next(h for h in actual if h["eventName"] == "sessionStart")["enabled"])
        self.assertIn("disabled", validation["normal_validator_rejected"])

    def test_wrong_enabled_hash_and_extra_active_hook_are_rejected(self):
        mutations = [(0, "enabled", True), (1, "enabled", False), (0, "trustStatus", "untrusted"),
                     (0, "currentHash", "wrong"), (1, "command", "changed")]
        for index, key, value in mutations:
            response = self.hooks()
            response["result"]["data"][0]["hooks"][index][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(runner.observer.ObservationStopped):
                self.inventory_check(response)
        response = self.hooks()
        response["result"]["data"][0]["hooks"].append({"pluginId":"other", "enabled":True})
        with self.assertRaises(runner.observer.ObservationStopped):
            self.inventory_check(response)

    def test_default_preflight_has_no_mutation_or_native_process(self):
        with patch.object(runner.subprocess, "run", side_effect=AssertionError("native forbidden")):
            plan = self.plan()
        self.assertEqual(self.context["config"].read_bytes(), self.original)
        self.assertEqual(base64.b64decode(plan["config_before_base64"]), self.original)
        self.assertFalse(self.destination.exists())

    def test_default_cli_and_unreviewed_run_never_execute(self):
        argv = ["runner", "--evidence", str(self.destination), "--package-record", str(self.package)]
        for extra, expected in (([], 0), (["--run"], 2)):
            with patch.object(sys, "argv", argv + extra), patch.object(runner, "paths", return_value=self.context), \
                    patch.object(runner, "execute", side_effect=AssertionError("native forbidden")), patch("builtins.print"):
                self.assertEqual(runner.main(), expected)
        self.assertFalse(self.destination.exists())

    def test_existing_evidence_and_changed_config_fail_before_mutation(self):
        plan = self.plan()
        self.context["config"].write_bytes(self.original + b"# concurrent\r\n")
        with self.assertRaisesRegex(ValueError, "config differs"):
            runner.execute(plan, lambda *_: self.fail("observer forbidden"))
        self.assertFalse(self.destination.exists())
        self.context["config"].write_bytes(self.original)
        self.destination.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "fresh C05"):
            self.plan()

    def test_exact_config_restored_before_inventory_confirmation(self):
        plan = self.plan()
        phases = []
        def invoke(selected, phase):
            phases.append(phase)
            expected = runner.disable_session_start(self.original) if phase == "disabled" else self.original
            self.assertEqual(self.context["config"].read_bytes(), expected)
            return self.native_records(selected, phase)
        result = runner.execute(plan, invoke)
        self.assertEqual(phases, ["disabled", "restored"])
        self.assertEqual(result["conclusion"], "pass")
        self.assertTrue(result["restoration"]["complete"])
        self.assertEqual(self.context["config"].read_bytes(), self.original)
        raw = runner.read_json(self.destination / "config-before.raw.json")
        self.assertEqual(base64.b64decode(raw["bytes"]), self.original)

    def test_unknown_cleanup_restores_config_without_another_native_launch(self):
        plan = self.plan()
        calls = []
        def failed(_, phase):
            calls.append(phase)
            raise RuntimeError("synthetic observer failure")
        result = runner.execute(plan, failed)
        self.assertEqual(calls, ["disabled"])
        self.assertEqual(self.context["config"].read_bytes(), self.original)
        self.assertTrue(result["restoration"]["config_restored"])
        self.assertFalse(result["restoration"]["inventory_confirmed"])

    def test_concurrent_config_is_preserved_and_no_inventory_launched(self):
        plan = self.plan()
        calls = []
        def changed(_, phase):
            calls.append(phase)
            self.context["config"].write_bytes(b"another actor")
            raise RuntimeError("synthetic collision")
        result = runner.execute(plan, changed)
        self.assertEqual(calls, ["disabled"])
        self.assertEqual(self.context["config"].read_bytes(), b"another actor")
        self.assertFalse(result["restoration"]["complete"])

    def test_absence_alone_is_not_pass_without_actual_readonly_turn(self):
        plan = self.plan()
        self.native_records(plan, "disabled")
        self.assertTrue(runner.native_result(plan, "disabled")["matches_expected"])
        self.put(self.destination / "disabled/transcript.json", b"[]\n")
        self.assertFalse(runner.native_result(plan, "disabled")["matches_expected"])

    def test_outcome_claim_without_matching_received_turn_is_not_evidence(self):
        plan = self.plan()
        self.native_records(plan, "disabled")
        path = self.destination / "disabled/transcript.json"
        transcript = runner.read_json(path)
        self.put(path, runner.encoded([row for row in transcript if "received_monotonic" not in row]))
        self.assertFalse(runner.native_result(plan, "disabled")["matches_expected"])

    def test_session_receipt_or_dispatch_append_rejects_disabled_result(self):
        plan = self.plan()
        self.native_records(plan, "disabled")
        path = self.destination / "disabled/transcript.json"
        transcript = runner.read_json(path)
        transcript.append({"received_monotonic":3,"message":{"method":"hook/completed","params":{"run":{"eventName":"sessionStart"}}}})
        self.put(path, runner.encoded(transcript))
        self.assertFalse(runner.native_result(plan, "disabled")["matches_expected"])
        self.native_records(plan, "disabled")
        self.put(Path(plan["dispatch_audit"]["path"]), b"unexpected dispatch\n")
        self.assertFalse(runner.native_result(plan, "disabled")["matches_expected"])

    def test_restoration_inventory_failure_does_not_claim_complete(self):
        plan = self.plan()
        def invoke(selected, phase):
            result = self.native_records(selected, phase)
            if phase == "restored":
                path = self.destination / "restored/observations.json"
                observed = runner.read_json(path)
                observed["hooks"] = self.hooks(False)
                self.put(path, runner.encoded(observed))
            return result
        result = runner.execute(plan, invoke)
        self.assertEqual(result["conclusion"], "fail")
        self.assertTrue(result["restoration"]["config_restored"])
        self.assertFalse(result["restoration"]["inventory_confirmed"])

    def test_native_inventory_config_drift_is_detected_after_confirmation(self):
        plan = self.plan()
        def invoke(selected, phase):
            result = self.native_records(selected, phase)
            if phase == "restored":
                self.context["config"].write_bytes(self.original + b"# changed by observer\r\n")
            return result
        result = runner.execute(plan, invoke)
        self.assertFalse(result["restoration"]["config_restored"])
        self.assertFalse(result["restoration"]["complete"])

    def test_private_observer_rejects_another_profile_before_import_or_launch(self):
        plan = self.plan()
        with self.assertRaisesRegex(ValueError, "exact accepted disposable paths"):
            runner.observe(plan, "disabled")


if __name__ == "__main__":
    unittest.main()
