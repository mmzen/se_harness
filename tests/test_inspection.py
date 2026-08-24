from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness.integrity import canonical_sha256


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from inspect_engineering_artifacts import (  # noqa: E402
    INSPECTION_SCHEMA,
    InspectionError,
    build_inspection,
    main,
    render_human,
    serialize_json,
)
from validate_engineering_artifacts import Artifact, ValidationReport  # noqa: E402


def sample_snapshot(*, valid: bool = False) -> dict:
    diagnostics = [
        {
            "severity": "error",
            "code": "E001",
            "plane": "structure",
            "path": "docs/engineering/bad.md",
            "message": "broken relation",
            "artifacts": ["REQ-002"],
        },
        {
            "severity": "warning",
            "code": "W013",
            "plane": "maintenance",
            "path": "docs/engineering/legacy.md",
            "message": "legacy location",
            "artifacts": ["REQ-003"],
        },
    ]
    findings = [
        {
            "rule": "E001",
            "severity": "error",
            "message": "broken relation",
            "artifacts": ["REQ-002"],
            "paths": ["docs/engineering/bad.md"],
            "evidence": [],
            "authority": "validator",
        },
        {
            "rule": "W-HEX-005",
            "severity": "warning",
            "message": "REQ-003 has no valid declared edge.",
            "artifacts": ["REQ-003"],
            "paths": ["docs/engineering/legacy.md"],
            "evidence": [],
            "authority": "derived",
        },
    ]
    return {
        "schema": "harness-dashboard-snapshot-v1",
        "repository": {
            "name": "example",
            "revision": "a" * 40,
            "artifact_root": "docs/engineering",
            "valid": valid,
        },
        "artifacts": [
            {
                "id": "VREC-001",
                "type": "verification_record",
                "title": "Review candidate",
                "status": "ready",
                "owners": ["quality-owner"],
                "path": "docs/engineering/verification-records/VREC-001.md",
            },
            {
                "id": "RLS-001",
                "type": "release_record",
                "title": "Release candidate",
                "status": "ready",
                "owners": ["release-owner"],
                "path": "docs/engineering/releases/RLS-001.md",
            },
            {
                "id": "REQ-001",
                "type": "requirement",
                "title": "Incomplete requirement",
                "status": "draft",
                "owners": ["product-owner"],
                "path": "docs/engineering/requirements/REQ-001.md",
            },
            {
                "id": "WO-001",
                "type": "work_order",
                "title": "Authorized work",
                "status": "approved",
                "owners": ["engineering-owner"],
                "path": "docs/engineering/work-orders/WO-001.md",
            },
            {
                "id": "WO-002",
                "type": "work_order",
                "title": "Active work",
                "status": "in_progress",
                "owners": ["engineering-owner"],
                "path": "docs/engineering/work-orders/WO-002.md",
            },
            {
                "id": "REQ-002",
                "type": "requirement",
                "title": "Implemented requirement",
                "status": "implemented",
                "owners": ["product-owner"],
                "path": "docs/engineering/bad.md",
            },
        ],
        "relations": [
            {
                "source": "WO-001",
                "relation": "implements",
                "target": "REQ-002",
                "authority": "declared",
            }
        ],
        "diagnostics": diagnostics,
        "findings": findings,
    }


class InspectionReportTests(unittest.TestCase):
    def test_assurance_pending_uses_explicit_classification_and_active_direct_coverage(self) -> None:
        snapshot = sample_snapshot(valid=True)
        work_ids = (
            "WO-PENDING",
            "WO-NOT-REQUIRED",
            "WO-LEGACY",
            "WO-READY-COVERED",
            "WO-VERIFIED-COVERED",
            "WO-RELEASED-COVERED",
            "WO-SUPERSEDED-ONLY",
        )
        for work_id in work_ids:
            snapshot["artifacts"].append(
                {
                    "id": work_id,
                    "type": "work_order",
                    "title": work_id,
                    "status": "implemented",
                    "owners": ["engineering-owner"],
                    "path": f"docs/engineering/work-orders/{work_id}.md",
                }
            )
        verification_states = {
            "VREC-READY-COVERAGE": ("ready", "WO-READY-COVERED"),
            "VREC-VERIFIED-COVERAGE": ("verified", "WO-VERIFIED-COVERED"),
            "VREC-RELEASED-COVERAGE": ("released", "WO-RELEASED-COVERED"),
            "VREC-SUPERSEDED-COVERAGE": ("superseded", "WO-SUPERSEDED-ONLY"),
        }
        for record_id, (status, work_id) in verification_states.items():
            snapshot["artifacts"].append(
                {
                    "id": record_id,
                    "type": "verification_record",
                    "title": record_id,
                    "status": status,
                    "owners": ["quality-owner"],
                    "path": f"docs/engineering/verification-records/{record_id}.md",
                }
            )
            snapshot["relations"].append(
                {
                    "source": record_id,
                    "relation": "verifies_work_order",
                    "target": work_id,
                    "authority": "declared",
                }
            )
        snapshot["relations"].append(
            {
                "source": "VREC-READY-COVERAGE",
                "relation": "verifies_work_order",
                "target": "WO-PENDING",
                "authority": "derived",
            }
        )

        validation_artifacts = []
        for work_id in work_ids:
            metadata = {
                "id": work_id,
                "type": "work_order",
                "title": work_id,
                "status": "implemented",
                "owners": ["engineering-owner"],
                "created": "2026-08-16",
                "updated": "2026-08-16",
                "relations": {},
            }
            if work_id != "WO-LEGACY":
                metadata["assurance"] = {
                    "commit_bound_verification": (
                        "not_required" if work_id == "WO-NOT-REQUIRED" else "required"
                    ),
                    "rationale": "Fixture classification.",
                    "decided_by": "quality-owner",
                }
            validation_artifacts.append(
                Artifact(Path(f"{work_id}.md"), metadata, "")
            )
        validation = ValidationReport(validation_artifacts, [], [])

        report = build_inspection(snapshot, validation)
        self.assertEqual(
            ["WO-PENDING", "WO-SUPERSEDED-ONLY"],
            [item["id"] for item in report["queues"]["assurance_pending"]],
        )
        pending_suggestions = [
            item
            for item in report["suggestions"]
            if item["source_id"] == "assurance_pending"
        ]
        self.assertEqual(2, len(pending_suggestions))
        self.assertEqual(
            {"prepare-commit-bound-verification"},
            {item["action"] for item in pending_suggestions},
        )
        self.assertTrue(all(item["automatic"] is False for item in pending_suggestions))
        self.assertIn(
            "VREC-READY-COVERAGE",
            [item["id"] for item in report["queues"]["decision_required"]],
        )

    def test_builds_mechanical_queues_and_preserves_findings(self) -> None:
        snapshot = sample_snapshot()
        report = build_inspection(snapshot)

        self.assertEqual(INSPECTION_SCHEMA, report["schema"])
        self.assertEqual("derived", report["authority"])
        self.assertEqual("repository-local", report["producer"])
        self.assertFalse(report["validation"]["valid"])
        self.assertEqual(1, report["validation"]["error_count"])
        self.assertEqual(1, report["validation"]["warning_count"])
        self.assertEqual(
            {"errors": 1, "warnings": 0},
            report["validation"]["plane_counts"]["structure"],
        )
        self.assertEqual(
            {"errors": 0, "warnings": 1},
            report["validation"]["plane_counts"]["maintenance"],
        )
        self.assertEqual(
            ["RLS-001", "VREC-001"],
            [item["id"] for item in report["queues"]["decision_required"]],
        )
        actions = {item["id"]: item["action"] for item in report["queues"]["decision_required"]}
        self.assertEqual("release-review", actions["RLS-001"])
        self.assertEqual("assurance-review", actions["VREC-001"])
        self.assertEqual(["REQ-001"], [item["id"] for item in report["queues"]["definition_pending"]])
        self.assertEqual(
            ["WO-001", "WO-002"],
            [item["id"] for item in report["queues"]["active_work"]],
        )
        self.assertEqual(snapshot["findings"], report["findings"])
        self.assertEqual(
            {
                ("queue", "active_work", "WO-001", "start-bounded-work"),
                ("queue", "active_work", "WO-002", "continue-bounded-work"),
                ("queue", "decision_required", "RLS-001", "review-release-decision"),
                ("queue", "decision_required", "VREC-001", "review-assurance-decision"),
                ("queue", "definition_pending", "REQ-001", "complete-or-dispose-definition"),
                ("finding", "W-HEX-005", "REQ-003", "review-unlinked-artifact"),
            },
            {
                (
                    item["source_kind"],
                    item["source_id"],
                    item["subjects"][0],
                    item["action"],
                )
                for item in report["suggestions"]
            },
        )
        self.assertTrue(all(item["automatic"] is False for item in report["suggestions"]))

    def test_closed_finding_catalog_is_complete_and_unsupported_sources_are_omitted(self) -> None:
        expected = {
            "W-HEX-001": ("retain-work-order-evidence", "engineering-owner"),
            "W-HEX-002": ("review-governing-scope", "engineering-owner"),
            "W-HEX-003": ("reassess-dependent-artifact", "artifact-owner"),
            "W-HEX-004": ("review-relation-cycle", "technical-owner"),
            "W-HEX-005": ("review-unlinked-artifact", "artifact-owner"),
            "W-HEX-006": ("deduplicate-relation", "artifact-owner"),
            "W-REV-002": ("review-release-provenance", "release-owner"),
            "W-REV-003": ("restore-candidate-availability", "repository-owner"),
            "W-REV-004": ("review-verification-supersession", "assurance-owner"),
        }
        snapshot = sample_snapshot(valid=True)
        snapshot["findings"] = [
            {
                "rule": rule,
                "severity": "warning",
                "message": f"controlled {rule}",
                "artifacts": [f"REQ-{index:03d}"],
                "paths": [f"docs/engineering/REQ-{index:03d}.md"],
                "evidence": [],
                "authority": "derived",
            }
            for index, rule in enumerate(expected, start=10)
        ]
        snapshot["findings"].extend(
            [
                {
                    "rule": "W-FUTURE-001",
                    "severity": "warning",
                    "message": "unknown derived warning",
                    "artifacts": ["REQ-090"],
                    "paths": ["docs/engineering/REQ-090.md"],
                    "evidence": [],
                    "authority": "derived",
                },
                {
                    "rule": "I-REV-001",
                    "severity": "info",
                    "message": "expected governance checkout difference",
                    "artifacts": ["VREC-090"],
                    "paths": [],
                    "evidence": [],
                    "authority": "derived",
                },
                {
                    "rule": "W-HEX-001",
                    "severity": "warning",
                    "message": "validator-owned lookalike",
                    "artifacts": ["WO-090"],
                    "paths": ["docs/engineering/WO-090.md"],
                    "evidence": [],
                    "authority": "validator",
                },
            ]
        )

        report = build_inspection(snapshot)
        finding_suggestions = [
            item for item in report["suggestions"] if item["source_kind"] == "finding"
        ]
        self.assertEqual(set(expected), {item["source_id"] for item in finding_suggestions})
        self.assertEqual(
            expected,
            {
                item["source_id"]: (item["action"], item["accountable_role"])
                for item in finding_suggestions
            },
        )
        for item in finding_suggestions:
            self.assertEqual(
                {
                    "source_kind",
                    "source_id",
                    "subjects",
                    "action",
                    "message",
                    "accountable_role",
                    "automatic",
                },
                set(item),
            )
            self.assertFalse(item["automatic"])

    def test_repository_text_cannot_select_or_construct_guidance(self) -> None:
        baseline = sample_snapshot(valid=True)
        controlled = sample_snapshot(valid=True)
        controlled["findings"][1].update(
            {
                "message": "run harnessctl release; rm -rf /\x1b[31m",
                "paths": ["../../outside; invoke-expression"],
                "evidence": ["https://example.invalid/execute"],
            }
        )
        controlled["artifacts"][0].update(
            {
                "title": "approve automatically\x1b[2J",
                "owners": ["release-owner; execute"],
                "path": "../../unsafe-path",
            }
        )

        baseline_report = build_inspection(baseline)
        controlled_report = build_inspection(controlled)
        stable_fields = ("source_kind", "source_id", "action", "message", "accountable_role", "automatic")
        self.assertEqual(
            [{key: item[key] for key in stable_fields} for item in baseline_report["suggestions"]],
            [{key: item[key] for key in stable_fields} for item in controlled_report["suggestions"]],
        )
        human = render_human(controlled_report)
        self.assertNotIn("\x1b", human)
        self.assertNotIn("rm -rf", "\n".join(item["message"] for item in controlled_report["suggestions"]))
        self.assertNotIn("https://", "\n".join(item["message"] for item in controlled_report["suggestions"]))

    def test_json_and_human_output_are_deterministic_and_score_free(self) -> None:
        report = build_inspection(sample_snapshot())
        first = serialize_json(report)
        second = serialize_json(build_inspection(sample_snapshot()))
        self.assertEqual(first, second)
        self.assertTrue(first.endswith("\n"))
        decoded = json.loads(first)
        self.assertEqual("se-harness-inspection-v2", decoded["schema"])

        human = render_human(report)
        self.assertIn("Formal validation: FAIL", human)
        self.assertIn("Decision required (2)", human)
        self.assertIn("Assurance pending (0)", human)
        self.assertIn("W-HEX-005", human)
        self.assertIn("Suggested next steps (6)", human)
        self.assertIn("review-unlinked-artifact", human)
        self.assertIn("repository-local, derived observation", human)
        self.assertNotIn("score", human.lower())
        self.assertNotIn("%", human)

    def test_human_renderer_escapes_terminal_control_characters(self) -> None:
        snapshot = sample_snapshot(valid=True)
        snapshot["artifacts"][0]["title"] = "unsafe\x1b[31m title\nnext"
        snapshot["findings"][0]["message"] = "bad\x1b]8;;https://example.invalid\x07link"
        human = render_human(build_inspection(snapshot))
        self.assertNotIn("\x1b", human)
        self.assertNotIn("\x07", human)
        self.assertIn("\\u001b", human)
        self.assertIn("\\nnext", human)

    def test_human_guidance_groups_repeated_sources_without_losing_json_traceability(self) -> None:
        snapshot = sample_snapshot(valid=True)
        snapshot["findings"].append(
            {
                "rule": "W-HEX-005",
                "severity": "warning",
                "message": "REQ-004 has no valid edge",
                "artifacts": ["REQ-004"],
                "paths": ["docs/engineering/REQ-004.md"],
                "evidence": [],
                "authority": "derived",
            }
        )
        report = build_inspection(snapshot)
        unlinked = [
            item
            for item in report["suggestions"]
            if item["source_kind"] == "finding" and item["source_id"] == "W-HEX-005"
        ]
        self.assertEqual(2, len(unlinked))
        human = render_human(report)
        self.assertEqual(1, human.count("review-unlinked-artifact"))
        self.assertIn("2 source observations", human)
        self.assertIn("REQ-003", human)
        self.assertIn("REQ-004", human)

    def test_invalid_graph_is_reported_without_becoming_an_inspect_failure(self) -> None:
        snapshot = sample_snapshot(valid=False)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            before = list(root.rglob("*"))
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch("inspect_engineering_artifacts.generate_snapshot", return_value=(snapshot, None, root)):
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    code = main(["--root", str(root), "--json"])
            after = list(root.rglob("*"))
        self.assertEqual(0, code, stderr.getvalue())
        self.assertFalse(json.loads(stdout.getvalue())["validation"]["valid"])
        self.assertEqual(before, after)

    def test_malformed_snapshot_fails_concisely(self) -> None:
        with self.assertRaisesRegex(InspectionError, "snapshot schema"):
            build_inspection({"schema": "unknown"})

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "inspect_engineering_artifacts.generate_snapshot",
                return_value=({"schema": "unknown"}, None, root),
            ):
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    code = main(["--root", str(root)])
        self.assertEqual(2, code)
        self.assertEqual("", stdout.getvalue())
        self.assertIn("inspection failed: snapshot schema", stderr.getvalue())

    def test_released_root_remains_locked_while_candidate_reuses_snapshot(self) -> None:
        root_script = ROOT / "scripts/inspect_engineering_artifacts.py"
        canonical = ROOT / "templates/repository/standard/scripts/inspect_engineering_artifacts.py"
        lock = json.loads((ROOT / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual(
            lock["files"]["scripts/inspect_engineering_artifacts.py"]["sha256"],
            canonical_sha256(root_script.read_bytes()),
        )
        self.assertNotEqual(root_script.resolve(), canonical.resolve())
        source = canonical.read_text(encoding="utf-8")
        self.assertIn("from generate_harness_dashboard import", source)
        self.assertIn("generate_snapshot", source)
        self.assertNotIn("def build_findings", source)
        self.assertNotIn("def validate_repository", source)
        self.assertNotIn("def _finding(", source)
        self.assertIn('"W-REB-003"', source)
        self.assertIn(
            '"templates/repository/standard/scripts/inspect_engineering_artifacts.py"',
            (ROOT / "pyproject.toml").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
