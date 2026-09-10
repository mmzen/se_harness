+++
id = "WO-PLG-008"
type = "work_order"
title = "Implement supported before-tool evaluator checks"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-10"

[assurance]
commit_bound_verification = "required"
rationale = "Proposed classification: future governed work relies on the correctness of this plugin behavior and its instructions."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "plugins/verity-plane/common/scripts/check-tool-action.py",
  "tests/plugin_integration/tool_action/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-008.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-008/",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-006.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-006-evaluator.json",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-013.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-014.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-008.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-008.md",
]

[relations]
implements = ["REQ-PLG-013", "REQ-PLG-014"]
specifications = ["SPEC-PLG-008"]
verification = ["VER-PLG-008"]
architecture = ["ARCH-PLG-002", "ADR-PLG-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T06:44:41Z"
decided_by = "engineering-owner"
reason = "The operator explicitly approved the reviewed plugin packets and on 2026-09-10 selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\". WO-PLG-007 implementation is delivered separately in draft PR #435; the D04 governing definitions and bounded Windows decisions are present and approved. Record only WO-PLG-008 approve. Completion, VREC preparation, assurance, release and merge remain separate decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-10T06:45:25Z"
decided_by = "engineering-owner"
reason = "The operator explicitly approved the reviewed plugin packets and on 2026-09-10 selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\". WO-PLG-007 implementation is delivered separately in draft PR #435; the D04 governing definitions and bounded Windows decisions are present and approved. Record only WO-PLG-008 start. Completion, VREC preparation, assurance, release and merge remain separate decisions."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-10T16:57:13Z"
decided_by = "engineering-owner"
reason = "On 2026-09-10 the operator replied \"you can mark as implemented\" to the explicit handoff requesting the engineering-owner completion decision for WO-PLG-008. Record only WO-PLG-008 as implemented, accepting its authorized implementation and retained evidence delivered in PR #436 at ea566fa53d08214b31456ab9422fec7f206db9c4. WO-PLG-007 completion, VREC preparation, assurance, release and merge remain separate decisions."
+++

# Work Order: Implement supported before-tool evaluator checks

## Lifecycle

Marked implemented by the engineering owner on 2026-09-10 after the operator accepted the implementation and retained evidence in PR #436. The released evaluator recorded the explicit completion decision. Verification-record preparation, assurance, release and merge remain separate decisions under the installed rules.

## Objective

Map supported host actions to current evaluator checks and return effective refusals before covered effects.

## In scope

One Python tool-event handler, explicit coverage mapping, refusal translation and focused effect-boundary tests.


The [definition-delivery plan](../../../notes/plugin-definition-delivery-2026-09-08.md) introduces this packet in D04 under WO-PLG-007. This WO's definition paths support its own introduction and separately authorized decisions.

## Out of scope

Universal shell analysis, new policy or approval authentication, host registration and independent remote controls from issue #347.

## Authorized decision envelope

After approval, choose adapter parsing and diagnostics within SPEC-PLG-008. Narrow unsupported mappings rather than assuming their effects.

## Constraints

Invoke the verified evaluator with the absolute environment Python and `-I`. Preserve required gates; successful checking confers no additional authority.

## Expected change surface

The new handler, mapping fixtures/tests, this WO and its evidence only.

## Required verification

Satisfy VER-PLG-008 using captured protocol fixtures and the released evaluator after WO-PLG-001/002. Live interception belongs to WO-PLG-005/006 and WO-PLG-015; it does not block this handler's fixture acceptance.

## Evidence to record

Retain captured event, evaluator command/result, refusal output, fixture effects, coverage gaps and typical/slow timing observations. Do not claim live-host enforcement from fixtures.

## Stop and escalate conditions

Stop when inputs cannot map reliably, refusal is not demonstrable, a required check is unavailable or implementation needs changes outside this scope.

## Completion report format

Identify supported routes and explicit gaps, actual effects/tests, evidence, blockers, final state and one next step.
