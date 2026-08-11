from __future__ import annotations

import re
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

    def test_manual_inputs_and_serial_production_environment_are_explicit(self) -> None:
        workflow = self.workflow
        self.assertIn("  workflow_dispatch:\n", workflow)
        self.assertNotIn("  release:\n", workflow)
        self.assertNotIn("  push:\n", workflow)
        for input_name in ("tag", "wheel_sha256", "sdist_sha256"):
            self.assertRegex(
                workflow,
                rf"(?m)^      {input_name}:\n(?:        .+\n)+?        required: true$",
            )
        self.assertIn("  group: pypi-production\n", workflow)
        self.assertIn("  cancel-in-progress: false\n", workflow)
        self.assertIn("    if: github.ref == 'refs/heads/main'\n", workflow)
        self.assertIn("    environment:\n      name: pypi\n", workflow)
        self.assertIn("      url: https://pypi.org/p/se-harness\n", workflow)

    def test_release_and_hash_inputs_are_validated_as_untrusted_data(self) -> None:
        workflow = self.workflow
        self.assertIn("RELEASE_TAG: ${{ inputs.tag }}", workflow)
        self.assertIn("WHEEL_SHA256: ${{ inputs.wheel_sha256 }}", workflow)
        self.assertIn("SDIST_SHA256: ${{ inputs.sdist_sha256 }}", workflow)
        self.assertIn('[[ ! "$RELEASE_TAG" =~ ^v[0-9]+\\.[0-9]+\\.[0-9]+$ ]]', workflow)
        self.assertEqual(2, workflow.count('=~ ^[0-9a-f]{64}$'))
        self.assertIn("--json tagName,isDraft,isPrerelease", workflow)
        self.assertIn("'.isDraft'", workflow)
        self.assertIn("'.isPrerelease'", workflow)
        self.assertNotIn("${{ inputs.tag }}\"", self._run_script(workflow))

    def test_exact_distribution_names_and_independent_hashes_are_required(self) -> None:
        workflow = self.workflow
        self.assertIn('wheel_name="se_harness-${version}-py3-none-any.whl"', workflow)
        self.assertIn('sdist_name="se_harness-${version}.tar.gz"', workflow)
        self.assertIn('for asset in "$wheel_name" "$sdist_name" SHA256SUMS', workflow)
        self.assertEqual(2, workflow.count("sha256sum \"release-assets/$"))
        self.assertIn('[[ "$actual_wheel_sha256" != "$WHEEL_SHA256" ]]', workflow)
        self.assertIn('[[ "$actual_sdist_sha256" != "$SDIST_SHA256" ]]', workflow)
        self.assertIn("printf '%s  %s\\n%s  %s\\n'", workflow)
        self.assertIn('cmp --silent "$expected_manifest" release-assets/SHA256SUMS', workflow)
        self.assertIn('cp -- "release-assets/$wheel_name" "release-assets/$sdist_name" dist/', workflow)

    def test_oidc_job_is_least_privilege_and_does_not_execute_repository_code(self) -> None:
        workflow = self.workflow
        self.assertEqual(1, workflow.count("id-token: write"))
        self.assertEqual(1, workflow.count("contents: read"))
        self.assertIn("    permissions:\n      contents: read\n      id-token: write\n", workflow)
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
                self.assertNotIn(text, workflow)

    def test_publisher_is_immutable_and_preserves_strict_pypi_behavior(self) -> None:
        workflow = self.workflow
        self.assertIn(
            f"uses: pypa/gh-action-pypi-publish@{PUBLISH_ACTION_SHA} # v1.14.2 peeled commit",
            workflow,
        )
        self.assertNotIn(PUBLISH_ACTION_TAG_OBJECT_SHA, workflow)
        self.assertRegex(PUBLISH_ACTION_SHA, r"\A[0-9a-f]{40}\Z")
        self.assertNotRegex(workflow, r"pypa/gh-action-pypi-publish@(release/|v?\d)")
        self.assertIn("          packages-dir: dist/\n", workflow)
        self.assertIn("          verify-metadata: true\n", workflow)
        self.assertIn("          attestations: true\n", workflow)
        self.assertIn("          print-hash: true\n", workflow)
        self.assertNotIn("skip-existing", workflow)

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

    @staticmethod
    def _run_script(workflow: str) -> str:
        match = re.search(
            r"(?ms)^        run: \|\n(?P<script>.+?)^      - name: Publish exact distributions",
            workflow,
        )
        if match is None:
            raise AssertionError("workflow preflight run block is missing")
        return match.group("script")


if __name__ == "__main__":
    unittest.main()
