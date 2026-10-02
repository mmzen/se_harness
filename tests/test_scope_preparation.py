"""REQ-KIS-010 / SPEC-KIS-004: assess a plan without creating authority."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest import mock

from se_harness.workflow_result import restitution_digest
from tests.artifact_support import (
    RELEASED_EVALUATOR_EVIDENCE_PATH,
    create_base_chain, verification_record, release_record, write,
)
from tests.cli_support import invoke
from tests.fixture_support import standard_repository
from tests.git_support import git, init_repository
from tests.mutation_guard_support import patch_mutation_authority


WO_PATH = "docs/engineering/product/work-orders/WO-001.md"


class PlannedPathTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        standard_repository(self.root)
        create_base_chain(self.root, work_order_status="draft", operating_contract_status="draft")
        self.work_order = self.root / WO_PATH
        self.work_order.write_text(
            self.work_order.read_text(encoding="utf-8").replace(
                "[relations]", '[execution_scope]\npaths = ["src/exact.py", "src/component/"]\n\n[relations]', 1,
            ), encoding="utf-8",
        )

    def check(self, *paths: str, extra: tuple[str, ...] = ()) -> tuple[int, dict, str]:
        args = ["check", str(self.root), "--artifact", "WO-001", "--json"]
        for path in paths:
            args += ["--planned-path", path]
        code, output, error = invoke(*args, *extra)
        return code, json.loads(output) if output else {}, error

    def snapshot(self) -> dict[str, bytes]:
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_plan_coverage_preserves_projection_and_does_not_write(self) -> None:
        before = self.snapshot()
        code, ordinary, error = self.check()
        self.assertEqual(0, code, error)
        code, result, error = self.check(
            "src/exact.py", "src/component/future.py", "src/component-extra/test.py", WO_PATH,
        )
        self.assertEqual(0, code, error)  # Command completion is deliberately not a coverage verdict.
        preparation = result["scope"].pop("preparation")
        self.assertEqual("uncovered", preparation["coverage"])
        self.assertEqual([
            {"path": "src/component/future.py", "scope_entry": "src/component/"},
            {"path": "src/exact.py", "scope_entry": "src/exact.py"},
        ], preparation["explicit_matches"])
        self.assertEqual([{"path": WO_PATH, "rule": "own-work-order", "work_order": "WO-001"}],
                         preparation["automatic_matches"])
        self.assertEqual(["src/component-extra/test.py"], preparation["uncovered_paths"])
        self.assertEqual("not_assessed", preparation["impact_analysis"])
        result.pop("result_sha256")
        ordinary.pop("result_sha256")
        self.assertEqual(ordinary, result)
        self.assertEqual(before, self.snapshot())

    def test_covered_draft_and_approved_plans_are_not_gates_or_actual_changes(self) -> None:
        for state in ("draft", "approved"):
            with self.subTest(state=state):
                if state == "approved":
                    self.work_order.write_text(self.work_order.read_text().replace('status = "draft"', 'status = "approved"', 1))
                _, ordinary, _ = self.check()
                code, result, error = self.check("src/exact.py")
                self.assertEqual("covered", result["scope"]["preparation"]["coverage"], error)
                self.assertEqual(ordinary["operation"], result["operation"])
                self.assertEqual(ordinary["restitution"], result["restitution"])
                self.assertEqual([], result["compliance"]["gates"])
                self.assertEqual([], result["scope"]["changed_paths"])
                self.assertFalse(result["scope"]["change_set_complete"])
                self.assertEqual([], result["mutation"]["writes"])

    def test_linked_outputs_are_exact_and_other_evidence_needs_scope(self) -> None:
        record = "docs/engineering/product/verification-records/VREC-001.md"
        evaluator = "docs/engineering/product/evidence/VREC-001-evaluator.json"
        release = "docs/engineering/releases/RLS-001.md"
        release_evaluator = "docs/engineering/product/evidence/RLS-001-evaluator.json"
        text = verification_record("a" * 40, status="ready").replace(
            "[relations]", f'evaluator_evidence_path = "{evaluator}"\n\n[relations]', 1,
        )
        write(self.root / record, text)
        write(self.root / release, release_record("a" * 40, status="ready").replace(
            RELEASED_EVALUATOR_EVIDENCE_PATH, release_evaluator,
        ))
        unrelated = record.replace("VREC-001", "VREC-002")
        write(self.root / unrelated, text.replace("VREC-001", "VREC-002").replace(
            'verifies_work_order = ["WO-001"]', 'verifies_work_order = ["WO-002"]',
        ))
        neighbor = "docs/engineering/product/evidence/unlisted-review.md"
        packet = "docs/engineering/product/evidence/WO-001/handoff.json"
        _, result, _ = self.check(record, evaluator, release, release_evaluator, unrelated, neighbor, packet)
        preparation = result["scope"]["preparation"]
        self.assertEqual({record, evaluator, release, release_evaluator, packet},
                         {item["path"] for item in preparation["automatic_matches"]})
        self.assertEqual(sorted([unrelated, neighbor]), preparation["uncovered_paths"])

    def test_invalid_paths_and_duplicate_case_variants_never_become_matches(self) -> None:
        before = self.snapshot()
        for paths in (("../escape",), ("/absolute",), ("C:/drive",), ("src/./dot",),
                      ("src\\alternate",), ("src/directory/",), ("src/A.py", "src/a.py")):
            with self.subTest(paths=paths):
                code, result, error = self.check(*paths)
                self.assertNotEqual(0, code)
                self.assertTrue(result.get("restitution", {}).get("blocked_by") or error)
                self.assertNotIn("preparation", result.get("scope", {}))
        self.assertEqual(before, self.snapshot())

    def test_invalid_scope_is_reported_without_fallback_admission(self) -> None:
        self.work_order.write_text(self.work_order.read_text().replace(
            '["src/exact.py", "src/component/"]', '["../escape"]',
        ))
        _, result, _ = self.check(WO_PATH)
        preparation = result["scope"]["preparation"]
        self.assertEqual("invalid", preparation["coverage"])
        self.assertIn("../escape", preparation["invalid_declarations"][0])
        self.assertEqual([], preparation["automatic_matches"])

    def test_existing_directory_and_symlink_escape_are_refused(self) -> None:
        (self.root / "src/component").mkdir(parents=True)
        code, _, _ = self.check("src/component")
        self.assertNotEqual(0, code)
        with tempfile.TemporaryDirectory() as outside:
            try:
                (self.root / "src/link").symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"host cannot create test symlink: {exc}")
            code, _, error = self.check("src/link/future.py")
            self.assertNotEqual(0, code, error)

    def test_mixed_options_and_missing_or_non_work_order_selection_are_refused(self) -> None:
        for extra in (("--checkpoint", "scope"), ("--target", "approved"),
                      ("--procedure", "PROC-WO-START"), ("--changed-path", "src/exact.py"),
                      ("--changes-complete",), ("--change-manifest", "changes.json"),
                      ("--from-git", "HEAD"), ("--pull-request-body", "body.md")):
            with self.subTest(extra=extra):
                code, _, error = invoke("check", str(self.root), "--artifact", "WO-001",
                                        "--planned-path", "src/exact.py", *extra)
                self.assertNotEqual(0, code)
                self.assertIn("--planned-path cannot be combined with", error)
        for selection in ((), ("--artifact", "WO-404"), ("--artifact", "INT-001")):
            with self.subTest(selection=selection):
                code, output, error = invoke("check", str(self.root), *selection,
                                            "--planned-path", "src/exact.py", "--json")
                self.assertNotEqual(0, code, output + error)
        write(self.root / "docs/engineering/product/verification-records/VREC-001.md",
              verification_record("a" * 40, status="ready"))
        code, output, error = invoke("check", str(self.root), "--artifact", "VREC-001",
                                    "--planned-path", "src/exact.py", "--json")
        self.assertNotEqual(0, code)
        self.assertIn("only to a work order", output + error)

    def test_report_is_clear_and_machine_planning_data_is_digest_bound(self) -> None:
        _, result, _ = self.check("src/exact.py", "tests/missing.py")
        self.assertEqual(result["result_sha256"], restitution_digest(result))
        edited = copy.deepcopy(result)
        edited["scope"]["preparation"]["uncovered_paths"] = []
        self.assertNotEqual(result["result_sha256"], restitution_digest(edited))
        edited = copy.deepcopy(result)
        edited["scope"]["preparation"]["planned_paths"].append("tests/another.py")
        self.assertNotEqual(result["result_sha256"], restitution_digest(edited))
        _, output, _ = invoke("check", str(self.root), "--artifact", "WO-001",
                              "--planned-path", "src/exact.py", "--planned-path", "tests/missing.py")
        self.assertIn("Coverage: uncovered", output)
        self.assertIn("tests/missing.py: uncovered", output)
        self.assertIn("No approval, gate result or proof of complete impact analysis.", output)

    def test_planning_reuses_one_repository_validation(self) -> None:
        from se_harness.engine import validate_engineering_artifacts

        with mock.patch.object(validate_engineering_artifacts, "validate_repository",
                               wraps=validate_engineering_artifacts.validate_repository) as validate:
            self.check("src/exact.py")
        self.assertEqual(1, validate.call_count)


class ScopeDemonstrationTests(unittest.TestCase):
    """Small real fixture workflows, not claims about exhaustive discovery."""

    def setUp(self) -> None:
        patch_mutation_authority(self)
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        standard_repository(self.root)
        create_base_chain(self.root, work_order_status="draft", operating_contract_status="draft")
        for path in list((self.root / "docs/engineering").rglob("*.md")):
            path.write_text(path.read_text().replace("WO-001", "WO-PRD-001"), encoding="utf-8")
            if "WO-001" in path.name:
                path.rename(path.with_name(path.name.replace("WO-001", "WO-PRD-001")))
        lock_path = self.root / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text())
        lock["evaluator"]["archive_name"] = f"se_harness-{lock['tool_version']}-py3-none-any.whl"
        lock["evaluator"]["archive_sha256"] = "a" * 64
        lock_path.write_text(json.dumps(lock), encoding="utf-8")

    def command(self, *args: str) -> dict:
        code, output, error = invoke(args[0], str(self.root), *args[1:], "--json")
        self.assertEqual(0, code, output + error)
        return json.loads(output)

    def demonstrate(self, name: str, files: dict[str, str], before: dict[str, str]) -> None:
        expected = list(files)
        for path, content in before.items():
            write(self.root / path, content)
        evidence_dir = "docs/engineering/product/evidence/WO-PRD-001/"
        evidence = evidence_dir + "review.md"
        wo = self.root / WO_PATH.replace('WO-001', 'WO-PRD-001')
        template = wo.read_text()
        def declare(paths: list[str]) -> None:
            fields = (
                '[assurance]\ncommit_bound_verification = "required"\n'
                'rationale = "Fixture implementation needs exact-candidate verification."\n'
                'decided_by = "Fixture human"\n'
                '[execution_scope]\npaths = ' + json.dumps([*paths, evidence_dir]) + "\n\n"
            )
            wo.write_text(template.replace("[relations]", fields + "[relations]", 1), encoding="utf-8")
        planned_args = [arg for path in expected for arg in ("--planned-path", path)]
        declare(expected[:-1])
        omitted = self.command("check", "--artifact", "WO-PRD-001", *planned_args)
        self.assertEqual([expected[-1]], omitted["scope"]["preparation"]["uncovered_paths"])
        declare(expected)
        planned = self.command("check", "--artifact", "WO-PRD-001", *planned_args)
        self.assertEqual("covered", planned["scope"]["preparation"]["coverage"])
        init_repository(self.root)
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "Fixture definitions and planned scope")
        base = git(self.root, "rev-parse", "HEAD")
        self.command("transition", "--set", "WO-PRD-001=approved", "--decision", "WO-PRD-001=Fixture human",
                     "--reason", "WO-PRD-001=Approve this temporary fixture scope and required verification.", "--apply")
        approved_paths = tomllib.loads(wo.read_text().split("+++")[1])["execution_scope"]["paths"]
        self.command("preflight", "--work-order", "WO-PRD-001", "--phase", "start")
        self.command("transition", "--set", "WO-PRD-001=in_progress", "--decision", "WO-PRD-001=Fixture agent", "--apply")
        code, output, _ = invoke("check", str(self.root), "--artifact", "WO-PRD-001", "--checkpoint", "scope",
                                 "--changed-path", "unrelated/new.py", "--changes-complete", "--json")
        self.assertNotEqual(0, code)
        expansion = json.loads(output)
        self.assertTrue(any("QGP-G4I-PATHS" in item for item in expansion["restitution"]["blocked_by"]))
        # Exercise the new assertion against the old behavior before fixing it.
        write(self.root / expected[-1], files[expected[-1]])
        test_argv = [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"]
        regression = subprocess.run(test_argv, cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(0, regression.returncode, "The example must reproduce the old behavior's failure.")
        for path, content in files.items():
            write(self.root / path, content)
        test = subprocess.run(test_argv, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(0, test.returncode, test.stdout + test.stderr)
        write(self.root / evidence, "# Before correction\n\n" + regression.stdout + regression.stderr
              + "\n# After correction\n\n" + test.stdout + test.stderr)
        self.command("evidence", "--artifact", "WO-PRD-001", "--checkpoint", "handoff")
        handoff = self.command("check", "--artifact", "WO-PRD-001", "--checkpoint", "handoff", "--from-git", base)
        self.command("transition", "--set", "WO-PRD-001=implemented", "--decision", "WO-PRD-001=Fixture agent", "--apply")
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "Fixture implementation and handoff")
        candidate = git(self.root, "rev-parse", "HEAD")
        self.command("capture-verification", "--id", "VREC-001", "--work-order", "WO-PRD-001",
                     "--verification", "VER-001", "--evidence", evidence, "--owner", "Fixture agent")
        record_path = "docs/engineering/product/verification-records/VREC-001.md"
        record = tomllib.loads((self.root / record_path).read_text().split("+++")[1])
        self.assertEqual("ready", record["status"])
        self.assertEqual(candidate, record["commit"])
        actual = self.command("check", "--artifact", "WO-PRD-001", "--planned-path", record_path,
                              "--planned-path", record["evaluator_evidence_path"])
        self.assertEqual("covered", actual["scope"]["preparation"]["coverage"])
        final = tomllib.loads(wo.read_text().split("+++")[1])
        self.assertEqual("implemented", final["status"])
        self.assertEqual(approved_paths, final["execution_scope"]["paths"])
        self.assertEqual(1, len(list(wo.parent.glob("WO-*.md"))))
        print(json.dumps({
            "demonstration": name, "planned": planned["scope"]["preparation"],
            "detected_omission": omitted["scope"]["preparation"]["uncovered_paths"],
            "expansion_blocked_by": expansion["restitution"]["blocked_by"],
            "changed_paths": handoff["scope"]["changed_paths"],
            "handoff": handoff["operation"], "candidate": candidate,
            "record": {"id": record["id"], "status": record["status"], "commit": record["commit"]},
            "generated_outputs": actual["scope"]["preparation"],
            "work_order_count": 1, "approved_scope_unchanged": True,
            "regression_exit": regression.returncode, "corrected_exit": test.returncode,
        }, sort_keys=True))

    def test_bug_fix_reaches_verification_without_an_extra_work_order(self) -> None:
        self.demonstrate("bug-fix", {
            "src/parser.py": "def parse(text, prefix=''):\n    return int(text.removeprefix(prefix))\n",
            "src/caller.py": "from src.parser import parse\ndef display(text):\n    return str(parse(text, prefix='#'))\n",
            "fixtures/number.txt": "#42\n",
            "tests/test_number.py": (
                "import unittest\nfrom pathlib import Path\nfrom src.caller import display\n"
                "class NumberTest(unittest.TestCase):\n"
                "    def test_prefixed_number(self):\n"
                "        self.assertEqual('42', display('#42'))\n"
                "        self.assertEqual('42', display(Path('fixtures/number.txt').read_text().strip()))\n"
            ),
        }, before={
            "src/parser.py": "def parse(text):\n    return int(text)\n",
            "src/caller.py": "from src.parser import parse\ndef display(text):\n    return str(parse(text))\n",
            "fixtures/number.txt": "42\n",
            "tests/test_number.py": "import unittest\n",
        })

    def test_instruction_change_reaches_verification_without_an_extra_work_order(self) -> None:
        self.demonstrate("instruction-change", {
            "docs/procedure.md": "# Prepare work\nInspect dependencies and use --planned-path before approval.\n",
            "templates/work.md": "# Expected change surface\nRecord each path and its reason.\n",
            "docs/cli.md": "# CLI\n--planned-path reports coverage; it does not approve work.\n",
            "tests/test_guidance.py": (
                "import unittest\nfrom pathlib import Path\nclass GuidanceTest(unittest.TestCase):\n"
                "    def test_preparation_contract(self):\n"
                "        self.assertIn('--planned-path before approval', Path('docs/procedure.md').read_text())\n"
                "        self.assertIn('path and its reason', Path('templates/work.md').read_text())\n"
                "        self.assertIn('does not approve work', Path('docs/cli.md').read_text())\n"
            ),
        }, before={
            "docs/procedure.md": "# Prepare work\nDraft a work order.\n",
            "templates/work.md": "# Expected change surface\nName a component.\n",
            "docs/cli.md": "# CLI\nUse check to select work.\n",
            "tests/test_guidance.py": "import unittest\n",
        })
