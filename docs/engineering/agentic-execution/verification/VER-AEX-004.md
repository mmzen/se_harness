+++
id = "VER-AEX-004"
type = "verification"
title = "Independent Phase 4 delegated effect and workflow conformance"
status = "approved"
owners = ["assurance-owner", "quality-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
verifies = ["REQ-AEX-010", "REQ-AEX-011", "REQ-AEX-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Independent Phase 4 delegated effect and workflow conformance

## Independence

Primary evidence comes from verifier-owned repositories, reference schema
vectors, adversarial filesystem fixtures, fault-injection processes, external
released evaluator installations, and independent expected-state manifests.
Expected observations, delegation intersections, bundles, receipts, lifecycle
results, and stops are derived from approved requirements, specifications, and
ADRs rather than implementation constants, worker output, provider claims, or
successful tests alone.

The verifier controls clocks, nonce sources where deterministic injection is
needed, concurrent mutation, process interruption, journal corruption, and
cross-platform fixtures. Candidate-source tests are necessary but not
sufficient. Activation evidence must use a separately released evaluator
installed outside a disposable target repository.

Applicable `VER-AEX-001`, `VER-AEX-002`, and `VER-AEX-003` methods remain
required for the existing authority, contract, skill, package, and host
surfaces touched by an implementation work order.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-AEX-010` live authority derivation | reference observation encoder, double-observation race harness, formal delegation matrix, evaluator identity substitution, clock/nonce tests, receipt-chain model | stable and unstable Git/worktree states, clean start, explained chained dirty states, unknown objects, wider requests, expired/revoked delegation, stale and replayed envelopes | only the exact released evaluator derives v2 from two identical observations; every admitted dimension is within all current authorities; fresh state, expiry, nonce, and receipt continuity are enforced before effect; all rejected cases have zero effect |
| `REQ-AEX-011` transactional bundle effects | independent bundle encoder, object-store audit, target manifest oracle, link/path attacks, write/race fault injection, kill-and-recover matrix, receipt validation | create/replace/delete combinations, malformed and duplicated governance data, stale before digests, object corruption, directory creation, links/reparse points, ordinary failures, interruption at every journal phase | bundle bytes are canonical and governance-normalized; only admitted regular-file deltas apply; ordinary failure restores proven prior state; interruption is recovered or blocks explicitly; receipt state equals independent live manifests |
| `REQ-AEX-012` delegated workflow advancement | decision-right table oracle, lifecycle transition matrix, gate/evidence failure injection, skill/evaluator parity tests, assurance packet review | delegated and undelegated start/complete/VREC prepare, expired or wrong delegate, missing receipt, unexplained path, failed/not-assessable gate, commit required/absent, prohibited approval/Git/release/external request | exactly the three activated rights can advance when all conditions pass; implementation effects remain receipt-bound; preparation makes no assurance decision; every reserved decision/action stops with one canonical next step |

## Acceptance scenarios

1. Two independent observations of an unchanged clean repository produce exact
   canonical bytes and digest on supported Windows and POSIX fixtures.
2. A mutation between observations restarts or stops derivation; no envelope is
   returned from a mixed pair.
3. A mutation after derivation but before admission is detected by the fresh
   under-lock observation and consumes no target effect.
4. Candidate, modified, wrong-version, in-checkout, or payload-mismatched
   evaluators cannot label an observation stable or envelope derived.
5. A maximum formal delegation is intersected with a narrower request across
   rights, operations, profiles, paths, evidence, retries, writer count, expiry,
   state, and stops. Every widening attempt is rejected.
6. A nonce is admitted once. Replay, concurrent admission, expiry, revocation,
   lifecycle change, work-order edit, and evaluator change all stop.
7. A verified receipt's `state_after` can anchor one new envelope; caller-
   supplied, incomplete, altered, skipped, or foreign receipts cannot.
8. Initial work-order start rejects dirty index/worktree state. Chained dirty
   state is accepted only when every difference is explained by receipts.
9. The reference encoder and implementation produce identical change-bundle v1
   bytes and digest for create, replace, delete, and mixed vectors.
10. Bundle inspection finds no copied title, owner, status, scope list, gates,
    delegation, decision history, or evidence policy from the work order.
11. A valid create, replace, delete, and parent-directory creation bundle
    produces the exact independently predicted target manifest and receipt.
12. Unknown fields, duplicate keys, noncanonical order, duplicate paths,
    over-bound data, stale prior state, missing object, wrong object digest, and
    cross-context identity each fail before target change.
13. Traversal, absolute, device, alternate-stream, alternate-separator, URI,
    wildcard, control-character, case-colliding, Unicode-ambiguous, link,
    junction, reparse, hard-link, submodule, special-file, and `.git` cases fail.
14. A direct worker target write invalidates the state chain and is never
    legitimized by a later matching bundle.
15. Faults before journal preparation change no target; ordinary faults at each
    apply and validation phase restore and prove the complete prior state.
16. Process termination at every journal transition leaves a detectable
    nonterminal journal. Restart either proves rollback, proves the complete
    intended result, or stops for human recovery; it never silently continues.
17. Corrupt or missing recovery material reports every uncertain path and
    blocks new derivation, effect, completion, and assurance preparation.
18. Two concurrent writers cannot both acquire a target session or admit an
    effect; one receives a stable session-conflict result.
19. Valid delegated `DR-WO-START` performs only the legal approved-to-in-
    progress transition and records start evidence.
20. Valid delegated completion passes only with continuous receipts, exact
    changed paths, required tests, gates, evidence, and current state.
21. Valid `DR-VREC-PREPARE` creates a reviewable draft record and packet but no
    verification outcome or approval lifecycle event.
22. Missing commit-bound evidence requests a separately authorized Git action
    and performs no Git mutation.
23. Approval, verification decision, release preparation/decision, delivery,
    Git, credential, network, publish, deploy, merge, and external requests all
    stop with zero prohibited effect.
24. Codex and Claude writing skills invoke the same evaluator operations and
    cannot write the governed target directly or weaken a stop.
25. Removing the Phase 4 delegation declaration or using 0.6.0 preserves the
    current command-driven behavior and reports the capability unavailable.

## Property and model tests

- Canonical observation and bundle encoding is idempotent and invariant to map
  insertion order, host path spelling, and platform newline defaults.
- Any one-bit semantic input change alters the applicable digest or makes the
  object invalid.
- Every admitted request is a subset of delegation, work-order, policy, and
  gate bounds; property generators find no widening counterexample.
- Mandatory stops occur in every derived envelope and logical execution profile.
- A nonce has at most one admitted terminal attempt in the ledger.
- Receipt graphs form one acyclic contiguous chain whose states equal live
  observation digests.
- Each bundle path is unique, canonically ordered, within scope, and represented
  by exactly one operation invariant.
- Bundle foreign keys resolve to one current work order, envelope, and state;
  mutable governance fields are absent.
- At any terminal broker result, state is proved prior, proved intended, or
  explicitly recovery-required; there is no unlabelled terminal condition.
- Lifecycle model exploration finds no path from delegated operations to an
  approval, verification decision, release action, Git action, or external
  action.
- Single-agent execution and the existing command-driven equivalent produce the
  same legal formal outcomes for matching inputs.

## Static and architecture checks

- Confirm observer, envelope authority, session, bundle builder, broker,
  journal, workflow coordinator, and evidence projector follow the dependency
  direction in `ARCH-AEX-002`.
- Confirm every target-writing Phase 4 call passes through
  `require_mutation_authority()` and the bundle broker.
- Confirm no skill, provider adapter, model-facing file, or candidate module can
  label an envelope derived/admitted or write a target path directly.
- Confirm the currently executing external evaluator payload cannot appear in
  the broker's target set.
- Confirm bundle and receipt schemas have one packaged authoritative definition
  and retained vectors.
- Confirm work-order delegation, workflow, decision-right, and gate schema
  updates occur only in candidate templates and package data, not hash-locked
  0.6.0 root managed files.
- Confirm every changed implementation path is admitted by its started work
  order and all new public files are in source and wheel inventories.
- Confirm `DR-RLS-PREPARE`, multi-agent, parallel writer, Git, credential,
  network, and external-effect integrations remain absent.

## Security and privacy checks

- Substitute malicious Git output, formal TOML, lock JSON, workflow JSON,
  bundle JSON, content objects, receipt JSON, journal bytes, paths, clocks,
  nonces, and provider results.
- Exercise time-of-check/time-of-use changes before and after each observation,
  path resolution, object hash, temp-file creation, journal write, replace, and
  result observation.
- Exercise symlink and reparse swaps, case changes, hard-link aliasing, reserved
  devices, alternate streams, long paths, permission changes, locked files, and
  external-runtime directory aliasing.
- Confirm subprocesses use bounded argument vectors without shell evaluation.
- Confirm artifacts, packets, logs, journals, and normal errors exclude tokens,
  credentials, environment dumps, absolute user paths, private file bodies,
  provider transcripts, and hidden reasoning.
- Confirm runtime permissions, OS identity, skill names, signed provider output,
  successful tests, and model confidence cannot create authority.

## Performance and resilience checks

- Measure two-pass observations at 100, 10,000, and 100,000 entries and near
  byte/entry bounds; memory remains bounded and file bodies are streamed.
- Measure bundle construction and apply at 1, 100, and 1,024 entries and near
  per-file and total-byte bounds.
- Exercise insufficient disk, read-only targets, locked paths, filesystem-full,
  interrupted fsync, process kill, machine-restart simulation, journal replay,
  stale lock, and abandoned session behavior.
- Run relevant fixtures on supported Windows and POSIX filesystems and record
  actual atomic-replace and durability capabilities.
- Confirm unsupported containment or durability primitives fail closed rather
  than silently reduce guarantees.

## Manual assessments

- Requirements and product owners confirm the three activated delegated rights
  and assurance terminal stop match Phase 4 intent.
- Technical and security owners inspect observation fields, delegation schema,
  bundle normalization, deny policy, nonce handling, transaction journal, and
  recovery design.
- Repository and quality owners observe direct-write denial, a successful
  sequential bundle session, ordinary rollback, interruption recovery, exact
  changed-path proof, and VREC preparation in a disposable repository.
- An independent assurance owner reviews the ready packet and confirms no
  implementation actor or evaluator made the verification decision.

## Activation ladder

1. Verify candidate source under the exact current released evaluator.
2. Build and independently inspect a non-promotable candidate distribution.
3. After separate approval, qualify and release the successor evaluator.
4. Install that exact release outside a disposable target.
5. Run schema, adversarial, rollback, recovery, and workflow pilot matrices.
6. Run one low-risk disposable end-to-end work order to the assurance stop.
7. Only after independent review, consider an explicitly approved low-risk
   self-host trial. Never use candidate source to govern its own implementation.

## Evidence retention

Each work order retains evidence at its declared
`docs/engineering/agentic-execution/evidence/WO-AEX-00N-verification.md` path.
Retain exact source commit, candidate and released package identities, external
evaluator payload, operating system and filesystem, runtime-directory policy,
reference vectors, observer manifests, work-order and delegation digests,
envelope and nonce evidence, bundle/object inventories, journal transitions,
fault and recovery matrices, receipt chains, lifecycle results, test and gate
outputs, host parity results, changed-path audits, decision packets, manual
assessments, deviations, and residual uncertainty.

## Residual uncertainty

Verification cannot make arbitrary multi-file replacement instantaneously
atomic to all outside observers, prove durability beyond the guarantees of the
tested filesystem and hardware, authenticate the real-world human from a role
string, prove a hostile provider obeys instructions outside the enforced target
boundary, or predict future host and platform behavior.

Those limitations require explicit journals, recovery stops, recorded platform
support, provider defense in depth, and accountable decisions. They do not
permit hidden partial success, direct target writes, authority inference,
unverified continuation, or activation on an untested evaluator.
