+++
id = "REQ-REV-002"
type = "requirement"
title = "Bind verification to a full clean Git revision"
status = "implemented"
owners = ["quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a verification record becomes active, THE SYSTEM SHALL require a full lowercase SHA-1 or SHA-256 Git commit, clean worktree state, verification timestamp, artifact snapshot SHA-256, and retained evidence paths."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-REV-001"]
+++

# Requirement

Commit abbreviations and dirty source states cannot establish verified provenance. Evidence paths remain repository-relative and contained.
