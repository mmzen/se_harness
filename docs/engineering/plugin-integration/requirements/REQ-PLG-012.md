+++
id = "REQ-PLG-012"
type = "requirement"
title = "Complete governance delivery despite context limits"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-10"
statement = "IF host limits prevent complete governance injection, THEN THE SESSION HANDLER SHALL keep governance context unready until the complete verified content is read through a supported fallback."
verification_method = ["test"]
priority = "must"
source = "PR #360 at 9e894e99; plugin implementation request, 2026-09-08"

[relations]
derives_from = ["CAP-IAR-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T06:11:30Z"
decided_by = "requirements-steward"
reason = "The operator explicitly approved the reviewed plugin packets in this task: \"i approve the packets, i authorize the work\". On 2026-09-10 they selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\" after deciding DEC-PLG-001 and DEC-PLG-002 for the tested Windows activation routes. Record only the named definitions decision for the D04 governing chain or WO-PLG-007, from reviewed proposal 0b42325b. Sibling work-order states, completion, assurance, release and merge remain separate."
+++

# Requirement: Complete governance delivery despite context limits

## In plain words

A short excerpt must never be mistaken for the complete rules. If the host cannot deliver the full text directly, the agent needs a verified way to read everything.

## Why

Hosts differ in how much hook output reaches a conversation. Silent truncation can remove the very rule that requires a stop. The fallback must preserve the same content and readiness boundary, without asking the user to repeat a decision.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Direct context delivery cannot carry all required governance content. | Identify complete verified content for a supported full read before readiness. | Report a delivery blocker if completeness cannot be established. |

## Examples

### Normal

**Given** the host can perform a complete file read but its hook context is too small,

**When** governance delivery exceeds that limit,

**Then** the supported full-read route restores the verified complete content before governed work.

### Failure

**Given** the host truncates both direct output and the available fallback,

**When** context restoration is attempted,

**Then** readiness remains false; a summary is not accepted as a substitute.
