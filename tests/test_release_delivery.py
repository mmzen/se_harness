from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_release_delivery.py"
FIXTURE = ROOT / "tests/fixtures/release_delivery/complete"
SPEC = importlib.util.spec_from_file_location("release_delivery_test_subject", SCRIPT)
DELIVERY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DELIVERY)


class ReleaseDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "evidence"
        shutil.copytree(FIXTURE, self.root)
        self.plan = json.loads((self.root / "plan.json").read_text())
        self.observed = json.loads((self.root / "observations.json").read_text())

    def save(self, rebind=True):
        raw = json.dumps(self.plan, indent=2).encode()
        (self.root / "plan.json").write_bytes(raw)
        if rebind:
            self.observed["plan_sha256"] = hashlib.sha256(raw).hexdigest()
        (self.root / "observations.json").write_text(json.dumps(self.observed), encoding="utf-8")

    def assess(self, rebind=True):
        self.save(rebind)
        return DELIVERY.assess(self.root / "plan.json", self.root / "observations.json", self.root)

    def row(self, result, name):
        return next(row for row in result["surfaces"] if row["id"] == name)

    def complete_route(self):
        self.plan = json.loads((FIXTURE.parent / 'complete-release/plan.json').read_text())
        for wanted, observed in zip(self.plan['surfaces'], self.observed['surfaces']):
            observed['source'] = wanted['destination']
            observed['identity'] = dict(wanted['expected'])
            if wanted['id'] == 'demonstration':
                observed['identity']['governance_commit'] = 'a' * 40
                observed['evidence']['deployment'] = self.observed['release']['evidence']
            for route in observed.get('routes', []):
                route.update(source=wanted['destination'], revision=wanted['expected']['public_revision'],
                             evaluator_version='1.2.3', wheel_sha256='1' * 64)
        self.observed['release']['record'] = 'RLS-TST-001'

    def test_complete_route_preserves_legacy_and_requires_explicit_selection(self):
        self.complete_route()
        DELIVERY.validate_plan(self.plan)
        self.plan['schema'] = DELIVERY.PLAN_SCHEMA
        with self.assertRaises(DELIVERY.InvalidInput):
            DELIVERY.validate_plan(self.plan)

    def test_complete_route_refuses_changed_targets_and_unprepared_inputs(self):
        self.complete_route()
        for change in ('action', 'destination', 'candidate', 'parent', 'host', 'pending', 'documentation'):
            with self.subTest(change=change):
                saved = copy.deepcopy(self.plan)
                if change == 'action': self.plan['complete_release']['actions'].append('other-release')
                if change == 'destination': self.plan['surfaces'][1]['destination'] += '-other'
                if change == 'candidate': self.plan['complete_release']['candidate_commit'] = 'e' * 40
                if change == 'parent': self.plan['complete_release']['marketplace']['parent'] = 'c' * 40
                if change == 'host': self.plan['surfaces'][1]['hosts'] = ['codex']
                if change == 'pending': self.plan['surfaces'][0]['expected']['version'] = None
                if change == 'documentation': self.plan['complete_release']['documentation'] = {'../escape': 'a' * 64}
                with self.assertRaises(DELIVERY.InvalidInput): DELIVERY.validate_plan(self.plan)
                self.plan = saved

    def test_marker_readiness_does_not_claim_completion_or_hide_host_failure(self):
        self.complete_route()
        self.observed['surfaces'].pop()
        self.save()
        result, code = DELIVERY.assess(self.root/'plan.json', self.root/'observations.json', self.root,
                                      governance_commit='a'*40, before_markers=True)
        self.assertEqual((0, 'ready_for_markers'), (code, result['status']))
        self.assertEqual('pending', self.row(result, 'release_markers')['status'])
        self.observed['surfaces'][1]['routes'][0]['status'] = 'pending'
        self.save()
        result, code = DELIVERY.assess(self.root/'plan.json', self.root/'observations.json', self.root,
                                      governance_commit='a'*40, before_markers=True)
        self.assertEqual((1, 'incomplete'), (code, result['status']))

    def test_complete_route_needs_resolved_governance_and_exact_plan_bytes(self):
        self.complete_route()
        result, code = self.assess()
        self.assertEqual(2, code)
        self.save()
        result, code = DELIVERY.assess(self.root/'plan.json', self.root/'observations.json', self.root,
                                      governance_commit='a'*40)
        self.assertEqual((0, 'complete'), (code, result['status']))
        self.observed['plan_sha256'] = '0'*64
        self.save(rebind=False)
        result, code = DELIVERY.assess(self.root/'plan.json', self.root/'observations.json', self.root,
                                      governance_commit='a'*40)
        self.assertEqual(1, code)

    def test_checked_in_example_is_complete_without_rewriting(self):
        result, code = DELIVERY.assess(FIXTURE / "plan.json", FIXTURE / "observations.json", FIXTURE)
        self.assertEqual((code, result["status"], result["input_status"]), (0, "complete", "valid"))
        self.assertEqual(result["formal_release"]["status"], "released")
        self.assertEqual(result["evaluator_publication"], "satisfied")
        self.assertEqual(self.row(result, "demonstration")["disposition"], "unchanged")

    def test_unchanged_needs_a_compatibility_justification(self):
        del self.plan["surfaces"][3]["compatibility"]["reason"]
        result, code = self.assess()
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "incomplete")
        self.assertIn("compatibility.reason", result["findings"][-1]["message"])

    def test_evaluator_success_does_not_hide_missing_marketplace(self):
        self.observed["surfaces"].pop(1)
        self.plan["surfaces"][1]["next_action"] = "Assemble and qualify the declared plugin"
        result, code = self.assess()
        self.assertEqual(code, 1)
        self.assertEqual(result["evaluator_publication"], "satisfied")
        row = self.row(result, "marketplace")
        self.assertEqual(row["status"], "pending")
        self.assertEqual(row["owner"], "Example owner")
        self.assertIn("Assemble", DELIVERY.render(result))

    def test_omitted_surface_is_invalid(self):
        self.plan["surfaces"].pop(1)
        result, code = self.assess()
        self.assertEqual(code, 2)
        self.assertIn("missing surfaces", result["findings"][-1]["message"])

    def test_deferral_cannot_be_delivery(self):
        surface = self.plan["surfaces"][1]
        surface.update(disposition="deferred", required_observations=["deferral"],
                       deferral={"reason": "Await qualification", "decision_reference": "example-human-decision",
                                 "follow_up": "WO-EXAMPLE-002", "revisit": "Evaluator published"})
        self.observed["surfaces"][1]["evidence"]["deferral"] = self.observed["release"]["evidence"]
        result, code = self.assess()
        self.assertEqual(code, 1)
        self.assertEqual(self.row(result, "marketplace")["status"], "deferred")
        self.assertIn("Await qualification", DELIVERY.render(result))

    def test_mismatched_identity_under_equal_version_fails(self):
        for field, different in (("codex_content_sha256", "d" * 64), ("wheel_sha256", "d" * 64),
                                 ("public_revision", "6" * 40), ("evaluator_version", "0.18.0")):
            with self.subTest(field=field):
                saved = copy.deepcopy(self.observed)
                self.observed["surfaces"][1]["identity"][field] = different
                result, code = self.assess()
                self.assertEqual(code, 1)
                row = self.row(result, "marketplace")
                self.assertEqual(row["status"], "failed")
                self.assertTrue(any(f.get("observed") == different for f in row["findings"]))
                self.observed = saved

    def test_observations_cannot_bind_another_plan(self):
        self.observed["plan_sha256"] = "d" * 64
        result, code = self.assess(rebind=False)
        self.assertEqual(code, 1)
        self.assertEqual(result["findings"][0]["location"], "plan_sha256")

    def test_local_only_and_missing_host_update_proof_fail(self):
        routes = self.observed["surfaces"][1].pop("routes")
        result, code = self.assess()
        self.assertEqual(code, 1)
        self.assertEqual(len([f for f in self.row(result, "marketplace")["findings"] if "routes" in f["location"]]), 4)
        self.observed["surfaces"][1]["routes"] = routes[:-1]
        result, code = self.assess()
        self.assertEqual(code, 1)
        self.assertIn("claude-code.update", DELIVERY.render(result))
        self.observed["surfaces"][1]["routes"] = routes
        self.assertEqual(self.assess()[1], 0)

    def test_wrong_route_and_failed_installation_do_not_pass(self):
        route = self.observed["surfaces"][1]["routes"][0]
        route["source"] = "local-marketplace-directory"
        route["status"] = "failed"
        result, code = self.assess()
        self.assertEqual(code, 1)
        text = DELIVERY.render(result)
        self.assertIn("Identity differs", text)
        self.assertIn("Public route has not passed", text)

    def test_local_plan_destination_or_symbolic_revision_is_invalid(self):
        for value in ("local-directory", "https://example.invalid/repository.git", "file:///local#branch"):
            with self.subTest(destination=value):
                original = self.plan["surfaces"][1]["destination"]
                self.plan["surfaces"][1]["destination"] = value
                self.observed["surfaces"][1]["source"] = value
                result, code = self.assess()
                self.assertEqual(code, 2)
                self.assertIn("HTTPS repository URL", result["findings"][-1]["message"])
                self.plan["surfaces"][1]["destination"] = original
        self.plan["surfaces"][1]["expected"]["public_revision"] = "main"
        result, code = self.assess()
        self.assertEqual(code, 2)
        self.assertIn("full commit ID", result["findings"][-1]["message"])

    def test_missing_and_changed_evidence_are_incomplete(self):
        path = self.root / "evidence/observations.txt"
        path.write_text("changed", encoding="utf-8")
        result, code = self.assess()
        self.assertEqual(code, 1)
        self.assertIn("Evidence digest differs", DELIVERY.render(result))
        path.unlink()
        result, code = self.assess()
        self.assertEqual(code, 1)
        self.assertIn("Evidence unavailable", DELIVERY.render(result))

    def test_unreadable_evidence_is_incomplete(self):
        self.save()
        original = Path.open

        def deny(path, *args, **kwargs):
            if path.name == "observations.txt":
                raise PermissionError("denied by test")
            return original(path, *args, **kwargs)

        with mock.patch.object(Path, "open", deny):
            result, code = DELIVERY.assess(self.root / "plan.json", self.root / "observations.json", self.root)
        self.assertEqual(code, 1)
        self.assertIn("Evidence unavailable", DELIVERY.render(result))

    def test_evidence_path_cannot_escape(self):
        for path in ("../outside.txt", "/outside.txt", "C:/outside.txt", "evidence\\outside.txt"):
            with self.subTest(path=path):
                self.observed["release"]["evidence"][0]["path"] = path
                result, code = self.assess()
                self.assertEqual(code, 2)
                self.assertEqual(result["status"], "incomplete")

    def test_symlink_escape_is_invalid(self):
        outside = self.root.parent / "outside.txt"
        outside.write_text("outside", encoding="utf-8")
        link = self.root / "escape.txt"
        try:
            link.symlink_to(outside)
        except OSError as error:
            self.skipTest(f"Host does not permit symlink creation: {error}")
        self.observed["release"]["evidence"][0]["path"] = "escape.txt"
        result, code = self.assess()
        self.assertEqual(code, 2)
        self.assertIn("escapes root", result["findings"][-1]["message"])

    def test_duplicate_keys_schema_and_structural_errors_are_invalid(self):
        for mutation in (lambda: self.plan.update(schema="unknown"),
                         lambda: self.plan["surfaces"].append(copy.deepcopy(self.plan["surfaces"][0])),
                         lambda: self.plan["surfaces"][0].update(disposition=[]),
                         lambda: self.observed["surfaces"][0].update(status=[]),
                         lambda: self.plan["surfaces"][1].update(required_observations=["assembly"]),
                         lambda: self.observed["surfaces"][1]["routes"][0].update(kind=[])):
            with self.subTest(mutation=mutation):
                original_plan, original_observed = copy.deepcopy(self.plan), copy.deepcopy(self.observed)
                mutation()
                result, code = self.assess()
                self.assertEqual(code, 2)
                self.assertEqual(result["status"], "incomplete")
                self.plan, self.observed = original_plan, original_observed
        self.save()
        (self.root / "plan.json").write_text('{"schema":"x","schema":"y"}', encoding="utf-8")
        result, code = DELIVERY.assess(self.root / "plan.json", self.root / "observations.json", self.root)
        self.assertEqual(code, 2)
        self.assertIn("duplicate JSON key", result["findings"][-1]["message"])

    def test_pending_identity_is_not_satisfied(self):
        self.plan["surfaces"][1]["expected"]["public_revision"] = None
        self.observed["surfaces"][1]["identity"]["public_revision"] = None
        result, code = self.assess()
        self.assertEqual(code, 1)
        self.assertIn("not yet selected", DELIVERY.render(result))

    def test_formal_authorization_is_separate(self):
        self.observed["release"]["status"] = "ready"
        result, code = self.assess()
        self.assertEqual(code, 1)
        self.assertEqual(result["formal_release"]["status"], "ready")
        self.assertEqual(result["evaluator_publication"], "satisfied")

    def test_cli_outputs_and_no_file_or_subprocess_side_effects(self):
        self.save()
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with mock.patch("subprocess.run", side_effect=AssertionError("candidate invoked a subprocess")), \
             mock.patch("socket.socket", side_effect=AssertionError("candidate used the network")):
            self.assertEqual(DELIVERY.assess(self.root / "plan.json", self.root / "observations.json", self.root)[1], 0)
        command = [sys.executable, "-B", str(SCRIPT), "--plan", str(self.root / "plan.json"),
                   "--observations", str(self.root / "observations.json"), "--evidence-root", str(self.root), "--json"]
        proc = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["status"], "complete")
        self.assertIn("Grants no lifecycle or external authority", proc.stderr)
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
