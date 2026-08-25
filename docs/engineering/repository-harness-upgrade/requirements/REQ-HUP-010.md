+++
id = "REQ-HUP-010"
type = "requirement"
title = "Prove the exact released successor carrying the directive-surface and risk capabilities"
status = "draft"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a public se-harness release exists whose released record covers WO-ADS-001, WO-ADS-002, and WO-RSK-001, THE SYSTEM SHALL prove that exact release's wheel and installed-payload digests from an isolated installation outside the checkout, against the release record, before any standard-root action names it as the target evaluator."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Prove the exact released successor carrying the directive-surface and risk capabilities

## Rationale

`WO-ADS-001`, `WO-ADS-002`, and `WO-RSK-001` changed the managed templates,
contracts, validator, and layout registry. This repository's root still runs
the released 0.6.0 copies; the operating card, the closed manifest, the
corrective forms, the router scope, and the risk artifact are not in effect
here until a release carries them and the root adopts it. The 0.5.0 RCA's
lesson stands: the target must be an already published, immutable evaluator
proven from outside the checkout, never candidate source.

## Preconditions and trigger

A `released` `RLS-` record whose `releases_work` includes the three work
orders, with its bound wheel and sdist digests, on `main`.

## Required response

Mirror of `REQ-HUP-004` for the successor version: isolated install of the
exact wheel, `identity released-evaluator` with the expected version, wheel
digest, and payload digest equal to the release record's bindings, retained
as canonical evaluator evidence.

## Failure and boundary behavior

A digest mismatch, a candidate-source identity, or an absent released record
stops the upgrade before any root file is planned.

## Constraints

No self-governance: the proof runs with the successor installed outside the
checkout while 0.6.0 remains the governor.

## Acceptance examples

### Example: normal behavior

**Given** `RLS-SEH-013` released for version X with wheel digest W

**When** the successor is installed in an isolated environment and its
identity is captured

**Then** the evidence records version X, wheel W, and the payload digest.

### Example: failure behavior

**Given** a wheel built from the checkout

**When** identity is captured

**Then** it is candidate-source and the upgrade does not proceed.

## Open decisions

The version and digests are supplied by the release record; they are not
asserted here.
