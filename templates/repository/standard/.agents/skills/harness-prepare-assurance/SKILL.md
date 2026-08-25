---
name: harness-prepare-assurance
description: Prepare one exact-candidate ready SE Harness verification record from implemented work and retained evidence. Use only when explicitly named with a preparation actor; stop before assurance, delivery, release, Git, credentials, network, or external action.
---

# Harness Prepare Assurance

Prepare one `ready` verification record and its assurance decision packet. The
released evaluator remains authoritative for candidate cleanliness, gates,
canonical destination, record preparation, and the next accountable decision.

## Required inputs

Require the exact skill name, one target, a structured launcher and expected
identity for its external released evaluator, requested outcome and non-effects,
implemented work orders, applicable verification contracts, retained evidence
paths, exact clean candidate commit, one unused collision-checked VREC ID and
canonical destination, and an explicit preparation actor. Read repository
instructions and this complete core. Validate `skill-contract.json` and the
portable-core digest.

## Procedure

1. Reject implicit activation, a missing preparation actor, an ambiguous
   selection, or any exact skill value other than
   `harness-prepare-assurance`.
2. Run evaluator `version`, released `identity`, `doctor`, `validate --json`,
   current focus, and review preflight. Confirm every selected work order is
   `implemented`, evidence is retained, and the observed clean commit equals
   the requested candidate.
3. Build the exact `capture-verification` argument array. Treat the evaluator's
   derived VREC and evaluator-evidence destinations as the only admitted paths.
   Use `scripts/check_prepare.py` to validate the closed plan before its
   injectable preparation callback.
4. Immediately repeat identity, integrity, candidate, record-ID, actor, gate,
   and destination checks. Invoke only the existing evaluator
   `capture-verification` operation.
5. Re-run formal validation and focus the new record. Require exactly one new
   VREC in `ready`, bound to the exact candidate, work, verification contracts,
   evidence, and preparer. Compare all actual paths with evaluator-derived
   destinations.
6. Run the evaluator's `risks` operation for every selected work order and
   include the register in the assurance decision packet; the skill never
   disposes a risk. Return the structured result, receipt identity, and
   assurance decision packet. Stop before the assurance-owner decision.

## Boundaries

- Do not verify, reject, supersede, deliver, release, mutate Git, use
  credentials, access the network, or perform an external action.
- The preparation actor is evidence of preparation, never proof of assurance
  ownership or an assurance decision.
- Stop on a dirty or changed candidate, stale state, failed gate, missing
  evidence, ID collision, unexpected path, invalid graph, or missing required
  capability.
- Use the complete single-agent procedure. Do not spawn or coordinate workers.

The new record begins `ready` only because the existing preparation operation
creates it there. That creation is not a lifecycle transition or verification.
