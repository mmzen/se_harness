# Approve repository adoption of evaluator 0.22.0

**Decision requested:** Approve [WO-HUP-028](../../work-orders/WO-HUP-028.md) and
[VER-HUP-005](../../verification/VER-HUP-005.md), with required verification tied
to the exact implementation commit, plus the described review-branch push/PR.

## What will change

- The installer updates **two files**: configuration and lock select the exact
  public 0.22.0 wheel released under RLS-SEH-032.
- The owner-maintained CI version pin becomes **0.22.0**.
- Both development-source version fields become **0.22.1**, unpublished. This
  prevents CI from confusing the candidate with the selected release.
- Seven current guides/indexes state the adopted release and completed public
  delivery. The complete-release route still needs separate provider configuration.

[The proposed patch](proposed-adoption.patch) shows all twelve implementation
files. The formal records, canonical upgrade transaction and planned
VREC-HUP-027/evaluator evidence are also inside the declared scope.

## What has been checked

The exact published wheel is prepared in a separate private environment. A
disposable checkout passed upgrade, doctor, resource lookup and an unchanged
repeat preview. All retained integrations remain selected. No copied instruction
file is recreated or retired by this upgrade.

The rehearsal reproduced PRE008 while evaluator and source were both 0.22.0.
Source 0.22.1 resolves it. **127 tests ran successfully, with two skipped** across
the focused and public-onboarding suites. The proposed README is 645 words.
Draft validation reports **zero errors** and 61 existing repository warnings.

Preflight correctly remains pending: the work order and verification contract
are draft, and the human has not yet confirmed required commit-bound assurance.
These are the only selected preflight findings.

[Checks and limitations](proposal-checks.json) identify the raw evidence archive,
including the earlier failed preparation invocations. The full source suite,
real candidate qualification and hosted checks run after approval; the rehearsal
does not verify the eventual adoption candidate.

## Boundaries and next steps

The working repository remains on **0.21.0** until approval and installer apply.
AGENTS.md, historical records and frozen evidence are preserved. This work does
not update the host plugin, refresh credentials, change provider settings, publish
0.22.1 or activate the single-approval release route. Claude Code and Codex Windows
desktop remain unverified by this adoption.

Approval permits the listed implementation, checks and verification preparation,
and a review PR from `work/adopt-0-22-0` to `mmzen/se_harness:main`. The agent will
publish the implementation before requesting your verification, then push your
recorded decision. Your final verification and merge remain separate.
