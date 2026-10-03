# Plugin 0.2.5 qualification for verification

Both packages match the public evaluator 0.22.0 wheel. Package checks pass on
Windows and Linux. Native Codex CLI checks pass within the conditions below.
**Claude Code host tests and Codex Windows desktop tests are not run / unverified.**
Human mmzen instructed continuation with these omissions disclosed. DEC-RLS-005
and DEC-RLS-006 record that current-release decision and its paired risks.

## What the evidence establishes

| Contract / criterion | Observed result |
| --- | --- |
| VER-RLS-034: exact packages | Released-input builder and independent checker passed; both archives and inventories bind the public wheel. |
| Package and delivery suites | Windows: 62 tests, 2 skips. Linux: 62 tests, 1 skip. Skips remain visible. |
| VER-IAR-021: bootstrap and activation | Native Codex CLI starts above the checkout, then selects the exact cloned fixture and complete entry. |
| Native delivery and recovery | Codex CLI startup, manual and actual automatic compaction, and resume passed with retained session/resource identity. |
| Release/session isolation | Two selected releases, interleaved native sessions, explicit switch/clear and unavailable selection passed. |
| Portable failure boundaries | Both platforms passed the 41-step adapter checks, including expected refusals. Unit checks cover contention, atomic selection and invalid resources; these are not native host evidence. |
| Repeated work and delivery boundary | Native Codex CLI created a new draft and completed authorized existing work in both 0.22.0 and 0.20.0 fixtures. Exact notes, lifecycle history, local commits, handoff and empty remote refs were independently checked. |
| Claude and Codex desktop | Not assessed under the recorded current-release omissions; no verified-host claim. |
| VER-RLS-034: delivery inputs | The versioned five-surface plan retains exact source/wheel/package identities, prior plan digest and explicit tested-host boundary. |
| Full source qualification | Reuse verified VREC-SEH-032 for immutable source abbec12ac5524c8adfb28693f846dd59de88f759. No source or package bytes changed here. |

## Failures and limits

The original [progress report](review.md) and [raw archive](raw.zip) remain intact.
They retain PyPI index latency, the failed long-path Claude context check, the
first Linux environment prerequisite failure and expired Claude OAuth.
The same packages passed portable checks in a shorter temporary directory;
the failing long-path configuration is not claimed supported.

The native workflow also exposed a published-evaluator limitation: a separate
draft with a missing file in `evidence_paths` caused an unrelated start preview
to crash. The draft now describes the future file in its body and adds no
retained-evidence reference before the file exists. The normal workflow passed
under that condition. No published evaluator or accepted definition was changed.
The original crash and recovery are retained in RISK-RLS-006 for follow-up; no
acceptance of that separate risk is inferred. One command with undefined paths
was declined before execution, then retried with explicit paths. The new draft's
unconfirmed assurance classification stayed in prose rather than fabricated
decision metadata. These observations are not hidden by the successful retries.

The CLI test used synthetic fixture approvals and local bare remotes. It made
no public push or PR. Its disposable profile's original plugin was restored.
No credentials or ordinary host settings are included in retained evidence.

## Evidence and next decision

[qualification-v2.json](qualification-v2.json) maps results to exact raw hashes.
[native-workflow-raw.zip](native-workflow-raw.zip) retains the native event traces,
reviewed commands, fixture effects and independent assessment.
[delivery-plan-v2.json](delivery-plan-v2.json) names Codex CLI as native public-route
coverage while retaining both distributed packages and byte checks.

Prepare VREC-PLG-032 for this committed evidence, publish its review PR and
request the human verification decision. This report supplies no such verdict.
Marketplace publication, public-route checks and latest/last remain outstanding.
