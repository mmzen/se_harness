+++
id = "ARCH-REB-001"
type = "architecture"
title = "Standard lock-bound released-evaluator boundary"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-27"

[relations]
addresses = ["REQ-REB-001", "REQ-REB-002", "REQ-REB-003", "REQ-REB-004"]
conforms_to = ["SPEC-REB-001", "SPEC-REB-002"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "data-ownership-or-persistence", "security-privacy-or-trust-boundary", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The approved design moves evaluator identity into the standard lock, changes public mutation preconditions and upgrade migration, reverses active workflow dependencies on a retired descriptor, and establishes a cross-cutting trust boundary across CLI, CI, provenance, and release behavior. These controlled triggers and the materially different descriptor, workflow-only, and standard-lock options require the accepted ADR-REB-001."
assessed_by = "technical-owner"
+++

# Architecture: Standard lock-bound released-evaluator boundary

## Context and scope

The root is an ordinary standard governed repository, but proof of the independently released evaluator is currently procedural and split across runtime identity commands, managed CI, repository-specific publication code, and retained prose. This architecture makes the standard installation the single identity source and directs every active root mutation and publication check through a shared released-evaluator boundary.

The architecture covers standard lock identity, runtime enforcement, publication resolution, readiness evidence, and separate evaluator-upgrade sequencing. Conflict observations and the recovery runbook consume these boundaries but do not own evaluator identity.

## Components and responsibilities

- **Standard configuration and lock:** own selected tool version, managed-file integrity, canonical installed payload identity, and optional exact archive identity. The `se_harness` root requires archive identity.
- **Runtime identity inspector:** computes bounded origins, payload/archive agreement, isolation state, and checkout exclusion without reading target product code.
- **Mutation guard:** converts a passing locked identity into an in-process precondition immediately before an installed-root write; it grants no lifecycle authority.
- **Installer and upgrade transaction:** establish or migrate standard identity and preserve old-root integrity and rollback semantics.
- **Repository publication resolver:** reads the standard snapshot identity, acquires exact public bytes, and proves an external released-evaluator environment before validation or promotion.
- **Provenance preparation and validator:** bind canonical identity evidence to ready release records and recheck it without transitioning state.
- **Active-surface policy tests:** prevent executable or packaged reintroduction of the retired special lifecycle.
- **Inspection and recovery support:** report structural ambiguity and rehearse restoration using the same standard components.

## Dependency direction

```text
approved standard identity -> immutable wheel acquisition -> external installed evaluator
        |                                      |
        +-> mutation guard <-------------------+
        +-> publication resolver <-------------+
        +-> readiness evidence <---------------+

candidate source/package -> tests and candidate evidence only
human owners -> approval, verification, release, publication, and recovery decisions
```

The evaluator never derives its expected identity from candidate source, a candidate-built descriptor, mutable workflow input, or the target repository's import path.

## Data and control flow

1. A trusted standard installation records evaluator payload identity; an explicitly verified archive additionally records exact wheel identity.
2. A lifecycle operation resolves the target and classifies itself as read-only, ordinary mutation, or upgrade apply.
3. The identity inspector compares the current environment to the standard lock and target boundary.
4. A mutator proceeds only after a pass and still uses its existing atomic or exclusive write mechanism.
5. Publication independently acquires the locked public wheel, validates its digest, installs externally, and repeats identity proof before reading governance as evidence.
6. Release preparation canonicalizes and binds identity evidence; publication rechecks the binding.
7. Candidate lanes exercise positive and negative paths and prove that the checkout remains unchanged when no work order authorizes mutation.

## Trust boundaries

- Repository content, config, lock, formal artifacts, workflows, distribution metadata, archive filenames, downloaded bytes, paths, environment state, and CLI input are untrusted.
- The independently selected expected archive digest plus verified acquired bytes establishes distribution identity for publication-enabled roots.
- Installed payload verification and common-environment origins establish runtime correspondence.
- GitHub protected environments and OIDC bound external publication but never create lifecycle authority.
- Accountable humans remain outside the automation trust boundary and make approval, assurance, release, and emergency decisions.

## Required patterns

- One standard lock schema and transaction; no parallel evaluator descriptor.
- One shared fail-closed identity implementation reused by runtime reporting and mutation enforcement.
- Internal guard placement at every public mutator, with zero-write boundary tests.
- Exact archive download and digest verification before installation in publication paths.
- Normalized, canonical, digest-bound retained evidence.
- Closed allowlists for historical fixtures and closed catalogs for conflict observations.
- Separate work orders for product release and later evaluator adoption.

## Prohibited patterns

- Candidate source or a locally built candidate wheel acting as the root evaluator.
- Runtime qualification from version string, role argument, or caller-provided digest alone.
- Active `.self-hosting/governor.toml`, special self-hosting workflow/profile, `reconcile-governor`, `--role governor`, or duplicate promotion channel.
- CLI-only guards that library mutation entry points can bypass.
- Absolute host paths or environment dumps in permanent formal records.
- Automated conflict disposition, VREC verification, RLS release, publication, deployment, or recovery authorization.
- One circular work order that builds, publishes, and adopts the same candidate as evaluator.

## Quality attributes

- **Security:** exact distribution and checkout exclusion prevent candidate authority substitution.
- **Atomicity:** identity failure precedes writes and upgrade migration reuses recoverable transactions.
- **Auditability:** one standard identity and one canonical evidence binding make the evaluator reviewable.
- **Portability:** normalized evidence and standard installation semantics work across supported platforms.
- **Compatibility:** legacy locks retain read-only and bounded upgrade paths without reintroducing a profile.
- **Operability:** stage-specific diagnostics and a rehearsed runbook reduce recovery improvisation.

## Conformance checks

- Validate schema-3 lock identity, canonical payload hashing, archive-pair rules, duplicate keys, and migration.
- Exercise every mutator through official, wrong-version, wrong-digest, editable, source, candidate-wheel, path, symlink, user-site, and `PYTHONPATH` cases with zero-write snapshots.
- Execute repository publication resolver against a disposable standard governance snapshot and the real current CLI parser.
- Scan active package/workflow/script surfaces for retired contracts while preserving historical fixtures.
- Prepare and validate a ready RLS with canonical identity evidence and reject modified or host-leaking evidence.
- Run separate-upgrade, conflicting-chain, and recovery-rehearsal scenarios from `VER-REB-001`.

## Related ADRs

`ADR-REB-001` records the accepted decision to own evaluator identity in the standard lock and consume it through shared runtime, publication, and provenance boundaries instead of restoring a special descriptor or relying on workflow-only procedure.

## Amendment, 2026-08-27

Under `WO-REB-027`, `REQ-REB-005` left this architecture's `addresses` set when it was superseded by `REQ-REB-027` and `REQ-REB-028`, which `ARCH-REB-011` addresses. The boundary this architecture describes is unchanged.
