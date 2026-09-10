+++
id = "REQ-PLG-009"
type = "requirement"
title = "Activate the shared integration through Claude Code"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-10"
statement = "WHEN a supported Claude Code session activates the plugin, THE CLAUDE ADAPTER SHALL connect discovered skills and supported host events to the selected shared implementation."
verification_method = ["test","inspection","demonstration"]
priority = "must"
source = "Owner-reviewed plugin proposal, PR #360 at 9e894e99; granular implementation request of 2026-09-08."

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T06:11:30Z"
decided_by = "requirements-steward"
reason = "The operator explicitly approved the reviewed plugin packets in this task: \"i approve the packets, i authorize the work\". On 2026-09-10 they selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\" after deciding DEC-PLG-001 and DEC-PLG-002 for the tested Windows activation routes. Record only the named definitions decision for the D04 governing chain or WO-PLG-007, from reviewed proposal 0b42325b. Sibling work-order states, completion, assurance, release and merge remain separate."
+++

# Requirement: Activate the shared integration through Claude Code

## In plain words

Claude Code exposes the shared skills and sends supported events to their handlers. Its integration files do not redefine engineering rules.

## Why

The working activation sequence must remain separate from the common engineering behavior.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Plugin activation on an accepted Claude Code version and platform | Expose shared skills and connect supported events using the accepted compatibility sequence. | Report failed activation or unsupported events without claiming readiness. |

## Examples

### Normal

**Given** a host and platform accepted by the compatibility decision.

**When** the production adapter activates.

**Then** the expected skills and event handlers are observed.

### Failure

**Given** a required handler fails to activate.

**When** readiness is assessed.

**Then** the failure remains visible and governed readiness is not claimed.
