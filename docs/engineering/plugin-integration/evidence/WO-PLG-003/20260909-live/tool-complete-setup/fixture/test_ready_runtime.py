"""Negative reporting tests, not synthetic proof of Codex host behavior."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("ready_observer", Path(__file__).with_name("observe_ready_runtime.py"))
observer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(observer)


def result(data, **changes):
    record = {"exit_status": 0, "timed_out": False, "output_truncated": False, "result": data}
    record.update(changes)
    return record


class ReadinessEvidenceTests(unittest.TestCase):
    def test_utf8_input_with_bom_is_supported(self):
        event = {"cwd": str(Path.cwd()), "hook_event_name": "SessionStart"}
        self.assertEqual(observer.parse_event(b"\xef\xbb\xbf" + json.dumps(event).encode()), event)

    def test_relative_or_oversized_input_is_rejected(self):
        for raw in (b'{"cwd":"relative"}', b" " * (observer.MAX_INPUT + 1)):
            with self.assertRaises(ValueError):
                observer.parse_event(raw)

    def test_failed_identity_prevents_readiness_calls(self):
        calls = []
        def run(argv, cwd):
            calls.append(argv)
            return result({"passed": False})
        reading = observer.observe({"cwd": str(Path.cwd())}, run)
        self.assertFalse(reading["governance_readiness"])
        self.assertEqual(len(calls), 1)
        self.assertIn(observer.ARCHIVE, calls[0])
        self.assertIn(observer.PAYLOAD, calls[0])

    def test_success_exit_or_truthy_text_is_not_boolean_readiness(self):
        for ready in (False, "true", 1, None):
            def run(argv, cwd):
                return result({"passed": True} if argv[0] == "identity" else {"ready": ready})
            self.assertFalse(observer.observe({"cwd": str(Path.cwd())}, run)["governance_readiness"])

    def test_timeout_truncation_and_nonzero_exit_cannot_pass(self):
        for changes in ({"timed_out": True}, {"output_truncated": True}, {"exit_status": 1}):
            self.assertFalse(observer.succeeded(result({"ready": True}, **changes)))

    def test_manifest_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            repo.mkdir()
            (repo.parent / "outside.txt").write_text("outside")
            with self.assertRaises(ValueError):
                observer.read_manifest(repo, ["../outside.txt"])

    def test_current_check_manifest_is_required_and_hashes_exact_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            source = b"controlled fixture\r\n"
            (repo / "AGENTS.md").write_bytes(source)
            def run(argv, cwd):
                data = {"identity": {"passed": True}, "doctor": {}, "preflight": {"ready": True},
                        "check": {"context": {"reading_manifest": ["AGENTS.md"]}}}[argv[0]]
                return result(data)
            reading = observer.observe({"cwd": str(repo), "hook_event_name": "SessionStart"}, run)
            self.assertTrue(reading["governance_readiness"])
            self.assertEqual(reading["manifest_files"][0]["text"], source.decode())
            self.assertEqual(reading["manifest_files"][0]["sha256"], observer.hashlib.sha256(source).hexdigest())
            self.assertIn("No real approval", observer.output_context(reading))
            reading["event"] = "PreToolUse"
            self.assertIsNone(observer.output_context(reading))


if __name__ == "__main__":
    unittest.main()
