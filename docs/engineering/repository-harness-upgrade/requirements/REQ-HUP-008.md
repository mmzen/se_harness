+++
id = "REQ-HUP-008"
type = "requirement"
title = "Assess governor changes through exact base and target identities"
status = "approved"
owners = ["repository-owner", "quality-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "WHEN hosted CI observes a candidate whose selected governor differs from its trusted base revision, THE SYSTEM SHALL validate one approved exact governor-transition contract, immutable target evaluator identity, canonical transaction evidence, and complete target-root qualification without running the predecessor evaluator against the successor root or hard-coding a concrete version pair."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-HUP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T20:22:49Z"
decided_by = "repository-owner"
+++

# Requirement: Assess governor changes through exact base and target identities

## Required behavior

- Resolve one full trusted base commit for pull-request, ordinary push, and
  branch-creation events; ambiguity is a blocking error.
- Read the selected governor version and canonical lock identity at base and
  target.
- For equal versions, report that the transition assessment is not applicable;
  ordinary managed CI remains authoritative.
- For different versions, require one approved work order whose evaluator-
  upgrade declaration binds the prior lock hash, target version, archive name,
  archive SHA-256, and installed-payload SHA-256.
- Require committed canonical transaction evidence that binds the same base,
  target, scope, and immutable evaluator identity.
- Install only the exact declared public target wheel outside the checkout,
  verify archive and installed-payload identities, and run target-governor
  doctor and complete validation directly on the target checkout.
- Prove that assessment did not change the checkout and did not receive or use
  write credentials.

## Failure behavior

Fail before target evaluation on missing or multiple contracts, untrusted or
unavailable base, non-ancestor base where ancestry is required, malformed
configuration or lock, undeclared version change, digest mismatch, wrong
runtime origin, evidence mismatch, dirty checkout, or credential exposure.

## Compatibility boundary

Historical predecessor compatibility may be exercised only against an
immutable historical fixture or explicit manual rehearsal. It is not inferred
from, or overlaid onto, the current repository.
