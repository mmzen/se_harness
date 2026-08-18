+++
id = "ARCH-RLO-001"
type = "architecture"
title = "Trust-separated released-record orchestration"
status = "approved"
owners = ["engineering-owner", "security-owner", "release-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[relations]
addresses = ["REQ-RLO-001", "REQ-RLO-002", "REQ-RLO-003", "REQ-RLO-004", "REQ-RLO-005", "REQ-RLO-006", "REQ-RLO-007", "REQ-RLO-008"]
conforms_to = ["SPEC-RLO-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "responsibility-or-dependency-direction", "public-interface-or-protocol", "security-privacy-or-trust-boundary", "deployment-or-operating-model", "concurrency-consistency-reliability-or-failure-strategy", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The change coordinates irreversible GitHub and PyPI state, protected OIDC and Pages environments, candidate execution, formal release provenance, recovery semantics, and an externally registered workflow identity; these boundaries and alternatives require an explicit architectural decision."
assessed_by = "engineering-owner"
+++

# Architecture: Trust-separated released-record orchestration

## Context and scope

The last mile crosses formal governance, untrusted candidate code, reproducible package construction, Git object and GitHub Release writes, a protected PyPI OIDC publisher, a protected Pages deployment, and public observation. These are not one atomic system. The architecture must reduce operator inputs while preserving smaller credential boundaries and honest partial outcomes.

The scope is repository-specific SE Harness publication after a released RLS is in `main`. It does not govern consumer-repository CI or create formal authority.

## Components and responsibilities

- **Trusted-main resolver:** parses one RLS ID, validates the graph with the released governor, resolves first-parent governance provenance, and emits canonical immutable identities.
- **Distribution-manifest support:** validates candidate-generated bundle evidence and copies its exact fields into a ready RLS proposal without publishing.
- **Credential-free qualifier:** checks out the candidate, runs release gates, builds twice, compares deterministic bytes, and uploads a bounded bundle.
- **GitHub materializer:** verifies transferred hashes, creates or reconciles the tag and draft/final release, and owns only repository-content write permission.
- **PyPI publisher:** downloads final GitHub assets, reconciles public PyPI state, waits on the protected environment, and owns only read plus OIDC permissions.
- **Pages publisher:** generates from the immutable governance snapshot and separates Pages write permission from build and package publication.
- **Result observer:** performs public checks and emits stage-specific JSON and summaries without formal transitions.
- **Manual Pages recovery:** replays only derived demonstration deployment from explicit immutable identities in a main-authorized context.

## Dependency direction

Formal released provenance controls resolution. Resolution controls qualification. Qualification produces inert bytes consumed by GitHub publication. PyPI depends only on the final GitHub Release, never on candidate checkout or build output directly. Pages depends on the GitHub release identity and immutable governance snapshot, not on PyPI success. Observation depends on public states and cannot feed new release identity into an active run.

The existing `SPEC-PYP-001`, `ARCH-PYP-001`, and `OPS-PYP-001` continue to constrain the PyPI job; the existing dashboard-publication chain constrains Pages. Orchestration may narrow and connect their triggers but may not bypass their controls.

## Data and control flow

1. One RLS ID enters a main-only manual dispatch.
2. The resolver emits a canonical release plan containing all immutable identities.
3. The qualifier independently reconstructs the candidate and emits exact bytes plus a result manifest.
4. The GitHub job re-verifies the plan and bytes before any tag or release mutation.
5. PyPI and Pages consume GitHub-complete state through separate permission boundaries.
6. The observer joins stage outputs into evidence without changing formal artifacts.

No stage accepts replacement identity values from a downstream job or operator.

## Trust boundaries

- **Formal boundary:** only a released RLS on main is authoritative input; workflow dispatch is an operational request.
- **Execution boundary:** candidate code is untrusted and executes only in a no-credential job.
- **GitHub write boundary:** tag and release mutation uses trusted-main code and exact transferred bytes.
- **PyPI identity boundary:** the top-level workflow filename and `pypi` environment are externally registered identity; no reusable workflow is substituted.
- **Pages boundary:** generation is read-only; only the deploy job receives Pages write/OIDC under a main-authorized event.
- **External-state boundary:** GitHub, PyPI, and Pages responses are independently verified and classified.

## Required patterns

- One canonical release plan derived from one RLS.
- Full-history, first-parent provenance resolution from `main`.
- Two deterministic builds at the candidate epoch.
- Artifact transfer rather than candidate checkout across credential boundaries.
- Job-scoped least privilege and full action pins.
- Draft-before-final GitHub Release staging.
- Explicit absent/exact/partial/mismatched reconciliation.
- Protected PyPI approval and main-context Pages deployment.
- Separate stage results rather than one aggregate score.

## Prohibited patterns

- Selecting latest release state or accepting redundant override inputs.
- Running candidate code in any write, OIDC, or Pages job.
- Using a reusable workflow as the PyPI Trusted Publisher while PyPI does not support it.
- Rebuilding in the GitHub or PyPI publication boundary.
- Moving tags, replacing final assets, suppressing publisher duplicates, deleting partial external state, or rewriting history.
- Letting a `release` tag-ref event enter the main-only Pages environment.
- Automatically committing evidence or transitioning a formal artifact.

## Quality attributes

Determinism, provenance, least privilege, idempotent observation, failure containment, auditability, and operational simplicity take precedence over minimum wall-clock time. Human interaction is reduced to selection and protected approval without combining incompatible privileges.

## Conformance checks

- Static workflow tests prove trigger, input count, ref restriction, permissions, environments, action pins, checkout placement, and absence of candidate execution in credentialed jobs.
- Resolver and state-machine fixtures cover main history, manifest schema, exact and mismatched GitHub/PyPI states, and Pages recovery.
- Two-build tests prove package and checksum determinism at a recorded epoch.
- Hosted tests exercise workflow parsing and credential-free jobs without creating production external state.
- Manual review confirms GitHub environment rules and the PyPI workflow filename/environment registration.

## Related ADRs

`ADR-RLO-001` selects a single top-level, trust-separated orchestration while preserving the existing PyPI publisher workflow identity.
