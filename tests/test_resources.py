"""External resource selection and its failure boundary (VER-IAR-020)."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from se_harness import __version__, resources
from se_harness.artifact_layout import authoring_checklist, create_artifact
from se_harness.evaluator_identity import installed_evaluator_identity
from se_harness.instruction_discovery import describe, load_catalog, locations
from se_harness.integrity import EXTERNAL_RESOURCE_LAYOUT, HASH_ALGORITHM, HASH_MODE, validate_lock
from se_harness.preflight import inspect_installation
from tests.cli_support import invoke
from tests.mutation_guard_support import patch_mutation_authority


TEMPLATES = Path(__file__).resolve().parents[1] / "templates/repository/standard"
INSTALLED_RESOURCE_ROOT = resources._installed_resource_root


class ResourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repository"
        self.root.mkdir()
        self.bundle = Path(self.temp.name) / "resources"
        shutil.copytree(TEMPLATES, self.bundle)
        self.addCleanup(patch.stopall)
        # Unit fixture only. Independent wheel qualification exercises the real
        # installed-only origin check outside the source checkout.
        patch.object(resources, "_installed_resource_root", return_value=self.bundle).start()
        patch_mutation_authority(self)
        self.lock = {
            "schema": 5, "resource_layout": EXTERNAL_RESOURCE_LAYOUT,
            "tool_version": __version__, "hash_algorithm": HASH_ALGORITHM,
            "hash_mode": HASH_MODE, "evaluator": installed_evaluator_identity().to_lock(),
            "files": {},
        }
        self.write_lock()
        (self.root / resources.CONFIG).write_text(
            f'[harness]\ntool_version = "{__version__}"\nresource_layout = "{EXTERNAL_RESOURCE_LAYOUT}"\nproject_name = "Example"\n',
            encoding="utf-8",
        )

    def write_lock(self):
        (self.root / resources.LOCK).write_text(json.dumps(self.lock), encoding="utf-8")

    def files(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_query_resolves_all_declared_locations_and_renders_only_requested_entry(self):
        before = self.files()
        selected = resources.ResourceSet(self.root)
        result = selected.query()
        self.assertEqual("se-harness-resources-v1", result["schema"])
        entries = {item["resource"]: item for item in result["resources"]}
        for location in locations():
            self.assertIn(location["heading"], entries[location["file"]]["headings"])
            self.assertTrue(Path(entries[location["file"]]["path"]).is_relative_to(self.bundle))
        code, output, error = invoke("resources", str(self.root), "--resource", resources.ENTRY, "--content", "--json")
        self.assertEqual(0, code, error)
        entry = json.loads(output)
        self.assertIn("# Engineering Harness for Example", entry["content"])
        self.assertIn(f"This repository uses SE Harness {__version__}.", entry["content"])
        self.assertNotIn("{{", entry["content"])
        self.assertEqual(before, self.files())
        with self.assertRaisesRegex(resources.ResourceError, "requires one"):
            selected.query(content=True)

    def test_authoring_writes_only_requested_artifact_and_uses_packaged_checklist(self):
        before = self.files()
        for artifact_type, artifact_id in (("requirement", "REQ-TST-001"), ("work_order", "WO-TST-001")):
            change = create_artifact(self.root, domain="product", artifact_type=artifact_type, artifact_id=artifact_id, dry_run=False)
            raw = (self.root / change.path).read_text(encoding="utf-8")
            self.assertIn(f'id = "{artifact_id}"', raw)
            self.assertIn('status = "draft"', raw)
            self.assertTrue(authoring_checklist(self.root, artifact_type))
        added = set(self.files()) - set(before)
        self.assertEqual({"docs/engineering/product/requirements/REQ-TST-001.md", "docs/engineering/product/work-orders/WO-TST-001.md"}, added)
        self.assertFalse((self.root / "docs/engineering/templates").exists())
        checks = inspect_installation(self.root)
        self.assertTrue(all(item.passed for item in checks), checks)

    def test_all_typed_steps_identify_portable_release_references_without_changing_selection(self):
        for pid, procedure in load_catalog()["procedures"].items():
            for sid in procedure["steps"]:
                selected = {"id": pid, "current_step": sid}
                legacy = describe(selected, ["WO-TST-001"])
                external = describe(selected, ["WO-TST-001"], repository=self.root)
                self.assertEqual("se-harness-instruction-discovery-v2", external["schema"])
                self.assertEqual("repository", external["formal_artifact_source"])
                self.assertEqual("released-resource", external["agent_instructions"]["current_step"]["location"]["source"])
                self.assertEqual(legacy["agent_instructions"]["current_step"]["location"]["file"], external["agent_instructions"]["current_step"]["location"]["file"])
                self.assertNotIn(str(self.bundle), json.dumps(external))
                self.assertNotIn(str(self.root), json.dumps(external))

    def test_wrong_version_digest_missing_or_changed_resource_refuses_before_authoring(self):
        for problem in ("version", "digest", "missing", "altered"):
            with self.subTest(problem=problem):
                original = deepcopy(self.lock)
                path = self.bundle / "docs/engineering/templates/REQUIREMENT.template.md"
                raw = path.read_bytes()
                if problem == "version":
                    self.lock["tool_version"] = self.lock["evaluator"]["version"] = "999.0.0"
                elif problem == "digest":
                    self.lock["evaluator"]["payload_sha256"] = "0" * 64
                elif problem == "missing":
                    path.unlink()
                else:
                    path.write_bytes(raw + b"\nchanged\n")
                self.write_lock()
                before = self.files()
                with self.assertRaises(resources.ResourceError):
                    create_artifact(self.root, domain="product", artifact_type="requirement", artifact_id="REQ-TST-001", dry_run=False)
                self.assertEqual(before, self.files())
                self.lock = original
                self.write_lock()
                path.write_bytes(raw)

    def test_unknown_or_escaping_resource_and_concurrent_selection_are_refused(self):
        selected = resources.ResourceSet(self.root)
        for identifier in ("../outside", "/outside", "docs\\outside", "C:/outside", "docs//outside", "unknown.md"):
            with self.subTest(identifier=identifier), self.assertRaises(resources.ResourceError):
                selected.query(identifier)
        (self.root / resources.CONFIG).write_bytes((self.root / resources.CONFIG).read_bytes() + b"\n# changed selection\n")
        with self.assertRaisesRegex(resources.ResourceError, "selection changed"):
            selected.read(resources.ENTRY)

    def test_selection_change_during_mutation_guard_writes_no_artifact(self):
        def change_selection(*args, **kwargs):
            self.lock["evaluator"]["payload_sha256"] = "0" * 64
            self.write_lock()
        with patch("se_harness.artifact_layout.mutation_guard.require_mutation_authority", side_effect=change_selection):
            with self.assertRaisesRegex(resources.ResourceError, "selection changed"):
                create_artifact(self.root, domain="product", artifact_type="requirement", artifact_id="REQ-TST-001", dry_run=False)
        self.assertFalse((self.root / "docs").exists())

    def test_external_layout_cannot_hide_copied_policy_or_downgrade_its_schema(self):
        for field in ("schema", "resource_layout", "files", "skill_ownership"):
            malformed = deepcopy(self.lock)
            malformed[field] = {"schema": 4, "resource_layout": "unknown", "files": {resources.ENTRY: {"mode": "seed", "state": "present"}}, "skill_ownership": {"provider": "plugin"}}[field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_lock(malformed)

    def test_source_tree_is_never_an_external_resource_fallback(self):
        with patch.object(resources, "_installed_resource_root", side_effect=INSTALLED_RESOURCE_ROOT):
            with self.assertRaisesRegex(resources.ResourceError, "installed evaluator wheel"):
                resources.ResourceSet(self.root)

    def test_partial_selection_cannot_fall_back_to_repository_copies(self):
        del self.lock["resource_layout"]
        self.lock["schema"] = 3
        self.write_lock()
        with self.assertRaisesRegex(resources.ResourceError, "layouts differ"):
            resources.uses_external_resources(self.root)
        (self.root / resources.LOCK).unlink()
        with self.assertRaisesRegex(resources.ResourceError, "missing its lock"):
            resources.uses_external_resources(self.root)

    def test_linked_resource_input_is_refused(self):
        entry = self.bundle / (resources.ENTRY + ".tpl")
        outside = Path(self.temp.name) / "entry.tpl"
        outside.write_bytes(entry.read_bytes())
        entry.unlink()
        try:
            entry.symlink_to(outside)
        except OSError:
            self.skipTest("host cannot create symlinks")
        with self.assertRaisesRegex(resources.ResourceError, "linked"):
            resources.ResourceSet(self.root)


if __name__ == "__main__":
    unittest.main()
