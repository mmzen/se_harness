+++
id = "REQ-DST-003"
type = "requirement"
title = "Operate validation, visualization, and diagnostics locally"
status = "implemented"
owners = ["engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a harness-enabled repository is selected, THE SYSTEM SHALL expose validate, dashboard, and doctor commands with the underlying command exit status preserved."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement

The commands use the installed repository scripts, allowing CI and humans to invoke the same validator and deterministic dashboard generator.

