+++
id = "REQ-ECP-016"
type = "requirement"
title = "Handoff evidence binds a chain-scoped snapshot"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN `check` evaluates `review_evidence_available` for a work order, THE SYSTEM SHALL bind the evidence to a snapshot digest computed over the selected artifact's governing chain and dependencies only."
verification_method = ["test"]
priority = "must"
source = "review section 5, weakness 16; workflow_contract.json:509"

[relations]
derives_from = ["CAP-ECP-001"]
+++

# Requirement: Handoff evidence binds a chain-scoped snapshot

## Rationale

The formal snapshot digest is computed over every artifact, so any merge to
`main` invalidates every branch's handoff evidence (docs/notes/agentic-
execution-review-2026-08.md:266-269; se_harness/workflow_contract.json:509).
`WO-HUP-007` re-bound its evidence twice for edits elsewhere in the tree
(docs/notes/agentic-execution-review-2026-08.md:235-237). Principle 4 of the
target architecture makes concurrency a matter of branches, which requires the
snapshot to be scoped to the governing chain so a merge elsewhere does not
invalidate handoff evidence (docs/notes/agentic-execution-
review-2026-08.md:394-396).

## Behavior

- Trigger: `harnessctl check` evaluates `review_evidence_available` for a work
  order at any checkpoint.
- Response: the expected digest is computed over the canonical bytes of the
  selected work order, every artifact reachable from it through `implements`,
  `specifications`, `architecture`, `verification`, `derives_from`, and
  `decides` relations, and the artifacts those depend on, and nothing else; the
  predicate is `pass` when the evidence header carries that digest.
- On failure: when the chain cannot be resolved (a dangling relation), the
  predicate is `fail` and names the missing artifact; it is never `pass` by a
  whole-tree digest.

## Assumptions and dependencies

- `formal_snapshot_digest` gains a chain scope argument; its whole-tree form
  stays available to the release lanes that bind it today.
- `harnessctl evidence` (REQ-ECP-003) writes this digest, so agent and harness
  compute the same value.
- The dashboard-manifest digest bound by verification records is untouched.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-016.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** `WO-X-004`'s evidence header carries the chain-scoped digest; another
branch then merges a change to `REQ-Y-009`, outside the chain.

**When** `check . --artifact WO-X-004 --checkpoint handoff --from-git
origin/main` runs after rebasing on `main`.

**Then** `review_evidence_available` is `pass` without re-binding.

### Example: failure behavior

**Given** the merge instead amended `SPEC-X-002`, which `WO-X-004` specifies.

**When** the same command runs.

**Then** `review_evidence_available` is `fail`, the corrective names `harnessctl
evidence` for `WO-X-004`, and the result shows the old and expected digests.

## Open decisions

None.
