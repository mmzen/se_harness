+++
id = "WO-PLG-007"
type = "work_order"
title = "Implement verified session governance delivery"
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
  "plugins/verity-plane/common/scripts/session-context.py",
  "tests/plugin_integration/session_context/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-007.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-007/",
]

[relations]
implements = ["REQ-PLG-010", "REQ-PLG-011", "REQ-PLG-012"]
specifications = ["SPEC-PLG-007"]
verification = ["VER-PLG-007"]
architecture = ["ARCH-PLG-002", "ADR-PLG-002"]
+++

# Work Order: Implement verified session governance delivery

## Lifecycle

Draft proposal only; no execution or delegation is authorized. Approval of this WO and its governing chain precedes work; later lifecycle decisions follow the installed rules.

## Objective

Deliver current verified governance at startup, resume and compaction recovery, including a complete-read fallback.

## In scope

One Python session handler and focused fixtures for identity, integrity, context completeness and failure behavior.

## Out of scope

Host registration, Python installation, evaluator changes, new governance rules and any authority to merge or publish.

## Authorized decision envelope

After approval, choose internal parsing, diagnostics and fixture structure within SPEC-PLG-007. Host transport must follow accepted adapter contracts.

## Constraints

Use the verified environment's absolute Python with `-I`; reuse existing identity and integrity checks. Preserve full gate/router content. Remain read-only.

## Expected change surface

The new handler, its tests, this WO and its retained evidence only.

## Required verification

Satisfy VER-PLG-007 with captured protocol fixtures and the released evaluator after WO-PLG-001/002. Live transport qualification belongs to WO-PLG-005/006 and WO-PLG-015; it does not block this handler's fixture acceptance.

## Evidence to record

Record source identities, fixture outputs, fallback reads, failures and protocol/Python/evaluator versions. Do not present fixtures as live-host delivery evidence.

## Stop and escalate conditions

Stop on incomplete fixture delivery, unspecified host protocol, runtime mismatch or a need to change evaluator or managed policy.

## Completion report format

List changed paths, actual test results, retained evidence, supported hosts, remaining blockers, lifecycle state and one next step.
