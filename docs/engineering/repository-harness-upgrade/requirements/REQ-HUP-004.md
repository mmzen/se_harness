+++
id = "REQ-HUP-004"
type = "requirement"
title = "Prove the exact released 0.6.0 evaluator"
status = "approved"
owners = ["repository-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "WHEN the repository plans or applies successor-governor adoption, THE SYSTEM SHALL use an isolated installation of the immutable public se-harness 0.6.0 wheel and prove its version, archive digest, installed payload digest, module root, entry point, and checkout separation before relying on it."
verification_method = "automated-test"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T17:17:09Z"
decided_by = "repository-owner"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Prove the exact released 0.6.0 evaluator

## Rationale

Publication makes the successor eligible for adoption but does not prove which bytes an operator executes. The applying runtime must be the public release rather than current checkout source or a post-release rebuild that still reports version 0.6.0.

## Required response

- Require wheel SHA-256 `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Require installed payload SHA-256 `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.
- Resolve every evaluator origin outside the operational checkout.
- Stop before mutation on any identity, origin, archive, payload, or entry-point mismatch.

## Acceptance examples

An isolated public wheel with matching archive and payload identities passes. Candidate source, a locally reconstructed wheel, an editable install, or an unexpected entry point fails before apply.
