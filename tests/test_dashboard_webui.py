from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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
        self.assertEqual(1, content.count("__HARNESS_BOOTSTRAP_JSON__"))
        self.assertIn('id="harness-dashboard-bootstrap"', content)
        self.assertIn('raw.schema!=="harness-dashboard-snapshot-v1"', content)
        self.assertIn('data-current-view="overview"', content)
        self.assertIn('data-view="lineage"', content)
        self.assertIn('data-view="readiness"', content)
        self.assertIn('data-od-id="three-dimensional-graph"', content)
        self.assertIn('data-od-id="graph-color-legend"', content)
        self.assertIn('id="lineageGraph" role="group"', content)
        self.assertIn('data-od-id="lineage-navigation-history"', content)
        self.assertIn('linkDirectionalArrowLength(1.8)', content)
        self.assertIn('clip:rect(0 0 0 0)', content)
        self.assertEqual(1, content.count("function renderLineage(focusTarget=null){"))
        self.assertIn('const GRAPH_SOURCE="https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js"', content)
        self.assertIn('Interactive 3D topology unavailable', content)
        for forbidden in (
            "<script src=",
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
        self.assertIn('coverage:definition?{applicable:true', content)

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

    def test_lineage_board_is_structured_bounded_and_reversibly_navigable(self) -> None:
        content = self.template.read_text(encoding="utf-8")

        self.assertIn('id="lineageDepth"', content)
        self.assertIn('<option value="1">1 - direct relations</option>', content)
        self.assertIn('<option value="2">2 - second-level context</option>', content)
        self.assertIn('LINEAGE_CONTEXT_NODE_LIMIT=100', content)
        self.assertIn('LINEAGE_HISTORY_LIMIT=20', content)
        self.assertIn('const LINEAGE_STAGES=Object.freeze([', content)
        for stage, types in (
            ('id:"purpose",label:"Purpose"', '["intent","capability"]'),
            ('id:"definition",label:"Definition"', '["requirement","specification"]'),
            ('id:"design",label:"Design"', '["architecture","adr"]'),
            ('id:"delivery",label:"Delivery"', '["work_order"]'),
            ('id:"assurance",label:"Assurance"', '["verification","verification_record"]'),
            (
                'id:"release-operation",label:"Release and operation"',
                '["release_contract","release_record","operating_contract"]',
            ),
        ):
            with self.subTest(stage=stage):
                self.assertIn(stage, content)
                self.assertIn(f"types:{types}", content)

        self.assertIn('function lineageScope(root,depth=1)', content)
        self.assertIn('const directRelations=lineageIncident(root.id,true)', content)
        self.assertIn('eligibleSecond.slice(0,LINEAGE_CONTEXT_NODE_LIMIT)', content)
        self.assertIn('function renderLineageEdges()', content)
        self.assertIn('sourceId===scope.root.id||targetId===scope.root.id', content)
        self.assertIn('link.derived?" derived":""', content)
        self.assertIn('Unresolved target ${esc(endpoint(link.target))}', content)
        self.assertIn('data-stage="${esc(group.id)}"', content)
        self.assertIn('Unknown type', content)
        self.assertNotIn('function neighborhood(root,maxDepth=2,maxNodes=9)', content)
        self.assertNotIn('function setLineageZoom', content)
        self.assertNotIn('data-od-id="zoom-in"', content)

        for control in (
            'id="lineageBack"',
            'id="lineageForward"',
            'id="lineageHistory"',
            'id="lineageInitial"',
            'aria-live="polite"',
            'Visited artifacts only - this is not a formal lineage relation.',
        ):
            with self.subTest(control=control):
                self.assertIn(control, content)
        self.assertIn('lineageHistory=lineageHistory.slice(0,lineageHistoryIndex+1)', content)
        self.assertIn('if(lineageHistory.length>LINEAGE_HISTORY_LIMIT)', content)
        self.assertIn('lineageHistory.shift()', content)
        self.assertIn('function revealCurrentLineageHistory(){', content)
        self.assertIn("querySelector('[aria-current=\"true\"]')", content)
        self.assertIn('list.scrollLeft-=listRect.left+margin-currentRect.left', content)
        self.assertIn('list.scrollLeft+=currentRect.right-listRect.right+margin', content)
        self.assertIn('requestAnimationFrame(revealCurrentLineageHistory)', content)
        self.assertNotIn('current.scrollIntoView', content)
        self.assertIn('renderLineage("history")', content)
        self.assertIn('resetLineageHistory(id)', content)
        for forbidden in ("history.pushState", "localStorage", "sessionStorage", "document.cookie"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, content)
        self.assertIn("async function fetchBoundResource", content)
        self.assertIn('crypto.subtle.digest("SHA-256",bytes)', content)

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
                bootstrap, _, _, _ = GENERATOR.build_dashboard_bundle(fixture)
                rendered = GENERATOR.render_dashboard(bootstrap)
                self.assertIn(f'"repository_revision":"{revision}"', rendered)

    def test_semantic_routes_and_authority_boundaries_remain_explicit(self) -> None:
        content = self.template.read_text(encoding="utf-8")
        for retired_phrase in (
            "Why does this exist?",
            "Is the definition covered?",
            "What needs reassessment?",
            "What is inconsistent or unassessable?",
            "Does the harness help?",
        ):
            with self.subTest(retired_phrase=retired_phrase):
                self.assertNotIn(retired_phrase, content)

        for phrase in (
            'data-view="overview"',
            'data-view="lineage"',
            'data-view="readiness"',
            "DERIVED · READ-ONLY",
            "No approval, verification, or release decision is inferred here.",
            "Explorer gate groupings",
            "NAVIGATION LABELS · NOT POLICY",
            "QUALITY_GATES.md",
            "[data-od-id=graph-lens-summary] .lens{grid-template-columns:repeat(2,minmax(0,1fr))",
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
        self.assertEqual("harness-findings-v8", snapshot["finding_rules_version"])
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
                "evidence_documents",
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
        future["repository"] = {**snapshot["repository"], "revision": "a" * 40}
        future["artifacts"] = [*snapshot["artifacts"], {"id": "FUTURE-001", "type": "future_control", "title": "Future control", "status": "draft", "owners": [], "path": "future.md"}]
        bootstrap, manifest, resources, observations = GENERATOR.build_dashboard_bundle(future)
        rendered = GENERATOR.render_dashboard(bootstrap)
        topology = json.loads(resources[manifest["entrypoints"]["topology"]["path"]])
        self.assertTrue(any(item.get("type") == "future_control" for item in topology["artifacts"]))
        self.assertIn("new Option(v,v)", rendered)
        self.assertEqual(GENERATOR.BUNDLE_SCHEMA, manifest["schema"])
        self.assertEqual(len(manifest["resources"]), observations["resource_count"])
        self.assertLessEqual(len(rendered.encode("utf-8")), GENERATOR.MAX_INDEX_BYTES)
        self.assertNotIn("# SE Harness", rendered)

    def test_evidence_discovery_supports_flat_directory_nested_and_multi_key_layouts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = (
                "docs/engineering/example/evidence/WO-AAA-001-check.md",
                "docs/engineering/example/evidence/WO-BBB-002/check.md",
                "docs/engineering/example/evidence/archive/WO-CCC-003/check.md",
                "docs/engineering/example/evidence/WO-ZZZ-009/WO-AAA-001-extra.md",
                "docs/engineering/WO-DDD-004/evidence/check.md",
                "docs/engineering/example/not-evidence/WO-EEE-005.md",
            )
            for relative in paths:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("evidence\n", encoding="utf-8")

            self.assertEqual(
                {
                    "WO-AAA-001": [
                        "docs/engineering/example/evidence/WO-AAA-001-check.md",
                        "docs/engineering/example/evidence/WO-ZZZ-009/WO-AAA-001-extra.md",
                    ],
                    "WO-BBB-002": ["docs/engineering/example/evidence/WO-BBB-002/check.md"],
                    "WO-CCC-003": [
                        "docs/engineering/example/evidence/archive/WO-CCC-003/check.md"
                    ],
                    "WO-ZZZ-009": [
                        "docs/engineering/example/evidence/WO-ZZZ-009/WO-AAA-001-extra.md"
                    ],
                },
                GENERATOR.discover_evidence(root),
            )

    def test_evidence_discovery_does_not_associate_a_symlinked_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "outside.md"
            target.write_text("outside\n", encoding="utf-8")
            link = root / "docs/engineering/example/evidence/WO-LNK-001/check.md"
            link.parent.mkdir(parents=True)
            try:
                link.symlink_to(target)
            except OSError as exc:
                self.skipTest(f"host cannot create test symlink: {exc}")
            self.assertEqual({}, GENERATOR.discover_evidence(root))

    def test_progressive_bundle_is_deterministic_partitioned_and_bounded(self) -> None:
        snapshot, report, _ = GENERATOR.generate_snapshot(ROOT)
        self.assertTrue(report.valid)
        snapshot["repository"] = {**snapshot["repository"], "revision": "a" * 40}
        first = GENERATOR.build_dashboard_bundle(snapshot)
        second = GENERATOR.build_dashboard_bundle(snapshot)
        self.assertEqual(first, second)
        bootstrap, manifest, resources, observations = first

        manifest_bytes = GENERATOR.serialize_json(manifest).encode("utf-8")
        self.assertEqual(GENERATOR.BUNDLE_SCHEMA, manifest["schema"])
        self.assertEqual(hashlib.sha256(manifest_bytes).hexdigest(), bootstrap["manifest"]["sha256"])
        self.assertEqual(len(manifest_bytes), bootstrap["manifest"]["bytes"])
        paths = [item["path"] for item in manifest["resources"]]
        self.assertEqual(sorted(paths), paths)
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(set(paths), set(resources))
        for descriptor in manifest["resources"]:
            encoded = resources[descriptor["path"]].encode("utf-8")
            self.assertEqual(descriptor["bytes"], len(encoded))
            self.assertEqual(descriptor["sha256"], hashlib.sha256(encoded).hexdigest())
            self.assertEqual(descriptor["sha256"], Path(descriptor["path"]).stem)

        summary = json.loads(resources[manifest["entrypoints"]["summary"]["path"]])
        topology = json.loads(resources[manifest["entrypoints"]["topology"]["path"]])
        readiness = json.loads(resources[manifest["entrypoints"]["readiness"]["path"]])
        self.assertNotIn("artifacts", summary)
        self.assertNotIn("relations", summary)
        self.assertEqual({"draft", "ready", "unresolved_relations"}, set(summary["queue_counts"]))
        self.assertTrue(all("content" not in item and "detail" in item for item in topology["artifacts"]))
        self.assertTrue(all(item["authority"] == "formal" for item in topology["artifacts"]))
        self.assertNotIn('"markdown"', resources[manifest["entrypoints"]["topology"]["path"]])
        self.assertNotIn('"markdown"', resources[manifest["entrypoints"]["readiness"]["path"]])
        self.assertEqual(len(snapshot["readiness"]), len(readiness["readiness"]))
        detail_descriptors = [item for item in manifest["resources"] if item["role"] == "artifact"]
        self.assertEqual(len(snapshot["artifacts"]), len(detail_descriptors))
        detail = json.loads(resources[detail_descriptors[0]["path"]])
        self.assertIn("content", detail["artifact"])
        self.assertTrue(all("markdown" not in item for item in detail["evidence_documents"]))
        rendered = GENERATOR.render_dashboard(bootstrap)
        self.assertLessEqual(len(rendered.encode("utf-8")), GENERATOR.MAX_INDEX_BYTES)
        self.assertLessEqual(manifest["entrypoints"]["summary"]["bytes"], GENERATOR.MAX_SUMMARY_BYTES)
        self.assertLessEqual(manifest["entrypoints"]["topology"]["bytes"], GENERATOR.TOPOLOGY_ACCEPTANCE_BYTES)
        self.assertFalse(observations["topology_target_exceeded"])

    def test_progressive_browser_contract_is_verified_lazy_and_race_safe(self) -> None:
        content = self.template.read_text(encoding="utf-8")
        for marker in (
            'redirect:"error",cache:"no-cache"',
            'crypto.subtle.digest("SHA-256",bytes)',
            'response.url,location.href',
            'if(location.protocol==="file:")',
            'async function ensureTopology()',
            'async function ensureReadiness()',
            'async function ensureArtifactDetail(id,generation)',
            'selectedId===id&&selectionGeneration===generation',
            'details[data-evidence-path]',
            'async function ensureEvidence(details)',
            'requestCache=new Map()',
            'verifiedCache=new Map()',
            'data-retry="topology"',
            'async function retryLoad(scope,trigger)',
            'clearVerified(manifest?.entrypoints?.readiness)',
            'clearVerified(node?.detail)',
            'clearVerified(resourceByPath.get(details.dataset.evidencePath))',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)
        self.assertNotIn("localStorage", content)
        self.assertNotIn("sessionStorage", content)

    def test_content_projection_is_additive_bounded_and_deterministic(self) -> None:
        snapshot, report, _ = GENERATOR.generate_snapshot(ROOT)
        parsed = {artifact.artifact_id: artifact for artifact in report.artifacts}
        self.assertTrue(snapshot["artifacts"])
        for projected in snapshot["artifacts"]:
            content = projected["content"]
            source = parsed[projected["id"]]
            expected = source.body.replace("\r\n", "\n").replace("\r", "\n")
            self.assertEqual("markdown", content["format"])
            self.assertEqual("included", content["state"])
            self.assertEqual(expected, content["markdown"])
            self.assertEqual(len(expected.encode("utf-8")), content["bytes"])
            self.assertEqual(hashlib.sha256(expected.encode("utf-8")).hexdigest(), content["sha256"])

        evidence_documents = snapshot["evidence_documents"]
        self.assertEqual(
            sorted(document["path"] for document in evidence_documents),
            [document["path"] for document in evidence_documents],
        )
        for document in evidence_documents:
            self.assertEqual(sorted(set(document["associations"])), document["associations"])
            if document["state"] == "included":
                self.assertEqual(f"content/{document['sha256']}.txt", document["raw_path"])

        budget = GENERATOR.ContentBudget()
        oversized = budget.project("x" * (GENERATOR.MAX_CONTENT_DOCUMENT_BYTES + 1))
        self.assertEqual("omitted", oversized["state"])
        self.assertEqual("document_too_large", oversized["reason"])
        self.assertNotIn("markdown", oversized)

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "dashboard"
            GENERATOR.write_output_transactionally(
                output,
                {"index.html": "ok\n", "content/" + "a" * 64 + ".txt": "raw\n"},
            )
            self.assertEqual("raw\n", (output / "content" / ("a" * 64 + ".txt")).read_text(encoding="utf-8"))

    def test_content_capacity_and_evidence_path_boundaries_fail_closed(self) -> None:
        for size, state in (
            (0, "included"),
            (1, "included"),
            (GENERATOR.MAX_CONTENT_DOCUMENT_BYTES - 1, "included"),
            (GENERATOR.MAX_CONTENT_DOCUMENT_BYTES, "included"),
            (GENERATOR.MAX_CONTENT_DOCUMENT_BYTES + 1, "omitted"),
        ):
            with self.subTest(size=size):
                projected = GENERATOR.ContentBudget().project("x" * size)
                self.assertEqual(state, projected["state"])
                self.assertEqual(size, projected["bytes"])
                if state == "omitted":
                    self.assertEqual("document_too_large", projected["reason"])

        total_budget = GENERATOR.ContentBudget()
        full_document = "x" * GENERATOR.MAX_CONTENT_DOCUMENT_BYTES
        for _ in range(GENERATOR.MAX_CONTENT_TOTAL_BYTES // GENERATOR.MAX_CONTENT_DOCUMENT_BYTES):
            self.assertEqual("included", total_budget.project(full_document)["state"])
        overflow = total_budget.project("x")
        self.assertEqual("omitted", overflow["state"])
        self.assertEqual("total_content_budget_exceeded", overflow["reason"])

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence_root = root / "docs/engineering/example/evidence"
            evidence_root.mkdir(parents=True)
            valid = evidence_root / "WO-TST-001-verification.md"
            valid.write_bytes(b"# Evidence\r\n\r\nExact.\r\n")
            projected = GENERATOR._project_evidence_document(
                root,
                "docs/engineering/example/evidence/WO-TST-001-verification.md",
                ["WO-TST-001", "VREC-TST-001"],
                GENERATOR.ContentBudget(),
            )
            self.assertEqual("included", projected["state"])
            self.assertEqual("# Evidence\n\nExact.\n", projected["markdown"])
            self.assertEqual(["VREC-TST-001", "WO-TST-001"], projected["associations"])

            original_read_bytes = Path.read_bytes

            def read_then_change(path: Path) -> bytes:
                content = original_read_bytes(path)
                if path == valid:
                    path.write_bytes(content + b"changed")
                return content

            with mock.patch.object(Path, "read_bytes", read_then_change):
                changed = GENERATOR._project_evidence_document(
                    root,
                    "docs/engineering/example/evidence/WO-TST-001-verification.md",
                    ["WO-TST-001"],
                    GENERATOR.ContentBudget(),
                )
            self.assertEqual("omitted", changed["state"])
            self.assertEqual("evidence_changed_during_generation", changed["reason"])
            valid.write_bytes(b"# Evidence\r\n\r\nExact.\r\n")

            invalid_utf8 = evidence_root / "WO-TST-002-verification.md"
            invalid_utf8.write_bytes(b"\xff\xfe\x00")
            cases = (
                ("../outside.md", "unsafe_evidence_path"),
                ("docs/engineering/example/evidence/unsupported.html", "unsupported_evidence_format"),
                ("docs/engineering/example/evidence/missing.md", "evidence_unavailable"),
                ("docs/engineering/example/evidence/WO-TST-002-verification.md", "evidence_not_utf8"),
            )
            for path, reason in cases:
                with self.subTest(path=path):
                    omitted = GENERATOR._project_evidence_document(
                        root,
                        path,
                        ["WO-TST-002"],
                        GENERATOR.ContentBudget(),
                    )
                    self.assertEqual("omitted", omitted["state"])
                    self.assertEqual(reason, omitted["reason"])

            link = evidence_root / "WO-TST-003-verification.md"
            try:
                link.symlink_to(valid)
            except OSError:
                pass
            else:
                omitted = GENERATOR._project_evidence_document(
                    root,
                    "docs/engineering/example/evidence/WO-TST-003-verification.md",
                    ["WO-TST-003"],
                    GENERATOR.ContentBudget(),
                )
                self.assertEqual("symlink_not_allowed", omitted["reason"])

    def test_nested_output_failure_preserves_the_previous_dashboard(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            output = parent / "dashboard"
            output.mkdir()
            (output / "index.html").write_text("previous\n", encoding="utf-8")
            with self.assertRaises(GENERATOR.GenerationError):
                GENERATOR.write_output_transactionally(
                    output,
                    {"../escape.txt": "escape\n", "index.html": "replacement\n"},
                )
            self.assertEqual("previous\n", (output / "index.html").read_text(encoding="utf-8"))
            self.assertFalse((parent / "escape.txt").exists())

            with self.assertRaisesRegex(GENERATOR.GenerationError, "collision"):
                GENERATOR.write_output_transactionally(
                    output,
                    {"content/A.txt": "first\n", "content/a.txt": "second\n"},
                )
            self.assertEqual("previous\n", (output / "index.html").read_text(encoding="utf-8"))

    def test_rich_detail_contract_is_local_safe_and_navigable(self) -> None:
        content = self.template.read_text(encoding="utf-8")
        for marker in (
            'id="detailLabels"',
            'detailLabelMarkup("Type",n.type)',
            'detailLabelMarkup("State",n.status)',
            'detailLabelMarkup("Assurance",assurance(n))',
            'n.id+" - "+n.title',
            "function safeMarkdownHref(value)",
            "function sanitizeMarkdownMarkup(markup)",
            "function renderMarkdown(value)",
            "function earsMarkup(statement)",
            "Presentation only, not validation.",
            "Specification coverage",
            "Verification-contract coverage",
            "function artifactReference(id,resolved=true)",
            "visitLineage(artifact.dataset.artifactId)",
            "Open raw evidence",
            "Evidence presence is retained material only",
            "publishing the bundle exposes every declared resource",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)
        for forbidden in (
            'id="detailbadge"',
            "javascript:",
            "data:text/html",
            "marked.min.js",
            "dompurify",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, content.lower())

    def test_renderer_context_escapes_hostile_repository_text(self) -> None:
        hostile = '</script><img src=x onerror="alert(1)">&\u2028\u2029__HARNESS_BOOTSTRAP_JSON__'
        bootstrap = {
            "schema": GENERATOR.BOOTSTRAP_SCHEMA,
            "bundle_schema": GENERATOR.BUNDLE_SCHEMA,
            "repository_revision": hostile,
            "manifest": {"path": "dashboard-manifest.json", "bytes": 1, "sha256": "a" * 64},
        }
        rendered = GENERATOR.render_dashboard(bootstrap)
        self.assertNotIn('</script><img src=x onerror="alert(1)">', rendered)
        self.assertIn("\\u003c/script\\u003e", rendered)
        self.assertIn("\\u0026\\u2028\\u2029__HARNESS_BOOTSTRAP_JSON__", rendered)
        self.assertEqual(2, rendered.count("<script"))
        self.assertNotIn("__HARNESS_BOOTSTRAP_JSON__</script>", rendered)

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
        self.assertIn("connect-src 'self'", content)
        self.assertNotIn("integrity=", content)


if __name__ == "__main__":
    unittest.main()
