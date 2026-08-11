+++
id = "REQ-REV-005"
type = "requirement"
title = "Prepare provenance records without granting authority"
status = "implemented"
owners = ["quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN capture-verification or prepare-release is invoked, THE SYSTEM SHALL derive bounded Git metadata and create a reviewable ready record without committing, tagging, approving, releasing, or publishing it."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-REV-001"]
+++

# Requirement

The commands fail closed for an absent HEAD, dirty worktree, unknown artifact ID, unsafe path, existing destination, or commit inconsistency.
