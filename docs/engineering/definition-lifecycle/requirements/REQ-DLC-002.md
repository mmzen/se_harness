+++
id = "REQ-DLC-002"
type = "requirement"
title = "Terminate the definition lifecycle at approved"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "WHEN the managed lifecycle contract is asked which states a definition artifact may transition to from approved, THE SYSTEM SHALL offer rejected only, SHALL refuse a planned or applied transition to implemented for the intent, capability, requirement, specification, architecture, adr, verification, release_contract, and operating_contract families, and SHALL continue to accept, display, and treat as governing authority every definition that already carries the implemented status."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DLC-001"]
+++

# Requirement: Terminate the definition lifecycle at approved

## Rationale

The `approved -> implemented` edge exists in `WORKFLOW.json`, in
`se_harness/workflow_contract.json`, and in the `WORKFLOW.md` state table. It
exists nowhere else that matters:

- **No decision right grants it.** `DR-DEFINITION-DECIDE` in
  `DECISION_RIGHTS.md` is defined as "Approve or reject an intent, capability,
  requirement, specification, architecture, ADR, verification contract, release
  contract, or operating contract". It has two outcomes.
  `PROC-DEFINITION-COMPLETE` offers `outcomes = ["implemented", "reject",
  "stop"]`, so the workflow contract admits an outcome no decision right
  authorizes.
- **No step of the managed procedure performs it.** The eleven numbered steps
  in `WORKFLOW.md` move from approving definitions (steps 2 to 4) to approving
  a bounded work order. No step marks a definition `implemented`.
- **Nobody has ever taken it.** Across 630 definitions the only recorded edges
  are `draft -> approved` (181) and `approved -> rejected` (6). The transition
  has been applied zero times.
- **It buys nothing and forecloses everything.** Planning
  `REQ-TCM-001=implemented` against `c189b58` with the released `0.6.0`
  evaluator returns `PLANNED`, reports "REQ-TCM-001 is implemented and
  terminal", and recommends inspecting the related work order — the same advice
  the `approved` recommendation already gives. The state grants no authority
  that `approved` does not already grant, since both carry `grants_authority:
  true`, and `transitions_to: []` with `transitionable: false` means nothing
  can ever follow it.
- **The claim it makes cannot stay true.** 86 of the 244 requirements named by
  a work order are named by more than one, and `REQ-DST-006` is named by 16. 49
  of the 104 `implemented` requirements are named by more than one work order.
  A terminal `implemented` on a requirement asserts completion while further
  work orders continue to implement it, and can never be corrected.

Removing the edge makes the reachable lifecycle agree with the two managed
documents that already describe it correctly.

## Preconditions and trigger

- A definition artifact is `approved` and an actor plans or applies a
  transition, or a conformance test reads the reachable transition graph.
- Or a definition artifact already carries `implemented`, and the harness reads,
  validates, displays, focuses, or reports it.

## Required response

- Set the definition family's `approved.transitions_to` to `["rejected"]` in
  both byte-identical contract copies: `se_harness/workflow_contract.json` and
  `templates/repository/standard/docs/engineering/WORKFLOW.json`.
- Keep the definition family's `implemented` row present, with
  `grants_authority: true`, `must_remain_visible: true`, `transitionable:
  false`, and `transitions_to: []`, exactly as `ready`, `in_progress`,
  `verified`, and `released` are already kept as unreachable compatibility
  vocabulary in that family.
- Set the `implemented` row's `predecessor_adapter` to whatever the migration
  contract requires for a state that a predecessor evaluator could still admit
  a transition into.
- Change the `WORKFLOW.md` state table row `| Definition | approved |
  implemented, rejected |` to `| Definition | approved | rejected |`, and state
  that `implemented` remains accepted, visible, and authority-granting on
  existing definitions.
- Retire `PROC-DEFINITION-COMPLETE` and its `STEP-DEFINITION-COMPLETE`, the
  only carriers of the `implemented` outcome for a definition.
- Re-point `WFL-DEFINITION-COMPLETE` at the work-selection procedure with
  `DR-WO-SELECT` and `QG-G3-WORK-AUTHORIZATION`, so an approved definition is
  routed to the decision that actually comes next, and revise its handoff to
  cover the case where no work order names the definition yet.
- Leave `WFL-DEFINITION-WORK` matching `implemented` unchanged, so the 165
  existing implemented definitions keep a resolvable recommendation.
- Leave `DR-DEFINITION-DECIDE` unchanged. It already describes exactly the
  approve-or-reject decision that survives.

## Failure and boundary behavior

- A planned or applied `approved -> implemented` transition on any definition
  family is refused by the ordinary lifecycle-legality path, with the ordinary
  diagnostic. No special-case message and no new code is introduced.
- `implemented` stays in `ALLOWED_STATUSES`. A definition carrying it is valid,
  is not a warning, is not an error, and is not migrated.
- Every `(artifact_type, status)` pair that exists in the repository keeps a
  matching recommendation rule. A pair with no rule is a hard failure in the
  workflow resolver, so the conformance tests must enumerate all nine families
  against all reachable and all historical statuses.
- A predecessor evaluator that still admits the edge is handled by the
  migration contract's adapter, not by re-admitting the edge.

## Constraints

- No artifact bytes change. The 165 `implemented` definitions are not migrated,
  normalized, superseded, or re-decided in either direction. Editing an
  `implemented` architecture back to `approved` would convert `W014` into
  `E014`; `REQ-DLC-001` must land first regardless, and this requirement still
  does not touch the field.
- `HRN-006` holds: nothing in this change makes a work-order transition move a
  definition.
- The `WFL-DEFINITION-COMPLETE` identifier is kept rather than renamed, because
  it is published in a managed document and in a machine contract that
  consumers pin. The resulting name-versus-behaviour residue is accepted and
  must be disclosed in the implementation notes.
- Whether this is a within-`se-harness-workflow-v3` edge retirement or requires
  `se-harness-workflow-v4` is a technical-owner decision recorded before
  implementation starts. Either way, the two delivery copies stay
  byte-identical and a governance-migration scenario covers the version pair.

## Acceptance examples

### Example: normal behavior

**Given** an approved requirement, specification, architecture, intent,
capability, ADR, verification contract, release contract, and operating
contract

**When** each is planned to `implemented`

**Then** every plan is refused as an illegal transition, and each is planned to
`rejected` successfully.

### Example: existing records keep authority

**Given** the 165 definitions that already carry `implemented`

**When** the graph is validated and each is focused, reported, and displayed

**Then** the verdict is 0 errors, each is treated as governing authority for
coverage, each resolves a recommendation, and no byte of any of them changes.

### Example: failure behavior

**Given** the revised contract

**When** a conformance test enumerates every definition family against every
status in `ALLOWED_STATUSES`

**Then** no `(family, status)` pair that occurs in the repository resolves to no
recommendation rule, and the reachable transition graph matches the
`WORKFLOW.md` state table exactly.

## Open decisions

Before approval, the technical owner must decide the contract-schema question —
within-v3 retirement or a v4 bump — and the repository owner must accept that
`WFL-DEFINITION-COMPLETE` keeps its identifier while its procedure and decision
right change.
