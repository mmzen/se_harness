+++
id = "REQ-PLG-014"
type = "requirement"
title = "Explicit limits of hook coverage"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "IF an action cannot be reliably mapped from its host event, THEN THE TOOL HANDLER SHALL report unavailable coverage without presenting the action as governance-checked."
verification_method = ["test"]
priority = "must"
source = "PR #360 at 9e894e99; plugin implementation request, 2026-09-08"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Explicit limits of hook coverage

## In plain words

An unsupported tool, ambiguous command or malformed event is a visible gap. It must not receive a reassuring success message just because the hook ran.

## Why

A host hook does not observe every possible route to an effect. Treating an unknown action as checked would disguise that limit and weaken the authorization boundary. Existing external controls remain necessary for privileged effects.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| An event is malformed, ambiguous or outside the supported action mapping. | Identify the coverage limitation; do not claim a successful governance check. | Block affected governed automation where the host can refuse; otherwise report the unenforced route. |

## Examples

### Normal

**Given** a documented supported edit event containing all required fields,

**When** the handler examines it,

**Then** the action reaches the applicable evaluator check rather than the unsupported route.

### Failure

**Given** a governed shell action whose effective writes cannot be determined reliably,

**When** the handler receives it,

**Then** it refuses the action before effect where the host supports refusal; otherwise it identifies the unenforced route. Neither outcome claims a successful governance check.
