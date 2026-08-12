+++
id = "REQ-SHB-006"
type = "requirement"
title = "Invalidate promotion when a commit-bound candidate changes"
status = "implemented"
owners = ["requirements-steward", "quality-owner", "release-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN source, managed distribution content, CI behavior, or release payload changes after commit-bound verification or release approval, THE SYSTEM SHALL preserve the prior records as history, block their use for the changed payload, and require a new candidate, verification record, and release decision."
verification_method = "automated-test-and-human-review"

[relations]
derives_from = ["CAP-SHB-001"]
+++

# Requirement: Invalidate promotion when a commit-bound candidate changes

## Required behavior

- Candidate identity is the full commit named by the applicable VREC and RLS.
- Any payload-affecting correction after that commit creates a different candidate, even when the intended version string is unchanged and nothing was externally published.
- The old VREC/RLS commit, snapshot, scope, evidence, status, version, and tag fields are never rewritten to name the correction.
- Tagging, GitHub release creation, PyPI publication, or deployment stops when the selected candidate differs from the record.
- New evidence, aggregate verification, and release approval bind the replacement candidate before promotion.
- Governance explicitly records the pre-publication disposition of the abandoned release decision; automation does not infer supersession or erase it.

## Current application

Closed PR #28 retains `VREC-SEH-003` and `RLS-SEH-003` as facts about candidate `9ba0cec3710167ad4568931747ed5f4e48a63532`. The clean recovery branch excludes those failed governance files. Implementation of this packet changes the payload and therefore requires new aggregate record IDs before tagging or publication.
