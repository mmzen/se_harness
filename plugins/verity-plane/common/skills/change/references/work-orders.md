# Work orders

Select one WO. Use `check REPO --artifact WO-ID --json` without a checkpoint
to inspect its state and procedure. Read its approved behavior, exact path
scope, constraints, verification contract and the phase reading manifest.
Projection itself is read only and establishes neither readiness nor authority.

## Approval and start

Approval and start are separate decisions. Apply only the selected transition
covered by the operator; approval alone leaves a WO `approved`.

For an approved WO, follow `PROC-WO-START` from installed `WORKFLOW.json`:
focus, run `preflight REPO --work-order WO-ID --phase start --json`, resolve the
actual start right, preview the exact transition, apply it, then inspect state.
Use the evaluator-returned actor for a qualifying delegated route; otherwise
the accountable owner's actual start decision is required. Passing preflight
or writing `--decision WO-ID=engineering-owner` cannot provide that decision.

Example argument shapes after the actual decision and passing gates:

```text
harnessctl transition REPO --set WO-ID=in_progress --decision WO-ID=ACTOR --reason WO-ID=REASON --json
harnessctl transition REPO --set WO-ID=in_progress --decision WO-ID=ACTOR --reason WO-ID=REASON --apply --json
```

Each `ID=value` is one argument. Replace only with inspected, selected values.
No implementation begins from a preview alone.

## Implement and complete

Once start is applied, continue edits and ordinary commits within the approved
WO without asking for its approval again. Compare every proposed edit with
both its behavioral scope and declared paths. Use the `scope` checkpoint with
the complete change set, including intended paths before an edit. Use
`pre-action` when the selected procedure calls for it; do not introduce
`pre-action --procedure PROC-WO-IMPLEMENT` as a new gate before every edit.
That checkpoint requires evidence and is not a replacement for edit-scope
validation. A path allowed by a directory prefix does not authorize unrelated
behavior. Stop an out-of-scope action before invoking its editing tool.

Run the selected verification contract and repository checks. Retain actual
commands, outcomes and failed attempts. Use the installed handoff procedure and
its trusted Git base, including the complete change set. Be aware that
`check --checkpoint handoff --from-git BASE` and `evidence` can write retained
evidence: they need covered preparation authority and scoped destinations.

When implementation and required evidence are complete, follow
`PROC-WO-IMPLEMENT` and its actual completion decision. Preview and apply only
the selected WO's `implemented` transition. A passing check alone cannot mark
it complete. Then follow the returned preparation step if already authorized;
otherwise hand off that exact missing decision. Ready VREC preparation,
assurance, release and external delivery remain distinct operations.

## Execution delegation

Use DR-015 only as the installed evaluator qualifies it: execution class must
exist at the configured PR base, and the required check must be live and
successful for the exact current HEAD. It permits only `DR-WO-START`,
`DR-WO-COMPLETE` and `DR-VREC-PREPARE`, through `delegated-executor`.

Retain its check identity and candidate in the result. After a new commit,
wait for that commit's required result before a delegated mutation. Never move
the configured base, write a local passing gate, or add branch-only delegation
to unlock a blocked action. Delegation grants no definition approval,
assurance, release, merge, publication or other external authority.
