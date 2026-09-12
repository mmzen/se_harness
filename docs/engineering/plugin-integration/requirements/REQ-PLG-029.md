+++
id = "REQ-PLG-029"
type = "requirement"
title = "Preserve selected ownership through integrity checks and upgrades"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-12"
updated = "2026-09-12"
statement = "WHILE a repository uses plugin-owned skills, THE EVALUATOR SHALL preserve its recorded ownership selection during integrity checks and ordinary upgrades."
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
reason = "The operator selected the reviewed WO-PLG-020 packet and execution delegation on 2026-09-12 with \"take the delegated route\", then approved its supplemental DEC-PLG-007 reconciliation and amendments with \"i approve DEC-PLG-007\u2019s `narrow-schema4-exception` with amendements\". Record only REQ-PLG-029 approval as requirements-steward. The reviewed packet at 2d32b57bcdf805a83d5902fb37a3d2b7580c16e0 supplies the selected scope, eight applicability amendments, and candidate policy text. Implementation, assurance, release, and integration results are not recorded by this approval."
+++

# Requirement: Preserve selected ownership through integrity checks and upgrades

## In plain words

Integrity checks understand which retained skills come from the plugin. Routine upgrades keep that choice.

## Why

A routine upgrade must not silently restore a second copy of a selected skill.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| An integrity check or ordinary upgrade reads a plugin-owned repository. | Validate the recorded selection and preserve it. | Report an invalid selection without replacing it. |

## Examples

### Normal

**Given** a valid plugin ownership record, **when** an ordinary upgrade is planned, **then** the plan keeps the recorded ownership choice.

### Failure

**Given** a repository copy reappears for a plugin-owned skill, **when** integrity is checked, **then** the duplicate is reported.
