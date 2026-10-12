# Review: literal JSON pointers and precise native reports

The C42 runs remain incomplete. Their retained reports are in
[the full lifecycle assessment](../../WO-HAG-009/final42-result/assessment.md)
and [the focused assessment](../focused42-result/assessment.md).

This six-file correction is within WO-HAG-011's approved test-driver and
instruction paths:

- Preserve literal JSON pointers in Windows Claude child processes with
  `MSYS_NO_PATHCONV=1`. No host configuration or permission rule changes.
- Return exact small failure lists with observation summaries. Keep full snapshots
  and explicit pointers for larger lists. State that later calls are excluded.
- Clarify that reports include local recovered errors and later snapshot-read
  failures, and distinguish the test runtime from the lifecycle evaluator.
- Clarify the existing scope review: compare each generated path, including a
  paired record, to `execution_scope.paths`. A prose note adds no path.
- Distinguish REL definition approval from the RLS release decision. Supplied
  decisions determine the actor; an artifact owner field grants no right.

No evaluator, service, protocol, dependency, fixture outcome, host permission or
qualification criterion changed. The helper neither authors artifacts nor selects
the workflow. These changes address observed failures without another framework.

Validation: 1,339 source tests, 24 reported skips; 52 native checks, one skip;
28 resource checks, two skips; 11 plugin checks, one skip. Distribution and CLI
checks passed. Released validation: 1,991 artifacts, zero errors, 63 existing
warnings. Scope and both review preflights passed. The initial sandboxed resource
check failed on atomic hard-link creation in disposable files; its log is retained
beside the successful permitted rerun.

The next candidate needs fresh native results. Start the focused sequence with
Claude's missing-input case and review it before proceeding. Keep the PR draft
and all three work orders in progress. No assurance, merge or release is claimed.
