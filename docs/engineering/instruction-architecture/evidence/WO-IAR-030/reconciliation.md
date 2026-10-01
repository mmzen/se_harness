# Minimal-layout reconciliation with adopted 0.20.1

The saved implementation is reconciled on `work/reconcile-minimal-resources` at local commit
`c1bcbfb8e053ee8099e98b1dc34fcf547adc46eb`. The merge preserves the saved commit `6dd70f29cd43ffc230779d61ee1a7ced43a7a611` and
adopted main `d0157d969d0e3c2d5ed58d218c74abcd28592248` as parents. Nothing was pushed.

## Preserved material

The original checkout and all its uncommitted files are unchanged. Copies of
its dirty and untracked files are retained outside the repository with digests.
The reconciled branch includes the saved IAR decision and evidence. Earlier
untracked maintenance-release drafts remain in the saved checkout; they did
not replace main's accepted release records.

The installed root, owner AGENTS.md, configuration, lock, conditional guides,
CI evaluator selection and accepted release records match adopted main.
The real repository still uses the released 0.20.1 repository-copy layout.
The 0.21.0 minimal layout remains a candidate tested in disposable repositories.

## Changes needed by the merge

Two documentation conflicts were resolved in the installation guide and
marketplace publication guide. Current public 0.20.1 / plugin 0.2.3 facts and
unreleased minimal-layout instructions remain distinct. The README and developer
guide now use the adopted baseline. No product-code conflict required a change.

## Checks

| Check | Result |
| --- | --- |
| Released evaluator identity and installation | Passed for exact public 0.20.1. |
| Formal validation | Zero errors; 54 existing warnings. |
| Initial full suite | 1,209 tests; one README length failure; 20 skips. Failure retained. |
| README correction | All 16 onboarding tests passed; the existing limit was kept. |
| Final full suite | 1,209 tests; no failures; 20 skips. |
| Release distribution validation | Passed for all 20 distribution-bearing records. |
| Windows candidate-package qualification | Passed using released 0.20.1. |
| Linux candidate-package qualification | Passed using the same wheel and released 0.20.1. |
| Linux installed package | Minimal init, empty validation, repeat init, package resources, domain creation, owner preservation, draft creation and actual symlink/path refusal passed. |
| Complete Git scope | Blocked: DEC-IAR-004.md is outside existing approved paths. |

The independently built, non-promotable candidate wheel has SHA-256
`66467146b32853ce87d7a782a9452aca8e20ead4ba4cb07837ec16c518aa784d`. Both platform qualifications bind
that wheel to `c1bcbfb8e053ee8099e98b1dc34fcf547adc46eb`. This resolves the released-0.20.0 acceptance
runner incompatibility that led to DEC-IAR-004. It is not a release build.

## Required next decision

The evaluator reports QGP-G4I-PATHS / WEX201 for the transported DEC-IAR-004.
[WO-IAR-038](../../work-orders/WO-IAR-038.md) proposes that exact scope correction
and required verification within VREC-IAR-020. The draft validates. Its assurance
classification awaits mmzen; no approval or start is recorded.

The selected implementation work orders remain `in_progress`. The evaluator's
current blocked step is `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`:
escalate the uncovered decision path to the accountable owner under
`DR-REMEDIATION-SCOPE`. A passed package qualification does not override it.

## Qualification limits

VREC-IAR-020 has not been prepared. Complete handoff and the remaining integrated
criteria still need assessment after the scope gap is resolved. Codex Windows
desktop delivery remains unverified. Historical native CLI evidence is retained;
this reconciliation adds no claim of native delivery for the final wheel.

The original accepted contracts retain their 0.20.0 wording. The later recorded
DEC-IAR-004 sequence and separately approved WO-HUP-025 adoption establish the
new selected evaluator; reconciliation does not rewrite that history or waive
verification criteria. No verification, release, push, PR or publication decision
was applied.

[reconciliation.json](reconciliation.json) retains the actual checks, candidate
identities, original failures, scope finding and draft validation.
