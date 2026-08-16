+++
id = "WO-RLS-006"
type = "work_order"
title = "Qualify the integrated se-harness 0.4.0 candidate"
status = "implemented"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[assurance]
commit_bound_verification = "required"
rationale = "Release, package, installation, and future governor decisions will rely on the exact versioned candidate, protected controls, integrated behavior, retained evidence, and reproducible distributions."
decided_by = "repository-owner"

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]
+++

# Work Order: Qualify the integrated se-harness 0.4.0 candidate

## Lifecycle and authorization

On 2026-08-16, after reviewing the complete release packet, the repository owner stated `i approve`. That decision approves `REL-SEH-005`, this work order, and its explicit commit-bound assurance classification. It authorizes the bounded candidate implementation, retained qualification evidence, candidate commit, and later preparation of `VREC-SEH-006` as `ready`. It does not authorize push, pull-request creation or merge, the VREC's verification transition, release-record preparation or transition, tag, publication, deployment, or governor promotion.

Start preflight passed with this work order in `approved`, so bounded release implementation is now `in_progress`.

## Objective

Produce one clean, fully qualified 0.4.0 candidate containing the nine already implemented release-bearing work items, consistent distribution and repository identity, reproducible release artifacts, and explicit three-plane evidence. Then prepare a later aggregate ready VREC for the exact ten-work-order release set.

## Exact aggregate scope

- Work orders: `WO-DOC-012`, `WO-IAR-006`, `WO-IAR-007`, `WO-IAR-008`, `WO-IAR-009`, `WO-IAR-010`, `WO-OCA-001`, `WO-OCA-002`, `WO-RLS-006`, and `WO-WAC-001`.
- Verification contracts: `VER-DST-001`, `VER-DST-009`, `VER-IAR-006`, `VER-IAR-007`, `VER-IAR-008`, `VER-IAR-009`, `VER-IAR-010`, `VER-OCA-001`, `VER-OCA-002`, and `VER-WAC-001`.
- Evidence: the nine existing work-order-keyed evidence files plus `docs/engineering/release-0.4.0/evidence/WO-RLS-006-verification.md`.
- Planned aggregate verification record: `VREC-SEH-006` under `docs/engineering/release-0.4.0/verification-records/`.
- Planned release record after verification: `RLS-SEH-006` under `docs/engineering/release-0.4.0/releases/`.
- Proposed immutable tag and public version: `v0.4.0` and `0.4.0`.

Repository-specific governor promotion/assurance (`WO-SHB-004`, `WO-SHB-005`), stale-record supersession/publication (`WO-VSP-003`, `WO-VSP-004`, `WO-VSP-005`), release-proposal disposition (`WO-RCD-001`), and architecture reassessment (`WO-DST-010`) are deliberately excluded as governance maintenance. The release contract is an allow-list, not evidence that every post-tag work order is payload.

## In scope after approval

- Reconfirm the post-`v0.3.0` work-order ledger against merged history and retain the exact include/exclude rationale.
- Set candidate package and public release identity to 0.4.0 in every authoritative version-bearing source and derived managed output required by current repository policy.
- Keep `.self-hosting/governor.toml` and all released 0.3.0 governor URL, wheel, tag, commit, release-record, and SHA-256 fields unchanged.
- Update the active self-hosting workflow only where it identifies the candidate version; preserve its immutable 0.3.0 governor inputs, permissions, three-plane separation, and pinned reusable-workflow identity.
- Treat `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, `ENGINEERING_HARNESS.md`, and `.engineering-harness.lock` as explicitly reviewed protected controls. Resolve candidate-distribution parity through the supported self-hosting boundary without presenting candidate code as its own governor.
- Align package metadata, `se_harness.__version__`, README installation guidance, templates, package-data expectations, version-specific tests, and public command identity with 0.4.0.
- Preserve the implemented validation, inspection, suggestion, temporal-finding, operating-assurance, and work-order-assurance contracts exactly as approved by their source work orders.
- Run the complete verification matrix in `REL-SEH-005`, including Python 3.11 and local-runtime tests, released-governor checks, candidate-source and candidate-package acceptance, deterministic replay, formal graph validation, CLI, doctor, preflight, validation, inspection, Explorer generation, workflow parsing, package inspection, safe archives, reproducible builds, offline reconstruction, and fresh installation.
- Retain exact hashes, manifests, commands, exit codes, warning/observation classifications, protected-control before/after evidence, version inventory, and external-action boundaries in `docs/engineering/release-0.4.0/evidence/WO-RLS-006-verification.md`.
- Mark this work order `implemented`, create one clean candidate commit, and only afterward prepare `VREC-SEH-006` as `ready` against that exact commit.

## Out of scope

Changing or promoting the selected 0.3.0 governor; adding new harness behavior; expanding the release allow-list without accountable review; bulk-classifying historical work orders; changing validation or inspection authority; inventing missing evidence; editing or superseding historical VRECs or release records; transitioning `VREC-SEH-006`; preparing or transitioning `RLS-SEH-006`; creating or moving `v0.4.0`; GitHub Release or PyPI publication; deployment; merge; force push; or history rewriting.

## Authorized decision envelope

After approval, implementation may choose deterministic build directories, explicit build epoch, concise evidence layout, test helpers, and mechanical version-bearing updates required by the current implementation. It may not change the selected work-order or verification-contract sets, reinterpret an earlier candidate, change governor identity, weaken a gate, add product behavior, make an accountable transition, or perform an external publication action.

## Constraints

- Python 3.11+ standard-library runtime behavior remains supported.
- The exact released 0.3.0 governor remains the independent governance authority for this candidate.
- Candidate-owned source and package checks are qualification evidence, not independent assurance.
- Managed and protected changes follow canonical ownership, lock integrity, customization preservation, transactional update, and fail-closed migration rules.
- Repository content, paths, archives, Markdown, TOML, environment, workflow inputs, and generated reports are untrusted.
- Historical commit-bound and release records remain immutable.
- The final candidate commit cannot truthfully contain a VREC naming its own not-yet-created commit ID.

## Required verification

- Formal artifact validation reports zero errors; all warnings are classified by plane and rule.
- Start and review preflights return the complete governing manifest at their appropriate phases.
- `harnessctl inspect` is deterministic, read-only, preserves the versioned report contract, and reports every relevant pending or maintenance observation without becoming a gate.
- Full Python 3.11 and local-runtime suites pass with only documented conditional skips.
- Released-governor, candidate-source, and candidate-package planes pass and expose their exact runtime, source, package, target, and checkout-mutation boundaries.
- Candidate acceptance runs produce byte-identical canonical manifests where required; evidence identifies which evaluator produced each result.
- Version, CLI, package metadata, repository candidate configuration, workflow candidate declaration, README pin, wheel metadata, sdist metadata, and fresh-install identity all equal 0.4.0.
- The current governor descriptor and all governor inputs remain exactly 0.3.0 and resolve to the already released immutable artifact.
- Doctor, managed distribution parity, protected-control checks, workflow parsing, lock integrity, and deterministic Explorer generation pass.
- Two wheel and raw-sdist builds at one explicit candidate epoch yield byte-identical wheels and normalized sdists. Archive payloads are safe and equivalent, wheel RECORD metadata is valid, and an offline rebuild from the normalized sdist installs and operates under Python 3.11.
- Historical VREC metadata and relations remain unchanged. The new aggregate VREC contains exactly the selected work, complete verification-contract union, keyed evidence, one artifact snapshot, and one candidate commit.
- `git diff --check`, candidate ancestry, changed-path inventory, and bounded diff review pass.

## Evidence to record

Retain the baseline tag and commit, merged PR/work-order ledger, exact release scope and exclusions, pre/post version inventory, governor and candidate identities, protected-control and lock hashes, all local and hosted results, validation-plane counts, inspection queues and suggestions, deterministic manifests and snapshots, build epochs and hashes, archive-member checks, fresh-install outputs, deviations, residual risks, and explicitly unperformed external actions.

The final implementation report must identify the candidate commit separately from its later VREC governance commit. Existing VRECs support the work history but cannot replace an aggregate record bound to the final 0.4.0 candidate.

## Stop and escalate conditions

Stop on a changed proposed scope, missing evidence, incomplete contract union, version-bearing source not governed by this work, protected-policy loss, governor-field change, self-governance ambiguity, cross-role import, failed required check, unclassified warning, package mismatch, unsafe archive, nondeterministic output, mutable external dependency, candidate change after exact-commit evidence, or need for authority beyond an approved work order.

## Completion report format

Report the final ten-work-order scope and exclusions, version inventory, exact candidate commit and tree, governor identity, protected-control changes and hashes, source/package/evaluator role identities, verification counts, validation-plane summary, inspection and Explorer hashes, wheel/sdist/checksum hashes, reproducibility and offline-install results, warnings and residual risks, evidence path, work-order status, planned VREC inputs, and explicitly unperformed verification transition, release record, tag, publication, deployment, and governor promotion.

## Implementation result

The bounded 0.4.0 versioning and preliminary integrated qualification are complete. Candidate identity is 0.4.0 across package metadata, CLI, public installation guidance, candidate configuration, workflow input, managed router, and integrity lock. The independently released governor remains exactly 0.3.0. Dual-runtime regression, formal validation, managed integrity, deterministic inspection and Explorer generation, reproducible wheel and normalized-sdist builds, wheel reconstruction, and a fresh external Python 3.11 installation pass. Evidence is retained in `docs/engineering/release-0.4.0/evidence/WO-RLS-006-verification.md`.

This `implemented` state records completed work and retained evidence, not commit-bound assurance. The exact candidate commit does not yet exist, so exported-source replay, final hashes, hosted three-plane CI, and `VREC-SEH-006` preparation remain post-commit steps. No push, pull request, verification transition, release record, tag, publication, deployment, or governor promotion has been performed.
