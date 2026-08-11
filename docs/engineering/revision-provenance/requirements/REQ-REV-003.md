+++
id = "REQ-REV-003"
type = "requirement"
title = "Bind a release instance to verified work"
status = "implemented"
owners = ["release-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a release record becomes active, THE SYSTEM SHALL require a version, full commit, release timestamp, authorizing owner, release contract, verification record, and released work order whose declared commits agree."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-REV-001"]
+++

# Requirement

A release record is an immutable instance of a release decision. Its commit must equal every included verification record commit.
