+++
id = "REQ-HUP-006"
type = "requirement"
title = "Prove complete-graph operation after governor adoption"
status = "approved"
owners = ["quality-owner", "repository-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "WHEN the 0.6.0 root candidate is produced, THE SYSTEM SHALL prove exact released-evaluator doctor, integrity, complete-graph validation, inspection, dashboard, workflow, and supported-runtime behavior without a compatibility view, while demonstrating that product, release, tag, publication, deployment, maintenance, and historical governance identities did not change."
verification_method = "automated-test"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T17:17:09Z"
decided_by = "repository-owner"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Prove complete-graph operation after governor adoption

## Required response

- Run exact public 0.6.0 directly against the complete checkout.
- Require zero structure, governance, and policy errors.
- Prove the managed Engineering Harness workflow selects exact 0.6.0.
- Run complete repository tests and changed-surface checks.
- Compare product, release, tag-related repository bytes, and repository-specific publication workflows with the base.

Historical migration fixtures and retained 0.5 evidence remain immutable. Retirement of transitional repository-specific workflows is a separate follow-up, not part of this root-only adoption.
