+++
id = "REQ-DST-004"
type = "requirement"
title = "Plan and apply safe managed-file upgrades"
status = "implemented"
owners = ["engineering-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN an upgrade is inspected or applied, THE SYSTEM SHALL classify managed files from retained hashes and preserve files whose managed content was customized."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement

Planning is the default. Applying changes updates only missing or unmodified managed content and reports customized paths for manual reconciliation.

