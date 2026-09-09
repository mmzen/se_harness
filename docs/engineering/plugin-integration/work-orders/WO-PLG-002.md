+++
id = "WO-PLG-002"
type = "work_order"
title = "Document and verify first private environment setup"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-09"

[assurance]
commit_bound_verification = "required"
rationale = "Future governed commands rely on selecting a genuine released evaluator with safe interpreter origins and exact repository identity."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "plugins/verity-plane/common/skills/setup/SKILL.md",
  "plugins/verity-plane/common/skills/setup/references/environment.md",
  "tests/plugin_integration/environment_setup/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-002.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-002/",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-003.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-004.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-005.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-002.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-002.md",
]

[relations]
implements = ["REQ-PLG-003","REQ-PLG-004","REQ-PLG-005"]
specifications = ["SPEC-PLG-002"]
verification = ["VER-PLG-002"]
architecture = ["ARCH-PLG-001", "ADR-PLG-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-09T20:19:31Z"
decided_by = "engineering-owner"
reason = "The operator explicitly selected and authorized WO-PLG-002 in this task on 2026-09-09: \"you can start WO-PLG-002\". The previously approved plugin packet and this instruction authorize its bounded setup-skill implementation and disposable-fixture tests. Record only this work-order approval; no completion, assurance, release or merge decision is inferred."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-09T20:20:40Z"
decided_by = "engineering-owner"
reason = "The operator explicitly selected and authorized WO-PLG-002 in this task on 2026-09-09: \"you can start WO-PLG-002\". The previously approved plugin packet and this instruction authorize its bounded setup-skill implementation and disposable-fixture tests. Record only this work-order start; no completion, assurance, release or merge decision is inferred."
+++

# Work Order: Document and verify first private environment setup

## Lifecycle

The operator approved and started this work order on 2026-09-09: "you can start
WO-PLG-002". The released evaluator recorded both decisions in the lifecycle
events above. The work is in progress, without execution delegation.
Completion and commit-bound verification remain separate decisions.

## Objective

Implement the setup skill's procedure for preparing a verified private evaluator with provided Python and the packaged wheel.

## In scope

Prerequisite guidance, isolated environment creation, offline installation, matching-environment reuse, and existing evaluator identity checks.


The [definition-delivery plan](../../../notes/plugin-definition-delivery-2026-09-08.md) introduces this packet in D03 under WO-PLG-001. This WO's definition paths support its own introduction and separately authorized decisions.

## Out of scope

Core evaluator changes, managed repository controls, approved definition amendments, public release or publication, and installation outside disposable host fixtures.

## Authorized decision envelope

After approval, choose instruction structure and fixture organization. Invoke existing shell, Python, environment, package-installation, and identity commands directly; add no bootstrap command.

## Constraints

Use WO-PLG-001's wheel and inventory contract. WO-PLG-009 and WO-PLG-013 may add their scoped repository and maintenance links to the same skill. This packet stops before repository initialization.
The proposal source is PR #360 at `9e894e99`; this work order's approved relations and scope govern implementation.

## Expected change surface

The setup skill, its environment procedure, and focused executable checks of those documented commands.
Definition delivery may also change its exact declared records and assigned index files.

## Required verification

Execute VER-PLG-002 against the exact candidate.
Record real host, operating-system, Python, and released-evaluator versions; no unrun case counts as passing.

## Evidence to record

Retain commands, independent expectations, observed results, candidate identity, and limitations under `evidence/WO-PLG-002/`.
Prepare the later verification record through the existing evaluator when authorized.

## Stop and escalate conditions

Stop for missing approval, unmet prerequisites, failed required checks, unsafe interpreter identity, or changes outside the selected scope.
New host permissions or unsupported API assumptions require a concrete decision.

## Completion report format

Report changed paths, requirement coverage, checks and failures, exact candidate, retained evidence paths, and unresolved limits.
Do not infer approval, verification, release, or publication from successful tests.
