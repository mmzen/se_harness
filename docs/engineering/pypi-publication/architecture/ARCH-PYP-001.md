+++
id = "ARCH-PYP-001"
type = "architecture"
title = "Separated exact-asset PyPI publication boundary"
status = "implemented"
owners = ["engineering-owner", "security-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
constrains = ["REQ-PYP-001", "REQ-PYP-002", "REQ-PYP-003", "REQ-PYP-004", "REQ-PYP-005"]
+++

# Architecture: Separated exact-asset PyPI publication boundary

## Context and scope

Production package publication combines mutable repository administration, externally retained release assets, short-lived deployment identity, and an immutable package index. The credential-bearing boundary must remain smaller than the build and verification boundary.

## Components and responsibilities

- **Verified GitHub release:** retains the candidate-derived wheel, normalized sdist, and checksum manifest.
- **Manual dispatch preflight:** validates explicit release identity and copies only exact verified distributions into `dist/`.
- **GitHub `pypi` environment:** applies human deployment approval and binds the OIDC subject expected by PyPI.
- **Pinned PyPA publisher:** validates metadata, exchanges the OIDC identity, creates attestations, and uploads.
- **Governance evidence:** records authorization before dispatch and observed PyPI state after completion.

## Dependency direction

Publication depends on an already verified and released artifact set. Build, tests, package source, and repository scripts never depend on or execute inside the PyPI credential boundary.

## Data and control flow

The release owner selects a tag and retained hashes; environment approval releases the job; GitHub provides release metadata/assets; shell preflight validates state and integrity; only two distribution files cross into `dist/`; the pinned publisher obtains a short-lived PyPI token and uploads; humans retain observed evidence.

## Trust boundaries

Workflow inputs, GitHub release state, downloaded bytes, checksum manifests, mutable action references, repository content, and external-service responses are untrusted. The protected environment and exact PyPI publisher configuration are administrative controls, not formal release authority.

## Required patterns

- Manual explicit inputs and environment approval.
- Main-only job and environment deployment policy.
- Independent expected hashes plus exact manifest comparison.
- Job-scoped least privilege and OIDC.
- Full-SHA action pinning.
- No checkout, repository-code execution, build, or credential fallback.
- Fail-closed duplicate and metadata behavior.

## Prohibited patterns

- `on: release` automatic production publication.
- `actions/checkout` or package building in the OIDC job.
- PyPI API tokens, passwords, `.pypirc`, or secret-based fallback.
- Mutable third-party action references.
- `skip-existing`, artifact rewriting, or implicit latest-release selection.

## Quality attributes

Provenance, least privilege, human control, determinism, auditability, and failure visibility take precedence over one-click convenience.

## Conformance checks

Artifact validation, static workflow tests, workflow syntax validation on GitHub, GitHub environment API inspection, PyPI publisher inspection by the owner, checksum preflight using known release data, and post-publication hash/installation evidence.

## Related ADRs

`ADR-PYP-001` selects Trusted Publishing and promotion of existing release assets.
