+++
id = "REQ-AGR-006"
type = "requirement"
title = "Expose aggregate release lineage"
status = "implemented"
owners = ["product-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the Harness Explorer renders aggregate provenance, THE SYSTEM SHALL show one release version and candidate commit connected to every included verification record, work order, requirement, capability, and intent."
verification_method = "automated-test-and-visual-review"

[relations]
derives_from = ["CAP-AGR-001"]
+++

# Requirement: Expose aggregate release lineage

The Explorer must distinguish release payload work from governance-only activity and retain the existing distinction between declared candidate provenance and the observed checkout. Each affected work-order readiness view must identify the shared release record.
