# WO-RLS-006 implementation and preliminary qualification evidence

Date: 2026-08-16

Candidate version: `0.4.0`

Baseline branch head: `76cda089aa30d347f2517c976a6bab3bf2e0ef6e`

Baseline tree: `09ae1ab81244ba4c61d5fa9a1865ddceac3e5b1e`

Previous release candidate and tag target: `dd06660a94f06d934adb1df0352b81e709f2ffd3` (`v0.3.0`)

This file is retained by the working-tree candidate. That candidate cannot truthfully name its own commit before the commit exists. Exact candidate-commit identity, exported-source replay, final distribution hashes, and candidate acceptance therefore remain prerequisites to the later ready aggregate verification record. No verification, release, tag, publication, deployment, or governor-promotion decision is asserted here.

## Authorized release scope

The approved aggregate payload is exactly:

- `WO-DOC-012`;
- `WO-IAR-006`, `WO-IAR-007`, `WO-IAR-008`, `WO-IAR-009`, and `WO-IAR-010`;
- `WO-OCA-001` and `WO-OCA-002`;
- `WO-WAC-001`; and
- release-integration work order `WO-RLS-006`.

The complete verification-contract union is `VER-DST-001`, `VER-DST-009`, `VER-IAR-006`, `VER-IAR-007`, `VER-IAR-008`, `VER-IAR-009`, `VER-IAR-010`, `VER-OCA-001`, `VER-OCA-002`, and `VER-WAC-001`.

Repository-specific governor promotion and assurance (`WO-SHB-004`, `WO-SHB-005`), stale-record supersession and publication (`WO-VSP-003`, `WO-VSP-004`, `WO-VSP-005`), obsolete release-proposal disposition (`WO-RCD-001`), and architecture reassessment (`WO-DST-010`) were reviewed and deliberately excluded as governance maintenance. The release allow-list is not inferred from dates, statuses, or every commit after `v0.3.0`.

## Version and protected-control changes

Candidate identity is 0.4.0 in:

- `pyproject.toml` and `se_harness.__version__`;
- README and installation-note public pins;
- current conceptual and self-hosting development notes;
- `.engineering-harness.toml`;
- `.github/workflows/engineering-harness.yml` candidate input;
- the active rendered `ENGINEERING_HARNESS.md`; and
- `.engineering-harness.lock` tool identity and protected-file hashes.

The exact protected hashes after the candidate update are:

- `.engineering-harness.toml`: `f27881da7e21d73f9fec8aa1a2f9b514a6229db2fa74fbb819c930c6d0c8ffce`;
- `.github/workflows/engineering-harness.yml`: `711a7098b08d2a5d97aa7dd8c3b9c71bfbb86d37dc42573220ea7dfb811cb3f3`; and
- `ENGINEERING_HARNESS.md`: `f2978acca17630dd8bb22cd7e31b92cacf10e9327a732c227eca44220921bfe8`.

`.self-hosting/governor.toml` is unchanged and continues to select version 0.3.0, tag `v0.3.0`, wheel `se_harness-0.3.0-py3-none-any.whl`, release record `RLS-SEH-005`, candidate commit `dd06660a94f06d934adb1df0352b81e709f2ffd3`, and wheel SHA-256 `260e22371b05e5bb6c59143a1f0229855305a6bf7994984be50aa147a02ea516`. The workflow retains the same immutable reusable-workflow pin and all governor inputs; only `candidate-version` changed to 0.4.0.

Two release-sensitive assertions were corrected:

- the self-hosting workflow test now requires its candidate version to equal `se_harness.__version__`; and
- the development-note test reads the selected governor version from `.self-hosting/governor.toml` instead of requiring historical literal 0.2.1.

## Repository qualification

All final commands in this section completed with exit code 0 unless stated otherwise.

- Start preflight passed for approved `WO-RLS-006` with commit-bound verification classified `required` by `repository-owner`.
- `python -m se_harness doctor .` passed required files, canonical distribution parity, protected lock integrity, repository-specific self-hosting controls, and Python checks. It confirmed governor 0.3.0 and reported only the known historical non-canonical-location warnings.
- Formal validation passed with 377 artifacts, zero errors, and 40 maintenance warnings: 11 `W013`, 14 `W014`, and 15 `W015`. Structure, governance, and policy planes contain zero errors and zero warnings. The warnings are declared legacy locations or architecture compatibility observations and are not release gates.
- The complete Python 3.14.6 suite passed 201 tests with three conditional skips.
- The complete Python 3.11.9 suite passed 201 tests with the same three conditional skips.
- The first Python 3.14 suite exposed one stale documentation assertion requiring literal governor 0.2.1. The test was corrected to derive the selected governor from the authoritative descriptor, and both complete suites then passed.
- Inspection reported 377 artifacts, 1,369 relations, 40 maintenance findings, no decision-ready definitions, no assurance backlog, and only the active release work order before its implemented transition.
- Two inspection JSON projections were byte-identical after capture normalization, SHA-256 `613b1509a22b076b5195c674b249f06b5655c70a4cffb7cb6bdea77b485e39a7`.
- Two Explorer generations were byte-identical: snapshot SHA-256 `32f656910e90ba4c8be4675658336750b7ea72bf0d9097adb2e22e9e2ea1ec82` and rendered HTML SHA-256 `4a4e1434a94a36d0cf36c5e9a8cd3811773383564b8d9e6ac135241fb88c10c1`.

The inspection and Explorer hashes above precede the honest `in_progress -> implemented` transition of `WO-RLS-006`. Final review hashes are recorded below after that lifecycle update; the earlier hashes are retained to show deterministic behavior during implementation.

After the transition to `implemented`, review preflight, formal validation, doctor, and diff hygiene passed again. Final inspection reported no decision-ready definitions, no active work, and exactly one expected assurance item: `WO-RLS-006`, recommending preparation of commit-bound verification only after a clean candidate commit exists. Two final inspection JSON projections were byte-identical with SHA-256 `2dd60acd6c7aa4353f185f319326232dadd2ea6483f7e77ce88cc218073e8070`. Two final Explorer generations were byte-identical with snapshot SHA-256 `18b540961c6ad737729fa5e8eb570564616ac4e25cb0489c0ecfef0563da2412` and rendered HTML SHA-256 `5bde84caf4a07adb39952234888ddf50e527dcd003d1c871bb4a36541869b400`.

## Preliminary reproducible package exercise

Two independent builds used Python 3.14.6, `python -m build --wheel --sdist --no-isolation`, and explicit preliminary epoch `1786875636`, the baseline branch-head commit timestamp.

- wheel A SHA-256: `83f6623b5f2a3c3c15f932985e16d090c093e334331118c1335c7b159b247294`;
- wheel B SHA-256: `83f6623b5f2a3c3c15f932985e16d090c093e334331118c1335c7b159b247294`;
- raw sdist A SHA-256: `83df6c30566dbe994ea3017967c8a65451f54f141f6f5abcc397864c49cb7b1c`;
- raw sdist B SHA-256: `d142f8820bc991d8b993ce8870c8c199024033e9bbddb015c34de6150f3c2a41`;
- normalized sdist A and B SHA-256: `4892af19418b747d0fcd281530f9f70092c135f41586dacd000e85d76d7a971b`; and
- wheel rebuilt from the safely normalized sdist SHA-256: `83f6623b5f2a3c3c15f932985e16d090c093e334331118c1335c7b159b247294`.

The raw gzip containers vary before normalization as designed. Wheels are byte-identical, normalized sdists are byte-identical, and the reconstructed wheel is byte-identical to both direct wheels. Normalization validated member paths and types before producing the canonical archive. The complete release-build and package-publication regression tests also passed in both runtime suites.

Setuptools emitted its existing deprecation warning for the TOML-table form of `project.license`, with a stated 2027-02-18 deadline. It does not alter package identity, build success, archive safety, or reproducibility. Changing license metadata is outside this release-integration work order and remains later governed maintenance.

## Fresh Python 3.11 package exercise

The preliminary wheel installed with `pip --no-index --no-deps` into a new Python 3.11.9 virtual environment. The authoritative external run was launched from outside the source checkout and proved:

- CLI and distribution version `0.4.0`;
- Python executable under the isolated environment;
- module origin under that environment's `Lib/site-packages/se_harness`, not the checkout;
- initialization of all 34 standard consumer files;
- managed-integrity doctor success;
- formal validation with zero artifacts, errors, or warnings;
- inspection with zero findings or suggestions; and
- Explorer generation with zero errors and snapshot SHA-256 `c5a3f2dfc7a78a7bc2dd30f066c79789efec264ab70bb44a137912e5a9aeb53a`.

An earlier run launched from the checkout resolved the module from the checkout because the current directory precedes site-packages on Python's import path. That run is explicitly discarded as package-origin evidence. It led to the required external-working-directory repetition above and did not reveal a package defect.

## Residual checks and authority boundary

The exact candidate commit and commit timestamp do not exist yet. After a separately authorized candidate commit, qualification must be replayed from an exact Git export, final wheel and normalized-sdist hashes must be recorded, the released 0.3.0 governor must assess the exact candidate boundary, and hosted three-plane CI must pass before `VREC-SEH-006` can be considered for accountable verification.

No push, pull request, merge, ready verification record, verification transition, release record, release decision, tag, GitHub Release, PyPI publication, deployment, governor reconciliation, force push, or history rewrite was performed during this implementation step.
