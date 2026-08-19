+++
id = "ARCH-RLO-002"
type = "architecture"
title = "Portable governance and repository publication boundary"
status = "approved"
owners = ["engineering-owner", "security-owner", "release-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[relations]
addresses = ["REQ-RLO-009", "REQ-RLO-010", "REQ-RLO-011"]
conforms_to = ["SPEC-RLO-002"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "responsibility-or-dependency-direction", "public-interface-or-protocol", "security-privacy-or-trust-boundary", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The correction removes a public CLI and packaged module, reverses a dependency between portable governance and repository policy, relocates trusted release validation, and must preserve credential and immutable-state boundaries; these controlled choices require an ADR."
assessed_by = "engineering-owner"
+++

# Architecture: Portable governance and repository publication boundary

## Context and scope

RLO-001 correctly made the production workflow repository-specific but placed its Python bundle validation in the packaged harness and managed consumer files. That reversed the intended dependency: all repositories inherited policy needed only to publish SE Harness. This architecture restores a one-way boundary while retaining the exact release transaction.

The scope covers portable CLI/module/template/validator behavior, repository distribution preparation and validation, and the import boundary of the trusted-main release workflow. It does not redesign GitHub, PyPI, Pages, RLS lifecycle, or external publisher configuration.

## Components and responsibilities

- **Portable release governance:** prepares ready RLS core metadata and validates formal identities, relations, lifecycle, and exact candidate coverage.
- **Repository distribution library:** defines the SE Harness bundle and distribution-table schemas and is excluded from the packaged namespace and consumer template.
- **Repository binder:** matches one bundle to one ready RLS and atomically adds only repository distribution metadata.
- **Repository policy validator:** checks distribution-bearing SE Harness records in local and hosted verification, separately from core graph validation.
- **Trusted-main resolver:** consumes the released RLS and repository library before untrusted candidate execution or credential-bearing jobs.
- **Existing release jobs:** qualify, publish, deploy, and observe without changed permissions or authority.

## Dependency direction

Repository scripts may invoke portable `harnessctl` and interpret repository extensions. Portable `se_harness` code and managed consumer files must not import, copy, name, or validate repository distribution and channel policy. The workflow imports trusted repository tooling from the main governance snapshot, never distribution logic from the candidate package.

## Data and control flow

1. Generic preparation derives the RLS core from eligible VRECs and work.
2. Repository build tooling creates the exact bundle manifest from candidate bytes.
3. The binder independently reads both and performs an atomic extension write.
4. Accountable review and lifecycle transitions occur later under existing governance.
5. The main-only workflow resolves the released record and revalidates the repository extension.
6. Existing credential-free qualification and inert-byte transfer feed the separated publication jobs.

## Trust boundaries

- **Portable boundary:** installed harness and consumer templates contain only repository-independent policy.
- **Definition boundary:** the repository distribution table is local policy and is not core-assessed merely because it is embedded in an RLS.
- **Binding boundary:** untrusted manifest and RLS bytes are checked before an atomic local write; lifecycle fields remain immutable to the binder.
- **Execution boundary:** candidate code remains confined to no-credential qualification.
- **Publication boundary:** GitHub, PyPI, and Pages jobs consume trusted-main plans and checked inert bytes exactly as in `ARCH-RLO-001`.

## Required patterns

- One repository-owned implementation shared by manifest generation, binding, validation, workflow resolution, and tests.
- Explicit separate commands for generic RLS preparation and repository distribution binding.
- Safe bounded parsing and atomic replacement.
- A distinct repository CI gate for repository metadata no longer assessed by the core validator.
- Negative consumer-install and wheel-content tests.
- Preservation of the one-input release workflow and stage-specific results.

## Prohibited patterns

- A generic plugin framework or new installation profile.
- Python package filenames, PyPI, Pages, or checksum-layout rules in portable runtime or managed consumer files.
- Importing candidate `se_harness` code in trusted resolution or privileged jobs.
- Treating an opaque repository extension as core verification.
- Weakening exact hash, replay, protected-environment, action-pin, or immutable-state checks.
- Rewriting RLO-001 artifacts, VREC-RLO-001, or historical release records.

## Quality attributes

Policy independence, explicit ownership, deterministic provenance, least privilege, safe upgrade, auditability, and operational simplicity take precedence over preserving an unreleased convenience flag.

## Conformance checks

- Inspect built wheel contents and installed CLI help for the absence of distribution-specific product surfaces.
- Install or upgrade a disposable consumer and inspect its validator and release template for repository policy leakage.
- Exercise exact, malformed, mismatched, replay, and atomic-failure binder cases.
- Validate the repository extension through a separate local and CI command.
- Statistically assert the workflow input, import source, permissions, environments, action pins, checkout placement, and external-state rules.
- Run the existing deterministic release-orchestration suite to prove behavior parity.

## Related ADRs

`ADR-RLO-002` selects direct relocation to repository-owned tooling rather than retaining the leak or designing a general release-extension framework.
