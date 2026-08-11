+++
id = "REQ-AGR-005"
type = "requirement"
title = "Validate aggregate lifecycle and scope consistency"
status = "implemented"
owners = ["quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the artifact graph is validated, THE SYSTEM SHALL reject aggregate verification and release records with incomplete contract coverage, unequal verified and released work sets, incompatible lifecycle states, or commit disagreement."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AGR-001"]
+++

# Requirement: Validate aggregate lifecycle and scope consistency

A ready release may be prepared for review from ready or verified records, but it cannot transition to `released` unless every included verification record is `verified` or `released`. Validation remains deterministic and reports the specific missing, extra, ungated, inactive, or inconsistent IDs.
