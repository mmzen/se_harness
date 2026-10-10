"""Standard-library client for the explicitly selected hosted draft sandbox.

This transport has no local authoring fallback, lifecycle policy or retry/rebase.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

from se_harness import __version__

LIMIT = 2 * 1024 * 1024
MUTATIONS = {"import": "imports", "draft-open": "contexts", "freeze": "baselines",
             "create-artifact": "commands", "revise-artifact": "commands"}


class RemoteError(ValueError):
    pass


class TransportUncertain(RemoteError):
    pass


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise RemoteError("Duplicate JSON object key.")
            result[key] = value
        return result

    def number(value):
        raise RemoteError("Remote requests require integer JSON numbers.")

    return json.loads(raw, object_pairs_hook=pairs, parse_float=number, parse_constant=number)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        fp.close()
        raise RemoteError("Sandbox redirects are refused; no credential was forwarded.")

    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302


def endpoint_url(value):
    parsed = urllib.parse.urlsplit(value)
    if (parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
            or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in {"", "/"}):
        raise RemoteError("The private sandbox requires an explicit loopback HTTP endpoint.")
    return value.rstrip("/")


def installed_client(wheel):
    path = Path(wheel)
    root = Path(__file__).resolve().parent.parent
    try:
        with zipfile.ZipFile(path) as archive:
            members = [n for n in archive.namelist() if n.startswith("se_harness/") and not n.endswith("/")]
            if not members or any((root / name).read_bytes() != archive.read(name) for name in members):
                raise RemoteError("Client wheel does not match the executing installed package.")
            metadata = [n for n in archive.namelist() if n.endswith(".dist-info/METADATA")]
            if len(metadata) != 1 or ("\nVersion: " + __version__ + "\n") not in archive.read(metadata[0]).decode():
                raise RemoteError("Client wheel version does not match the executing package.")
    except (OSError, zipfile.BadZipFile) as exc:
        raise RemoteError("Cannot inspect the exact client wheel.") from exc
    return {"version": __version__, "wheel_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def send(endpoint, token, method, path, payload=None, timeout=130, *, capture=None):
    if not token or "\r" in token or "\n" in token:
        raise RemoteError("The named secret source contains no usable sandbox credential.")
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode() if payload is not None else None
    request = urllib.request.Request(endpoint_url(endpoint) + path, data=data, method=method,
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json", "Accept": "application/json"})
    # Ignore proxy environment variables for the private loopback sandbox.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        try:
            response = opener.open(request, timeout=timeout)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            raw = response.read(LIMIT + 1)
            if capture:
                capture.response(response.status, raw, complete=len(raw) <= LIMIT)
            if len(raw) > LIMIT:
                raise TransportUncertain("Remote response exceeds 2 MiB; its outcome is unknown.")
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise TransportUncertain("Remote response is not an object; its outcome is unknown.")
            return response.status, value
    except TransportUncertain:
        raise
    except (OSError, urllib.error.URLError, ValueError) as exc:
        # Never include credentials, response bodies, or a guessed refused receipt.
        raise TransportUncertain("Remote transport is uncertain. Look up the original operation key or retry the identical request; do not change its expected versions.") from exc


def register(commands):
    parser = commands.add_parser("remote", help="use an explicit private hosted sandbox; no local fallback")
    parser.add_argument("operation", choices=["status", "baseline", "operation", "read", "check", "query", "rehearse", "export", *MUTATIONS])
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--project")
    parser.add_argument("--token-env", required=True, help="name of an environment variable containing a sandbox token")
    parser.add_argument("--request", help="complete versioned JSON request file; never a credential file")
    parser.add_argument("--client-wheel", help="exact separately installed candidate wheel")
    parser.add_argument("--baseline")
    parser.add_argument("--context")
    parser.add_argument("--context-version", type=int)
    parser.add_argument("--key")
    parser.add_argument("--test-copy", action="store_true", help="explicitly select test data; Git remains authoritative")
    parser.add_argument("--destination", help="new destination for an exact test export")
    parser.add_argument("--json", action="store_true")
    from se_harness.remote_authoring import register as register_authoring
    register_authoring(parser)
    parser.set_defaults(handler=run)


def run(args):
    from se_harness.remote_authoring import Capture, TYPED_FIELDS, encoded, file_bytes, revision_request, typed_request
    capture = None
    sent = False
    payload = None
    token = os.environ.get(args.token_env, "")
    try:
        endpoint_url(args.endpoint)
        if not token or "\r" in token or "\n" in token:
            raise RemoteError("The named secret source contains no usable sandbox credential.")
        op = args.operation
        typed = getattr(args, "typed", False)
        compact = getattr(args, "compact", False)
        include_document = getattr(args, "include_document", False)
        destination = getattr(args, "record_directory", None)
        if compact and not destination:
            raise RemoteError("--compact requires --record-directory.")
        if include_document and (op != "create-artifact" or not compact):
            raise RemoteError("--include-document requires create-artifact with --compact.")
        if not typed and any(getattr(args, field, None) is not None for field in TYPED_FIELDS):
            raise RemoteError("Typed fields require --typed and cannot be mixed with --request.")
        if typed:
            payload = typed_request(args)
        if op == "status":
            method, path, payload = "GET", "/v1/status", None
        else:
            if not args.project:
                raise RemoteError("--project is required.")
            base = "/v1/projects/" + urllib.parse.quote(args.project, safe="")
            if op in {"baseline", "operation"}:
                identifier = args.baseline if op == "baseline" else args.key
                if not identifier:
                    raise RemoteError("The exact --baseline or --key is required.")
                method, path, payload = "GET", base + ("/baselines/" if op == "baseline" else "/operations/") + urllib.parse.quote(identifier, safe=""), None
            else:
                if not typed and not args.request:
                    raise RemoteError("--request must name the explicit versioned request.")
                if not typed:
                    payload = strict_json(file_bytes(args.request, 4 * 1024 * 1024))
                if not isinstance(payload, dict) or payload.get("project_id", args.project) != args.project:
                    raise RemoteError("Request and selected project disagree.")
                payload["project_id"] = args.project
                if op in {"rehearse", "export"}:
                    if not getattr(args, "test_copy", False) or payload.get("test_copy") is not True:
                        raise RemoteError("--test-copy and test_copy=true are required; actors are test inputs only.")
                    if not args.client_wheel:
                        raise RemoteError("--client-wheel must identify the separately installed candidate client.")
                    identity = installed_client(args.client_wheel)
                    if payload.get("client", identity) != identity:
                        raise RemoteError("Request client identity differs from the installed package.")
                    payload["client"] = identity
                    base = "/v2/projects/" + urllib.parse.quote(args.project, safe="")
                    route = "rehearsals" if op == "rehearse" else "exports"
                    if op == "export":
                        new_export_destination(getattr(args, "destination", None))
                elif op in MUTATIONS:
                    if not args.client_wheel:
                        raise RemoteError("--client-wheel must identify the separately installed candidate client.")
                    identity = installed_client(args.client_wheel)
                    if payload.get("client", identity) != identity or payload.get("operation") != op:
                        raise RemoteError("Request operation or client identity disagrees with the actual invocation.")
                    payload["client"] = identity
                    route = MUTATIONS[op]
                else:
                    wanted = "cypher" if op == "query" else "check" if op == "check" else payload.get("operation")
                    if payload.get("operation") != wanted:
                        raise RemoteError("Request operation disagrees with the selected read.")
                    if args.baseline and args.context:
                        raise RemoteError("Select one view.")
                    selector = ({"kind": "baseline", "baseline_id": args.baseline} if args.baseline else
                                {"kind": "context", "context_id": args.context, "context_version": args.context_version} if args.context else None)
                    if selector and payload.get("view", selector) != selector:
                        raise RemoteError("Request and CLI view disagree.")
                    if selector:
                        payload["view"] = selector
                    route = "reads/" + urllib.parse.quote(str(wanted), safe="")
                method, path = "POST", base + "/" + route
        wire = encoded(payload) if payload is not None else b""
        if len(wire) > 4 * 1024 * 1024 or token.encode() in wire:
            raise RemoteError("Oversized request or credential content in request; refused before sending.")
        if payload and "document_base64" in payload and token.encode() in base64.b64decode(payload["document_base64"], validate=True):
            raise RemoteError("Credential content in document; refused before sending.")
        if destination:
            capture = Capture(destination, token)
            capture.request(method, path, payload)
        sent = True
        if capture:
            capture.sent = True
        status, result = send(args.endpoint, token, method, path, payload, **({"capture": capture} if capture else {}))
        if token in json.dumps(result, ensure_ascii=False):
            raise RemoteError("Refusing credential content in remote output.")
        if op == "export" and status == 200:
            result = save_export(result, args.destination)
        output = capture.compact(result) if compact else result
        code = 0 if status == 200 else 1
        if include_document and status == 200 and result.get("outcome") == "accepted":
            affected = result.get("affected_artifacts", [])
            if len(affected) != 1:
                raise RemoteError("Create response does not select one exact artifact; inspect its retained result.")
            request = revision_request(args.project, result["view"], affected[0]["artifact_id"], affected[0]["revision_id"])
            read_path = "/v1/projects/" + urllib.parse.quote(args.project, safe="") + "/reads/revision"
            capture.request("POST", read_path, request)
            read_status, document = send(args.endpoint, token, "POST", read_path, request, capture=capture)
            if (read_status == 200 and (document.get("project_id") != args.project or document.get("view") != result["view"] or
                    document.get("data", {}).get("revision_id") != affected[0]["revision_id"] or
                    document.get("data", {}).get("envelope", {}).get("artifact_id") != affected[0]["artifact_id"])):
                raise RemoteError("Document read differs from the created revision; inspect retained responses.")
            output["document_read"] = capture.compact(document)
            if read_status != 200:
                code = 1
        if capture:
            capture.finish(code, result.get("outcome", "response_received"))
        # ASCII JSON escapes preserve Unicode through Windows legacy consoles.
        # Exact HTTP/document bytes are retained separately by Capture.
        print(json.dumps(output, ensure_ascii=True, indent=2))
        return code
    except (RemoteError, OSError, ValueError, KeyError, TypeError) as exc:
        unknown = sent or isinstance(exc, TransportUncertain)
        result = {"schema": "se-harness-remote-transport/v1", "outcome": "unknown" if unknown else "not_sent",
                  "message": str(exc) if isinstance(exc, RemoteError) else "Invalid remote input or incomplete local capture.",
                  "operation_key": payload.get("operation_key") if isinstance(payload, dict) else None,
                  "recovery": "A remote effect may have committed. Inspect retained responses and the original operation key; do not choose a new key." if unknown else None}
        if token and token in result["message"]:
            result["message"] = "Remote input or capture failed; credential content withheld."
        if capture:
            result["evidence"] = str(capture.path)
            try:
                capture.finish(2, result["outcome"])
            except (OSError, ValueError):
                result["capture_incomplete"] = True
        print(json.dumps(result), file=sys.stderr)
        return 2


def new_export_destination(value):
    if not value:
        raise RemoteError("--destination must name a new directory for test data.")
    path = Path(value).absolute()
    for parent in (path, *path.parents):
        if parent.is_symlink() or getattr(parent, "is_junction", lambda: False)():
            raise RemoteError("Export destinations cannot contain links or junctions.")
    if path.exists():
        raise RemoteError("HAG_REMOTE_EXPORT_EXISTS: the export destination already exists.")
    if not path.parent.is_dir():
        raise RemoteError("Create the export parent directory first.")
    return path


def save_export(value, destination):
    """Write exact bounded bytes; an interrupted download stays visibly incomplete."""
    def canonical(obj):
        return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")

    def digest(scheme, obj):
        return hashlib.sha256(scheme.encode() + b"\n" + canonical(obj)).hexdigest()

    def decode(item):
        raw = base64.b64decode(item["content_base64"], validate=True)
        if (len(raw) != item["bytes"] or hashlib.sha256(raw).hexdigest() != item["sha256"]
                or base64.b64encode(raw).decode("ascii") != item["content_base64"]):
            raise RemoteError("Export bytes do not match their declared hash.")
        return raw

    try:
        if value.get("schema") != "se-harness-lifecycle-export/v2" or value.get("test_copy") is not True:
            raise RemoteError("The response is not a test-copy export.")
        snapshot, baseline = value["snapshot"], value["baseline"]
        scheme = "se-harness-test-snapshot/v2"
        if (snapshot["schema"] != scheme or snapshot.get("test_copy") is not True
                or snapshot["snapshot_id"] != "sha256:" + digest(scheme, {k: v for k, v in snapshot.items() if k != "snapshot_id"})
                or baseline["manifest"]["provenance"]["snapshot_id"] != snapshot["snapshot_id"]
                or baseline["baseline_id"] != baseline["schema"] + ":sha256:" + digest(baseline["schema"], baseline["manifest"])):
            raise RemoteError("Export snapshot or baseline binding differs.")
        files = {}
        for path, item in snapshot["files"].items():
            if (not isinstance(path, str) or not path or path.startswith("/") or "\\" in path or ":" in path
                    or any(ord(c) < 32 or ord(c) == 127 for c in path)
                    or any(p.casefold() in ("", ".", "..", ".git") or p.rstrip(" .") != p
                           or p.split(".", 1)[0].upper() in {"CON", "PRN", "AUX", "NUL", *[f"COM{i}" for i in range(1, 10)], *[f"LPT{i}" for i in range(1, 10)]}
                           for p in path.split("/"))):
                raise RemoteError("Unsafe export path.")
            files[path] = decode(item)
        names = {p.casefold() for p in files}
        if len(names) != len(files) or any(str(parent).replace("\\", "/").casefold() in names for p in files for parent in Path(p).parents if str(parent) != "."):
            raise RemoteError("Conflicting export paths.")
        bundle = decode(snapshot["git_bundle"])
        if sum(map(len, files.values())) + len(bundle) > LIMIT or len(files) > 10000:
            raise RemoteError("Export content exceeds its bound.")
        path = new_export_destination(destination)
        path.mkdir()
        marker = path / ".incomplete"
        marker.write_text("Incomplete test export. Do not use for replay.\n", encoding="utf-8")
        tree = path / "files"
        tree.mkdir()
        for relative, raw in files.items():
            target = tree / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(raw)
            if target.read_bytes() != raw:
                raise RemoteError("Export readback differs; incomplete marker retained.")
        (path / "history.bundle").write_bytes(bundle)
        manifest = {**value, "snapshot": {**snapshot, "files": {p: {k: v for k, v in item.items() if k != "content_base64"} for p, item in snapshot["files"].items()},
                    "git_bundle": {k: v for k, v in snapshot["git_bundle"].items() if k != "content_base64"}}}
        (path / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if (path / "history.bundle").read_bytes() != bundle:
            raise RemoteError("Git bundle readback differs; incomplete marker retained.")
        marker.unlink()
        return {"schema": "se-harness-saved-test-export/v2", "test_copy": True,
                "authority": "rehearsal-only; Git remains authoritative", "destination": str(path),
                "baseline_id": baseline["baseline_id"], "snapshot_id": snapshot["snapshot_id"],
                "files": len(files), "independent_replay": "not yet performed"}
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, RemoteError):
            raise
        raise RemoteError("Malformed exact export; no successful export is claimed.") from exc
