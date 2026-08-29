+++
id = "SPEC-ECP-009"
type = "specification"
title = "The scope checkpoint and the state-independent pull-request gate"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
specifies = ["REQ-ECP-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T08:26:59Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-29 by the accountable owner, 'i approve the artifact packet', for the repair of issue #255: a fifth public checkpoint, scope, at which the three scope predicates of QG-G4-IMPLEMENTATION-EVIDENCE are evaluated for a work order in every lifecycle state, and a managed workflow step that runs it on every pull request while keeping the handoff check and the digest comparison for in_progress work orders; ADR-ECP-006 Option B, with the SPEC-ECP-003 amendment record and the ARCH-ECP-001 amendment that follows this approval. Measured before this transition over branch state 6f29e70 carrying unmoved main 1d19d17: validate PASS at 0 errors under the governing 0.9.0 root; start preflight reads the draft signature plus the architecture pincer W018 and W021 that the ADR approval and the ARCH-ECP-001 amendment resolve. Approval of a definition authorizes no work; the work order is approved separately."
+++

# Specification: The scope checkpoint and the state-independent pull-request gate

## Scope

A fifth public checkpoint, `scope`, at which the evaluator checks a work
order's declared scope against a change set in every lifecycle state, and
the managed workflow step that uses it so that the required check's verdict
depends on the diff and not on where the work order is in its lifecycle
(issue #255). `SPEC-ECP-003` rules `ECP-GTE-001`, `ECP-GTE-002` and
`ECP-GTE-004` are amended by record to refer to this specification. No
lifecycle state, decision right, or digest preimage changes.

## Terms

- **Scope predicates:** `QGP-G4I-SCOPE`, `QGP-G4I-COMPLETE` and
  `QGP-G4I-PATHS` of `QG-G4-IMPLEMENTATION-EVIDENCE`.
- **Scope checkpoint:** the public checkpoint `scope`.

## Behavioral rules

### The scope checkpoint

**ECP-SCP-001:** `scope` is a public checkpoint of `harnessctl check`,
accepted for a work order in any lifecycle state and refused with `WEX210`
for a verification or release record. `harnessctl evidence` does not accept
it: no packet is keyed by it.

**ECP-SCP-002:** At `scope` the evaluator evaluates
`QG-G4-IMPLEMENTATION-EVIDENCE` regardless of the rule the work order's
state selects, and only its scope predicates apply: the gate declares
`scope` among its checkpoints, the three scope predicates declare `scope`
among theirs, and the five other predicates declare exactly the gate's
previous checkpoints (`pre-action`, `transition`, `handoff`), so they are
not evaluated at `scope`. No predicate identifier or evaluator changes.

**ECP-SCP-003:** At `scope` the change set is supplied exactly as at
`handoff` (`--from-git`, typed paths with `--changes-complete`, or a
manifest); without a completeness assertion the scope predicates are
`not_assessable` and the outcome is `blocked`. Repository-level errors block
as at every checkpoint.

**ECP-SCP-004:** A completed `scope` check writes nothing: `handoff.json`
is retained only by the handoff checkpoint. Its `result_sha256` is computed
as `ECP-DIG-001` and `ECP-DIG-002` define, and is not the value a
`Harness-Restitution` line declares.

**ECP-SCP-005:** The rule, procedure and step reported at `scope` are those
the work order's state selects; when the check passes the step is the
procedure's decision step, otherwise the command step that re-runs the
check, as at `handoff`.

### The pull-request gate

**ECP-SCP-006:** On every `pull_request` event the managed workflow runs
`check . --artifact WO --checkpoint scope --from-git BASE-SHA --json` after
fetching `BASE-SHA`, and fails the step when the result's
`operation.outcome` is not `completed` or any `QGP-G4I-PATHS` status is not
`pass`, naming the first path outside scope with `WEX201`.

**ECP-SCP-007:** When the result's `state` reads the work order as
`in_progress`, the step additionally runs `check ... --checkpoint handoff
--from-git BASE-SHA --json`, fails when its outcome is not `completed`, and
compares a declared `Harness-Restitution` line with the recomputed
`result_sha256` as `ADS-DIG-003` requires.

**ECP-SCP-008:** When the work order is in any other state and a
`Harness-Restitution` line is declared, the step logs that the digest was
bound at handoff and is not recomputed after completion, and the line is
neither compared nor a failure; absence of the line is never a failure.

**ECP-SCP-009:** The step keeps `ECP-GTE-003` (the work order comes from
`select-work-order --event`, never from a branch name) and `ECP-GTE-005`
(the released evaluator from the lock, `python -I -m se_harness`).

### Documentation

**ECP-SCP-010:** `docs/engineering/QUALITY_GATES.md`, `WORKFLOW.md`,
`docs/notes/harnessctl-reference.md` and `docs/notes/harnessctl-check.md`
name the five checkpoints, and the check reference's tables show `scope`
against the gate and predicates it evaluates.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-020 | ECP-SCP-001 to ECP-SCP-010 |

## Failure behaviour

Every rule fails closed: an evaluation refusal, an unresolvable base, a
missing trailer, an out-of-scope path, or a non-`completed` outcome of the
scope check fails the required check with a message naming the cause. A
lifecycle state never fails it by itself.

## Compatibility and migration

The contract schema identifiers of `WORKFLOW.json` and `QUALITY_GATES.json`
are unchanged; a consumer receives the new gate binding and the new workflow
step through `upgrade --apply` of the release carrying them. A pull request
opened under a root older than that release keeps the previous behaviour
until the root advances.
