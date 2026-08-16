from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPOSITORY_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_engineering_artifacts import validate_repository  # noqa: E402


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def formal(
    artifact_id: str,
    artifact_type: str,
    status: str,
    relations: dict[str, list[str]],
    *,
    extra: str = "",
) -> str:
    relation_lines = "\n".join(
        f"{name} = {json.dumps(targets)}" for name, targets in relations.items()
    )
    return f'''+++
id = "{artifact_id}"
type = "{artifact_type}"
title = "{artifact_id}"
status = "{status}"
owners = ["owner"]
created = "2026-08-16"
updated = "2026-08-16"
{extra.strip()}

[relations]
{relation_lines}
+++

# {artifact_id}
'''


class OperatingContractReadinessTests(unittest.TestCase):
    def findings(
        self,
        *,
        ops_status: str = "approved",
        target_type: str = "requirement",
        requirement_status: str = "implemented",
        work_status: str | None = "implemented",
        require_verified_work: bool = False,
        vrec_status: str | None = None,
        extra_incomplete_work: bool = False,
        vrec_work_order: str = "WO-OPS-001",
    ) -> list[tuple[str, str, str]]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            base = root / "docs/engineering/product"
            write(
                root / ".engineering-harness.toml",
                "[revision_provenance]\n"
                f"required_for_verified_work = {str(require_verified_work).lower()}\n"
                "required_for_release = false",
            )
            write(
                base / "intent/INT-OPS-001.md",
                formal("INT-OPS-001", "intent", "approved", {}),
            )
            write(
                base / "capabilities/CAP-OPS-001.md",
                formal(
                    "CAP-OPS-001",
                    "capability",
                    "approved",
                    {"derives_from": ["INT-OPS-001"]},
                ),
            )
            write(
                base / "requirements/REQ-OPS-001.md",
                formal(
                    "REQ-OPS-001",
                    "requirement",
                    requirement_status,
                    {"derives_from": ["CAP-OPS-001"]},
                    extra=(
                        'statement = "THE SYSTEM SHALL retain operating assurance."\n'
                        'verification_method = "automated-test"'
                    ),
                ),
            )
            write(
                base / "specifications/SPEC-OPS-001.md",
                formal(
                    "SPEC-OPS-001",
                    "specification",
                    "implemented",
                    {"specifies": ["REQ-OPS-001"]},
                ),
            )
            write(
                base / "verification/VER-OPS-001.md",
                formal(
                    "VER-OPS-001",
                    "verification",
                    "approved",
                    {"verifies": ["REQ-OPS-001"]},
                ),
            )

            work_order_ids: list[str] = []
            if work_status is not None:
                work_order_ids.append("WO-OPS-001")
                write(
                    base / "work-orders/WO-OPS-001.md",
                    formal(
                        "WO-OPS-001",
                        "work_order",
                        work_status,
                        {
                            "implements": ["REQ-OPS-001"],
                            "specifications": ["SPEC-OPS-001"],
                            "verification": ["VER-OPS-001"],
                        },
                    ),
                )
            if extra_incomplete_work:
                work_order_ids.append("WO-OPS-002")
                write(
                    base / "work-orders/WO-OPS-002.md",
                    formal(
                        "WO-OPS-002",
                        "work_order",
                        "in_progress",
                        {
                            "implements": ["REQ-OPS-001"],
                            "specifications": ["SPEC-OPS-001"],
                            "verification": ["VER-OPS-001"],
                        },
                    ),
                )

            target_id = "REQ-OPS-001"
            if target_type == "release_contract":
                target_id = "REL-OPS-001"
                write(
                    base / "release/REL-OPS-001.md",
                    formal(
                        "REL-OPS-001",
                        "release_contract",
                        "approved",
                        {"gates": work_order_ids or ["WO-OPS-001"]},
                    ),
                )
            elif target_type == "specification":
                target_id = "SPEC-OPS-001"
            elif target_type == "unknown":
                target_id = "REQ-OPS-999"
            write(
                base / "operations/OPS-OPS-001.md",
                formal(
                    "OPS-OPS-001",
                    "operating_contract",
                    ops_status,
                    {"assures": [target_id]},
                ),
            )

            if vrec_status is not None:
                evidence = "docs/engineering/product/evidence/WO-OPS-001-verification.md"
                write(root / evidence, "# Evidence\n\nCandidate checks passed.")
                write(
                    base / "verification-records/VREC-OPS-001.md",
                    formal(
                        "VREC-OPS-001",
                        "verification_record",
                        vrec_status,
                        {
                            "verifies_work_order": [vrec_work_order],
                            "conforms_to": ["VER-OPS-001"],
                        },
                        extra=f'''commit = "{'a' * 40}"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-16T12:00:00Z"
artifact_snapshot_sha256 = "{'b' * 64}"
evidence_paths = ["{evidence}"]''',
                    ),
                )

            report = validate_repository(root)
            return [
                (item.code, item.plane, item.message)
                for item in report.errors
                if item.code in {"E006", "E011", "E017", "E018"}
            ]

    def test_assures_target_type_is_enforced_for_every_ops_state(self) -> None:
        for status in ("draft", "ready", "approved"):
            for target_type in ("release_contract", "specification"):
                with self.subTest(status=status, target_type=target_type):
                    findings = self.findings(
                        ops_status=status,
                        target_type=target_type,
                    )
                    self.assertEqual(1, len(findings))
                    self.assertEqual(("E011", "structure"), findings[0][:2])
        self.assertEqual([], self.findings(target_type="requirement"))
        unknown = self.findings(target_type="unknown")
        self.assertEqual(1, len(unknown))
        self.assertEqual(("E006", "structure"), unknown[0][:2])

    def test_active_ops_requires_an_active_requirement(self) -> None:
        for requirement_status in ("draft", "ready", "rejected", "superseded"):
            with self.subTest(requirement_status=requirement_status):
                findings = self.findings(requirement_status=requirement_status)
                self.assertEqual(1, len(findings))
                self.assertEqual(("E017", "governance"), findings[0][:2])
                self.assertIn("inactive requirement 'REQ-OPS-001'", findings[0][2])

    def test_active_ops_requires_completed_implementing_work(self) -> None:
        for work_status in (None, "approved", "in_progress"):
            with self.subTest(work_status=work_status):
                findings = self.findings(work_status=work_status)
                self.assertEqual(1, len(findings))
                self.assertEqual(("E017", "governance"), findings[0][:2])
                self.assertIn("without completed implementing work", findings[0][2])
        for work_status in ("implemented", "verified", "released"):
            with self.subTest(work_status=work_status):
                self.assertEqual([], self.findings(work_status=work_status))

    def test_completed_work_passes_when_commit_bound_policy_is_disabled(self) -> None:
        self.assertEqual([], self.findings(require_verified_work=False))

    def test_commit_bound_policy_requires_eligible_vrec_coverage(self) -> None:
        for vrec_status in (None, "draft", "ready", "rejected", "superseded"):
            with self.subTest(vrec_status=vrec_status):
                findings = self.findings(
                    require_verified_work=True,
                    vrec_status=vrec_status,
                )
                self.assertEqual(1, len(findings))
                self.assertEqual(("E018", "policy"), findings[0][:2])
        for vrec_status in ("verified", "released"):
            with self.subTest(vrec_status=vrec_status):
                self.assertEqual(
                    [],
                    self.findings(
                        require_verified_work=True,
                        vrec_status=vrec_status,
                    ),
                )

    def test_only_a_vrec_covering_completed_work_satisfies_policy(self) -> None:
        findings = self.findings(
            require_verified_work=True,
            vrec_status="verified",
            extra_incomplete_work=True,
            vrec_work_order="WO-OPS-002",
        )
        self.assertEqual(1, len(findings))
        self.assertEqual(("E018", "policy"), findings[0][:2])

    def test_one_eligible_path_is_enough_and_ready_ops_skips_readiness(self) -> None:
        self.assertEqual(
            [],
            self.findings(
                require_verified_work=True,
                vrec_status="verified",
                extra_incomplete_work=True,
            ),
        )
        self.assertEqual(
            [],
            self.findings(
                ops_status="ready",
                work_status=None,
                require_verified_work=True,
            ),
        )


if __name__ == "__main__":
    unittest.main()
