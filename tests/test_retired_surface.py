"""Every tombstone of the suite, in one table (SPEC-TST-002 TST-HYG-009).

A tombstone asserts that a retired name, path, option or phrase is absent. They
used to sit beside the tests of the features that replaced them, one module per
retirement; here each retirement is one row, named by the work order that
retired it, and the checks below read the rows. A name that reappears fails the
row that reserved it.
"""

from __future__ import annotations

import ast
import inspect
import json
import tempfile
import unittest
from pathlib import Path

from se_harness import cli, release_qualification
from se_harness.installer import template_files, template_root
from tests.cli_support import invoke
from tests.fixture_support import standard_repository
from tests.root_identity_support import load_evaluator_module

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates" / "repository" / "standard"
ARTIFACT_TEMPLATES = TEMPLATES / "docs" / "engineering" / "templates"
EXPLORER_TEMPLATE = ROOT / "se_harness" / "engine" / "harness_explorer" / "index.template.html"

#: Paths a retirement deleted; a file reappearing under one of them is the retired path returning.
ABSENT_PATHS = (
    # WO-REB-028: the predecessor bootstrap path
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
    # WO-CIP-*: the publication rehearsal's digest declaration and script
    ".github/scripts/rehearse_publication.py",
    ".github/scripts/publication_rehearsal_mechanics.json",
    "tests/test_publication_rehearsal.py",
    # WO-REB-030: the interpreter-safety rule is code, never a declaration or a second loader
    "se_harness/interpreter_safety.json",
    "repository_tools/interpreter_safety.py",
)

#: Retired phrases and the one file each must stay out of.
ABSENT_TEXT: dict[str, tuple[str, ...]] = {
    # WO-REB-028, WO-ECP-010: retired operations and their options
    "se_harness/cli.py": ("predecessor-view", "--view-output", "rehearse-migration"),
    # WO-REB-030
    "pyproject.toml": ("interpreter_safety.json",),
    "se_harness/interpreter_safety.py": ("load_declaration", "declared_boundaries", "declared_corpus", "ISD1"),
    "scripts/check_portable_release_surface.py": ('"se_harness/interpreter_safety.json"',),
    # the one former holder of a guarded cross-package import keeps no residue of it
    "se_harness/release_qualification.py": ("repository_tools", "ImportError", "lazily imported"),
    # WO-REB-031, the migration scenario: no acceptance-contract output or env exists anywhere
    ".github/workflows/candidate-evidence.yml": ("migration_scenario", "acceptance_contract_sha256"),
    # the inspector composes the validator and the generator; it defines none of their functions
    "se_harness/engine/inspect_engineering_artifacts.py": ("def build_findings", "def validate_repository", "def _finding("),
    # reader-first templates (WO-TCM-006 to WO-TCM-009): the retired headings and fields
    "templates/repository/standard/docs/engineering/templates/REQUIREMENT.template.md": ("Open decisions", "acceptance/"),
    "templates/repository/standard/docs/engineering/templates/CAPABILITY.template.md": tuple(
        f"## {heading}" for heading in ("Capability statement", "Boundaries", "Outcomes", "Candidate requirements", "Derived requirements", "Open decisions")
    ),
    "templates/repository/standard/docs/engineering/templates/INTENT.template.md": tuple(
        f"## {heading}" for heading in ("Desired outcomes", "Actors and stakeholders", "Principles and immutable constraints", "Risks and assumptions", "Non-goals", "Open decisions")
    ),
    "templates/repository/standard/docs/engineering/templates/SPECIFICATION.template.md": (
        *(
            f"## {heading}"
            for heading in (
                "Actors and external systems", "Inputs", "Outputs", "State model", "Behavioral rules", "Data and interface contracts",
                "Security and privacy properties", "Performance and capacity", "Observability", "Compatibility and migration",
                "Explicitly unspecified decisions", "Open decisions",
            )
        ),
        "Number rules",
    ),
    # RSK-MGT-011: no configuration key governs the raise
    "templates/repository/standard/.engineering-harness.toml.tpl": ("[risk",),
    # WO-WEX-011: the handoff policy names no verbatim block
    "templates/repository/standard/ENGINEERING_HARNESS.md.tpl": ("block verbatim", "restitution verbatim"),
    "templates/repository/standard/docs/engineering/WORKFLOW.md": ("block verbatim", "restitution verbatim"),
    "templates/repository/standard/AGENTS.md.fragment": ("block verbatim", "restitution verbatim"),
    "templates/repository/standard/CLAUDE.md.fragment": ("block verbatim", "restitution verbatim"),
    # ECP-CTX-007 as amended under WO-ECP-020: nothing names next or accept-candidate as a command
    "templates/repository/standard/docs/engineering/WORKFLOW.md": ("harnessctl next",),
    "docs/notes/harnessctl-reference.md": ("| `next` |", "harnessctl next [", "| `accept-candidate` |", "harnessctl accept-candidate"),
    "docs/notes/harnessctl-check.md": ("harnessctl next",),
    # the designed Explorer (WO-DPB-*): the phrases of the prototype it replaced
    "se_harness/engine/harness_explorer/index.template.html": (
        'data-od-id="definition-coverage"',
        'id="coverageRows"',
        '$("coverageRows")',
        "function neighborhood(root,maxDepth=2,maxNodes=9)",
        "function setLineageZoom",
        'data-od-id="zoom-in"',
        "current.scrollIntoView",
        "decodeURIComponent(parts[1])",
        "decodeURIComponent(parts[2])",
        "Why does this exist?",
        "Is the definition covered?",
        "What needs reassessment?",
        "What is inconsistent or unassessable?",
        "Does the harness help?",
        "const artifactTypes",
        "switch(node.type)",
        "Math.abs(hash)%semanticPalette.length",
    ),
}

#: Retired phrases scanned over a set of files, with the files history permits to keep them.
#: (label, files, phrases, permitted holders)
ABSENT_TEXT_IN_FILES: tuple[tuple[str, tuple[Path, ...], tuple[str, ...], frozenset[str]], ...]


def _python_sources(*trees: str) -> tuple[Path, ...]:
    found: list[Path] = []
    for tree in trees:
        root = ROOT / tree
        if root.exists():
            found.extend(sorted(root.rglob("*.py")))
    return tuple(found)


def _sources(*trees: str, suffixes: frozenset[str]) -> tuple[Path, ...]:
    found: list[Path] = []
    for tree in trees:
        root = ROOT / tree
        if not root.exists():
            continue
        found.extend(path for path in sorted(root.rglob("*")) if path.is_file() and path.suffix in suffixes)
    return tuple(found)


def _markdown_outside(*excluded: str) -> tuple[Path, ...]:
    return tuple(
        path
        for path in sorted(ROOT.rglob("*.md"))
        if not path.relative_to(ROOT).as_posix().startswith(excluded) and ".venv" not in path.relative_to(ROOT).as_posix()
    )


#: Files history permits to name the retired repository-context path (WO-DST-021, WO-ADS-002), with the reason.
REPOSITORY_CONTEXT_MENTIONS = {
    "docs/engineering/agent-directive-surface/evidence/WO-ADS-001/WO-ADS-001-verification.md": "retained evidence naming the file it left untouched",
    "docs/engineering/agent-directive-surface/evidence/WO-ADS-002/WO-ADS-002-verification.md": "retained evidence for this retirement",
    "docs/engineering/agent-directive-surface/work-orders/WO-ADS-001.md": "work order whose execution scope names the retained file",
    "docs/engineering/agent-directive-surface/requirements/REQ-ADS-007.md": "draft requirement that retires the file",
    "docs/engineering/agent-directive-surface/specifications/SPEC-ADS-002.md": "draft specification of the retirement",
    "docs/engineering/agent-directive-surface/work-orders/WO-ADS-002.md": "draft work order whose execution scope names the file it removes",
    "docs/engineering/harness-distribution/README.md": "packet index recording the retirement",
    "docs/engineering/harness-distribution/evidence/WO-DST-021-verification.md": "retained evidence for this retirement",
    "docs/engineering/harness-distribution/evidence/WO-DOC-007-verification.md": "historical evidence",
    "docs/engineering/harness-distribution/evidence/WO-DOC-009-verification.md": "historical evidence",
    "docs/engineering/harness-distribution/evidence/WO-DOC-013-verification.md": "historical evidence",
    "docs/engineering/harness-distribution/requirements/REQ-DST-008.md": "superseded requirement retained as history",
    "docs/engineering/harness-distribution/requirements/REQ-DST-065.md": "the retiring requirement",
    "docs/engineering/harness-distribution/specifications/SPEC-DST-021.md": "the retiring specification",
    "docs/engineering/harness-distribution/work-orders/WO-DOC-007.md": "historical work order",
    "docs/engineering/harness-distribution/work-orders/WO-DOC-009.md": "historical work order",
    "docs/engineering/harness-distribution/work-orders/WO-DST-021.md": "the retiring work order",
    "docs/engineering/instruction-architecture/README.md": "packet index recording the retirement",
    "docs/engineering/instruction-architecture/evidence/WO-DST-021-verification.md": "retained evidence for this retirement",
    "docs/engineering/instruction-architecture/evidence/WO-IAR-012-verification.md": "retained evidence for the owner-region revision",
    "docs/engineering/instruction-architecture/requirements/REQ-IAR-005.md": "superseded requirement retained as history",
    "docs/engineering/instruction-architecture/requirements/REQ-IAR-020.md": "owner-region requirement, ordinary owner content only",
    "docs/engineering/instruction-architecture/requirements/REQ-IAR-021.md": "the routing requirement",
    "docs/engineering/instruction-architecture/specifications/SPEC-IAR-012.md": "owner-region contract, ordinary owner content only",
    "docs/engineering/instruction-architecture/verification/VER-IAR-012.md": "owner-region verification contract",
    "docs/engineering/instruction-architecture/work-orders/WO-IAR-012.md": "owner-region work order",
    "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-001-verification.md": "historical evidence",
    "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-001.md": "historical work order",
    "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-002.md": "approved root-upgrade scope names the owner context path",
    "docs/engineering/release-orchestration/work-orders/WO-RLO-004.md": "approved execution scope names the owner context path",
    "docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-010.md": "names this repository's own owner context file as an affected operator path",
    "docs/engineering/released-evaluator-boundary/evidence/WO-REB-005-verification.md": "retained released-0.5 preflight evidence",
    "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-023.md": "names this repository's own owner context file as an affected operator path",
    "docs/engineering/self-hosting-boundary/work-orders/WO-SHB-001.md": "historical work order",
    "docs/engineering/verification-supersession/engineering-README.md": "historical domain note",
    "docs/engineering/work-order-assurance-classification/evidence/WO-WAC-001-verification.md": "historical evidence",
    "docs/engineering/workflow-execution/evidence/WO-WEX-002-verification.md": "historical evidence",
    "docs/engineering/workflow-execution/work-orders/WO-WEX-002.md": "historical work order",
    "docs/notes/harness-migration-repository-context-retirement.md": "migration note describing the retirement",
}

#: The root copy of the validator alone kept a retired schema name; since the 0.16.0 root no copy exists.
ROOT_VALIDATOR = "scripts/validate_engineering_artifacts.py"

ABSENT_TEXT_IN_FILES = (
    (
        "WO-DST-021: no package module reads the retired repository-context path",
        _python_sources("se_harness"),
        ("REPOSITORY_CONTEXT", "CTX-ACT-", "repository_commands", "repository_context"),
        frozenset(),
    ),
    (
        "RSK-MGT-011: no package module reads a risk threshold",
        _python_sources("se_harness"),
        ("raise_threshold", "acceptance_level"),
        frozenset(),
    ),
    (
        "ARCH-REB-012: nothing reconstructs a predecessor view",
        _python_sources("se_harness", "repository_tools", "scripts", ".github/scripts"),
        ("sparse-checkout", "--sparse", "predecessor view"),
        frozenset(),
    ),
    (
        "WO-REB-028: the retired check codes are reserved by their declaration and emitted by no path",
        _python_sources("se_harness", "repository_tools", "scripts", ".github/scripts"),
        release_qualification.RETIRED_CHECK_CODES,
        frozenset({"se_harness/release_qualification.py"}),
    ),
    (
        "WO-REB-028: a retired schema name appears only in retained history",
        _sources("se_harness", "repository_tools", "scripts", ".github", "templates", suffixes=frozenset({".py", ".json", ".yml", ".md"})),
        ("se-harness-release-bootstrap-v1", "se-harness-predecessor-bootstrap-v1", "se-harness-predecessor-view-exclusion/v1"),
        frozenset({ROOT_VALIDATOR}),
    ),
    (
        "WO-REB-025: the exclusion observation schema was never written",
        _sources("se_harness", "repository_tools", "scripts", ".github", "templates", suffixes=frozenset({".py", ".json", ".yml", ".md"})),
        ("se-harness-predecessor-view-exclusion",),
        frozenset(),
    ),
    (
        "WO-DST-021: only recorded files name the retired repository-context path",
        _markdown_outside("target/", "tests/", "templates/"),
        ("REPOSITORY_CONTEXT",),
        frozenset(REPOSITORY_CONTEXT_MENTIONS),
    ),
    (
        "SPEC-DST-006: the expertise label is a comment, never the old block-quote marker",
        (*sorted((ROOT / "docs" / "notes").glob("*.md")), ROOT / "README.md", ROOT / "GLOSSARY.md"),
        ("> **Target expertise:",),
        frozenset(),
    ),
)

#: WO-REB-028: module names no retained Python file may import, at any import level, and the trees scanned.
DELETED_MODULES = ("release_bootstrap", "predecessor_preparation", "predecessor_publication", "predecessor_assessment")
SCANNED_TREES = ("se_harness", "repository_tools", "scripts", ".github/scripts", "tests", "templates")

#: WO-REB-029: every name deleted from the validator, absent from its text and from the loaded module.
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

#: WO-DST-021: the retired owner-context scaffold, its lock entry and its field labels, as the
#: released 0.5.0 baseline recorded them.
CONTEXT_BASELINE = json.loads((ROOT / "tests" / "fixtures" / "repository_context_retirement" / "released-baseline.json").read_text(encoding="utf-8"))
RETIRED_CONTEXT_PATH = CONTEXT_BASELINE["retired_path"]
RETIRED_CONTEXT_LABELS = tuple(CONTEXT_BASELINE["retired_field_labels"])

#: Retired command-line options, absent from their command's help.
ABSENT_FROM_COMMAND_HELP = {
    "init": ("--profile",),
    "prepare-release": ("--distribution-manifest",),
}
#: Retired commands the top-level help no longer lists (ECP-TMB-001 to ECP-TMB-003, WO-ECP-025).
ABSENT_FROM_HELP = ("focus", " next ", "{next", ",next", "accept-candidate", "predecessor-view", "rehearse-migration", "renumber-artifacts", "rehearse-recovery")
#: Retired commands the parser refuses as it refuses any unknown command, with no guard of its own.
REFUSED_COMMANDS = ("focus", "next", "accept-candidate")
#: ECP-TMB-001 to ECP-TMB-003: the tombstone guards left `main()`; its source names none of these.
ABSENT_FROM_MAIN_SOURCE = ("focus", "next", "accept-candidate", "--authorized-by")


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


class RetiredSurfaceTests(unittest.TestCase):
    def test_retired_paths_are_absent(self) -> None:
        for relative in ABSENT_PATHS:
            with self.subTest(path=relative):
                self.assertFalse((ROOT / relative).exists(), f"the retired path {relative} is back")

    def test_retired_phrases_are_absent_from_their_files(self) -> None:
        for relative, phrases in ABSENT_TEXT.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            for phrase in phrases:
                with self.subTest(path=relative, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_retired_phrases_appear_only_where_history_permits(self) -> None:
        for label, files, phrases, permitted in ABSENT_TEXT_IN_FILES:
            self.assertTrue(files, f"{label}: the scan reached no file")
            for phrase in phrases:
                holders = {
                    path.relative_to(ROOT).as_posix()
                    for path in files
                    if phrase in path.read_text(encoding="utf-8", errors="ignore")
                }
                with self.subTest(retirement=label, phrase=phrase):
                    self.assertEqual(set(), holders - permitted)
            if permitted and len(phrases) == 1 and permitted == frozenset(REPOSITORY_CONTEXT_MENTIONS):
                # the permitted list is exact: a mention that left history is removed from it
                holders = {
                    path.relative_to(ROOT).as_posix()
                    for path in files
                    if phrases[0] in path.read_text(encoding="utf-8", errors="ignore")
                }
                self.assertEqual(sorted(permitted), sorted(holders))

    def test_no_retained_python_file_imports_a_retired_module(self) -> None:
        offenders: set[str] = set()
        scanned = 0
        for source in _python_sources(*SCANNED_TREES):
            scanned += 1
            for name in _imported_names(source):
                if name.split(".")[-1] in DELETED_MODULES:
                    offenders.add(f"{source.relative_to(ROOT).as_posix()}: {name}")
        self.assertEqual(set(), offenders)
        self.assertGreater(scanned, 100, "a scan that reached nothing would pass vacuously")

    def test_the_candidate_validator_carries_no_retired_name(self) -> None:
        # Absence in the text is not absence in the loaded module: a survivor reintroduced
        # through an import would not show up in a static read, so both are checked.
        path = ROOT / "se_harness/engine/validate_engineering_artifacts.py"
        text = path.read_text(encoding="utf-8")
        module = load_evaluator_module("validate_engineering_artifacts", directory=path.parent)
        for name in DELETED_VALIDATOR_NAMES:
            with self.subTest(name=name):
                self.assertNotIn(name, text)
                if name.isidentifier():
                    self.assertFalse(hasattr(module, name))
        for retained in ("validate_repository", "validate_revision_consistency", "WORKFLOW_LIFECYCLES"):
            with self.subTest(retained=retained):
                self.assertTrue(hasattr(module, retained))

    def test_no_template_maps_to_the_retired_context_path(self) -> None:
        self.assertNotIn(RETIRED_CONTEXT_PATH, [item.target.as_posix() for item in template_files()])
        for item in template_files():
            if item.mode != "seed":
                continue
            text = item.source.read_text(encoding="utf-8")
            for label in RETIRED_CONTEXT_LABELS:
                with self.subTest(seed=item.target.as_posix(), label=label):
                    self.assertNotIn(f"- {label}:", text)
        root = template_root()
        self.assertEqual([], sorted(path.relative_to(root).as_posix() for path in root.rglob("*CONTEXT*")))

    def test_a_fresh_installation_carries_no_retired_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "fresh"
            standard_repository(target)
            self.assertFalse((target / RETIRED_CONTEXT_PATH).exists())
            lock = (target / ".engineering-harness.lock").read_text(encoding="utf-8")
            self.assertNotIn(RETIRED_CONTEXT_PATH, lock)

    def test_the_command_line_lists_no_retired_option_or_command(self) -> None:
        for command, options in ABSENT_FROM_COMMAND_HELP.items():
            _, help_text, _ = invoke(command, "--help")
            for option in options:
                with self.subTest(command=command, option=option):
                    self.assertNotIn(option, help_text)
        _, help_text, _ = invoke("--help")
        for retired in ABSENT_FROM_HELP:
            with self.subTest(retired=retired):
                self.assertNotIn(retired, help_text)
        with tempfile.TemporaryDirectory() as temporary:
            for command in REFUSED_COMMANDS:
                with self.subTest(command=command):
                    code, output, error = invoke(command, temporary, "--artifact", "WO-001", "--json")
                    self.assertEqual((2, ""), (code, output))
                    self.assertIn("invalid choice", error)
                    self.assertNotIn("was removed", error)
        # A product-source read that names its rule (SPEC-TST-002 TST-HYG-011): ECP-TMB-001 to
        # ECP-TMB-003 retired the guards from main(), so the function's source names none of them.
        source = inspect.getsource(cli.main)
        for retired in ABSENT_FROM_MAIN_SOURCE:
            with self.subTest(retired=retired):
                self.assertNotIn(retired, source)
