from __future__ import annotations

import ast
import difflib
import hashlib
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

from se_harness import release_qualification


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

#: Every path `WO-REB-028` deleted. Pinned as an exhaustive list rather than a
#: prefix rule: a file reappearing under any of these names is the retired path
#: returning, and this inventory names it.
DELETED_PATHS = (
    "repository_tools/release_bootstrap.py",
    "repository_tools/predecessor_preparation.py",
    "repository_tools/predecessor_publication.py",
    "repository_tools/predecessor_assessment.py",
    "scripts/bind_release_bootstrap.py",
    "scripts/prepare_predecessor_release.py",
    "scripts/validate_predecessor_publication_view.py",
    "scripts/assess_predecessor_evaluator.py",
    "tests/test_release_bootstrap.py",
    "tests/test_predecessor_preparation.py",
    "tests/test_predecessor_publication.py",
    "tests/test_predecessor_assessment_contract.py",
)

#: The module names no retained file may import, at any import level.
DELETED_MODULES = (
    "release_bootstrap",
    "predecessor_preparation",
    "predecessor_publication",
    "predecessor_assessment",
)

#: The trees the import scan covers, in the order `VER-REB-012` lists them.
SCANNED_TREES = (
    "se_harness",
    "repository_tools",
    "scripts",
    ".github/scripts",
    "tests",
    "templates",
)

#: Schema names the retired path owned. They are never reused for another
#: meaning, so each one may appear only where this module permits it.
RETIRED_SCHEMAS = (
    "se-harness-release-bootstrap-v1",
    "se-harness-predecessor-bootstrap-v1",
    "se-harness-predecessor-view-exclusion/v1",
)

#: The closed 0.6.0 artifacts that keep the retired path's facts. Each stays on
#: disk with the marker that made it a bootstrap-era record.
RETAINED_HISTORY = {
    "docs/engineering/release-0-6-0/release/REL-SEH-008.md": "[bootstrap]",
    "docs/engineering/release-0-6-0/release/REL-SEH-009.md": "[bootstrap]",
    "docs/engineering/release-0-6-0/release/REL-SEH-010.md": "[bootstrap]",
    "docs/engineering/release-0-6-0/release/REL-SEH-011.md": "[bootstrap]",
    "docs/engineering/release-0-6-0/releases/RLS-SEH-009.md": 'preparation_schema = "se-harness-predecessor-bootstrap-v1"',
    "docs/engineering/release-0-6-0/releases/RLS-SEH-012.md": 'preparation_schema = "se-harness-predecessor-bootstrap-v1"',
}

#: The evidence bindings that must keep verifying after the machinery that
#: produced them is gone: a retained digest is only a fact while its file
#: still hashes to it.
RETAINED_EVIDENCE_BINDINGS = (
    (
        "docs/engineering/release-0-6-0/releases/RLS-SEH-012.md",
        "preparation_view_evidence_path",
        "preparation_view_evidence_sha256",
    ),
    (
        "docs/engineering/release-0-6-0/releases/RLS-SEH-012.md",
        "evaluator_evidence_path",
        "evaluator_evidence_sha256",
    ),
    (
        "docs/engineering/release-0-6-0/releases/RLS-SEH-009.md",
        "evaluator_evidence_path",
        "evaluator_evidence_sha256",
    ),
)

#: The two managed validator copies. `WO-REB-028` edited neither. `WO-REB-029`
#: edits the template copy, the one consumer repositories install, and no byte
#: of the root copy: the root copy is the exact released evaluator's file and is
#: hash-locked, so the retirement reaches this repository's own verdicts only
#: when the root evaluator next advances. The root copy is therefore the one
#: place a retired schema name still appears in executable code.
MANAGED_VALIDATORS = (
    "scripts/validate_engineering_artifacts.py",
    "templates/repository/standard/scripts/validate_engineering_artifacts.py",
)

#: The root copy alone. `WO-REB-029` edits the template copy, so the root copy
#: is the only place a retired schema name still appears in executable code.
ROOT_VALIDATOR = "scripts/validate_engineering_artifacts.py"
CANDIDATE_VALIDATOR_PATH = "templates/repository/standard/scripts/validate_engineering_artifacts.py"

#: Every name `WO-REB-029` deleted from the candidate copy, named individually
#: as `VER-REB-013` case 1 requires: one regular expression over the whole file
#: would also pass while a renamed survivor stayed behind. Each name must be
#: absent from the candidate copy and present in the root copy, which pins the
#: divergence from both sides at once.
DELETED_VALIDATOR_NAMES = (
    "RELEASE_BOOTSTRAP_SCHEMA",
    "PREDECESSOR_PREPARATION_SCHEMA",
    "PREDECESSOR_VIEW_EVIDENCE_SCHEMA",
    "PREDECESSOR_VIEW_EVIDENCE_MAX_BYTES",
    "RELEASE_BOOTSTRAP_KEYS",
    "_validated_release_bootstrap",
    "_bootstrap_for_release_record",
    "_validate_predecessor_view_evidence",
    "_canonical_utf8_text_lf",
    "bootstrap_contract",
    "approved_bootstrap_contracts",
    "rejected_predecessor_history",
    "preparation_schema",
    "preparation_view_evidence",
    "se-harness-release-bootstrap-v1",
    "se-harness-predecessor-bootstrap-v1",
)

#: The declared candidate exception, as `VER-REB-013` case 8 requires: the exact
#: difference between the two copies, block by block, as the first line of the
#: block in the root copy, that line's 1-based number in the root copy, and the
#: number of root lines the block spans. Nothing is added or changed, so the
#: candidate copy is the root copy with exactly these ten blocks removed.
CANDIDATE_VALIDATOR_DELETIONS = (
    (58, 15, 'RELEASE_BOOTSTRAP_SCHEMA = "se-harness-release-bootstrap-v1"'),
    (791, 133, "def _validated_release_bootstrap("),
    (932, 1, "    bootstrap_contract: dict[str, Any] | None = None,"),
    (1062, 39, "    if bootstrap_contract is not None:"),
    (1133, 325, "def _validate_predecessor_view_evidence("),
    (1940, 18, "    approved_bootstrap_contracts = ["),
    (1990, 3, "            _validated_release_bootstrap(artifact, errors, report_root)"),
    (2115, 23, "            bootstrap_contract = _bootstrap_for_release_record("),
    (2180, 27, '            if artifact.status == "ready" and bootstrap_contract is not None:'),
    (2237, 1, "                bootstrap_contract=bootstrap_contract,"),
)

#: 585 deleted lines, the figure `WO-REB-029` records as its measured deletion.
CANDIDATE_VALIDATOR_DELETED_LINES = 585

#: `WO-ECP-006` (2026-08-29): the candidate copy is the 0.10.0 root copy with the
#: `[agentic_delegation]` validator removed, three blocks, 147 lines, declared in the
#: same form: first line in the root copy, its 1-based number, lines spanned.
ECP006_CANDIDATE_VALIDATOR_DELETIONS = (
    (72, 22, 'AGENTIC_DELEGATION_SCHEMA = "se-harness-agentic-delegation-v1"'),
    (2649, 124, "def _path_is_within(child: str, parent: str) -> bool:"),
    (2999, 1, "        errors.extend(validate_agentic_delegations(artifacts, repository_root))"),
)
ECP006_CANDIDATE_VALIDATOR_DELETED_LINES = 147

#: `WO-ECP-018` (2026-08-29): against a root that already carries the `[agentic_delegation]`
#: removal (0.11.0), the candidate copy adds the `[delegation]` class validator: two inserted
#: blocks, 23 lines, declared as (root line the block follows, lines inserted, first line).
ECP018_CANDIDATE_VALIDATOR_INSERTIONS = (
    (2564, 22, "def validate_work_order_delegation("),
    (2853, 1, "        errors.extend(validate_work_order_delegation(artifacts, repository_root))"),
)
ECP018_CANDIDATE_VALIDATOR_INSERTED_LINES = 23

#: `WO-AUT-004` (2026-08-30): on top of the `WO-ECP-018` insertions, the candidate copy
#: carries the advisory class (SPEC-AUT-002): every non-equal opcode of the root-to-candidate
#: diff, declared as (tag, 1-based root line, root lines spanned, candidate lines spanned,
#: first line of the block). Root line numbers are those of the 0.11.0 root copy.
AUT004_CANDIDATE_VALIDATOR_EDITS = (
    ("replace", 17, 1, 1, "from dataclasses import asdict, dataclass, field"),
    ("replace", 292, 2, 7, "def validate_authoring(artifacts: list[Artifact], report_root: Path) -> tuple[list[Diagnostic], list[Diagnostic], list[Diagnostic]]:"),
    ("insert", 297, 0, 1, "    advisories: list[Diagnostic] = []"),
    ("insert", 301, 0, 1, '        draft = artifact.status == "draft"'),
    ("replace", 302, 1, 1, "        if isinstance(statement, str) and statement.strip() and draft:"),
    ("replace", 308, 1, 1, '                advisories.append(Diagnostic(_display_path(artifact.path, report_root), "W-AUT-001",'),
    ("replace", 312, 1, 1, '                advisories.append(Diagnostic(_display_path(artifact.path, report_root), "W-AUT-002",'),
    ("replace", 315, 1, 1, '                advisories.append(Diagnostic(_display_path(artifact.path, report_root), "W-AUT-003",'),
    ("replace", 319, 2, 2, "            if method.strip() and draft:"),
    ("replace", 341, 1, 1, "    return errors, warnings, advisories"),
    ("insert", 408, 0, 2, "    # SPEC-AUT-002 AUT-ADV-001: the advisory class, apart from errors and warnings."),
    ("insert", 433, 0, 1, '            "advisory_count": len(self.advisories),'),
    ("insert", 435, 0, 1, '            "advisories": [asdict(item) for item in sorted(self.advisories)],'),
    ("insert", 2564, 0, 22, "def validate_work_order_delegation("),
    ("replace", 2838, 1, 1, "        authoring_errors, authoring_warnings, authoring_advisories = validate_authoring(artifacts, repository_root)"),
    ("insert", 2853, 0, 1, "        errors.extend(validate_work_order_delegation(artifacts, repository_root))"),
    ("insert", 2887, 0, 1, "        advisories=sorted(set(authoring_advisories)),"),
    ("replace", 2890, 1, 1, "def render_human(report: ValidationReport, *, show_advisories: bool = False) -> str:"),
    ("replace", 2898, 1, 1, '        f"Artifacts: {len(report.artifacts)} | Errors: {len(report.errors)} | Warnings: {len(report.warnings)} | Advisories: {len(report.advisories)}",'),
    ("insert", 2915, 0, 7, "    if show_advisories and report.advisories:"),
    ("insert", 2928, 0, 4, "    parser.add_argument("),
    ("replace", 2942, 1, 1, "        print(render_human(report, show_advisories=args.show_advisories))"),
)
AUT004_CANDIDATE_VALIDATOR_LINE_DELTA = 46

#: WO-LRE-002 (SPEC-LRE-002): the candidate copy is the 0.11.0 root copy with
#: the WO-ECP-018 insertions, the WO-AUT-004 advisory class and the legacy
#: release-evidence machinery removed, declared opcode by opcode.
LRE002_CANDIDATE_VALIDATOR_EDITS = (
    ("replace", 17, 1, 1, 'from dataclasses import asdict, dataclass, field'),
    ("replace", 58, 27, 4, '# The legacy release-evidence declaration mechanism (SPEC-LRE-001) was retired'),
    ("replace", 292, 2, 7, 'def validate_authoring(artifacts: list[Artifact], report_root: Path) -> tuple[list[Diagnostic], list[Diagnostic], list[Diagnostic]]:'),
    ("insert", 297, 0, 1, '    advisories: list[Diagnostic] = []'),
    ("insert", 301, 0, 1, '        draft = artifact.status == "draft"'),
    ("replace", 302, 1, 1, '        if isinstance(statement, str) and statement.strip() and draft:'),
    ("replace", 308, 1, 1, '                advisories.append(Diagnostic(_display_path(artifact.path, report_root), "W-AUT-001",'),
    ("replace", 312, 1, 1, '                advisories.append(Diagnostic(_display_path(artifact.path, report_root), "W-AUT-002",'),
    ("replace", 315, 1, 1, '                advisories.append(Diagnostic(_display_path(artifact.path, report_root), "W-AUT-003",'),
    ("replace", 319, 2, 2, '            if method.strip() and draft:'),
    ("replace", 341, 1, 1, '    return errors, warnings, advisories'),
    ("insert", 408, 0, 2, '    # SPEC-AUT-002 AUT-ADV-001: the advisory class, apart from errors and warnings.'),
    ("insert", 433, 0, 1, '            "advisory_count": len(self.advisories),'),
    ("insert", 435, 0, 1, '            "advisories": [asdict(item) for item in sorted(self.advisories)],'),
    ("delete", 1166, 215, 0, 'def _legacy_declaration(work_order: dict[str, Any]) -> Any:'),
    ("delete", 1383, 21, 0, ''),
    ("replace", 1614, 5, 5, '            # REQ-LRE-003 (the evaluator-evidence floor, owner decision of'),
    ("delete", 1620, 1, 0, '                and artifact.artifact_id in legacy_exemptions'),
    ("replace", 1628, 1, 1, '                required=not unbound,'),
    ("insert", 2564, 0, 22, 'def validate_work_order_delegation('),
    ("replace", 2838, 1, 1, '        authoring_errors, authoring_warnings, authoring_advisories = validate_authoring(artifacts, repository_root)'),
    ("insert", 2853, 0, 1, '        errors.extend(validate_work_order_delegation(artifacts, repository_root))'),
    ("delete", 2869, 7, 0, '    legacy_evidence_warnings: list[Diagnostic] = []'),
    ("delete", 2880, 1, 0, '        *legacy_evidence_warnings,'),
    ("insert", 2887, 0, 1, '        advisories=sorted(set(authoring_advisories)),'),
    ("replace", 2890, 1, 1, 'def render_human(report: ValidationReport, *, show_advisories: bool = False) -> str:'),
    ("replace", 2898, 1, 1, '        f"Artifacts: {len(report.artifacts)} | Errors: {len(report.errors)} | Warnings: {len(report.warnings)} | Advisories: {len(report.advisories)}",'),
    ("insert", 2915, 0, 7, '    if show_advisories and report.advisories:'),
    ("insert", 2928, 0, 4, '    parser.add_argument('),
    ("replace", 2942, 1, 1, '        print(render_human(report, show_advisories=args.show_advisories))'),
)
LRE002_CANDIDATE_VALIDATOR_LINE_DELTA = -222

#: The bootstrap-era markers under the closed 0.6.0 domain, pinned as counts.
#: The retirement removes their readers, not the data: a count that moved would
#: mean retained history had been rewritten.
RETAINED_MARKER_COUNTS = {"[bootstrap]": 4, "preparation_schema": 2}

FIELD = "([A-Za-z0-9_]+) = \"([^\"]*)\""


def _fields(relative: str) -> dict[str, str]:
    text = (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")
    return dict(re.findall(FIELD, text.split("+++", 2)[1]))


def _python_sources(tree: str) -> list[Path]:
    root = REPOSITORY_ROOT / tree
    if not root.exists():
        return []
    return sorted(root.rglob("*.py"))


def _imported_names(source: Path) -> set[str]:
    names: set[str] = set()
    module = ast.parse(source.read_text(encoding="utf-8"))
    for node in ast.walk(module):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            names.add(base)
            names.update(f"{base}.{alias.name}".strip(".") for alias in node.names)
    return names


def _load_candidate_validator():
    """Load the copy of the managed validator consumer repositories install.

    Loaded by path, never by import name: `WO-REB-029` edits this copy only, so
    a test that silently picked up the root copy would report the retirement as
    incomplete or as complete for the wrong file.
    """
    path = REPOSITORY_ROOT / CANDIDATE_VALIDATOR_PATH
    specification = importlib.util.spec_from_file_location(
        "_reb029_candidate_validator", path
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load the candidate validator: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class DeletedSurfaceTests(unittest.TestCase):
    """The twelve deleted paths are gone and nothing imports what they held."""

    def test_every_deleted_path_is_absent(self) -> None:
        self.assertEqual(12, len(DELETED_PATHS))
        for relative in DELETED_PATHS:
            with self.subTest(path=relative):
                self.assertFalse((REPOSITORY_ROOT / relative).exists())

    def test_no_retained_python_file_imports_a_deleted_module(self) -> None:
        offenders: set[str] = set()
        scanned = 0
        for tree in SCANNED_TREES:
            for source in _python_sources(tree):
                scanned += 1
                relative = source.relative_to(REPOSITORY_ROOT).as_posix()
                for name in _imported_names(source):
                    if name.split(".")[-1] in DELETED_MODULES:
                        offenders.add(f"{relative}: {name}")
        self.assertEqual(set(), offenders)
        # A scan that reached nothing would pass vacuously.
        self.assertGreater(scanned, 100)

    def test_no_entry_point_script_of_the_retired_path_remains(self) -> None:
        # The four scripts were the only callers with a command line, so a
        # surviving one would be an unreachable published command.
        for source in _python_sources("scripts"):
            relative = source.relative_to(REPOSITORY_ROOT).as_posix()
            with self.subTest(script=relative):
                self.assertNotIn(relative, DELETED_PATHS)

    def test_the_live_predecessor_facts_and_transition_tools_are_untouched(self) -> None:
        # Deleting `predecessor_assessment.py` must not reach the governor-transition
        # lane or the candidate-evidence lane, which name neither module.
        for relative in (
            "repository_tools/evaluator_facts.py",
            "scripts/validate_governor_transition.py",
        ):
            source = REPOSITORY_ROOT / relative
            with self.subTest(module=relative):
                self.assertTrue(source.exists())
                names = {name.split(".")[-1] for name in _imported_names(source)}
                self.assertEqual(set(), names & set(DELETED_MODULES))


class RetiredNameReservationTests(unittest.TestCase):
    """A retired schema name or check code is reserved, never reused."""

    def test_the_retired_check_codes_are_reserved_and_emitted_by_no_path(self) -> None:
        self.assertEqual(("PV001", "PV002"), release_qualification.RETIRED_CHECK_CODES)
        for code in release_qualification.RETIRED_CHECK_CODES:
            with self.subTest(code=code):
                # The declaration reserves the value; no other package or
                # repository-owned source may produce it.
                holders = set()
                for tree in ("se_harness", "repository_tools", "scripts", ".github/scripts"):
                    for source in _python_sources(tree):
                        if code in source.read_text(encoding="utf-8"):
                            holders.add(source.relative_to(REPOSITORY_ROOT).as_posix())
                self.assertEqual({"se_harness/release_qualification.py"}, holders)

    def test_the_retired_operation_is_absent_from_the_published_surface(self) -> None:
        self.assertNotIn("predecessor-view", release_qualification.OPERATIONS)
        self.assertNotIn("predecessor-view", release_qualification.INDEPENDENCE)
        self.assertEqual(
            set(release_qualification.OPERATIONS), set(release_qualification.INDEPENDENCE)
        )
        cli = (REPOSITORY_ROOT / "se_harness" / "cli.py").read_text(encoding="utf-8")
        self.assertNotIn("predecessor-view", cli)
        self.assertNotIn("--view-output", cli)

    @staticmethod
    def _holders(schema: str) -> set[str]:
        holders: set[str] = set()
        for tree in ("se_harness", "repository_tools", "scripts", ".github", "templates"):
            root = REPOSITORY_ROOT / tree
            if not root.exists():
                continue
            for source in sorted(root.rglob("*")):
                if not source.is_file() or source.suffix not in {".py", ".json", ".yml", ".md"}:
                    continue
                if schema in source.read_text(encoding="utf-8", errors="ignore"):
                    holders.add(source.relative_to(REPOSITORY_ROOT).as_posix())
        return holders

    def test_a_retired_schema_name_appears_only_in_retained_history(self) -> None:
        # `WO-REB-029` removed the template copy from this list: it is now the
        # root copy alone, and the list shrinks again when that copy advances.
        permitted = {ROOT_VALIDATOR}
        for schema in RETIRED_SCHEMAS:
            with self.subTest(schema=schema):
                self.assertEqual(set(), self._holders(schema) - permitted)

    def test_the_exclusion_observation_schema_was_never_written(self) -> None:
        # `WO-REB-025`'s conditional exclusion was superseded before it shipped,
        # so its schema name is reserved without ever having been written. Unlike
        # the other two, no retained record carries it, so nothing may hold it.
        self.assertEqual(
            set(), self._holders("se-harness-predecessor-view-exclusion")
        )


class RetainedHistoryTests(unittest.TestCase):
    """The closed 0.6.0 facts stay verifiable while no longer being re-derivable."""

    def test_every_closed_artifact_keeps_its_bootstrap_era_marker(self) -> None:
        self.assertEqual(6, len(RETAINED_HISTORY))
        for relative, marker in RETAINED_HISTORY.items():
            source = REPOSITORY_ROOT / relative
            with self.subTest(artifact=relative):
                self.assertTrue(source.exists())
                self.assertIn(marker, source.read_text(encoding="utf-8"))

    def test_every_retained_evidence_digest_still_verifies(self) -> None:
        for relative, path_field, digest_field in RETAINED_EVIDENCE_BINDINGS:
            fields = _fields(relative)
            bound = REPOSITORY_ROOT / fields[path_field]
            with self.subTest(artifact=relative, field=digest_field):
                self.assertTrue(bound.exists())
                self.assertEqual(
                    fields[digest_field], hashlib.sha256(bound.read_bytes()).hexdigest()
                )

    def test_the_hash_bound_declaration_still_carries_the_retired_path_fields(self) -> None:
        # Retiring the producer must not retire the binding: an unclaimed digest
        # field in a retained record would stop being checked at all.
        declaration = (REPOSITORY_ROOT / "se_harness" / "hash_bound_classes.json").read_text(
            encoding="utf-8"
        )
        for field in (
            "evaluator_evidence_sha256",
            "preparation_view_evidence_sha256",
            "from_lock_sha256",
        ):
            with self.subTest(field=field):
                self.assertIn(f'"{field}"', declaration)
        hash_bound = (REPOSITORY_ROOT / "se_harness" / "hash_bound.py").read_text(encoding="utf-8")
        for module in DELETED_MODULES:
            with self.subTest(module=module):
                self.assertNotIn(module, hash_bound)

    def test_the_predecessor_lock_digest_of_the_closed_contract_is_unchanged(self) -> None:
        fields = _fields("docs/engineering/release-0-6-0/release/REL-SEH-011.md")
        self.assertEqual(
            "08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3",
            fields["from_lock_sha256"],
        )
        self.assertEqual("0.5.0", fields["from_lock_tool_version"])

    def test_nothing_reconstructs_a_predecessor_view(self) -> None:
        # `ARCH-REB-012`: no projection, view, sparse checkout or omitting clone
        # of this repository is constructed for any evaluator. The migration
        # rehearsal is the one retained handover mechanism and builds none.
        # `WO-REB-029`: the managed validator copies were skipped here while one
        # of them still described a predecessor view. Neither does now, so the
        # scan covers every source in these trees with no exception.
        for tree in ("se_harness", "repository_tools", "scripts", ".github/scripts"):
            for source in _python_sources(tree):
                relative = source.relative_to(REPOSITORY_ROOT).as_posix()
                text = source.read_text(encoding="utf-8")
                for absent in ("sparse-checkout", "--sparse", "predecessor view"):
                    with self.subTest(source=relative, absent=absent):
                        self.assertNotIn(absent, text)

    def test_the_upgrade_rehearsal_is_the_remaining_handover_mechanism(self) -> None:
        # WO-ECP-010 replaced the governance-migration stage machine with the real
        # upgrade rehearsal; the module stays, dead, until the root advances (its
        # deletion is refused by released 0.7.1's hash-bound class) and nothing
        # invokes it.
        self.assertTrue((REPOSITORY_ROOT / "repository_tools" / "upgrade_rehearsal.py").exists())
        cli = (REPOSITORY_ROOT / "se_harness" / "cli.py").read_text(encoding="utf-8")
        self.assertNotIn("rehearse-migration", cli)


class ExplorerPayloadTests(unittest.TestCase):
    """The Explorer's own bootstrap payload is a different thing and still works."""

    def test_the_dashboard_bootstrap_payload_schema_is_untouched(self) -> None:
        # `harness-dashboard-bootstrap-v2` names the Explorer's embedded JSON,
        # not a release bootstrap. It is out of `WO-REB-028`'s scope and the two
        # producers plus the template must still agree on it.
        for relative in (
            "scripts/generate_harness_dashboard.py",
            ".github/scripts/publish_dashboard.py",
            "scripts/harness_explorer/index.template.html",
        ):
            with self.subTest(producer=relative):
                self.assertIn(
                    "harness-dashboard-bootstrap-v2",
                    (REPOSITORY_ROOT / relative).read_text(encoding="utf-8"),
                )


class ConsumerValidatorRetirementTests(unittest.TestCase):
    """`WO-REB-029`: the validator consumer repositories install carries none of
    the retired rules. The root copy is the released evaluator's hash-locked
    policy: under the 0.7.1 root it still carried all of them, and the
    divergence was declared line for line; since `WO-HUP-008` adopted 0.8.0 the
    root copy is the candidate copy byte for byte. The assertions read the root
    identity from the lock rather than assume either state."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.root_text = (REPOSITORY_ROOT / ROOT_VALIDATOR).read_text(encoding="utf-8")
        cls.candidate_text = (REPOSITORY_ROOT / CANDIDATE_VALIDATOR_PATH).read_text(encoding="utf-8")
        cls.candidate = _load_candidate_validator()
        lock = json.loads((REPOSITORY_ROOT / ".engineering-harness.lock").read_text(encoding="utf-8"))
        cls.root_version = lock["evaluator"]["version"]
        # The released 0.7.1 root is the last one whose validator carried the retired rules.
        cls.root_carries_retired_rules = cls.root_version == "0.7.1"

    def test_every_deleted_name_is_absent_from_the_candidate_copy(self) -> None:
        self.assertEqual(16, len(DELETED_VALIDATOR_NAMES))
        for name in DELETED_VALIDATOR_NAMES:
            with self.subTest(name=name):
                self.assertNotIn(name, self.candidate_text)
                if self.root_carries_retired_rules:
                    # Present in the root copy: a name that was never there would
                    # make the absence case pass without proving anything.
                    self.assertIn(name, self.root_text)
                else:
                    # WO-HUP-008: the root is the released candidate; the name is gone from both.
                    self.assertNotIn(name, self.root_text)

    def test_the_candidate_module_no_longer_defines_the_deleted_attributes(self) -> None:
        # Absence in the text is not absence in the loaded module: a survivor
        # reintroduced through an import would not show up in a static read.
        for name in DELETED_VALIDATOR_NAMES:
            if not name.isidentifier():
                continue
            with self.subTest(attribute=name):
                self.assertFalse(hasattr(self.candidate, name))
        for retained in ("validate_repository", "validate_revision_consistency", "WORKFLOW_LIFECYCLES"):
            with self.subTest(retained=retained):
                self.assertTrue(hasattr(self.candidate, retained))

    def test_the_candidate_copy_differs_from_the_root_copy_only_by_the_declared_deletions(self) -> None:
        if not self.root_carries_retired_rules:
            # WO-HUP-008: the root copy is the released 0.8.0 validator, which is the
            # candidate template byte for byte; the deletion ledger below describes the
            # 0.7.1 root and is retained for that state only.
            if "validate_agentic_delegations" not in self.root_text:
                if "validate_work_order_delegation" in self.root_text:
                    self.assertEqual(self.candidate_text, self.root_text)
                    return
                if "resolve_legacy_release_evidence" not in self.candidate_text and "resolve_legacy_release_evidence" in self.root_text:
                    # WO-LRE-002 (SPEC-LRE-002): the legacy release-evidence machinery
                    # is removed from the candidate copy on top of the earlier edits.
                    self._assert_root_plus_declared_edits(
                        LRE002_CANDIDATE_VALIDATOR_EDITS, LRE002_CANDIDATE_VALIDATOR_LINE_DELTA
                    )
                    return
                if "advisories" in self.candidate_text and "advisories" not in self.root_text:
                    # WO-AUT-004 (SPEC-AUT-002): the candidate copy is the 0.11.0 root copy with
                    # the WO-ECP-018 insertions and the advisory class, declared opcode by opcode.
                    self._assert_root_plus_declared_edits(
                        AUT004_CANDIDATE_VALIDATOR_EDITS, AUT004_CANDIDATE_VALIDATOR_LINE_DELTA
                    )
                    return
                # WO-ECP-018 (SPEC-ECP-006 ECP-DLG-001): the candidate copy is the 0.11.0 root
                # copy with the `[delegation]` class validator inserted, declared block by block.
                self._assert_root_plus_declared_insertions(
                    ECP018_CANDIDATE_VALIDATOR_INSERTIONS, ECP018_CANDIDATE_VALIDATOR_INSERTED_LINES
                )
                return
            # WO-ECP-006 (SPEC-ECP-006 ECP-DLG-008): the candidate copy is the root copy
            # with the `[agentic_delegation]` validator removed, declared block by block
            # in the same form as the 0.7.1 ledger; a root released with this removal
            # takes the equality branch above.
            self._assert_root_minus_declared_blocks(ECP006_CANDIDATE_VALIDATOR_DELETIONS, ECP006_CANDIDATE_VALIDATOR_DELETED_LINES)
            return
        self._assert_root_minus_declared_blocks(CANDIDATE_VALIDATOR_DELETIONS, CANDIDATE_VALIDATOR_DELETED_LINES)

    def _assert_root_plus_declared_edits(self, declared, line_delta) -> None:
        root_lines = self.root_text.splitlines()
        candidate_lines = self.candidate_text.splitlines()
        self.assertEqual(line_delta, len(candidate_lines) - len(root_lines))
        matcher = difflib.SequenceMatcher(a=root_lines, b=candidate_lines, autojunk=False)
        observed = []
        for tag, start, stop, candidate_start, candidate_stop in matcher.get_opcodes():
            if tag == "equal":
                continue
            first = candidate_lines[candidate_start] if candidate_stop > candidate_start else root_lines[start]
            observed.append((tag, start + 1, stop - start, candidate_stop - candidate_start, first))
        self.assertEqual(len(declared), len(observed), observed)
        for expected, actual in zip(declared, observed):
            with self.subTest(root_line=expected[1], first=expected[4][:48]):
                self.assertEqual(expected, actual)

    def _assert_root_plus_declared_insertions(self, declared, inserted_lines) -> None:
        root_lines = self.root_text.splitlines()
        candidate_lines = self.candidate_text.splitlines()
        self.assertEqual(inserted_lines, len(candidate_lines) - len(root_lines))
        matcher = difflib.SequenceMatcher(a=root_lines, b=candidate_lines, autojunk=False)
        observed = []
        for tag, start, stop, candidate_start, candidate_stop in matcher.get_opcodes():
            if tag == "equal":
                continue
            # Nothing is deleted and nothing is rewritten: the candidate copy is the root copy
            # plus the declared blocks.
            self.assertEqual("insert", tag, f"unexpected {tag} at root line {start + 1}")
            observed.append((start + 1, candidate_stop - candidate_start, candidate_lines[candidate_start]))
        self.assertEqual(len(declared), len(observed))
        for (line, count, first), (observed_line, observed_count, observed_first) in zip(declared, observed):
            with self.subTest(root_line=line, first=first[:48]):
                self.assertEqual((line, count, first), (observed_line, observed_count, observed_first))

    def _assert_root_minus_declared_blocks(self, declared, deleted_lines) -> None:
        root_lines = self.root_text.splitlines()
        candidate_lines = self.candidate_text.splitlines()
        self.assertEqual(deleted_lines, len(root_lines) - len(candidate_lines))
        matcher = difflib.SequenceMatcher(a=root_lines, b=candidate_lines, autojunk=False)
        observed = []
        for tag, start, stop, _candidate_start, _candidate_stop in matcher.get_opcodes():
            if tag == "equal":
                continue
            # Nothing is added and nothing is rewritten: the candidate copy is a
            # deletion of the root copy, which is what makes the divergence
            # reviewable line for line.
            self.assertEqual("delete", tag, f"unexpected {tag} at root line {start + 1}")
            observed.append((start + 1, stop - start, root_lines[start:stop]))
        self.assertEqual(len(declared), len(observed))
        for (line, count, marker), (observed_line, observed_count, block) in zip(declared, observed):
            with self.subTest(root_line=line, marker=marker[:48]):
                self.assertEqual((line, count), (observed_line, observed_count))
                self.assertIn(marker, block)
        self.assertEqual(
            CANDIDATE_VALIDATOR_DELETED_LINES, sum(count for _, count, _ in CANDIDATE_VALIDATOR_DELETIONS)
        )

    def test_the_closed_release_artifacts_are_inert_data(self) -> None:
        # `VER-REB-013` case 4: the markers stay, and no rule in the validator
        # that consumer repositories install reads any of them.
        domain = REPOSITORY_ROOT / "docs/engineering/release-0-6-0"
        for marker, expected in RETAINED_MARKER_COUNTS.items():
            observed = sum(
                source.read_text(encoding="utf-8").count(marker)
                for source in sorted(domain.rglob("*.md"))
            )
            with self.subTest(marker=marker):
                self.assertEqual(expected, observed)
                self.assertNotIn(marker.strip("[]"), self.candidate_text)
        for relative in RETAINED_HISTORY:
            with self.subTest(artifact=relative):
                self.assertTrue(str(relative).startswith("docs/engineering/release-0-6-0/"))

    def test_a_rejected_record_still_cannot_claim_a_version_against_a_successor(self) -> None:
        # `VER-REB-013` case 6, and `REQ-REB-011` preserved. The rule now stands
        # on the lifecycle matrix alone: `rejected` reserves no version, so a
        # rejected record is inert whether or not it carries the retired
        # `preparation_schema` marker, and two active records still collide.
        lifecycles = self.candidate.WORKFLOW_LIFECYCLES["release_record"]
        self.assertFalse(lifecycles["rejected"].reserves_version)
        for active in ("ready", "released"):
            with self.subTest(status=active):
                self.assertTrue(lifecycles[active].reserves_version)

        def record(identifier: str, status: str, **extra: object):
            metadata = {
                "id": identifier,
                "type": "release_record",
                "status": status,
                "version": "9.9.9",
            }
            metadata.update(extra)
            return self.candidate.Artifact(
                path=REPOSITORY_ROOT / f"docs/engineering/releases/{identifier}.md",
                metadata=metadata,
                body="",
            )

        def collisions(*artifacts) -> list[str]:
            return [
                diagnostic.message
                for diagnostic in self.candidate.validate_revision_consistency(
                    list(artifacts), REPOSITORY_ROOT
                )
                if "duplicate release record version" in diagnostic.message
            ]

        rejected = record("RLS-TST-101", "rejected", rejected_at="2026-08-27T00:00:00Z", rejected_by="release-owner")
        marked = record(
            "RLS-TST-102",
            "rejected",
            rejected_at="2026-08-27T00:00:00Z",
            rejected_by="release-owner",
            preparation_schema="se-harness-predecessor-bootstrap-v1",
        )
        ready = record("RLS-TST-103", "ready")
        released = record("RLS-TST-104", "released")

        self.assertEqual([], collisions(rejected, ready))
        self.assertEqual([], collisions(rejected, released))
        # The retired marker changes nothing: the condition that read it is gone,
        # and no diagnostic mentions it.
        self.assertEqual([], collisions(marked, released))
        for diagnostic in self.candidate.validate_revision_consistency([marked, released], REPOSITORY_ROOT):
            with self.subTest(code=diagnostic.code):
                self.assertNotIn("bootstrap", diagnostic.message)
                self.assertNotIn("predecessor", diagnostic.message)
        # Two records that do reserve the version still collide, so the removal
        # narrowed nothing beyond the named rules.
        both = collisions(ready, released)
        self.assertEqual(2, len(both))
        for message in both:
            self.assertIn("RLS-TST-103, RLS-TST-104", message)


if __name__ == "__main__":
    unittest.main()
