"""Pure adversarial observer tests. No Codex process, network or native hook."""
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import queue
import tempfile
import types
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("one_edit_observer", Path(__file__).with_name("edit_observer.py"))
edit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edit)


class GateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.repo = Path(self.directory.name)
        self.plan = edit.Plan(self.repo, {"schema": "verity-one-edit-v1", "target": "governed-target.txt",
                                         "before_utf8": "old\n", "after_utf8": "new\n"})
        self.plan.target.write_bytes(self.plan.before)
        self.gate = edit.EditGate(self.plan)
        self.gate.thread = "thread"
        self.gate.turn_requested = True
        self.gate.bind_turn("thread", "turn")
        self.changes = [{"path": str(self.plan.target), "kind": {"type": "update"},
                         "diff": "@@ -1 +1 @@\n-old\n+new\n"}]

    def item(self, changes=None, *, method="item/started", status="inProgress", item_id="item"):
        return {"method": method, "params": {"threadId": "thread", "turnId": "turn", "startedAtMs": 1,
                "item": {"type": "fileChange", "id": item_id, "status": status,
                         "changes": self.changes if changes is None else changes}}}

    def request(self, **params):
        return {"id": "native-1", "method": "item/fileChange/requestApproval", "params": {
            "threadId": "thread", "turnId": "turn", "itemId": "item", "startedAtMs": 1, **params}}

    def ready(self):
        self.gate.observe(self.item())
        self.gate.observe(self.request())

    def test_exact_one_shot_update_and_completion(self):
        self.ready()
        response, proof = self.gate.take_approval()
        self.assertEqual(response, {"id": "native-1", "result": {"decision": "accept"}})
        self.assertEqual(proof["before_sha256"], edit.digest(b"old\n"))
        self.assertEqual(self.plan.target.read_bytes(), b"old\n")  # The gate never writes the target.
        self.assertIsNone(self.gate.take_approval())
        self.gate.observe(self.item(method="item/completed", status="completed"))
        self.assertEqual(self.gate.completed_file_items, 1)
        with self.assertRaises(edit.Stop):
            self.gate.observe(self.request(itemId="item"))

    def test_patch_must_precede_request_and_cannot_be_inferred_from_reason(self):
        for started in (False, True):
            gate = edit.EditGate(self.plan)
            gate.thread, gate.turn, gate.turn_requested = "thread", "turn", True
            if started:
                gate.observe(self.item(changes=[]))
            with self.assertRaises(edit.Stop):
                gate.observe(self.request(reason=self.plan.prompt()))
            self.assertFalse(gate.accepted)

    def test_complete_patch_update_can_fill_initial_empty_item(self):
        self.gate.observe(self.item(changes=[]))
        self.gate.observe({"method": "item/fileChange/patchUpdated", "params": {
            "threadId": "thread", "turnId": "turn", "itemId": "item", "changes": self.changes}})
        self.gate.observe(self.request())
        self.assertEqual(self.gate.take_approval()[0]["result"], {"decision": "accept"})

    def test_stale_thread_turn_and_item_requests(self):
        self.gate.observe(self.item())
        for field in ("threadId", "turnId", "itemId"):
            with self.subTest(field=field), self.assertRaises(edit.Stop):
                request = self.request(**{field: "stale"})
                request["id"] = field
                self.gate.observe(request)

    def test_request_collision_replay_and_invalid_identifiers(self):
        self.gate.observe(self.item())
        with self.assertRaises(edit.Stop):
            self.gate.observe(self.request(), {edit.identifier("native-1")})
        self.gate.observe(self.request())
        with self.assertRaises(edit.Stop):
            self.gate.observe(self.request())
        for bad in (True, False, None, 1.5, [], {}, ""):
            with self.subTest(bad=bad), self.assertRaises(edit.Stop):
                edit.identifier(bad)

    def test_permission_expansion_unknown_fields_and_other_requests_refused(self):
        for params in ({"grantRoot": str(self.repo)}, {"grantRoot": ""}, {"permissions": {}},
                       {"startedAtMs": True}, {"reason": {"decision": "accept"}}):
            gate = edit.EditGate(self.plan)
            gate.thread, gate.turn, gate.turn_requested = "thread", "turn", True
            gate.observe(self.item())
            with self.subTest(params=params), self.assertRaises(edit.Stop):
                gate.observe(self.request(**params))
        for method in ("item/commandExecution/requestApproval", "item/permissions/requestApproval",
                       "applyPatchApproval", "item/tool/requestUserInput", "mcpServer/elicitation/request", "unknown"):
            request = self.request()
            request["method"] = method
            with self.subTest(method=method), self.assertRaises(edit.Stop):
                edit.EditGate(self.plan).observe(request)

    def test_changed_target_before_accept_has_no_response(self):
        self.ready()
        self.plan.target.write_bytes(b"changed while waiting\n")
        with self.assertRaises(edit.Stop):
            self.gate.take_approval()
        self.assertFalse(self.gate.accepted)

    def test_changed_or_late_patch_and_extra_item_always_stop(self):
        self.ready()
        self.gate.take_approval()
        changed = copy.deepcopy(self.changes)
        changed[0]["diff"] = "@@ -1 +1 @@\n-old\n+malicious\n"
        for message in (self.item(item_id="extra"),
                        {"method": "item/fileChange/patchUpdated", "params": {
                            "threadId": "thread", "turnId": "turn", "itemId": "item", "changes": changed}},
                        self.item(changes=changed, method="item/completed", status="completed")):
            with self.assertRaises(edit.Stop):
                self.gate.observe(message)
        self.gate.observe(self.item(method="item/completed", status="completed"))
        with self.assertRaises(edit.Stop):
            self.gate.observe({"method": "item/fileChange/patchUpdated", "params": {
                "threadId": "thread", "turnId": "turn", "itemId": "item", "changes": self.changes}})

    def test_add_delete_move_extra_paths_and_hidden_fields_rejected(self):
        variants = []
        for kind in ({"type": "add"}, {"type": "delete"}, {"type": "update", "move_path": "other"},
                     {"type": "update", "mode": "100755"}):
            variants.append([{**self.changes[0], "kind": kind}])
        variants.extend([self.changes * 2, [], [{**self.changes[0], "mode": "100755"}]])
        for name in ("../governed-target.txt", "./governed-target.txt", "governed-target.txt:stream",
                     "C:governed-target.txt", "\\governed-target.txt", "outside-scope.txt"):
            variants.append([{**self.changes[0], "path": name}])
        for value in variants:
            with self.subTest(value=value), self.assertRaises(edit.Stop):
                self.gate.validate_changes(value)

    def test_hard_link_and_reparse_identity_cannot_receive_approval(self):
        other = self.repo / "hard-linked.txt"
        os.link(self.plan.target, other)
        self.ready()
        with self.assertRaises(edit.Stop):
            self.gate.take_approval()
        other.unlink()
        original = self.plan.target.lstat()
        with patch.object(Path, "lstat", return_value=types.SimpleNamespace(
                st_mode=original.st_mode, st_file_attributes=0x400)):
            with self.assertRaises(edit.Stop):
                self.plan.read_before()

    def test_native_refusal_not_overridden_but_handler_failure_not_invented_refusal(self):
        self.gate.observe(self.item())
        hook = {"method": "hook/completed", "params": {"threadId": "thread", "turnId": "turn",
                "run": {"eventName": "preToolUse", "status": "failed"}}}
        self.gate.observe(hook)
        self.assertFalse(self.gate.hook_blocked)
        hook["params"]["run"]["status"] = "blocked"
        self.gate.observe(hook)
        with self.assertRaises(edit.Stop):
            self.gate.observe(self.request())

    def test_command_item_and_unapproved_completed_edit_stop(self):
        for kind in ("commandExecution", "mcpToolCall", "collabAgentToolCall", "webSearch", "unknown"):
            with self.subTest(kind=kind), self.assertRaises(edit.Stop):
                self.gate.observe({"method": "item/started", "params": {"item": {"type": kind}}})
        self.gate.observe(self.item())
        with self.assertRaises(edit.Stop):
            self.gate.observe(self.item(method="item/completed", status="completed"))

    def test_unified_diff_exact_whole_file_with_context_quotes_unicode_and_crlf(self):
        for ending in ("\n", "\r\n"):
            plan = edit.Plan(self.repo, {"schema": "verity-one-edit-v1", "target": "café quoted ' target.txt",
                "before_utf8": "unchanged" + ending + "old" + ending,
                "after_utf8": "unchanged" + ending + "café" + ending})
            diff = ("--- a/café quoted ' target.txt\n+++ b/café quoted ' target.txt\n@@ -1,2 +1,2 @@\n" +
                    " unchanged" + ending + "-old" + ending + "+café" + ending)
            self.assertEqual(edit.apply_complete_diff(plan, diff), plan.after)

    def test_unsupported_partial_binary_or_ambiguous_diff_stops(self):
        for diff in ("", "old -> new", "@@ -2 +2 @@\n-old\n+new\n", "@@ -1,2 +1 @@\n-old\n+new\n",
                     "@@ -1 +1 @@\n-old\n+new", "@@ -1 +1 @@\n-old\n+new\n@@ -2 +2 @@\n",
                     "@@ -1 +1 @@\n-old\n+new\n\\ No newline at end of file\n",
                     "--- a/other\n+++ b/other\n@@ -1 +1 @@\n-old\n+new\n",
                     "GIT binary patch\n", "*** Begin Patch\n", "@@ -1 +1 @@\n-old\r\n+new\r\n"):
            with self.subTest(diff=diff), self.assertRaises(edit.Stop):
                edit.apply_complete_diff(self.plan, diff)

    def test_strict_json_rejects_replacement_decoding_duplicate_keys_and_nonfinite(self):
        for raw in (b'{"id":1,"id":2}', b'{"a":"\xff"}', b'{"a":"\\ud800"}', b'[]', b'{"a":NaN}'):
            with self.subTest(raw=raw), self.assertRaises(edit.Stop):
                edit.strict_json(raw)
        self.assertEqual(edit.strict_json(b'{"id":1}'), {"id": 1})

    def test_thread_profile_cannot_expand_or_choose_automated_reviewer(self):
        expected = {"approvalPolicy": "on-request", "approvalsReviewer": "user", "cwd": str(self.repo),
                    "sandbox": {"type": "readOnly", "networkAccess": False}, "thread": {"id": "thread"},
                    "runtimeWorkspaceRoots": [str(self.repo)], "activePermissionProfile": None}
        self.assertEqual(edit.check_thread(expected, self.repo), "thread")
        self.assertEqual(edit.thread_params(self.repo), {"cwd": str(self.repo), "sandbox": "read-only",
                                                       "approvalPolicy": "on-request", "ephemeral": False})
        for change in ({"approvalPolicy": "never"}, {"approvalsReviewer": "auto_review"},
                       {"sandbox": {"type": "workspaceWrite"}}, {"sandbox": {"type": "readOnly", "networkAccess": True}},
                       {"runtimeWorkspaceRoots": []}, {"runtimeWorkspaceRoots": [str(self.repo), "another"]},
                       {"runtimeWorkspaceRoots": ["another"]}, {"activePermissionProfile": {"id": "new-profile"}}):
            with self.assertRaises(edit.Stop):
                edit.check_thread({**expected, **change}, self.repo)

    def test_schema_identity_drift_fails_before_any_launch(self):
        root = self.repo / "schemas"
        for name in edit.SCHEMA_PINS:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"changed schema")
        with self.assertRaises(edit.Stop):
            edit.pinned_schemas(root)

    def test_cli_default_preflight_and_tampered_plan_never_spawn(self):
        root = self.repo
        repo = root / "repo with spaces"
        repo.mkdir()
        (repo / "governed-target.txt").write_bytes(self.plan.before)
        plan_path = root / "plan.json"
        plan_path.write_bytes(edit.encoded(self.plan.value))
        allowed = root / "docs/engineering/plugin-integration/evidence/WO-PLG-005"
        identity = allowed / "preparation/accepted-profile/identity.json"
        identity.parent.mkdir(parents=True)
        identity.write_text(json.dumps({"host_sha256": "a" * 64}))
        fake_fixture = types.SimpleNamespace(ROOT=root, SANDBOX=root, PROFILE=root / "profile", SCHEMAS=root / "schemas",
            CODEX=root / "fake-executable", __file__=str(root / "fixture.py"), sha=lambda path: "a" * 64,
            host_argv=lambda *args: [str(root / "fake-executable"), *args])
        fake_observer = types.SimpleNamespace(package_record=lambda path: {
            "payload": {"hooks/hooks.json": "a" * 64, "scripts/codex-dispatch.py": "a" * 64}})
        args = ["--plan", str(plan_path), "--approved-plan-sha256", edit.digest(plan_path.read_bytes()),
                "--package-record", str(root / "package.json"), "--evidence", str(allowed / "new"),
                "--stop-marker", str(root / "STOP")]
        modules = {"fixture": fake_fixture, "observer": fake_observer,
                   "sanitize_output": types.SimpleNamespace(sanitize_value=lambda value: value)}
        with patch.dict("sys.modules", modules), patch.object(edit, "pinned_schemas", return_value={}), \
                patch.object(edit, "os", types.SimpleNamespace(name="nt")), \
                patch.object(edit, "run_session") as runner, patch("subprocess.Popen") as popen, \
                patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(edit.main(args), 0)
            self.assertEqual(json.loads(output.getvalue())["mode"], "preflight-only; no host spawned")
            self.assertFalse((allowed / "new").exists())
            plan_path.write_bytes(edit.encoded({**self.plan.value, "after_utf8": "tampered\n"}))
            with patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
                edit.main(args + ["--run"])
            runner.assert_not_called()
            popen.assert_not_called()

    def test_transport_contains_unknown_request_and_persists_before_exact_accept(self):
        # A fake byte-pipe host exercises the real loop; the only file writes are
        # test fixture writes, not a Codex launch or a native enforcement result.
        for mode in ("success", "unknown-request", "stop-before-accept"):
            malicious = mode != "success"
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                plan = edit.Plan(root, self.plan.value)
                for name in edit.TARGETS:
                    (root / name).write_bytes(plan.before)
                dest = root / "evidence"
                dest.mkdir()
                hooks_path = root / "plugins/verity-plane/codex/hooks/hooks.json"
                hooks_path.parent.mkdir(parents=True)
                hooks_path.write_bytes(b"{}")
                inbox, sent, cleaned, spawns = queue.Queue(), [], [], []
                class Output:
                    def readline(self, limit):
                        return inbox.get()
                class Input:
                    def write(inner, raw):
                        message = json.loads(raw)
                        sent.append(message)
                        def emit(value):
                            inbox.put(edit.encoded(value) + b"\n")
                        method = message.get("method")
                        if method == "initialize" and mode == "unknown-request":
                            emit({"id": "native", "method": "item/commandExecution/requestApproval", "params": {}})
                        elif method == "thread/start":
                            emit({"id": message["id"], "result": {"cwd": str(root), "approvalPolicy": "on-request",
                                "approvalsReviewer": "user", "sandbox": {"type": "readOnly"}, "thread": {"id": "thread"},
                                "runtimeWorkspaceRoots": [str(root)], "activePermissionProfile": None}})
                        elif method == "turn/start":
                            emit({"id": message["id"], "result": {"turn": {"id": "turn"}}})
                            emit({"method": "turn/started", "params": {"threadId": "thread", "turn": {"id": "turn"}}})
                            item = self.item()
                            item["params"]["item"]["changes"][0]["path"] = str(plan.target)
                            emit(item)
                            emit(self.request())
                        elif "method" not in message:
                            self.assertTrue((dest / "approval-prepared.json").exists())
                            self.assertEqual(message["result"], {"decision": "accept"})
                            plan.target.write_bytes(plan.after)
                            item = self.item(method="item/completed", status="completed")
                            item["params"]["item"]["changes"][0]["path"] = str(plan.target)
                            emit(item)
                            emit({"method": "turn/completed", "params": {"threadId": "thread", "turn": {"id": "turn"}}})
                        elif "id" in message:
                            emit({"id": message["id"], "result": {}})
                    def flush(inner):
                        pass
                process = types.SimpleNamespace(stdin=Input(), stdout=Output(), stderr=io.BytesIO(b""), poll=lambda: None)
                def spawn(argv, **kwargs):
                    spawns.append((argv, kwargs))
                    return process
                def stop(value):
                    cleaned.append(value)
                    inbox.put(b"")
                    return {"active_processes": 0}
                fixture = types.SimpleNamespace(ROOT=root, PROFILE=root / "profile", CODEX="fake-never-executed", host_environment=lambda: {},
                                                host_argv=lambda *args: ["fake-never-executed", *args])
                observer = types.SimpleNamespace(active_bindings=lambda *args: [{"sourcePath": str(root / "cache/hooks/hooks.json")}],
                                                 loaded_payload=lambda *args: {})
                sanitizer = types.SimpleNamespace(sanitize_value=lambda value: value, sanitize_text=lambda value: value)
                modules = {"fixture": fixture, "observer": observer, "processes": types.SimpleNamespace(spawn=spawn, stop_owned_tree=stop),
                           "sanitize_output": sanitizer}
                details = {"plan_sha256": "synthetic-test-only"}
                retain = edit.retain
                def retain_then_stop(path, value):
                    retain(path, value)
                    if mode == "stop-before-accept" and path.name == "approval-prepared.json":
                        (root / "STOP").touch()
                with patch.dict("sys.modules", modules), patch.object(edit, "retain", side_effect=retain_then_stop):
                    result = edit.run_session(plan, dest, {"payload": {"hooks/hooks.json": "synthetic"}}, root / "STOP", details)
                self.assertEqual(len(spawns), 1)
                self.assertEqual(cleaned, [process])
                self.assertNotIn("shell", spawns[0][1])
                approvals = [value for value in sent if "result" in value]
                self.assertEqual(len(approvals), 0 if malicious else 1)
                self.assertEqual(result, 1 if malicious else 0)
                self.assertEqual(plan.target.read_bytes(), plan.before if malicious else plan.after)
                self.assertFalse(json.loads((dest / "observations.json").read_text())["qualified"])


if __name__ == "__main__":
    unittest.main()
