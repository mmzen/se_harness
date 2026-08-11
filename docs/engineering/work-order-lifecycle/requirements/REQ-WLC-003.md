+++
id = "REQ-WLC-003"
type = "requirement"
title = "Enforce configured commit-bound work verification"
status = "implemented"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN revision_provenance.required_for_verified_work is true, THE SYSTEM SHALL reject every verified or released work order not covered by a verified or released verification record."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WLC-001"]
+++

# Requirement: Enforce configured commit-bound work verification

## Acceptance criteria

- No configuration or `false` preserves compatibility and does not require a VREC.
- A missing VREC fails validation.
- A `ready` or `superseded` VREC does not satisfy the rule.
- A `verified` or `released` VREC covering the exact work order satisfies the rule.
- The diagnostic identifies the uncovered work order.
