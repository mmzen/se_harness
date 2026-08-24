+++
id = "REQ-AEX-007"
type = "requirement"
title = "Orchestrate workers and materialize runtime adapters without changing authority"
status = "approved"
owners = ["product-owner", "requirements-steward", "technical-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN a supported workflow delegates work to multiple agents or materializes runtime-native agent configuration, THE SYSTEM SHALL preserve the same selected scope, permitted operations, stop decisions, evidence obligations, and final validation as the single-agent procedure; constrain concurrent writers to explicit disjoint scopes with one final integration owner; treat generated runtime configuration as derived and replaceable; and provide a deterministic single-agent fallback."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "requirements-steward"
+++

# Requirement: Orchestrate workers and materialize runtime adapters without changing authority

## Rationale

Subagents can reduce context pollution, improve analytical coverage, and execute
independent work concurrently. They also introduce coordination, stale-state,
permission-inheritance, cost, and write-conflict risks. Runtime-native agent
definitions vary across providers and can evolve independently from the
engineering model.

## Preconditions and trigger

A skill or orchestrator proposes more than one worker, or an operator requests
runtime-native agent definitions derived from logical execution profiles.

## Required response

- Begin from the same validated scope and procedure used by the single-agent
  path.
- Assign each worker one bounded task, execution profile, allowed operation set,
  input manifest, and structured return contract.
- Prefer parallel read-only work for exploration, tests, logs, and review.
- Require explicit disjoint path or artifact scopes and isolated worktrees for
  concurrent writers.
- Designate one integration coordinator as the sole owner of the final combined
  candidate.
- Re-run required gates and evidence binding against the combined repository,
  not individual worker snapshots.
- Materialize runtime configuration from logical profiles through a
  plan-by-default, ownership-aware, transactional adapter.
- Mark generated files and manifests as derived and preserve user customization.
- Fall back to the single-agent procedure when orchestration or an adapter
  feature is unavailable.

## Failure and boundary behavior

- Worker failure, timeout, interruption, missing output, overlap, or conflicting
  scope remains visible in the aggregate result.
- A worker cannot spawn a child with broader scope or authority than its own.
- Parallel writes without proven disjoint scope fail before execution.
- Integration conflict or stale evidence stops before a completion claim.
- Unsupported runtime behavior produces explicit degradation; it cannot bypass
  a gate or silently omit a required stage.
- Adapter generation never changes formal lifecycle state.

## Constraints

- Different contexts, models, or sandboxes do not create accountable separation
  of duties.
- Model selection is an execution optimization rather than an authoritative
  product decision unless a separately approved requirement makes it part of a
  verified contract.
- Adapter files may narrow technical permissions but cannot grant engineering
  authority.
- Multi-agent benefit must be measured against token, latency, conflict, and
  coordination cost.

## Acceptance examples

### Example: parallel read-only review

**Given** one approved candidate and three read-only review tasks

**When** the orchestrator delegates security, test-gap, and architecture
analysis

**Then** each worker receives the same candidate identity and bounded task, all
results appear in the receipt, and the integration coordinator emits one
combined decision packet without changing repository content.

### Example: overlapping writers

**Given** two proposed implementation workers whose path scopes overlap

**When** orchestration is planned

**Then** the plan fails or serializes the work before either worker writes.

## Open decisions

Before approval, the architecture must define logical profile storage,
worktree and writer-lease semantics, adapter ownership modes, conformance
levels, and which runtime-specific metadata may be generated or committed.
