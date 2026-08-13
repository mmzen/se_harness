from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

GENERATOR_SPEC = importlib.util.spec_from_file_location(
    "dashboard_webui_generator",
    SCRIPTS / "generate_harness_dashboard.py",
)
if GENERATOR_SPEC is None or GENERATOR_SPEC.loader is None:
    raise RuntimeError("dashboard generator is unavailable")
GENERATOR = importlib.util.module_from_spec(GENERATOR_SPEC)
sys.modules[GENERATOR_SPEC.name] = GENERATOR
GENERATOR_SPEC.loader.exec_module(GENERATOR)


class DashboardWebUIContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.template = ROOT / "scripts/harness_explorer/index.template.html"
        self.canonical = ROOT / "templates/repository/standard/scripts/harness_explorer/index.template.html"
        self.prototype = ROOT / "templates/webui/harness-lineage-prototype.html"
        self.webui = ROOT / "templates/webui"

    def test_templates_preserve_the_original_3d_design_and_canonical_boundary(self) -> None:
        content = self.template.read_text(encoding="utf-8")
        self.assertEqual(content, self.canonical.read_text(encoding="utf-8"))
        self.assertEqual(content, self.prototype.read_text(encoding="utf-8"))
        self.assertEqual(1, content.count("__HARNESS_SNAPSHOT_JSON__"))
        self.assertIn('raw.schema!=="harness-dashboard-snapshot-v1"', content)
        self.assertIn('data-current-view="overview"', content)
        self.assertIn('data-view="lineage"', content)
        self.assertIn('data-view="readiness"', content)
        self.assertIn('data-od-id="three-dimensional-graph"', content)
        self.assertIn('const GRAPH_SOURCE="https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js"', content)
        self.assertIn('Interactive 3D topology unavailable', content)
        for forbidden in (
            "<script src=",
            "fetch(",
            "WebSocket(",
            "generatedAt",
            "Show complete graph",
            "Active coverage",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, content)

    def test_five_questions_and_semantic_states_remain_explicit(self) -> None:
        content = self.template.read_text(encoding="utf-8")
        for phrase in (
            "Why does this exist?",
            "Is the definition covered?",
            "What needs reassessment?",
            "What is inconsistent or unassessable?",
            "Does the harness help?",
            "Definition coverage",
            "Commit-bound provenance",
            "not_assessable",
            "superseded_by",
            "Controlled outcomes",
            "item.type",
            "new Option(v,v)",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

        self.assertNotIn("const artifactTypes", content)
        self.assertNotIn("switch(node.type)", content)

    def test_design_materials_describe_the_canonical_contract(self) -> None:
        manifest = json.loads((self.webui / "DESIGN-MANIFEST.json").read_text(encoding="utf-8"))
        schema = json.loads((self.webui / "harness-dashboard-data.schema.json").read_text(encoding="utf-8"))
        contract = (self.webui / "harness-dashboard-data.md").read_text(encoding="utf-8")
        handoff = (self.webui / "DESIGN-HANDOFF.md").read_text(encoding="utf-8")

        self.assertEqual("harness-dashboard-snapshot-v1", manifest["dataContract"]["schema"])
        self.assertFalse(manifest["dataContract"]["persistedPresentationSchema"])
        self.assertTrue(manifest["security"]["runtimeNetwork"])
        self.assertEqual(
            "https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js",
            manifest["security"]["thirdPartyRuntimeAssets"][0]["url"],
        )
        self.assertFalse(manifest["security"]["thirdPartyRuntimeAssets"][0]["integrityPinned"])
        self.assertEqual([], manifest["sourceFiles"]["missing"])
        self.assertEqual("harness-dashboard-snapshot-v1", schema["properties"]["schema"]["const"])
        self.assertNotIn("generatedAt", schema.get("properties", {}))
        self.assertIn("definition coverage", contract.lower())
        self.assertIn("ADR-DST-008", handoff)
        self.assertIn("3d-force-graph@1.79.0", handoff)

        for relative in manifest["sourceFiles"]["all"]:
            self.assertTrue((self.webui / relative).is_file(), relative)
        self.assertFalse(any(path.suffix.lower() == ".png" for path in self.webui.iterdir()))

    def test_real_snapshot_matches_documented_top_level_contract(self) -> None:
        snapshot, report, _ = GENERATOR.generate_snapshot(ROOT)
        self.assertTrue(report.valid)
        schema = json.loads((self.webui / "harness-dashboard-data.schema.json").read_text(encoding="utf-8"))
        self.assertEqual("harness-dashboard-snapshot-v1", snapshot["schema"])
        self.assertEqual(set(schema["required"]), set(snapshot))
        self.assertNotIn("generatedAt", snapshot)
        self.assertNotIn("metrics", snapshot)
        self.assertNotIn("graph", snapshot)
        self.assertTrue(all({"source", "relation", "target", "authority", "target_exists"} <= set(item) for item in snapshot["relations"]))
        self.assertTrue(all({"rule", "severity", "message", "artifacts", "paths", "authority", "evidence"} <= set(item) for item in snapshot["findings"]))
        self.assertTrue(all(gate["state"] in {"satisfied", "unsatisfied", "not_assessable"} for item in snapshot["readiness"] for gate in item["gates"]))
        self.assertEqual(GENERATOR.serialize_json(snapshot), GENERATOR.serialize_json(snapshot))

        future = dict(snapshot)
        future["artifacts"] = [*snapshot["artifacts"], {"id": "FUTURE-001", "type": "future_control", "title": "Future control", "status": "draft", "owners": [], "path": "future.md"}]
        rendered = GENERATOR.render_dashboard(future)
        self.assertIn('"type":"future_control"', rendered)
        self.assertIn("new Option(v,v)", rendered)

    def test_renderer_context_escapes_hostile_repository_text(self) -> None:
        snapshot, _, _ = GENERATOR.generate_snapshot(ROOT)
        hostile = '</script><img src=x onerror="alert(1)">&\u2028\u2029__HARNESS_SNAPSHOT_JSON__'
        snapshot["artifacts"][0]["title"] = hostile
        rendered = GENERATOR.render_dashboard(snapshot)
        self.assertNotIn('</script><img src=x onerror="alert(1)">', rendered)
        self.assertIn("\\u003c/script\\u003e", rendered)
        self.assertIn("\\u0026\\u2028\\u2029__HARNESS_SNAPSHOT_JSON__", rendered)
        self.assertEqual(2, rendered.count("<script"))
        self.assertNotIn("__HARNESS_SNAPSHOT_JSON__</script>", rendered)

    def test_only_the_explicitly_accepted_runtime_url_is_present(self) -> None:
        content = self.template.read_text(encoding="utf-8")
        self.assertEqual(1, content.count("https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js"))
        self.assertIn("script-src 'unsafe-inline' https://unpkg.com", content)
        self.assertIn("connect-src 'none'", content)
        self.assertNotIn("integrity=", content)


if __name__ == "__main__":
    unittest.main()
