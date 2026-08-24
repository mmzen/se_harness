# Agentic Execution Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this directory
> or this index.

This domain proposes how SE Harness can delegate routine engineering execution
to agent workers while retaining accountable humans at product, architecture,
assurance, release, risk, and external-action decisions.

## Phase 1 definition packet

- `INT-AEX-001`: make governed agent execution autonomous between accountable
  decisions.
- `CAP-AEX-001`: delegate bounded engineering execution to agent workers.
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
- `SPEC-AEX-001`: authority, delegation, decision-packet, and execution-receipt
  contract.
- `SPEC-AEX-002`: portable skill, read-only orientation, orchestration, and
  runtime-adapter contract.
- `ARCH-AEX-001`: harness-owned authority plane with replaceable execution and
  runtime planes.
- `ADR-AEX-001`: accepted design choice to keep authority in the harness and treat
  skills, profiles, and adapters as non-authoritative execution machinery.
- `ADR-AEX-002`: accepted design choice to establish deterministic single-agent
  execution before bounded multi-agent parallelism and retain one final
  integration owner.
- `VER-AEX-001`: independent evidence contract for the seven proposed
  requirements.
- `WO-AEX-001`: bounded read-only `harness-orient` pilot with commit-bound
  verification classified as `required`.

The authoritative state of each artifact is its front-matter `status` and
lifecycle history. Accountable content review does not itself authorize
implementation, a lifecycle transition, a commit, a pull request, assurance,
release, runtime materialization, or an external action.

## Phase 2 runtime-neutral contract layer

- `SPEC-AEX-003` is the approved definition of the core contract catalog,
  repository-state binding, envelope semantics, bounds, compatibility rules,
  decision-packet projection, receipt coverage, and logical profiles.
- `ADR-AEX-003` is the approved decision to derive future authoritative
  envelopes through the exact released evaluator, pass them in memory by
  default, and persist only declared evidence and digests.
- `WO-AEX-002` is in progress. Its bounded implementation adds the canonical
  `se_harness/agent_contract.json` catalog and the pure
  `se_harness.agent_contract` module for strict parsing, canonical encoding,
  candidate construction, narrowing, admissibility assessment, packet
  projection, receipt validation, and provider-neutral profile validation.
- The non-authoritative
  [`agentic-execution-phase-2-contract-closure.md`](../../notes/agentic-execution-phase-2-contract-closure.md)
  records the gap assessment and accepted planning recommendations.
- The contributor guide
  [`agentic-execution-contracts.md`](../../notes/agentic-execution-contracts.md)
  explains the executable API and its authority boundary.

Phase 2 returns `constructed` and `admissible` only. It does not observe a live
repository, derive an authoritative envelope, admit or perform a mutation,
invoke a skill, coordinate a worker, materialize a runtime adapter, or grant an
accountable decision right. Those effects require later approved work and a
fresh exact-evaluator check.

## Planning context

The non-authoritative
[`agentic-execution-roadmap.md`](../../notes/agentic-execution-roadmap.md)
explains the proposed sequencing. The formal artifacts in this directory must
be reviewed on their own merits and supersede that note wherever they differ.

The non-authoritative
[`agentic-execution-phase-1-definition-review.md`](../../notes/agentic-execution-phase-1-definition-review.md)
groups the draft artifacts into accountable review decisions, records revision
dispositions, and preserves a read-only candidate transition preview. It does
not
approve or transition any artifact.

The non-authoritative
[`agentic-execution-phase-1-accountable-review-checklist.md`](../../notes/agentic-execution-phase-1-accountable-review-checklist.md)
provides artifact-specific checks and non-transition response templates for the
product, requirements, technical, assurance, engineering, quality, and
repository reviewers.

The non-authoritative
[`agentic-execution-phase-1-approval-decision.md`](../../notes/agentic-execution-phase-1-approval-decision.md)
records the current 0.6.0 validation and no-write transition preview and presents
the exact accountable decision required to complete Phase 1.

## Scope boundary

`WO-AEX-001` intentionally covers only the read-only orientation pilot. It does
not implement autonomous mutation, VREC or RLS preparation, multi-agent writing,
or runtime adapter materialization. Those capabilities require later bounded
work orders after the relevant definitions and architecture decisions are
approved.
