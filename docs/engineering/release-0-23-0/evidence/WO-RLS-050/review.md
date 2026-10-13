# Proposal: one content-readiness decision

**Approve WO-RLS-050 and required verification**, including the exact linked
REL-SEH-036 membership amendment and the existing PR #544 review-publication grant.
The instruction edit and release amendment are **unapplied**.

## What this fixes

Claude saved a draft and called its content complete while required operational
inputs were missing. It also supplied unsupported problem and scope statements.
The [independent assessment](../WO-RLS-046/candidate-f2ddb5af-claude-assessment.json)
and [qualification report](../WO-RLS-045/qualification-progress-f2ddb5af.md)
retain that failure. No tool failed in this diagnostic, so it does not test the
earlier correction's handling of a failed tool call.

The instructions already contain the rules, but their readiness guidance is
scattered. This is a wording correction to test, not a proven root-cause fix.

## Exact change

Only `plugins/verity-plane/common/skills/change/references/hosted-drafts.md` changes:

1. Use one table: missing required input → incomplete; omitted supplied input →
   correct the draft; supported complete content → complete; assessment blocked →
   report the limitation.
2. State that saving, an empty `incomplete` list and `content_review: not_assessed`
   do not establish content completeness. A partial draft may remain saved.
3. Point the final report back to that same decision; remove repeated wording.

Read the [exact diff](hosted-drafts.patch) or [full proposed file](hosted-drafts-proposed.txt).
Length is nearly unchanged: 1,529 → 1,532 words. No new helper, policy layer or
tool call is introduced. No duration or context improvement is claimed before testing.
Both hosts use the existing shared package file. The test task, model, source
fixture, permissions and acceptance criteria remain unchanged.

## Verification after approval

Build a new exact candidate and run one fresh Claude diagnostic. Stop if it
fails. If it passes, continue the already required Codex and positive drafting
cases, then remaining release qualification. Preserve all previous failures.
Use the existing aggregate commit-bound verification record; no separate
verification layer is added. Desktop evidence remains independently pending.

## Authority and limits

The prior WO-RLS-049 approval identified different exact instruction bytes.
This proposal therefore needs new authority for the replacement text.
The [new work order](../../work-orders/WO-RLS-050.md) defines the full scope.

The installed evaluator cannot generically activate a linked definition revision.
The requested bounded manual amendment adds **only WO-RLS-050** to REL-SEH-036's
gates, preserving and linking its accepted version and all lifecycle history.
Review the [one-line amendment](REL-SEH-036.patch) and [byte binding](review-binding.json).
Neither accepted definitions nor product instructions have changed in this proposal.

Approval includes this correction in review pushes to `codex/release-0-23-0`
and PR #544 targeting `main`, including a later separately given verification
decision. Human verification, merge, complete-release approval, desktop omission,
adoption and host updates remain separate.

## Preparation checks

Released 0.22.1 validates 2,006 artifacts with **zero errors**, 63 existing
warnings and no advisories. All 16 planned paths are covered, with no invalid
declarations or uncovered path. The evaluator reports WO-RLS-050 as `draft`;
its checkpoint-free next step is `PROC-FOCUS-SELECTED / STEP-FOCUS-SELECTED`
(`harnessctl check REPO --artifact WO-RLS-050`). This is context, not approval.

The first draft creation was blocked by the Windows sandbox's atomic-file
permission. The destination was confirmed absent before the same released
command created it in the permitted host context. Initial validation also
rejected a partial assurance table: no human has yet confirmed its classification.
The table was removed and the required classification remains an explicit proposal
in the work-order text. The corrected validation and scope checks pass. Original
and corrected command records are retained in [proposal-checks.zip](proposal-checks.zip).
No native rerun or implementation has occurred.
