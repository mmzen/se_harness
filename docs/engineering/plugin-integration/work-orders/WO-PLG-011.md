+++
id = "WO-PLG-011"
type = "work_order"
title = "Evidence skill using existing lifecycle procedures"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"
[assurance]
commit_bound_verification = "required"
rationale = "Later decisions rely on changed plugin behavior or trusted guidance; assurance must bind the exact candidate."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "plugins/verity-plane/common/skills/evidence/",
  "tests/plugin_integration/evidence-skill/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-011.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-011/",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-019.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-011.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-011.md",
]

[relations]
implements = ["REQ-PLG-019"]
specifications = ["SPEC-PLG-011"]
verification = ["VER-PLG-011"]
+++

# Work Order: Evidence skill using existing lifecycle procedures

## Lifecycle

Draft proposal; classification and scope await approval. Start, completion, preparation, assurance and integration remain separate accountable decisions. No delegation is proposed.

## Objective

Implement evidence-skill instructions over existing lifecycle commands, retaining truthful results and decision boundaries.

## In scope

Skill instructions and references; evidence, verification-preparation, release-preparation and refusal tests. Retain this work order's evidence; definition delivery uses only the exact declared artifact paths.


Definition introduction D06 selects this WO and the exact records listed in the [definition-delivery plan](../../../notes/plugin-definition-delivery-2026-09-08.md). Those paths cover draft introduction and separately authorized decisions, not implementation of another WO.

## Out of scope

New evaluator commands, changed gates, assurance decisions, automatic merge/publication, and release builds. No other packet's implementation or managed root changes.

## Authorized decision envelope

After approval, choose names, fixtures and wording within SPEC-PLG-011. Scope, acceptance criteria and decision ownership remain accountable-owner decisions.

## Constraints

Use setup's verified evaluator invocation. Read the project release procedure before authorized release actions. Keep issue #347 separate.

## Expected change surface

Only declared exact files and component directories. Inspect before editing; coordinate overlapping setup changes.

## Required verification

Execute VER-PLG-011, repository-required checks and Git-derived scope/handoff checks using the governing released evaluator. Record candidate and host versions.

## Evidence to record

Retain inputs, outputs, changed paths, refusals and limitations under `evidence/WO-PLG-011/`. No VREC or RLS is prepared while this work remains draft.

## Stop and escalate conditions

Stop on failed identity, undeclared effects, unsupported required host behavior, unresolved blocking decisions, or scope expansion. Passing checks cannot approve work.

## Completion report format

Report implemented behavior, evidence, material non-effects, limitations and the evaluator's next accountable step. Completion does not decide assurance, merge or publication.
