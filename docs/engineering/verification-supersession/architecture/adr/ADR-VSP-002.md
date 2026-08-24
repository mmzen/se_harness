+++
id = "ADR-VSP-002"
type = "adr"
title = "State-aware dual-generation verification provenance"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-VSP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:35:25Z"
decided_by = "technical-owner"
+++

# ADR: State-aware dual-generation verification provenance

## Status

Proposed.

## Context

Pre-0.6.0 VRECs used `verified_at` as candidate-capture metadata even while status was ready. Version 0.6.0 corrected preparation semantics by introducing `prepared_at` and reserving `verified_at` for the later assurance decision. The supersession validator still assumes the old field is universally present, so a current record written by 0.6.0 cannot traverse its declared `ready -> superseded` edge.

## Decision drivers

Do not invent a verification decision, preserve immutable historical facts, keep the public lifecycle edge operational, maintain older record validity, avoid repository migrations, use one validator for transition and direct checks, and fail closed for actual verified authority.

## Considered options

1. Add `verified_at` and `verified_by` during supersession. Rejected because it falsely claims that the superseded candidate was verified.
2. Rename every historical `verified_at` capture to `prepared_at`. Rejected because released governance history is immutable and its original schema meaning must remain visible.
3. Make `verified_at` optional in every state. Rejected because current verified records require an explicit decision timestamp and actor.
4. Add a repository-specific exception for affected IDs. Rejected because the defect is in the portable state model and identifier allowlists do not generalize.
5. Select validation semantics from the current preparation-field pair while retaining the legacy no-preparation shape. Selected.

## Decision

For records containing `prepared_at` or `prepared_by`, treat the pair as current capture provenance. Require verification decision fields only when the VREC is actually verified or released; require supersession fields, and prohibit verification decision fields, when it is superseded directly from ready.

For records without preparation fields, preserve the historical contract in which `verified_at` may be candidate-capture metadata. A legacy superseded record retaining that field remains valid without requiring a fabricated `verified_by` or any migration.

The transition mutator remains status-specific and does not synthesize compatibility fields. The packaged validator owns both generation shapes and is used unchanged by direct validation and proposed-final-graph validation.

## Consequences

Current supported VRECs can be superseded accurately, and legacy records remain readable. Validator logic becomes explicitly generation-aware instead of assuming one timestamp meaning. Tests must protect both shapes and prevent future broad relaxation. Consumer roots receive the correction only in a later released evaluator, so candidate development intentionally leaves the current managed root copy unchanged.

No concrete record is disposed by this decision. Rejection, verification, successor eligibility, and active-release protections remain unchanged.

## Validation

Run command-level capture, successor verification, supersession plan/apply, full validation, and inspection tests. Add direct current/legacy metadata matrices, check transition write sets, verify installed-template behavior, run the complete suite, and confirm the released root remains healthy and unmodified.
