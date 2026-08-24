+++
id = "REQ-AEX-008"
type = "requirement"
title = "Complete a bounded single-agent workflow through outcome skills"
status = "approved"
owners = ["product-owner", "requirements-steward", "technical-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN an operator explicitly invokes a supported SE Harness skill to prepare draft definitions, execute one already-started bounded work order, or prepare commit-bound assurance material, THE SYSTEM SHALL execute the applicable command-equivalent single-agent procedure using current released-evaluator state, constrain effects to the declared preparation or work-order boundary, retain deterministic evidence, and stop before every accountable approval, work-completion decision, assurance decision, delivery choice, release decision, Git mutation, credential use, or external action."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T13:50:24Z"
decided_by = "requirements-steward"
+++

# Requirement: Complete a bounded single-agent workflow through outcome skills

## Rationale

The read-only `harness-orient` pilot proves skill discovery and portable
inspection, but operators still need to assemble the drafting, implementation,
evidence, and assurance-preparation procedures from individual commands. The
MVP should reduce those procedural interactions without moving accountable
decisions into prompts, skills, runtime permissions, or agent judgment.

## Preconditions and trigger

An operator explicitly invokes exactly one supported writing skill, supplies an
unambiguous repository and selected scope, and provides any actor assertion or
candidate identity required by the existing managed procedure. Implicit skill
activation is not a precondition for a write.

## Required response

- Provide `harness-draft-change`, `harness-execute-work-order`, and
  `harness-prepare-assurance` alongside the unchanged `harness-orient` skill.
- Use the target repository's exact released evaluator for installed integrity,
  formal state, workflow checkpoints, and governed preparation commands.
- Require explicit activation for each skill whose declared mutation class is
  not `read-only`.
- Recheck evaluator identity, repository state, selected artifact, applicable
  checkpoint, and allowed path source immediately before a helper-controlled
  effect.
- Create or revise only explicitly selected drafts during definition
  preparation and never approve or transition them.
- Execute implementation only when the selected work order is already
  `in_progress`, and change only paths admitted by its declared execution
  scope.
- Retain the selected work order's required implementation evidence and stop
  before marking it implemented.
- Prepare a VREC only from an exact clean candidate, complete applicable work
  and evidence, passing preparation gates, and an explicitly named preparation
  actor; produce only a `ready` record.
- Emit one structured result and one deterministic receipt identity for every
  completed, stopped, degraded, or failed invocation.
- Preserve a complete single-agent procedure without requiring subagents,
  provider-specific configuration, connectors, or a hosted service.

## Failure and boundary behavior

- Missing or damaged managed content, wrong evaluator identity, invalid graph,
  ambiguous selection, stale state, failed required gate, unauthorized
  lifecycle state, path-scope mismatch, or incomplete evidence stops before the
  associated effect.
- An `approved` but not started work order produces the current start decision
  packet and no implementation write.
- An unexpected changed path prevents a completion claim and is reported for
  bounded remediation; the skill does not widen the work order or hide the
  change.
- A draft-preparation skill cannot edit an approved formal artifact or use a
  note, prompt, or previous conversation as approval.
- Assurance preparation cannot verify, reject, supersede, deliver, release, or
  publish the candidate.
- No skill may commit, push, merge, tag, publish, deploy, operate, use a
  credential, or perform another external action without a separate exact
  action-time authorization and procedure outside this MVP.

## Constraints

- Skills remain non-authoritative procedure packages. They do not duplicate or
  override managed workflow, decision-right, quality-gate, or traceability
  rules.
- Phase 3 does not introduce autonomy-envelope-backed delegated lifecycle
  transitions. That remains later governed work.
- Runtime write permission is not proof that a path or operation is authorized.
- Receipts and successful commands are evidence, not approval, verification,
  release, or proof of substantive correctness.
- Existing `harness-orient` behavior, contract identity, and read-only boundary
  remain unchanged.

## Acceptance examples

### Example: execute one started work order

**Given** one `in_progress` work order with a passing current preflight and an
exact declared path scope

**When** the operator explicitly invokes `harness-execute-work-order`

**Then** the skill implements, tests, reviews, and retains evidence inside that
scope, emits a handoff result, and stops before the engineering owner records
completion.

### Example: work order has not started

**Given** one approved work order that has no recorded start decision

**When** the operator invokes `harness-execute-work-order`

**Then** the skill performs only the applicable read-only checks, returns the
start decision packet, and changes no implementation or lifecycle byte.

### Example: prepare assurance

**Given** one implemented work order, its required verification contract and
evidence, one exact clean candidate commit, and an explicitly named preparation
actor

**When** the operator invokes `harness-prepare-assurance`

**Then** the skill prepares one ready VREC and assurance packet and stops before
the assurance-owner decision.

### Example: writing skill activates implicitly

**Given** a natural-language request that could match more than one writing
skill and no explicit skill selection

**When** the runtime proposes an invocation

**Then** no writing procedure starts and the result requests an exact selection
without changing repository state.

## Open decisions

Before approval, the specification and ADR must close the portable writing-skill
contract version, exact activation and checkpoint behavior, skill-specific
effect boundaries, evidence retention, packaging, compatibility, and
single-agent fallback.
