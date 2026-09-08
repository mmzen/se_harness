+++
id = "WO-PLG-010"
type = "work_order"
title = "Implement the bounded change workflow skill"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"

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
+++

# Work Order: Implement the bounded change workflow skill

## Lifecycle

Draft proposal only; no execution or delegation is authorized. Approval of this WO and its governing chain precedes work; later lifecycle decisions follow the installed rules.

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
