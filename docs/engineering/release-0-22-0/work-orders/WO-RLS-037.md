+++
id = "WO-RLS-037"
type = "work_order"
title = "Remove the duplicated README host-limit paragraph"
status = "draft"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[execution_scope]
paths = [
  "README.md",
  "docs/engineering/release-0-22-0/work-orders/WO-RLS-037.md",
  "docs/engineering/release-0-22-0/verification/VER-RLS-001.md",
  "docs/engineering/release-0-22-0/verification-records/VREC-PLG-034.md",
  "docs/engineering/release-0-22-0/evidence/VREC-PLG-034-evaluator.json",
  "docs/engineering/release-0-22-0/evidence/WO-RLS-037/"
]

[relations]
implements = ["REQ-DST-069"]
specifications = ["SPEC-DST-024", "SPEC-DST-029"]
verification = ["VER-RLS-001"]
+++

# Remove the duplicated README host-limit paragraph

## Objective and cause

Restore the accepted README size limit without changing its public claims.
CI run 37101342557 failed `test_root_is_a_bounded_human_entry_point`: 676 words
exceed the 650-word limit. The release update duplicated the same host-limit
paragraph. Removing its second copy produces 648 words.

## In scope

Apply only `evidence/WO-RLS-037/proposed-readme.patch`: remove the duplicate
under `Fewer repository files`. Keep the complete first warning beside the
installation instructions. Retain the failure, check the corrected document,
prepare its new verification record and transport the approved correction in
the existing release review.

## Out of scope and constraints

No test or threshold changes, new public claims, package rebuild, runtime change,
host tests, adoption, provider-setting change or release-marker action. Preserve
the accepted definitions, WO-RLS-036 history, VREC-PLG-032/033 and their bound
evidence. No architecture change or new architecture decision is needed.

## Authority and assurance proposal

Propose required commit-bound verification because release closeout relies on
the corrected public guidance. Human mmzen must confirm this classification
and approve this work order and VER-RLS-001; no decision is inferred here.

After approval, the agent may apply the exact deletion, run checks, retain
evidence, record completion and prepare verification. A changed correction
returns for review. The proposed approval also includes ordinary pushes and
updates of PR #530 from work/release-0-22-0 to mmzen/se_harness:main, under the
existing review-delivery request. Human verification and merge remain separate.

## Required verification and evidence

VER-RLS-001 defines the checks. Use the existing test suites and compare the
exact diff. Retain actual results in `evidence/WO-RLS-037/`, including generated
handoff evidence, review and later CI receipts. The selected evaluator remains
0.21.0. Planned VREC-PLG-034 and its fixed evaluator evidence path are explicitly
covered above; confirm ID availability before capture.

## Stop conditions and completion report

Stop for a changed patch, failed required check, unavailable evidence or an
uncovered path. A new candidate requires a new verification decision; do not
extend VREC-PLG-033 to changed bytes. Report the final word count, actual checks,
candidate, evidence location, CI state and the next accountable decision.

## Simplicity review

Remove the repeated paragraph and reuse existing tests. Keep the 650-word
requirement and all unique information. No new test helper or product mechanism
is required. This draft has not started implementation.
