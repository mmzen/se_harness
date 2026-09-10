"""Mapping/denial boundaries, plus real owned-process cleanup on Windows."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[3] / "plugins/verity-plane/common/scripts/check-tool-action.py"
spec = importlib.util.spec_from_file_location("tool_action", SCRIPT)
handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler)


def config(repo, **changes):
    values = dict(repo=str(repo), host="claude", artifact="WO-TEST-001", refusal_mode="deny",
                  inner_timeout=2, cleanup_margin=1, startup_margin=.5, output_margin=.5, host_timeout=5)
    values.update(changes)
    return argparse.Namespace(**values)


class MappingBoundaries(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.cfg = config(self.repo)
        self.event = {"hook_event_name": "PreToolUse", "cwd": str(self.repo), "tool_name": "Write",
                      "tool_input": {"file_path": "inside.txt", "content": "new"}}

    def test_write_and_edit_use_the_actual_path(self):
        for tool, data in (("Write", {"file_path": "inside.txt", "content": "new"}),
                           ("Edit", {"file_path": str(self.repo / "inside.txt"), "old_string": "a", "new_string": "b"})):
            result = handler.map_action(self.cfg, {**self.event, "tool_name": tool, "tool_input": data})
            self.assertEqual(result["paths"], ["inside.txt"])
            self.assertEqual(result["checkpoint"], "pre-action")
            self.assertEqual(result["procedure"], "PROC-WO-IMPLEMENT")

    def test_patch_move_includes_both_paths(self):
        command = "*** Begin Patch\n*** Update File: old.txt\n*** Move to: new.txt\n@@\n-a\n+b\n*** Delete File: gone.txt\n*** Add File: added.txt\n+x\n*** End Patch"
        event = {**self.event, "tool_name": "apply_patch", "tool_input": {"command": command}}
        result = handler.map_action(config(self.repo, host="codex"), event)
        self.assertEqual(result["paths"], ["added.txt", "gone.txt", "new.txt", "old.txt"])

    def test_patch_shell_wrappers_and_unknown_syntax_are_refused(self):
        for value in ("echo bad", "*** Begin Patch\n*** Add File: x\n*** End Patch",
                      "*** Begin Patch\n*** Unknown: x\n*** End Patch",
                      "*** Begin Patch\n*** Add File: x\n+ok\n*** End Patch\nrun evil"):
            with self.assertRaises(handler.CoverageError):
                handler.patch_paths(value)

    def test_outside_traversal_and_stream_paths_are_refused(self):
        for name in ("../outside", str(self.repo.parent / "outside"), "inside.txt:stream", "x\nother", " x"):
            with self.assertRaises(ValueError):
                handler.map_action(self.cfg, {**self.event, "tool_input": {"file_path": name, "content": "new"}})

    def test_hardlink_alias_cannot_change_another_target(self):
        original = self.repo / "original.txt"
        alias = self.repo / "alias.txt"
        original.write_text("retained")
        os.link(original, alias)
        with self.assertRaises(handler.CoverageError):
            handler.mapped_path(self.repo, "alias.txt")
        self.assertEqual(original.read_text(), "retained")

    def test_event_fields_cannot_weaken_the_fixed_checkpoint(self):
        for key in ("checkpoint", "procedure", "changed_paths", "skip_check"):
            with self.assertRaises(handler.CoverageError):
                handler.map_action(self.cfg, {**self.event, key: "scope"})

    def test_recursion_marker_does_not_exempt_a_shell(self):
        event = {**self.event, "tool_name": "Bash", "tool_input": {"command": "write target"}, "recursion_marker": True}
        with self.assertRaises(handler.CoverageError):
            handler.map_action(self.cfg, event)

    def test_malformed_tool_data_is_refused(self):
        for data in ({}, {"file_path": "x", "content": None}, {"file_path": "x", "content": "a", "path": "other"}):
            with self.assertRaises(handler.CoverageError):
                handler.map_action(self.cfg, {**self.event, "tool_input": data})

    def test_denial_schema_and_no_permission_escalation(self):
        denied = handler.response(True, "blocked")["hookSpecificOutput"]
        self.assertEqual(denied, {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "blocked"})
        self.assertNotIn("permissionDecision", handler.response(False, "checked")["hookSpecificOutput"])
        self.assertNotIn("hookSpecificOutput", handler.response(True, "gap", False))

    def test_malformed_results_never_count_as_a_pass(self):
        valid = {"schema": "se-harness-workflow-result-v2", "operation": {"outcome": "completed"},
                 "compliance": {"status": "pass"}, "selection": {"primary": "WO-TEST-001"}}
        self.assertTrue(handler.checked_result(valid, "WO-TEST-001"))
        for data in ({}, {**valid, "operation": None}, {**valid, "compliance": []},
                     {**valid, "selection": {"primary": "WO-OTHER-001"}}):
            self.assertFalse(handler.checked_result(data, "WO-TEST-001"))

    def test_budget_is_one_deadline_and_requires_strict_margin(self):
        budget = handler.Deadline(self.cfg, entered=time.monotonic())
        before = budget.inner_end
        self.assertGreater(budget.remaining(), 0)
        self.assertEqual(budget.inner_end, before)
        for changes in ({"inner_timeout": 3}, {"host_timeout": float("nan")}, {"cleanup_margin": 0}):
            with self.assertRaises(handler.CoverageError):
                handler.Deadline(config(self.repo, **changes), entered=time.monotonic())
        with self.assertRaises(TimeoutError):
            handler.Deadline(self.cfg, entered=time.monotonic() - 10).remaining()


@unittest.skipUnless(os.name == "nt", "owned-process implementation currently qualifies Windows only")
class ProcessBoundaries(unittest.TestCase):
    def test_successful_child_is_collected_before_result(self):
        budget = handler.Deadline(config(Path.cwd()), entered=time.monotonic())
        result = budget.run([sys.executable, "-I", "-c", "print('{}')"], Path.cwd(), os.environ.copy())
        self.assertEqual(result["exit_status"], 0)
        self.assertEqual(result["cleanup"]["active_processes"], 0)
        self.assertEqual(result["cleanup"]["exited_processes"], result["cleanup"]["total_processes"])

    def test_stalled_child_tree_is_stopped_within_the_reserved_margin(self):
        cfg = config(Path.cwd(), inner_timeout=.6, cleanup_margin=1, host_timeout=4)
        budget = handler.Deadline(cfg, entered=time.monotonic())
        code = "import subprocess,sys,time; subprocess.Popen([sys.executable,'-I','-c','import time; time.sleep(30)']); time.sleep(30)"
        with self.assertRaises(handler.session.Blocked):
            budget.run([sys.executable, "-I", "-c", code], Path.cwd(), os.environ.copy())
        record = budget.records[-1]
        self.assertGreaterEqual(record["cleanup"]["total_processes"], 2)
        self.assertEqual(record["cleanup"]["active_processes"], 0)
        self.assertEqual(record["cleanup"]["exited_processes"], record["cleanup"]["total_processes"])
        self.assertLess(record["finished_monotonic"], budget.output_end)

    def test_multiple_calls_do_not_reset_the_inner_deadline(self):
        budget = handler.Deadline(config(Path.cwd(), inner_timeout=.65), entered=time.monotonic())
        argv = [sys.executable, "-I", "-c", "import time; time.sleep(.4); print('{}')"]
        budget.run(argv, Path.cwd(), os.environ.copy())
        with self.assertRaises(handler.session.Blocked):
            budget.run(argv, Path.cwd(), os.environ.copy())
        self.assertEqual(len(budget.records), 2)
        self.assertEqual(budget.records[0]["inner_deadline_monotonic"], budget.records[1]["inner_deadline_monotonic"])


if __name__ == "__main__":
    unittest.main()
