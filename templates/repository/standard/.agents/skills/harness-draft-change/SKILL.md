---
name: harness-draft-change
description: Prepare explicitly requested SE Harness planning notes and complete draft formal artifacts. Use only when the operator names this skill and requests draft creation or revision; stop before approval, transition, implementation, Git, credentials, network, or external action.
---

# Harness Draft Change

Prepare one reviewable definition packet while leaving every formal artifact in
`draft`. The released evaluator and installed harness remain authoritative for
identity, canonical destinations, formal validity, lifecycle, and next action.

## Required inputs

Require the exact skill name, one target repository, a structured launcher and
expected identity for its external released evaluator, the requested outcome
and non-effects, one domain, a finite artifact plan, an optional single planning
note, and any existing drafts selected for revision. Read repository
instructions and this complete core first. Validate `skill-contract.json` and
the portable-core digest.

Before assigning an identifier, inspect every locally available Git ref. Do not
fetch. The plan must declare each type, unused ID, title, owner, relation, and
canonical destination. Only explicitly selected artifacts that are currently
`draft` may be revised.

## Procedure

1. Reject implicit, inferred, or ambiguous activation. Confirm the explicit
   skill value is exactly `harness-draft-change`.
2. Run the supplied evaluator's `version`, released `identity`, `doctor`, and
   `validate --json` operations directly. Stop on a required failure.
3. Build a closed plan containing only canonical draft destinations, explicitly
   selected current drafts, and at most one declared path under `docs/notes/`.
4. Immediately repeat identity, integrity, and formal-state checks. Reconfirm
   identifier uniqueness and destination absence before each creation.
5. Use only the evaluator's existing `scaffold-domain` and `create-artifact`
   preparation operations for new formal destinations. Use `scripts/guard.py`
   before a controlled draft, revision, or note write; its callable boundary is
   testable and it grants no authority.
6. Complete the declared draft bodies and relations without adding a lifecycle
   event. Compare actual changed paths with the admitted plan.
7. Run formal validation again. Return the structured result and receipt facts,
   then stop at accountable content review.

## Boundaries

- Do not approve, transition, start, implement, complete, verify, deliver,
  release, mutate Git, use credentials, access the network, or perform an
  external action.
- Do not write an undeclared note, revise an unselected artifact, or modify a
  non-draft artifact.
- Treat an unexpected path, stale result, collision, invalid graph, customized
  managed file, or missing required capability as a stop before further effect.
- Use the complete single-agent procedure. Do not spawn or coordinate workers.

The drafts and optional planning note are retained repository content. The
inline receipt is evidence only and is never an approval decision.
