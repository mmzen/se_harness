"""Closed released-command adapter. No lifecycle state machine lives here."""
from __future__ import annotations

import base64
import copy
import hashlib
from contextlib import contextmanager

from .canonical import canonical_json, make_revision, named_digest
from .pilot_git import AUTHORITY, commit, decoded, initial, restore, safe_path, scan, snapshot
from .protocol import EVALUATOR, MAX_RESPONSE, Refusal, require

COMMAND = "se-harness-lifecycle-command/v2"
RESULT = "se-harness-lifecycle-result/v2"
READ_ONLY = {"check", "preflight", "validate"}


def refusal_result(project_id, exc):
    return {"schema": RESULT, "test_copy": True, "authority": AUTHORITY, "project_id": project_id,
            "outcome": "refused", "operation_key": None, "request_digest": None, "preview_digest": None,
            "receipt_id": None, "view": None, "versions": None, "baseline_id": None, "evaluator": EVALUATOR,
            "evaluator_output": exc.evaluator_output, "http_status": exc.status,
            "error": {"code": exc.code, "message": exc.message}, "affected_revision_ids": [],
            "affected_artifacts": [], "files": [], "provenance": None}


def binding(command, principal, selected, retained, source_inventory):
    inputs = {k: v for k, v in command.items() if k not in ("mode", "preview_digest", "operation_key")}
    inputs.update(principal_id=principal["id"], revisions={a: r["revision_id"] for a, r in selected["revisions"].items()},
                  snapshot_id=retained["snapshot_id"] if retained else None, source_inventory=source_inventory)
    return "sha256:" + named_digest(COMMAND, inputs)


@contextmanager
def project(service, selected, retained):
    with service.evaluator.project(selected["revisions"]) as root:
        if retained:
            restore(root, retained)
            for revision in selected["revisions"].values():
                target = root / safe_path(revision["envelope"]["original_path"])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(base64.b64decode(revision["document_base64"], validate=True))
        else:
            initial(root)
        yield root


class Adapter:
    def __init__(self, service, command, principal, selected, retained):
        self.service, self.evaluator = service, service.evaluator
        self.command, self.principal, self.selected, self.retained = command, principal, selected, retained
        self.action, self.steps = command["action"], []

    def invoke(self, root, name, *args, permit_failure=False):
        code, output = self.evaluator.invoke(["-m", "se_harness", name, root, *args, "--json"])
        self.steps.append({"command": name, "arguments": list(map(str, args)), "exit": code, "result": output})
        require(code == 0 or permit_failure, 422, "EVALUATOR_REFUSED", "Released evaluator refused the test operation.",
                evaluator_output={"commands": self.steps})
        return output

    def targets(self, catalog):
        a, kind = self.action, self.action["kind"]
        if kind == "transition":
            ids = {item["artifact"] for item in a["assignments"]}
            require(len(ids) == len(a["assignments"]), 400, "MALFORMED", "Duplicate transition target.")
        elif kind == "decide":
            ids = {a["artifact"]}
            require(a["artifact"] in catalog, 404, "UNKNOWN_IDENTITY", "Unknown test decision.")
            ids.update(x for x in catalog[a["artifact"]]["relations"].get("concerns", [])
                       if x in catalog and catalog[x]["type"] == "risk")
        elif kind == "handoff":
            ids = {a["work_order"]}
        elif kind in ("capture-verification", "prepare-release"):
            ids = set(a["work_orders"])
        elif kind == "raise-risk":
            ids = set(a["threatens"])
        else:
            return set()
        for artifact_id in ids:
            revision = self.selected["revisions"].get(artifact_id)
            require(revision is not None, 404, "UNKNOWN_IDENTITY", "Selected test artifact does not exist.")
            require(revision["envelope"]["provenance"]["kind"] in ("draft", "test-copy"),
                    422, "PROTECTED_FIELD", "Imported records cannot receive rehearsal decisions or evidence.")
        return ids

    def execute(self, root, catalog):
        a, kind = self.action, self.action["kind"]
        if kind == "validate":
            self.invoke(root, "validate", permit_failure=True)
        elif kind == "check":
            args = ["--artifact", a["artifact"]]
            for key in ("checkpoint", "from_git"):
                if key in a:
                    args += ["--" + key.replace("_", "-"), a[key]]
            self.invoke(root, "check", *args, permit_failure=True)
        elif kind == "preflight":
            self.invoke(root, "preflight", "--work-order", a["work_order"], "--phase", a["phase"], permit_failure=True)
        elif kind == "transition":
            args = []
            for item in a["assignments"]:
                ident = item["artifact"]
                args += ["--set", ident + "=" + item["state"], "--decision", ident + "=" + item["actor"],
                         "--reason", ident + "=" + item["reason"]]
            self.invoke(root, "transition", *args)
            self.invoke(root, "transition", *args, "--apply")
        elif kind == "decide":
            args = ["--artifact", a["artifact"], "--decision", a["decision"], "--reason", a["reason"]]
            for key in ("option", "authority_owner", "revisit"):
                if key in a:
                    args += ["--" + key.replace("_", "-"), a[key]]
            if a["disposition"] != "decide":
                args += ["--" + a["disposition"]]
            for key in ("scope", "mitigated_by", "avoided_by"):
                for value in a.get(key, []):
                    args += ["--" + key.replace("_", "-"), value]
            self.invoke(root, "decide", *args)
            self.invoke(root, "decide", *args, "--apply")
        elif kind == "raise-risk":
            args = []
            for key in ("domain", "id", "title", "description", "action", "owner", "raised_by", "stage", "category", "likelihood", "impact", "recommend"):
                if key in a:
                    args += ["--" + key.replace("_", "-"), str(a[key])]
            for ident in a["threatens"]:
                args += ["--threatens", ident]
            if "decision_id" in a:
                args += ["--with-decision", "--decision-id", a["decision_id"]]
            self.invoke(root, "raise-risk", *args, "--dry-run")
            self.invoke(root, "raise-risk", *args)
        elif kind == "handoff":
            ids = {item["path"] for item in a["files"]}
            require(len(ids) == len(a["files"]), 400, "MALFORMED", "Duplicate handoff input path.")
            formal_paths = {v["path"] for v in catalog.values()}
            for item in a["files"]:
                name = safe_path(item["path"])
                parts = name.split("/")
                require(name not in formal_paths and not any(p.startswith(".") for p in parts)
                        and parts[-1] not in ("AGENTS.md", "CLAUDE.md", "ENGINEERING_HARNESS.md")
                        and (not name.startswith("docs/engineering/") or "/evidence/" in name),
                        422, "PROTECTED_FIELD", "Handoff inputs cannot replace formal or instruction files.")
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(decoded(item))
            args = ["--artifact", a["work_order"], "--checkpoint", "scope", "--changes-complete"]
            for name in sorted(ids):
                args += ["--changed-path", name]
            if ids:
                self.invoke(root, "check", *args)
            self.invoke(root, "preflight", "--work-order", a["work_order"], "--phase", "review")
            self.invoke(root, "evidence", "--artifact", a["work_order"], "--checkpoint", "handoff")
            self.invoke(root, "check", "--artifact", a["work_order"], "--checkpoint", "handoff", "--from-git", a["from_git"])
        elif kind == "capture-verification":
            args = ["--id", a["id"], "--domain", a["domain"], "--owner", a["owner"]]
            for key, flag in (("work_orders", "work-order"), ("verifications", "verification"), ("evidence", "evidence")):
                for value in a[key]:
                    args += ["--" + flag, value]
            self.invoke(root, "capture-verification", *args)
        elif kind == "prepare-release":
            args = []
            for key in ("id", "domain", "release_contract", "verification_record", "version", "owner", "tag"):
                args += ["--" + key.replace("_", "-"), a[key]]
            for value in a["work_orders"]:
                args += ["--work-order", value]
            self.invoke(root, "prepare-release", *args)
        else:
            raise Refusal(400, "MALFORMED", "Unsupported closed test action.")

    def allowed(self, catalog, targets):
        a, kind = self.action, self.action["kind"]
        if kind in READ_ONLY:
            return set(), set()
        ids, paths = set(), set()
        if kind in ("transition", "decide"):
            ids = targets
            paths = {catalog[i]["path"] for i in ids}
        elif kind == "raise-risk":
            ids = {a["id"]} | ({a["decision_id"]} if "decision_id" in a else set())
            paths = {f"docs/engineering/{a['domain']}/risks/{a['id']}.md"}
            if "decision_id" in a:
                paths.add(f"docs/engineering/{a['domain']}/decisions/{a['decision_id']}.md")
        elif kind in ("capture-verification", "prepare-release"):
            ids = {a["id"]}
            folder = "verification-records" if kind == "capture-verification" else "releases"
            paths = {f"docs/engineering/{a['domain']}/{folder}/{a['id']}.md",
                     f"docs/engineering/{a['domain']}/evidence/{a['id']}-evaluator.json"}
        elif kind == "handoff":
            domain = catalog[a["work_order"]]["path"].rsplit("/", 2)[0]
            prefix = domain + "/evidence/" + a["work_order"] + "/"
            paths = {prefix + a["work_order"] + "-handoff.md", prefix + "handoff.json"}
            paths.update(item["path"] for item in a["files"])
        return ids, paths

    def prepare(self):
        command, action = self.command, self.action
        mode, kind = command["mode"], action["kind"]
        require((kind in READ_ONLY) == (mode == "inspect"), 400, "MALFORMED", "Read actions use inspect; mutations use preview/apply.")
        input_digest = binding(command, self.principal, self.selected, self.retained, self.evaluator.support)
        require(mode != "apply" or command["preview_digest"] == input_digest, 409,
                "STALE_PREVIEW", "Apply needs a preview bound to these exact inputs.")
        with project(self.service, self.selected, self.retained) as root:
            before, catalog = scan(root), self.evaluator.catalog(root)
            targets = self.targets(catalog)
            permitted_ids, permitted_paths = self.allowed(catalog, targets)
            candidates = copy.deepcopy(self.retained["candidates"] if self.retained else [])
            source = self.evaluator.manifest["source"]
            input_snapshot = input_baseline = None
            if kind not in READ_ONLY:
                input_snapshot = snapshot(root, source=source, evaluator=EVALUATOR, candidates=candidates)
                input_baseline = self.service.freeze(self.selected["revisions"], {
                    "kind": "test-copy", "source": source, "snapshot_id": input_snapshot["snapshot_id"]})
            if kind == "capture-verification":
                candidate = commit(root, "Materialize exact rehearsal candidate")
                require(action["id"] not in catalog, 422, "PROTECTED_FIELD", "Capture must create a new record.")
                candidates.append({"input_baseline": input_baseline["baseline_id"], "source": source,
                    "test_candidate": candidate, "verification_record": action["id"], "evaluator": EVALUATOR,
                    "files": {p: hashlib.sha256(raw).hexdigest() for p, raw in sorted(before.items())},
                    "implementation_candidate": "separate actual qualification record; never this test candidate"})
            self.execute(root, catalog)
            after, actual_catalog = scan(root), self.evaluator.catalog(root)
            require(set(before) <= set(after), 422, "UNEXPECTED_OUTPUT", "Evaluator deleted a projection file.")
            changed = {p for p, raw in after.items() if before.get(p) != raw}
            require(changed <= permitted_paths, 422, "UNEXPECTED_OUTPUT", "Evaluator wrote outside this closed operation's file set.")
            require(set(catalog) <= set(actual_catalog), 422, "UNEXPECTED_OUTPUT", "Evaluator removed an artifact.")
            revisions, metadata = {}, {}
            for ident, item in actual_catalog.items():
                if item["path"] not in changed:
                    continue
                require(ident in permitted_ids, 422, "UNEXPECTED_OUTPUT", "Unexpected affected formal artifact.")
                previous = self.selected["revisions"].get(ident)
                require(previous is None or previous["envelope"]["provenance"]["kind"] in ("draft", "test-copy"),
                        422, "PROTECTED_FIELD", "Imported formal bytes are immutable.")
                raw = after[item["path"]]
                sidecar = item["metadata"].get("evaluator_evidence_path")
                if sidecar:
                    require(sidecar in after and hashlib.sha256(after[sidecar]).hexdigest() == item["metadata"].get("evaluator_evidence_sha256"),
                            422, "UNEXPECTED_OUTPUT", "Generated record has a missing or mismatched evaluator sidecar.")
                revision = make_revision(project_id=self.service.project_id, artifact_id=ident, document=raw,
                    original_path=item["path"], declared_relations=item["relations"],
                    provenance={"kind": "test-copy", "test_copy": True, "principal_id": self.principal["id"],
                                "input_digest": input_digest, "operation_key": command["operation_key"]})
                revisions[revision["revision_id"]], metadata[ident] = revision, item
            result = {"schema": RESULT, "test_copy": True, "authority": AUTHORITY,
                "project_id": self.service.project_id, "operation_key": command["operation_key"],
                "request_digest": "sha256:" + named_digest(COMMAND, command), "preview_digest": input_digest,
                "receipt_id": None, "view": self.selected["view"], "versions": None, "baseline_id": None,
                "evaluator": EVALUATOR, "evaluator_output": {"commands": self.steps}, "http_status": 200, "error": None,
                "outcome": "inspected" if mode == "inspect" else "previewed",
                "affected_revision_ids": sorted(revisions),
                "affected_artifacts": sorted([{"artifact_id": r["envelope"]["artifact_id"], "revision_id": k} for k, r in revisions.items()], key=lambda r: r["artifact_id"]),
                "files": [{"path": p, "bytes": len(after[p]), "sha256": hashlib.sha256(after[p]).hexdigest()} for p in sorted(changed)],
                "provenance": {"test_copy": True, "source": source, "candidates": candidates,
                               "input_baseline": input_baseline["baseline_id"] if input_baseline else None,
                               "input_git_head": input_snapshot["head"] if input_snapshot else None}}
            plan = {"revisions": revisions, "metadata": metadata, "result": result}
            if mode == "apply":
                retained = snapshot(root, source=source, evaluator=EVALUATOR, candidates=candidates)
                combined = {**self.selected["revisions"], **{r["envelope"]["artifact_id"]: r for r in revisions.values()}}
                output_baseline = self.service.freeze(combined, {"kind": "test-copy", "snapshot_id": retained["snapshot_id"], "source": source})
                plan.update(snapshot=retained, baseline=output_baseline,
                            input_baseline=input_baseline, input_snapshot=input_snapshot)
                result.update(outcome="accepted", baseline_id=output_baseline["baseline_id"],
                    view={"kind": "context", "context_id": command["context_id"], "context_version": command["expected_context_version"] + 1},
                    receipt_id="sha256:" + named_digest(RESULT, {"principal": self.principal["id"], "request": result["request_digest"]}),
                    versions={"project": {"before": command["expected_project_version"], "after": command["expected_project_version"] + 1},
                              "context": {"context_id": command["context_id"], "before": command["expected_context_version"], "after": command["expected_context_version"] + 1}})
                result["provenance"]["output_git_head"] = retained["head"]
            require(len(canonical_json(result)) <= MAX_RESPONSE, 429, "RESOURCE_LIMIT", "Complete test result exceeds 2 MiB.")
            return plan
