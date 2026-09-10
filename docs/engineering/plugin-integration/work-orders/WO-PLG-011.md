+++
id = "WO-PLG-011"
type = "work_order"
title = "Evidence skill using existing lifecycle procedures"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-10"
[delegation]
class = "execution"

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
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-008.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-008-evaluator.json",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-019.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-011.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-011.md",
]

[relations]
implements = ["REQ-PLG-019"]
specifications = ["SPEC-PLG-011"]
verification = ["VER-PLG-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T18:17:14Z"
decided_by = "engineering-owner"
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only WO-PLG-011 approval under engineering-owner, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 9d09c401be4119a0533b7ff5fac66bcbcbb5d1d0c596ae8920aec07c84c447c4. The owner expressly requests [delegation] class execution for WO-PLG-011; approval is the delegating act for DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE only. It includes the exact planned VREC and evaluator-sidecar paths in this bounded scope. The class must exist at origin/main and the required live GitHub validate check must succeed for the exact head before the delegated executor acts. No implementation has started. Assurance of implementation, release and PR merge remain separate human decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-10T19:25:56Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at b319bffd383d010de5b24640a667a61874b9d2ab (check-run 103015218599, source github-checks)."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-10T20:19:17Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-COMPLETE under [delegation] class 'execution': required check 'validate' success at cb5df4da98f98fe73f01336784b95866e1b05683 (check-run 103033194549, source github-checks)."
+++

# Work Order: Evidence skill using existing lifecycle procedures

## Lifecycle

The operator selected WO-PLG-011 for the delegated execution route on 2026-09-10. The released evaluator records definition and work-order approval separately. The execution class permits only start, completion and ready-VREC preparation, after this approved work order is present at the configured PR base and the required GitHub check succeeds for the exact candidate. No implementation has started in this definition delivery. Assurance, release and integration remain separate human decisions.

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
