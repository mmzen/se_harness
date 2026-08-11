+++
id = "REQ-DST-001"
type = "requirement"
title = "Provide exactly one standard installation"
status = "implemented"
owners = ["product-owner", "engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a user initializes, adopts, or upgrades the harness, THE SYSTEM SHALL use exactly one complete standard template without a minimal, offline, or other selectable profile."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement

Every target receives the same validator, dashboard, artifact templates, workflow documentation, agent integration, and CI definition. The CLI exposes no profile option and the canonical template tree contains no profile variants.

