+++
id = "CAP-LRE-001"
type = "capability"
title = "Declare pre-enforcement released records instead of rewriting or freezing them"
status = "approved"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
derives_from = ["INT-LRE-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:44:00Z"
decided_by = "repository-owner"
+++

# Capability: Declare pre-enforcement released records instead of rewriting or freezing them

## Actor and need

A repository owner adopting schema-3 evaluator-evidence enforcement needs to say,
once and accountably, which of their already-released records predate the rule, so
that validation reports those records as known outstanding debt rather than as
governance errors that stop all work.

They also need to learn this before the upgrade writes anything. Today the
transaction succeeds, the lock moves to schema 3, and the repository discovers on
the next `validate` that it is frozen with no forward path and no clean way back.

## Capability statement

`A repository owner can declare, in the authorizing upgrade work order, the
released release records that predate evaluator-evidence enforcement, and the
harness accepts exactly those records as unbound, reports each one as
outstanding debt, and refuses an upgrade that would leave any undeclared record
enforcing.`

## Boundaries

- The capability applies only to release records whose status is `released` and
  which carry neither evaluator-evidence field. A `ready` record, a partially
  bound record, and a verification record are all outside it.
- The declaration is bounded by the declaring work order's own approval instant.
  A record released after that instant is outside the declaration's reach, so a
  declaration cannot pre-authorize future unbound releases.
- The capability grants no lifecycle authority. It performs no transition, writes
  no record field, and recomputes no digest.
- Evaluator-evidence capture, canonicalization and hashing are unchanged and are
  owned by `CAP-REB-001`.
- The predecessor-bootstrap transition remains owned by `REQ-REB-008` and
  `SPEC-REB-003`. This capability is not an alternative route to it and never
  substitutes for a `ready` record's binding.
- The six-identifier self-hosting compatibility set continues to govern this
  repository's own history. The capability declares its status explicitly and
  closes it to additions; it does not retire or migrate it.
- Operator assertions at run time, environment variables and command-line flags
  are not within the capability. The only input is governed artifact content.

## Outcomes

- One reviewable table in one governed artifact answers "which released records
  predate the binding, and who said so, and when".
- A declaration survives every later upgrade without restatement, because the
  question asked is whether some authoritative work order declares the record,
  not whether the latest one does.
- An undeclared unbound released record stops the upgrade before any write, with
  a message naming the record and the work order that must declare it.
- Every exemption in force produces a maintenance diagnostic, so the debt is
  countable on the dashboard for as long as it exists.
- A malformed, undated or over-reaching declaration is a governance error on the
  declaring work order rather than a silent no-op.

## Candidate requirements

`REQ-LRE-001` defines the declaration, the acceptance conditions, the fail-closed
treatment of a declaration that does not resolve, and the visible-debt
diagnostic. `REQ-LRE-002` defines the pre-apply refusal, so an upgrade that would
freeze the repository never writes.
