+++
id = "REQ-DST-060"
type = "requirement"
title = "Keep explanatory documentation synchronized with authoritative repository state"
status = "approved"
owners = ["product-owner", "documentation-owner", "quality-owner"]
created = "2026-08-19"
updated = "2026-08-19"
statement = "WHEN public or repository-owned explanatory documentation describes current behavior, navigation, lifecycle coverage, or self-hosting identity, THE SYSTEM SHALL agree with the active implementation, formal records, and exact selected governor."
verification_method = "automated-consistency-checks-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Keep explanatory documentation synchronized with authoritative repository state

## Rationale

The documentation audit found four bounded forms of current-state drift: one obsolete public limitation, missing engineering-index entries, an obsolete self-hosting governor description, and domain summaries that still describe completed assurance as pending. These statements can misdirect readers even though the formal graph and implementation are valid.

## Preconditions and trigger

This requirement applies when non-authoritative public guidance or repository-owned indexes make a present-tense factual claim that can be checked against implementation, configuration, or formal artifact metadata.

## Required response

- Remove claims that contradict current executable behavior or managed authoring guidance.
- Keep repository navigation indexes complete for current engineering domains and release packets.
- Derive self-hosting identity statements from the exact selected governor descriptor.
- Describe lifecycle coverage using the applicable VREC and RLS records without changing those records.
- Keep focused documentation tests aligned with the corrected statements.

## Failure and boundary behavior

When sources disagree, stop and report the discrepancy instead of choosing the most convenient statement. Explanatory documentation must not rewrite historical artifacts, invent authority, transition lifecycle state, or treat derived inspection as a human decision.

## Constraints

The correction is documentation and focused regression coverage only. It does not authorize CLI, validator, template, workflow, package-version, governor-selection, release, publication, deployment, or historical-artifact changes.

## Acceptance examples

### Example: obsolete implementation limitation

**Given** the validator and work-order template permit omission of an inapplicable architecture relation

**When** the public README describes current limitations

**Then** it does not claim that the validator always requires that relation.

### Example: stale lifecycle narrative

**Given** an explanatory domain index says assurance remains pending

**When** an authoritative verified VREC now covers that work

**Then** the index reports the verified coverage while preserving the historical sequence and separate release boundary.

## Open decisions

None. On 2026-08-19, the accountable owner approved the packet then identified as `REQ-DST-060`, `SPEC-DST-017`, `VER-DST-017`, and `WO-DOC-013` for implementation, accepting the four audited priority groups and their focused tests as the complete bounded scope. After current `main` independently assigned the two `017` identifiers to the Explorer dashboard packet, the owner explicitly approved renumbering this specification and verification contract to `SPEC-DST-018` and `VER-DST-018` without changing the requirement or scope.
