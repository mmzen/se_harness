+++
id = "WO-PLG-001"
type = "work_order"
title = "Build shared native plugin package assembly"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "Future host installation and support decisions rely on the integrity and shared provenance of assembled executable packages."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "repository_tools/plugin_distribution.py",
  "scripts/build_plugin_archives.py",
  "tests/plugin_integration/package_assembly/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-001.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-001/",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/architecture/ARCH-PLG-001.md",
  "docs/engineering/plugin-integration/architecture/adr/ADR-PLG-001.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-001.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-002.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-003.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-004.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-005.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-001.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-002.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-001.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-002.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-002.md",
]

[relations]
implements = ["REQ-PLG-001","REQ-PLG-002"]
specifications = ["SPEC-PLG-001"]
verification = ["VER-PLG-001"]
architecture = ["ARCH-PLG-001", "ADR-PLG-001"]
+++

# Work Order: Build shared native plugin package assembly

## Lifecycle

Draft only: this proposes scope and assurance classification, not authorization.
The engineering owner decides approval and start under existing rules.
No execution delegation is proposed; later verification needs a commit-bound record.

## Objective

Implement package assembly from one selected published evaluator wheel and shared resources into separate Codex and Claude Code packages.

## In scope

Assembly inputs, release-digest checks, shared-file inventories, host-specific output selection, and bounded failure handling.


Definition introduction D03 selects this WO and the exact records listed in the [definition-delivery plan](../../../notes/plugin-definition-delivery-2026-09-08.md). Those paths cover draft introduction and separately authorized decisions, not implementation of another WO.

## Out of scope

Core evaluator changes, managed repository controls, approved definition amendments, public release or publication, and installation outside disposable host fixtures.

## Authorized decision envelope

After approval, choose internal function names, fixture layout, and archive compression within SPEC-PLG-001. Use temporary non-promotable outputs for tests.

## Constraints

Consume exact published wheel bytes; do not import or rebuild the candidate evaluator. Missing production assets remain explicit; fixtures do not establish host support.
The proposal source is PR #360 at `9e894e99`; this work order's approved relations and scope govern implementation.

## Expected change surface

Two assembly entry files and focused package-assembly fixtures.
Definition delivery may also change its exact declared records and assigned index files.

## Required verification

Execute VER-PLG-001 against the exact candidate.
Record real host, operating-system, Python, and released-evaluator versions; no unrun case counts as passing.

## Evidence to record

Retain commands, independent expectations, observed results, candidate identity, and limitations under `evidence/WO-PLG-001/`.
Prepare the later verification record through the existing evaluator when authorized.

## Stop and escalate conditions

Stop for missing approval, unmet prerequisites, failed required checks, unsafe interpreter identity, or changes outside the selected scope.
New host permissions or unsupported API assumptions require a concrete decision.

## Completion report format

Report changed paths, requirement coverage, checks and failures, exact candidate, retained evidence paths, and unresolved limits.
Do not infer approval, verification, release, or publication from successful tests.
