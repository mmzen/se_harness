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


class ApprovalPredicateTests(unittest.TestCase):
    """WO-CIP-005: QGP-G5P-RELEASE-UNIT refuses a contract whose census differs from the derivation."""

    def setUp(self) -> None:
        from tests.fixture_support import standard_repository
        from tests.mutation_guard_support import trusted_mutation_authority
        from tests.test_revision_provenance import create_additional_chain, create_base_chain

        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root, "Release Unit Fixture")
        guard = mock.patch("se_harness.mutation_guard.require_mutation_authority", side_effect=trusted_mutation_authority)
        guard.start()
        self.addCleanup(guard.stop)
        create_base_chain(self.root, operating_contract_status="draft")
        create_additional_chain(self.root)  # WO-002 exists in the catalog but no commit carries its trailer
        (self.root / "docs/engineering/product/release/REL-001.md").unlink()
        _git(self.root, "init", "-q", "-b", "main")
        _git(self.root, "config", "user.email", "t@example.invalid")
        _git(self.root, "config", "user.name", "t")
        _git(self.root, "config", "commit.gpgsign", "false")
        _git(self.root, "add", "-A")
        _git(self.root, "commit", "-q", "-m", "base")
        _git(self.root, "tag", "v1")
        (self.root / "feature.txt").write_text("done", encoding="utf-8")
        _git(self.root, "add", "-A")
        _git(self.root, "commit", "-q", "-m", "feature\n\nHarness-Work-Order: WO-001\n")
        self.candidate = _git(self.root, "rev-parse", "HEAD")

    def contract(self, *, gates: list[str], candidate: bool = True, exemptions: list[str] | None = None) -> None:
        front = [
            '+++', 'id = "REL-001"', 'type = "release_contract"', 'title = "Release one"', 'status = "draft"',
            'owners = ["release-owner"]', 'created = "2026-08-26"', 'updated = "2026-08-26"',
        ]
        if candidate:
            front += [f'candidate_commit = "{self.candidate}"', 'previous_release_tag = "v1"']
        if exemptions is not None:
            front += ['[release_unit]', 'untraced_exemptions = [' + ', '.join(f'"{e}"' for e in exemptions) + ']']
        front += ['[relations]', 'gates = [' + ', '.join(f'"{g}"' for g in gates) + ']', '+++', '', '# Release Contract: Release one', '']
        (self.root / "docs/engineering/product/release/REL-001.md").write_text("\n".join(front), encoding="utf-8")

    def approve(self) -> tuple[int, str]:
        output, error = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(["transition", str(self.root), "--set", "REL-001=approved", "--decision", "REL-001=release-owner", "--apply"])
        return code, output.getvalue() + error.getvalue()

    def test_a_differing_census_is_refused_and_a_matching_one_is_approved(self) -> None:
        self.contract(gates=["WO-001", "WO-002"])
        code, message = self.approve()
        self.assertEqual(1, code)
        self.assertIn("QGP-G5P-RELEASE-UNIT", message)
        self.assertIn("E-CIP-001", message)
        self.assertIn("not in the derivation: WO-002", message)
        self.assertIn('status = "draft"', (self.root / "docs/engineering/product/release/REL-001.md").read_text(encoding="utf-8"))
        self.contract(gates=["WO-001"])
        code, message = self.approve()
        self.assertEqual(0, code, message)
        self.assertIn('status = "approved"', (self.root / "docs/engineering/product/release/REL-001.md").read_text(encoding="utf-8"))

    def test_the_allow_list_form_is_not_measured(self) -> None:
        self.contract(gates=["WO-001", "WO-002"], candidate=False)
        code, message = self.approve()
        self.assertEqual(0, code, message)

    def test_an_untraced_commit_needs_an_exemption(self) -> None:
        (self.root / "note.txt").write_text("untraced", encoding="utf-8")
        _git(self.root, "add", "-A")
        _git(self.root, "commit", "-q", "-m", "no trailer")
        self.candidate = _git(self.root, "rev-parse", "HEAD")
        untraced = self.candidate
        self.contract(gates=["WO-001"])
        code, message = self.approve()
        self.assertEqual(1, code)
        self.assertIn("carry no Harness-Work-Order trailer", message)
        self.contract(gates=["WO-001"], exemptions=[untraced])
        code, message = self.approve()
        self.assertEqual(0, code, message)

    def test_evaluator_is_in_the_contract_inventory(self) -> None:
        from se_harness.workflow_contract import EVALUATORS, load_validated_contracts

        self.assertIn("release_unit_ready", EVALUATORS)
        _, _, _, _, gates = load_validated_contracts()
        self.assertIn("QGP-G5P-RELEASE-UNIT", [p["id"] for p in gates["QG-G5-RELEASE-PREPARATION"]["predicates"]])


if __name__ == "__main__":
    unittest.main()
