+++
id = "REQ-REV-006"
type = "requirement"
title = "Expose intent-to-commit lineage and checkout drift"
status = "implemented"
owners = ["product-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the Harness Explorer is generated, THE SYSTEM SHALL display declared verification and release commits in lineage and distinguish them from the observed checkout revision and any exact-match drift state."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-REV-001"]
+++

# Requirement

Requirement selection must traverse through implementing work orders to verification and release records. A checkout mismatch is evidence for review, not automatic proof of failure.
