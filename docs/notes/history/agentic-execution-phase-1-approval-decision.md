# Phase 1 Agentic Execution Approval Decision

> Historical record from 2026-08-24, at `6268821`. Kept for the decision trail; it describes the tool as it was then.

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Prepared: 2026-08-24\
Selected domain: `agentic-execution`\
Selected packet: 16 formal artifacts, `INT-AEX-001` through `WO-AEX-001`\
Decision outcome: approved by the user under separate accountable-role assertions\
Application outcome: completed atomically after synchronizing current `main`\
Current lifecycle state: all selected artifacts are `approved`\
Lifecycle effect of this document: none

> This is non-authoritative decision input. It does not approve an artifact,
> apply a transition, authorize implementation, or prove a person's real-world
> role. Formal authority remains in the artifacts and managed lifecycle.

## Decision outcome

On 2026-08-24, the user approved the complete Phase 1 definition packet and
bounded `harness-orient` work order under all accountable-role assertions and
authorized exactly one atomic `draft -> approved` transaction. The user also
prohibited implementation and external action.

Accountable content review is complete, the accepted revisions are
incorporated, and evaluator 0.6.0 reports a valid formal graph. The read-only
transition planner accepts all 16 proposed changes with no scoped or repository
blockers.

## Application result

The first authorized apply attempt stopped before any write because the old
local checkout still carried the schema-2 root lock:

```text
operation: transition
outcome: blocked
blocker: WEX201 / MG002
message: ordinary mutation requires a schema-3 evaluator identity; use a
         separately governed upgrade
writes: 0
```

The checkout was then fast-forwarded to current `origin/main` at `db70496`,
which already contains the governed schema-3 root adoption and exact released
evaluator 0.6.0 identity. The Phase 1 work was preserved across that sync.

An index-installed evaluator then stopped before write with `MG005` because it
lacked the exact PEP 610 wheel-archive identity. The published wheel was
downloaded, independently verified against root-lock SHA-256
`2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`,
and installed into the isolated sibling evaluator from those exact local bytes.

The released evaluator subsequently passed managed-integrity doctor and graph
validation. The exact authorized transaction then completed atomically:

```text
operation: transition
outcome: completed
applied transitions: 16
partial writes: 0
```

Post-transition checks confirm that all 16 artifacts are `approved` and the
725-artifact graph validates with zero errors. `RLS-SEH-009` and `RLS-SEH-012`
were not changed.

## Readiness evidence

| Check | Result |
| --- | --- |
| Accountable content review | Complete for all 16 artifacts under the user's separate assertions for all accountable roles |
| Accepted revisions | Decision-class terminology, nine cross-cutting invariants, and the 16-path pilot scope are incorporated |
| Assurance classification | Repository-owner content decision recorded as commit-bound verification `required` |
| Architecture decisions | Technical-owner content acceptance recorded for both Option D decisions and the architecture assessment |
| Evaluator version used for the current graph and preview | 0.6.0 |
| Evaluator 0.6.0 graph validation | Pass: 725 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| Read-only lifecycle preview | Pass: 16 planned transitions, compatibility pass, 0 blockers, 0 files written |
| Applied lifecycle transaction | Pass: 16 transitions applied atomically by the isolated exact-wheel evaluator |
| Current AEX states | All 16 are `approved` |

The earlier isolated 0.5.0 release-history findings are predecessor-compatibility
observations, not defects in `RLS-SEH-009`, `RLS-SEH-012`, or the AEX packet.
They do not require release-record investigation for this decision.

The repository's managed root lock is schema 3 and binds evaluator 0.6.0 by
version, payload digest, wheel name, and wheel SHA-256. The applied transition
used an isolated evaluator installed from those exact wheel bytes.

## Applied atomic transaction

| Accountable assertion | Artifacts | Proposed change |
| --- | --- | --- |
| Product owner | `INT-AEX-001`, `CAP-AEX-001` | `draft -> approved` |
| Requirements steward | `REQ-AEX-001` through `REQ-AEX-007` | `draft -> approved` |
| Technical owner | `SPEC-AEX-001`, `SPEC-AEX-002`, `ARCH-AEX-001`, `ADR-AEX-001`, `ADR-AEX-002` | `draft -> approved` |
| Assurance owner | `VER-AEX-001` | `draft -> approved` |
| Engineering owner | `WO-AEX-001` | `draft -> approved` |
| Repository owner | `WO-AEX-001` assurance classification and exact transaction | confirm `required` and authorize only this packet |

The transaction changed only each selected artifact's `status`, `updated`, and
`lifecycle_events` fields.

## Effects of approval and application

- Phase 1 definitions, architecture, ADRs, and verification contract become
  authoritative approved inputs.
- `WO-AEX-001` becomes bounded implementation authority for only the read-only
  `harness-orient` pilot and its 16 declared paths.
- Phase 1 reaches its roadmap exit criterion: the first implementation work is
  approved and bounded.
- Implementation still begins only after successful start preflight and an
  explicit implementation handoff.

## Explicit non-effects

Approval does not:

- start implementation or change source code;
- apply an autonomy envelope or authorize mutating skills;
- authorize subagents, parallel writers, or runtime adapters;
- create a commit, branch, pull request, VREC, release, tag, publication, or
  deployment;
- authorize credentials, network access, or another external action; or
- alter `RLS-SEH-009`, `RLS-SEH-012`, managed root files, or evaluator
  installation state.

## Accountable response retained for audit

The lifecycle transaction was authorized with this decision:

```text
As product owner, approve INT-AEX-001 and CAP-AEX-001.
As requirements steward, approve REQ-AEX-001 through REQ-AEX-007.
As technical owner, accept ADR-AEX-001 and ADR-AEX-002 and approve
SPEC-AEX-001, SPEC-AEX-002, and ARCH-AEX-001.
As assurance owner, approve VER-AEX-001.
As repository owner, confirm commit-bound verification is required for
WO-AEX-001 and authorize the exact reviewed atomic transaction.
As engineering owner, approve WO-AEX-001 for its exact 16-path scope.
Apply only these 16 draft-to-approved transitions. Do not start implementation
or perform any external action.
```

## Read-only preview result

Evaluator 0.6.0 returned:

```text
operation: transition
outcome: completed
compatibility: pass
planned transitions: 16
scoped blockers: 0
repository blockers: 0
files written: 0
```

The preview intentionally omitted `--apply`.

## Current handoff

**Completed:** Reconciled the accepted formal content, validated the graph with
evaluator 0.6.0, regenerated the exact no-write preview, recorded accountable
approval, and attempted the authorized atomic transaction once. The mutation
guard stopped it before writing.

**Current lifecycle state:** All 16 AEX artifacts are `approved`.

**Recommended next step:** Stop before implementation. When separately
authorized, select `WO-AEX-001` and run its start checkpoint and preflight.

**Human decision or approval required:** A separate implementation-start
handoff. Phase 1 approval does not itself start implementation.

**Command or suggested response:** `Begin WO-AEX-001 start checkpoint and
preflight; do not change files until the returned manifest has been read.`
