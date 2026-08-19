+++
id = "ADR-RLO-002"
type = "adr"
title = "Repository-owned distribution policy behind portable governance"
status = "approved"
owners = ["engineering-owner", "security-owner", "release-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[relations]
decides = ["ARCH-RLO-002"]
+++

# ADR: Repository-owned distribution policy behind portable governance

## Status

Accepted for definition on 2026-08-18. Implementation remains subject to separate approval of `WO-RLO-002`.

## Context

The RLO-001 workflow is intentionally specific to this repository, but its implementation added `prepare-release --distribution-manifest`, `se_harness.release_distribution`, and SE Harness wheel/sdist rules to the portable package and managed consumer files. The functionality is not present in a tagged release and no current RLS uses the new table, so the boundary can be corrected before compatibility debt forms.

## Decision drivers

- Preserve generic RLS governance and exact commit-bound authority.
- Preserve exact wheel, sdist, checksum, and source-manifest provenance for this repository.
- Keep the one-input GitHub/PyPI/Pages workflow and its trust separation.
- Remove repository assumptions from the wheel and standard installation.
- Avoid a generalized plugin or multi-ecosystem release framework.
- Make invalid local distribution state fail before external mutation.
- Avoid rewriting verified historical artifacts and records.

## Considered options

1. Keep the current optional portable flag and document that consumers may ignore it.
2. Generalize the current schema into a universal artifact and publisher framework.
3. Add a plugin mechanism through which repositories extend core release preparation and validation.
4. Keep core `prepare-release` format-neutral and move the existing distribution schema, binding, and validation into repository-owned tooling.
5. Remove structured distribution provenance entirely and rebuild whatever the candidate produces at publication time.

## Decision

Choose option 4.

Remove the unreleased distribution flag, packaged module, core schema validation, and consumer-template guidance. Preserve generic RLS preparation unchanged. Add an explicit repository-owned binding step after generic preparation and before accountable review. Keep the existing schema-1 distribution table as local SE Harness metadata and require trusted repository tooling to validate it both during binding and workflow resolution.

Use one shared repository implementation across the manifest generator, binder, policy check, resolver, and tests. Keep it outside `se_harness*` and the standard template. Do not add a plugin interface or generic payload abstraction in this correction.

## Consequences

- Positive: consumer installations return to repository-independent governance and the product dependency direction becomes explicit.
- Positive: the release owner retains exact distribution identity and the production workflow retains all RLO-001 guarantees.
- Positive: removal occurs before a tagged release, so no public CLI deprecation or RLS migration is required.
- Negative: SE Harness release preparation uses two agent-run commands rather than one portable command.
- Negative: core `harnessctl validate` no longer assesses the local distribution table; repository CI and workflow validation become mandatory compensating controls.
- Operational: binding failure leaves a valid but non-publishable local ready RLS, which must not be committed for release review until corrected.
- Security: trusted-main code owns package validation; candidate code remains excluded from credential boundaries.
- Migration: standard managed templates and validator hashes change through the normal transactional upgrade mechanism; historical records remain untouched.

## Validation

- Prove the built wheel and disposable consumer installation contain no distribution-specific product behavior.
- Prove generic RLS preparation still enforces exact coverage and candidate identity.
- Prove repository binding is atomic and exact across success, replay, malformed, mismatch, and conflict cases.
- Prove the trusted resolver uses only main-owned repository code and blocks invalid distribution state before qualification and credentials.
- Re-run the existing workflow security, reproducibility, replay, PyPI, and Pages suites without production mutation.
