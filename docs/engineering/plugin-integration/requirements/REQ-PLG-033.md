+++
id = "REQ-PLG-033"
type = "requirement"
title = "Keep replacement bounded and repeatable"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-13"
updated = "2026-09-13"

statement = "WHEN skill replacement is interrupted, THE MIGRATION COMMAND SHALL allow a repeat operation that finishes within the named repository destinations."
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
reason = "The owner accepted the complete plugin simplification proposal on 2026-09-13 and requested its artifact packet and work order through the delegated route: \"i accept this proposal, let's go you can create the artifact packet and work order (delegated route)\". Record the requirements-steward approval of REQ-PLG-033 for that accepted scope, including explicit checks instead of blocking hooks and SPEC-PLG-021's applicability table. The retained proposal and 50-scenario coverage map identify the accepted behavior. This approves a definition or the bounded execution delegation only; it records no implementation start, completion, verification result, release, merge, publication or live adoption."
+++

# Requirement: Keep replacement bounded and repeatable

## In plain words

Run the same command again after an interruption. It only replaces the selected skill folders inside the chosen project.

## Why

A failed file operation is plausible. A recovery protocol for forged journals and competing editors is unnecessary for this installation.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The operator repeats an interrupted switch or restores repository skills. | Finish replacement and save the provider choice last. | Report the failed path; reject a redirected destination before deletion. |

## Examples

### Normal

**Given** an earlier attempt stopped after deleting one folder. **When** the operator reruns it. **Then** the remaining replacement finishes.

### Failure

**Given** an old skill path points outside the project. **When** replacement starts. **Then** the command refuses that destination.
