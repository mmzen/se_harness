+++
id = "WO-PLG-006"
type = "work_order"
title = "Implement the accepted Claude Code host adapter"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-12"

[delegation]
class = "execution"

[assurance]
commit_bound_verification = "required"
rationale = "Future governed Claude Code sessions rely on correct host bindings and truthful reporting of supported checks."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "plugins/verity-plane/claude-code/",
  "tests/plugin_integration/claude_adapter/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-006.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-006/",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-013.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-013-evaluator.json",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-009.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-006.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-006.md",
]

[relations]
implements = ["REQ-PLG-009"]
specifications = ["SPEC-PLG-006"]
verification = ["VER-PLG-006"]
architecture = ["ARCH-PLG-002", "ADR-PLG-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-11T19:00:19Z"
decided_by = "engineering-owner"
reason = "The operator explicitly selected WO-PLG-005 and WO-PLG-006 for implementation through the delegated route on 2026-09-11. Approve this work order with the requested execution class and exact future verification-record paths. This delegates only DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE, conditional on the class at the PR base and a successful live required check for the exact head. No implementation has started; verification, release and merge remain human decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-11T19:08:36Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at 78cd64df7c130a6f42ab357836093db30f710753 (check-run 103386776253, source github-checks)."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-12T09:06:10Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-COMPLETE under [delegation] class 'execution': required check 'validate' success at d6e9f8063dbee01dbb112f5cd2aef219def4e4cc (check-run 103529953216, source github-checks). Complete the bounded adapter implementation and fresh assessment under the approved criteria merged by PR #458. qualification-review-20260912/assessment.md binds unchanged production source, immutable package/recorded-loaded inventories and current definitions; required healthy-path and shared obligations remain satisfied. C10/C11 remain failed enforcement under accepted DEC-PLG-006. Only qualification with a documented local limitation is proposed for independent assurance; no verification, merge, release or expanded host profile is claimed."
+++

# Work Order: Implement the accepted Claude Code host adapter

## Lifecycle

The operator selected WO-PLG-006 for the delegated route on 2026-09-11. Work-order approval records the requested execution delegation. The class permits only DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE, after it is present at the pull-request base and the required live GitHub check succeeds for the exact head. The released evaluator recorded delegated implementation completion on 2026-09-12, as retained in the lifecycle event above. The [dated qualification assessment](../evidence/WO-PLG-006/qualification-review-20260912/assessment.md) applies the criteria merged by PR #458 to unchanged adapter source and retained native observations. C10/C11 remain failed enforcement; the proposed assurance outcome is qualification with a documented local limitation under DEC-PLG-006. Verification, release and merge remain human decisions.

## Objective

Connect accepted Claude Code host discovery and event bindings to the shared plugin components.

## In scope

Claude Code manifests, supported event argument/result mapping, shared skill discovery, and activation failure reporting.


The [definition-delivery plan](../../../notes/plugin-definition-delivery-2026-09-08.md) introduces this packet in D04 under WO-PLG-007. This WO's definition paths support its own introduction and separately authorized decisions.

## Out of scope

Core evaluator changes, managed repository controls, approved definition amendments, public release or publication, and installation outside disposable host fixtures.

## Authorized decision envelope

After approval, choose host-file organization and test fixtures within the accepted compatibility decision. Translate host inputs and results; add no evaluator policy.

## Constraints

The technical owner accepted the demonstrated Windows route in DEC-PLG-002, and SPEC-PLG-006 is approved. That decision's profile and retained limits govern this work. Other host, platform, Python or evaluator profiles remain unqualified; this work does not expand the accepted profile.
Selecting exclude-claude authorizes no implementation or support. Rejection, deferral, or amendment requires its own artifact decision. Consume completed outputs from WO-PLG-001, WO-PLG-002, WO-PLG-004, WO-PLG-007, and WO-PLG-008. Missing skill assets remain an explicit integration prerequisite.
The proposal source is PR #360 at `9e894e99`; this work order's approved relations and scope govern implementation.

## Expected change surface

The Claude Code adapter component and its focused integration tests.
Definition delivery may also change its exact declared records and assigned index files.

## Required verification

Execute VER-PLG-006 against the exact candidate.
Record real host, operating-system, Python, and released-evaluator versions; no unrun case counts as passing.

## Evidence to record

Retain commands, independent expectations, observed results, candidate identity, and limitations under `evidence/WO-PLG-006/`.
Prepare the later verification record through the existing evaluator when authorized.

## Stop and escalate conditions

Stop for missing approval, unmet prerequisites, failed required checks, unsafe interpreter identity, or changes outside the selected scope.
New host permissions or unsupported API assumptions require a concrete decision.

## Completion report format

Report changed paths, requirement coverage, checks and failures, exact candidate, retained evidence paths, and unresolved limits.
Do not infer approval, verification, release, or publication from successful tests.
