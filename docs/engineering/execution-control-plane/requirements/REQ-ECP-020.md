+++
id = "REQ-ECP-020"
type = "requirement"
title = "Scope is enforced on the pull request in every lifecycle state"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN the managed workflow runs on a pull-request event, THE SYSTEM SHALL evaluate the selected work order's scope predicates over the pull request's Git difference whatever the work order's lifecycle state, and fail the required check only on a scope violation or an evaluation failure."
verification_method = ["test"]
priority = "must"
source = "issue #255; pull requests #253 and #257, 2026-08-29"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T08:26:59Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-29 by the accountable owner, 'i approve the artifact packet', for the repair of issue #255: a fifth public checkpoint, scope, at which the three scope predicates of QG-G4-IMPLEMENTATION-EVIDENCE are evaluated for a work order in every lifecycle state, and a managed workflow step that runs it on every pull request while keeping the handoff check and the digest comparison for in_progress work orders; ADR-ECP-006 Option B, with the SPEC-ECP-003 amendment record and the ARCH-ECP-001 amendment that follows this approval. Measured before this transition over branch state 6f29e70 carrying unmoved main 1d19d17: validate PASS at 0 errors under the governing 0.9.0 root; start preflight reads the draft signature plus the architecture pincer W018 and W021 that the ADR approval and the ARCH-ECP-001 amendment resolve. Approval of a definition authorizes no work; the work order is approved separately."
+++

# Requirement: Scope is enforced on the pull request in every lifecycle state

## Rationale

`REQ-ECP-006` made the pull-request gate unconditional, and `WO-ECP-003`
implemented it as `check --checkpoint handoff` on every pull request
(`ECP-GTE-001`). The handoff checkpoint exists only for an `in_progress`
work order: the rule the work order's state selects carries the gate that is
evaluated, and only `QG-G4-IMPLEMENTATION-EVIDENCE` declares `handoff`
(`docs/engineering/QUALITY_GATES.json`). Two consequences were measured on
2026-08-29 (issue #255):

- once the pull request carries the completion transition, the evaluator
  refuses the check with `WEX210: gate ... does not apply at checkpoint
  handoff` and the required check is red until merge, for every pull request
  that carries its own completion, verification record, and verification
  (#253 at `1108a0e`, `1c7012d`, `f279d34`; #257 at `bc6cd74` and later);
- while the work order is `draft` or `approved`, the rule selected carries
  no gate at all, so the same check completes with no predicate and scope
  is not enforced on a packet-only pull request.

Both make the gate's verdict a function of lifecycle state rather than of the
diff, which is the opposite of what `REQ-ECP-006` asks for.

## Behavior

- Trigger: the managed workflow runs for a `pull_request` event whose body
  selects a work order, in any lifecycle state of that work order.
- Response: the scope predicates (`QGP-G4I-SCOPE`, `QGP-G4I-COMPLETE`,
  `QGP-G4I-PATHS`) are evaluated over the Git-derived change set and the
  required check fails on any path outside the declared scope; while the
  work order is `in_progress` the full handoff check is evaluated as well
  and a declared `Harness-Restitution` digest is compared with its
  recomputed value; in any other state a declared digest is reported as
  bound at handoff and not recomputed, and never fails the check by itself.
- On failure: an evaluation refusal, a missing trailer, an unresolvable
  base, or an out-of-scope path fails the check naming the cause; a lifecycle
  state by itself never does.

## Assumptions and dependencies

- The evaluator offers a checkpoint at which the scope predicates are
  evaluated for a work order regardless of its state (`SPEC-ECP-009`).
- `REQ-ECP-006`'s `QGP-G4I-PATHS` remains the predicate that fails the
  check; its identifier and evaluator do not change.
- The change to the managed workflow reaches a consumer through
  `upgrade --apply` of the release that carries it (`ECP-GTE-006`).

## Acceptance examples

### Example: normal behavior

**Given** a pull request whose work order is `implemented` with a `verified`
verification record, and whose diff is inside the declared scope.

**When** the managed workflow runs.

**Then** the required check passes.

### Example: failure behavior

**Given** a pull request whose work order is `draft` and whose diff carries a
path outside the declared scope.

**When** the managed workflow runs.

**Then** the required check fails naming that path with `WEX201`.

## Open decisions

None.
