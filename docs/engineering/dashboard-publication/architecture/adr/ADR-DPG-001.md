+++
id = "ADR-DPG-001"
type = "adr"
title = "Deploy an exact governance snapshot through Pages artifacts"
status = "approved"
owners = ["technical-owner", "repository-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
decides = ["ARCH-DPG-001"]
+++

# ADR: Deploy an exact governance snapshot through Pages artifacts

## Status

Accepted.

## Context

The public dashboard is intended to demonstrate SE Harness by exposing the governed history of its own development. A release has two relevant commits: the tag points to the candidate payload, while a later governance commit contains the verified and released decisions. GitHub Pages can publish from a branch or from an Actions artifact, but neither a moving branch nor the candidate tag alone faithfully represents the completed graph.

The site is promotional and derived. It must not become another authority surface or a managed feature imposed on consumer repositories.

## Decision drivers

- Show the completed release lineage rather than only the software candidate.
- Preserve immutable, reproducible provenance.
- Avoid generated commits and branch-history noise.
- Keep publication repository-specific and independent from consumer installation.
- Use GitHub's supported static Pages deployment path with least privilege and recoverable failure.
- Preserve the existing canonical Explorer contract and accepted optional CDN boundary.

## Considered options

1. Keep screenshots in documentation. Rejected because they become stale and do not permit exploration.
2. Publish the release tag checkout. Rejected because the candidate predates its completed verification and release governance.
3. Publish the current `main` head. Rejected because a moving head may contain post-release work and is not reproducibly release-bound.
4. Commit generated output to a `gh-pages` branch. Rejected because it adds derived repository history, write permissions, and reconciliation obligations without adding formal authority.
5. Resolve the immutable main-history commit that integrated the released record, validate and generate there, then deploy a bounded GitHub Pages artifact. Selected.

## Decision

Adopt option 5. A repository-specific workflow handles a published GitHub Release and supports a controlled manual replay. It uniquely resolves the released formal record, proves that its tag targets its recorded candidate, identifies the immutable main first-parent governance commit where the released state was integrated, validates that checkout using the released governor, and generates the canonical Explorer using the target-local managed generator.

After an exact payload gate, official Pages actions pinned to full commit SHAs upload and deploy the artifact through the protected `github-pages` environment. The site visibly identifies itself as a derived, non-authoritative demonstration of SE Harness governing its own development. Generated output is never committed.

The workflow is deliberately absent from `templates/repository/standard/` and from install, adopt, upgrade, and governor reconciliation. General-purpose dashboard hosting for consumer repositories would require a separate governed decision.

## Consequences

Visitors receive a realistic interactive demonstration tied to a completed release. Maintainers can reproduce deployment from immutable inputs, and failed replacements preserve the previous successful site. The workflow adds external dependencies on GitHub Actions and Pages, operational review of action pins, and nontrivial history resolution tests. The live URL shows the latest selected deployment rather than a permanent per-release archive.

The release candidate and governance snapshot remain separate and are both displayed. Pages success never implies formal verification or release. GitHub availability is not covered by an independent SLO. The optional `3d-force-graph` request retains the exact risk acceptance, CSP, timeout, and fallback in `ADR-DST-008`; this decision grants no additional browser network access.

## Validation

`VER-DPG-001` exercises successful and ambiguous history resolution, annotated and lightweight tags, mismatched candidates, unreachable manual commits, graph failures, deterministic output, allowlisted uploads, public labeling, permission and pin policy, concurrency, environment deployment, replay, failure preservation, and consumer-template isolation.
