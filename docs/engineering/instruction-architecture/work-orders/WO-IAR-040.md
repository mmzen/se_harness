+++
id = "WO-IAR-040"
type = "work_order"
title = "Correct the minimal-installer symlink refusal assertion"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification in VREC-IAR-022. Later CI, assurance and release decisions rely on this refusal check."
decided_by = "mmzen"

[execution_scope]
paths = [
  "tests/test_installer.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-040.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-040/",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-022.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-022-evaluator.json",
]

[relations]
implements = ["REQ-IAR-031"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T18:08:30Z"
decided_by = "mmzen"
reason = "Human mmzen: i approve. Answers the explicit WO-IAR-040 and required commit-bound verification in VREC-IAR-022 request for the one-line exception assertion correction and Linux/Windows checks. Reviewed draft SHA256 8a6fefc79188687baea21a0b4d20f03398dc25d89bcb5847ea866c0913d69b95; only the confirmed assurance metadata and explanatory paragraph were completed before approval."
scope_paths = ["tests/test_installer.py", "docs/engineering/instruction-architecture/work-orders/WO-IAR-040.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-040/", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-022.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-022-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-01T18:09:05Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-01T18:16:43Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Completed the approved one-line test correction. Real Linux symlink check, 11-test minimal installer class, 1211-test Linux suite and 26-test Windows installer suite passed with recorded skips. Retained original CI and test-environment failures; passing complete scope and handoff. Human verification remains separate."
+++

# Correct the minimal-installer symlink refusal assertion

## Objective and observed failure

Make the existing symlink refusal test assert the installer's actual public
exception while retaining its no-write checks. PR #516 candidate source CI
failed at d507c528a1a092469b0574b74cab93a4f163be40: 1,211 tests ran on Linux,
with one error and two skips. The installer refused the linked .github parent
before writing, as required. The test expected ValueError but safe_destination
raises installer.HarnessError. The Windows source run skipped this test because
that host could not create the symlink.

Failure: https://github.com/mmzen/se_harness/actions/runs/36903728008/job/110508927545

## In scope and expected change surface

Change only the exception argument in
MinimalInstallationTests.test_linked_parent_refuses_without_writes:

```diff
-        with self.assertRaisesRegex(ValueError, "linked|symlink"):
+        with self.assertRaisesRegex(installer.HarnessError, "linked|symlink"):
```

Preserve the diagnostic match, outside-directory and configuration no-write
assertions, and host-capability skip. Use the existing test and exception;
no production change, new helper or new test framework is needed.
Retain this work order, its checks and one new verification record at the
explicit destinations above.

## Confirmed assurance

Required commit-bound verification in VREC-IAR-022, with VER-IAR-022.
Later CI, assurance and release decisions rely on this refusal check. Human
mmzen confirmed the work order and required verification: "i approve".
Recheck ID availability before capture and stop if the destination conflicts.

## Authorized decision envelope

Approval authorizes the one-line correction, local checks and commits, evidence
retention, completion recording and required verification preparation. Human
verification remains separate. The existing request to update PR #516 through
push and PR does not itself approve this work order or waive verification.

## Constraints and exclusions

Use this repository's selected released 0.20.1 evaluator. Reuse the accepted
REQ-IAR-031, SPEC-IAR-016, ARCH-IAR-012, ADR-IAR-012 and VER-IAR-022 unchanged.
Do not change installer behavior, CI workflows, accepted definitions, authority,
gates, existing work-order histories or VREC-IAR-020 and its bound evidence.
No release, marketplace publication, adoption or merge. Codex Windows desktop
remains unverified; this test correction supplies no desktop evidence.

## Required verification

1. Preserve the actual failed CI result and the before-fix test assertion.
2. Run the exact symlink test on Linux with a real symlink and no skip, then
   the complete MinimalInstallationTests class. Confirm the linked destination
   and repository configuration remain untouched on refusal.
3. Run the full source suite on Linux with the CI options (four workers and
   full scale). Run the focused installer tests on Windows and retain any
   host-capability skips explicitly. Do not claim a skipped test passed.
4. Confirm only the intended test line and new governance/evidence files differ
   from the verified implementation. Reuse unaffected installed-wheel and
   native evidence only with this input comparison; do not rerun model sessions
   for an unchanged product or claim they reassess the desktop gap.
5. Run released validation, review preflight and complete Git-derived scope and
   handoff checks. Bind the exact corrected candidate and explicit evidence
   files through capture-verification. Updated PR CI remains required before merge.

## Evidence to record

Keep a compact result under evidence/WO-IAR-040/ with the failed run/job URL,
exact command, source commit, platform, Python identity, exit status, test counts,
skips, failure excerpt and source comparison. Preserve raw local logs outside
the repository and link retained CI artifacts with their actual retention limits.
Do not duplicate the existing aggregate evidence or alter its bytes.

## Stop and escalate conditions

Stop for another required code path, changed production behavior, a failing or
skipped Linux symlink check, changed accepted criteria, unavailable evidence or
an occupied verification destination. Do not reopen completed work orders or
manually edit lifecycle status.

## Completion report format

State the exact assertion correction, actual Linux and Windows results, source
comparison, candidate identity, retained limitations, verification record and
the evaluator's next step. Preparation does not supply human verification.
