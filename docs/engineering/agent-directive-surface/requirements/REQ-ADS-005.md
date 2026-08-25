+++
id = "REQ-ADS-005"
type = "requirement"
title = "A restitution block carries a recomputable digest"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN `harnessctl check --json` renders a restitution block, THE SYSTEM SHALL include `result_sha256`, the lowercase SHA-256 of the canonical schema-2 block bytes, and WHEN a pull-request body declares `Harness-Restitution: <sha256>`, the managed CI workflow SHALL recompute the block at the same formal snapshot and fail on mismatch."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-ADS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T10:36:12Z"
decided_by = "requirements-steward"
+++

# Requirement: A restitution block carries a recomputable digest

## Rationale

"Return the block verbatim" is the router's strongest behavioural rule and has
no check. A model can hand-type a plausible block. Evidence bindings already
carry the formal-snapshot digest; restitution carries nothing. A digest turns
"verbatim" from an instruction into a predicate, which is what `HRN-004` asks.

## Preconditions and trigger

`check --json` at any checkpoint; the managed CI workflow evaluating a
pull-request event whose body declares the optional trailer.

## Required response

- `se-harness-workflow-result-v2` gains one field `result_sha256`. The digest
  is over the canonical human block rendered from the same result, encoded as
  UTF-8 with LF line endings, without trailing whitespace.
- The pull-request template offers `Harness-Restitution:` beside
  `Harness-Work-Order:`. It is optional in this increment.
- CI, when the trailer is present, runs the bound `check` for the declared
  work order at the checkout's snapshot and compares digests.

## Failure and boundary behavior

An absent trailer is not a failure. A present trailer that does not match is a
failed required check with a diagnostic naming both digests and the snapshot.
A digest never proves that the agent read the block, only that the block it
returned was the tool's.

## Constraints

Schema version stays 2; the field is additive. No change to lifecycle, gates,
or decision rights.

## Acceptance examples

### Example: normal behavior

**Given** an agent returns the block from `check --json` unchanged and its
digest in the pull-request body

**When** CI runs

**Then** the digest check passes.

### Example: failure behavior

**Given** the body's block has one edited word

**When** CI runs

**Then** the check fails naming the declared and recomputed digests.

## Open decisions

None.
