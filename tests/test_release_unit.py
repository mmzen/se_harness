"""Evidence for REQ-CIP-004 (WO-CIP-004): the release unit is a candidate commit with a measured census."""

from __future__ import annotations

import contextlib
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness import release_unit
from se_harness.cli import main
from se_harness.installer import HarnessError

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/templates/RELEASE_CONTRACT.template.md"


def _git(root: Path, *arguments: str) -> str:
    return subprocess.run(["git", "-C", str(root), *arguments], capture_output=True, text=True, check=True).stdout.strip()


class _History:
    """A tagged first-parent history with forge-style merges (no trailer on the merge itself)."""

    def __init__(self, root: Path) -> None:
        self.root = root
        _git(root, "init", "-q", "-b", "main")
        _git(root, "config", "user.email", "t@example.invalid")
        _git(root, "config", "user.name", "t")
        _git(root, "config", "commit.gpgsign", "false")
        self.commit("base", trailer=None)
        _git(root, "tag", "v1")

    def commit(self, name: str, *, trailer: str | None) -> str:
        (self.root / f"{name}.txt").write_text(name, encoding="utf-8")
        _git(self.root, "add", "-A")
        message = f"{name}\n\n" + (f"Harness-Work-Order: {trailer}\n" if trailer else "")
        _git(self.root, "commit", "-q", "-m", message)
        return _git(self.root, "rev-parse", "HEAD")

    def merge(self, branch: str, commits: list[tuple[str, str | None]]) -> str:
        _git(self.root, "checkout", "-q", "-b", branch)
        for name, trailer in commits:
            self.commit(name, trailer=trailer)
        _git(self.root, "checkout", "-q", "main")
        _git(self.root, "merge", "-q", "--no-ff", "--no-edit", "-m", f"Merge pull request from {branch}", branch)
        return _git(self.root, "rev-parse", "HEAD")


STATUSES = {"WO-X-001": ("implemented", True), "WO-X-002": ("implemented", False), "WO-X-003": ("in_progress", True)}


def lookup(work_order: str) -> tuple[str | None, bool | None]:
    return STATUSES.get(work_order, (None, None))


class ReleaseUnitDerivationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.history = _History(Path(self.temporary.name))

    def test_census_reads_merged_trailers_lists_untraced_and_fails_closed(self) -> None:
        h = self.history
        m1 = h.merge("one", [("a1", "WO-X-001"), ("a2", "WO-X-001")])
        m2 = h.merge("two", [("b1", "WO-X-002"), ("b2", "WO-X-001")])
        untraced = h.merge("docs", [("d1", None)])
        direct = h.commit("direct", trailer="WO-X-003")
        unit = release_unit.derive_release_unit(h.root, from_ref="v1", to_ref="HEAD", lookup=lookup)
        self.assertEqual(("WO-X-001", "WO-X-002", "WO-X-003"), unit.gates)
        by_id = {entry.id: entry for entry in unit.work_orders}
        self.assertEqual((m1, m2), by_id["WO-X-001"].commits)
        self.assertEqual((m2,), by_id["WO-X-002"].commits)
        self.assertEqual((direct,), by_id["WO-X-003"].commits)
        self.assertEqual(("implemented", True), (by_id["WO-X-001"].status, by_id["WO-X-001"].packaged_surface))
        self.assertEqual(("in_progress", True), (by_id["WO-X-003"].status, by_id["WO-X-003"].packaged_surface))
        self.assertEqual((untraced,), unit.untraced)
        self.assertFalse(unit.complete)
        self.assertEqual(2, len(unit.reasons))
        self.assertIn("WO-X-003 is in_progress, not implemented", unit.reasons)
        self.assertTrue(any("no Harness-Work-Order trailer" in reason for reason in unit.reasons))
        self.assertEqual('gates = ["WO-X-001", "WO-X-002", "WO-X-003"]\n', release_unit.render_gates_toml(unit))

    def test_exemption_names_a_full_commit_and_a_later_merge_does_not_move_the_unit(self) -> None:
        h = self.history
        h.merge("one", [("a1", "WO-X-001")])
        untraced = h.merge("docs", [("d1", None)])
        candidate = _git(h.root, "rev-parse", "HEAD")
        with self.assertRaisesRegex(HarnessError, "full commit id"):
            release_unit.derive_release_unit(h.root, from_ref="v1", to_ref=candidate, exempt=["abc"], lookup=lookup)
        unit = release_unit.derive_release_unit(h.root, from_ref="v1", to_ref=candidate, exempt=[untraced], lookup=lookup)
        self.assertTrue(unit.complete)
        self.assertEqual((untraced,), unit.exempted)
        # ordinary development continues on main; the unit named by the candidate commit is unchanged
        h.merge("later", [("z1", "WO-X-003")])
        again = release_unit.derive_release_unit(h.root, from_ref="v1", to_ref=candidate, exempt=[untraced], lookup=lookup)
        self.assertEqual(unit.gates, again.gates)
        self.assertEqual(candidate, again.to_commit)

    def test_contract_comparison_reports_e_cip_001_on_every_difference(self) -> None:
        h = self.history
        h.merge("one", [("a1", "WO-X-001")])
        candidate = _git(h.root, "rev-parse", "HEAD")
        unit = release_unit.derive_release_unit(h.root, from_ref="v1", to_ref=candidate, lookup=lookup)
        exact = {"candidate_commit": candidate, "previous_release_tag": "v1", "relations": {"gates": ["WO-X-001", "VER-X-001"]}}
        self.assertEqual([], release_unit.compare_with_contract(unit, exact))
        wrong = {"candidate_commit": "0" * 40, "previous_release_tag": "v0", "relations": {"gates": ["WO-X-002"]}}
        findings = release_unit.compare_with_contract(unit, wrong)
        self.assertEqual(3, len(findings))
        self.assertTrue(all(item.startswith("E-CIP-001") for item in findings))
        self.assertIn("missing from gates: WO-X-001; not in the derivation: WO-X-002", findings[2])

    def test_cli_is_registered_and_the_template_names_the_unit(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaises(SystemExit):
            main(["release-unit", "--help"])
        text = output.getvalue()
        for option in ("--from", "--to", "--exempt", "--contract", "--json", "--toml"):
            self.assertIn(option, text)
        template = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn('candidate_commit = "<full commit id, 40 or 64 hex>"', template)
        self.assertIn('previous_release_tag = "v<version>"', template)
        self.assertIn("harnessctl release-unit", template)
        self.assertIn("E-CIP-001", template)
        self.assertIn("A merge to `main` after the cut changes nothing about this unit.", template)

    def test_cli_derives_against_the_repository_catalog(self) -> None:
        # the command's own catalog lookup, on a fixture history, with the catalog stubbed
        h = self.history
        h.merge("one", [("a1", "WO-X-001")])

        class _Artifact:
            def __init__(self, metadata):
                self.metadata = metadata

        catalog = {
            "WO-X-001": _Artifact({"type": "work_order", "status": "implemented", "execution_scope": {"paths": ["se_harness/x.py"]}}),
            "REL-X-001": _Artifact({"type": "release_contract", "candidate_commit": _git(h.root, "rev-parse", "HEAD"), "previous_release_tag": "v1", "relations": {"gates": ["WO-X-001"]}}),
        }
        with (
            mock.patch("se_harness.workflow._validation", return_value=(None, None)),
            mock.patch("se_harness.workflow._catalog", return_value=catalog),
        ):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(["release-unit", str(h.root), "--from", "v1", "--to", "HEAD", "--contract", "REL-X-001"])
            self.assertEqual(0, code, output.getvalue())
            self.assertIn("Release unit: COMPLETE", output.getvalue())
            self.assertIn("WO-X-001: implemented; packaged; 1 commit(s)", output.getvalue())
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(["release-unit", str(h.root), "--from", "v1", "--to", "HEAD", "--toml"])
            self.assertEqual(0, code)
            self.assertEqual('gates = ["WO-X-001"]\n', output.getvalue())


if __name__ == "__main__":
    unittest.main()
