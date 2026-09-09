"""Independent fixture safety checks, separate from live Codex observations."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("codex_probe", Path(__file__).with_name("probe.py"))
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


class ProbeSafetyTests(unittest.TestCase):
    def test_credentials_and_user_paths_are_not_inherited(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "MUST-NOT-LEAK", "CODEX_ACCESS_TOKEN": "SECRET",
                                      "PYTHONPATH": "HOST", "CODEX_HOME": "NORMAL", "PATH": "HOST"}):
            env = probe.isolated_environment(Path("C:/disposable profile"))
        self.assertNotIn("OPENAI_API_KEY", env)
        self.assertNotIn("CODEX_ACCESS_TOKEN", env)
        self.assertNotIn("PYTHONPATH", env)
        self.assertNotEqual("HOST", env["PATH"])
        self.assertIn("disposable profile", env["CODEX_HOME"])

    def test_existing_sandbox_is_never_erased(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            sentinel = root / "keep.txt"
            sentinel.write_text("keep")
            with self.assertRaises(ValueError):
                probe.prepare(root)
            self.assertEqual("keep", sentinel.read_text())

    def test_existing_evidence_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            old = directory / "result.json"
            old.write_text('{"original": true}')
            with self.assertRaises(ValueError):
                probe.retain(directory, "result", {"stdout": "new", "stderr": ""})
            self.assertEqual('{"original": true}', old.read_text())

    def test_manifest_resolves_inside_marketplace_and_declares_real_skill(self):
        with tempfile.TemporaryDirectory() as temp:
            home, repo, market, env = probe.prepare(Path(temp) / "new sandbox with spaces")
            manifest = json.loads((market / ".agents/plugins/marketplace.json").read_text())
            plugin = market / manifest["plugins"][0]["source"]["path"]
            self.assertTrue(plugin.is_relative_to(market))
            self.assertTrue((plugin / "skills/setup/SKILL.md").is_file())
            self.assertIn("not governance-ready", (plugin / "skills/setup/SKILL.md").read_text())
            self.assertEqual("unchanged sentinel\n", (repo / "governed-target.txt").read_text())
            self.assertIn('cli_auth_credentials_store = "file"', (home / "codex/config.toml").read_text())
            self.assertFalse((home / "codex/auth.json").exists())

    def test_hook_no_trust_or_permissions_bypass(self):
        with tempfile.TemporaryDirectory() as temp:
            _, _, market, _ = probe.prepare(Path(temp) / "new")
            hooks = json.loads((market / "plugins/codex-probe/hooks/hooks.json").read_text())["hooks"]
            self.assertEqual({"SessionStart", "PreToolUse"}, set(hooks))
            self.assertEqual("startup|resume|clear|compact", hooks["SessionStart"][0]["matcher"])
            for groups in hooks.values():
                for group in groups:
                    for hook in group["hooks"]:
                        self.assertNotIn("bypass", hook["command"].lower())
                        self.assertIn("${PLUGIN_ROOT}", hook["command"])

    def test_inline_variant_does_not_evaluate_the_refused_script(self):
        with tempfile.TemporaryDirectory() as temp:
            _, _, market, _ = probe.prepare(Path(temp) / "new", inline=True)
            hooks = json.loads((market / "plugins/codex-probe/hooks/hooks.json").read_text())["hooks"]
            command = hooks["SessionStart"][0]["hooks"][0]["command"]
            self.assertIn("-Command", command)
            self.assertNotIn("observe.ps1", command)
            self.assertNotIn("ExecutionPolicy", command)
            self.assertNotIn("Invoke-Expression", command)
            self.assertIn("Test-Path -LiteralPath $python", command)

    def test_real_child_timeout_is_not_reported_as_success(self):
        with tempfile.TemporaryDirectory() as temp:
            result = probe.run([sys.executable, "-I", "-c", "import time; time.sleep(5)"],
                               Path(temp), dict(os.environ), timeout=.1)
            self.assertTrue(result["timed_out"])
            self.assertIsNone(result["exit_status"])

    def test_timeout_stops_own_descendant_but_not_unrelated_process(self):
        def alive(pid):
            if os.name == "nt":
                import ctypes
                from ctypes import wintypes
                kernel = ctypes.WinDLL("kernel32", use_last_error=True)
                kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
                kernel.OpenProcess.restype = wintypes.HANDLE
                kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
                kernel.CloseHandle.argtypes = [wintypes.HANDLE]
                handle = kernel.OpenProcess(0x1000, False, pid)
                if not handle:
                    return False
                try:
                    code = wintypes.DWORD()
                    return bool(kernel.GetExitCodeProcess(handle, ctypes.byref(code))) and code.value == 259
                finally:
                    kernel.CloseHandle(handle)
            try:
                os.kill(pid, 0)
                return True
            except ProcessLookupError:
                return False
        unrelated = probe.spawn([sys.executable, "-I", "-c", "import time; time.sleep(60)"])
        try:
            with tempfile.TemporaryDirectory() as temp:
                program = ("import subprocess,sys,time; "
                           "child=subprocess.Popen([sys.executable,'-I','-c','import time; time.sleep(60)']); "
                           "print(child.pid,flush=True); time.sleep(60)")
                result = probe.run([sys.executable, "-I", "-c", program], Path(temp), dict(os.environ), timeout=1)
                descendant = int(result["stdout"].strip())
                self.assertTrue(result["timed_out"])
                self.assertFalse(result["cleanup"].get("descendant_cleanup_unconfirmed", False))
                for _ in range(20):
                    if not alive(descendant):
                        break
                    time.sleep(.05)
                self.assertFalse(alive(descendant))
                self.assertIsNone(unrelated.poll())
        finally:
            probe.stop_owned_tree(unrelated)

    def test_nonzero_exit_and_raw_output_are_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            result = probe.run([sys.executable, "-I", "-c", "import sys; print('SENTINEL'); sys.exit(7)"],
                               Path(temp), dict(os.environ))
            self.assertEqual(7, result["exit_status"])
            self.assertIn("SENTINEL", result["stdout"])
            self.assertFalse(result["timed_out"])

    def test_exited_parent_cannot_leave_descendant_holding_output_pipe(self):
        with tempfile.TemporaryDirectory() as temp:
            program = ("import subprocess,sys; "
                       "child=subprocess.Popen([sys.executable,'-I','-c','import time; time.sleep(60)']); "
                       "print(child.pid,flush=True)")
            result = probe.run([sys.executable, "-I", "-c", program], Path(temp), dict(os.environ), timeout=1)
            self.assertTrue(result["timed_out"])
            self.assertGreater(int(result["stdout"].strip()), 0)
            self.assertLess(result["duration_seconds"], 5)
            self.assertFalse(result["cleanup"].get("descendant_cleanup_unconfirmed", False))
            if os.name == "nt":
                self.assertEqual(0, result["cleanup"]["active_processes"])


if __name__ == "__main__":
    unittest.main()
