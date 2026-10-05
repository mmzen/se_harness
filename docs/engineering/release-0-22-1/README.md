# Proposed evaluator 0.22.1 and plugin 0.2.6 release

Status: **preparation implemented; final candidate verification pending**.

The outcome is a public evaluator that provides standalone draft validation
and records the actual human behind an existing ownership label. This removes
the release dependency for Hosted Artifact Graph work. Explicit adoption and
amendment of the hosted pin follow publication; this package does neither.

## Approved preparation work

| Work | Result | Verification |
| --- | --- | --- |
| [WO-RLS-040](work-orders/WO-RLS-040.md) | Integrate the two verified evaluator corrections on an isolated branch from main; qualify the final candidate and prepare its exact release inputs. | [VER-RLS-036](verification/VER-RLS-036.md) |
| [WO-RLS-041](work-orders/WO-RLS-041.md) | Qualify and stage both plugin 0.2.6 packages before final release approval. | [VER-RLS-037](verification/VER-RLS-037.md) and existing VER-IAR-021 |
| [WO-RLS-042](work-orders/WO-RLS-042.md) | After the exact complete-release decision, execute and confirm all public surfaces. | [VER-RLS-038](verification/VER-RLS-038.md) |
| [WO-RLS-043](work-orders/WO-RLS-043.md) | Correct the native-test transition defect and requalify changed packages, preserving the original failure. | [VER-RLS-004](verification/VER-RLS-004.md) |

[REL-SEH-035](release/REL-SEH-035.md) selects the existing complete-release
route. The approved package reuses accepted product, distribution and delivery
definitions. No new policy engine, artifact type or release mechanism is needed.
The three original work orders separate candidate qualification, host-package qualification
and public observations so publication is not its own precondition.

Released 0.22.0 validation reports **zero errors**, with 61 existing repository
warnings. The planning checks cover 193, 15 and 30 proposed paths respectively,
with no uncovered paths or invalid declarations. These are preparation results,
not approval or an assurance verdict. The required assurance classification is
proposed in each work order; mmzen confirmed it and the released evaluator recorded the approvals.

## Exact scope

- Base: main at `82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1`.
- Integrate WO-HAG-002/003 source from
  `64b4feb0cbaff06111876a1d4c0cc35a6c814415`, with unchanged governing records
  and historical evidence. Do not merge the unfinished hosted branch wholesale.
- Include main's already-approved WO-DST-028 4 MiB dashboard correction. It is
  present in the proposed baseline but absent from the published 0.22.0 wheel.
- Final release membership: WO-HAG-002, WO-HAG-003, WO-DST-028, WO-RLS-040,
  WO-RLS-041 and WO-RLS-043. Require one new aggregate verified VREC at the final candidate.
- Deliver evaluator 0.22.1, plugin 0.2.6, current documentation, Pages and
  latest/last through one later frozen complete-release plan.
- Keep PR #535 draft and targeted at `codex/hosted-artifact-graph-inputs`.
  Preserve DEC-HAG-001, all accepted hosted pins and the incomplete hosted work.

## Recorded preparation approval

mmzen answered "Approve preparation and review publication", confirming the
seven artifacts and **required commit-bound verification**. The grant includes
ordinary review pushes and draft PRs from `codex/release-0-22-1` to
`mmzen/se_harness:main`, their later verification-decision updates, read-only
CI rehearsals, and the plugin review staging ref `codex/plugin-0-2-6-staging`.

This approves preparation and qualification. Human verification, merge and the
exact complete-release decision follow once their inputs are reviewable. The
complete-release decision can cover evaluator, tags, PyPI, Pages, documentation,
marketplace and listed receipts together. Provider-setting changes, adoption
and amendments to accepted hosted definitions require separate bounded review.

## Qualification evidence

The [evaluator review](evidence/WO-RLS-040/qualification-review.md) records the
preparation candidate, Windows/Linux checks, pinned builds and current provider
controls. The [plugin review](evidence/WO-RLS-041/qualification-review.md) records
the exact packages, native host observations and remaining desktop/walkthrough
criteria. WO-RLS-040/041/043 have implementation completion recorded; assurance remains pending. There is no final aggregate VREC
or release record yet.

The native Claude walkthrough found an evaluator transition crash, reproduced
on Windows and Linux. mmzen approved WO-RLS-043 and VER-RLS-004 with required
commit-bound verification and the exact manual linked amendment of REL-SEH-035.
The correction and amendment are applied. The previous accepted contract and
all original failure evidence are preserved.

The [current correction qualification review](evidence/WO-RLS-043/corrected-qualification-review.md)
records the corrected package identities, passing Windows/Linux and native CLI
checks and the then-pending desktop/provider criteria. Those three readiness
items are now resolved as recorded below; the original report remains a historical snapshot. The earlier evaluator/plugin
reviews describe the original preparation package, not the corrected wheel.
No final aggregate VREC or release record exists yet.

The draft preparation PR supports qualification and review. It does not request
verification or merge. The tested preparation commit and later evidence commits
remain distinct; final candidate capture will establish the release binding.

## Desktop decision and provider readiness

mmzen accepted [DEC-RLS-009 and RISK-RLS-007](evidence/WO-RLS-041/desktop-deferral-review.md)
for this release only. Codex Windows desktop remains **not run / unverified**;
CLI evidence does not replace it. Revisit before the next plugin release or any
verified-desktop claim, whichever comes first. Required CLI and public-route
checks, human verification and the final complete-release decision remain intact.

The separately authorized [pypi environment change](evidence/WO-RLS-040/provider-configuration-applied.json)
removed only the required reviewer. Readback confirms main-only deployment,
main protections and workflow permissions are unchanged. mmzen confirmed the
four PyPI Trusted Publisher fields. This is human account-side confirmation,
not an authenticated PyPI read by the agent. No release was dispatched.

The next preparation work is the exact marketplace staging commit and final
candidate verification. The required handoff and completion checks passed; the work orders are
`implemented`. Final candidate capture has not yet supplied human verification. This update supplies no verification,
merge, release or adoption decision.

## Known dependencies

The current governor remains released 0.22.0. Native and desktop test readiness
and independent provider controls must be checked during preparation. The bounded desktop omission for this release is recorded above; older
release-specific omissions remain historical. Missing required
results block the affected readiness claim until resolved through the proper
decision procedure. No new risk acceptance is bundled into this proposal.

After delivery, prepare explicit adoption and preserved linked revisions of
SPEC-HAG-003 and VER-HAG-001. Then use the adopted released decision command to
record mmzen's existing `extend-evaluator` choice with the correct owner binding.
The choice is already known; do not ask it again or fabricate a disposition.
