#!/usr/bin/env python3
"""Create or verify the repository-specific SE Harness maintenance line."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


EXPECTED_REPOSITORY = "mmzen/se_harness"
API_ROOT = "https://api.github.com"
API_VERSION = "2022-11-28"
MAX_RESPONSE_BYTES = 1024 * 1024
VERSION_PATTERN = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
COMMIT_PATTERN = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")


class MaintenanceBranchError(RuntimeError):
    """A maintenance-line reconciliation invariant failed."""


@dataclass(frozen=True)
class ApiResponse:
    status: int
    payload: Any


@dataclass(frozen=True)
class ReconciliationResult:
    repository: str
    version: str
    candidate: str
    branch: str
    ref: str
    state: str
    tip: str


RequestFunction = Callable[[str, str, dict[str, Any] | None], ApiResponse]


def derive_branch(version: str) -> str:
    match = VERSION_PATTERN.fullmatch(version)
    if match is None:
        raise MaintenanceBranchError("version must match canonical MAJOR.MINOR.PATCH form")
    major, minor, _patch = match.groups()
    return f"release/{major}.{minor}"


def _validate_candidate(candidate: str) -> None:
    if COMMIT_PATTERN.fullmatch(candidate) is None:
        raise MaintenanceBranchError("candidate must be one full lowercase Git commit ID")


def _api_path(repository: str, suffix: str) -> str:
    return f"/repos/{quote(repository, safe='/')}/{suffix}"


def _ref_payload(payload: Any, branch: str) -> str:
    expected_ref = f"refs/heads/{branch}"
    if not isinstance(payload, dict) or payload.get("ref") != expected_ref:
        raise MaintenanceBranchError(f"GitHub returned malformed ref state for {expected_ref}")
    target = payload.get("object")
    if not isinstance(target, dict) or target.get("type") != "commit":
        raise MaintenanceBranchError(f"{expected_ref} does not identify a commit")
    tip = target.get("sha")
    if not isinstance(tip, str) or COMMIT_PATTERN.fullmatch(tip) is None:
        raise MaintenanceBranchError(f"{expected_ref} has an invalid commit ID")
    return tip


def _read_ref(request: RequestFunction, repository: str, branch: str) -> str | None:
    ref_parameter = quote(f"heads/{branch}", safe="")
    response = request("GET", _api_path(repository, f"git/ref/{ref_parameter}"), None)
    if response.status == 404:
        return None
    if response.status != 200:
        raise MaintenanceBranchError(
            f"GitHub ref lookup failed for refs/heads/{branch} with HTTP {response.status}"
        )
    return _ref_payload(response.payload, branch)


def _contains_candidate(
    request: RequestFunction,
    repository: str,
    branch: str,
    candidate: str,
    tip: str,
) -> None:
    if tip == candidate:
        return
    response = request("GET", _api_path(repository, f"compare/{candidate}...{tip}"), None)
    if response.status != 200 or not isinstance(response.payload, dict):
        raise MaintenanceBranchError(
            f"GitHub history comparison failed for refs/heads/{branch} with HTTP {response.status}"
        )
    status = response.payload.get("status")
    if status not in {"ahead", "identical"}:
        raise MaintenanceBranchError(
            f"refs/heads/{branch} does not contain released candidate {candidate}; "
            f"tip is {tip} and comparison is {status!r}"
        )


def reconcile(
    repository: str,
    version: str,
    candidate: str,
    request: RequestFunction,
) -> ReconciliationResult:
    if repository != EXPECTED_REPOSITORY:
        raise MaintenanceBranchError(
            f"maintenance-line automation is restricted to {EXPECTED_REPOSITORY}"
        )
    _validate_candidate(candidate)
    branch = derive_branch(version)
    ref = f"refs/heads/{branch}"
    tip = _read_ref(request, repository, branch)
    if tip is not None:
        _contains_candidate(request, repository, branch, candidate, tip)
        return ReconciliationResult(repository, version, candidate, branch, ref, "existing", tip)

    response = request("POST", _api_path(repository, "git/refs"), {"ref": ref, "sha": candidate})
    if response.status == 201:
        created_tip = _ref_payload(response.payload, branch)
        if created_tip != candidate:
            raise MaintenanceBranchError(
                f"GitHub created {ref} at {created_tip}, expected released candidate {candidate}"
            )
        tip = _read_ref(request, repository, branch)
        if tip is None:
            raise MaintenanceBranchError(f"GitHub did not retain newly created {ref}")
        _contains_candidate(request, repository, branch, candidate, tip)
        return ReconciliationResult(repository, version, candidate, branch, ref, "created", tip)

    if response.status in {409, 422}:
        # A concurrent actor may have created the same ref after the absence check.
        tip = _read_ref(request, repository, branch)
        if tip is not None:
            _contains_candidate(request, repository, branch, candidate, tip)
            return ReconciliationResult(repository, version, candidate, branch, ref, "existing", tip)

    raise MaintenanceBranchError(
        f"GitHub ref creation failed for {ref} with HTTP {response.status}; no existing compatible ref was found"
    )


def _decode_response(raw: bytes, status: int) -> Any:
    if len(raw) > MAX_RESPONSE_BYTES:
        raise MaintenanceBranchError(f"GitHub returned an oversized HTTP {status} response")
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise MaintenanceBranchError(f"GitHub returned invalid JSON with HTTP {status}") from exc


def github_request(token: str) -> RequestFunction:
    if not token:
        raise MaintenanceBranchError("GH_TOKEN is required for maintenance-line reconciliation")

    def request(method: str, path: str, payload: dict[str, Any] | None) -> ApiResponse:
        data = None
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "se-harness-release-automation",
            "X-GitHub-Api-Version": API_VERSION,
        }
        if data is not None:
            headers["Content-Type"] = "application/json"
        request_value = Request(f"{API_ROOT}{path}", data=data, headers=headers, method=method)
        try:
            with urlopen(request_value, timeout=30) as response:  # noqa: S310 - fixed HTTPS origin
                raw = response.read(MAX_RESPONSE_BYTES + 1)
                return ApiResponse(response.status, _decode_response(raw, response.status))
        except HTTPError as exc:
            raw = exc.read(MAX_RESPONSE_BYTES + 1)
            return ApiResponse(exc.code, _decode_response(raw, exc.code))
        except (OSError, URLError) as exc:
            raise MaintenanceBranchError("GitHub API request failed") from exc

    return request


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    content = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _append_github_output(path: Path, result: ReconciliationResult) -> None:
    values = {"branch": result.branch, "ref": result.ref, "state": result.state, "tip": result.tip}
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        for key, value in values.items():
            stream.write(f"{key}={value}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create or verify the mmzen/se_harness release/MAJOR.MINOR maintenance line."
    )
    parser.add_argument("--repository", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--github-output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = reconcile(
            args.repository,
            args.version,
            args.candidate,
            github_request(os.environ.get("GH_TOKEN", "")),
        )
        value = asdict(result)
        _write_json(args.output, value)
        if args.github_output is not None:
            _append_github_output(args.github_output, result)
        print(
            f"Maintenance line: {result.state.upper()} | {result.branch} | "
            f"candidate={result.candidate} | tip={result.tip}"
        )
        return 0
    except MaintenanceBranchError as exc:
        print(f"maintenance-line reconciliation: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
