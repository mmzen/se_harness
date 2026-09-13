+++
id = "REQ-PLG-034"
type = "requirement"
title = "Preserve a portable plugin choice"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-13"
updated = "2026-09-13"

statement = "WHILE plugin ownership is selected, THE INSTALLER SHALL keep repository skill copies absent during ordinary upgrades without requiring local plugin files."
verification_method = ["test", "inspection"]
priority = "must"
source = "Owner acceptance on 2026-09-13 of the plugin simplification proposal; retained under WO-PLG-021 governance evidence."

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T06:30:56Z"
decided_by = "requirements-steward"
reason = "The owner accepted the complete plugin simplification proposal on 2026-09-13 and requested its artifact packet and work order through the delegated route: \"i accept this proposal, let's go you can create the artifact packet and work order (delegated route)\". Record the requirements-steward approval of REQ-PLG-034 for that accepted scope, including explicit checks instead of blocking hooks and SPEC-PLG-021's applicability table. The retained proposal and 50-scenario coverage map identify the accepted behavior. This approves a definition or the bounded execution delegation only; it records no implementation start, completion, verification result, release, merge, publication or live adoption."
+++

# Requirement: Preserve a portable plugin choice

## In plain words

The project remembers that its skills come from the plugin. A clone can be checked without installing that plugin.

## Why

An upgrade must not recreate duplicate skills. Plugin updates must not require new fingerprints in every project.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A plugin-owned project is checked or upgraded. | Use its provider choice to exclude the old skill inventory. | Report malformed lock data through the normal diagnostics. |

## Examples

### Normal

**Given** the project is cloned without the plugin. **When** the checker reads its valid lock. **Then** the provider choice remains usable.

### Failure

**Given** the lock names an unknown provider. **When** the installer reads it. **Then** the installer reports the invalid provider.
