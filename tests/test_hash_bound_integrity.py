"""Assurance for declared hash-bound text classes and their doctor assessment.

Digests asserted here are computed over bytes this module reads itself, never
over a value the implementation under test reports. Small byte examples cover
LF/CRLF equivalence; one real checkout exercises each supported host OS.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness import hash_bound
from se_harness.evaluator_identity import InstalledEvaluatorIdentity
from se_harness.hash_bound import (
    CANONICAL_MODE,
    CHECK_ATTRIBUTE_EFFECTIVE,
    CHECK_CLASS_DECLARED,
    CHECK_MODE_CONSISTENT,
    CHECK_NAMES,
    HashBoundError,
    LOCK_RELATIVE,
    MATCH_DECLARED,
    MATCH_MISMATCH,
    RAW_MODE,
    assess,
    compare_declared_digest,
    declared_digest,
    load_declaration,
    matches,
    pattern_specificity,
    resolve_class,
    resolve_mode,
)
from se_harness.integrity import canonical_sha256, raw_sha256
from se_harness.preflight import inspect_installation
from tests.artifact_support import write
from tests.git_support import git, git_available, run_git


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "hash_bound"
DECLARATION_PATH = ROOT / "se_harness" / "hash_bound_classes.json"
TEMPLATE_FRAGMENT = ROOT / "templates" / "repository" / "standard" / "gitattributes.fragment"
ATTRIBUTES = ROOT / ".gitattributes"
LOCK = ROOT / ".engineering-harness.lock"
SPECIFIED_CLASSES = {
    "evaluator-evidence": (
        ("docs/engineering/**/evidence/*.json",),
        RAW_MODE,
        "text eol=lf",
        "template",
    ),
    "standard-lock": ((".engineering-harness.lock",), CANONICAL_MODE, None, "template"),
}
#: Committed files whose exact bytes the candidate suite compares or hashes. No
#: recorded SHA-256 binds them, so no hash-bound class covers them and `doctor` does
#: not assess them; the byte rule is still load-bearing, because the release
#: orchestrator runs that suite inside a `git worktree` it creates on `windows-2022`,
#: which inherits the checkout's `core.autocrlf`.
BYTE_EXACT_FILES = (
    "se_harness/hash_bound_classes.json",
    "release/build-recipe.json",
    "release/build-toolchain.lock",
)
#: Trees whose every tracked file the candidate suite reads byte for byte. The inventory
#: below is derived from the tracked set under each prefix rather than from an extension
#: list, because an extension list cannot report a file it does not match:
#: `WO-HBI-003` declared `*.json`, `*.md` and `*.py` here and a concurrent pull request
#: added `agents/openai.yaml` with a byte-exact assertion, which stayed converted and
#: failed the release orchestrator's `windows-2022` candidate qualification.
BYTE_EXACT_TREES = ("templates/repository/standard/.agents/skills/",)

UPGRADE_WORK_ORDER = (
    ROOT / "docs" / "engineering" / "repository-harness-upgrade" / "work-orders" / "WO-HUP-002.md"
)
# Recorded before the lock's class was declared, over the bytes a CRLF checkout
# produced. Rule 11 forbids rewriting it, so the digest below is quoted from the
# artifact and the commit is the tree it was taken over.
RECORDED_PRIOR_LOCK_SHA256 = "c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af"
RECORDED_PRIOR_LOCK_COMMIT = "842ad90869ac153dc7aa407611992f066de78dd5"
SYNTHETIC_FILES = {
    "docs/engineering/x/evidence/a.json": b'{"a": 1}\n',
    ".engineering-harness.lock": b'{"schema": 3}\n',
    "README.md": b"synthetic\n",
}


def build_source(root: Path, attributes: bytes, files: dict[str, bytes] | None = None) -> None:
    """Create a committed repository whose blobs are exactly the bytes given."""

    git(root, "init", "-q", "-b", "main")
    git(root, "config", "core.autocrlf", "false")
    git(root, "config", "user.email", "assurance@example.invalid")
    git(root, "config", "user.name", "assurance")
    git(root, "config", "commit.gpgsign", "false")
    for relative, payload in (files or SYNTHETIC_FILES).items():
        write(root / relative, payload)
    write(root / ".gitattributes", attributes)
    git(root, "add", "-A")
    git(root, "-c", "core.autocrlf=false", "commit", "-q", "-m", "synthetic")


def clone(source: Path, destination: Path, autocrlf: str) -> Path:
    subprocess.run(
        [
            "git",
            "-c",
            f"core.autocrlf={autocrlf}",
            "clone",
            "-q",
            str(source),
            str(destination),
        ],
        check=True,
        capture_output=True,
    )
    return destination


def committed_attributes() -> bytes:
    """Return the repository's .gitattributes as committed, independent of checkout."""

    return git(ROOT, "cat-file", "blob", "HEAD:.gitattributes", binary=True)


def working_tree_attributes() -> bytes:
    """Return this checkout's `.gitattributes` with its newlines normalized.

    `committed_attributes` reads `HEAD`, which lags an edited rule by one commit. A guard
    over the rules themselves has to read what the working tree presents, or it reports
    the previous commit's coverage and goes green only after the change is committed.
    """

    return ATTRIBUTES.read_bytes().replace(b"\r\n", b"\n")


def revision_available(revision: str) -> bool:
    """Return whether this checkout holds the object, which a shallow clone may not."""

    if not git_available():
        return False
    return run_git(ROOT, "cat-file", "-e", f"{revision}^{{commit}}", check=False).returncode == 0


def historical_lock() -> bytes:
    return git(ROOT, "cat-file", "blob", f"{RECORDED_PRIOR_LOCK_COMMIT}:{LOCK_RELATIVE}", binary=True)


def newline_forms(payload: bytes) -> dict[str, bytes]:
    """Return the three materializations a checkout can produce from one blob."""

    canonical = payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return {
        "lf": canonical,
        "crlf": canonical.replace(b"\n", b"\r\n"),
        "cr": canonical.replace(b"\n", b"\r"),
    }


def raw_lock_declaration() -> hash_bound.Declaration:
    """Return the real declaration with the lock's class flipped to raw mode.

    Used to prove a caller follows the declaration rather than a mode of its own:
    under this declaration the same bytes must reach a different verdict.
    """

    declared = load_declaration()
    return hash_bound.Declaration(
        classes=tuple(
            hash_bound.HashBoundClass(
                item.class_id,
                item.patterns,
                RAW_MODE if item.class_id == "standard-lock" else item.mode,
                item.required_attribute,
            )
            for item in declared.classes
        ),
    )


def upgrade_packet(root: Path, prior_lock_sha256: str, identity: InstalledEvaluatorIdentity) -> None:
    """Write one approved evaluator-upgrade work order and nothing else."""

    body = f"""+++
id = "WO-TST-001"
type = "work_order"
status = "approved"
title = "Synthetic evaluator upgrade"

[evaluator_upgrade]
schema = "se-harness-evaluator-upgrade-v1"
scope = "standard-root-only"
prior_lock_sha256 = "{prior_lock_sha256}"
target_version = "{identity.version}"
target_payload_sha256 = "{identity.payload_sha256}"
target_archive_name = "{identity.archive_name}"
target_archive_sha256 = "{identity.archive_sha256}"
publication = "immutable"
authorized_by = "engineering-owner"
+++

Synthetic.
"""
    write(root / "docs/engineering/upgrade/work-orders/WO-TST-001.md", body.encode("utf-8"))


#: Paths that exist only in candidate source. REQ-HBI-004: nothing the wheel ships
#: to a consumer may name one of them.
CANDIDATE_ONLY_PREFIXES = ("se_harness/", "tests/", "repository_tools/")
SYNTHETIC_REPOSITORY_CLASS = "owner-notes"
SYNTHETIC_REPOSITORY_PATTERN = "notes/*.txt"


def repository_declaration() -> hash_bound.Declaration:
    """Return the real declaration plus one synthetic `repository`-region raw class.

    The shipped table carries no `repository`-region class since `WO-HBI-005`, so
    the owner-declared behaviours (fail closed on an empty match, require the rule
    in owner content) are exercised on a class an owner would declare.
    """

    declared = load_declaration()
    extra = hash_bound.HashBoundClass(
        SYNTHETIC_REPOSITORY_CLASS,
        (SYNTHETIC_REPOSITORY_PATTERN,),
        RAW_MODE,
        "text eol=lf",
    )
    return hash_bound.Declaration(
        classes=(*declared.classes, extra),
    )


def results(root: Path, declaration=None) -> dict[str, tuple[bool, str]]:
    return {name: (passed, detail) for name, passed, detail in assess(root, declaration)}


def worktree_state(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".git/" not in path.relative_to(root).as_posix()
    }


class LoaderFailClosedTests(unittest.TestCase):
    cases = {
        "overlapping-classes.json": None,
        "raw-without-attribute.json": "raw class only must require",
        "canonical-with-attribute.json": "must not require a Git attribute",
        "duplicate-binding.json": "bound by two classes",
        "bound-and-unbound.json": "both bound and unbound",
        "unknown-mode.json": "unsupported mode",
        "duplicate-key.json": "duplicate declaration key",
        "unknown-class-field.json": "fields must be exactly",
    }

    def test_declaration_defects_are_refused(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "classes.json"
            source = json.loads(DECLARATION_PATH.read_text(encoding="utf-8"))
            for field, value in [("mode", "invalid"), ("patterns", ["../outside"]), ("required_attribute", None)]:
                candidate = json.loads(json.dumps(source))
                candidate["classes"][0][field] = value
                path.write_text(json.dumps(candidate), encoding="utf-8")
                with self.subTest(field=field), self.assertRaises(HashBoundError):
                    load_declaration(path)

    def test_missing_declaration_fails_closed(self) -> None:
        with self.assertRaises(HashBoundError):
            load_declaration(FIXTURES / "absent.json")

    def test_wrong_schema_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "d.json"
            path.write_bytes(b'{"schema": "other", "classes": [], "removed_field": []}')
            with self.assertRaises(HashBoundError) as caught:
                load_declaration(path)
            self.assertIn("must use schema", str(caught.exception))

    def test_invalid_utf8_declaration_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "d.json"
            path.write_bytes(b'{"schema": "\xff"}')
            with self.assertRaises(HashBoundError):
                load_declaration(path)

    def test_unreadable_declaration_makes_every_check_fail(self) -> None:
        with mock.patch.object(
            hash_bound, "load_declaration", side_effect=HashBoundError("declaration unreadable")
        ):
            observed = assess(ROOT)
        self.assertEqual(CHECK_NAMES, tuple(name for name, _, _ in observed))
        for _, passed, detail in observed:
            self.assertFalse(passed)
            self.assertIn("declaration unreadable", detail)


class ResolutionTests(unittest.TestCase):
    def test_specificity_ordering(self) -> None:
        self.assertGreater(
            pattern_specificity(".engineering-harness.lock"),
            pattern_specificity("se_harness/governance_migration*.py"),
        )
        self.assertGreater(
            pattern_specificity("se_harness/governance_migration*.py"),
            pattern_specificity("docs/engineering/**/evidence/*.json"),
        )

    def test_known_paths_resolve_to_exactly_one_class(self) -> None:
        expected = {
            "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-003-evaluator.json": "evaluator-evidence",
            "docs/engineering/x/evidence/a.json": "evaluator-evidence",
            ".engineering-harness.lock": "standard-lock",
        }
        for relative, class_id in expected.items():
            with self.subTest(path=relative):
                self.assertEqual(class_id, resolve_class(relative).class_id)

    def test_uncovered_path_fails_closed(self) -> None:
        for relative in ("README.md", "se_harness/integrity.py", "docs/engineering/README.md"):
            with self.subTest(path=relative):
                with self.assertRaises(HashBoundError) as caught:
                    resolve_class(relative)
                self.assertIn(relative, str(caught.exception))

    def test_equal_specificity_overlap_fails_closed(self) -> None:
        declaration = load_declaration(FIXTURES / "overlapping-classes.json")
        with self.assertRaises(HashBoundError) as caught:
            resolve_class("docs/a/evidence/b.json", declaration)
        message = str(caught.exception)
        self.assertIn("equal specificity", message)
        self.assertIn("left", message)
        self.assertIn("right", message)

    def test_resolution_never_returns_a_default(self) -> None:
        with self.assertRaises(HashBoundError):
            resolve_class("docs/engineering/x/evidence/a.txt")

    def test_pattern_matching_respects_component_boundaries(self) -> None:
        self.assertFalse(matches("se_harness/governance_migration*.py", "se_harness/a/governance_migration.py"))
        self.assertFalse(matches("docs/engineering/**/evidence/*.json", "docs/engineering/x/evidence/y/z.json"))
        self.assertTrue(matches("docs/engineering/**/evidence/*.json", "docs/engineering/evidence/z.json"))

    def test_ordering_independence(self) -> None:
        declaration = load_declaration()
        reversed_declaration = hash_bound.Declaration(
            classes=tuple(reversed(declaration.classes)),
        )
        for relative in (".engineering-harness.lock", "docs/engineering/x/evidence/a.json"):
            self.assertEqual(
                resolve_class(relative, declaration).class_id,
                resolve_class(relative, reversed_declaration).class_id,
            )


class CheckContractTests(unittest.TestCase):
    def test_names_are_exact_and_ordered(self) -> None:
        self.assertEqual(
            (
                "hash-bound-class-declared",
                "hash-bound-attribute-effective",
                "hash-bound-mode-consistent",
            ),
            CHECK_NAMES,
        )
        self.assertEqual(CHECK_NAMES, tuple(name for name, _, _ in assess(ROOT)))


    @unittest.skipUnless(git_available(), "git is unavailable")
    def test_doctor_surfaces_the_checks_in_order(self) -> None:
        checks = inspect_installation(ROOT)
        observed = [check.name for check in checks if check.name.startswith("hash-bound-")]
        self.assertEqual(list(CHECK_NAMES), observed)
        self.assertEqual(list(CHECK_NAMES), [check.name for check in checks[-3:]])

    def test_non_git_target_emits_no_hash_bound_check(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / ".engineering-harness.toml").write_bytes(b"")
            checks = inspect_installation(target)
        self.assertEqual([], [check.name for check in checks if check.name.startswith("hash-bound-")])

    def test_details_are_bounded_and_disclose_nothing(self) -> None:
        for _, _, detail in assess(ROOT):
            self.assertLessEqual(len(detail), 400)
            self.assertEqual(1, len(detail.splitlines()))
            lowered = detail.lower()
            for secret in ("token", "password", "secret", "users/", "c:\\", "home/"):
                self.assertNotIn(secret, lowered, detail)


class RepositoryAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not git_available() or not (ROOT / ".git").exists():
            raise unittest.SkipTest("assessment requires a Git working tree")

    def test_this_repository_passes_every_check(self) -> None:
        for name, (passed, detail) in results(ROOT).items():
            self.assertTrue(passed, f"{name}: {detail}")

    def test_assessment_is_deterministic(self) -> None:
        self.assertEqual(assess(ROOT), assess(ROOT))

    def test_assessment_is_read_only(self) -> None:
        before = {
            path: (ROOT / path).read_bytes()
            for path in (".gitattributes", ".engineering-harness.lock", ".engineering-harness.toml")
        }
        status_before = git(ROOT, "status", "--porcelain", binary=True)
        assess(ROOT)
        for path, payload in before.items():
            self.assertEqual(payload, (ROOT / path).read_bytes(), path)
        self.assertEqual(status_before, git(ROOT, "status", "--porcelain", binary=True))

    def test_managed_attribute_block_still_matches_its_recorded_digest(self) -> None:
        lock = json.loads(LOCK.read_bytes().decode("utf-8"))
        recorded = lock["files"][".gitattributes"]["sha256"]
        text = ATTRIBUTES.read_bytes().decode("utf-8")
        start = text.index(hash_bound.ATTRIBUTE_BEGIN_MARKER)
        end = text.index(hash_bound.ATTRIBUTE_END_MARKER) + len(hash_bound.ATTRIBUTE_END_MARKER)
        block = (text[start:end] + "\n").encode("utf-8")
        self.assertEqual(recorded, canonical_sha256(block))


@unittest.skipUnless(git_available(), "git is unavailable")
class ByteExactSurfaceTests(unittest.TestCase):
    """Byte-exact surfaces outside every hash-bound class still carry a byte rule.

    A hash-bound class exists where a recorded digest binds a file. These files are
    compared byte for byte by the candidate suite instead, so no class covers them and
    no check assesses them. The orchestrator qualifies the candidate in a `git worktree`
    that inherits the checkout's `core.autocrlf`, so a missing byte rule here fails
    qualification on one runner type and passes on the other.

    The inventory is the tracked set, not a pattern list. A pattern list is blind to the
    file it does not match, which is how `agents/openai.yaml` reached a hosted failure
    while this class passed.
    """

    @classmethod
    def setUpClass(cls) -> None:
        if not (ROOT / ".git").exists():
            raise unittest.SkipTest("byte rules resolve from a Git working tree")
        cls.tracked = hash_bound.tracked_paths(ROOT)
        named = set(BYTE_EXACT_FILES).intersection(cls.tracked)
        under_trees = {
            relative
            for relative in cls.tracked
            if any(relative.startswith(tree) for tree in BYTE_EXACT_TREES)
        }
        cls.paths = tuple(sorted(named | under_trees))

    def test_every_declared_file_is_tracked(self) -> None:
        for relative in BYTE_EXACT_FILES:
            with self.subTest(path=relative):
                self.assertIn(
                    relative,
                    self.tracked,
                    f"{relative} is not tracked, so its byte rule is dead",
                )

    def test_every_declared_tree_holds_a_tracked_file(self) -> None:
        for tree in BYTE_EXACT_TREES:
            with self.subTest(tree=tree):
                self.assertTrue(
                    any(relative.startswith(tree) for relative in self.tracked),
                    f"{tree} holds no tracked file, so its byte rule is dead",
                )

    def test_the_inventory_holds_every_tracked_file_under_each_tree(self) -> None:
        """No extension is filtered out, so a new one is covered without a new rule."""

        for tree in BYTE_EXACT_TREES:
            expected = sorted(item for item in self.tracked if item.startswith(tree))
            self.assertEqual(expected, sorted(item for item in self.paths if item.startswith(tree)))

    def test_every_surface_resolves_the_required_attribute(self) -> None:
        resolved = hash_bound.resolved_attributes(ROOT, self.paths)
        for relative in self.paths:
            with self.subTest(path=relative):
                attributes = resolved[relative]
                self.assertEqual("set", attributes.get("text"), attributes)
                self.assertEqual("lf", attributes.get("eol"), attributes)

    def test_no_surface_is_converted_in_this_working_tree(self) -> None:
        payload = git(ROOT, "ls-files", "--eol", "-z", "--", *self.paths, binary=True)
        reported = {}
        for record in payload.decode("utf-8").split("\0"):
            if not record.strip():
                continue
            fields = record.split("\t")
            worktree = next(
                item[2:] for item in fields[0].split() if item.startswith("w/")
            )
            reported[fields[-1]] = worktree
        self.assertEqual(sorted(reported), sorted(self.paths))
        for relative, worktree in sorted(reported.items()):
            with self.subTest(path=relative):
                self.assertIn(worktree, ("lf", "none"), f"{relative} is {worktree}")

    def test_a_novel_extension_in_a_byte_exact_tree_needs_no_new_rule(self) -> None:
        """The committed rules cover a byte-exact tree, not a list of its extensions.

        Measured against the bytes a fresh `core.autocrlf=true` clone produces, not only
        against the attribute Git reports. `WO-HBI-003`'s three per-extension rules fail
        this: `.yaml` and an unseen extension both check out converted under them.
        """

        tree = BYTE_EXACT_TREES[0]
        novel = f"{tree}harness-probe/agents/openai.yaml"
        unseen = f"{tree}harness-probe/nested/deeper/probe.novel-extension"
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            source.mkdir()
            build_source(
                source,
                working_tree_attributes(),
                {
                    novel: b"policy:\n  allow_implicit_invocation: false\n",
                    unseen: b"first\nsecond\n",
                    "README.md": b"synthetic\n",
                },
            )
            checkout = clone(source, Path(directory) / "checkout", "true")
            resolved = hash_bound.resolved_attributes(checkout, (novel, unseen))
            for relative in (novel, unseen):
                with self.subTest(path=relative):
                    self.assertEqual("set", resolved[relative].get("text"), resolved[relative])
                    self.assertEqual("lf", resolved[relative].get("eol"), resolved[relative])
                    self.assertNotIn(b"\r\n", (checkout / relative).read_bytes())
            outside = hash_bound.resolved_attributes(checkout, ("README.md",))["README.md"]
            self.assertEqual("unspecified", outside.get("text"), outside)


@unittest.skipUnless(git_available(), "git is unavailable")
class FreshCheckoutTests(unittest.TestCase):
    """One real checkout on the running OS, plus small byte-level newline checks."""

    def test_checkout_preserves_raw_evidence_and_canonical_lock_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "source"
            source.mkdir()
            build_source(source, committed_attributes())
            autocrlf = "true" if os.name == "nt" else "input"
            checkout = clone(source, base / "checkout", autocrlf)
            raw_path = "docs/engineering/x/evidence/a.json"
            blob = git(checkout, "cat-file", "blob", f"HEAD:{raw_path}", binary=True)
            self.assertEqual(blob, (checkout / raw_path).read_bytes())
            lock_blob = git(checkout, "cat-file", "blob", "HEAD:.engineering-harness.lock", binary=True)
            self.assertEqual(canonical_sha256(lock_blob), canonical_sha256((checkout / ".engineering-harness.lock").read_bytes()))
            for name, (passed, detail) in results(checkout).items():
                with self.subTest(check=name):
                    self.assertTrue(passed, detail)

    def test_effective_git_info_attributes_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "source"
            source.mkdir()
            build_source(source, b"# se-harness:begin\n# se-harness:end\n")
            root = clone(source, base / "clone", "false")
            git(root, "config", "core.autocrlf", "false")
            git(root, "config", "core.eol", "lf")
            (root / ".git" / "info").mkdir(parents=True, exist_ok=True)
            (root / ".git" / "info" / "attributes").write_bytes(
                b"docs/engineering/**/evidence/*.json text eol=lf\n"
                b"se_harness/governance_migration*.py text eol=lf\n"
                b"se_harness/governance_migration_contract.json text eol=lf\n"
                b"tests/fixtures/governance_migration/*.json text eol=lf\n"
            )
            passed, detail = results(root)[CHECK_ATTRIBUTE_EFFECTIVE]
        self.assertTrue(passed, detail)


@unittest.skipUnless(git_available(), "git is unavailable")
class AttributeEffectivenessTests(unittest.TestCase):
    def assess_with_attributes(self, attributes: bytes) -> dict[str, tuple[bool, str]]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            build_source(root, attributes)
            return results(root)

    def test_baseline_attributes_are_effective(self) -> None:
        observed = self.assess_with_attributes(committed_attributes())
        self.assertTrue(observed[CHECK_ATTRIBUTE_EFFECTIVE][0], observed[CHECK_ATTRIBUTE_EFFECTIVE][1])

    def test_absent_attribute_is_ineffective(self) -> None:
        attributes = committed_attributes().replace(
            b"docs/engineering/**/evidence/*.json text eol=lf\n", b""
        )
        passed, detail = self.assess_with_attributes(attributes)[CHECK_ATTRIBUTE_EFFECTIVE]
        self.assertFalse(passed)
        self.assertIn("evaluator-evidence", detail)
        self.assertIn("docs/engineering/x/evidence/a.json", detail)

    def test_more_specific_negated_text_override_is_ineffective(self) -> None:
        attributes = committed_attributes() + b"docs/engineering/x/evidence/*.json -text\n"
        passed, detail = self.assess_with_attributes(attributes)[CHECK_ATTRIBUTE_EFFECTIVE]
        self.assertFalse(passed)
        self.assertIn("evaluator-evidence", detail)
        self.assertIn("docs/engineering/x/evidence/a.json", detail)
        self.assertIn("text=unset", detail)
        self.assertIn("requires text eol=lf", detail)

    def test_more_specific_crlf_override_is_ineffective(self) -> None:
        attributes = committed_attributes() + b"docs/engineering/x/evidence/*.json text eol=crlf\n"
        passed, detail = self.assess_with_attributes(attributes)[CHECK_ATTRIBUTE_EFFECTIVE]
        self.assertFalse(passed)
        self.assertIn("eol=crlf", detail)


    def assess_repository_class(self, attributes: bytes) -> dict[str, tuple[bool, str]]:
        files = {**SYNTHETIC_FILES, "notes/a.txt": b"owner note\n"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            build_source(root, attributes, files)
            return results(root, repository_declaration())


    def test_repository_class_in_owner_content_is_effective(self) -> None:
        attributes = (
            b"# se-harness:begin\n"
            b"docs/engineering/**/evidence/*.json text eol=lf\n"
            b"# se-harness:end\n"
            b"notes/*.txt text eol=lf\n"
        )
        observed = self.assess_repository_class(attributes)
        self.assertTrue(observed[CHECK_CLASS_DECLARED][0], observed[CHECK_CLASS_DECLARED][1])
        self.assertTrue(observed[CHECK_ATTRIBUTE_EFFECTIVE][0], observed[CHECK_ATTRIBUTE_EFFECTIVE][1])

    def test_duplicate_identical_rule_in_both_regions_stays_effective(self) -> None:
        attributes = committed_attributes() + b"docs/engineering/**/evidence/*.json text eol=lf\n"
        observed = self.assess_with_attributes(attributes)
        self.assertTrue(observed[CHECK_ATTRIBUTE_EFFECTIVE][0], observed[CHECK_ATTRIBUTE_EFFECTIVE][1])

    def test_hostile_attribute_content_is_read_not_executed(self) -> None:
        attributes = (
            committed_attributes()
            + b"$(touch pwned) text eol=lf\n"
            + b"`rm -rf /` text\n"
            + b"'; python -c \"1\" ; ' text\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            build_source(root, attributes)
            before = worktree_state(root)
            observed = results(root)
            self.assertEqual(before, worktree_state(root))
        self.assertTrue(observed[CHECK_ATTRIBUTE_EFFECTIVE][0], observed[CHECK_ATTRIBUTE_EFFECTIVE][1])
        self.assertFalse((Path.cwd() / "pwned").exists())


class ModeArbitrationTests(unittest.TestCase):
    """One query answers what mode a bound path is hashed under, or refuses."""

    def test_every_declared_class_arbitrates_its_own_mode(self) -> None:
        for relative, expected in (
            (LOCK_RELATIVE, CANONICAL_MODE),
            ("docs/engineering/x/evidence/a.json", RAW_MODE),
        ):
            with self.subTest(relative=relative):
                self.assertEqual(expected, resolve_mode(relative))

    def test_an_undeclared_path_fails_closed_rather_than_defaulting(self) -> None:
        for relative in ("README.md", "docs/engineering/x/evidence/a.txt", "se_harness/cli.py"):
            with self.subTest(relative=relative):
                with self.assertRaises(HashBoundError) as raised:
                    resolve_mode(relative)
                self.assertIn(relative, str(raised.exception))

    def test_the_declared_lock_path_is_the_installer_path(self) -> None:
        from se_harness.installer import LOCK_NAME

        self.assertEqual(LOCK_NAME, LOCK_RELATIVE)
        self.assertIn(LOCK_RELATIVE, [item for entry in SPECIFIED_CLASSES.values() for item in entry[0]])

    def test_a_canonical_class_reaches_one_digest_from_every_materialization(self) -> None:
        forms = newline_forms(LOCK.read_bytes())
        digests = {name: declared_digest(LOCK_RELATIVE, value) for name, value in forms.items()}
        self.assertEqual({canonical_sha256(forms["lf"])}, set(digests.values()), digests)
        for name, value in forms.items():
            with self.subTest(materialization=name):
                self.assertEqual(
                    MATCH_DECLARED,
                    compare_declared_digest(LOCK_RELATIVE, value, digests["lf"]),
                )

    def test_a_raw_class_keeps_every_materialization_distinct(self) -> None:
        relative = "docs/engineering/x/evidence/a.json"
        forms = newline_forms(b'{"a": 1}\n')
        digests = {name: declared_digest(relative, value) for name, value in forms.items()}
        self.assertEqual(raw_sha256(forms["lf"]), digests["lf"])
        self.assertEqual(3, len(set(digests.values())), digests)

    def test_a_single_byte_tamper_is_a_mismatch_in_every_class(self) -> None:
        for relative in (
            LOCK_RELATIVE,
            "docs/engineering/x/evidence/a.json",
        ):
            with self.subTest(relative=relative):
                payload = b'{"a": 1}\n'
                expected = declared_digest(relative, payload)
                self.assertEqual(MATCH_DECLARED, compare_declared_digest(relative, payload, expected))
                self.assertEqual(
                    MATCH_MISMATCH, compare_declared_digest(relative, b'{"a": 2}\n', expected)
                )

    def test_invalid_utf8_fails_closed_in_a_canonical_class(self) -> None:
        with self.assertRaises(HashBoundError) as raised:
            declared_digest(LOCK_RELATIVE, b'{"a": \xff}\n')
        detail = str(raised.exception)
        self.assertIn(LOCK_RELATIVE, detail)
        self.assertIn(CANONICAL_MODE, detail)
        with self.assertRaises(HashBoundError):
            compare_declared_digest(LOCK_RELATIVE, b'{"a": \xff}\n', "0" * 64)

    def test_invalid_utf8_is_hashable_in_a_raw_class(self) -> None:
        # Raw mode binds bytes and never decodes them, so undecodable content is
        # a digest like any other rather than a refusal.
        payload = b"\xff\xfe\x00"
        relative = "docs/engineering/x/evidence/a.json"
        self.assertEqual(raw_sha256(payload), declared_digest(relative, payload))

    def test_an_undeclared_comparison_refuses_before_hashing(self) -> None:
        with self.assertRaises(HashBoundError):
            compare_declared_digest("README.md", b"synthetic\n", raw_sha256(b"synthetic\n"))


class LegacyNewlineRetirementTests(unittest.TestCase):
    """WO-HUP-012 (HUP-LSF-006): no newline-variant digest matches anything."""

    def test_the_recorded_prior_lock_digest_is_unchanged_on_disk(self) -> None:
        # The historical work order keeps its recorded digest as retained data;
        # nothing recomputes or rewrites it.
        text = UPGRADE_WORK_ORDER.read_text(encoding="utf-8")
        self.assertIn(f'prior_lock_sha256 = "{RECORDED_PRIOR_LOCK_SHA256}"', text)

    @unittest.skipUnless(
        revision_available(RECORDED_PRIOR_LOCK_COMMIT), "the historical lock revision is unavailable"
    )
    def test_the_recorded_digest_is_a_newline_variant_of_the_historical_lock(self) -> None:
        blob = historical_lock()
        self.assertNotIn(b"\r", blob)
        self.assertNotEqual(RECORDED_PRIOR_LOCK_SHA256, canonical_sha256(blob))
        self.assertEqual(RECORDED_PRIOR_LOCK_SHA256, raw_sha256(blob.replace(b"\n", b"\r\n")))

    @unittest.skipUnless(
        revision_available(RECORDED_PRIOR_LOCK_COMMIT), "the historical lock revision is unavailable"
    )
    def test_a_newline_variant_digest_no_longer_matches_any_materialization(self) -> None:
        for name, value in newline_forms(historical_lock()).items():
            with self.subTest(materialization=name):
                self.assertEqual(
                    MATCH_MISMATCH,
                    compare_declared_digest(LOCK_RELATIVE, value, RECORDED_PRIOR_LOCK_SHA256),
                )

    def test_the_match_vocabulary_is_binary(self) -> None:
        self.assertEqual((MATCH_DECLARED, MATCH_MISMATCH), hash_bound.MATCH_RESULTS)
        payload = b'{"schema": 3}\n'
        self.assertEqual(
            MATCH_MISMATCH,
            compare_declared_digest(
                LOCK_RELATIVE, payload, raw_sha256(payload.replace(b"\n", b"\r\n"))
            ),
        )
        self.assertEqual(
            MATCH_DECLARED,
            compare_declared_digest(LOCK_RELATIVE, payload, canonical_sha256(payload)),
        )

    def test_a_raw_class_is_never_relaxed_to_a_newline_variant(self) -> None:
        relative = "docs/engineering/x/evidence/a.json"
        payload = b'{"a": 1}\n'
        self.assertEqual(
            MATCH_MISMATCH,
            compare_declared_digest(
                relative, payload, raw_sha256(payload.replace(b"\n", b"\r\n"))
            ),
        )


class ProducerNewlineTests(unittest.TestCase):
    """A producer of hash-bound text fixes its newlines instead of the platform."""


    @unittest.skipUnless(git_available(), "git is unavailable")
    def test_an_initialized_lock_carries_no_carriage_return(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "initialized"
            completed = subprocess.run(
                [sys.executable, "-B", "-m", "se_harness", "init", str(target), "--project-name", "Assurance"],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            written = (target / LOCK_RELATIVE).read_bytes()
        self.assertNotIn(b"\r", written)
        # On a CRLF-default platform the two modes coincide only because the
        # producer chose LF; that coincidence is the assertion.
        self.assertEqual(raw_sha256(written), declared_digest(LOCK_RELATIVE, written))


class SafetyTests(unittest.TestCase):
    @unittest.skipUnless(git_available(), "git is unavailable")
    def test_unsafe_declared_path_shapes_are_refused(self) -> None:
        for pattern in ("/docs/a.json", "docs/../a.json", "docs/a\nb.json", "docs/a;b.json"):
            with self.subTest(pattern=pattern):
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "d.json"
                    path.write_text(
                        json.dumps(
                            {
                                "classes": [
                                    {
                                        "bindings": [],
                                        "id": "only",
                                        "mode": "raw",
                                        "patterns": [pattern],
                                        "region": "repository",
                                        "required_attribute": "text eol=lf",
                                    }
                                ],
                                "schema": "se-harness-hash-bound-classes-v1",
                                "removed_field": [],
                            }
                        ),
                        encoding="utf-8",
                    )
                    with self.assertRaises(HashBoundError):
                        load_declaration(path)

    @unittest.skipUnless(git_available(), "git is unavailable")
    def test_a_symlinked_covered_path_changes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            build_source(root, committed_attributes())
            target = root / "docs" / "engineering" / "x" / "evidence" / "link.json"
            try:
                target.symlink_to(root / "README.md")
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation is unavailable")
            git(root, "add", "-A")
            git(root, "-c", "core.autocrlf=false", "commit", "-q", "-m", "link")
            before = worktree_state(root)
            observed = results(root)
            self.assertEqual(before, worktree_state(root))
        self.assertIn(CHECK_ATTRIBUTE_EFFECTIVE, observed)


class UnmodifiedBehaviourTests(unittest.TestCase):
    def test_integrity_surface_is_unchanged(self) -> None:
        from se_harness import integrity

        self.assertEqual("utf8-text-lf-v1", integrity.HASH_MODE)
        self.assertEqual(CANONICAL_MODE, integrity.HASH_MODE)
        self.assertEqual(3, integrity.LOCK_SCHEMA)


    @unittest.skipUnless(git_available(), "git is unavailable")
    def test_cli_help_still_lists_doctor(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-B", "-m", "se_harness", "--help"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("doctor", completed.stdout)


if __name__ == "__main__":
    unittest.main()


@unittest.skipUnless(git_available(), "git is unavailable")
class LocalFormatTests(unittest.TestCase):
    def test_new_checksum_field_needs_no_registry(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            build_source(root, committed_attributes())
            path = root / "docs/engineering/note.md"
            path.write_text('+++\nid = "NOTE-001"\nunrelated_sha256 = "not a consumed checksum"\n+++\n', encoding="utf-8")
            git(root, "add", ".")
            self.assertTrue(results(root)[CHECK_CLASS_DECLARED][0])

    def test_equivalent_attribute_locations_have_the_same_result(self):
        rule = b"docs/engineering/**/evidence/*.json text eol=lf\n"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            build_source(root, b"# se-harness:begin\n" + rule + b"# se-harness:end\n")
            before = results(root)[CHECK_ATTRIBUTE_EFFECTIVE]
            (root / ".gitattributes").write_bytes(b"# se-harness:begin\n# se-harness:end\n" + rule)
            after = results(root)[CHECK_ATTRIBUTE_EFFECTIVE]
            self.assertTrue(before[0], before[1])
            self.assertEqual(before, after)
