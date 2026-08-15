+++
id = "REL-SEH-004"
type = "release_contract"
title = "Qualify and release se-harness 0.3.0"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
gates = ["WO-DOC-007", "WO-DOC-008", "WO-DOC-009", "WO-DOC-010", "WO-DOC-011", "WO-DST-007", "WO-DST-009", "WO-RLS-005", "WO-SHB-002"]
+++

# Release Contract: Qualify and release se-harness 0.3.0

## Release unit

One incremental `se-harness` 0.3.0 release derived from a single clean candidate commit: a reproducible wheel, normalized source distribution, checksum manifest, immutable `v0.3.0` tag, GitHub Release assets, and unchanged promotion of the qualified files to the `se-harness` PyPI project.

The exact release-bearing work is:

- `WO-DOC-007`: progressive current documentation for readers from overview through practical use;
- `WO-DOC-008`: concise public README with operational detail moved to maintained notes;
- `WO-DOC-009`: explicit trunk-based development and maintenance-branch examples;
- `WO-DOC-010`: refused-verification and append-only Git consequences;
- `WO-DOC-011`: public Harness Explorer screenshots and action-oriented README presentation;
- `WO-DST-007`: canonical interactive Harness Explorer WebUI;
- `WO-DST-009`: Explorer presentation refinements and canonical-template consolidation;
- `WO-SHB-002`: protected self-hosting upgrades, published-governor reconciliation, and replayable candidate acceptance; and
- `WO-RLS-005`: 0.3.0 versioning, integrated qualification, reproducible packaging, and final-candidate evidence.

`WO-DST-006`, `WO-DST-008`, `WO-PUB-005`, `WO-VSP-002`, and `WO-SHB-003` are governance-only transition, publication, or supersession records. They remain auditable but are not release payload and are deliberately absent from `gates`, aggregate verification coverage, and `releases_work`.

## Entry criteria

- All nine gated work orders are `implemented`, active, and supported by retained evidence keyed to each work-order ID.
- The final repository, package, candidate workflow, public install guidance, and integrity metadata consistently identify version 0.3.0.
- `.self-hosting/governor.toml` continues to select immutable released governor 0.2.1 during this creation release; candidate versioning must not silently change governor identity or claim that 0.3.0 independently governed itself.
- Protected self-hosting controls change only where explicitly required for the 0.3.0 candidate identity and matching lock evidence; ordinary `upgrade` is not used to overwrite or bless those controls.
- The released-governor, candidate-source, and candidate-package planes pass with their authority meanings kept distinct. Candidate-owned acceptance evidence is never relabelled as independent released-governor proof.
- Formal validation has zero errors. Every warning or compatibility boundary is classified and shown not to weaken the release payload.
- Supported-runtime regression, CLI, doctor, start/review preflight, deterministic Explorer, workflow parsing, managed parity, package content, archive safety, reproducibility, fresh installation, and exact-version checks pass.
- One clean candidate commit exists before aggregate `VREC-SEH-005` is captured as `ready` in a later governance commit.

## Required aggregate verification

`VREC-SEH-005` must bind one clean 0.3.0 candidate commit to exactly the nine gated work orders. Its `conforms_to` relation must be the union of their declared contracts: `VER-DST-001`, `VER-DST-006`, `VER-DST-007`, `VER-DST-008`, and `VER-SHB-002`. It must retain one repository-contained evidence path keyed to every selected work order.

Historical records remain immutable evidence but cannot form the 0.3.0 release manifest because they identify different commits. This includes verified `VREC-DST-005`, `VREC-DST-008`, `VREC-DST-009`, and `VREC-SHB-001`, ready `VREC-DST-006`, and the absence of a standalone VREC for `WO-DOC-010`. The new aggregate record assesses the complete integrated payload at one final candidate; it does not rewrite or retroactively change those records.

After accountable assurance review transitions `VREC-SEH-005` to `verified`, `RLS-SEH-005` may be prepared as `ready`. Its `releases_work` set must equal the VREC work set exactly, it must include only commit-compatible verification records, and it must copy the same candidate commit and Git object format.

## Compatibility and migration

Retain Python 3.11+ and the single standard consumer installation. Existing consumer repositories remain upgradeable through the customization-preserving managed workflow. Current repository-specific self-hosting policy remains explicit. Configuration-schema and workflow changes must preserve repository-owned values, require explicit decisions for authority-bearing inputs, and fail closed on incompatible or ambiguous migration.

The 0.3.0 release is the first immutable publication of the reconciler and released acceptance runner implemented by `WO-SHB-002`. Publication does not activate either as the current governor. A later, separately authorized promotion work order may select the published 0.3.0 commit, release record, wheel, URL, and SHA-256 through the previously trusted promotion process. Until that change is accepted, governor 0.2.1 remains authoritative.

## Security, provenance, and reproducibility

- The aggregate VREC, release record, tag, wheel, normalized source distribution, checksum manifest, GitHub Release, and PyPI files identify or derive from the same candidate commit.
- Build twice from exported candidate source at one explicit epoch; require byte-identical wheels and normalized sdists plus matching safe payload manifests.
- Reconstruct the wheel offline from the normalized sdist and prove fresh Python 3.11 installation and core operations.
- Acquire the selected governor only from its immutable release URL and retained SHA-256. Treat checkout, archive, workflow, path, environment, PR metadata, and artifact content as untrusted input.
- Retain exact runtime, package, source, template, workflow, governor, and candidate identities without secrets or complete environment dumps.
- A candidate change after verification invalidates the VREC and release proposal and requires a new candidate-bound sequence.

## Promotion policy and authority

The repository owner approved `REL-SEH-004` and `WO-RLS-005` on 2026-08-15. That decision authorizes the bounded implementation, qualification evidence, candidate commit, and later preparation of `VREC-SEH-005` as `ready`. It does not authorize push, pull-request creation or merge, the VREC's `ready -> verified` transition, preparation or transition of a release record, tag creation, GitHub or PyPI publication, deployment, or governor promotion.

After separate approval, `WO-RLS-005` may prepare and qualify the candidate and later create only a `ready` aggregate VREC. Accountable quality and release owners separately decide `verified` and `released`. Tagging, GitHub release creation, PyPI promotion, deployment, and post-publication governor promotion remain separately authorized external actions.

## Stop and rollback policy

Stop on an omitted or extra release-bearing work order, governance-only work included as payload, missing keyed evidence, inconsistent contract union, changed historical provenance, commit mismatch, version disagreement, protected-control ambiguity, failed required check, unexplained warning, non-reproducible artifact, unsafe archive member, stale or mutable governor source, package/repository divergence, or authority beyond the approved phase.

Before publication, correct a failure through a new candidate and newly captured VREC/RLS sequence without rewriting history. After publication, never move the tag or replace an uploaded package file; preserve evidence and issue a separately governed corrective version.
