+++
id = "REQ-PLG-011"
type = "requirement"
title = "Fresh governance after compaction or resume"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-10"
statement = "WHEN a governed session resumes or restores context after compaction, THE SESSION HANDLER SHALL re-establish governance context from freshly verified repository and runtime state."
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

# Requirement: Fresh governance after compaction or resume

## In plain words

A resumed conversation must use the governance instructions that apply now. The earlier session's successful check is not enough after its context or underlying installation changes.

## Why

Compaction can remove instructions, and an inactive session can outlive changes to its repository or environment. Reusing stale readiness would hide these changes. This requirement uses the same readiness boundary as session start rather than a separate policy.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A supported resume or post-compaction context-restoration event occurs. | Recheck current inputs and restore the applicable governance context. | Keep context unready and identify the changed or unavailable prerequisite. |

## Examples

### Normal

**Given** an intact installation and a previously ready session,

**When** the host resumes that session,

**Then** fresh verification precedes restored governance context.

### Failure

**Given** the environment was removed while the session was inactive,

**When** the session resumes,

**Then** the host-shell guard reports setup required because the Python handler cannot run. Earlier success cannot establish current readiness.
