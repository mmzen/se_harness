+++
id = "ARCH-DPG-001"
type = "architecture"
title = "Release-bound static demonstration deployment"
status = "implemented"
owners = ["technical-owner", "security-owner", "service-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
addresses = ["REQ-DPG-001", "REQ-DPG-002", "REQ-DPG-003"]
conforms_to = ["SPEC-DPG-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "responsibility-or-dependency-direction", "security-privacy-or-trust-boundary", "deployment-or-operating-model", "concurrency-consistency-reliability-or-failure-strategy", "technology-framework-vendor-or-external-service", "cross-cutting-policy"]
rationale = "Publishing repository-derived data through GitHub Actions and Pages adds a public deployment boundary, external services, privileged deployment steps, release-to-governance provenance resolution, concurrency behavior, and cross-cutting non-authority rules."
assessed_by = "technical-owner"
+++

# Architecture: Release-bound static demonstration deployment

## Context and scope

SE Harness already generates a self-contained Explorer from a deterministic canonical snapshot. This architecture adds only the repository-specific path from a completed SE Harness release to a public static demonstration. It does not create a dashboard service or change the consumer harness.

## Components and responsibilities

- The GitHub release event or accountable replay supplies the selected release identity.
- A provenance resolver reads main-history release records and Git objects, then selects one immutable governance commit or fails.
- The independently released governor validates the formal graph at that commit.
- The target-local canonical Explorer generator creates the static demonstration from the validated checkout.
- A payload gate checks the file allowlist, schema, provenance, hashes, and visible non-authority notice.
- The Pages upload action transports one static artifact.
- The Pages deploy action updates the protected `github-pages` environment.
- GitHub Actions logs and the deployment environment expose operational status; formal artifacts retain governance authority.

## Dependency direction

The release event and Git history feed provenance resolution. The immutable checkout feeds independent validation and the existing one-way Explorer pipeline from repository artifacts to canonical snapshot to safe static presentation. The payload gate feeds Pages upload and deployment. Nothing flows from Pages back into repository artifacts, Git history, releases, packages, or lifecycle state.

Consumer repositories do not depend on this workflow. The standard distribution, installed `harnessctl`, and self-hosting governor do not depend on the public site.

## Data and control flow

```text
published GitHub Release or authorized replay
  -> unique released RLS + tag/candidate checks
  -> immutable main-history governance commit
  -> released-governor graph validation
  -> target-local canonical dashboard generation
  -> schema, provenance, hash, and payload allowlist gate
  -> Pages artifact upload
  -> protected github-pages deployment
  -> public read-only SE Harness development demonstration
```

## Trust boundaries

Release metadata, manual inputs, repository artifacts, Git paths, generated files, and external action outputs are untrusted until validated. The Actions runner crosses into the GitHub Pages deployment boundary using short-lived platform credentials with job-scoped permissions. Published files become public. GitHub Actions, GitHub Pages, action publishers, PyPI/GitHub release distribution for the independent governor, and the existing unpkg runtime exception are external dependencies.

## Required patterns

- Immutable dual provenance: candidate commit for released software and governance commit for completed decision history.
- Unique, fail-closed resolution from main first-parent history.
- Released-governor validation separated from target-local generation.
- New empty staging directory and exact payload allowlist.
- Immutable action pins, least privilege, protected environment, serialized deployment, and observable hashes.
- Static derived output with visible demonstration and non-authority labeling.
- Existing canonical Explorer schema, safe renderer, CSP, accessibility, and 3D fallback.

## Prohibited patterns

- Publishing the tag checkout as though it contains the later release decision.
- Publishing a mutable default-branch head or arbitrary manual branch.
- Treating successful deployment as verification, release approval, or evidence completeness.
- Running Pages deployment from the standard consumer template or adding it to managed upgrade/reconciliation.
- Committing generated site output to any branch.
- Broad write tokens, event-text shell evaluation, unpinned actions, unexpected upload files, or an expanded runtime network boundary.
- Using the target-local candidate validator to govern its own correctness.

## Quality attributes

The design prioritizes provenance clarity, reproducibility, semantic fidelity, least privilege, fail-closed behavior, recoverable deployment, visitor accessibility, and consumer isolation. Promotional-site availability is best effort and subordinate to governance correctness.

## Conformance checks

`VER-DPG-001` checks unique provenance resolution, main-history reachability, tag peeling, released-record matching, independent validation, deterministic generation, payload allowlisting, visible non-authority copy, workflow permissions, immutable action pins, deployment concurrency, protected environment use, replay, failure behavior, and absence from consumer-managed templates.

## Related ADRs

`ADR-DPG-001` decides this deployment architecture. `ADR-DST-008` remains the active decision for the canonical Explorer model boundary and its exact optional CDN risk; this architecture neither supersedes nor broadens it.
