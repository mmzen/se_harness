+++
id = "REQ-PLG-032"
type = "requirement"
title = "Replace disposable repository skills"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-13"
updated = "2026-09-13"

statement = "WHEN the operator selects the plugin, THE MIGRATION COMMAND SHALL replace the named repository skill copies regardless of edits, extra contents, or missing files."
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
reason = "The owner accepted the complete plugin simplification proposal on 2026-09-13 and requested its artifact packet and work order through the delegated route: \"i accept this proposal, let's go you can create the artifact packet and work order (delegated route)\". Record the requirements-steward approval of REQ-PLG-032 for that accepted scope, including explicit checks instead of blocking hooks and SPEC-PLG-021's applicability table. The retained proposal and 50-scenario coverage map identify the accepted behavior. This approves a definition or the bounded execution delegation only; it records no implementation start, completion, verification result, release, merge, publication or live adoption."
+++

# Requirement: Replace disposable repository skills

## In plain words

Switching to the plugin removes the old copies. Changes inside those old skill folders are disposable.

## Why

The owner has one development installation and explicitly chose replacement. Preserving edits to generated skills adds work without useful protection.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The operator applies the switch with a complete plugin. | Remove the four named old skill folders and their managed entries. | Report an invalid replacement before deletion. |

## Examples

### Normal

**Given** old copies include local edits. **When** the operator applies the switch. **Then** those copies disappear.

### Failure

**Given** a required replacement file is missing. **When** the operator requests the switch. **Then** the command reports the missing file before deletion.
