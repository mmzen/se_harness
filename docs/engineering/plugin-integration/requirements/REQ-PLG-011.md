+++
id = "REQ-PLG-011"
type = "requirement"
title = "Fresh governance after compaction or resume"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN a governed session resumes or restores context after compaction, THE SESSION HANDLER SHALL re-establish governance context from freshly verified repository and runtime state."
verification_method = ["test"]
priority = "must"
source = "PR #360 at 9e894e99; plugin implementation request, 2026-09-08"

[relations]
derives_from = ["CAP-IAR-001"]
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
