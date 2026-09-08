"""Evidence for REQ-RSK-010 to REQ-RSK-013 and REQ-RSK-015 (WO-RSK-010): the risk artifact and its borrowed stop.

Each case names the SPEC-RSK-010 rules it covers (RSK-MGT-036). Expected values
are the contract's, computed by hand in the case, never read back from the
candidate (VER-RSK-010).
"""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness.artifact_layout import ARTIFACT_DIRECTORIES, ARTIFACT_PREFIXES
from se_harness.cli import build_parser, main
from se_harness.engine import validate_engineering_artifacts
from se_harness.risks import MEASUREMENT, OPTION_TARGETS, RISK_OPTIONS, compute_score
from se_harness.workflow import LIFECYCLE_REGISTRY
from tests.mutation_guard_support import patch_mutation_authority
from tests.artifact_support import create_base_chain, formal, write
from tests.cli_support import invoke
from tests.git_support import git
from tests.fixture_support import standard_repository

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering"
PACKAGE = REPOSITORY_ROOT / "se_harness"
#: RSK-MGT-014: the predicate identifiers of `main`'s quality-gates contract, 43 of them since
#: WO-ECP-030 removed the unreachable QG-G0-INTENT gate; the risk family adds none.
MAIN_PREDICATES = frozenset({
    "QGP-G1-AUTHORING", "QGP-G1-DECISION", "QGP-G1-GRAPH", "QGP-G1-INTEGRITY",
    "QGP-G2-AUTHORING", "QGP-G2-DECISION", "QGP-G2-GRAPH", "QGP-G2-INTEGRITY", "QGP-G3-DECISION", "QGP-G3-GRAPH",
    "QGP-G3-INTEGRITY", "QGP-G3-PREFLIGHT", "QGP-G3-SCOPE", "QGP-G3-STATUS", "QGP-G4A-DECISION", "QGP-G4A-GRAPH",
    "QGP-G4A-INTEGRITY", "QGP-G4C-GRAPH", "QGP-G4C-INTEGRITY", "QGP-G4C-STATUS", "QGP-G4I-COMPLETE", "QGP-G4I-DECISION",
    "QGP-G4I-EVIDENCE", "QGP-G4I-GRAPH", "QGP-G4I-INTEGRITY", "QGP-G4I-PATHS", "QGP-G4I-PREFLIGHT", "QGP-G4I-SCOPE",
    "QGP-G4I-STATUS", "QGP-G4V-DECISION", "QGP-G4V-GRAPH", "QGP-G4V-INTEGRITY", "QGP-G5D-DECISION", "QGP-G5D-GRAPH",
    "QGP-G5D-INTEGRITY", "QGP-G5D-STATUS", "QGP-G5E-GRAPH", "QGP-G5E-INTEGRITY", "QGP-G5E-STATUS", "QGP-G5P-DECISION",
    "QGP-G5P-GRAPH", "QGP-G5P-INTEGRITY", "QGP-G5P-RELEASE-UNIT",
})
#: The state model of SPEC-RSK-010, by hand.
RISK_EDGES = {
    "identified": {"raised", "withdrawn"},
    "raised": {"accepted", "avoided", "mitigating", "withdrawn"},
    "mitigating": {"mitigated", "withdrawn"},
    "accepted": set(),
    "avoided": set(),
    "mitigated": set(),
    "withdrawn": set(),
}
RISK_PATH = "docs/engineering/product/risks/RISK-PRD-001.md"
DECISION_PATH = "docs/engineering/product/decisions/DEC-PRD-001.md"


def _subcommands() -> set[str]:
    action = next(a for a in build_parser()._actions if getattr(a, "choices", None) and "preflight" in a.choices)
    return set(action.choices)


def risk_text(
    risk_id: str = "RISK-PRD-001",
    *,
    status: str = "raised",
    likelihood: object = 3,
    impact: object = 4,
    score: object = 12,
    threatens: tuple[str, ...] = ("WO-001",),
    drop: tuple[str, ...] = (),
    extra: str = "",
    relations_extra: dict[str, list[str]] | None = None,
) -> str:
    """A hand-written risk; `drop` removes fields, `extra` appends front-matter lines."""

    scalars = {
        "stage": 'stage = "release"',
        "category": 'category = "process"',
        "cause": 'cause = "A consumer pins the harness and never upgrades."',
        "effect": 'effect = "The consumer keeps writing keys the evaluator no longer reads."',
        "likelihood": f"likelihood = {likelihood}",
        "impact": f"impact = {impact}",
        "score": f"score = {score}",
        "raised_by": 'raised_by = "implementation-agent"',
    }
    lines = [line for name, line in scalars.items() if name not in drop]
    if extra:
        lines.append(extra)
    relations = {"threatens": list(threatens), **(relations_extra or {})}
    return formal(risk_id, "risk", status, relations, "\n".join(lines))


def pairing_decision_text(decision_id: str = "DEC-PRD-001", *, risk_id: str = "RISK-PRD-001", blocks: tuple[str, ...] = ("WO-001",), status: str = "open") -> str:
    scalars = [
        'kind = "question"',
        'question = "How is the threat answered: accept, avoid or mitigate?"',
        'raised_by = "implementation-agent"',
        'recommendation = "mitigate"',
    ]
    tables = "\n\n".join(f'[[options]]\nid = "{option_id}"\nlabel = "{label}"' for option_id, label in RISK_OPTIONS)
    return formal(decision_id, "decision", status, {"concerns": [risk_id, *blocks], "blocks": list(blocks)}, "\n".join(scalars) + "\n\n" + tables)


class RiskFixture(unittest.TestCase):
    RAISE = (
        "--domain", "product", "--title", "Config drift", "--stage", "release", "--category", "process",
        "--cause", "A consumer pins the harness and never upgrades.",
        "--effect", "The consumer keeps writing keys the evaluator no longer reads.",
        "--threatens", "WO-001", "--raised-by", "implementation-agent",
    )

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root)
        lock_path = self.root / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["evaluator"]["archive_name"] = f"se_harness-{lock['tool_version'].replace('-', '_')}-py3-none-any.whl"
        lock["evaluator"]["archive_sha256"] = "a" * 64
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        patch_mutation_authority(self)
        create_base_chain(self.root, operating_contract_status="draft")

    def in_progress_work_order(self, *scope: str) -> Path:
        path = self.root / "docs/engineering/product/work-orders/WO-001.md"
        text = path.read_text(encoding="utf-8").replace('status = "implemented"', 'status = "in_progress"', 1)
        paths = ", ".join(json.dumps(item) for item in (scope or ("src/",)))
        text = text.replace(
            "[relations]",
            '[assurance]\ncommit_bound_verification = "required"\nrationale = "Risk fixture."\n'
            f'decided_by = "repository-owner"\n\n[execution_scope]\npaths = [{paths}]\n\n[relations]',
            1,
        )
        path.write_text(text, encoding="utf-8")
        return path

    def raise_risk(self, *extra: str, likelihood: str = "3", impact: str = "4", risk_id: str = "RISK-PRD-001", decision_id: str | None = "DEC-PRD-001") -> tuple[int, str, str]:
        arguments = ["raise-risk", str(self.root), *self.RAISE, "--likelihood", likelihood, "--impact", impact, "--id", risk_id]
        if decision_id is not None:
            arguments += ["--with-decision", "--decision-id", decision_id]
        return invoke(*arguments, *extra)

    def validate(self):
        return validate_engineering_artifacts.validate_repository(self.root)

    def codes(self, prefix: str = "E-RSK") -> list[str]:
        return sorted(f"{item.code}: {item.message}" for item in self.validate().errors if item.code.startswith(prefix))

    def handoff_check(self, *changed: str) -> dict:
        arguments = ["check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff"]
        for path in changed or ("src/main.py",):
            arguments += ["--changed-path", path]
        code, output, error = invoke(*arguments, "--changes-complete", "--json")
        self.assertIn(code, (0, 1), error)
        return json.loads(output)

    @staticmethod
    def predicates(result: dict) -> dict:
        return {p["id"]: p for gate in result["compliance"]["gates"] for p in gate["predicates"]}

    def risk_file(self) -> Path:
        return self.root / RISK_PATH

    def decision_file(self) -> Path:
        return self.root / DECISION_PATH

    def decide(self, *extra: str, decision_id: str = "DEC-PRD-001", actor: str = "engineering-owner") -> tuple[int, str, str]:
        return invoke("decide", str(self.root), "--artifact", decision_id, "--decision", actor, *extra, "--apply")


class RiskArtifactTests(RiskFixture):
    """REQ-RSK-010: one cause, one effect and a measured size (RSK-MGT-001 to RSK-MGT-006)."""

    def test_layout_registry_templates_and_policy_route_the_risk_type(self) -> None:
        # RSK-MGT-001: the type, its prefix, its directory, the templates index and the authoring policy.
        self.assertEqual(("risks",), ARTIFACT_DIRECTORIES["risk"])
        self.assertEqual("RISK-", ARTIFACT_PREFIXES["risk"])
        self.assertIn("| `risk` | `risks/` |", (TEMPLATES / "templates/README.md").read_text(encoding="utf-8"))
        self.assertIn("## risk", (TEMPLATES / "ARTIFACT_AUTHORING.md").read_text(encoding="utf-8"))
        traceability = (TEMPLATES / "TRACEABILITY.md").read_text(encoding="utf-8")
        for token in ("| `risk` | `RISK-` |", "`TRC-REL-023`", "`TRC-REL-024`", "`TRC-REL-025`", "`TRC-016`"):
            self.assertIn(token, traceability)  # RSK-MGT-031
        code, output, error = invoke("create-artifact", str(self.root), "--domain", "product", "--type", "risk", "--id", "RISK-PRD-009")
        self.assertEqual(0, code, error + output)
        text = (self.root / "docs/engineering/product/risks/RISK-PRD-009.md").read_text(encoding="utf-8")
        self.assertIn('type = "risk"', text)
        self.assertIn('status = "identified"', text)
        self.assertIn("harnessctl raise-risk", text)

    def test_measurement_boundaries_draw_e_rsk_002_naming_the_field(self) -> None:
        # RSK-MGT-003: 1 and 5 pass, 0 and 6 fail, and a stored score must be the product.
        write(self.root / DECISION_PATH, pairing_decision_text())
        for field_name in ("likelihood", "impact"):
            for value in (1, 5):
                other = {"likelihood": 2, "impact": 2}
                other[field_name] = value
                write(self.root / RISK_PATH, risk_text(likelihood=other["likelihood"], impact=other["impact"], score=other["likelihood"] * other["impact"]))
                with self.subTest(field=field_name, value=value):
                    self.assertEqual([], self.codes("E-RSK-002"))
            for value in (0, 6):
                other = {"likelihood": 2, "impact": 2}
                other[field_name] = value
                write(self.root / RISK_PATH, risk_text(likelihood=other["likelihood"], impact=other["impact"], score=other["likelihood"] * other["impact"]))
                with self.subTest(field=field_name, value=value):
                    found = self.codes("E-RSK-002")
                    self.assertEqual(1, len(found), found)
                    self.assertIn(f"'{field_name}'", found[0])
        write(self.root / RISK_PATH, risk_text(likelihood=3, impact=4, score=13))
        found = self.codes("E-RSK-002")
        self.assertEqual(1, len(found), found)
        self.assertIn("'score' is 13; likelihood 3 times impact 4 is 12", found[0])
        write(self.root / RISK_PATH, risk_text(likelihood='"3"', impact=4, score=12))
        self.assertTrue(any("'likelihood' must be an integer" in item for item in self.codes("E-RSK-002")), self.codes())

    def test_each_missing_field_draws_e_rsk_001_naming_it_and_no_other_code(self) -> None:
        # RSK-MGT-002: the eight declared fields.
        write(self.root / DECISION_PATH, pairing_decision_text())
        for field_name in ("cause", "effect", "stage", "category", "likelihood", "impact", "score", "raised_by"):
            write(self.root / RISK_PATH, risk_text(drop=(field_name,)))
            with self.subTest(field=field_name):
                found = self.codes()
                self.assertEqual(1, len(found), found)
                self.assertTrue(found[0].startswith("E-RSK-001"), found[0])
                self.assertIn(f"'{field_name}'", found[0])
        write(self.root / RISK_PATH, risk_text())
        self.assertEqual([], self.codes())

    def test_stage_category_one_sentence_and_no_decision_field(self) -> None:
        # RSK-MGT-004, RSK-MGT-005, RSK-MGT-006 and ARCH-RSK-010 conformance check 3.
        write(self.root / DECISION_PATH, pairing_decision_text())
        write(self.root / RISK_PATH, risk_text().replace('stage = "release"', 'stage = "deployment"'))
        self.assertTrue(any("E-RSK-001" in item and "'stage' must name one of" in item for item in self.codes()), self.codes())
        write(self.root / RISK_PATH, risk_text().replace('category = "process"', 'category = "budget"'))
        self.assertTrue(any("E-RSK-001" in item and "'category' must name one of" in item for item in self.codes()), self.codes())
        write(self.root / RISK_PATH, risk_text().replace(
            'cause = "A consumer pins the harness and never upgrades."', 'cause = "A consumer pins the harness. It never upgrades."'))
        self.assertTrue(any("'cause' must be one sentence" in item for item in self.codes()), self.codes())
        write(self.root / RISK_PATH, risk_text(extra='question = "Which option?"'))
        self.assertTrue(any("decision field 'question'" in item for item in self.codes()), self.codes())

    def test_the_workflow_contract_declares_the_family_with_exactly_the_state_model(self) -> None:
        # RSK-MGT-007 and RSK-MGT-008, on the package copy and the template copy alike.
        self.assertEqual((TEMPLATES / "WORKFLOW.json").read_bytes(), (PACKAGE / "workflow_contract.json").read_bytes())
        self.assertEqual(RISK_EDGES, {state: set(row.transitions_to) for state, row in LIFECYCLE_REGISTRY["risk"].items()})
        self.assertFalse(any(row.grants_authority for row in LIFECYCLE_REGISTRY["risk"].values()))
        terminal = {state for state, row in LIFECYCLE_REGISTRY["risk"].items() if not row.transitionable}
        self.assertEqual({"accepted", "avoided", "mitigated", "withdrawn"}, terminal)
        validator = validate_engineering_artifacts
        self.assertEqual(RISK_EDGES, {state: set(row.transitions_to) for state, row in validator.WORKFLOW_LIFECYCLES["risk"].items()})
        workflow_policy = (TEMPLATES / "WORKFLOW.md").read_text(encoding="utf-8")
        for row in ("| Risk | `identified` | `raised`, `withdrawn` |", "| Risk | `raised` | `accepted`, `avoided`, `mitigating`, `withdrawn` |", "| Risk | `mitigating` | `mitigated`, `withdrawn` |"):
            self.assertIn(row, workflow_policy)


class RaiseTests(RiskFixture):
    """REQ-RSK-011: every recorded risk is raised; there is no threshold (RSK-MGT-009 to RSK-MGT-011)."""

    def test_raise_risk_writes_one_raised_file_with_the_hand_computed_score_and_refuses_out_of_range(self) -> None:
        # RSK-MGT-009 and RSK-MGT-010: one act, or nothing.
        code, output, error = self.raise_risk("--json")
        self.assertEqual(0, code, error + output)
        payload = json.loads(output)
        self.assertEqual(("raise-risk", "completed", 12, "RISK-PRD-001", "DEC-PRD-001"),
                         (payload["command"], payload["outcome"], payload["score"], payload["risk"], payload["decision"]))
        text = self.risk_file().read_text(encoding="utf-8")
        self.assertIn('status = "raised"', text)
        self.assertIn("score = 12", text)  # 3 x 4, by hand
        self.assertIn('from = "identified"\nto = "raised"', text)
        self.assertIn('decided_by = "implementation-agent"', text)
        self.assertEqual([], self.codes())
        for arguments in (
            dict(likelihood="6", risk_id="RISK-PRD-002", decision_id="DEC-PRD-002"),
            dict(impact="0", risk_id="RISK-PRD-002", decision_id="DEC-PRD-002"),
            dict(risk_id="RISK-PRD-001", decision_id="DEC-PRD-003"),  # RSK-MGT-010: the identifier is declared already
        ):
            with self.subTest(**arguments):
                before = sorted(path.as_posix() for path in (self.root / "docs/engineering/product").rglob("*.md"))
                code, output, error = self.raise_risk(**arguments)
                self.assertEqual(2, code, output + error)
                self.assertEqual("", output)
                self.assertEqual(before, sorted(path.as_posix() for path in (self.root / "docs/engineering/product").rglob("*.md")))
        self.assertNotIn("6", self.risk_file().read_text(encoding="utf-8").split("likelihood = ")[1][:1])

    def test_a_raise_without_a_decision_names_the_corrective_command_and_dry_run_writes_nothing(self) -> None:
        code, output, error = self.raise_risk("--dry-run", decision_id=None)
        self.assertEqual(0, code, error)
        self.assertIn("dry run", output)
        self.assertFalse(self.risk_file().exists())
        code, output, error = self.raise_risk(decision_id=None)
        self.assertEqual(0, code, error)
        self.assertIn("E-RSK-003", output)
        found = self.codes("E-RSK-003")
        self.assertEqual(1, len(found), found)
        self.assertIn("--with-decision", found[0])

    def test_no_configuration_key_governs_the_raise(self) -> None:
        # RSK-MGT-011: no threshold is read from anywhere; the installed template keeps its keys.
        import tomllib

        configuration = tomllib.loads((self.root / ".engineering-harness.toml").read_text(encoding="utf-8"))
        self.assertNotIn("risk", configuration)
        self.assertNotIn("risks", configuration)
        self.assertNotIn("risk", (PACKAGE / "risks.py").read_text(encoding="utf-8").split("tomllib")[0].lower().split("configuration")[1:2])

    def test_the_domain_token_of_one_domain_resolves_and_an_ambiguous_one_is_refused(self) -> None:
        code, _, error = invoke("create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-PRD-002")
        self.assertEqual(0, code, error)
        code, output, error = self.raise_risk("--dry-run", "--json")
        self.assertEqual(0, code, error)
        arguments = [item if item != "product" else "PRD" for item in self.RAISE]
        code, output, error = invoke("raise-risk", str(self.root), *arguments, "--likelihood", "1", "--impact", "1", "--id", "RISK-PRD-002", "--dry-run", "--json")
        self.assertEqual(0, code, error)
        self.assertEqual("docs/engineering/product/risks/RISK-PRD-002.md", json.loads(output)["changes"][0]["path"])
        code, output, error = invoke("raise-risk", str(self.root), *[item if item != "product" else "ZZZ" for item in self.RAISE], "--likelihood", "1", "--impact", "1", "--id", "RISK-PRD-002", "--dry-run")
        self.assertEqual(2, code)
        self.assertIn("no engineering domain carries the identifier token ZZZ", error)

    def test_every_in_range_pair_stores_its_product(self) -> None:
        # VER-RSK-010 property: the stored score equals the product for every pair.
        for likelihood in MEASUREMENT:
            for impact in MEASUREMENT:
                self.assertEqual(likelihood * impact, compute_score(likelihood, impact))
        for likelihood in (1, 5):
            for impact in (1, 5):
                risk_id = f"RISK-PRD-{likelihood}{impact}1"
                code, _, error = self.raise_risk(likelihood=str(likelihood), impact=str(impact), risk_id=risk_id, decision_id=None)
                self.assertEqual(0, code, error)
                text = (self.root / f"docs/engineering/product/risks/{risk_id}.md").read_text(encoding="utf-8")
                self.assertIn(f"score = {likelihood * impact}\n", text)
        self.assertEqual([], self.codes("E-RSK-002"))
        self.assertEqual(set(RISK_EDGES), set(LIFECYCLE_REGISTRY["risk"]))


class BorrowedStopTests(RiskFixture):
    """REQ-RSK-012: a raised risk stops the threatened stage through a decision (RSK-MGT-012 to RSK-MGT-015, RSK-MGT-033)."""

    def test_the_paired_decision_stops_the_work_order_naming_the_decision_and_not_the_risk(self) -> None:
        self.in_progress_work_order()
        code, _, error = self.raise_risk()
        self.assertEqual(0, code, error)
        self.assertEqual([], self.codes())
        predicate = self.predicates(self.handoff_check())["QGP-G4I-DECISION"]
        self.assertEqual("fail", predicate["status"], predicate)
        message = predicate["message"]
        self.assertIn("DEC-PRD-001", message)
        for option in ("accept", "avoid", "mitigate"):
            self.assertIn(option, message)
        self.assertIn("engineering-owner", message)
        self.assertIn("harnessctl decide", message)
        self.assertNotIn("RISK-PRD-001", message)
        risk_before, decision_before = self.risk_file().read_bytes(), self.decision_file().read_bytes()
        code, output, error = invoke(
            "transition", str(self.root), "--set", "WO-001=implemented", "--decision", "WO-001=engineering-owner", "--apply",
        )
        self.assertEqual(1, code)
        self.assertIn("QGP-G4I-DECISION", output + error)
        self.assertIn("DEC-PRD-001", output + error)
        self.assertNotIn("RISK-PRD-001", output + error)
        self.assertEqual((risk_before, decision_before), (self.risk_file().read_bytes(), self.decision_file().read_bytes()))
        self.assertIn('status = "in_progress"', (self.root / "docs/engineering/product/work-orders/WO-001.md").read_text(encoding="utf-8"))

    def test_a_raised_risk_needs_exactly_one_pending_decision_whose_blocks_equal_its_threatens(self) -> None:
        # RSK-MGT-012 and RSK-MGT-013.
        write(self.root / RISK_PATH, risk_text())
        found = self.codes("E-RSK-003")
        self.assertEqual(1, len(found), found)
        self.assertIn("no open or deferred decision", found[0])
        write(self.root / DECISION_PATH, pairing_decision_text(blocks=("REQ-001",)))
        found = self.codes("E-RSK-004")
        self.assertEqual(1, len(found), found)
        self.assertIn("DEC-PRD-001 blocks ['REQ-001'] but RISK-PRD-001 threatens ['WO-001']", found[0])
        write(self.root / DECISION_PATH, pairing_decision_text())
        self.assertEqual([], self.codes())
        write(self.root / "docs/engineering/product/decisions/DEC-PRD-002.md", pairing_decision_text("DEC-PRD-002"))
        found = self.codes("E-RSK-003")
        self.assertEqual(1, len(found), found)
        self.assertIn("2 pending decisions (DEC-PRD-001, DEC-PRD-002); exactly one answers it", found[0])
        write(self.root / "docs/engineering/product/decisions/DEC-PRD-002.md", pairing_decision_text("DEC-PRD-002", status="withdrawn").replace(
            "[relations]", '[disposition]\noption = "withdrawn"\nlabel = "x"\ndecided_by = "owner"\ndecided_at = "2026-09-01T00:00:00Z"\nreason = "x"\n\n[relations]'
        ) + '\n[[lifecycle_events]]\nfrom = "open"\nto = "withdrawn"\ndecided_at = "2026-09-01T00:00:00Z"\ndecided_by = "owner"\nreason = "x"\n')
        self.assertEqual([], self.codes())

    def test_no_predicate_or_gate_group_is_added_and_the_risk_edges_bind_none(self) -> None:
        # RSK-MGT-014 and ARCH-RSK-010 conformance check 1.
        for copy in (PACKAGE / "quality_gates_contract.json", TEMPLATES / "QUALITY_GATES.json"):
            quality = json.loads(copy.read_text(encoding="utf-8"))
            with self.subTest(copy=copy.name):
                self.assertEqual(MAIN_PREDICATES, {p["id"] for gate in quality["gates"] for p in gate["predicates"]})
                risk_bindings = [b for b in quality["transition_bindings"] if b["family"] == "risk"]
                self.assertEqual({"raised", "accepted", "avoided", "mitigating", "mitigated", "withdrawn"}, {b["target"] for b in risk_bindings})
                self.assertTrue(all(b["predicates"] == [] and b["structural"] == ["QGS-EDGE"] for b in risk_bindings), risk_bindings)
                self.assertFalse(any("RISK" in p["id"] or "risk" in json.dumps(p) for gate in quality["gates"] for p in gate["predicates"]))
        self.assertEqual((PACKAGE / "quality_gates_contract.json").read_bytes(), (TEMPLATES / "QUALITY_GATES.json").read_bytes())
        self.assertIn("| risk | `raised`, `accepted`, `avoided`, `mitigating`, `mitigated`, `withdrawn` | none | `QGS-EDGE` |",
                      (TEMPLATES / "QUALITY_GATES.md").read_text(encoding="utf-8"))

    def test_risks_lists_the_threats_to_an_artifact_and_its_chain_and_writes_nothing(self) -> None:
        # RSK-MGT-033.
        code, _, error = self.raise_risk()
        self.assertEqual(0, code, error)
        before = {path: path.read_bytes() for path in self.root.rglob("*.md")}
        code, output, error = invoke("risks", str(self.root), "--artifact", "WO-001", "--json")
        self.assertEqual(0, code, error)
        payload = json.loads(output)
        self.assertEqual("risks", payload["command"])
        self.assertEqual([("RISK-PRD-001", 12, "raised", ["WO-001"], "DEC-PRD-001")],
                         [(row["id"], row["score"], row["status"], row["threatens"], row["decision"]) for row in payload["risks"]])
        code, output, error = invoke("risks", str(self.root), "--artifact", "REQ-001")
        self.assertEqual(0, code, error)
        self.assertIn("no risk threatens REQ-001", output)
        code, output, error = invoke("risks", str(self.root), "--artifact", "WO-404")
        self.assertEqual(2, code)
        self.assertIn("unknown artifact ID: WO-404", error)
        self.assertEqual(before, {path: path.read_bytes() for path in self.root.rglob("*.md")})


class DisposalTests(RiskFixture):
    """REQ-RSK-013: the answer is given once, on the decision, and copied over (RSK-MGT-016 to RSK-MGT-021)."""

    def test_disposing_the_decision_moves_the_risk_in_the_same_act_for_each_option(self) -> None:
        # RSK-MGT-016, RSK-MGT-018, RSK-MGT-019 and RSK-MGT-020, once per option.
        for number, option, extra in (
            ("1", "accept", ("--revisit", "v1.1.0")),
            ("2", "avoid", ()),
            ("3", "mitigate", ("--mitigated-by", "WO-001")),
        ):
            risk_id, decision_id = f"RISK-PRD-00{number}", f"DEC-PRD-00{number}"
            code, _, error = self.raise_risk(risk_id=risk_id, decision_id=decision_id)
            self.assertEqual(0, code, error)
            reason = f"The owner chose {option} for {risk_id}."
            code, output, error = self.decide("--option", option, "--reason", reason, *extra, decision_id=decision_id)
            with self.subTest(option=option):
                self.assertEqual(0, code, output + error)
                risk = (self.root / f"docs/engineering/product/risks/{risk_id}.md").read_text(encoding="utf-8")
                decision = (self.root / f"docs/engineering/product/decisions/{decision_id}.md").read_text(encoding="utf-8")
                self.assertIn(f'status = "{OPTION_TARGETS[option]}"', risk)
                self.assertIn('status = "decided"', decision)
                self.assertIn("[disposition]", risk)
                self.assertIn(f'option = "{option}"', risk)
                self.assertIn(f'label = "{dict(RISK_OPTIONS)[option]}"', risk)
                self.assertIn('decided_by = "engineering-owner"', risk)
                self.assertIn(f'reason = "{reason}"', risk)
                self.assertIn(f'reason = "{reason}"', decision)
                stamp = decision.split('decided_at = "', 2)[1].split('"')[0]
                self.assertIn(f'decided_at = "{stamp}"', risk)
                self.assertLess(risk.index("[disposition]"), risk.index("[[lifecycle_events]]"))
                if option == "accept":
                    self.assertIn('revisit = "v1.1.0"', risk)
                if option == "avoid":
                    self.assertIn(f'avoided_by = ["{decision_id}"]', risk)
                if option == "mitigate":
                    self.assertIn('mitigated_by = ["WO-001"]', risk)
                    self.assertLess(risk.index('threatens = ["WO-001"]\nmitigated_by'), risk.index("[disposition]"))
        self.assertEqual([], self.codes())
        self.assertEqual([], [f"{i.code}: {i.message}" for i in self.validate().errors])

    def test_refused_answers_write_nothing(self) -> None:
        code, _, error = self.raise_risk()
        self.assertEqual(0, code, error)
        before = (self.risk_file().read_bytes(), self.decision_file().read_bytes())
        for extra, expected in (
            (("--option", "accept", "--reason", "Live with it."), "requires --revisit"),
            (("--option", "mitigate", "--reason", "Reduce it."), "requires --mitigated-by"),
            (("--option", "mitigate", "--reason", "Reduce it.", "--mitigated-by", "REQ-001"), "must name a work order"),
            (("--option", "avoid", "--reason", "Design it out.", "--avoided-by", "WO-001"), "must name an ADR or a decision"),
            (("--option", "avoid", "--reason", "Design it out.", "--mitigated-by", "WO-001"), "--mitigated-by applies to the mitigate answer only"),
            (("--option", "accept", "--reason", "x", "--revisit", "v2"), "DR-DECISION-DISPOSE"),
        ):
            actor = "release-owner" if expected == "DR-DECISION-DISPOSE" else "engineering-owner"
            with self.subTest(extra=extra):
                code, output, error = self.decide(*extra, actor=actor)
                self.assertEqual(1, code, output + error)
                self.assertIn(expected, output + error)
                self.assertEqual(before, (self.risk_file().read_bytes(), self.decision_file().read_bytes()))
        code, _, error = self.decide("--option", "avoid", "--reason", "Design it out.", "--avoided-by", "ADR-001")
        self.assertEqual(0, code, error)
        self.assertIn('avoided_by = ["ADR-001"]', self.risk_file().read_text(encoding="utf-8"))

    def test_a_hand_written_disposition_is_e_rsk_005(self) -> None:
        # RSK-MGT-018.
        write(self.root / DECISION_PATH, pairing_decision_text())
        table = '[disposition]\noption = "accept"\nlabel = "x"\ndecided_by = "owner"\ndecided_at = "2026-09-01T00:00:00Z"\nreason = "typed by hand"\nrevisit = "v9"\n\n[relations]'
        write(self.root / RISK_PATH, risk_text().replace("[relations]", table))
        self.assertTrue(any("E-RSK-005" in item and "raised risk carries no disposition" in item for item in self.codes()), self.codes())
        write(self.root / RISK_PATH, risk_text(status="accepted"))
        found = self.codes("E-RSK-005")
        self.assertTrue(any("carries a [disposition] table written by harnessctl decide" in item for item in found), found)
        write(self.root / RISK_PATH, risk_text(status="accepted").replace("[relations]", table))
        found = self.codes("E-RSK-005")
        self.assertTrue(any("without a lifecycle event was written by hand" in item for item in found), found)
        write(self.root / RISK_PATH, risk_text(status="mitigating").replace("[relations]", table.replace('option = "accept"', 'option = "mitigate"')))
        found = self.codes("E-RSK-005")
        self.assertTrue(any("names its mitigating work orders in mitigated_by" in item for item in found), found)

    def test_a_deferral_leaves_the_risk_raised_and_admits_only_the_scoped_transition(self) -> None:
        # RSK-MGT-017.
        self.in_progress_work_order()
        code, _, error = self.raise_risk()
        self.assertEqual(0, code, error)
        code, output, error = self.decide("--defer", "--scope", "WO-001:in_progress-implemented", "--revisit", "v1.1.0", "--reason", "Not before the field lands.")
        self.assertEqual(0, code, output + error)
        risk = self.risk_file().read_text(encoding="utf-8")
        self.assertIn('status = "raised"', risk)
        self.assertNotIn("[disposition]", risk)
        self.assertIn('status = "deferred"', self.decision_file().read_text(encoding="utf-8"))
        self.assertEqual([], self.codes())
        self.assertEqual("pass", self.predicates(self.handoff_check())["QGP-G4I-DECISION"]["status"])
        from se_harness.repository_graph import artifact_catalog, validated_repository
        from se_harness.workflow_compliance import blocking_decisions

        catalog = artifact_catalog(validated_repository(self.root)[1])
        self.assertEqual(["DEC-PRD-001"], [item.artifact_id for item in blocking_decisions(catalog, catalog["WO-001"], "verified")])
        code, _, error = self.decide("--option", "accept", "--revisit", "v1.2.0", "--reason", "The field landed; we live with it.")
        self.assertEqual(0, code, error)
        self.assertIn('status = "accepted"', self.risk_file().read_text(encoding="utf-8"))

    def test_withdrawing_the_decision_withdraws_the_risk_and_retains_both(self) -> None:
        # VER-RSK-010 acceptance scenario 4.
        self.in_progress_work_order()
        code, _, error = self.raise_risk()
        self.assertEqual(0, code, error)
        code, output, error = self.decide("--withdraw", "--reason", "Raised against the wrong work order.")
        self.assertEqual(0, code, output + error)
        risk = self.risk_file().read_text(encoding="utf-8")
        self.assertIn('status = "withdrawn"', risk)
        self.assertIn('option = "withdrawn"', risk)
        self.assertIn('status = "withdrawn"', self.decision_file().read_text(encoding="utf-8"))
        self.assertEqual([], [f"{i.code}: {i.message}" for i in self.validate().errors])
        self.assertEqual("pass", self.predicates(self.handoff_check())["QGP-G4I-DECISION"]["status"])

    def test_a_bare_transition_never_raises_or_answers_a_risk_but_withdraws_one_with_a_reason(self) -> None:
        # RSK-MGT-021.
        code, _, error = self.raise_risk()
        self.assertEqual(0, code, error)
        before = self.risk_file().read_bytes()
        for target in ("accepted", "avoided", "mitigating"):
            with self.subTest(target=target):
                code, output, error = invoke("transition", str(self.root), "--set", f"RISK-PRD-001={target}", "--decision", "RISK-PRD-001=engineering-owner", "--reason", "RISK-PRD-001=x", "--apply")
                self.assertEqual(1, code)
                self.assertIn("harnessctl raise-risk", output + error)
                self.assertIn("harnessctl decide", output + error)
                self.assertEqual(before, self.risk_file().read_bytes())
        code, output, error = invoke("transition", str(self.root), "--set", "RISK-PRD-001=withdrawn", "--decision", "RISK-PRD-001=engineering-owner", "--apply")
        self.assertEqual(1, code)
        self.assertIn("requires --reason", output + error)
        code, output, error = invoke("transition", str(self.root), "--set", "RISK-PRD-001=withdrawn", "--decision", "RISK-PRD-001=engineering-owner", "--reason", "RISK-PRD-001=Recorded twice.", "--apply")
        self.assertEqual(0, code, output + error)
        self.assertIn('status = "withdrawn"', self.risk_file().read_text(encoding="utf-8"))
        self.assertEqual([], self.codes())

    def test_only_the_transition_path_writes_a_disposition_and_the_decision_module_never_reads_risks(self) -> None:
        # ARCH-RSK-010: the dependency runs one way; RSK-MGT-018: one writer.
        writers = sorted(path.name for path in PACKAGE.glob("*.py") if '"[disposition]"' in path.read_text(encoding="utf-8"))
        self.assertEqual(["workflow.py"], writers)
        decisions = (PACKAGE / "decisions.py").read_text(encoding="utf-8")
        self.assertNotIn("risks", decisions)
        self.assertIn("from se_harness.decisions import", (PACKAGE / "risks.py").read_text(encoding="utf-8"))

    def test_a_past_revisit_on_an_accepted_risk_is_a_maintenance_warning_until_a_decision_concerns_it_again(self) -> None:
        # RSK-MGT-019, W-RSK-001.
        from tests.artifact_support import release_record, verification_record

        write(self.root / "docs/engineering/product/verification-records/VREC-001.md", verification_record("a" * 40))
        write(self.root / "docs/engineering/product/releases/RLS-001.md", release_record("a" * 40))
        code, _, error = self.raise_risk()
        self.assertEqual(0, code, error)
        code, _, error = self.decide("--option", "accept", "--revisit", "v1.0.0", "--reason", "Accepted for one release.")
        self.assertEqual(0, code, error)
        warnings = [item for item in self.validate().warnings if item.code == "W-RSK-001"]
        self.assertEqual(1, len(warnings), warnings)
        self.assertIn("past its revisit 'v1.0.0'", warnings[0].message)
        write(self.root / "docs/engineering/product/decisions/DEC-PRD-002.md", pairing_decision_text("DEC-PRD-002"))
        self.assertEqual([], [item for item in self.validate().warnings if item.code == "W-RSK-001"])

    def test_no_command_deletes_or_rewrites_a_terminal_risk(self) -> None:
        # RSK-MGT-034, second clause. The first clause names `renumber-artifacts`, which
        # WO-ECP-030 retired while this work was in progress; DEC-RSK-001 records the deviation.
        self.assertNotIn("renumber-artifacts", {action.dest for action in build_parser()._actions if action.dest} | set(_subcommands()))
        code, _, error = self.raise_risk()
        self.assertEqual(0, code, error)
        code, _, error = self.decide("--option", "avoid", "--reason", "Design it out.")
        self.assertEqual(0, code, error)
        before = self.risk_file().read_bytes()
        for target in ("raised", "mitigating", "withdrawn", "accepted"):
            code, output, error = invoke("transition", str(self.root), "--set", f"RISK-PRD-001={target}", "--decision", "RISK-PRD-001=engineering-owner", "--reason", "RISK-PRD-001=x", "--apply")
            self.assertEqual(1, code, output + error)
            self.assertIn("is not allowed", output + error)
        code, output, error = self.decide("--option", "accept", "--revisit", "v9", "--reason", "again")
        self.assertEqual(1, code)
        self.assertEqual(before, self.risk_file().read_bytes())
        self.assertTrue(self.risk_file().is_file())

    def test_an_interrupted_disposal_restores_both_files(self) -> None:
        # VER-RSK-010 resilience: the second write fails; neither file is half-written.
        code, _, error = self.raise_risk()
        self.assertEqual(0, code, error)
        before = (self.risk_file().read_bytes(), self.decision_file().read_bytes())
        from se_harness import workflow

        original = workflow._replace
        calls: list[int] = []

        def failing_replace(staged, target):
            calls.append(1)
            if len(calls) == 2:
                raise OSError("disk full")
            original(staged, target)

        with mock.patch.object(workflow, "_replace", failing_replace):
            code, output, error = self.decide("--option", "avoid", "--reason", "Design it out.")
        self.assertEqual(1, code)
        self.assertIn("restored", output + error)
        self.assertEqual(before, (self.risk_file().read_bytes(), self.decision_file().read_bytes()))
        code, _, error = self.decide("--option", "avoid", "--reason", "Design it out.")
        self.assertEqual(0, code, error)


class SecurityTests(RiskFixture):
    """VER-RSK-010 security checks: text stays data, the raise carries no authority, crafted identifiers are refused."""

    def test_hostile_text_stays_data_everywhere(self) -> None:
        hostile = "<script>alert(1)</script> +++ `rm -rf` \"quoted\" \\backslash"
        self.in_progress_work_order()
        arguments = [item if item != "Config drift" else hostile for item in self.RAISE]
        code, output, error = invoke("raise-risk", str(self.root), *arguments, "--likelihood", "2", "--impact", "5", "--id", "RISK-PRD-001", "--with-decision", "--decision-id", "DEC-PRD-001")
        self.assertEqual(0, code, error + output)
        self.assertEqual([], [f"{i.code}: {i.message}" for i in self.validate().errors])
        message = self.predicates(self.handoff_check())["QGP-G4I-DECISION"]["message"]
        self.assertIn(hostile, message)
        code, output, error = invoke("risks", str(self.root), "--artifact", "WO-001", "--json")
        self.assertEqual(0, code, error)
        self.assertEqual(hostile, json.loads(output)["risks"][0]["title"])
        code, output, error = invoke("raise-risk", str(self.root), *self.RAISE, "--likelihood", "1", "--impact", "1", "--id", "RISK-PRD-002", "--cause", "Line one\nline two")
        self.assertEqual(2, code)
        self.assertIn("single-line", error)

    def test_the_raise_carries_no_authority_and_the_raiser_cannot_answer(self) -> None:
        code, _, error = self.raise_risk("--raised-by", "nobody-with-a-right")
        self.assertEqual(0, code, error)
        before = (self.risk_file().read_bytes(), self.decision_file().read_bytes())
        code, output, error = self.decide("--option", "accept", "--revisit", "v2", "--reason", "x", actor="nobody-with-a-right")
        self.assertEqual(1, code)
        self.assertIn("DR-DECISION-DISPOSE", output + error)
        self.assertEqual(before, (self.risk_file().read_bytes(), self.decision_file().read_bytes()))

    def test_a_crafted_identifier_is_refused(self) -> None:
        for crafted in ("../RISK-PRD-001", "RISK-PRD-001/../x", "RISK-PRD-001.md", "WO-PRD-001"):
            with self.subTest(identifier=crafted):
                code, output, error = self.raise_risk(risk_id=crafted, decision_id=None)
                self.assertEqual(2, code, output)
                self.assertFalse(list((self.root / "docs/engineering/product").rglob("RISK-*")))


class ScopeAdmissionTests(RiskFixture):
    """REQ-RSK-015: recording a risk never widens a work order's scope (RSK-MGT-026, RSK-MGT-027)."""

    def commit_all(self, message: str) -> str:
        git(self.root, "add", ".")
        git(self.root, "commit", "-q", "-m", message)
        return git(self.root, "rev-parse", "HEAD")

    def checkpoint(self, checkpoint: str, *arguments: str) -> dict:
        code, output, error = invoke("check", str(self.root), "--artifact", "WO-001", "--checkpoint", checkpoint, *arguments, "--json")
        self.assertIn(code, (0, 1), error)
        return json.loads(output)

    def setUp(self) -> None:
        super().setUp()
        # The pairing decision lands in a declared directory; only the risk file relies on the admission.
        self.in_progress_work_order("src/", "docs/engineering/product/decisions/")
        git(self.root, "init", "-q", "-b", "main")
        self.commit_all("base")

    def test_an_added_risk_file_of_the_work_orders_domain_is_admitted_and_only_that_file(self) -> None:
        # RSK-MGT-026, on a Git-derived set and on a declared one.
        code, _, error = self.raise_risk()
        self.assertEqual(0, code, error)
        for checkpoint in ("scope", "handoff"):
            with self.subTest(checkpoint=checkpoint, source="git"):
                result = self.checkpoint(checkpoint, "--from-git", "HEAD")
                paths = self.predicates(result)["QGP-G4I-PATHS"]
                self.assertEqual("pass", paths["status"], paths)
                # The self-binding handoff adds its own retained packet to the set (ECP-SBH-004).
                self.assertLessEqual({RISK_PATH, DECISION_PATH}, set(result["scope"]["changed_paths"]))
            with self.subTest(checkpoint=checkpoint, source="declared"):
                result = self.checkpoint(checkpoint, "--changed-path", RISK_PATH, "--changed-path", DECISION_PATH, "--changes-complete")
                self.assertEqual("pass", self.predicates(result)["QGP-G4I-PATHS"]["status"])
        from se_harness.repository_graph import artifact_catalog, validated_repository
        from se_harness.workflow_compliance import git_change_set, risk_admissions

        catalog = artifact_catalog(validated_repository(self.root)[1])
        self.assertEqual((RISK_PATH,), risk_admissions(self.root, catalog["WO-001"], git_change_set(self.root, "HEAD")))

    def test_an_unrelated_added_file_and_a_modified_or_deleted_risk_file_still_need_a_declared_path(self) -> None:
        # RSK-MGT-027.
        code, _, error = self.raise_risk()
        self.assertEqual(0, code, error)
        write(self.root / "notes/stray.md", "# stray")
        paths = self.predicates(self.checkpoint("scope", "--from-git", "HEAD"))["QGP-G4I-PATHS"]
        self.assertEqual("fail", paths["status"])
        self.assertIn("notes/stray.md", paths["message"])
        self.assertNotIn(RISK_PATH, paths["message"])
        (self.root / "notes/stray.md").unlink()
        (self.root / "notes").rmdir()
        self.commit_all("risk recorded")
        self.assertEqual("pass", self.predicates(self.checkpoint("scope", "--from-git", "HEAD"))["QGP-G4I-PATHS"]["status"])
        risk = self.risk_file()
        risk.write_text(risk.read_text(encoding="utf-8").replace('residual = ""', 'residual = "edited by hand"'), encoding="utf-8")
        paths = self.predicates(self.checkpoint("scope", "--from-git", "HEAD"))["QGP-G4I-PATHS"]
        self.assertEqual("fail", paths["status"])
        self.assertIn(RISK_PATH, paths["message"])
        git(self.root, "checkout", "--", RISK_PATH)
        risk.unlink()
        paths = self.predicates(self.checkpoint("scope", "--from-git", "HEAD"))["QGP-G4I-PATHS"]
        self.assertEqual("fail", paths["status"])
        self.assertIn(RISK_PATH, paths["message"])

    def test_another_domains_risk_and_an_approved_work_order_are_not_admitted(self) -> None:
        write(self.root / "docs/engineering/other/risks/RISK-OTH-001.md", risk_text("RISK-OTH-001", status="identified"))
        paths = self.predicates(self.checkpoint("scope", "--from-git", "HEAD"))["QGP-G4I-PATHS"]
        self.assertEqual("fail", paths["status"])
        self.assertIn("RISK-OTH-001", paths["message"])
        (self.root / "docs/engineering/other/risks/RISK-OTH-001.md").unlink()
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        work_order.write_text(work_order.read_text(encoding="utf-8").replace('status = "in_progress"', 'status = "approved"'), encoding="utf-8")
        write(self.root / RISK_PATH, risk_text(status="identified"))
        paths = self.predicates(self.checkpoint("scope", "--from-git", "HEAD"))["QGP-G4I-PATHS"]
        self.assertEqual("fail", paths["status"])
        self.assertIn(RISK_PATH, paths["message"])


class ScopeAdmissionWithoutGitTests(RiskFixture):
    def test_without_a_checkout_nothing_is_provably_added_so_the_path_must_be_declared(self) -> None:
        self.in_progress_work_order()
        code, _, error = self.raise_risk()
        self.assertEqual(0, code, error)
        code, output, error = invoke("check", str(self.root), "--artifact", "WO-001", "--checkpoint", "scope", "--changed-path", RISK_PATH, "--changes-complete", "--json")
        paths = self.predicates(json.loads(output))["QGP-G4I-PATHS"]
        self.assertEqual("fail", paths["status"])
        self.assertIn(RISK_PATH, paths["message"])


if __name__ == "__main__":
    unittest.main()
