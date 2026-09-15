# Owner release authorization

On 2026-09-15, the owner replied:

> i authorize

The selected decision was: "I authorize release record RLS-SEH-027."
The installed 0.17.0 evaluator applied the release-owner decision to that
record only. RLS-SEH-027 is released for checker 0.18.0 at candidate
353da23881fdf045a52322a313c1e67341f7a9b1. Its verified scope and bound distribution hashes
are unchanged.

The [ready-record replay](https://github.com/mmzen/se_harness/actions/runs/34939337745),
independent review and release-decision gate passed. All checks on reviewed
head 4d7d4410f5778539fe3a8136543532c4bd633781 passed or were intentionally
skipped before the decision. Earlier preparation evidence preserves its
observed ready state.

This records authorization, not a public package. PR #480 must be merged
before the existing publication workflow can use this released record from
main. No merge, tag, publication, live installation or root upgrade was
performed by this transition.
