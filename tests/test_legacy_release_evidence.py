"""Verification for SPEC-LRE-001: declared pre-enforcement release exemptions.

`VER-LRE-001` requires that one semantics is implemented twice - once in
`se_harness/legacy_release_evidence.py` for the package and once, self-contained, in
the candidate validator script - and that the two agree. Every vector in
`tests/fixtures/legacy_release_evidence/resolution_vectors.json` is resolved by both.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from se_harness import legacy_release_evidence as PACKAGE
from se_harness.evaluator_identity import PAYLOAD_MANIFEST, InstalledEvaluatorIdentity
from se_harness.hash_bound import MATCH_DECLARED
from se_harness.installer import HarnessError, apply_changes, plan_install
from se_harness.workflow_contract import load_lifecycle_registry
from tests.mutation_guard_support import trusted_mutation_authority


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = REPOSITORY_ROOT / "tests/fixtures/legacy_release_evidence/resolution_vectors.json"


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load test module: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


CANDIDATE_VALIDATOR = load_module(
    "legacy_release_evidence_candidate_validator",
    REPOSITORY_ROOT / "templates/repository/standard/scripts/validate_engineering_artifacts.py",
)
PUBLICATION = load_module(
    "legacy_release_evidence_publication",
    REPOSITORY_ROOT / ".github/scripts/publish_dashboard.py",
)

VECTORS = json.loads(VECTOR_PATH.read_text(encoding="utf-8"))
PACKET_HEAD = {
    "schema": PACKAGE.UPGRADE_AUTHORIZATION_SCHEMA,
    "scope": PACKAGE.UPGRADE_AUTHORIZATION_SCOPE,
}


def package_resolution(records: list[dict], work_orders: list[dict]) -> dict:
    return PACKAGE.resolve(records, work_orders).as_dict()


def script_resolution(records: list[dict], work_orders: list[dict]) -> dict:
    return CANDIDATE_VALIDATOR.resolve_legacy_release_evidence(records, work_orders)


def released_record(identifier: str, released_at: str = "2026-06-01T00:00:00Z") -> dict:
    return {
        "id": identifier,
        "status": "released",
        "released_at": released_at,
        "path_present": False,
        "digest_present": False,
    }


def declaring_work_order(
    members: object,
    *,
    identifier: str = "WO-CON-001",
    status: str = "approved",
    approved_at: str = "2026-08-24T10:44:00Z",
) -> dict:
    packet = dict(PACKET_HEAD)
    packet[PACKAGE.DECLARATION_FIELD] = members
    return {
        "id": identifier,
        "status": status,
        "approved_at": approved_at,
        "evaluator_upgrade": packet,
    }


class ResolutionVectorTests(unittest.TestCase):
    """Both implementations return the committed result for every vector."""

    def test_fixture_declares_its_own_schema_and_specification(self) -> None:
        self.assertEqual("se-harness-legacy-release-evidence-vectors-v1", VECTORS["schema"])
        self.assertEqual("SPEC-LRE-001", VECTORS["specification"])
        names = [case["name"] for case in VECTORS["cases"]]
        self.assertEqual(sorted(set(names)), sorted(names))
        self.assertGreaterEqual(len(names), 20)

    def test_package_implementation_matches_every_vector(self) -> None:
        for case in VECTORS["cases"]:
            with self.subTest(case=case["name"], implementation="package"):
                self.assertEqual(
                    case["expected"],
                    package_resolution(case["records"], case["work_orders"]),
                )

    def test_script_implementation_matches_every_vector(self) -> None:
        for case in VECTORS["cases"]:
            with self.subTest(case=case["name"], implementation="candidate-validator"):
                self.assertEqual(
                    case["expected"],
                    script_resolution(case["records"], case["work_orders"]),
                )

    def test_every_specification_rule_with_a_vector_is_covered(self) -> None:
        covered = {case["rule"] for case in VECTORS["cases"]}
        self.assertEqual(
            {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"},
            covered,
        )


class AuthorityMatrixTests(unittest.TestCase):
    """SPEC-LRE-001 rule 3: only an authority-granting work-order state declares."""

    def setUp(self) -> None:
        self.states = sorted(load_lifecycle_registry()["work_order"])
        self.granting = PACKAGE.authority_granting_work_order_statuses()

    def test_the_lifecycle_registry_declares_the_expected_states(self) -> None:
        self.assertEqual(
            {"approved", "in_progress", "implemented", "verified", "released"},
            set(self.granting),
        )
        self.assertEqual(
            {"draft", "ready", "superseded", "rejected"},
            set(self.states) - set(self.granting),
        )

    def test_both_implementations_read_the_same_authority_set(self) -> None:
        script = {
            state
            for state, row in CANDIDATE_VALIDATOR.WORKFLOW_LIFECYCLES["work_order"].items()
            if row.grants_authority
        }
        self.assertEqual(set(self.granting), script)

    def test_exemption_follows_authority_across_every_declared_state(self) -> None:
        for state in self.states:
            with self.subTest(state=state):
                records = [released_record("RLS-CON-001")]
                work_orders = [declaring_work_order(["RLS-CON-001"], status=state)]
                expected_exemptions = (
                    {"RLS-CON-001": "WO-CON-001"} if state in self.granting else {}
                )
                expected = {
                    "exemptions": expected_exemptions,
                    "defects": [],
                    "undeclared": [] if expected_exemptions else ["RLS-CON-001"],
                }
                self.assertEqual(expected, package_resolution(records, work_orders))
                self.assertEqual(expected, script_resolution(records, work_orders))

    def test_an_unknown_state_never_grants(self) -> None:
        records = [released_record("RLS-CON-001")]
        work_orders = [declaring_work_order(["RLS-CON-001"], status="invented")]
        expected = {"exemptions": {}, "defects": [], "undeclared": ["RLS-CON-001"]}
        self.assertEqual(expected, package_resolution(records, work_orders))
        self.assertEqual(expected, script_resolution(records, work_orders))


class DeclarationBoundTests(unittest.TestCase):
    """SPEC-LRE-001 rule 1: the declaration is bounded at 512 entries."""

    def members(self, count: int) -> list[str]:
        return [f"RLS-CON-{index:03d}" for index in range(1, count + 1)]

    def test_the_bound_is_the_same_in_both_implementations(self) -> None:
        self.assertEqual(512, PACKAGE.MAX_DECLARED_RECORDS)
        self.assertEqual(512, CANDIDATE_VALIDATOR.MAX_DECLARED_LEGACY_RELEASES)

    def test_the_bound_is_accepted_and_resolves_member_by_member(self) -> None:
        work_orders = [declaring_work_order(self.members(512))]
        for resolution in (package_resolution([], work_orders), script_resolution([], work_orders)):
            self.assertEqual({}, resolution["exemptions"])
            self.assertEqual(512, len(resolution["defects"]))
            self.assertEqual(
                {PACKAGE.REASON_UNKNOWN_RECORD},
                {defect["reason"] for defect in resolution["defects"]},
            )

    def test_one_entry_beyond_the_bound_is_a_single_declaration_defect(self) -> None:
        work_orders = [declaring_work_order(self.members(513))]
        expected = {
            "exemptions": {},
            "defects": [
                {
                    "work_order": "WO-CON-001",
                    "record": None,
                    "reason": PACKAGE.REASON_DECLARATION_SIZE,
                }
            ],
            "undeclared": [],
        }
        self.assertEqual(expected, package_resolution([], work_orders))
        self.assertEqual(expected, script_resolution([], work_orders))


class ReasonTextTests(unittest.TestCase):
    """One semantics means one diagnostic vocabulary."""

    def test_both_implementations_carry_identical_reason_text(self) -> None:
        pairs = (
            ("REASON_DECLARATION_SHAPE", "LEGACY_REASON_DECLARATION_SHAPE"),
            ("REASON_DECLARATION_SIZE", "LEGACY_REASON_DECLARATION_SIZE"),
            ("REASON_NO_APPROVAL", "LEGACY_REASON_NO_APPROVAL"),
            ("REASON_INVALID_ID", "LEGACY_REASON_INVALID_ID"),
            ("REASON_UNKNOWN_RECORD", "LEGACY_REASON_UNKNOWN_RECORD"),
            ("REASON_AMBIGUOUS_RECORD", "LEGACY_REASON_AMBIGUOUS_RECORD"),
            ("REASON_NOT_RELEASED", "LEGACY_REASON_NOT_RELEASED"),
            ("REASON_ALREADY_BOUND", "LEGACY_REASON_ALREADY_BOUND"),
            ("REASON_NO_RELEASED_AT", "LEGACY_REASON_NO_RELEASED_AT"),
            ("REASON_NOT_YET_RELEASED", "LEGACY_REASON_NOT_YET_RELEASED"),
        )
        for package_name, script_name in pairs:
            with self.subTest(reason=package_name):
                self.assertEqual(
                    getattr(PACKAGE, package_name),
                    getattr(CANDIDATE_VALIDATOR, script_name),
                )

    def test_the_declaration_field_and_packet_identity_agree(self) -> None:
        self.assertEqual(
            PACKAGE.DECLARATION_FIELD,
            CANDIDATE_VALIDATOR.LEGACY_EVIDENCE_DECLARATION_FIELD,
        )
        self.assertEqual(
            PACKAGE.UPGRADE_AUTHORIZATION_SCHEMA,
            CANDIDATE_VALIDATOR.UPGRADE_AUTHORIZATION_SCHEMA,
        )
        self.assertEqual(
            PACKAGE.UPGRADE_AUTHORIZATION_SCOPE,
            CANDIDATE_VALIDATOR.UPGRADE_AUTHORIZATION_SCOPE,
        )


class SelfHostingCompatibilitySetTests(unittest.TestCase):
    """SPEC-LRE-001 rule 11: one frozen set, held identically by every reader."""

    expected = frozenset(
        {"RLS-SEH-001", "RLS-SEH-002", "RLS-SEH-004", "RLS-SEH-005", "RLS-SEH-006", "RLS-SEH-007"}
    )

    def test_every_holder_carries_the_same_frozen_set(self) -> None:
        self.assertEqual(self.expected, PACKAGE.SELF_HOSTING_COMPATIBILITY_SET)
        self.assertEqual(
            self.expected, CANDIDATE_VALIDATOR.LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE
        )
        self.assertEqual(self.expected, PUBLICATION.LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE)
        for holder in (
            PACKAGE.SELF_HOSTING_COMPATIBILITY_SET,
            CANDIDATE_VALIDATOR.LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE,
            PUBLICATION.LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE,
        ):
            self.assertIsInstance(holder, frozenset)

    def test_the_declarer_name_is_not_a_work_order_identifier(self) -> None:
        self.assertEqual("self-hosting-compatibility-set", PACKAGE.SELF_HOSTING_DECLARER)
        self.assertEqual(PACKAGE.SELF_HOSTING_DECLARER, CANDIDATE_VALIDATOR.SELF_HOSTING_DECLARER)
        self.assertIsNone(
            PACKAGE.RELEASE_RECORD_PATTERN.fullmatch(PACKAGE.SELF_HOSTING_DECLARER)
        )

    def test_the_publication_view_exempts_only_a_wholly_unbound_member(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            binding = PUBLICATION._validated_evaluator_binding(
                repository,
                "0" * 40,
                {"id": "RLS-SEH-001"},
            )
            self.assertEqual({"path": None, "sha256": None}, binding)
            with self.assertRaises(PUBLICATION.PublicationError):
                PUBLICATION._validated_evaluator_binding(
                    repository,
                    "0" * 40,
                    {"id": "RLS-SEH-001", "evaluator_evidence_path": "docs/engineering/x/evidence/e.json"},
                )
            with self.assertRaises(PUBLICATION.PublicationError):
                PUBLICATION._validated_evaluator_binding(
                    repository,
                    "0" * 40,
                    {"id": "RLS-SEH-003"},
                )


class RepositoryResolutionTests(unittest.TestCase):
    """Resolution from artifact files, including the fail-closed enumeration."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "docs/engineering").mkdir(parents=True)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def record_artifact(self, identifier: str, released_at: str = "2026-06-01T00:00:00Z") -> None:
        self.write(
            f"docs/engineering/sample/releases/{identifier}.md",
            "+++\n"
            f'id = "{identifier}"\n'
            'type = "release_record"\n'
            'status = "released"\n'
            f'released_at = "{released_at}"\n'
            "+++\n\n"
            f"# {identifier}\n",
        )

    def work_order_artifact(
        self,
        identifier: str,
        members: list[str],
        *,
        status: str = "approved",
        decided_at: str | None = "2026-08-24T10:44:00Z",
    ) -> None:
        rendered = ", ".join(f'"{member}"' for member in members)
        events = ""
        if decided_at is not None:
            events = (
                "\n[[lifecycle_events]]\n"
                'from = "draft"\n'
                'to = "approved"\n'
                f'decided_at = "{decided_at}"\n'
                'decided_by = "repository-owner"\n'
            )
        self.write(
            f"docs/engineering/sample/work-orders/{identifier}.md",
            "+++\n"
            f'id = "{identifier}"\n'
            'type = "work_order"\n'
            f'status = "{status}"\n'
            "\n[evaluator_upgrade]\n"
            f'schema = "{PACKAGE.UPGRADE_AUTHORIZATION_SCHEMA}"\n'
            f'scope = "{PACKAGE.UPGRADE_AUTHORIZATION_SCOPE}"\n'
            f"{PACKAGE.DECLARATION_FIELD} = [{rendered}]\n"
            f"{events}"
            "+++\n\n"
            f"# {identifier}\n",
        )

    def test_a_declared_record_resolves_from_artifact_files(self) -> None:
        self.record_artifact("RLS-CON-001")
        self.work_order_artifact("WO-CON-001", ["RLS-CON-001"])
        resolution = PACKAGE.resolve_repository(self.root)
        self.assertEqual({"RLS-CON-001": "WO-CON-001"}, dict(resolution.exemptions))
        self.assertEqual((), resolution.defects)
        self.assertEqual((), PACKAGE.undeclared_legacy_releases(self.root))

    def test_an_undeclared_record_is_reported(self) -> None:
        self.record_artifact("RLS-CON-001")
        self.assertEqual(("RLS-CON-001",), PACKAGE.undeclared_legacy_releases(self.root))

    def test_the_last_draft_to_approved_event_is_the_approval_instant(self) -> None:
        self.record_artifact("RLS-CON-001", released_at="2026-07-01T00:00:00Z")
        self.write(
            "docs/engineering/sample/work-orders/WO-CON-001.md",
            "+++\n"
            'id = "WO-CON-001"\n'
            'type = "work_order"\n'
            'status = "approved"\n'
            "\n[evaluator_upgrade]\n"
            f'schema = "{PACKAGE.UPGRADE_AUTHORIZATION_SCHEMA}"\n'
            f'scope = "{PACKAGE.UPGRADE_AUTHORIZATION_SCOPE}"\n'
            f'{PACKAGE.DECLARATION_FIELD} = ["RLS-CON-001"]\n'
            "\n[[lifecycle_events]]\n"
            'from = "draft"\n'
            'to = "approved"\n'
            'decided_at = "2026-06-01T00:00:00Z"\n'
            'decided_by = "repository-owner"\n'
            "\n[[lifecycle_events]]\n"
            'from = "draft"\n'
            'to = "approved"\n'
            'decided_at = "2026-08-01T00:00:00Z"\n'
            'decided_by = "repository-owner"\n'
            "+++\n\n"
            "# WO-CON-001\n",
        )
        resolution = PACKAGE.resolve_repository(self.root)
        self.assertEqual({"RLS-CON-001": "WO-CON-001"}, dict(resolution.exemptions))

    def test_an_undated_declarer_declares_nothing(self) -> None:
        self.record_artifact("RLS-CON-001")
        self.work_order_artifact("WO-CON-001", ["RLS-CON-001"], decided_at=None)
        resolution = PACKAGE.resolve_repository(self.root)
        self.assertEqual({}, dict(resolution.exemptions))
        self.assertEqual(
            [{"work_order": "WO-CON-001", "record": None, "reason": PACKAGE.REASON_NO_APPROVAL}],
            [defect.as_dict() for defect in resolution.defects],
        )

    def test_evidence_and_template_trees_are_not_governed_artifacts(self) -> None:
        self.record_artifact("RLS-CON-001")
        self.work_order_artifact("WO-CON-001", ["RLS-CON-001"])
        for excluded in ("evidence", "templates"):
            self.write(
                f"docs/engineering/{excluded}/RLS-CON-002.md",
                "+++\n"
                'id = "RLS-CON-002"\n'
                'type = "release_record"\n'
                'status = "released"\n'
                'released_at = "2026-06-01T00:00:00Z"\n'
                "+++\n\n# excluded\n",
            )
        self.assertEqual((), PACKAGE.undeclared_legacy_releases(self.root))

    def test_an_unparsable_artifact_fails_closed(self) -> None:
        self.record_artifact("RLS-CON-001")
        self.write(
            "docs/engineering/sample/work-orders/WO-CON-001.md",
            "+++\nid = \nstatus \"broken\"\n+++\n\n# broken\n",
        )
        with self.assertRaises(PACKAGE.LegacyReleaseEvidenceError):
            PACKAGE.resolve_repository(self.root)

    def test_an_oversized_artifact_fails_closed(self) -> None:
        self.record_artifact("RLS-CON-001")
        filler = "x" * (PACKAGE.MAX_ARTIFACT_BYTES + 1)
        self.write("docs/engineering/sample/work-orders/WO-CON-001.md", f"+++\n+++\n\n{filler}\n")
        with self.assertRaises(PACKAGE.LegacyReleaseEvidenceError):
            PACKAGE.resolve_repository(self.root)

    def test_a_tree_without_governed_artifacts_resolves_empty(self) -> None:
        resolution = PACKAGE.resolve_repository(self.root / "absent")
        self.assertEqual({}, dict(resolution.exemptions))
        self.assertEqual((), resolution.defects)
        self.assertEqual((), resolution.undeclared)

    def test_a_file_without_front_matter_is_skipped(self) -> None:
        self.write("docs/engineering/sample/notes.md", "# ordinary prose\n")
        self.assertEqual((), PACKAGE.undeclared_legacy_releases(self.root))

    def test_this_repository_resolves_to_the_frozen_self_hosting_set(self) -> None:
        resolution = PACKAGE.resolve_repository(REPOSITORY_ROOT)
        self.assertEqual(
            {
                identifier: PACKAGE.SELF_HOSTING_DECLARER
                for identifier in sorted(PACKAGE.SELF_HOSTING_COMPATIBILITY_SET)
            },
            dict(resolution.exemptions),
        )
        self.assertEqual((), resolution.defects)
        self.assertEqual((), resolution.undeclared)


class InstallerRefusalTests(unittest.TestCase):
    """REQ-LRE-002: refuse before the first write, never into a frozen repository."""

    def authority(self, declared: tuple[str, ...] = ()):
        """Authorize a transition onto the identity the installed root already carries.

        The refusal under test happens before the first write, so the transition's
        target is deliberately the observed identity: any postcondition failure would
        be a fixture defect rather than the behaviour being verified.
        """

        def factory(repository, **keywords):
            value = trusted_mutation_authority(repository, **keywords)
            lock_path = Path(repository) / ".engineering-harness.lock"
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            observed = lock["evaluator"]
            # SPEC-REB-012: no packet. The transition's target is the observed
            # identity itself; the legacy-release declaration is read from the
            # fixture's work order by the installer, not carried by the authority.
            value.transition = True
            value.target_identity = InstalledEvaluatorIdentity(
                version=observed["version"],
                payload_manifest=observed["payload_manifest"],
                payload_sha256=observed["payload_sha256"],
                archive_name=observed.get("archive_name"),
                archive_sha256=observed.get("archive_sha256"),
            )
            return value

        return factory

    def installed_root(self, temporary: str) -> Path:
        target = Path(temporary) / "repository"
        with mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=trusted_mutation_authority,
        ):
            changes, old_lock = plan_install(target, project_name="Fixture", mode="init")
            apply_changes(target, changes, old_lock, allow_updates=False)
        return target

    def write_record(self, target: Path, identifier: str) -> Path:
        path = target / f"docs/engineering/sample/releases/{identifier}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "+++\n"
            f'id = "{identifier}"\n'
            'type = "release_record"\n'
            'status = "released"\n'
            'released_at = "2026-06-01T00:00:00Z"\n'
            "+++\n\n"
            f"# {identifier}\n",
            encoding="utf-8",
            newline="\n",
        )
        return path

    def write_declaration(self, target: Path, members: list[str]) -> None:
        rendered = ", ".join(f'"{member}"' for member in members)
        path = target / "docs/engineering/sample/work-orders/WO-CON-001.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "+++\n"
            'id = "WO-CON-001"\n'
            'type = "work_order"\n'
            'status = "approved"\n'
            "\n[evaluator_upgrade]\n"
            f'schema = "{PACKAGE.UPGRADE_AUTHORIZATION_SCHEMA}"\n'
            f'scope = "{PACKAGE.UPGRADE_AUTHORIZATION_SCOPE}"\n'
            f"{PACKAGE.DECLARATION_FIELD} = [{rendered}]\n"
            "\n[[lifecycle_events]]\n"
            'from = "draft"\n'
            'to = "approved"\n'
            'decided_at = "2026-08-24T10:44:00Z"\n'
            'decided_by = "repository-owner"\n'
            "+++\n\n"
            "# WO-CON-001\n",
            encoding="utf-8",
            newline="\n",
        )

    def snapshot(self, target: Path) -> dict[str, bytes]:
        return {
            path.relative_to(target).as_posix(): path.read_bytes()
            for path in sorted(target.rglob("*"))
            if path.is_file()
        }

    def test_an_undeclared_released_record_refuses_the_transition(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.installed_root(temporary)
            record = self.write_record(target, "RLS-CON-001")
            before = self.snapshot(target)
            evidence = Path("docs/engineering/sample/evidence/WO-CON-001-evaluator-upgrade.json")
            with mock.patch(
                "se_harness.mutation_guard.require_mutation_authority",
                side_effect=self.authority(),
            ):
                changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
                with self.assertRaises(HarnessError) as raised:
                    apply_changes(
                        target,
                        changes,
                        old_lock,
                        allow_updates=True,
                        evidence_output=evidence,
                    )
            message = str(raised.exception)
            self.assertIn("RLS-CON-001", message)
            self.assertIn("no files were written", message)
            self.assertIn(PACKAGE.DECLARATION_FIELD, message)
            self.assertIn("an approved work order under [evaluator_upgrade]", message)
            self.assertEqual(before, self.snapshot(target))
            self.assertFalse((target / evidence).exists())
            self.assertTrue(record.is_file())

    def test_a_declared_record_lets_the_transition_proceed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.installed_root(temporary)
            self.write_record(target, "RLS-CON-001")
            self.write_declaration(target, ["RLS-CON-001"])
            evidence = Path("docs/engineering/sample/evidence/WO-CON-001-evaluator-upgrade.json")
            with mock.patch(
                "se_harness.mutation_guard.require_mutation_authority",
                side_effect=self.authority(("RLS-CON-001",)),
            ):
                changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
                apply_changes(
                    target,
                    changes,
                    old_lock,
                    allow_updates=True,
                    evidence_output=evidence,
                )
            written = json.loads((target / evidence).read_text(encoding="utf-8"))
            self.assertEqual(["RLS-CON-001"], written[PACKAGE.DECLARATION_FIELD])

    def test_an_unassessable_tree_refuses_the_transition(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.installed_root(temporary)
            broken = target / "docs/engineering/sample/work-orders/WO-CON-001.md"
            broken.parent.mkdir(parents=True, exist_ok=True)
            broken.write_text("+++\nid = \n+++\n", encoding="utf-8", newline="\n")
            before = self.snapshot(target)
            evidence = Path("docs/engineering/sample/evidence/WO-CON-001-evaluator-upgrade.json")
            with mock.patch(
                "se_harness.mutation_guard.require_mutation_authority",
                side_effect=self.authority(),
            ):
                changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
                with self.assertRaisesRegex(HarnessError, "cannot assess released records"):
                    apply_changes(
                        target,
                        changes,
                        old_lock,
                        allow_updates=True,
                        evidence_output=evidence,
                    )
            self.assertEqual(before, self.snapshot(target))

    def test_a_repository_without_released_records_is_unaffected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.installed_root(temporary)
            evidence = Path("docs/engineering/sample/evidence/WO-CON-001-evaluator-upgrade.json")
            with mock.patch(
                "se_harness.mutation_guard.require_mutation_authority",
                side_effect=self.authority(),
            ):
                changes, old_lock = plan_install(target, project_name=None, mode="upgrade")
                apply_changes(
                    target,
                    changes,
                    old_lock,
                    allow_updates=True,
                    evidence_output=evidence,
                )
            written = json.loads((target / evidence).read_text(encoding="utf-8"))
            self.assertNotIn(PACKAGE.DECLARATION_FIELD, written)


class ValidatorDiagnosticTests(unittest.TestCase):
    """The candidate validator exempts, warns, and refuses on the same declaration."""

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
        }
        metadata.update(overrides)
        return self.artifact(f"docs/engineering/sample/releases/{identifier}.md", metadata)

    def work_order(self, members: object, *, status: str = "approved", decided: bool = True):
        packet = dict(PACKET_HEAD)
        packet[PACKAGE.DECLARATION_FIELD] = members
        metadata = {
            "id": "WO-CON-001",
            "type": "work_order",
            "status": status,
            "evaluator_upgrade": packet,
        }
        if decided:
            metadata["lifecycle_events"] = [
                {
                    "from": "draft",
                    "to": "approved",
                    "decided_at": "2026-08-24T10:44:00Z",
                    "decided_by": "repository-owner",
                }
            ]
        return self.artifact("docs/engineering/sample/work-orders/WO-CON-001.md", metadata)

    def test_an_accepted_exemption_emits_exactly_one_maintenance_warning(self) -> None:
        artifacts = [self.record(), self.work_order(["RLS-CON-001"])]
        warnings = CANDIDATE_VALIDATOR.validate_legacy_release_evidence_warnings(
            artifacts, self.root
        )
        self.assertEqual(1, len(warnings))
        warning = warnings[0]
        self.assertEqual("W024", warning.code)
        self.assertEqual("maintenance", warning.plane)
        self.assertIn("RLS-CON-001", warning.message)
        self.assertIn("WO-CON-001", warning.message)
        self.assertIn("the binding remains outstanding", warning.message)

    def test_an_undeclared_record_raises_no_warning(self) -> None:
        warnings = CANDIDATE_VALIDATOR.validate_legacy_release_evidence_warnings(
            [self.record()], self.root
        )
        self.assertEqual([], warnings)

    def test_the_frozen_set_warns_like_a_declaration(self) -> None:
        warnings = CANDIDATE_VALIDATOR.validate_legacy_release_evidence_warnings(
            [self.record("RLS-SEH-001")], self.root
        )
        self.assertEqual(1, len(warnings))
        self.assertIn(PACKAGE.SELF_HOSTING_DECLARER, warnings[0].message)

    def test_an_unresolved_declaration_is_an_error_on_the_declarer(self) -> None:
        artifacts = [self.record(), self.work_order(["RLS-CON-404"])]
        errors = CANDIDATE_VALIDATOR.validate_type_specific_metadata(artifacts, self.root)
        selected = [
            error
            for error in errors
            if PACKAGE.DECLARATION_FIELD in error.message
            and PACKAGE.REASON_UNKNOWN_RECORD in error.message
        ]
        self.assertEqual(1, len(selected))
        self.assertEqual("E012", selected[0].code)
        self.assertEqual("governance", selected[0].plane)
        self.assertIn("work-orders/WO-CON-001.md", selected[0].path.replace("\\", "/"))
        self.assertIn("RLS-CON-404", selected[0].message)

    def test_a_declared_record_no_longer_requires_the_binding(self) -> None:
        declared = CANDIDATE_VALIDATOR.validate_type_specific_metadata(
            [self.record(), self.work_order(["RLS-CON-001"])], self.root
        )
        undeclared = CANDIDATE_VALIDATOR.validate_type_specific_metadata(
            [self.record()], self.root
        )
        self.assertEqual(
            [],
            [error for error in declared if "evaluator_evidence" in error.message],
        )
        self.assertNotEqual(
            [],
            [error for error in undeclared if "evaluator_evidence" in error.message],
        )

    def test_a_partially_bound_record_still_requires_the_binding(self) -> None:
        artifacts = [
            self.record(evaluator_evidence_path="docs/engineering/sample/evidence/e.json"),
            self.work_order(["RLS-CON-001"]),
        ]
        errors = CANDIDATE_VALIDATOR.validate_type_specific_metadata(artifacts, self.root)
        self.assertNotEqual(
            [],
            [error for error in errors if "evaluator_evidence" in error.message],
        )
        self.assertNotEqual(
            [],
            [
                error
                for error in errors
                if PACKAGE.REASON_ALREADY_BOUND in error.message
            ],
        )


if __name__ == "__main__":  # pragma: no cover - direct execution convenience
    unittest.main()
