+++
id = "ADR-REB-001"
type = "adr"
title = "Standard lock ownership of released-evaluator identity"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
decides = ["ARCH-REB-001"]
+++

# ADR: Standard lock ownership of released-evaluator identity

## Status

Accepted. The accountable approval of `ADR-REB-001` and `ARCH-REB-001` selects standard-lock ownership of released-evaluator identity.

## Context

The special self-hosting governor descriptor coupled product development to root governance and contributed directly to the 0.5.0 deadlock. The recovery removed that descriptor and converted the root to the standard lifecycle. The current runtime now recognizes `released-evaluator`, but identity remains procedural: the standard lock records only a tool version and managed hashes, publication code still reads the removed descriptor and uses retired CLI terms, mutation functions do not automatically enforce runtime identity, and release records do not bind evaluator evidence.

The correction must preserve one standard installation, prevent candidate substitution before writes, support a safe legacy-lock migration, work on supported platforms, and avoid moving human authority into automation.

## Decision drivers

- One authoritative, portable evaluator identity source for root commands and publication workflows.
- Cryptographic distinction between installed official payload and candidate code sharing a version string.
- No special repository profile, descriptor, workflow role, or promotion command.
- Transactional migration and zero-write failure.
- Durable but privacy-bounded release-readiness evidence.
- Compatibility with standard consumers and existing historical records.

## Considered options

1. **Keep procedural identity only.** Continue requiring maintainers and workflows to invoke `harnessctl identity` manually. This leaves direct mutators unguarded and permits contract drift.
2. **Restore a dedicated governor descriptor.** Preserve wheel URL, digest, release record, and candidate in `.self-hosting/governor.toml`. This recreates the architectural cause and a second lifecycle.
3. **Enforce only in GitHub workflows.** Pin the evaluator in hosted CI while leaving local mutators unchanged. This protects one path but detects local candidate misuse late and cannot bind one standard root identity.
4. **Own evaluator identity in the standard lock and enforce it through shared boundaries.** Extend the standard lock with canonical payload identity and optional exact archive identity; require the `se_harness` root to pin the archive; reuse one runtime inspector for mutators, workflows, and readiness evidence.
5. **Require a network lookup for every operation.** Resolve the official digest from PyPI on demand. This adds an external runtime dependency, weakens offline operation, and makes availability part of local governance.

## Decision

Select option 4.

Schema 3 of the existing standard `.engineering-harness.lock` owns evaluator version and canonical installed payload identity. When the installing operator or governed upgrade has exact archive bytes, the lock also owns the safe wheel basename and SHA-256; archive fields are mandatory for the `se_harness` root because its publication workflows must reacquire the exact evaluator. The runtime verifies the installed payload, common environment origins, and the archive hash recorded by the installer when available.

All installed-root mutators call one shared fail-closed identity guard internally. Publication and release-bound Pages resolve the external evaluator from the same standard config and lock, acquire exact public bytes, and use the supported `released-evaluator` runtime contract. Release preparation binds a normalized canonical identity observation. Historical governor material remains evidence only.

A separately published target evaluator may migrate a valid legacy lock through the ordinary reviewed upgrade transaction. This migration is not a special profile or promotion command and does not authorize product release or evaluator adoption by itself.

## Consequences

### Positive

- Candidate substitution fails at the first mutating command rather than during later validation.
- Root lifecycle, CI, publication, and readiness use one identity vocabulary and data owner.
- Exact archive identity is durable for high-assurance roots without requiring network access for every command.
- Existing transactional and path-safety mechanisms remain the mutation foundation.
- Historical evidence survives without remaining executable.

### Negative and migration cost

- The lock schema, installer, integrity parser, runtime identity, mutators, provenance schema, validator, workflows, tests, and documentation all change coherently.
- Existing schema-2 roots must perform a separately governed migration before guarded ordinary mutation.
- General installations that did not retain wheel bytes can prove installed payload identity but cannot later enable archive-required publication until an exact archive is selected through upgrade.
- Payload canonicalization becomes a security-sensitive compatibility contract.

### Operational and security consequences

- Operators should download and verify exact wheels before external installation when archive identity is required.
- Publication stops before credential-bearing stages on missing or inconsistent identity.
- Lock modification remains repository state subject to review and managed integrity; it is not a cryptographic signature or substitute for hosting controls.
- Human approval, assurance, release, and recovery rights remain unchanged.

## Validation

Execute `VER-REB-001`. In particular, prove standard-lock schema migration, payload and archive identity, zero-write rejection across every mutator and candidate role, current CLI/workflow compatibility, active legacy-surface absence, canonical evidence binding, separate upgrade sequencing, deterministic conflict observations, and disposable recovery restoration on Windows and POSIX-supported paths.
