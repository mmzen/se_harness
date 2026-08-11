+++
id = "REQ-REV-001"
type = "requirement"
title = "Represent commit-bound verification and release instances"
status = "implemented"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN assurance or release provenance is retained, THE SYSTEM SHALL represent it as formal verification_record and release_record artifacts distinct from reusable verification and release contracts."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-REV-001"]
+++

# Requirement

Verification records use `VREC-` IDs. Release records use `RLS-` IDs. Both participate in the formal artifact graph and lifecycle.
