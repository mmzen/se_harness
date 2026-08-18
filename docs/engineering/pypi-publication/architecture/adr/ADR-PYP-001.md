+++
id = "ADR-PYP-001"
type = "adr"
title = "Promote existing release assets with OIDC"
status = "approved"
owners = ["engineering-owner", "security-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-18"

[relations]
decides = ["ARCH-PYP-001"]
+++

# ADR: Promote existing release assets with OIDC

## Status

Accepted.

## Context

The repository already builds, normalizes, independently verifies, and publishes release artifacts to GitHub. PyPI publication needs authentication and should not create a second build path or a long-lived credential.

## Decision drivers

- Exact identity with verified GitHub artifacts.
- No stored PyPI secret.
- Explicit human approval for production distribution.
- Minimal executable surface with OIDC permission.
- Auditable third-party dependencies and external results.
- PyPI filename immutability.

## Considered options

1. Upload manually from a maintainer workstation with Twine and an API token.
2. Rebuild from the tag in GitHub Actions and publish with a stored token.
3. Rebuild from the tag in GitHub Actions and publish with OIDC.
4. Manually approve promotion of exact GitHub release assets with independent hashes and OIDC.

## Decision

Choose option 4. Configure a dedicated manually dispatched workflow and `pypi` environment, both restricted to `main`. Download the named final GitHub release, verify exact filenames, independent expected hashes, and the retained manifest, then pass only those files to the official PyPA publisher. Use PyPI Trusted Publishing and attestations. Do not checkout, build, tolerate duplicates, or store an API token.

Amended on 2026-08-18 by `ADR-RLO-001`: preserve the registered top-level `publish-pypi.yml` identity while the workflow expands into a released-record orchestrator. The operator now selects one released RLS and the workflow derives tag and hashes. The PyPI job, `pypi` environment, exact-asset boundary, and no-checkout/no-build decision remain unchanged. The publisher uses reviewed peeled commit `dc37677b2e1c63e2034f94d8a5b11f265b73ba33` for `v1.14.2`.

## Consequences

- Positive: PyPI bytes match the verified GitHub release; credentials are short-lived; environment approval is visible; the publisher identity and action code are bounded.
- Negative: each release requires a released structured distribution record and protected approval; GitHub/PyPI configuration is external state; universal-wheel naming is intentionally fixed; publication cannot be fully exercised without irreversible external state.
- Operational: action revisions and publisher/environment configuration require periodic review; post-publication evidence is mandatory.
- Security: repository code cannot execute in the OIDC job, but repository administrators and environment approvers remain privileged actors.
- Migration: future prereleases, platform wheels, or automated tag triggers need a new approved decision.

## Validation

Static tests enforce trigger, permissions, environment, input, filename, hash, manifest, no-checkout/no-build/no-secret, immutable action, attestation, and duplicate-failure rules. External inspection verifies the GitHub environment and PyPI publisher. A separately authorized first publication verifies hashes, attestations, and exact-version installation.
