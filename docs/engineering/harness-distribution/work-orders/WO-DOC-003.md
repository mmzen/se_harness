+++
id = "WO-DOC-003"
type = "work_order"
title = "Make public onboarding PyPI-first and package metadata complete"
status = "implemented"
owners = ["engineering-owner", "documentation-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-DST-009", "REQ-DST-010", "REQ-DST-011", "REQ-DST-012", "REQ-DST-013"]
specifications = ["SPEC-DST-003"]
architecture = ["ARCH-DST-003", "ADR-DST-003"]
verification = ["VER-DST-003"]
+++

# Work Order: Make public onboarding PyPI-first and package metadata complete

## Lifecycle and authorization

The repository owner authorized creation of this artifact packet on 2026-08-11 with the instruction `ok go for the artifact packet`, then reviewed the packet and explicitly approved its governing chain and bounded implementation with `ok go for implementation`. This places the work order `in_progress`. Commit, verification capture, lifecycle transition beyond implementation, push, pull request, release selection, build, tag, and publication remain separately controlled.

## Objective

Make the root README an accurate, efficient entry point for installing the released harness from PyPI and adopting or initializing a repository, while publishing that same README, the license, and canonical project links through static package metadata and preserving the implemented governance and authority model.

## In scope after approval

- Reorder and edit the root README according to `SPEC-DST-003` without removing accurate detailed governance guidance.
- Make production PyPI installation in an explicit virtual environment the primary path.
- Document Windows and POSIX activation, environment-local launcher paths, exact-version installation, and module invocation.
- Add a concise initialization/adoption quick start.
- Explain the package-update versus target-repository-upgrade boundary.
- Surface implemented instruction routing, work-order lifecycle, aggregate provenance, verification supersession, deterministic release, and OIDC publication capabilities concisely.
- Replace version-specific conceptual CI baseline prose with configuration-neutral language while retaining the bootstrap boundary.
- Add static README, license, and project URL metadata to `pyproject.toml` without changing version, runtime dependencies, or console entry point.
- Add deterministic focused tests and retain work-order-keyed evidence.

## Out of scope

- Changing CLI behavior, installed templates, managed files, lock data, runtime dependencies, Python support, initialization, adoption, preflight, provenance, supersession, release, or publisher logic.
- Updating the independent CI baseline pin or either GitHub workflow.
- Bumping the package version or build-system dependency floor.
- Building wheel or source distributions, changing existing release records, creating a VREC/RLS, committing, pushing, opening a pull request, tagging, creating or editing a GitHub release, publishing to PyPI, or mutating external configuration.
- Changing or disposing `REL-PYP-001`; its low-severity lifecycle hygiene is separate.
- Claiming that existing PyPI 0.2.1 metadata can be changed.

## Authorized decision envelope after approval

Implementation may choose concise wording, badge use, heading names, retained-section placement, and focused test organization. It may not weaken authority boundaries, hide virtual-environment ownership, make source installation primary, duplicate the README, add dynamic or network-derived metadata, alter the configured baseline, remove detailed lifecycle/provenance behavior, or report deferred release checks as complete.

## Expected change surface

- `README.md`;
- static `[project]` metadata in `pyproject.toml`;
- one focused standard-library test module;
- this distribution-domain packet index and acceptance scenarios if clarification is needed;
- `docs/engineering/harness-distribution/evidence/WO-DOC-003-verification.md` after implementation.

Canonical installed templates and self-hosting lock files are expected to remain unchanged because the root distribution README and project metadata are not installed target content.

## Implementation sequence after approval

1. Run start preflight and read the complete manifest.
2. Add deterministic failing tests for the approved public documentation and metadata contract.
3. Rewrite the README onboarding path while retaining accurate deep reference material.
4. Add the static package metadata fields without a version or build-system change.
5. Run `VER-DST-003`, inspect the diff, and retain exact evidence.
6. Stop for separate commit and verification-capture authority.

## Required verification

Perform every locally authorized check in `VER-DST-003`; run the complete unit suite, validator, doctor, CLI help, start/review preflight, and dashboard; inspect README structure and metadata; confirm no installed template, lock, workflow, historical artifact, version, or external state changed. Do not build a distribution under this work order.

## Evidence to record

Retain exact commands and outputs, runtime versions, test counts, parsed metadata, version synchronization, README section and link inspection, graph counts, doctor/preflight/dashboard results, changed paths, deferred next-release checks, deviations, and residual risks in `docs/engineering/harness-distribution/evidence/WO-DOC-003-verification.md`.

## Stop and escalate conditions

Stop if implementation requires a version bump, release build, network dependency, runtime dependency, build-backend floor change, workflow or baseline-pin edit, template/lock mutation, removal of materially accurate governance behavior, ambiguous license claim, failed test, external publication, or authority outside this approved chain.

## Completion report format

Report the onboarding outcome, metadata fields, synchronization checks, test and harness results, unchanged protected surfaces, deferred release verification, deviations, residual risks, and the exact evidence path. Do not describe the work as verified, released, or published without later accountable records.

## Implementation result

The root README now makes released PyPI installation and environment-local launcher discovery the primary onboarding path, provides a concise new/existing-repository quick start, distinguishes package and repository upgrades, surfaces the implemented governance and publication controls, and keeps baseline language configuration-neutral. Static project metadata selects the README and license and exposes canonical URLs. Eight focused tests, both supported-runtime suites, and the harness checks pass; exact evidence and deferred release inspection are retained in `docs/engineering/harness-distribution/evidence/WO-DOC-003-verification.md`.
