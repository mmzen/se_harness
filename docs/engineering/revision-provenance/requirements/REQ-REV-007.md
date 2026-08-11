+++
id = "REQ-REV-007"
type = "requirement"
title = "Avoid self-referential release metadata"
status = "implemented"
owners = ["technical-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN provenance workflow guidance is installed, THE SYSTEM SHALL define a candidate commit followed by a later governance record so no artifact claims the hash of the commit containing itself."
verification_method = "document-review-and-automated-test"

[relations]
derives_from = ["CAP-REV-001"]
+++

# Requirement

The candidate commit is verified and released. A later governance commit may retain the record naming that candidate. A release tag may point to the candidate but is not created by the harness command.
