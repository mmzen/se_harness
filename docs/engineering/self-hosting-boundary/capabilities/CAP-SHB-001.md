+++
id = "CAP-SHB-001"
type = "capability"
title = "Govern and qualify a self-hosted harness through isolated identities"
status = "approved"
owners = ["repository-owner", "engineering-owner", "quality-owner", "release-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
derives_from = ["INT-SHB-001"]
+++

# Capability: Govern and qualify a self-hosted harness through isolated identities

## Capability statement

Maintainers can develop a new harness version under an exact released governor, test candidate source as untrusted implementation, accept the built candidate in fresh repositories, and promote the published version to governor later without confusing those roles or granting the candidate authority over itself.

## Observable outcomes

- One released governor identity is pinned by immutable version, artifact name, source URL, and SHA-256.
- The governor's operational installation and lock are isolated outside the candidate checkout and attributable only to the released governor.
- Candidate-source checks explicitly resolve modules from the checkout and cannot claim external independence.
- Candidate-package checks explicitly resolve modules from an isolated installed wheel and cannot fall back to the checkout.
- Independent CI uses the governor only for same-version installation smoke and explicitly compatible read-only bootstrap checks.
- CI fails closed on missing identity evidence, path shadowing, cross-version `doctor`, checkout writes, or candidate/governor ambiguity.
- A separate post-publication workflow advances the governor for the next cycle.

## Exclusions

This capability does not create a second installation profile for consumers, let the old governor validate semantics it does not understand, make candidate tests authoritative, publish software automatically, or permit historical VREC/RLS mutation.
