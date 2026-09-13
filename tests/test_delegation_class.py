"""Local delegation uses the existing approval and selected local checks."""
from __future__ import annotations
import json, re, tempfile, unittest
from pathlib import Path
from unittest import mock
from se_harness.gate_source import DELEGATED_ROLE
from tests.fixture_support import standard_repository
from tests.mutation_guard_support import patch_mutation_authority
from tests.artifact_support import create_base_chain, write
from tests.cli_support import invoke
from tests.git_support import git

ASSURANCE_AND_SCOPE = """[assurance]
commit_bound_verification = "required"
rationale = "The executable fixture requires exact-candidate assurance."
decided_by = "engineering-owner"

[execution_scope]
paths = ["src/"]

[relations]"""

class DelegationFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root)
        create_base_chain(self.root, work_order_status="approved", operating_contract_status="draft")
        # Preflight requires a domain-segmented id (WO-XXX-NNN); the base chain writes WO-001.
        original = self.root / "docs/engineering/product/work-orders/WO-001.md"
        self.work_order = self.root / "docs/engineering/product/work-orders/WO-PRD-001.md"
        self.work_order.write_text(original.read_text(encoding="utf-8").replace('id = "WO-001"', 'id = "WO-PRD-001"', 1), encoding="utf-8")
        original.unlink()
        for artifact in (self.root / "docs/engineering/product").rglob("*.md"):
            content = artifact.read_text(encoding="utf-8")
            if "WO-001" in content:
                artifact.write_text(content.replace("WO-001", "WO-PRD-001"), encoding="utf-8")
        text = self.work_order.read_text(encoding="utf-8")
        if "[assurance]" not in text:
            self.work_order.write_text(text.replace("[relations]", ASSURANCE_AND_SCOPE, 1), encoding="utf-8")
        patch_mutation_authority(self)



    def commit(self, message: str) -> str:
        if not (self.root / ".git").exists():
            git(self.root, "init", "-q", "-b", "main")
            git(self.root, "config", "user.email", "fixture@example.invalid")
            git(self.root, "config", "user.name", "Fixture")
            git(self.root, "config", "core.autocrlf", "false")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-q", "--allow-empty", "-m", message)
        return git(self.root, "rev-parse", "HEAD")

    def branch(self, name: str = "wo/001") -> None:
        git(self.root, "checkout", "-q", "-b", name)


    def transition(self, target: str, actor: str = DELEGATED_ROLE, *, apply: bool = True) -> tuple[int, dict, str]:
        arguments = ["transition", str(self.root), "--set", f"WO-PRD-001={target}", "--decision", f"WO-PRD-001={actor}", "--json"]
        if apply:
            arguments.append("--apply")
        code, out, err = invoke(*arguments)
        return code, json.loads(out) if out.strip().startswith("{") else {}, err

    def status(self) -> str:
        return re.search(r'(?m)^status = "([a-z_]+)"$', self.work_order.read_text(encoding="utf-8")).group(1)

    def blockers(self, result: dict, err: str) -> str:
        return " ".join(result.get("restitution", {}).get("blocked_by", [])) + err


    def approve_delegation(self) -> None:
        text = self.work_order.read_text(encoding="utf-8").replace('status = "approved"', 'status = "draft"', 1)
        text = text.replace("[relations]", '[delegation]\nclass = "execution"\n\n[relations]', 1)
        self.work_order.write_text(text, encoding="utf-8")
        code, result, err = self.transition("approved", "engineering-owner")
        self.assertEqual(0, code, self.blockers(result, err))


class LocalDelegationTests(DelegationFixture):
    def test_owner_approval_on_local_branch_starts_without_ci_or_base_merge(self):
        self.commit("initial"); self.branch()
        self.approve_delegation()
        with mock.patch("urllib.request.urlopen", side_effect=AssertionError("network was contacted")):
            code, result, err = self.transition("in_progress")
        self.assertEqual(0, code, self.blockers(result, err))
        self.assertEqual("in_progress", self.status())
        self.assertIn("recorded engineering-owner approval", self.work_order.read_text())

    def test_class_label_without_owner_approval_is_refused(self):
        text=self.work_order.read_text().replace("[relations]", '[delegation]\nclass = "execution"\n\n[relations]',1)
        self.work_order.write_text(text)
        code,result,err=self.transition("in_progress")
        self.assertNotEqual(0,code)
        self.assertIn("approval",self.blockers(result,err))
        self.assertEqual("approved",self.status())

    def test_changed_scope_needs_owner_approval(self):
        self.approve_delegation()
        self.work_order.write_text(self.work_order.read_text().replace('paths = ["src/"]','paths = ["src/", "outside/"]',1))
        code,result,err=self.transition("in_progress")
        self.assertNotEqual(0,code)
        self.assertIn("scope changed",self.blockers(result,err))

    def test_legacy_approval_can_be_read_from_local_git_history(self):
        self.approve_delegation()
        text=re.sub(r'(?m)^(scope_paths|delegation_class) = .*\n','',self.work_order.read_text())
        self.work_order.write_text(text)
        self.commit("local owner approval")
        code,result,err=self.transition("in_progress")
        self.assertEqual(0,code,self.blockers(result,err))

    def test_failed_local_completion_gate_still_blocks(self):
        self.approve_delegation()
        code,result,err=self.transition("in_progress")
        self.assertEqual(0,code,self.blockers(result,err))
        code,result,err=self.transition("implemented")
        self.assertNotEqual(0,code)
        self.assertEqual("in_progress",self.status())

    def test_approval_and_assurance_remain_owner_decisions(self):
        from se_harness.gate_source import authorize_delegated_right, DelegationError
        for right in ("DR-WO-APPROVE", "DR-VREC-DECIDE", "DR-RLS-DECIDE"):
            with self.subTest(right=right), self.assertRaises(DelegationError):
                authorize_delegated_right(self.root, work_order_metadata={},work_order_path=self.work_order,right=right)

    def test_projection_offers_local_delegated_start(self):
        self.approve_delegation()
        code,out,err=invoke("check",str(self.root),"--artifact","WO-PRD-001","--json")
        self.assertEqual(0,code,err)
        result=json.loads(out)
        self.assertEqual(DELEGATED_ROLE,result["restitution"]["decision_required"]["role"])
        self.assertEqual("command",result["restitution"]["command_or_response"]["kind"])
