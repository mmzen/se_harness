from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

from se_harness import __version__


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TECHNICAL_COMMUNICATION_NOTE = REPOSITORY_ROOT / "docs/notes/technical-communication.md"
README_PATH = REPOSITORY_ROOT / "README.md"
PYPROJECT_PATH = REPOSITORY_ROOT / "pyproject.toml"


class PublicOnboardingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.project = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))["project"]

    def section(self, heading: str) -> str:
        marker = f"## {heading}\n"
        self.assertEqual(1, self.readme.count(marker), f"expected one {marker.strip()} section")
        remainder = self.readme.split(marker, 1)[1]
        return remainder.split("\n## ", 1)[0]

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

    def test_technical_communication_note_explains_use_and_claim_boundaries(self) -> None:
        note = TECHNICAL_COMMUNICATION_NOTE.read_text(encoding="utf-8")
        normalized = " ".join(note.split())
        index = (REPOSITORY_ROOT / "docs/notes/README.md").read_text(encoding="utf-8")
        self.assertIn("technical-communication.md", index)
        for phrase in (
            "Target expertise: 5/10",
            "based on ASD-STE100",
            "does not claim compliance",
            "operator-communication",
            "technical-artifact-writing",
            "harness-operator-brief",
            "harness-orient",
            "changes no repository path",
            "Human review remains necessary for meaning",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, normalized)

    def test_root_is_a_bounded_human_entry_point(self) -> None:
        self.assertLessEqual(len(self.readme.splitlines()), 200)
        headings = re.findall(r"(?m)^## (.+)$", self.readme)

        self.assertLessEqual(len(headings), 9)
        self.assertEqual(
            [
                "Who it is for",
                "Install or upgrade",
                "Start using it",
                "What this looks like in practice",
                "What you get",
                "Who does what",
                "Known limitations",
                "Learn more",
                "Developing SE Harness",
            ],
            headings,
        )
        self.assertIn("<!-- Target expertise: 6/10.", self.readme)
        self.assertIn("knowledge expected from the reader", self.readme)
        self.assertNotIn("> **Target expertise:", self.readme)

    def test_audience_section_is_specific_and_honest_about_assurance(self) -> None:
        audience = self.section("Who it is for")
        for phrase in (
            "<!-- Target expertise: 5/10. -->",
            "teams adopting coding agents",
            "audited, safety-sensitive, security-sensitive, or high-impact systems",
            "consistent engineering governance across repositories",
            "small teams and solo developers",
            "less suitable for throwaway code or rapid experiments",
            "strongest assurance comes from genuine role separation",
            "but not independent assurance",
            "does not by itself certify regulatory compliance",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, audience)

        for removed_heading in (
            "Engineering artifact model",
            "Command reference",
            "Installed repository layout",
            "Commit-bound verification and release lineage",
            "Pull-request enforcement and bootstrap",
            "Safe upgrades",
            "Distribution development",
        ):
            with self.subTest(removed_heading=removed_heading):
                self.assertNotIn(f"## {removed_heading}\n", self.readme)

    def test_installation_is_short_released_and_upgrade_aware(self) -> None:
        install = self.section("Install or upgrade")
        for text in (
            "Python 3.11 or later",
            "python -m venv .venv",
            "python -m pip install --upgrade pip",
            "python -m pip install se-harness",
            f'python -m pip install "se-harness=={self.project["version"]}"',
            "harnessctl --version",
            "does **not** update",
            "explicitly authorized transactional apply",
            "harness-installation-and-upgrades.md",
        ):
            with self.subTest(text=text):
                self.assertIn(text, install)
        self.assertNotIn("harnessctl upgrade", install)
        self.assertNotIn("python -m pip install .", install)
        self.assertEqual(self.project["version"], __version__)

    def test_start_exposes_only_the_human_repository_surface(self) -> None:
        start = self.section("Start using it")
        commands = (
            "harnessctl init C:\\path\\to\\new-repository --project-name my-project",
            "harnessctl adopt C:\\path\\to\\existing-repository --project-name my-project",
            "harnessctl doctor C:\\path\\to\\repository",
            "harnessctl validate C:\\path\\to\\repository",
            "harnessctl inspect C:\\path\\to\\repository",
            "harnessctl dashboard C:\\path\\to\\repository",
        )
        for command in commands:
            with self.subTest(command=command):
                self.assertIn(command, start)
        self.assertIn("checks installed-harness integrity", start)
        self.assertIn("checks the formal artifact graph", start)
        self.assertIn("summarizes current lifecycle attention", start)
        self.assertIn("generates the read-only Harness Explorer", start)
        self.assertIn("does not invent or approve product intent", start)
        self.assertIn("harness-orient", start)
        self.assertIn(".agents/skills/harness-orient/", start)
        self.assertIn("Codex discovers those canonical cores directly", start)
        self.assertIn(".claude/skills/", start)
        self.assertIn("thin adapters", start)
        self.assertIn("docs/notes/harness-orient.md", start)
        self.assertIn("without changing the repository", start)
        for skill in ("harness-draft-change", "harness-execute-work-order", "harness-prepare-assurance"):
            self.assertIn(skill, start)
        self.assertIn("complement `harnessctl`", start)
        self.assertIn("Phase 4 evaluator clients", start)
        self.assertIn("prohibit direct governed-target writes", start)
        self.assertIn("zero-effect stop", start)
        self.assertIn("docs/notes/agentic-execution-phase4-skills.md", start)
        self.assertIn("docs/notes/agentic-execution-skills-mvp.md", start)
        self.assertIn("docs/notes/agentic-execution-host-adapters.md", start)

    def test_phase4_skill_note_explains_capability_and_activation_boundaries(self) -> None:
        note = (
            REPOSITORY_ROOT / "docs/notes/agentic-execution-phase4-skills.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(note.split())
        index = (REPOSITORY_ROOT / "docs/notes/README.md").read_text(encoding="utf-8")
        for phrase in (
            "se-harness-skill-contract-v3",
            "direct_target_writes: false",
            "delegated-workflow execute",
            "delegated-workflow prepare-vrec",
            "No helper accepts a target-write callback",
            "Exact public 0.6.0 has no `delegated-workflow` command",
            "stop before any effect",
            "does not select a successor version",
            "independent assurance decision",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, normalized)
        self.assertIn("agentic-execution-phase4-skills.md", index)

    def test_fenced_harness_subcommands_use_the_exact_allowlist(self) -> None:
        fenced = "\n".join(re.findall(r"```[^\n]*\n(.*?)\n```", self.readme, flags=re.DOTALL))
        subcommands = set(re.findall(r"(?m)^harnessctl\s+([a-z][a-z-]*)\b", fenced))
        self.assertEqual(
            {"init", "adopt", "doctor", "validate", "focus", "check", "transition", "inspect", "dashboard"},
            subcommands,
        )
        for forbidden in (
            "preflight",
            "upgrade",
            "scaffold-domain",
            "create-artifact",
            "identity",
            "capture-verification",
            "prepare-release",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotRegex(fenced, rf"(?m)^harnessctl\s+{re.escape(forbidden)}\b")

    def test_practical_example_preserves_value_and_human_authority(self) -> None:
        practical = self.section("What this looks like in practice")
        for phrase in (
            "per-customer API rate limiting",
            "`429`",
            "`Retry-After`",
            "waits for approval",
            "implements only that scope",
            "retains evidence",
            "exact candidate commit",
            "assurance owner",
            "release owner",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), practical.lower())

        mermaid_blocks = re.findall(r"```mermaid\n(.*?)\n```", practical, flags=re.DOTALL)
        self.assertEqual(1, len(mermaid_blocks))
        graph = mermaid_blocks[0]
        node_ids = set(re.findall(r"\b([A-Z][A-Z0-9_]*)\s*[\[{]", graph))
        self.assertEqual(
            {"HUMAN", "DEF", "WORK", "AGENT", "CANDIDATE", "VERIFY", "RELEASE", "EXPLORER"},
            node_ids,
        )
        self.assertLessEqual(len(node_ids), 9)
        self.assertIn('VERIFY{"Human verification"}', graph)
        self.assertIn('RELEASE{"Human release decision"}', graph)
        self.assertIn('EXPLORER["Harness Explorer"] -. "traceability and anomalies" .-> DEF', graph)
        self.assertIn("classDef human", graph)
        self.assertIn("classDef explorer", graph)
        self.assertIn("When Mermaid is not rendered", practical)
        self.assertIn("Color is supplementary", practical)

    def test_practical_example_shows_stage_aware_handoffs(self) -> None:
        practical = self.section("What this looks like in practice")
        for phrase in (
            "Completed",
            "Current lifecycle state",
            "Recommended next step",
            "Human decision or approval required",
            "Command or suggested response",
            "Alternative next steps",
            "WO-RATE-001",
            "VREC-RATE-001",
            "state is unchanged",
            "failed",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, practical)

    def test_practical_example_uses_repository_owned_explorer_screenshots(self) -> None:
        practical = self.section("What this looks like in practice")
        expected_images = (
            "docs/images/harness-explorer-overview.png",
            "docs/images/harness-explorer-lineage.png",
            "docs/images/harness-explorer-readiness.png",
        )
        image_links = re.findall(r"!\[[^]]+\]\(([^)]+)\)", practical)
        self.assertEqual(list(expected_images), image_links)
        for target in expected_images:
            with self.subTest(target=target):
                self.assertFalse(Path(target).is_absolute())
                image_path = (REPOSITORY_ROOT / target).resolve()
                self.assertTrue(image_path.is_relative_to(REPOSITORY_ROOT.resolve()))
                self.assertTrue(image_path.is_file(), f"missing README image: {target}")
                self.assertEqual(b"\x89PNG\r\n\x1a\n", image_path.read_bytes()[:8])

        self.assertIn("derived, read-only views", practical)
        self.assertIn("without approving work, verifying a commit, or authorizing a release", practical)

    def test_value_and_responsibility_boundaries_remain_visible(self) -> None:
        value = self.section("What you get")
        for phrase in (
            "repository-native",
            "managed instruction route",
            "exact candidate commit",
            "safe adoption",
            "Harness Explorer",
            "portable read-only orientation skill",
            "never approves work",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, value)

        responsibility = self.section("Who does what")
        for phrase in (
            "Human owners",
            "Coding agent",
            "Repository policy and hosting controls",
            "run preflight",
            "never commit, push, approve, verify, release, tag, publish, or deploy",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, responsibility)

    def test_known_limitations_remain_explicit_and_current(self) -> None:
        limitations = self.section("Known limitations")
        normalized = " ".join(limitations.split())
        self.assertIn("exact `QG-*` IDs", normalized)
        self.assertIn("derived readiness groupings", normalized)
        self.assertIn("not gate results", normalized)
        self.assertIn("harness-operational-phasing.md", limitations)
        self.assertNotIn("non-empty work-order `architecture` relation", limitations)
        self.assertNotIn("validator still requires", limitations)

    def test_deeper_user_and_contributor_routes_are_discoverable(self) -> None:
        learning = self.section("Learn more")
        development = self.section("Developing SE Harness")
        self.assertIn("harness-overview.md", learning)
        self.assertIn("[overview](docs/notes/harness-overview.md)", learning)
        self.assertNotIn("[4/10 overview]", learning)
        self.assertIn("docs/notes/README.md", learning)
        self.assertIn("ENGINEERING_HARNESS.md", learning)
        self.assertIn("developing-se-harness.md", development)
        self.assertIn("candidate development evidence", development)
        self.assertNotIn("python -m pip install -e .", development)

    def test_internal_documentation_links_are_repository_relative(self) -> None:
        for target in (
            "docs/notes/harness-installation-and-upgrades.md",
            "docs/notes/harness-orient.md",
            "docs/notes/agentic-execution-skills-mvp.md",
            "docs/notes/harness-operational-phasing.md",
            "docs/notes/harness-overview.md",
            "docs/notes/README.md",
            "docs/notes/developing-se-harness.md",
        ):
            with self.subTest(target=target):
                self.assertIn(f"]({target})", self.readme)
        self.assertNotIn("https://github.com/mmzen/se_harness/blob/main/", self.readme)

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


if __name__ == "__main__":
    unittest.main()


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
            git = ["git", "-c", f"core.autocrlf={autocrlf}", "-C", str(consumer)]
            subprocess.run([*git, "init", "-q", "-b", "main"], check=True, capture_output=True)
            subprocess.run([*git, "config", "user.email", "adopter@example.invalid"], check=True)
            subprocess.run([*git, "config", "user.name", "adopter"], check=True)
            subprocess.run([*git, "config", "commit.gpgsign", "false"], check=True)
            subprocess.run([*git, "add", "-A"], check=True, capture_output=True)
            subprocess.run([*git, "commit", "-q", "-m", "init"], check=True, capture_output=True)
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
