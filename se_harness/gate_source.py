"""Local execution delegation from the work order's recorded owner approval.

Local gates are evaluated by the caller. CI remains an integration/publication
check and is never contacted to authorize a local transition.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Mapping
from se_harness import front_matter
from se_harness._process import run_git, text
from se_harness.workflow_contract import DelegatedOperation, delegated_operations
from se_harness.codes import CodedError, WEX_ECP_022

DELEGATED_ROLE = "delegated-executor"
DELEGATION_CLASS = "execution"
#: ECP-PRM-019: the delegated rights and the guard operation each applies, read from
#: `workflow_contract.json` `agentic_operations`; nothing here restates the contract.
DELEGATED_RIGHTS: Mapping[str, str] = {
    operation.decision_right: operation.mutation_operation for operation in delegated_operations()
}
#: The transition a delegated right applies, by (family, current status, target status).
DELEGATED_TRANSITIONS: Mapping[tuple[str, str, str], str] = {
    operation.transition: operation.decision_right
    for operation in delegated_operations()
    if operation.transition is not None
}


def delegated_operation(right: str) -> DelegatedOperation:
    """The contract entry of one delegated right; KeyError for a human right."""

    for operation in delegated_operations():
        if operation.decision_right == right:
            return operation
    raise KeyError(right)

class DelegationError(CodedError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code, message)
        self.predicate_id = code


def declares_class(metadata: Mapping[str, Any]) -> bool:
    table = metadata.get("delegation")
    return isinstance(table, dict) and table.get("class") == DELEGATION_CLASS


def _approved_scope(root: Path, path: Path, metadata: Mapping[str, Any]) -> Mapping[str, Any]:
    approvals = [e for e in metadata.get("lifecycle_events", [])
                 if e.get("to") == "approved" and e.get("decided_by") == "engineering-owner"]
    if not approvals:
        raise DelegationError(WEX_ECP_022, f"{path.name} has no recorded engineering-owner approval")
    approval = approvals[-1]
    if "scope_paths" in approval:
        return {"execution_scope": {"paths": approval["scope_paths"]},
                "delegation": {"class": approval.get("delegation_class")}}
    # Older approval events did not include scope. Read their original committed
    # document, on any local branch; no base-branch merge or network is needed.
    relative = path.resolve().relative_to(root.resolve()).as_posix()
    history = run_git(root, "log", "--reverse", "--format=%H", "HEAD", "--", relative,
                      error=lambda message: DelegationError(WEX_ECP_022, message))
    if history.returncode == 0:
        for commit in text(history.stdout).splitlines():
            result = run_git(root, "show", f"{commit}:{relative}",
                             error=lambda message: DelegationError(WEX_ECP_022, message))
            if result.returncode:
                continue
            try:
                previous = front_matter.parse(text(result.stdout))
            except front_matter.FrontMatterError:
                continue
            if approval in previous.get("lifecycle_events", []):
                return previous
    raise DelegationError(WEX_ECP_022, f"{path.name} needs a recorded approval of its scope")


def authorize_delegated_right(root: Path, *, work_order_metadata: Mapping[str, Any],
                              work_order_path: Path, right: str | None) -> str:
    if right not in DELEGATED_RIGHTS:
        raise DelegationError(WEX_ECP_022, f"{right or 'This transition'} remains an owner decision")
    if not declares_class(work_order_metadata):
        raise DelegationError(WEX_ECP_022, f"{work_order_path.name} declares no execution delegation")
    approved = _approved_scope(root, work_order_path, work_order_metadata)
    if not declares_class(approved) or approved.get("execution_scope") != work_order_metadata.get("execution_scope"):
        raise DelegationError(WEX_ECP_022, f"{work_order_path.name} delegation or scope changed since owner approval")
    return "recorded engineering-owner approval"


def delegated_reason(right: str, approval: str, supplied: str | None) -> str:
    reason = f"Delegated {right} under execution class and {approval}; relevant local gates passed."
    return reason if not supplied else f"{reason} {supplied}"


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
    try:
        authorize_delegated_right(root, work_order_metadata=work_order_metadata,
                                 work_order_path=work_order_path, right=right)
    except DelegationError:
        return restitution
    operation = delegated_operation(right)
    if operation.transition is not None:
        argv = ["harnessctl", "transition", ".", "--set", f"{artifact_id}={operation.result_status}", "--decision", f"{artifact_id}={DELEGATED_ROLE}", "--apply"]
    else:
        argv = ["harnessctl", "capture-verification", ".", "--work-order", artifact_id, "--owner", DELEGATED_ROLE, "--id", "VREC-...", "--verification", "VER-...", "--evidence", "..."]
    return {
        **restitution,
        "decision_required": {
            **decision,
            "role": DELEGATED_ROLE,
            "delegation": {"class": DELEGATION_CLASS, "source": "owner-approval"},
        },
        "command_or_response": {"kind": "command", "argv": argv},
    }
