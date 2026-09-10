+++
id = "WO-PLG-007"
type = "work_order"
title = "Implement verified session governance delivery"
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
  "plugins/verity-plane/common/scripts/session-context.py",
  "tests/plugin_integration/session_context/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-007.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-007/",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/architecture/ARCH-PLG-002.md",
  "docs/engineering/plugin-integration/architecture/adr/ADR-PLG-002.md",
  "docs/engineering/plugin-integration/decisions/DEC-PLG-001.md",
  "docs/engineering/plugin-integration/decisions/DEC-PLG-002.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-008.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-009.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-010.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-011.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-012.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-013.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-014.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-024.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-005.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-006.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-007.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-008.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-014.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-005.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-006.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-007.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-008.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-014.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-005.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-006.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-008.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-014.md",
]

[relations]
implements = ["REQ-PLG-010", "REQ-PLG-011", "REQ-PLG-012"]
specifications = ["SPEC-PLG-007"]
verification = ["VER-PLG-007"]
architecture = ["ARCH-PLG-002", "ADR-PLG-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T06:12:21Z"
decided_by = "engineering-owner"
reason = "The operator explicitly approved the reviewed plugin packets in this task: \"i approve the packets, i authorize the work\". On 2026-09-10 they selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\" after deciding DEC-PLG-001 and DEC-PLG-002 for the tested Windows activation routes. Record only the named approve decision for the D04 governing chain or WO-PLG-007, from reviewed proposal 0b42325b. Sibling work-order states, completion, assurance, release and merge remain separate."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-10T06:13:00Z"
decided_by = "engineering-owner"
reason = "The operator explicitly approved the reviewed plugin packets in this task: \"i approve the packets, i authorize the work\". On 2026-09-10 they selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\" after deciding DEC-PLG-001 and DEC-PLG-002 for the tested Windows activation routes. Record only the named start decision for the D04 governing chain or WO-PLG-007, from reviewed proposal 0b42325b. Sibling work-order states, completion, assurance, release and merge remain separate."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-10T17:10:39Z"
decided_by = "engineering-owner"
reason = "On 2026-09-10 the operator requested \"can WO-PLG-007 be set to implemented ?\" after delivery of its implementation and retained evidence in PR #435 at 692407030f30aed7e462e7cac9760e256d7a7f5d. Record the engineering-owner completion decision for WO-PLG-007 only, conditional on passing released evaluator gates. VREC preparation, assurance, release and PR merge remain separate decisions."
+++

# Work Order: Implement verified session governance delivery

## Lifecycle

Marked implemented by the engineering owner on 2026-09-10 after the operator
requested completion of the delivered implementation and evidence in PR #435.
The released evaluator applied the explicit completion decision. Verification-record
preparation, assurance, release and merge remain separate decisions.

## Objective

Deliver current verified governance at startup, resume and compaction recovery, including a complete-read fallback.

## In scope

One Python session handler and focused fixtures for identity, integrity, context completeness and failure behavior.


Definition introduction D04 selects this WO and the exact records listed in the [definition-delivery plan](../../../notes/plugin-definition-delivery-2026-09-08.md). Those paths cover draft introduction and separately authorized decisions, not implementation of another WO.

## Out of scope

Host registration implementation, Python installation, evaluator changes, new governance rules and any authority to merge or publish.

## Authorized decision envelope

After approval, choose internal parsing, diagnostics and fixture structure within SPEC-PLG-007. Host transport must follow accepted adapter contracts.

## Constraints

D04 delivery waits for evidenced positive host-route decisions and approval of the shared governing chain. The probe work orders run first; graph and scope checks do not supply those decisions.

Use the verified environment's absolute Python with `-I`; reuse existing identity and integrity checks. Preserve full gate/router content. Remain read-only.

## Expected change surface

The handler, its tests, this WO, its evidence, and the exact D04 definition-introduction paths.

## Required verification

Satisfy VER-PLG-007 with captured protocol fixtures and the released evaluator after WO-PLG-001/002. Live transport qualification belongs to WO-PLG-005/006 and WO-PLG-015; it does not block this handler's fixture acceptance.

## Evidence to record

Record source identities, fixture outputs, fallback reads, failures and protocol/Python/evaluator versions. Do not present fixtures as live-host delivery evidence.

## Stop and escalate conditions

Stop on incomplete fixture delivery, unspecified host protocol, runtime mismatch or a need to change evaluator or managed policy.

## Completion report format

List changed paths, actual test results, retained evidence, supported hosts, remaining blockers, lifecycle state and one next step.
