+++
id = "REQ-PLG-031"
type = "requirement"
title = "Bind external skill content without executing it"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-12"
updated = "2026-09-12"
statement = "WHEN a plugin is selected for ownership migration, THE EVALUATOR SHALL validate its explicit identity and bounded content inventory without executing plugin content."
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
reason = "The operator selected the reviewed WO-PLG-020 packet and execution delegation on 2026-09-12 with \"take the delegated route\", then approved its supplemental DEC-PLG-007 reconciliation and amendments with \"i approve DEC-PLG-007\u2019s `narrow-schema4-exception` with amendements\". Record only REQ-PLG-031 approval as requirements-steward. The reviewed packet at 2d32b57bcdf805a83d5902fb37a3d2b7580c16e0 supplies the selected scope, eight applicability amendments, and candidate policy text. Implementation, assurance, release, and integration results are not recorded by this approval."
+++

# Requirement: Bind external skill content without executing it

## In plain words

The evaluator checks the selected plugin as data before trusting its ownership claim.

## Why

A plugin directory can be changed, incomplete, ambiguous, or supplied by an untrusted source.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| An operator selects a plugin for migration. | Check the independently selected identity and complete bounded inventory. | Refuse a mismatched or unsafe input before changing the repository. |

## Examples

### Normal

**Given** an explicitly selected identity and matching plugin files, **when** the evaluator inspects the plugin, **then** its content is checked without running it.

### Failure

**Given** the plugin manifest changes after review, **when** application is attempted, **then** the operation refuses the stale input.
