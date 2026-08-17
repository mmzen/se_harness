+++
id = "ARCH-DST-011"
type = "architecture"
title = "Single-runtime consumer CI boundary"
status = "implemented"
owners = ["technical-owner", "security-owner"]
created = "2026-08-17"
updated = "2026-08-17"

[relations]
addresses = ["REQ-DST-056", "REQ-DST-057", "REQ-DST-058", "REQ-DST-059"]
conforms_to = ["SPEC-DST-015"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "responsibility-or-dependency-direction", "security-privacy-or-trust-boundary", "deployment-or-operating-model", "cross-cutting-policy", "material-alternatives"]
rationale = "The change removes a runtime role, moves CI authority from checkout scripts to the installed release, defines additive workflow ownership, and preserves a different self-hosting trust boundary; those are significant system, dependency, deployment, and trust decisions with material alternatives."
assessed_by = "technical-owner"
+++

# Architecture: Single-runtime consumer CI boundary

## Context and scope

The standard consumer installation currently carries a checksum-pinned older bootstrap job plus a separately installed current candidate evaluator. The bootstrap validates only its own temporary target; consumer semantics come from the later runtime. This architecture replaces that consumer topology with one exact released evaluator while keeping the implementation repository's self-hosting topology separate and protected.

## Components and responsibilities

- **Installer and upgrader:** render and safely own the dedicated consumer workflow through the existing standard transaction.
- **Dedicated GitHub workflow:** respond independently to repository events and orchestrate one evaluator job.
- **Released evaluator environment:** provide all executable work selection, preflight, diagnosis, validation, inspection if selected, and dashboard semantics outside the checkout.
- **Consumer checkout:** provide untrusted artifacts, evidence, configuration, and application code under assessment.
- **Repository-owned workflows:** run application tests, builds, deployments, and other project policy independently.
- **GitHub rulesets and branch protection:** optionally make checks mandatory through externally administered policy.
- **Self-hosting controls:** retain the independent released-governor and candidate-source/package planes only in the SE Harness implementation repository.

## Dependency direction

The managed workflow selects an exact external released package. The evaluator reads the checkout as data; the checkout never supplies executable evaluator semantics. Repository-owned workflows do not depend on or get rewritten by the installer. External GitHub policy may require both check results, but no repository file is treated as proof that this enforcement exists.

## Data and control flow

1. The operator installs a released package and initializes, adopts, or upgrades a repository.
2. The managed transaction writes or updates the dedicated workflow and lock evidence.
3. GitHub discovers that workflow beside any existing workflows.
4. A runner installs the exact declared release into a temporary environment and proves its identity.
5. Package-owned logic selects authorized PR work and evaluates repository data.
6. Results and the optional dashboard remain observations; GitHub rulesets decide whether the check gates merge.

## Trust boundaries

The package index and exact declared release are external supply-chain dependencies. The runner environment, repository checkout, event payload, and generated output are untrusted until checked at their applicable boundaries. Exact-version acquisition and isolated origin prevent accidental checkout substitution but do not claim repository-pinned artifact attestation. Self-hosting adds a separate older-governor boundary because its checkout is itself the evaluator implementation; consumers do not.

## Required patterns

- one dedicated managed workflow rather than generic YAML merge;
- one exact released evaluator and one isolated environment per consumer run;
- package-owned CI semantics with explicit untrusted-repository inputs;
- stable workflow/check identity and read-only permissions;
- plan-first, conflict-preserving, failure-atomic installation and upgrade;
- explicit external-enforcement disclosure;
- exact role classification before applying self-hosting exceptions.

## Prohibited patterns

- a second consumer bootstrap that validates only itself;
- importing or directly executing evaluator logic from the checkout;
- modifying unrelated workflows during init, adopt, or upgrade;
- treating workflow presence as branch-protection proof;
- invoking `reconcile-governor` for a consumer;
- substituting the consumer workflow for the protected implementation-repository workflow.

## Quality attributes

The design favors comprehensibility, deterministic ownership, low CI latency, isolated evaluator identity, safe upgrades, and explicit authority. It accepts PyPI exact-version availability as the simple consumer dependency and leaves stronger supply-chain attestation to a separately governed enhancement.

## Conformance checks

Tests render new and adopted repositories with and without existing workflows; compare unrelated bytes; reject conflicts; assert exactly one released evaluator/version and no consumer governor fields; prove package origins outside adversarial checkouts; execute package-owned selection and assessment; migrate unmodified older workflows; preserve customized workflows; verify idempotence; and prove self-hosting protected controls remain unchanged.

## Related ADRs

`ADR-DST-011` decides the additive dedicated workflow, single released evaluator, package-owned CI semantics, ordinary-upgrade path, and retained self-hosting exception.
