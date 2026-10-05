"""One Memgraph store; explicit transactions own all accepted effects."""
from __future__ import annotations

import json
from contextlib import contextmanager

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

from .canonical import canonical_json, named_digest, verify_revision, BASELINE_SCHEME
from .protocol import Refusal, SCHEMA_REVISION, contract_path, require


def text(value):
    return canonical_json(value).decode("utf-8")


class Store:
    def __init__(self, uri, project_id):
        self.project_id = project_id
        self.driver = GraphDatabase.driver(uri, auth=None, max_connection_pool_size=8,
                                          connection_timeout=10, max_transaction_retry_time=0)

    @contextmanager
    def transaction(self, timeout=120):
        with self.driver.session() as session:
            tx = session.begin_transaction(timeout=timeout)
            try:
                yield tx
            finally:
                if not tx.closed():
                    tx.rollback()

    def initialize(self):
        with self.driver.session() as session:
            nodes = session.run("MATCH (n) RETURN count(n) AS count").single()["count"]
            if nodes:
                self.ready()
                return {"initialized": False, "project_id": self.project_id}
            raw = contract_path("graph-v1.cypher").read_text(encoding="utf-8")
            statements = "\n".join(line for line in raw.splitlines() if not line.lstrip().startswith("//"))
            for statement in statements.split(";"):
                if statement.strip():
                    session.run(statement).consume()
            schema = self.schema_inventory(session)
            session.run("CREATE (:Project {project_id:$p, command_version:0, schema_revision:$s, schema_json:$schema})",
                        p=self.project_id, s=SCHEMA_REVISION, schema=text(schema)).consume()
        return {"initialized": True, "project_id": self.project_id}

    @staticmethod
    def schema_inventory(session):
        return {name: sorted([dict(r) for r in session.run(query)], key=text)
                for name, query in (("constraints", "SHOW CONSTRAINT INFO"), ("indexes", "SHOW INDEX INFO"))}

    def ready(self):
        with self.driver.session() as session:
            row = session.run("MATCH (p:Project) RETURN properties(p) AS p").data()
            require(len(row) == 1 and row[0]["p"]["project_id"] == self.project_id, 409,
                    "SCHEMA_MISMATCH", "Store is uninitialized or selects another project.")
            p = row[0]["p"]
            require(p["schema_revision"] == SCHEMA_REVISION and p.get("schema_json") == text(self.schema_inventory(session)),
                    409, "SCHEMA_MISMATCH", "Store schema does not match initialized revision 1.")
            return p["command_version"]

    def project(self, tx):
        row = tx.run("MATCH (p:Project {project_id:$p}) RETURN properties(p) AS p", p=self.project_id).single()
        require(row is not None and row["p"]["schema_revision"] == SCHEMA_REVISION, 409,
                "SCHEMA_MISMATCH", "Missing compatible project schema.")
        return row["p"]

    def operation(self, tx, principal, key):
        row = tx.run("MATCH (o:Operation {project_id:$p, principal_id:$a, operation_key:$k}) "
                     "RETURN o.request_sha256 AS digest, o.result_json AS result",
                     p=self.project_id, a=principal, k=key).single()
        return (row["digest"], json.loads(row["result"])) if row else None

    def baseline(self, tx, identity):
        row = tx.run("MATCH (b:Baseline {project_id:$p, baseline_id:$b}) RETURN b.manifest_json AS manifest",
                     p=self.project_id, b=identity).single()
        require(row is not None, 404, "UNKNOWN_IDENTITY", "Unknown selected baseline.")
        manifest = json.loads(row["manifest"])
        require(identity == BASELINE_SCHEME + ":sha256:" + named_digest(BASELINE_SCHEME, manifest),
                422, "INCOMPLETE_SELECTION", "Stored baseline content differs from its identity.")
        edges = tx.run("MATCH (b:Baseline {project_id:$p, baseline_id:$b})-[:SELECTS]->(r:Revision) "
                       "RETURN r.artifact_id AS id, r.revision_id AS revision", p=self.project_id, b=identity).data()
        require(len(edges) == len(manifest["selection"]) and {e["id"]: e["revision"] for e in edges} == manifest["selection"],
                422, "INCOMPLETE_SELECTION", "Baseline edges differ from its canonical manifest.")
        return {"schema": BASELINE_SCHEME, "baseline_id": identity, "manifest": manifest}

    def revisions(self, tx, selection):
        rows = tx.run("MATCH (r:Revision {project_id:$p}) WHERE r.revision_id IN $ids "
                      "RETURN r.revision_id AS id, r.envelope_json AS envelope, r.document_base64 AS document",
                      p=self.project_id, ids=list(selection.values())).data()
        values = {}
        for row in rows:
            stored = verify_revision({"revision_id": row["id"], "envelope": json.loads(row["envelope"]),
                                      "document_base64": row["document"]})
            values[stored["envelope"]["artifact_id"]] = stored
        require({a: r["revision_id"] for a, r in values.items()} == selection, 422,
                "INCOMPLETE_SELECTION", "Selected revision content is missing.")
        declared = tx.run("MATCH (r:Revision {project_id:$p})-[e:DECLARES]->(a:Artifact) "
                          "WHERE r.revision_id IN $ids RETURN r.revision_id AS r, e.kind AS k, "
                          "e.target_artifact_id AS t, a.artifact_id AS a, a.project_id AS p",
                          p=self.project_id, ids=list(selection.values())).data()
        known = set(tx.run("MATCH (a:Artifact {project_id:$p}) RETURN a.artifact_id AS id", p=self.project_id).value())
        expected = {(r["revision_id"], k, target) for r in values.values()
                    for k, targets in r["envelope"]["declared_relations"].items() for target in targets if target in known}
        observed = {(e["r"], e["k"], e["t"]) for e in declared}
        require(all(e["p"] == self.project_id and e["a"] == e["t"] for e in declared)
                and observed == expected and len(declared) == len(expected), 422,
                "INCOMPLETE_SELECTION", "Stored declared edges differ from canonical content.")
        return values

    def view(self, tx, view):
        project = self.project(tx)
        context = None
        if view["kind"] == "baseline":
            baseline = self.baseline(tx, view["baseline_id"])
            selection = dict(baseline["manifest"]["selection"])
        else:
            row = tx.run("MATCH (c:DraftContext {project_id:$p, context_id:$c}) RETURN properties(c) AS c",
                         p=self.project_id, c=view["context_id"]).single()
            require(row is not None, 404, "UNKNOWN_IDENTITY", "Unknown selected context.")
            context = row["c"]
            require(context["context_version"] == view["context_version"], 409,
                    "STALE_CONTEXT", "Selected context version has changed.")
            baseline = self.baseline(tx, context["base_baseline_id"])
            selection = dict(baseline["manifest"]["selection"])
            proposals = tx.run("MATCH (c:DraftContext {project_id:$p, context_id:$c})-[e:PROPOSES]->(r:Revision) "
                               "RETURN e.artifact_id AS id, r.revision_id AS r, r.project_id AS p",
                               p=self.project_id, c=view["context_id"]).data()
            require(len({v["id"] for v in proposals}) == len(proposals)
                    and all(v["p"] == self.project_id for v in proposals), 422,
                    "INCOMPLETE_SELECTION", "Context proposals are inconsistent.")
            selection.update({v["id"]: v["r"] for v in proposals})
        return {"view": view, "version": project["command_version"], "baseline": baseline,
                "context": context, "revisions": self.revisions(tx, selection)}

    def new_revisions(self, tx, revisions, metadata):
        ids = list(revisions)
        existing = {r["id"] for r in tx.run("MATCH (r:Revision {project_id:$p}) WHERE r.revision_id IN $ids "
                                             "RETURN r.revision_id AS id", p=self.project_id, ids=ids)}
        fresh = [r for rid, r in revisions.items() if rid not in existing]
        rows = [{"p": self.project_id, "a": r["envelope"]["artifact_id"], "r": r["revision_id"],
                 "envelope": text(r["envelope"]), "document": r["document_base64"],
                 "digest": r["envelope"]["document_sha256"], "type": metadata[r["envelope"]["artifact_id"]]["type"],
                 "status": metadata[r["envelope"]["artifact_id"]]["status"]} for r in fresh]
        for start in range(0, len(rows), 100):
            tx.run("UNWIND $rows AS row MERGE (a:Artifact {project_id:row.p, artifact_id:row.a}) "
                   "CREATE (r:Revision {project_id:row.p, artifact_id:row.a, revision_id:row.r, "
                   "envelope_json:row.envelope, document_base64:row.document, document_sha256:row.digest, "
                   "type:row.type, status:row.status}) CREATE (a)-[:HAS_REVISION]->(r)", rows=rows[start:start + 100]).consume()
        edges = [{"r": r["revision_id"], "kind": k, "target": target} for r in fresh
                 for k, targets in r["envelope"]["declared_relations"].items() for target in targets]
        for start in range(0, len(edges), 200):
            # Only real targets get nodes. Unfilled template links stay in evaluator findings.
            tx.run("UNWIND $edges AS row MATCH (r:Revision {project_id:$p, revision_id:row.r}), "
                   "(a:Artifact {project_id:$p, artifact_id:row.target}) "
                   "CREATE (r)-[:DECLARES {kind:row.kind, target_artifact_id:row.target}]->(a)",
                   p=self.project_id, edges=edges[start:start + 200]).consume()
        return sorted(r["revision_id"] for r in fresh)

    def add_baseline(self, tx, baseline):
        identity, manifest = baseline["baseline_id"], baseline["manifest"]
        exists = tx.run("MATCH (b:Baseline {project_id:$p, baseline_id:$b}) RETURN b", p=self.project_id, b=identity).single()
        if exists:
            require(self.baseline(tx, identity) == baseline, 409, "SOURCE_MISMATCH", "Baseline identity conflict.")
            return
        tx.run("CREATE (:Baseline {project_id:$p, baseline_id:$b, manifest_json:$m})",
               p=self.project_id, b=identity, m=text(manifest)).consume()
        tx.run("UNWIND $ids AS id MATCH (b:Baseline {project_id:$p, baseline_id:$b}), "
               "(r:Revision {project_id:$p, revision_id:id}) CREATE (b)-[:SELECTS]->(r)",
               p=self.project_id, b=identity, ids=list(manifest["selection"].values())).consume()

    def commit(self, command, principal, digest, plan, *, fault=None):
        """No driver retry: stale inputs require a new deliberate client request."""
        try:
            with self.transaction() as tx:
                old = self.operation(tx, principal, command["operation_key"])
                if old:
                    require(old[0] == digest, 409, "KEY_REUSE", "Operation key has different content.")
                    return old[1]
                before = command["expected_project_version"]
                matched = tx.run("MATCH (p:Project {project_id:$p}) WHERE p.command_version=$n "
                                 "SET p.command_version=$next RETURN p.command_version AS v",
                                 p=self.project_id, n=before, next=before + 1).single()
                require(matched is not None, 409, "STALE_PROJECT", "Project inputs changed before acceptance.")
                if "context_id" in command:
                    current = self.view(tx, {"kind": "context", "context_id": command["context_id"],
                                             "context_version": command["expected_context_version"]})
                    if "expected_revision_id" in command:
                        selected = current["revisions"].get(command["artifact_id"], {})
                        require(selected.get("revision_id") == command["expected_revision_id"], 409,
                                "STALE_REVISION", "Selected revision changed before acceptance.")
                fresh = self.new_revisions(tx, plan.get("revisions", {}), plan.get("metadata", {}))
                if plan.get("baseline"):
                    self.add_baseline(tx, plan["baseline"])
                if plan.get("new_context"):
                    c = plan["new_context"]
                    tx.run("MATCH (b:Baseline {project_id:$p, baseline_id:$b}) "
                           "CREATE (c:DraftContext {project_id:$p, context_id:$c, base_baseline_id:$b, "
                           "work_order_id:$wo, context_version:0}) CREATE (c)-[:BASED_ON]->(b)",
                           p=self.project_id, b=c["base_baseline_id"], c=c["context_id"], wo=c["work_order_id"]).consume()
                if command["operation"] in ("create-artifact", "revise-artifact"):
                    revision = next(iter(plan["revisions"].values()))
                    artifact_id = revision["envelope"]["artifact_id"]
                    tx.run("MATCH (c:DraftContext {project_id:$p, context_id:$c}) "
                           "OPTIONAL MATCH (c)-[e:PROPOSES {artifact_id:$a}]->() DELETE e",
                           p=self.project_id, c=command["context_id"], a=artifact_id).consume()
                    tx.run("MATCH (c:DraftContext {project_id:$p, context_id:$c}), "
                           "(r:Revision {project_id:$p, revision_id:$r}) "
                           "SET c.context_version=c.context_version+1 CREATE (c)-[:PROPOSES {artifact_id:$a}]->(r)",
                           p=self.project_id, c=command["context_id"], r=revision["revision_id"], a=artifact_id).consume()
                if fault:
                    fault("after_graph", tx)
                result = plan["result"]
                result["affected_revision_ids"] = fresh
                result["affected_artifacts"] = sorted([
                    {"artifact_id": r["envelope"]["artifact_id"], "revision_id": rid}
                    for rid, r in plan.get("revisions", {}).items() if rid in fresh], key=lambda x: x["artifact_id"])
                tx.run("CREATE (:Operation {project_id:$p, principal_id:$a, operation_key:$k, "
                       "request_sha256:$digest, result_json:$result})", p=self.project_id, a=principal,
                       k=command["operation_key"], digest=digest, result=text(result)).consume()
                if fault:
                    fault("before_commit", tx)
                tx.commit()
                return result
        except Neo4jError as exc:
            # Recover an identical winner only; never replay at a newer version.
            with self.transaction() as tx:
                winner = self.operation(tx, principal, command["operation_key"])
            if winner:
                require(winner[0] == digest, 409, "KEY_REUSE", "Operation key has different content.")
                return winner[1]
            if "TransientError" in (exc.code or "") or "conflict" in str(exc).lower():
                raise Refusal(409, "STALE_PROJECT", "Concurrent project mutation refused.") from exc
            raise
