from __future__ import annotations

import importlib.util
import re
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


def temporal_findings(
    *,
    source_type: str,
    source_status: str,
    relation_name: str,
    authority: str = "declared",
    source_updated: str = "2026-08-01",
    target_updated: str = "2026-08-02",
    target_exists: bool = True,
    relation_count: int = 1,
) -> list[dict]:
    artifacts = [
        {
            "id": "SOURCE-001",
            "type": source_type,
            "status": source_status,
            "updated": source_updated,
            "path": "docs/engineering/source.md",
        },
        {
            "id": "TARGET-001",
            "type": "requirement",
            "status": "approved",
            "updated": target_updated,
            "path": "docs/engineering/target.md",
        },
    ]
    relation = {
        "source": "SOURCE-001",
        "relation": relation_name,
        "target": "TARGET-001",
        "authority": authority,
        "target_exists": target_exists,
    }
    relations = [
        {
            **relation,
        }
        for _ in range(relation_count)
    ]
    findings = GENERATOR.build_findings(
        artifacts,
        relations,
        [],
        {},
        [],
        {"required_for_release": False},
    )
    return [item for item in findings if item["rule"] == "W-HEX-003"]


class DashboardWebUIContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.template = ROOT / "scripts/harness_explorer/index.template.html"
        self.canonical = ROOT / "templates/repository/standard/scripts/harness_explorer/index.template.html"

    def test_templates_preserve_the_reviewed_3d_design_and_canonical_boundary(self) -> None:
        content = self.template.read_text(encoding="utf-8")
        self.assertEqual(content, self.canonical.read_text(encoding="utf-8"))
        self.assertEqual(1, content.count("__HARNESS_SNAPSHOT_JSON__"))
        self.assertIn('raw.schema!=="harness-dashboard-snapshot-v1"', content)
        self.assertIn('data-current-view="overview"', content)
        self.assertIn('data-view="lineage"', content)
        self.assertIn('data-view="readiness"', content)
        self.assertIn('data-od-id="three-dimensional-graph"', content)
        self.assertIn('data-od-id="graph-color-legend"', content)
        self.assertIn('id="lineageGraph" role="group"', content)
        self.assertIn('data-od-id="zoom-in"', content)
        self.assertIn('linkDirectionalArrowLength(1.8)', content)
        self.assertIn('clip:rect(0 0 0 0)', content)
        self.assertEqual(1, content.count("function renderLineage(){"))
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

    def test_overview_is_concise_and_context_projection_is_bounded(self) -> None:
        content = self.template.read_text(encoding="utf-8")
        self.assertNotIn('data-od-id="definition-coverage"', content)
        self.assertNotIn('id="coverageRows"', content)
        self.assertNotIn('$("coverageRows")', content)
        self.assertIn('id="metricCoverage"', content)
        self.assertIn('id="metricCoverageDetail"', content)
        self.assertIn('coverage:{label:definition?', content)

        self.assertIn('id="graphDepth"', content)
        self.assertIn('<option value="0">0 — matches only</option>', content)
        self.assertIn('<option value="1">1 — direct neighbors</option>', content)
        self.assertIn('<option value="2">2 — two hops</option>', content)
        self.assertIn('CONTEXT_NODE_LIMIT=100', content)
        self.assertIn('function overviewScope(){', content)
        self.assertIn('for(let head=0;head<queue.length;head+=1)', content)
        self.assertIn('scopeRole:"match"', content)
        self.assertIn('scopeRole:"context"', content)
        self.assertIn('TRUNCATED AT ${CONTEXT_NODE_LIMIT} CONTEXT NODES', content)
        self.assertIn('node.scopeRole==="match"?9:4', content)
        self.assertIn('Node size distinguishes filter matches from context nodes', content)
        self.assertIn('$("graphDepth").value="0"', content)

    def test_search_clear_and_revision_presentation_preserve_state_and_provenance(self) -> None:
        content = self.template.read_text(encoding="utf-8")
        self.assertIn('id="clearSearch"', content)
        self.assertIn('data-od-id="artifact-search-clear"', content)
        self.assertIn('aria-label="Clear artifact filter" disabled', content)
        self.assertIn('function updateSearch(){', content)
        self.assertIn('function clearSearch(){', content)
        self.assertIn('$("search").addEventListener("input",updateSearch)', content)
        self.assertIn('$("clearSearch").addEventListener("click",clearSearch)', content)
        self.assertIn('$("search").focus()', content)
        self.assertIn('$("clearSearch").disabled=$("search").value.length===0', content)
        self.assertIn('.search-control:focus-within{outline:3px solid var(--accent);outline-offset:2px}', content)
        self.assertIn('.search-control .search:focus-visible,.search-control .icon-btn:focus-visible{outline:none}', content)

        self.assertIn('function displayedRevision(value)', content)
        self.assertIn('[0-9a-f]{40}|[0-9a-f]{64}', content)
        self.assertIn('revision.slice(0,12)', content)
        self.assertIn('Observed revision ${displayedRevision(revision)}', content)
        self.assertIn('Full observed revision ${revision}', content)
        self.assertIn('overflow-wrap:anywhere', content)
        self.assertIn('word-break:break-word', content)

        snapshot, _, _ = GENERATOR.generate_snapshot(ROOT)
        for revision in ("a" * 40, "B" * 64, "unavailable", "not-a-full-object-id"):
            with self.subTest(revision=revision):
                fixture = {**snapshot, "repository": {**snapshot["repository"], "revision": revision}}
                rendered = GENERATOR.render_dashboard(fixture)
                self.assertIn(f'"revision":"{revision}"', rendered)

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

    def test_graph_analysis_modes_use_stable_distinct_category_colors(self) -> None:
        content = self.template.read_text(encoding="utf-8")
        palette = re.findall(r"--graph-(\d+):([^;]+)", content)
        self.assertEqual([str(index) for index in range(1, 13)], [index for index, _ in palette])
        self.assertEqual(len(palette), len({color for _, color in palette}))
        self.assertIn("SEMANTIC_COLOR_TOKENS=Object.freeze", content)
        self.assertIn("function semanticValueForMode(node,mode)", content)
        self.assertIn("function semanticModePalette(mode)", content)
        self.assertIn("nodes().map(node=>String(semanticValueForMode(node,mode)))", content)
        self.assertIn("semanticPalettes.set(mode,new Map(values.map", content)
        self.assertIn("colors[index]??fallbackSemanticColor(index)", content)
        self.assertNotIn("Math.abs(hash)%semanticPalette.length", content)

    def test_canonical_template_is_the_only_committed_webui_source(self) -> None:
        self.assertTrue(self.template.is_file())
        self.assertTrue(self.canonical.is_file())
        self.assertFalse((ROOT / "templates/webui").exists())
        self.assertEqual([], list(ROOT.rglob("harness-lineage-prototype.html")))

    def test_real_snapshot_matches_documented_top_level_contract(self) -> None:
        snapshot, report, _ = GENERATOR.generate_snapshot(ROOT)
        self.assertTrue(report.valid)
        self.assertEqual(GENERATOR.SNAPSHOT_SCHEMA, snapshot["schema"])
        self.assertEqual("harness-findings-v7", snapshot["finding_rules_version"])
        self.assertEqual(
            {
                "schema",
                "finding_rules_version",
                "quality_gates_version",
                "repository",
                "artifacts",
                "relations",
                "diagnostics",
                "findings",
                "coverage",
                "readiness",
                "revision_provenance",
                "revision_policy",
                "experiments",
                "evidence",
            },
            set(snapshot),
        )
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

    def test_temporal_reassessment_supports_only_governed_declared_dependencies(self) -> None:
        supported = {
            "capability": ("derives_from",),
            "requirement": ("derives_from",),
            "specification": ("specifies",),
            "architecture": ("addresses", "conforms_to", "constrains"),
            "adr": ("decides",),
            "verification": ("verifies",),
            "release_contract": ("gates",),
            "operating_contract": ("assures",),
        }
        for source_type, relation_names in supported.items():
            for relation_name in relation_names:
                with self.subTest(source_type=source_type, relation=relation_name):
                    findings = temporal_findings(
                        source_type=source_type,
                        source_status="implemented",
                        relation_name=relation_name,
                    )
                    self.assertEqual(1, len(findings))

        for relation_name in ("implements", "specifications", "architecture", "verification"):
            with self.subTest(work_order_relation=relation_name):
                self.assertEqual(
                    1,
                    len(
                        temporal_findings(
                            source_type="work_order",
                            source_status="approved",
                            relation_name=relation_name,
                        )
                    ),
                )

        for status in ("draft", "approved", "in_progress"):
            with self.subTest(work_order_status=status):
                self.assertEqual(
                    1,
                    len(
                        temporal_findings(
                            source_type="work_order",
                            source_status=status,
                            relation_name="verification",
                        )
                    ),
                )

    def test_temporal_reassessment_excludes_history_and_unsupported_edges(self) -> None:
        cases = [
            ("work_order", "implemented", "verification", "declared", "2026-08-01", "2026-08-02"),
            ("work_order", "verified", "implements", "declared", "2026-08-01", "2026-08-02"),
            ("work_order", "released", "implements", "declared", "2026-08-01", "2026-08-02"),
            ("work_order", "rejected", "implements", "declared", "2026-08-01", "2026-08-02"),
            ("work_order", "superseded", "implements", "declared", "2026-08-01", "2026-08-02"),
            ("verification_record", "ready", "verification", "declared", "2026-08-01", "2026-08-02"),
            ("verification_record", "verified", "verification", "declared", "2026-08-01", "2026-08-02"),
            ("verification_record", "released", "verification", "declared", "2026-08-01", "2026-08-02"),
            ("verification_record", "superseded", "superseded_by", "declared", "2026-08-01", "2026-08-02"),
            ("release_record", "ready", "release_contract", "declared", "2026-08-01", "2026-08-02"),
            ("release_record", "released", "verification_records", "declared", "2026-08-01", "2026-08-02"),
            ("architecture", "rejected", "conforms_to", "declared", "2026-08-01", "2026-08-02"),
            ("architecture", "superseded", "conforms_to", "declared", "2026-08-01", "2026-08-02"),
            ("architecture", "implemented", "conforms_transitively_to_requirement", "derived", "2026-08-01", "2026-08-02"),
            ("architecture", "implemented", "future_relation", "declared", "2026-08-01", "2026-08-02"),
            ("architecture", "implemented", "conforms_to", "declared", "2026-08-02", "2026-08-02"),
            ("architecture", "implemented", "conforms_to", "declared", "2026-08-03", "2026-08-02"),
            ("architecture", "implemented", "conforms_to", "declared", "", "2026-08-02"),
            ("architecture", "implemented", "conforms_to", "declared", "2026-08-01", ""),
            ("architecture", "implemented", "conforms_to", "derived", "2026-08-01", "2026-08-02"),
            ("future_control", "implemented", "conforms_to", "declared", "2026-08-01", "2026-08-02"),
        ]
        for case in cases:
            with self.subTest(case=case):
                self.assertEqual(
                    [],
                    temporal_findings(
                        source_type=case[0],
                        source_status=case[1],
                        relation_name=case[2],
                        authority=case[3],
                        source_updated=case[4],
                        target_updated=case[5],
                    ),
                )

        self.assertEqual(
            [],
            temporal_findings(
                source_type="architecture",
                source_status="implemented",
                relation_name="conforms_to",
                target_exists=False,
            ),
        )

    def test_temporal_reassessment_identifies_relation_and_preserves_contract(self) -> None:
        findings = temporal_findings(
            source_type="architecture",
            source_status="implemented",
            relation_name="conforms_to",
            relation_count=2,
        )
        self.assertEqual(
            [
                {
                    "rule": "W-HEX-003",
                    "severity": "warning",
                    "message": "SOURCE-001 predates newer declared conforms_to target TARGET-001 and may require reassessment.",
                    "artifacts": ["SOURCE-001", "TARGET-001"],
                    "paths": ["docs/engineering/source.md", "docs/engineering/target.md"],
                    "evidence": ["2026-08-01 < 2026-08-02", "relation=conforms_to"],
                    "authority": "derived",
                }
            ],
            findings,
        )

    def test_only_the_explicitly_accepted_runtime_url_is_present(self) -> None:
        content = self.template.read_text(encoding="utf-8")
        self.assertEqual(1, content.count("https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js"))
        self.assertIn("script-src 'unsafe-inline' https://unpkg.com", content)
        self.assertIn("connect-src 'none'", content)
        self.assertNotIn("integrity=", content)


if __name__ == "__main__":
    unittest.main()
