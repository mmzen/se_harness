+++
id = "REQ-PLG-035"
type = "requirement"
title = "Retry ordinary checker setup"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-13"
updated = "2026-09-13"

statement = "WHEN setup is requested, THE PLUGIN SHALL create or repair its private checker environment using the selected evaluator wheel."
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
reason = "The owner accepted the complete plugin simplification proposal on 2026-09-13 and requested its artifact packet and work order through the delegated route: \"i accept this proposal, let's go you can create the artifact packet and work order (delegated route)\". Record the requirements-steward approval of REQ-PLG-035 for that accepted scope, including explicit checks instead of blocking hooks and SPEC-PLG-021's applicability table. The retained proposal and 50-scenario coverage map identify the accepted behavior. This approves a definition or the bounded execution delegation only; it records no implementation start, completion, verification result, release, merge, publication or live adoption."
+++

# Requirement: Retry ordinary checker setup

## In plain words

Setup uses one documented private folder. If installation fails, running setup again repairs that folder.

## Why

A partial environment is a normal installation problem. Requiring a new folder or a separate proof file makes recovery needlessly difficult.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The operator runs setup with the selected wheel and available Python. | Create or reuse the private environment, install the wheel, and run the checker. | Report the actual missing prerequisite or installation error with a retry command. |

## Examples

### Normal

**Given** a previous installation stopped halfway. **When** setup runs again. **Then** the same private environment becomes usable.

### Failure

**Given** Python cannot create an environment. **When** setup runs. **Then** it explains the missing prerequisite.
