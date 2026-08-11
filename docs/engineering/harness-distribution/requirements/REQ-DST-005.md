+++
id = "REQ-DST-005"
type = "requirement"
title = "Keep adoption observations non-authoritative"
status = "implemented"
owners = ["product-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN adopting an existing repository, THE SYSTEM SHALL label detected ecosystems and CI files as observations and SHALL require humans to author and approve product intent and requirements."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement

The adoption report is an inventory and decision checklist, not a formal product artifact. It never infers lifecycle approvals or creates an active requirement chain.

