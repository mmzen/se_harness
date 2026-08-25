from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness import preflight as preflight_module
from se_harness.cli import main
from se_harness.installer import plan_install, template_files, template_root
from se_harness.preflight import render_preflight, run_preflight
from tests.mutation_guard_support import trusted_mutation_authority


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads(
    (
        REPOSITORY_ROOT / "tests" / "fixtures" / "repository_context_retirement" / "released-baseline.json"
    ).read_text(encoding="utf-8")
)
RETIRED_PATH = BASELINE["retired_path"]
RETIRED_FAMILY = tuple(BASELINE["retired_diagnostic_family"])
RETIRED_LABELS = tuple(BASELINE["retired_field_labels"])
OWNER_CONTENT_CASES = (
    ("empty", b""),
    ("crlf", b"# Curated\r\n- Test: python -m unittest\r\n"),
    ("binary", bytes(range(256))),
    ("long-lf", ("# Curated\n" + "".join(f"- line {index}\n" for index in range(400))).encode("utf-8")),
    ("no-trailing-newline", b"- Test: python -m unittest"),
)


class RepositoryContextRetirementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.guard = mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=trusted_mutation_authority,
        )
        self.guard.start()
        self.addCleanup(self.guard.stop)
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

    def installed_target(self, name: str) -> Path:
        target = self.root / name
        code, _, error = self.invoke("init", str(target), "--project-name", "Example")
        self.assertEqual(0, code, error)
        return target

    def lock_bytes(self, target: Path) -> bytes:
        return (target / ".engineering-harness.lock").read_bytes()

    def test_no_template_maps_to_the_retired_path_or_a_successor_scaffold(self) -> None:
        seeds = [item for item in template_files() if item.mode == "seed"]
        self.assertNotIn(RETIRED_PATH, [item.target.as_posix() for item in seeds])
        self.assertNotIn(RETIRED_PATH, [item.target.as_posix() for item in template_files()])
        for item in seeds:
            text = item.source.read_text(encoding="utf-8")
            for label in RETIRED_LABELS:
                with self.subTest(seed=item.target.as_posix(), label=label):
                    self.assertNotIn(f"- {label}:", text)
        root = template_root()
        self.assertEqual([], sorted(path.relative_to(root).as_posix() for path in root.rglob("*CONTEXT*")))

    def test_fresh_installation_creates_no_file_and_no_lock_entry(self) -> None:
        target = self.installed_target("fresh")
        self.assertFalse((target / RETIRED_PATH).exists())
        lock = json.loads(self.lock_bytes(target).decode("utf-8"))
        self.assertNotIn(RETIRED_PATH, lock["files"])

    def test_start_preflight_is_ready_without_the_retired_family_or_path(self) -> None:
        target = self.installed_target("ready")
        self.add_selected_work_order(target)
        report = run_preflight(target, work_order_id="WO-EX-001", phase="start")
        self.assertTrue(report.ready, report.diagnostics)
        emitted = {item.code for item in report.diagnostics}
        self.assertEqual(set(), emitted.intersection(RETIRED_FAMILY))
        self.assertNotIn(RETIRED_PATH, report.reading_manifest)
        self.assertNotIn(RETIRED_PATH, render_preflight(report))

    def test_upgrade_converges_the_four_prior_states_to_one_lock(self) -> None:
        owner_bytes = b"# Owner curated\n- Test: python -m unittest\n"
        locks: dict[str, bytes] = {}
        for row in ("absent-absent", "present-present", "present-absent", "removed-absent"):
            target = self.installed_target(row)
            lock_path = target / ".engineering-harness.lock"
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            if row == "absent-absent":
                pass
            elif row == "removed-absent":
                lock["files"][RETIRED_PATH] = {"mode": "seed", "state": "removed"}
            else:
                lock["files"][RETIRED_PATH] = {"mode": "seed", "state": "present"}
            if row.endswith("-present"):
                (target / RETIRED_PATH).write_bytes(owner_bytes)
            lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            code, output, error = self.invoke("upgrade", str(target), "--apply")
            self.assertEqual(0, code, error)
            self.assertNotIn(RETIRED_PATH, output)
            regenerated = json.loads(lock_path.read_text(encoding="utf-8"))
            self.assertNotIn(RETIRED_PATH, regenerated["files"])
            if row.endswith("-present"):
                self.assertEqual(owner_bytes, (target / RETIRED_PATH).read_bytes())
            else:
                self.assertFalse((target / RETIRED_PATH).exists())
            locks[row] = self.lock_bytes(target)

        distinct = sorted(set(locks.values()))
        self.assertEqual(1, len(distinct), sorted(locks))

    def test_repeated_upgrade_is_idempotent(self) -> None:
        target = self.installed_target("idempotent")
        self.assertEqual(0, self.invoke("upgrade", str(target), "--apply")[0])
        first = self.lock_bytes(target)
        before = self.snapshot(target)
        self.assertEqual(0, self.invoke("upgrade", str(target), "--apply")[0])
        self.assertEqual(first, self.lock_bytes(target))
        self.assertEqual(before, self.snapshot(target))

    def test_upgrade_never_alters_owner_bytes_at_the_retired_path(self) -> None:
        for name, content in OWNER_CONTENT_CASES:
            with self.subTest(content=name):
                target = self.installed_target(f"owner-{name}")
                owner_path = target / RETIRED_PATH
                owner_path.write_bytes(content)
                code, _, error = self.invoke("upgrade", str(target), "--apply")
                self.assertEqual(0, code, error)
                self.assertEqual(content, owner_path.read_bytes())
                code, output, _ = self.invoke("doctor", str(target))
                self.assertEqual(0, code, output)
                self.assertNotIn(RETIRED_PATH, output)
                lock = json.loads(self.lock_bytes(target).decode("utf-8"))
                self.assertNotIn(RETIRED_PATH, lock["files"])

    def test_upgrade_plans_no_change_for_owner_content_at_the_retired_path(self) -> None:
        target = self.installed_target("planned")
        (target / RETIRED_PATH).write_bytes(b"# Owner curated\n")
        changes, _ = plan_install(target, project_name=None, mode="upgrade")
        self.assertNotIn(RETIRED_PATH, [item.path for item in changes])

    def test_reading_manifest_keeps_the_baseline_order_without_the_retired_path(self) -> None:
        expected = [item for item in BASELINE["preflight"]["policy_paths"] if item != RETIRED_PATH]
        self.assertNotIn(RETIRED_PATH, preflight_module.POLICY_PATHS)
        self.assertNotIn(RETIRED_PATH, preflight_module.REQUIRED_PATHS)
        self.assert_ordered_subsequence(expected, list(preflight_module.POLICY_PATHS))
        self.assert_ordered_subsequence(
            [item for item in BASELINE["preflight"]["required_paths"] if item != RETIRED_PATH],
            list(preflight_module.REQUIRED_PATHS),
        )

        target = self.installed_target("manifest")
        self.add_selected_work_order(target)
        for phase in ("start", "review"):
            with self.subTest(phase=phase):
                report = run_preflight(target, work_order_id="WO-EX-001", phase=phase)
                manifest = list(report.reading_manifest)
                self.assertEqual(list(preflight_module.READING_PATHS), manifest[: len(preflight_module.READING_PATHS)])
                self.assertFalse(set(preflight_module.POLICY_PATHS) - set(preflight_module.READING_PATHS) & set(manifest))
                self.assertNotIn(RETIRED_PATH, manifest)

    def test_payload_advances_the_schema_and_drops_only_the_command_object(self) -> None:
        target = self.installed_target("payload")
        self.add_selected_work_order(target)
        payload = run_preflight(target, work_order_id="WO-EX-001", phase="start").to_dict()
        baseline_keys = list(BASELINE["preflight"]["payload_keys"])
        self.assertEqual(
            [key for key in baseline_keys if key != "repository_commands"],
            list(payload),
        )
        self.assertEqual("se-harness-preflight-v2", payload["schema"])
        self.assertNotEqual(BASELINE["preflight"]["schema"], payload["schema"])
        self.assertNotIn("repository_commands", json.dumps(payload))

    def test_adoption_guidance_directs_operational_facts_to_the_owner_region(self) -> None:
        target = self.root / "guided"
        target.mkdir()
        (target / "pyproject.toml").write_text("[project]\nname = \"guided\"\n", encoding="utf-8")
        code, _, error = self.invoke("adopt", str(target), "--project-name", "Example")
        self.assertEqual(0, code, error)
        report = (target / "docs" / "engineering" / "ADOPTION_REPORT.md").read_text(encoding="utf-8")
        steps = [line for line in report.splitlines() if line[:3] in {"1. ", "2. ", "3. ", "4. ", "5. "}]
        self.assertEqual(["1. ", "2. ", "3. ", "4. ", "5. "], [line[:3] for line in steps])
        self.assertIn("owner-controlled region of `AGENTS.md`", steps[0])
        self.assertNotIn("CONTEXT", report)
        self.assertNotIn(RETIRED_PATH, report)

    def test_retired_diagnostic_family_is_absent_from_the_emitted_code_space(self) -> None:
        target = self.installed_target("codes")
        self.add_selected_work_order(target)
        emitted: set[str] = set()
        cases = (
            ("WO-EX-001", "start"),
            ("WO-EX-001", "review"),
            ("WO-EX-001;echo-pwned", "start"),
            ("WO-EX-404", "start"),
        )
        (target / RETIRED_PATH).write_text(
            "".join(f"- {label}: TODO[{index}]\n" for index, label in enumerate(RETIRED_LABELS)),
            encoding="utf-8",
        )
        for work_order_id, phase in cases:
            report = run_preflight(target, work_order_id=work_order_id, phase=phase)
            emitted.update(item.code for item in report.diagnostics)
        self.assertEqual(set(), emitted.intersection(RETIRED_FAMILY))
        self.assertTrue(emitted, "the corpus must exercise at least one diagnostic")

    def add_selected_work_order(self, target: Path) -> None:
        domain = target / "docs" / "engineering" / "example"
        for folder in ("intent", "capabilities", "requirements", "specifications", "verification", "work-orders"):
            (domain / folder).mkdir(parents=True, exist_ok=True)
        (domain / "intent" / "INT-EX-001.md").write_text(
            self.artifact("INT-EX-001", "intent", "Example intent", relations=""),
            encoding="utf-8",
        )
        (domain / "capabilities" / "CAP-EX-001.md").write_text(
            self.artifact("CAP-EX-001", "capability", "Example capability", relations='derives_from = ["INT-EX-001"]'),
            encoding="utf-8",
        )
        (domain / "requirements" / "REQ-EX-001.md").write_text(
            self.artifact(
                "REQ-EX-001",
                "requirement",
                "Example requirement",
                relations='derives_from = ["CAP-EX-001"]',
                extra='statement = "WHEN a case runs, THE SYSTEM SHALL behave."\nverification_method = "automated-test"',
            ),
            encoding="utf-8",
        )
        (domain / "specifications" / "SPEC-EX-001.md").write_text(
            self.artifact("SPEC-EX-001", "specification", "Example specification", relations='specifies = ["REQ-EX-001"]'),
            encoding="utf-8",
        )
        (domain / "verification" / "VER-EX-001.md").write_text(
            self.artifact("VER-EX-001", "verification", "Example verification", relations='verifies = ["REQ-EX-001"]'),
            encoding="utf-8",
        )
        (domain / "work-orders" / "WO-EX-001.md").write_text(
            self.artifact(
                "WO-EX-001",
                "work_order",
                "Example work order",
                relations=(
                    'implements = ["REQ-EX-001"]\n'
                    'specifications = ["SPEC-EX-001"]\n'
                    'verification = ["VER-EX-001"]'
                ),
                extra=(
                    "[assurance]\n"
                    'commit_bound_verification = "required"\n'
                    'rationale = "The fixture changes trusted engineering behavior."\n'
                    'decided_by = "test-owner"\n\n'
                    "[execution_scope]\n"
                    'paths = ["src/"]'
                ),
                status="in_progress",
            ),
            encoding="utf-8",
        )

    def artifact(
        self,
        artifact_id: str,
        artifact_type: str,
        title: str,
        *,
        relations: str,
        extra: str = "",
        status: str = "approved",
    ) -> str:
        lines = [
            "+++",
            f'id = "{artifact_id}"',
            f'type = "{artifact_type}"',
            f'title = "{title}"',
            f'status = "{status}"',
            'owners = ["engineering-owner"]',
            'created = "2026-08-21"',
            'updated = "2026-08-21"',
        ]
        if extra:
            lines.extend(["", extra])
        if relations:
            lines.extend(["", "[relations]", relations])
        lines.extend(["+++", "", f"# {title}", "", "Fixture content."])
        return "\n".join(lines) + "\n"

    def snapshot(self, target: Path) -> dict[str, bytes]:
        return {
            path.relative_to(target).as_posix(): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }

    def assert_ordered_subsequence(self, expected: list[str], actual: list[str]) -> None:
        positions = [actual.index(item) if item in actual else -1 for item in expected]
        self.assertNotIn(-1, positions, f"{expected} is not contained in {actual}")
        self.assertEqual(sorted(positions), positions, f"{expected} is reordered in {actual}")


if __name__ == "__main__":
    unittest.main()
