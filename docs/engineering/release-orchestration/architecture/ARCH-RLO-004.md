+++
id = "ARCH-RLO-004"
type = "architecture"
title = "Recipe-bound hermetic release producer"
status = "approved"
owners = ["engineering-owner", "security-owner", "release-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
addresses = ["REQ-RLO-013", "REQ-RLO-014"]
conforms_to = ["SPEC-RLO-004"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "responsibility-or-dependency-direction", "public-interface-or-protocol", "security-privacy-or-trust-boundary", "deployment-or-operating-model", "concurrency-consistency-reliability-or-failure-strategy", "technology-framework-vendor-or-external-service", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The change establishes a versioned repository protocol, moves accepted build identity from workflow text into release provenance, selects an immutable external producer, constrains candidate execution, and defines forward and historical replay paths; the material alternatives and trust boundaries require an ADR."
assessed_by = "engineering-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T12:01:04Z"
decided_by = "engineering-owner"
+++

# Architecture: Recipe-bound hermetic release producer

## Context and scope

The current release path has two incomplete sources of build truth. The RLS owns the candidate, epoch, source, filenames, and output hashes, while `publish-pypi.yml` owns the Windows runner label, Python patch, direct tool versions, environment setup, build command, and normalization invocation. Neither source contains the complete effective producer. The workflow can drift without changing the release provenance it is meant to replay.

This architecture makes one candidate-tree recipe the build-mechanics source of truth, binds its exact bytes in the repository-owned RLS distribution extension, and uses one strict interpreter in local creation, hosted pre-release replay, and production qualification. Portable release governance remains unaware of the repository format.

## Components and responsibilities

- **Canonical recipe:** `release/build-recipe.json` declares the immutable producer, exact runtime, complete toolchain reference, closed environment, typed commands, normalizer, and outputs.
- **Toolchain lock:** `release/build-toolchain.lock` enumerates every direct and transitive Python build distribution with exact versions and acceptable file hashes.
- **Recipe parser and planner:** trusted repository-owned Python validates canonical bytes, safe paths, closed fields, bounded tokens, schema, and candidate-tree identity without executing candidate content.
- **Hermetic producer adapter:** launches the digest-pinned Linux/amd64 OCI image twice, establishes only the declared environment and toolchain, executes validated argument arrays, and observes the runtime and installed inventory.
- **Bundle and RLS binder:** extends repository bundle and distribution schemas with the recipe path, schema, and digest, while preserving generic RLS core fields and atomic binding.
- **Hosted pre-release replay:** selects one ready RLS and runs the producer twice with read-only permissions and no credentials, then retains exact comparison evidence.
- **Production qualifier:** resolves a released RLS from trusted main and delegates schema-2 reconstruction to the same producer adapter before any privileged stage.
- **Legacy adapter:** preserves the existing schema-1 publication reconstruction only for already released history and labels its weaker identity explicitly.

## Dependency direction

The candidate tree owns recipe and lock data. Repository policy parses and executes that data. The ready RLS binds exact candidate, recipe, and output identities. Hosted and production workflows call repository policy and do not restate schema-2 build mechanics.

Portable `se_harness` prepares and validates only format-neutral RLS core governance. It does not import repository recipe code, know OCI or Python package policy, or distribute the recipe to consumers. Privileged publication stages depend on the inert, hash-checked output bundle and never on the recipe interpreter or candidate execution.

## Data and control flow

1. The exact candidate contains canonical recipe and lock bytes.
2. Repository tooling validates the recipe, exports the candidate twice, and runs two fresh producer instances.
3. The producer result proves declared and observed platform, Python, toolchain, environment, commands, normalization, and output hashes.
4. Accepted bytes and recipe identity enter bundle schema 2.
5. The binder matches bundle, candidate, recipe, and ready RLS, then atomically writes distribution schema 2.
6. A hosted no-credential lane resolves that ready RLS and independently reproduces the exact accepted bytes.
7. After a separate release decision, trusted main resolves the released record and the production qualifier repeats the same recipe replay.
8. Only the resulting independently checked inert bytes cross into GitHub, PyPI, or Pages permission boundaries.

No downstream job or operator can replace recipe fields or expected hashes.

## Trust boundaries

- **Governance boundary:** a recipe and replay result are technical evidence; only formal lifecycle commands and accountable actors can approve work, verification, or release.
- **Parsing boundary:** RLS, JSON, lock, paths, tokens, and image metadata are untrusted and validated before any candidate execution.
- **Producer boundary:** candidate code, build backends, and normalizer run only inside a no-credential immutable producer.
- **Supply boundary:** the producer image is content-addressed and the complete Python toolchain is hash-locked and inventory-checked.
- **Host boundary:** host environment, user configuration, credentials, caches, absolute paths, and runner-selected Python do not enter accepted build identity.
- **Publication boundary:** write and OIDC jobs receive verified inert bytes only and do not launch the producer.
- **Compatibility boundary:** schema-1 history remains immutable behind an isolated legacy adapter; it cannot be selected for a new ready record.

## Required patterns

- One canonical JSON recipe and one complete hash-locked toolchain inventory.
- Exact candidate-tree recipe path plus raw-byte SHA-256 in bundle and RLS.
- Immutable platform-specific OCI image digest and observed identity comparison.
- Closed environment and typed argument arrays interpreted without a shell.
- Two independent exports, producers, tool environments, and output directories.
- One repository implementation shared by creation, binding, validation, pre-release replay, and production qualification.
- Schema-aware forward policy with historical read/replay compatibility.
- Bounded result evidence that distinguishes declared, observed, expected, and actual identities.

## Prohibited patterns

- Floating runner, image, Python, or dependency versions in accepted identity.
- Direct-only tool pins that omit transitive build packages.
- Inheriting the host environment, user site, build cache, credentials, or configuration.
- Free-form shell text, workflow-duplicated schema-2 commands, or an update-expected replay option.
- Reusing source, environment, cache, or output state between the two builds.
- Falling back from the declared producer to the host runner.
- Putting repository build policy in portable `harnessctl`, managed consumer files, or the built wheel.
- Rewriting historical RLS records or describing schema-1 evidence as recipe-bound.

## Quality attributes

Reproducibility, exact provenance, fail-closed behavior, least privilege, auditability, historical compatibility, and one-source maintainability take precedence over fastest builds, shortest workflow YAML, or minimizing public immutable downloads.

## Conformance checks

- Schema and property tests exercise every required field, duplicate/extra field, size, type, path, digest, token, environment, command, and normalization boundary.
- Toolchain tests prove direct and transitive completeness, hash-required installation, observed-inventory equality, and extra-package refusal.
- Adapter tests use injected process/container fixtures for argument boundaries, environment closure, cleanup, timeouts, bounded output, two-instance separation, and no-write failure.
- Real local and hosted tests build twice and compare exact wheel and normalized-sdist bytes with accepted hashes.
- Workflow tests prove one RLS input, ready-state pre-release selection, read-only/no-OIDC permissions, no secrets or protected environment, shared interpreter use, and no duplicated schema-2 build commands.
- Package and disposable-consumer tests prove recipe policy remains outside portable distributions and managed installations.
- Historical tests replay `RLS-SEH-012` through the labeled schema-1 path without modifying it.

## Related ADRs

`ADR-RLO-004` selects a candidate-tree declarative recipe executed by a strict repository interpreter inside a digest-pinned OCI producer, with recipe-bearing schema 2 for new records and isolated schema-1 historical compatibility.
