"""One ASGI process, one set of read handlers for HTTP and the maintained MCP SDK."""
from __future__ import annotations

import contextlib
import contextvars
import json
import logging
import traceback
from pathlib import Path

from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.types import Tool, TextContent
from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from .canonical import CanonicalError, decode_json
from .protocol import MAX_REQUEST, Refusal, require
from .reads import read
from .service import Service

PRINCIPAL = contextvars.ContextVar("sandbox_principal")
LOG = logging.getLogger("harness.hosted")


class Auth:
    def __init__(self, app, service):
        self.app, self.service = app, service

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["path"] == "/health":
            return await self.app(scope, receive, send)
        try:
            principal = self.service.authenticate(Request(scope).headers.get("authorization"))
        except Refusal as exc:
            return await JSONResponse(exc.result(), status_code=exc.status)(scope, receive, send)
        token = PRINCIPAL.set(principal)
        size = 0

        async def bounded_receive():
            nonlocal size
            message = await receive()
            size += len(message.get("body", b""))
            require(size <= MAX_REQUEST, 429, "RESOURCE_LIMIT", "Request exceeds 4 MiB.")
            return message
        try:
            await self.app(scope, bounded_receive, send)
        finally:
            PRINCIPAL.reset(token)


def create_app(config_path, credentials_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    credentials = json.loads(Path(credentials_path).read_text(encoding="utf-8"))
    service = Service(config, credentials)
    mcp = Server("se-harness-hosted-sandbox", version="0.1.0.dev1")

    @mcp.list_tools()
    async def list_tools():
        schema = service.wire.schemas["read-v1.json"]
        definitions = {**service.wire.schemas["remote-v1.json"]["$defs"], **schema["$defs"]}
        def inline_refs(value):
            if isinstance(value, dict):
                return {k: (v.replace("urn:se-harness:remote-wire:v1#/$defs/", "#/$defs/") if k == "$ref" else inline_refs(v)) for k, v in value.items()}
            if isinstance(value, list):
                return [inline_refs(v) for v in value]
            return value
        return [Tool(name=variant["allOf"][1]["properties"]["operation"]["const"],
                     description="Read the explicit sandbox view. No approval or mutation authority.",
                     inputSchema=inline_refs({"type": "object", **variant, "$defs": definitions})) for variant in schema["$defs"]["Request"]["oneOf"]]

    @mcp.call_tool()
    async def call_tool(name, arguments):
        try:
            require(arguments.get("operation") == name, 400, "MALFORMED", "MCP tool and operation differ.")
            result = await run_in_threadpool(read, service, PRINCIPAL.get(), arguments)
        except Refusal as exc:
            result = exc.result()
        # Hosts may save large text responses. Line breaks keep metadata readable
        # through bounded file reads without changing JSON values or byte size.
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, separators=(",\n", ": ")))]

    manager = StreamableHTTPSessionManager(app=mcp, json_response=True, stateless=True)

    @contextlib.asynccontextmanager
    async def lifespan(app):
        # Uninitialized/mismatched schema is observable through readiness; no startup migration.
        async with manager.run():
            yield
        service.store.driver.close()

    async def health(request):
        return JSONResponse({"alive": True})

    async def status(request):
        try:
            service.access(PRINCIPAL.get(), service.project_id)
            result = await run_in_threadpool(service.readiness)
            return JSONResponse(result)
        except Refusal as exc:
            return JSONResponse({"ready": False, **exc.result()}, status_code=exc.status)

    async def handle(request):
        try:
            principal, project = PRINCIPAL.get(), request.path_params["project"]
            service.access(principal, project)
            if request.method == "GET":
                if "baseline" in request.path_params:
                    result = await run_in_threadpool(service.baseline, principal, project, request.path_params["baseline"])
                else:
                    result = await run_in_threadpool(service.lookup, principal, project, request.path_params["key"])
            else:
                chunks = []
                size = 0
                async for chunk in request.stream():
                    size += len(chunk)
                    require(size <= MAX_REQUEST, 429, "RESOURCE_LIMIT", "Request exceeds 4 MiB.")
                    chunks.append(chunk)
                try:
                    body = decode_json(b"".join(chunks), max_bytes=MAX_REQUEST)
                except CanonicalError as exc:
                    raise Refusal(400, "MALFORMED", "Malformed strict UTF-8 JSON.") from exc
                require(isinstance(body, dict) and body.get("project_id") == project, 400,
                        "MALFORMED", "Route and body project differ.")
                route = request.path_params.get("operation")
                if request.url.path.startswith("/v2/"):
                    handler = service.export_test if request.url.path.endswith("/exports") else service.rehearse
                    result = await run_in_threadpool(handler, principal, body)
                elif route:
                    require(body.get("operation") == route, 400, "MALFORMED", "Route and read operation differ.")
                    result = await run_in_threadpool(read, service, principal, body)
                else:
                    allowed = {"imports": {"import"}, "contexts": {"draft-open"}, "baselines": {"freeze"},
                               "commands": {"create-artifact", "revise-artifact"}}[request.url.path.rsplit("/", 1)[-1]]
                    require(body.get("operation") in allowed, 400, "UNSUPPORTED_OPERATION", "Operation is not supported at this route.")
                    result = await run_in_threadpool(service.command, principal, body)
            LOG.info("request outcome=%s operation_key=%s", result.get("outcome", "read"), result.get("operation_key"))
            return JSONResponse(result)
        except Refusal as exc:
            LOG.info("request refusal=%s", exc.code)
            if request.url.path.startswith("/v2/"):
                from .lifecycle import refusal_result
                return JSONResponse(refusal_result(service.project_id, exc), status_code=exc.status)
            return JSONResponse(exc.result(), status_code=exc.status)
        except Exception as exc:
            # Keep class and source locations only, never exception messages,
            # source lines or local variables that may contain input or secrets.
            locations = [(Path(frame.filename).name, frame.name, frame.lineno)
                         for frame in traceback.extract_tb(exc.__traceback__)]
            LOG.error("request outcome=unknown failure_type=%s locations=%s; reconcile by operation lookup",
                      type(exc).__name__, locations)
            return JSONResponse({"schema": "se-harness-remote-transport/v1", "outcome": "unknown",
                                 "message": "Service could not establish the result. Look up or identically retry the operation."}, status_code=503)

    class MCPApp:
        async def __call__(self, scope, receive, send):
            await manager.handle_request(scope, receive, send)

    base = "/v1/projects/{project}"
    routes = [Route("/health", health), Route("/v1/status", status),
              Route("/v2/projects/{project}/rehearsals", handle, methods=["POST"]),
              Route("/v2/projects/{project}/exports", handle, methods=["POST"]),
              Route(base + "/baselines/{baseline:path}", handle),
              Route(base + "/operations/{key}", handle),
              Route(base + "/reads/{operation}", handle, methods=["POST"]),
              *[Route(base + "/" + part, handle, methods=["POST"]) for part in ("imports", "contexts", "baselines", "commands")],
              Route("/mcp", MCPApp(), methods=["GET", "POST", "DELETE"])]
    return Auth(Starlette(routes=routes, lifespan=lifespan), service)
