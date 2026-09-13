"""User-facing plugin migration behavior, also runnable against an installed wheel."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

from se_harness import skill_ownership as ownership
from se_harness.installer import HarnessError, load_lock

CATALOG = (
    ".agents/skills/harness-orient/SKILL.md",
    ".agents/skills/harness-orient/skill-contract.json",
    ".agents/skills/harness-orient/scripts/orient.py",
    ".agents/skills/harness-operator-brief/SKILL.md",
    ".agents/skills/harness-operator-brief/skill-contract.json",
    ".agents/skills/harness-operator-brief/scripts/check_brief.py",
    ".claude/skills/harness-orient/SKILL.md",
)


class SkillOwnershipTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="plugin-migration-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.root = self.base / "repository"
        self.root.mkdir()
        self.plugin = self.base / "plugin"
        self.write(self.plugin / ".codex-plugin/plugin.json", '{"name":"verity-plane","version":"1.0"}')
        for name in CATALOG:
            self.write(self.root / name, "old skill")
            if name.startswith(".agents/"):
                self.write(self.plugin / name.removeprefix(".agents/"), "replacement")
        self.original_lock = {
            "schema": 3, "hash_algorithm": "sha256", "hash_mode": "utf8-text-lf-v1",
            "tool_version": "0.17.0",
            "evaluator": {"version": "0.17.0", "payload_manifest": "se-harness-installed-payload-v1",
                          "payload_sha256": "a" * 64},
            "files": {name: {"mode": "managed", "sha256": "b" * 64} for name in CATALOG},
        }
        self.write(self.root / ownership.LOCK_NAME, json.dumps(self.original_lock))
        self.write(self.root / "README.md", "my project")
        self.write(self.root / ".agents/skills/my-skill/SKILL.md", "my unrelated skill")

    @staticmethod
    def write(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def migrate(self):
        return ownership.apply_skill_ownership(self.root, provider="plugin", plugin_root=self.plugin)

    def test_plan_is_read_only_and_apply_replaces_disposable_skills(self):
        plan = ownership.plan_skill_ownership(self.root, provider="plugin", plugin_root=self.plugin)
        self.assertEqual("planned", plan["outcome"])
        self.assertTrue(all((self.root / path).exists() for path in CATALOG))
        result = self.migrate()
        self.assertEqual("applied", result["outcome"])
        self.assertFalse(any((self.root / path).exists() for path in CATALOG))
        lock = load_lock(self.root)
        self.assertEqual({"provider": "plugin"}, lock["skill_ownership"])
        self.assertEqual(self.original_lock["evaluator"], lock["evaluator"])
        self.assertEqual({}, lock["files"])
        self.assertEqual("my project", (self.root / "README.md").read_text())
        self.assertEqual("my unrelated skill", (self.root / ".agents/skills/my-skill/SKILL.md").read_text())
        self.assertEqual("replacement", (self.plugin / "skills/harness-orient/SKILL.md").read_text())

    def test_modified_missing_and_extra_old_skill_files_do_not_block_replacement(self):
        self.write(self.root / CATALOG[0], "edited old skill")
        (self.root / CATALOG[1]).unlink()
        self.write(self.root / ".agents/skills/harness-orient/old-notes.txt", "disposable")
        self.write(self.root / ".claude/skills/harness-operator-brief/SKILL.md", "old copy")
        lock = load_lock(self.root)
        del lock['files'][CATALOG[1]]
        lock['files']['README.md'] = {'mode': 'managed', 'sha256': 'c'*64}
        self.write(self.root / ownership.LOCK_NAME, json.dumps(lock))
        self.migrate()
        for directory in ownership.SKILL_DIRECTORIES:
            self.assertFalse((self.root / directory).exists())

    def test_repeating_migration_is_harmless_and_cleans_reintroduced_copies(self):
        self.migrate()
        self.assertEqual("unchanged", self.migrate()["outcome"])
        self.write(self.root / CATALOG[0], "old copy returned")
        self.migrate()
        self.assertFalse((self.root / CATALOG[0]).exists())

    def test_plugin_updates_do_not_require_new_hashes_or_evaluator_identity(self):
        self.migrate()
        self.write(self.plugin / "skills/harness-orient/scripts/orient.py", "new helper")
        self.write(self.plugin / ".codex-plugin/plugin.json", '{"name":"verity-plane","version":"2.0","new_field":true}')
        self.assertEqual("unchanged", self.migrate()["outcome"])

    def test_claude_plugin_is_accepted(self):
        (self.plugin / ".codex-plugin/plugin.json").unlink()
        self.write(self.plugin / ".claude-plugin/plugin.json", '{"name":"verity-plane"}')
        self.assertTrue(self.migrate()["passed"])

    def test_missing_replacement_skill_stops_before_deleting_old_skills(self):
        (self.plugin / "skills/harness-orient/SKILL.md").unlink()
        with self.assertRaisesRegex(ownership.OwnershipError, "replacement skill missing"):
            self.migrate()
        self.assertTrue(all((self.root / name).exists() for name in CATALOG))
        self.assertEqual(self.original_lock, load_lock(self.root))

    def test_missing_repository_lock_stops_before_deleting_skills(self):
        (self.root / ownership.LOCK_NAME).unlink()
        with self.assertRaisesRegex(ownership.OwnershipError, "initialize the repository"):
            self.migrate()
        self.assertTrue(all((self.root / name).exists() for name in CATALOG))

    def test_malformed_lock_or_wrong_plugin_stops_before_deletion(self):
        self.write(self.root / ownership.LOCK_NAME, '{invalid')
        with self.assertRaises(HarnessError):
            self.migrate()
        self.assertTrue(all((self.root / name).exists() for name in CATALOG))
        self.write(self.root / ownership.LOCK_NAME, json.dumps(self.original_lock))
        self.write(self.plugin / '.codex-plugin/plugin.json', '{"name":"another-plugin"}')
        with self.assertRaisesRegex(ownership.OwnershipError, 'select the verity-plane'):
            self.migrate()
        self.assertTrue(all((self.root / name).exists() for name in CATALOG))

    def test_old_schema_four_metadata_is_readable_and_normalized(self):
        self.migrate()
        lock = load_lock(self.root)
        lock['skill_ownership'].update(schema='se-harness-skill-ownership-v1', plugin={'version':'old'}, checksum='old')
        self.write(self.root / ownership.LOCK_NAME, json.dumps(lock))
        self.assertEqual('plugin', load_lock(self.root)['skill_ownership']['provider'])
        self.migrate()
        self.assertEqual({'provider':'plugin'}, load_lock(self.root)['skill_ownership'])
        lock['skill_ownership']['provider'] = 'unknown'
        self.write(self.root / ownership.LOCK_NAME, json.dumps(lock))
        with self.assertRaises(HarnessError):
            load_lock(self.root)

    def test_retry_finishes_after_partial_deletion(self):
        original = shutil.rmtree
        calls = 0
        def interrupt(path):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("interrupted deletion")
            original(path)
        with mock.patch.object(ownership.shutil, "rmtree", side_effect=interrupt):
            with self.assertRaisesRegex(OSError, "interrupted deletion"):
                self.migrate()
        self.assertEqual(3, load_lock(self.root)["schema"])
        self.assertTrue(self.migrate()["passed"])
        self.assertEqual(4, load_lock(self.root)["schema"])

    def test_retry_finishes_if_saving_the_lock_fails(self):
        with mock.patch.object(ownership, "atomic_write_bytes", side_effect=OSError("disk unavailable")):
            with self.assertRaisesRegex(OSError, "disk unavailable"):
                self.migrate()
        self.assertTrue(self.migrate()["passed"])
        self.assertEqual("unchanged", self.migrate()["outcome"])

    def test_plugin_inside_deleted_skill_directory_is_rejected(self):
        nested = self.root / ".agents/skills/harness-orient/plugin"
        shutil.copytree(self.plugin, nested)
        with self.assertRaisesRegex(ownership.OwnershipError, "inside a skill directory"):
            ownership.apply_skill_ownership(self.root, provider="plugin", plugin_root=nested)
        self.assertTrue((nested / ".codex-plugin/plugin.json").exists())

    def test_linked_skill_parent_does_not_delete_another_directory(self):
        outside = self.base / "elsewhere"
        (self.root / ".agents").rename(outside)
        try:
            (self.root / ".agents").symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"directory symlinks unavailable: {error}")
        with self.assertRaisesRegex(ownership.OwnershipError, "linked skill path"):
            self.migrate()
        self.assertTrue((outside / "skills/harness-orient/SKILL.md").exists())

    def test_restore_replaces_old_skills_and_can_be_repeated(self):
        self.migrate()
        self.write(self.root / CATALOG[0], "disposable local copy")
        result = ownership.apply_skill_ownership(self.root, provider="repository")
        self.assertEqual("applied", result["outcome"])
        self.assertEqual(3, load_lock(self.root)["schema"])
        self.assertTrue(all((self.root / name).is_file() for name in CATALOG))
        self.assertNotEqual("disposable local copy", (self.root / CATALOG[0]).read_text())
        self.assertEqual("unchanged", ownership.apply_skill_ownership(self.root, provider="repository")["outcome"])

    def test_portable_provider_record_does_not_require_local_plugin(self):
        self.migrate()
        shutil.rmtree(self.plugin)
        from se_harness.installer import effective_template_files
        paths = {item.target.as_posix() for item in effective_template_files(load_lock(self.root))}
        self.assertFalse(paths.intersection(CATALOG))


if __name__ == "__main__":
    unittest.main()
