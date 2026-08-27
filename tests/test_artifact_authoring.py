from __future__ import annotations

import contextlib
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
# The candidate registry and validator live in the standard template; the root copies
# are the released evaluator's and may lag them (WO-RSK-001).
SCRIPTS = REPOSITORY_ROOT / "templates/repository/standard/scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import artifact_layout_registry as portable_layout  # noqa: E402
from tests.mutation_guard_support import trusted_mutation_authority  # noqa: E402
from validate_engineering_artifacts import validate_repository  # noqa: E402
from tests.fixture_support import standard_repository


class ArtifactAuthoringTests(unittest.TestCase):
    def setUp(self) -> None:
        self.guard = mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=trusted_mutation_authority,
        )
        self.guard.start()
        self.addCleanup(self.guard.stop)
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repository"
        standard_repository(self.root, "Authoring Sample")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(list(arguments))
        return code, stdout.getvalue(), stderr.getvalue()

    def test_portable_and_package_layout_registries_are_identical(self) -> None:
        self.assertEqual(ARTIFACT_DIRECTORIES, portable_layout.ARTIFACT_DIRECTORIES)
        self.assertEqual(ARTIFACT_PREFIXES, portable_layout.ARTIFACT_PREFIXES)
        self.assertEqual(DOMAIN_PATTERN.pattern, portable_layout.DOMAIN_PATTERN.pattern)
        self.assertEqual(RESERVED_DOMAINS, portable_layout.RESERVED_DOMAINS)
        released_registry = (REPOSITORY_ROOT / "scripts/artifact_layout_registry.py").read_bytes().replace(b"\r\n", b"\n")
        candidate_registry = (
            REPOSITORY_ROOT / "templates/repository/standard/scripts/artifact_layout_registry.py"
        ).read_bytes()
        # The released root registry predates the risk artifact; the candidate adds exactly
        # the risk directory, prefix, and reserved slug (WO-RSK-001).
        expected_candidate = (
            released_registry.replace(b'    "operating_contract": ("operations",),\n}', b'    "operating_contract": ("operations",),\n    "risk": ("risks",),\n}', 1)
            .replace(b'    "operating_contract": "OPS-",\n}', b'    "operating_contract": "OPS-",\n    "risk": "RISK-",\n}', 1)
            .replace(b'"operations", "release", "releases", "requirements", "specifications",', b'"operations", "release", "releases", "requirements", "risks", "specifications",', 1)
        )
        self.assertNotEqual(released_registry, candidate_registry)
        self.assertEqual(
            expected_candidate.replace(b"\r\n", b"\n"), candidate_registry.replace(b"\r\n", b"\n")
        )
        self.assertEqual(set(ARTIFACT_DIRECTORIES), set(ARTIFACT_TEMPLATES))

    def test_scaffold_dry_run_and_apply_create_the_complete_owner_domain(self) -> None:
        code, output, error = self.invoke(
            "scaffold-domain", str(self.root), "--domain", "simulation", "--title", "Simulation", "--dry-run"
        )
        self.assertEqual(0, code, error)
        self.assertIn("dry run: no files were written", output)
        self.assertFalse((self.root / "docs/engineering/simulation").exists())

        code, output, error = self.invoke(
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
        self.assertEqual(0, self.invoke("scaffold-domain", str(self.root), "--domain", "simulation")[0])
        self.assertEqual(original, index.read_bytes())

    def test_create_artifact_routes_every_supported_type_to_an_incomplete_draft(self) -> None:
        identifiers = {
            artifact_type: f"{ARTIFACT_PREFIXES[artifact_type]}TST-{index:03d}"
            for index, artifact_type in enumerate(sorted(ARTIFACT_DIRECTORIES), start=1)
        }
        for artifact_type, artifact_id in identifiers.items():
            with self.subTest(artifact_type=artifact_type):
                code, output, error = self.invoke(
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
                self.assertIn('status = "draft"', content)
        self.assertFalse((self.root / "docs/engineering/simulation/README.md").exists())

    def test_create_dry_run_conflict_and_invalid_input_never_overwrite(self) -> None:
        destination = self.root / "docs/engineering/simulation/requirements/REQ-SIM-001.md"
        code, output, error = self.invoke(
            "create-artifact", str(self.root), "--domain", "simulation", "--type", "requirement",
            "--id", "REQ-SIM-001", "--dry-run",
        )
        self.assertEqual(0, code, error)
        self.assertIn("dry run", output)
        self.assertFalse(destination.exists())

        destination.parent.mkdir(parents=True)
        original = b"repository owned\n"
        destination.write_bytes(original)
        code, _, error = self.invoke(
            "create-artifact", str(self.root), "--domain", "simulation", "--type", "requirement",
            "--id", "REQ-SIM-001",
        )
        self.assertEqual(2, code)
        self.assertIn("already exists", error)
        self.assertEqual(original, destination.read_bytes())

        duplicate = self.root / "docs/engineering/other-domain/REQ-SIM-003.md"
        duplicate.parent.mkdir(parents=True)
        duplicate.write_text('+++\nid = "REQ-SIM-003"\ntype = "requirement"\n+++\n', encoding="utf-8")
        code, _, error = self.invoke(
            "create-artifact", str(self.root), "--domain", "simulation", "--type", "requirement",
            "--id", "REQ-SIM-003",
        )
        self.assertEqual(2, code)
        self.assertIn("ID already exists", error)

        for domain in ("../escape", "Simulation", "requirements", "two/slugs", "a" * 65):
            with self.subTest(domain=domain):
                code, _, error = self.invoke(
                    "create-artifact", str(self.root), "--domain", domain, "--type", "requirement",
                    "--id", "REQ-SIM-002",
                )
                self.assertEqual(2, code)
                self.assertTrue(error)
        code, _, error = self.invoke(
            "create-artifact", str(self.root), "--domain", "simulation", "--type", "requirement",
            "--id", "WO-SIM-002",
        )
        self.assertEqual(2, code)
        self.assertIn("REQ-", error)

    def test_scaffold_failure_rolls_back_only_directories_created_by_the_command(self) -> None:
        with mock.patch("se_harness.artifact_layout._atomic_create", side_effect=HarnessError("injected failure")):
            code, _, error = self.invoke("scaffold-domain", str(self.root), "--domain", "rollback-test")
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
        code, _, error = self.invoke(
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

        code, output, error = self.invoke("doctor", str(self.root))
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
        self.assertEqual(0, self.invoke("upgrade", str(self.root), "--apply")[0])
        self.assertEqual(before, {path: path.read_bytes() for path in before})


if __name__ == "__main__":
    unittest.main()
