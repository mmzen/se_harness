+++
id = "REQ-ECP-007"
type = "requirement"
title = "The restitution digest covers the change set and gates"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-28"
statement = "THE SYSTEM SHALL compute `result_sha256` over canonical block bytes that include the sorted changed-path set, the change-set completeness assertion, and every gate predicate status."
verification_method = ["test"]
priority = "must"
source = "se_harness/workflow_result.py:174-207"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Requirement: The restitution digest covers the change set and gates

## Rationale

The `result_sha256` preimage renders restitution fields only, so identical
digests cover different change sets (se_harness/workflow_result.py:174-207;
docs/notes/agentic-execution-review-2026-08.md:209-213). The digest is the only
mechanism binding an agent's stated restitution to a measured snapshot and CI
recomputes it at the pull-request head (docs/notes/complexity-
audit-2026-08.md:337-339), so a preimage that omits the change set proves less
than the restitution line claims. Widening the digest makes the line prove what
was declared (docs/notes/agentic-execution-review-2026-08.md:423-427).

## Behavior

- Trigger: always: any schema-2 result that carries `result_sha256`.
- Response: the digest is SHA-256 over the canonical JSON bytes of a block that
  contains, in addition to the fields it contains today, the sorted changed-path
  set, the boolean completeness assertion, and the ordered list of every gate
  predicate identifier with its `pass`, `fail`, or `not_assessable` status;
  recomputing over the same block on another host yields the same digest.
- On failure: when the change set is unknown, the block records it as absent
  with completeness `false` and the digest still covers that fact; a digest is
  never computed over a partial block.

## Assumptions and dependencies

- Canonical JSON is the single implementation in `json_bytes.py`.
- CI recomputes the digest through the same renderer (REQ-ECP-006).
- Results without a change set (for example `focus`) carry an explicit empty
  set, so the block shape is one.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-007.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** two handoff runs on `WO-X-004` differ only in that the second changed
one more in-scope file.

**When** `result_sha256` is computed for both.

**Then** the two digests differ, and each recomputes identically from its block
on Linux and on Windows.

### Example: failure behavior

**Given** a result block is edited after rendering so that `tests/test_a.py` is
removed from its changed-path set.

**When** CI recomputes `result_sha256` from the edited block at the pull-request
head.

**Then** the recomputed digest differs from the `Harness-Restitution:` line and
the check fails.

## Open decisions

None.
