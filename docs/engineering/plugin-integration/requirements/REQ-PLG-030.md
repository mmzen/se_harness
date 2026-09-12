+++
id = "REQ-PLG-030"
type = "requirement"
title = "Recover ownership changes without losing repository content"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-12"
updated = "2026-09-12"
statement = "IF an ownership change fails or its reviewed inputs change, THEN THE EVALUATOR SHALL preserve or restore the previous repository files and ownership records."
verification_method = ["test", "inspection"]
priority = "must"
source = "DEC-PLG-004 supported-migration decision at proposal commit 17382d8e; operator continuation on 2026-09-12"

[relations]
derives_from = ["CAP-DST-001"]
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
