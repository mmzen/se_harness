+++
id = "ADR-ECP-006"
type = "adr"
title = "A state-independent scope checkpoint for the pull-request gate"
status = "draft"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
decides = ["ARCH-ECP-001"]
+++

# ADR: A state-independent scope checkpoint for the pull-request gate

## Status

Proposed.

## Context

`WO-ECP-003` made the managed pull-request gate run `check --checkpoint
handoff` unconditionally (`ECP-GTE-001`). The handoff checkpoint is bound to
the rule an `in_progress` work order selects; for any other state the
evaluator refuses it, and for `draft` and `approved` the selected rule has
no gate, so the check completes without enforcing anything. Measured on
2026-08-29 on pull requests #253 and #257: green while `in_progress`, red
from the completion transition to the merge, and never enforced on a
packet-only pull request (issue #255). The repository's own way of working
— implementation, completion, verification record and verification on one
branch — is the case that is red.

## Decision drivers

- `REQ-ECP-006`: scope enforced on the diff of every pull request.
- The gate's verdict must depend on the diff, not on lifecycle state.
- `ECP-KRN-009`: gates and predicates declare their checkpoints; the
  evaluator, not the workflow YAML, decides what applies.
- The `Harness-Restitution` digest is a handoff artefact; it cannot be
  recomputed after completion without redefining handoff.
- Consumers receive the change through `upgrade --apply`; the contracts'
  schema identifiers should not move for this.

## Considered options

### Option A: keep handoff, make the workflow step state-aware

The managed step reads the work order's state and skips the check unless
`in_progress`. Consequences: the lane goes green after completion, but scope
is not enforced on the completion, verification or packet-only heads, and
the gate becomes a function of state again, which `REQ-ECP-006` forbids.

### Option B: a `scope` checkpoint evaluating the scope predicates in every state

Add the public checkpoint `scope` to the evaluator; bind it to
`QG-G4-IMPLEMENTATION-EVIDENCE` with only `QGP-G4I-SCOPE`, `QGP-G4I-COMPLETE`
and `QGP-G4I-PATHS` applicable, by per-predicate checkpoint declarations the
contract already admits; the managed step runs the scope check on every
pull request and the handoff check, with the digest comparison, only while
`in_progress`. Consequences: scope is enforced in every state including
`draft`; predicate identifiers and evaluators are unchanged; the handoff
checkpoint keeps its meaning and its retained result; the contracts gain one
checkpoint name and one binding; `SPEC-ECP-003`'s three gate rules are
amended by record.

### Option C: let handoff apply in every state

Declare `handoff` on every gate a work order can select after
`in_progress`. Consequences: the handoff checkpoint would evaluate
assurance-decision and verified-coverage gates that have nothing to do with a
diff, `handoff.json` would be rewritten after completion, and the digest a
pull request declares would change meaning by state.

## Decision

Select Option B (`SPEC-ECP-009`, `ECP-SCP-001` to `ECP-SCP-010`). The
checkpoint set of `harnessctl check` becomes `start`, `pre-action`,
`transition`, `handoff`, `scope`; `harnessctl evidence` keeps four.
`WO-ECP-013` writes the amendment record on `SPEC-ECP-003`.

## Consequences

- Positive: a pull request that carries its own completion and verification
  is green when its diff is inside scope; a packet-only pull request is
  enforced for the first time; `REQ-ECP-006` holds by construction.
- Negative: a fifth checkpoint to document; consumers on an older root keep
  the old step until they upgrade.
- Operational: this repository's own root is 0.9.0, so its managed lane
  keeps the old step until the next root adoption; the pull request of
  `WO-ECP-013` itself is therefore red after completion, by the rule it
  removes, and the evidence says so.
- Security: no new authority; the scope check writes nothing.
- Migration: the contract schema identifiers do not change; the new binding
  and step arrive with `upgrade --apply`.

## Validation

`VER-ECP-009`: per-state checkpoint tests, the template step test, the
contract byte-equality checks, and the hosted reading of the first pull
request governed by the release that carries this change.
