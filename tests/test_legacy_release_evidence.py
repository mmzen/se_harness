"""Verification for SPEC-LRE-002: the evaluator-evidence floor (WO-LRE-002).

A released record carrying neither evaluator-evidence field is not assessed
against the binding (REQ-LRE-003, owner decision of 2026-08-30). The
declaration mechanism of SPEC-LRE-001 — the package module, the validator
resolver, the frozen self-hosting set, the `W024` debt warnings and the
pre-apply upgrade refusal — is retired; `W024` stays reserved.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load test module: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


CANDIDATE_VALIDATOR = load_module(
    "evidence_floor_candidate_validator",
    REPOSITORY_ROOT / "templates/repository/standard/scripts/validate_engineering_artifacts.py",
)
PUBLICATION = load_module(
    "evidence_floor_publication",
    REPOSITORY_ROOT / ".github/scripts/publish_dashboard.py",
)


class FloorValidationTests(unittest.TestCase):
    """LRE-FLR-001, LRE-FLR-002 and LRE-FLR-005 on fixture artifacts."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def artifact(self, relative: str, metadata: dict):
        return CANDIDATE_VALIDATOR.Artifact(path=self.root / relative, metadata=metadata, body="")

    def record(self, identifier: str = "RLS-CON-001", **overrides):
        metadata = {
            "id": identifier,
            "type": "release_record",
            "status": "released",
            "released_at": "2026-06-01T00:00:00Z",
            "version": "0.0.1",
            "relations": {
                "satisfies": ["REL-CON-001"],
                "includes_verification": ["VREC-CON-001"],
                "releases_work": ["WO-CON-001"],
            },
        }
        metadata.update(overrides)
        return self.artifact(f"docs/engineering/sample/releases/{identifier}.md", metadata)

    def binding_errors(self, artifacts) -> list:
        errors = CANDIDATE_VALIDATOR.validate_type_specific_metadata(artifacts, self.root)
        return [item for item in errors if "evaluator" in item.message or "evidence" in item.message]

    def test_an_unbound_released_record_is_not_assessed(self) -> None:
        self.assertEqual([], self.binding_errors([self.record()]))

    def test_a_partially_bound_record_still_fails(self) -> None:
        for fields in (
            {"evaluator_evidence_path": "docs/engineering/sample/evidence/e.json"},
            {"evaluator_evidence_sha256": "a" * 64},
        ):
            with self.subTest(fields=sorted(fields)):
                self.assertNotEqual([], self.binding_errors([self.record(**fields)]))

    def test_a_bound_record_keeps_the_binding_checks(self) -> None:
        malformed = self.record(
            evaluator_evidence_path="docs/engineering/sample/evidence/e.json",
            evaluator_evidence_sha256="not-a-digest",
        )
        self.assertNotEqual([], self.binding_errors([malformed]))

    def test_the_declaration_key_is_inert(self) -> None:
        # LRE-FLR-005: a historical work order carrying the optional key stays
        # valid, and the value grants and changes nothing.
        packet = {
            "schema": "se-harness-evaluator-upgrade-v1",
            "scope": "standard-root-only",
            "legacy_releases_without_evaluator_evidence": ["RLS-CON-001", "not even an id"],
        }
        work_order = self.artifact(
            "docs/engineering/sample/work-orders/WO-CON-001.md",
            {
                "id": "WO-CON-001",
                "type": "work_order",
                "status": "approved",
                "evaluator_upgrade": packet,
                "relations": {
                    "implements": ["REQ-CON-001"],
                    "specifications": ["SPEC-CON-001"],
                    "verification": ["VER-CON-001"],
                },
            },
        )
        errors = CANDIDATE_VALIDATOR.validate_type_specific_metadata(
            [self.record(), work_order], self.root
        )
        self.assertEqual(
            [], [item for item in errors if "legacy_releases_without_evaluator_evidence" in item.message]
        )
        self.assertEqual([], self.binding_errors([self.record(), work_order]))


class ThisRepositoryTests(unittest.TestCase):
    """LRE-FLR-001 and LRE-FLR-003 over this repository's own tree."""

    def test_this_repository_validates_clean_with_no_w024(self) -> None:
        report = CANDIDATE_VALIDATOR.validate_repository(REPOSITORY_ROOT)
        self.assertEqual([], report.errors)
        self.assertEqual([], [item for item in report.warnings if item.code == "W024"])

    def test_the_retired_machinery_is_absent_from_the_validator(self) -> None:
        for name in (
            "resolve_legacy_release_evidence",
            "legacy_release_evidence_state",
            "validate_legacy_release_evidence_warnings",
            "LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE",
            "SELF_HOSTING_DECLARER",
        ):
            with self.subTest(name=name):
                self.assertFalse(hasattr(CANDIDATE_VALIDATOR, name))


class PublicationViewTests(unittest.TestCase):
    """LRE-FLR-006: the dashboard exempts only a wholly unbound record."""

    def test_the_publication_view_exempts_only_a_wholly_unbound_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            binding = PUBLICATION._validated_evaluator_binding(
                repository,
                "0" * 40,
                {"id": "RLS-ANY-001"},
            )
            self.assertEqual({"path": None, "sha256": None}, binding)
            with self.assertRaises(PUBLICATION.PublicationError):
                PUBLICATION._validated_evaluator_binding(
                    repository,
                    "0" * 40,
                    {"id": "RLS-ANY-001", "evaluator_evidence_path": "docs/engineering/x/evidence/e.json"},
                )
            self.assertFalse(hasattr(PUBLICATION, "LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE"))


class FloorSweepTests(unittest.TestCase):
    """LRE-FLR-004 and LRE-FLR-007: nothing of the mechanism survives."""

    SOURCES = ("se_harness", "templates/repository/standard/scripts", ".github/scripts", "repository_tools")

    def sources(self) -> list[Path]:
        found = [
            path
            for base in self.SOURCES
            for path in sorted((REPOSITORY_ROOT / base).rglob("*.py"))
            if "__pycache__" not in path.parts
        ]
        self.assertGreater(len(found), 10)
        return found

    def test_no_legacy_machinery_survives(self) -> None:
        # The root scripts/ copies are the released 0.11.0 evaluator's files and
        # keep the resolver until the next root adoption; they are not swept.
        for forbidden in (
            "legacy_release_evidence",
            "LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE",
            "SELF_HOSTING_DECLARER",
            "RLS-SEH-0",
            '"W024"',
        ):
            with self.subTest(forbidden=forbidden):
                hits = [
                    path.relative_to(REPOSITORY_ROOT).as_posix()
                    for path in self.sources()
                    if forbidden in path.read_text(encoding="utf-8")
                ]
                self.assertEqual([], hits)

    def test_the_module_and_the_vector_fixture_are_gone(self) -> None:
        self.assertFalse((REPOSITORY_ROOT / "se_harness/legacy_release_evidence.py").exists())
        self.assertFalse((REPOSITORY_ROOT / "tests/fixtures/legacy_release_evidence").exists())

    def test_the_upgrade_evidence_carries_no_declaration(self) -> None:
        from se_harness.installer import _upgrade_evidence_bytes

        value = json.loads(
            _upgrade_evidence_bytes(
                prior_lock_sha256="a" * 64,
                old_lock={"schema": 3, "tool_version": "0.11.0", "files": {}},
                lock={"schema": 3, "tool_version": "0.12.0", "files": {}},
                changes=[],
            )
        )
        self.assertNotIn("legacy_releases_without_evaluator_evidence", value)


if __name__ == "__main__":
    unittest.main()
