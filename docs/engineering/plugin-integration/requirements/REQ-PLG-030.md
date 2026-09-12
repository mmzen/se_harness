+++
id = "REQ-PLG-030"
type = "requirement"
title = "Recover ownership changes without losing repository content"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-12"
updated = "2026-09-12"
statement = "IF an ownership change fails or its reviewed inputs change, THEN THE EVALUATOR SHALL preserve or restore the previous repository files and ownership records."
verification_method = ["test", "inspection"]
priority = "must"
source = "DEC-PLG-004 supported-migration decision at proposal commit 17382d8e; operator continuation on 2026-09-12"

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-12T12:56:34Z"
decided_by = "requirements-steward"
reason = "The operator selected the reviewed WO-PLG-020 packet and execution delegation on 2026-09-12 with \"take the delegated route\", then approved its supplemental DEC-PLG-007 reconciliation and amendments with \"i approve DEC-PLG-007\u2019s `narrow-schema4-exception` with amendements\". Record only REQ-PLG-030 approval as requirements-steward. The reviewed packet at 2d32b57bcdf805a83d5902fb37a3d2b7580c16e0 supplies the selected scope, eight applicability amendments, and candidate policy text. Implementation, assurance, release, and integration results are not recorded by this approval."
+++

# Requirement: Recover ownership changes without losing repository content

## In plain words

A failed change leaves the previous repository usable. Restoring repository-owned skills uses the same reviewed transaction.

## Why

Removing files and updating their ownership separately can leave an installation inconsistent.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Application fails or the reviewed input changes. | Preserve or restore the previous files and ownership records. | Report incomplete recovery and refuse to claim success. |

## Examples

### Normal

**Given** a plugin-owned repository and a valid restoration plan, **when** restoration succeeds, **then** the retained repository skills and ownership records agree.

### Failure

**Given** a write fails during migration, **when** the operation stops, **then** the previous file bytes and ownership records are restored.
