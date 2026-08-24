+++
id = "CAP-HUP-003"
type = "capability"
title = "Qualify an exact governor succession without version-specific CI logic"
status = "approved"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
derives_from = ["INT-HUP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T20:22:49Z"
decided_by = "repository-owner"
+++

# Capability: Qualify an exact governor succession without version-specific CI logic

## Actor and need

A repository owner needs the same controlled CI behavior when moving from any
released governor N to an exact released successor N+1, without teaching a
repository-owned workflow each concrete version pair.

## Capability statement

`A repository owner can qualify an approved exact governor succession from a trusted base revision to a locked target revision while ordinary changes continue to use only the current governor.`

## Boundaries

- The managed Engineering Harness workflow remains responsible for ordinary
  current-root validation.
- The transition assessment observes base and target identities, approved
  upgrade metadata, transaction evidence, and target-governor results.
- Historical predecessor assessment is not performed against the current root.
- No transition assessment approves work, verifies a VREC, merges, publishes,
  deploys, changes credentials, or changes external policy.

## Outcomes

- Same-version changes take a deterministic not-applicable transition path and
  remain governed by normal managed CI.
- Version-changing candidates fail closed on ambiguous base identity, missing
  approval, hash mismatch, unverified evaluator origin, incomplete evidence,
  checkout mutation, or target-governor failure.
- Cross-platform tests accept legitimate canonical-byte convergence while
  preserving evaluator-role separation.

## Candidate requirements

- `REQ-HUP-008`: select and validate the governor-transition lane from exact
  trusted identities and evidence rather than hard-coded versions.
- `REQ-HUP-009`: make root/candidate assertions stable across LF and CRLF
  checkouts without weakening lock or origin checks.
