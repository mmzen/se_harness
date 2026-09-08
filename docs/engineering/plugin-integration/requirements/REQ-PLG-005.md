+++
id = "REQ-PLG-005"
type = "requirement"
title = "Verify the installed evaluator before governed work"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN an installed evaluator is selected for governed work, THE PLUGIN SHALL establish its exact released identity against the repository's governing lock."
verification_method = ["test","inspection"]
priority = "must"
source = "Owner-reviewed plugin proposal, PR #360 at 9e894e99; granular implementation request of 2026-09-08."

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Verify the installed evaluator before governed work

## In plain words

The plugin checks that the installed tool matches the repository's required release. Similar names or version text are insufficient.

## Why

A source checkout or unrelated installation must not gain the authority of the released checking tool.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Selection for governed work in an installed repository | Use the existing identity checks on the selected external environment and repository lock. | Stop on mismatch, damaged content, or unavailable proof; keep governed state unchanged. |

## Examples

### Normal

**Given** an external installation matching the repository lock.

**When** the plugin selects it for governed work.

**Then** the existing identity check establishes the required identity.

### Failure

**Given** an environment with a different release or changed package files.

**When** the same selection occurs.

**Then** the plugin stops before governed work.
