"""Replay the real packaged client against a private service, retaining every result.

This executable suite never claims skipped scenarios passed. Supplemental database
fault/MCP/recovery qualification is reported separately by the sandbox runner.
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import os
import subprocess
import time
import uuid
from pathlib import Path


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class Walkthrough:
    def __init__(self, args):
        self.args = args
        self.config = json.loads(args.configuration.read_text(encoding="utf-8"))
        self.credentials = json.loads(args.credentials.read_text(encoding="utf-8"))
        self.expected = json.loads(args.scenario_fixture.read_text(encoding="utf-8"))["reference_context"]
        self.manifest = json.loads(args.source_manifest.read_text(encoding="utf-8"))
        self.output = args.output
        self.output.mkdir(parents=True, exist_ok=False)
        self.prefix = str(uuid.uuid4())
        self.sequence = 0
        self.observations = []
        self.version = None

    def cli(self, name, operation, *, principal="operator", request=None, expected_exit=0, extra=()):
        self.sequence += 1
        label = f"{self.sequence:03}-{name}"
        command = [str(self.args.client_python), "-I", "-m", "se_harness", "remote", operation,
                   "--endpoint", self.args.endpoint, "--project", self.config["project_id"],
                   "--token-env", "HAG_TEST_TOKEN", "--json", *extra]
        if request is not None:
            file = self.output / (label + "-request.json")
            save(file, request)
            command += ["--request", str(file)]
        if operation in ("import", "draft-open", "freeze", "create-artifact", "revise-artifact"):
            command += ["--client-wheel", str(self.args.client_wheel)]
        token = next(p["token"] for p in self.credentials["principals"] if p["id"] == principal)
        start = time.monotonic()
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env=dict(os.environ, HAG_TEST_TOKEN=token), timeout=180)
        stdout, stderr = result.stdout.decode("utf-8"), result.stderr.decode("utf-8")
        assert token not in stdout + stderr, "Credential appeared in client output"
        entry = {"command": command, "cwd": os.getcwd(), "seconds": round(time.monotonic() - start, 3),
                 "exit": result.returncode, "stdout": stdout, "stderr": stderr}
        save(self.output / (label + "-result.json"), entry)
        print(json.dumps({"step": name, "exit": result.returncode, "seconds": entry["seconds"]}), flush=True)
        assert result.returncode == expected_exit, label + ": unexpected exit; inspect retained result"
        parsed = json.loads(stdout)
        self.observations.append({"name": name, "result": label + "-result.json"})
        return parsed

    def command(self, operation, **fields):
        return {"schema": "se-harness-remote-command/v1", "project_id": self.config["project_id"],
                "operation_key": self.prefix + "-" + str(self.sequence), "operation": operation,
                "expected_project_version": self.version, "expected_evaluator": self.evaluator,
                "client": self.config["client"], **fields}

    def accepted(self, name, command, principal="operator"):
        result = self.cli(name, command["operation"], request=command, principal=principal)
        assert result["outcome"] == "accepted"
        assert result["versions"]["project"]["before"] == command["expected_project_version"]
        assert result["versions"]["project"]["after"] == command["expected_project_version"] + 1
        self.version = result["versions"]["project"]["after"]
        return result

    def read(self, name, operation, view, **fields):
        return self.cli(name, "read", request={"schema": "se-harness-graph-read/v1", "project_id": self.config["project_id"],
            "operation": operation, "view": view, "budget": {"rows": 500, "bytes": 2097152, "depth": 8}, **fields})

    def run(self):
        status = self.cli("ready", "status")
        assert status["ready"]
        self.version, self.evaluator = status["project_version"], status["evaluator"]
        imported_command = self.command("import", source_manifest=self.manifest)
        imported = self.accepted("import-reference", imported_command)
        baseline = imported["view"]
        original = self.cli("baseline-original", "baseline", extra=("--baseline", baseline["baseline_id"]))
        assert len(original["manifest"]["selection"]) == len(self.manifest["artifacts"])
        repeated = self.cli("repeat-same-import-key", "import", request=imported_command)
        assert repeated == imported, "Identical-key import changed its accepted receipt"
        work = self.read("work-context", "work-context", baseline, work_order_id=self.expected["work_order_id"])
        assert work["complete"], "Reference governing context is incomplete"
        for output_key, expectation in (("governing_artifacts", "governing_ids"), ("dependencies", "dependency_ids"),
                                         ("relevant_decisions", "relevant_decision_ids")):
            assert [a["artifact_id"] for a in work["data"][output_key]] == sorted(self.expected[expectation]), output_key
        assert work["data"]["declared_scope"] == sorted(self.expected["declared_scope"])
        opened = self.accepted("open-context", self.command("draft-open", base_baseline_id=baseline["baseline_id"], work_order_id=self.expected["work_order_id"]))
        context = opened["view"]
        created = self.accepted("create-incomplete-draft", self.command("create-artifact", context_id=context["context_id"],
             expected_context_version=context["context_version"], domain="instruction-architecture", artifact_type="requirement", artifact_id=None), "author-one")
        assert created["evaluator_output"]["admissible"] and created["evaluator_output"]["incomplete"]
        context = created["view"]
        binding = created["affected_artifacts"][0]
        revision = self.read("read-created-revision", "revision", context, **binding)
        raw = base64.b64decode(revision["data"]["document_base64"]).decode("utf-8")
        # This is a test draft. Expected target type comes from the approved reference fixture.
        old_relations = revision["data"]["envelope"]["declared_relations"]
        targets = old_relations.get("derives_from", [])
        assert len(targets) == 1, "Update the test if the released template changes its authoring slot"
        revised_raw = raw.replace('"' + targets[0] + '"', '"CAP-IAR-002"') + "\nSandbox test outcome: retrieve explicit hosted context.\n"
        revise = self.command("revise-artifact", context_id=context["context_id"], expected_context_version=context["context_version"],
                              artifact_id=binding["artifact_id"], expected_revision_id=binding["revision_id"],
                              document_base64=base64.b64encode(revised_raw.encode()).decode())
        updated = self.accepted("revise-body-and-relation", revise, "author-one")
        assert updated["affected_revision_ids"] != created["affected_revision_ids"]
        context = updated["view"]
        current = updated["affected_artifacts"][0]
        bad = self.command("revise-artifact", context_id=context["context_id"], expected_context_version=context["context_version"],
                           artifact_id=current["artifact_id"], expected_revision_id=current["revision_id"],
                           document_base64=base64.b64encode(revised_raw.replace('"CAP-IAR-002"', '"RLS-SEH-032"').encode()).decode())
        refused = self.cli("refuse-prohibited-relation", "revise-artifact", request=bad, principal="author-one", expected_exit=1)
        assert refused["error"]["code"] == "HAG_REMOTE_INVALID_DRAFT" and refused["receipt_id"] is None
        stale = copy.deepcopy(revise)
        stale["operation_key"] += "-stale"
        refused = self.cli("refuse-stale-input", "revise-artifact", request=stale, principal="author-one", expected_exit=1)
        assert refused["error"]["code"] == "HAG_REMOTE_STALE_PROJECT"
        recovered = self.cli("recover-accepted-retry", "revise-artifact", request=revise, principal="author-one")
        assert recovered == updated
        mismatch = copy.deepcopy(revise)
        mismatch["document_base64"] = base64.b64encode((revised_raw + "changed").encode()).decode()
        refused = self.cli("refuse-key-reuse", "revise-artifact", request=mismatch, principal="author-one", expected_exit=1)
        assert refused["error"]["code"] == "HAG_REMOTE_KEY_REUSE"
        unchanged = self.cli("baseline-unchanged", "baseline", extra=("--baseline", baseline["baseline_id"]))
        assert unchanged == original
        comparison = self.read("compare-draft", "compare", {"kind": "comparison", "left": baseline, "right": context})
        assert comparison["complete"] and [a["artifact_id"] for a in comparison["data"]["changes"]] == [current["artifact_id"]]
        query = self.read("cypher-baseline", "cypher", baseline, query="MATCH (r:Revision) WHERE r.artifact_id = $id RETURN r.artifact_id AS id LIMIT 5", parameters={"id": self.expected["work_order_id"]})
        assert query["data"]["rows"] == [[self.expected["work_order_id"]]]
        checked = self.read("check-selected-work", "check", context, artifact_id=self.expected["work_order_id"])
        assert checked["evaluator_output"]["selection"]["primary"] == self.expected["work_order_id"]
        frozen = self.accepted("freeze-draft", self.command("freeze", context_id=context["context_id"], expected_context_version=context["context_version"]))
        assert frozen["versions"]["context"]["before"] == frozen["versions"]["context"]["after"]
        save(self.output / "walkthrough.json", {"state": "client_sequence_passed", "baseline": baseline, "context": context,
             "project_version": self.version, "frozen": frozen["view"], "observations": self.observations,
             "remaining": ["MCP parity", "independent evaluator comparison", "concurrency and faults", "negative variants", "restart and restore", "plugin qualification", "final candidate qualification"]})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("client-python", "client-wheel", "configuration", "credentials", "source-manifest", "scenario-fixture", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--endpoint", required=True)
    args = parser.parse_args()
    run = Walkthrough(args)
    try:
        run.run()
    except BaseException as exc:
        save(args.output / "walkthrough.json", {"state": "failed", "failure": type(exc).__name__ + ": " + str(exc),
             "observations": run.observations, "all_hosted_scenarios_passed": False})
        raise
