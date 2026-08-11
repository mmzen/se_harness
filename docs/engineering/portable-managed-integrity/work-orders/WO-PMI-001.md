+++
id = "WO-PMI-001"
type = "work_order"
title = "Implement portable managed-file integrity"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-PMI-001", "REQ-PMI-002", "REQ-PMI-003", "REQ-PMI-004", "REQ-PMI-005", "REQ-PMI-006", "REQ-PMI-007"]
specifications = ["SPEC-PMI-001"]
architecture = ["ARCH-PMI-001", "ADR-PMI-001"]
verification = ["VER-PMI-001"]
+++

# Work Order: Implement portable managed-file integrity

## Objective

Replace platform-sensitive managed-text integrity with the versioned canonical schema-2 contract, migrate legacy locks conservatively, regenerate a correct self-repository lock, and verify the complete source-to-wheel installation path.

## Authorization

The accountable repository owner explicitly accepted this bounded work order on 2026-08-11 with the instruction `ok accepted`. The authorization covers the implementation and verification described here; it does not authorize a commit, push, pull request, verification transition, release record, tag, package publication, or deployment.

## In scope

- Shared canonical UTF-8 text hashing and explicit lock-schema interpretation.
- Schema-2 lock writing for complete managed files and managed fragments.
- Mode-aware doctor and upgrade behavior, including conservative schema-1 migration.
- Deterministic diagnostics for exact, canonical, customized, missing, malformed, and unsupported states.
- Safe self-repository lock regeneration through the supported writer.
- Documentation and canonical standard-template updates required by the lock contract.
- Property, unit, integration, security, compatibility, self-repository, wheel, and fresh-install tests.
- Retained evidence for the corrected candidate and superseding or recapturing the ready aggregate verification record as governed after implementation.

## Out of scope

- Changing repository-wide Git newline policy.
- Supporting binary managed assets or arbitrary encodings.
- Automatically rewriting customized or ambiguous legacy content.
- Adding installation profiles, runtime dependencies, or network services.
- Transitioning `VREC-AGR-001`, creating a release record or tag, committing, pushing, opening a pull request, publishing a package, or deploying without separate authorization.

## Authorized decision envelope

After explicit approval, the implementation agent may select internal module names, typed result structures, bounded diagnostic wording, fixture organization, and a deterministic supported mechanism for regenerating the self lock. It may not alter canonicalization, migration proof, ownership boundaries, authority semantics, or compatibility commitments.

## Constraints

Preserve one standard installation, Python 3.11 compatibility, standard-library runtime, path containment, symlink rejection, atomic writes, target-content non-execution, customized-file preservation, source/canonical parity, and commit-bound provenance sequencing.

## Expected change surface

Managed-integrity helpers, installer and upgrade classification, doctor diagnostics, lock writer/schema handling, distribution workflow documentation, canonical templates when required, self-repository lock generation, and deterministic test suites.

## Required verification

Execute `VER-PMI-001`, the artifact validator, the complete unit suite, CLI help, doctor on the source repository, upgrade planning/application fixtures, LF/CRLF property and integration cases, path and fragment security regressions, source/canonical parity, wheel inspection, and fresh installation from the wheel.

## Evidence to record

Retain exact commands and results; before/after doctor output; hash vectors; schema migration cases; self-lock generation method; test counts; wheel hash and contents; fresh-install results; deviations; platform limitations; and residual risks in `docs/engineering/portable-managed-integrity/evidence/WO-PMI-001-verification.md`.

## Stop and escalate conditions

Stop if safe legacy migration requires guessing original bytes, canonicalization would hide non-newline edits, a binary mode becomes necessary, customized content would be overwritten, existing locks become unreadable, source and packaged semantics diverge, or a lifecycle, release, or publication action is implied.

## Completion report format

Report implemented requirements, exact verification results, lock migration behavior, corrected candidate identity only after separately authorized creation, deviations, residual risks, and explicitly excluded governance and release actions.
