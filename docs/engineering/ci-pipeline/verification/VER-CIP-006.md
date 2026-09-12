+++
id = "VER-CIP-006"
type = "verification"
title = "Check disposable Git repositories finish writing before cleanup"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-12"
updated = "2026-09-12"

[relations]
verifies = ["REQ-ECP-012", "REQ-TST-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-12T10:11:29Z"
decided_by = "assurance-owner"
reason = "Approve both and proceed"
+++

# Verification Contract: Check disposable Git repositories finish writing before cleanup

## Independence

The real handover and fixture contract derive from SPEC-ECP-007 ECP-PRD-008
and SPEC-TST-002 TST-HYG-005. A separate positive control enables Git automatic
maintenance and proves the fixture can trigger it. A green teardown alone
does not prove that the process race was removed.

## Requirement-to-evidence matrix

| Requirement and rule | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-ECP-012; SPEC-ECP-007 ECP-PRD-008 | test, inspection, demonstration | CLN01-CLN06 | Disposable export prevents automatic maintenance writers; the real handover, strict cleanup and semantic agreement pass. |
| REQ-TST-004; SPEC-TST-002 TST-HYG-005 | test, inspection, analysis | CLN01-CLN03, CLN06 | The shared Git launcher retains identity, signing, output and error behavior while preventing automatic fixture maintenance. |

## Acceptance scenarios

| Case | Action | Observable pass condition |
| --- | --- | --- |
| CLN01 - Sensitive control | Create a bounded loose-object fixture that demonstrably triggers automatic maintenance with it enabled; capture Git process events. | The positive control observes the maintenance work. The same trigger through the repaired fixture/rehearsal setup launches no automatic maintenance writer. Controls run on Linux and Windows; missing platform evidence remains missing. |
| CLN02 - Inherited settings | Enable maintenance and a low automatic-GC threshold through an isolated parent configuration, then initialize and commit disposable fixtures. | Disposable settings take precedence before commit; no parent/user config changes. Repository content and commit creation remain valid. |
| CLN03 - Setup and helper failures | Fail each new rehearsal configuration operation and a fixture Git operation; exercise binary and UTF-8 output. | Setup fails before staging/commit; the failed timing stage and original error remain visible. Shared helper return/check behavior, fixture identity and signing controls remain intact. |
| CLN04 - Strict teardown | Exercise successful and failing evaluator paths and inject a cleanup error. | Scratch disappears when cleanup succeeds. Cleanup exceptions still propagate and timing reports an error/incomplete replay; no retry or ignore-cleanup-errors path exists. |
| CLN05 - Real hosted handover | Run the existing two replays on Linux and Windows for the exact repair candidate. | All six evaluator checks retain their expected meanings, including predecessor refusal after upgrade. Both replays and both platforms agree on the semantic lock digest; cleanup succeeds in all four. |
| CLN06 - Required checks and scope | Run focused tests, the complete normal suite, distribution validation, candidate CLI help/validate/doctor, released doctor/validate, preflight and Git scope checks. | Required checks pass under released 0.17.0. Any known candidate-template skew is identified precisely. Only WO-CIP-010 paths change; managed policy, plugin candidates and historical records remain intact. |

## Property and invariant tests

No background maintenance process may rely on the temporary directory after
the launching Git operation returns. Test this with process evidence and the
positive control rather than sleeps or a probabilistic cleanup failure.
Handover failure paths and the existing cleanup-error test remain mandatory.

## Static and architecture checks

Review the complete diff against the WO baseline. The rehearsal stays standard
library only; fixture support remains test-only. No workflow trigger, dependency,
permission, timeout, archive capacity or product package behavior changes.

## Security and privacy checks

Configure only disposable repositories or the fixture command invocation.
No global Git configuration, credentials, broad environment dumps or process
termination. Store traces outside the operational checkout.

## Performance and resilience checks

Bound the positive control's data and commands. Do not add a sleep, rmtree
retry, extra hosted replay or full-suite duplication to make results pass.
Record observed Linux/Windows stage costs without claiming a benchmark.

## Manual assessments

Distinguish a confirmed process mechanism from historical teardown errors
whose logs name no writer. Confirm that historical release replay code remains
immutable and can retain its earlier behavior until separately superseded.

## Evidence retention

Retain compact results under WO-CIP-010, with raw log/trace hashes and external
run/job links. Bind each comparison to its exact head, tested merge and runtime.
The two failed PR #456 attempts remain retained and cannot become passing
evidence because a later candidate succeeds.

## Residual uncertainty

Removing automatic Git maintenance does not establish that every possible
filesystem writer is excluded. A repeated unrelated cleanup error remains a
failure requiring its own diagnosis. Windows observations do not substitute
for Linux evidence, and a passing rerun alone does not prove the fix.
