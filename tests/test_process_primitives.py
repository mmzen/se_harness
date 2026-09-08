"""WO-ECP-031 (SPEC-ECP-023 ECP-PRM-001 to ECP-PRM-005): the one launcher and the one parser.

Boundary cases the copies disagreed on: a missing `git`, a timeout, output over
the cap, each raised as the caller's class; a BOM, CRLF and lone-CR documents,
and a `+++` inside a body, each parsed like the LF form.
"""

from __future__ import annotations

import ast
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness import _process, front_matter
from se_harness.installer import HarnessError

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class CallerError(RuntimeError):
    pass


class LauncherTests(unittest.TestCase):
    def test_a_missing_git_is_the_callers_error_and_names_the_executable(self) -> None:
        with mock.patch("se_harness._process.shutil.which", return_value=None):
            with self.assertRaises(CallerError) as caught:
                _process.run_git(Path("."), "status", error=CallerError)
        self.assertIn("git executable is unavailable", str(caught.exception))

    def test_a_start_failure_and_a_timeout_are_the_callers_error(self) -> None:
        for failure in (FileNotFoundError("nope"), subprocess.TimeoutExpired(cmd="x", timeout=1)):
            with self.subTest(failure=type(failure).__name__):
                with mock.patch("se_harness._process.subprocess.run", side_effect=failure):
                    with self.assertRaises(CallerError) as caught:
                        _process.run(["x", "--flag"], timeout=1, error=CallerError)
                self.assertIn("x", str(caught.exception))
        # ECP-PRM-002: an error factory that builds a coded class keeps its shape.
        with mock.patch("se_harness._process.subprocess.run", side_effect=OSError("boom")):
            with self.assertRaises(HarnessError) as coded:
                _process.run(["y"], error=lambda message: HarnessError(f"WEX-ZZZ-001: {message}"))
        self.assertTrue(str(coded.exception).startswith("WEX-ZZZ-001: y could not run"))

    def test_output_over_the_cap_is_refused_and_a_non_zero_exit_is_returned(self) -> None:
        big = subprocess.CompletedProcess(args=["x"], returncode=0, stdout=b"a" * 11, stderr=b"")
        with mock.patch("se_harness._process.subprocess.run", return_value=big):
            with self.assertRaises(CallerError) as caught:
                _process.run(["x"], output_cap=10, error=CallerError)
        self.assertIn("output exceeds 10 bytes", str(caught.exception))
        failed = subprocess.CompletedProcess(args=["x"], returncode=3, stdout=b"", stderr=b"bad")
        with mock.patch("se_harness._process.subprocess.run", return_value=failed):
            completed = _process.run(["x"], error=CallerError)
        self.assertEqual(3, completed.returncode)

    def test_the_launch_closes_stdin_captures_both_streams_and_passes_the_timeout(self) -> None:
        completed = subprocess.CompletedProcess(args=["x"], returncode=0, stdout=b"", stderr=b"")
        with mock.patch("se_harness._process.subprocess.run", return_value=completed) as run:
            _process.run(["x"], timeout=7)
        kwargs = run.call_args.kwargs
        self.assertEqual(subprocess.DEVNULL, kwargs["stdin"])
        self.assertTrue(kwargs["capture_output"])
        self.assertEqual(7, kwargs["timeout"])
        self.assertFalse(kwargs["shell"])
        with mock.patch("se_harness._process.subprocess.run", return_value=completed) as run:
            _process.run(["x"], stdin=b"data")
        self.assertIsNone(run.call_args.kwargs["stdin"])
        self.assertEqual(b"data", run.call_args.kwargs["input"])

    def test_a_real_launch_decodes_utf8_regardless_of_the_locale(self) -> None:
        completed = _process.run([sys.executable, "-c", "import sys; sys.stdout.buffer.write('é\\n'.encode('utf-8'))"], timeout=60)
        self.assertEqual(0, completed.returncode)
        self.assertEqual("é", _process.text(completed.stdout).strip())
        self.assertEqual("", _process.text(None))
        self.assertEqual("already text", _process.text("already text"))

    def test_no_module_of_the_package_or_the_tools_launches_git_directly(self) -> None:
        # ECP-PRM-003: every Git launch of the package goes through run_git. repository_tools keeps its
        # own launchers behind the import barrier of ARCH-REB-013 / SPEC-REB-015 (DEC-ECP-001), and the
        # engine keeps its copies until wave 3 (#378).
        offenders: list[str] = []
        for path in sorted((REPOSITORY_ROOT / "se_harness").glob("*.py")):
            relative = path.relative_to(REPOSITORY_ROOT).as_posix()
            if relative == "se_harness/_process.py":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
                    continue
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" and node.func.attr in {"run", "Popen", "check_output", "check_call"}:
                    offenders.append(f"{relative}:{node.lineno}")
        self.assertEqual([], offenders)


class FrontMatterTests(unittest.TestCase):
    LF = b'+++\nid = "WO-X-001"\ntype = "work_order"\n+++\n\n# Title\n\nBody with +++ inside a sentence.\n\n+++\nnot front matter\n'

    def variants(self) -> dict[str, bytes]:
        return {
            "lf": self.LF,
            "crlf": self.LF.replace(b"\n", b"\r\n"),
            "cr": self.LF.replace(b"\n", b"\r"),
            "bom": b"\xef\xbb\xbf" + self.LF,
            "bom-crlf": b"\xef\xbb\xbf" + self.LF.replace(b"\n", b"\r\n"),
        }

    def test_every_line_ending_form_and_the_bom_parse_like_lf(self) -> None:
        expected = front_matter.parse(self.LF)
        self.assertEqual({"id": "WO-X-001", "type": "work_order"}, expected)
        for name, data in self.variants().items():
            with self.subTest(form=name):
                self.assertEqual(expected, front_matter.parse(data))
                lines, terminated = front_matter.front_matter_lines(data)
                self.assertEqual(['id = "WO-X-001"', 'type = "work_order"'], lines)
                self.assertTrue(terminated)

    def test_delimiters_are_line_anchored(self) -> None:
        # A +++ inside a body line is not a delimiter; an unanchored split would have ended the front matter there.
        inline = b'+++\nid = "X"\ntitle = "a +++ b"\n+++\nbody\n'
        self.assertEqual({"id": "X", "title": "a +++ b"}, front_matter.parse(inline))
        self.assertIsNone(front_matter.front_matter_lines(b"# no front matter\n+++\n"))
        self.assertIsNone(front_matter.front_matter_lines(b" +++\nid = 1\n+++\n"))

    def test_missing_unterminated_and_invalid_front_matter_are_named(self) -> None:
        with self.assertRaisesRegex(front_matter.FrontMatterError, "no TOML front matter"):
            front_matter.parse(b"# heading\n")
        with self.assertRaisesRegex(front_matter.FrontMatterError, "unterminated"):
            front_matter.parse(b'+++\nid = "X"\n')
        with self.assertRaisesRegex(front_matter.FrontMatterError, "not valid TOML"):
            front_matter.parse(b"+++\nid = \n+++\n")
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "missing.md"
            self.assertIsNone(front_matter.read_or_none(path))
            with self.assertRaisesRegex(front_matter.FrontMatterError, "cannot read"):
                front_matter.read(path)
            path.write_bytes(self.variants()["bom-crlf"])
            self.assertEqual("WO-X-001", front_matter.read(path)["id"])

    def test_split_document_keeps_the_body_newlines_and_the_bom_for_the_write_back(self) -> None:
        for name, data in self.variants().items():
            with self.subTest(form=name):
                document = front_matter.split_document(data)
                self.assertEqual(('id = "WO-X-001"', 'type = "work_order"'), document.front_lines)
                newline = "\r\n" if b"\r\n" in data else ("\r" if b"\r" in data else "\n")
                self.assertEqual(newline, document.newline)
                self.assertTrue(document.body.startswith(newline + "# Title"))
                self.assertEqual(data.startswith(b"\xef\xbb\xbf"), document.opening.startswith("﻿"))
                self.assertTrue(document.opening.endswith("+++" + newline))
        with self.assertRaisesRegex(HarnessError, "closing front-matter delimiter"):
            front_matter.split_document(b"+++\nid = 1\n", error=HarnessError)

    def test_partition_returns_the_toml_text_and_the_body(self) -> None:
        head, body = front_matter.partition(self.LF.decode("utf-8"))
        self.assertEqual('id = "WO-X-001"\ntype = "work_order"', head)
        self.assertTrue(body.startswith("\n# Title"))
        self.assertIsNone(front_matter.partition("plain prose"))

    def test_no_module_of_the_package_or_the_tools_splits_front_matter_itself(self) -> None:
        # ECP-PRM-005: nothing in the package looks for the delimiter itself. The engine keeps its parser
        # until wave 3 (#378); repository_tools keeps its own behind the import barrier (DEC-ECP-001).
        offenders: list[str] = []
        for path in sorted((REPOSITORY_ROOT / "se_harness").glob("*.py")):
            if path.name == "front_matter.py":
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if ('split("+++"' in line or 'index("+++"' in line or 'partition("\\n+++' in line
                        or 'startswith("+++' in line or ".find(\"\\n+++" in line):
                    offenders.append(f"{path.relative_to(REPOSITORY_ROOT).as_posix()}:{number}")
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
