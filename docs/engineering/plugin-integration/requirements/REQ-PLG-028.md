+++
id = "REQ-PLG-028"
type = "requirement"
title = "Transfer repository skill ownership explicitly"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-12"
updated = "2026-09-12"
statement = "WHEN an operator applies a reviewed skill migration, THE EVALUATOR SHALL transfer only the selected unchanged managed skill files to a validated plugin ownership binding."
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
reason = "The operator selected the reviewed WO-PLG-020 packet and execution delegation on 2026-09-12 with \"take the delegated route\", then approved its supplemental DEC-PLG-007 reconciliation and amendments with \"i approve DEC-PLG-007\u2019s `narrow-schema4-exception` with amendements\". Record only REQ-PLG-028 approval as requirements-steward. The reviewed packet at 2d32b57bcdf805a83d5902fb37a3d2b7580c16e0 supplies the selected scope, eight applicability amendments, and candidate policy text. Implementation, assurance, release, and integration results are not recorded by this approval."
+++

# Requirement: Transfer repository skill ownership explicitly

## In plain words

An operator can switch the retained skills to an identified plugin through one reviewed operation.

## Why

Manual deletion loses ownership evidence and can leave duplicate discovery routes.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| An operator applies an unchanged reviewed migration. | Transfer the selected owned files and their ownership records together. | Preserve the target when ownership or content differs. |

## Examples

### Normal

**Given** the retained files match their ownership records, **when** the reviewed migration is applied, **then** the plugin owns the selected route and the old copies are absent.

### Failure

**Given** one selected file contains a local customization, **when** migration is requested, **then** the target is preserved and the conflict is reported.
