from __future__ import annotations

import os
import re
import shlex
import struct
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

from se_harness import __version__
from tests.git_support import git


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TECHNICAL_COMMUNICATION_NOTE = REPOSITORY_ROOT / "docs/notes/technical-communication.md"
README_PATH = REPOSITORY_ROOT / "README.md"
PYPROJECT_PATH = REPOSITORY_ROOT / "pyproject.toml"


class PublicOnboardingTests(unittest.TestCase):
    """Public presentation contract in REQ-DST-069 and SPEC-DST-024."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.project = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))["project"]

    def section(self, heading: str) -> str:
        marker = f"## {heading}\n"
        self.assertEqual(1, self.readme.count(marker), f"expected one {marker.strip()} section")
        return self.readme.split(marker, 1)[1].split("\n## ", 1)[0]

    def test_root_is_a_bounded_human_entry_point(self) -> None:
        self.assertLessEqual(len(self.readme.split()), 650)
        self.assertLessEqual(len(self.readme.splitlines()), 200)
        self.assertLessEqual(len(re.findall(r"(?m)^## ", self.readme)), 7)
        self.assertIn("SE Harness / Verity Plane", self.readme)

    def test_opening_identifies_the_harness_and_retained_authority(self) -> None:
        opening = self.readme.split("## How it works today", 1)[0].lower()
        for concept in (
            "open source harness", "ai coding agents", "bounded authority",
            "verification stays independent", "decisions stay human",
            "intent", "requirements", "design", "code", "evidence",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, opening)

    def test_current_workflow_preserves_scope_evidence_and_separate_decisions(self) -> None:
        workflow = self.section("How it works today").lower()
        for concept in (
            "human approves", "work order", "agent works within that scope",
            "retains evidence", "exact candidate commit", "assurance owner",
            "release owner", "separate release decision",
            "separation between implementation and verification",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, workflow)

    def test_virtual_twin_propagation_is_a_vision_with_conformity_evidence(self) -> None:
        vision = self.section("A Virtual Twin of your Software").lower()
        for concept in (
            "vision", "building toward", "authoritative model",
            "intended software", "code is its implementation",
            "approved changes", "independent verification", "evidence",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, vision)

    def test_installation_uses_a_released_package_and_separate_repository_upgrade(self) -> None:
        install = self.section("Get started")
        for text in (
            "Python 3.11+", "outside your repository", "-m venv",
            "python -m pip install se-harness", "bin/activate",
            r"Scripts\Activate.ps1", "pinned by that repository",
            "leaves its managed files unchanged", "harness-installation-and-upgrades.md",
        ):
            with self.subTest(text=text):
                self.assertIn(text, install)
        self.assertNotRegex(install, r"pip install\s+se-harness==")
        self.assertNotIn("python -m pip install .", install)
        self.assertNotIn("harnessctl upgrade", install)
        self.assertEqual(self.project["version"], __version__)

    def test_quick_start_commands_parse_against_the_current_cli(self) -> None:
        from se_harness.cli import build_parser

        blocks = "\n".join(re.findall(r"```[^\n]*\n(.*?)\n```", self.readme, re.DOTALL))
        commands = re.findall(r"(?m)^harnessctl [^\r\n]+", blocks)
        # WO-ECP-026 (ECP-INS-009): the quick start shows the one installation command.
        self.assertEqual({"init", "doctor"}, {shlex.split(command)[1] for command in commands})
        for command in commands:
            with self.subTest(command=command):
                build_parser().parse_args(shlex.split(command)[1:])

    def test_fenced_commands_remain_on_the_public_operational_surface(self) -> None:
        blocks = "\n".join(re.findall(r"```[^\n]*\n(.*?)\n```", self.readme, re.DOTALL))
        commands = set(re.findall(r"(?m)^harnessctl\s+([a-z][a-z-]*)\b", blocks))
        self.assertTrue({"init", "doctor"}.issubset(commands))
        self.assertTrue(commands.issubset({"init", "adopt", "doctor", "validate", "inspect", "dashboard"}))

    def test_explorer_images_are_readable_repository_owned_pngs(self) -> None:
        examples = self.section("See the whole change")
        expected = [
            "docs/images/harness-explorer-lineage.png",
            "docs/images/harness-explorer-virtual-twin.png",
        ]
        self.assertEqual(expected, re.findall(r"!\[[^]]+\]\(([^)]+)\)", examples))
        for target in expected:
            with self.subTest(target=target):
                image_path = (REPOSITORY_ROOT / target).resolve()
                self.assertTrue(image_path.is_relative_to(REPOSITORY_ROOT.resolve()))
                data = image_path.read_bytes()
                self.assertEqual(b"\x89PNG\r\n\x1a\n", data[:8])
                self.assertEqual(b"IHDR", data[12:16])
                width, height = struct.unpack(">II", data[16:24])
                self.assertGreater(width, 0)
                self.assertGreater(height, 0)

    def test_deeper_guidance_remains_directly_discoverable(self) -> None:
        for target in (
            "docs/notes/README.md", "docs/notes/getting-started.md",
            "docs/notes/harness-overview.md", "docs/notes/harness-lineage-example.md",
            "docs/notes/harnessctl-reference.md", "docs/notes/developing-se-harness.md",
            "docs/notes/harness-installation-and-upgrades.md",
        ):
            with self.subTest(target=target):
                self.assertIn(f"]({target})", self.readme)
                self.assertTrue((REPOSITORY_ROOT / target).is_file())
        self.assertNotIn("https://github.com/mmzen/se_harness/blob/main/", self.readme)
        headings = re.findall(r"(?m)^## (.+)$", self.readme)
        anchors = {re.sub(r"[^\w\s-]", "", title.lower()).replace(" ", "-") for title in headings}
        for anchor in re.findall(r"\]\(#([^)]*)\)", self.readme):
            self.assertIn(anchor, anchors)

    def test_project_metadata_exposes_public_readme_license_and_urls(self) -> None:
        self.assertEqual("README.md", self.project["readme"])
        self.assertEqual({"file": "LICENSE"}, self.project["license"])
        self.assertEqual(
            {
                "Homepage": "https://github.com/mmzen/se_harness",
                "Repository": "https://github.com/mmzen/se_harness",
                "Issues": "https://github.com/mmzen/se_harness/issues",
                "Releases": "https://github.com/mmzen/se_harness/releases",
            },
            self.project["urls"],
        )
        self.assertEqual(">=3.11", self.project["requires-python"])
        self.assertEqual([], self.project["dependencies"])
        self.assertEqual("se_harness.cli:main", self.project["scripts"]["harnessctl"])

    # SPEC-TST-002 TST-HYG-013: the notes are checked for what can be resolved, not for wording.
    # The expertise label is the one sentence a specification fixes (SPEC-DST-006).
    NOTE_SECTIONS = {
        "technical-communication.md": (
            "5/10",
            ("## What the policy changes", "## What the policy protects", "## Using `harness-operator-brief`", "## Boundaries", "## Contributor checks"),
            (".agents/skills/harness-operator-brief", ".agents/skills/harness-orient"),
        ),
        "agentic-execution-phase4-skills.md": (
            None,
            ("## What changed", "## Client boundary", "## Capability and compatibility", "## Host parity and stops", "## Package qualification"),
            (".agents/skills/harness-orient",),
        ),
    }

    def test_operator_notes_are_indexed_sectioned_and_point_at_shipped_paths(self) -> None:
        index = (REPOSITORY_ROOT / "docs/notes/README.md").read_text(encoding="utf-8")
        for note, (expertise, headings, shipped) in self.NOTE_SECTIONS.items():
            content = (REPOSITORY_ROOT / "docs/notes" / note).read_text(encoding="utf-8")
            with self.subTest(note=note):
                self.assertIn(note, index)
                if expertise is not None:
                    self.assertIn(f"<!-- Target expertise: {expertise}.", content)
                for heading in headings:
                    self.assertIn(f"\n{heading}\n", content)
                for relative in shipped:
                    self.assertTrue((REPOSITORY_ROOT / relative).exists(), relative)
                    self.assertIn(Path(relative).name, content)

    def test_release_links_and_public_project_routes_remain(self) -> None:
        for url in (
            "https://pypi.org/project/se-harness/",
            "https://github.com/mmzen/se_harness",
            "https://github.com/mmzen/se_harness/issues",
            "https://github.com/mmzen/se_harness/releases",
        ):
            with self.subTest(url=url):
                self.assertIn(url, self.readme)

    def test_public_markdown_has_no_placeholders_mojibake_or_missing_local_links(self) -> None:
        for marker in ("PENDING_", "TODO", "FIXME", "\ufffd", "\u00c3", "\u00e2\u20ac"):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, self.readme)
        self.assertEqual(0, self.readme.count("```") % 2)
        self.assertNotRegex(self.readme, r"(?i)<(?:script|style)\b")
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", self.readme):
            if re.match(r"(?:https?://|mailto:|#)", target):
                continue
            local_path = (REPOSITORY_ROOT / target.split("#", 1)[0]).resolve()
            with self.subTest(target=target):
                self.assertTrue(local_path.is_file(), f"missing local README link: {target}")





HASH_BOUND_CHECKS = (
    "hash-bound-class-declared",
    "hash-bound-attribute-effective",
    "hash-bound-mode-consistent",
)


@unittest.skipUnless(shutil.which("git"), "git is unavailable")
class FreshConsumerDoctorTests(unittest.TestCase):
    """The state every adopter meets first: installed, committed once, `doctor`.

    `WO-HBI-005` for issue #207. Until then `doctor` exited 1 here on two
    hash-bound checks, and no scenario observed it because the acceptance lane
    never commits its initialized target.
    """

    def harnessctl(self, *arguments: str, cwd: Path) -> subprocess.CompletedProcess[str]:
        environment = {**os.environ, "PYTHONPATH": str(REPOSITORY_ROOT), "PYTHONNOUSERSITE": "1"}
        return subprocess.run(
            [sys.executable, "-m", "se_harness", *arguments],
            cwd=cwd,
            env=environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def fresh_consumer_doctor(self, autocrlf: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            consumer = base / "consumer"
            init = self.harnessctl("init", str(consumer), "--project-name", "Consumer", cwd=base)
            self.assertEqual(0, init.returncode, init.stdout + init.stderr)
            conversion = ("-c", f"core.autocrlf={autocrlf}")
            git(consumer, *conversion, "init", "-q", "-b", "main")
            git(consumer, *conversion, "config", "user.email", "adopter@example.invalid")
            git(consumer, *conversion, "config", "user.name", "adopter")
            git(consumer, *conversion, "config", "commit.gpgsign", "false")
            git(consumer, *conversion, "add", "-A")
            git(consumer, *conversion, "commit", "-q", "-m", "init")
            return self.harnessctl("doctor", str(consumer), cwd=base)

    def assert_doctor_passes(self, autocrlf: str) -> None:
        doctor = self.fresh_consumer_doctor(autocrlf)
        self.assertEqual(0, doctor.returncode, doctor.stdout + doctor.stderr)
        self.assertNotIn("FAIL ", doctor.stdout)
        for check in HASH_BOUND_CHECKS:
            with self.subTest(autocrlf=autocrlf, check=check):
                lines = [line for line in doctor.stdout.splitlines() if f" {check}:" in line]
                self.assertEqual(1, len(lines), doctor.stdout)
                self.assertTrue(lines[0].startswith("PASS "), lines[0])

    def test_init_commit_doctor_exits_zero_on_an_lf_checkout(self) -> None:
        self.assert_doctor_passes("false")

    def test_init_commit_doctor_exits_zero_on_a_crlf_checkout(self) -> None:
        # Mirrors a Windows checkout: `core.autocrlf=true` converts every text file
        # the managed `.gitattributes` block does not pin.
        self.assert_doctor_passes("true")


if __name__ == "__main__":
    unittest.main()
