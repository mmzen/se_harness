"""Independent verification of the declared environment entry-point safety rule.

The corpus below is owned by these tests as data and is compared against
``se_harness/interpreter_safety.json`` in both directions, so neither the
declaration nor either loader can define its own passing condition. Every
filesystem form is built for real; digests are recomputed here from the bytes
these tests wrote rather than read back from the observation under test.
"""

from __future__ import annotations

import ast
import contextlib
import hashlib
import json
import os
import platform
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from repository_tools import interpreter_safety as tools_safety
from se_harness import governance_migration, interpreter_safety, runtime_identity


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WINDOWS = os.name == "nt"
PLATFORM = "windows" if WINDOWS else "linux"

#: Every module that reaches the declared rule directly, mapped to the boundary
#: identifiers the registry must carry for it. Produced by reading the two
#: packages rather than by reading the declaration. `WO-REB-028` retired the six
#: sites of the predecessor-bootstrap release path, so the two survivors are the
#: migration runtime probe and the runtime-identity entry-point observation, and
#: no module delegates.
EXPECTED_RULE_BOUNDARIES = {
    "se_harness/governance_migration.py": 1,
    "se_harness/runtime_identity.py": 1,
}
EXPECTED_DELEGATING_BOUNDARIES: dict[str, int] = {}

#: The complete set of ``se_harness`` names ``repository_tools`` may import, as a
#: pinned exhaustive inventory rather than a prefix rule. `WO-REB-028` deleted the
#: last holder of the pre-existing ``se_harness.hash_bound`` crossing that arrived
#: with ``WO-HBI-002``, so the inventory is now empty. Any new crossing fails this
#: check by name.
PERMITTED_PACKAGE_IMPORTS: frozenset[str] = frozenset()

#: The complete set of ``repository_tools`` names ``se_harness`` may import, as a
#: pinned exhaustive inventory. `WO-REB-028` retired `qualify_predecessor_view`,
#: the one function that reached a `repository_tools` service through a guarded
#: function-local import, so the package no longer names that package at all.
PERMITTED_TOOLS_IMPORTS: frozenset[str] = frozenset()

#: Patterns `ARCH-REB-010` prohibits, each with the module set allowed to carry
#: it. `interpreter_safety` itself is the one place link classification lives.
LOADER_MODULES = frozenset(
    {"se_harness/interpreter_safety.py", "repository_tools/interpreter_safety.py"}
)

#: Boundary-module functions that still test for a junction inline, mapped to the
#: reason that use is not a restatement of the declared interpreter rule. Pinned as
#: an exhaustive inventory: a new inline junction test anywhere in a boundary module
#: fails the check by name. `WO-REB-028` deleted the one retained walker with the
#: module that held it.
RETAINED_INLINE_JUNCTION_FUNCTIONS: dict[str, dict[str, str]] = {}

#: Boundary-module expressions that legitimately derive a directory two levels
#: above a path, mapped to the subject each one names. None of these subjects is
#: an interpreter, so none of them derives an environment root from a resolved
#: interpreter target, which is what `ARCH-REB-010` prohibits.
RETAINED_GRANDPARENT_DERIVATIONS = {
    "se_harness/runtime_identity.py": ("Path(__file__).parent.parent",),
}

#: Substrings that mark an expression or argument as naming an interpreter.
INTERPRETER_NAME_MARKERS = ("python", "interpreter", "executable")


def _functions_naming(tree: ast.AST, name: str) -> set[str]:
    """Names of the functions whose body mentions ``name``.

    Both spellings count: an attribute access and the string literal a
    ``getattr`` or ``hasattr`` probe would carry.
    """

    found: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for inner in ast.walk(node):
            if isinstance(inner, ast.Attribute) and inner.attr == name:
                found.add(node.name)
            elif isinstance(inner, ast.Constant) and inner.value == name:
                found.add(node.name)
    return found


def _calls_to(tree: ast.AST, name: str) -> list[ast.Call]:
    """Every call of the plain function ``name`` in one module."""

    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == name
    ]


def _grandparent_derivations(tree: ast.AST) -> set[str]:
    """Every ``<something>.parent.parent`` expression in one module."""

    found: set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Attribute)
            and node.attr == "parent"
            and isinstance(node.value, ast.Attribute)
            and node.value.attr == "parent"
        ):
            found.add(ast.unparse(node))
    return found


def _symlink_available() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        target = base / "target"
        target.write_bytes(b"target\n")
        try:
            (base / "link").symlink_to(target)
        except (OSError, NotImplementedError) as exc:
            return False, f"this host cannot create a symbolic link: {exc}"
    return True, ""


def _junction_available() -> tuple[bool, str]:
    if not WINDOWS:
        return False, "directory junctions are a Windows reparse-point construct"
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        (base / "real").mkdir()
        completed = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(base / "link"), str(base / "real")],
            check=False,
            capture_output=True,
        )
        if completed.returncode != 0 or not (base / "link").exists():
            return False, "this host refused mklink /J"
    return True, ""


SYMLINK_OK, SYMLINK_REASON = _symlink_available()
JUNCTION_OK, JUNCTION_REASON = _junction_available()


def _junction(link: Path, target: Path) -> None:
    completed = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(link), str(target)],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise unittest.SkipTest(f"mklink /J failed: {completed.stderr!r}")


class _Fixture:
    """A base directory holding real environments, checkouts, and link forms."""

    def __init__(self, base: Path) -> None:
        self.base = base
        self.payload = b"#!/not-a-real-interpreter\n" + bytes(range(256))
        self.digest = hashlib.sha256(self.payload).hexdigest()

    def environment(self, name: str, *, leaf: str = "python") -> Path:
        root = self.base / name
        binary_directory = root / ("Scripts" if WINDOWS else "bin")
        binary_directory.mkdir(parents=True, exist_ok=True)
        entry = binary_directory / leaf
        entry.write_bytes(self.payload)
        return entry


class DeclarationShapeTests(unittest.TestCase):
    def test_declaration_parses_under_its_schema_from_both_loaders(self) -> None:
        for loader in (interpreter_safety, tools_safety):
            with self.subTest(loader=loader.__name__):
                declaration = loader.load_declaration()
                self.assertEqual(loader.DECLARATION_SCHEMA, declaration["schema"])

    def test_both_loaders_read_identical_declaration_bytes(self) -> None:
        self.assertEqual(interpreter_safety.declaration_bytes(), tools_safety.declaration_bytes())

    def test_both_loaders_agree_on_every_declared_structure(self) -> None:
        self.assertEqual(interpreter_safety.load_declaration(), tools_safety.load_declaration())
        self.assertEqual(interpreter_safety.EVALUATION_ORDER, tools_safety.EVALUATION_ORDER)
        self.assertEqual(interpreter_safety.POSITION_CLASSES, tools_safety.POSITION_CLASSES)

    def test_declaration_is_data_only_and_carries_no_waiver(self) -> None:
        declaration = interpreter_safety.load_declaration()
        prohibited = {"waiver", "waivers", "allowlist", "allow_list", "exception", "exceptions",
                      "bypass", "override", "code", "eval", "expression", "platform_conditional"}

        def walk(value: object, trail: str) -> None:
            if isinstance(value, dict):
                for key, item in value.items():
                    self.assertNotIn(
                        key.lower(), prohibited, f"{trail}: prohibited declaration key {key!r}"
                    )
                    walk(item, f"{trail}.{key}")
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    walk(item, f"{trail}[{index}]")
            else:
                self.assertIsInstance(value, (str, int, float, bool, type(None)), trail)

        walk(declaration, "declaration")

    def test_declaration_rejects_a_duplicate_key(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "declaration.json"
            path.write_text('{"schema": "a", "schema": "b"}', encoding="utf-8")
            with self.assertRaisesRegex(interpreter_safety.InterpreterSafetyError, "ISD101"):
                interpreter_safety.load_declaration(path)

    def test_declaration_rejects_an_unknown_case_identifier(self) -> None:
        declaration = interpreter_safety.load_declaration()
        declaration["cases"][0]["id"] = "XYZ001"
        with self._written(declaration) as path:
            with self.assertRaisesRegex(interpreter_safety.InterpreterSafetyError, "ISD114"):
                interpreter_safety.load_declaration(path)

    def test_declaration_rejects_a_malformed_corpus_entry(self) -> None:
        declaration = interpreter_safety.load_declaration()
        declaration["corpus"][0]["expected"] = "EPS999"
        with self._written(declaration) as path:
            with self.assertRaisesRegex(interpreter_safety.InterpreterSafetyError, "ISD129"):
                interpreter_safety.load_declaration(path)

    def test_declaration_rejects_a_reordered_case_list(self) -> None:
        declaration = interpreter_safety.load_declaration()
        declaration["cases"].reverse()
        with self._written(declaration) as path:
            with self.assertRaisesRegex(interpreter_safety.InterpreterSafetyError, "ISD117"):
                interpreter_safety.load_declaration(path)

    def test_declaration_rejects_a_declared_case_with_no_corpus_entry(self) -> None:
        declaration = interpreter_safety.load_declaration()
        declaration["corpus"] = [
            entry for entry in declaration["corpus"] if entry["expected"] != "EPS009"
        ]
        with self._written(declaration) as path:
            with self.assertRaisesRegex(interpreter_safety.InterpreterSafetyError, "ISD135"):
                interpreter_safety.load_declaration(path)

    def test_declaration_rejects_an_unsorted_boundary_registry(self) -> None:
        declaration = interpreter_safety.load_declaration()
        declaration["boundaries"].reverse()
        with self._written(declaration) as path:
            with self.assertRaisesRegex(interpreter_safety.InterpreterSafetyError, "ISD124"):
                interpreter_safety.load_declaration(path)

    @contextlib.contextmanager
    def _written(self, declaration: dict[str, object]):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "declaration.json"
            path.write_text(json.dumps(declaration, indent=2), encoding="utf-8")
            yield path


class BidirectionalCorpusTests(unittest.TestCase):
    """Neither side may define its own passing condition."""

    #: Test-owned expectation, written independently of the declaration.
    OWNED = {
        "ISC001": "accepted",
        "ISC002": "accepted",
        "ISC003": "accepted",
        "ISC004": "EPS001",
        "ISC005": "EPS002",
        "ISC006": "EPS003",
        "ISC007": "EPS003",
        "ISC008": "EPS004",
        "ISC009": "EPS004",
        "ISC010": "EPS005",
        "ISC011": "EPS006",
        "ISC012": "EPS007",
        "ISC013": "EPS008",
        "ISC014": "EPS009",
        "ISC015": "EPS010",
        "ISC016": "EPS011",
        "ISC017": "accepted",
        "ISC018": "accepted",
    }

    def test_every_declared_corpus_entry_is_owned_by_these_tests(self) -> None:
        declared = {entry["id"]: entry["expected"] for entry in interpreter_safety.declared_corpus()}
        self.assertEqual(sorted(self.OWNED), sorted(declared), "corpus identifiers diverge")
        for identifier, expected in sorted(self.OWNED.items()):
            with self.subTest(corpus=identifier):
                self.assertEqual(expected, declared[identifier])

    def test_every_declared_case_is_reachable_from_the_owned_corpus(self) -> None:
        declared = {entry["id"] for entry in interpreter_safety.declared_cases()}
        reached = set(self.OWNED.values()) - {"accepted"}
        self.assertEqual(sorted(declared), sorted(reached))

    def test_the_owned_case_set_equals_the_implemented_evaluation_order(self) -> None:
        self.assertEqual(
            sorted(interpreter_safety.EVALUATION_ORDER),
            sorted(set(self.OWNED.values()) - {"accepted"}),
        )

    def test_every_unconstructable_entry_records_a_reason(self) -> None:
        for entry in interpreter_safety.declared_corpus():
            with self.subTest(corpus=entry["id"]):
                if sorted(entry["constructable_on"]) != sorted(interpreter_safety.PLATFORMS):
                    self.assertIn("unconstructable_reason", entry)
                    self.assertTrue(entry["unconstructable_reason"].strip())


class RuleEvaluationTests(unittest.TestCase):
    """Build each corpus form for real and assert the outcome both loaders give."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = _Fixture(Path(self.temporary.name).resolve())
        self.declared = {
            entry["id"]: entry for entry in interpreter_safety.declared_corpus()
        }

    def _require(self, corpus_id: str) -> None:
        entry = self.declared[corpus_id]
        if PLATFORM not in entry["constructable_on"]:
            self.skipTest(f"{corpus_id} on {PLATFORM}: {entry.get('unconstructable_reason', '')}")

    def _both(self, path: Path | str, **kwargs: object) -> str | None:
        first = interpreter_safety.refusal_case(path, **kwargs)  # type: ignore[arg-type]
        second = tools_safety.refusal_case(path, **kwargs)  # type: ignore[arg-type]
        self.assertEqual(
            first,
            second,
            f"the two loaders disagree for {path!r}: se_harness={first} repository_tools={second}",
        )
        return first

    def test_isc001_ordinary_file_entry_is_accepted(self) -> None:
        self._require("ISC001")
        entry = self.fixture.environment("env")
        self.assertIsNone(self._both(entry))
        observed = interpreter_safety.evaluate(entry)
        self.assertEqual(entry, observed.entry_point)
        self.assertEqual(self.fixture.base / "env", observed.environment_root)
        self.assertFalse(observed.entry_is_link)
        self.assertEqual(self.fixture.digest, observed.binary_sha256)

    def test_isc002_terminal_symlink_entry_is_accepted_and_keeps_its_lexical_root(self) -> None:
        self._require("ISC002")
        if not SYMLINK_OK:
            self.skipTest(f"ISC002: {SYMLINK_REASON}")
        system = self.fixture.base / "system"
        system.mkdir()
        target = system / "python3.11"
        target.write_bytes(self.fixture.payload)
        root = self.fixture.base / "venv"
        (root / "bin").mkdir(parents=True)
        entry = root / "bin" / "python"
        entry.symlink_to(target)
        self.assertIsNone(self._both(entry))
        observed = interpreter_safety.evaluate(entry)
        self.assertEqual(entry, observed.entry_point)
        self.assertEqual(root, observed.environment_root, "the root must be lexical, not resolved")
        self.assertNotEqual(observed.entry_point, observed.resolved_target)
        self.assertTrue(observed.entry_is_link)
        self.assertEqual(self.fixture.digest, observed.binary_sha256)

    def test_isc003_hardlink_entry_is_accepted(self) -> None:
        self._require("ISC003")
        entry = self.fixture.environment("env")
        second = entry.with_name("python-hard")
        os.link(entry, second)
        self.assertIsNone(self._both(second))
        self.assertFalse(interpreter_safety.evaluate(second).entry_is_link)

    def test_isc004_symlink_parent_is_refused(self) -> None:
        self._require("ISC004")
        if not SYMLINK_OK:
            self.skipTest(f"ISC004: {SYMLINK_REASON}")
        entry = self.fixture.environment("real")
        alias = self.fixture.base / "alias"
        alias.symlink_to(self.fixture.base / "real", target_is_directory=True)
        self.assertEqual("EPS001", self._both(alias / entry.parent.name / entry.name))

    def test_isc005_junction_parent_is_refused(self) -> None:
        self._require("ISC005")
        if not JUNCTION_OK:
            self.skipTest(f"ISC005: {JUNCTION_REASON}")
        entry = self.fixture.environment("real")
        alias = self.fixture.base / "alias"
        _junction(alias, self.fixture.base / "real")
        self.assertFalse(alias.is_symlink(), "the junction must not be a symbolic link")
        attributes = os.lstat(alias)
        self.assertTrue(attributes.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
        self.assertEqual(stat.IO_REPARSE_TAG_MOUNT_POINT, attributes.st_reparse_tag)
        self.assertEqual("EPS002", self._both(alias / entry.parent.name / entry.name))

    def test_isc006_dangling_terminal_symlink_is_refused(self) -> None:
        self._require("ISC006")
        if not SYMLINK_OK:
            self.skipTest(f"ISC006: {SYMLINK_REASON}")
        root = self.fixture.base / "venv"
        (root / "bin").mkdir(parents=True)
        entry = root / "bin" / "python"
        entry.symlink_to(self.fixture.base / "absent" / "python")
        self.assertEqual("EPS003", self._both(entry))

    def test_isc007_absent_entry_is_refused(self) -> None:
        self._require("ISC007")
        self.assertEqual("EPS003", self._both(self.fixture.base / "env" / "bin" / "python"))

    def test_isc008_directory_entry_is_refused(self) -> None:
        self._require("ISC008")
        entry = self.fixture.base / "env" / "bin" / "python"
        entry.mkdir(parents=True)
        self.assertEqual("EPS004", self._both(entry))

    def test_isc009_terminal_junction_entry_is_refused(self) -> None:
        self._require("ISC009")
        if not JUNCTION_OK:
            self.skipTest(f"ISC009: {JUNCTION_REASON}")
        real = self.fixture.base / "real"
        real.mkdir()
        binary_directory = self.fixture.base / "env" / "Scripts"
        binary_directory.mkdir(parents=True)
        entry = binary_directory / "python.exe"
        _junction(entry, real)
        self.assertEqual("EPS004", self._both(entry))

    def test_isc012_entry_inside_the_checkout_is_refused(self) -> None:
        self._require("ISC012")
        checkout = self.fixture.base / "checkout"
        checkout.mkdir()
        entry = self.fixture.environment("checkout/.venv")
        self.assertEqual("EPS007", self._both(entry, checkout_root=checkout))
        self.assertIsNone(self._both(entry), "the refusal must need a supplied checkout root")

    def test_isc013_target_inside_the_checkout_is_refused(self) -> None:
        self._require("ISC013")
        if not SYMLINK_OK:
            self.skipTest(f"ISC013: {SYMLINK_REASON}")
        checkout = self.fixture.base / "checkout"
        checkout.mkdir()
        target = checkout / "python"
        target.write_bytes(self.fixture.payload)
        root = self.fixture.base / "venv"
        (root / "bin").mkdir(parents=True)
        entry = root / "bin" / "python"
        entry.symlink_to(target)
        self.assertEqual("EPS008", self._both(entry, checkout_root=checkout))

    def test_isc014_entry_outside_the_declared_root_is_refused(self) -> None:
        self._require("ISC014")
        entry = self.fixture.environment("first")
        self.assertEqual(
            "EPS009", self._both(entry, declared_root=self.fixture.base / "second")
        )
        self.assertIsNone(self._both(entry, declared_root=self.fixture.base / "first"))

    def test_isc015_rootless_entry_is_refused(self) -> None:
        self._require("ISC015")
        anchor = Path(self.fixture.base.anchor)
        self.assertEqual("EPS010", self._both(anchor / "python"))

    def test_isc016_a_runtime_without_either_predicate_route_refuses(self) -> None:
        self._require("ISC016")
        entry = self.fixture.environment("env")
        for loader in (interpreter_safety, tools_safety):
            with self.subTest(loader=loader.__name__):
                with mock.patch.object(loader, "link_classification_available", return_value=False):
                    self.assertEqual("EPS011", loader.refusal_case(entry))

    def test_isc017_relative_entry_is_accepted(self) -> None:
        self._require("ISC017")
        entry = self.fixture.environment("env")
        previous = Path.cwd()
        os.chdir(self.fixture.base)
        self.addCleanup(os.chdir, previous)
        relative = Path("env") / entry.parent.name / entry.name
        self.assertIsNone(self._both(relative))
        self.assertEqual(entry, interpreter_safety.evaluate(relative).entry_point)

    def test_isc018_parent_component_entry_is_accepted_without_dereferencing(self) -> None:
        self._require("ISC018")
        entry = self.fixture.environment("env")
        noisy = entry.parent / ".." / entry.parent.name / entry.name
        self.assertIsNone(self._both(noisy))
        observed = interpreter_safety.evaluate(noisy)
        self.assertEqual(entry, observed.entry_point)
        self.assertEqual(self.fixture.base / "env", observed.environment_root)

    def test_a_link_cycle_is_refused_rather_than_looping(self) -> None:
        if not SYMLINK_OK:
            self.skipTest(f"link cycle: {SYMLINK_REASON}")
        root = self.fixture.base / "venv"
        (root / "bin").mkdir(parents=True)
        first = root / "bin" / "python"
        second = root / "bin" / "python-other"
        first.symlink_to(second)
        second.symlink_to(first)
        self.assertEqual("EPS003", self._both(first))

    def test_a_resolution_loop_reported_as_a_runtime_error_is_refused(self) -> None:
        """Hold both loaders to `EPS003` when resolution reports a link cycle.

        Constructing the cycle needs a link privilege one lane lacks, and below
        Python 3.13 `Path.resolve` replaces the underlying `ELOOP` with a
        `RuntimeError`. Supplying that report directly covers the rule's own
        handling of it on either lane and at either version.
        """

        entry = self.fixture.environment("env")

        def loop(target: Path, strict: bool = False) -> Path:
            raise RuntimeError("Symlink loop from %r" % str(target))

        with mock.patch.object(Path, "resolve", loop):
            self.assertEqual("EPS003", self._both(entry))

    def test_a_deep_parent_chain_terminates_at_the_filesystem_root(self) -> None:
        deep = self.fixture.base
        for index in range(40):
            deep = deep / f"d{index}"
        deep.mkdir(parents=True)
        entry = deep / "bin"
        entry.mkdir()
        binary = entry / "python"
        binary.write_bytes(self.fixture.payload)
        self.assertIsNone(self._both(binary))

    def test_an_unreadable_target_is_refused_rather_than_recorded_as_a_null_digest(self) -> None:
        entry = self.fixture.environment("env")
        with mock.patch.object(
            Path, "open", side_effect=PermissionError("denied")
        ):
            with self.assertRaises(interpreter_safety.InterpreterSafetyRefusal) as caught:
                interpreter_safety.evaluate(entry)
        self.assertEqual("EPS004", caught.exception.case)

    def test_an_oversize_target_is_refused(self) -> None:
        entry = self.fixture.environment("env")
        with mock.patch.object(interpreter_safety, "MAX_INTERPRETER_BYTES", 4):
            with self.assertRaises(interpreter_safety.InterpreterSafetyRefusal) as caught:
                interpreter_safety.evaluate(entry)
        self.assertEqual("EPS004", caught.exception.case)

    def test_no_refusal_message_echoes_target_bytes_or_environment_values(self) -> None:
        os.environ["INTERPRETER_SAFETY_PROBE"] = "probe-secret-value"
        self.addCleanup(os.environ.pop, "INTERPRETER_SAFETY_PROBE", None)
        secret = b"a-credential-inside-the-interpreter"
        root = self.fixture.base / "env" / ("Scripts" if WINDOWS else "bin")
        root.mkdir(parents=True)
        entry = root / "python"
        entry.write_bytes(secret)
        with mock.patch.object(interpreter_safety, "MAX_INTERPRETER_BYTES", 4):
            with self.assertRaises(interpreter_safety.InterpreterSafetyRefusal) as caught:
                interpreter_safety.evaluate(entry)
        message = str(caught.exception)
        self.assertNotIn(secret.decode("utf-8"), message)
        self.assertNotIn("probe-secret-value", message)


class RecordedFactsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = _Fixture(Path(self.temporary.name).resolve())

    def test_position_class_is_within_expected_root_for_an_environment_internal_target(self) -> None:
        entry = self.fixture.environment("env")
        observed = interpreter_safety.evaluate(entry)
        self.assertEqual(interpreter_safety.WITHIN_EXPECTED_ROOT, observed.binary_position)

    def test_position_class_is_outside_declared_roots_for_an_external_target(self) -> None:
        if not SYMLINK_OK:
            self.skipTest(f"outside-declared-roots: {SYMLINK_REASON}")
        system = self.fixture.base / "system"
        system.mkdir()
        target = system / "python3.11"
        target.write_bytes(self.fixture.payload)
        root = self.fixture.base / "venv"
        (root / "bin").mkdir(parents=True)
        entry = root / "bin" / "python"
        entry.symlink_to(target)
        observed = interpreter_safety.evaluate(entry)
        self.assertEqual(interpreter_safety.OUTSIDE_DECLARED_ROOTS, observed.binary_position)

    def test_within_checkout_root_exists_but_is_unreachable_through_the_rule(self) -> None:
        self.assertIn(interpreter_safety.WITHIN_CHECKOUT_ROOT, interpreter_safety.POSITION_CLASSES)
        checkout = self.fixture.base / "checkout"
        checkout.mkdir()
        entry = self.fixture.environment("env")
        observed = interpreter_safety.evaluate(entry, checkout_root=checkout)
        self.assertNotEqual(interpreter_safety.WITHIN_CHECKOUT_ROOT, observed.binary_position)

    def test_the_digest_matches_a_digest_these_tests_compute(self) -> None:
        entry = self.fixture.environment("env")
        observed = interpreter_safety.evaluate(entry)
        self.assertEqual(
            hashlib.sha256(entry.read_bytes()).hexdigest(), observed.binary_sha256
        )

    def test_an_altered_binary_moves_the_recorded_digest(self) -> None:
        entry = self.fixture.environment("env")
        before = interpreter_safety.evaluate(entry).binary_sha256
        entry.write_bytes(self.fixture.payload + b"tampered")
        self.assertNotEqual(before, interpreter_safety.evaluate(entry).binary_sha256)

    def test_a_repointed_link_moves_the_recorded_target_and_digest(self) -> None:
        if not SYMLINK_OK:
            self.skipTest(f"repointed link: {SYMLINK_REASON}")
        system = self.fixture.base / "system"
        system.mkdir()
        first = system / "python-a"
        first.write_bytes(self.fixture.payload)
        second = system / "python-b"
        second.write_bytes(self.fixture.payload + b"other")
        root = self.fixture.base / "venv"
        (root / "bin").mkdir(parents=True)
        entry = root / "bin" / "python"
        entry.symlink_to(first)
        before = interpreter_safety.evaluate(entry)
        entry.unlink()
        entry.symlink_to(second)
        after = interpreter_safety.evaluate(entry)
        self.assertEqual(before.entry_point, after.entry_point)
        self.assertNotEqual(before.resolved_target, after.resolved_target)
        self.assertNotEqual(before.binary_sha256, after.binary_sha256)

    def test_facts_are_deterministic_across_runs_and_working_directories(self) -> None:
        entry = self.fixture.environment("env")
        first = interpreter_safety.evaluate(entry)
        previous = Path.cwd()
        os.chdir(self.fixture.base)
        self.addCleanup(os.chdir, previous)
        second = interpreter_safety.evaluate(entry)
        self.assertEqual(first, second)

    def test_normalized_origin_carries_no_drive_letter_backslash_or_user_directory(self) -> None:
        entry = self.fixture.environment("env")
        observed = interpreter_safety.evaluate(entry)
        origin = interpreter_safety.normalized_origin(observed)
        self.assertTrue(origin.startswith("<evaluator-root>/"))
        self.assertNotIn("\\", origin)
        self.assertNotIn(":", origin)
        self.assertNotIn(Path.home().name, origin)

class PurityAndCostTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = _Fixture(Path(self.temporary.name).resolve())

    def test_evaluation_mutates_nothing_under_the_environment(self) -> None:
        entry = self.fixture.environment("env")
        before = {
            item.relative_to(self.fixture.base).as_posix(): item.stat().st_mtime_ns
            for item in sorted(self.fixture.base.rglob("*"))
        }
        interpreter_safety.evaluate(entry)
        after = {
            item.relative_to(self.fixture.base).as_posix(): item.stat().st_mtime_ns
            for item in sorted(self.fixture.base.rglob("*"))
        }
        self.assertEqual(before, after)

    def test_evaluation_spawns_no_subprocess_and_opens_no_socket(self) -> None:
        entry = self.fixture.environment("env")
        with mock.patch.object(subprocess, "Popen", side_effect=AssertionError("spawned")):
            with mock.patch("socket.socket", side_effect=AssertionError("socket")):
                interpreter_safety.evaluate(entry)
                self.assertEqual("EPS003", interpreter_safety.refusal_case(entry.with_name("gone")))

    def test_the_entry_is_resolved_once_and_digested_once_per_observation(self) -> None:
        entry = self.fixture.environment("env")
        original_resolve = Path.resolve
        resolves: list[Path] = []

        def counting_resolve(self: Path, strict: bool = False) -> Path:
            resolves.append(self)
            return original_resolve(self, strict=strict)

        original_digest = interpreter_safety._digest
        digests: list[Path] = []

        def counting_digest(target: Path, supplied: bytes | None) -> str:
            digests.append(target)
            return original_digest(target, supplied)

        original_walk = interpreter_safety._traverses_link
        walks: list[tuple[Path, bool]] = []

        def counting_walk(path: Path, *, include_self: bool) -> Path | None:
            walks.append((path, include_self))
            return original_walk(path, include_self=include_self)

        with mock.patch.object(Path, "resolve", counting_resolve):
            with mock.patch.object(interpreter_safety, "_digest", counting_digest):
                with mock.patch.object(interpreter_safety, "_traverses_link", counting_walk):
                    observed = interpreter_safety.evaluate(entry)

        self.assertEqual([entry], [item for item in resolves if item == entry])
        self.assertEqual([observed.resolved_target], digests)
        self.assertEqual([(entry, False), (observed.resolved_target, True)], walks)

    def test_the_first_refusal_wins_regardless_of_a_second_matching_form(self) -> None:
        if not SYMLINK_OK:
            self.skipTest(f"first-refusal-wins: {SYMLINK_REASON}")
        checkout = self.fixture.base / "checkout"
        checkout.mkdir()
        alias = checkout / "alias"
        real = self.fixture.base / "real"
        self.fixture.environment("real")
        alias.symlink_to(real, target_is_directory=True)
        # Both EPS001 (symbolic-link parent) and EPS007 (inside the checkout)
        # match; the declared order makes EPS001 the stable identifier.
        self.assertEqual(
            "EPS001",
            interpreter_safety.refusal_case(
                alias / ("Scripts" if WINDOWS else "bin") / "python", checkout_root=checkout
            ),
        )

    def test_the_environment_root_never_depends_on_the_resolved_target(self) -> None:
        if not SYMLINK_OK:
            self.skipTest(f"lexical root: {SYMLINK_REASON}")
        system = self.fixture.base / "system" / "deep" / "elsewhere"
        system.mkdir(parents=True)
        target = system / "python3.11"
        target.write_bytes(self.fixture.payload)
        root = self.fixture.base / "venv"
        (root / "bin").mkdir(parents=True)
        entry = root / "bin" / "python"
        entry.symlink_to(target)
        self.assertEqual(root, interpreter_safety.evaluate(entry).environment_root)


ABSENT_PREDICATE = "is_junction_withdrawn_for_conformance"
ABSENT_REPARSE_CONSTANTS = (
    "FILE_ATTRIBUTE_REPARSE_POINT_WITHDRAWN",
    "IO_REPARSE_TAG_MOUNT_POINT_WITHDRAWN",
)
#: A stat-result member no runtime carries. Naming it withdraws the
#: reparse-observability route on a platform whose stat result does carry
#: reparse information.
ABSENT_REPARSE_STAT_MEMBERS = ("st_file_attributes_withdrawn_for_conformance",)
#: A stat-result member every runtime carries. Naming it supplies that route on a
#: platform whose stat result reports no reparse information, so a lane can
#: construct the combination its own runtime cannot produce.
PRESENT_REPARSE_STAT_MEMBERS = ("st_mode",)
#: A `pathlib.Path` attribute and two `stat` constants every runtime carries.
#: The capability function probes only for their presence, so naming them
#: supplies the corresponding route on a runtime that lacks the real one. They
#: are used by the route-matrix test alone, which never classifies a real path.
PRESENT_PATHLIB_PREDICATE = "is_dir"
PRESENT_REPARSE_CONSTANTS = ("S_IFDIR", "S_IFREG")


@contextlib.contextmanager
def _without_routes(
    loader: object,
    *,
    pathlib_route: bool,
    stat_route: bool,
    reparse_observable: bool | None = None,
):
    """Withdraw a junction-detection route from a loader for one block.

    Each route is named by a module constant, so withdrawing one is a matter of
    pointing that constant at a name the runtime does not carry. Nothing is
    monkey-patched inside `stat`, `os` or `pathlib`, so the withdrawal cannot
    leak. `reparse_observable` left as `None` keeps the running runtime's own
    answer for the third route; setting it withdraws or supplies that route, so
    either lane can construct the combination it cannot produce itself.
    """

    patches = []
    if not pathlib_route:
        patches.append(mock.patch.object(loader, "JUNCTION_PREDICATE", ABSENT_PREDICATE))
    if not stat_route:
        patches.append(mock.patch.object(loader, "REPARSE_CONSTANTS", ABSENT_REPARSE_CONSTANTS))
    if reparse_observable is not None:
        patches.append(
            mock.patch.object(
                loader,
                "REPARSE_STAT_MEMBERS",
                PRESENT_REPARSE_STAT_MEMBERS
                if reparse_observable
                else ABSENT_REPARSE_STAT_MEMBERS,
            )
        )
    with contextlib.ExitStack() as stack:
        for item in patches:
            stack.enter_context(item)
        yield


@contextlib.contextmanager
def _routes(loader: object, *, pathlib_route: bool, stat_route: bool, reparse_observable: bool):
    """Pin all three named routes present or absent, whatever this runtime has.

    `_without_routes` can only take a route away, so on any one lane it reaches
    the combinations below that lane's own capabilities. This manager pins each
    route to a name the runtime either does or does not carry, so every
    combination in the decision table is constructable on every lane. It is used
    only to exercise the capability decision, never to classify a real path: the
    substituted names are probed for presence and are not read as reparse data.
    """

    with contextlib.ExitStack() as stack:
        stack.enter_context(
            mock.patch.object(
                loader,
                "JUNCTION_PREDICATE",
                PRESENT_PATHLIB_PREDICATE if pathlib_route else ABSENT_PREDICATE,
            )
        )
        stack.enter_context(
            mock.patch.object(
                loader,
                "REPARSE_CONSTANTS",
                PRESENT_REPARSE_CONSTANTS if stat_route else ABSENT_REPARSE_CONSTANTS,
            )
        )
        stack.enter_context(
            mock.patch.object(
                loader,
                "REPARSE_STAT_MEMBERS",
                PRESENT_REPARSE_STAT_MEMBERS
                if reparse_observable
                else ABSENT_REPARSE_STAT_MEMBERS,
            )
        )
        yield


class JunctionPredicateTests(unittest.TestCase):
    """`SPEC-REB-011` rule 4 as amended: three routes, any one sufficient.

    ``pathlib.Path.is_junction`` exists only from Python 3.12 while every
    supported lane pins 3.11, so the reparse-point ``stat`` route must carry the
    predicate there. That route rests on constants the platform publishes only
    where it defines them, so a pre-3.12 runtime on a filesystem that reports no
    reparse information has neither route and nothing for either to classify;
    there the predicate answers ``False`` by construction. These tests exercise
    each route in isolation and prove that only an unclassifiable reparse point
    refuses.
    """

    def test_both_loaders_report_the_capability_on_this_runtime(self) -> None:
        self.assertTrue(interpreter_safety.link_classification_available())
        self.assertTrue(tools_safety.link_classification_available())

    def test_at_least_one_route_is_present_on_every_supported_runtime(self) -> None:
        pathlib_route = hasattr(Path, "is_junction")
        stat_route = all(
            hasattr(stat, name)
            for name in ("FILE_ATTRIBUTE_REPARSE_POINT", "IO_REPARSE_TAG_MOUNT_POINT")
        )
        reparse_observable = all(
            hasattr(os.stat_result, name) for name in ("st_file_attributes", "st_reparse_tag")
        )
        self.assertTrue(
            pathlib_route or stat_route or not reparse_observable,
            f"no route decides the predicate on {platform.python_version()} / {PLATFORM}",
        )
        if sys.version_info < (3, 12):
            self.assertFalse(pathlib_route, "3.11 must not expose the pathlib route")
            if reparse_observable:
                self.assertTrue(
                    stat_route,
                    "a pre-3.12 runtime that observes reparse information must carry "
                    "the predicate through stat",
                )

    def test_the_stat_route_alone_reports_the_capability(self) -> None:
        for loader in (interpreter_safety, tools_safety):
            with self.subTest(loader=loader.__name__):
                with _routes(
                    loader, pathlib_route=False, stat_route=True, reparse_observable=True
                ):
                    self.assertTrue(loader.link_classification_available())

    def test_the_pathlib_route_alone_reports_the_capability(self) -> None:
        for loader in (interpreter_safety, tools_safety):
            with self.subTest(loader=loader.__name__):
                with _routes(
                    loader, pathlib_route=True, stat_route=False, reparse_observable=True
                ):
                    self.assertTrue(loader.link_classification_available())

    def test_an_unobservable_reparse_surface_alone_reports_the_capability(self) -> None:
        """The Python 3.11 POSIX combination: neither predicate route, no junction.

        This is the combination every supported lane below 3.12 reaches off
        Windows. Both predicate routes are absent there, so a capability rule
        that consulted only those two would refuse every interpreter on the
        pinned lane. The third route decides it instead.
        """

        for loader in (interpreter_safety, tools_safety):
            with self.subTest(loader=loader.__name__):
                with _routes(
                    loader, pathlib_route=False, stat_route=False, reparse_observable=False
                ):
                    self.assertTrue(loader.link_classification_available())

    def test_the_capability_decision_covers_every_route_combination(self) -> None:
        """The whole decision table, constructed on whatever lane runs it.

        Written as a test-owned expectation rather than by calling the loader
        twice: the capability holds unless reparse information is observable
        while neither predicate route can classify it.
        """

        owned = {
            (True, True, True): True,
            (True, True, False): True,
            (True, False, True): True,
            (True, False, False): True,
            (False, True, True): True,
            (False, True, False): True,
            (False, False, True): False,
            (False, False, False): True,
        }
        for (pathlib_route, stat_route, reparse_observable), expected in sorted(owned.items()):
            for loader in (interpreter_safety, tools_safety):
                with self.subTest(
                    loader=loader.__name__,
                    pathlib_route=pathlib_route,
                    stat_route=stat_route,
                    reparse_observable=reparse_observable,
                ):
                    with _routes(
                        loader,
                        pathlib_route=pathlib_route,
                        stat_route=stat_route,
                        reparse_observable=reparse_observable,
                    ):
                        self.assertEqual(expected, loader.link_classification_available())

    def test_reparse_observability_is_reported_from_the_stat_result_members(self) -> None:
        for loader in (interpreter_safety, tools_safety):
            with self.subTest(loader=loader.__name__):
                self.assertEqual(
                    all(
                        hasattr(os.stat_result, name)
                        for name in ("st_file_attributes", "st_reparse_tag")
                    ),
                    loader.reparse_information_observable(),
                )
                with _without_routes(
                    loader, pathlib_route=True, stat_route=True, reparse_observable=False
                ):
                    self.assertFalse(loader.reparse_information_observable())
                with _without_routes(
                    loader, pathlib_route=True, stat_route=True, reparse_observable=True
                ):
                    self.assertTrue(loader.reparse_information_observable())

    def test_the_capability_rule_names_no_platform(self) -> None:
        """`REQ-REB-024`: detection shall not depend on the platform name.

        The third route is a capability observation on the runtime's own stat
        result, not a platform test, and this asserts that mechanically over the
        source of both loaders rather than trusting the docstring that says so.
        """

        markers = ("os.name", "sys.platform", "platform.system", "platform.platform", '"nt"')
        for relative in sorted(LOADER_MODULES):
            source = (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if not isinstance(node, ast.FunctionDef):
                    continue
                if node.name not in {
                    "link_classification_available",
                    "reparse_information_observable",
                    "_is_junction",
                    "_is_symlink",
                }:
                    continue
                body = ast.get_source_segment(source, node) or ""
                statements = "\n".join(
                    line for line in body.splitlines() if not line.strip().startswith("#")
                )
                for marker in markers:
                    with self.subTest(module=relative, function=node.name, marker=marker):
                        self.assertNotIn(marker, statements)

    def test_withdrawing_both_routes_reports_no_capability(self) -> None:
        for loader in (interpreter_safety, tools_safety):
            with self.subTest(loader=loader.__name__):
                with _without_routes(
                    loader, pathlib_route=False, stat_route=False, reparse_observable=True
                ):
                    self.assertFalse(loader.link_classification_available())

    def test_withdrawing_both_routes_refuses_a_real_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = _Fixture(Path(temporary).resolve())
            entry = fixture.environment("env")
            for loader in (interpreter_safety, tools_safety):
                with self.subTest(loader=loader.__name__):
                    with _without_routes(
                        loader, pathlib_route=False, stat_route=False, reparse_observable=True
                    ):
                        self.assertEqual("EPS011", loader.refusal_case(entry))

    def test_a_runtime_with_no_reparse_surface_accepts_a_real_environment(self) -> None:
        """The regression this amendment repairs, asserted against a real path.

        Withdrawing both predicate routes on a runtime whose stat result reports
        no reparse information must accept an ordinary environment rather than
        refuse it with `EPS011`.
        """

        with tempfile.TemporaryDirectory() as temporary:
            fixture = _Fixture(Path(temporary).resolve())
            entry = fixture.environment("env")
            for loader in (interpreter_safety, tools_safety):
                with self.subTest(loader=loader.__name__):
                    with _routes(
                        loader, pathlib_route=False, stat_route=False, reparse_observable=False
                    ):
                        self.assertIsNone(loader.refusal_case(entry))
                        self.assertEqual(
                            entry.parent.parent, loader.evaluate(entry).environment_root
                        )

    def test_withdrawing_both_routes_refuses_rather_than_passing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = _Fixture(Path(temporary).resolve())
            entry = fixture.environment("env")
            for loader in (interpreter_safety, tools_safety):
                with self.subTest(loader=loader.__name__):
                    with mock.patch.object(
                        loader, "link_classification_available", return_value=False
                    ):
                        self.assertEqual("EPS011", loader.refusal_case(entry))

    def test_both_routes_agree_on_a_real_junction(self) -> None:
        if not JUNCTION_OK:
            self.skipTest(f"junction agreement: {JUNCTION_REASON}")
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            (base / "real").mkdir()
            alias = base / "alias"
            _junction(alias, base / "real")
            self.assertFalse(alias.is_symlink(), "a junction is not a symbolic link")
            attributes = os.lstat(alias)
            stat_route = bool(
                attributes.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
            ) and attributes.st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT
            self.assertTrue(stat_route, "the stat route must classify a real junction")
            predicate = getattr(Path, "is_junction", None)
            if predicate is not None:
                self.assertTrue(predicate(alias), "the two routes must agree")
            for loader in (interpreter_safety, tools_safety):
                with self.subTest(loader=loader.__name__):
                    self.assertTrue(loader._is_junction(alias))
                    with _without_routes(loader, pathlib_route=False, stat_route=True):
                        self.assertTrue(
                            loader._is_junction(alias), "the stat route alone must classify it"
                        )

    def test_an_ordinary_directory_is_not_classified_as_a_junction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ordinary = Path(temporary).resolve() / "plain"
            ordinary.mkdir()
            for loader in (interpreter_safety, tools_safety):
                with self.subTest(loader=loader.__name__):
                    self.assertFalse(loader._is_junction(ordinary))
                    with _without_routes(loader, pathlib_route=False, stat_route=True):
                        self.assertFalse(loader._is_junction(ordinary))

    def test_a_symbolic_link_is_not_classified_as_a_junction(self) -> None:
        if not SYMLINK_OK:
            self.skipTest(f"symbolic-link disjointness: {SYMLINK_REASON}")
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            (base / "real").mkdir()
            alias = base / "alias"
            alias.symlink_to(base / "real", target_is_directory=True)
            for loader in (interpreter_safety, tools_safety):
                with self.subTest(loader=loader.__name__):
                    self.assertTrue(loader._is_symlink(alias))
                    self.assertFalse(
                        loader._is_junction(alias), "the two predicates must stay distinct"
                    )


class BoundaryRegistryTests(unittest.TestCase):
    def test_the_registry_matches_an_independent_inventory(self) -> None:
        rule_modules: dict[str, int] = {}
        delegating_modules: dict[str, int] = {}
        for entry in interpreter_safety.declared_boundaries():
            bucket = rule_modules if entry["kind"] == "rule" else delegating_modules
            bucket[entry["module"]] = bucket.get(entry["module"], 0) + 1
        self.assertEqual(EXPECTED_RULE_BOUNDARIES, rule_modules)
        self.assertEqual(EXPECTED_DELEGATING_BOUNDARIES, delegating_modules)

    def test_the_independent_inventory_matches_what_the_packages_actually_do(self) -> None:
        reaches: set[str] = set()
        delegates: set[str] = set()
        for package in ("se_harness", "repository_tools"):
            for source in sorted((REPOSITORY_ROOT / package).glob("*.py")):
                relative = source.relative_to(REPOSITORY_ROOT).as_posix()
                if relative in LOADER_MODULES:
                    continue
                text = source.read_text(encoding="utf-8")
                if "interpreter_safety" in text:
                    reaches.add(relative)
                elif "_safe_interpreter" in text:
                    delegates.add(relative)
        self.assertEqual(sorted(EXPECTED_RULE_BOUNDARIES), sorted(reaches))
        self.assertEqual(sorted(EXPECTED_DELEGATING_BOUNDARIES), sorted(delegates))

    def test_every_registered_module_exists_and_names_its_own_runtime(self) -> None:
        for entry in interpreter_safety.declared_boundaries():
            with self.subTest(boundary=entry["id"]):
                self.assertTrue((REPOSITORY_ROOT / entry["module"]).is_file())
                self.assertTrue(entry["module"].startswith(f"{entry['runtime']}/"))
                self.assertTrue(entry["id"].startswith(f"{entry['runtime']}."))

    def test_an_unregistered_validation_fails_the_registry_check(self) -> None:
        rule_modules = {
            entry["module"]
            for entry in interpreter_safety.declared_boundaries()
            if entry["kind"] == "rule"
        }
        self.assertNotIn("se_harness/installer.py", rule_modules)
        inflated = dict(EXPECTED_RULE_BOUNDARIES)
        inflated["se_harness/installer.py"] = 1
        self.assertNotEqual(
            inflated,
            {
                entry["module"]: 1
                for entry in interpreter_safety.declared_boundaries()
                if entry["kind"] == "rule"
            },
        )

    def test_boundary_identifiers_can_be_filtered_by_runtime(self) -> None:
        for runtime in interpreter_safety.RUNTIMES:
            with self.subTest(runtime=runtime):
                identifiers = interpreter_safety.boundary_identifiers(runtime)
                for identifier in identifiers:
                    self.assertTrue(identifier.startswith(f"{runtime}."))
        self.assertEqual(
            len(interpreter_safety.declared_boundaries()),
            sum(
                len(interpreter_safety.boundary_identifiers(runtime))
                for runtime in interpreter_safety.RUNTIMES
            ),
        )
        # WO-REB-028: every declared site is a package one now. The second loader
        # stays held to the same declaration by the conformance cases above, so an
        # empty runtime is a real state of the registry rather than a gap in it.
        self.assertEqual((), interpreter_safety.boundary_identifiers("repository_tools"))
        self.assertTrue(interpreter_safety.boundary_identifiers("se_harness"))

    def test_the_declaration_names_no_retired_predecessor_module(self) -> None:
        # WO-REB-028: no declared site may name a file the work order deleted.
        boundaries = interpreter_safety.declared_boundaries()
        modules = {entry["module"] for entry in boundaries}
        for relative in (
            "repository_tools/release_bootstrap.py",
            "repository_tools/predecessor_preparation.py",
            "repository_tools/predecessor_publication.py",
            "repository_tools/predecessor_assessment.py",
        ):
            with self.subTest(module=relative):
                self.assertNotIn(relative, modules)
                self.assertFalse((REPOSITORY_ROOT / relative).exists())
        self.assertNotIn(
            "se_harness.release_qualification.external_evaluator",
            {entry["id"] for entry in boundaries},
        )


class ImportBarrierTests(unittest.TestCase):
    @staticmethod
    def _imported(package: str) -> dict[str, set[str]]:
        found: dict[str, set[str]] = {}
        for source in sorted((REPOSITORY_ROOT / package).glob("*.py")):
            relative = source.relative_to(REPOSITORY_ROOT).as_posix()
            names: set[str] = set()
            for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Import):
                    names.update(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and not node.level:
                    module = node.module or ""
                    names.update(f"{module}.{alias.name}" for alias in node.names)
            found[relative] = names
        return found

    def test_repository_tools_imports_only_the_standard_library_and_its_own_package(self) -> None:
        crossings: set[str] = set()
        for relative, names in self._imported("repository_tools").items():
            for name in sorted(names):
                head = name.split(".")[0]
                if head == "repository_tools":
                    continue
                if head == "se_harness":
                    crossings.add(name)
                    continue
                with self.subTest(module=relative, imported=name):
                    self.assertIn(head, sys.stdlib_module_names, f"{relative} imports {name}")
        self.assertEqual(
            sorted(PERMITTED_PACKAGE_IMPORTS),
            sorted(crossings),
            "the repository_tools -> se_harness crossing inventory changed",
        )

    def test_no_crossing_from_repository_tools_into_the_package_remains(self) -> None:
        # WO-REB-028: the deleted modules held the only se_harness.hash_bound import.
        self.assertEqual(frozenset(), PERMITTED_PACKAGE_IMPORTS)
        for relative, names in self._imported("repository_tools").items():
            with self.subTest(module=relative):
                self.assertEqual(
                    set(), {name for name in names if name.split(".")[0] == "se_harness"}
                )

    def test_no_crossing_from_the_package_into_repository_tools_remains(self) -> None:
        # WO-REB-028: qualify_predecessor_view held the one guarded function-local
        # import. The package neither names nor needs repository_tools now, at any
        # import level, so an installed evaluator has nothing left to refuse.
        self.assertEqual(frozenset(), PERMITTED_TOOLS_IMPORTS)
        crossings: set[str] = set()
        for relative, names in self._imported("se_harness").items():
            for name in sorted(names):
                if name.split(".")[0] == "repository_tools":
                    crossings.add(f"{relative}: {name}")
        self.assertEqual(set(), crossings)
        # The one former holder keeps no residue of the guarded import either.
        text = (REPOSITORY_ROOT / "se_harness/release_qualification.py").read_text(
            encoding="utf-8"
        )
        for absent in ("repository_tools", "ImportError", "lazily imported"):
            with self.subTest(absent=absent):
                self.assertNotIn(absent, text)

    def test_neither_package_crossing_carries_an_interpreter_safety_name(self) -> None:
        for name in sorted(PERMITTED_PACKAGE_IMPORTS | PERMITTED_TOOLS_IMPORTS):
            with self.subTest(imported=name):
                self.assertNotIn("interpreter_safety", name)

    def test_neither_loader_imports_the_other_runtime(self) -> None:
        for relative in sorted(LOADER_MODULES):
            with self.subTest(module=relative):
                source = (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")
                for node in ast.walk(ast.parse(source)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.assertIn(alias.name.split(".")[0], sys.stdlib_module_names)
                    elif isinstance(node, ast.ImportFrom) and not node.level:
                        head = (node.module or "").split(".")[0]
                        self.assertIn(head, sys.stdlib_module_names, f"{relative}: {node.module}")


class StaticArchitectureTests(unittest.TestCase):
    def test_no_boundary_restates_interpreter_junction_detection_inline(self) -> None:
        for relative in sorted(
            set(EXPECTED_RULE_BOUNDARIES) | set(EXPECTED_DELEGATING_BOUNDARIES)
        ):
            tree = ast.parse((REPOSITORY_ROOT / relative).read_text(encoding="utf-8"))
            holders = _functions_naming(tree, interpreter_safety.JUNCTION_PREDICATE)
            permitted = RETAINED_INLINE_JUNCTION_FUNCTIONS.get(relative, {})
            with self.subTest(module=relative):
                self.assertEqual(
                    sorted(permitted),
                    sorted(holders),
                    f"{relative}: the inline junction-test inventory changed",
                )
            # A retained walker is only outside the declaration while no caller
            # hands it an interpreter. That is what makes it not a restatement.
            for name in sorted(holders):
                for call in _calls_to(tree, name):
                    subject = ast.unparse(call.args[0]).lower() if call.args else ""
                    for marker in INTERPRETER_NAME_MARKERS:
                        with self.subTest(module=relative, function=name, call=subject):
                            self.assertNotIn(marker, subject)

    def test_no_interpreter_boundary_derives_an_environment_root_from_an_interpreter_path(
        self,
    ) -> None:
        for relative in sorted(EXPECTED_RULE_BOUNDARIES):
            tree = ast.parse((REPOSITORY_ROOT / relative).read_text(encoding="utf-8"))
            derivations = _grandparent_derivations(tree)
            permitted = RETAINED_GRANDPARENT_DERIVATIONS.get(relative, ())
            with self.subTest(module=relative):
                self.assertEqual(
                    sorted(permitted),
                    sorted(derivations),
                    f"{relative}: the two-levels-up derivation inventory changed",
                )
            for expression in sorted(derivations):
                lowered = expression.lower()
                for marker in INTERPRETER_NAME_MARKERS:
                    with self.subTest(module=relative, expression=expression):
                        self.assertNotIn(marker, lowered)
                with self.subTest(module=relative, expression=expression):
                    self.assertNotIn("resolve()", lowered)

    def test_every_rule_boundary_reaches_the_loader_instead_of_deciding_for_itself(
        self,
    ) -> None:
        for relative in sorted(EXPECTED_RULE_BOUNDARIES):
            with self.subTest(module=relative):
                text = (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")
                self.assertIn("interpreter_safety", text)

    def test_the_migration_refusal_map_covers_exactly_the_declared_cases(self) -> None:
        declared = {entry["id"] for entry in interpreter_safety.declared_cases()}
        self.assertEqual(sorted(declared), sorted(governance_migration.INTERPRETER_REFUSAL_CODES))
        for case, code in sorted(governance_migration.INTERPRETER_REFUSAL_CODES.items()):
            with self.subTest(case=case):
                self.assertRegex(code, r"^MIG2[0-9]{2}$")

    def test_migration_retains_mig205_for_the_link_and_junction_refusals(self) -> None:
        for case in ("EPS001", "EPS002", "EPS005", "EPS006", "EPS011"):
            with self.subTest(case=case):
                self.assertEqual("MIG205", governance_migration.INTERPRETER_REFUSAL_CODES[case])
        for case in ("EPS007", "EPS008", "EPS009"):
            with self.subTest(case=case):
                self.assertEqual("MIG202", governance_migration.INTERPRETER_REFUSAL_CODES[case])

    def test_the_declaration_ships_as_package_data(self) -> None:
        text = (REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('"interpreter_safety.json",', text)

    def test_the_declaration_appears_in_the_portable_release_surface_list(self) -> None:
        text = (REPOSITORY_ROOT / "scripts/check_portable_release_surface.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('"se_harness/interpreter_safety.json"', text)
        self.assertIn('"se_harness/interpreter_safety.py"', text)
        self.assertIn("REQUIRED_INTERPRETER_SAFETY_MEMBERS", text)

    def test_the_runtime_identity_schema_identifier_is_unchanged(self) -> None:
        self.assertEqual("se-harness-runtime-identity-v3", runtime_identity.IDENTITY_SCHEMA)

    def test_the_added_identity_fields_are_the_three_declared_ones(self) -> None:
        fields = set(runtime_identity.RuntimeIdentity.__dataclass_fields__)
        self.assertLessEqual(
            {"python_entry_is_link", "python_binary_position", "python_binary_sha256"}, fields
        )

    def test_only_environment_bounded_roles_turn_a_refusal_into_a_diagnostic(self) -> None:
        self.assertEqual(
            frozenset({"released-evaluator", "candidate-package"}),
            runtime_identity.ENVIRONMENT_BOUNDED_ROLES,
        )
        self.assertLess(runtime_identity.ENVIRONMENT_BOUNDED_ROLES, runtime_identity.ROLES)


class PlatformCoverageTests(unittest.TestCase):
    """Record, rather than infer, what this lane could and could not construct."""

    def test_this_lane_records_its_construction_capabilities(self) -> None:
        report = {
            "platform": PLATFORM,
            "python": platform.python_version(),
            "symlink": SYMLINK_OK,
            "junction": JUNCTION_OK,
            "pathlib_is_junction": hasattr(Path, "is_junction"),
        }
        self.assertIn(report["platform"], interpreter_safety.PLATFORMS)
        # A lane must be able to construct at least the platform-independent
        # forms; a lane that can construct neither link form proves nothing
        # about REQ-REB-024 and the contract requires both lanes.
        self.assertTrue(SYMLINK_OK or JUNCTION_OK, f"neither link form is constructable: {report}")

    def test_every_corpus_entry_is_constructable_on_at_least_one_platform_or_records_why_not(
        self,
    ) -> None:
        for entry in interpreter_safety.declared_corpus():
            with self.subTest(corpus=entry["id"]):
                if not entry["constructable_on"]:
                    self.assertIn("unconstructable_reason", entry)


if __name__ == "__main__":
    unittest.main()
