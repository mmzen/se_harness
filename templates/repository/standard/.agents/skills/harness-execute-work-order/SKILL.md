---
name: harness-execute-work-order
description: Execute one explicitly selected SE Harness work order that is already in_progress. Use for bounded implementation and evidence collection; stop before completion, assurance preparation, delivery, Git, credentials, network, or external action.
---

# Harness Execute Work Order

Implement exactly one already-started work order. The released evaluator and
formal work-order bytes remain authoritative for lifecycle state, scope, gates,
evidence obligations, and the next accountable decision.

## Required inputs

Require the exact skill name, one target, the structured launcher and expected
identity of its external released evaluator, exact requested outcome and
non-effects, one work-order ID, current focus and start-preflight JSON, complete
execution scope, verification and evidence obligations, repository-owned
commands, and optional narrowing constraints. Read repository instructions,
this complete core, and every file in the current work-order manifest. Validate
`skill-contract.json` and the portable-core digest.

## Procedure

1. Reject implicit activation and any selection other than exactly
   `harness-execute-work-order` plus one work order.
2. Run evaluator `version`, released `identity`, `doctor`, `validate --json`,
   `focus --json`, and start `preflight --json`. If the work order is
   `approved`, stop at the work-start decision. Only `in_progress` admits an
   implementation effect.
3. Construct a closed effect plan from current `[execution_scope].paths`.
   Operator constraints may narrow but never widen it. Use
   `scripts/check_scope.py` to admit every proposed implementation and evidence
   path before a write callback.
4. Immediately before each controlled effect, repeat identity, integrity,
   selected-state, checkpoint, and path checks. Preserve unrelated user work.
5. Implement only admitted paths, run only structured repository-owned command
   arrays, and retain evidence only at declared destinations. Record failures;
   do not erase unexpected paths to manufacture success.
6. Compare actual changed paths with planned and admitted paths. Run the review
   checkpoint and formal validation, retaining exact command results and
   digests.
7. Return the structured result and receipt facts. Stop before the engineering
   owner's work-completion decision.

## Boundaries

- Do not start or complete the work order, apply a lifecycle transition,
  prepare a VREC, verify, deliver, release, mutate Git, use credentials, access
  the network, or perform an external action.
- Do not execute when current state is `draft`, `approved`, `implemented`, or
  otherwise not `in_progress`.
- Stop on stale state, failed required gate, scope mismatch, unexpected path,
  missing evidence, invalid graph, or missing required capability.
- Use the complete single-agent procedure. Do not spawn or coordinate workers.

Retained evidence and the inline receipt support a later decision. They do not
complete the work order or attest that the implementation is correct.
