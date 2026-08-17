+++
id = "SPEC-DST-015"
type = "specification"
title = "Additive single-runtime consumer GitHub CI"
status = "implemented"
owners = ["technical-owner", "security-owner", "quality-owner", "product-owner"]
created = "2026-08-17"
updated = "2026-08-17"

[relations]
specifies = ["REQ-DST-056", "REQ-DST-057", "REQ-DST-058", "REQ-DST-059"]
+++

# Specification: Additive single-runtime consumer GitHub CI

## Scope

Simplify the one standard consumer installation so GitHub runs one dedicated managed workflow using one exact released SE Harness evaluator. Preserve the distinct protected self-hosting governor/candidate architecture used only while developing SE Harness.

## Actors and external systems

- A repository operator installs or upgrades the released package and reviews repository changes.
- GitHub Actions discovers independent workflows and executes push and pull-request jobs.
- PyPI supplies the exact binary-only released evaluator selected by the managed workflow.
- GitHub repository owners separately configure rulesets, branch protection, required checks, and deployment ordering.

## Inputs

- the installed distribution version and canonical standard template;
- target repository files, configuration, and schema-2 managed lock;
- GitHub event payload and checkout revision;
- repository artifacts and retained evidence treated as untrusted data.

## Outputs

- one dedicated `.github/workflows/engineering-harness.yml` managed by the standard distribution;
- one isolated evaluator identity per CI run;
- bounded work-order-selection, preflight, doctor, validation, and Explorer results;
- an optional uploaded derived dashboard artifact;
- an explicit reminder that GitHub enforcement remains external configuration.

## State model

The workflow installation state is `absent`, `managed-current`, `managed-upgradable`, or `conflicting/customized`. Init/adopt may move `absent` to `managed-current`; standard apply may move `managed-upgradable` to `managed-current`; conflict/customization is terminal for that transaction and requires owner resolution.

A CI run progresses `checkout -> evaluator-install -> evaluator-identity -> work-selection when PR -> assessment -> derived-output`. Failure stops dependent steps except explicitly configured diagnostic or artifact-retention steps and never creates governance authority.

## Behavioral rules

1. Init and adopt plan the same dedicated consumer workflow whether zero, one, or many unrelated workflows already exist.
2. The installer never parses, merges, renames, or edits unrelated workflow files.
3. An unknown or customized exact destination blocks the complete installation or upgrade transaction.
4. The workflow declares `pull_request` and `push`, stable read-only permissions, and one primary `validate` job whose check name is suitable for owner-configured branch protection.
5. The workflow renders one `SE_HARNESS_VERSION` equal to the distribution's `HARNESS_VERSION`; it contains no independent consumer bootstrap/governor version.
6. The job creates a runner-temporary virtual environment, installs `se-harness==$SE_HARNESS_VERSION` with binary-only and no-dependency constraints, and uses absolute environment-owned command paths.
7. Identity checks prove exact version and package origin outside the checkout before assessment.
8. Pull-request work-order extraction is package-owned, accepts exactly one standalone structured declaration, and preserves current bounded rejection behavior.
9. Review preflight, doctor, graph validation, and Explorer generation execute through package-owned entry points, not checkout scripts.
10. Application tests, builds, deployments, releases, and their dependency ordering remain repository-owned workflows or jobs.
11. Installation and `doctor` explain that workflow discovery is automatic but required-check enforcement is not configured by SE Harness.
12. Standard upgrade remains plan-first and atomically updates only safe managed content plus lock evidence; no consumer calls `reconcile-governor`.
13. A package-only update and an uncommitted repository update do not change hosted CI.
14. The exact `se_harness` implementation repository remains fail-closed self-hosting and continues to protect its root configuration and workflow from ordinary upgrade.
15. Commands and CI outputs remain observations or evidence and never approve work, verification, release, publication, deployment, or external enforcement.

## Error and recovery behavior

Unsafe paths, workflow conflicts, managed drift, malformed events, missing or ambiguous work-order IDs, evaluator install/origin/version failures, graph errors, and derived-output failures retain existing bounded diagnostics and nonzero status. Installer and upgrade failures write nothing. A failed CI run is retried by GitHub or after a new commit; it never falls back to a global, checkout, bootstrap, or candidate runtime.

## Data and interface contracts

- Public operator commands remain `init`, `adopt`, `upgrade`, and `doctor`; no separate `ci install`, `ci upgrade`, or consumer reconciliation command is added.
- A narrow package-owned CI interface may be added for GitHub event work-order selection, but it remains agent/automation-facing and validates the same standalone field contract.
- The canonical workflow contains the rendered exact evaluator version and remains tracked as `managed` in `.engineering-harness.lock`.
- Existing target-local portable scripts remain managed distribution content until separately removed, but consumer CI does not execute them as its oracle.

## Security and privacy properties

Repository content, events, paths, configuration, Markdown, and managed-script copies are untrusted. The evaluator environment is outside the checkout, uses no repository executable import, requests only `contents: read`, exposes no secrets, and performs no external mutation. Exact-version PyPI acquisition is the accepted KISS trust dependency; repository-pinned wheel digests, attestations, and alternate indexes are outside this packet.

## Performance and capacity

Removing the self-only bootstrap job eliminates one checkout, Python setup, virtual environment, package download, init, and doctor cycle per run. No fixed timing target is authoritative because GitHub runner and package-index latency are external.

## Observability

CI logs the declared and resolved evaluator version and safe module origin, selected work-order ID, command status, and derived dashboard upload outcome without logging repository bodies or secrets. Installation and upgrade plans show the workflow disposition and evaluator-version change.

## Compatibility and migration

An unmodified standard consumer workflow from 0.4.0 migrates through ordinary `harnessctl upgrade --apply` when this change is released. The managed two-job consumer workflow is replaced by the single-job template and its lock entry is refreshed in the same transaction. Customized workflow content blocks migration without partial writes. The protected self-hosting root workflow is neither substituted nor reconciled by this path.

## Examples and counterexamples

- Creating the dedicated workflow beside `build.yml` is conforming; inserting generated steps into `build.yml` is not.
- One exact released evaluator running package-owned checks is conforming; a 0.2.1 bootstrap followed by an independently installed newer consumer evaluator is not.
- GitHub running both workflows after a pull request is conforming; claiming installation made the harness check required is not.
- An ordinary consumer running standard upgrade is conforming; a consumer invoking `reconcile-governor` is not.

## Explicitly unspecified decisions

The implementation agent may choose stable internal module names, the narrow package-owned work-selection command name, step labels, and whether non-gating inspection is also emitted, provided the one-runtime, package-owned, additive, managed, and authority boundaries remain exact. Changes to artifact attestation, GitHub ruleset automation, non-GitHub providers, application-test orchestration, or self-hosting governance require separate decisions.
