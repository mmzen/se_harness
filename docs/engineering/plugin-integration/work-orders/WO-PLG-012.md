+++
id = "WO-PLG-012"
type = "work_order"
title = "Retained orientation and explicit operator briefing"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"
[assurance]
commit_bound_verification = "required"
rationale = "Later decisions rely on changed plugin behavior or trusted guidance; assurance must bind the exact candidate."
decided_by = "engineering-owner"

[execution_scope]
paths = ["plugins/verity-plane/common/skills/harness-orient/", "plugins/verity-plane/common/skills/harness-operator-brief/", "tests/plugin_integration/retained-skills/", "docs/engineering/plugin-integration/work-orders/WO-PLG-012.md", "docs/engineering/plugin-integration/evidence/WO-PLG-012/"]

[relations]
implements = ["REQ-PLG-020", "REQ-PLG-021"]
specifications = ["SPEC-PLG-012"]
verification = ["VER-PLG-012"]
+++

# Work Order: Retained orientation and explicit operator briefing

## Lifecycle

Draft proposal; classification and scope await approval. Start, completion, preparation, assurance and integration remain separate accountable decisions. No delegation is proposed.

## Objective

Adapt retained orientation and operator-brief cores for plugin installation without changing their invocation or effect contracts.

## In scope

Plugin skill copies, existing helpers/contracts, invocation-path adaptation and preservation tests. Retain only this work order's evidence and lifecycle metadata within its engineering paths.

## Out of scope

Root managed skill edits, changed schemas, automatic briefing, lifecycle mutation, or retired outcome skills. No other packet or managed root changes.

## Authorized decision envelope

After approval, choose names, fixtures and wording within SPEC-PLG-012. Scope, acceptance criteria and decision ownership remain accountable-owner decisions.

## Constraints

Existing skill contracts supply expected behavior. Live coexistence waits for DEC-PLG-004's supported migration route; fixtures may test isolated copies.

## Expected change surface

Only declared exact files and component directories. Inspect before editing; coordinate overlapping setup changes.

## Required verification

Execute VER-PLG-012, repository-required checks and Git-derived scope/handoff checks using the governing released evaluator. Record candidate and host versions.

## Evidence to record

Retain inputs, outputs, changed paths, refusals and limitations under `evidence/WO-PLG-012/`. No VREC or RLS is prepared while this work remains draft.

## Stop and escalate conditions

Stop on failed identity, undeclared effects, unsupported required host behavior, unresolved blocking decisions, or scope expansion. Passing checks cannot approve work.

## Completion report format

Report implemented behavior, evidence, material non-effects, limitations and the evaluator's next accountable step. Completion does not decide assurance, merge or publication.
