```toml
artifact = "WO-CIP-010"
checkpoint = "handoff"
formal_snapshot_sha256 = "c91f72a391a7cfc08f1b9b3cc93f9bd89cb886a9f81f274f185ceaa55e64ead7"
rebound_at = "2026-09-12T10:20:49Z"
```

# WO-CIP-010 implementation evidence

The released 0.17.0 evaluator generated the binding above. The operator
approved WO-CIP-010 and VER-CIP-006, implementation, Linux/Windows CI and a
separate repair PR with "Approve both and proceed" on 2026-09-12.

## Problem and diagnosis

[Issue #269](https://github.com/mmzen/se_harness/issues/269) was closed as
unreproducible on 2026-09-08. The same `.git` directory-not-empty teardown
error occurred in both attempts of PR #456 run 34686202700, jobs
103533661141 and 103533878695. Their raw logs remain outside this checkout.
All handover evaluator stages completed before these cleanup failures.

The Windows analysis exported PR #456 head
`fef18f3188febf95049c6ede077f68178cccb13f` with Git 2.52.0.windows.1 and Python
3.13.3. The unchanged export launched maintenance, garbage collection, repack
and pack-objects; 7,523 objects ended in a pack. The proposed settings produced
the identical tracked tree with 7,523 loose objects and no maintenance child.
`process-observations.json` retains command observations and raw trace hashes.
These were analysis exports, not hosted repair-candidate replays.

Windows waited for maintenance to finish. Git 2.55.0's
[maintenance implementation](https://github.com/git/git/blob/v2.55.0/builtin/gc.c)
can detach before running background tasks, and its
[launcher](https://github.com/git/git/blob/v2.55.0/run-command.c) honors
maintenance.auto. This supports the Linux race mechanism; the old failed job
logs alone do not identify the writer. Hosted repair evidence remains separate.

## Change and controls

The rehearsal writes maintenance.auto=false and gc.auto=0 immediately after
initializing its disposable Git repository, before staging or committing.
The shared fixture launcher applies the same settings per invocation.
No user/global Git configuration or operational checkout is changed.

The real-Git regression enables an inherited loose-object maintenance task.
Both the fixture and actual rehearsal exporter suppress its launch. Enabling
maintenance explicitly in a foreground positive control must launch
pack-objects and create a pack; an insensitive fixture cannot pass. The test
also checks the parent configuration bytes and clean tracked content.

Other cases preserve UTF-8/binary output, identity, signing and Git failures.
Each rejected rehearsal configuration stops before staging/commit and reports
the failed timing stage. Existing evaluator failures and the injected cleanup
error retain their failures. There is no cleanup retry or ignored exception.

## Local checks

`local-checks.json` records exact commands, source hashes, exit statuses and raw
output hashes. The first normal full suite had one checkout-format failure;
its unmodified final summary is:

```text
----------------------------------------------------------------------
Ran 1163 tests in 576.328s (184 classes, 8 workers)

FAILED (failures=1, skipped=23)
```

The sole failure was the unchanged AGENTS.md owner-region byte budget:
Windows CRLF checkout yielded 6,024 bytes against a limit below 6,000.
The file differed from HEAD only in line endings. Restoring the exact committed
LF bytes produced no Git diff; all 10 tests of OwnerInstructionRegionTests then
passed. The full run's other tests, including the cleanup regressions, passed.
The failed full-run output remains retained. The hosted Linux suite will supply
the complete candidate run on committed bytes.

Candidate validate/help, distribution validation, released doctor/validate and
review preflight pass. Candidate-source doctor reports exactly the six existing
0.18.0-versus-0.17.0 managed-template differences listed in the JSON; released
integrity passes. Managed files are unchanged.

The first focused development run had one misplaced assertion in the new test
(NameError). The assertion was restored to its original test; both affected
tests passed and the subsequent full suite covers the corrected source.
The failed development log is retained outside the checkout, not relabelled.

## Hosted acceptance and scope

Implementation head `73cd1b4a4f62efa1c260863e60901fa9a321f79b` passed all 17 checks on
[PR #459](https://github.com/mmzen/se_harness/pull/459).
Run 34688718324, attempt 1, tested merge `9a9e844af85d2da69cf1ec6158991dfffc8d27b6`.
The Linux full-scale source suite passed 1,163 tests with 4 skips in 27.506s,
including the same real-Git positive controls that passed locally on Windows.
Managed validation, package acceptance, both publication rehearsals and both
integration-package platform checks also passed.

| Platform | Replay | Total seconds | Cleanup seconds | Verdict |
| --- | --- | --- | --- | --- |
| Linux | 1 | 11.421 | 0.410 | pass |
| Linux | 2 | 11.274 | 0.409 | pass |
| Windows | 1 | 30.386 | 2.755 | pass |
| Windows | 2 | 30.283 | 2.643 | pass |

All four results have semantic digest
`400b4712935c72fe70040cd372c6c1e988edfc8a3c97df99b730dacbcd84be87`.
Both new configuration stages and cleanup finished in all four replays; all
six evaluator checks retained their expected outcomes. Runtime facts, original
result/timing JSON, hashes, check URLs and run identities are retained in
`hosted/` and `hosted-checks.json`. Cross-host durations are observations,
not a controlled performance comparison.
Git storage uses UTF-8/LF; the index records both retained and original-download
hashes. Original downloaded bytes remain outside the checkout.

This evidence binds the implementation head above. The later commit adding
these records has its own normal PR checks, which must finish before delivery.
Historical release replays continue to execute their exact old candidate;
this repair does not rewrite their fixture code.

Only WO-CIP-010 paths change. PR #456 and #457 and their verified records remain
unchanged. WO-CIP-010 is in_progress; this packet does not record completion,
VREC preparation, verification, merge or release.
