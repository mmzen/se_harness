# Proposed evaluator 0.22.1 and plugin 0.2.6 release

Status: **preparation approved by mmzen; qualification in progress**.

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

[REL-SEH-035](release/REL-SEH-035.md) selects the existing complete-release
route. These seven drafts reuse accepted product, distribution and delivery
definitions. No new policy engine, artifact type or release mechanism is needed.
The three work orders separate candidate qualification, host-package qualification
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
- Final release membership: WO-HAG-002, WO-HAG-003, WO-DST-028, WO-RLS-040
  and WO-RLS-041. Require one new aggregate verified VREC at the final candidate.
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

## Known dependencies

The current governor remains released 0.22.0. Native and desktop test readiness
and independent provider controls must be checked during preparation. Earlier
release-specific omissions are not accepted for this release. Missing required
results block the affected readiness claim until resolved through the proper
decision procedure. No new risk acceptance is bundled into this proposal.

After delivery, prepare explicit adoption and preserved linked revisions of
SPEC-HAG-003 and VER-HAG-001. Then use the adopted released decision command to
record mmzen's existing `extend-evaluator` choice with the correct owner binding.
The choice is already known; do not ask it again or fabricate a disposition.
