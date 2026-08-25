+++
id = "ADR-AEX-007"
type = "adr"
title = "Isolated proposals with evaluator-owned transactional bundle effects"
status = "approved"
owners = ["technical-owner", "repository-owner", "security-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
decides = ["ARCH-AEX-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "technical-owner"
+++

# ADR: Isolated proposals with evaluator-owned transactional bundle effects

## Status

Proposed.

## Context

An admitted envelope is useful only if it controls the actual mutation path.
Current writing skills are cooperative: an agent with workspace-write tools can
change target files directly, after which validation can detect but not prevent
an out-of-scope or stale effect. Phase 4 needs a single enforceable target-write
boundary that remains portable across Codex, Claude Code, and later runtimes.

No generally available filesystem gives an instantaneous atomic commit across
an arbitrary set of files. The design must therefore distinguish rejected
operations, recoverable ordinary failures, and process or machine interruption
without claiming stronger visibility guarantees than the platform provides.

## Decision drivers

- Prevent direct worker writes to the governed target through the Phase 4 path.
- Validate exact proposed bytes and prior state before effect.
- Keep authority in the external released evaluator.
- Preserve or deterministically recover repository state after failure.
- Support Windows and POSIX without links or Git worktree dependence.
- Produce portable, reviewable, content-addressed evidence.
- Avoid duplicating work-order governance in a transport object.

## Considered options

### Option A — allow direct target writes and validate afterward

This reuses existing coding-agent tools, but stale, out-of-scope, or partially
written content already exists before the evaluator can reject it. Detection is
not admission control.

### Option B — rely on provider sandbox path permissions

Provider sandboxes can restrict access but differ by host, may be advisory or
coarse, and cannot enforce harness decision rights, state fingerprints, or
transaction recovery. They remain useful defense in depth.

### Option C — use a Git worktree and merge or copy the result

A worktree gives a familiar coding environment, but creation and removal mutate
target Git administrative state, link back to the main repository, introduce
branch/index semantics, and complicate Windows portability and Git authority.

### Option D — use an evaluator-created isolated session and an evaluator-built
content-addressed bundle applied by a journaled broker

The worker edits only non-authoritative session bytes. The evaluator snapshots
the proposed delta into a canonical bundle, admits it against live state, and
is the sole target writer. Durable external journals and backups support
rollback and crash recovery.

## Decision

Choose Option D, subject to approval of `REQ-AEX-011`, `SPEC-AEX-007`,
`VER-AEX-004`, and the applicable implementation work order.

The external evaluator creates a session workspace outside the target checkout.
The worker cannot use the Phase 4 interface to write target paths. The evaluator
constructs change-bundle v1 from the session delta and explicit deletions. The
bundle contains ordered regular-file create, replace, and delete entries,
content digests and sizes, content-object references, and only the work-order,
envelope, and before-state foreign keys needed to prevent cross-context use.

Under one exclusive target lock, the broker freshly admits the envelope,
preflights the complete bundle, writes a durable journal and recovery material,
applies entries in canonical order, observes the result, and emits a state-bound
receipt. Ordinary failures roll back and prove the prior state. Interruption
leaves a visible recovery-required journal that blocks continuation until the
evaluator proves complete rollback or complete result.

V1 rejects links, junctions, reparse points, special files, submodules, modes,
directory deletes, `.git`, managed current-evaluator surfaces, path ambiguity,
and parallel writers. It does not claim cross-file atomic visibility.

## Consequences

### Positive

- Actual target mutation has one evaluator-owned choke point.
- Proposed bytes can be tested and rejected without first changing the target.
- Bundle identity is deterministic, portable, and reviewable.
- Governance remains normalized: bundles reference authoritative artifacts
  instead of copying their mutable facts.
- Journals make partial interruption explicit and block unsafe continuation.

### Negative

- Agents need an isolated workspace and cannot use ordinary target-writing tools
  during Phase 4 execution.
- Copying or materializing a useful session may cost time and disk space.
- A multi-file bundle can be externally observed midway through application.
- Durable journals, backups, platform-specific replace behavior, and recovery
  tests add implementation complexity.
- Large or unusual repository objects are initially unsupported.

### Operational

- Runtime and session directories must be explicitly configured outside the
  target, access-restricted, space-checked, and cleaned under retention policy.
- Operators must resolve any `human_recovery_stop` before other governed work.
- Provider sandboxing should deny target writes where available, but its absence
  cannot widen the broker contract.
- Later Git or multi-agent support requires new approved architecture.

### Security

- Content objects are immutable, digest-addressed regular files.
- Paths are portable, case-audited, handle-contained, and never followed
  through links or reparse points.
- Journals contain bounded metadata and restricted backups, not credentials or
  hidden reasoning.
- The broker never executes staged content or bundle strings as commands.

### Migration

- Existing direct-writing skills remain on their command-driven non-Phase 4
  contracts until a successor skill version and evaluator are installed.
- No existing checkout is moved into a worktree or rewritten during upgrade.
- Change-bundle v1 and effect-receipt v1 are new schemas with no implicit
  conversion from patches, diffs, or previous receipts.

## Validation

`VER-AEX-004` verifies canonical bundle vectors, content-addressing, path and
object attacks, stale prior state, all supported operations, complete preflight,
ordinary rollback, interruption recovery, journal corruption, receipt linkage,
single-writer behavior, direct-write detection, cross-platform behavior, and
the absence of duplicated governance facts.
