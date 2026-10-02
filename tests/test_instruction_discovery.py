"""Instruction discovery must describe, never replace, workflow selection."""
from copy import deepcopy
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from se_harness import instruction_discovery as discovery
from se_harness.workflow_contract import load_validated_contracts, ContractError
from se_harness.workflow_procedures import resolve_procedure
from se_harness.workflow_result import restitution_digest
from tests import test_workflow_restitution as restitution_tests


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates/repository/standard"


class InstructionDiscoveryTests(unittest.TestCase):
    def test_catalogue_matches_all_released_procedures_and_typed_steps(self):
        _, _, _, procedures, _ = load_validated_contracts()
        catalog = discovery.load_catalog()
        self.assertEqual(19, len(catalog["procedures"]))
        self.assertEqual(24, sum(len(p["steps"]) for p in catalog["procedures"].values()))
        discovery.validate_coverage(procedures)
        for procedure in catalog["procedures"].values():
            references = [procedure["location"], *procedure["prerequisites"]]
            for step in procedure["steps"].values():
                references += [step["location"], *step["prerequisites"]]
            for ref in references:
                path = TEMPLATE / ref["file"]
                text = path.read_text(encoding="utf-8")
                headings = {re.sub(r"[^\w\- ]", "", x.lower()).replace(" ", "-")
                            for x in re.findall(r"^#{1,6} (.+)$", text, re.M)}
                self.assertIn(ref["heading"], headings, ref)

    def test_start_reading_distinguishes_preflight_from_applied_start(self):
        _, _, _, procedures, _ = load_validated_contracts()
        resolved = resolve_procedure(procedures, "PROC-WO-START", {"artifact_id": "WO-ABC-001"})
        before = deepcopy(resolved)
        result = discovery.describe({**resolved, "current_step": "STEP-WO-START-PREFLIGHT"}, ["WO-ABC-001", "REQ-ABC-001"])
        self.assertEqual(before, resolved)
        self.assertEqual("establish-the-execution-context", result["agent_instructions"]["current_step"]["location"]["heading"])
        self.assertEqual("start-the-selected-work", result["agent_instructions"]["procedure"]["steps"]["STEP-WO-START-APPLY"]["location"]["heading"])
        self.assertEqual(["REQ-ABC-001", "WO-ABC-001"], result["formal_artifact_ids"])
        self.assertEqual(["docs/engineering/WORKFLOW.json", "docs/engineering/QUALITY_GATES.json"], result["evaluator_only_inputs"])
        self.assertNotIn("argv", result)

    def test_prerequisites_are_conditional_and_machine_inputs_are_separate(self):
        catalog = discovery.load_catalog()
        for p in catalog["procedures"].values():
            for req in p["prerequisites"]:
                self.assertTrue(req["when"].strip())
                self.assertTrue(req["file"].endswith(".md"))
        external = catalog["procedures"]["PROC-REPOSITORY-INTEGRATION"]
        self.assertIn("When the selected external action prepares or checks a pull request.",
                      [p["when"] for p in external["prerequisites"]])

    def test_unknown_returned_identifier_reports_a_version_gap(self):
        for proc, step in [("PROC-UNKNOWN", "STEP-UNKNOWN"), ("PROC-WO-START", "STEP-UNKNOWN")]:
            with self.subTest(proc=proc, step=step), self.assertRaisesRegex(discovery.DiscoveryError, "no released reading location"):
                discovery.describe({"id": proc, "current_step": step}, [])

    def test_pr_verification_discovers_publication_before_the_decision(self):
        catalog = discovery.load_catalog()["procedures"]
        decision = catalog["PROC-VREC-DECIDE"]
        for prerequisites in (decision["prerequisites"],
                              decision["steps"]["STEP-VREC-DECIDE"]["prerequisites"]):
            publication = next(p for p in prerequisites
                               if p["heading"] == "publish-the-review-package")
            self.assertEqual("docs/engineering/harness/PULL_REQUEST.md", publication["file"])
            self.assertIn("work delivered through a pull request", publication["when"])
        review = catalog["PROC-REVIEW-PUBLISH"]
        self.assertEqual("publish-the-review-package", review["location"]["heading"])
        self.assertEqual(review["location"], review["steps"]["STEP-REVIEW-PUBLISH"]["location"])
        self.assertIn("review-publication-authority",
                      [p["heading"] for p in review["prerequisites"]])

    def test_missing_step_mapping_refuses_contract_loading(self):
        value = discovery.load_catalog()
        del value["procedures"]["PROC-WO-START"]["steps"]["STEP-WO-START-APPLY"]
        with patch.object(discovery, "load_catalog", return_value=value):
            with self.assertRaisesRegex(ContractError, "typed steps and instruction discovery version disagree"):
                load_validated_contracts()

    def test_unsafe_location_or_missing_condition_is_refused(self):
        for mutation in ("path", "condition", "schema"):
            value = discovery.load_catalog()
            if mutation == "path":
                value["procedures"]["PROC-WO-START"]["location"]["file"] = "../../outside.md"
            elif mutation == "condition":
                value["shared_prerequisites"][0]["when"] = ""
            else:
                value["schema"] = "unsupported"
            with tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "catalog.json"
                path.write_text(json.dumps(value), encoding="utf-8")
                with patch.object(discovery, "CATALOG_PATH", path), self.assertRaises(discovery.DiscoveryError):
                    discovery.load_catalog()

    def test_discovery_is_additive_and_bound_without_reinterpreting_old_results(self):
        # A pre-existing synthetic result with an unknown STEP-NEXT stays readable
        # and identifies its discovery mismatch instead of inventing a route.
        result = restitution_tests.WorkflowRestitutionTests().result()
        self.assertEqual("se-harness-workflow-result-v2", result["schema"])
        self.assertEqual("incompatible", result["instruction_discovery"]["status"])
        changed = deepcopy(result)
        changed["instruction_discovery"]["status"] = "available"
        self.assertNotEqual(restitution_digest(result), restitution_digest(changed))
        old = deepcopy(result)
        old.pop("instruction_discovery")
        self.assertEqual(restitution_digest(old), restitution_digest(deepcopy(old)))
        for name in ("state", "compliance", "procedure", "scope", "restitution"):
            self.assertEqual(result[name], old[name])

    def test_human_index_uses_the_catalogue_destinations(self):
        text = (TEMPLATE / "docs/engineering/harness/CONTINUE.md").read_text(encoding="utf-8")
        for pid, p in discovery.load_catalog()["procedures"].items():
            for sid, item in [(pid, p), *p["steps"].items()]:
                row = next(line for line in text.splitlines() if line.startswith(f"| `{sid}` |"))
                location = item["location"]
                self.assertIn(Path(location["file"]).name + "#" + location["heading"], row)


if __name__ == "__main__":
    unittest.main()
