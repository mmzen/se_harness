# Change skill evidence

The plugin's `change` skill guides artifact packages and bounded work-order
execution through existing released commands. It adds no evaluator operation,
authority store, host registration or policy exception.

## Evidence map

| Evidence | What it establishes |
| --- | --- |
| [Independent Windows report](acceptance/independent-windows/REPORT.md) | Actual agent-directed CHG01â€“06 and CHG08â€“10 observations using released 0.16.0; fixed oracle, requests, raw calls, state readbacks and prompt counts. |
| [Case summary](acceptance/independent-windows/behavior-evidence/summary.json) | Exact observed cases and the limits of grouped variants. |
| [Retained file inventory](acceptance/independent-windows/retention-inventory.json) | Hashes of the copied observations and original/corrected skill bytes. |
| [Windows live guard cases](acceptance/live-guard-win-016-02/chg07-guard.json) and [Linux live guard cases](acceptance/live-guard-linux-016-02/chg07-guard.json) | The real 0.16.0 guard admits exactly three execution rights for a published passing commit, refuses four other rights, refuses branch-only delegation, and refuses a new unpublished head despite its parent's passing check. These are guard probes, not lifecycle applications. |
| [Current evaluator guard cases](acceptance/live-guard-win-05/chg07-guard.json) | The same nine observations with governing release 0.17.0 on Windows. |
| [Actual delegated start](governance/start/selection.json) | WO-PLG-010 was started by the released 0.17.0 evaluator after the exact live `validate` check passed and delegation existed at `origin/main`. |
| [Linux replay](acceptance/linux-replay-attempt2/summary.json) | 75 actual process calls using released 0.16.0 on WSL Ubuntu 24.04 / Python 3.12.3. Fixed Windows-observed actions replay correctly, including two scoped commits, package states, receipt readback and complete shared-handler delivery. This is command portability evidence, not fresh model behavior. |
| [Qualification limits](checks/qualification-limits.json) | The retained Windows regression cleanup failure and expected candidate/released template differences. |

## Corrections supported by observations

The initial instructions attempted definition readback through `check`, which
accepts WO/VREC/RLS/DEC targets, and introduced an evidence-dependent pre-action
check before ordinary edits. The corrected instructions read definition files
and lifecycle history directly, use edit-scope validation, and follow the
installed procedure's actual checkpoints. The observer repeated the affected
cases and confirmed the corrected skill hashes match the delivered files.

The corrected run performed two scoped edits and local commits with zero
duplicate approval/start prompts. It preserved draft/open creation states,
stopped changed or absent authority, refused an outside-scope edit, and recovered
from two deliberately lost tool receipts without replaying successful writes.
Readiness recovery reused an unchanged decision after setup and complete fresh
governance delivery.

The first Linux replay retained 47 successful calls before a test-runner
commit-count assertion used the moving local `main` ref. The corrected runner
uses the fixture's fixed `origin/main` baseline. Both attempts are retained;
this runner defect is not attributed to the product skill.

## Qualification boundaries

- These are shared-skill instruction observations and released-command
  fixtures. Native Codex/Claude registration, implicit discovery and live
  context transport remain separate work.
- The independent observer grouped the CHG02, CHG06 and CHG10 variants in one
  agent session. Linux command replay is separate from fresh model reasoning.
- Receipt-loss tests suppress acknowledgement after the real process exits.
  They do not claim an in-flight atomic-transaction crash test.
- The actual CHG07 live delivery begins with the retained start. Completion and
  ready-VREC preparation are later delivery steps; guard-only results do not
  claim those mutations occurred.
- Linux CI at `0600fb70` passed 1,134 source tests (four skipped). The local
  Windows run and unsandboxed retry each reached one unchanged test's Git-object
  cleanup error (23 skipped). Those failures remain visible; no out-of-scope
  test repair is included. The governing released doctor passes. Candidate
  0.18.0 doctor reports its expected template differences from managed 0.17.0.

No result here authenticates a human decision, verifies a VREC, grants external
authority, or demonstrates universal prevention of tool bypasses.
