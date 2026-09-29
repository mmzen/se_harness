+++
id = "WO-PLG-029"
type = "work_order"
title = "Align the publication guidance test with observed delivery"
status = "in_progress"
owners = ["mmzen"]
created = "2026-09-29"
updated = "2026-09-29"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required exact-commit assurance because later acceptance relies on this documentation check."
decided_by = "mmzen"

[execution_scope]
paths = [
  "tests/plugin_integration/package_assembly/test_refresh_guidance.py",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-029.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-029/",
  "docs/engineering/plugin-integration/verification-records/",
  "docs/engineering/plugin-integration/evidence/",
]

[relations]
implements = ["REQ-PLG-041"]
specifications = ["SPEC-PLG-023"]
verification = ["VER-PLG-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-29T06:20:14Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen explicitly decided \"Approve WO-PLG-029 and verification\" on 2026-09-29, approving the one-file publication-test correction and required commit-bound verification. The approval confirms the existing 0.19.0 engineering-owner encoding; mmzen is the actual human decision-maker and Codex applies it. Reviewed draft SHA-256 e09cec22347bbc137d6d3309990268ae50e4cc66da0be5a5d6312ce8efdd826c; only confirmed assurance fields/prose added, transition input SHA-256 9d3883487d5829a9102b19313cec3f77488b25dc705d82b8750eaee655cb06ba. No external integration is authorized."
scope_paths = ["tests/plugin_integration/package_assembly/test_refresh_guidance.py", "docs/engineering/plugin-integration/work-orders/WO-PLG-029.md", "docs/engineering/plugin-integration/evidence/WO-PLG-029/", "docs/engineering/plugin-integration/verification-records/", "docs/engineering/plugin-integration/evidence/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-29T06:22:11Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed."
+++

# Align the publication guidance test with observed delivery

## Objective

Make the existing offline publication-guidance test assess the observed public
0.2.1 delivery instead of requiring the old pending-publication wording.

## In scope

Change only the named test module to read WO-PLG-028's new publication receipt.
Keep manifest, released-wheel, public-identity and link checks. Require retained
comparison with the accepted package. Reject stale pending-publication text and
contradictory observations. Retain focused test results and prepare exact-commit
verification, which may cover WO-PLG-028 and this work order together.

## Out of scope

Package or runtime changes, public ref updates, changes to completed work orders
or their evidence, weaker pass criteria, and any additional test or source path.
WO-PLG-028 already covers the current documentation and public-onboarding test.

## Confirmed assurance

Commit-bound verification: **required**, confirmed by human mmzen on
2026-09-29 with "Approve WO-PLG-029 and verification" in response to the
one-file test correction review. This is separate from publication authority.

## Expected change surface

One existing test module, this work order, and new evidence for this work or its
selected VREC. The wider evidence-directory entry permits only a new generated
VREC evaluator companion; it does not admit edits to historical evidence.

## Constraints and design

Use the selected released 0.19.0 evaluator, REQ-PLG-041, SPEC-PLG-023 and
VER-PLG-027. The implementation base is the clean merged preparation
703df23c9c41d60903933106a5eeec988702a789, descended from the package's approved
source baseline. Read observations retained by WO-PLG-028; do not change them to
make a test pass. Keep normal tests offline. No new test framework, architecture
or ADR is needed for this bounded observation-source correction.

## Authorized decision envelope

After approval and start, Codex may apply the reviewed test correction, run
checks, retain new evidence, commit locally, record completion and prepare the
required VREC. Human mmzen decides approval and verification. No external
mutation is included. Existing 0.19.0 owner labels may encode the right only if
the approval confirms that compatibility encoding and retains the human identity.

## Required verification and evidence

Run the refresh-guidance and public-onboarding suites against the actual current
documentation and retained public receipt. Confirm that contradictory observed
versions, missing accepted-package comparison and stale publication wording
fail. Preserve the existing wrong-manifest, wrong-wheel and broken-link cases.
Apply VER-PLG-027's candidate checks to the combined delivery confirmation.
Retain changed-path review, actual command results, scope/handoff checks and
exact-commit verification under this work order and the selected VREC.

## Stop and escalate conditions

Stop if another path or accepted definition needs to change, public evidence is
unavailable or contradictory, a required check fails, or broader behavior would
be needed. Do not edit another work order to grant this scope.

## Completion report format

Report the corrected check, actual results and limits, exact candidate and
selected work orders, and the evaluator's next human decision. Completion does
not authorize verification acceptance, publication, push, PR or merge.
