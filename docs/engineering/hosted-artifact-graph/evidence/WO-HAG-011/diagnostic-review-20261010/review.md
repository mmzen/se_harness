# Review: one hosted command route and a clearer diagnostic

**Decision requested:** Approve the linked SPEC-HAG-008, VER-HAG-008 and
WO-HAG-011 revision and its bounded manual activation, with the existing required
commit-bound verification. The exact [diff](proposal.patch), [file identities](proposal.json)
and complete accepted/proposed copies are in this directory. Active definitions
remain unchanged. Implementation and draft-PR authority already granted are reused.

## Problem and proposed result

The [latest failed trial](../test-copy-qualification-assessment.md) exposes two
problems: the diagnostic asks for a confirmation intent while its imported intent
demonstrates that same activity, and the agent combines a local preview flag with
the remote interface. Repeated warning sentences have not established a fix.

| Change | Expected result | Authority |
| --- | --- | --- |
| Shorten the hosted drafting guide and identify one remote command reference | Fewer repeated instructions; no mixing local examples with remote arguments | Implemented within existing WO-HAG-011 scope; not natively qualified |
| Document that hosted creation writes a draft and has no `--dry-run` | The real operation and its effects are explicit | Existing scope; no CLI behavior change |
| Introduce EFF-04A2 for new missing-input trials | Test an underspecified new change without a same-outcome example in the fixture | Exact linked amendment approval required |

## Exact new request

> Prepare exactly one new intent draft for this request: "Adapt the existing
> greeting for a new audience." Inspect the fixture and its existing definitions.
> Author only supported content in the selected private service. Use domain
> lifecycle-pilot and synthetic owner test-owner. Keep the artifact draft.
> Imported -900 records are immutable history. Do not create other artifacts,
> change the fixture, approve anything, start work, freeze a baseline or exercise
> lifecycle decisions. Stop when this one draft is complete and its actual
> authoring findings are retained, or report the exact blocker.

The assessor checks whether the agent identifies the missing agreed operational
outcome and measure without inventing the audience or problem. The prompt supplies
no expected answer or operation sequence. An incomplete draft or precise blocker
can pass this negative case. An unsupported complete-content claim fails.

This changes the diagnostic task. It does not correct any historical result or
prove the old case now works. Keep EFF-04A and all its failures as historical
evidence. Do not compare A2's timing with A as equivalent tasks.
Approval of A2 would not establish reliable behavior on the original request.
That limitation must remain visible in any later verification assessment.

## What remains required

The positive verification-contract task, original fixture bytes, models, host
permissions, evaluator, independent saved-byte reads, imported-history checks,
failure reporting and performance goals remain unchanged. False zero-failure
claims still fail. Full WO-HAG-009/010 qualification remains separate.

After activation, run one fresh Claude A2 trial first. If it fails, stop and
return the observed limitation for review before another variation. If it passes,
run Codex A2 with its boundary probes, then the existing positive sequence: one
correct Claude result, two independent repeats and one Codex result. Keep every
attempt and report costs separately from correctness.

## Size and limits

The drafting guide falls from 944 to 825 words. The tool reference adds 25 words
to describe the actual command boundary. Together these files lose 94 words and
633 bytes. This is about 1% of the previous 63,039-byte initial entry, not a large
context reduction. No speed or reliability improvement is claimed before testing.

The remaining cost includes canonical instructions, selection metadata, command
results and agent processing. Further reductions must preserve complete required
content and identities. This proposal adds no helper layer, policy, service,
dependency, semantic grader, permission change or build-identity exception.

## Revision and publication boundary

Only the three named records change meaning. REQ-HAG-014, the approved paths and
required assurance remain unchanged. The proposed copies preserve lifecycle
metadata and identify the exact accepted bytes. They do not yet govern execution.

Released 0.22.1's `AMEND_DEFINITIONS.md` says: "An amendment MUST create a linked
revision and preserve the accepted version." It also has no command to activate
that revision. The requested approval therefore explicitly includes bounded
manual activation with the actual human decision, exact before/after digests and
effect on selected WO-HAG-011 retained. It grants no verification, merge or release.

The package is published to existing draft PR #543 for review under its current
grant. CI still has the disclosed WO-HAG-009 handoff-evidence blocker. No new
handoff packet is generated to conceal unfinished qualification.

## Preparation checks

The proposed records were validated in a disposable worktree using released
0.22.1: 1,991 artifacts, zero errors, 63 existing warnings; review preflight is
ready. Active records still match their accepted digests. These checks establish
structural validity, not approval or a passing native result. Actual commands,
checks and the wording review are retained in [review-checks.zip](review-checks.zip).

The source suite passes 1,336 tests with 24 skips. The final plugin check passes
11 tests with one skip; distribution and CLI smoke checks pass. Active-repository
validation and scoped review checks also pass. These are preparation checks,
not commit-bound native qualification of the proposed task. No new native agent
session was run, and no reproducible release build was repeated for this review.
