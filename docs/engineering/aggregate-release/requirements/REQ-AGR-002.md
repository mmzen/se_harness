+++
id = "REQ-AGR-002"
type = "requirement"
title = "Prepare an aggregate release manifest"
status = "implemented"
owners = ["release-owner", "requirements-steward"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a release is prepared from aggregate verification, THE SYSTEM SHALL create one ready release record that explicitly enumerates all included verification records and all release-bearing work orders covered by them."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AGR-001"]
+++

# Requirement: Prepare an aggregate release manifest

Every released work order must be gated by the selected release contract. The released-work set must equal the union of work covered by the included verification records so the manifest neither omits verified release scope nor claims unverified work.
