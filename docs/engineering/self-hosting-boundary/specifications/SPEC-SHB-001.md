+++
id = "SPEC-SHB-001"
type = "specification"
title = "Three-plane self-hosting and bootstrap contract"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
specifies = ["REQ-SHB-001", "REQ-SHB-002", "REQ-SHB-003", "REQ-SHB-004", "REQ-SHB-005", "REQ-SHB-006"]
+++

# Specification: Three-plane self-hosting and bootstrap contract

## Scope

Define the identities, state ownership, process isolation, CI gates, migration, and release invalidation rules required to develop `se_harness` without making an unreleased candidate its own sole governor.

## Terminology and identities

- **Governor:** one exact released wheel selected to govern the repository during a development cycle.
- **Governor target:** the operational managed files, configuration, and lock created by the governor outside the candidate checkout.
- **Candidate source:** the reviewed checkout implementation at one commit.
- **Candidate package:** the wheel and normalized sdist built from the exact candidate commit.
- **Acceptance target:** a disposable repository outside the checkout, created for candidate-package testing.

Every execution declares exactly one role: `governor`, `candidate-source`, or `candidate-package`. Roles do not change within a process.

## State-ownership contract

The current single parity invariant is refined for the harness implementation repository:

1. Governor managed files and the governor lock match the selected released governor in an external disposable target.
2. The checkout root is candidate source. Its normal managed files match candidate canonical templates; only the repository-specific self-hosting configuration and three-plane workflow intentionally differ and remain hash-locked.
3. Candidate canonical templates match candidate-created acceptance targets and packaged template payloads.

Candidate development does not require candidate canonical templates to equal the governor target. Tests compare each plane with its declared distribution. Ordinary consumer repositories still have one standard installation and retain the existing distribution-to-target parity rule.

Repository-specific instructions and integrity tests must state this exception narrowly for the harness implementation repository. It is an execution boundary, not an install profile.

## Governor acquisition and execution

The self-hosting descriptor and CI configuration record governor version, immutable wheel URL, wheel filename, and SHA-256 independently of `pyproject.toml` candidate version. CI downloads the wheel, verifies the digest before installation, and installs it without dependencies or editable source into a fresh environment outside the checkout.

Governor execution must either use isolated Python mode or start outside the checkout. Before any substantive check, it asserts:

- `se_harness.__version__` equals the pinned governor version;
- resolved package and template paths are below the governor environment;
- neither path is below the checkout;
- candidate source is absent from effective import search paths.

The governor may initialize and doctor a disposable governor-owned repository. It may run read-only checkout checks only through its installed code and only where the compatibility contract says the old version is authoritative. It never runs same-version distribution parity against candidate-managed files.

## Candidate-source execution

Candidate-source CI asserts that package paths resolve below `GITHUB_WORKSPACE` or the explicit local checkout and that version metadata matches the candidate. It runs the full repository suite, candidate validator, doctor against candidate-owned fixtures or the declared migration state, preflight, Explorer, CLI, security, deterministic migration, and diff checks.

Candidate commands are evidence. Formal artifacts and accountable decisions remain authority.

## Candidate-package execution

Release-authorized CI exports the exact candidate, builds twice at the candidate commit epoch, normalizes source distributions, verifies eligible artifact equality, and installs the exact wheel into a fresh environment. It proves package identity and runs init, adopt/upgrade fixtures, doctor, formal validation, preflight-capable content, and Explorer only against disposable acceptance targets.

The candidate-package environment must not contain an editable install, checkout `PYTHONPATH`, or governor package. Import and entry-point paths must be below that environment.

## CI job contract

### `governor`

1. Acquire and hash-check the pinned released wheel.
2. Emit and assert governor identity.
3. Initialize a temporary repository and run governor `doctor` there.
4. Run installed-distribution bootstrap compatibility checks against the checkout without importing local candidate modules.
5. Make no checkout write.

### `candidate-source`

1. Depend on successful governor bootstrap unless an approved compatibility migration defines a distinct expected result.
2. Emit and assert checkout-source identity.
3. Select exactly one structured work order for pull requests.
4. Run review preflight, full tests, candidate formal validation, doctor, Explorer, and security/migration checks.

### `candidate-package`

1. Depend on candidate-source success.
2. Build or consume artifacts for the exact candidate.
3. Emit and assert installed-wheel identity.
4. Run acceptance only in fresh external targets and retain artifact hashes.

Candidate job names, logs, and summaries identify the assurance source. A skipped required lane is not success.

## Import-isolation contract

Tests exercise at least these deceptive cases:

- checkout is the current working directory;
- checkout is present in `PYTHONPATH`;
- another `se_harness` exists in user site-packages;
- console entry point and `python -m` resolve different installations;
- a subprocess inherits candidate import paths;
- symlink or case variation makes a path appear outside its boundary;
- version strings agree while module origin differs.

Identity checks resolve paths before comparison, use component-aware containment, and treat repository and environment values as untrusted. Diagnostics expose bounded paths and versions but never tokens or full environment content.

## Governor promotion

After immutable publication, a separate work order obtains the published wheel by retained hash, qualifies its governor target and transactional upgrade behavior, then updates the selected descriptor and CI pin. The prior governor identity remains in Git history as rollback provenance. Candidate implementation and governor promotion cannot share a commit-bound VREC merely because their version strings match.

## Candidate invalidation and current release recovery

Any implementation of this packet changes distributed CI and self-hosting behavior after candidate `9ba0cec3710167ad4568931747ed5f4e48a63532`. Closed PR #28 retains failed `VREC-SEH-003` and `RLS-SEH-003` as audit history for that candidate. The clean recovery branch excludes those governance files and requires new aggregate record IDs for a corrected tag or publication.

Before external promotion, a replacement candidate must pass this specification, receive a new aggregate VREC, and receive a new release decision. Version selection and the formal disposition vocabulary for the abandoned unpublished release are reviewed during implementation; no existing captured field is mutated.

## One-time migration

The first implementation necessarily corrects a workflow created under the mixed model. It must retain explicit before/after identity evidence, avoid claiming independent success for the broken lane, and establish a state from which future candidate cycles keep governor runtime and managed state outside the candidate checkout until post-release promotion.

## Explicitly delegated choices

Implementation may choose exact configuration key names, identity JSON schema, job names, temporary paths, and diagnostic codes. It may not merge roles, expand the two-file repository-specific parity exception, make checkout import resolution implicit, weaken exact-hash acquisition, add consumer install profiles, mutate historical records, or promote an unpublished candidate to governor.
