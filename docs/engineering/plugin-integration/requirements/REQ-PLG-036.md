+++
id = "REQ-PLG-036"
type = "requirement"
title = "Use explicit checks during governed work"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-13"
updated = "2026-09-13"

statement = "WHEN governed work begins, THE PLUGIN SHALL invoke the repository-selected checker explicitly without intercepting ordinary editor actions."
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
reason = "The owner accepted the complete plugin simplification proposal on 2026-09-13 and requested its artifact packet and work order through the delegated route: \"i accept this proposal, let's go you can create the artifact packet and work order (delegated route)\". Record the requirements-steward approval of REQ-PLG-036 for that accepted scope, including explicit checks instead of blocking hooks and SPEC-PLG-021's applicability table. The retained proposal and 50-scenario coverage map identify the accepted behavior. This approves a definition or the bounded execution delegation only; it records no implementation start, completion, verification result, release, merge, publication or live adoption."
+++

# Requirement: Use explicit checks during governed work

## In plain words

Read the project instructions and run the checker when starting governed work. Ordinary edits do not trigger blocking hooks.

## Why

This project has one user. Repeating a check around every edit adds delays and complicated host-specific code.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The operator starts or resumes selected governed work. | Read the applicable instructions and use the normal checker workflow. | Report a required checker failure; diagnostic logging alone does not block work. |

## Examples

### Normal

**Given** the host receives a patch update. **When** the operator starts governed work. **Then** the plugin uses the working interface without a version allowlist.

### Failure

**Given** the required checker fails. **When** the plugin checks the selected work. **Then** it reports the failure without claiming success.
