+++
id = "REQ-HUP-005"
type = "requirement"
title = "Apply one bounded schema-3 standard-root transaction"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "WHEN exact public se-harness 0.6.0 is authorized to replace the schema-2 root, THE SYSTEM SHALL require one approved evaluator-upgrade work order bound to the prior lock and target evaluator, apply only the reviewed standard-root plan atomically, retain canonical evidence, and fail closed on customization, plan drift, or postcondition failure."
verification_method = "automated-test"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T17:17:09Z"
decided_by = "repository-owner"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Apply one bounded schema-3 standard-root transaction

## Required response

- Bind the transaction to prior lock SHA-256 `c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af`.
- Require approved or in-progress `WO-HUP-002` and its exact `[evaluator_upgrade]` packet.
- Preserve the three post-release migration LF rules by placing them outside the 0.6.0-managed `.gitattributes` block without changing their semantics.
- Apply only the public evaluator's reviewed managed changes and transactional schema-3 lock.
- Write canonical `WO-HUP-002` evaluator-upgrade evidence and require a no-op replay.

## Failure behavior

Unexpected paths, customized managed bytes after the integration adjustment, identity drift, partial output, evidence collision, lock mismatch, or non-no-op replay stops the transaction and restores the pre-write snapshot where supported.
