+++
id = "WO-PLG-005"
type = "work_order"
title = "Implement the accepted Codex host adapter"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "Future governed Codex sessions rely on correct host bindings and truthful reporting of supported checks."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "plugins/verity-plane/codex/",
  "tests/plugin_integration/codex_adapter/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-005.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-005/",
]

[relations]
implements = ["REQ-PLG-008"]
specifications = ["SPEC-PLG-005"]
verification = ["VER-PLG-005"]
architecture = ["ARCH-PLG-002", "ADR-PLG-002"]
+++

# Work Order: Implement the accepted Codex host adapter

## Lifecycle

Draft only: this proposes scope and assurance classification, not authorization.
The engineering owner decides approval and start under existing rules.
No execution delegation is proposed; later verification needs a commit-bound record.

## Objective

Connect accepted Codex host discovery and event bindings to the shared plugin components.

## In scope

Codex manifests, supported event argument/result mapping, shared skill discovery, and activation failure reporting.

## Out of scope

Core evaluator changes, managed repository controls, approved definition amendments, public release or publication, and installation outside disposable host fixtures.

## Authorized decision envelope

After approval, choose host-file organization and test fixtures within the accepted compatibility decision. Translate host inputs and results; add no evaluator policy.

## Constraints

The blocked, unapproved SPEC-PLG-005 prevents this work order's approval. The technical owner must select a positively supported route through DEC-PLG-001 before approving that specification.
Selecting exclude-codex authorizes no implementation or support. Rejection, deferral, or amendment requires its own artifact decision. Consume completed outputs from WO-PLG-001, WO-PLG-002, WO-PLG-003, WO-PLG-007, and WO-PLG-008. Missing skill assets remain an explicit integration prerequisite.
The proposal source is PR #360 at `9e894e99`; this work order's approved relations and scope govern implementation.

## Expected change surface

The Codex adapter component and its focused integration tests.
Only this work order and its evidence directory may also change.

## Required verification

Execute VER-PLG-005 against the exact candidate.
Record real host, operating-system, Python, and released-evaluator versions; no unrun case counts as passing.

## Evidence to record

Retain commands, independent expectations, observed results, candidate identity, and limitations under `evidence/WO-PLG-005/`.
Prepare the later verification record through the existing evaluator when authorized.

## Stop and escalate conditions

Stop for missing approval, unmet prerequisites, failed required checks, unsafe interpreter identity, or changes outside the selected scope.
New host permissions or unsupported API assumptions require a concrete decision.

## Completion report format

Report changed paths, requirement coverage, checks and failures, exact candidate, retained evidence paths, and unresolved limits.
Do not infer approval, verification, release, or publication from successful tests.
