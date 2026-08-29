"""The delegation class: who may delegate, and the gate that unlocks it.

`SPEC-ECP-006` (`ECP-DLG-001` to `ECP-DLG-007`, `ECP-DLG-009`, `ECP-DLG-010`):
a work order that carries ``[delegation] class = "execution"`` *at the base of
the pull request* lets the ``delegated-executor`` role apply exactly
``DR-WO-START``, ``DR-WO-COMPLETE`` and ``DR-VREC-PREPARE`` while the required
pull-request check for the candidate head reads ``success``. The gate is read
from the configured source by commit id — the CI provider, or a local file in a
rehearsal — never from a request body, an environment variable, a token or an
actor name.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

DELEGATED_ROLE = "delegated-executor"
DELEGATION_CLASS = "execution"
DELEGATED_RIGHTS: Mapping[str, str] = {
    "DR-WO-START": "delegated-work-order-start",
    "DR-WO-COMPLETE": "delegated-work-order-complete",
    "DR-VREC-PREPARE": "delegated-vrec-prepare",
}
#: The transition a delegated right applies, by (family, current status, target status).
DELEGATED_TRANSITIONS: Mapping[tuple[str, str, str], str] = {
    ("work_order", "approved", "in_progress"): "DR-WO-START",
    ("work_order", "in_progress", "implemented"): "DR-WO-COMPLETE",
}
GITHUB_API = "https://api.github.com"
#: Owner-controlled configuration, beside the managed `.engineering-harness.toml` and never
#: inside it: the managed file is hash-locked, and a consumer editing it reads as customization.
CONFIGURATION_NAME = ".engineering-harness.delegation.toml"


class DelegationError(RuntimeError):
    """A coded refusal of the delegated route; the code is the check that refused."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.predicate_id = code
        self.message = message


@dataclass(frozen=True)
class DelegationConfiguration:
    gate_source: str
    check_name: str
    repository: str | None
    base_ref: str
    local_file: str | None


@dataclass(frozen=True)
class GateReading:
    sha: str
    conclusion: str
    check_run_id: str
    check_name: str
    source: str

    @property
    def passing(self) -> bool:
        return self.conclusion == "success"


def load_configuration(root: Path) -> DelegationConfiguration | None:
    """The `[delegation]` table of `.engineering-harness.delegation.toml`, or `None` when absent."""

    path = root / CONFIGURATION_NAME
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return None
    table = data.get("delegation")
    if not isinstance(table, dict):
        return None
    source = table.get("gate_source")
    if source not in {"github-checks", "local-file"}:
        raise DelegationError("WEX-ECP-040", f"delegation.gate_source must be github-checks or local-file, not {source!r}")
    check_name = table.get("check_name")
    if not isinstance(check_name, str) or not check_name.strip():
        raise DelegationError("WEX-ECP-040", "delegation.check_name must name the required check")
    repository = table.get("repository")
    base_ref = table.get("base_ref", "origin/main")
    local_file = table.get("local_file")
    if source == "local-file":
        if not isinstance(local_file, str) or not local_file:
            raise DelegationError("WEX-ECP-040", "delegation.local_file is required for the local-file source")
        if os.environ.get("SE_HARNESS_REHEARSAL") != "1":
            # ECP-DLG-004: the local-file source exists for tests and rehearsals only.
            print(
                "W-ECP-005: delegation.gate_source is local-file outside a rehearsal; "
                "the gate this run reads is not the CI provider's",
                file=sys.stderr,
            )
    return DelegationConfiguration(
        gate_source=str(source),
        check_name=check_name.strip(),
        repository=str(repository) if isinstance(repository, str) and repository else None,
        base_ref=str(base_ref),
        local_file=str(local_file) if isinstance(local_file, str) else None,
    )


def _git(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments], capture_output=True, text=True, check=False,
    )
    if completed.returncode != 0:
        raise DelegationError("WEX-ECP-040", f"git {' '.join(arguments)} failed: {completed.stderr.strip()[:200]}")
    return completed.stdout.strip()


def candidate_head(root: Path) -> str:
    return _git(root, "rev-parse", "HEAD")


def _repository_from_origin(root: Path) -> str | None:
    try:
        url = _git(root, "remote", "get-url", "origin")
    except DelegationError:
        return None
    for prefix in ("git@github.com:", "https://github.com/", "ssh://git@github.com/"):
        if url.startswith(prefix):
            return url[len(prefix):].removesuffix(".git")
    return None


def class_at_base(root: Path, configuration: DelegationConfiguration, work_order_path: Path) -> bool:
    """Whether the work order carries the class in the pull request's base copy (never the branch's)."""

    relative = work_order_path.resolve().relative_to(root.resolve()).as_posix()
    try:
        base = _git(root, "merge-base", "HEAD", configuration.base_ref)
        content = _git(root, "show", f"{base}:{relative}")
    except DelegationError:
        return False
    front = content.split("+++", 2)
    if len(front) < 3:
        return False
    try:
        metadata = tomllib.loads(front[1])
    except tomllib.TOMLDecodeError:
        return False
    table = metadata.get("delegation")
    return isinstance(table, dict) and table.get("class") == DELEGATION_CLASS


def declares_class(metadata: Mapping[str, Any]) -> bool:
    table = metadata.get("delegation")
    return isinstance(table, dict) and set(table) == {"class"} and table.get("class") == DELEGATION_CLASS


def read_gate(root: Path, configuration: DelegationConfiguration, sha: str) -> GateReading:
    """The required check's conclusion for `sha` from the configured source (ECP-DLG-003/-004)."""

    if configuration.gate_source == "local-file":
        path = root / str(configuration.local_file)
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as exc:
            raise DelegationError("WEX-ECP-040", f"gate source {path.name} unreadable at {sha[:7]}: {exc}") from exc
        if not isinstance(value, dict) or value.get("sha") != sha:
            raise DelegationError("WEX-ECP-040", f"gate source names no check for head {sha[:7]} (head not found)")
        conclusion = str(value.get("conclusion", "missing"))
        reading = GateReading(sha, conclusion, str(value.get("check_run_id", "local")), configuration.check_name, "local-file")
    else:
        repository = configuration.repository or _repository_from_origin(root)
        if repository is None:
            raise DelegationError("WEX-ECP-040", "delegation.repository is not configured and origin is not a GitHub remote")
        url = f"{GITHUB_API}/repos/{repository}/commits/{quote(sha, safe='')}/check-runs?check_name={quote(configuration.check_name, safe='')}"
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "se-harness"}
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:  # noqa: S310 - fixed https host
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code == 404:
                raise DelegationError("WEX-ECP-040", f"head {sha[:7]} not found on {repository}") from exc
            raise DelegationError("WEX-ECP-040", f"gate source error for {sha[:7]}: HTTP {exc.code}") from exc
        except (URLError, OSError, ValueError) as exc:
            raise DelegationError("WEX-ECP-040", f"gate source error for {sha[:7]}: {exc}") from exc
        runs = [item for item in payload.get("check_runs", []) if item.get("name") == configuration.check_name]
        if not runs:
            raise DelegationError("WEX-ECP-040", f"check {configuration.check_name!r} is missing at head {sha[:7]}")
        latest = runs[0]
        conclusion = str(latest.get("conclusion") or latest.get("status") or "missing")
        reading = GateReading(sha, conclusion, str(latest.get("id", "")), configuration.check_name, "github-checks")
    return reading


def require_passing_gate(root: Path, configuration: DelegationConfiguration, sha: str) -> GateReading:
    reading = read_gate(root, configuration, sha)
    if not reading.passing:
        raise DelegationError(
            "WEX-ECP-040",
            f"required check {reading.check_name!r} at head {sha[:7]} is {reading.conclusion}, not success",
        )
    return reading


def delegated_reason(right: str, reading: GateReading, supplied: str | None) -> str:
    """The lifecycle event's reason: the class, the check-run id and the head sha (ECP-DLG-005)."""

    evidence = (
        f"Delegated {right} under [delegation] class {DELEGATION_CLASS!r}: required check "
        f"{reading.check_name!r} success at {reading.sha} (check-run {reading.check_run_id}, source {reading.source})."
    )
    return evidence if not supplied else f"{evidence} {supplied}"


def authorize_delegated_right(
    root: Path,
    *,
    work_order_metadata: Mapping[str, Any],
    work_order_path: Path,
    right: str | None,
) -> GateReading:
    """Admit the delegated role for one right, or refuse with the coded reason.

    Order (ECP-DLG-002/-003/-006/-007): the right must be one of the three;
    the work order must declare the class and carry it at the base; the gate
    must read success for the candidate head.
    """

    if right not in DELEGATED_RIGHTS:
        raise DelegationError(
            "WEX-ECP-022",
            f"{DELEGATED_ROLE} may apply only {', '.join(DELEGATED_RIGHTS)}; {right or 'this transition'} is a human decision right",
        )
    if not declares_class(work_order_metadata):
        raise DelegationError("WEX-ECP-022", f"{work_order_path.name} declares no [delegation] class; {DELEGATED_ROLE} is refused")
    configuration = load_configuration(root)
    if configuration is None:
        raise DelegationError("WEX-ECP-040", f"no [delegation] gate source is configured in {CONFIGURATION_NAME}")
    if not class_at_base(root, configuration, work_order_path):
        raise DelegationError(
            "WEX-ECP-022",
            f"{work_order_path.name} carries no [delegation] class at the base {configuration.base_ref}; a branch cannot widen its own delegation",
        )
    return require_passing_gate(root, configuration, candidate_head(root))


def delegation_overlay(
    root: Path,
    *,
    work_order_metadata: Mapping[str, Any],
    work_order_path: Path,
    artifact_id: str,
    restitution: dict[str, Any],
) -> dict[str, Any]:
    """ECP-DLG-010: tell the actor when the decision due is its own.

    Only a decision-required restitution for one of the three rights on a
    class-bearing work order is touched; everything else returns unchanged.
    """

    decision = restitution.get("decision_required")
    command = restitution.get("command_or_response") or {}
    right: str | None = None
    if isinstance(decision, dict) and decision.get("decision_right") in DELEGATED_RIGHTS:
        right = str(decision["decision_right"])
    elif str(restitution.get("next", {}).get("procedure_id")) == "PROC-WO-START" and command.get("kind") == "command":
        # The start decision is not a decision step: PROC-WO-START is a chain of commands whose
        # last one carries the human role in its argv. An approved, class-bearing work order in
        # that procedure has DR-WO-START due.
        right = "DR-WO-START"
        decision = {
            "decision_right": right,
            "role": "engineering-owner",
            "artifact": artifact_id,
            "decision": "whether to start the approved work order",
            "outcomes": ["in_progress"],
        }
    if right is None or not isinstance(decision, dict):
        return restitution
    if not declares_class(work_order_metadata):
        return restitution
    configuration = load_configuration(root)
    if configuration is None or not class_at_base(root, configuration, work_order_path):
        return restitution
    try:
        reading = require_passing_gate(root, configuration, candidate_head(root))
    except DelegationError as exc:
        return {
            **restitution,
            "decision_required": {**decision, "role": DELEGATED_ROLE, "delegation": {"class": DELEGATION_CLASS, "gate": "not passing"}},
            "command_or_response": {
                "kind": "response",
                "value": f"Wait for or repair the required check before the delegated {right}: {exc.message}",
            },
        }
    if right == "DR-WO-START":
        argv = ["harnessctl", "transition", ".", "--set", f"{artifact_id}=in_progress", "--decision", f"{artifact_id}={DELEGATED_ROLE}", "--apply"]
    elif right == "DR-WO-COMPLETE":
        argv = ["harnessctl", "transition", ".", "--set", f"{artifact_id}=implemented", "--decision", f"{artifact_id}={DELEGATED_ROLE}", "--apply"]
    else:
        argv = ["harnessctl", "capture-verification", ".", "--work-order", artifact_id, "--owner", DELEGATED_ROLE, "--id", "VREC-...", "--verification", "VER-...", "--evidence", "..."]
    return {
        **restitution,
        "decision_required": {
            **decision,
            "role": DELEGATED_ROLE,
            "delegation": {"class": DELEGATION_CLASS, "gate": "success", "check_run_id": reading.check_run_id, "head": reading.sha},
        },
        "command_or_response": {"kind": "command", "argv": argv},
    }


__all__ = [
    "DELEGATED_RIGHTS",
    "DELEGATED_ROLE",
    "DELEGATED_TRANSITIONS",
    "DELEGATION_CLASS",
    "DelegationConfiguration",
    "DelegationError",
    "GateReading",
    "authorize_delegated_right",
    "candidate_head",
    "class_at_base",
    "declares_class",
    "delegated_reason",
    "delegation_overlay",
    "load_configuration",
    "read_gate",
    "require_passing_gate",
]
