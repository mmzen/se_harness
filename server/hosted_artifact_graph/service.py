"""Sandbox admission: authenticate, select, ask the release, then commit once."""
from __future__ import annotations

import base64
import hashlib
import json
import secrets
import os
import platform
import re
import zipfile
import sys
from importlib.metadata import PackageNotFoundError, version as package_version
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .canonical import CanonicalError, canonical_json, make_baseline, make_revision, named_digest
from .evaluator import Evaluator
from .protocol import (EVALUATOR, MAX_REVISIONS, MAX_RESPONSE, READ, RESULT, Refusal,
                       Wire, contained_file, decode_document, require)
from .store import Store


class Service:
    def __init__(self, config, credentials):
        self.config, self.credentials = config, credentials
        self.project_id = config["project_id"]
        self.wire = Wire()
        self.evaluator = Evaluator(config)
        self.store = Store(config["database_uri"], self.project_id)

    def authenticate(self, authorization):
        require(isinstance(authorization, str) and authorization.startswith("Bearer "), 401,
                "UNAUTHENTICATED", "A sandbox bearer credential is required.")
        token = authorization[7:]
        principal = next((p for p in self.credentials["principals"] if secrets.compare_digest(p["token"], token)), None)
        require(principal is not None, 401, "UNAUTHENTICATED", "Unknown sandbox credential.")
        return principal

    def access(self, principal, project, operation=None):
        require(project == self.project_id and project in principal["projects"], 403,
                "FORBIDDEN", "Principal cannot access the selected project.")
        if operation:
            allowed = {"operator"} if operation == "import" else {"operator", "sandbox-author"}
            require(principal["role"] in allowed, 403, "FORBIDDEN", "Principal cannot perform this sandbox operation.")

    def readiness(self):
        identity = self.evaluator.identity()
        self.compatibility()
        self.evaluator.verify_source()
        version = self.store.ready()
        require(self.config.get("authority_mode") == "sandbox-projection" and self.config.get("client"),
                409, "UNSUPPORTED_TUPLE", "The explicit sandbox component tuple is missing.")
        return {"ready": True, "project_id": self.project_id, "schema_revision": 1,
                "project_version": version, "evaluator": EVALUATOR,
                "components": self.config["components"], "client": self.config["client"],
                "authority_mode": "sandbox-projection", "protocols": self.config["protocols"],
                "database_read_only_enforcement": "deferred: RISK-HAG-001"}

    def compatibility(self):
        """Validate the selected closed combination and observed in-image identities.

        The deployment's image manifest is read back by the qualification runner;
        the process verifies its source label, wheel bytes and runtime separately.
        """
        def expect(condition):
            if not condition:
                raise ValueError("Unsupported component tuple")

        try:
            value = self.config["components"]
            expected_keys = {"schema", "source", "client", "plugins", "server", "evaluator", "runtime", "database",
                             "schema_revision", "protocols", "deployment_sha256", "required_secret_keys"}
            expect(set(value) == expected_keys and value["schema"] == "se-harness-hosted-combination/v1")
            expect(value["source"]["repository"] == "https://github.com/mmzen/se_harness.git")
            expect(re.fullmatch(r"[0-9a-f]{40}", value["source"]["candidate_commit"]))
            expect(value["source"]["candidate_commit"] == os.environ.get("HAG_SOURCE_COMMIT"))
            expect(value["client"] == self.config["client"] and value["client"]["version"] == "0.22.2")
            expect(value["evaluator"] == EVALUATOR and value["schema_revision"] == 1)
            protocols = ["se-harness-remote-command/v1", "se-harness-remote-result/v1", "se-harness-graph-read/v1",
                         "se-harness-artifact-revision/v1", "se-harness-artifact-baseline/v1"]
            expect(value["protocols"] == self.config["protocols"] == protocols)
            expect(value["runtime"] == {"python": "3.13.16", "platform": "linux/amd64",
                "image": "python@sha256:88310c082760d93ac7c74d579e95e53a4ab6ea52dd8901abc61a103daf488ac4"})
            expect(platform.python_version() == value["runtime"]["python"] and platform.system() == "Linux" and platform.machine() == "x86_64")
            expect(value["database"] == {"version": "3.13.1", "image": "memgraph/memgraph@sha256:4710bee1ab5b47599876e30f17ae1679d0bbb2262d84dc06641521fecb7c89ce"})
            expect(value["server"]["version"] == package_version("se-harness-hosted-sandbox") == "0.1.0.dev1")
            expect(set(value["plugins"]) == {"codex", "claude"})
            digests = [value["client"]["wheel_sha256"], value["deployment_sha256"]]
            for item in value["plugins"].values():
                expect(item["version"] == "0.2.7")
                digests.extend([item["archive_sha256"], item["inventory_sha256"]])
            server = value["server"]
            expect(re.fullmatch(r"sha256:[0-9a-f]{64}", server["image_manifest"]))
            digests.extend([server["wheel_sha256"], server["dependency_lock_sha256"], server["system_packages_sha256"]])
            expect(all(isinstance(d, str) and re.fullmatch(r"[0-9a-f]{64}", d) and len(set(d)) > 1 for d in digests))
            expect(hashlib.sha256(Path("/opt/requirements.lock").read_bytes()).hexdigest() == server["dependency_lock_sha256"])
            expect(hashlib.sha256(Path("/opt/system-packages.lock.json").read_bytes()).hexdigest() == server["system_packages_sha256"])
            deployment = {"configuration": {k: v for k, v in self.config.items() if k != "components"},
                          "compose_sha256": hashlib.sha256(Path("/opt/compose.yaml").read_bytes()).hexdigest()}
            expect(hashlib.sha256(canonical_json(deployment)).hexdigest() == value["deployment_sha256"])
            wheel, = Path("/opt/service-wheel").glob("*.whl")
            expect(hashlib.sha256(wheel.read_bytes()).hexdigest() == server["wheel_sha256"])
            with zipfile.ZipFile(wheel) as archive:
                for name in archive.namelist():
                    if name.startswith("hosted_artifact_graph/") and not name.endswith("/"):
                        expect((Path(__file__).parent.parent / name).read_bytes() == archive.read(name))
                    elif ".data/data/" in name and not name.endswith("/"):
                        relative = name.split(".data/data/", 1)[1]
                        expect((Path(sys.prefix) / relative).read_bytes() == archive.read(name))
        except (AssertionError, KeyError, TypeError, ValueError, OSError, zipfile.BadZipFile, PackageNotFoundError) as exc:
            raise Refusal(409, "UNSUPPORTED_TUPLE", "Missing or incompatible sandbox component identities.") from exc

    def lookup(self, principal, project, key):
        self.access(principal, project)
        with self.store.transaction() as tx:
            value = self.store.operation(tx, principal["id"], key)
        require(value is not None, 404, "OPERATION_UNKNOWN", "No accepted operation is currently visible for this principal and key.")
        return value[1]

    def baseline(self, principal, project, identity):
        self.access(principal, project)
        with self.store.transaction() as tx:
            value = self.store.baseline(tx, identity)
            self.store.revisions(tx, value["manifest"]["selection"])
        require(len(canonical_json(value)) <= MAX_RESPONSE, 429, "RESOURCE_LIMIT", "Baseline response exceeds 2 MiB.")
        return value

    def command(self, principal, raw, *, fault=None):
        require(isinstance(raw, dict), 400, "MALFORMED", "Expected a command object.")
        self.access(principal, raw.get("project_id"), raw.get("operation"))
        command, digest = self.wire.command(raw)
        with self.store.transaction() as tx:
            old = self.store.operation(tx, principal["id"], command["operation_key"])
            if old:
                require(old[0] == digest, 409, "KEY_REUSE", "Operation key has different content.")
                return old[1]
            require(command["expected_evaluator"] == EVALUATOR and command["client"] == self.config["client"],
                    409, "UNSUPPORTED_TUPLE", "Unsupported client/evaluator component tuple.")
            project = self.store.project(tx)
            view = None
            if command["operation"] == "draft-open":
                view = {"kind": "baseline", "baseline_id": command["base_baseline_id"]}
            elif "context_id" in command:
                view = {"kind": "context", "context_id": command["context_id"],
                        "context_version": command["expected_context_version"]}
            # Known identity, project guard, then context and revision guards.
            if view and view["kind"] == "baseline":
                self.store.baseline(tx, view["baseline_id"])
            elif view:
                exists = tx.run("MATCH (c:DraftContext {project_id:$p, context_id:$c}) RETURN c.context_id AS id",
                                p=self.project_id, c=view["context_id"]).single()
                require(exists is not None, 404, "UNKNOWN_IDENTITY", "Unknown selected context.")
            require(project["command_version"] == command["expected_project_version"], 409,
                    "STALE_PROJECT", "Expected project version is stale.")
            selected = self.store.view(tx, view) if view else None
            if "expected_revision_id" in command:
                revision = selected["revisions"].get(command["artifact_id"], {})
                require(revision.get("revision_id") == command["expected_revision_id"], 409,
                        "STALE_REVISION", "Expected artifact revision differs.")
            count = tx.run("MATCH (r:Revision {project_id:$p}) RETURN count(r) AS n", p=self.project_id).single()["n"]
            retained = set(tx.run("MATCH (r:Revision {project_id:$p}) RETURN r.revision_id AS id", p=self.project_id).value())
            reserved = tx.run("MATCH (a:Artifact {project_id:$p}) RETURN a.artifact_id AS id", p=self.project_id).value()
        self.evaluator.identity()
        self.compatibility()
        self.store.ready()
        plan = self.prepare(command, principal, selected, set(reserved))
        fresh = {rid: r for rid, r in plan.get("revisions", {}).items() if rid not in retained}
        require(count + len(fresh) <= MAX_REVISIONS, 429,
                "RESOURCE_LIMIT", "Project would exceed 10,000 retained revisions.")
        plan["result"]["affected_revision_ids"] = sorted(fresh)
        plan["result"]["affected_artifacts"] = sorted([
            {"artifact_id": r["envelope"]["artifact_id"], "revision_id": rid} for rid, r in fresh.items()], key=lambda a: a["artifact_id"])
        require(len(canonical_json(plan["result"])) <= MAX_RESPONSE, 429,
                "RESOURCE_LIMIT", "Accepted receipt would exceed 2 MiB.")
        if fault:
            fault("after_evaluation", None)
        return self.store.commit(command, principal["id"], digest, plan, fault=fault)

    def prepare(self, command, principal, selected, reserved):
        operation = command["operation"]
        plan = {}
        context_versions = None
        output = None
        view = None
        if operation == "import":
            manifest = command["source_manifest"]
            expected = json.loads(json.dumps(self.evaluator.manifest))
            expected["artifacts"].sort(key=lambda e: (e["path"], e["artifact_id"]))
            require({(e["artifact_id"], e["path"]) for e in manifest["artifacts"]}
                    == {(e["artifact_id"], e["path"]) for e in expected["artifacts"]},
                    422, "INVALID_IMPORT", "Import must select the complete configured artifact set.")
            require(manifest == expected, 409, "SOURCE_MISMATCH", "Only the complete configured source manifest is admitted.")
            require(sum(e["bytes"] for e in manifest["artifacts"]) <= 64 * 1024 * 1024,
                    429, "RESOURCE_LIMIT", "Formal import exceeds 64 MiB.")
            with self.evaluator.project() as root:
                catalog = self.evaluator.catalog(root)
                output = self.evaluator.bridge("validate", root)
                require(output["valid"], 422, "INVALID_IMPORT", "Released validation rejected the import.", evaluator_output=output)
                require({(e["artifact_id"], e["path"]) for e in manifest["artifacts"]}
                        == {(a["id"], a["path"]) for a in catalog.values()}, 422,
                        "INVALID_IMPORT", "Manifest differs from released formal discovery.")
                revisions = {}
                for entry in manifest["artifacts"]:
                    raw = contained_file(self.evaluator.source, entry["path"]).read_bytes()
                    oid = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
                    require(len(raw) == entry["bytes"] and hashlib.sha256(raw).hexdigest() == entry["raw_sha256"]
                            and oid == entry["blob_oid"], 409, "SOURCE_MISMATCH", "Manifest byte/provenance conflict: " + entry["path"])
                    artifact = catalog[entry["artifact_id"]]
                    revision = make_revision(project_id=self.project_id, artifact_id=artifact["id"], document=raw,
                        declared_relations=artifact["relations"], original_path=entry["path"],
                        provenance={"kind": "git", "source": manifest["source"], "blob_oid": oid})
                    revisions[artifact["id"]] = revision
            provenance = {"kind": "git", "source": manifest["source"],
                          "source_manifest_sha256": hashlib.sha256(canonical_json(manifest)).hexdigest()}
            baseline = self.freeze(revisions, provenance)
            plan.update(revisions={r["revision_id"]: r for r in revisions.values()}, metadata=catalog, baseline=baseline)
            view = {"kind": "baseline", "baseline_id": baseline["baseline_id"]}
        elif operation == "draft-open":
            revisions = selected["revisions"]
            require(command["work_order_id"] in revisions, 404, "UNKNOWN_IDENTITY", "Work order is absent from the selected baseline.")
            with self.evaluator.project(revisions) as root:
                catalog = self.evaluator.catalog(root)
                require(catalog[command["work_order_id"]]["type"] == "work_order", 422,
                        "INVALID_DRAFT", "A draft context must select a work order.")
                output = self.evaluator.cli(root, "check", "--artifact", command["work_order_id"])
            context_id = str(uuid4())
            plan["new_context"] = {"context_id": context_id, "base_baseline_id": command["base_baseline_id"],
                                   "work_order_id": command["work_order_id"]}
            context_versions = {"context_id": context_id, "before": None, "after": 0}
            view = {"kind": "context", "context_id": context_id, "context_version": 0}
        elif operation == "freeze":
            c = selected["context"]
            baseline = self.freeze(selected["revisions"], {"kind": "draft-context", "context_id": c["context_id"],
                                   "context_version": c["context_version"], "base_baseline_id": c["base_baseline_id"]})
            plan["baseline"] = baseline
            view = {"kind": "baseline", "baseline_id": baseline["baseline_id"]}
            context_versions = {"context_id": c["context_id"], "before": c["context_version"], "after": c["context_version"]}
        else:
            plan, output = self.prepare_draft(command, principal, selected, reserved)
            version = command["expected_context_version"]
            context_versions = {"context_id": command["context_id"], "before": version, "after": version + 1}
            view = {"kind": "context", "context_id": command["context_id"], "context_version": version + 1}
        plan["result"] = {"schema": RESULT, "operation_key": command["operation_key"],
                          "request_digest": "sha256:" + named_digest(command["schema"], command),
                          "project_id": self.project_id, "view": view,
                          "versions": {"project": {"before": command["expected_project_version"], "after": command["expected_project_version"] + 1},
                                       "context": context_versions}, "affected_revision_ids": [], "affected_artifacts": [],
                          "evaluator": EVALUATOR, "evaluator_output": output, "outcome": "accepted",
                          "http_status": 200, "receipt_id": str(uuid4())}
        return plan

    def freeze(self, revisions, provenance):
        try:
            value = make_baseline(project_id=self.project_id, revisions=revisions, provenance=provenance, evaluator=EVALUATOR)
        except CanonicalError as exc:
            raise Refusal(422, "INCOMPLETE_SELECTION", str(exc)) from exc
        require(len(canonical_json(value)) <= MAX_RESPONSE, 429, "RESOURCE_LIMIT", "Complete baseline exceeds 2 MiB.")
        return value

    def prepare_draft(self, command, principal, selected, reserved):
        revisions = selected["revisions"]
        with self.evaluator.project(revisions) as root:
            before_catalog = self.evaluator.catalog(root)
            if command["operation"] == "create-artifact":
                # Reserve identities outside this view using the release's allocation API.
                # Allocation sees a separate disposable catalog; no reserved content becomes governing input.
                artifact_id = command["artifact_id"]
                require(artifact_id is None or artifact_id not in reserved, 422, "INVALID_DRAFT", "Artifact identity is already reserved.")
                if artifact_id is None:
                    self.evaluator.enable_allocation(root)
                    # Ask the released allocator; if another context reserved its candidate,
                    # supply that reserved ID as an inert catalog entry and ask again.
                    # The release only scans IDs here, not synthetic authoring validity.
                    reserve_dir = root / "docs/engineering/sandbox-reservations"
                    reserve_dir.mkdir()
                    for identity in sorted(reserved - before_catalog.keys()):
                        (reserve_dir / (identity + ".md")).write_text('+++\nid = ' + json.dumps(identity) + '\n+++\n', encoding="utf-8")
                    try:
                        preview = self.evaluator.cli(root, "create-artifact", "--domain", command["domain"],
                                                     "--type", command["artifact_type"], "--dry-run")
                        artifact_id = preview.get("allocated_id")
                        require(artifact_id is not None, 422, "INVALID_DRAFT", "Released allocator could not allocate a draft ID.", evaluator_output=preview)
                    finally:
                        import shutil
                        shutil.rmtree(reserve_dir)
                created = self.evaluator.cli(root, "create-artifact", "--domain", command["domain"],
                                             "--type", command["artifact_type"], "--id", artifact_id)
                require(created.get("outcome") == "completed", 422, "INVALID_DRAFT", "Released template creation refused.", evaluator_output=created)
                path = created["changes"][0]["path"]
            else:
                artifact_id = command["artifact_id"]
                previous = revisions[artifact_id]
                require(previous["envelope"]["provenance"]["kind"] == "draft", 422,
                        "PROTECTED_FIELD", "Imported records are immutable; create a separate draft proposal.")
                path = previous["envelope"]["original_path"]
                (root / path).write_bytes(decode_document(command["document_base64"]))
            catalog = self.evaluator.catalog(root)
            require(artifact_id in catalog, 422, "PROTECTED_FIELD", "Draft identity cannot change.")
            metadata = catalog[artifact_id]
            if command["operation"] == "revise-artifact":
                protected = ("id", "type", "status", "lifecycle_events", "disposition", "approval", "approved_by",
                             "verified_by", "released_by", "commit", "git_object_format", "provenance", "evaluator")
                prior = before_catalog[artifact_id]["metadata"]
                if metadata["metadata"].get("type") != prior.get("type"):
                    typed = self.evaluator.cli(root, "validate-draft", "--artifact", artifact_id)
                    require(typed.get("admissible") is True, 422, "INVALID_DRAFT",
                            "Released draft admission refused the type/identity combination.", evaluator_output=typed)
                require(all(metadata["metadata"].get(k) == prior.get(k) for k in protected), 422,
                        "PROTECTED_FIELD", "Draft revision changes protected identity, lifecycle or provenance.")
            output = self.evaluator.cli(root, "validate-draft", "--artifact", artifact_id)
            require(output.get("admissible") is True, 422, "INVALID_DRAFT", "Released draft admission refused the proposed content.", evaluator_output=output)
            raw = (root / path).read_bytes()
            revision = make_revision(project_id=self.project_id, artifact_id=artifact_id, document=raw,
                                     original_path=path, declared_relations=metadata["relations"],
                                     provenance={"kind": "draft", "principal_id": principal["id"],
                                                 "operation_key": command["operation_key"],
                                                 "created_at": datetime.now(timezone.utc).isoformat()})
            return {"revisions": {revision["revision_id"]: revision}, "metadata": {artifact_id: metadata}}, output
