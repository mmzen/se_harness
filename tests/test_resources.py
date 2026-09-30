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
from se_harness.engine.validate_engineering_artifacts import validate_repository
from se_harness.instruction_discovery import describe, load_catalog, locations
from se_harness.integrity import EXTERNAL_RESOURCE_LAYOUT, HASH_ALGORITHM, HASH_MODE, validate_lock
from se_harness.preflight import inspect_installation
from se_harness.workflow_result import machine_fields, restitution_digest
from tests.artifact_support import create_base_chain, record_execution_approval
from tests.cli_support import invoke
from tests.fixture_support import standard_repository
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

    def test_empty_external_install_validates_without_creating_an_artifact_directory(self):
        before = self.files()
        report = validate_repository(self.root)
        self.assertTrue(report.valid, report.errors)
        self.assertEqual([], report.artifacts)
        self.assertEqual([], report.advisories)
        self.assertTrue(validate_repository(self.root, self.root / "docs/engineering").valid)
        code, output, error = invoke("validate", str(self.root), "--json")
        self.assertEqual(0, code, output + error)
        self.assertTrue(json.loads(output)["valid"])
        self.assertEqual(before, self.files())
        self.assertFalse((self.root / "docs").exists())

    def test_scaffold_previews_missing_parents_then_creates_only_the_requested_domain(self):
        before = self.files()
        self.assertEqual({resources.CONFIG, resources.LOCK}, set(before))
        args = ("scaffold-domain", str(self.root), "--domain", "example", "--json")
        code, output, error = invoke(*args, "--dry-run")
        self.assertEqual(0, code, error)
        preview = json.loads(output)["changes"]
        self.assertEqual(["docs", "docs/engineering"], [c["path"] for c in preview[:2]])
        self.assertTrue(all(c["action"] == "create" for c in preview))
        self.assertEqual(before, self.files())
        self.assertFalse((self.root / "docs").exists())
        code, output, error = invoke(*args)
        self.assertEqual(0, code, error)
        self.assertEqual(preview, json.loads(output)["changes"])
        self.assertEqual({c["path"] for c in preview},
                         {p.relative_to(self.root).as_posix() for p in (self.root / "docs").rglob("*")} | {"docs"})
        self.assertEqual({"docs/engineering/example/README.md"}, set(self.files()) - set(before))
        for name, raw in before.items():
            self.assertEqual(raw, (self.root / name).read_bytes())
        index = self.root / "docs/engineering/example/README.md"
        index.write_bytes(b"Owner index\r\n")
        before = self.files()
        code, output, error = invoke(*args)
        self.assertEqual(0, code, error)
        self.assertTrue(all(c["action"] == "present" for c in json.loads(output)["changes"]))
        self.assertEqual(before, self.files())

    def test_scaffold_rollback_preserves_preexisting_parent_content(self):
        for existing in (False, True):
            with self.subTest(existing=existing):
                if existing:
                    owner = self.root / "docs/engineering/owner.txt"
                    owner.parent.mkdir(parents=True)
                    owner.write_bytes(b"Owner bytes\r\n")
                before = self.files()
                paths = set(self.root.rglob("*"))
                with patch("se_harness.artifact_layout.atomic_create", side_effect=OSError("interrupted index write")):
                    code, _, error = invoke("scaffold-domain", str(self.root), "--domain", "example")
                self.assertEqual(2, code)
                self.assertIn("interrupted index write", error)
                self.assertEqual(before, self.files())
                self.assertEqual(paths, set(self.root.rglob("*")))

    def test_scaffold_refuses_a_file_in_the_required_parent_path_without_writes(self):
        (self.root / "docs").write_bytes(b"Owner file\r\n")
        before = self.files()
        for preview in ((), ("--dry-run",)):
            with self.subTest(preview=preview):
                code, _, error = invoke("scaffold-domain", str(self.root), "--domain", "example", *preview)
                self.assertEqual(2, code)
                self.assertIn("not a directory", error)
                self.assertEqual(before, self.files())

    def test_scaffold_refuses_a_linked_parent_without_touching_its_destination(self):
        outside = Path(self.temp.name) / "owner"
        outside.mkdir()
        (outside / "keep.txt").write_bytes(b"Owner bytes\r\n")
        try:
            (self.root / "docs").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("host cannot create symlinks")
        before = self.files()
        code, _, error = invoke("scaffold-domain", str(self.root), "--domain", "example")
        self.assertEqual(2, code)
        self.assertRegex(error, "linked|symlink|escape")
        self.assertEqual(before, self.files())
        self.assertEqual([outside / "keep.txt"], list(outside.iterdir()))
        self.assertEqual(b"Owner bytes\r\n", (outside / "keep.txt").read_bytes())

    def test_missing_legacy_or_alternate_artifact_root_remains_an_error(self):
        legacy = Path(self.temp.name) / "legacy"
        standard_repository(legacy)
        artifact_root = (legacy / "docs/engineering").resolve()
        self.assertTrue(artifact_root.is_relative_to(Path(self.temp.name).resolve()))
        shutil.rmtree(artifact_root)
        for root, selected in ((legacy, None), (self.root, self.root / "alternate")):
            with self.subTest(root=root, selected=selected):
                report = validate_repository(root, selected)
                self.assertFalse(report.valid)
                self.assertEqual([], report.advisories)
                self.assertTrue(any(item.code == "E001" and item.message == "artifact root does not exist"
                                    for item in report.errors), report.errors)

    def test_empty_artifact_root_does_not_hide_invalid_selection_or_missing_resources(self):
        config = self.root / resources.CONFIG
        original = config.read_bytes()
        for problem in ("malformed", "missing-lock", "digest", "resources"):
            with self.subTest(problem=problem):
                self.lock["evaluator"] = installed_evaluator_identity().to_lock()
                self.write_lock()
                config.write_bytes(original)
                if problem == "malformed":
                    config.write_bytes(b"[invalid")
                elif problem == "missing-lock":
                    (self.root / resources.LOCK).unlink()
                elif problem == "digest":
                    self.lock["evaluator"]["payload_sha256"] = "0" * 64
                    self.write_lock()
                else:
                    (self.bundle / "docs/engineering/templates/REQUIREMENT.template.md").unlink()
                before = self.files()
                report = validate_repository(self.root)
                self.assertFalse(report.valid)
                self.assertTrue(any(item.code == "E001" for item in report.errors), report.errors)
                self.assertEqual(before, self.files())
                self.assertFalse((self.root / "docs").exists())

    def test_existing_invalid_artifacts_are_not_an_empty_installation(self):
        create_artifact(self.root, domain="product", artifact_type="requirement",
                        artifact_id="REQ-TST-001", dry_run=False)
        path = self.root / "docs/engineering/product/requirements/REQ-TST-001.md"
        path.write_text('+++\nid = [broken\n+++\n', encoding="utf-8")
        before = self.files()
        report = validate_repository(self.root)
        self.assertFalse(report.valid)
        self.assertTrue(report.errors)
        self.assertEqual(before, self.files())

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

    def workflow_fixture(self, status="approved"):
        create_base_chain(self.root, work_order_status=status, operating_contract_status="draft")
        for artifact in (self.root / "docs/engineering/product").rglob("*.md"):
            artifact.write_text(artifact.read_text(encoding="utf-8").replace("WO-001", "WO-TST-001"), encoding="utf-8")
        original_path = self.root / "docs/engineering/product/work-orders/WO-001.md"
        path = original_path.with_name("WO-TST-001.md")
        original_path.rename(path)
        path.write_text(path.read_text(encoding="utf-8").replace(
            "[relations]",
            '[assurance]\ncommit_bound_verification = "required"\n'
            'rationale = "Exact candidate required."\ndecided_by = "repository-owner"\n\n'
            '[execution_scope]\npaths = ["src/component/"]\n\n[relations]', 1,
        ), encoding="utf-8")
        record_execution_approval(path)
        return path

    def test_public_results_preserve_legacy_lifecycle_and_scope_verdicts(self):
        work = self.workflow_fixture()
        legacy = Path(self.temp.name) / "legacy"
        standard_repository(legacy)
        shutil.copytree(self.root / "docs/engineering/product", legacy / "docs/engineering/product", dirs_exist_ok=True)
        # Byte-preservation setup remains required for hash-bound evidence.
        shutil.copyfile(legacy / ".gitattributes", self.root / ".gitattributes")
        cases = (
            ("approved", (), 0, None),
            ("approved", ("--checkpoint", "start"), 0, "pass"),
            ("in_progress", (), 0, None),
            ("in_progress", ("--checkpoint", "scope", "--changed-path", "src/component/ok.py", "--changes-complete"), 0, "pass"),
            ("in_progress", ("--checkpoint", "scope", "--changed-path", "src/outside.py", "--changes-complete"), 1, "fail"),
            ("in_progress", ("--checkpoint", "scope", "--changed-path", "src/component/ok.py"), 1, "not_assessable"),
        )
        original = work.read_text(encoding="utf-8")
        for status, arguments, expected_code, expected_gate in cases:
            with self.subTest(status=status, arguments=arguments):
                for root in (self.root, legacy):
                    (root / work.relative_to(self.root)).write_text(
                        original.replace('status = "approved"', f'status = "{status}"', 1), encoding="utf-8",
                    )
                    record_execution_approval(root / work.relative_to(self.root))
                results = []
                for root in (legacy, self.root):
                    code, output, error = invoke("check", str(root), "--artifact", "WO-TST-001", *arguments, "--json")
                    self.assertEqual(expected_code, code, output + error)
                    results.append(json.loads(output))
                old, new = results
                self.assertEqual("se-harness-instruction-discovery-v1", old["instruction_discovery"]["schema"])
                self.assertEqual("se-harness-instruction-discovery-v2", new["instruction_discovery"]["schema"])
                self.assertEqual("available", new["instruction_discovery"]["status"])
                for field in ("operation", "state", "procedure", "scope", "restitution"):
                    self.assertEqual(old[field], new[field], field)
                self.assertEqual(old["compliance"]["gates"], new["compliance"]["gates"])
                if expected_gate is not None:
                    self.assertEqual(expected_gate, new["compliance"]["status"])
                else:
                    discovery = new["instruction_discovery"]
                    self.assertEqual("repository", discovery["formal_artifact_source"])
                    self.assertIn({"id": "WO-TST-001", "file": work.relative_to(self.root).as_posix()}, discovery["formal_artifacts"])
                    self.assertNotIn(resources.ENTRY, new["context"]["reading_manifest"])

    def test_public_result_digest_binds_resource_identity_but_not_local_paths(self):
        self.workflow_fixture()
        relocated = Path(self.temp.name) / "relocated"
        shutil.copytree(self.root, relocated)
        relocated_bundle = Path(self.temp.name) / "relocated-resources"
        shutil.copytree(self.bundle, relocated_bundle)
        results = []
        for root, bundle in ((self.root, self.bundle), (relocated, relocated_bundle)):
            with patch.object(resources, "_installed_resource_root", return_value=bundle):
                code, output, error = invoke("check", str(root), "--artifact", "WO-TST-001", "--json")
            self.assertEqual(0, code, output + error)
            result = json.loads(output)
            self.assertEqual(result["result_sha256"], restitution_digest(result))
            self.assertNotIn(str(root), json.dumps(machine_fields(result)))
            self.assertNotIn(str(bundle), json.dumps(machine_fields(result)))
            results.append(result)
        self.assertEqual(results[0]["result_sha256"], results[1]["result_sha256"])
        altered = deepcopy(results[0])
        altered["instruction_discovery"]["release"]["payload_sha256"] = "0" * 64
        self.assertNotEqual(results[0]["result_sha256"], restitution_digest(altered))

    def test_public_checkpoint_reports_unavailable_selection_without_instruction_fallback(self):
        self.workflow_fixture("in_progress")
        self.lock["evaluator"]["payload_sha256"] = "0" * 64
        self.write_lock()
        before = self.files()
        code, output, error = invoke("check", str(self.root), "--artifact", "WO-TST-001", "--checkpoint", "scope",
                                    "--changed-path", "src/component/ok.py", "--changes-complete", "--json")
        self.assertEqual(0, code, output + error)  # Scope supplies no execution authority.
        discovery = json.loads(output)["instruction_discovery"]
        self.assertEqual("incompatible", discovery["status"])
        self.assertIn("payload_sha256", discovery["reason"])
        self.assertNotIn("agent_instructions", discovery)
        self.assertEqual(before, self.files())

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
