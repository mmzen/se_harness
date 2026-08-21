+++
id = "ARCH-REB-002"
type = "architecture"
title = "Predecessor-evaluator bootstrap adapter"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
addresses = ["REQ-REB-008"]
conforms_to = ["SPEC-REB-003"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "data-ownership-or-persistence", "security-privacy-or-trust-boundary", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The correction introduces a one-release trust adapter between a schema-2 predecessor evaluator, candidate evidence format, and credential-gated publication. It changes provenance ownership and publication dependency direction at a security boundary, has several materially different alternatives, and therefore requires the technical and security owners to accept ADR-REB-002 before implementation."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T15:40:28Z"
decided_by = "technical-owner"
+++

# Architecture: Predecessor-evaluator bootstrap adapter

## Context and scope

The standard lock-bound architecture assumes that the root already carries schema-3 evaluator identity before a new ready RLS is prepared. That assumption cannot hold for the release that first ships the feature: released 0.5.0 owns a schema-2 root and cannot emit the candidate evidence format, while unreleased 0.6.0 cannot authorize its own root adoption.

This architecture adds one narrow adapter at the repository provenance and publication boundary. It preserves the current evaluator for lifecycle work, binds a candidate-format observation to the predecessor-prepared RLS, and lets publication reacquire the predecessor from an approved exact contract. It does not add another root descriptor or installation profile.

## Components and responsibilities

- **Approved release contract:** owns the one-shot bootstrap tuple—schema, RLS ID, version, canonical `utf8-text-lf-v1` old-lock digest, predecessor version, wheel name, and wheel digest.
- **Released 0.5.0 evaluator:** remains the only runtime that prepares and authoritatively validates the RLS under the installed root.
- **Repository bootstrap binder:** verifies the contract, old root, public wheel, installed predecessor, and RLS; writes only canonical evidence and its binding as an atomic preparatory transaction.
- **Candidate validator:** recognizes the contract-bound preparation schema, validates evidence against the approved tuple and canonical schema-2 lock, and retains the normal schema-3 rule elsewhere.
- **Publication resolver:** replays the same tuple from the governance commit, reacquires public predecessor bytes, validates externally, and gates build/promotion before credentials.
- **Assurance/release lifecycle:** binds the new candidate through a new VREC/RLS chain; human owners retain all decisions.

## Dependency direction

```text
approved bootstrap contract -> expected old lock + predecessor archive
             |                              |
released 0.5 prepare RLS                     +-> binder observation
             |                                      |
             +-------------------------------> evidence-bound RLS
                                                    |
candidate validator + publication resolver <-------+

candidate source/package -> implementation and candidate evidence only
human owners -> requirement, architecture, verification, release decisions
```

Expected identity never comes from candidate runtime claims or from the evidence object being checked.

## Trust boundaries

- The contract is repository authority only after accountable approval; draft text grants nothing.
- The schema-2 lock is untrusted until its canonical `utf8-text-lf-v1` digest and managed integrity pass.
- Public wheel bytes are untrusted until their contract digest passes.
- The binder is candidate-owned repository tooling and therefore may record an observation but may not prepare the RLS, validate as released evaluator, change lifecycle, or alter the root.
- Credentials and external writes remain downstream of complete replay.

## Required patterns

- Exact closed bootstrap tuple in one active approved release contract.
- Canonical evidence rather than a missing-evidence exception.
- Atomic exclusive binding with before/after byte proofs.
- Separate predecessor, candidate-source, and candidate-package runtime identities.
- Stable dual-validator fixtures and publication replay from committed snapshots.
- New candidate, aggregate VREC, and RLS rather than repointing captured records.

## Prohibited patterns

- Generic schema-2 acceptance, version-only trust, or record-ID-only allowlisting.
- Candidate `prepare-release`, candidate root mutation, direct lock synthesis, or pre-publication evaluator upgrade.
- Expected digests supplied only by the runtime or evidence under test.
- Rewriting historical released records or the stopped C/VREC/RLS chain.
- Credential availability before identity, evidence, candidate, bundle, and release agreement.

## Quality attributes

- **Security:** exact contract, lock, wheel, and origins keep the exception narrower than the blocked release.
- **Auditability:** one sidecar and one preparation marker expose the predecessor observation without reinterpreting a release decision.
- **Atomicity:** failed binding changes neither RLS nor sidecar destination.
- **Compatibility:** released 0.5 and candidate 0.6 can both assess the prepared record, while later schema-3 roots retain historical evidence.
- **Removability:** the adapter is disabled for every record except the one declared contract tuple.

## Conformance checks

- Validate complete/partial/unknown/duplicate bootstrap contract fields and exact canonical lock identity, including CRLF/LF equivalence and non-line-ending drift rejection.
- Exercise public-wheel, installed-payload, origin, entry-point, user-site, `PYTHONPATH`, checkout, symlink, traversal, and changed-RLS failures with byte snapshots.
- Prove current 0.5 preparation/validation and candidate validation pass for the one bound record.
- Prove every other ready RLS still requires schema-3 current-lock evidence.
- Replay publisher resolution from exact governance commits and stop before simulated credentials on every mismatch.
- Run full source, package, reproducibility, verifier-owned, hosted, and release-distribution qualification at C2.

## Related ADRs

Accepted `ADR-REB-002` selects this contract-bound adapter over a separately published bridge evaluator, a blanket legacy exception, candidate self-adoption, or ignoring the candidate gate.

The accountable owners authorized a bounded correction on 2026-08-21 at `2026-08-21T16:31:42Z`: old-lock identity means canonical `utf8-text-lf-v1` bytes, not platform-smudged working-tree bytes. Approved status and every other architecture boundary remain unchanged.
