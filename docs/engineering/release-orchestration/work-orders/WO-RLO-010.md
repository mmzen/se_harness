+++
id = "WO-RLO-010"
type = "work_order"
title = "Support plugin-owned evaluator locks in publication readers"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-27"
updated = "2026-09-27"

[assurance]
commit_bound_verification = "required"
rationale = "Publication will rely on these executable readers to validate evaluator identity and immutable release provenance. The correction needs a commit-bound human assurance decision."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".github/scripts/publish_dashboard.py",
  "tests/test_dashboard_publication.py",
  "tests/test_release_orchestration.py",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-010.md",
  "docs/engineering/release-orchestration/verification/VER-RLO-007.md",
  "docs/engineering/release-orchestration/evidence/WO-RLO-010/",
  "docs/engineering/release-orchestration/verification-records/VREC-RLO-010.md",
  "docs/engineering/release-orchestration/evidence/VREC-RLO-010-evaluator.json"
]

[relations]
implements = ["REQ-RLO-001"]
specifications = ["SPEC-RLO-001", "SPEC-PLG-021"]
architecture = ["ARCH-RLO-001", "ADR-RLO-001"]
verification = ["VER-RLO-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T19:07:08Z"
decided_by = "engineering-owner"
reason = "The human accepted the reviewed bounded publication compatibility correction in this task: Ok for the correction. This work order formalizes the accepted shared-helper and test paths with required commit-bound assurance. Codex may execute that scope under DR-015. No released record, bound package, workflow or publication change is authorized."
scope_paths = [".github/scripts/publish_dashboard.py", "tests/test_dashboard_publication.py", "tests/test_release_orchestration.py", "docs/engineering/release-orchestration/work-orders/WO-RLO-010.md", "docs/engineering/release-orchestration/verification/VER-RLO-007.md", "docs/engineering/release-orchestration/evidence/WO-RLO-010/", "docs/engineering/release-orchestration/verification-records/VREC-RLO-010.md", "docs/engineering/release-orchestration/evidence/VREC-RLO-010-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-27T19:07:41Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the human-approved publication lock compatibility correction under DR-015 after released start preflight passes."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-27T19:18:41Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Codex records scoped implementation completion under the human-approved WO and DR-015. The 65 focused tests, full 1126-test suite with 16 existing skips, frozen-main readers, repository checks and bound handoff passed. No candidate verification or publication is applied."
+++

# Support plugin-owned evaluator locks in publication readers

## Objective and accepted input

Correct the publication refusals observed after PR #490 merged at
`523ff825773e05c970c041ecee5c22bfabedaa3f`. The human answered
“Ok for the correction” to the bounded publication compatibility proposal
in this task. This work order and VER-RLO-007 formalize that reviewed scope.
The accepted proposal and original read-only failures are retained with the
work evidence. No new publication or ownership policy is introduced.

## In scope

1. Correct `_validated_evaluator_binding` and `read_evaluator` in the shared
   publication helper to accept supported schema-4 plugin ownership.
2. Preserve schema-3 behavior and every existing identity, digest, provenance,
   archive and unsupported-schema check. Accept older plugin-binding fields
   as required by SPEC-PLG-021; do not read or execute local plugin content.
3. Add the bounded regression cases in VER-RLO-007 to the existing test files.
4. Demonstrate both read-only entry points against the frozen merged snapshot.
5. Retain evidence, complete this WO after checks, and prepare VREC-RLO-010.

## Existing authority and design

REQ-RLO-001 and SPEC-RLO-001 rules 3-5 already require exact record and evaluator
resolution from main. SPEC-PLG-021 defines the supported ownership formats.
Their existing requirements need a compatible reader, not a changed contract.
ARCH-RLO-001 and ADR-RLO-001 retain the separation between trusted publication
code, candidate code and credentials. Use a small shared local predicate if
needed; do not import the candidate package into this publication boundary.
No architecture decision or amendment is needed for this correction.

## Authorized decision envelope

The human's acceptance covers this bounded correction and its stated tests.
After the released evaluator applies approval and start, Codex may perform
the scoped edits, local commits, checks, evidence retention, completion and
required VREC preparation under DR-015. Local names and fixture organization
are implementation choices. Human verification of the resulting VREC remains
a separate decision. Delivery uses the session's push/PR authorization only
for an ordinary correction-branch push and a draft PR to `mmzen/se_harness`
`main`; no force push, merge or publication is included.

## Constraints and exclusions

Use isolated released 0.18.0 for governance. Preserve every pre-existing
formal artifact and retained evidence byte, including RLS-SEH-028 and
VREC-SEH-028. Preserve the root lock, bound candidate and archive hashes.
No workflow, runtime, fixture, installed instruction, template, packaging,
release or external-service change is included. No promotable build, workflow
dispatch, tag creation, release publication, latest promotion or root adoption.

## Required checks and evidence

Pass VER-RLO-007 and the repository's applicable checks. Retain the exact
baseline, actual runtimes, argument arrays, exit codes, meaningful outputs,
original failures and unchanged-history comparison under `evidence/WO-RLO-010/`.
Use committed fixture bytes for the full suite as specified in that contract;
report the existing Windows line-ending limitation without claiming a fix.
Review the diff for the smallest compatible correction and meaningful tests.

## Stop conditions and completion

Stop the affected action for a required failure, changed scope, altered
historical input or a need to weaken publication controls. Resolve in-scope
failures without expanding authority. Report implemented behavior, actual
checks, evidence limits, the ready VREC and the evaluator's next human decision.
