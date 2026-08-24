"""Verification for the repository publication rehearsal (VER-RLO-005).

The rehearsal program itself runs a full release qualification, which no unit
test may do. What is tested here is every decision the program makes without a
network, a build, or an authorized release: platform layout resolution, alias
canonicalization, link-safe teardown, determinism reporting, candidate-plan
derivation, the data-only declaration, the bounded workflow reader, command-key
extraction, job classification, and both divergence directions. Job structures
are supplied as fixtures so no third-party parser is required.
"""

from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import unittest
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / ".github" / "scripts" / "rehearse_publication.py"
DECLARATION_PATH = (
    REPOSITORY_ROOT / ".github" / "scripts" / "publication_rehearsal_mechanics.json"
)
ORCHESTRATOR_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "publish-pypi.yml"
LANE_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "publication-rehearsal.yml"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "publication_rehearsal"

SPEC = importlib.util.spec_from_file_location("publication_rehearsal_test_module", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - packaging accident
    raise RuntimeError("cannot load the publication rehearsal module")
REHEARSAL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = REHEARSAL
SPEC.loader.exec_module(REHEARSAL)

#: The release orchestrator must stay byte-unchanged under WO-RLO-005. The digest
#: is taken over the file with LF endings so a checkout that materializes CRLF
#: compares equal to the stored blob.
ORCHESTRATOR_LF_SHA256 = "d7313d16db7f013e4f8b961840eb60af31c27633a1366f95362e5befab9d51a2"


def lf_digest(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(raw).hexdigest()


def make_temporary_directory(case: unittest.TestCase) -> Path:
    directory = Path(tempfile.mkdtemp(prefix="rehearsal-test-"))
    case.addCleanup(shutil.rmtree, directory, ignore_errors=True)
    return Path(os.path.realpath(directory))


def try_directory_symlink(case: unittest.TestCase, link: Path, target: Path) -> bool:
    """Create a directory link, or report that this platform withheld the right.

    Symlink creation is unprivileged on the Linux runner and privileged on the
    Windows one, so Windows falls back to a junction, which needs no privilege
    and is the link shape a virtual environment or a build tool actually leaves
    behind there. Both shapes must be unlinked rather than followed.
    """
    try:
        os.symlink(target, link, target_is_directory=True)
        return True
    except (OSError, NotImplementedError):
        pass
    if os.name != "nt":
        return False
    completed = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(link), str(target)],
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0 and link.exists()


class PlatformLayoutTests(unittest.TestCase):
    def test_scripts_layout_is_derived_from_the_platform(self) -> None:
        root = Path("/opt/example-venv") if os.name != "nt" else Path(r"C:\example-venv")
        scripts = REHEARSAL.venv_scripts_directory(root)
        scheme = "nt_venv" if os.name == "nt" else "posix_venv"
        expected = Path(
            sysconfig.get_path(
                "scripts",
                scheme,
                vars={
                    "base": str(root),
                    "platbase": str(root),
                    "installed_base": str(root),
                    "installed_platbase": str(root),
                },
            )
        )
        self.assertEqual(expected, scripts)
        self.assertEqual("Scripts" if os.name == "nt" else "bin", scripts.name)
        self.assertEqual(scripts / ("python.exe" if os.name == "nt" else "python"),
                         REHEARSAL.venv_python(root))
        self.assertEqual(scripts / ("harnessctl.exe" if os.name == "nt" else "harnessctl"),
                         REHEARSAL.venv_entry_point(root, "harnessctl"))

    def test_source_hardcodes_neither_layout_name(self) -> None:
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        for hardcoded in ('"Scripts"', "'Scripts'", '/ "bin"', "'bin'"):
            self.assertNotIn(hardcoded, source)

    def test_absent_layout_fails_naming_the_platform_and_expectation(self) -> None:
        root = make_temporary_directory(self) / "missing-venv"
        with self.assertRaises(REHEARSAL.RehearsalError) as raised:
            REHEARSAL.assert_venv_layout(root)
        message = str(raised.exception)
        self.assertIn(REHEARSAL.platform_family(), message)
        self.assertIn(REHEARSAL.venv_scripts_directory(root).name, message)

    def test_runner_labels_map_to_families_and_refuse_the_unknown(self) -> None:
        self.assertEqual("Linux", REHEARSAL.runner_platform_family("ubuntu-latest"))
        self.assertEqual("Windows", REHEARSAL.runner_platform_family("windows-2022"))
        self.assertEqual("macOS", REHEARSAL.runner_platform_family("macos-14"))
        for invalid in (["ubuntu-latest"], None, "self-hosted", "${{ matrix.runner }}"):
            with self.subTest(label=invalid):
                with self.assertRaises(REHEARSAL.RehearsalError):
                    REHEARSAL.runner_platform_family(invalid)


class CanonicalPathTests(unittest.TestCase):
    def test_relative_segments_and_trailing_separators_canonicalize(self) -> None:
        base = make_temporary_directory(self)
        (base / "child").mkdir()
        spellings = [
            str(base / "child"),
            f"{base / 'child'}{os.sep}",
            str(base / "." / "child"),
            str(base / "child" / ".." / "child"),
        ]
        resolved = {
            REHEARSAL.canonical_existing_directory(spelling, label="root")
            for spelling in spellings
        }
        self.assertEqual({base / "child"}, resolved)

    def test_an_alias_resolves_to_the_directory_it_points_at(self) -> None:
        base = make_temporary_directory(self)
        target = base / "real"
        target.mkdir()
        alias = base / "alias"
        if not try_directory_symlink(self, alias, target):
            self.skipTest("this platform withheld the right to create a directory link")
        self.assertEqual(
            target, REHEARSAL.canonical_existing_directory(alias, label="rehearsal root")
        )

    def test_missing_and_non_directory_paths_are_refused(self) -> None:
        base = make_temporary_directory(self)
        absent = base / "absent"
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "cannot be canonicalized"):
            REHEARSAL.canonical_existing_directory(absent, label="rehearsal root")
        regular = base / "file.txt"
        regular.write_text("data\n", encoding="utf-8")
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "is not a directory"):
            REHEARSAL.canonical_existing_directory(regular, label="rehearsal root")


class TeardownTests(unittest.TestCase):
    def test_containment_is_component_wise(self) -> None:
        base = make_temporary_directory(self)
        root = base / "rehearsal"
        root.mkdir()
        (root / "inner").mkdir()
        sibling = base / "rehearsal-2"
        sibling.mkdir()
        root_real = os.path.realpath(root)
        self.assertTrue(REHEARSAL.path_is_within(root_real, root))
        self.assertTrue(REHEARSAL.path_is_within(root_real, root / "inner"))
        self.assertTrue(REHEARSAL.path_is_within(root_real, root / "inner" / "deeper"))
        self.assertFalse(REHEARSAL.path_is_within(root_real, sibling))
        self.assertFalse(REHEARSAL.path_is_within(root_real, base))
        other_drive = "Z:\\elsewhere" if os.name == "nt" else "/elsewhere"
        self.assertFalse(REHEARSAL.path_is_within(root_real, other_drive))

    def test_a_tree_is_removed_and_every_deletion_reported(self) -> None:
        root = make_temporary_directory(self) / "derived"
        (root / "a" / "b").mkdir(parents=True)
        (root / "a" / "b" / "file.txt").write_text("x\n", encoding="utf-8")
        (root / "top.txt").write_text("y\n", encoding="utf-8")
        deleted: list[str] = []
        REHEARSAL.remove_tree_without_following_links(root, deleted)
        self.assertFalse(root.exists())
        self.assertEqual(5, len(deleted))
        self.assertIn(root.as_posix(), deleted)

    def test_an_absent_root_is_not_an_error(self) -> None:
        deleted: list[str] = []
        REHEARSAL.remove_tree_without_following_links(
            make_temporary_directory(self) / "never-created", deleted
        )
        self.assertEqual([], deleted)

    def test_a_link_out_of_the_root_is_unlinked_and_its_target_survives(self) -> None:
        base = make_temporary_directory(self)
        outside = base / "outside"
        outside.mkdir()
        (outside / "keep.txt").write_text("keep\n", encoding="utf-8")
        root = base / "derived"
        (root / "venv").mkdir(parents=True)
        if not try_directory_symlink(self, root / "venv" / "escape", outside):
            self.skipTest("this platform withheld the right to create a directory link")
        deleted: list[str] = []
        REHEARSAL.remove_tree_without_following_links(root, deleted)
        self.assertFalse(root.exists())
        self.assertTrue((outside / "keep.txt").is_file())
        self.assertIn((root / "venv" / "escape").as_posix(), deleted)

    def test_a_linked_root_is_refused_rather_than_followed(self) -> None:
        base = make_temporary_directory(self)
        target = base / "real"
        target.mkdir()
        (target / "keep.txt").write_text("keep\n", encoding="utf-8")
        alias = base / "linked-root"
        if not try_directory_symlink(self, alias, target):
            self.skipTest("this platform withheld the right to create a directory link")
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "linked rehearsal root"):
            REHEARSAL.remove_tree_without_following_links(alias, [])
        self.assertTrue((target / "keep.txt").is_file())


class _TeardownAuditStub:
    """The state `Rehearsal._teardown` reads, without a repository or a rehearsal.

    The post-audit is the subject: it re-examines what the removal reported rather
    than trusting it. Driving the real method keeps the audited list the one the
    remover actually produced.
    """

    def __init__(self, root: Path, *, status_before: str = "") -> None:
        self.root = root
        self.repository = root
        self.candidate_checkout = root / "candidate-checkout"
        self.deleted_paths: list[str] = []
        self.git_status_before = status_before
        self.commands: list[list[str]] = []

    def _run(self, argv: Any, **_: Any) -> None:
        self.commands.append([str(item) for item in argv])

    def _git(self, *_: str) -> str:
        return self.git_status_before


class TeardownAuditTests(unittest.TestCase):
    def test_the_root_s_own_removal_satisfies_the_audit(self) -> None:
        root = make_temporary_directory(self) / "derived"
        (root / "a").mkdir(parents=True)
        (root / "a" / "file.txt").write_text("x\n", encoding="utf-8")
        stub = _TeardownAuditStub(root)
        detail, evidence = REHEARSAL.Rehearsal._teardown(stub)
        self.assertFalse(root.exists())
        # The root is reported as removed, and its parent lies outside the root, so an
        # audit that examined every parent would refuse the removal it just performed.
        self.assertIn(root.as_posix(), stub.deleted_paths)
        self.assertIn("removed without following a link", detail)
        self.assertEqual(len(stub.deleted_paths), evidence["removed_paths"])
        self.assertTrue(evidence["repository_worktree_clean"])
        self.assertEqual([], evidence["residue"])

    def test_a_deletion_outside_the_root_is_still_refused(self) -> None:
        base = make_temporary_directory(self)
        root = base / "derived"
        root.mkdir()
        stub = _TeardownAuditStub(root)
        stub.deleted_paths.append((base / "elsewhere.txt").as_posix())
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "outside the rehearsal root"):
            REHEARSAL.Rehearsal._teardown(stub)

    def test_a_sibling_sharing_the_root_s_name_prefix_is_refused(self) -> None:
        base = make_temporary_directory(self)
        root = base / "derived"
        root.mkdir()
        stub = _TeardownAuditStub(root)
        stub.deleted_paths.append((base / "derived-2").as_posix())
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "outside the rehearsal root"):
            REHEARSAL.Rehearsal._teardown(stub)

    def test_residue_the_rehearsal_did_not_inherit_is_refused(self) -> None:
        root = make_temporary_directory(self) / "derived"
        root.mkdir(parents=True)
        stub = _TeardownAuditStub(root)
        stub.git_status_before = ""
        stub._git = lambda *_: "?? leftover\n"  # type: ignore[method-assign]
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "untracked or modified"):
            REHEARSAL.Rehearsal._teardown(stub)

    def test_inherited_uncommitted_entries_are_not_read_as_residue(self) -> None:
        root = make_temporary_directory(self) / "derived"
        root.mkdir(parents=True)
        stub = _TeardownAuditStub(root, status_before=" M docs/notes/README.md\n")
        _, evidence = REHEARSAL.Rehearsal._teardown(stub)
        self.assertEqual([], evidence["residue"])
        self.assertFalse(evidence["repository_worktree_clean"])


class _PredecessorSubjectStub:
    """The state `Rehearsal._predecessor_view_exclusion` reads."""

    def __init__(self, repository: Path, mode: str, subject: str, evaluator: dict[str, Any]) -> None:
        self.repository = repository
        self.mode = mode
        self.subject_record = subject
        self.evaluator = evaluator

    # The reader under test is the program's own, not a re-implementation of it.
    _declared_predecessor_evaluator = REHEARSAL.Rehearsal._declared_predecessor_evaluator


def _write_release_record(
    repository: Path,
    identifier: str,
    *,
    predecessor_version: str | None,
    predecessor_sha256: str | None,
) -> None:
    directory = repository / "docs" / "engineering" / "release-x"
    (directory / "evidence").mkdir(parents=True, exist_ok=True)
    frontmatter = [
        "+++",
        f'id = "{identifier}"',
        'type = "release_record"',
        'status = "released"',
    ]
    if predecessor_version is not None:
        evidence = directory / "evidence" / f"{identifier}-evaluator.json"
        evidence.write_text(
            json.dumps(
                {
                    "role": "released-evaluator",
                    "evaluator": {
                        "version": predecessor_version,
                        "archive_name": f"se_harness-{predecessor_version}-py3-none-any.whl",
                        "archive_sha256": predecessor_sha256,
                    },
                }
            )
            + "\n",
            encoding="utf-8",
        )
        relative = evidence.relative_to(repository).as_posix()
        frontmatter.append(f'evaluator_evidence_path = "{relative}"')
    frontmatter += ["+++", "", f"# {identifier}", ""]
    (directory / f"{identifier}.md").write_text("\n".join(frontmatter), encoding="utf-8")


class PredecessorViewSubjectTests(unittest.TestCase):
    """A released record cannot be the subject of its successor's predecessor view.

    The orchestrator resolves the evaluator from the schema-3 lock and qualifies the
    candidate against the record's own predecessor contract. Those agree while a record
    is being prepared and disagree by one release afterwards, so candidate mode has to
    report the mechanic as excluded with both measured identities rather than let a
    subject mismatch read as a failure of the publication path.
    """

    RESOLVED = "1" * 64
    OTHER = "2" * 64

    def test_a_record_binding_the_resolved_evaluator_is_a_valid_subject(self) -> None:
        repository = make_temporary_directory(self)
        _write_release_record(
            repository, "RLS-SEH-099", predecessor_version="0.6.0", predecessor_sha256=self.RESOLVED
        )
        stub = _PredecessorSubjectStub(
            repository, "candidate", "RLS-SEH-099", {"version": "0.6.0", "sha256": self.RESOLVED}
        )
        self.assertIsNone(REHEARSAL.Rehearsal._predecessor_view_exclusion(stub))

    def test_a_record_binding_another_evaluator_excludes_and_names_both(self) -> None:
        repository = make_temporary_directory(self)
        _write_release_record(
            repository, "RLS-SEH-099", predecessor_version="0.5.0", predecessor_sha256=self.OTHER
        )
        stub = _PredecessorSubjectStub(
            repository, "candidate", "RLS-SEH-099", {"version": "0.6.0", "sha256": self.RESOLVED}
        )
        exclusion = REHEARSAL.Rehearsal._predecessor_view_exclusion(stub)
        self.assertIsNotNone(exclusion)
        assert exclusion is not None
        reason, evidence = exclusion
        self.assertIn("0.6.0", reason)
        self.assertIn("0.5.0", reason)
        self.assertIn("RLS-SEH-099", reason)
        self.assertEqual("0.6.0", evidence["resolved_evaluator_version"])
        self.assertEqual(self.RESOLVED, evidence["resolved_evaluator_sha256"])
        self.assertEqual("0.5.0", evidence["record_predecessor_evaluator_version"])
        self.assertEqual(self.OTHER, evidence["record_predecessor_evaluator_sha256"])

    def test_a_record_binding_no_predecessor_contract_excludes_and_says_so(self) -> None:
        repository = make_temporary_directory(self)
        _write_release_record(
            repository, "RLS-SEH-099", predecessor_version=None, predecessor_sha256=None
        )
        stub = _PredecessorSubjectStub(
            repository, "candidate", "RLS-SEH-099", {"version": "0.6.0", "sha256": self.RESOLVED}
        )
        exclusion = REHEARSAL.Rehearsal._predecessor_view_exclusion(stub)
        assert exclusion is not None
        reason, evidence = exclusion
        self.assertIn("binds no predecessor evaluator contract", reason)
        self.assertIsNone(evidence["record_predecessor_evaluator_version"])

    def test_release_record_mode_never_excludes(self) -> None:
        repository = make_temporary_directory(self)
        _write_release_record(
            repository, "RLS-SEH-099", predecessor_version="0.5.0", predecessor_sha256=self.OTHER
        )
        stub = _PredecessorSubjectStub(
            repository,
            "release-record",
            "RLS-SEH-099",
            {"version": "0.6.0", "sha256": self.RESOLVED},
        )
        # A record under preparation must bind the governing evaluator, so a mismatch
        # there is a defect in the record and has to fail rather than be excluded.
        self.assertIsNone(REHEARSAL.Rehearsal._predecessor_view_exclusion(stub))

    def test_the_governing_lock_and_the_newest_released_record_disagree_here(self) -> None:
        """Measure the condition on the repository itself rather than asserting it."""
        lock = json.loads(
            (REPOSITORY_ROOT / ".engineering-harness.lock").read_text(encoding="utf-8")
        )
        self.assertEqual(3, lock.get("schema"))
        governing = lock["evaluator"]["archive_sha256"]
        bound = set()
        for path in sorted((REPOSITORY_ROOT / "docs" / "engineering").rglob("RLS-*.md")):
            text = path.read_text(encoding="utf-8")
            if 'status = "released"' not in text:
                continue
            for line in text.splitlines():
                if line.startswith("evaluator_evidence_path = "):
                    evidence = REPOSITORY_ROOT / line.split('"')[1]
                    evaluator = json.loads(evidence.read_text(encoding="utf-8"))["evaluator"]
                    bound.add(evaluator["archive_sha256"])
        self.assertNotIn(
            governing,
            bound,
            "a released record binds the governing evaluator; candidate mode can now "
            "exercise predecessor-view qualification and this expectation is stale",
        )


class DeterminismReportingTests(unittest.TestCase):
    def write(self, directory: Path, name: str, payload: bytes) -> Path:
        path = directory / name
        path.write_bytes(payload)
        return path

    def test_identical_files_report_no_difference(self) -> None:
        base = make_temporary_directory(self)
        left = self.write(base, "left", b"identical payload")
        right = self.write(base, "right", b"identical payload")
        self.assertIsNone(REHEARSAL.first_difference(left, right))
        self.assertEqual(REHEARSAL.sha256_file(left), REHEARSAL.sha256_file(right))
        self.assertEqual(
            hashlib.sha256(b"identical payload").hexdigest(), REHEARSAL.sha256_file(left)
        )

    def test_the_first_differing_offset_is_reported(self) -> None:
        base = make_temporary_directory(self)
        left = self.write(base, "left", b"abcdef")
        right = self.write(base, "right", b"abcXef")
        self.assertEqual(3, REHEARSAL.first_difference(left, right))

    def test_a_length_difference_is_reported_at_the_shorter_end(self) -> None:
        base = make_temporary_directory(self)
        left = self.write(base, "left", b"abcdef")
        right = self.write(base, "right", b"abc")
        self.assertEqual(3, REHEARSAL.first_difference(left, right))
        self.assertEqual(3, REHEARSAL.first_difference(right, left))


class CandidatePlanDerivationTests(unittest.TestCase):
    def base_plan(self) -> dict[str, Any]:
        plan = {key: "" for key in REHEARSAL.CANDIDATE_PLAN_MARKERS}
        plan.update({key: "" for key in REHEARSAL.CANDIDATE_PLAN_MEASURED})
        plan["governance_commit"] = ""
        plan["repository"] = "mmzen/se_harness"
        return plan

    def manifest(self) -> dict[str, Any]:
        return {
            "commit": "c" * 40,
            "git_object_format": "sha1",
            "version": "0.6.1",
            "source_date_epoch": "1787573480",
            "wheel": "se_harness-0.6.1-py3-none-any.whl",
            "wheel_sha256": "a" * 64,
            "sdist": "se_harness-0.6.1.tar.gz",
            "sdist_sha256": "b" * 64,
            "checksums": "SHA256SUMS",
            "checksums_sha256": "d" * 64,
            "source_manifest_sha256": "e" * 64,
        }

    def test_identity_comes_from_the_manifest_and_authority_is_marked_absent(self) -> None:
        plan = REHEARSAL.derive_rehearsal_plan(self.base_plan(), self.manifest(), "c" * 40)
        self.assertEqual(set(self.base_plan()), set(plan))
        self.assertEqual("c" * 40, plan["candidate_commit"])
        self.assertEqual("c" * 40, plan["governance_commit"])
        self.assertEqual("a" * 64, plan["wheel_sha256"])
        self.assertEqual(
            "REHEARSAL-CANDIDATE-MODE-NOT-A-RELEASE-RECORD", plan["release_record"]
        )
        self.assertEqual("rehearsal-candidate-mode", plan["tag"])
        self.assertNotRegex(plan["release_record"], r"^RLS-[A-Z0-9-]+-\d{3}$")
        for emptied in ("released_at", "release_contract", "release_record_path"):
            self.assertEqual("", plan[emptied])
        self.assertEqual([], plan["verification_records"])
        self.assertEqual("mmzen/se_harness", plan["repository"])

    def test_a_manifest_missing_a_measured_field_is_refused(self) -> None:
        manifest = self.manifest()
        del manifest["wheel_sha256"]
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "no wheel_sha256"):
            REHEARSAL.derive_rehearsal_plan(self.base_plan(), manifest, "c" * 40)

    def test_a_non_canonical_plan_field_set_is_refused(self) -> None:
        plan = self.base_plan()
        del plan["tag"]
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "not canonical"):
            REHEARSAL.derive_rehearsal_plan(plan, self.manifest(), "c" * 40)


class TemporaryIdentityTests(unittest.TestCase):
    def test_the_platform_case_rule_decides_identity(self) -> None:
        expected = r"C:\Temp\rehearsal" if os.name == "nt" else "/tmp/rehearsal"
        REHEARSAL.assert_temporary_identity(expected, expected)
        if os.name == "nt":
            REHEARSAL.assert_temporary_identity(expected, expected.upper())

    def test_a_mismatch_names_both_spellings(self) -> None:
        with self.assertRaises(REHEARSAL.RehearsalError) as raised:
            REHEARSAL.assert_temporary_identity(
                os.path.join("base", "rehearsal", "temp"),
                os.path.join("base", "RUNNER~1", "temp"),
            )
        message = str(raised.exception)
        self.assertIn("temporary-path identity divergence", message)
        self.assertIn("rehearsal", message)
        self.assertIn("RUNNER~1", message)

    def test_the_child_probe_observes_the_root_the_rehearsal_sets(self) -> None:
        root = make_temporary_directory(self)
        environment = dict(os.environ)
        for name in ("TMPDIR", "TEMP", "TMP"):
            environment[name] = str(root)
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                "import os, tempfile; print(os.path.realpath(tempfile.gettempdir()))",
            ],
            capture_output=True,
            text=True,
            check=True,
            env=environment,
        )
        REHEARSAL.assert_temporary_identity(str(root), completed.stdout.strip())


class DeclarationTests(unittest.TestCase):
    def test_the_repository_declaration_is_data_only(self) -> None:
        declaration = REHEARSAL.load_declaration(DECLARATION_PATH)
        self.assertEqual(REHEARSAL.DECLARATION_SCHEMA, declaration["schema"])
        self.assertEqual(".github/workflows/publish-pypi.yml", declaration["orchestrator"])
        self.assertEqual(
            ".github/workflows/publication-rehearsal.yml", declaration["rehearsal_lane"]
        )
        self.assertEqual(["Linux", "Windows"], sorted(declaration["required_platforms"]))
        index = REHEARSAL.declaration_index(declaration)
        self.assertEqual(len(declaration["mechanics"]), len(index))
        surfaces = set(declaration["realization_surfaces"])
        for mechanic in declaration["mechanics"]:
            with self.subTest(mechanic=mechanic["id"]):
                self.assertIn(mechanic["origin"], {"orchestrator", "rehearsal-only"})
                self.assertIsInstance(mechanic["commands"], list)
                self.assertIn(mechanic["realized_by"], surfaces)
                self.assertTrue(mechanic["summary"])
        for step in declaration["steps"]:
            with self.subTest(step=step["step"]):
                self.assertRegex(step["run_sha256"], r"^[0-9a-f]{64}$")
                self.assertTrue(step["mechanics"])

    def test_every_declared_mechanic_is_run_by_the_program(self) -> None:
        declaration = REHEARSAL.load_declaration(DECLARATION_PATH)
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        for mechanic in declaration["mechanics"]:
            with self.subTest(mechanic=mechanic["id"]):
                self.assertIn(f'"{mechanic["id"]}"', source)

    def test_an_undeclared_realization_surface_is_refused(self) -> None:
        base = make_temporary_directory(self)
        path = base / "mechanics.json"
        payload = {
            "schema": REHEARSAL.DECLARATION_SCHEMA,
            "steps": [],
            "trivia_commands": [],
            "required_platforms": [],
            "realization_surfaces": ["rehearsal-program"],
            "mechanics": [{"id": "one", "realized_by": "an-invented-surface"}],
        }
        path.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaisesRegex(
            REHEARSAL.RehearsalError, "undeclared realization surface"
        ):
            REHEARSAL.load_declaration(path)

    def test_every_declared_step_mechanic_is_a_declared_mechanic(self) -> None:
        declaration = REHEARSAL.load_declaration(DECLARATION_PATH)
        index = REHEARSAL.declaration_index(declaration)
        for step in declaration["steps"]:
            for identifier in step["mechanics"]:
                with self.subTest(step=step["step"], mechanic=identifier):
                    self.assertIn(identifier, index)
                    self.assertEqual(step["job"], index[identifier]["job"])

    def test_a_non_json_declaration_is_refused(self) -> None:
        base = make_temporary_directory(self)
        path = base / "mechanics.yaml"
        path.write_text("schema: anything\n", encoding="utf-8")
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "must be JSON data"):
            REHEARSAL.load_declaration(path)

    def test_a_repeated_key_is_refused(self) -> None:
        base = make_temporary_directory(self)
        path = base / "mechanics.json"
        path.write_text(
            '{"schema": "one", "schema": "two"}', encoding="utf-8"
        )
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "repeats the key"):
            REHEARSAL.load_declaration(path)

    def test_an_executable_shaped_declaration_is_refused(self) -> None:
        base = make_temporary_directory(self)
        for payload, expected in (
            ({"schema": "x", "__class__": "os.system"}, "executable-shaped"),
            ({"schema": "x", "mechanics": [{"eval": "1+1"}]}, "executable-shaped"),
            ({"schema": "x", "steps": [{"run": "rm -rf /"}]}, "executable-shaped"),
            ({"schema": "x", "nested": {"deep": {"exec": "x"}}}, "executable-shaped"),
        ):
            with self.subTest(payload=sorted(payload)):
                path = base / "mechanics.json"
                path.write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaisesRegex(REHEARSAL.RehearsalError, expected):
                    REHEARSAL.load_declaration(path)

    def test_the_schema_and_array_shapes_are_required(self) -> None:
        base = make_temporary_directory(self)
        path = base / "mechanics.json"
        path.write_text('{"schema": "other/v1"}', encoding="utf-8")
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "declaration schema must be"):
            REHEARSAL.load_declaration(path)
        path.write_text(
            json.dumps({"schema": REHEARSAL.DECLARATION_SCHEMA, "mechanics": {}}),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "mechanics must be an array"):
            REHEARSAL.load_declaration(path)
        path.write_text(
            json.dumps(
                {
                    "schema": REHEARSAL.DECLARATION_SCHEMA,
                    "mechanics": [{"id": "same"}, {"id": "same"}],
                    "steps": [],
                    "trivia_commands": [],
                    "required_platforms": [],
                    "realization_surfaces": [],
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "repeats a mechanic identifier"):
            REHEARSAL.load_declaration(path)

    def test_a_mapping_is_required(self) -> None:
        base = make_temporary_directory(self)
        path = base / "mechanics.json"
        path.write_text("[]", encoding="utf-8")
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "must be a mapping"):
            REHEARSAL.load_declaration(path)
        path.write_text("{", encoding="utf-8")
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "not strict JSON data"):
            REHEARSAL.load_declaration(path)


class BoundedWorkflowReaderTests(unittest.TestCase):
    def parse(self, text: str) -> dict[str, Any]:
        return REHEARSAL._WorkflowReader(text, "fixture.yml").parse()

    def test_the_actions_subset_is_read(self) -> None:
        value = self.parse(
            "name: Example\n"
            "on:\n"
            "  workflow_dispatch:\n"
            "    inputs:\n"
            "      release_record:\n"
            "        required: true\n"
            "permissions: {}\n"
            "env:\n"
            '  PYTHON_VERSION: "3.11"\n'
            "jobs:\n"
            "  build:\n"
            "    runs-on: ubuntu-latest\n"
            "    permissions:\n"
            "      contents: read\n"
            "    strategy:\n"
            "      matrix:\n"
            "        include:\n"
            "          - runner: ubuntu-latest\n"
            "            platform: Linux\n"
            "    steps:\n"
            "      - name: Literal block  # trailing comment\n"
            "        run: |\n"
            "          set -euo pipefail\n"
            "          echo one\n"
            "      - name: Folded block\n"
            "        run: >-\n"
            "          one\n"
            "          two\n"
            "\n"
            "          three\n"
            "      - uses: actions/checkout@v7\n"
            "        with:\n"
            "          fetch-depth: 0\n"
            "          persist-credentials: false\n"
            "        env:\n"
            "          FLOW: [a, b]\n"
        )
        self.assertEqual("Example", value["name"])
        self.assertEqual({}, value["permissions"])
        self.assertEqual("3.11", value["env"]["PYTHON_VERSION"])
        self.assertTrue(value["on"]["workflow_dispatch"]["inputs"]["release_record"]["required"])
        job = value["jobs"]["build"]
        self.assertEqual({"contents": "read"}, job["permissions"])
        self.assertEqual(
            [{"runner": "ubuntu-latest", "platform": "Linux"}],
            job["strategy"]["matrix"]["include"],
        )
        self.assertEqual("Literal block", job["steps"][0]["name"])
        self.assertEqual("set -euo pipefail\necho one\n", job["steps"][0]["run"])
        self.assertEqual("one two\nthree", job["steps"][1]["run"])
        self.assertEqual(0, job["steps"][2]["with"]["fetch-depth"])
        self.assertFalse(job["steps"][2]["with"]["persist-credentials"])
        self.assertEqual(["a", "b"], job["steps"][2]["env"]["FLOW"])

    def test_a_hash_inside_a_quoted_scalar_is_not_a_comment(self) -> None:
        value = self.parse(
            "jobs:\n"
            "  build:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            '      - name: "Tag #1"\n'
            "        run: echo kept\n"
        )
        self.assertEqual("Tag #1", value["jobs"]["build"]["steps"][0]["name"])

    def test_shapes_outside_the_subset_are_refused(self) -> None:
        cases = {
            "anchor": "jobs:\n  build: &anchor\n    runs-on: ubuntu-latest\n",
            "alias": "jobs:\n  build: *anchor\n",
            "tag": "jobs: !!map\n",
            "tab": "jobs:\n\tbuild: x\n",
            "duplicate": (
                "jobs:\n  build:\n    runs-on: ubuntu-latest\n    runs-on: windows-2022\n"
            ),
            "keep_chomping": (
                "jobs:\n  build:\n    steps:\n      - run: |+\n          echo x\n"
            ),
            "unterminated_double": 'name: "unfinished\njobs:\n  build: x\n',
            "unterminated_single": "name: 'unfinished\njobs:\n  build: x\n",
            "unterminated_flow": "name: [a, b\njobs:\n  build: x\n",
            "empty": "\n#  only a comment\n",
        }
        for label, text in cases.items():
            with self.subTest(shape=label):
                with self.assertRaises(REHEARSAL.RehearsalError):
                    self.parse(text)

    def test_a_missing_or_malformed_job_mapping_is_refused(self) -> None:
        base = make_temporary_directory(self)
        path = base / "workflow.yml"
        path.write_text("name: Example\n", encoding="utf-8")
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "no job mapping"):
            REHEARSAL.read_workflow(path)
        path.write_text("jobs:\n  build: not-a-mapping\n", encoding="utf-8")
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "is not a mapping"):
            REHEARSAL.read_workflow(path)
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "unreadable"):
            REHEARSAL.read_workflow(base / "absent.yml")

    def test_the_reader_and_the_repository_workflows_agree_on_job_structure(self) -> None:
        for path in (ORCHESTRATOR_PATH, LANE_PATH):
            with self.subTest(workflow=path.name):
                workflow = REHEARSAL.read_workflow(path)
                self.assertTrue(workflow["jobs"])
                for name, job in workflow["jobs"].items():
                    self.assertIsInstance(job, dict, msg=name)


class CrossCheckTests(unittest.TestCase):
    """The optional second-parser cross-check, exercised without a dependency."""

    def install(self, module: Any) -> None:
        previous = sys.modules.get("yaml", "absent")
        sys.modules["yaml"] = module

        def restore() -> None:
            if previous == "absent":
                sys.modules.pop("yaml", None)
            else:
                sys.modules["yaml"] = previous

        self.addCleanup(restore)

    def stub(self, payload: Any) -> Any:
        class Error(Exception):
            pass

        class Stub:
            YAMLError = Error

            @staticmethod
            def safe_load(_: str) -> Any:
                if isinstance(payload, Exception):
                    raise payload
                return payload

        return Stub()

    def workflow(self) -> tuple[Path, dict[str, Any]]:
        base = make_temporary_directory(self)
        path = base / "workflow.yml"
        path.write_text(
            "jobs:\n"
            "  build:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - name: One\n"
            "        run: echo one\n",
            encoding="utf-8",
        )
        return path, {
            "jobs": {
                "build": {
                    "runs-on": "ubuntu-latest",
                    "steps": [{"name": "One", "run": "echo one"}],
                }
            }
        }

    def test_an_agreeing_parser_passes(self) -> None:
        path, reference = self.workflow()
        self.install(self.stub(reference))
        value = REHEARSAL.read_workflow(path, cross_check=True)
        self.assertEqual(reference["jobs"], value["jobs"])

    def test_a_disagreeing_parser_names_the_job(self) -> None:
        path, reference = self.workflow()
        reference = copy.deepcopy(reference)
        reference["jobs"]["build"]["runs-on"] = "windows-2022"
        self.install(self.stub(reference))
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "disagree about build"):
            REHEARSAL.read_workflow(path, cross_check=True)

    def test_a_reference_parse_without_jobs_is_refused(self) -> None:
        path, _ = self.workflow()
        self.install(self.stub({"name": "no jobs"}))
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "under a reference parse"):
            REHEARSAL.read_workflow(path, cross_check=True)

    def test_an_absent_parser_is_reported_rather_than_ignored(self) -> None:
        path, _ = self.workflow()
        self.install(None)
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "PyYAML is not installed"):
            REHEARSAL.read_workflow(path, cross_check=True)


class CommandKeyTests(unittest.TestCase):
    def test_redirections_and_substitutions_stay_inside_their_word(self) -> None:
        script = (
            "set -euo pipefail\n"
            'python -m se_harness doctor "$GITHUB_WORKSPACE" 2>&1\n'
            'echo "failed" >&2\n'
            'cmp --silent "$(pwd)/a" "${{ runner.temp }}/b"\n'
        )
        keys = REHEARSAL.command_keys(script)
        self.assertIn("cmp", keys)
        self.assertIn("python -m se_harness doctor", keys)
        for bogus in ("1", "2", ""):
            self.assertNotIn(bogus, keys)

    def test_a_literal_argument_carrying_whitespace_is_kept_verbatim(self) -> None:
        keys = REHEARSAL.command_keys('printf "%s  %s\\n" one two\n')
        self.assertEqual(1, len(keys))
        self.assertTrue(keys[0].startswith("printf"))

    def test_a_prefix_never_satisfies_a_longer_declared_command(self) -> None:
        keys = REHEARSAL.command_keys("python -m pip install --no-deps wheel\n")
        self.assertIn("python -m pip install", keys)
        self.assertNotIn("python", keys)
        self.assertNotIn("python -m pip", keys)

    def test_an_array_assignment_is_not_a_command(self) -> None:
        keys = REHEARSAL.command_keys(
            "arguments=(\n  rehearse\n  --repository .\n)\n"
            'python .github/scripts/rehearse_publication.py "${arguments[@]}"\n'
        )
        self.assertNotIn("rehearse", keys)
        self.assertTrue(any(key.startswith("python ") for key in keys))

    def test_a_shell_keyword_leading_a_command_is_stripped(self) -> None:
        keys = REHEARSAL.command_keys("if ! python -m build --wheel .; then\n  exit 1\nfi\n")
        self.assertIn("python -m build", keys)


class JobClassificationTests(unittest.TestCase):
    def workflow(self) -> dict[str, Any]:
        return {
            "jobs": {
                "resolve": {
                    "runs-on": "ubuntu-latest",
                    "permissions": {"contents": "read"},
                    "steps": [
                        {
                            "name": "Check out",
                            "uses": "actions/checkout@" + "1" * 40,
                            "with": {"persist-credentials": False},
                        },
                        {"name": "Resolve", "run": "python resolve.py\n"},
                    ],
                },
                "qualify": {
                    "runs-on": "windows-2022",
                    "permissions": {"contents": "read"},
                    "needs": "resolve",
                    "steps": [{"name": "Build", "run": "python -m build .\n"}],
                },
                "pypi": {
                    "runs-on": "ubuntu-latest",
                    "permissions": {"id-token": "write"},
                    "environment": "pypi",
                    "needs": ["qualify"],
                    "steps": [{"name": "Upload", "uses": "pypa/gh-action-pypi-publish@v1"}],
                },
                "observe": {
                    "runs-on": "ubuntu-latest",
                    "permissions": {"contents": "read"},
                    "needs": ["pypi"],
                    "steps": [{"name": "Observe", "run": "echo observed\n"}],
                },
            }
        }

    def classify(self, workflow: dict[str, Any]) -> dict[str, Any]:
        return REHEARSAL.classify_jobs(workflow, ["pypa/gh-action-pypi-publish"])

    def test_credential_free_jobs_are_required_and_the_rest_report_their_attribute(self) -> None:
        classifications = self.classify(self.workflow())
        required = sorted(name for name, item in classifications.items() if not item.excluded)
        self.assertEqual(["qualify", "resolve"], required)
        self.assertEqual("Linux", classifications["resolve"].platform)
        self.assertEqual("Windows", classifications["qualify"].platform)
        self.assertIn("id-token: write permission", classifications["pypi"].attributes)
        self.assertIn("declares a protected environment", classifications["pypi"].attributes)
        self.assertIn(
            "uses the external-state action pypa/gh-action-pypi-publish",
            classifications["pypi"].attributes,
        )

    def test_exclusion_is_transitive(self) -> None:
        classifications = self.classify(self.workflow())
        self.assertTrue(classifications["observe"].excluded)
        self.assertEqual(
            ["depends on the excluded job pypi"], classifications["observe"].attributes
        )

    def test_a_disabled_credential_option_is_not_an_attribute(self) -> None:
        workflow = self.workflow()
        self.assertEqual([], self.classify(workflow)["resolve"].attributes)
        workflow["jobs"]["resolve"]["steps"][0]["with"]["persist-credentials"] = True
        self.assertTrue(self.classify(workflow)["resolve"].excluded)

    def test_a_read_all_permission_string_stays_credential_free(self) -> None:
        workflow = self.workflow()
        workflow["jobs"]["resolve"]["permissions"] = "read-all"
        self.assertFalse(self.classify(workflow)["resolve"].excluded)
        workflow["jobs"]["resolve"]["permissions"] = "write-all"
        self.assertTrue(self.classify(workflow)["resolve"].excluded)

    def test_an_absent_permission_block_is_an_attribute(self) -> None:
        workflow = self.workflow()
        del workflow["jobs"]["resolve"]["permissions"]
        self.assertIn(
            "declares no explicit permissions", self.classify(workflow)["resolve"].attributes
        )

    def test_a_secret_expression_or_token_env_is_an_attribute(self) -> None:
        workflow = self.workflow()
        workflow["jobs"]["resolve"]["steps"][1]["env"] = {"GH_TOKEN": "${{ github.token }}"}
        self.assertTrue(self.classify(workflow)["resolve"].excluded)
        workflow = self.workflow()
        workflow["jobs"]["resolve"]["env"] = {"VALUE": "${{ secrets.EXAMPLE }}"}
        self.assertTrue(self.classify(workflow)["resolve"].excluded)

    def test_unclassifiable_job_shapes_are_refused(self) -> None:
        cases: dict[str, Any] = {}
        workflow = self.workflow()
        workflow["jobs"]["resolve"] = "not-a-mapping"
        cases["non-mapping job"] = workflow
        workflow = self.workflow()
        workflow["jobs"]["resolve"]["permissions"] = ["contents"]
        cases["list permissions"] = workflow
        workflow = self.workflow()
        del workflow["jobs"]["resolve"]["steps"]
        cases["absent steps"] = workflow
        workflow = self.workflow()
        workflow["jobs"]["resolve"]["steps"] = ["not-a-mapping"]
        cases["non-mapping step"] = workflow
        workflow = self.workflow()
        workflow["jobs"]["qualify"]["needs"] = "absent"
        cases["unknown dependency"] = workflow
        workflow = self.workflow()
        workflow["jobs"]["resolve"]["runs-on"] = ["ubuntu-latest"]
        cases["list runs-on"] = workflow
        for label, broken in cases.items():
            with self.subTest(shape=label):
                with self.assertRaises(REHEARSAL.RehearsalError):
                    self.classify(broken)


class FixtureDivergenceTests(unittest.TestCase):
    """Both divergence directions against a miniature orchestrator and lane."""

    def setUp(self) -> None:
        self.repository = make_temporary_directory(self)
        workflows = self.repository / ".github" / "workflows"
        workflows.mkdir(parents=True)
        for name in ("orchestrator.yml", "lane.yml", "lane-linux-only.yml"):
            shutil.copy(FIXTURES / name, workflows / name)
        self.declaration = REHEARSAL.load_declaration(FIXTURES / "mechanics.json")

    def check(self, declaration: dict[str, Any] | None = None) -> dict[str, Any]:
        return REHEARSAL.check_divergence(
            self.repository, declaration if declaration is not None else self.declaration
        )

    def kinds(self, result: dict[str, Any]) -> list[str]:
        return [finding["kind"] for finding in result["findings"]]

    def orchestrator(self) -> Path:
        return self.repository / ".github" / "workflows" / "orchestrator.yml"

    def test_the_fixture_pair_does_not_diverge(self) -> None:
        result = self.check()
        self.assertEqual("exact", result["verdict"])
        self.assertEqual([], result["findings"])
        self.assertEqual(["qualify", "resolve"], result["rehearsed_jobs"])
        self.assertEqual(["Linux", "Windows"], result["orchestrator_platforms"])
        self.assertEqual(["Linux", "Windows"], result["lane"]["platforms"])
        self.assertTrue(result["lane"]["permissions_read_only"])
        excluded = {item["job"]: item["attributes"] for item in result["excluded_jobs"]}
        self.assertEqual({"observe", "pypi"}, set(excluded))
        self.assertEqual(["depends on the excluded job pypi"], excluded["observe"])
        coverage = {item["mechanic"]: item["coverage"] for item in result["mechanics"]}
        self.assertEqual("rehearsal-only", coverage["teardown"])
        self.assertEqual("covered", coverage["plan-resolution"])

    def test_an_undeclared_credential_free_step_fails_closed(self) -> None:
        text = self.orchestrator().read_text(encoding="utf-8")
        text = text.replace(
            "  pypi:\n",
            "      - name: Sign the artifacts\n"
            "        run: |\n"
            "          set -euo pipefail\n"
            "          python -m sigstore sign dist-a/wheel\n"
            "\n"
            "  pypi:\n",
        )
        self.orchestrator().write_text(text, encoding="utf-8", newline="\n")
        result = self.check()
        self.assertEqual("divergent", result["verdict"])
        finding = next(item for item in result["findings"] if item["kind"] == "undeclared_step")
        self.assertEqual("uncovered", finding["direction"])
        self.assertEqual("qualify", finding["job"])
        self.assertEqual("Sign the artifacts", finding["step"])
        self.assertRegex(finding["run_sha256"], r"^[0-9a-f]{64}$")
        self.assertIn("unclassified_command", self.kinds(result))

    def test_a_changed_step_script_fails_closed(self) -> None:
        text = self.orchestrator().read_text(encoding="utf-8")
        text = text.replace("cmp --silent dist-a/wheel", "cmp --quiet dist-a/wheel")
        self.orchestrator().write_text(text, encoding="utf-8", newline="\n")
        result = self.check()
        self.assertEqual("divergent", result["verdict"])
        finding = next(item for item in result["findings"] if item["kind"] == "changed_step")
        self.assertEqual("qualify", finding["job"])
        self.assertNotEqual(finding["declared_sha256"], finding["run_sha256"])

    def test_an_unnamed_credential_free_step_cannot_be_declared(self) -> None:
        text = self.orchestrator().read_text(encoding="utf-8")
        text = text.replace(
            "      - name: Build both deterministic distribution sets\n        run: |\n",
            "      - run: |\n",
        )
        self.orchestrator().write_text(text, encoding="utf-8", newline="\n")
        result = self.check()
        self.assertIn("unnamed_step", self.kinds(result))

    def test_a_stale_declared_step_fails_closed(self) -> None:
        declaration = copy.deepcopy(self.declaration)
        declaration["steps"].append(
            {
                "job": "resolve",
                "step": "A step publication no longer performs",
                "run_sha256": "0" * 64,
                "mechanics": ["plan-resolution"],
            }
        )
        declaration["steps"].append(
            {
                "job": "pypi",
                "step": "Upload the exact files",
                "run_sha256": "0" * 64,
                "mechanics": ["plan-resolution"],
            }
        )
        result = self.check(declaration)
        self.assertEqual("divergent", result["verdict"])
        stale = [item for item in result["findings"] if item["kind"] == "stale_step"]
        self.assertEqual(2, len(stale))
        self.assertEqual({"stale"}, {item["direction"] for item in stale})
        self.assertIn(
            "no longer rehearsed", " ".join(item["detail"] for item in stale)
        )

    def test_a_declared_command_the_orchestrator_no_longer_invokes_is_stale(self) -> None:
        declaration = copy.deepcopy(self.declaration)
        index = REHEARSAL.declaration_index(declaration)
        index["plan-resolution"]["commands"] = ["python .github/scripts/publish_release.py plan"]
        result = self.check(declaration)
        self.assertEqual("divergent", result["verdict"])
        stale = next(item for item in result["findings"] if item["kind"] == "stale_mechanic")
        self.assertEqual("plan-resolution", stale["mechanic"])
        self.assertEqual("python .github/scripts/publish_release.py plan", stale["command"])
        coverage = {item["mechanic"]: item["coverage"] for item in result["mechanics"]}
        self.assertEqual("stale", coverage["plan-resolution"])
        self.assertIn("unclassified_command", self.kinds(result))

    def test_a_mechanic_of_a_no_longer_rehearsed_job_is_stale(self) -> None:
        declaration = copy.deepcopy(self.declaration)
        index = REHEARSAL.declaration_index(declaration)
        index["plan-resolution"]["job"] = "pypi"
        result = self.check(declaration)
        stale = next(item for item in result["findings"] if item["kind"] == "stale_mechanic")
        self.assertEqual("pypi", stale["job"])
        self.assertIn("no longer rehearsed", stale["detail"])

    def test_a_platform_claim_must_match_the_job_runner(self) -> None:
        declaration = copy.deepcopy(self.declaration)
        index = REHEARSAL.declaration_index(declaration)
        index["deterministic-build"]["orchestrator_platforms"] = ["Linux"]
        result = self.check(declaration)
        finding = next(item for item in result["findings"] if item["kind"] == "platform_claim")
        self.assertEqual(["Linux"], finding["declared"])
        self.assertEqual(["Windows"], finding["observed"])

    def test_an_unclassified_command_fails_closed(self) -> None:
        declaration = copy.deepcopy(self.declaration)
        declaration["trivia_commands"] = [
            item for item in declaration["trivia_commands"] if item != "set"
        ]
        result = self.check(declaration)
        finding = next(
            item for item in result["findings"] if item["kind"] == "unclassified_command"
        )
        self.assertEqual("set", finding["command"])
        self.assertEqual("uncovered", finding["direction"])

    def test_trivia_matches_the_command_name_and_never_a_longer_mechanic(self) -> None:
        declaration = copy.deepcopy(self.declaration)
        declaration["trivia_commands"] = sorted(
            set(declaration["trivia_commands"]) | {"python"}
        )
        index = REHEARSAL.declaration_index(declaration)
        index["deterministic-build"]["commands"] = ["python -m build --wheel"]
        result = self.check(declaration)
        # `python` as trivia silences the uncovered direction, but the declared
        # command must still match a whole observed key, so the stale direction
        # reports the mechanic.
        self.assertIn("stale_mechanic", self.kinds(result))

    def test_an_undeclared_or_unpinned_action_fails_closed(self) -> None:
        text = self.orchestrator().read_text(encoding="utf-8")
        text = text.replace(
            "        uses: actions/checkout@" + "1" * 40 + " # v7.0.1\n",
            "        uses: actions/checkout@v7\n",
        )
        self.orchestrator().write_text(text, encoding="utf-8", newline="\n")
        result = self.check()
        finding = next(item for item in result["findings"] if item["kind"] == "unpinned_action")
        self.assertEqual("resolve", finding["job"])
        self.assertEqual("actions/checkout@v7", finding["command"])

        text = self.orchestrator().read_text(encoding="utf-8")
        text = text.replace(
            "        uses: actions/checkout@v7\n",
            "        uses: example/publish-action@" + "3" * 40 + "\n",
        )
        self.orchestrator().write_text(text, encoding="utf-8", newline="\n")
        result = self.check()
        finding = next(
            item for item in result["findings"] if item["kind"] == "unclassified_action"
        )
        self.assertEqual("example/publish-action", finding["command"])

    def test_a_lane_missing_a_required_platform_fails_closed(self) -> None:
        declaration = copy.deepcopy(self.declaration)
        declaration["rehearsal_lane"] = ".github/workflows/lane-linux-only.yml"
        result = self.check(declaration)
        self.assertEqual("divergent", result["verdict"])
        finding = next(item for item in result["findings"] if item["kind"] == "missing_platform")
        self.assertIn("Windows", finding["detail"])
        self.assertEqual(["Windows"], result["lane"]["missing_platforms"])

    def test_an_absent_lane_fails_closed(self) -> None:
        declaration = copy.deepcopy(self.declaration)
        declaration["rehearsal_lane"] = ".github/workflows/absent.yml"
        result = self.check(declaration)
        self.assertIn("missing_lane", self.kinds(result))
        self.assertFalse(result["lane"]["permissions_read_only"])

    def test_a_lane_claiming_authority_fails_closed(self) -> None:
        lane = self.repository / ".github" / "workflows" / "lane.yml"
        cases = {
            "lane_permissions": ("      contents: read\n", "      contents: write\n"),
            "lane_environment": (
                "    permissions:\n      contents: read\n    strategy:\n",
                "    permissions:\n      contents: read\n    environment: pypi\n    strategy:\n",
            ),
            "lane_secret": (
                "      - name: Rehearse\n",
                "      - name: Rehearse\n        env:\n          GH_TOKEN: ${{ github.token }}\n",
            ),
            "lane_external_state": (
                "      - name: Rehearse\n",
                "      - name: Deploy\n"
                "        uses: pypa/gh-action-pypi-publish@" + "4" * 40 + "\n"
                "      - name: Rehearse\n",
            ),
        }
        original = lane.read_text(encoding="utf-8")
        for kind, (old, new) in cases.items():
            with self.subTest(kind=kind):
                lane.write_text(original.replace(old, new, 1), encoding="utf-8", newline="\n")
                result = self.check()
                self.assertIn(kind, self.kinds(result))
                self.assertFalse(result["lane"]["permissions_read_only"])
        lane.write_text(original, encoding="utf-8", newline="\n")

    def test_no_remaining_credential_free_job_is_refused(self) -> None:
        text = self.orchestrator().read_text(encoding="utf-8")
        text = text.replace("      contents: read\n", "      contents: write\n")
        self.orchestrator().write_text(text, encoding="utf-8", newline="\n")
        with self.assertRaisesRegex(REHEARSAL.RehearsalError, "no credential-free"):
            self.check()

    def test_one_finding_is_reported_per_condition(self) -> None:
        text = self.orchestrator().read_text(encoding="utf-8")
        text = text.replace(
            "          cmp --silent dist-a/wheel dist-b/wheel\n",
            "          jq -n true\n          jq -n true\n",
        )
        self.orchestrator().write_text(text, encoding="utf-8", newline="\n")
        result = self.check()
        unclassified = [
            item
            for item in result["findings"]
            if item["kind"] == "unclassified_command" and item["command"] == "jq"
        ]
        self.assertEqual(1, len(unclassified))

    def test_the_result_is_serializable_and_states_its_absence_of_authority(self) -> None:
        result = self.check()
        self.assertEqual(REHEARSAL.DIVERGENCE_SCHEMA, result["schema"])
        self.assertEqual(REHEARSAL.AUTHORITY, result["authority"])
        json.dumps(result)
        summary = REHEARSAL.human_divergence_summary(result)
        self.assertIn("EXACT", summary)
        self.assertIn("No uncovered or stale mechanic.", summary)


class RepositoryDivergenceTests(unittest.TestCase):
    """The real orchestrator, declaration, and lane, with no third-party parser."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.declaration = REHEARSAL.load_declaration(DECLARATION_PATH)
        cls.result = REHEARSAL.check_divergence(REPOSITORY_ROOT, cls.declaration)

    def test_the_orchestrator_and_the_rehearsed_set_do_not_diverge(self) -> None:
        self.assertEqual("exact", self.result["verdict"], msg=self.result["findings"])
        self.assertEqual(["qualify", "resolve"], self.result["rehearsed_jobs"])
        self.assertEqual(["Linux", "Windows"], self.result["orchestrator_platforms"])

    def test_every_excluded_job_reports_the_attribute_that_excluded_it(self) -> None:
        excluded = {item["job"]: item["attributes"] for item in self.result["excluded_jobs"]}
        self.assertEqual(
            {"github_release", "observe", "pages_build", "pages_deploy", "pypi"}, set(excluded)
        )
        for job, attributes in excluded.items():
            with self.subTest(job=job):
                self.assertTrue(attributes)
        self.assertIn("depends on the excluded job github_release", excluded["observe"])

    def test_the_lane_covers_both_required_platforms_read_only(self) -> None:
        self.assertEqual(["Linux", "Windows"], self.result["lane"]["platforms"])
        self.assertTrue(self.result["lane"]["permissions_read_only"])
        self.assertEqual([], self.result["lane"]["missing_platforms"])

    def test_every_orchestrator_mechanic_is_covered(self) -> None:
        coverage = {item["mechanic"]: item["coverage"] for item in self.result["mechanics"]}
        self.assertEqual({"covered", "rehearsal-only"}, set(coverage.values()))
        self.assertEqual("rehearsal-only", coverage["teardown"])
        orchestrator = [name for name, state in coverage.items() if state == "covered"]
        self.assertEqual(21, len(orchestrator))

    def test_the_release_orchestrator_is_byte_unchanged(self) -> None:
        self.assertEqual(ORCHESTRATOR_LF_SHA256, lf_digest(ORCHESTRATOR_PATH))
        workflow = REHEARSAL.read_workflow(ORCHESTRATOR_PATH)
        self.assertEqual(["release_record"], list(workflow["on"]["workflow_dispatch"]["inputs"]))
        self.assertEqual({}, workflow["permissions"])
        self.assertEqual(
            ["github_release", "observe", "pages_build", "pages_deploy", "pypi", "qualify", "resolve"],
            sorted(workflow["jobs"]),
        )


class RehearsalAuthorityTests(unittest.TestCase):
    def test_the_lane_declares_no_credential_environment_or_write_permission(self) -> None:
        lane = REHEARSAL.read_workflow(LANE_PATH)
        self.assertEqual({"contents": "read"}, lane["permissions"])
        self.assertNotIn("secrets.", LANE_PATH.read_text(encoding="utf-8"))
        for name, job in lane["jobs"].items():
            with self.subTest(job=name):
                self.assertEqual({"contents": "read"}, job["permissions"])
                self.assertIsNone(job.get("environment"))
                attributes: list[str] = []
                REHEARSAL._secret_attributes(job, f"job {name}", attributes)
                self.assertEqual([], attributes)

    def test_the_lane_runs_on_pull_requests_main_and_dispatch_only(self) -> None:
        lane = REHEARSAL.read_workflow(LANE_PATH)
        self.assertEqual(
            ["pull_request", "push", "workflow_dispatch"], sorted(lane["on"])
        )
        self.assertEqual(["main"], lane["on"]["push"]["branches"])
        inputs = lane["on"]["workflow_dispatch"]["inputs"]
        self.assertEqual(["release_record"], list(inputs))
        self.assertFalse(inputs["release_record"]["required"])

    def test_the_program_creates_no_external_state(self) -> None:
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        for forbidden in (
            "git push",
            "git tag",
            "gh release",
            "gh api",
            "twine",
            "upload.pypi.org",
            "actions/deploy-pages",
        ):
            with self.subTest(token=forbidden):
                self.assertNotIn(forbidden, source)

    def test_the_result_and_divergence_schemas_disclaim_authority(self) -> None:
        self.assertEqual(
            "derived operational evidence; no formal lifecycle transition", REHEARSAL.AUTHORITY
        )
        for schema in (REHEARSAL.RESULT_SCHEMA, REHEARSAL.DIVERGENCE_SCHEMA):
            self.assertTrue(schema.startswith("se-harness-publication-rehearsal-"))

    def test_candidate_mode_can_never_name_a_release_record(self) -> None:
        marker = REHEARSAL.CANDIDATE_PLAN_MARKERS["release_record"]
        self.assertIsNone(REHEARSAL.RELEASE_RECORD_PATTERN.search(marker))
        self.assertNotIn("RLS-", marker.replace("RECORD", ""))


class PortableBoundaryTests(unittest.TestCase):
    def test_no_packaged_module_or_template_mentions_the_rehearsal(self) -> None:
        roots = (
            REPOSITORY_ROOT / "se_harness",
            REPOSITORY_ROOT / "templates",
            REPOSITORY_ROOT / "scripts",
        )
        for root in roots:
            for path in sorted(root.rglob("*.py")) + sorted(root.rglob("*.yml")):
                if "__pycache__" in path.parts:
                    continue
                with self.subTest(path=path.relative_to(REPOSITORY_ROOT).as_posix()):
                    self.assertNotIn("rehearse_publication", path.read_text(encoding="utf-8"))

    def test_the_rehearsal_lives_only_in_repository_owned_locations(self) -> None:
        for path in (SCRIPT_PATH, DECLARATION_PATH, LANE_PATH):
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file())
                relative = path.relative_to(REPOSITORY_ROOT).as_posix()
                self.assertTrue(relative.startswith(".github/"))


class CommandLineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = make_temporary_directory(self)
        workflows = self.repository / ".github" / "workflows"
        workflows.mkdir(parents=True)
        for name in ("orchestrator.yml", "lane.yml"):
            shutil.copy(FIXTURES / name, workflows / name)
        self.declaration_path = self.repository / "mechanics.json"
        shutil.copy(FIXTURES / "mechanics.json", self.declaration_path)

    def run_main(self, *arguments: str) -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return REHEARSAL.main(list(arguments))

    def test_an_exact_check_writes_its_result_and_exits_zero(self) -> None:
        output = self.repository / "out" / "divergence.json"
        summary = self.repository / "summary.md"
        code = self.run_main(
            "check-divergence",
            "--repository",
            str(self.repository),
            "--declaration",
            str(self.declaration_path),
            "--output",
            str(output),
            "--summary",
            str(summary),
        )
        self.assertEqual(0, code)
        result = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual("exact", result["verdict"])
        self.assertIn("EXACT", summary.read_text(encoding="utf-8"))

    def test_a_divergent_check_exits_one(self) -> None:
        declaration = json.loads(self.declaration_path.read_text(encoding="utf-8"))
        declaration["steps"][0]["run_sha256"] = "0" * 64
        self.declaration_path.write_text(json.dumps(declaration), encoding="utf-8")
        output = self.repository / "divergence.json"
        code = self.run_main(
            "check-divergence",
            "--repository",
            str(self.repository),
            "--declaration",
            str(self.declaration_path),
            "--output",
            str(output),
        )
        self.assertEqual(1, code)
        self.assertEqual(
            "divergent", json.loads(output.read_text(encoding="utf-8"))["verdict"]
        )

    def test_a_refusal_exits_one_without_writing_a_result(self) -> None:
        output = self.repository / "divergence.json"
        code = self.run_main(
            "check-divergence",
            "--repository",
            str(self.repository),
            "--declaration",
            str(self.repository / "absent.json"),
            "--output",
            str(output),
        )
        self.assertEqual(1, code)
        self.assertFalse(output.exists())

    def test_the_declaration_defaults_to_the_repository_copy(self) -> None:
        self.assertEqual(
            DECLARATION_PATH, REHEARSAL._declaration_path(REPOSITORY_ROOT, None)
        )
        override = Path("elsewhere.json")
        self.assertEqual(override, REHEARSAL._declaration_path(REPOSITORY_ROOT, override))

    def test_the_rehearse_defaults_are_candidate_mode_and_the_tracking_ref(self) -> None:
        parsed = REHEARSAL.build_parser().parse_args(["rehearse", "--root", "root"])
        self.assertEqual("candidate", parsed.mode)
        self.assertEqual("refs/remotes/origin/main", parsed.default_ref)
        self.assertEqual(REHEARSAL.DEFAULT_REF, parsed.default_ref)
        self.assertIsNone(parsed.release_record)
        self.assertFalse(parsed.keep_root)

    def test_the_two_modes_refuse_each_other_s_arguments(self) -> None:
        for arguments in (
            ["rehearse", "--root", "r", "--mode", "release-record"],
            ["rehearse", "--root", "r", "--mode", "candidate", "--release-record", "RLS-SEH-012"],
        ):
            with self.subTest(arguments=arguments[3:]):
                code = self.run_main(
                    *arguments,
                    "--repository",
                    str(self.repository),
                    "--declaration",
                    str(self.declaration_path),
                )
                self.assertEqual(1, code)

    def test_a_root_is_mandatory_for_a_rehearsal(self) -> None:
        with self.assertRaises(SystemExit):
            REHEARSAL.build_parser().parse_args(["rehearse"])


class HumanSummaryTests(unittest.TestCase):
    def test_a_failed_mechanic_and_an_unclean_checkout_are_stated(self) -> None:
        result = {
            "state": "failed",
            "platform": "Windows",
            "mode": "candidate",
            "candidate_commit": "c" * 40,
            "verification_plan_source": None,
            "authority": REHEARSAL.AUTHORITY,
            "preconditions": {
                "clean_worktree": False,
                "uncommitted_entries": 3,
                "uncommitted_sample": ["?? a", "?? b", " M c"],
            },
            "mechanics": [
                {"mechanic": "teardown", "outcome": "executed", "detail": "removed", "reason": None},
                {
                    "mechanic": "candidate-unit-suite",
                    "outcome": "failed",
                    "detail": "Windows",
                    "reason": "4 failing tests",
                },
            ],
        }
        summary = REHEARSAL.human_rehearsal_summary(result)
        self.assertIn("FAILED", summary)
        self.assertIn("Verification plan: none", summary)
        self.assertIn("Inherited checkout: not clean, 3 uncommitted entries", summary)
        self.assertIn("4 failing tests", summary)

    def test_a_converting_checkout_is_stated(self) -> None:
        result = {
            "state": "failed",
            "platform": "Windows",
            "mode": "candidate",
            "candidate_commit": "c" * 40,
            "verification_plan_source": None,
            "authority": REHEARSAL.AUTHORITY,
            "preconditions": {
                "clean_worktree": True,
                "uncommitted_entries": 0,
                "uncommitted_sample": [],
                "line_ending_conversion": "true",
            },
            "mechanics": [],
        }
        summary = REHEARSAL.human_rehearsal_summary(result)
        self.assertIn("core.autocrlf=true", summary)
        self.assertIn("converts line endings", summary)

    def test_an_excluded_mechanic_states_its_reason(self) -> None:
        result = {
            "state": "rehearsed",
            "platform": "Linux",
            "mode": "candidate",
            "candidate_commit": "c" * 40,
            "verification_plan_source": "candidate-manifest",
            "authority": REHEARSAL.AUTHORITY,
            "preconditions": {
                "clean_worktree": True,
                "uncommitted_entries": 0,
                "uncommitted_sample": [],
                "line_ending_conversion": "unset",
            },
            "mechanics": [
                {
                    "mechanic": "predecessor-view-qualification",
                    "outcome": "excluded",
                    "detail": "no committed record binds the resolved evaluator as its predecessor",
                    "reason": "the resolved evaluator 0.6.0 is not the predecessor evaluator 0.5.0",
                }
            ],
        }
        summary = REHEARSAL.human_rehearsal_summary(result)
        self.assertIn("excluded predecessor-view-qualification", summary)
        self.assertIn("predecessor evaluator 0.5.0", summary)

    def test_a_clean_checkout_adds_no_precondition_line(self) -> None:
        result = {
            "state": "rehearsed",
            "platform": "Linux",
            "mode": "release-record",
            "candidate_commit": "c" * 40,
            "verification_plan_source": "release-record",
            "authority": REHEARSAL.AUTHORITY,
            "preconditions": {
                "clean_worktree": True,
                "uncommitted_entries": 0,
                "uncommitted_sample": [],
            },
            "mechanics": [],
        }
        self.assertNotIn("Inherited checkout", REHEARSAL.human_rehearsal_summary(result))


if __name__ == "__main__":  # pragma: no cover - direct invocation
    unittest.main()
