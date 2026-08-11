+++
id = "REQ-PMI-005"
type = "requirement"
title = "Centralize integrity semantics"
status = "implemented"
owners = ["engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN installation, upgrade, lock generation, or doctor evaluates managed integrity, THE SYSTEM SHALL use one shared implementation of schema validation, canonicalization, fragment extraction, and digest comparison."
verification_method = "architecture-review"

[relations]
derives_from = ["CAP-PMI-001"]
+++

# Requirement: Centralize integrity semantics

## Rationale

The observed stale lock entry demonstrates that separately maintained hash calculations can drift even when source and canonical templates agree.

## Preconditions and trigger

Any command or internal workflow produces or consumes managed-file lock evidence.

## Required response

Delegate hash-mode interpretation and canonical digest calculation to one dependency-light integrity component. Lock writing and checking must use the same public internal contract and deterministic diagnostics.

## Failure and boundary behavior

Callers may supply bounded path and management-mode context but may not reimplement canonicalization. Unsupported modes fail closed.

## Constraints

The runtime remains standard-library only and must not execute target content.

## Acceptance examples

The same fixture produces identical digest decisions through init, adopt, upgrade, and doctor tests.

## Open decisions

The implementation agent may select the module boundary and function names while preserving a single semantic authority.
