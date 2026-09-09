"""REQ-DST-072 to REQ-DST-075 / SPEC-DST-027 (WO-DST-026): the managed template's
failure surface, header and pins, the gitignore markers, the environment inventory.

DST-MWF-012 pins rules 001 to 008 by parsing the standard template and by driving
the installer; DST-MWF-011 pins the inventory of environment variables the package
reads against the specifications that name them.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from se_harness.installer import (
    ATTRIBUTE_BEGIN_MARKER,
    ATTRIBUTE_END_MARKER,
    BEGIN_MARKER,
    END_MARKER,
    _block,
    plan_install,
    tracked_content,
)
from se_harness.integrity import canonical_sha256
from tests.cli_support import invoke
from tests.git_support import git_available
from tests.mutation_guard_support import patch_mutation_authority

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPOSITORY_ROOT / "templates/repository/standard/.github/workflows/engineering-harness.yml"
PACKAGE_ROOT = REPOSITORY_ROOT / "se_harness"
ENGINEERING_ROOT = REPOSITORY_ROOT / "docs/engineering"

#: SPEC-CIP-003 CIP-ONE-006, reused by DST-MWF-005: a full commit digest and the exact tag.
PIN_FORM = re.compile(r"^[\w.-]+/[\w./-]+@[0-9a-f]{40} # v\d+\.\d+\.\d+(?:\.post\d+)?$")

#: DST-MWF-011: the environment names read under se_harness/ today, each named in a
#: specification. SE_HARNESS_REHEARSAL and GITHUB_TOKEN belong to the delegation
#: gate (SPEC-ECP-006); PYTHONPATH is read by the runtime identity (SPEC-ECP-023).
SPECIFIED_ENVIRONMENT_NAMES = frozenset({"SE_HARNESS_REHEARSAL", "GITHUB_TOKEN", "PYTHONPATH"})
ENVIRONMENT_READ = re.compile(r"""os\.(?:environ\.get|getenv)\(\s*["']([A-Z_][A-Z0-9_]*)["']|os\.environ\[\s*["']([A-Z_][A-Z0-9_]*)["']\s*\]""")


def _template_text() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def _header(text: str) -> str:
    """The leading comment block, joined into one line."""

    lines = []
    for line in text.splitlines():
        if not line.startswith("#"):
            break
        lines.append(line[1:].strip())
    return " ".join(lines)


def _step_names(text: str) -> list[str]:
    return re.findall(r"(?m)^      - name: (.+)$", text)


def _uses_lines(text: str) -> list[str]:
    return re.findall(r"(?m)^\s+- uses: (.+)$", text)


def _embedded_reader(text: str, after: str) -> str:
    """The Python heredoc that follows ``after`` in the template, dedented."""

    body = text.split(after, 1)[1].split("<<'PY'\n", 1)[1].split("\n          PY\n", 1)[0]
    return "\n".join(line[10:] if line.startswith("          ") else line for line in body.splitlines()) + "\n"


class ManagedWorkflowTemplateTests(unittest.TestCase):
    """DST-MWF-001 to DST-MWF-005 on the standard template."""

    def setUp(self) -> None:
        self.text = _template_text()

    def test_the_header_names_only_the_steps_the_file_runs(self) -> None:
        # DST-MWF-004: every named step is in the header, the upload is named, and
        # the two steps the file stopped running are not.
        header = _header(self.text).lower()
        steps = _step_names(self.text)
        self.assertEqual(7, len(steps), steps)
        for step in steps:
            with self.subTest(step=step):
                self.assertIn(step.lower(), header)
        self.assertIn("upload", header)
        self.assertIn("harness-dashboard", header)
        for absent in ("doctor", "validate", "dashboard."):
            with self.subTest(absent=absent):
                self.assertNotIn(absent, header)
        self.assertIn("trigger policy: pull requests, and pushes to", header)

    def test_every_action_takes_the_pin_form(self) -> None:
        # DST-MWF-005: three public actions, each a full digest with its exact tag.
        uses = _uses_lines(self.text)
        self.assertEqual(3, len(uses), uses)
        for line in uses:
            with self.subTest(uses=line):
                self.assertRegex(line, PIN_FORM)
        self.assertEqual(
            ["actions/checkout", "actions/setup-python", "actions/upload-artifact"],
            [line.split("@", 1)[0] for line in uses],
        )

    def test_the_check_steps_capture_status_and_stderr(self) -> None:
        # DST-MWF-001: neither check appends `|| true`; each records its status and
        # redirects its stderr to a file the reader receives.
        self.assertNotIn("|| true", self.text)
        for checkpoint, status, stderr in (
            ("scope", "scope_status", "scope.stderr"),
            ("handoff", "handoff_status", "restitution.stderr"),
        ):
            with self.subTest(checkpoint=checkpoint):
                step = self.text.split(f"--checkpoint {checkpoint}", 1)[1].split("<<'PY'", 1)[0]
                self.assertIn(f'2> "$RUNNER_TEMP/{stderr}" || {status}=$?', step)
                self.assertIn(f'"$RUNNER_TEMP/{stderr}" "${status}" <<', step + "<<")
                self.assertIn(f"{status}=0", self.text.split(f"--checkpoint {checkpoint}", 1)[0][-1200:])

    def _run_reader(self, reader: str, *arguments: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary:
            script = Path(temporary) / "reader.py"
            script.write_text(reader, encoding="utf-8")
            return subprocess.run(
                [sys.executable, "-I", str(script), *arguments],
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=temporary,
                check=False,
            )

    def test_the_readers_fail_with_the_captured_status_and_text_on_an_empty_result(self) -> None:
        # DST-MWF-002: an empty result file is the shape of a refusal; the reader
        # prints the captured stderr and exits with the captured status, never with
        # a decoder traceback.
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            empty = root / "empty.json"
            empty.write_bytes(b"")
            refusal = root / "refusal.stderr"
            refusal.write_text("MG005: runtime identity is not the released evaluator\n", encoding="utf-8")
            not_json = root / "not.json"
            not_json.write_text("usage: harnessctl check [-h]\n", encoding="utf-8")
            cases = (
                ("scope", _embedded_reader(self.text, "--checkpoint scope"), (str(refusal), "2"), 2),
                ("handoff", _embedded_reader(self.text, "--checkpoint handoff"), ("", str(refusal), "3"), 3),
            )
            for name, reader, tail, status in cases:
                with self.subTest(reader=name, result="empty"):
                    completed = self._run_reader(reader, str(empty), *tail)
                    self.assertEqual(status, completed.returncode, completed.stderr)
                    self.assertIn("MG005: runtime identity is not the released evaluator", completed.stderr)
                    self.assertIn(f"wrote no result (exit status {status})", completed.stderr)
                    self.assertNotIn("Traceback", completed.stderr)
                    self.assertEqual("", completed.stdout)
                with self.subTest(reader=name, result="not-json"):
                    completed = self._run_reader(reader, str(not_json), *tail)
                    self.assertEqual(status, completed.returncode, completed.stderr)
                    self.assertNotIn("Traceback", completed.stderr)
                with self.subTest(reader=name, result="empty-with-status-zero"):
                    zero_tail = tail[:-1] + ("0",)
                    completed = self._run_reader(reader, str(empty), *zero_tail)
                    self.assertEqual(1, completed.returncode, "an empty result with status 0 must still fail")
                    self.assertNotIn("Traceback", completed.stderr)

    def test_the_readers_judge_a_parsed_result_as_before(self) -> None:
        # DST-MWF-003: a parsed result is evaluated on QGP-G4I-PATHS, the outcome,
        # the blockers and the declared digest, with the same messages as before.
        scope_reader = _embedded_reader(self.text, "--checkpoint scope")
        handoff_reader = _embedded_reader(self.text, "--checkpoint handoff")
        completed_result = {
            "operation": {"outcome": "completed"},
            "compliance": {"gates": [{"predicates": [{"id": "QGP-G4I-PATHS", "status": "pass"}]}]},
            "restitution": {"blocked_by": [], "current_lifecycle_state": ["WO-X is in_progress."]},
            "result_sha256": "a" * 64,
        }
        blocked_result = {
            "operation": {"outcome": "blocked"},
            "compliance": {"gates": [{"predicates": [{"id": "QGP-G4I-PATHS", "status": "pass"}]}]},
            "restitution": {"blocked_by": ["QGP-G4I-EVIDENCE: No readable evidence"], "current_lifecycle_state": []},
        }
        violation_result = {
            "operation": {"outcome": "blocked"},
            "compliance": {"gates": [{"predicates": [{"id": "QGP-G4I-PATHS", "status": "fail", "message": "1 path outside scope"}]}]},
            "restitution": {"blocked_by": ["QGP-G4I-PATHS: WEX201"], "current_lifecycle_state": []},
        }
        implemented_result = json.loads(json.dumps(completed_result))
        implemented_result["restitution"]["current_lifecycle_state"] = ["WO-X is implemented."]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            quiet = root / "quiet.stderr"
            quiet.write_bytes(b"")
            results = {}
            for name, payload in (
                ("completed", completed_result),
                ("blocked", blocked_result),
                ("violation", violation_result),
                ("implemented", implemented_result),
            ):
                results[name] = root / f"{name}.json"
                results[name].write_text(json.dumps(payload), encoding="utf-8")

            run = self._run_reader(scope_reader, str(results["completed"]), str(quiet), "0")
            self.assertEqual((0, "yes\n"), (run.returncode, run.stdout), run.stderr)
            run = self._run_reader(scope_reader, str(results["implemented"]), str(quiet), "0")
            self.assertEqual((0, "no\n"), (run.returncode, run.stdout), run.stderr)
            run = self._run_reader(scope_reader, str(results["blocked"]), str(quiet), "1")
            self.assertEqual(1, run.returncode)
            self.assertIn("blocked: QGP-G4I-EVIDENCE: No readable evidence", run.stderr)
            self.assertIn("The scope check did not complete (outcome blocked).", run.stderr)
            run = self._run_reader(scope_reader, str(results["violation"]), str(quiet), "1")
            self.assertEqual(1, run.returncode)
            self.assertIn("scope: 1 path outside scope", run.stderr)
            self.assertIn("The pull request's diff leaves the work order's declared scope.", run.stderr)

            run = self._run_reader(handoff_reader, str(results["completed"]), "", str(quiet), "0")
            self.assertEqual(0, run.returncode, run.stderr)
            self.assertIn("inside the declared scope; no restitution digest was declared.", run.stdout)
            run = self._run_reader(handoff_reader, str(results["completed"]), "a" * 64, str(quiet), "0")
            self.assertEqual(0, run.returncode, run.stderr)
            self.assertIn("the declared restitution digest matches.", run.stdout)
            run = self._run_reader(handoff_reader, str(results["completed"]), "b" * 64, str(quiet), "0")
            self.assertEqual(1, run.returncode)
            self.assertIn("does not match the recomputed result_sha256", run.stderr)
            run = self._run_reader(handoff_reader, str(results["blocked"]), "", str(quiet), "1")
            self.assertEqual(1, run.returncode)
            self.assertIn("blocked: QGP-G4I-EVIDENCE: No readable evidence", run.stderr)
            self.assertIn("The handoff check did not complete (outcome blocked).", run.stderr)
            for name in results:
                with self.subTest(result=name):
                    self.assertNotIn("Traceback", self._run_reader(scope_reader, str(results[name]), str(quiet), "1").stderr)


class GitignoreMarkerTests(unittest.TestCase):
    """DST-MWF-006 to DST-MWF-008: the installer's fragment writer and the upgrade."""

    def setUp(self) -> None:
        patch_mutation_authority(self)
        self._temporary = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name)

    def test_block_chooses_the_marker_pair_by_target(self) -> None:
        # DST-MWF-006: the Git dot-files take hash markers, the Markdown fragments keep HTML.
        for target in (".gitignore", ".gitattributes"):
            with self.subTest(target=target):
                block = _block(b"rule\n", Path(target)).decode("utf-8")
                self.assertEqual(f"{ATTRIBUTE_BEGIN_MARKER}\nrule\n{ATTRIBUTE_END_MARKER}\n", block)
        for target in ("AGENTS.md", "CLAUDE.md"):
            with self.subTest(target=target):
                block = _block(b"rule\n", Path(target)).decode("utf-8")
                self.assertEqual(f"{BEGIN_MARKER}\nrule\n{END_MARKER}\n", block)

    def test_init_writes_the_ignore_block_between_markers_git_reads_as_comments(self) -> None:
        target = self.root / "fresh"
        code, _, error = invoke("init", str(target), "--project-name", "Markers")
        self.assertEqual(0, code, error)
        ignore = (target / ".gitignore").read_text(encoding="utf-8")
        self.assertTrue(ignore.startswith(f"{ATTRIBUTE_BEGIN_MARKER}\n"), ignore)
        self.assertTrue(ignore.endswith(f"\n{ATTRIBUTE_END_MARKER}\n"), ignore)
        self.assertNotIn("<!--", ignore)
        self.assertIn("/target/harness-dashboard/\n", ignore)
        if not git_available():
            self.skipTest("git is not available")
        subprocess.run(["git", "init", "-q", str(target)], check=True, capture_output=True)
        for marker in (ATTRIBUTE_BEGIN_MARKER, ATTRIBUTE_END_MARKER, BEGIN_MARKER, END_MARKER):
            with self.subTest(marker=marker):
                probe = subprocess.run(["git", "check-ignore", "-q", marker], cwd=target, capture_output=True, check=False)
                self.assertEqual(1, probe.returncode, "no ignore rule may match the marker text")
        probe = subprocess.run(["git", "check-ignore", "-q", "target/harness-dashboard/index.html"], cwd=target, capture_output=True, check=False)
        self.assertEqual(0, probe.returncode, "the managed rule must still ignore the Explorer output")

    def _fixture_with_html_markers(self, name: str, *, edit_inside: bool = False) -> tuple[Path, bytes]:
        """A target as released 0.16.0 left it: owner lines, then the block between HTML comments."""

        target = self.root / name
        self.assertEqual(0, invoke("init", str(target), "--project-name", "Older")[0])
        ignore_path = target / ".gitignore"
        current = ignore_path.read_bytes()
        block = tracked_content("fragment", current)
        assert block is not None
        inner = block[len(ATTRIBUTE_BEGIN_MARKER.encode()) + 1 : -len(ATTRIBUTE_END_MARKER.encode()) - 1]
        owner_head = b"/build/\n/.venv/\n\n"
        owner_tail = b"\n# owner rule kept below the block\n*.tmp\n"
        older = owner_head + BEGIN_MARKER.encode() + b"\n" + inner + END_MARKER.encode() + b"\n" + owner_tail
        ignore_path.write_bytes(older)
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        older_block = tracked_content("fragment", older)
        assert older_block is not None
        lock["files"][".gitignore"] = {"mode": "fragment", "sha256": canonical_sha256(older_block)}
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if edit_inside:
            edited = older.replace(b"/target/harness-dashboard/\n", b"/target/harness-dashboard/edited\n")
            self.assertNotEqual(older, edited)
            ignore_path.write_bytes(edited)
            return target, edited
        return target, older

    def test_upgrade_rewrites_an_html_marked_ignore_block_and_keeps_every_owner_byte(self) -> None:
        # DST-MWF-007, DST-MWF-008: the older block is planned as a fragment update by
        # the existing rule, the rewrite replaces only the block, and doctor passes.
        target, older = self._fixture_with_html_markers("older")
        changes, _ = plan_install(target, project_name=None, mode="upgrade")
        ignore_change = next(change for change in changes if change.path == ".gitignore")
        self.assertEqual(("update", "fragment"), (ignore_change.action, ignore_change.mode))
        code, output, error = invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertIn("update     .gitignore", output)
        after = (target / ".gitignore").read_bytes()
        self.assertNotIn(b"<!--", after)
        self.assertIn(ATTRIBUTE_BEGIN_MARKER.encode() + b"\n", after)
        self.assertIn(ATTRIBUTE_END_MARKER.encode() + b"\n", after)
        older_block = tracked_content("fragment", older)
        new_block = tracked_content("fragment", after)
        assert older_block is not None and new_block is not None
        self.assertEqual(older.replace(older_block, b""), after.replace(new_block, b""), "owner bytes moved")
        self.assertTrue(after.startswith(b"/build/\n/.venv/\n\n"))
        self.assertTrue(after.endswith(b"\n# owner rule kept below the block\n*.tmp\n"))
        code, _, error = invoke("doctor", str(target))
        self.assertEqual(0, code, error)
        self.assertEqual(0, invoke("upgrade", str(target), "--apply")[0], "a second apply is a no-op")

    def test_upgrade_refuses_an_ignore_block_edited_inside(self) -> None:
        target, edited = self._fixture_with_html_markers("edited", edit_inside=True)
        changes, _ = plan_install(target, project_name=None, mode="upgrade")
        ignore_change = next(change for change in changes if change.path == ".gitignore")
        self.assertEqual("customized", ignore_change.action)
        code, output, _ = invoke("upgrade", str(target), "--apply")
        self.assertEqual(1, code)
        self.assertIn("no files were written", output)
        self.assertEqual(edited, (target / ".gitignore").read_bytes())


class EnvironmentInventoryTests(unittest.TestCase):
    """DST-MWF-011: every environment variable read under se_harness/ is specified."""

    def test_every_environment_variable_read_under_the_package_is_specified(self) -> None:
        found: dict[str, set[str]] = {}
        for path in sorted(PACKAGE_ROOT.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            for match in ENVIRONMENT_READ.finditer(path.read_text(encoding="utf-8")):
                name = match.group(1) or match.group(2)
                found.setdefault(name, set()).add(path.relative_to(REPOSITORY_ROOT).as_posix())
        self.assertEqual(SPECIFIED_ENVIRONMENT_NAMES, set(found), found)
        specifications = sorted(ENGINEERING_ROOT.glob("*/specifications/SPEC-*.md"))
        self.assertGreater(len(specifications), 20)
        for name in sorted(found):
            with self.subTest(variable=name, read_in=sorted(found[name])):
                naming = [path.name for path in specifications if name in path.read_text(encoding="utf-8")]
                self.assertTrue(naming, f"{name} is read but named in no specification")

    def test_the_rehearsal_marker_is_named_where_its_exemption_lives(self) -> None:
        # DST-MWF-009, DST-MWF-010: the amendment record on SPEC-ECP-006 and the
        # delegation note both name the variable beside the local-file source.
        specification = (ENGINEERING_ROOT / "execution-control-plane/specifications/SPEC-ECP-006.md").read_text(encoding="utf-8")
        self.assertIn("SE_HARNESS_REHEARSAL", specification)
        self.assertIn("## Amendment record", specification)
        amendment = specification.split("**`SE_HARNESS_REHEARSAL`", 1)[1]
        self.assertIn("ECP-DLG-004", amendment)
        self.assertIn("gate_source.load_configuration", amendment)
        note = (REPOSITORY_ROOT / "docs/notes/delegation-class.md").read_text(encoding="utf-8")
        local_file = note.split("`local-file` exists for tests and rehearsals", 1)[1][:400]
        self.assertIn("SE_HARNESS_REHEARSAL=1", local_file)


if __name__ == "__main__":
    unittest.main()
