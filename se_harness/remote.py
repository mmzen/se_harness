"""Standard-library client for the explicitly selected hosted draft sandbox.

This transport has no local authoring fallback, lifecycle policy or retry/rebase.
"""
from __future__ import annotations

import argparse
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
        raise RemoteError("The Phase 2 sandbox requires an explicit loopback HTTP endpoint.")
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


def send(endpoint, token, method, path, payload=None, timeout=130):
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
            if len(raw) > LIMIT:
                raise TransportUncertain("Remote response exceeds 2 MiB; its outcome is unknown.")
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise TransportUncertain("Remote response is not an object; its outcome is unknown.")
            return response.status, value
    except (OSError, urllib.error.URLError, ValueError) as exc:
        # Never include credentials, response bodies, or a guessed refused receipt.
        raise TransportUncertain("Remote transport is uncertain. Look up the original operation key or retry the identical request; do not change its expected versions.") from exc


def register(commands):
    parser = commands.add_parser("remote", help="use an explicit private hosted sandbox; no local fallback")
    parser.add_argument("operation", choices=["status", "baseline", "operation", "read", "check", "query", *MUTATIONS])
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--project")
    parser.add_argument("--token-env", required=True, help="name of an environment variable containing a sandbox token")
    parser.add_argument("--request", help="complete versioned JSON request file; never a credential file")
    parser.add_argument("--client-wheel", help="exact separately installed candidate wheel")
    parser.add_argument("--baseline")
    parser.add_argument("--context")
    parser.add_argument("--context-version", type=int)
    parser.add_argument("--key")
    parser.add_argument("--json", action="store_true")
    parser.set_defaults(handler=run)


def run(args):
    try:
        token = os.environ.get(args.token_env, "")
        op = args.operation
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
                if not args.request:
                    raise RemoteError("--request must name the explicit versioned request.")
                source = Path(args.request)
                if source.stat().st_size > 4 * 1024 * 1024:
                    raise RemoteError("Request exceeds 4 MiB.")
                payload = strict_json(source.read_text(encoding="utf-8"))
                if not isinstance(payload, dict) or payload.get("project_id", args.project) != args.project:
                    raise RemoteError("Request and selected project disagree.")
                payload["project_id"] = args.project
                if op in MUTATIONS:
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
        status, result = send(args.endpoint, token, method, path, payload)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if status == 200 else 1
    except (RemoteError, OSError, ValueError) as exc:
        result = {"schema": "se-harness-remote-transport/v1", "outcome": "unknown" if isinstance(exc, TransportUncertain) else "not_sent",
                  "message": str(exc) if isinstance(exc, RemoteError) else "Invalid local remote-request input."}
        print(json.dumps(result), file=sys.stderr)
        return 2
