+++
id = "CAP-PYP-001"
type = "capability"
title = "Promote a verified GitHub release to PyPI"
status = "approved"
owners = ["repository-owner", "release-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
derives_from = ["INT-PYP-001"]
+++

# Capability: Promote a verified GitHub release to PyPI

## Actor and need

An accountable release owner needs to make an existing verified GitHub release installable through PyPI without rebuilding it or delegating publication to an ambient long-lived secret.

## Capability statement

`A release owner can approve promotion of one final se-harness GitHub release to PyPI using exact artifact hashes, a protected GitHub environment, and short-lived Trusted Publishing credentials.`

## Boundaries

The capability configures a production PyPI publication path for final universal-wheel releases of `se-harness`. It does not grant release authority, choose a tag, infer hashes, create or replace artifacts, publish prereleases, or support another index.

## Outcomes

- One auditable manual workflow dispatch per authorized release.
- Exact GitHub-release artifacts promoted without rebuild.
- No stored PyPI credential.
- Deterministic rejection of draft, prerelease, malformed, mismatched, or duplicate publication attempts.
- Retained evidence connecting PyPI files to GitHub checksums and the governing release decision.

## Candidate requirements

`REQ-PYP-001` through `REQ-PYP-005` govern selection, integrity, identity, publication, and authority separation.
