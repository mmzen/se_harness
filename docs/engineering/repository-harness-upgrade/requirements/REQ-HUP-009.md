+++
id = "REQ-HUP-009"
type = "requirement"
title = "Keep evaluator-role assertions stable across checkout line endings"
status = "approved"
owners = ["quality-owner", "engineering-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "WHEN tests compare a released root with candidate templates, THE SYSTEM SHALL derive evaluator-role separation from canonical lock integrity, distinct paths and origins, and declared authority, while accepting either canonical-byte convergence or governed candidate drift independently of checkout line endings."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-HUP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T20:22:49Z"
decided_by = "repository-owner"
+++

# Requirement: Keep evaluator-role assertions stable across checkout line endings

## Required behavior

- Canonicalize managed root bytes according to the lock's declared hash mode
  before integrity comparison.
- Require the released root path and candidate template path to remain distinct.
- Do not use raw byte inequality as proof of role, origin, authority, or
  isolation.
- Permit exact canonical convergence immediately after adoption and later
  candidate drift when each side still satisfies its own contract.
- Run the affected assertion on LF and CRLF materializations or equivalent
  deterministic fixtures.

## Preserved negative controls

Wrong root lock digest, wrong managed path, checkout-source governor origin,
and unexpected candidate semantics must continue to fail.
