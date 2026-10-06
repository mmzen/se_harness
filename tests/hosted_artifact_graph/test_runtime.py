"""Run with the installed service dependencies; these do not replace live scenarios."""
import asyncio
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from hosted_artifact_graph.cypher import compile_query
from hosted_artifact_graph.protocol import EVALUATOR, Refusal, Wire


class ReadAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = {"revisions": {"REQ-DEMO-001": {"revision_id": "sha256:" + "1" * 64}},
                         "baseline": {"baseline_id": "selected-baseline"}, "context": None}
        self.budget = {"rows": 10, "bytes": 20000, "depth": 3}

    def compile(self, query, parameters=None):
        return compile_query(query, parameters or {}, self.snapshot, self.budget, "project")

    def test_parsed_literals_comments_and_case_cannot_grant_syntax(self):
        result = self.compile("mAtCh (r:Revision) /* CREATE is inert here */ WHERE r.artifact_id = $id RETURN r.artifact_id AS id LIMIT 5",
                              {"id": "'; CREATE (:Leak) //"})
        self.assertNotIn("Leak", result.cypher)
        self.assertEqual(result.parameters["id"], "'; CREATE (:Leak) //")
        self.assertEqual(result.parameters["__revisions"], ["sha256:" + "1" * 64])
        self.assertEqual(result.columns, ["id"])
        self.compile("MATCH (r:Revision) WHERE r.status = 'CREATE' RETURN r LIMIT 2")

    def test_unsupported_constructs_refuse_before_database_execution(self):
        queries = ["MATCH (n:Revision) DELETE n RETURN n LIMIT 2", "CALL db.labels()", "MATCH (n:Operation) RETURN n LIMIT 2",
                   "MATCH (n:Revision) RETURN n LIMIT 2; CREATE (:Leak)", "MATCH (n:Revision) RETURN n.schema_json LIMIT 2",
                   "MATCH (n:Revision) WHERE EXISTS { MATCH (a) } RETURN n LIMIT 2", "LOAD CSV FROM 'file:///x' AS x RETURN x",
                   "MATCH (n:Revision) RETURN n[$field] LIMIT 2", "MATCH (n:Revision) RETURN labels(n) LIMIT 2",
                   "MATCH (n:Revision) RETURN n", "MATCH (n:Revision) RETURN n LIMIT 0"]
        for query in queries:
            with self.subTest(query=query), self.assertRaises(Refusal):
                self.compile(query)

    def test_depth_and_budget_are_explicit(self):
        self.compile("MATCH (r:Revision)-[e:DECLARES*1..3]->(a:Artifact) RETURN a.artifact_id LIMIT 20")
        with self.assertRaises(Refusal):
            self.compile("MATCH (r:Revision)-[e:DECLARES*1..4]->(a:Artifact) RETURN a LIMIT 10")


class ImportAdmissionTests(unittest.TestCase):
    def test_parser_failure_fits_client_bound_without_unrelated_catalog(self):
        from hosted_artifact_graph.evaluator import BRIDGE

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifacts = root / "docs/engineering/requirements"
            artifacts.mkdir(parents=True)
            for number in range(4):
                document = ('+++\nid = "REQ-DEMO-%03d"\ntype = "requirement"\n'
                            'title = "Large valid metadata"\nstatus = "draft"\n'
                            'statement = "%s"\n+++\n\n# Requirement\n') % (number + 1, "x" * 600000)
                (artifacts / ("REQ-DEMO-%03d.md" % (number + 1))).write_text(document, encoding="utf-8")
            broken = artifacts / "REQ-DEMO-005.md"
            broken.write_text('+++\nid = "REQ-DEMO-005"\nbroken = [\n+++\n', encoding="utf-8")
            argv = ["/opt/evaluator/bin/python", "-I", "-B", str(BRIDGE), "catalog", str(root)]
            result = subprocess.run(argv, capture_output=True, check=True, timeout=30)
            self.assertLess(len(result.stdout), 2 * 1024 * 1024)
            failed = json.loads(result.stdout)
            self.assertTrue(failed["errors"])
            self.assertEqual(failed["artifacts"], [])
            broken.unlink()
            result = subprocess.run(argv, capture_output=True, check=True, timeout=30)
            valid = json.loads(result.stdout)
            self.assertEqual(valid["errors"], [])
            self.assertEqual(len(valid["artifacts"]), 4)
            self.assertTrue(all(len(a["metadata"]["statement"]) == 600000 for a in valid["artifacts"]))

    def test_unsupported_source_is_distinct_from_missing_command_inputs(self):
        wire = Wire()
        for source in ({"schema": "explorer-export", "nodes": [], "edges": []},
                       {"schema": "se-harness-source-manifest/v1", "source": {"kind": "worktree"}, "artifacts": []}):
            with self.subTest(source=source), self.assertRaises(Refusal) as caught:
                wire.command({"operation": "import", "source_manifest": source})
            self.assertEqual((422, "HAG_REMOTE_INVALID_IMPORT"), (caught.exception.status, caught.exception.code))
        with self.assertRaises(Refusal) as caught:
            wire.command({"operation": "import"})
        self.assertEqual((400, "HAG_REMOTE_MALFORMED"), (caught.exception.status, caught.exception.code))


class MCPDiscoveryTests(unittest.TestCase):
    def test_large_partial_result_keeps_metadata_readable_in_a_saved_file(self):
        from mcp.types import CallToolRequest, CallToolRequestParams
        from hosted_artifact_graph.app import PRINCIPAL, create_app

        request = {"schema": "se-harness-graph-read/v1", "operation": "impact",
                   "project_id": "11111111-1111-4111-8111-111111111111",
                   "view": {"kind": "baseline", "baseline_id": "se-harness-artifact-baseline/v1:sha256:" + "1" * 64},
                   "budget": {"rows": 500, "bytes": 2097152, "depth": 8}, "artifact_id": "CAP-DEMO-001"}
        response = {"schema": request["schema"], "operation": "impact", "project_id": request["project_id"],
                    "view": request["view"], "complete": False,
                    "continuation": {"reason": "row_limit", "strategy": "repeat_at_same_view_with_narrower_selection"},
                    "unresolved_references": [], "data": {"artifacts": [{"body": "large é result " * 100} for _ in range(100)]}}
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "config.json"
            config.write_text("{}", encoding="utf-8")
            with patch("hosted_artifact_graph.app.Service", return_value=SimpleNamespace(wire=Wire())), \
                    patch("hosted_artifact_graph.app.StreamableHTTPSessionManager") as manager, \
                    patch("hosted_artifact_graph.app.read", return_value=response):
                create_app(config, config)
                handler = manager.call_args.kwargs["app"].request_handlers[CallToolRequest]
                token = PRINCIPAL.set({"id": "test-reader"})
                try:
                    result = asyncio.run(handler(CallToolRequest(method="tools/call",
                        params=CallToolRequestParams(name="impact", arguments=request))))
                finally:
                    PRINCIPAL.reset(token)
            self.assertFalse(result.root.isError)
            self.assertEqual(len(result.root.content), 1)
            text = result.root.content[0].text
            self.assertEqual(json.loads(text), response)
            self.assertGreater(len(text), 30000)
            self.assertEqual(len(text.encode("utf-8")), len(json.dumps(response, ensure_ascii=False).encode("utf-8")))
            saved = Path(directory) / "saved-response.json"
            saved.write_text(text, encoding="utf-8")
            with saved.open(encoding="utf-8") as stream:
                prefix = "".join(line for _, line in zip(range(10), stream))
            self.assertLess(len(prefix), 4096)
            self.assertIn('"complete": false', prefix)
            self.assertIn('"reason": "row_limit"', prefix)

    def test_advertised_tools_have_object_schemas_and_keep_operation_constraints(self):
        from jsonschema import Draft202012Validator
        from mcp.types import ListToolsRequest
        from hosted_artifact_graph.app import create_app

        wire = Wire()
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "config.json"
            config.write_text("{}", encoding="utf-8")
            with patch("hosted_artifact_graph.app.Service", return_value=SimpleNamespace(wire=wire)), \
                    patch("hosted_artifact_graph.app.StreamableHTTPSessionManager") as manager:
                create_app(config, config)
                server = manager.call_args.kwargs["app"]
                handler = server.request_handlers[ListToolsRequest]
                result = asyncio.run(handler(ListToolsRequest(method="tools/list")))
        tools = result.root.tools
        self.assertEqual({tool.name for tool in tools},
                         {"revision", "work-context", "compare", "impact", "lineage", "check", "cypher"})
        for tool in tools:
            with self.subTest(tool=tool.name):
                # Native MCP clients require the root object type even when an
                # allOf branch already constrains the instance to an object.
                self.assertEqual(tool.inputSchema.get("type"), "object")
                Draft202012Validator.check_schema(tool.inputSchema)
                validator = Draft202012Validator(tool.inputSchema)
                self.assertFalse(validator.is_valid([]))
                self.assertFalse(validator.is_valid({"operation": "approve"}))
                self.assertNotIn("urn:se-harness:remote-wire:v1#", json.dumps(tool.inputSchema))


import base64
from hosted_artifact_graph.canonical import canonical_json


class HostedTestSnapshotTests(unittest.TestCase):
    def test_snapshot_freezes_candidate_inputs_and_bundle_replays_without_branch_override(self):
        from hosted_artifact_graph.pilot_git import initial, snapshot, verify_snapshot, restore
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'original'; root.mkdir()
            (root / 'record.txt').write_bytes(b'exact fixture\r\n')
            initial(root)
            candidates = []
            source = {'commit': 'a' * 40}
            evaluator = {'version': 'released'}
            value = snapshot(root, source=source, evaluator=evaluator, candidates=candidates)
            original = canonical_json(value)
            candidates.append({'new': 'candidate'})
            source['commit'] = 'b' * 40
            evaluator['version'] = 'changed'
            self.assertEqual(original, canonical_json(verify_snapshot(value)))
            replay = Path(directory) / 'replay'; replay.mkdir()
            restore(replay, value)
            self.assertEqual(b'exact fixture\r\n', (replay / 'record.txt').read_bytes())
            self.assertIn(b' HEAD\n', base64.b64decode(value['git_bundle']['content_base64']).split(b'\n\n')[0] + b'\n')

    def test_projection_paths_reject_cross_platform_ambiguity(self):
        from hosted_artifact_graph.pilot_git import safe_path
        from hosted_artifact_graph.protocol import Refusal
        for path in ('../escape', 'a/.git/config', 'C:/escape', 'a\\b', 'a/CON.txt', 'a/trailing.', 'a//b'):
            with self.subTest(path=path), self.assertRaises(Refusal):
                safe_path(path)

if __name__ == "__main__":
    unittest.main()
