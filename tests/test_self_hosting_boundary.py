from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest import mock

from se_harness import __version__
from se_harness.preflight import inspect_installation
from se_harness.runtime_identity import _within, inspect_runtime_identity
from se_harness.self_hosting import (
    DESCRIPTOR_PATH,
    load_governor_descriptor,
    self_hosting_enabled,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GOVERNOR_SHA256 = "533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454"
FAILED_PR_RECORDS = (
    "docs/engineering/release-0.2.2/verification-records/VREC-SEH-003.md",
    "docs/engineering/release-0.2.2/releases/RLS-SEH-003.md",
)


class SelfHostingBoundaryTests(unittest.TestCase):
    def test_governor_descriptor_is_exact_and_matches_self_hosting_workflow(self) -> None:
        descriptor = load_governor_descriptor(REPOSITORY_ROOT)
        self.assertEqual("0.2.1", descriptor.version)
        self.assertEqual("v0.2.1", descriptor.tag)
        self.assertEqual(GOVERNOR_SHA256, descriptor.sha256)
        self.assertEqual("RLS-SEH-002", descriptor.selected_release_record)

        workflow = (REPOSITORY_ROOT / ".github/workflows/engineering-harness.yml").read_text(
            encoding="utf-8"
        )
        for value in (
            descriptor.version,
            descriptor.tag,
            descriptor.wheel,
            descriptor.url,
            descriptor.sha256,
        ):
            self.assertIn(value, workflow)

    def test_invalid_governor_descriptor_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / DESCRIPTOR_PATH
            path.parent.mkdir(parents=True)
            source = (REPOSITORY_ROOT / DESCRIPTOR_PATH).read_text(encoding="utf-8")
            path.write_text(source.replace(GOVERNOR_SHA256, "0" * 63), encoding="utf-8")
            with self.assertRaisesRegex(Exception, "SHA-256"):
                load_governor_descriptor(root)

    def test_candidate_source_identity_is_deterministic_and_bounded(self) -> None:
        commit = "a" * 40
        with mock.patch.dict(
            os.environ,
            {"EXAMPLE_SECRET_TOKEN": "must-not-appear"},
            clear=True,
        ), mock.patch("se_harness.runtime_identity.site.ENABLE_USER_SITE", False):
            first = inspect_runtime_identity(
                role="candidate-source",
                expected_version=__version__,
                expected_root=REPOSITORY_ROOT,
                checkout_root=REPOSITORY_ROOT,
                candidate_commit=commit,
            )
            second = inspect_runtime_identity(
                role="candidate-source",
                expected_version=__version__,
                expected_root=REPOSITORY_ROOT,
                checkout_root=REPOSITORY_ROOT,
                candidate_commit=commit,
            )
        self.assertTrue(first.passed, first.diagnostics)
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertNotIn("must-not-appear", json.dumps(first.to_dict(), sort_keys=True))

    def test_equal_version_cannot_substitute_checkout_source_for_installed_role(self) -> None:
        identity = inspect_runtime_identity(
            role="candidate-package",
            expected_version=__version__,
            expected_root=Path(sys.prefix),
            checkout_root=REPOSITORY_ROOT,
            candidate_commit="b" * 40,
        )
        self.assertFalse(identity.passed)
        codes = {item.code for item in identity.diagnostics}
        self.assertTrue({"RID003", "RID006"}.intersection(codes), codes)

    def test_candidate_source_rejects_external_distribution_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, mock.patch(
            "se_harness.runtime_identity._distribution_root",
            return_value=Path(temporary),
        ):
            identity = inspect_runtime_identity(
                role="candidate-source",
                expected_version=__version__,
                expected_root=REPOSITORY_ROOT,
                checkout_root=REPOSITORY_ROOT,
                candidate_commit="d" * 40,
            )
        self.assertIn("RID018", {item.code for item in identity.diagnostics})

    def test_installed_role_rejects_entry_point_from_another_environment(self) -> None:
        identity = inspect_runtime_identity(
            role="candidate-package",
            expected_version=__version__,
            expected_root=Path(sys.prefix),
            checkout_root=REPOSITORY_ROOT,
            candidate_commit="e" * 40,
            entry_point=REPOSITORY_ROOT / "foreign-harnessctl",
            require_entry_point=True,
        )
        self.assertIn("RID010", {item.code for item in identity.diagnostics})

    def test_installed_role_rejects_inherited_pythonpath(self) -> None:
        with mock.patch.dict(os.environ, {"PYTHONPATH": str(REPOSITORY_ROOT)}):
            identity = inspect_runtime_identity(
                role="governor",
                expected_version=__version__,
                expected_root=Path(sys.prefix),
                checkout_root=REPOSITORY_ROOT,
                governor_wheel_sha256="c" * 64,
            )
        self.assertIn("RID008", {item.code for item in identity.diagnostics})

    def test_path_containment_is_component_aware_and_resolves_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            boundary = root / "candidate"
            inside = boundary / "package" / "module.py"
            sibling = root / "candidate-shadow" / "module.py"
            inside.parent.mkdir(parents=True)
            sibling.parent.mkdir(parents=True)
            inside.write_text("", encoding="utf-8")
            sibling.write_text("", encoding="utf-8")
            self.assertTrue(_within(inside, boundary))
            self.assertFalse(_within(sibling, boundary))

    def test_self_hosting_exception_is_narrow_and_descriptor_backed(self) -> None:
        self.assertTrue(self_hosting_enabled(REPOSITORY_ROOT))
        checks = inspect_installation(REPOSITORY_ROOT)
        governor = [item for item in checks if item.name == "self-hosting-governor"]
        self.assertEqual(1, len(governor))
        self.assertTrue(governor[0].passed)
        self.assertTrue(all(item.passed for item in checks), [item for item in checks if not item.passed])
        exceptions = [
            item
            for item in checks
            if item.name.startswith("distribution:")
            and item.detail == "repository-specific self-hosting control"
        ]
        self.assertEqual(
            {
                "distribution:.engineering-harness.toml",
                "distribution:.github/workflows/engineering-harness.yml",
            },
            {item.name for item in exceptions},
        )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".engineering-harness.toml").write_text(
                '[self_hosting]\nrole = "implementation-repository"\n',
                encoding="utf-8",
            )
            self.assertFalse(self_hosting_enabled(root))

    def test_workflow_has_non_substitutable_three_plane_gates(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github/workflows/engineering-harness.yml").read_text(
            encoding="utf-8"
        )
        self.assertRegex(workflow, r"(?m)^  governor:$")
        self.assertRegex(workflow, r"(?m)^  candidate-source:$")
        self.assertRegex(workflow, r"(?m)^  candidate-package:$")
        self.assertRegex(workflow, r"(?s)candidate-source:.*?needs: governor")
        self.assertRegex(workflow, r"(?s)candidate-package:.*?needs: candidate-source")
        self.assertIn('doctor "$RUNNER_TEMP/governor-target"', workflow)
        self.assertNotIn("harnessctl doctor .", workflow)
        self.assertIn("git archive \"$GITHUB_SHA\"", workflow)
        self.assertIn("non-promotable candidate wheel", workflow)
        self.assertIn("--require-isolated-python", workflow)
        self.assertIn("--entry-point", workflow)
        governor_lane = workflow.split("  governor:", 1)[1].split("  candidate-source:", 1)[0]
        self.assertNotIn("validate_engineering_artifacts.py", governor_lane)
        self.assertIn("compatibility_scope", governor_lane)
        self.assertIn("git diff --exit-code", workflow)
        self.assertNotIn("pull_request_target", workflow)
        self.assertNotIn("permissions:\n  contents: write", workflow)

    def test_failed_pr_records_are_excluded_from_recovery_candidate(self) -> None:
        for relative in FAILED_PR_RECORDS:
            with self.subTest(relative=relative):
                self.assertFalse((REPOSITORY_ROOT / relative).exists())


if __name__ == "__main__":
    unittest.main()
