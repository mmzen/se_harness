"""Run with the installed service dependencies; these do not replace live scenarios."""
import unittest

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


if __name__ == "__main__":
    unittest.main()
