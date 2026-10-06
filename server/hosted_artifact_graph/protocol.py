"""Closed wire decoding and remote errors, separate from evaluator admission."""
from __future__ import annotations

import base64
import copy
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from .canonical import canonical_json, decode_json, named_digest

EVALUATOR = {
    "version": "0.22.1",
    "archive_sha256": "cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053",
    "payload_sha256": "0e7b7c2bc10b06150c6c1ebe88d796d047f5d906bdfb5ef4e00914a56c79e7ff",
}
COMMAND = "se-harness-remote-command/v1"
READ = "se-harness-graph-read/v1"
RESULT = "se-harness-remote-result/v1"
MAX_RESPONSE = 2 * 1024 * 1024
MAX_REQUEST = 4 * 1024 * 1024
MAX_REVISIONS = 10000
SCHEMA_REVISION = 1


def contract_path(name):
    installed = Path(sys.prefix) / "share/se-harness-hosted/contracts" / name
    return installed if installed.is_file() else Path(__file__).parent.parent / "contracts" / name


class Refusal(Exception):
    def __init__(self, status, code, message, *, evaluator_output=None):
        super().__init__(message)
        self.status, self.code, self.message = status, "HAG_REMOTE_" + code, message
        self.evaluator_output = evaluator_output

    def result(self):
        return dict(schema=RESULT, operation_key=None, request_digest=None,
                    project_id=None, view=None, versions=None, affected_revision_ids=[],
                    affected_artifacts=[], evaluator=None, evaluator_output=self.evaluator_output,
                    outcome="refused", receipt_id=None, http_status=self.status,
                    error={"code": self.code, "message": self.message})


def require(condition, status, code, message, **kwargs):
    if not condition:
        raise Refusal(status, code, message, **kwargs)


class Wire:
    def __init__(self):
        self.schemas = {}
        registry = Registry()
        for filename in ("remote-v1.json", "read-v1.json", "result-v1.json",
                         "lifecycle-v2.json", "lifecycle-result-v2.json", "export-v2.json", "read-result-v2.json"):
            schema = json.loads(contract_path(filename).read_text(encoding="utf-8"))
            self.schemas[filename] = schema
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
        self.registry = registry

    def validate(self, value, filename, definition=None):
        schema = self.schemas[filename]
        if definition:
            schema = {"$ref": schema["$id"] + "#/$defs/" + definition}
        validator = Draft202012Validator(schema, registry=self.registry, format_checker=FormatChecker())
        # Do not echo submitted documents or authentication material in diagnostics.
        require(validator.is_valid(value), 400, "MALFORMED", "Request does not match the closed wire schema.")

    def command(self, value):
        require(isinstance(value, dict), 400, "MALFORMED", "Expected one command object.")
        require(value.get("operation") in {"import", "draft-open", "create-artifact", "revise-artifact", "freeze"},
                400, "UNSUPPORTED_OPERATION", "Only sandbox draft operations are supported.")
        if value.get("operation") == "import" and "source_manifest" in value:
            try:
                self.validate(value["source_manifest"], "remote-v1.json", "SourceManifest")
            except Refusal as exc:
                raise Refusal(422, "INVALID_IMPORT", "Only a complete versioned Git source manifest is supported.") from exc
        self.validate(value, "remote-v1.json")
        command = copy.deepcopy(value)
        if "document_base64" in command:
            decode_document(command["document_base64"])
        if "source_manifest" in command:
            entries = command["source_manifest"]["artifacts"]
            for key in ("path", "artifact_id"):
                require(len({e[key].casefold() for e in entries}) == len(entries), 422,
                        "INVALID_IMPORT", "Source manifest contains duplicate " + key + ".")
            entries.sort(key=lambda e: (e["path"], e["artifact_id"]))
        digest = "sha256:" + named_digest(COMMAND, command)
        return command, digest


def decode_document(encoded):
    try:
        raw = base64.b64decode(encoded, validate=True)
        require(base64.b64encode(raw).decode("ascii") == encoded, 400, "MALFORMED", "Noncanonical base64.")
    except (ValueError, TypeError) as exc:
        raise Refusal(400, "MALFORMED", "Invalid document base64.") from exc
    require(len(raw) <= 1024 * 1024, 429, "RESOURCE_LIMIT", "Document exceeds 1 MiB.")
    try:
        raw.decode("utf-8")
    except UnicodeError as exc:
        raise Refusal(422, "INVALID_DRAFT", "Document is not UTF-8.") from exc
    return raw


def contained_file(root: Path, relative: str):
    require(isinstance(relative, str) and relative and "\\" not in relative and ":" not in relative
            and "\x00" not in relative and all(p not in ("", ".", "..") for p in relative.split("/")),
            422, "BINDING_UNAVAILABLE", "Invalid contained source path.")
    path = root
    for part in relative.split("/"):
        path = path / part
        require(not path.is_symlink(), 422, "BINDING_UNAVAILABLE", "Source links are not supported.")
    require(path.resolve().is_relative_to(root.resolve()) and path.is_file(), 422,
            "BINDING_UNAVAILABLE", "Missing regular source file: " + relative)
    return path
