# Repository adoption of 0.23.0 — approval review

## Decision requested

Approve implementation and review publication under
[WO-HUP-031](../../work-orders/WO-HUP-031.md) and
[VER-HUP-026](../../verification/VER-HUP-026.md), with required verification tied
to the exact final commit. Both records are drafts. Accountable human: mmzen.
Their reviewed contents and governing definitions are bound in
[reviewed-artifacts.json](reviewed-artifacts.json).

## Why and proposed changes

Public evaluator 0.23.0 and plugin 0.2.7 are delivered, but this repository still
selects evaluator 0.22.1. Adopt the published evaluator through its normal
installer, update the CI pin, and correct the named current documentation and
refresh-guidance test. Advance development source to unpublished 0.23.1 so CI
can distinguish candidate source from the independently released evaluator.

One work order and one verification contract reuse the existing upgrade rules.
The work-order table names all proposed paths, including the installer transaction
and fixed verification outputs. No new product mechanism is proposed.

## Observed preparation results

| Check | Result |
| --- | --- |
| Public identity | Digest-checked 0.23.0 wheel; independent delivery verified in VREC-RLS-005 and merged in PR #548. |
| Installer preview | Only `.engineering-harness.toml` and `.engineering-harness.lock` change. |
| Disposable Windows apply | Passed; target doctor and released-root qualification passed. |
| Repeat preview | No changes. |
| Owner preservation | AGENTS.md, Git attributes/ignore, PR template and CI bytes preserved by the installer. The CI pin remains a separate proposed owner edit. |
| Version boundary | Disposable evaluator 0.23.0 / development source 0.23.1 accepted by evaluator-facts. |
| Draft validation | 2,020 artifacts; zero errors; 65 repository maintenance warnings. No warning is treated as acceptance. |
| Planned paths | All 30 supplied paths covered; no uncovered path or invalid declaration. This does not prove completeness of impact analysis. |
| Approval readiness | Graph, integrity and decision gates pass. `QGS-ASSURANCE` awaits the human's confirmation of required commit-bound verification. |

Actual commands, exits and outputs are in
[preparation-checks.zip](preparation-checks.zip). It preserves the first sandbox
permission failures and the successful retries. Target setup's initial doctor
reported the expected old-selection mismatch; this was not an adopted-state pass.

## Success criteria

The actual checkout and CI select 0.23.0. Owner files and historical evidence
remain preserved. Required focused/full tests, distribution checks, two matching
upgrade rehearsals, scope/handoff checks and final candidate capture pass.
Publish the ready verification record and evidence in the review PR before
requesting human verification. Required CI must pass before merge.

## Approval scope

Approval permits the listed local changes, checks, session activation and
verification preparation. It also permits review pushes and a draft PR from
`codex/adopt-0-23-0` to `mmzen/se_harness:main`, the later verification-decision
push, and marking the PR ready after that decision is recorded remotely.
Human acceptance of the implementation and merge remain separate decisions.

Host-plugin updates and native/desktop tests are outside this adoption. Preserve
the accepted open findings R23-NATIVE-010/011 and desktop omission under
DEC-RLS-010/011 and RISK-RLS-008/009. The private HAG service remains pinned to
0.22.1; Git remains authoritative. No new release or provider change is proposed.

## Current state and next input

The real checkout still selects 0.22.1. WO-HUP-031 and VER-HUP-026 remain `draft`.
No implementation, lifecycle transition, push or PR publication occurred.
The evaluator's current step is `STEP-FOCUS-SELECTED`, with corrective input:
resolve `QGS-ASSURANCE` by obtaining the accountable human's classification.
Package approval can confirm that classification and authorize both selected
transitions. Passing preparation checks supplies neither decision.
