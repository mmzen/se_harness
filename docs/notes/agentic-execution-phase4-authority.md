# Phase 4 live observation and delegated authority

> This is non-authoritative implementation guidance. It does not approve,
> start, complete, verify, release, or activate delegated execution. Formal
> authority remains in the approved artifacts and the target repository's
> exact released evaluator.

## What WO-AEX-005 adds

The candidate separates four concerns:

1. `se_harness.repository_state` reads Git, regular files, formal artifacts,
   managed policy, and evaluator identity into one canonical repository
   observation.
2. `se_harness.delegated_authority` parses the maximum delegation recorded in a
   work order and derives one narrower autonomy envelope for one request.
3. `se_harness.runtime_state` stores session ownership, consumed nonces,
   revocations, terminal outcomes, and recovery state outside the target
   checkout.
4. `se_harness.agent_contract` validates the portable bytes shared across those
   layers.

None of these modules applies a target change. The effect broker belongs to
`WO-AEX-006`.

## The three portable contracts

### Repository observation v1

`se-harness-repository-observation-v1` commits to:

- a hashed local repository identity;
- evaluator package, version, payload digest, and launcher digest;
- Git object format, HEAD, symbolic ref, index, tracked content, untracked
  nonignored content, conflicts, and submodules;
- managed lock, formal snapshot, workflow, decision-rights, and selected
  work-order identities;
- platform, case behavior, the complete regular-file manifest digest, and
  unsupported-object count; and
- an optional previous verified receipt digest.

The observation has no clock or absolute path. Two consecutive captures must
produce identical canonical bytes before derivation. A future effect broker
must capture the same state again while holding the exclusive effect lock.

### Agentic delegation v1

`se-harness-agentic-delegation-v1` is an optional work-order front-matter
table. Absence means no delegation. Presence records the accountable
delegator, logical delegate, rights, operations, profiles, paths, retained
evidence kind/path pairs, expiry, retry limit, one-writer limit, no-child rule,
and mandatory stops.

This table is the approved maximum, not the authority used for an effect. The
exact evaluator cross-checks it against its managed catalogs and the work
order's execution scope.

### Autonomy envelope v2

`se-harness-autonomy-envelope-v2` preserves the v1 selection, delegation, and
evidence objects and adds:

- the selected decision right, worker, and profile;
- delegation and work-order digests;
- expected live repository state and optional previous receipt;
- a random single-use nonce;
- issue and expiry times; and
- the retry ordinal.

The maximum lifetime is five minutes. The effective expiry is earlier when the
formal delegation or a managed limit expires first.

## Admission and state continuity

The intended sequence is:

~~~text
observation A == observation B
             |
             v
resolve formal maximum delegation
             |
             v
derive one envelope and nonce
             |
             v
fresh observation under future effect lock
             |
             v
consume nonce in external runtime state
             |
             v
future WO-AEX-006 effect broker
             |
             v
verify receipt state_before and fresh state_after
~~~

Initial delegated work-order start requires a clean repository. A later dirty
state requires an uninterrupted previous-receipt link. A stale state, changed
evaluator, changed work-order bytes, revoked delegation, expired envelope,
failed gate, reused nonce, conflict, submodule, link, reparse point, or
unsupported path stops before an effect.

## Why this does not duplicate the change bundle

The observation, work order, envelope, change bundle, and receipt repeat some
identifiers deliberately, but they serve different integrity checks:

| Artifact | Question answered |
| --- | --- |
| Work order | What maximum implementation and delegation did an accountable owner approve? |
| Observation | What exact repository and governance state exists now? |
| Envelope | Which narrow operation is admissible against that state for a few minutes? |
| Change bundle | Which exact file-byte transformation is proposed? |
| Receipt | What was admitted, what happened, and what state followed? |

The repeated values are foreign keys and consistency checks, not competing
sources of truth. A mismatch invalidates the operation. The bundle does not
copy the work-order narrative or observation manifest; it carries only the
identities needed to bind proposed bytes to authority and state.

## Runtime boundary

The runtime directory must be explicitly supplied and external to the target.
It cannot alias, contain, or be contained by the checkout. State files are
canonical JSON, atomically replaced, access-restricted where the platform
supports POSIX modes, and bounded to 1,024 retained nonce admissions per
repository.

The candidate APIs accept evaluator identity and managed catalogs from their
caller. They cannot prove that their own checkout is the released evaluator.
Only a later externally installed release may connect these APIs to identity
proof, workflow activation, and an effect broker.

## Current implementation status

The focused contract, observer, authority, runtime-state, and candidate
validator tests pass. The governed scope amendment adds the compatibility test
that previously required byte identity between the candidate and released
work-order templates. Its revised exhaustive assertion reconstructs the
candidate from the unchanged released template plus the exact delegation table
and guidance paragraph. The expanded focused suite passes 57 tests with 2
platform skips, and the complete repository suite passes 943 tests with 22
skips. The exact handoff gate passed and the work order is `implemented`. The
next boundary is a ready verification record bound to a clean exact candidate
commit, followed by a separate independent assurance decision.
