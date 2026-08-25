+++
id = "SPEC-AEX-006"
type = "specification"
title = "Live observation and delegated authority derivation contract"
status = "approved"
owners = ["technical-owner", "security-owner", "repository-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
specifies = ["REQ-AEX-002", "REQ-AEX-004", "REQ-AEX-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "technical-owner"
+++

# Specification: Live observation and delegated authority derivation contract

## Scope

This specification defines the Phase 4 live repository observer, the formal
maximum-delegation declaration, evaluator-derived autonomy-envelope v2, stable
observation protocol, nonce and expiry behavior, and receipt-linked state
chain. It integrates the pure contracts approved by `SPEC-AEX-003` with a real
target repository without changing the authority model in `SPEC-AEX-001`.

It does not define change bytes, transactional apply, accountable approvals,
verification or release decisions, Git mutation, credentials, network access,
external actions, multi-agent scheduling, or provider-specific permissions.

## Actors and external systems

- An accountable engineering owner records the maximum delegation in a work
  order before approving it.
- One logical worker requests a narrower operation through a supported skill or
  evaluator interface.
- The target repository's exact released evaluator validates governance,
  observes live state, derives envelopes, admits effects, and records receipts.
- Git supplies read-only object, index, and worktree observations.
- An explicitly configured evaluator runtime directory outside the target
  checkout stores nonce, session, and recovery state.

## Inputs

- exact target repository root and exact external evaluator launcher;
- valid installed managed lock and evaluator payload identity;
- one approved, started work order and its canonical bytes;
- one approved `se-harness-agentic-delegation-v1` declaration in that work
  order;
- requested operation, decision right when applicable, worker identity,
  execution profile, path set, evidence set, and retry ordinal;
- current formal snapshot and applicable gate results; and
- optional preceding admitted-effect receipt for a chained request.

The worker request is untrusted and can only narrow the formal declaration.

## Outputs

- `se-harness-repository-observation-v1` canonical bytes and SHA-256 digest;
- `se-harness-autonomy-envelope-v2` canonical bytes and digest held in memory;
- a single-use admission record linked to the nonce ledger;
- normalized derivation or rejection evidence; and
- after an effect, a verified receipt link eligible to anchor the next request.

No successful output is itself an accountable decision or external-action
authorization.

## State model

```text
unobserved
  -> observation_1
  -> observation_2
  -> stable_observation
  -> delegation_resolved
  -> envelope_derived
  -> fresh_observation_under_effect_lock
  -> admitted_once
  -> receipt_verified
  -> next_stable_observation

any stage -> stopped_without_effect
admitted_once -> completed | failed_consumed | recovery_required
```

The observer is stateless. The evaluator runtime directory retains only the
minimum nonce, session, lock, and recovery data needed to prevent reuse and
continue safely after interruption.

## Formal delegation declaration

A future candidate work-order template adds one optional
`[agentic_delegation]` table. Its absence means no agentic delegation. When
present it contains exactly:

| Field | Type | Rule |
| --- | --- | --- |
| `schema` | string | `se-harness-agentic-delegation-v1` |
| `delegated_by` | managed role ID | accountable role allowed for all named rights |
| `delegate` | profile name | one non-accountable logical worker identity |
| `decision_rights` | set | subset of the managed advance-delegable catalog |
| `operations` | non-empty set | closed evaluator operation IDs |
| `execution_profiles` | non-empty set | approved logical profiles |
| `paths` | non-empty set | paths within `[execution_scope].paths` |
| `required_evidence` | non-empty set | retained evidence kinds and paths |
| `valid_until` | UTC timestamp | no later than the work order's review horizon |
| `max_retry` | integer | 0 through 3 in Phase 4 |
| `max_parallel_writers` | integer | exactly 1 in Phase 4 |
| `child_delegation` | boolean | exactly `false` in Phase 4 |
| `stop_before` | non-empty set | includes both mandatory stop classes |

The declaration is part of the work-order bytes approved by the accountable
owner. A later edit invalidates the work-order digest and cannot silently widen
an existing execution. The declaration never changes the work-order lifecycle
state by itself.

## Repository observation contract

`se-harness-repository-observation-v1` contains exactly:

- `schema`;
- `repository`, containing a stable local repository identifier derived from
  the canonical root identity without exposing its absolute path;
- `evaluator`, containing released package name, version, immutable payload
  digest, and launcher identity digest;
- `git`, containing object format, `HEAD` object or null, symbolic ref or null,
  canonical index-entry digest, tracked-worktree digest, untracked-nonignored
  regular-file digest, and conflict/submodule flags;
- `governance`, containing managed-lock digest, formal-snapshot digest,
  workflow-contract digest, decision-rights digest, selected work-order ID,
  selected work-order digest, and selected status;
- `filesystem`, containing platform family, effective case-sensitivity result,
  canonical regular-file manifest digest, and unsupported-object count; and
- `previous_receipt_sha256`, nullable and present only for a chained state.

The observation digest is SHA-256 over canonical JSON. Volatile timestamps,
process IDs, absolute paths, command output, environment values, and secrets are
not part of the observation. Diagnostic evidence may record bounded timings
separately.

The regular-file manifest covers tracked and nonignored untracked files except
closed evaluator-created transient session paths. Each entry commits to the
portable path, object kind, byte size, and content digest. The observer never
follows a link or reparse point.

## Stable observation and state-chain algorithm

1. Prove exact released evaluator identity and acquire the read-only observer
   phase of the target session lock.
2. Capture observation 1 from one normalized repository view.
3. Capture observation 2 independently using the same closed algorithm.
4. Continue only when their canonical bytes are identical.
5. Resolve formal delegation and intersect every requested dimension with it,
   current policy, selected work-order scope, and current gates.
6. Derive envelope v2 and record its digest, but persist no reusable envelope
   bytes by default.
7. At effect time acquire the exclusive target session lock, capture a fresh
   observation, and require its digest to equal the envelope's expected state.
8. Atomically mark the nonce admitted before invoking the effect broker.
9. On success, validate the effect receipt and require its `state_before` to
   equal the admitted observation and its `state_after` to equal a fresh live
   observation.
10. For a next operation, use that receipt digest and `state_after` in a new
    stable observation and derive a new envelope. Never mutate or reuse the
    prior envelope.

Initial `DR-WO-START` requires a clean index and worktree. A later dirty state is
admissible only when the complete difference from that clean baseline is
covered by the uninterrupted verified receipt chain. Conflicts, submodules,
unsupported objects, or unexplained changes are never admissible.

## Autonomy-envelope v2

Envelope v2 preserves the v1 `selection`, `delegation`, and `evidence` objects
and adds one `authority` object containing exactly:

- `decision_right`, nullable for a pure implementation effect;
- `delegate` and `execution_profile`;
- `delegation_sha256` and selected work-order digest;
- `expected_repository_state`;
- `previous_receipt_sha256`, nullable;
- evaluator-generated 128-bit-or-greater random `nonce` encoded as lowercase
  hexadecimal;
- `issued_at` and `not_after` UTC timestamps; and
- `retry_ordinal`.

`not_after` is the earliest of five minutes after issue, formal delegation
expiry, work-order review horizon, and any smaller managed limit. Randomness is
used only for nonce uniqueness; all admitted authority dimensions remain a
deterministic intersection. V1 remains valid for pure parsing and historical
evidence but cannot admit a Phase 4 effect.

## Behavioral rules

1. **AEX-OBS-001:** Only the target's exact released evaluator may label a live
   observation stable, an envelope derived, or an effect admitted.
2. **AEX-OBS-002:** Two byte-identical observations are mandatory before every
   derivation; bounded retries restart the pair rather than mix observations.
3. **AEX-OBS-003:** A fresh observation under the exclusive lock is mandatory
   immediately before effect admission.
4. **AEX-OBS-004:** Every requested dimension is equal to or narrower than the
   formal delegation, work order, managed policy, and current gate result.
5. **AEX-OBS-005:** Omission, wildcard, parent directory, provider permission,
   or inferred intent creates no authority.
6. **AEX-OBS-006:** Nonces are repository-session scoped, single-use, and
   consumed at admission even if the admitted effect later fails.
7. **AEX-OBS-007:** Expiry, revocation, lifecycle change, evaluator change,
   work-order-byte change, state change, or receipt discontinuity invalidates
   the envelope.
8. **AEX-OBS-008:** State chaining requires a complete evaluator-verified
   receipt; caller-supplied `state_after` cannot advance expected state.
9. **AEX-OBS-009:** Mandatory accountable and action-time stop classes survive
   every intersection and cannot be delegated away.
10. **AEX-OBS-010:** One target repository admits at most one writer and one
    active Phase 4 session.
11. **AEX-OBS-011:** The observer performs no repository, Git, lifecycle,
    credential, network, or external mutation.
12. **AEX-OBS-012:** Diagnostics expose field classes and digests, not secret
    bytes, hidden reasoning, or unbounded command output.

## Error and recovery behavior

Stable codes distinguish evaluator identity failure, unstable observation,
unsupported repository object, dirty initial state, receipt-chain gap, invalid
delegation, denied narrowing, failed gate, expired authority, nonce reuse,
stale state, session conflict, and internal failure. Every such result stops
before the requested effect.

An interrupted derivation leaves no authority. An interruption after nonce
admission defers to the effect broker's journal and blocks new derivations until
recovery is complete and freshly observed.

## Security and privacy properties

- Treat Git output, paths, formal files, locks, staged content, receipts, and
  runtime state as untrusted input.
- Use argument-vector subprocess calls with bounded output and no shell.
- Reject path escapes, links, reparse points, case collisions, reserved names,
  alternate data streams, unmerged index entries, and unsupported submodules.
- Store only salted repository identity, digests, nonces, timestamps, and
  recovery metadata in the external runtime directory; restrict its access to
  the invoking operator.
- Do not infer real-world actor identity from an operating-system username,
  provider identity, model identity, or skill profile.

## Performance and observability

Observation is linear in covered entries and streams file digests. Default
bounds are inherited from `SPEC-AEX-003`; over-bound repositories stop with a
diagnostic rather than silently omit entries. Evidence records observation
digests, pair attempts, duration, entry and byte counts, evaluator and work-
order identities, requested and admitted scope counts, nonce digest, expiry,
receipt links, gate outcomes, and deviations.

## Compatibility and migration

- Preserve all v1 pure-contract parsing and historical evidence behavior.
- Add v2 rather than changing v1 bytes or semantics.
- Repositories without the new delegation table retain command-driven workflow
  and cannot derive Phase 4 mutation authority.
- Root managed 0.6.0 files remain unchanged. The new template, evaluator, and
  workflow behavior becomes authoritative only through a successor release and
  explicit target upgrade.

## Explicitly unspecified decisions

- Private module, type, cache, and helper names.
- The secure operating-system primitive used for random nonce generation.
- A smaller configured expiry than the five-minute maximum.
- Fixture organization inside approved work-order prefixes.

These choices cannot change observation fields, canonicalization, delegation
meaning, state-chain continuity, mandatory stops, or evaluator ownership.
