+++
id = "CAP-AEX-001"
type = "capability"
title = "Delegate bounded engineering execution to agent workers"
status = "approved"
owners = ["product-owner", "repository-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
derives_from = ["INT-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "product-owner"
+++

# Capability: Delegate bounded engineering execution to agent workers

## Actor and need

An accountable engineering operator needs to delegate routine, bounded
execution to one or more agent workers and receive trustworthy evidence and a
decision-ready handoff without supervising every command.

## Capability statement

An accountable operator can authorize a bounded engineering objective and
delegation boundary, allow runtime-neutral skills and agent workers to execute
the permitted procedure, and regain control at each accountable decision point
with the exact state, evidence, recommendation, alternatives, and authority
requirement needed to decide.

## Boundaries

- The capability delegates execution, not accountability.
- Accountable roles remain distinct from agent execution profiles.
- Read-only orientation requires no lifecycle authority; governed mutation
  requires a valid work order and every applicable harness-side authority check.
- A runtime permission is a technical capability, not a decision right.
- Subagents are optional execution contexts, not independent assurance owners or
  security principals by default.
- Skills and adapters do not define permitted transitions, quality gates, or
  lifecycle state.
- Release, exception, external-action, and credential-bearing decisions remain
  separately authorized.

## Outcomes

- Operators interact primarily at definition, exception, assurance, release,
  and external-action decisions.
- Agents receive a deterministic scope, procedure, evidence obligation, and stop
  boundary.
- Read-only orientation is available as the first portable skill and works
  without subagents.
- Later mutation skills can be added without moving authority out of the
  harness.
- Multi-agent execution can improve speed or coverage while producing the same
  final governed result as single-agent execution.
- Runtime adapters can be replaced or omitted without changing formal state or
  decision rights.

## Candidate requirements

- `REQ-AEX-001`: distinguish accountable authority from agent execution.
- `REQ-AEX-002`: constrain autonomous mutation with an explicit autonomy
  envelope.
- `REQ-AEX-003`: stop at accountable decision points with a canonical decision
  packet.
- `REQ-AEX-004`: retain attributable execution receipts.
- `REQ-AEX-005`: expose governed workflows through portable outcome-oriented
  skills.
- `REQ-AEX-006`: orient an operator through a read-only portable skill.
- `REQ-AEX-007`: orchestrate workers and materialize runtime adapters without
  changing authority.
