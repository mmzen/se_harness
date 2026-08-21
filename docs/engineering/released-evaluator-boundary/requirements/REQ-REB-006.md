+++
id = "REQ-REB-006"
type = "requirement"
title = "Expose conflicting draft release chains without granting authority"
status = "approved"
owners = ["requirements-steward", "quality-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN release readiness or repository attention is inspected, THE SYSTEM SHALL report structurally overlapping or conflicting draft and ready governing chains with their affected identities and SHALL NOT select, reject, supersede, or promote any chain automatically."
verification_method = "deterministic-inspection-test-and-human-review"

[relations]
derives_from = ["CAP-REB-001"]
+++

# Requirement: Expose conflicting draft release chains without granting authority

## Rationale

Multiple attempted 0.5.0 chains accumulated and obscured the authoritative path. Early, non-authoritative visibility reduces operator error while preserving every historical fact and human decision boundary.

## Preconditions and trigger

The validator and inspection pipeline has loaded valid formal artifacts and is computing release-readiness attention.

## Required response

- Identify multiple active release records proposing the same version.
- Identify ready verification records that overlap work-order coverage at different commits without a valid explicit supersession relation.
- Identify draft or active release contracts whose gates create competing release proposals for the same selected work when the conflict is structurally provable.
- Report affected IDs, commits or versions where available, source rule, and `automatic = false` guidance.

## Failure and boundary behavior

Unknown semantic intent remains visible as an observation rather than a guessed conflict. The observation never changes lifecycle state, chooses authority, deletes drafts, or blocks unrelated validation unless an existing normative invariant is violated.

## Constraints

- Historical verified, released, superseded, or rejected records are not reopened merely because coverage overlaps.
- Same-commit aggregate coverage that is explicitly related is not a conflict.
- Suggestions name accountable roles but contain no executable mutation command.

## Acceptance examples

### Example: normal behavior

**Given** two ready VRECs at different commits covering the same work with no supersession

**When** inspection runs

**Then** both IDs and commits appear in one deterministic conflict observation with no automatic action.

### Example: failure behavior

**Given** a historical released RLS and a later unrelated release

**When** inspection runs

**Then** it does not label normal release history as a conflict.

## Open decisions

The approved closed structural rule catalog is defined by `SPEC-REB-002`.
