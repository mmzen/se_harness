"""Independent transport, binding and failure checks for the Codex adapter."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
HOST = ROOT / "plugins/verity-plane/codex"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


adapter = load("codex_adapter", HOST / "dispatch.py")
renderer = load("codex_hook_renderer", HOST / "render_hooks.py")


class AdapterTests(unittest.TestCase):
    def test_generated_native_commands_are_exact(self):
        self.assertEqual(renderer.definitions(HOST), json.loads((HOST / "hooks/hooks.json").read_text()))
        for name, rows in renderer.definitions(HOST)["hooks"].items():
            command = rows[0]["hooks"][0]
            self.assertFalse(command["async"])
            self.assertEqual(command["timeout"], 30)
            self.assertNotIn("-File", command["command"])
            self.assertNotIn("powershell.exe", command["command"])
            self.assertIn("$kind='" + name + "'", command["command"])
        self.assertLess(sum(adapter.TIMING[name] for name in ("inner-timeout", "startup-margin", "cleanup-margin", "output-margin")), 30)

    def test_decode_rejects_malformed_duplicate_and_large_inputs(self):
        for raw in (b"[1]", b"{", b'{"a":1,"a":2}', b" " * 65537):
            with self.subTest(raw=raw[:40]), self.assertRaises(ValueError):
                adapter.decode(raw)

    def test_binding_rejects_unaccepted_profile(self):
        binding = {"schema": "verity-codex-binding-v1", "repo": "unused", "environment": "unused",
                   "artifact": "WO-PROBE-001", "capture": False,
                   "decision": {"id": "DEC-PLG-001", "status": "decided", "option": "prove-supported-route"},
                   "profile": {"host": "0.153.5", "os": "windows", "python": "3.14.6", "evaluator": "0.16.0"}}
        with self.assertRaisesRegex(ValueError, "unsupported selected profile"):
            adapter.arguments(binding, {}, Path.cwd())

    def test_only_documented_decision_envelopes_are_returned(self):
        for value in ({"hookEventName": "PreToolUse", "permissionDecision": "allow"},
                      {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": ""},
                      {"hookEventName": "PreToolUse", "additionalContext": "ok", "updatedInput": {}},
                      {"hookEventName": "SessionStart", "additionalContext": "wrong event"}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                adapter.validate_output(json.dumps({"hookSpecificOutput": value}).encode(), "PreToolUse", 0)
        for value in ({"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "refused"},
                      {"hookEventName": "PreToolUse", "additionalContext": "current checks passed"}):
            expected = {"hookSpecificOutput": value}
            self.assertEqual(adapter.validate_output(json.dumps(expected).encode(), "PreToolUse", 0), expected)
            with self.assertRaises(ValueError):
                adapter.validate_output(json.dumps(expected).encode(), "PreToolUse", 1)

    def test_missing_empty_or_whitespace_context_is_unready(self):
        for name in ("SessionStart", "PreToolUse"):
            for context in (None, "", " ", "\r\n\t", [], {}):
                specific = {"hookEventName": name, "additionalContext": context}
                with self.subTest(name=name, context=context), self.assertRaises(ValueError):
                    adapter.validate_output(json.dumps({"hookSpecificOutput": specific}).encode(), name, 0)
            expected = {"hookSpecificOutput": {"hookEventName": name, "additionalContext": "Fresh context\n"}}
            self.assertEqual(adapter.validate_output(json.dumps(expected).encode(), name, 0), expected)

    @unittest.skipUnless(os.name == "nt", "accepted guard profile is Windows")
    def test_native_guard_failures_and_setup_access(self):
        with tempfile.TemporaryDirectory(prefix="codex guard spaces '") as space:
            folder = Path(space)
            environment = os.environ.copy()
            environment.update(PLUGIN_DATA=str(folder), PLUGIN_ROOT=str(folder))
            shell = str(Path(os.environ["SYSTEMROOT"]) / "System32/WindowsPowerShell/v1.0/powershell.exe")
            for name, raw in (("PreToolUse", b"{"), ("PreToolUse", b'{}'),
                              ("SessionStart", json.dumps({"hook_event_name":"SessionStart","source":"startup","cwd":str(folder)}).encode()),
                              ("PreToolUse", b'{"hook_event_name":"PreToolUse","tool_name":"apply_patch"}')):
                command = renderer.definitions(HOST)["hooks"][name][0]["hooks"][0]["command"]
                run = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-Command", command],
                                     input=raw, capture_output=True, env=environment, timeout=10)
                self.assertEqual(run.returncode, 0, run.stderr)
                output = json.loads(run.stdout)
                self.assertEqual(output["hookSpecificOutput"]["hookEventName"], name)
                if name == "PreToolUse":
                    self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")
                else:
                    self.assertIn("no Python invoked", output["hookSpecificOutput"]["additionalContext"])
            raw = json.dumps({"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"setup"},"cwd":str(folder)}).encode()
            command = renderer.definitions(HOST)["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
            run = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-Command", command],
                                 input=raw, capture_output=True, env=environment, timeout=10)
            self.assertEqual(run.returncode, 0)
            self.assertEqual(set(json.loads(run.stdout)), {"systemMessage"})
            self.assertIn("COVERAGE GAP", json.loads(run.stdout)["systemMessage"])
            for tool in ("", " ", {}, ["Bash"]):
                raw = json.dumps({"hook_event_name":"PreToolUse","tool_name":tool,"tool_input":{},"cwd":str(folder)}).encode()
                run = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-Command", command],
                                     input=raw, capture_output=True, env=environment, timeout=10)
                self.assertEqual(json.loads(run.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")

    @unittest.skipUnless(os.name == "nt", "accepted argv profile is Windows")
    def test_native_guard_rejects_drive_and_root_relative_paths_before_python(self):
        with tempfile.TemporaryDirectory(prefix="codex path boundary ") as space:
            folder = Path(space)
            (folder / "scripts").mkdir()
            repo = folder / "repo"
            repo.mkdir()
            marker = folder / "python-invoked.txt"
            (folder / "scripts/codex-dispatch.py").write_text(
                "from pathlib import Path; Path(" + repr(str(marker)) + ").write_text('invoked')", encoding="utf8")
            environment_root = Path(sys.executable).parent.parent
            selected = {"schema": "verity-codex-binding-v1", "environment": str(environment_root),
                        "repo": str(repo), "artifact": "WO-PROBE-001", "capture": False,
                        "profile": {"host": "0.153.4", "os": "windows", "python": "3.14.6", "evaluator": "0.16.0"},
                        "decision": {"id": "DEC-PLG-001", "status": "decided", "option": "prove-supported-route"}}
            environment = os.environ.copy()
            environment.update(PLUGIN_DATA=str(folder), PLUGIN_ROOT=str(folder))
            shell = str(Path(os.environ["SYSTEMROOT"]) / "System32/WindowsPowerShell/v1.0/powershell.exe")
            command = renderer.definitions(HOST)["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
            event = {"hook_event_name": "PreToolUse", "cwd": str(repo), "tool_name": "apply_patch",
                     "tool_input": {"command": "*** Begin Patch\n*** End Patch"}}
            for field, path in (("environment", environment_root.drive + environment_root.name),
                                ("environment", str(environment_root)[2:]), ("repo", str(repo)[2:])):
                (folder / "binding.json").write_text(json.dumps({**selected, field:path}), encoding="utf8")
                denied = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-Command", command],
                    input=json.dumps(event).encode(), capture_output=True, env=environment,
                    cwd=environment_root.parent, timeout=10)
                with self.subTest(field=field, path=path):
                    self.assertEqual(denied.returncode, 0, denied.stderr)
                    self.assertFalse(marker.exists(), "non-absolute selection invoked Python")
                    failure = json.loads(denied.stdout)["hookSpecificOutput"]
                    self.assertEqual(failure["permissionDecision"], "deny")
                    self.assertIn("Fully qualified", failure["permissionDecisionReason"])

    @unittest.skipUnless(os.name == "nt", "accepted argv profile is Windows")
    def test_native_guard_preserves_unicode_quotes_and_absolute_argv(self):
        with tempfile.TemporaryDirectory(prefix="codex quoted '") as space:
            folder = Path(space)
            (folder / "scripts").mkdir()
            (folder / "repo with spaces").mkdir()
            fake = folder / "scripts/codex-dispatch.py"
            fake.write_text("import json,sys; print(json.dumps({'argv':sys.argv,'input':json.load(sys.stdin)},ensure_ascii=False))", encoding="utf8")
            selected = {"schema": "verity-codex-binding-v1", "environment": str(Path(sys.executable).parent.parent),
                        "repo": str(folder / "repo with spaces"), "artifact": "WO-PROBE-001", "capture": False,
                        "profile": {"host": "0.153.4", "os": "windows", "python": "3.14.6", "evaluator": "0.16.0"},
                        "decision": {"id": "DEC-PLG-001", "status": "decided", "option": "prove-supported-route"}}
            (folder / "binding.json").write_text(json.dumps(selected), encoding="utf8")
            environment = os.environ.copy()
            environment.update(PLUGIN_DATA=str(folder), PLUGIN_ROOT=str(folder))
            raw = {"hook_event_name": "PreToolUse", "tool_name": "apply_patch", "cwd":str(folder / "repo with spaces"), "tool_input":
                   {"command": '*** Begin Patch\n*** Add File: café \' test.txt\n+"quoted" \\ $value `tick`\n*** End Patch'}}
            shell = str(Path(os.environ["SYSTEMROOT"]) / "System32/WindowsPowerShell/v1.0/powershell.exe")
            command = renderer.definitions(HOST)["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
            run = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-Command", command],
                                 input=json.dumps(raw, ensure_ascii=False).encode(), capture_output=True,
                                 env=environment, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            output = json.loads(run.stdout)
            self.assertEqual(output["input"], raw)
            self.assertEqual(output["argv"], [str(fake), "--data", str(folder), "--event", "PreToolUse"])
            # A selected eligibility failure must happen in the shell, before
            # even the fixture dispatcher can record a Python invocation.
            marker = folder / "python-spawned.txt"
            fake.write_text("from pathlib import Path; Path(" + repr(str(marker)) + ").write_text('spawned')", encoding="utf8")
            for changes in ({"profile": {}}, {"profile": {**selected["profile"], "host": "0.153.5"}},
                            {"decision": {}}, {"decision": {**selected["decision"], "status": "open"}},
                            {"decision": {**selected["decision"], "option": "exclude-codex"}}):
                (folder / "binding.json").write_text(json.dumps({**selected, **changes}), encoding="utf8")
                for name in ("SessionStart", "PreToolUse"):
                    event = {"hook_event_name": name, "source": "startup", "cwd": selected["repo"],
                             "tool_name": "apply_patch", "tool_input": {"command": "*** Begin Patch\n*** End Patch"}}
                    guard = renderer.definitions(HOST)["hooks"][name][0]["hooks"][0]["command"]
                    denied = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-Command", guard],
                                            input=json.dumps(event).encode(), capture_output=True, env=environment, timeout=10)
                    with self.subTest(changes=changes, event=name):
                        self.assertFalse(marker.exists(), "negative selection invoked Python")
                        self.assertEqual(denied.returncode, 0, denied.stderr)
                        failure = json.loads(denied.stdout)["hookSpecificOutput"]
                        self.assertEqual(failure["hookEventName"], name)
                        if name == "PreToolUse":
                            self.assertEqual(failure["permissionDecision"], "deny")
                        else:
                            self.assertIn("UNREADY", failure["additionalContext"])


if __name__ == "__main__":
    unittest.main()
