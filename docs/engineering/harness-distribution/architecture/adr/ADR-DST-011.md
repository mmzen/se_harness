+++
id = "ADR-DST-011"
type = "adr"
title = "Use an additive single-runtime consumer workflow"
status = "approved"
owners = ["technical-owner", "security-owner", "engineering-owner"]
created = "2026-08-17"
updated = "2026-08-17"

[relations]
decides = ["ARCH-DST-011"]
+++

# ADR: Use an additive single-runtime consumer workflow

## Status

Accepted.

## Context

The standard consumer workflow currently installs a hash-pinned 0.2.1 bootstrap that proves only its own origin and temporary installation, then installs the current release separately to assess the consumer. This applies the SE Harness self-hosting topology to repositories that are not developing the evaluator. It also leaves operators uncertain about which version governs their repository and how CI upgrades.

GitHub already discovers every workflow below `.github/workflows`, so modifying an existing repository-owned workflow is unnecessary. The standard installer already owns a dedicated managed path and a safe upgrade transaction.

## Decision drivers

- make installation and upgrade explainable through one public path;
- ensure the runtime that actually assesses the consumer is the declared release;
- avoid executing checkout copies as the CI oracle;
- preserve existing workflows and customization safety;
- preserve independent self-hosting governance where the evaluator itself is under development;
- minimize runtime roles, jobs, downloads, and operator concepts.

## Considered options

1. **Keep the current two-runtime consumer workflow.** Rejected because the bootstrap does not assess the consumer and creates misleading assurance and upgrade complexity.
2. **Inject a job into an existing workflow.** Rejected because arbitrary YAML ownership, dependencies, matrices, reusable calls, and customizations cannot be merged safely or upgraded deterministically.
3. **Call only a centrally hosted reusable workflow.** Rejected as the standard default because it adds a separate remote workflow pin and availability/compatibility surface; it may remain an optional future repository policy.
4. **Install one dedicated managed workflow using one exact released evaluator.** Selected as the smallest boundary that is additive, reviewable, safely upgradeable, and sufficient for consumers.

## Decision

The standard consumer installation shall own one dedicated `.github/workflows/engineering-harness.yml`. GitHub runs it independently beside existing workflows. It installs one exact released SE Harness version in an isolated environment and uses package-owned entry points for all harness CI semantics. The rendered evaluator version follows the package performing the standard installation or upgrade. Ordinary managed upgrade is the only consumer CI upgrade mechanism.

Workflow installation does not configure branch protection or deployment dependencies; owners make the stable harness check required through external GitHub policy when desired. The `se_harness` implementation repository retains its independently published governor plus candidate evidence planes and its protected `reconcile-governor` path.

## Consequences

Positive consequences are fewer jobs and downloads, one visible consumer version, no obsolete bootstrap, stronger evaluator/check-out separation, no generic YAML merge, and one familiar upgrade transaction.

Negative consequences are continued dependence on exact-version PyPI acquisition, required internal refactoring so selection/validation/dashboard semantics are package-owned, and no automatic proof that GitHub branch protection requires the check. Customized managed workflows continue to block automatic upgrade and need explicit owner reconciliation.

Migration replaces an unmodified older two-job consumer workflow during a later released standard upgrade. It never rewrites a customized workflow and never changes the protected self-hosting workflow through ordinary upgrade.

## Validation

`VER-DST-015` verifies additive installation, single-runtime identity and isolation, package-owned execution, safe migration/idempotence, conflict preservation, external-enforcement wording, and unchanged self-hosting controls through source, package, disposable-repository, and workflow tests.
