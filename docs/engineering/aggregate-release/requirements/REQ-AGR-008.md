+++
id = "REQ-AGR-008"
type = "requirement"
title = "Upgrade aggregate release support safely"
status = "implemented"
owners = ["engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN an installed harness is upgraded, THE SYSTEM SHALL deliver aggregate release commands, validation, templates, workflow guidance, and Explorer behavior without invalidating existing single-work-order records or overwriting customized files."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AGR-001"]
+++

# Requirement: Upgrade aggregate release support safely

The change must remain within the one standard installation profile, preserve hash-based ownership and repository-owned context, and update both distribution sources and canonical installed-template copies consistently.
