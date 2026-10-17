# Proposed early communication pointer

**Request: approve WO-RLS-054, required commit-bound verification and the exact
linked REL-SEH-036 membership amendment. No implementation is applied.**

Both native hosts read the communication policy after their first explanation.
Their functional lifecycle passes independent review; full instruction compliance
remains incomplete. The early hosted selection route currently has no direct
pointer to this prerequisite. Both traces show that route was read before the
first explanation, so it is the smallest observed insertion point.

Add one short paragraph to the existing hosted-context.md. It points to the
existing released communication section and permits reuse when already supplied.
It adds no new policy, tool or workflow. The already required read moves earlier.
This is a hypothesis until fresh native evidence establishes the ordering.

Review [the exact patch](hosted-context.patch) and [the work order](../../work-orders/WO-RLS-054.md).
The [release patch](REL-SEH-036.patch) only adds this work order to membership;
accepted bytes/history are preserved. Approval must explicitly permit manual
activation because released 0.22.1 has no generic amendment command.

The new paragraph can consume complete-input headroom. Measure before launch;
keep the existing 64 KiB refusal. Native performance goals and every qualification
criterion remain unchanged. Desktop evidence and the local handoff cycle remain
separate from the resolved focused-drafting issue. No human verification, merge,
release, omission, adoption or host update is requested here.

Validation and planned-path coverage are retained in preparation-checks.json.
