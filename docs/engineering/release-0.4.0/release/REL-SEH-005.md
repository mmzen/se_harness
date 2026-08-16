+++
id = "REL-SEH-005"
type = "release_contract"
title = "Qualify and release se-harness 0.4.0"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
gates = ["WO-DOC-012", "WO-IAR-006", "WO-IAR-007", "WO-IAR-008", "WO-IAR-009", "WO-IAR-010", "WO-OCA-001", "WO-OCA-002", "WO-RLS-006", "WO-WAC-001"]
+++

# Release Contract: Qualify and release se-harness 0.4.0

## Lifecycle and authorization

On 2026-08-16, after reviewing the exact allow-list, verification boundary, compatibility policy, and release procedure, the repository owner stated `i approve`. That decision approves this release contract and `WO-RLS-006` and authorizes the bounded 0.4.0 candidate implementation, qualification evidence, candidate commit, and later preparation of `VREC-SEH-006` as `ready`. It does not authorize push, pull-request creation or merge, the VREC's verification transition, release-record preparation or transition, tagging, publication, deployment, or governor promotion.

## Release unit

One incremental `se-harness` 0.4.0 release derived from a single clean candidate commit: a reproducible wheel, normalized source distribution, checksum manifest, immutable `v0.4.0` tag, GitHub Release assets, and unchanged promotion of the qualified files to the `se-harness` PyPI project.

The exact release-bearing work is:

- `WO-IAR-006`: authoritative artifact-purpose and applicability catalog with conditional architecture coverage;
- `WO-IAR-007`: four-plane validation diagnostic taxonomy without changing gate semantics;
- `WO-IAR-008`: deterministic, read-only `harnessctl inspect` command;
- `WO-IAR-009`: bounded, non-executable inspection suggestions;
- `WO-IAR-010`: typed temporal-reassessment finding semantics;
- `WO-DOC-012`: current validation and inspection documentation;
- `WO-OCA-001`: active operating-contract definitions and corrected distributed authoring material;
- `WO-OCA-002`: operating-assurance target and readiness enforcement;
- `WO-WAC-001`: explicit work-order commit-bound assurance classification and inspection follow-up; and
- `WO-RLS-006`: 0.4.0 versioning, integrated qualification, reproducible packaging, and final-candidate evidence.

The release contract is an allow-list, not an inference from dates, statuses, branches, or all changes after `v0.3.0`.

## Explicit exclusions

The following post-0.3.0 work remains auditable in the selected candidate but is not release payload and is deliberately absent from `gates`, aggregate verification coverage, and `releases_work`:

- `WO-SHB-004` and `WO-SHB-005`: repository-specific promotion and assurance recording for the already published 0.3.0 governor;
- `WO-VSP-003`, `WO-VSP-004`, and `WO-VSP-005`: governance-only supersession and publication of stale-record cleanup;
- `WO-RCD-001`: governance-only rejection of obsolete draft release proposals; and
- `WO-DST-010`: accountable reassessment of existing architecture after dependency revisions.

Those exclusions do not hide their repository changes. Qualification still validates the complete selected commit and reports any effect they have on graph consistency, packaging, CI, or release safety.

## Entry criteria

- The nine existing gated work orders are `implemented`, active, and supported by retained evidence keyed to each work-order ID.
- The final repository, package, candidate workflow, public installation guidance, and integrity metadata consistently identify candidate version 0.4.0.
- `.self-hosting/governor.toml` continues to select immutable released governor 0.3.0 during creation of this release. Candidate qualification must not silently promote 0.4.0 or claim that it independently governed itself.
- The root self-hosting workflow continues to acquire the exact released 0.3.0 governor by immutable URL and checksum while identifying the candidate package as 0.4.0.
- Protected configuration, workflow, router, and lock changes are explicit, bounded, customization-safe, and fail closed.
- The released-governor, candidate-source, and candidate-package planes pass with their distinct authority meanings preserved.
- Formal validation has zero errors. Every warning and inspection observation is classified and shown not to weaken the release payload.
- Supported-runtime regression, CLI, doctor, start/review preflight, validation, inspection, Explorer generation, managed parity, workflow parsing, package content, archive safety, reproducibility, fresh installation, and exact-version checks pass.
- One clean candidate commit exists before aggregate `VREC-SEH-006` is captured as `ready` in a later governance commit.

## Required aggregate verification

`VREC-SEH-006` must bind one clean 0.4.0 candidate commit to exactly the ten gated work orders. Its `conforms_to` relation must be the union of their declared contracts: `VER-DST-001`, `VER-DST-009`, `VER-IAR-006`, `VER-IAR-007`, `VER-IAR-008`, `VER-IAR-009`, `VER-IAR-010`, `VER-OCA-001`, `VER-OCA-002`, and `VER-WAC-001`. It must retain one repository-contained evidence path keyed to every selected work order.

Existing verified records demonstrate earlier isolated candidates and remain immutable evidence, but they cannot form the 0.4.0 release manifest because they identify different commits. The new aggregate record assesses the complete integrated payload at one final candidate; it does not rewrite or retroactively extend any earlier VREC.

After accountable assurance review transitions `VREC-SEH-006` to `verified`, `RLS-SEH-006` may be prepared as `ready`. Its `releases_work` set must equal the VREC work set exactly, it must include only commit-compatible verification records, and it must copy the same candidate commit and Git object format.

## Compatibility and migration

Retain Python 3.11+ and the single standard consumer installation. Existing repositories remain upgradeable through the customization-preserving managed workflow. The new work-order assurance declaration is mandatory for newly created work orders while legacy work orders remain valid under the explicit compatibility rule; upgrades must not fabricate classification decisions for repository-owned historical work.

Validation keeps its existing gating meaning while adding plane metadata. Inspection remains read-only, non-gating, deterministic, and advisory. Existing automation that consumes validation output must retain compatible codes, messages, severity, validity, and exit behavior; inspection JSON uses its documented versioned contract.

Operating-contract readiness enforcement applies to active assurance claims without inventing recurring assessment records or release-to-operations relations. Existing explicitly migrated contracts and repository-owned policy values must remain intact.

## Security, provenance, and reproducibility

- The aggregate VREC, release record, tag, wheel, normalized source distribution, checksum manifest, GitHub Release, and PyPI files identify or derive from the same candidate commit.
- Build twice from exported candidate source at one explicit epoch; require byte-identical wheels and normalized sdists plus matching safe payload manifests.
- Reconstruct the wheel offline from the normalized sdist and prove fresh Python 3.11 installation and core operations, including `validate` and `inspect`.
- Acquire the selected 0.3.0 governor only from its immutable release URL and retained SHA-256. Treat checkout, archive, workflow, path, environment, PR metadata, artifact content, Markdown, and TOML as untrusted input.
- Prove inspection suggestions remain closed-catalog, non-executable, and incapable of granting authority or mutating repository state.
- Retain exact runtime, package, source, template, workflow, governor, candidate, report-schema, and artifact identities without secrets or complete environment dumps.
- A candidate change after verification invalidates the VREC and release proposal and requires a new candidate-bound sequence.

## Promotion policy and authority

Under the recorded approval, `WO-RLS-006` may implement versioning, qualify the bounded candidate, retain evidence, create one clean candidate commit, and later prepare only `VREC-SEH-006` as `ready`. Accountable quality and release owners separately decide `verified` and `released`.

Approval of this packet will not authorize push, pull-request creation or merge, the VREC's `ready -> verified` transition, release-record preparation or transition, tag creation, GitHub or PyPI publication, deployment, or governor promotion. Each remains a separately requested action at the applicable boundary.

Publication of 0.4.0 will not activate it as this repository's governor. A later, separately governed `reconcile-governor` transaction may propose that promotion only after the exact release is immutable and independently identifiable.

## Stop and rollback policy

Stop on an omitted or extra release-bearing work order, governance-only work included as payload, missing keyed evidence, inconsistent contract union, changed historical provenance, commit mismatch, version disagreement, protected-control ambiguity, governor identity drift, failed required check, unexplained warning, non-reproducible artifact, unsafe archive member, stale or mutable governor source, package/repository divergence, or authority beyond the approved phase.

Before publication, correct a failure through a new candidate and newly captured VREC/RLS sequence without rewriting history. After publication, never move the tag or replace an uploaded package file; preserve evidence and issue a separately governed corrective version.

## Post-release observation window

After publication, confirm the immutable tag and GitHub assets, PyPI metadata and hashes, fresh public installation on Python 3.11, `harnessctl --version`, initialization of a clean repository, managed-integrity doctor, formal validation, deterministic inspection, and dashboard generation. Record any failure without replacing published files or treating publication automation as release authority.
