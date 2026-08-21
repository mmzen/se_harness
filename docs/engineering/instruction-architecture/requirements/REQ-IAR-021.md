+++
id = "REQ-IAR-021"
type = "requirement"
title = "Route repository-local operational facts to the owner-controlled region"
status = "implemented"
owners = ["requirements-steward", "repository-owner", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN the managed instruction surface routes an agent to repository-local operational facts, THE SYSTEM SHALL name the owner-controlled region of AGENTS.md as their location, SHALL NOT name a harness-scaffolded context document, and SHALL NOT make the presence or completeness of ungoverned owner content a harness stop condition."
verification_method = "Automated managed-integrity, routing-content, and workflow-conformance tests plus accountable review of the authority boundary"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Route repository-local operational facts to the owner-controlled region

## Lifecycle

Drafted on 2026-08-21 as the instruction-surface half of the repository-context boundary change, and approved by the repository owner the same day together with `REQ-DST-065` and the rest of the packet. Paired with `REQ-DST-065`, which governs scaffolding and readiness. The two open decisions were resolved at approval and are recorded below.

Approval makes this requirement active. It does not authorize implementation, which `WO-DST-021` governs, and it does not transition `REQ-IAR-005` or revise `REQ-IAR-003`; both are implementation work under the same work order.

## Rationale

`INT-IAR-001` makes harness instructions simple, adaptable, and enforceable. `CAP-IAR-001` routes and enforces repository-aware engineering instructions. Routing is only useful when the destination holds the fact and the harness can say something true about it.

The managed router currently names `REPOSITORY_CONTEXT.md` in three roles: as the location of repository commands, as owner information in the component model, and as a stop condition when "repository context is incomplete". All three are unsound once the scaffold is withdrawn, and two of them were unsound already.

The stop condition is the clearest case. It makes harness operation conditional on the completeness of a document the harness tracks by presence only. `SPEC-IAR-001` records the mode as `seed` with the repository owner as post-installation owner, so the harness has no content stake and no definition of complete beyond fifteen non-empty labels that a placeholder satisfies. A stop condition the harness cannot evaluate is not enforceable, and `INT-IAR-001` exists to make instructions enforceable.

The routing role is redundant rather than wrong. `AGENTS.md` is already loaded on every agent turn through the single `@AGENTS.md` import in `CLAUDE.md`, which `inspect_installation` verifies. Routing from an always-loaded file to a second document, to recover facts the owner could have stated in the first, adds a read without adding information. The owner-controlled region is the correct destination because it is the one surface that is simultaneously always present, always loaded, and wholly owner-owned.

The workflow-execution coupling must be resolved in the same change. `REQ-WEX-010` permits a procedure step of kind `reference` to resolve one "repository-context action ID", and `SPEC-WEX-002` locates those identifiers in `REPOSITORY_CONTEXT.md`. Measurement shows the form is unexercised: across the seventeen procedures in both the released `se_harness/workflow_contract.json` and the candidate template, zero steps declare an `action_id`, and every step kind is `command` or `decision`. Only a synthetic test fixture exercises `context_actions`. Withdrawing the form therefore costs no behavior.

Withdrawing it is also the principled outcome. `resolve_procedure` raises `WEX220` unless the named action resolves exactly once in a `seed`-mode file whose content nothing verifies. Executing steps read from ungoverned owner content contradicts the requirement that every directive bind to an executable procedure under harness authority. If the harness cannot govern the content, it must not execute it.

## Preconditions and trigger

- The managed instruction surface routes an agent to repository commands, entry points, boundaries, or ownership; or
- a workflow procedure step resolves a reference; or
- a stop condition is evaluated against repository-local content.

The trigger includes operational and exploratory tasks that never reach a lifecycle handoff, because the router is loaded before task selection.

## Required response

1. The managed router SHALL name the owner-controlled region of `AGENTS.md` as the location of repository-local operational facts, and SHALL NOT name a harness-scaffolded context document in any role.
2. The managed router SHALL NOT make the presence, completeness, or currency of ungoverned owner content a stop condition.
3. The managed router SHALL retain every stop condition it can evaluate, including a missing or damaged managed gate and a material conflict between owner instructions and managed policy.
4. The installed managed fragment SHALL continue to name exactly one harness destination. This requirement adds no second destination.
5. Installation guidance SHALL state, once, that the owner is responsible for recording build, test, verification, ownership, and boundary facts in the region the installer preserves.
6. The procedure step kind `reference` SHALL resolve only to a procedure identifier. The repository-context action-identifier form SHALL be withdrawn from the requirement, the specification, the contract schema, and the resolver.
7. Managed policy modules SHALL be revised so that no active artifact describes the withdrawn document as a live obligation, while historical records remain unchanged.
8. The owner-controlled region SHALL remain wholly owner-owned. This requirement states where facts belong; it does not track, validate, or hash-lock their content.

## Failure and boundary behavior

- A repository whose owner region states nothing operational is not blocked. The harness loses a pointer, not a gate. That is the intended trade: an unenforceable stop condition is replaced by no stop condition rather than by a stricter one.
- A managed router still naming the withdrawn document fails the routing-content check.
- A workflow contract still declaring an action-identifier reference fails conformance.
- A change that reflows, splits, or re-whitespaces the tracked block between the `se-harness` markers changes the fragment digest and fails `doctor`, preflight `I001`, and the required CI check. `utf8-text-lf-v1` canonicalizes line endings only.
- Adding validation of owner-region content would violate response item 8 and is a failure of this requirement, not a stricter satisfaction of it.

## Constraints

- Change portable managed policy and the packaged templates. Repository-local application to this repository's own `AGENTS.md` owner region is governed separately by `REQ-IAR-020`.
- Preserve the single managed harness destination and the existing router-to-focused-policy split.
- Do not introduce a formatter or linter gate, and do not add a machine-readable schema for owner-region content.
- Do not waive formal artifact authority, approved work-order scope, required evidence, or accountable verification and release decisions.
- Historical evidence, verification records, and release records remain unchanged.

## Acceptance examples

### Example: normal routing

**Given** an agent has loaded `CLAUDE.md` and `AGENTS.md` in a freshly installed repository

**When** it is asked where the repository's test command is recorded

**Then** the managed router names the owner-controlled region of `AGENTS.md`, names no scaffolded context document, and the agent needs no further managed reading to locate the fact.

### Example: unenforceable stop condition withdrawn

**Given** a repository with no repository-context document and no operational facts in its owner region

**When** the managed stop conditions are evaluated

**Then** no stop condition fires on incomplete repository context, and the retained stop conditions on a missing or damaged managed gate remain in force.

### Example: failure behavior

**Given** a candidate managed router that names `REPOSITORY_CONTEXT.md` as the source of repository commands

**When** the routing-content check runs

**Then** the check fails and identifies the naming line, because the document is no longer a governed destination.

## Resolved decisions

Both were resolved by the repository owner on 2026-08-21 at approval.

First, the withdrawn `reference` action-identifier form is retained as a rejected value with an explicit diagnostic rather than silently dropped from the schema, so a stale contract is distinguishable from an unrecognized field. Adopted by approving `SPEC-IAR-013` rule 7, which governs the behavior; the rejection point is left to the implementer provided it precedes resolution.

Second, `ARCH-IAR-001` requires no revision and no deciding ADR. The change is visible in its descriptive text but alters no component boundary, dependency direction, or trust boundary, and the artifact declares only the deprecated `constrains` relation rather than `addresses` on this requirement. The accountable no-ADR rationale is recorded in `REQ-DST-065`, which resolved the same question for `ARCH-DST-002` and `ARCH-DST-007` in the same decision.
