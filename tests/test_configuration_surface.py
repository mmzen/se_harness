"""SPEC-DST-026: the installed configuration declares only keys the harness reads."""

from __future__ import annotations

import json
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest import mock

from se_harness import __version__
from se_harness.engine.validate_engineering_artifacts import load_revision_policy
from se_harness.installer import HarnessError, apply_changes, plan_install
from se_harness.integrity import canonical_sha256
from se_harness.preflight import inspect_installation
from se_harness.workflow import _revision_policy
from tests.mutation_guard_support import trusted_mutation_authority


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CONFIG = ".engineering-harness.toml"
LOCK = ".engineering-harness.lock"

#: SPEC-DST-026 DST-CFG-013: every declared key, beside the module that reads it.
#: A key with no reader does not belong in a hash-locked file, because the
#: integrity check would then defend a promise the tool never keeps.
READERS = {
    "harness": {
        # mutation_guard._configured_version; a missing value is MG001.
        "tool_version": "se_harness/mutation_guard.py",
        # installer.plan_install carries both values across an upgrade.
        "installed_at": "se_harness/installer.py",
        "project_name": "se_harness/installer.py",
    },
    "revision_provenance": {
        # load_revision_policy; E010 for an uncovered verified work order.
        "required_for_verified_work": "se_harness/engine/validate_engineering_artifacts.py",
        # workflow._revision_policy; QGS-EDGE closes the release transition.
        "required_for_release": "se_harness/workflow.py",
    },
}

#: SPEC-DST-026 DST-CFG-003 to DST-CFG-005: the keys WO-DST-025 removed, in the
#: shape released 0.16.0 wrote them.
RETIRED_CONFIG = (
    "[harness]\n"
    "schema_version = 2\n"
    'tool_version = "0.16.0"\n'
    'installed_at = "{installed_at}"\n'
    'project_name = "{project_name}"\n'
    'artifact_root = "docs/engineering"\n'
    'dashboard_output = "target/harness-dashboard"\n'
    "\n"
    "[revision_provenance]\n"
    "require_full_commit = true\n"
    "require_clean_worktree = true\n"
    "required_for_verified_work = true\n"
    "required_for_release = true\n"
    'verification_record_status = "ready"\n'
    'release_record_status = "ready"\n'
)

RETIRED_KEYS = (
    "schema_version",
    "artifact_root",
    "dashboard_output",
    "require_full_commit",
    "require_clean_worktree",
    "verification_record_status",
    "release_record_status",
)


class ConfigurationSurfaceTests(unittest.TestCase):
    def setUp(self) -> None:
        guard = mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=trusted_mutation_authority,
        )
        guard.start()
        self.addCleanup(guard.stop)

    def install(self, temporary: str, *, project_name: str = "Fixture") -> Path:
        target = Path(temporary) / "repository"
        changes, old_lock = plan_install(target, project_name=project_name, mode="init")
        apply_changes(target, changes, old_lock, allow_updates=False)
        return target

    def rebind(self, target: Path, relative: str) -> None:
        """Record the current bytes as the installed bytes, as an install would."""

        lock_path = target / LOCK
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"][relative]["sha256"] = canonical_sha256((target / relative).read_bytes())
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def test_installed_configuration_declares_only_keys_a_reader_uses(self) -> None:
        # DST-CFG-001, DST-CFG-002, DST-CFG-012, DST-CFG-013.
        with tempfile.TemporaryDirectory() as temporary:
            target = self.install(temporary, project_name="Example")
            config = tomllib.loads((target / CONFIG).read_text(encoding="utf-8"))

            self.assertEqual(sorted(READERS), sorted(config))
            for table, readers in READERS.items():
                self.assertEqual(sorted(readers), sorted(config[table]), table)
                for key, reader in readers.items():
                    source = REPOSITORY_ROOT / reader
                    self.assertIn(key, source.read_text(encoding="utf-8"), f"{key} has no reader in {reader}")

            self.assertEqual(__version__, config["harness"]["tool_version"])
            self.assertEqual("Example", config["harness"]["project_name"])
            self.assertTrue(config["revision_provenance"]["required_for_verified_work"])
            self.assertTrue(config["revision_provenance"]["required_for_release"])

    def test_the_retired_keys_are_declared_nowhere(self) -> None:
        # DST-CFG-003 to DST-CFG-005: the template is the only place they could
        # come back from, and no test fixture may reintroduce them silently.
        template = REPOSITORY_ROOT / "templates/repository/standard/.engineering-harness.toml.tpl"
        rendered = template.read_text(encoding="utf-8")
        for key in RETIRED_KEYS:
            self.assertNotIn(key, rendered, key)

    def test_the_retired_keys_change_no_behaviour(self) -> None:
        # DST-CFG-007, DST-CFG-011: an unknown key is still tolerated, and the
        # two provenance loaders read the same policy through it.
        with tempfile.TemporaryDirectory() as temporary:
            target = self.install(temporary)
            lean = (load_revision_policy(target), _revision_policy(target))
            self.assertEqual([], [item for item in inspect_installation(target) if not item.passed])

            (target / CONFIG).write_text(
                RETIRED_CONFIG.format(installed_at="2026-09-01", project_name="Fixture"),
                encoding="utf-8",
            )
            self.rebind(target, CONFIG)

            self.assertEqual(lean, (load_revision_policy(target), _revision_policy(target)))
            # The lock still calls the file unchanged; only the drift against the
            # new template shows, and `upgrade --apply` is what closes it.
            self.assertEqual(
                [f"distribution:{CONFIG}"],
                [item.name for item in inspect_installation(target) if not item.passed],
            )

    def test_upgrade_removes_the_retired_keys_and_preserves_owner_values(self) -> None:
        # DST-CFG-008, DST-CFG-009.
        with tempfile.TemporaryDirectory() as temporary:
            target = self.install(temporary, project_name="Consumer")
            (target / CONFIG).write_text(
                RETIRED_CONFIG.format(installed_at="2026-09-01", project_name="Consumer"),
                encoding="utf-8",
            )
            self.rebind(target, CONFIG)

            changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
            actions = {item.path: item.action for item in changes}
            self.assertEqual("update", actions[CONFIG])
            apply_changes(target, changes, old_lock, allow_updates=True)

            config = tomllib.loads((target / CONFIG).read_text(encoding="utf-8"))
            self.assertEqual(sorted(READERS), sorted(config))
            for table, readers in READERS.items():
                self.assertEqual(sorted(readers), sorted(config[table]), table)
            self.assertEqual("Consumer", config["harness"]["project_name"])
            self.assertEqual("2026-09-01", config["harness"]["installed_at"])
            self.assertEqual(__version__, config["harness"]["tool_version"])
            self.assertEqual([], [item for item in inspect_installation(target) if not item.passed])

    def test_upgrade_refuses_a_customized_configuration(self) -> None:
        # DST-CFG-010.
        with tempfile.TemporaryDirectory() as temporary:
            target = self.install(temporary, project_name="Consumer")
            (target / CONFIG).write_text(
                RETIRED_CONFIG.format(installed_at="2026-09-01", project_name="Consumer"),
                encoding="utf-8",
            )
            self.rebind(target, CONFIG)
            with (target / CONFIG).open("a", encoding="utf-8") as handle:
                handle.write('owner_note = "edited by hand"\n')
            before = (target / CONFIG).read_bytes()
            lock_before = (target / LOCK).read_bytes()

            changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
            actions = {item.path: item.action for item in changes}
            self.assertEqual("customized", actions[CONFIG])
            with self.assertRaisesRegex(HarnessError, "customizations"):
                apply_changes(target, changes, old_lock, allow_updates=True)

            self.assertEqual(before, (target / CONFIG).read_bytes())
            self.assertEqual(lock_before, (target / LOCK).read_bytes())


if __name__ == "__main__":
    unittest.main()
