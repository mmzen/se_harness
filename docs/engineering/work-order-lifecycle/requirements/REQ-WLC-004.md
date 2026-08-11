+++
id = "REQ-WLC-004"
type = "requirement"
title = "Keep validation and Explorer findings non-duplicative"
status = "implemented"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN uncovered verified work is an authoritative validation failure, THE SYSTEM SHALL expose the validator diagnostic in Harness Explorer and SHALL NOT add a duplicate derived W-REV-001 finding."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WLC-001"]
+++

# Requirement: Keep validation and Explorer findings non-duplicative

## Acceptance criteria

- Harness Explorer reuses the validator report.
- `W-REV-001` is no longer emitted.
- Other derived findings, including stale-ready supersession review, remain non-authoritative and unchanged.
