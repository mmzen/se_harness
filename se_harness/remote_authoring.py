"""File inputs and evidence-backed views of existing remote operations.

No lifecycle selection, version refresh or automatic mutation retry lives here.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import time
import uuid
from pathlib import Path

from se_harness.remote import RemoteError, strict_json
from se_harness.resources import _read, _safe_path

TYPED_FIELDS = ("evaluator_file", "source_manifest", "operation_key", "expected_project_version",
                "work_order", "domain", "artifact_type", "artifact", "expected_revision", "document_file")
TYPES = ("intent", "capability", "requirement", "specification", "architecture", "adr",
         "verification", "work_order", "release_contract", "operating_contract")


def register(parser):
    parser.add_argument("--typed", action="store_true", help="construct the existing request from explicit fields")
    for field in TYPED_FIELDS:
        parser.add_argument("--" + field.replace("_", "-"), type=int if field == "expected_project_version" else str)
    parser.add_argument("--record-directory", help="new local directory for exact request/response evidence")
    parser.add_argument("--compact", action="store_true", help="concise fields backed by --record-directory")
    parser.add_argument("--include-document", action="store_true", help="after create, read its exact revision (no further mutation)")


def encoded(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")


def file_bytes(value, limit):
    if not value:
        raise RemoteError("A required file input is missing.")
    return _read(Path(value), limit=limit)


def matches(value, pattern, label):
    if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
        raise RemoteError("Invalid or missing " + label + ".")
    return value


def integer(value, label):
    if type(value) is not int or not 0 <= value <= 9223372036854775807:
        raise RemoteError("An integer from 0 through 9223372036854775807 is required for " + label + ".")
    return value


def identifier(value, label):
    try:
        if str(uuid.UUID(value, version=4)) != value:
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise RemoteError("Invalid or missing " + label + " UUIDv4.") from None
    return value


def manifest(value):
    """Validate the existing manifest shape, leaving Git and graph checks to the service."""
    if not isinstance(value, dict) or set(value) != {"schema", "source", "artifacts"} or value["schema"] != "se-harness-source-manifest/v1":
        raise RemoteError("Invalid source manifest.")
    source = value["source"]
    if not isinstance(source, dict) or set(source) != {"repository", "object_format", "commit"} or source["object_format"] != "sha1":
        raise RemoteError("Invalid source identity.")
    matches(source["commit"], r"[0-9a-f]{40}", "source commit")
    matches(source["repository"], r"[^\x00-\x1f]+", "source repository")
    if not isinstance(value["artifacts"], list) or len(value["artifacts"]) > 2500:
        raise RemoteError("Invalid source artifact list.")
    for item in value["artifacts"]:
        if not isinstance(item, dict) or set(item) != {"artifact_id", "path", "blob_oid", "raw_sha256", "bytes"}:
            raise RemoteError("Invalid source artifact entry.")
        matches(item["artifact_id"], r"[A-Z]+-[A-Z0-9]+-[0-9]{3,}", "artifact ID")
        matches(item["blob_oid"], r"[0-9a-f]{40}", "blob ID")
        matches(item["raw_sha256"], r"[0-9a-f]{64}", "document digest")
        path = item["path"]
        if not isinstance(path, str) or "\\" in path or ":" in path or any(c in path for c in "\r\n\x00") or any(p in {"", ".", ".."} for p in path.split("/")):
            raise RemoteError("Unsafe source path.")
        if not 1 <= integer(item["bytes"], "source bytes") <= 1048576:
            raise RemoteError("Invalid source byte count.")
    return value


def typed_request(args):
    op = args.operation
    common = {"evaluator_file", "operation_key", "expected_project_version"}
    allowed = {
        "import": common | {"source_manifest"},
        "draft-open": common | {"baseline", "work_order"},
        "create-artifact": common | {"context", "context_version", "domain", "artifact_type", "artifact"},
        "revise-artifact": common | {"context", "context_version", "artifact", "expected_revision", "document_file"},
        "read": {"baseline", "context", "context_version", "artifact", "expected_revision"},
    }
    if op not in allowed or args.request:
        raise RemoteError("Typed mode supports import, draft-open, create-artifact, revise-artifact and revision read; it cannot use --request.")
    for field in (*TYPED_FIELDS, "baseline", "context", "context_version", "key", "destination"):
        if getattr(args, field, None) is not None and field not in allowed[op]:
            raise RemoteError("Input does not apply to this typed operation: --" + field.replace("_", "-"))
    project = identifier(args.project, "project")
    artifact = getattr(args, "artifact", None)
    if artifact is not None or op in {"read", "revise-artifact"}:
        matches(artifact, r"[A-Z]+-[A-Z0-9]+-[0-9]{3,}", "artifact ID")
    if op == "read":
        if bool(args.baseline) == bool(args.context) or (args.baseline and args.context_version is not None):
            raise RemoteError("Select exactly one baseline or versioned context.")
        view = ({"kind": "baseline", "baseline_id": matches(args.baseline, r"se-harness-artifact-baseline/v1:sha256:[0-9a-f]{64}", "baseline")}
                if args.baseline else {"kind": "context", "context_id": identifier(args.context, "context"),
                                      "context_version": integer(args.context_version, "context version")})
        return revision_request(project, view, artifact, args.expected_revision)
    evaluator = strict_json(file_bytes(args.evaluator_file, 8192))
    if not isinstance(evaluator, dict) or set(evaluator) != {"version", "archive_sha256", "payload_sha256"}:
        raise RemoteError("Evaluator file must contain exactly version, archive_sha256 and payload_sha256.")
    matches(evaluator["version"], r"[^\x00-\x1f]+", "evaluator version")
    for field in ("archive_sha256", "payload_sha256"):
        matches(evaluator[field], r"[0-9a-f]{64}", field)
    result = {"schema": "se-harness-remote-command/v1", "operation": op, "project_id": project,
              "operation_key": matches(args.operation_key, r"[^\x00-\x1f]{1,128}", "operation key"),
              "expected_project_version": integer(args.expected_project_version, "project version"), "expected_evaluator": evaluator}
    if op == "import":
        result["source_manifest"] = manifest(strict_json(file_bytes(args.source_manifest, 4 * 1024 * 1024)))
    elif op == "draft-open":
        result.update(base_baseline_id=matches(args.baseline, r"se-harness-artifact-baseline/v1:sha256:[0-9a-f]{64}", "baseline"),
                      work_order_id=matches(args.work_order, r"WO-[A-Z0-9]+-[0-9]{3,}", "work order"))
    else:
        result.update(context_id=identifier(args.context, "context"), expected_context_version=integer(args.context_version, "context version"), artifact_id=artifact)
        if op == "create-artifact":
            if args.artifact_type not in TYPES:
                raise RemoteError("Select a supported --artifact-type.")
            result.update(domain=matches(args.domain, r"[a-z0-9]+(?:-[a-z0-9]+)*", "domain"), artifact_type=args.artifact_type)
        else:
            raw = file_bytes(args.document_file, 1048576)
            raw.decode("utf-8")
            if not raw:
                raise RemoteError("The document is empty.")
            result.update(expected_revision_id=matches(args.expected_revision, r"sha256:[0-9a-f]{64}", "revision"), document_base64=base64.b64encode(raw).decode("ascii"))
    return result


def revision_request(project, view, artifact, revision):
    return {"schema": "se-harness-graph-read/v1", "operation": "revision", "project_id": project,
            "view": view, "artifact_id": artifact, "revision_id": matches(revision, r"sha256:[0-9a-f]{64}", "revision"),
            "budget": {"rows": 1, "bytes": 2097152, "depth": 0}}


class Capture:
    """Retain exact exchanges before rendering; incomplete stays visible on failure."""
    def __init__(self, destination, token):
        self.path = _safe_path(Path(destination))
        if self.path.exists() or not self.path.parent.is_dir():
            raise RemoteError("Evidence destination must be new with an existing parent directory.")
        self.token = token.encode()
        self.started = time.monotonic()
        self.sent = False
        self.index = 0
        self.key = None
        self.exchanges = []
        self.path.mkdir()
        self.write(".incomplete", b"Incomplete remote capture; inspect original operation key before retry.\n")

    def write(self, name, raw):
        if self.token and self.token in raw:
            raise RemoteError("Refusing credential content in remote evidence.")
        path = self.path / name
        _safe_path(path)
        with path.open("xb") as stream:
            stream.write(raw)
        if path.read_bytes() != raw:
            raise RemoteError("Remote evidence readback differs.")
        return path

    def request(self, method, path, payload):
        self.index += 1
        self.exchange_started = time.monotonic()
        self.key = (payload or {}).get("operation_key", self.key)
        prefix = str(self.index)
        raw = encoded(payload) if payload is not None else b""
        self.write(prefix + "-request.json", raw)
        self.exchanges.append({"method": method, "path": path, "request": prefix + "-request.json",
                               "request_sha256": hashlib.sha256(raw).hexdigest()})

    def response(self, status, raw, *, complete=True):
        name = str(self.index) + "-response.json"
        self.write(name, raw)
        self.exchanges[-1].update(status=status, response=name, response_sha256=hashlib.sha256(raw).hexdigest(),
                                 body_complete=complete, elapsed_seconds=round(time.monotonic() - self.exchange_started, 6))

    def finish(self, exit_code, outcome):
        self.write("capture.json", encoded({"exchanges": self.exchanges, "exit": exit_code, "outcome": outcome,
            "sent": self.sent, "operation_key": self.key, "elapsed_seconds": round(time.monotonic() - self.started, 6)}))
        (self.path / ".incomplete").unlink()

    def compact(self, result, *, response_name=None):
        """Keep exact small fields; make every omission explicit and readable."""
        omitted, documents = [], []
        response_name = response_name or str(self.index) + "-response.json"
        remaining = [16000]
        validation = result.get("evaluator_output") if isinstance(result, dict) else None
        discovery = validation.get("instruction_discovery", {}) if isinstance(validation, dict) else {}
        instructions = discovery.get("agent_instructions", {}) if isinstance(discovery, dict) else {}
        # Keep the selected step, its prerequisites and executable procedure in view.
        # The full instruction catalogue and machine-policy inputs remain in evidence.
        deferred = set()
        if (isinstance(validation, dict) and validation.get("schema") == "se-harness-workflow-result-v2"
                and isinstance(instructions, dict) and isinstance(instructions.get("current_step"), dict)
                and instructions["current_step"].get("location")):
            deferred = {
                "/evaluator_output/instruction_discovery/agent_instructions/procedure/steps",
                "/evaluator_output/instruction_discovery/evaluator_only_inputs",
            }
        def render(value, pointer=""):
            if pointer in deferred:
                note = {"pointer": pointer, "reason": "instruction catalogue in full_response"}
                replacement = {"omitted": True}
                if len(encoded(value)) > len(encoded(note)) + len(encoded(replacement)):
                    omitted.append(note)
                    return replacement
            if isinstance(value, dict) and "document_base64" in value:
                raw = base64.b64decode(value["document_base64"], validate=True)
                digest = hashlib.sha256(raw).hexdigest()
                if (len(raw) > 1048576 or value.get("envelope", {}).get("document_sha256") != digest or
                        base64.b64encode(raw).decode("ascii") != value["document_base64"]):
                    raise RemoteError("Returned document bytes differ from their declared identity.")
                name = str(self.index) + "-document-" + str(len(documents) + 1) + ".md"
                path = self.write(name, raw)
                document = {"path": str(path), "sha256": digest, "bytes": len(raw)}
                if len(raw) <= 6000:
                    document["text"] = raw.decode("utf-8")
                documents.append(document)
                omitted.append({"pointer": pointer + "/document_base64", "reason": "decoded exact document", "path": str(path)})
                value = {k: v for k, v in value.items() if k != "document_base64"}
            if isinstance(value, dict):
                return {k: render(v, pointer + "/" + k.replace("~", "~0").replace("/", "~1")) for k, v in value.items()}
            size = len(encoded(value))
            if size > remaining[0]:
                omitted.append({"pointer": pointer, "reason": "display budget", "path": str(self.path / response_name), "required_reading": True})
                return {"omitted": True, "read": str(self.path / response_name), "pointer": pointer}
            remaining[0] -= size
            return value
        visible = render(result)
        view = {"schema": "se-harness-remote-view/v1", "result": visible, "documents": documents, "omitted": omitted,
                "findings_complete": not any(item.get("required_reading") for item in omitted),
                "evidence": str(self.path), "full_response": str(self.path / response_name)}
        if isinstance(validation, dict) and validation.get("schema") == "se-harness-draft-validation-v1":
            # This describes the evaluator's existing boundary, not a content verdict.
            view["draft_review"] = {"validation_scope": "draft_shape_and_required_links",
                                    "content_review": "not_assessed",
                                    "source": "/result/evaluator_output"}
        return view
