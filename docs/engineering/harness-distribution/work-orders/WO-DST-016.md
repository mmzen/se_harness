+++
id = "WO-DST-016"
type = "work_order"
title = "Simplify consumer GitHub CI installation and upgrade"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "technical-owner", "quality-owner", "security-owner"]
created = "2026-08-17"
updated = "2026-08-17"

[assurance]
commit_bound_verification = "required"
rationale = "Future consumer governance and upgrade decisions will rely directly on the changed managed CI, package-owned evaluator behavior, trust boundary, and migration mechanics."
decided_by = "repository-owner"

[relations]
implements = ["REQ-DST-056", "REQ-DST-057", "REQ-DST-058", "REQ-DST-059"]
specifications = ["SPEC-DST-015"]
architecture = ["ARCH-DST-011", "ADR-DST-011"]
verification = ["VER-DST-015"]
+++

# Work Order: Simplify consumer GitHub CI installation and upgrade

## Lifecycle

On 2026-08-17 the repository owner challenged the need for a separate bootstrap runtime in consumer repositories, accepted the KISS proposal for one additive workflow and one released evaluator, clarified GitHub's automatic multi-workflow discovery, and requested this artifact packet. After reviewing the conflict behavior, the owner explicitly instructed `ok, then go implement`. That decision approves `REQ-DST-056..059`, `SPEC-DST-015`, `ARCH-DST-011`, `ADR-DST-011`, `VER-DST-015`, and this bounded work order and transitions implementation to `in_progress`.

Implementation, tests, documentation, and retained local evidence within the approved scope are authorized. Commit, push, pull request, verification-record preparation or transition, release, package publication, demonstrator deployment, and external GitHub ruleset or branch-protection changes remain separate decisions.

## Objective

Replace the standard consumer workflow's obsolete bootstrap/current-runtime split with one dedicated additive workflow using one exact released package for all harness CI semantics, and make init/adopt/upgrade the only installation and upgrade path while preserving the implementation repository's self-hosting governor boundary.

## In scope

- Replace only the canonical standard consumer workflow with the single-runtime contract in `SPEC-DST-015`.
- Make consumer work-order selection, preflight, doctor, graph validation, and Explorer generation execute through package-owned evaluator entry points.
- Preserve target-local managed material as data/integrity content where still required without executing checkout copies as the CI oracle.
- Keep init and adopt additive beside zero or more existing GitHub workflows and fail on exact-path conflict.
- Keep standard upgrade plan-first, failure-atomic, customization-preserving, and responsible for the workflow version and lock migration.
- Remove consumer bootstrap/governor constants and tests that encode the obsolete two-runtime consumer model.
- Preserve the root self-hosting classifier, protected controls, independent released governor, candidate source/package evidence, and `reconcile-governor` behavior.
- Add focused source, package, workflow, migration, adversarial, security, and regression tests plus retained work-order evidence.
- Update operator and coding-agent documentation to explain automatic GitHub workflow discovery, parallel execution, required-check external configuration, and the distinct self-hosting exception.

## Out of scope

- Editing or merging arbitrary repository-owned workflows.
- Configuring GitHub rulesets, branch protection, required checks, environments, permissions, deployments, or secrets.
- Making application tests/builds part of the generic harness workflow.
- Supporting GitLab, Azure Pipelines, other CI providers, selectable profiles, or reusable-workflow installation modes.
- Adding repository-pinned wheel hashes, artifact attestations, alternate package indexes, offline installation, or a new runtime dependency.
- Removing portable installed scripts from the standard distribution unless required solely to eliminate executable CI authority and explicitly accepted during implementation review.
- Reconciling or promoting the root self-hosting governor, changing its descriptor, releasing a version, publishing a package, or deploying the demonstrator.

## Authorized decision envelope

After explicit implementation approval, the agent may choose stable internal package module names, the narrow automation-facing work-order-selection interface, exact step labels, test fixture organization, and safe import/refactor mechanics. It may not add a second consumer runtime, execute checkout scripts as the evaluator, merge unrelated YAML, infer or mutate external enforcement, weaken managed conflict handling, substitute the consumer workflow for self-hosting, or claim package-index acquisition provides unapproved attestation guarantees.

## Constraints

- Preserve Python 3.11+ standard-library runtime behavior and the one-standard-installation rule.
- Treat targets, events, workflows, paths, configuration, artifacts, evidence, and checkout code as untrusted.
- Preserve exact exit, authority, lifecycle, validation-plane, provenance, and dashboard semantics except where this packet explicitly changes runtime ownership.
- Keep writes contained, planned, deterministic, failure-atomic, and schema-2 integrity-aware.
- Preserve unrelated user changes and stop if the branch or worktree changes unexpectedly.
- Do not build a promotable distribution without separate release authorization.

## Expected change surface

- canonical standard GitHub workflow and installer rendering variables;
- package-owned validator, inspector/dashboard, event-selection, and CLI adapters needed to remove checkout execution from consumer CI;
- installer, upgrade, doctor, preflight, package-data, and managed-integrity tests;
- self-hosting boundary regression tests proving protected behavior is unchanged;
- installation/upgrade, command, CI, and self-hosting documentation;
- distribution acceptance scenarios, domain index, and `WO-DST-016` evidence.

## Implementation plan

1. Obtain explicit approval for `REQ-DST-056..059`, `SPEC-DST-015`, `ARCH-DST-011`, `ADR-DST-011`, `VER-DST-015`, and this work order.
2. Run start preflight and read its complete manifest.
3. Add failing workflow, install/adopt, conflict, upgrade, import-shadowing, checkout-script, and self-hosting-preservation tests.
4. Refactor shared evaluator semantics behind package-owned entry points without changing formal graph behavior.
5. Replace the standard consumer template with one isolated exact-version job and remove obsolete consumer governor constants.
6. Implement and test unmodified migration, idempotence, customized blocking, and package-only versus repository-apply boundaries.
7. Update concise operator and agent documentation without duplicating policy.
8. Execute `VER-DST-015`, full regression, formal validation, both preflight phases, deterministic Explorer, source/package acceptance, workflow syntax, managed parity, and diff hygiene.
9. Retain evidence, transition completed implementation artifacts only as authorized, and stop for candidate-commit and commit-bound verification decisions.

## Required verification

Execute every case in `VER-DST-015`, affected `VER-DST-001`, `VER-IAR-001..002`, and `VER-SHB-001..002` regressions, complete Python tests, formal graph validation, exact CLI help, doctor, start/review preflight, deterministic Explorer generation, candidate source and fresh wheel acceptance, consumer install/adopt/upgrade fixtures, current-root protected plan/apply fixtures, GitHub CI, and `git diff --check`.

## Evidence to record

Retain exact candidate identity; rendered workflow and parsed structure; old/new consumer workflow hashes; package/version/origin records; command-spy traces; target and unrelated-workflow pre/post manifests; conflict/no-write snapshots; event fixtures; migration plans and lock hashes; self-hosting protected hashes; test counts/runtimes; hosted CI results; documentation review; deviations; residual risks; and explicitly unperformed external actions under `docs/engineering/harness-distribution/evidence/WO-DST-016-verification.md`.

## Stop and escalate conditions

Stop if implementation requires generic YAML merge, modifies unrelated workflows, cannot make evaluator semantics package-owned, imports checkout code as authority, needs two consumer runtimes, silently falls back after identity failure, changes protected self-hosting controls through standard upgrade, weakens conflict/no-write guarantees, changes formal semantics beyond this packet, requires a new dependency/profile/provider, encounters concurrent branch changes, fails required tests, or needs authority outside an approved work order.

## Completion report format

Report the consumer workflow/job model; evaluator version/origin and package-owned command boundary; install/adopt behavior with existing and absent CI; conflict handling; upgrade/migration/idempotence results; external-enforcement disclosure; self-hosting preservation; tests and hosted CI; documentation; changed paths; evidence; deviations; residual risks; lifecycle status; and every unperformed commit, PR, release, publication, deployment, or external GitHub action.

## Completion

Implementation completed on 2026-08-17 within the approved envelope. The standard consumer distribution now installs one additive managed GitHub workflow with one exact isolated released evaluator; every harness operation in that workflow is invoked through the evaluator's `python -I -m se_harness` boundary. Init/adopt preservation, exact-path conflict, real published-0.4.0 migration, idempotence, customized blocking, package origin, adversarial event parsing, checkout-script non-authority, and protected self-hosting behavior passed the retained verification described in `../evidence/WO-DST-016-verification.md`.

`REQ-DST-056..059`, `SPEC-DST-015`, `ARCH-DST-011`, and this work order transition to `implemented`. `ADR-DST-011` and `VER-DST-015` remain approved decisions/contracts. No candidate commit, commit-bound verification record, push, pull request, release, package publication, demonstrator deployment, hosted-CI run, or external GitHub policy change was performed.
