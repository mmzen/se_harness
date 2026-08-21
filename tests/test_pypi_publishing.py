from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "publish-pypi.yml"
PUBLISH_ACTION_SHA = "dc37677b2e1c63e2034f94d8a5b11f265b73ba33"
PUBLISH_ACTION_TAG_OBJECT_SHA = "a892a5a61159132606e93a2fa6f4358831b04d26"


class PyPIPublishingWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.pypi_job = cls.workflow.split("  pypi:\n", 1)[1].split("  pages_build:\n", 1)[0]

    def test_one_released_record_input_and_serial_production_environment_are_explicit(self) -> None:
        workflow = self.workflow
        self.assertIn("  workflow_dispatch:\n", workflow)
        self.assertNotIn("  release:\n", workflow)
        self.assertNotIn("  push:\n", workflow)
        self.assertEqual(1, workflow.count("        required: true\n"))
        self.assertIn("      release_record:\n", workflow)
        for obsolete in ("      tag:\n", "      wheel_sha256:\n", "      sdist_sha256:\n"):
            self.assertNotIn(obsolete, workflow)
        self.assertIn("      group: pypi-production\n", self.pypi_job)
        self.assertIn("      cancel-in-progress: false\n", self.pypi_job)
        self.assertIn("    environment:\n      name: pypi\n", self.pypi_job)
        self.assertIn("      url: https://pypi.org/p/se-harness\n", self.pypi_job)

    def test_exact_distributions_are_derived_and_independently_verified(self) -> None:
        self.assertIn("WHEEL: ${{ needs.resolve.outputs.wheel }}", self.pypi_job)
        self.assertIn("SDIST: ${{ needs.resolve.outputs.sdist }}", self.pypi_job)
        self.assertIn("CHECKSUMS_SHA256: ${{ needs.resolve.outputs.checksums_sha256 }}", self.pypi_job)
        self.assertIn("gh release download", self.pypi_job)
        self.assertIn("sha256sum --check", self.pypi_job)
        self.assertIn("cmp --silent - release-assets/SHA256SUMS", self.pypi_job)
        self.assertIn('test "$actual" = "$expected"', self.pypi_job)

    def test_governance_validation_uses_only_the_standard_released_evaluator(self) -> None:
        self.assertEqual(2, self.workflow.count("publish_dashboard.py evaluator"))
        self.assertEqual(2, self.workflow.count("--role released-evaluator"))
        self.assertEqual(
            2, self.workflow.count("identity_args+=(--evaluator-payload-sha256")
        )
        self.assertEqual(
            2,
            self.workflow.count(
                "identity --help 2>&1 | grep -q -- '--evaluator-payload-sha256'"
            ),
        )
        self.assertEqual(2, self.workflow.count("--evaluator-wheel-sha256"))
        for retired in (
            "publish_dashboard.py governor",
            "--role governor",
            "--governor-wheel-sha256",
            "GOVERNOR_",
            "governor-env",
            "steps.governor",
        ):
            self.assertNotIn(retired, self.workflow)

    def test_oidc_job_is_least_privilege_and_does_not_execute_repository_code(self) -> None:
        self.assertEqual(1, self.pypi_job.count("id-token: write"))
        self.assertEqual(1, self.pypi_job.count("contents: read"))
        forbidden = (
            "actions/checkout",
            "python -m build",
            "python -m pip",
            "pip install",
            "secrets.",
            "PYPI_TOKEN",
            "password:",
            ".pypirc",
        )
        for text in forbidden:
            with self.subTest(text=text):
                self.assertNotIn(text, self.pypi_job)

    def test_publisher_is_immutable_and_strict_replay_does_not_use_skip_existing(self) -> None:
        self.assertIn(
            f"uses: pypa/gh-action-pypi-publish@{PUBLISH_ACTION_SHA} # v1.14.2 peeled commit",
            self.pypi_job,
        )
        self.assertNotIn(PUBLISH_ACTION_TAG_OBJECT_SHA, self.pypi_job)
        self.assertIn("          packages-dir: dist/\n", self.pypi_job)
        self.assertIn("          verify-metadata: true\n", self.pypi_job)
        self.assertIn("          attestations: true\n", self.pypi_job)
        self.assertIn("          print-hash: true\n", self.pypi_job)
        self.assertNotIn("skip-existing", self.workflow)

    def test_known_v020_manifest_vector_is_exact(self) -> None:
        version = "0.2.0"
        wheel_hash = "56db717e5287492c421e11157545586b1e8f0ec2dd4011a9932ccf35f233d63d"
        sdist_hash = "7c94cc0f4998b045b2766c60bc03a887bfdc53ae87f3494bb702e1d947bf873d"
        manifest = (
            f"{wheel_hash}  se_harness-{version}-py3-none-any.whl\n"
            f"{sdist_hash}  se_harness-{version}.tar.gz\n"
        )
        retained = (
            REPOSITORY_ROOT
            / "docs"
            / "engineering"
            / "release-0.2.0"
            / "evidence"
            / "RLS-SEH-001-release.md"
        ).read_text(encoding="utf-8")
        self.assertIn(wheel_hash, retained)
        self.assertIn(sdist_hash, retained)
        self.assertEqual(190, len(manifest.encode("utf-8")))


if __name__ == "__main__":
    unittest.main()
