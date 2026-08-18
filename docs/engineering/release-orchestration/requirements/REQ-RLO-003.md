+++
id = "REQ-RLO-003"
type = "requirement"
title = "Reproduce and qualify the exact candidate without credentials"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-18"
updated = "2026-08-18"
statement = "WHEN a released RLS passes resolution, THE SYSTEM SHALL qualify and build its exact candidate twice in credential-free jobs and proceed only when deterministic outputs match each other and the RLS distribution identities."
verification_method = "automated-exact-candidate-replay"

[relations]
derives_from = ["CAP-RLO-001"]
+++

# Requirement: Reproduce and qualify the exact candidate without credentials

## Rationale

A released decision does not justify publishing bytes reconstructed from a moving branch, dirty checkout, different epoch, or credential-bearing environment.

## Preconditions and trigger

Trusted resolution has produced an exact candidate commit, source-date epoch, expected filenames, and expected hashes.

## Required response

Export the exact candidate, prove its commit and tree, run formal and release-specific checks, build the wheel and raw sdist twice at the recorded epoch, normalize both sdists, validate archive safety and wheel metadata, and require byte equality across both builds and the RLS hashes. Upload only the exact final wheel, normalized sdist, checksum manifest, and machine-readable build result for later jobs.

## Failure and boundary behavior

Any source drift, unsafe archive member, test failure, nondeterminism, metadata disagreement, or hash mismatch stops before write permissions or publication credentials become available. No workflow retry may substitute newly accepted hashes for the RLS values.

## Constraints

The qualification job has read-only repository access and no `contents: write`, `pages: write`, `id-token: write`, environment secret, or persistent credential. Candidate code never runs in later credential-bearing jobs.

## Acceptance examples

Two builds matching the RLS produce one bounded artifact bundle. A single-byte difference between builds or against the record fails and uploads no promotable bundle.

## Open decisions

None.
