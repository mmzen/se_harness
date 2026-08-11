+++
id = "REQ-AGR-007"
type = "requirement"
title = "Preserve release decision boundaries"
status = "implemented"
owners = ["release-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN aggregate provenance is prepared, THE SYSTEM SHALL create only ready review artifacts and SHALL NOT infer release scope, approve verification, authorize release, mutate Git, create tags, build packages, or publish artifacts."
verification_method = "automated-test-and-review"

[relations]
derives_from = ["CAP-AGR-001"]
+++

# Requirement: Preserve release decision boundaries

Product owners explicitly identify release-bearing work. Quality owners transition verification records. Release owners transition release records. Separate authorized operations create tags and publish packages against the declared candidate commit.
