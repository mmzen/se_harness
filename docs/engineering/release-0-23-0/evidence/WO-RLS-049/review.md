# Proposed correction after the Claude diagnostic

**Decision requested:** approve WO-RLS-049 and required commit-bound verification,
the exact one-file instruction correction and linked REL-SEH-036 membership
amendment, with inclusion in the existing PR #544 review-publication grant.

The failed run is preserved in the [qualification report](../WO-RLS-045/qualification-progress.md).
It missed the user's operational need and falsely reported no failures after a
failed local read. The supplied instructions already contained the relevant rules;
no missing package file explains this result. The correction below is a bounded
instruction-ordering proposal, not a proven root-cause fix.

1. Move the existing intent-input paragraph next to the clarification action.
   Keep missing facts explicit instead of drafting a guessed outcome.
2. Make the existing failure check common to both report forms. Include failed
   reads and recovered failures; reuse complete retained observations.
3. Use the supplied absolute selection path instead of guessing from a filename.

Read the [exact diff](hosted-drafts.patch) or [complete proposed file](hosted-drafts-proposed.txt).
The [work order](../../work-orders/WO-RLS-049.md) contains the scope and verification.
Only one product file changes. The existing package map, test driver and content
criteria stay in use. There is no new helper, approval step or test-specific answer.
The [byte binding](review-binding.json) fixes the reviewed inputs.

The installed evaluator cannot generically amend an accepted definition. The
explicit manual amendment adds only WO-RLS-049 to REL-SEH-036.gates; its complete
accepted bytes and lifecycle history are preserved. This proposal is unapplied.

After approval, build a new candidate and run the unchanged first Claude
diagnostic. Stop on failure. On a pass, resume the existing qualification sequence.
Preserve this candidate's failures and do not combine performance samples across
candidates. Required desktop evidence remains pending; no deferral is requested
or inferred by this correction. Human verification, merge and the final exact
complete-release decision remain separate.
