"""Verification for SPEC-DLC-001: the declared architecture-generation exemption.

`VER-DLC-001` requires that one semantics is implemented twice - once in
`se_harness/definition_generation.py` for the package and once, self-contained, in
the candidate validator script - and that the two agree. Every vector in
`tests/fixtures/definition_generation/resolution_vectors.json` is resolved by both.

The scenarios here also hold the line the increment exists to draw: an architecture's
lifecycle status is not an input to its decision assessment, and an accepted exemption
suppresses the error without ever suppressing the `W014` diagnostic.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness import definition_generation as PACKAGE
from tests import definition_generation_measurement as MEASUREMENT


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = REPOSITORY_ROOT / "tests/fixtures/definition_generation/resolution_vectors.json"
CANDIDATE_TEMPLATE = (
    REPOSITORY_ROOT / "templates/repository/standard/scripts/validate_engineering_artifacts.py"
)
MEASUREMENT_EVIDENCE = (
    REPOSITORY_ROOT
    / "docs/engineering/definition-lifecycle/evidence/WO-DLC-001/frozen_set_measurement.json"
)


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load test module: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


CANDIDATE_VALIDATOR = load_module("definition_generation_candidate_validator", CANDIDATE_TEMPLATE)
VECTORS = json.loads(VECTOR_PATH.read_text(encoding="utf-8"))


def package_resolution(artifacts: list[dict], work_orders: list[dict]) -> dict:
    return PACKAGE.resolve(artifacts, work_orders).as_dict()


def script_resolution(artifacts: list[dict], work_orders: list[dict]) -> dict:
    return CANDIDATE_VALIDATOR.resolve_definition_generation(artifacts, work_orders)


def architecture_artifact(identifier: str, status: str, *, assessed: bool = False):
    """Build the artifact `decision_assessment_state` reads, with nothing else on it."""

    metadata: dict[str, object] = {"id": identifier, "type": "architecture", "status": status}
    if assessed:
        metadata["decision_assessment"] = {
            "outcome": "no_significant_decision",
            "triggers": [],
            "rationale": "The fixture applies the existing architecture.",
            "assessed_by": "technical-owner",
        }
    return CANDIDATE_VALIDATOR.Artifact(
        path=Path(f"docs/engineering/sample/architecture/{identifier}.md"),
        metadata=metadata,
        body="",
    )


class ResolutionVectorTests(unittest.TestCase):
    """Both implementations return the committed result for every vector."""

    def test_fixture_declares_its_own_schema_and_specification(self) -> None:
        self.assertEqual("se-harness-definition-generation-vectors-v1", VECTORS["schema"])
        self.assertEqual("SPEC-DLC-001", VECTORS["specification"])
        names = [case["name"] for case in VECTORS["cases"]]
        self.assertEqual(sorted(set(names)), sorted(names))
        self.assertGreaterEqual(len(names), 20)

    def test_package_implementation_matches_every_vector(self) -> None:
        for case in VECTORS["cases"]:
            with self.subTest(case=case["name"], implementation="package"):
                self.assertEqual(
                    case["expected"],
                    package_resolution(case["artifacts"], case["work_orders"]),
                )

    def test_script_implementation_matches_every_vector(self) -> None:
        for case in VECTORS["cases"]:
            with self.subTest(case=case["name"], implementation="candidate-validator"):
                self.assertEqual(
                    case["expected"],
                    script_resolution(case["artifacts"], case["work_orders"]),
                )

    def test_every_specification_rule_with_a_vector_is_covered(self) -> None:
        # Rules 6, 9 and 10 are not resolution rules. 6 and 10 constrain the emitted
        # diagnostic and are covered by DiagnosticSurfaceTests; 9 is the agreement the
        # two vector tests above assert.
        self.assertEqual(
            {"1", "2", "3", "4", "5", "7", "8"},
            {case["rule"] for case in VECTORS["cases"]},
        )

    def test_every_stable_reason_has_a_vector(self) -> None:
        reasons = {
            defect["reason"]
            for case in VECTORS["cases"]
            for defect in case["expected"]["defects"]
        }
        self.assertEqual(
            {
                PACKAGE.REASON_DECLARATION_SHAPE,
                PACKAGE.REASON_DECLARATION_SIZE,
                PACKAGE.REASON_NO_APPROVAL,
                PACKAGE.REASON_INVALID_ID,
                PACKAGE.REASON_UNKNOWN_ARCHITECTURE,
                PACKAGE.REASON_AMBIGUOUS_ARCHITECTURE,
                PACKAGE.REASON_NOT_ARCHITECTURE,
                PACKAGE.REASON_ALREADY_ASSESSED,
            },
            reasons,
        )

    def test_one_semantics_means_one_vocabulary(self) -> None:
        """DLC-GEN-009: the two implementations agree constant by constant."""

        pairs = (
            ("SELF_HOSTING_COMPATIBILITY_SET", "ARCHITECTURES_WITHOUT_DECISION_ASSESSMENT"),
            ("SELF_HOSTING_DECLARER", "SELF_HOSTING_DECLARER"),
            ("DECLARATION_SCHEMA", "DEFINITION_GENERATION_SCHEMA"),
            ("DECLARATION_SCOPE", "DEFINITION_GENERATION_SCOPE"),
            ("DECLARATION_PACKET", "DEFINITION_GENERATION_PACKET"),
            ("DECLARATION_FIELD", "GENERATION_EXEMPTION_DECLARATION_FIELD"),
            ("MAX_DECLARED_ARCHITECTURES", "MAX_DECLARED_GENERATION_EXEMPTIONS"),
            ("REASON_DECLARATION_SHAPE", "GENERATION_REASON_DECLARATION_SHAPE"),
            ("REASON_DECLARATION_SIZE", "GENERATION_REASON_DECLARATION_SIZE"),
            ("REASON_NO_APPROVAL", "GENERATION_REASON_NO_APPROVAL"),
            ("REASON_INVALID_ID", "GENERATION_REASON_INVALID_ID"),
            ("REASON_UNKNOWN_ARCHITECTURE", "GENERATION_REASON_UNKNOWN_ARCHITECTURE"),
            ("REASON_AMBIGUOUS_ARCHITECTURE", "GENERATION_REASON_AMBIGUOUS_ARCHITECTURE"),
            ("REASON_NOT_ARCHITECTURE", "GENERATION_REASON_NOT_ARCHITECTURE"),
            ("REASON_ALREADY_ASSESSED", "GENERATION_REASON_ALREADY_ASSESSED"),
        )
        for package_name, script_name in pairs:
            with self.subTest(constant=package_name):
                self.assertEqual(
                    getattr(PACKAGE, package_name),
                    getattr(CANDIDATE_VALIDATOR, script_name),
                )

    def test_the_declarer_name_is_not_a_work_order_identifier(self) -> None:
        self.assertEqual("self-hosting-compatibility-set", PACKAGE.SELF_HOSTING_DECLARER)
        self.assertIsNone(
            PACKAGE.ARCHITECTURE_PATTERN.fullmatch(PACKAGE.SELF_HOSTING_DECLARER)
        )


class FrozenSetTests(unittest.TestCase):
    """DLC-GEN-001: one closed set of fourteen, measured rather than asserted."""

    def test_the_set_is_a_frozenset_of_fourteen_identifiers(self) -> None:
        self.assertIsInstance(PACKAGE.SELF_HOSTING_COMPATIBILITY_SET, frozenset)
        self.assertIsInstance(
            CANDIDATE_VALIDATOR.ARCHITECTURES_WITHOUT_DECISION_ASSESSMENT, frozenset
        )
        self.assertEqual(14, len(PACKAGE.SELF_HOSTING_COMPATIBILITY_SET))

    def test_every_member_matches_the_architecture_pattern(self) -> None:
        for identifier in sorted(PACKAGE.SELF_HOSTING_COMPATIBILITY_SET):
            with self.subTest(identifier=identifier):
                self.assertIsNotNone(PACKAGE.ARCHITECTURE_PATTERN.fullmatch(identifier))

    def test_the_generating_measurement_reproduces_the_committed_constant(self) -> None:
        """The membership is measured. Running the measurement must still yield it.

        The measurement's criterion is the removed proxy's own - unassessed and
        completed - so this is the one comparison that can tell a hand-edited constant
        from a measured one.
        """

        measured = MEASUREMENT.measure(REPOSITORY_ROOT)
        self.assertEqual(
            sorted(PACKAGE.SELF_HOSTING_COMPATIBILITY_SET),
            measured["architectures_without_decision_assessment"],
        )

    def test_the_committed_evidence_is_the_measurement_output(self) -> None:
        committed = json.loads(MEASUREMENT_EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual(MEASUREMENT.SCHEMA, committed["schema"])
        self.assertEqual("SPEC-DLC-001", committed["specification"])
        self.assertEqual(MEASUREMENT.measure(REPOSITORY_ROOT), committed)

    def test_no_architecture_is_left_needing_an_exemption_the_set_cannot_give(self) -> None:
        """The closure argument: every unassessed architecture is already a member.

        If this ever fails, an architecture was authored without an assessment and the
        closed set cannot cover it. The remedy is a declaration, never a new member.
        """

        measured = MEASUREMENT.measure(REPOSITORY_ROOT)
        self.assertEqual([], measured["unassessed_with_an_ongoing_status"])

    def test_this_repository_resolves_to_the_frozen_set_and_nothing_else(self) -> None:
        resolution = PACKAGE.resolve_repository(REPOSITORY_ROOT)
        self.assertEqual(
            {
                identifier: PACKAGE.SELF_HOSTING_DECLARER
                for identifier in sorted(PACKAGE.SELF_HOSTING_COMPATIBILITY_SET)
            },
            dict(resolution.exemptions),
        )
        self.assertEqual((), resolution.defects)
        self.assertEqual((), resolution.enforced)

    def test_removing_one_member_leaves_exactly_that_one_enforcing(self) -> None:
        """The per-identifier ablation: each member carries its own exemption."""

        artifacts, work_orders = PACKAGE._views(REPOSITORY_ROOT)
        for identifier in sorted(PACKAGE.SELF_HOSTING_COMPATIBILITY_SET):
            with self.subTest(identifier=identifier):
                reduced = PACKAGE.SELF_HOSTING_COMPATIBILITY_SET - {identifier}
                with mock.patch.object(PACKAGE, "SELF_HOSTING_COMPATIBILITY_SET", reduced):
                    resolution = PACKAGE.resolve(artifacts, work_orders)
                self.assertEqual((identifier,), resolution.enforced)
                self.assertNotIn(identifier, resolution.exemptions)


class StatusIndependenceTests(unittest.TestCase):
    """DLC-GEN-005: no code path in this assessment reads an architecture's status."""

    def test_the_removed_constant_is_absent_from_the_candidate_template(self) -> None:
        text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
        self.assertNotIn("LEGACY_ARCHITECTURE_STATUSES", text)

    def test_the_package_resolver_names_no_completed_status(self) -> None:
        source = (REPOSITORY_ROOT / "se_harness/definition_generation.py").read_text(
            encoding="utf-8"
        )
        for status in ("implemented", "verified", "released"):
            with self.subTest(status=status):
                self.assertNotIn(f'"{status}"', source)

    def test_resolution_ignores_a_status_carried_on_the_artifact_view(self) -> None:
        for status in ("draft", "approved", "in_progress", "implemented", "verified", "released"):
            with self.subTest(status=status):
                artifacts = [
                    {"id": "ARCH-XYZ-001", "type": "architecture", "assessed": False, "status": status}
                ]
                expected = {"exemptions": {}, "defects": [], "enforced": ["ARCH-XYZ-001"]}
                self.assertEqual(expected, package_resolution(artifacts, []))
                self.assertEqual(expected, script_resolution(artifacts, []))

    def test_a_declared_exemption_holds_at_every_status(self) -> None:
        for status in ("draft", "approved", "in_progress", "implemented", "verified", "released"):
            with self.subTest(status=status):
                artifacts = [
                    {"id": "ARCH-XYZ-001", "type": "architecture", "assessed": False, "status": status}
                ]
                work_orders = [
                    {
                        "id": "WO-CON-001",
                        "approved": True,
                        PACKAGE.DECLARATION_PACKET: {
                            "schema": PACKAGE.DECLARATION_SCHEMA,
                            "scope": PACKAGE.DECLARATION_SCOPE,
                            PACKAGE.DECLARATION_FIELD: ["ARCH-XYZ-001"],
                        },
                    }
                ]
                expected = {
                    "exemptions": {"ARCH-XYZ-001": "WO-CON-001"},
                    "defects": [],
                    "enforced": [],
                }
                self.assertEqual(expected, package_resolution(artifacts, work_orders))
                self.assertEqual(expected, script_resolution(artifacts, work_orders))

    def test_a_frozen_member_is_exempt_at_every_status_and_a_stranger_at_none(self) -> None:
        for status in ("draft", "approved", "in_progress", "implemented", "verified", "released"):
            for identifier, expected in (
                ("ARCH-REV-001", "legacy_missing"),
                ("ARCH-NOPE-001", "missing"),
            ):
                with self.subTest(status=status, identifier=identifier):
                    state = CANDIDATE_VALIDATOR.decision_assessment_state(
                        architecture_artifact(identifier, status)
                    )
                    self.assertEqual(expected, state["state"])

    def test_a_declared_exemption_reaches_decision_assessment_state(self) -> None:
        state = CANDIDATE_VALIDATOR.decision_assessment_state(
            architecture_artifact("ARCH-NOPE-001", "draft"), {"ARCH-NOPE-001": "WO-CON-001"}
        )
        self.assertEqual("legacy_missing", state["state"])
        self.assertEqual("WO-CON-001", state["exempt_source"])
        self.assertEqual([], state["issues"])

    def test_omitting_the_mapping_withholds_declarations_and_fails_closed(self) -> None:
        state = CANDIDATE_VALIDATOR.decision_assessment_state(
            architecture_artifact("ARCH-NOPE-001", "implemented")
        )
        self.assertEqual("missing", state["state"])
        self.assertIsNone(state["exempt_source"])
        self.assertEqual(["architecture decision assessment is required"], state["issues"])

    def test_an_assessed_architecture_reports_no_exempt_source(self) -> None:
        state = CANDIDATE_VALIDATOR.decision_assessment_state(
            architecture_artifact("ARCH-REV-001", "implemented", assessed=True)
        )
        self.assertNotEqual("legacy_missing", state["state"])
        self.assertIsNone(state["exempt_source"])


class DiagnosticSurfaceTests(unittest.TestCase):
    """DLC-GEN-006 and DLC-GEN-010: the diagnostic always fires, and names no status."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.report = CANDIDATE_VALIDATOR.validate_repository(REPOSITORY_ROOT)

    def w014(self) -> list:
        return [item for item in self.report.warnings if item.code == "W014"]

    def test_one_warning_is_emitted_for_every_exempt_architecture(self) -> None:
        warned = {Path(item.path).stem for item in self.w014()}
        self.assertEqual(set(PACKAGE.SELF_HOSTING_COMPATIBILITY_SET), warned)
        self.assertEqual(len(PACKAGE.SELF_HOSTING_COMPATIBILITY_SET), len(self.w014()))

    def test_the_exemption_suppresses_the_error_and_never_the_warning(self) -> None:
        self.assertEqual([], [item for item in self.report.errors if item.code == "E014"])
        self.assertNotEqual([], self.w014())

    def test_the_warning_names_the_declared_source_and_no_lifecycle_status(self) -> None:
        for item in self.w014():
            with self.subTest(path=item.path):
                self.assertEqual("maintenance", item.plane)
                self.assertIn("exempt through", item.message)
                self.assertIn(PACKAGE.SELF_HOSTING_DECLARER, item.message)
                self.assertIn("the assessment remains outstanding", item.message)
                for status in ("implemented", "verified", "released"):
                    self.assertNotIn(status, item.message)
                self.assertNotIn("compatibility window", item.message)

    def test_the_declarer_of_an_exemption_appears_in_its_warning(self) -> None:
        """A declaration-sourced exemption names the work order, not the frozen set."""

        artifacts = [
            architecture_artifact("ARCH-NOPE-001", "draft"),
            CANDIDATE_VALIDATOR.Artifact(
                path=Path("docs/engineering/sample/work-orders/WO-CON-001.md"),
                metadata={
                    "id": "WO-CON-001",
                    "type": "work_order",
                    "status": "approved",
                    PACKAGE.DECLARATION_PACKET: {
                        "schema": PACKAGE.DECLARATION_SCHEMA,
                        "scope": PACKAGE.DECLARATION_SCOPE,
                        PACKAGE.DECLARATION_FIELD: ["ARCH-NOPE-001"],
                    },
                    "lifecycle_events": [
                        {
                            "from": "draft",
                            "to": "approved",
                            "decided_at": "2026-08-24T10:44:00Z",
                            "decided_by": "repository-owner",
                        }
                    ],
                },
                body="",
            ),
        ]
        state = CANDIDATE_VALIDATOR.definition_generation_state(artifacts)
        self.assertEqual({"ARCH-NOPE-001": "WO-CON-001"}, state["exemptions"])
        self.assertEqual([], state["defects"])

    def test_a_declaration_defect_is_reported_on_the_declaring_work_order(self) -> None:
        artifacts = [
            CANDIDATE_VALIDATOR.Artifact(
                path=Path("docs/engineering/sample/work-orders/WO-CON-001.md"),
                metadata={
                    "id": "WO-CON-001",
                    "type": "work_order",
                    "status": "approved",
                    PACKAGE.DECLARATION_PACKET: {
                        "schema": PACKAGE.DECLARATION_SCHEMA,
                        "scope": PACKAGE.DECLARATION_SCOPE,
                        PACKAGE.DECLARATION_FIELD: ["ARCH-GHOST-001"],
                    },
                    "lifecycle_events": [
                        {
                            "from": "draft",
                            "to": "approved",
                            "decided_at": "2026-08-24T10:44:00Z",
                            "decided_by": "repository-owner",
                        }
                    ],
                },
                body="",
            )
        ]
        errors, warnings = CANDIDATE_VALIDATOR.validate_decision_assessments(
            artifacts, REPOSITORY_ROOT
        )
        self.assertEqual([], warnings)
        selected = [
            error for error in errors if PACKAGE.DECLARATION_FIELD in error.message
        ]
        self.assertEqual(1, len(selected))
        self.assertEqual("E012", selected[0].code)
        self.assertEqual("governance", selected[0].plane)
        self.assertIn("ARCH-GHOST-001", selected[0].message)
        self.assertIn(PACKAGE.REASON_UNKNOWN_ARCHITECTURE, selected[0].message)
        self.assertIn("WO-CON-001.md", selected[0].path.replace("\\", "/"))

    def test_no_declaration_field_turns_the_warning_off(self) -> None:
        """DLC-GEN-006: there is no suppression input. An extra key changes nothing."""

        artifacts = [{"id": "ARCH-NEW-001", "type": "architecture", "assessed": False}]
        work_orders = [
            {
                "id": "WO-CON-001",
                "approved": True,
                PACKAGE.DECLARATION_PACKET: {
                    "schema": PACKAGE.DECLARATION_SCHEMA,
                    "scope": PACKAGE.DECLARATION_SCOPE,
                    PACKAGE.DECLARATION_FIELD: ["ARCH-NEW-001"],
                    "suppress_warning": True,
                },
            }
        ]
        expected = {
            "exemptions": {"ARCH-NEW-001": "WO-CON-001"},
            "defects": [],
            "enforced": [],
        }
        self.assertEqual(expected, package_resolution(artifacts, work_orders))
        self.assertEqual(expected, script_resolution(artifacts, work_orders))


class RepositoryResolutionTests(unittest.TestCase):
    """DLC-GEN-008: an unassessable tree fails closed rather than reading as empty."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def architecture(self, identifier: str, *, assessed: bool = False) -> None:
        assessment = ""
        if assessed:
            assessment = (
                "\n[decision_assessment]\n"
                'outcome = "no_significant_decision"\n'
                "triggers = []\n"
                'rationale = "The fixture applies the existing architecture."\n'
                'assessed_by = "technical-owner"\n'
            )
        self.write(
            f"docs/engineering/sample/architecture/{identifier}.md",
            "+++\n"
            f'id = "{identifier}"\n'
            'type = "architecture"\n'
            'status = "approved"\n'
            f"{assessment}"
            "+++\n\n"
            f"# {identifier}\n",
        )

    def work_order(self, members: list[str], *, decided: bool = True) -> None:
        rendered = ", ".join(f'"{member}"' for member in members)
        events = ""
        if decided:
            events = (
                "\n[[lifecycle_events]]\n"
                'from = "draft"\n'
                'to = "approved"\n'
                'decided_at = "2026-08-24T10:44:00Z"\n'
                'decided_by = "repository-owner"\n'
            )
        self.write(
            "docs/engineering/sample/work-orders/WO-CON-001.md",
            "+++\n"
            'id = "WO-CON-001"\n'
            'type = "work_order"\n'
            'status = "approved"\n'
            f"\n[{PACKAGE.DECLARATION_PACKET}]\n"
            f'schema = "{PACKAGE.DECLARATION_SCHEMA}"\n'
            f'scope = "{PACKAGE.DECLARATION_SCOPE}"\n'
            f"{PACKAGE.DECLARATION_FIELD} = [{rendered}]\n"
            f"{events}"
            "+++\n\n"
            "# WO-CON-001\n",
        )

    def test_a_declared_architecture_resolves_from_artifact_files(self) -> None:
        self.architecture("ARCH-CON-001")
        self.work_order(["ARCH-CON-001"])
        resolution = PACKAGE.resolve_repository(self.root)
        self.assertEqual({"ARCH-CON-001": "WO-CON-001"}, dict(resolution.exemptions))
        self.assertEqual((), resolution.defects)
        self.assertEqual((), PACKAGE.enforcing_architectures(self.root))

    def test_an_undeclared_architecture_is_left_enforcing(self) -> None:
        self.architecture("ARCH-CON-001")
        self.assertEqual(("ARCH-CON-001",), PACKAGE.enforcing_architectures(self.root))

    def test_an_undecided_declarer_declares_nothing(self) -> None:
        self.architecture("ARCH-CON-001")
        self.work_order(["ARCH-CON-001"], decided=False)
        resolution = PACKAGE.resolve_repository(self.root)
        self.assertEqual({}, dict(resolution.exemptions))
        self.assertEqual(
            [
                {
                    "work_order": "WO-CON-001",
                    "architecture": None,
                    "reason": PACKAGE.REASON_NO_APPROVAL,
                }
            ],
            [defect.as_dict() for defect in resolution.defects],
        )
        self.assertEqual(("ARCH-CON-001",), resolution.enforced)

    def test_an_assessed_architecture_needs_no_exemption(self) -> None:
        self.architecture("ARCH-CON-001", assessed=True)
        resolution = PACKAGE.resolve_repository(self.root)
        self.assertEqual({}, dict(resolution.exemptions))
        self.assertEqual((), resolution.enforced)

    def test_evidence_and_template_trees_are_not_governed_artifacts(self) -> None:
        for excluded in ("evidence", "templates"):
            self.write(
                f"docs/engineering/{excluded}/ARCH-CON-002.md",
                "+++\n"
                'id = "ARCH-CON-002"\n'
                'type = "architecture"\n'
                'status = "approved"\n'
                "+++\n\n# excluded\n",
            )
        self.assertEqual((), PACKAGE.enforcing_architectures(self.root))

    def test_a_tree_without_governed_artifacts_resolves_empty(self) -> None:
        resolution = PACKAGE.resolve_repository(self.root / "absent")
        self.assertEqual({}, dict(resolution.exemptions))
        self.assertEqual((), resolution.defects)
        self.assertEqual((), resolution.enforced)

    def test_a_file_without_front_matter_is_skipped(self) -> None:
        self.write("docs/engineering/sample/notes.md", "# ordinary prose\n")
        self.assertEqual((), PACKAGE.enforcing_architectures(self.root))

    def test_an_unparsable_artifact_fails_closed(self) -> None:
        self.architecture("ARCH-CON-001")
        self.write(
            "docs/engineering/sample/work-orders/WO-CON-001.md",
            '+++\nid = \nstatus "broken"\n+++\n\n# broken\n',
        )
        with self.assertRaises(PACKAGE.DefinitionGenerationError):
            PACKAGE.resolve_repository(self.root)

    def test_an_oversized_artifact_fails_closed(self) -> None:
        self.architecture("ARCH-CON-001")
        filler = "x" * (PACKAGE.MAX_ARTIFACT_BYTES + 1)
        self.write("docs/engineering/sample/work-orders/WO-CON-001.md", f"+++\n+++\n\n{filler}\n")
        with self.assertRaises(PACKAGE.DefinitionGenerationError):
            PACKAGE.resolve_repository(self.root)


class MigrationSurfaceTests(unittest.TestCase):
    """What a consumer repository sees across the version pair this increment lands in.

    The increment removes an exemption a consumer may be relying on today, and the
    governance-migration contract cannot express that: its capability vocabulary is a
    closed set of eight names, all of which the predecessor already holds in full, so
    the pair classifies compatible whatever this increment does. These tests stand in
    for the boundary the contract cannot declare - they pin the forward-compatible
    migration path instead, which is what actually protects a consumer.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(
            (REPOSITORY_ROOT / "se_harness/governance_migration_contract.json").read_text(
                encoding="utf-8"
            )
        )
        cls.scenario = json.loads(
            (
                REPOSITORY_ROOT
                / "tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.0.json"
            ).read_text(encoding="utf-8")
        )

    def test_the_capability_vocabulary_names_nothing_this_increment_adds(self) -> None:
        """The scope item's real answer: there is no capability name to declare.

        If a later increment does need one, this assertion fails and the missing name
        has to be added to the migration contract under a work order that owns it.
        """

        self.assertEqual(
            {
                "complete-graph-validation",
                "evaluator-evidence-v1",
                "predecessor-compatible-assessment-view",
                "predecessor-compatible-preparation-view",
                "predecessor-compatible-publication-view",
                "rejected-record-terminal-state",
                "schema-v2-release-preparation",
                "separate-root-adoption",
            },
            set(self.contract["capabilities"]),
        )

    def test_the_pair_for_this_increment_classifies_compatible(self) -> None:
        capabilities = self.scenario["capabilities"]
        self.assertEqual(
            sorted(capabilities["predecessor"]), sorted(capabilities["successor_required"])
        )
        self.assertEqual("0.6.0", self.scenario["versions"]["predecessor"])
        self.assertEqual("0.7.0", self.scenario["versions"]["successor"])

    def test_the_declaration_packet_is_additive_for_the_predecessor(self) -> None:
        """The migration path: declare first on the predecessor, then upgrade.

        The predecessor accepts a work order carrying the packet because no closed
        field set covers a top-level artifact table. That is what lets a consumer add
        the declaration before upgrading rather than after breaking.
        """

        released = load_module(
            "definition_generation_released_validator",
            REPOSITORY_ROOT / "scripts/validate_engineering_artifacts.py",
        )
        metadata = {
            "id": "WO-CON-001",
            "type": "work_order",
            "title": "WO-CON-001 title",
            "status": "approved",
            "owners": ["engineering-owner"],
            "created": "2026-08-26",
            "updated": "2026-08-26",
            "assurance": {
                "commit_bound_verification": "not_required",
                "rationale": "The fixture records an already authorized declaration.",
                "decided_by": "engineering-owner",
            },
            "relations": {"implements": ["REQ-CON-001"]},
        }
        without = released.Artifact(
            path=Path("docs/engineering/sample/work-orders/WO-CON-001.md"),
            metadata=dict(metadata),
            body="",
        )
        declared = dict(metadata)
        declared[PACKAGE.DECLARATION_PACKET] = {
            "schema": PACKAGE.DECLARATION_SCHEMA,
            "scope": PACKAGE.DECLARATION_SCOPE,
            PACKAGE.DECLARATION_FIELD: ["ARCH-CON-001"],
        }
        with_packet = released.Artifact(
            path=Path("docs/engineering/sample/work-orders/WO-CON-001.md"),
            metadata=declared,
            body="",
        )
        baseline = released.validate_type_specific_metadata([without], REPOSITORY_ROOT)
        after = released.validate_type_specific_metadata([with_packet], REPOSITORY_ROOT)
        self.assertEqual(
            [(item.code, item.message) for item in baseline],
            [(item.code, item.message) for item in after],
        )
        self.assertEqual(
            [],
            [item for item in after if PACKAGE.DECLARATION_PACKET in item.message],
        )


class DeclarationCorpusTests(unittest.TestCase):
    """The two corpus cases the committed vector fixture is the wrong size to carry."""

    def test_two_approved_maximal_declarations_resolve_together(self) -> None:
        """The bound is per declaration, so two approved declarers resolve 1024 entries."""

        first = [f"ARCH-AAA-{index:03d}" for index in range(PACKAGE.MAX_DECLARED_ARCHITECTURES)]
        second = [f"ARCH-BBB-{index:03d}" for index in range(PACKAGE.MAX_DECLARED_ARCHITECTURES)]
        artifacts = [
            {"id": identifier, "type": "architecture", "assessed": False}
            for identifier in first + second
        ]
        work_orders = [
            {
                "id": declarer,
                "approved": True,
                PACKAGE.DECLARATION_PACKET: {
                    "schema": PACKAGE.DECLARATION_SCHEMA,
                    "scope": PACKAGE.DECLARATION_SCOPE,
                    PACKAGE.DECLARATION_FIELD: members,
                },
            }
            for declarer, members in (("WO-CON-001", first), ("WO-CON-002", second))
        ]
        expected = {identifier: "WO-CON-001" for identifier in first}
        expected.update({identifier: "WO-CON-002" for identifier in second})
        for label, resolve in (("package", package_resolution), ("script", script_resolution)):
            with self.subTest(implementation=label):
                resolution = resolve(artifacts, work_orders)
                self.assertEqual(expected, resolution["exemptions"])
                self.assertEqual([], resolution["defects"])
                self.assertEqual([], resolution["enforced"])

    def test_a_duplicate_key_declaration_fails_closed(self) -> None:
        """DLC-GEN-008 names duplicate keys; TOML refuses them before resolution begins."""

        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        architecture = root / "docs/engineering/sample/architecture/ARCH-CON-001.md"
        architecture.parent.mkdir(parents=True, exist_ok=True)
        architecture.write_text(
            "+++\n"
            'id = "ARCH-CON-001"\n'
            'type = "architecture"\n'
            'status = "approved"\n'
            "+++\n\n# ARCH-CON-001\n",
            encoding="utf-8",
            newline="\n",
        )
        declarer = root / "docs/engineering/sample/work-orders/WO-CON-001.md"
        declarer.parent.mkdir(parents=True, exist_ok=True)
        declarer.write_text(
            "+++\n"
            'id = "WO-CON-001"\n'
            'type = "work_order"\n'
            'status = "approved"\n'
            f"\n[{PACKAGE.DECLARATION_PACKET}]\n"
            f'schema = "{PACKAGE.DECLARATION_SCHEMA}"\n'
            f'scope = "{PACKAGE.DECLARATION_SCOPE}"\n'
            f'{PACKAGE.DECLARATION_FIELD} = ["ARCH-CON-001"]\n'
            f'{PACKAGE.DECLARATION_FIELD} = ["ARCH-CON-001"]\n'
            "+++\n\n# WO-CON-001\n",
            encoding="utf-8",
            newline="\n",
        )
        with self.assertRaises(PACKAGE.DefinitionGenerationError):
            PACKAGE.resolve_repository(root)


if __name__ == "__main__":  # pragma: no cover - direct execution convenience
    unittest.main()
