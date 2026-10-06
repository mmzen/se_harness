"""Exercise installed identity and rollback-only graph corruption boundaries.

Run in a disposable Compose service process, never the serving container.
Installed files are restored in finally blocks. Graph mutations never commit.
"""
import argparse
import copy
import json
import tempfile
from pathlib import Path

from qualify_boundaries import Boundaries
from hosted_artifact_graph.protocol import Refusal, contract_path


class Integrity(Boundaries):
    def expect_refusal(self, name, action, codes):
        before = self.snapshot()
        try:
            action()
        except Refusal as exc:
            result = exc.result()
        except Exception as exc:
            result = {"unexpected_exception_type": type(exc).__name__}
        else:
            result = {"unexpected_acceptance": True}
        after = self.snapshot()
        self.record(name, {"result": result, "before": before, "after": after})
        assert result.get("error", {}).get("code") in {"HAG_REMOTE_" + c for c in codes}, name
        assert before == after, name + ": changed persistent state"

    def identities(self):
        self.service.readiness()
        self.record("original-identities", {"result": "ready", "components": self.config["components"]})
        saved = copy.deepcopy(self.config)
        for name, change in [
            ("deployment-digest", lambda: self.config["components"].update(deployment_sha256="ab" * 32)),
            ("deployment-setting", lambda: self.config.update(authority_mode="remote-authority")),
            ("unsupported-schema-tuple", lambda: self.config["components"].update(schema_revision=2)),
            ("unsupported-evaluator-tuple", lambda: self.config["components"]["evaluator"].update(payload_sha256="ab" * 32)),
        ]:
            try:
                change()
                self.expect_refusal(name, self.service.compatibility, {"UNSUPPORTED_TUPLE"})
            finally:
                self.config.clear(); self.config.update(copy.deepcopy(saved))
        for filename in ("remote-v1.json", "read-v1.json", "result-v1.json", "graph-v1.cypher"):
            path = contract_path(filename)
            raw = path.read_bytes()
            try:
                path.write_bytes(raw + b"\n")
                self.expect_refusal("installed-contract-" + filename, self.service.compatibility, {"UNSUPPORTED_TUPLE"})
            finally:
                path.write_bytes(raw)
        original = self.service.evaluator.wheel
        with tempfile.TemporaryDirectory(prefix="hag-substitution-") as directory:
            substituted = Path(directory) / original.name
            substituted.write_bytes(original.read_bytes() + b"\n")
            try:
                self.service.evaluator.wheel = substituted
                self.expect_refusal("same-version-substituted-evaluator-wheel", self.service.evaluator.identity, {"UNSUPPORTED_TUPLE"})
            finally:
                self.service.evaluator.wheel = original
        # The evaluator is private to this disposable test container.
        engine, = Path("/opt/evaluator/lib").glob("python*/site-packages/se_harness/engine/validation_core.py")
        raw = engine.read_bytes()
        try:
            engine.write_bytes(raw + b"\n")
            self.expect_refusal("changed-installed-evaluator-payload", self.service.evaluator.identity,
                                {"UNSUPPORTED_TUPLE", "BINDING_UNAVAILABLE"})
        finally:
            engine.write_bytes(raw)
        original = self.service.evaluator.python
        try:
            self.service.evaluator.python = self.args.client_python
            self.expect_refusal("candidate-cannot-govern", self.service.evaluator.identity,
                                {"UNSUPPORTED_TUPLE", "BINDING_UNAVAILABLE"})
        finally:
            self.service.evaluator.python = original
        self.service.readiness()

    def graph_consistency(self):
        before = self.snapshot()
        for name, statement in [
            ("missing-context-base-edge", "MATCH (c:DraftContext {project_id:$p, context_id:$c})-[e:BASED_ON]->() DELETE e"),
            ("duplicate-context-base-edge", "MATCH (c:DraftContext {project_id:$p, context_id:$c})-[:BASED_ON]->(b) CREATE (c)-[:BASED_ON]->(b)"),
            ("wrong-context-base-edge", "MATCH (c:DraftContext {project_id:$p, context_id:$c})-[e:BASED_ON]->() DELETE e CREATE (c)-[:BASED_ON]->(c)"),
        ]:
            with self.service.store.transaction() as tx:
                tx.run(statement, p=self.project, c=self.context["context_id"]).consume()
                try:
                    self.service.store.view(tx, self.context)
                except Refusal as exc:
                    result = exc.result()
                else:
                    result = {"unexpected_acceptance": True}
            after = self.snapshot()
            self.record(name, {"result": result, "before": before, "after": after})
            assert result.get("error", {}).get("code") == "HAG_REMOTE_INCOMPLETE_SELECTION"
            assert before == after


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("/run/config/config.json"))
    parser.add_argument("--credentials", type=Path, default=Path("/run/secrets/sandbox_credentials"))
    parser.add_argument("--endpoint", default="http://service:8080")
    parser.add_argument("--walkthrough", type=Path, required=True)
    parser.add_argument("--continuation", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--client-python", type=Path, required=True)
    parser.add_argument("--client-wheel", type=Path)
    args = parser.parse_args()
    args.only = "identities,graph_consistency"
    suite = Integrity(args)
    try:
        suite.run()
    finally:
        suite.service.store.driver.close()
