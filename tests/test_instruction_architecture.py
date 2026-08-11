from __future__ import annotations

import contextlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from se_harness.cli import main
from se_harness.installer import BEGIN_MARKER, END_MARKER, plan_install, tracked_content
from se_harness.integrity import HASH_ALGORITHM, HASH_MODE, canonical_sha256


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKET_ROOT = REPOSITORY_ROOT / "docs" / "engineering" / "instruction-architecture"
WHEEL_SHA256 = "56db717e5287492c421e11157545586b1e8f0ec2dd4011a9932ccf35f233d63d"


class InstructionArchitectureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = main(list(arguments))
        return result, stdout.getvalue(), stderr.getvalue()

    def installed_target(self, name: str = "target") -> Path:
        target = self.root / name
        code, _, error = self.invoke("init", str(target), "--project-name", "Example")
        self.assertEqual(0, code, error)
        return target

    def add_active_packet(self, target: Path, *, status: str = "in_progress") -> None:
        destination = target / "docs" / "engineering" / "instruction-architecture"
        shutil.copytree(PACKET_ROOT, destination)
        work_order = destination / "work-orders" / "WO-IAR-001.md"
        text = work_order.read_text(encoding="utf-8")
        text = re.sub(r'^status = "[^"]+"$', f'status = "{status}"', text, count=1, flags=re.MULTILINE)
        work_order.write_text(text, encoding="utf-8")

    def curate_context(self, target: Path) -> None:
        path = target / "docs" / "engineering" / "REPOSITORY_CONTEXT.md"
        text = re.sub(r"TODO\[[A-Za-z0-9-]+\]", "confirmed", path.read_text(encoding="utf-8"))
        text = text.replace("- Repository purpose: confirmed", "- Repository purpose: Track TODO items safely")
        path.write_text(text, encoding="utf-8")

    def test_instruction_route_and_ownership_modes_are_explicit(self) -> None:
        target = self.installed_target()
        agents = (target / "AGENTS.md").read_text(encoding="utf-8")
        managed = agents.split(BEGIN_MARKER, 1)[1].split(END_MARKER, 1)[0]
        self.assertIn("ENGINEERING_HARNESS.md", managed)
        self.assertNotIn("REPOSITORY_CONTEXT.md", managed)
        claude = (target / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertEqual(1, sum(line.strip() == "@AGENTS.md" for line in claude.splitlines()))

        router = (target / "ENGINEERING_HARNESS.md").read_text(encoding="utf-8")
        for name in ("WORKFLOW.md", "DECISION_RIGHTS.md", "QUALITY_GATES.md", "TRACEABILITY.md"):
            self.assertIn(name, router)
        index = (target / "docs" / "engineering" / "README.md").read_text(encoding="utf-8")
        self.assertIn("Repository-owned after installation", index)
        self.assertNotIn("## Workflow", index)

        lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual("fragment", lock["files"]["AGENTS.md"]["mode"])
        self.assertEqual("fragment", lock["files"]["CLAUDE.md"]["mode"])
        self.assertEqual("managed", lock["files"]["ENGINEERING_HARNESS.md"]["mode"])
        self.assertEqual("seed", lock["files"]["docs/engineering/README.md"]["mode"])
        self.assertEqual("seed", lock["files"]["docs/engineering/REPOSITORY_CONTEXT.md"]["mode"])
        self.assertTrue((target / ".github" / "PULL_REQUEST_TEMPLATE.md").is_file())

    def test_managed_readme_to_seed_migration_is_safe_and_transactional(self) -> None:
        target = self.installed_target("exact")
        readme = target / "docs" / "engineering" / "README.md"
        old_managed = b"# Old managed engineering index\n"
        readme.write_bytes(old_managed)
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"]["docs/engineering/README.md"] = {
            "mode": "managed",
            "sha256": canonical_sha256(old_managed),
        }
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        changes, _ = plan_install(target, project_name=None, mode="upgrade")
        action = {item.path: item.action for item in changes}
        self.assertEqual("update", action["docs/engineering/README.md"])
        code, output, error = self.invoke("upgrade", str(target), "--apply")
        self.assertEqual(0, code, error)
        self.assertIn("update     docs/engineering/README.md", output)
        self.assertIn("Repository-owned after installation", readme.read_text(encoding="utf-8"))
        migrated = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertEqual({"mode": "seed", "state": "present"}, migrated["files"]["docs/engineering/README.md"])
        self.assertEqual(0, self.invoke("upgrade", str(target), "--apply")[0])

        customized = self.installed_target("customized")
        customized_readme = customized / "docs" / "engineering" / "README.md"
        customized_readme.write_bytes(old_managed + b"Owner customization.\n")
        customized_lock_path = customized / ".engineering-harness.lock"
        customized_lock = json.loads(customized_lock_path.read_text(encoding="utf-8"))
        customized_lock["files"]["docs/engineering/README.md"] = {
            "mode": "managed",
            "sha256": canonical_sha256(old_managed),
        }
        customized_lock_path.write_text(
            json.dumps(customized_lock, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        missing = customized / "docs" / "engineering" / "TRACEABILITY.md"
        missing.unlink()
        original_readme = customized_readme.read_bytes()
        original_lock = customized_lock_path.read_bytes()

        code, output, error = self.invoke("upgrade", str(customized), "--apply")
        self.assertEqual(1, code)
        self.assertIn("customized docs/engineering/README.md", output)
        self.assertIn("no files were written", error)
        self.assertEqual(original_readme, customized_readme.read_bytes())
        self.assertEqual(original_lock, customized_lock_path.read_bytes())
        self.assertFalse(missing.exists())

        legacy = self.installed_target("legacy-newlines")
        legacy_readme = legacy / "docs" / "engineering" / "README.md"
        legacy_lf = b"# Legacy managed index\n\nLine two.\n"
        legacy_readme.write_bytes(legacy_lf.replace(b"\n", b"\r\n"))
        legacy_lock_path = legacy / ".engineering-harness.lock"
        legacy_lock = json.loads(legacy_lock_path.read_text(encoding="utf-8"))
        legacy_lock["schema"] = 1
        legacy_lock.pop("hash_algorithm", None)
        legacy_lock.pop("hash_mode", None)
        legacy_lock["files"]["docs/engineering/README.md"] = {
            "mode": "managed",
            "sha256": canonical_sha256(legacy_lf),
        }
        legacy_lock_path.write_text(
            json.dumps(legacy_lock, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        changes, _ = plan_install(legacy, project_name=None, mode="upgrade")
        self.assertEqual(
            "update",
            {item.path: item.action for item in changes}["docs/engineering/README.md"],
        )

    def test_preflight_returns_deterministic_reading_manifest_without_writes(self) -> None:
        target = self.installed_target()
        self.curate_context(target)
        self.add_active_packet(target)
        before = {
            path.relative_to(target).as_posix(): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }

        code, output, error = self.invoke(
            "preflight",
            str(target),
            "--work-order",
            "WO-IAR-001",
            "--json",
        )
        self.assertEqual(0, code, error)
        report = json.loads(output)
        self.assertEqual("se-harness-preflight-v1", report["schema"])
        self.assertTrue(report["ready"])
        self.assertEqual("start", report["phase"])
        self.assertEqual("in_progress", report["work_order"]["status"])
        self.assertEqual([], report["diagnostics"])
        for path in (
            "ENGINEERING_HARNESS.md",
            "docs/engineering/WORKFLOW.md",
            "docs/engineering/instruction-architecture/intent/INT-IAR-001.md",
            "docs/engineering/instruction-architecture/work-orders/WO-IAR-001.md",
        ):
            self.assertIn(path, report["reading_manifest"])
        self.assertEqual("confirmed", report["repository_commands"]["test"])
        after = {
            path.relative_to(target).as_posix(): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }
        self.assertEqual(before, after)

    def test_preflight_reports_context_phase_integrity_and_id_failures(self) -> None:
        incomplete = self.installed_target("incomplete")
        self.add_active_packet(incomplete)
        code, output, _ = self.invoke("preflight", str(incomplete), "--work-order", "WO-IAR-001")
        self.assertEqual(1, code)
        self.assertIn("[C004]", output)
        self.assertIn("unresolved context field", output)

        completed = self.installed_target("completed")
        self.curate_context(completed)
        self.add_active_packet(completed, status="implemented")
        code, output, _ = self.invoke("preflight", str(completed), "--work-order", "WO-IAR-001")
        self.assertEqual(1, code)
        self.assertIn("[W005]", output)
        code, output, error = self.invoke(
            "preflight",
            str(completed),
            "--work-order",
            "WO-IAR-001",
            "--phase",
            "review",
        )
        self.assertEqual(0, code, error)
        self.assertIn("Harness preflight: PASS", output)

        agents = completed / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8").replace(
                "Read `ENGINEERING_HARNESS.md`",
                "Skip `ENGINEERING_HARNESS.md`",
            ),
            encoding="utf-8",
        )
        code, output, _ = self.invoke(
            "preflight",
            str(completed),
            "--work-order",
            "WO-IAR-001",
            "--phase",
            "review",
        )
        self.assertEqual(1, code)
        self.assertIn("[I001] managed:AGENTS.md", output)

        code, output, _ = self.invoke(
            "preflight",
            str(completed),
            "--work-order",
            "WO-IAR-001;echo-pwned",
        )
        self.assertEqual(1, code)
        self.assertIn("[W001]", output)

    def test_distribution_comparison_detects_coordinated_file_and_lock_change(self) -> None:
        target = self.installed_target()
        agents = target / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8").replace(
                "Read `ENGINEERING_HARNESS.md`",
                "Skip `ENGINEERING_HARNESS.md`",
            ),
            encoding="utf-8",
        )
        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        managed = tracked_content("fragment", agents.read_bytes())
        self.assertIsNotNone(managed)
        lock["files"]["AGENTS.md"]["sha256"] = canonical_sha256(managed)
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        code, output, _ = self.invoke("doctor", str(target))
        self.assertEqual(1, code)
        self.assertIn("PASS managed:AGENTS.md", output)
        self.assertIn("FAIL distribution:AGENTS.md", output)

    def test_pull_request_work_order_selection_is_strict(self) -> None:
        target = self.installed_target()
        script = target / "scripts" / "select_harness_work_order.py"
        event = self.root / "event.json"
        event.write_text(
            json.dumps({"pull_request": {"body": "Summary\n\nHarness-Work-Order: WO-IAR-001\n"}}),
            encoding="utf-8",
        )
        completed = subprocess.run(
            [sys.executable, str(script), "--event", str(event)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("WO-IAR-001", completed.stdout.strip())

        for body in (
            "No declaration",
            "Harness-Work-Order: WO-IAR-001\nHarness-Work-Order: WO-IAR-002\n",
            "Harness-Work-Order: WO-IAR-001; echo pwned\n",
            "Harness-Work-Order: WO-...\n",
        ):
            event.write_text(json.dumps({"pull_request": {"body": body}}), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(script), "--event", str(event)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(2, completed.returncode)
            self.assertIn("expected exactly one", completed.stderr)

    def test_workflow_separates_exact_baseline_and_candidate_assurance(self) -> None:
        target = self.installed_target()
        workflow = (target / ".github" / "workflows" / "engineering-harness.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("independent-baseline:", workflow)
        self.assertIn("candidate:", workflow)
        self.assertIn("se-harness==0.2.0", workflow)
        self.assertIn(WHEEL_SHA256, workflow)
        self.assertIn("releases/download/v0.2.0/se_harness-0.2.0-py3-none-any.whl", workflow)
        self.assertIn("sha256sum --check", workflow)
        self.assertIn("template_root()", workflow)
        self.assertIn("select_harness_work_order.py", workflow)
        self.assertIn("--phase review", workflow)
        self.assertNotIn("${{ github.event.pull_request.body", workflow)
        self.assertNotIn("{{HARNESS", workflow)
        self.assertNotIn("{{BASELINE", workflow)

    def test_lock_remains_schema_two_after_instruction_install(self) -> None:
        target = self.installed_target()
        lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual(2, lock["schema"])
        self.assertEqual(HASH_ALGORITHM, lock["hash_algorithm"])
        self.assertEqual(HASH_MODE, lock["hash_mode"])


if __name__ == "__main__":
    unittest.main()
