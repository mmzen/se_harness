+++
id = "REQ-IAR-024"
type = "requirement"
title = "Evaluator-owned discovery results"
status = "approved"
owners = ["repository-owner", "technical-owner"]
created = "2026-09-20"
updated = "2026-09-27"
statement = "The evaluator returns sufficient instruction locations and selected formal inputs for its current procedure without making agents derive lifecycle decisions from machine policy files."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Repository owner discussion culminating in the 2026-09-20 instruction-discovery split and request to create its delivery artifacts."

[relations]
derives_from = ["CAP-IAR-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T07:37:39Z"
decided_by = "repository-owner"
reason = "User instruction: so let's start the work orders. Apply the reviewed package under DEC-IAR-001 versioned-successor; selected 0.18.0 governance remains installed until separate release/adoption."
+++

# Evaluator-owned discovery results

## Why

The reading route must remain consistent with the evaluator that owns lifecycle states, legal transitions and next actions.

## Behavior

Results distinguish agent instructions, selected formal artifacts and machine inputs. Procedure and typed-step references resolve to exact file headings. Normal agent reading excludes WORKFLOW.json and QUALITY_GATES.json; the evaluator continues to load and enforce both.

## Acceptance

For every supported returned procedure and typed step, test a valid destination and complete prerequisites. Compare lifecycle results on equivalent valid installations using fixed formal inputs: states, legality, required lifecycle gates, decision rights, effects and next-action arguments remain the same. Separately test the intended changes to instruction ownership and discovery readiness.

## Failure

Unknown procedure references, absent required instructions and incompatible discovery metadata produce an explicit discovery failure; no alternate lifecycle algorithm or success fallback is used.
