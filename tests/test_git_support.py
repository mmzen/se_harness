"""WO-CIP-010: real Git controls for disposable repository cleanup (issue #269)."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from repository_tools.upgrade_rehearsal import export_tracked_tree
from tests.git_support import git, git_available, init_repository, run_git


@unittest.skipUnless(git_available(), "git is unavailable")
class DisposableGitTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / "source"
        self.root.mkdir()
        self.config = self.base / "parent.gitconfig"
        # A real maintenance task with a low trigger; keep the positive control
        # in the foreground so the regression test never creates a teardown race.
        self.config.write_text(
            "[maintenance]\n\tauto = true\n\tautoDetach = false\n"
            "[maintenance \"gc\"]\n\tenabled = false\n"
            "[maintenance \"loose-objects\"]\n\tenabled = true\n\tauto = 1\n"
            "[gc]\n\tauto = 1\n\tautoDetach = false\n"
            "[commit]\n\tgpgsign = true\n", encoding="utf-8",
        )
        self.original_config = self.config.read_bytes()
        self.environment = {
            "GIT_CONFIG_GLOBAL": str(self.config), "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_COUNT": "0",
        }
        self.environment_patch = patch.dict(os.environ, self.environment)
        self.environment_patch.start()
        self.addCleanup(self.environment_patch.stop)
        init_repository(self.root)
        for number in range(3):
            (self.root / f"file-{number}.txt").write_text(f"unique content {number}\n", encoding="utf-8")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-q", "-m", "fixture")

    @staticmethod
    def children(trace: Path) -> list[list[str]]:
        return [event["argv"] for line in trace.read_text(encoding="utf-8").splitlines()
                if (event := json.loads(line))["event"] == "child_start"]

    def test_fixture_and_rehearsal_block_real_automatic_maintenance(self) -> None:
        # CLN01/02: the enabled control must perform real packing; the negative
        # assertion alone could pass if this fixture never triggered maintenance.
        for route in ("fixture", "rehearsal"):
            with self.subTest(route=route):
                trace = self.base / f"{route}.jsonl"
                with patch.dict(os.environ, {"GIT_TRACE2_EVENT": str(trace)}):
                    if route == "fixture":
                        target = self.root
                        git(target, "commit", "--allow-empty", "-q", "-m", "safe fixture")
                    else:
                        target = self.base / "export"
                        target.mkdir()
                        export_tracked_tree(self.root, target)
                self.assertFalse(any("maintenance" in argv or "gc" in argv
                                     for argv in self.children(trace)))
                self.assertEqual([], list((target / ".git/objects/pack").glob("*.pack")))
                self.assertEqual("", git(target, "status", "--porcelain"))

                positive = self.base / f"{route}-positive.jsonl"
                git(target, "-c", "maintenance.auto=true", "-c", "gc.auto=1",
                    "commit", "--allow-empty", "-q", "-m", "positive control",
                    env={"GIT_TRACE2_EVENT": str(positive)})
                children = self.children(positive)
                self.assertTrue(any("maintenance" in argv for argv in children), children)
                self.assertTrue(any("pack-objects" in argv for argv in children), children)
                self.assertTrue(list((target / ".git/objects/pack").glob("*.pack")))
                self.assertEqual(self.original_config, self.config.read_bytes())

    def test_fixture_command_overrides_inherited_config_without_changing_it(self) -> None:
        self.assertEqual("false", git(self.root, "config", "--bool", "maintenance.auto"))
        self.assertEqual("0", git(self.root, "config", "--int", "gc.auto"))
        self.assertEqual("false", git(self.root, "config", "--bool", "commit.gpgsign"))
        self.assertEqual("true", git(self.root, "config", "--global", "--bool", "maintenance.auto"))
        self.assertEqual("1", git(self.root, "config", "--global", "--int", "gc.auto"))
        self.assertEqual("Fixture <fixture@example.invalid>", git(self.root, "log", "-1", "--format=%an <%ae>"))
        self.assertEqual(self.original_config, self.config.read_bytes())

    def test_output_and_git_failures_retain_the_helper_contract(self) -> None:
        payload = "UTF-8: caf\u00e9\n".encode("utf-8")
        (self.root / "text.txt").write_bytes(payload)
        git(self.root, "add", "text.txt")
        git(self.root, "commit", "-q", "-m", "UTF-8")
        self.assertEqual(payload, git(self.root, "show", "HEAD:text.txt", binary=True))
        self.assertEqual(payload.decode("utf-8").strip(), git(self.root, "show", "HEAD:text.txt"))
        self.assertNotEqual(0, run_git(self.root, "rev-parse", "--verify", "refs/heads/absent", check=False).returncode)
        with self.assertRaises(subprocess.CalledProcessError):
            git(self.root, "rev-parse", "--verify", "refs/heads/absent")


if __name__ == "__main__":
    unittest.main()
