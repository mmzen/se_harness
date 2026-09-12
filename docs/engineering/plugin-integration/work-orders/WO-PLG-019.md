+++
id = "WO-PLG-019"
type = "work_order"
title = "Record the accepted local hook limitation and reconcile qualification"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-12"
updated = "2026-09-12"

[assurance]
commit_bound_verification = "required"
rationale = "Future adapter assurance relies on these amended definitions and the truthful separation of accepted limitations from passing enforcement."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-005.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-006.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-008.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-005.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-006.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-008.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-019.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-019.md",
  "docs/engineering/plugin-integration/decisions/DEC-PLG-006.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-019/",
]

[relations]
implements = ["REQ-PLG-008", "REQ-PLG-009", "REQ-PLG-013", "REQ-PLG-014"]
specifications = ["SPEC-PLG-005", "SPEC-PLG-006", "SPEC-PLG-008"]
verification = ["VER-PLG-019"]
architecture = ["ARCH-PLG-002", "ADR-PLG-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-12T07:21:58Z"
decided_by = "engineering-owner"
reason = "The operator replied \"i approve\" to packet 29507242f4d17369d242da25f37043fdbdc9f1a3254ff9c01938e6c858845514. Record the engineering-owner approval of the exact WO-PLG-019 scope and assurance classification; start and conditional completion were separately authorized in that packet."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-12T07:24:55Z"
decided_by = "engineering-owner"
reason = "The operator approved packet 29507242f4d17369d242da25f37043fdbdc9f1a3254ff9c01938e6c858845514, explicitly authorizing WO-PLG-019 to start. Record only this selected work-order start after passing released start checks."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-12T07:31:19Z"
decided_by = "engineering-owner"
reason = "The operator approved packet 29507242f4d17369d242da25f37043fdbdc9f1a3254ff9c01938e6c858845514, expressly authorizing completion after required checks pass. VER-PLG-019 inspection and preservation checks and the released implementation-evidence handoff gate now pass. Record only WO-PLG-019 implemented; adapter qualification, VREC assurance and delivery remain separate."
+++

# Work Order: Record the accepted local hook limitation and reconcile qualification

## Lifecycle

The operator approved the exact reconciliation packet on 2026-09-12 under the technical, assurance and engineering owner roles.
owner-approval.json retains the verbatim response, named artifacts, amendment digest, revisit trigger and conditional completion authorization.
Released-evaluator lifecycle events record approval, start and completion; amendment-receipts.json records the six definition decisions separately.
The original reviewed drafts remain in approved-inputs/. This work carries no execution delegation and grants no adapter assurance, merge or release decision.

## Objective

Record one shared deviation and reconcile adapter qualification with the accepted local limitation while preserving every observed enforcement failure.

## In scope

Create DEC-PLG-006 against SPEC-PLG-008#PLG-HOOK-002; record its disposition through the released evaluator after the exact recording inputs are authorized.
Apply the six byte-bound amendments in proposal-manifest.json after their technical-owner and assurance-owner decisions.
Introduce VER-PLG-019, retain the authorizing instructions, review results, source identities, before/after hashes and the selected workflow handoff.
The exact approved source bytes remain unchanged during preparation; proposed replacements have .md.txt names beneath this work order's evidence.

## Out of scope

Adapter, shared-handler or evaluator code; managed files; runtime or native host installation; live service tests; external controls; other work-order transitions.
No original test result, acceptance report, decided activation DEC, VREC or RLS may change.
No adapter qualification, completion, assurance, integration, merge, publication or release is decided by this work order.

## Authorized decision envelope

The implementation actor may organize retained evidence and correct drafting errors within the exact approved amendment meaning.
Technical-owner owns specification amendments and the deviation; assurance-owner owns verification criteria; engineering-owner owns this work order and its start/completion.
Record each actual decision separately. A decision about one role or artifact never approves the others.

## Constraints

The only candidate limited profiles are DEC-PLG-001's Codex CLI 0.153.4 and DEC-PLG-002's Claude Code 2.1.266 on Windows.
Both use Python 3.14.6 and released evaluator 0.16.0. This repository's governing evaluator remains released 0.17.0.
Healthy checks and timely denial remain mandatory. C10/C11 enforcement failures remain failures; unsafe C12 bindings remain ineligible.
The approved Codex shell-start exception is an explicit unavailable subcase, never a passing observation or a refusal guarantee.
Review the accepted deviation before the first public plugin release, profile expansion or introduction of remote acceptance controls.
No code or architecture responsibility changes are proposed; ARCH-PLG-002 and ADR-PLG-002 remain applicable unchanged.

## Expected change surface

The exact definition files and this work order's new records/evidence, as listed in execution_scope.

## Required verification

Execute VER-PLG-019. Use the isolated released 0.17.0 evaluator for managed integrity, graph, work-order scope and phase-appropriate checkpoints.
Retain candidate CLI/graph and release-distribution checks when applying the packet. This documentation change adds no runtime test obligation or test waiver.

## Evidence to record

Retain proposal-manifest.json, sources.json, the six reviewed replacements, exact operator decisions and command arguments/results under evidence/WO-PLG-019/.
Retain pre-action evidence before applying approved amendments; compare preserved records and production trees with their exact starting commits.

## Stop and escalate conditions

Stop for missing exact owner decisions, altered approved inputs, failed integrity/graph/scope checks, expanded profiles, or any required change outside this scope.
An unapproved unavailable-case exception remains a blocker to the proposed limited qualification; it is not an implementation choice.

## Completion report format

Report applied record IDs and amendments, preserved raw evidence and code, checks, unresolved limitations and actual lifecycle states.
Use the released evaluator's selected result and one next action. Completing this governance work does not complete either adapter.
