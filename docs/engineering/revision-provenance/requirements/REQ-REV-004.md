+++
id = "REQ-REV-004"
type = "requirement"
title = "Validate typed revision provenance"
status = "implemented"
owners = ["quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the artifact graph is validated, THE SYSTEM SHALL reject malformed revision metadata, unsafe evidence paths, invalid target types, and inconsistent verification-to-release commits deterministically."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-REV-001"]
+++

# Requirement

Commit availability in the local clone is reported separately because shallow clones may not contain historical objects.
