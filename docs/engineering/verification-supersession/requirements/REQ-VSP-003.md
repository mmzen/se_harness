+++
id = "REQ-VSP-003"
type = "requirement"
title = "Preserve work coverage and prevent cycles"
status = "implemented"
owners = ["quality-owner", "technical-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN one verification record supersedes another, THE SYSTEM SHALL require the successor to cover every work order covered by the superseded record and SHALL reject cyclic supersession lineage."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-VSP-001"]
+++

# Requirement: Preserve work coverage and prevent cycles

## Rationale

Supersession must not silently discard verified scope or create lineage that has no authoritative end.

## Preconditions and trigger

An explicit `superseded_by` edge connects two VRECs.

## Required response

Compare the source and successor `verifies_work_order` sets and require the successor set to be a superset. Traverse supersession edges and reject self-loops and cycles deterministically.

## Failure and boundary behavior

Reject a successor that omits any source work order. Additional successor work is permitted and displayed. Do not infer equivalence from contract names, commits, branch history, or timestamps.

## Constraints

The rule preserves work coverage, not candidate identity: a corrected successor may intentionally name a different commit and additional verification contracts.

## Acceptance examples

`VREC-PMI-001` covers `WO-AGR-001` and `WO-PMI-001`, so it may supersede a record covering only `WO-AGR-001`. The reverse relation is invalid.

## Open decisions

None when approved.
