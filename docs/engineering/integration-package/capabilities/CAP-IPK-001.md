+++
id = "CAP-IPK-001"
type = "capability"
title = "Download and install a qualified commit-addressed integration package"
status = "approved"
owners = ["product-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
derives_from = ["INT-IPK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:15:40Z"
decided_by = "product-owner"
+++

# Capability: Download and install a qualified commit-addressed integration package

## Actor and need

A tester needs to evaluate the exact package produced from a selected `main` or
pull-request commit, in a clean environment and outside the source checkout,
without waiting for or pretending to perform a production release.

## Capability statement

`A tester can download one qualified integration artifact, verify its manifest
and checksums, install its wheel without consulting a package index, and trace
the installed version back to one exact Git commit and workflow run.`

## Boundaries

- GitHub Actions artifact storage is the only distribution channel in scope.
- The package is an expiring candidate artifact and never release authority.
- The committed source version remains unchanged. A narrowly declared overlay
  is applied only to disposable exported source used for the integration wheel.
- The retained wheel is available only after the same bytes pass Linux and
  Windows installation checks.
- The package never changes a target repository unless a tester separately runs
  an ordinary harness command against a disposable or explicitly selected
  target.
- Download authentication and GitHub artifact-retention policy remain external
  platform concerns; documentation must state them honestly.

## Outcomes

- One artifact contains one wheel, one canonical manifest, and one checksum
  file.
- The wheel version is unique for its event channel and commit.
- A tester can distinguish public release, candidate source, and integration
  package identities in command output and retained evidence.
- Failed qualification produces no final user-facing integration artifact.
- Expiration is visible and reproducibility comes from the bound commit rather
  than indefinite artifact retention.

## Candidate requirements

`REQ-IPK-001` defines deterministic identity and provenance. `REQ-IPK-002`
defines retained cross-platform installability. `REQ-IPK-003` preserves the
non-release authority boundary and operator guidance.
