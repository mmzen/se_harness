"""Synthetic boundary tests only: none of these records are native acceptance."""
import base64
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).absolute().parent))
import c08_runner as runner


class C08RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name).resolve()
        self.context = {
            "root":root, "repo":root / "sandbox/repo with spaces",
            "binding":root / "profile/data/binding.json",
            "owned_runtime":root / "sandbox/C08 owned runtime 016",
            "missing_runtime":root / "sandbox/C08 never prepared runtime",
            "wrong_runtime":root / "shared-017",
            "runner_python":root / "shared-016/Scripts/python.exe",
            "live_observer":root / "tests/plugin_integration/codex_adapter/live.py"}
        self.package = root / "package04.json"
        self.destination = root / "docs/engineering/plugin-integration/evidence/WO-PLG-005/C08/case01"
        self.original = {
            "schema":"verity-codex-binding-v1", "repo":str(self.context["repo"]),
            "environment":str(self.context["runner_python"].parent.parent),
            "artifact":"WO-PROBE-001", "capture":True,
            "profile":{"host":"0.153.4", "os":"windows", "python":"3.14.6", "evaluator":"0.16.0"},
            "decision":{"id":"DEC-PLG-001", "status":"decided", "option":"prove-supported-route"}}
        self.original_bytes = b"\xef\xbb\xbf" + json.dumps(self.original, indent=1).encode("utf8") + b"\r\n"
        self.put(self.context["binding"], self.original_bytes)
        for name in ("governed-target.txt", "outside-scope.txt", "café quoted ' target.txt"):
            self.put(self.context["repo"] / name, b"synthetic initial\r\n")
        self.put(self.context["repo"] / "AGENTS.md", b"owner\r\n<!-- se-harness:begin -->\r\nmanaged\r\n<!-- se-harness:end -->\r\n")
        self.put(self.context["repo"] / "ENGINEERING_HARNESS.md", b"synthetic router\r\n")
        for name in (".engineering-harness.lock", ".engineering-harness.toml"):
            self.put(self.context["repo"] / name, b"synthetic")
        for path in [*runner.source_paths(self.context)[:-1], self.context["runner_python"],
                     self.context["owned_runtime"] / "Scripts/python.exe",
                     self.context["wrong_runtime"] / "Scripts/python.exe"]:
            self.put(path, b"synthetic; never execute")
        payload = {}
        for packaged, source in (("hooks/hooks.json", "hooks/hooks.json"), ("scripts/codex-dispatch.py", "dispatch.py")):
            value = ("synthetic " + packaged).encode()
            self.put(root / "plugins/verity-plane/codex" / source, value)
            payload[packaged] = runner.digest(value)
        self.put(self.package, runner.encoded({"archive_sha256":runner.PACKAGE_SHA, "payload":payload}))

    @staticmethod
    def put(path, raw):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    def plan(self, case="missing", ready=None):
        return runner.build_plan(case, self.destination, self.package, ready, self.context)

    def ready_evidence(self):
        path = self.destination.parent / "ready/observations.json"
        self.put(path, runner.encoded({"case":"runtime-ready", "conclusion":"pass", "plan":{
            "selected_environment":str(self.context["owned_runtime"]),
            "owned_python_sha256":runner.file_hash(self.context["owned_runtime"] / "Scripts/python.exe")},
            "assessment":{"matches_expected":True}, "restoration":{"complete":True}}))
        return path

    def native_records(self, plan, kind="setup"):
        """Write deliberately synthetic receipts for assessor unit tests."""
        destination = Path(plan["evidence"]) / "live"
        loaded = self.context["root"] / "cache/checked-package04"
        context = "Verity Plane UNREADY: Setup required: selected interpreter absent; no Python invoked."
        if kind == "ready":
            context = base64.b64decode(plan["expected_body_base64"]).decode() + "END VERIFIED GOVERNANCE " + plan["expected_body_sha256"] + "; complete context delivered.\n"
        elif kind == "wrong":
            context = "Verity Plane governance context is UNREADY. Stop governed work. released evaluator identity refused"
        receipt = {"eventName":"sessionStart", "status":"completed", "sourcePath":str(loaded / "hooks/hooks.json"),
                   "entries":[{"kind":"context", "text":context}]}
        snapshot = {name:{"sha256":sha, "bytes":"synthetic initial\n"} for name, sha in plan["targets_before_sha256"].items()}
        observations = {"before":snapshot, "after":snapshot, "readers_complete":True,
                        "cleanup":{"active_processes":0}, "loaded_payload":{"root":str(loaded), "sha256":plan["package_payload"]},
                        "package_record_sha256":plan["package_record_sha256"]}
        self.put(destination / "observations.json", runner.encoded(observations))
        self.put(destination / "transcript.json", runner.encoded([{"received_monotonic":1,
            "message":{"method":"hook/completed", "params":{"run":receipt}}}]))
        dispatch = b""
        if kind in ("ready", "wrong"):
            environment = plan["selected_environment"]
            argv = [str(Path(environment) / "Scripts/python.exe"), "-I", "-B", str(loaded / "scripts/session-context.py"),
                "--repo",plan["repo"], "--environment",environment, "--version","0.16.0",
                "--payload-sha256","51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c",
                "--archive-sha256","a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae",
                "--host","codex", "--context-limit","16000", "--read-limit","0"]
            result = {"argv":argv, "exit_status":0, "status":"handler-output-returned",
                      "stdout":json.dumps({"hookSpecificOutput":{"additionalContext":context}}),
                      "stderr":json.dumps({"checks":[{"argv":[argv[0], "-I", "-B", "-m", "se_harness", "identity"],
                          "result":{"passed":False, "harness_version":"0.17.0"}}] if kind == "wrong" else []})}
            dispatch = (json.dumps(result) + "\n").encode()
        self.put(destination / "dispatch.jsonl", dispatch)
        log = Path(plan["dispatch_audit"]["path"])
        existing = log.read_bytes() if log.exists() else b""
        self.put(log, existing + dispatch)
        return subprocess.CompletedProcess(plan["argv"], 0, b"synthetic observer\n", b"")

    def test_default_preflight_does_not_mutate_or_spawn_and_retains_exact_bytes(self):
        with patch.object(runner.subprocess, "run", side_effect=AssertionError("process forbidden")):
            plan = self.plan()
        self.assertFalse(self.destination.exists())
        self.assertEqual(self.context["binding"].read_bytes(), self.original_bytes)
        self.assertEqual(base64.b64decode(plan["binding_before_base64"]), self.original_bytes)
        body = base64.b64decode(plan["expected_body_base64"])
        self.assertIn(b"managed\r\n<!-- se-harness:end -->\n\nENGINEERING", body)
        self.assertEqual(plan["binding_selected"]["environment"], str(self.context["missing_runtime"]))

    def test_default_cli_never_calls_execute(self):
        with patch.object(sys, "argv", ["runner", "--case", "missing", "--evidence", str(self.destination), "--package-record", str(self.package)]), \
                patch.object(runner, "paths", return_value=self.context), \
                patch.object(runner, "execute", side_effect=AssertionError("mutation forbidden")), \
                patch("builtins.print"):
            self.assertEqual(runner.main(), 0)
        self.assertFalse(self.destination.exists())

    def test_run_rejects_unreviewed_plan_without_mutation(self):
        with patch.object(sys, "argv", ["runner", "--case", "missing", "--evidence", str(self.destination), "--package-record", str(self.package), "--run"]), \
                patch.object(runner, "paths", return_value=self.context), patch("builtins.print"):
            self.assertEqual(runner.main(), 2)
        self.assertEqual(self.context["binding"].read_bytes(), self.original_bytes)
        self.assertFalse(self.destination.exists())

    def test_rejects_existing_evidence_and_non_c08_destination(self):
        self.destination.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "fresh C08"):
            self.plan()
        with self.assertRaisesRegex(ValueError, "fresh C08"):
            runner.build_plan("missing", self.context["root"] / "elsewhere", self.package, context=self.context)

    def test_rejects_relative_traversal_and_hardlinked_file(self):
        for path in (Path("relative"), self.context["root"] / ".." / "outside"):
            with self.assertRaises(ValueError):
                runner.ordinary(path)
        alias = self.context["binding"].with_name("hardlink.json")
        os.link(self.context["binding"], alias)
        with self.assertRaisesRegex(ValueError, "single-link"):
            self.plan()

    def test_rejects_reparse_ancestor_without_following_it(self):
        path = self.context["binding"]
        original = Path.lstat
        class Reparse:
            st_mode = 0
            st_file_attributes = 0x400
        def lstat(value, *args, **kwargs):
            return Reparse() if value == path.parent else original(value, *args, **kwargs)
        with patch.object(Path, "lstat", lstat), self.assertRaisesRegex(ValueError, "reparse"):
            runner.ordinary(path)

    def test_removed_requires_ready_receipt_for_same_owned_python(self):
        with self.assertRaisesRegex(ValueError, "prior owned-runtime"):
            self.plan("removed")
        ready = self.ready_evidence()
        self.assertEqual(self.plan("removed", ready)["expected_result"], "setup-required")
        self.put(self.context["owned_runtime"] / "Scripts/python.exe", b"changed")
        with self.assertRaisesRegex(ValueError, "does not prove"):
            self.plan("removed", ready)

    def test_rename_rejects_sibling_escape_and_changed_bytes(self):
        python = self.context["owned_runtime"] / "Scripts/python.exe"
        with self.assertRaisesRegex(ValueError, "exact owned"):
            runner.rename_owned(python, python.parent.parent / "python.c08-removed.exe", self.context["owned_runtime"], runner.file_hash(python))
        with self.assertRaisesRegex(ValueError, "bytes changed"):
            runner.rename_owned(python, python.with_name("python.c08-removed.exe"), self.context["owned_runtime"], "0" * 64)

    def test_changed_binding_target_or_source_stops_before_mutation(self):
        for target in (self.context["binding"], self.context["repo"] / "outside-scope.txt", self.context["live_observer"]):
            with self.subTest(target=target):
                plan = self.plan()
                original = target.read_bytes()
                target.write_bytes(original + b"changed")
                try:
                    with self.assertRaisesRegex(ValueError, "changed after preflight"):
                        runner.execute(plan, lambda _: self.fail("observer forbidden"))
                    self.assertFalse(self.destination.exists())
                finally:
                    target.write_bytes(original)

    def test_observer_exception_restores_literal_owned_python_and_raw_binding(self):
        plan = self.plan("removed", self.ready_evidence())
        def failed_observer(selected):
            self.assertFalse(Path(selected["owned_python"]).exists())
            self.assertTrue(Path(selected["removed_python"]).is_file())
            raise RuntimeError("synthetic observer failure")
        result = runner.execute(plan, failed_observer)
        self.assertEqual(result["conclusion"], "unavailable")
        self.assertTrue(result["restoration"]["complete"])
        self.assertEqual(self.context["binding"].read_bytes(), self.original_bytes)
        retained = runner.read_json(self.destination / "binding-before.raw.json")
        self.assertEqual(base64.b64decode(retained["bytes"]), self.original_bytes)

    def test_interpreter_restoration_failure_still_restores_binding(self):
        plan = self.plan("removed", self.ready_evidence())
        real_rename = runner.rename_owned
        def rename(source, *args):
            if Path(source).name == "python.c08-removed.exe":
                raise OSError("synthetic restore failure")
            return real_rename(source, *args)
        with patch.object(runner, "rename_owned", rename):
            result = runner.execute(plan, lambda _: (_ for _ in ()).throw(RuntimeError("observer failed")))
        self.assertEqual(result["conclusion"], "fail")
        self.assertTrue(result["restoration"]["binding_restored"])
        self.assertFalse(result["restoration"]["owned_python_restored"])
        self.assertEqual(self.context["binding"].read_bytes(), self.original_bytes)

    def test_atomic_replace_failure_keeps_original_binding(self):
        plan = self.plan()
        with patch.object(runner.os, "replace", side_effect=OSError("synthetic replace failure")):
            result = runner.execute(plan, lambda _: self.fail("observer forbidden"))
        self.assertTrue(result["restoration"]["complete"])
        self.assertEqual(self.context["binding"].read_bytes(), self.original_bytes)
        self.assertFalse(self.context["binding"].with_name("binding.c08-selected.tmp").exists())

    def test_concurrent_binding_is_preserved_and_restoration_reported_failed(self):
        plan = self.plan()
        def changed(_):
            self.context["binding"].write_bytes(b"another actor")
            raise RuntimeError("synthetic collision")
        result = runner.execute(plan, changed)
        self.assertFalse(result["restoration"]["complete"])
        self.assertEqual(self.context["binding"].read_bytes(), b"another actor")

    def test_missing_needs_native_guidance_and_zero_dispatch_append(self):
        plan = self.plan()
        result = runner.execute(plan, self.native_records)
        self.assertEqual(result["conclusion"], "pass")
        transcript_path = self.destination / "live/transcript.json"
        transcript = runner.read_json(transcript_path)
        transcript[0]["message"]["params"]["run"]["entries"] = []
        self.put(transcript_path, runner.encoded(transcript))
        self.assertFalse(runner.assess(plan)["matches_expected"])

    def test_wrong_identity_is_logical_unready_with_shared_exit_zero(self):
        plan = self.plan("wrong017")
        result = runner.execute(plan, lambda selected:self.native_records(selected, "wrong"))
        self.assertEqual(result["conclusion"], "pass")
        self.assertTrue(result["assessment"]["wrong_identity_observed"])
        self.assertFalse(result["assessment"]["setup_required"])

    def test_ready_requires_exact_native_context_arguments_audit_and_effects(self):
        plan = self.plan("runtime-ready")
        self.native_records(plan, "ready")
        self.assertTrue(runner.assess(plan)["matches_expected"])
        observed_path = self.destination / "live/observations.json"
        initial = observed_path.read_bytes()
        for field, value in (("readers_complete", False), ("package_record_sha256", "wrong"), ("observer_stopped", "approval requested")):
            observed = json.loads(initial)
            observed[field] = value
            self.put(observed_path, runner.encoded(observed))
            self.assertFalse(runner.assess(plan)["matches_expected"])
        self.put(observed_path, initial)
        observed = json.loads(initial)
        observed["before"]["outside-scope.txt"]["sha256"] = "wrong"
        observed["after"] = observed["before"]
        self.put(observed_path, runner.encoded(observed))
        self.assertFalse(runner.assess(plan)["matches_expected"])
        self.put(observed_path, initial)
        Path(plan["dispatch_audit"]["path"]).write_bytes(b"unrecorded append")
        self.assertFalse(runner.assess(plan)["matches_expected"])


if __name__ == "__main__":
    unittest.main()
