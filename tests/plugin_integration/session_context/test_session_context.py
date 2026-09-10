"""Boundary tests use injected evaluator results; acceptance runs use a released wheel."""
import argparse
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[3] / "plugins/verity-plane/common/scripts/session-context.py"
SPEC = importlib.util.spec_from_file_location("session_context", SCRIPT)
handler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(handler)


class SessionBoundaries(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.config = argparse.Namespace(repo=str(self.repo), environment=str(self.repo.parent / "environment"),
            version="0.17.0", payload_sha256="a" * 64, archive_sha256="b" * 64,
            host="codex", context_limit=32000, read_limit=32000, read_sha256=None)
        self.sources = {"AGENTS.md": b"PRIVATE OWNER NOTE\n" + handler.BEGIN + b"\r\ngate\r\n" + handler.END,
                        "ENGINEERING_HARNESS.md": b"router\r\n", ".engineering-harness.toml": b"fixture\n",
                        ".engineering-harness.lock": json.dumps({"evaluator": {
                            "version": self.config.version, "payload_sha256": self.config.payload_sha256,
                            "archive_sha256": self.config.archive_sha256,
                            "archive_name": "se_harness-0.17.0-py3-none-any.whl"}}).encode()}
        for name, raw in self.sources.items():
            (self.repo / name).write_bytes(raw)
        self.event = {"hook_event_name": "SessionStart", "source": "startup", "cwd": str(self.repo)}

    def paths(self, config=None):
        env = Path(self.config.environment)
        return self.repo, env, env / "Scripts/python.exe", env / "Scripts/harnessctl.exe"

    def fake_run(self, argv, cwd, env):
        if "identity" in argv:
            data = {"schema": "se-harness-runtime-identity-v3", "passed": True,
                    "harness_version": self.config.version,
                    "evaluator_payload_sha256": self.config.payload_sha256,
                    "evaluator_archive_sha256": self.config.archive_sha256}
        else:
            data = {"checks": [{"passed": True}]}
        return {"exit_status": 0, "result": data, "argv": argv}

    def test_exact_bytes_and_owner_content_exclusion(self):
        with patch.object(handler, "runtime_paths", self.paths):
            message, result = handler.deliver(self.config, self.event, self.fake_run)
        self.assertIn("\r\ngate\r\n", message)
        self.assertIn("router\r\n", message)
        self.assertNotIn("PRIVATE OWNER NOTE", message)
        self.assertTrue(message.rstrip().endswith("complete context delivered."))
        self.assertEqual(len(result["checks"]), 2)

    def test_malformed_json_and_unsafe_events_are_refused(self):
        for raw in (b'[]', b'{"cwd":"a","cwd":"b"}', b'{', b'\xff', b' ' * (handler.MAX_INPUT + 1)):
            with self.assertRaises((ValueError, UnicodeError)):
                handler.decode(raw)
        for event in ({**self.event, "source": "PostCompact"}, {**self.event, "hook_event_name": "PostCompact"},
                      {**self.event, "cwd": str(self.repo / "..")}, {**self.event, "cwd": "relative"}):
            with self.assertRaises(ValueError):
                handler.deliver(self.config, event)

    def test_identity_requires_actual_boolean_and_observed_archive(self):
        for changes in ({"passed": "true"}, {"passed": 1}, {"evaluator_archive_sha256": None},
                        {"evaluator_archive_sha256": "c" * 64}, {"schema": "wrong"}):
            calls = []
            def run(argv, cwd, env):
                calls.append(argv)
                result = self.fake_run(argv, cwd, env)
                result["result"].update(changes)
                return result
            with patch.object(handler, "runtime_paths", self.paths), self.assertRaises(handler.Blocked):
                handler.verify(self.config, run)
            self.assertEqual(len(calls), 1)

    def test_empty_or_nonboolean_doctor_results_cannot_pass(self):
        for checks in ([], None, [{"passed": "true"}], [None]):
            def run(argv, cwd, env):
                result = self.fake_run(argv, cwd, env)
                if "doctor" in argv:
                    result["result"] = {"checks": checks}
                return result
            with patch.object(handler, "runtime_paths", self.paths), self.assertRaises(handler.Blocked):
                handler.verify(self.config, run)

    def test_source_race_restarts_identity_and_integrity(self):
        calls = []
        def run(argv, cwd, env):
            calls.append(argv)
            if len(calls) == 2:
                (self.repo / "ENGINEERING_HARNESS.md").write_bytes(b"new router\r\n")
            return self.fake_run(argv, cwd, env)
        with patch.object(handler, "runtime_paths", self.paths):
            message, record = handler.deliver(self.config, self.event, run)
        self.assertEqual(len(calls), 4)
        self.assertIn("new router\r\n", message)
        self.assertEqual(record["router_sha256"], handler.digest(b"new router\r\n"))

    def test_continuously_changing_sources_remain_blocked(self):
        count = 0
        def run(argv, cwd, env):
            nonlocal count
            count += 1
            if "doctor" in argv:
                (self.repo / "ENGINEERING_HARNESS.md").write_text(str(count))
            return self.fake_run(argv, cwd, env)
        with patch.object(handler, "runtime_paths", self.paths), self.assertRaises(handler.Blocked):
            handler.deliver(self.config, self.event, run)
        self.assertEqual(count, 4)

    def test_complete_read_digest_and_capacity_are_required(self):
        self.config.read_sha256 = "f" * 64
        with patch.object(handler, "runtime_paths", self.paths), self.assertRaises(handler.Blocked):
            handler.deliver(self.config, run=self.fake_run)
        self.config.read_sha256 = handler.content(self.sources)[1]["body_sha256"]
        self.config.read_limit = 1
        with patch.object(handler, "runtime_paths", self.paths), self.assertRaises(handler.Blocked):
            handler.deliver(self.config, run=self.fake_run)

    def test_marker_order_and_duplicates_are_rejected(self):
        for raw in (handler.END + handler.BEGIN, handler.BEGIN * 2 + handler.END, handler.BEGIN):
            with self.assertRaises(ValueError):
                handler.content({**self.sources, "AGENTS.md": raw})

    def test_evaluator_environment_does_not_mutate_parent(self):
        with patch.dict(handler.os.environ, {"PYTHONPATH": "untrusted", "PYTHONHOME": "untrusted"}):
            result = handler.evaluator_environment(Path("/prepared/bin/python"))
            self.assertNotIn("PYTHONPATH", result)
            self.assertNotIn("PYTHONHOME", result)
            self.assertEqual(handler.os.environ["PYTHONPATH"], "untrusted")

    def test_malformed_findings_do_not_prevent_unready_output(self):
        for data in ({}, {"checks": None}, {"checks": [None]}, {"diagnostics": "wrong"}):
            self.assertEqual(handler.finding_summary([{"result": data}]), "")
        self.assertIn("RID021", handler.finding_summary([{"result": {
            "diagnostics": [{"code": "RID021", "message": "identity mismatch"}]}}]))


if __name__ == "__main__":
    unittest.main()
