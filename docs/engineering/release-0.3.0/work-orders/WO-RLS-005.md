+++
id = "WO-RLS-005"
type = "work_order"
title = "Qualify the integrated se-harness 0.3.0 candidate"
status = "implemented"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]
+++

# Work Order: Qualify the integrated se-harness 0.3.0 candidate

## Lifecycle and authorization

The repository owner reviewed the proposed release-scope rule, instructed `ok go`, and then explicitly stated `i approve both` on 2026-08-15. This approves `REL-SEH-004` and this work order and authorizes the bounded candidate implementation, retained qualification evidence, candidate commit, and later preparation of `VREC-SEH-005` as `ready`. It does not authorize push, pull-request creation or merge, verification transition, release-record preparation or transition, tag, publication, deployment, or governor promotion.

After start preflight passes, the work order may move to `in_progress`. `implemented` will record completed release integration and retained evidence; it will not assert independent correctness, verification, release, publication, or governor promotion.

## Objective

Produce one clean, fully qualified 0.3.0 candidate containing the eight already-implemented release-bearing work items, consistent distribution and repository identity, reproducible release artifacts, and explicit three-plane evidence. Then prepare a later aggregate ready VREC for the exact nine-work-order release set.

## Exact aggregate scope

- Work orders: `WO-DOC-007`, `WO-DOC-008`, `WO-DOC-009`, `WO-DOC-010`, `WO-DOC-011`, `WO-DST-007`, `WO-DST-009`, `WO-RLS-005`, and `WO-SHB-002`.
- Verification contracts: `VER-DST-001`, `VER-DST-006`, `VER-DST-007`, `VER-DST-008`, and `VER-SHB-002`.
- Evidence: the eight existing work-order-keyed evidence files plus `docs/engineering/release-0.3.0/evidence/WO-RLS-005-verification.md`.
- Planned aggregate verification record: `VREC-SEH-005` under `docs/engineering/release-0.3.0/verification-records/`.
- Planned release record after verification: `RLS-SEH-005` under `docs/engineering/release-0.3.0/releases/`.
- Proposed immutable tag and public version: `v0.3.0` and `0.3.0`.

Governance-only `WO-DST-006`, `WO-DST-008`, `WO-PUB-005`, `WO-VSP-002`, and `WO-SHB-003` remain excluded. The release contract is an allow-list, not evidence that every post-tag work order is payload.

## In scope after approval

- Reconfirm the post-`v0.2.2` work-order ledger against merged history and retain the include/exclude rationale.
- Set package and public release identity to 0.3.0 in every authoritative version-bearing source, including `pyproject.toml`, `se_harness/__init__.py`, `ENGINEERING_HARNESS.md`, repository configuration, the active self-hosting candidate-version declaration, README installation guidance, current version-specific notes, and matching managed-integrity evidence.
- Keep `.self-hosting/governor.toml` and all 0.2.1 governor URL, wheel, tag, commit, release-record, and SHA-256 fields unchanged.
- Treat changes to `.engineering-harness.toml` and `.github/workflows/engineering-harness.yml` as explicitly reviewed protected-control changes; update only candidate/release identity required by 0.3.0, preserve repository policy and governor fields, and refresh the lock through the supported integrity mechanism.
- Preserve candidate distribution parity for the Explorer, managed consumer material, and self-hosting release assets.
- Run the complete verification matrix in `REL-SEH-004`, including Python 3.11 and local-runtime tests, candidate-source and package acceptance, deterministic replay, exact role identity, formal graph validation, CLI, doctor, preflight, Explorer, workflow parsing, package inspection, safe archives, reproducible builds, offline reconstruction, and fresh installation.
- Retain exact hashes, manifests, commands, exit codes, warning classifications, protected-control before/after evidence, version inventory, and external-action boundaries in `docs/engineering/release-0.3.0/evidence/WO-RLS-005-verification.md`.
- Mark this work order `implemented`, create one clean candidate commit, and only afterward prepare `VREC-SEH-005` as `ready` against that exact commit.

## Required verification

- Formal artifact validation reports zero errors; all warnings are classified.
- Start and review preflights return the complete governing manifest at their appropriate phases.
- Full Python 3.11 and local-runtime suites pass with only documented conditional skips.
- The three hosted self-hosting planes pass and prove their exact runtime, source, package, target, and checkout-mutation boundaries.
- Two candidate acceptance runs produce byte-identical canonical manifests; evidence states whether the runner is candidate-owned or independently released.
- Version, CLI, package metadata, repository configuration, active workflow candidate version, README pin, wheel metadata, sdist metadata, and fresh-install identity all equal 0.3.0.
- Doctor, managed distribution parity, protected-control checks, workflow parsing, lock integrity, and deterministic Explorer generation pass.
- Two wheel and raw-sdist builds at one explicit candidate epoch yield byte-identical wheels and normalized sdists. Archive payloads are safe and equivalent, wheel RECORD metadata is valid, and an offline rebuild from the normalized sdist installs and operates under Python 3.11.
- Historical VREC metadata and relations remain unchanged. The new aggregate VREC contains exactly the selected work, complete verification-contract union, keyed evidence, one artifact snapshot, and one candidate commit.
- `git diff --check`, candidate ancestry, changed-path inventory, and bounded diff review pass.

## Evidence and completion

Retain the baseline tag and commit, merged PR/work-order ledger, exact release scope and exclusions, pre/post version inventory, governor and candidate identities, protected-control and lock hashes, all local and hosted results, deterministic manifests and snapshots, build epochs and hashes, archive member checks, fresh-install outputs, deviations, residual risks, and explicitly unperformed external actions.

The final implementation report must identify the candidate commit separately from its later VREC governance commit. The candidate cannot contain a truthful record naming its own not-yet-created commit ID.

Implementation and preliminary qualification completed on 2026-08-15. Retained results are in `docs/engineering/release-0.3.0/evidence/WO-RLS-005-verification.md`. Exact-commit replay remains a post-commit prerequisite to preparing `VREC-SEH-005`; it is not a verification decision.

## Out of scope

Changing the selected governor from 0.2.1; invoking root `reconcile-governor`; activating 0.3.0 as governor; using candidate code as retroactive independent authority; editing or superseding historical VRECs; transitioning `VREC-SEH-005`; preparing or transitioning `RLS-SEH-005`; creating or moving `v0.3.0`; GitHub Release or PyPI publication; deployment; merge; force push; history rewriting; or changing an already-published artifact.

## Stop conditions

Stop on a changed proposed scope, missing evidence, incomplete contract union, version-bearing source not governed by this work, protected-policy loss, governor-field change, root reconciliation requirement, cross-role import, candidate/governor authority confusion, failed required check, unclassified warning, package mismatch, unsafe archive, nondeterministic output, mutable external dependency, candidate change after evidence, or need for authority beyond an approved work order.

## Completion report format

Report the final nine-work-order scope, exclusions, version inventory, exact candidate commit and tree, governor identity, protected-control changes and hashes, source/package role identities, verification counts, replay and Explorer hashes, wheel/sdist/checksum hashes, reproducibility and offline-install results, warnings and residual risks, evidence path, work-order status, planned VREC command inputs, and explicitly unperformed verification transition, release record, tag, publication, deployment, and governor promotion.
