+++
id = "VER-RLO-011"
type = "verification"
title = "Verify one approval completes bounded release delivery"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[relations]
verifies = ["REQ-RLO-021", "REQ-RLO-022", "REQ-RLO-023"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T20:17:28Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package, verification and review PR\" to the exact package review for WO-RLO-014/015/016 and their governing definitions, with required commit-bound verification under VER-RLO-011. This authorizes bounded implementation, local checks and commits, completion and verification preparation, ordinary review-branch push and draft PR from work/complete-release-approval to mmzen/se_harness:main, and its later verification-decision update. Human verification acceptance, merge, actual releases and the exact live configuration change remain separate. The selected released evaluator 0.21.0 governs this work. Reviewed draft SHA-256 cccf71c49b14afbf83d5e9fb01addf7cdbe84b8210bc98b76b008e82cb54dca6; approved transition input SHA-256 cccf71c49b14afbf83d5e9fb01addf7cdbe84b8210bc98b76b008e82cb54dca6. Only the confirmed WO assurance fields were added before this transition."
+++

# Verify one approval completes bounded release delivery

## Independence

Expected actions, identities and refusal cases derive from REQ-RLO-021 through
REQ-RLO-023 and SPEC-RLO-007. Use fixture payloads and provider responses fixed
independently of candidate output. Read actual public inputs independently when
assessing readiness; a candidate's pass claim is not evidence of its own authority.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-RLO-021 | test, inspection, demonstration | ONE01, ONE02 | One explicit complete approval covers only the listed actions; old or changed authority refuses. |
| REQ-RLO-022 | test, inspection | ONE03, ONE04 | Both host packages qualify before publication; public wheel and immutable payload identity remain exact. |
| REQ-RLO-023 | test, inspection, demonstration | ONE05 through ONE08 | All outputs are rehearsed, failures resume safely, controls are assessed and completion is honest. |

## Cases and procedure

| Case | Execute | Expected result |
| --- | --- | --- |
| ONE01 — One response | Exercise release and external-action workflow results and the agent-facing procedure with a ready complete package and one retained human response. | The RLS transition and listed external grants remain distinct but use the same decision; no additional permission prompt for a matching step. |
| ONE02 — Narrow authority | Exercise a legacy RLS-only decision, missing plan, changed plan digest, changed candidate, destination and extra action. | No inferred authority; each unmatched action stops with the exact missing input. Passing checks alone never supply a grant. |
| ONE03 — Staging | Build and check the Codex and Claude plugin packages from a verified retained candidate wheel before a public RLS/wheel exists. Repeat with missing or incorrect provenance and run legacy builder cases. | Valid staging succeeds without publication; invalid input refuses; released-input checks remain required in the legacy path. |
| ONE04 — Identity | Simulate public wheel match and mismatch; apply a release decision and attach governance receipts while holding payloads fixed. | Marketplace promotion requires the approved wheel/payload digests; governance-only changes do not silently rebuild or replace payloads. |
| ONE05 — Whole delivery | Run the existing credential-free release rehearsal extended with marketplace, docs, pages, maintenance branch and marker stages. | Expected actions and destinations are exact; required public checks precede latest/last; all outputs appear in the report. No live publication is used as a test. |
| ONE06 — Recovery | Interrupt after each distinct external boundary; supply exact, absent, partial, conflicting and unknown state, including unexpected marketplace parent movement. | Inspect before retry; preserve completed actions; resume missing valid steps without a new approval; conflicts and failed checks leave delivery incomplete. |
| ONE07 — Controls | Inspect workflow permissions, candidate/credential separation, OIDC and protected refs; rehearse the proposed provider configuration diff and its recovery from sanitized snapshots. | No credential-bearing candidate execution, extra secrets or bypass; the exact reviewer-only change preserves other controls. Missing live readiness stays explicitly unverified. |
| ONE08 — Readiness and history | Run complete/incomplete delivery fixtures, required-check-unavailable cases, legacy records and the rollout procedure. | No false complete result or retrospective grant. The selected released evaluator governs rollout; candidate instructions do not govern themselves. |

## Platforms and checks

Use the repository-selected isolated 0.21.0 evaluator for formal preparation,
validation and gates until a separately authorized adoption changes it. Test
candidate product code with the repository's supported Python runtime. Run focused
workflow, plugin-package, publication, delivery and CI policy tests on Windows and
Linux, then the ordinary full suite and existing required CI checks. Extend the
existing release rehearsal rather than introducing a duplicate pipeline.

Required live host qualification for an actual future release remains in that
release's contract. These implementation tests do not claim public installation
or waive unavailable desktop or authentication evidence.

## Evidence retention

Retain commands, exit codes, candidate commits, fixture expectations, raw outputs
and relevant digests under each selected work order's evidence directory. Keep
large repeated outputs in bounded archives. Use existing capture-verification
to prepare commit-bound verification records; human acceptance remains separate.

WO-RLO-014 covers ONE01 through ONE04 and the product aspects of ONE08.
WO-RLO-015 covers ONE05, ONE06 and the integrated aspects of ONE07/ONE08.
WO-RLO-016 covers the live read-only configuration inventory and proposed change
in ONE07. Its result is an activation-readiness assessment, not a claim that a
live setting was changed. Report unavailable platform checks as gaps.
