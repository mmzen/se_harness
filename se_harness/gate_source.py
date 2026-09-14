"""The one execution grant: the work order's recorded owner approval.

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


def _approved_scope(root: Path, path: Path, metadata: Mapping[str, Any]) -> Mapping[str, Any]:
    approvals = [e for e in metadata.get("lifecycle_events", [])
                 if e.get("to") == "approved" and e.get("decided_by") == "engineering-owner"]
    if not approvals:
        raise DelegationError(WEX_ECP_022, f"{path.name} has no recorded engineering-owner approval")
    approval = approvals[-1]
    if "scope_paths" in approval:
        # New approvals grant execution directly. Older scoped events always
        # recorded delegation_class, including an empty value for no grant.
        if "delegation_class" in approval and approval["delegation_class"] != DELEGATION_CLASS:
            raise DelegationError(WEX_ECP_022, f"{path.name} needs owner approval of remaining execution; its old approval did not delegate it")
        return {"paths": approval["scope_paths"]}
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
                if previous.get("delegation", {}).get("class") != DELEGATION_CLASS:
                    raise DelegationError(WEX_ECP_022, f"{path.name} needs owner approval of remaining execution; its old approval did not delegate it")
                return previous.get("execution_scope", {})
    raise DelegationError(WEX_ECP_022, f"{path.name} needs a recorded approval of its scope")


def authorize_delegated_right(root: Path, *, work_order_metadata: Mapping[str, Any],
                              work_order_path: Path, right: str | None) -> str:
    if right not in DELEGATED_RIGHTS:
        raise DelegationError(WEX_ECP_022, f"{right or 'This transition'} remains an owner decision")
    approved = _approved_scope(root, work_order_path, work_order_metadata)
    if approved != work_order_metadata.get("execution_scope"):
        raise DelegationError(WEX_ECP_022, f"{work_order_path.name} scope changed since owner approval")
    return "recorded engineering-owner approval"


def delegated_reason(right: str, approval: str, supplied: str | None) -> str:
    reason = f"Execution of {right} under {approval}; relevant local gates passed."
    return reason if not supplied else f"{reason} {supplied}"
