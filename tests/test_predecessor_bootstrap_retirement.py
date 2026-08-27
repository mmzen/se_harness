from __future__ import annotations

import ast
import hashlib
import re
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

#: The two managed validator copies. `WO-REB-028` edits neither: the root copy
#: belongs to released 0.6.0 and the template copy is candidate source for a
#: later release. Their inert conditional bootstrap rules are the one place a
#: retired schema name legitimately appears in executable code.
MANAGED_VALIDATORS = (
    "scripts/validate_engineering_artifacts.py",
    "templates/repository/standard/scripts/validate_engineering_artifacts.py",
)

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
            "repository_tools/predecessor_facts.py",
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
        permitted = set(MANAGED_VALIDATORS)
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
        for tree in ("se_harness", "repository_tools", "scripts", ".github/scripts"):
            for source in _python_sources(tree):
                relative = source.relative_to(REPOSITORY_ROOT).as_posix()
                if relative in MANAGED_VALIDATORS:
                    continue
                text = source.read_text(encoding="utf-8")
                for absent in ("sparse-checkout", "--sparse", "predecessor view"):
                    with self.subTest(source=relative, absent=absent):
                        self.assertNotIn(absent, text)

    def test_the_migration_rehearsal_is_the_remaining_handover_mechanism(self) -> None:
        module = REPOSITORY_ROOT / "se_harness" / "governance_migration.py"
        self.assertTrue(module.exists())
        cli = (REPOSITORY_ROOT / "se_harness" / "cli.py").read_text(encoding="utf-8")
        self.assertIn("rehearse-migration", cli)


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


if __name__ == "__main__":
    unittest.main()
