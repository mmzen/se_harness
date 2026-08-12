+++
id = "REQ-SHB-005"
type = "requirement"
title = "Promote a published candidate through a separate governor upgrade"
status = "implemented"
owners = ["requirements-steward", "repository-owner", "release-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN a candidate has been immutably published and selected for self-hosting, THE SYSTEM SHALL advance the operational governor only through a separate governed upgrade that verifies the published artifact and preserves the prior governor as rollback provenance."
verification_method = "automated-test-and-human-review"

[relations]
derives_from = ["CAP-SHB-001"]
+++

# Requirement: Promote a published candidate through a separate governor upgrade

## Required behavior

- Candidate implementation, release approval, external publication, and governor adoption are separate events.
- A host-upgrade work order names the published version, immutable source, wheel hash, prior governor, and target governor.
- The upgrade uses the published artifact rather than checkout source or a local rebuild.
- Transactional plan/apply, customized-content protection, doctor, formal validation, CI identity, and rollback evidence pass before the new governor is accepted.
- The host-upgrade diff is reviewable independently from the candidate implementation and does not rewrite product artifacts or historical VREC/RLS records.
- Until that change is accepted, the previous governor remains authoritative for the repository.

## Failure behavior

Missing publication, hash disagreement, mutable source, failed migration, or host customization stops promotion without partial writes.
