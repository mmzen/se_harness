+++
id = "REQ-REV-008"
type = "requirement"
title = "Migrate existing installations safely"
status = "implemented"
owners = ["engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN an existing harness installation upgrades, THE SYSTEM SHALL add revision-record templates and schema documentation without invalidating existing artifact types or overwriting customized managed files."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-REV-001"]
+++

# Requirement

Existing work orders and release contracts remain valid. Commit-bound records become required only when a repository adopts schema version 2 and uses the new verified or released instance workflow.
