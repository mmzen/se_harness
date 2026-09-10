+++
id = "WO-PLG-010"
type = "work_order"
title = "Implement the bounded change workflow skill"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-10"

[delegation]
class = "execution"

[assurance]
commit_bound_verification = "required"
rationale = "Proposed classification: future governed work relies on the correctness of this plugin behavior and its instructions."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "plugins/verity-plane/common/skills/change/",
  "tests/plugin_integration/change_skill/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-010.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-010/",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-007.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-007-evaluator.json",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-017.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-018.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-010.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-010.md",
]

[relations]
implements = ["REQ-PLG-017", "REQ-PLG-018"]
specifications = ["SPEC-PLG-010"]
verification = ["VER-PLG-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T18:12:39Z"
decided_by = "engineering-owner"
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only WO-PLG-010 approval under engineering-owner, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 725d7fa9bc18b1c4d1e329ca1e92d3b7c3825570cb838089e634c7c16241a100. The owner expressly requests [delegation] class execution for WO-PLG-010; approval is the delegating act for DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE only. It includes the exact planned VREC and evaluator-sidecar paths in this bounded scope. The class must exist at origin/main and the required live GitHub validate check must succeed for the exact head before the delegated executor acts. No implementation has started. Assurance of implementation, release and PR merge remain separate human decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-10T18:31:30Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at 9bc323a7bd5bd259b1ba2098b719314091734a20 (check-run 102995269085, source github-checks). Begin the operator-selected change skill implementation within approved scope; execution delegation is now present at origin/main."
+++

# Work Order: Implement the bounded change workflow skill

## Lifecycle

The operator selected WO-PLG-010 for the delegated execution route on 2026-09-10. The released evaluator records definition and work-order approval separately. The execution class permits only start, completion and ready-VREC preparation, after this approved work order is present at the configured PR base and the required GitHub check succeeds for the exact candidate. No implementation has started in this definition delivery. Assurance, release and integration remain separate human decisions.

## Objective

Guide artifact packages and WO execution using current operations, with automatic continuation while actual authority still covers the work.

## In scope

The new change skill and operation references; drafting, amendment, approval/start/completion guidance and focused interaction fixtures.


Definition introduction D05 selects this WO and the exact records listed in the [definition-delivery plan](../../../notes/plugin-definition-delivery-2026-09-08.md). Those paths cover draft introduction and separately authorized decisions, not implementation of another WO.

## Out of scope

New evaluator commands, policy changes, authority stores, optional helper-agent implementation, evidence skill implementation and external merge/publication controls.

## Authorized decision envelope

After approval, choose clear organization and examples within SPEC-PLG-010. Preserve installed authoring, workflow and decision-rights contracts.

## Constraints

Invoke the verified released evaluator directly. Preserve DR-015 boundaries; a next step or actor assertion supplies no approval. Reuse covered decisions without redundant prompts.

## Expected change surface

Only the change skill directory, tests, this WO and its evidence.

## Required verification

Satisfy VER-PLG-010 and applicable repository checks. Fixtures can proceed after runtime setup; real host acceptance requires applicable WO-PLG-005/006 activation.

## Evidence to record

Retain actual command/state transcripts, partial-failure recovery, authorized-continuation prompt counts, scope-stop cases and exact host/runtime identities.

## Stop and escalate conditions

Stop affected work for missing or changed authority, failed gates, unsupported lifecycle operations or a required implementation outside scope.

## Completion report format

Report operations covered, actual test outcomes, prompt observations, evidence, remaining gaps, final state and one next step.
