+++
id = "INT-DLC-001"
type = "intent"
title = "Make a definition's lifecycle status mean exactly one thing"
status = "draft"
owners = ["product-owner", "domain-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
+++

# Intent: Make a definition's lifecycle status mean exactly one thing

## Problem

A definition artifact's `status` field is read today as an answer to three
unrelated questions:

1. **Governing authority.** Does this artifact bind downstream work? This is a
   lifecycle question and the field answers it correctly.
2. **Schema generation.** Was this artifact authored before
   `decision_assessment` existed? `LEGACY_ARCHITECTURE_STATUSES` in
   `scripts/validate_engineering_artifacts.py` infers the answer from status.
3. **Realization.** Has the thing this artifact describes been built? This is
   what `implemented` is trying to say on a definition.

Only the first belongs in a lifecycle field. The second is an authoring fact
that status approximates badly. The third is a claim about the world that the
`WO implemented -> VREC verified at an exact commit -> RLS released` path
already establishes with evidence, a commit binding, and an independent
decider.

Measured on `main` at commit `c189b58`, with the released `0.6.0` evaluator run
from outside the checkout (890 artifacts, 0 errors, 50 maintenance warnings):

| Fact | Value |
|---|---:|
| Definition artifacts | 630 |
| `approved` | 449 |
| `implemented` | 165 |
| `rejected` | 13 |
| `superseded` | 3 |
| `draft` | 0 |
| `approved -> implemented` transitions ever recorded | 0 |
| Definition lifecycle edges ever recorded | `draft -> approved` 181, `approved -> rejected` 6 |
| Definitions carrying no `lifecycle_events` at all | 449 |

The 165 `implemented` definitions are hand-authored terminal statuses. Not one
of them records a decision. The split is two eras of authoring, not two
policies: 158 were created between 2026-08-11 and 2026-08-17, 2 on 08-19, 5 on
08-21, and none since. Every domain created from 2026-08-18 onward is uniformly
`approved`. Only requirements, specifications, and architectures were ever
marked `implemented`; intents, capabilities, ADRs, verification contracts, and
operating contracts are 100% `approved`.

Three further facts make this a defect rather than an untidiness:

- **No decision right grants the transition.** `DECISION_RIGHTS.md` defines
  `DR-DEFINITION-DECIDE` as "Approve or reject" a definition. It has no third
  outcome. `PROC-DEFINITION-COMPLETE` nonetheless offers
  `outcomes = ["implemented", "reject", "stop"]`.
- **No step of the managed procedure performs it.** The eleven-step end-to-end
  procedure in `WORKFLOW.md` goes from approving definitions (steps 2 to 4)
  straight to approving a work order. Marking a definition `implemented`
  appears in no step.
- **The claim cannot stay true.** 86 of the 244 requirements named by a work
  order are named by more than one; `REQ-DST-006` is named by 16. 49 of the 104
  `implemented` requirements are named by more than one work order. Because
  `implemented` is terminal for a definition (`transitions_to: []`,
  `transitionable: false`), a requirement marked `implemented` while fifteen
  further work orders continue to implement it can never be corrected.

Meanwhile the state is not inert. `WFL-DEFINITION-WORK` — the recommendation
that routes an actor to `DR-WO-SELECT` and `QG-G3-WORK-AUTHORIZATION` — selects
definitions whose status is `implemented`. Because nothing ever reaches that
status, the 449 `approved` definitions are permanently routed to
`WFL-DEFINITION-COMPLETE`, whose procedure asks an owner to take a decision no
decision right grants.

## Desired outcomes

- A definition's `status` answers one question: does this artifact govern.
- Whether an architecture predates `decision_assessment` is resolved from an
  explicit declaration that says so, not inferred from a lifecycle value that
  is a 50%-accurate proxy for it.
- Whether a requirement, specification, or architecture has been realized is
  derived from the work orders that name it and the verification records bound
  to those work orders, names the covering commit, and self-corrects when a
  further work order selects the same definition.
- Every definition status past `draft` has a recorded, attributable decision
  behind it, or is explicitly declared as predating that obligation.
- No existing artifact is rewritten, no historical status is normalized, and
  the released-evaluator verdict stays at zero errors throughout.

## Actors and stakeholders

- Product, domain, and technical owners who approve definitions and must know
  what their decision means and what it does not claim.
- The requirements steward, who must be able to see which requirements are
  covered by verified work without reading a stale stored flag.
- Assurance and release owners, whose evidenced realization claims are today
  duplicated, unevidenced, by a definition status.
- Repository owners of consumer repositories that hold pre-contract
  architectures and pre-contract definition statuses and must not be broken.
- Any actor or agent reading `harnessctl transition`, `inspect`, or the Harness
  Explorer and acting on the recommended next step.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Questions answered by a definition's `status` field | 3 | 1 | Every governed change to the field's consumers |
| Reachable definition states that no decision right grants | 1 | 0 | Every workflow-contract conformance run |
| Architecture exemptions resolved from lifecycle status | 14 | 0 | Every validation run |
| Architecture exemptions resolved from an explicit declaration | 0 | 14 | Every validation run |
| Errors introduced into this repository's graph | 0 | 0 | Every released-evaluator validation run |
| Maintenance warnings silently removed by the change | 0 | 0 | Every released-evaluator validation run |
| Existing artifact bytes rewritten to normalize a status | 0 | 0 | Every implementation review |
| Definition statuses past `draft` without a recorded or declared decision | 449 | 0 | Every validation run after the third increment |

## Non-goals

- Normalizing, rewriting, or re-deciding the 165 existing `implemented`
  definitions in either direction.
- Removing `implemented` from the accepted status vocabulary, from the lock,
  from any existing artifact, or from a consumer repository's history.
- Changing the work-order, verification-record, or release-record lifecycles,
  where `implemented`, `verified`, and `released` are evidenced decisions about
  the artifact that carries them.
- Introducing a new role, a new gate, a new artifact type, or a new relation.
- Retiring `constrains` or resolving the 15 `W015` diagnostics, which are
  relation-shape findings and independent of status.
- Automatically approving, transitioning, or migrating anything in this
  repository or in a consumer repository.
- Making realization a stored field under a different name.

## Principles and immutable constraints

- `HRN-001`: artifacts are authority and code is evidence. A realization claim
  that no evidence binds does not belong in an artifact field.
- `HRN-005` and `WFL-004`: only an explicit actor decision and an applied
  transition change lifecycle state. A hand-authored terminal status is
  neither.
- `HRN-006`: related artifact states are never synchronized by inference.
  Nothing in this initiative may make completing a work order move a
  definition.
- A verified record and a released record are never rewritten. Nothing here
  reaches backwards into one.
- Gates fail closed. A new obligation on consumer repositories must arrive with
  an explicit, bounded, declared exemption route, never with a silent pass.
- The status vocabulary in `ALLOWED_STATUSES` and the lock's accepted schema
  strings are compatibility surfaces. Values are retired from reachability, not
  from acceptance.

## Risks and assumptions

- **Risk:** removing the status proxy for architecture generation converts 14
  `W014` maintenance warnings into 14 `E014` errors if the replacing
  declaration is not in place first. The increments must land in order, and the
  first must be provably outcome-neutral before the second is authorized.
- **Risk:** a derived realization signal can be read as an approval. Its output
  must state that it grants nothing and name the accountable decision that
  does.
- **Risk:** requiring a recorded decision past `draft` breaks every consumer
  repository holding pre-contract definitions. The obligation is only safe with
  a bounded declaration and a frozen self-hosting set, on the
  `SPEC-LRE-001` pattern.
- **Risk:** the naming of `WFL-DEFINITION-COMPLETE` becomes misleading once its
  procedure changes. Renaming a published managed identifier is a larger
  compatibility event than the residue; the residue is accepted and disclosed.
- **Assumption:** `approved` already carries `grants_authority: true`, so the
  449 approved definitions lose nothing and the 165 implemented ones keep
  everything.
- **Assumption:** no consumer repository has automation keyed to a definition
  reaching `implemented`, because the transition has never been applied here
  and the state is not reachable through any documented step.
- **Decided 2026-08-26 by the repository owner:** removing an edge from a
  family's `transitions_to` is a within-`se-harness-workflow-v3` retirement. The
  contract's shape does not change, so the version boundary is carried by the
  release version, the governance-migration scenario, and the `implemented` row's
  `predecessor_adapter` rather than by a contract generation. The accepted risk
  is that a consumer pinning `v3` sees reachable behaviour narrow without a
  generation signal.
- **Decided 2026-08-26 by the repository owner:** the pre-contract definition set
  is grandfathered by enumeration in a committed frozen vector, not by a frozen
  cutover date over `created`. `ADR-DLC-002` records the reasoning and the
  rejected alternatives.
- **Decided 2026-08-26 by the repository owner:** all three increments are
  authorized as a path, in the order `WO-DLC-001`, `WO-DLC-002`, `WO-DLC-003`.
  Partial adoption at P1, or at P1 and P2, was considered and declined.
