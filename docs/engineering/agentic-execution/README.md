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
- `WO-AEX-002` is implemented and covered by verified `VREC-AEX-002`. Its
  bounded implementation added the canonical
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

## Phase 3 single-agent workflow skills MVP

- `REQ-AEX-008` requires command-equivalent, explicitly activated single-agent
  procedures for draft preparation, already-started work execution, and
  assurance preparation.
- `SPEC-AEX-004` defines the closed `se-harness-skill-contract-v2` instances,
  checkpoints, effect classes, path sources, results, and stops while retaining
  the exact `harness-orient` v1 contract.
- `ADR-AEX-004` accepts a deterministic three-skill MVP over the existing
  released-evaluator control plane, without envelope-admitted effects,
  subagents, or runtime adapters.
- `VER-AEX-002` defines strict-contract, effect-sentinel, lifecycle, path,
  command-equivalence, installation, packaging, and end-to-end evidence.
- `WO-AEX-003` is implemented. Its bounded implementation adds
  `harness-draft-change`, `harness-execute-work-order`, and
  `harness-prepare-assurance`, preserving the exact orientation core and
  stopping before accountable completion, assurance, delivery, release, Git,
  credential, network, and external-action boundaries.

The [single-agent workflow skills MVP](../../notes/agentic-execution-skills-mvp.md)
is non-authoritative operator guidance for the installed surface.

## Phase 3 repository host activation

- `REQ-AEX-009` requires the four canonical repository skills to be available
  by default in supported Codex and Claude Code sessions without adding a
  second workflow authority.
- `SPEC-AEX-005` defines direct Codex discovery, explicit-only writing policy,
  thin same-name Claude adapters, package inventory, managed ownership, and
  fail-closed canonical loading.
- `ADR-AEX-005` selects repository-scoped adapters over duplicate cores,
  filesystem links, or user-wide provider installation.
- `VER-AEX-003` defines independent source, package, installation, binding,
  activation, hostile-input, and actual-host evidence.
- `WO-AEX-004` is implemented and covered by verified `VREC-AEX-004`. Its
  bounded implementation preserves the exact `harness-orient` v1 core, rebinds
  only the three writing-core patch versions, and adds managed Codex policy and
  Claude discovery surfaces.

The [repository host adapter guide](../../notes/agentic-execution-host-adapters.md)
explains the operator-facing mapping. Host discovery does not grant lifecycle,
Git, credential, network, release, or external-action authority.

## Phase 4 governed delegated execution definition packet

The complete Phase 4 definition packet is `approved`. `WO-AEX-005` through
`WO-AEX-007` are implemented with verified `VREC-AEX-005` through
`VREC-AEX-007`; `WO-AEX-008` is `in_progress` on that exact stacked candidate.
Approval or implementation does not activate
delegated execution, and the candidate implementation cannot govern its own
construction.

- `REQ-AEX-010` requires the exact released evaluator to derive short-lived,
  least-authority envelopes from stable live repository state and recorded
  advance delegation.
- `REQ-AEX-011` requires evaluator-owned transactional change-bundle effects,
  verified receipts, rollback, and explicit interruption recovery.
- `REQ-AEX-012` permits only delegated work-order start/completion and VREC
  preparation and preserves every accountable and external-action stop.
- `SPEC-AEX-006` closes the live observation, delegation declaration, envelope
  v2, nonce, expiry, and receipt-linked state-chain contracts.
- `SPEC-AEX-007` defines change-bundle v1 as byte deltas plus three governance
  foreign keys, the effect broker, journal, rollback, recovery, and receipt.
- `SPEC-AEX-008` defines the closed single-agent workflow through the independent
  assurance stop; release preparation remains disabled in this milestone.
- `ARCH-AEX-002` places live observation, ephemeral authority, isolated
  proposals, target effects, delegated workflow, and evidence under one exact
  external released-evaluator boundary.
- `ADR-AEX-006` proposes formal maximum delegation with one ephemeral
  evaluator-derived envelope per effect.
- `ADR-AEX-007` proposes isolated worker sessions and evaluator-built,
  transactionally applied change bundles rather than direct target writes.
- `VER-AEX-004` defines independent schema, race, replay, path, fault, recovery,
  lifecycle, host-parity, and activation-ladder evidence.

Implementation is split into four sequential work orders:

1. `WO-AEX-005` — live observation and delegated authority derivation;
2. `WO-AEX-006` — transactional change-bundle effect broker;
3. `WO-AEX-007` — delegated workflow advancement and VREC preparation; and
4. `WO-AEX-008` — writing-skill integration and candidate package qualification.

The verified `WO-AEX-007` dependency composes authority and effect components
into the closed delegated start, bundle effect, completion, and VREC-
preparation workflow. `WO-AEX-008` versions the three writing cores as
non-authoritative clients of that interface, preserves host parity, and
qualifies the complete source/wheel/install surface. The
[workflow note](../../notes/agentic-execution-phase4-workflow.md) explains the
coordinator, and the [skill integration note](../../notes/agentic-execution-phase4-skills.md)
explains capability gating and direct-write denial. These are candidate
materials, not release, installation, pilot, or activation.

Phase 4 must be implemented and verified through the existing released
evaluator. A separately governed successor release, external installation, and
disposable pilot are required before the capability can govern a real target or
be considered for low-risk self-hosting.

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

The current Phase 4 packet intentionally covers one logical worker, one target
repository, one active work order, sequential regular-file effects, delegated
start/completion, and VREC preparation. It excludes assurance decisions, release
preparation and decisions, delivery, Git mutation, credentials, network and
external actions, child delegation, multi-agent execution, and parallel writers.
