# Phase 3 Agentic Execution Single-Agent Skills MVP Contract-Closure Proposal

> Historical record from 2026-08-24, at `9a740be`. Kept for the decision trail; it describes the tool as it was then.

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Prepared: 2026-08-24

Selected domain: `agentic-execution`

Local baseline: Phase 2 candidate `fe901b8b52e75a5ffb9fb6be8ccd217371a14651`
with verified `VREC-AEX-002`; the user reports that its pull request is merged.
No network refresh was performed.

Formal artifacts prepared from this proposal: `REQ-AEX-008`, `SPEC-AEX-004`,
`ADR-AEX-004`, `VER-AEX-002`, and `WO-AEX-003` (all `draft`)

Lifecycle effect: none

Implementation effect: none

## Purpose

Phase 3 should prove that an operator can use outcome-oriented skills instead
of manually assembling harness commands. It should not yet change who decides,
delegate lifecycle decisions through autonomy envelopes, add subagents, or
make a runtime adapter authoritative.

This proposal closes the product, interface, architecture, assurance, and work
scope needed for that MVP. It is non-authoritative planning input. Formal
authority remains in approved engineering artifacts and their lifecycle state.
Accepting this proposal does not approve a draft or authorize implementation.

## Identifier audit

The audit inspected all 52 refs currently available in the local repository,
including local branches, locally known remote-tracking refs, tags, and the
candidate ref. The following identifiers were absent from every inspected ref:

- `REQ-AEX-008`
- `SPEC-AEX-004`
- `ADR-AEX-004`
- `VER-AEX-002`
- `WO-AEX-003`

The audit did not fetch or contact a remote because this preparation explicitly
forbids network, Git mutation, and external action. These identifiers are
therefore assigned against the complete locally available ref set, not against
unfetched remote state.

## Phase 2 baseline

The verified Phase 2 candidate provides:

- strict runtime-neutral autonomy-envelope, decision-packet,
  execution-receipt, repository-state, and logical-profile contracts;
- deterministic canonical encoding and validation;
- a portable managed skill package and manifest contract;
- the released `harness-orient` single-agent reference skill; and
- pure validation and admissibility assessment that performs no real mutation.

Phase 2 deliberately did not invoke a mutating skill, add a new workflow
operation, apply an autonomy envelope to a real write, or automate an
accountable decision.

## Phase 3 boundary

The MVP contains four portable skills. `harness-orient` is reused unchanged.
Three new skills are added:

| Skill | Outcome | Allowed effect | Required stop |
| --- | --- | --- | --- |
| `harness-draft-change` | Prepare a declared planning note and complete reviewable draft formal artifacts | Create declared notes and new drafts; revise only explicitly selected existing drafts | Before approval, transition, work start, or implementation |
| `harness-execute-work-order` | Execute and evidence one already-started work order | Modify only the selected `in_progress` work order's declared execution scope | Before marking the work order implemented, Git mutation, assurance, delivery, or external action |
| `harness-prepare-assurance` | Prepare one ready commit-bound VREC and its assurance packet | Run the existing verification-record preparation procedure for an exact clean candidate and named preparation actor | Before verification, delivery selection, release, or external action |

The MVP uses one agent. It does not spawn workers or claim that runtime
permissions enforce the engineering boundary. It proves a deterministic,
portable procedure and verifies every helper-controlled effect boundary. Phase
4 remains responsible for autonomy-envelope-backed delegated lifecycle
execution and stronger runtime enforcement.

## Recommended decisions

### D-AEX-P3-01 — retain `harnessctl` as the control plane

Recommendation: skills remain a user-facing procedure layer over public
released-evaluator operations. They consume structured harness results and do
not calculate lifecycle legality, decision roles, gate results, or transition
availability themselves.

`harnessctl` is therefore complementary to skills, not replaced by them.

### D-AEX-P3-02 — explicit activation for every writing skill

Recommendation: `harness-orient` retains its approved implicit read-only
activation. Each new writing skill requires explicit invocation and an exact
target. A natural-language match, tool permission, previous request, or skill
discovery cannot activate a write.

### D-AEX-P3-03 — preserve current decision points

Recommendation: Phase 3 skills do not apply lifecycle transitions.

- Draft preparation stops before definition or work-order approval.
- Work-order execution begins only when the selected work order is already
  `in_progress`. An `approved` work order produces the existing start decision
  packet and no implementation write.
- Work-order execution stops after evidence and handoff checks, before the
  engineering-owner completion decision.
- Assurance preparation requires an explicit request naming the preparation
  actor, produces only a `ready` VREC, and stops before assurance verification.
- Commit, push, merge, tag, publish, deploy, credentials, and other external
  actions remain separately authorized actions outside the skills.

This gives the operator an outcome-oriented path without prematurely applying
the Phase 4 advance-delegation model.

### D-AEX-P3-04 — add a mutation-aware skill contract without changing v1

Recommendation: preserve the exact `se-harness-skill-contract-v1` behavior and
`harness-orient` digest. Add `se-harness-skill-contract-v2` for the three new
skills. The v2 contract declares explicit activation, inputs, current-state
preconditions, mutation class, checkpoint operations, effect boundary, path
source, retained evidence, outputs, stops, and single-agent fallback.

An older parser must reject v2 as unsupported. It must not reinterpret it as
v1. The installer and distribution carry each canonical skill exactly once.

### D-AEX-P3-05 — recheck immediately around effects

Recommendation: every writing skill first validates the exact released
evaluator, installed integrity, formal graph, selected artifact, and applicable
workflow checkpoint. It builds an explicit effect plan and resolves each target
against the declared path source. Immediately before a helper-controlled
effect it repeats the required current-state and identity checks. After the
effect it compares actual changed paths and reruns applicable validation.

Failure, stale state, ambiguous scope, or an unexpected changed path stops the
skill. The skill must not silently widen scope or repair an unrelated path.

### D-AEX-P3-06 — one structured result and one receipt per invocation

Recommendation: each skill emits one structured result compatible with the
existing lifecycle restitution semantics and one
`se-harness-execution-receipt-v1` identity. Read-only and draft-preparation
receipts may remain inline. Work-order execution retains evidence only at the
work-order-declared evidence path. Assurance preparation binds the created VREC
and exact candidate without treating either as an assurance decision.

### D-AEX-P3-07 — use existing mutation commands

Recommendation: draft creation uses the released evaluator's existing
`create-artifact` or `scaffold-domain` operation. VREC preparation uses the
existing `capture-verification` operation. Work-order implementation continues
to use repository tools inside the already-started work order's declared path
scope. No new lifecycle state, decision right, transition, quality gate, or
general workflow command is added for the MVP.

### D-AEX-P3-08 — require commit-bound verification

Recommendation: `WO-AEX-003` requires commit-bound independent verification.
The work changes managed installed skills, trusted helper scripts, strict skill
contracts, installer behavior, and release packaging. Later users will rely on
the exact distributed bytes at decision boundaries.

## Why a new verification contract is required

`REQ-AEX-008` is a new observable obligation. `VER-AEX-001` verifies
`REQ-AEX-001` through `REQ-AEX-007` and cannot be edited as though its already
approved lifecycle decision covered a later requirement. Traceability requires
selected active verification coverage for every requirement selected by a work
order. Draft `VER-AEX-002` therefore defines the narrow Phase 3 delta while
reusing, rather than copying, applicable `VER-AEX-001` methods.

## Proposed implementation surface

The draft work order authorizes only:

- the strict portable skill-contract parser and installer/package surfaces
  needed to distribute the three new canonical skill cores;
- the three canonical skill directories and their bounded scripts;
- deterministic fixtures and tests for activation, state checks, path scope,
  command equivalence, receipts, installation, upgrade, and distribution;
- operator documentation and work-order-keyed evidence.

It excludes managed workflow and quality-gate files, lifecycle transitions,
autonomy-envelope effect admission, subagents, runtime adapters, commits,
network activity, credentials, releases, and other external actions.

## Exit criteria

Phase 3 is complete only when commit-bound independent evidence shows:

- all four skills install once from canonical provider-neutral sources;
- the three new skills work through a single-agent procedure;
- explicit activation and current-state checks prevent unintended effects;
- skill and command paths have equivalent governed lifecycle effects and stops;
- no skill applies an approval, work completion, verification, release, or
  external action;
- hostile inputs and helper-controlled mutation-boundary tests fail before the
  effect callback;
- retained evidence and receipts are complete and deterministic; and
- the representative workflow reduces procedural prompts without omitting an
  accountable decision.

## Human decision point

The five formal artifacts are ready for accountable content review, not
approval. The recommended next response is:

```text
Begin accountable content review of draft REQ-AEX-008, SPEC-AEX-004,
ADR-AEX-004, VER-AEX-002, and WO-AEX-003. Keep every artifact draft; do not
apply transitions, start implementation, or perform Git, network, or external
actions.
```
