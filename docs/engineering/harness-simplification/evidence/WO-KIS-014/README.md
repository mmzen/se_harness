# WO-KIS-014 continuation, 2026-09-20

State: **in_progress**. The owner approved the exact replacement draft and
closure of WO-KIS-010 with "Approve replacement scope and closure". Released
0.18.0 applied WO-KIS-014=approved and WO-KIS-010=rejected atomically, then
applied start for WO-KIS-014 after passing start checks. Old approval and start
events, partial code and retained evidence are preserved.

## Changes made

- Applied the reviewed tests/test_workflow_execution.py fixture correction.
  Completion tests now use a declared manual check and the real capture API,
  while preserving their separate completion/integrity assertions.
- Updated docs/notes/diagnostic-codes.md using the previously reviewed generated
  diff. No new code family, generator, service or runtime behavior was added.
- Reviewed the retained WO-KIS-010 implementation against SPEC-KIS-004 and its
  KISS constraints. The design explanation and E1–E5 cases remain in that
  order's evidence summary and tests/test_workflow_compliance.py.

## Actual checks

| Check | Observed result |
| --- | --- |
| Windows, Python 3.14.6 | 1081 tests; 12 failing onboarding assertions; 15 skipped |
| Ubuntu 24.04 on WSL, Python 3.12.3 | 1081 tests; the same 12 failing onboarding assertions; 2 skipped |
| Failure comparison | Both failure sets exactly match the starting-commit onboarding failures retained under WO-KIS-010 |
| Repair regression cases | No failures in either full-suite run, including the corrected completion fixture and diagnostic index |
| Distribution provenance, CLI help and candidate graph | Passed |
| Released doctor, graph, review and complete actual scope | Passed |
| Candidate doctor/review | Refuse the expected candidate 0.19.0 versus governing 0.18.0 identity mismatch |
| git diff --check | Passed |
| Hosted CI | Not run; local Windows/Ubuntu runs do not claim a hosted verdict |

The full suites are NOT passing. These are all discovered tests at the normal
reduced scale, using the repository runner. The hosted source job uses Python
3.11 and --scale full; that exact CI route has not been run. No passing CI or
package-install acceptance is inferred from local source tests.

The first Linux attempt on the Windows-mounted checkout was interrupted after
the workers spent time waiting for file I/O. A setup attempt that still scanned
mounted Git files was also interrupted. Neither attempt is counted as passing.
The completed Linux run used an isolated native /tmp checkout of the same HEAD,
reconstructed from a local Git bundle plus the four changed working files.
The overlay and bundle hashes were verified before execution. Original source,
other processes and branches were preserved. Setup/input logs are retained.

The first completed native run had 13 failures: the 12 known onboarding
assertions and one dashboard test that requires the source repository URL.
Cloning a local bundle sets origin to a file path, so that metadata differed
from the source checkout. The final run restored the source origin URL in the
temporary checkout's Git config only; no network operation or source change
was needed. The prior temporary directory was no longer available when
reused, so the same verified bundle and overlay were reconstructed in a new
temporary directory. Both completed-run logs are retained; only the final
corrected-setup run is reported in the table above.

Commands, runtime details and full output are in logs/. Tested working bytes
are listed in tested-working-inputs.json. A later local save commit does not
convert these records into commit-bound assurance.

## Remaining blocker

The four PublicOnboardingTests methods report 12 missing README onboarding
assertions: checker CLI examples, environment/version guidance and two guide
links. They reproduce at the starting commit and are unchanged by this repair.
README.md and tests/test_public_onboarding.py are explicitly outside this
approved continuation. No tests were removed or weakened, and no unrelated
README change was applied.

WO-KIS-014's approved text requires a separate bounded owner decision if those
failures keep blocking acceptance. The selected order remains in progress.
Do not record completion or a VREC based on an attachment-presence pass while
the required suite remains failed. Local execution approval is not assurance
acceptance, independent review or permission to push/merge/publish.

The final proposed-baseline-scope result is a read-only probe of README.md as
a possible remediation path, together with the complete current changes.
It is not a claim that README.md was changed. Actual scope passes separately.
Its typed next response escalates that additional path to the engineering owner
under DR-REMEDIATION-SCOPE. No additional approval has been inferred.
