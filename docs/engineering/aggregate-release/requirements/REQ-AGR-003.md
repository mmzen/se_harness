+++
id = "REQ-AGR-003"
type = "requirement"
title = "Bind aggregate assurance to one candidate commit"
status = "implemented"
owners = ["quality-owner", "release-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN aggregate verification or release provenance is active, THE SYSTEM SHALL require all included records to identify the same full Git commit and object format as the final release candidate."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AGR-001"]
+++

# Requirement: Bind aggregate assurance to one candidate commit

An ancestor relationship is insufficient because it does not prove behavior after integration. SHA-1 and SHA-256 repositories remain supported. The candidate commit precedes later governance commits containing its verification and release records.
