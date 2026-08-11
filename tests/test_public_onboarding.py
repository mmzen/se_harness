from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path

from se_harness import __version__


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
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

    def test_pypi_installation_is_primary_and_environment_scoped(self) -> None:
        install = self.section("Install from PyPI")
        required = (
            "Python 3.11 or later",
            "python -m venv .venv",
            ".\\.venv\\Scripts\\Activate.ps1",
            "python -m pip install --upgrade pip",
            "python -m pip install se-harness",
            f'python -m pip install "se-harness=={self.project["version"]}"',
            ".\\.venv\\Scripts\\harnessctl.exe --version",
            "source .venv/bin/activate",
            ".venv/bin/harnessctl --version",
            "python -m se_harness --version",
        )
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, install)
        self.assertNotIn("python -m pip install .", install)
        self.assertNotIn("python -m pip install -e .", install)
        self.assertNotRegex(install, r"(?m)^py(?:\.exe)?\s+-3")
        self.assertIn("virtual environment", install.lower())
        self.assertIn("does not move", install.lower())
        self.assertEqual(self.project["version"], __version__)

    def test_quick_start_covers_new_and_existing_repositories(self) -> None:
        quick_start = self.section("Quick start")
        for command in (
            "harnessctl init C:\\path\\to\\new-repository --project-name my-project",
            "harnessctl adopt C:\\path\\to\\existing-repository --project-name my-project",
            "harnessctl doctor C:\\path\\to\\repository",
            "harnessctl dashboard C:\\path\\to\\repository",
        ):
            with self.subTest(command=command):
                self.assertIn(command, quick_start)
        self.assertIn("REPOSITORY_CONTEXT.md", quick_start)
        self.assertIn("does not approve", quick_start)

    def test_feature_summary_surfaces_recently_implemented_controls(self) -> None:
        features = self.section("What it provides")
        for phrase in (
            "PyPI",
            "AGENTS.md",
            "ENGINEERING_HARNESS.md",
            "approved -> in_progress -> implemented",
            "aggregate",
            "superseded",
            "OIDC",
            "attestations",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, features)

    def test_practical_example_keeps_agent_mechanics_and_human_authority_distinct(self) -> None:
        practical = self.section("What this looks like in practice")
        headings = (
            self.readme.index("## Quick start\n"),
            self.readme.index("## What this looks like in practice\n"),
            self.readme.index("## What it provides\n"),
        )
        self.assertEqual(tuple(sorted(headings)), headings)

        for phrase in (
            "per-customer API rate limiting",
            "`429`",
            "`Retry-After`",
            "review before implementation",
            "approved scope",
            "clean candidate",
            "exact commit",
            "human assurance",
            "separate human decision",
            "pull-request CI",
            "visible anomalies",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), practical.lower())

        quoted_requests = "\n".join(
            line for line in practical.splitlines() if line.startswith(">")
        )
        for operation in (
            "doctor",
            "preflight",
            "validate",
            "dashboard",
            "capture-verification",
        ):
            with self.subTest(operation=operation):
                self.assertIn(f"`{operation}`", practical)
                self.assertNotIn(operation, quoted_requests)

    def test_practical_graph_has_semantic_styles_decisions_and_text_fallback(self) -> None:
        practical = self.section("What this looks like in practice")
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)\n```", practical, flags=re.DOTALL)
        self.assertEqual(1, len(mermaid_blocks))
        graph = mermaid_blocks[0]

        for node in (
            'USER["Your approved outcome"]',
            'INT["Intent"]',
            'CAP["Capability"]',
            'REQ["Requirement"]',
            'SPEC["Specification"]',
            'ARCH["Architecture"]',
            'ADR{"Architecture decision"}',
            'VER["Verification contract"]',
            'WO["Approved work order"]',
            'CHANGE["Agent implementation"]',
            'EVIDENCE["Tests and evidence"]',
            'COMMIT["Exact candidate commit"]',
            'READY["Ready verification record"]',
            'ASSURANCE{"Human assurance decision"}',
            'VREC["Verified record"]',
            'RELEASE{"Human release decision"}',
            'RLS["Released revision"]',
            'EXPLORER["Harness Explorer"]',
        ):
            with self.subTest(node=node):
                self.assertIn(node, graph)

        for relation in (
            'USER["Your approved outcome"] --> INT["Intent"]',
            "INT --> CAP",
            "CAP --> REQ",
            "WO --> CHANGE",
            "CHANGE --> EVIDENCE",
            "EVIDENCE --> COMMIT",
            "READY --> ASSURANCE",
            "ASSURANCE --> VREC",
            "VREC --> RELEASE",
            "RELEASE --> RLS",
            'EXPLORER["Harness Explorer"] -. "traceability and anomalies" .-> REQ',
        ):
            with self.subTest(relation=relation):
                self.assertIn(relation, graph)

        for style in (
            "human",
            "intent",
            "design",
            "work",
            "execution",
            "evidence",
            "provenance",
            "verified",
            "release",
            "explorer",
        ):
            with self.subTest(style=style):
                self.assertRegex(graph, rf"(?m)^\s*classDef {style} ")
        self.assertIn("class USER,ASSURANCE,RELEASE human", graph)
        self.assertIn("class INT,CAP,REQ intent", graph)
        self.assertIn("class VREC verified", graph)
        self.assertIn("class RLS release", graph)

        self.assertNotIn("![", practical)
        self.assertNotRegex(practical, r"(?i)<(?:script|style)\b")
        self.assertIn("When Mermaid is not rendered", practical)
        self.assertIn("labels, shapes, and prose", practical)

    def test_package_and_repository_upgrades_are_separate(self) -> None:
        upgrade = self.section("Safe upgrades")
        commands = (
            "python -m pip install --upgrade se-harness",
            "harnessctl upgrade C:\\path\\to\\repository",
            "harnessctl upgrade C:\\path\\to\\repository --apply",
            "harnessctl doctor C:\\path\\to\\repository",
        )
        positions = [upgrade.index(command) for command in commands]
        self.assertEqual(sorted(positions), positions)
        self.assertIn("does not modify an initialized or adopted repository", upgrade)
        self.assertIn("read-only", upgrade)
        self.assertIn("transactional", upgrade)

    def test_source_installation_is_development_only(self) -> None:
        development = self.section("Distribution development")
        self.assertIn("python -m pip install .", development)
        self.assertIn("python -m pip install -e .", development)
        self.assertIn("unreleased", development)
        self.assertIn("python -m unittest discover", development)

    def test_release_links_and_baseline_language_remain_truthful(self) -> None:
        for url in (
            "https://pypi.org/project/se-harness/",
            "https://github.com/mmzen/se_harness",
            "https://github.com/mmzen/se_harness/issues",
            "https://github.com/mmzen/se_harness/releases",
        ):
            with self.subTest(url=url):
                self.assertIn(url, self.readme)
        baseline = self.section("Pull-request enforcement and bootstrap")
        self.assertIn("exact configured released baseline", baseline)
        self.assertIn(".github/workflows/engineering-harness.yml", baseline)
        self.assertNotRegex(baseline, r"se-harness==\d+\.\d+\.\d+")
        self.assertIn("OIDC", self.readme)
        self.assertIn("without rebuilding", self.readme)
        self.assertIn("attestations", self.readme)

    def test_public_markdown_has_no_placeholders_mojibake_or_missing_local_links(self) -> None:
        for marker in ("PENDING_", "TODO", "FIXME", "\ufffd", "\u00c3", "\u00e2\u20ac"):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, self.readme)
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", self.readme):
            if re.match(r"(?:https?://|mailto:|#)", target):
                continue
            local_path = (REPOSITORY_ROOT / target.split("#", 1)[0]).resolve()
            with self.subTest(target=target):
                self.assertTrue(local_path.is_file(), f"missing local README link: {target}")


if __name__ == "__main__":
    unittest.main()
