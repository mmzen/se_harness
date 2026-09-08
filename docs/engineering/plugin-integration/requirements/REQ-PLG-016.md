+++
id = "REQ-PLG-016"
type = "requirement"
title = "Unambiguous ownership of discovered skills"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN repository and plugin skills coexist, THE SETUP SKILL SHALL establish one active, ownership-compatible implementation for each duplicated skill before declaring discovery ready."
verification_method = ["test"]
priority = "must"
source = "PR #360 at 9e894e99; plugin implementation request, 2026-09-08"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Unambiguous ownership of discovered skills

## In plain words

The host must not choose unpredictably between repository and plugin copies of the same skill. A migration also must respect ownership of existing files.

## Why

Current repository-local skills are managed and may carry contracts that require their installed locations. Removing them or giving a plugin copy priority is not automatically compatible. DEC-PLG-004 must settle the supported choice before migration implementation proceeds.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Connecting a repository exposes overlapping skill definitions. | Resolve discovery through the approved, supported ownership-compatible route. | Leave files intact and report discovery unready when compatibility remains unresolved. |

## Examples

### Normal

**Given** an approved compatibility choice supported by the released installer and host,

**When** setup connects a repository with duplicate skill names,

**Then** exactly one compatible implementation is active for each name.

### Failure

**Given** a managed repository skill cannot be superseded through a supported route,

**When** setup inspects coexistence,

**Then** it reports the compatibility blocker without deleting or editing the locked copy.
