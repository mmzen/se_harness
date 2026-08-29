from __future__ import annotations

import ast
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPOSITORY_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_engineering_artifacts import (  # noqa: E402
    TAXONOMY_VERSION,
    VALIDATION_PLANES,
    Diagnostic,
    ValidationReport,
    render_human,
    validate_repository,
)


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
created = "2026-08-15"
updated = "2026-08-15"
{extra.strip()}

[relations]
{relation_lines}
+++

# {artifact_id}
'''


class ValidationTaxonomyTests(unittest.TestCase):
    def test_every_diagnostic_emission_declares_a_plane(self) -> None:
        source = (REPOSITORY_ROOT / "scripts/validate_engineering_artifacts.py").read_text(
            encoding="utf-8"
        )
        tree = ast.parse(source)
        missing: list[int] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                continue
            if node.func.id == "_add_error" and not any(
                keyword.arg == "plane" for keyword in node.keywords
            ):
                missing.append(node.lineno)
            if (
                node.func.id == "Diagnostic"
                and len(node.args) < 4
                and not any(keyword.arg == "plane" for keyword in node.keywords)
            ):
                missing.append(node.lineno)
        self.assertEqual([], missing)

    def test_policy_and_operator_reference_define_the_same_small_vocabulary(self) -> None:
        quality = (REPOSITORY_ROOT / "docs/engineering/QUALITY_GATES.md").read_text(
            encoding="utf-8"
        )
        canonical_quality = (
            REPOSITORY_ROOT
            / "templates/repository/standard/docs/engineering/QUALITY_GATES.md"
        ).read_text(encoding="utf-8")
        reference = (REPOSITORY_ROOT / "docs/notes/harnessctl-reference.md").read_text(
            encoding="utf-8"
        )
        # The root copy is the hash-locked policy of the released evaluator named in
        # the lock. Under the 0.7.1 root the candidate template added WO-ECP-009's
        # transition binding index, the graph-structural checks and the amended
        # QG-010 / new QG-011, and that divergence was declared here rather than
        # hidden. Since WO-HUP-008 adopted 0.8.0 the root copy is the candidate
        # template byte for byte; the assertion reads the root identity, not a guess.
        root_version = json.loads(
            (REPOSITORY_ROOT / ".engineering-harness.lock").read_text(encoding="utf-8")
        )["evaluator"]["version"]
        markers = ("## Transition binding index", "### Graph-structural checks", "**QG-011:**", "`QGS-EDGE`", "`QG-STRUCTURAL`")
        for marker in markers:
            self.assertIn(marker, canonical_quality, marker)
        if root_version == "0.7.1":
            for marker in markers:
                self.assertNotIn(marker, quality, marker)
            released_lines = quality.splitlines()
            start = next(i for i, line in enumerate(released_lines) if line.startswith("**QG-010:**"))
            end = next(i for i in range(start + 1, len(released_lines)) if not released_lines[i].strip())
            retained = [line for i, line in enumerate(released_lines) if not (start <= i < end)]
            candidate_lines = set(canonical_quality.splitlines())
            self.assertEqual([], [line for line in retained if line not in candidate_lines])
        elif "`scope`" in quality:
            # The root carries WO-ECP-013's scope checkpoint: it is the candidate template.
            self.assertEqual(canonical_quality, quality)
        else:
            # WO-ECP-013: the candidate template amended QG-010 and QG-011 for the
            # scope checkpoint; a root released before it lacks exactly those two
            # paragraphs' new sentences, and that divergence is declared here.
            def without_paragraphs(text: str, *starts: str) -> list[str]:
                lines = text.splitlines()
                keep = []
                skipping = False
                for line in lines:
                    if any(line.startswith(start) for start in starts):
                        skipping = True
                    if skipping and not line.strip():
                        skipping = False
                        continue
                    if not skipping:
                        keep.append(line)
                return keep

            self.assertIn("`scope`", canonical_quality)
            self.assertEqual(
                without_paragraphs(canonical_quality, "**QG-010:**", "**QG-011:**"),
                without_paragraphs(quality, "**QG-010:**", "**QG-011:**"),
            )
        self.assertIn("| `authoring_ready` |", quality)
        self.assertIn("| `release_unit_ready` |", quality)
        self.assertIn("| `QG-G5-RELEASE-PREPARATION` | `QGP-G5P-GRAPH`, `QGP-G5P-INTEGRITY`, `QGP-G5P-RELEASE-UNIT` |\n", quality)
        self.assertIn("| `QG-G1-DEFINITION` | `QGP-G1-GRAPH`, `QGP-G1-INTEGRITY`, `QGP-G1-AUTHORING` |\n", quality)
        self.assertIn("| `QG-G2-ARCHITECTURE` | `QGP-G2-GRAPH`, `QGP-G2-INTEGRITY`, `QGP-G2-AUTHORING` |\n", quality)
        self.assertIn("BCP 14", canonical_quality)
        self.assertIn("`QG-G4-IMPLEMENTATION-EVIDENCE`", canonical_quality)
        for plane in VALIDATION_PLANES:
            self.assertIn(f"`{plane}`", canonical_quality)
            self.assertIn(f"`{plane}`", reference)
        self.assertIn("MUST NOT change error-versus-warning severity", canonical_quality)
        self.assertIn("do not change severity", reference)

    def test_vocabulary_and_diagnostic_construction_are_closed(self) -> None:
        self.assertEqual(
            ("structure", "governance", "policy", "maintenance"),
            VALIDATION_PLANES,
        )
        self.assertEqual("se-harness-validation-taxonomy-v1", TAXONOMY_VERSION)
        for plane in VALIDATION_PLANES:
            self.assertEqual(plane, Diagnostic("artifact.md", "E001", "message", plane).plane)
        with self.assertRaises(ValueError):
            Diagnostic("artifact.md", "E001", "message", "other")

    def test_json_and_human_reports_add_planes_without_a_score(self) -> None:
        report = ValidationReport(
            artifacts=[],
            errors=[Diagnostic("broken.md", "E001", "broken", "structure")],
            warnings=[Diagnostic("legacy.md", "W015", "legacy", "maintenance")],
        )
        payload = report.to_dict(Path.cwd())
        self.assertEqual(TAXONOMY_VERSION, payload["taxonomy"])
        self.assertEqual(
            {
                "structure": {"errors": 1, "warnings": 0},
                "governance": {"errors": 0, "warnings": 0},
                "policy": {"errors": 0, "warnings": 0},
                "maintenance": {"errors": 0, "warnings": 1},
            },
            payload["plane_counts"],
        )
        self.assertEqual("structure", payload["errors"][0]["plane"])
        self.assertEqual("maintenance", payload["warnings"][0]["plane"])
        rendered = render_human(report)
        self.assertIn("Planes:", rendered)
        self.assertIn("[E001] [structure] broken.md: broken", rendered)
        self.assertIn("[W015] [maintenance] legacy.md: legacy", rendered)
        self.assertNotIn("score", rendered.lower())

    def test_current_rule_authority_selects_the_expected_plane(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)

            structure_root = root / "structure"
            write(
                structure_root / "docs/engineering/sample/intent/INT-TAX-001.md",
                '''+++
id = "INT-TAX-001"
type = "intent"
status = "approved"
owners = ["owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
+++
''',
            )
            structure = validate_repository(structure_root)
            self.assertTrue(structure.errors)
            self.assertEqual({"structure"}, {item.plane for item in structure.errors})

            governance_root = root / "governance"
            base = governance_root / "docs/engineering/sample"
            write(base / "intent/INT-TAX-001.md", formal("INT-TAX-001", "intent", "approved", {}))
            write(
                base / "capabilities/CAP-TAX-001.md",
                formal("CAP-TAX-001", "capability", "approved", {"derives_from": ["INT-TAX-001"]}),
            )
            write(
                base / "requirements/REQ-TAX-001.md",
                formal(
                    "REQ-TAX-001",
                    "requirement",
                    "approved",
                    {"derives_from": ["CAP-TAX-001"]},
                    extra='statement = "THE SYSTEM SHALL classify findings."\nverification_method = "test"',
                ),
            )
            governance = validate_repository(governance_root)
            coverage = [item for item in governance.errors if item.code in {"E007", "E008"}]
            self.assertEqual(2, len(coverage))
            self.assertEqual({"governance"}, {item.plane for item in coverage})

            policy_root = root / "policy"
            base = policy_root / "docs/engineering/sample"
            write(
                policy_root / ".engineering-harness.toml",
                "[revision_provenance]\nrequired_for_verified_work = true\nrequired_for_release = false",
            )
            write(base / "intent/INT-TAX-001.md", formal("INT-TAX-001", "intent", "approved", {}))
            write(
                base / "capabilities/CAP-TAX-001.md",
                formal("CAP-TAX-001", "capability", "approved", {"derives_from": ["INT-TAX-001"]}),
            )
            write(
                base / "requirements/REQ-TAX-001.md",
                formal(
                    "REQ-TAX-001",
                    "requirement",
                    "implemented",
                    {"derives_from": ["CAP-TAX-001"]},
                    extra='statement = "THE SYSTEM SHALL classify findings."\nverification_method = "test"',
                ),
            )
            write(
                base / "specifications/SPEC-TAX-001.md",
                formal("SPEC-TAX-001", "specification", "implemented", {"specifies": ["REQ-TAX-001"]}),
            )
            write(
                base / "verification/VER-TAX-001.md",
                formal("VER-TAX-001", "verification", "approved", {"verifies": ["REQ-TAX-001"]}),
            )
            write(
                base / "work-orders/WO-TAX-001.md",
                formal(
                    "WO-TAX-001",
                    "work_order",
                    "verified",
                    {
                        "implements": ["REQ-TAX-001"],
                        "specifications": ["SPEC-TAX-001"],
                        "verification": ["VER-TAX-001"],
                    },
                ),
            )
            policy = validate_repository(policy_root)
            configured = [
                item
                for item in policy.errors
                if item.code == "E010" and "requires coverage" in item.message
            ]
            self.assertEqual(1, len(configured))
            self.assertEqual("policy", configured[0].plane)

            maintenance_root = root / "maintenance"
            write(
                maintenance_root / "docs/engineering/sample/INT-TAX-001.md",
                formal("INT-TAX-001", "intent", "approved", {}),
            )
            maintenance = validate_repository(maintenance_root)
            placement = [item for item in maintenance.warnings if item.code == "W013"]
            self.assertEqual(1, len(placement))
            self.assertEqual("maintenance", placement[0].plane)


if __name__ == "__main__":
    unittest.main()
