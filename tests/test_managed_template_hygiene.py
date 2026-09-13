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
#: specification. PYTHONPATH is read by runtime identity; local delegation
#: no longer reads a rehearsal flag or GitHub token (WO-KIS-002).
SPECIFIED_ENVIRONMENT_NAMES = frozenset({"PYTHONPATH"})
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




class ManagedWorkflowTemplateTests(unittest.TestCase):
    """DST-MWF-001 to DST-MWF-005 on the standard template."""

    def setUp(self) -> None:
        self.text = _template_text()

    def test_the_header_names_only_the_steps_the_file_runs(self) -> None:
        # DST-MWF-004: every named step is in the header, the upload is named, and
        # the two steps the file stopped running are not.
        header = _header(self.text).lower()
        steps = _step_names(self.text)
        self.assertEqual(5, len(steps), steps)
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





    def test_pr_check_propagates_its_exit_status_directly(self):
        step = self.text.split("      - name: Check the selected work orders", 1)[1].split("      - name:",1)[0]
        self.assertIn("-I -m se_harness check-pr .",step)
        self.assertNotIn("||",step)
        self.assertNotIn("json.load",step)


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
