+++
id = "ADR-ECP-002"
type = "adr"
title = "Enforce scope at the Git boundary, not through a proposed-workspace broker"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-28"

[relations]
decides = ["ARCH-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# ADR: Enforce scope at the Git boundary, not through a proposed-workspace broker

## Status

Proposed.

## Context

Execution scope is a coded predicate (`WEX201`), but it is evaluated only
by `check` over agent-typed paths (`se_harness/workflow_compliance.py:316-322`),
never by `transition`, and in CI only when a `Harness-Restitution:` line is
volunteered
(`templates/repository/standard/.github/workflows/engineering-harness.yml:56-89`).
`ADR-AEX-007` chose an isolated-proposal broker because "validation can
detect but not prevent an out-of-scope or stale effect"; `ADR-AEX-006`
wrapped it in an evaluator-derived ephemeral envelope. The result is 8,766
lines (39% of the package) that re-implement a version-control write
boundary inside the process, accept caller-asserted gates
(`se_harness/delegated_workflow.py:399`), guard a token that never leaves
the minting process (`se_harness/delegated_authority.py:25`, `:206-220`),
and have never run on a real work order because no `[agentic_delegation]`
table exists (`docs/notes/complexity-audit-2026-08.md`, P0-5). The one
boundary an agent cannot bypass on the way to `main` is the pull request.

## Decision drivers

- Principle 2 of the review: enforcement lives at Git boundaries.
- Principle 5: delegation is a work-order attribute unlocked by a green
  gate; no envelope, no broker.
- Prevention that survives an agent ignoring every skill.
- Retain the one Phase 4 property with a recorded reason to exist: the
  crash-safe journaled apply for multi-file writes on Windows
  (`tests/test_effect_broker.py:308-344`).
- Remove a second execution model that agents must recognise and ignore.
- Keep `result_sha256` meaningful: it must bind the change set it claims.

## Considered options

### Option A: the existing proposed-workspace broker (`ARCH-AEX-002`, `ADR-AEX-006`, `ADR-AEX-007`)

Keep the envelope, bundle, and broker; activate them by adding
`[agentic_delegation]` to work orders. Consequences: scope is enforced only
for writes routed through the broker; a direct write to the working tree is
invisible to it; gates are whatever the caller asserts; six full-tree
digests per bundle; the trust boundary the envelope defends does not exist;
every consumer must learn a second model. Rejected.

### Option B: Git worktrees per work order, checked by the harness

The harness creates a worktree per work order and diffs it against the base.
Consequences: gives isolation, but the agent already has that on a branch;
the harness would own checkout lifecycle and locking; the same diff could be
obtained without owning the worktree; adds host-specific behaviour on
Windows path length and file locks. Rejected as unnecessary ownership; its
observable value is the diff, which Option C obtains directly.

### Option C: enforce at the Git boundary; keep only the journaled apply

The change set is `git diff` plus untracked files; `check --from-git` and
the CI gate evaluate scope over it unconditionally; the digest covers it;
delegation is a `[delegation]` class that unlocks three transitions only
when the required check for the head is `success`; the envelope, bundle,
receipts, and `delegated-workflow` leave the product; the journaled apply is
retained for the harness's own multi-file writes. Consequences: prevention
for anything that reaches `main`; nothing for the agent to route through;
roughly 3,900 lines to 2,300 in the execution chain and about 1,800 fewer in
the client surface (audit, simplification 3); requires a required branch
protection rule the harness cannot set.

## Decision

Select Option C (`SPEC-ECP-003`, `SPEC-ECP-006`, and the `ECP-CHG-*` rules of
`SPEC-ECP-001`). Once accepted, this ADR supersedes the write-boundary
decision of `ADR-AEX-007` and the ephemeral-authority envelope decision of
`ADR-AEX-006`; `ARCH-AEX-002`'s effect broker survives only as the journaled
writer. Those artifacts, and the agentic-execution domain README, receive
amendment records under `WO-ECP-006` that name this ADR and state what
remains in force.

## Consequences

- Positive: scope becomes enforced for any agent on any host; the digest
  proves what was declared; one execution model; the fault-tested apply
  stays.
- Negative: a repository whose branch protection does not require the check
  gets detection, not prevention, and must be told so in `doctor`; the
  removal of `delegated-workflow` is not reversible without re-approving
  the superseded ADRs.
- Operational: consumers see the managed workflow updated and the
  `[agentic_delegation]` template block replaced by `[delegation]`; the
  delegated route needs a `[ci_status]` table and a token.
- Security: gates reaching a transition are the harness's own results, not
  caller JSON; a delegated actor is a verified identity (`ADR-ECP-003`)
  acting only behind a green gate on a named head.
- Migration: `WO-ECP-003` ships the gate and digest, `WO-ECP-006` removes the
  envelope and writes the amendment records on `ADR-AEX-006`, `ADR-AEX-007`,
  `ARCH-AEX-002`, and the domain README; no historical record is rewritten.

## Validation

`ECP-GTE-002` failing-path test in the template workflow on Linux and
Windows runners; `ECP-DIG-003` distinct-digest tests; `ECP-DLG-003` refusal
when the conclusion is not `success`; `ECP-DLG-008` absence test over the
wheel; `ECP-JNL-004` fault matrix on every writer; an amendment-record
presence test on the four agentic-execution artifacts.
