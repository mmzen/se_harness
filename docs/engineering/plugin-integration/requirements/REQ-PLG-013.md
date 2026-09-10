+++
id = "REQ-PLG-013"
type = "requirement"
title = "Evaluator checks before mapped tool effects"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-10"
statement = "WHEN a supported governed tool action is intercepted, THE TOOL HANDLER SHALL obtain the applicable current evaluator result before permitting its effect."
verification_method = ["test"]
priority = "must"
source = "PR #360 at 9e894e99; plugin implementation request, 2026-09-08"

[relations]
derives_from = ["CAP-WEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T06:11:30Z"
decided_by = "requirements-steward"
reason = "The operator explicitly approved the reviewed plugin packets in this task: \"i approve the packets, i authorize the work\". On 2026-09-10 they selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\" after deciding DEC-PLG-001 and DEC-PLG-002 for the tested Windows activation routes. Record only the named definitions decision for the D04 governing chain or WO-PLG-007, from reviewed proposal 0b42325b. Sibling work-order states, completion, assurance, release and merge remain separate."
+++

# Requirement: Evaluator checks before mapped tool effects

## In plain words

Covered edits and commands pass through the existing evaluator before the host executes them. Installing a hook does not create a second set of workflow rules.

## Why

An instruction to check later cannot prevent an already completed effect. Reusing the evaluator preserves its current scope, checkpoint and lifecycle semantics. The adapter must also translate a failed check into an actual refusal on the declared supported host route.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A tool event matches a declared supported governed action. | Run its applicable existing check using current action inputs before any permission response. | Refuse the covered effect when required checking fails or cannot complete. |

## Examples

### Normal

**Given** a mapped edit within a selected approved work order,

**When** the host emits its before-tool event,

**Then** the current evaluator result determines whether that covered edit may proceed.

### Failure

**Given** a mapped edit outside the work order's scope,

**When** the event is checked,

**Then** the host receives refusal before the edit changes any file.
