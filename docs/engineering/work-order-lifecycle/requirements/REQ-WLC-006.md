+++
id = "REQ-WLC-006"
type = "requirement"
title = "Normalize legacy statuses without changing decisions"
status = "implemented"
owners = ["requirements-steward", "repository-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN legacy completed governance work has a misleading approved or uncovered verified status, THE SYSTEM SHALL normalize only the work-order status to implemented while preserving its scope, evidence, decisions, commits, verification records, and release records."
verification_method = "inspection"

[relations]
derives_from = ["CAP-WLC-001"]
+++

# Requirement: Normalize legacy statuses without changing decisions

## Acceptance criteria

- The five completed publication work orders currently at `approved` become `implemented`.
- The six governance-decision work orders currently at uncovered `verified` become `implemented`.
- Work orders already covered by verified VRECs are unchanged.
- No VREC or RLS captured provenance field or lifecycle state changes.
