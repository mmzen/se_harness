+++
id = "ADR-AEX-002"
type = "adr"
title = "Single-agent baseline before bounded parallel agent execution"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "technical-owner"
+++

# ADR: Single-agent baseline before bounded parallel agent execution

## Status

Option D was accepted during accountable technical-owner content review. The
authoritative lifecycle state remains the front-matter `status` and lifecycle
events.

## Context

Subagents can isolate noisy exploration, run independent checks concurrently,
and improve analytical coverage. They can also inherit parent permissions,
share a filesystem, overlap edits, use stale snapshots, omit failed workers from
summaries, and increase token or coordination cost. Runtime support is not
uniform.

The governed result must not depend on whether a runtime can spawn subagents.
Parallelism should improve execution, not define correctness or authority.

## Decision drivers

- Preserve one deterministic governed procedure across runtimes.
- Provide a fallback when subagents are absent, disabled, or interrupted.
- Avoid concurrent write conflicts and stale evidence.
- Make worker coverage and failure visible.
- Revalidate the exact combined candidate before decision or completion.
- Bound token, latency, worktree, and coordination cost.
- Allow read-heavy tasks to gain parallel speed or independent analysis.

## Considered options

### Option A: multi-agent-first workflows

Every skill would decompose into specialized agents. This maximizes visible
parallelism but makes correctness depend on runtime orchestration and creates
unnecessary coordination for simple work.

### Option B: unrestricted agents sharing one worktree

Workers would coordinate informally through the shared filesystem. This is
simple but permits overlapping edits, stale assumptions, partial integration,
and nondeterministic evidence.

### Option C: always serialize all agent work

One agent would perform every task. This is deterministic but gives up useful
parallel read-only exploration, testing, and review.

### Option D: establish a single-agent baseline, then add bounded parallelism

Every skill has a complete single-agent procedure. Optional orchestration may
parallelize independent read-only tasks. Concurrent writers require explicit
disjoint scope and isolated worktrees. One integration coordinator owns the
combined candidate and reruns final validation and evidence binding.

## Decision

Choose Option D.

- Implement and verify the single-agent path first.
- Start orchestration with read-only exploration, tests, logs, and review.
- Require a bounded task contract and structured result for every worker.
- Require child scope and authority to be equal to or narrower than the parent.
- Use isolated worktrees and explicit disjoint scope for later concurrent
  writers.
- Assign one integration coordinator as sole owner of the final candidate.
- Run required gates and receipts against the combined repository.
- Use parallelism only when measured benefit justifies additional cost.

## Consequences

### Positive

- Correctness and authority do not depend on subagent availability.
- The simplest safe path remains available for every skill.
- Read-heavy parallelism can reduce context pollution and wall time.
- Writer coordination and final provenance have explicit owners.
- Cross-runtime conformance has a stable single-agent reference.

### Negative

- Multi-agent capabilities arrive later than basic skills.
- The integration coordinator may become a throughput bottleneck.
- Isolated worktrees and disjoint-scope analysis add orchestration complexity.
- Some parallel implementations will be rejected or serialized.

### Operational

- Worker statuses, timeouts, interruptions, and result digests must be retained.
- Worktree creation and cleanup require bounded, recoverable procedures.
- Cost and latency measurements must accompany multi-agent acceptance.

### Security

- Workers receive least-necessary task context, scope, operations, and tools.
- Permission inheritance cannot enlarge the autonomy envelope.
- A fresh context or different model is analytical separation, not accountable
  assurance independence.

### Migration

- Initial skills ship with delegation disabled or optional.
- Runtimes without subagents continue using the same portable skill.
- Multi-agent write support requires a later separately approved work order.

## Validation

- Run every acceptance scenario through the single-agent reference path.
- Compare multi-agent selected scope, commands, changed paths, evidence, final
  state, blockers, and decision packet with the reference result.
- Inject worker failure, timeout, cancellation, invalid output, overlapping
  scope, worktree conflict, stale integration, and final validation failure.
- Confirm failed workers remain visible and prevent false complete coverage.
- Measure wall time, token or compute cost, conflicts, retries, and coverage
  benefit before enabling orchestration by default.
