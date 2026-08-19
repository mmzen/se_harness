from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / ".github" / "scripts" / "reconcile_maintenance_branch.py"
SPEC = importlib.util.spec_from_file_location("maintenance_branch_test_module", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load maintenance-line reconciliation module")
MAINTENANCE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MAINTENANCE
SPEC.loader.exec_module(MAINTENANCE)

CANDIDATE = "a" * 40
DESCENDANT = "b" * 40
BRANCH = "release/0.5"
REF = f"refs/heads/{BRANCH}"
REF_PATH = "/repos/mmzen/se_harness/git/ref/heads%2Frelease%2F0.5"
CREATE_PATH = "/repos/mmzen/se_harness/git/refs"


def ref_payload(sha: str = CANDIDATE, *, object_type: str = "commit") -> dict[str, Any]:
    return {"ref": REF, "object": {"type": object_type, "sha": sha}}


class ScriptedRequest:
    def __init__(self, entries: list[tuple[str, str, int, Any]]) -> None:
        self.entries = list(entries)
        self.calls: list[tuple[str, str, dict[str, Any] | None]] = []

    def __call__(self, method: str, path: str, payload: dict[str, Any] | None) -> object:
        self.calls.append((method, path, payload))
        if not self.entries:
            raise AssertionError(f"unexpected API call: {method} {path}")
        expected_method, expected_path, status, response_payload = self.entries.pop(0)
        if (method, path) != (expected_method, expected_path):
            raise AssertionError(
                f"expected {expected_method} {expected_path}, received {method} {path}"
            )
        return MAINTENANCE.ApiResponse(status, response_payload)


class MaintenanceBranchTests(unittest.TestCase):
    def test_branch_derivation_is_canonical_and_repository_scoped(self) -> None:
        self.assertEqual(BRANCH, MAINTENANCE.derive_branch("0.5.0"))
        for invalid in ("v0.5.0", "0.5", "00.5.0", "0.5.0rc1", "0.5.0/other"):
            with self.subTest(version=invalid):
                with self.assertRaises(MAINTENANCE.MaintenanceBranchError):
                    MAINTENANCE.derive_branch(invalid)
        request = ScriptedRequest([])
        with self.assertRaisesRegex(MAINTENANCE.MaintenanceBranchError, "restricted"):
            MAINTENANCE.reconcile("example/consumer", "0.5.0", CANDIDATE, request)
        self.assertEqual([], request.calls)

    def test_absent_branch_is_created_at_exact_candidate_and_rechecked(self) -> None:
        request = ScriptedRequest(
            [
                ("GET", REF_PATH, 404, {"message": "Not Found"}),
                ("POST", CREATE_PATH, 201, ref_payload()),
                ("GET", REF_PATH, 200, ref_payload()),
            ]
        )
        result = MAINTENANCE.reconcile("mmzen/se_harness", "0.5.0", CANDIDATE, request)
        self.assertEqual("created", result.state)
        self.assertEqual(BRANCH, result.branch)
        self.assertEqual(("POST", CREATE_PATH, {"ref": REF, "sha": CANDIDATE}), request.calls[1])
        self.assertEqual([], request.entries)

    def test_exact_existing_branch_is_accepted_without_mutation(self) -> None:
        request = ScriptedRequest([("GET", REF_PATH, 200, ref_payload())])
        result = MAINTENANCE.reconcile("mmzen/se_harness", "0.5.1", CANDIDATE, request)
        self.assertEqual("existing", result.state)
        self.assertEqual([("GET", REF_PATH, None)], request.calls)

    def test_descendant_existing_branch_is_accepted_without_mutation(self) -> None:
        compare = f"/repos/mmzen/se_harness/compare/{CANDIDATE}...{DESCENDANT}"
        request = ScriptedRequest(
            [
                ("GET", REF_PATH, 200, ref_payload(DESCENDANT)),
                ("GET", compare, 200, {"status": "ahead"}),
            ]
        )
        result = MAINTENANCE.reconcile("mmzen/se_harness", "0.5.1", CANDIDATE, request)
        self.assertEqual("existing", result.state)
        self.assertEqual(DESCENDANT, result.tip)
        self.assertTrue(all(method == "GET" for method, _path, _payload in request.calls))

    def test_behind_or_diverged_branch_is_refused_without_mutation(self) -> None:
        compare = f"/repos/mmzen/se_harness/compare/{CANDIDATE}...{DESCENDANT}"
        for status in ("behind", "diverged"):
            with self.subTest(status=status):
                request = ScriptedRequest(
                    [
                        ("GET", REF_PATH, 200, ref_payload(DESCENDANT)),
                        ("GET", compare, 200, {"status": status}),
                    ]
                )
                with self.assertRaisesRegex(
                    MAINTENANCE.MaintenanceBranchError, "does not contain released candidate"
                ):
                    MAINTENANCE.reconcile("mmzen/se_harness", "0.5.1", CANDIDATE, request)
                self.assertTrue(all(method == "GET" for method, _path, _payload in request.calls))

    def test_concurrent_compatible_creation_is_reconciled(self) -> None:
        for status in (409, 422):
            with self.subTest(status=status):
                request = ScriptedRequest(
                    [
                        ("GET", REF_PATH, 404, {"message": "Not Found"}),
                        ("POST", CREATE_PATH, status, {"message": "Reference already exists"}),
                        ("GET", REF_PATH, 200, ref_payload()),
                    ]
                )
                result = MAINTENANCE.reconcile("mmzen/se_harness", "0.5.0", CANDIDATE, request)
                self.assertEqual("existing", result.state)
                self.assertEqual(CANDIDATE, result.tip)

    def test_malformed_and_failed_api_state_is_blocking(self) -> None:
        cases = (
            (200, {"ref": "refs/heads/wrong", "object": {"type": "commit", "sha": CANDIDATE}}, "malformed"),
            (200, ref_payload(object_type="tag"), "does not identify a commit"),
            (403, {"message": "Forbidden"}, "HTTP 403"),
        )
        for status, payload, message in cases:
            with self.subTest(message=message):
                request = ScriptedRequest([("GET", REF_PATH, status, payload)])
                with self.assertRaisesRegex(MAINTENANCE.MaintenanceBranchError, message):
                    MAINTENANCE.reconcile("mmzen/se_harness", "0.5.0", CANDIDATE, request)
                self.assertEqual(1, len(request.calls))

    def test_failed_create_without_compatible_ref_is_blocking(self) -> None:
        request = ScriptedRequest(
            [
                ("GET", REF_PATH, 404, {"message": "Not Found"}),
                ("POST", CREATE_PATH, 422, {"message": "Validation Failed"}),
                ("GET", REF_PATH, 404, {"message": "Not Found"}),
            ]
        )
        with self.assertRaisesRegex(MAINTENANCE.MaintenanceBranchError, "creation failed"):
            MAINTENANCE.reconcile("mmzen/se_harness", "0.5.0", CANDIDATE, request)


class MaintenanceWorkflowPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = (
            REPOSITORY_ROOT / ".github" / "workflows" / "publish-pypi.yml"
        ).read_text(encoding="utf-8")

    def test_reconciliation_is_after_exact_github_release_and_gates_promotion(self) -> None:
        github = self.workflow.split("  github_release:\n", 1)[1].split("  pypi:\n", 1)[0]
        final = github.index("      - name: Record final GitHub state\n")
        maintenance = github.index("      - name: Create or verify the maintenance line\n")
        self.assertLess(final, maintenance)
        self.assertIn("python .github/scripts/reconcile_maintenance_branch.py", github)
        self.assertIn("contents: write", github)
        self.assertIn("needs: [resolve, github_release]", self.workflow)

    def test_branch_is_derived_and_reported_without_another_operator_input(self) -> None:
        self.assertEqual(1, self.workflow.count("        required: true\n"))
        self.assertNotIn("      maintenance_branch:\n", self.workflow.split("permissions:", 1)[0])
        self.assertIn("maintenance_branch: ${{ steps.maintenance.outputs.branch }}", self.workflow)
        self.assertIn("maintenance_state: ${{ steps.maintenance.outputs.state }}", self.workflow)
        self.assertIn("MAINTENANCE_BRANCH: ${{ needs.github_release.outputs.maintenance_branch }}", self.workflow)


if __name__ == "__main__":
    unittest.main()
