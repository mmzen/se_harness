+++
id = "REQ-WLC-002"
type = "requirement"
title = "Terminate governance-only work at implementation"
status = "implemented"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a governance-only work order completes without being selected into a commit-bound verification record, THE SYSTEM SHALL record it as implemented rather than verified."
verification_method = "inspection"

[relations]
derives_from = ["CAP-WLC-001"]
+++

# Requirement: Terminate governance-only work at implementation

## Acceptance criteria

- Verification-transition, publication, and other governance-only work can complete without creating another VREC.
- A governance-only work order may become `verified` only if a distinct verified or released VREC explicitly covers it.
- Release payload remains an explicit selection and does not automatically include governance-only work.
