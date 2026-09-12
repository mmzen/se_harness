+++
id = "REQ-PLG-028"
type = "requirement"
title = "Transfer repository skill ownership explicitly"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-12"
updated = "2026-09-12"
statement = "WHEN an operator applies a reviewed skill migration, THE EVALUATOR SHALL transfer only the selected unchanged managed skill files to a validated plugin ownership binding."
verification_method = ["test", "inspection"]
priority = "must"
source = "DEC-PLG-004 supported-migration decision at proposal commit 17382d8e; operator continuation on 2026-09-12"

[relations]
derives_from = ["CAP-DST-001"]
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
