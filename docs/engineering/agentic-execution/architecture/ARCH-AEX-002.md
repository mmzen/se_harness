+++
id = "ARCH-AEX-002"
type = "architecture"
title = "Evaluator-owned single-agent effect broker"
status = "approved"
owners = ["technical-owner", "repository-owner", "security-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
addresses = ["REQ-AEX-010", "REQ-AEX-011", "REQ-AEX-012"]
conforms_to = ["SPEC-AEX-006", "SPEC-AEX-007", "SPEC-AEX-008"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "responsibility-or-dependency-direction", "public-interface-or-protocol", "security-privacy-or-trust-boundary", "concurrency-consistency-reliability-or-failure-strategy", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "Phase 4 introduces a new authority-bearing runtime boundary, live state fingerprint, public bundle and receipt protocols, durable recovery state, lifecycle integration, and a hard dependency direction between agents and the exact released evaluator. The delegation source and effect-isolation strategy have material alternatives and require explicit ADRs before implementation."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "technical-owner"
+++

# Architecture: Evaluator-owned single-agent effect broker

## Amendment of 2026-08-28 (`ADR-AEX-008`)

Superseded by `ARCH-ECP-001` on the owner's disposition of Phase 4 recorded in `ADR-AEX-008`: the effect broker, the bundle pipeline and the autonomy envelope leave the product under `WO-ECP-006`; delegation becomes a work-order attribute enforced at the pull-request gate, and the journaled apply with rollback and `human-recovery-stop` is retained as the one harness-owned write path. The text below is retained as the record of what Phase 4 built.

## Context and scope

`ARCH-AEX-001` establishes harness-owned authority and replaceable procedure,
execution, adapter, and evidence planes. Phases 1 through 3 delivered contracts,
pure admission logic, portable skills, and repository host discovery, but they
intentionally stopped short of applying an agent-proposed repository mutation.

Phase 4 adds that missing enforcement boundary for one worker and one writer.
It derives short-lived authority from approved formal delegation and live state,
keeps proposed work outside the governed target, applies admitted byte deltas
through the exact released evaluator, advances only selected delegated workflow
rights, and stops at independent assurance.

The architecture excludes multi-agent orchestration, child delegation,
parallel writers, Git mutation, release decisions, delivery, credentials,
network access, and external actions.

## Components and responsibilities

### Formal delegation source

The selected approved work order owns the maximum agentic delegation. The
declaration names the accountable delegator, logical delegate, decision rights,
operations, profiles, paths, evidence, expiry, retries, single-writer limit, and
mandatory stops. It is reviewed and approved with the work-order bytes.

This component is data in the authority plane, not a runtime bearer token.

### Live repository observer

The observer constructs a canonical fingerprint of every repository fact that
can invalidate effect admission:

- released evaluator and launcher identity;
- Git `HEAD`, ref, index entries, tracked worktree, and untracked nonignored
  regular files;
- managed lock, workflow, decision-right, formal snapshot, and selected work-
  order identities;
- filesystem case behavior and unsupported-object observations; and
- the prior effect receipt when continuing a session.

It performs two independent identical observations before derivation and a
fresh observation under the exclusive effect lock before admission. It never
mutates the target.

### Delegation resolver and envelope authority

The resolver intersects the untrusted worker request with the approved formal
delegation, work-order execution scope, managed operation catalog, current
gates, current lifecycle state, worker profile, and mandatory stop policy.

The envelope authority creates one in-memory autonomy-envelope v2 with a short
expiry, unique nonce, exact state anchor, and optional preceding receipt. The
external nonce ledger makes admission single-use. It cannot mint authority
when any input is missing or not assessable.

### Isolated execution session

The evaluator creates a session workspace outside the target checkout. The
worker may inspect the target through declared read-only inputs and may edit
only session material. Tests intended to exercise proposed bytes run in the
session or another non-authoritative disposable workspace.

The worker cannot make a direct target write through the Phase 4 interface.
Provider sandboxing may add defense in depth but is not the authority source.

### Change-bundle builder

The builder compares the evaluator-owned session baseline and proposed result,
accepts an explicit deletion intent, hashes all affected regular files, and
emits canonical change-bundle v1 plus immutable content objects. It rejects
unsupported objects and ambiguity before target admission.

The bundle transports deltas. It references, rather than duplicates, mutable
governance facts.

### Transactional effect broker

The broker is the only Phase 4 writer to a governed target path. Under an
exclusive session lock it:

1. admits the envelope against fresh live state;
2. validates bundle identities and every path through all authority layers;
3. verifies prior and proposed bytes;
4. writes a durable external journal and recovery material;
5. applies canonical regular-file operations;
6. validates the complete resulting repository;
7. emits a state-bound effect receipt; and
8. commits or recovers the journal.

Single-path replacement uses platform atomic primitives. Cross-file atomic
visibility is not claimed; interruption is represented as recovery-required and
blocks all governed continuation.

### Delegated workflow coordinator

The coordinator maps the closed Phase 4 operation catalog to existing managed
workflow operations and mutation guard. It may exercise delegated work-order
start, work-order completion, and verification-record preparation. Each request
requires current delegation and gates; no prior request creates standing
authority.

The coordinator cannot decide approval, verification, release, delivery, Git,
or an external action.

### Evidence and decision-packet projector

Receipts link start state, every admitted effect, final implementation state,
lifecycle results, tests, gates, and retained evidence. The projector creates
the existing lossless decision packet and one exact next action. At the Phase 4
terminal boundary it stops for independent verification or the separately
authorized commit needed for commit-bound verification.

## Dependency direction

```text
approved work order + delegation + managed policy
                         |
                         v
exact released evaluator identity + live observer
                         |
                         v
delegation resolver -> ephemeral envelope + nonce ledger
                         |
                         v
isolated session -> evaluator-built change bundle
                         |
                         v
transactional effect broker + durable journal
                         |
                         v
effect receipt -> new live-state anchor
                         |
                         v
delegated workflow coordinator
                         |
                         v
assurance draft + accountable decision packet
```

Agent, skill, adapter, model, and provider permissions exist below the evaluator
boundary. They submit requests and proposed bytes and receive results; no
dependency arrow allows them to define formal authority or current state.

## Control flow

1. A human approves the Phase 4 artifacts and work order through the existing
   released evaluator; a separate human decision starts implementation of the
   Phase 4 code itself.
2. Phase 4 code is built and verified without using the capability it is adding.
3. A successor evaluator is separately released and installed outside a
   disposable target repository.
4. For a governed session, the successor evaluator validates the target and
   performs delegated start from a clean baseline.
5. It creates an isolated session and supplies bounded inputs to one worker.
6. The worker proposes changes; the evaluator constructs a bundle.
7. The observer and resolver derive one envelope; the broker freshly admits and
   applies the bundle and emits a receipt.
8. Additional sequential bundles repeat with new envelopes linked to the prior
   receipt.
9. Completion proof permits the delegated work-order completion operation.
10. Assurance preparation creates the ready review artifact and decision packet.
11. Execution stops for independent assurance. No Git or later lifecycle action
    is inferred.

## Trust boundaries

- **Formal boundary:** only valid approved artifacts and managed policy define
  maximum authority.
- **Evaluator boundary:** only an exact released external evaluator may observe,
  derive, admit, write, transition, or attest.
- **Session boundary:** worker-writable session bytes are untrusted proposed
  content until bundle validation.
- **Target boundary:** all target paths and filesystem objects are hostile until
  handle-aware checks pass.
- **Evidence boundary:** receipts are observations, never approvals.
- **Provider boundary:** provider configuration and permissions are defense in
  depth and cannot weaken a stop.

## Consistency and reliability model

- One active work order, one logical worker, one target session, and one writer.
- An external exclusive lock serializes derivation/effect critical sections.
- Stable-pair observation detects racing inputs before derivation.
- Fresh under-lock observation detects changes between derivation and effect.
- Unique nonces prevent replay.
- Immutable receipt links make unexplained state discontinuity visible.
- Durable journals make interruption recoverable or explicitly human-blocked.
- No lifecycle completion or assurance preparation occurs with a nonterminal
  journal, state mismatch, receipt gap, failed gate, or unexplained path.

## Security and privacy

The architecture uses no shell interpretation, follows no link, rejects path
and case ambiguity, bounds all documents and content, and keeps evaluator
runtime material outside the target checkout. Runtime state records digests and
bounded metadata; content backups follow explicit restricted retention. Neither
formal artifacts nor evidence store credentials, environment dumps, private
transcripts, or hidden reasoning.

The operating-system account is not an accountable-role authentication
mechanism. Formal lifecycle events and configured actor assertions retain their
existing governance meaning.

## Deployment and compatibility

The Phase 4 implementation is candidate source until separately qualified and
released. It cannot use itself as the governing evaluator. Activation sequence:

```text
existing released evaluator builds and verifies candidate
  -> accountable successor release decision
  -> external successor installation
  -> disposable target pilot
  -> adversarial and recovery qualification
  -> explicit low-risk target upgrade
  -> optional later self-host trial
```

Published 0.6.0 and repositories that remain on it preserve command-driven
behavior. Absence of a delegation declaration or external runtime directory
fails closed to the existing human-driven procedure.

## Decision assessment and ADR coverage

The trigger assessment requires ADRs for:

- the formal delegation source, live-state derivation, ephemeral envelope, and
  single-use authority strategy (`ADR-AEX-006`); and
- isolated worker staging, evaluator-built change bundles, transactional target
  effects, and recovery behavior (`ADR-AEX-007`).

Any future decision to activate multi-agent execution, parallel writers, Git
effects, release preparation, or external actions requires new architecture and
ADR review.

## Explicitly deferred concerns

- multi-agent decomposition, worker-to-worker delegation, and integration;
- parallel read or write scheduling;
- provider-specific hard sandbox setup;
- Git commit, branch, merge, tag, push, or pull effects;
- credentials, network, connectors, publication, deployment, or delivery;
- automatic release-record preparation and decisions; and
- remote or distributed transaction coordination.
