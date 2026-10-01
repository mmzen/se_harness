+++
id = "WO-IAR-041"
type = "work_order"
title = "Correct the plugin setup integrity fixture for minimal installation"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification in VREC-IAR-023; later integration and release decisions rely on this integrity test."
decided_by = "mmzen"

[execution_scope]
paths = [
  "tests/plugin_integration/test_simple_plugin.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-041.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-041/",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-023.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-023-evaluator.json",
]

[relations]
implements = ["REQ-IAR-031"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T18:32:09Z"
decided_by = "mmzen"
reason = "Human mmzen: Approve WO-IAR-041 and required verification. Approves the reviewed one-file plugin acceptance fixture correction and required commit-bound verification in VREC-IAR-023. Reviewed draft SHA256 c2bb5760860ccc3b61fdaf46781db0aad80f22f814b3a369368ae7be66236ea8; only confirmed assurance metadata and paragraph completed before approval."
scope_paths = ["tests/plugin_integration/test_simple_plugin.py", "docs/engineering/instruction-architecture/work-orders/WO-IAR-041.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-041/", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-023.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-023-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-01T18:32:39Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-01T18:37:06Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Completed the exact reviewed plugin fixture correction. Original failure reproduced on Windows and Linux; all 11 real-wheel acceptance tests pass on each with no skips. Clean doctor passes and corrupted .gitattributes fails. Product inputs and prior evidence unchanged; validation, review, full scope and handoff pass. Human verification remains separate."
+++

# Correct the plugin setup integrity fixture for minimal installation

## Objective and observed failure

Preserve the real plugin setup integrity refusal check under the accepted minimal
layout. Both upgrade rehearsals in PR #516 fail in
test_real_setup_create_reuse_and_repair at candidate
7cd3711b3e499f7bbb961640f37c3d188a00b303. The test writes ENGINEERING_HARNESS.md
and expects setup to return a failing doctor result. Fresh minimal installation
does not create or manage that file, so doctor correctly returns success.
Each platform ran 11 tests with one failure and no skips.

- Linux: https://github.com/mmzen/se_harness/actions/runs/36906203554/job/110518048972
- Windows: https://github.com/mmzen/se_harness/actions/runs/36906203554/job/110518049071

The previous symlink assertion correction passes candidate source CI. Preserve
VREC-IAR-022, VREC-IAR-020, their evidence and completed work-order histories.

## In scope and expected change surface

Change only the existing real-wheel acceptance test in
tests/plugin_integration/test_simple_plugin.py:

1. Request the existing optional Git integration with --integration git when
   initializing the disposable fixture.
2. Assert that .gitattributes exists, then corrupt that tracked fragment instead
   of creating an untracked ENGINEERING_HARNESS.md file.
3. Keep the nonzero setup-result assertion and require its diagnostic to name
   .gitattributes.

Keep the environment creation, reuse and damaged-package refusal checks. Keep
all other tests and capability conditions. The fragment is already supported
and checked by doctor; no product change, new helper or test framework is needed.
The actual source correction has not been applied during drafting.

## Confirmed assurance

Required commit-bound verification in a new VREC-IAR-023 using VER-IAR-022.
Later integration and release decisions rely on this integrity test. Human
mmzen confirmed: "Approve WO-IAR-041 and required verification". Recheck the
verification destination before capture and stop if its identity conflicts.

## Authorized decision envelope

Approval would authorize the bounded test correction, local checks and commits,
evidence retention, implementation completion and verification preparation.
Human verification remains separate. Existing push/PR authority concerns updating
PR #516; it does not supply approval for this work order or verification acceptance.

## Constraints and exclusions

Use the repository-selected released 0.20.1 evaluator for governance. Reuse
REQ-IAR-031, SPEC-IAR-016, ARCH-IAR-012, ADR-IAR-012 and VER-IAR-022 unchanged.
The independently built 0.21.0 wheel remains a disposable test input, not the
repository's governing evaluator. Confirm its product payload is unchanged.

Do not change production code, plugin behavior, CI workflows, selected versions,
accepted criteria, authority or required gates. Do not edit prior verification
records or their bound evidence. No merge, release, publication or adoption.
Codex Windows desktop remains unverified; these checks provide no desktop proof.

## Required verification

1. Retain the failed Linux and Windows CI logs and the original assertion.
2. Run all 11 plugin acceptance tests on Windows and Linux with the exact
   candidate wheel and candidate Python explicitly supplied. The real-wheel test
   must execute, with no skip. Confirm the original fixture fails before the
   correction and the corrected fixture passes.
3. Inspect the failing doctor result for the corrupted .gitattributes fragment.
   Confirm successful initial setup and reuse, and damaged-package refusal remain.
4. Review the complete diff. Only this test and the new work-order/evidence/record
   files may change. Reuse prior product qualification only after an exact input
   comparison; do not rerun native model sessions for an unchanged product.
5. Run released validation, review preflight, complete Git-derived scope and
   handoff checks. Bind the corrected clean commit and retained evidence with
   capture-verification. Updated PR CI, including both upgrade rehearsals and
   downstream integration jobs, remains required before merge.

## Evidence to record

Keep compact command, commit, wheel digest, platform, Python version, exit status,
test counts, skips, diagnostic and source comparison under evidence/WO-IAR-041/.
Retain original failures. Keep raw local logs outside the repository. Do not
rebuild or replace a candidate wheel unless changed inputs require it; if rebuilt,
compare its payload and record its exact identity.

## Stop and escalate conditions

Stop for another implementation path, changed product behavior, a skipped
real-wheel test, failed required checks, changed criteria or unavailable evidence.
Preserve completed work orders; do not reopen them by editing lifecycle state.

## Completion report format

State the fixture correction, actual Windows/Linux results, unchanged product
inputs, candidate identity, evidence locations, verification record and the
selected evaluator's next step. Preparation does not grant human verification.
