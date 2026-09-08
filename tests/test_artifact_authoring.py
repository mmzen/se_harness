from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness.artifact_layout import (
    ARTIFACT_DIRECTORIES,
    ARTIFACT_PREFIXES,
    ARTIFACT_TEMPLATES,
    DOMAIN_PATTERN,
    RESERVED_DOMAINS,
    canonical_artifact_relative_path,
)
from se_harness.cli import main
from se_harness.installer import HarnessError


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
from tests.root_identity_support import evaluator_scripts_dir, root_copy  # noqa: E402
SCRIPTS = evaluator_scripts_dir()
from tests.mutation_guard_support import patch_mutation_authority  # noqa: E402
from tests.root_identity_support import load_evaluator_module
_validate_engineering_artifacts = load_evaluator_module("validate_engineering_artifacts")
validate_repository = _validate_engineering_artifacts.validate_repository
from tests.fixture_support import standard_repository
from tests.cli_support import invoke
from tests.artifact_support import write
from tests.root_identity_support import load_module
from tests.git_support import git, init_repository


class ArtifactAuthoringTests(unittest.TestCase):
    def setUp(self) -> None:
        patch_mutation_authority(self)
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repository"
        standard_repository(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_portable_and_package_layout_registries_are_identical(self) -> None:
        # The package registry is the candidate's portable registry. The root copy
        # under scripts/ is the released evaluator's and is hash-locked until
        # adoption; WO-DCM-001 (SPEC-DCM-001) added the decision type to the
        # candidate, so a root released before it is that registry minus the
        # decision entries, declared here. A root released with them takes equality.
        candidate_path = REPOSITORY_ROOT / "se_harness/engine/artifact_layout_registry.py"
        candidate_layout = load_module(candidate_path, "candidate_layout_registry")
        self.assertEqual(ARTIFACT_DIRECTORIES, candidate_layout.ARTIFACT_DIRECTORIES)
        self.assertEqual(ARTIFACT_PREFIXES, candidate_layout.ARTIFACT_PREFIXES)
        self.assertEqual(DOMAIN_PATTERN.pattern, candidate_layout.DOMAIN_PATTERN.pattern)
        self.assertEqual(RESERVED_DOMAINS, candidate_layout.RESERVED_DOMAINS)
        # The root module is loaded from its path: `import artifact_layout_registry`
        # resolves to whichever scripts directory another test put first on sys.path.
        root_path = root_copy("scripts/artifact_layout_registry.py")
        if root_path is None:
            # WO-HUP-017 (SPEC-HUP-017 HUP-ADP-016): a 0.16.0 or later root installs no
            # copy; the engine registry is the only one, and it is what was imported above.
            self.assertFalse((REPOSITORY_ROOT / "scripts/artifact_layout_registry.py").exists())
            self.assertEqual(set(ARTIFACT_DIRECTORIES), set(ARTIFACT_TEMPLATES))
            return
        root_layout = load_module(root_path, "root_layout_registry")
        if "decision" in root_layout.ARTIFACT_DIRECTORIES:
            self.assertEqual(root_path.read_bytes(), candidate_path.read_bytes())
        else:
            without_decision = {k: v for k, v in ARTIFACT_DIRECTORIES.items() if k != "decision"}
            self.assertEqual(without_decision, root_layout.ARTIFACT_DIRECTORIES)
            self.assertEqual(
                {k: v for k, v in ARTIFACT_PREFIXES.items() if k != "decision"},
                root_layout.ARTIFACT_PREFIXES,
            )
            self.assertEqual(RESERVED_DOMAINS - {"decisions"}, root_layout.RESERVED_DOMAINS)
            self.assertEqual(DOMAIN_PATTERN.pattern, root_layout.DOMAIN_PATTERN.pattern)
        self.assertEqual(set(ARTIFACT_DIRECTORIES), set(ARTIFACT_TEMPLATES))

    def test_scaffold_dry_run_and_apply_create_the_complete_owner_domain(self) -> None:
        code, output, error = invoke(
            "scaffold-domain", str(self.root), "--domain", "simulation", "--title", "Simulation", "--dry-run"
        )
        self.assertEqual(0, code, error)
        self.assertIn("dry run: no files were written", output)
        self.assertFalse((self.root / "docs/engineering/simulation").exists())

        code, output, error = invoke(
            "scaffold-domain", str(self.root), "--domain", "simulation", "--title", "Simulation"
        )
        self.assertEqual(0, code, error)
        domain = self.root / "docs/engineering/simulation"
        for parts in set(ARTIFACT_DIRECTORIES.values()) | {("evidence",), ("acceptance",)}:
            self.assertTrue(domain.joinpath(*parts).is_dir(), parts)
        index = domain / "README.md"
        self.assertIn("Repository-owned index", index.read_text(encoding="utf-8"))
        lock = json.loads((self.root / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertFalse(any(path.startswith("docs/engineering/simulation/") for path in lock["files"]))

        original = b"# Curated simulation navigation\n"
        index.write_bytes(original)
        self.assertEqual(0, invoke("scaffold-domain", str(self.root), "--domain", "simulation")[0])
        self.assertEqual(original, index.read_bytes())

    def test_create_artifact_routes_every_supported_type_to_an_incomplete_draft(self) -> None:
        identifiers = {
            artifact_type: f"{ARTIFACT_PREFIXES[artifact_type]}TST-{index:03d}"
            for index, artifact_type in enumerate(sorted(ARTIFACT_DIRECTORIES), start=1)
        }
        for artifact_type, artifact_id in identifiers.items():
            with self.subTest(artifact_type=artifact_type):
                code, output, error = invoke(
                    "create-artifact",
                    str(self.root),
                    "--domain", "simulation",
                    "--type", artifact_type,
                    "--id", artifact_id,
                )
                self.assertEqual(0, code, error)
                self.assertIn("incomplete draft", output)
                destination = self.root / canonical_artifact_relative_path("simulation", artifact_type, artifact_id)
                content = destination.read_text(encoding="utf-8")
                self.assertIn(f'id = "{artifact_id}"', content)
                self.assertIn(f'type = "{artifact_type}"', content)
                # a decision has no draft state; it is created open (SPEC-DCM-001 rule 4), and a
                # risk is created identified (SPEC-RSK-010 RSK-MGT-007)
                self.assertIn({"decision": 'status = "open"', "risk": 'status = "identified"'}.get(artifact_type, 'status = "draft"'), content)
        self.assertFalse((self.root / "docs/engineering/simulation/README.md").exists())

    def test_create_dry_run_conflict_and_invalid_input_never_overwrite(self) -> None:
        destination = self.root / "docs/engineering/simulation/requirements/REQ-SIM-001.md"
        code, output, error = invoke(
            "create-artifact", str(self.root), "--domain", "simulation", "--type", "requirement",
            "--id", "REQ-SIM-001", "--dry-run",
        )
        self.assertEqual(0, code, error)
        self.assertIn("dry run", output)
        self.assertFalse(destination.exists())

        destination.parent.mkdir(parents=True)
        original = b"repository owned\n"
        destination.write_bytes(original)
        code, _, error = invoke(
            "create-artifact", str(self.root), "--domain", "simulation", "--type", "requirement",
            "--id", "REQ-SIM-001",
        )
        self.assertEqual(2, code)
        self.assertIn("already exists", error)
        self.assertEqual(original, destination.read_bytes())

        duplicate = self.root / "docs/engineering/other-domain/REQ-SIM-003.md"
        duplicate.parent.mkdir(parents=True)
        duplicate.write_text('+++\nid = "REQ-SIM-003"\ntype = "requirement"\n+++\n', encoding="utf-8")
        code, _, error = invoke(
            "create-artifact", str(self.root), "--domain", "simulation", "--type", "requirement",
            "--id", "REQ-SIM-003",
        )
        self.assertEqual(2, code)
        self.assertIn("ID already exists", error)

        for domain in ("../escape", "Simulation", "requirements", "two/slugs", "a" * 65):
            with self.subTest(domain=domain):
                code, _, error = invoke(
                    "create-artifact", str(self.root), "--domain", domain, "--type", "requirement",
                    "--id", "REQ-SIM-002",
                )
                self.assertEqual(2, code)
                self.assertTrue(error)
        code, _, error = invoke(
            "create-artifact", str(self.root), "--domain", "simulation", "--type", "requirement",
            "--id", "WO-SIM-002",
        )
        self.assertEqual(2, code)
        self.assertIn("REQ-", error)

    def test_scaffold_failure_rolls_back_only_directories_created_by_the_command(self) -> None:
        with mock.patch("se_harness.artifact_layout._atomic_create", side_effect=HarnessError("injected failure")):
            code, _, error = invoke("scaffold-domain", str(self.root), "--domain", "rollback-test")
        self.assertEqual(2, code)
        self.assertIn("injected failure", error)
        self.assertFalse((self.root / "docs/engineering/rollback-test").exists())

    def test_link_escape_is_rejected_without_writing_outside_the_repository(self) -> None:
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        link = self.root / "docs/engineering/linked-domain"
        try:
            os.symlink(outside, link, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"host cannot create directory symlink: {exc}")
        code, _, error = invoke(
            "create-artifact", str(self.root), "--domain", "linked-domain", "--type", "requirement",
            "--id", "REQ-LNK-001",
        )
        self.assertEqual(2, code)
        self.assertIn("linked", error.lower())
        self.assertEqual([], list(outside.iterdir()))

    def test_flat_layout_is_valid_advisory_and_visible_in_doctor(self) -> None:
        artifact = self.root / "docs/engineering/simulation/INT-SIM-001.md"
        artifact.parent.mkdir(parents=True)
        artifact.write_text(
            '''+++
id = "INT-SIM-001"
type = "intent"
title = "Simulation"
status = "approved"
owners = ["product-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
+++

# Intent
''',
            encoding="utf-8",
        )
        report = validate_repository(self.root)
        self.assertTrue(report.valid)
        self.assertEqual(["W013"], [item.code for item in report.warnings])
        self.assertIn("simulation/intent/INT-SIM-001.md", report.warnings[0].message)

        code, output, error = invoke("doctor", str(self.root))
        self.assertEqual(0, code, error)
        self.assertIn("WARN W013", output)

    def test_upgrade_preserves_flat_and_canonical_owner_content(self) -> None:
        flat = self.root / "docs/engineering/simulation/REQ-SIM-001.md"
        canonical = self.root / "docs/engineering/simulation/requirements/REQ-SIM-002.md"
        index = self.root / "docs/engineering/simulation/README.md"
        for path, content in (
            (flat, b"flat owner artifact\n"),
            (canonical, b"canonical owner artifact\n"),
            (index, b"owner index\n"),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        before = {path: path.read_bytes() for path in (flat, canonical, index)}
        self.assertEqual(0, invoke("upgrade", str(self.root), "--apply")[0])
        self.assertEqual(before, {path: path.read_bytes() for path in before})


if __name__ == "__main__":
    unittest.main()


class IdentifierAllocationTests(unittest.TestCase):
    """REQ-ECP-004 / ECP-IDA-001 to -006: the lowest free identifier across every local ref."""

    def setUp(self) -> None:
        import subprocess

        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root)
        (self.root / "docs/engineering/product/requirements").mkdir(parents=True, exist_ok=True)
        write(self.root / "docs/engineering/product/requirements/REQ-PRD-001.md", "+++\n" + 'id = "REQ-PRD-001"' + "\n+++\n")
        write(self.root / "docs/engineering/product/requirements/REQ-PRD-002.md", "+++\n" + 'id = "REQ-PRD-002"' + "\n+++\n")

        self.git = lambda *arguments: git(self.root, *arguments)
        init_repository(self.root)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")

    def allocate(self, artifact_type: str = "requirement"):
        from se_harness.artifact_layout import allocate_artifact_id

        return allocate_artifact_id(self.root, domain="product", artifact_type=artifact_type)

    def test_allocation_sees_unmerged_branches_gaps_detached_refs_and_the_working_tree(self) -> None:
        self.assertEqual(("REQ-PRD-003", ("refs/heads/main", "worktree")), self.allocate())
        # a higher identifier present only on an unmerged local branch
        self.git("checkout", "-q", "-b", "feature")
        write(self.root / "docs/engineering/product/requirements/REQ-PRD-004.md", "+++\n" + 'id = "REQ-PRD-004"' + "\n+++\n")
        self.git("add", "-A"); self.git("commit", "-q", "-m", "feature")
        self.git("checkout", "-q", "main")
        self.assertEqual("REQ-PRD-003", self.allocate()[0])
        # the gap below the branch maximum is filled first, then the working tree counts
        write(self.root / "docs/engineering/product/requirements/REQ-PRD-003.md", "+++\n" + 'id = "REQ-PRD-003"' + "\n+++\n")
        identifier, refs = self.allocate()
        self.assertEqual("REQ-PRD-005", identifier)
        self.assertIn("refs/heads/feature", refs)  # REQ-PRD-004 was found there
        # a tag (detached ref) carrying a further identifier
        self.git("checkout", "-q", "feature")
        write(self.root / "docs/engineering/product/requirements/REQ-PRD-005.md", "+++\n" + 'id = "REQ-PRD-005"' + "\n+++\n")
        self.git("add", "-A"); self.git("commit", "-q", "-m", "more"); self.git("tag", "v-detached")
        self.git("checkout", "-q", "main")
        self.assertFalse((self.root / "docs/engineering/product/requirements/REQ-PRD-005.md").exists())
        self.assertEqual("REQ-PRD-006", self.allocate()[0])
        # remote-tracking refs are not consulted: with the branch and tag gone, only
        # main and the working tree (which no longer holds REQ-PRD-003, committed on
        # the deleted branch) remain, so the lowest free number is 003 again
        self.git("update-ref", "refs/remotes/origin/other", self.git("rev-parse", "feature").strip())
        self.git("branch", "-D", "feature"); self.git("tag", "-d", "v-detached")
        self.assertFalse((self.root / "docs/engineering/product/requirements/REQ-PRD-003.md").exists())
        self.assertEqual("REQ-PRD-003", self.allocate()[0])

    def test_allocation_sees_operating_contract_and_decision_ids_on_another_ref(self) -> None:
        # WO-ECP-027 (ECP-COR-016): the ref pattern covers every type _REF_PREFIX declares.
        from se_harness.artifact_layout import ARTIFACT_DIRECTORIES, reachable_artifact_ids

        operations = "/".join(ARTIFACT_DIRECTORIES["operating_contract"])
        decisions = "/".join(ARTIFACT_DIRECTORIES["decision"])
        self.git("checkout", "-q", "-b", "records")
        write(self.root / f"docs/engineering/product/{operations}/OPS-PRD-001.md", "+++\n" + 'id = "OPS-PRD-001"' + "\n+++\n")
        write(self.root / f"docs/engineering/product/{decisions}/DEC-PRD-001.md", "+++\n" + 'id = "DEC-PRD-001"' + "\n+++\n")
        self.git("add", "-A"); self.git("commit", "-q", "-m", "records")
        self.git("checkout", "-q", "main")
        seen = reachable_artifact_ids(self.root)
        self.assertIn("OPS-PRD-001", seen)
        self.assertIn("DEC-PRD-001", seen)
        self.assertEqual("OPS-PRD-002", self.allocate("operating_contract")[0])
        self.assertEqual("DEC-PRD-002", self.allocate("decision")[0])

    def test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref(self) -> None:
        import shutil

        from se_harness.artifact_layout import create_artifact
        from se_harness.installer import HarnessError

        self.git("checkout", "-q", "-b", "feature")
        write(self.root / "docs/engineering/product/requirements/REQ-PRD-007.md", "+++\n" + 'id = "REQ-PRD-007"' + "\n+++\n")
        self.git("add", "-A"); self.git("commit", "-q", "-m", "feature"); self.git("checkout", "-q", "main")
        with self.assertRaisesRegex(HarnessError, "already exists: REQ-PRD-007 on local ref refs/heads/feature"):
            create_artifact(self.root, domain="product", artifact_type="requirement", artifact_id="REQ-PRD-007", dry_run=True)
        change = create_artifact(self.root, domain="product", artifact_type="requirement", artifact_id=None, dry_run=True)
        self.assertEqual("REQ-PRD-003", change.allocated_id)
        shutil.rmtree(self.root / ".git")
        with self.assertRaisesRegex(HarnessError, "WEX-ECP-013"):
            self.allocate()



class EvaluatorDerivedPathTests(unittest.TestCase):
    """SPEC-ECP-008 ECP-HST-002 (issue #254): the resolver takes the evaluator's own path on every host."""

    def test_a_pure_windows_path_resolves_to_its_domain(self) -> None:
        from pathlib import PurePosixPath, PureWindowsPath

        from se_harness.artifact_layout import artifact_domain_from_relative_path

        relative = "docs/engineering/execution-control-plane/work-orders/WO-ECP-012.md"
        self.assertEqual("execution-control-plane", artifact_domain_from_relative_path(PureWindowsPath(relative)))
        self.assertEqual("execution-control-plane", artifact_domain_from_relative_path(PurePosixPath(relative)))
        self.assertEqual("execution-control-plane", artifact_domain_from_relative_path(relative))

    def test_a_backslash_in_untrusted_text_is_still_refused(self) -> None:
        from pathlib import PureWindowsPath

        from se_harness.artifact_layout import artifact_domain_from_relative_path

        text = r"docs\engineering\execution-control-plane\work-orders\WO-ECP-012.md"
        self.assertIsNone(artifact_domain_from_relative_path(text))
        self.assertIsNone(artifact_domain_from_relative_path(PureWindowsPath("C:/repo/docs/engineering/d/work-orders/WO-D-001.md")))
        self.assertIsNone(artifact_domain_from_relative_path(PureWindowsPath("docs/engineering/WO-D-001.md")))
