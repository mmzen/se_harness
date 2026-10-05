"""Live integration checks; run inside the installed service image on private data.

This suite uses actual HTTP/MCP and independent database connections. Fault hooks
are invoked only in this test process, never exposed through a network route.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import copy
import hashlib
import json
import time
import threading
import socket
import subprocess
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from hosted_artifact_graph.canonical import canonical_json
from hosted_artifact_graph.protocol import EVALUATOR, Refusal
from hosted_artifact_graph.service import Service


class Boundaries:
    def __init__(self, args):
        self.args = args
        self.config = json.loads(args.config.read_text())
        self.credentials = json.loads(args.credentials.read_text())
        self.service = Service(self.config, self.credentials)
        self.project = self.config["project_id"]
        self.prefix = str(uuid.uuid4())
        self.sequence = 0
        self.observations = []
        self.output = args.output
        self.output.mkdir(exist_ok=False, parents=True)
        completed = json.loads((args.walkthrough / "walkthrough.json").read_text())
        assert completed["state"] == "client_sequence_passed"
        self.baseline = completed["baseline"]
        self.context = completed["context"]
        revised = json.loads(json.loads((args.walkthrough / "009-revise-body-and-relation-result.json").read_text())["stdout"])
        self.binding = revised["affected_artifacts"][0]
        self.document = json.loads((args.walkthrough / "009-revise-body-and-relation-request.json").read_text())["document_base64"]
        if args.continuation:
            continued = json.loads(args.continuation.read_text())
            self.context, self.binding = continued["context"], continued["binding"]

    def record(self, name, value):
        self.sequence += 1
        filename = f"{self.sequence:03}-{name}.json"
        encoded = json.dumps(value, ensure_ascii=False, indent=2)
        assert all(p["token"] not in encoded for p in self.credentials["principals"])
        (self.output / filename).write_text(encoded + "\n", encoding="utf-8")
        self.observations.append({"name": name, "file": filename})
        print(json.dumps({"observation": name, "file": filename}), flush=True)

    def principal(self, name="author-one"):
        return next(p for p in self.credentials["principals"] if p["id"] == name)

    def http(self, path, request=None, principal="author-one"):
        token = self.principal(principal)["token"]
        req = urllib.request.Request(self.args.endpoint + path,
            data=canonical_json(request) if request is not None else None,
            headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
        try:
            response = urllib.request.urlopen(req, timeout=180)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            return response.status, json.load(response)

    def read(self, operation, view=None, **fields):
        return {"schema": "se-harness-graph-read/v1", "project_id": self.project,
                "operation": operation, "view": view or self.baseline,
                "budget": {"rows": 500, "bytes": 2097152, "depth": 8}, **fields}

    def snapshot(self):
        with self.service.store.transaction() as tx:
            version = self.service.store.project(tx)["command_version"]
            # An independent whole-store fingerprint catches partial edges/receipts/heads.
            nodes = sorted(hashlib.sha256(canonical_json(dict(r["p"]))).hexdigest()
                           for r in tx.run("MATCH (n) RETURN properties(n) AS p"))
            edges = sorted(hashlib.sha256(canonical_json(dict(r))).hexdigest() for r in tx.run(
                "MATCH (a)-[e]->(b) RETURN id(a) AS a, type(e) AS t, properties(e) AS p, id(b) AS b"))
        return {"version": version, "nodes": len(nodes), "edges": len(edges),
                "sha256": hashlib.sha256(canonical_json([nodes, edges])).hexdigest()}

    def command(self, operation="revise-artifact", **fields):
        value = {"schema": "se-harness-remote-command/v1", "project_id": self.project,
                 "operation_key": self.prefix + "-" + str(uuid.uuid4()), "operation": operation,
                 "expected_project_version": self.snapshot()["version"], "expected_evaluator": EVALUATOR,
                 "client": self.config["client"]}
        if operation == "revise-artifact":
            value.update(context_id=self.context["context_id"], expected_context_version=self.context["context_version"],
                         artifact_id=self.binding["artifact_id"], expected_revision_id=self.binding["revision_id"],
                         document_base64=self.document)
        value.update(fields)
        return copy.deepcopy(value)

    def refuse(self, name, command, code, principal="author-one"):
        before = self.snapshot()
        status, result = self.http(f"/v1/projects/{self.project}/commands", command, principal)
        after = self.snapshot()
        self.record(name, {"request": command, "status": status, "result": result, "before": before, "after": after})
        assert result.get("error", {}).get("code") == "HAG_REMOTE_" + code, (name, result)
        assert result["receipt_id"] is None and before == after, name + ": partial refusal effects"

    def invalid_and_rights(self):
        raw = base64.b64decode(self.document).decode()
        variants = [
            ("malformed-toml", raw.replace("+++", "+++\nbroken = [", 1), "INVALID_DRAFT"),
            ("duplicate-metadata", raw.replace("+++", '+++\nstatus = "draft"', 1), "INVALID_DRAFT"),
            ("id-type-mismatch", raw.replace('type = "requirement"', 'type = "capability"'), "INVALID_DRAFT"),
            ("prohibited-relation", raw.replace('"CAP-IAR-002"', '"RLS-SEH-032"'), "INVALID_DRAFT"),
            ("lifecycle-change", raw.replace('status = "draft"', 'status = "approved"'), "PROTECTED_FIELD"),
        ]
        for name, document, code in variants:
            self.refuse(name, self.command(document_base64=base64.b64encode(document.encode()).decode()), code)
        forged = self.command(actor="mmzen")
        self.refuse("forged-actor", forged, "MALFORMED")
        self.refuse("unsupported-lifecycle", self.command(operation="transition"), "UNSUPPORTED_OPERATION")
        self.refuse("reader-cannot-write", self.command(), "FORBIDDEN", "reader")
        wrong = self.command(); wrong["expected_evaluator"]["archive_sha256"] = "0" * 64
        self.refuse("wrong-evaluator", wrong, "UNSUPPORTED_TUPLE")
        wrong = self.command(); wrong["client"]["wheel_sha256"] = "0" * 64
        self.refuse("wrong-client", wrong, "UNSUPPORTED_TUPLE")
        self.refuse("stale-context", self.command(expected_context_version=0), "STALE_CONTEXT")
        self.refuse("stale-revision", self.command(expected_revision_id="sha256:" + "0" * 64), "STALE_REVISION")
        with self.service.store.transaction() as tx:
            b = self.service.store.baseline(tx, self.baseline["baseline_id"])
            revisions = self.service.store.revisions(tx, b["manifest"]["selection"])
        for artifact in ("WO-RLS-038", "DEC-RLS-007", "VREC-RLS-002"):
            r = revisions[artifact]
            self.refuse("imported-" + artifact, self.command(artifact_id=artifact, expected_revision_id=r["revision_id"],
                document_base64=r["document_base64"]), "PROTECTED_FIELD")

    def accept(self, result):
        self.context = result["view"]
        self.binding = result["affected_artifacts"][0]

    def concurrent(self):
        before = self.snapshot()
        first = self.command(); second = copy.deepcopy(first); second["operation_key"] += "-competitor"
        endpoint = f"/v1/projects/{self.project}/commands"
        with ThreadPoolExecutor(2) as pool:
            a = pool.submit(self.http, endpoint, first, "author-one")
            b = pool.submit(self.http, endpoint, second, "author-two")
            results = [a.result(), b.result()]
        self.record("concurrent-distinct", {"before": before, "requests": [first, second], "results": results, "after": self.snapshot()})
        assert sorted(s for s, _ in results) == [200, 409]
        accepted = next(r for s, r in results if s == 200)
        assert self.snapshot()["version"] == before["version"] + 1
        self.accept(accepted)
        before = self.snapshot()
        equal = self.command()
        with ThreadPoolExecutor(2) as pool:
            a = pool.submit(self.http, endpoint, equal)
            b = pool.submit(self.http, endpoint, equal)
            results = [a.result(), b.result()]
        self.record("concurrent-equal", {"before": before, "request": equal, "results": results, "after": self.snapshot()})
        assert results[0] == results[1] and results[0][0] == 200
        assert self.snapshot()["version"] == before["version"] + 1
        self.accept(results[0][1])
        status, lookup = self.http(f"/v1/projects/{self.project}/operations/{equal['operation_key']}")
        assert status == 200 and lookup == results[0][1]
        status, hidden = self.http(f"/v1/projects/{self.project}/operations/{equal['operation_key']}", principal="author-two")
        assert status == 404
        self.record("principal-scoped-lookup", {"accepted": lookup, "other_principal": hidden})
        # A different project command invalidates a prepared revision even though its target did not change.
        pending = self.command()
        opened = self.command("draft-open", base_baseline_id=self.baseline["baseline_id"], work_order_id="WO-RLS-038")
        status, result = self.http(f"/v1/projects/{self.project}/contexts", opened, "author-two")
        self.record("unrelated-input-changes-guard", {"request": opened, "status": status, "result": result})
        assert status == 200
        self.refuse("stale-governing-input", pending, "STALE_PROJECT")

    def faults(self):
        for stage in ("after_graph", "before_commit"):
            before = self.snapshot(); command = self.command()
            def fail(actual, tx):
                if actual == stage:
                    raise OSError("Qualification injected precommit failure")
            try:
                self.service.command(self.principal(), command, fault=fail)
            except OSError:
                pass
            else:
                raise AssertionError("Fault was not reached")
            after = self.snapshot()
            self.record("rollback-" + stage, {"before": before, "after": after, "request": command})
            assert before == after
        # End the actual transaction after graph writes. Its subsequent COMMIT must fail.
        before = self.snapshot(); command = self.command()
        def abort(actual, tx):
            if actual == "before_commit":
                tx.rollback()
        try:
            self.service.command(self.principal(), command, fault=abort)
        except Exception as exc:
            failure = type(exc).__name__
        else:
            raise AssertionError("Closed transaction committed")
        self.record("commit-failure", {"before": before, "after": self.snapshot(), "failure": failure, "request": command})
        assert before == self.snapshot()

    async def parity(self):
        import httpx
        from mcp import ClientSession
        from mcp.client.streamable_http import streamable_http_client
        requests = [self.read("revision", self.context, **self.binding),
                    self.read("work-context", work_order_id="WO-RLS-038"),
                    self.read("compare", {"kind": "comparison", "left": self.baseline, "right": self.context}),
                    self.read("impact", artifact_id="CAP-IAR-002"),
                    self.read("lineage", artifact_id="VREC-RLS-002"),
                    self.read("check", artifact_id="WO-RLS-038"),
                    self.read("cypher", query="MATCH (r:Revision) WHERE r.artifact_id = $id RETURN r.artifact_id AS id LIMIT 5", parameters={"id": "WO-RLS-038"})]
        async with httpx.AsyncClient(headers={"Authorization": "Bearer " + self.principal()["token"]}, timeout=180) as client:
            async with streamable_http_client(self.args.endpoint + "/mcp", http_client=client) as (incoming, outgoing, _):
                async with ClientSession(incoming, outgoing) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    assert {t.name for t in tools.tools} == {r["operation"] for r in requests}
                    self.record("mcp-tool-schemas", tools.model_dump(mode="json"))
                    for request in requests:
                        status, http = await asyncio.to_thread(self.http, f"/v1/projects/{self.project}/reads/{request['operation']}", request)
                        mcp = await session.call_tool(request["operation"], request)
                        response = json.loads(mcp.content[0].text)
                        self.record("parity-" + request["operation"], {"request": request, "http_status": status, "http": http, "mcp": response})
                        assert status == 200 and response == http, request["operation"]

    def resource_boundaries(self):
        before = self.snapshot()
        route = f"/v1/projects/{self.project}/reads/"
        for name, request, status_expected, complete in [
            ("row-budget", dict(self.read("work-context", work_order_id="WO-RLS-038"), budget={"rows": 1, "bytes": 2097152, "depth": 8}), 200, False),
            ("byte-budget", dict(self.read("work-context", work_order_id="WO-RLS-038"), budget={"rows": 500, "bytes": 1024, "depth": 8}), 429, None),
            ("depth-budget", dict(self.read("impact", artifact_id="CAP-IAR-002"), budget={"rows": 500, "bytes": 2097152, "depth": 0}), 200, False),
            ("unknown-baseline", self.read("impact", {"kind": "baseline", "baseline_id": "se-harness-artifact-baseline/v1:sha256:" + "0" * 64}, artifact_id="CAP-IAR-002"), 404, None),
            ("unknown-project", dict(self.read("impact", artifact_id="CAP-IAR-002"), project_id="22222222-2222-4222-8222-222222222222"), 403, None),
        ]:
            path = f"/v1/projects/{request['project_id']}/reads/{request['operation']}"
            status, result = self.http(path, request)
            self.record(name, {"request": request, "status": status, "result": result})
            assert status == status_expected, name
            if complete is not None:
                assert result["complete"] is complete and result["continuation"]
                assert result["view"] == request["view"]
        bad_queries = ["MATCH (n:Revision) DELETE n RETURN n LIMIT 2", "CALL db.labels()", "SHOW INDEX INFO",
            "MATCH (n:Revision) RETURN n LIMIT 2; CREATE (:Leak)", "CREATE INDEX ON :Leak(x)",
            "MATCH (n:Revision) WHERE EXISTS { MATCH (a) } RETURN n LIMIT 2", "LOAD CSV FROM 'file:///x' AS x RETURN x",
            "MATCH (n:Revision) RETURN n[$field] LIMIT 2", "MATCH (n:Revision) RETURN labels(n) LIMIT 2",
            "MATCH (n:Revision) RETURN n", "MATCH (n:Operation) RETURN n LIMIT 2", "CREATE USER hacked"]
        for index, query in enumerate(bad_queries):
            request = self.read("cypher", query=query, parameters={})
            status, result = self.http(route + "cypher", request)
            self.record("query-refusal-" + str(index), {"request": request, "status": status, "result": result})
            assert status == 400 and result["error"]["code"] == "HAG_REMOTE_QUERY_SYNTAX"
        queries = [(self.baseline, self.binding["artifact_id"], []),
                   (self.context, self.binding["artifact_id"], [[self.binding["artifact_id"]]]),
                   (self.baseline, "'; CREATE (:Leak) //", [])]
        for index, (view, value, expected) in enumerate(queries):
            request = self.read("cypher", view, query="mAtCh (r:Revision) /* DELETE is only a comment */ WHERE r.artifact_id = $id RETURN r.artifact_id AS id LIMIT 5", parameters={"id": value})
            status, result = self.http(route + "cypher", request)
            self.record("query-view-" + str(index), {"request": request, "status": status, "result": result})
            assert status == 200 and result["data"]["rows"] == expected
        assert before == self.snapshot(), "Read boundary probes changed the store"
        self.record("read-rollback", {"before": before, "after": self.snapshot()})

    def lost_reply(self):
        suite = self
        accepted = []
        class DropReply(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass
            def do_POST(self):
                body = self.rfile.read(int(self.headers["Content-Length"]))
                status, result = suite.http(self.path, json.loads(body))
                accepted.append((status, result))
                # The real server has committed, but the client receives no HTTP response.
                self.close_connection = True
                self.connection.shutdown(socket.SHUT_RDWR)
                self.connection.close()
        proxy = ThreadingHTTPServer(("127.0.0.1", 0), DropReply)
        thread = threading.Thread(target=proxy.serve_forever, daemon=True)
        thread.start()
        command = self.command()
        request_path = self.output / "lost-reply-request.json"
        request_path.write_bytes(canonical_json(command))
        argv = [str(self.args.client_python), "-I", "-m", "se_harness", "remote", "revise-artifact",
                "--endpoint", f"http://127.0.0.1:{proxy.server_port}", "--project", self.project,
                "--token-env", "HAG_TEST_TOKEN", "--client-wheel", str(self.args.client_wheel),
                "--request", str(request_path), "--json"]
        before = self.snapshot()
        try:
            child = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180,
                                   env=dict(os.environ, HAG_TEST_TOKEN=self.principal()["token"]))
        finally:
            proxy.shutdown(); proxy.server_close(); thread.join()
        self.record("lost-reply-client-transport", {"command": argv, "exit": child.returncode,
                    "stdout": child.stdout.decode(), "stderr": child.stderr.decode(), "server_result": accepted})
        output = json.loads(child.stdout if child.stdout.strip() else child.stderr)
        self.record("lost-committed-response", {"command": argv, "exit": child.returncode, "client_result": output,
                    "server_result": accepted, "before": before, "after": self.snapshot(), "stderr": child.stderr.decode()})
        assert child.returncode != 0 and output["outcome"] == "unknown" and accepted[0][0] == 200
        assert self.snapshot()["version"] == before["version"] + 1
        status, recovered = self.http(f"/v1/projects/{self.project}/commands", command)
        assert status == 200 and recovered == accepted[0][1]
        assert self.snapshot()["version"] == before["version"] + 1
        self.accept(recovered)
        self.record("lost-reply-identical-recovery", {"request": command, "result": recovered, "after": self.snapshot()})

    def run(self):
        for operation in self.args.only.split(","):
            if operation == "parity":
                asyncio.run(self.parity())
            else:
                getattr(self, operation)()
        self.record("completed", {"observations": list(self.observations), "context": self.context,
                                   "binding": self.binding, "state": "selected_live_boundary_checks_passed"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("/run/config/config.json"))
    parser.add_argument("--credentials", type=Path, default=Path("/run/secrets/sandbox_credentials"))
    parser.add_argument("--endpoint", default="http://service:8080")
    parser.add_argument("--walkthrough", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--continuation", type=Path)
    parser.add_argument("--only", default="invalid_and_rights,concurrent,faults,parity,resource_boundaries")
    parser.add_argument("--client-python", type=Path)
    parser.add_argument("--client-wheel", type=Path)
    args = parser.parse_args()
    suite = Boundaries(args)
    try:
        suite.run()
    finally:
        suite.service.store.driver.close()
