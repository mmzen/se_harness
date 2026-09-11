"""Pure owned-shell query tests: no Windows process handle is opened."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).absolute().parent))
from c09_shell_observer import Collector


class FakeQuery:
    def __init__(self):
        self.images = {1: r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe", 2: r"C:\runtime\python.exe"}
        self.creations = {1: 100, 2: 200}
        self.members = {1: True, 2: True}
        self.calls = []
        self.text = "powershell.exe -NoProfile -Command public-fixture"

    def pids(self): return list(self.images)
    def open(self, pid): self.calls.append(("open", pid)); return pid
    def member(self, handle): self.calls.append(("member", handle)); return self.members[handle]
    def created(self, handle): self.calls.append(("created", handle)); return self.creations[handle]
    def image(self, handle): self.calls.append(("image", handle)); return self.images[handle]
    def command(self, handle): self.calls.append(("command", handle)); return self.text
    def close(self, handle): self.calls.append(("close", handle))


class OwnedShells(unittest.TestCase):
    def test_only_owned_shell_command_is_read_after_membership_and_creation_checks(self):
        query = FakeQuery()
        collector = Collector(query, lambda text: text)
        collector.poll()
        self.assertEqual([call for call in query.calls if call[0] == "command"], [("command", 1)])
        self.assertLess(query.calls.index(("member", 1)), query.calls.index(("command", 1)))
        self.assertLess(query.calls.index(("created", 1)), query.calls.index(("command", 1)))
        self.assertEqual([row["pid"] for row in collector.result()["records"]], [1])
        self.assertTrue(collector.records[0]["raw_command_line_retained"])
        self.assertIn(("close", 1), query.calls)
        self.assertIn(("close", 2), query.calls)

    def test_unowned_pid_is_never_read_and_capture_failure_is_optional(self):
        query = FakeQuery()
        query.members[1] = False
        collector = Collector(query, lambda text: text)
        collector.poll()
        self.assertNotIn(("image", 1), query.calls)
        self.assertNotIn(("command", 1), query.calls)
        self.assertEqual(collector.result()["status"], "unavailable")
        self.assertNotIn("enforcement_observed", collector.result())

    def test_repeated_pid_creation_is_cached_but_pid_reuse_is_observed(self):
        query = FakeQuery()
        collector = Collector(query, lambda text: text)
        collector.poll()
        collector.poll()
        self.assertEqual(len(collector.records), 1)
        query.creations[1] = 300
        collector.poll()
        self.assertEqual([row["creation_filetime"] for row in collector.records], [100, 300])

    def test_sanitized_command_is_ineligible_as_exact_selector(self):
        query = FakeQuery()
        query.text = "secret command fixture"
        collector = Collector(query, lambda text: text.replace("secret", "<redacted>"))
        collector.poll()
        self.assertFalse(collector.records[0]["selector_eligible"])
        self.assertFalse(collector.records[0]["raw_command_line_retained"])
        self.assertNotIn("secret", collector.records[0]["command_line"])

    def test_query_error_does_not_leak_exception_payload_or_escape(self):
        query = FakeQuery()
        def denied(handle): raise PermissionError("private command text")
        query.command = denied
        collector = Collector(query, lambda text: text)
        collector.poll()
        self.assertEqual(collector.result()["status"], "unavailable")
        self.assertNotIn("private command text", str(collector.result()))
        self.assertIn(("close", 1), query.calls)

    def test_job_list_failure_or_oversize_never_opens_any_process(self):
        for oversized in (False, True):
            query = FakeQuery()
            def failed(): raise OSError("query unavailable")
            query.pids = (lambda: list(range(300))) if oversized else failed
            collector = Collector(query, lambda text: text)
            collector.poll()
            self.assertEqual(query.calls, [])
            self.assertEqual(collector.result()["status"], "unavailable")


if __name__ == "__main__":
    unittest.main()
