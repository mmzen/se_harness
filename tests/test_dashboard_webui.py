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
CANDIDATE_SCRIPTS = ROOT / "templates/repository/standard/scripts"
MANAGED_GENERATOR = ROOT / "scripts/generate_harness_dashboard.py"
if str(CANDIDATE_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(CANDIDATE_SCRIPTS))

VALIDATOR_SPEC = importlib.util.spec_from_file_location(
    "dashboard_webui_validator",
    CANDIDATE_SCRIPTS / "validate_engineering_artifacts.py",
)
if VALIDATOR_SPEC is None or VALIDATOR_SPEC.loader is None:
    raise RuntimeError("candidate validator is unavailable")
CANDIDATE_VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
sys.modules[VALIDATOR_SPEC.name] = CANDIDATE_VALIDATOR
VALIDATOR_SPEC.loader.exec_module(CANDIDATE_VALIDATOR)

GENERATOR_SPEC = importlib.util.spec_from_file_location(
    "dashboard_webui_generator",
    CANDIDATE_SCRIPTS / "generate_harness_dashboard.py",
)
if GENERATOR_SPEC is None or GENERATOR_SPEC.loader is None:
    raise RuntimeError("dashboard generator is unavailable")
GENERATOR = importlib.util.module_from_spec(GENERATOR_SPEC)
sys.modules[GENERATOR_SPEC.name] = GENERATOR
_prior_validator = sys.modules.get("validate_engineering_artifacts")
sys.modules["validate_engineering_artifacts"] = CANDIDATE_VALIDATOR
try:
    GENERATOR_SPEC.loader.exec_module(GENERATOR)
finally:
    if _prior_validator is None:
        sys.modules.pop("validate_engineering_artifacts", None)
    else:
        sys.modules["validate_engineering_artifacts"] = _prior_validator

INSPECTOR_SPEC = importlib.util.spec_from_file_location(
    "dashboard_webui_inspector",
    CANDIDATE_SCRIPTS / "inspect_engineering_artifacts.py",
)
if INSPECTOR_SPEC is None or INSPECTOR_SPEC.loader is None:
    raise RuntimeError("candidate inspector is unavailable")
INSPECTOR = importlib.util.module_from_spec(INSPECTOR_SPEC)
sys.modules[INSPECTOR_SPEC.name] = INSPECTOR
_prior_generator = sys.modules.get("generate_harness_dashboard")
_prior_validator = sys.modules.get("validate_engineering_artifacts")
sys.modules["generate_harness_dashboard"] = GENERATOR
sys.modules["validate_engineering_artifacts"] = CANDIDATE_VALIDATOR
try:
    INSPECTOR_SPEC.loader.exec_module(INSPECTOR)
finally:
    if _prior_generator is None:
        sys.modules.pop("generate_harness_dashboard", None)
    else:
        sys.modules["generate_harness_dashboard"] = _prior_generator
    if _prior_validator is None:
        sys.modules.pop("validate_engineering_artifacts", None)
    else:
        sys.modules["validate_engineering_artifacts"] = _prior_validator


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

    def test_candidate_topology_target_is_independent_from_the_managed_root(self) -> None:
        candidate_text = (CANDIDATE_SCRIPTS / "generate_harness_dashboard.py").read_text(
            encoding="utf-8"
        )
        managed_text = MANAGED_GENERATOR.read_text(encoding="utf-8")
        self.assertEqual(2_097_152, GENERATOR.TOPOLOGY_ACCEPTANCE_BYTES)
        self.assertIn("TOPOLOGY_ACCEPTANCE_BYTES = 2_097_152", candidate_text)
        self.assertIn("TOPOLOGY_ACCEPTANCE_BYTES = 2_097_152", managed_text)
        # The candidate evolves ahead of the released root copy between
        # adoptions; only the topology target must not regress on either side.
        self.assertIn("MAX_INDEX_BYTES = 524_288", candidate_text)

    def test_topology_target_boundary_is_strict_and_bounded(self) -> None:
        target = GENERATOR.TOPOLOGY_ACCEPTANCE_BYTES
        for topology_bytes, expected in (
            (target - 1, False),
            (target, False),
            (target + 1, True),
        ):
            with self.subTest(topology_bytes=topology_bytes):
                self.assertEqual(expected, GENERATOR.topology_target_exceeded(topology_bytes))

    def test_candidate_reports_closed_release_chain_conflicts_without_automatic_action(self) -> None:
        def artifact(artifact_id: str, artifact_type: str, status: str) -> dict:
            return {
                "id": artifact_id,
                "type": artifact_type,
                "status": status,
                "updated": "2026-08-21",
                "path": f"docs/engineering/test/{artifact_id}.md",
            }

        artifacts = [
            artifact("WO-TST-001", "work_order", "implemented"),
            artifact("REL-TST-001", "release_contract", "approved"),
            artifact("REL-TST-002", "release_contract", "approved"),
            artifact("VREC-TST-001", "verification_record", "ready"),
            artifact("VREC-TST-002", "verification_record", "ready"),
            artifact("RLS-TST-001", "release_record", "ready"),
            artifact("RLS-TST-002", "release_record", "draft"),
        ]
        relations = [
            {
                "source": contract,
                "relation": "gates",
                "target": "WO-TST-001",
                "authority": "declared",
                "target_exists": True,
            }
            for contract in ("REL-TST-001", "REL-TST-002")
        ]

        def revision(
            artifact_id: str,
            kind: str,
            status: str,
            commit: str,
            *,
            version: str | None = None,
            contracts: list[str] | None = None,
        ) -> dict:
            return {
                "id": artifact_id,
                "kind": kind,
                "status": status,
                "commit": commit,
                "commit_available": None,
                "match_state": "not_assessable",
                "work_orders": ["WO-TST-001"],
                "contracts": contracts or [],
                "superseded_by": [],
                "version": version,
            }

        revisions = [
            revision("VREC-TST-001", "verification", "ready", "a" * 40),
            revision("VREC-TST-002", "verification", "ready", "b" * 40),
            revision(
                "RLS-TST-001",
                "release",
                "ready",
                "a" * 40,
                version="1.2.3",
                contracts=["REL-TST-001"],
            ),
            revision(
                "RLS-TST-002",
                "release",
                "draft",
                "b" * 40,
                version="1.2.3",
                contracts=["REL-TST-002"],
            ),
        ]
        before = json.dumps({"artifacts": artifacts, "relations": relations, "revisions": revisions}, sort_keys=True)
        first = GENERATOR.build_findings(
            artifacts,
            relations,
            [],
            {"WO-TST-001": ["retained"]},
            revisions,
            {"required_for_release": False},
        )
        second = GENERATOR.build_findings(
            artifacts,
            relations,
            [],
            {"WO-TST-001": ["retained"]},
            revisions,
            {"required_for_release": False},
        )
        selected = [item for item in first if item["rule"].startswith("W-REB-")]
        self.assertEqual(first, second)
        self.assertEqual(before, json.dumps({"artifacts": artifacts, "relations": relations, "revisions": revisions}, sort_keys=True))
        self.assertEqual({"W-REB-001", "W-REB-002", "W-REB-003"}, {item["rule"] for item in selected})
        suggestions = INSPECTOR._build_suggestions(
            {
                "decision_required": [],
                "definition_pending": [],
                "active_work": [],
                "assurance_pending": [],
            },
            selected,
        )
        self.assertEqual(3, len(suggestions))
        self.assertTrue(all(item["automatic"] is False for item in suggestions))

    def test_canonical_template_is_the_self_contained_designed_explorer(self) -> None:
        content = self.canonical.read_text(encoding="utf-8")
        # The candidate managed UI evolves in the distribution template. The
        # root copy remains owned by the exact released self-hosting evaluator
        # until the next adoption replaces it.
        self.assertTrue(self.template.read_text(encoding="utf-8"))
        self.assertEqual(1, content.count("__HARNESS_BOOTSTRAP_JSON__"))
        self.assertIn(
            '<script id="harness-dashboard-bootstrap" type="application/json">__HARNESS_BOOTSTRAP_JSON__</script>',
            content,
        )
        self.assertEqual(3, content.count("<script"))
        self.assertIn(
            "content=\"default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline' 'unsafe-eval'; "
            "img-src data:; connect-src 'self'; font-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'\"",
            content,
        )
        for view in ("Overview", "Lineage View", "Graph"):
            with self.subTest(view=view):
                self.assertIn(f'<dc-import name="{view}"', content)
        for component in ("./Overview.dc.html", "./Lineage%20View.dc.html", "./Graph.dc.html", "./Record.dc.html"):
            with self.subTest(component=component):
                self.assertIn(f'"{component}": new Blob([', content)
        self.assertIn('<sc-if value="{{isReadiness}}"', content)
        self.assertIn("window.HarnessExplorer = Object.freeze({", content)
        # Component sources are embedded as JSON string literals, so their quotes are escaped.
        self.assertIn('href=\\"?view=readiness\\"', content)
        self.assertIn("harness-dashboard-snapshot-v1", GENERATOR.SNAPSHOT_SCHEMA)
        self.assertIn('cache: "no-cache"', content)
        self.assertIn('crypto.subtle.digest("SHA-256", bytes)', content)
        self.assertIn('if (location.protocol === "file:")', content)
        literals = set(re.findall(r"https?://[^\"'` )]+", content))
        self.assertEqual(
            {
                "http://www.w3.org/1998/Math/MathML",
                "http://www.w3.org/1999/xhtml",
                "http://www.w3.org/1999/xlink",
                "http://www.w3.org/2000/svg",
                "http://www.w3.org/XML/1998/namespace",
                "https://reactjs.org/docs/error-decoder.html?invariant=",
            },
            literals,
            "the template may name only XML namespaces and React's error pointer, never a fetched origin",
        )
        for forbidden in (
            "<script src=",
            "<link ",
            "googleapis",
            "jsdelivr",
            "unpkg",
            "3d-force-graph",
            "localStorage",
            "sessionStorage",
            "@import",
            "WebSocket(",
            "generatedAt",
            "Show complete graph",
            "Active coverage",
            "Rationale.dc.html",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, content)
        self.assertLessEqual(len(content.encode("utf-8")), GENERATOR.MAX_INDEX_BYTES)

    def test_canonical_template_reproduces_from_its_design_sources(self) -> None:
        from repository_tools.explorer_design import build_explorer_template as builder

        built = builder.build()
        self.assertEqual(built, self.canonical.read_text(encoding="utf-8").replace("\r\n", "\n"))
        self.assertEqual(builder.MAX_TEMPLATE_BYTES, GENERATOR.MAX_INDEX_BYTES)
        self.assertEqual(524_288, GENERATOR.MAX_INDEX_BYTES)
        for name in builder.VIEWS:
            source = (builder.SOURCES / f"{name}.dc.html").read_text(encoding="utf-8")
            with self.subTest(source=name):
                self.assertIn("class Component extends DCLogic", source)

    def test_distribution_table_admits_only_scalar_fields(self) -> None:
        table = GENERATOR._distribution_table(
            {
                "wheel": "se_harness-1.0.0-py3-none-any.whl",
                "schema": 2,
                "nested": {"x": 1},
                "flag": True,
                "Bad Key": "x",
                "too_long": "x" * 600,
                "wheel_sha256": "a" * 64,
            }
        )
        self.assertEqual({"schema": 2, "wheel": "se_harness-1.0.0-py3-none-any.whl", "wheel_sha256": "a" * 64}, table)
        self.assertIsNone(GENERATOR._distribution_table("python-wheel-sdist"))
        self.assertIsNone(GENERATOR._distribution_table({"nested": {}}))

    def test_github_remote_normalizes_to_one_public_url(self) -> None:
        for spelling in (
            "https://github.com/mmzen/se_harness.git",
            "https://github.com/mmzen/se_harness/",
            "git@github.com:mmzen/se_harness.git",
            "ssh://git@github.com/mmzen/se_harness",
        ):
            with self.subTest(spelling=spelling):
                match = GENERATOR.GITHUB_REMOTE.match(spelling)
                self.assertIsNotNone(match)
                self.assertEqual(("mmzen", "se_harness"), (match.group("owner"), match.group("name")))
        for rejected in ("https://gitlab.com/mmzen/se_harness.git", "https://github.com/mmzen/se_harness/tree/main", "file:///tmp/repo"):
            with self.subTest(rejected=rejected):
                self.assertIsNone(GENERATOR.GITHUB_REMOTE.match(rejected))

    def test_explorer_metrics_restate_lifecycle_and_release_facts(self) -> None:
        def event(source: str, target: str, at: str, actor: str) -> dict:
            return {"from": source, "to": target, "decided_at": at, "decided_by": actor, "reason": "recorded"}

        snapshot = {
            "artifacts": [
                {
                    "id": "WO-TST-001",
                    "type": "work_order",
                    "status": "implemented",
                    "lifecycle_events": [
                        event("draft", "approved", "2026-08-01T10:00:00Z", "repository-owner"),
                        event("approved", "in_progress", "2026-08-01T10:10:00Z", "delegated-executor"),
                        event("in_progress", "implemented", "2026-08-01T11:30:00Z", "delegated-executor"),
                    ],
                },
                {
                    "id": "VREC-TST-001",
                    "type": "verification_record",
                    "status": "verified",
                    "prepared_by": "delegated-executor",
                    "lifecycle_events": [event("ready", "verified", "2026-08-01T12:00:00Z", "")],
                },
                {
                    "id": "REL-TST-001",
                    "type": "release_contract",
                    "status": "approved",
                    "lifecycle_events": [event("draft", "approved", "2026-08-01T09:00:00Z", "release-owner")],
                },
                {"id": "RLS-TST-001", "type": "release_record", "status": "released", "version": "1.0.0", "released_at": "2026-08-01T13:00:00Z", "commit": "a" * 40},
                {"id": "RLS-TST-000", "type": "release_record", "status": "released", "version": "0.9.0", "released_at": "2026-07-01T13:00:00Z", "commit": "b" * 40},
            ],
            "relations": [
                {"source": "RLS-TST-001", "relation": "releases_work", "target": "WO-TST-001", "authority": "declared", "target_exists": True},
                {"source": "RLS-TST-001", "relation": "satisfies", "target": "REL-TST-001", "authority": "declared", "target_exists": True},
                {"source": "RLS-TST-001", "relation": "includes_verification", "target": "VREC-TST-001", "authority": "declared", "target_exists": True},
                {"source": "VREC-TST-001", "relation": "verifies_work_order", "target": "WO-TST-001", "authority": "declared", "target_exists": True},
                {"source": "RLS-TST-000", "relation": "releases_work", "target": "WO-TST-000", "authority": "declared", "target_exists": False},
            ],
        }
        metrics = GENERATOR.build_explorer_metrics(snapshot)
        self.assertEqual(metrics, GENERATOR.build_explorer_metrics(snapshot))
        self.assertEqual(
            {
                "lifecycle_events": 5,
                "unattributed_events": 1,
                "decided_by": {"delegated-executor": 2, "release-owner": 1, "repository-owner": 1},
                "delegated_transitions": 2,
                "delegated_records": 1,
                "delegated_artifacts": ["VREC-TST-001", "WO-TST-001"],
                "lead_times": [{"id": "WO-TST-001", "hours": 1.5}],
                "released_work_orders": 2,
                "released_work_orders_verified": 1,
                "latest_release": {
                    "id": "RLS-TST-001",
                    "version": "1.0.0",
                    "released_at": "2026-08-01T13:00:00Z",
                    "commit": "a" * 40,
                    "verification_record": "VREC-TST-001",
                },
                "release_arc": {
                    "contract_id": "REL-TST-001",
                    "contract_approved_at": "2026-08-01T09:00:00Z",
                    "released_at": "2026-08-01T13:00:00Z",
                    "hours": 4.0,
                },
            },
            metrics,
        )
        self.assertEqual(
            {"lifecycle_events": 0, "unattributed_events": 0, "decided_by": {}, "delegated_transitions": 0, "delegated_records": 0, "delegated_artifacts": [], "lead_times": [], "released_work_orders": 0, "released_work_orders_verified": 0, "latest_release": None, "release_arc": None},
            GENERATOR.build_explorer_metrics({"artifacts": [], "relations": []}),
        )

    def test_release_proof_fields_reach_the_summary_and_compact_topology(self) -> None:
        snapshot, report, _ = GENERATOR.generate_snapshot(ROOT)
        self.assertTrue(report.valid)
        self.assertNotIn("metrics", snapshot)
        released = [item for item in snapshot["artifacts"] if item["type"] == "release_record" and item.get("distribution")]
        self.assertTrue(released)
        for item in released:
            with self.subTest(record=item["id"]):
                self.assertRegex(item["distribution"]["wheel_sha256"], r"^[0-9a-f]{64}$")
                self.assertRegex(item["evaluator_evidence_sha256"], r"^[0-9a-f]{64}$")
        _, manifest, resources, _ = GENERATOR.build_dashboard_bundle(snapshot)
        summary = json.loads(resources[manifest["entrypoints"]["summary"]["path"]])
        metrics = summary["metrics"]
        self.assertEqual(metrics, GENERATOR.build_explorer_metrics(snapshot))
        self.assertEqual(0, metrics["unattributed_events"])
        self.assertEqual(metrics["released_work_orders"], metrics["released_work_orders_verified"])
        self.assertEqual([item["hours"] for item in metrics["lead_times"]], sorted(item["hours"] for item in metrics["lead_times"]))
        self.assertEqual("https://github.com/mmzen/se_harness", summary["repository"].get("source_url"))
        topology = json.loads(resources[manifest["entrypoints"]["topology"]["path"]])
        rows = {item["id"]: item for item in topology["artifacts"]}
        record = rows[metrics["latest_release"]["id"]]
        self.assertEqual(metrics["latest_release"]["version"], record["version"])
        self.assertEqual(metrics["latest_release"]["released_at"], record["released_at"])
        self.assertRegex(record["distribution"]["wheel_sha256"], r"^[0-9a-f]{64}$")
        self.assertTrue(all(isinstance(item.get("path"), str) for item in topology["artifacts"]))
        self.assertTrue(all("version" not in item for item in topology["artifacts"] if item["type"] != "release_record"))
        self.assertNotIn('"markdown"', resources[manifest["entrypoints"]["topology"]["path"]])

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
        for route_marker in (
            'history.pushState(null,"",route)',
            'history.replaceState(null,"",route)',
            'window.addEventListener("popstate",applyRoute)',
            'location.hash',
            'new URLSearchParams(query||"")',
            'function decodeRoutePart(value){try{return decodeURIComponent(value);}catch{return null;}}',
            '`#lineage/${encodeURIComponent(selectedId)}`',
            '`#readiness/subject/${encodeURIComponent(currentSubject.id)}`',
            '`#readiness?gate=${encodeURIComponent(gateSelection.id)}&state=${encodeURIComponent(gateSelection.state)}`',
        ):
            with self.subTest(route_marker=route_marker):
                self.assertIn(route_marker, content)
        self.assertIn('resetLineageHistory(selectedId);}applyRoute();renderOverviewGraph();', content)
        self.assertNotIn('decodeURIComponent(parts[1])', content)
        self.assertNotIn('decodeURIComponent(parts[2])', content)
        for forbidden in ("localStorage", "sessionStorage", "document.cookie"):
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
        self.assertEqual("harness-findings-v9", snapshot["finding_rules_version"])
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
        self.assertIn("this.KIND[n.type] || n.type", rendered)
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
        self.assertEqual(3, rendered.count("<script"))
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
        self.assertIn("data-integrity", content)
        self.assertIsNone(re.search(r"<script\b[^>]*\sintegrity\s*=", content, re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
