+++
id = "WO-PLG-012"
type = "work_order"
title = "Retained orientation and explicit operator briefing"
status = "in_progress"
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
  "plugins/verity-plane/common/skills/harness-orient/",
  "plugins/verity-plane/common/skills/harness-operator-brief/",
  "tests/plugin_integration/retained-skills/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-012.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-012/",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-009.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-009-evaluator.json",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-020.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-021.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-012.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-012.md",
]

[relations]
implements = ["REQ-PLG-020", "REQ-PLG-021"]
specifications = ["SPEC-PLG-012"]
verification = ["VER-PLG-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T18:20:07Z"
decided_by = "engineering-owner"
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only WO-PLG-012 approval under engineering-owner, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 fad319f2739a2cde999ff0fc614013d64454148d8977aedf26e8d96ada111925. The owner expressly requests [delegation] class execution for WO-PLG-012; approval is the delegating act for DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE only. It includes the exact planned VREC and evaluator-sidecar paths in this bounded scope. The class must exist at origin/main and the required live GitHub validate check must succeed for the exact head before the delegated executor acts. No implementation has started. Assurance of implementation, release and PR merge remain separate human decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-10T20:27:42Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at 7fe82c95823503e54d2e35e00d8c409a6dd4b065 (check-run 103035926587, source github-checks)."
+++

# Work Order: Retained orientation and explicit operator briefing

## Lifecycle

The operator selected WO-PLG-012 for the delegated execution route on 2026-09-10. The released evaluator records definition and work-order approval separately. The execution class permits only start, completion and ready-VREC preparation, after this approved work order is present at the configured PR base and the required GitHub check succeeds for the exact candidate. No implementation has started in this definition delivery. Assurance, release and integration remain separate human decisions.

## Objective

Adapt retained orientation and operator-brief cores for plugin installation without changing their invocation or effect contracts.

## In scope

Plugin skill copies, existing helpers/contracts, invocation-path adaptation and preservation tests. Retain this work order's evidence; definition delivery uses only the exact declared artifact paths.


Definition introduction D07 selects this WO and the exact records listed in the [definition-delivery plan](../../../notes/plugin-definition-delivery-2026-09-08.md). Those paths cover draft introduction and separately authorized decisions, not implementation of another WO.

## Out of scope

Root managed skill edits, changed schemas, automatic briefing, lifecycle mutation, or retired outcome skills. No other packet's implementation or managed root changes.

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
