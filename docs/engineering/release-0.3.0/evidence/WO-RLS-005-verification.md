# WO-RLS-005 implementation and preliminary qualification evidence

Date: 2026-08-15
Candidate version: `0.3.0`
Baseline commit: `00ef17be5240357e559c8d0bb2802c915c92fe03`
Baseline tree: `b78a5fab467b591cf2c27bdaf66c0f781776421b`
Previous release tag `v0.2.2`: `a7fbf8b6f24101c82f8f7515bbe3acf4626543d8`

This file is retained by the candidate commit. That commit cannot truthfully name itself before it exists. Exact candidate-commit identity, exported-source replay, candidate acceptance manifests, and final distribution hashes are therefore recorded by the later ready aggregate verification record. No verification, release, tag, publication, deployment, or governor-promotion decision is asserted here.

## Authorized release scope

The approved aggregate payload is exactly:

- `WO-DOC-007`, `WO-DOC-008`, `WO-DOC-009`, `WO-DOC-010`, and `WO-DOC-011`;
- `WO-DST-007` and `WO-DST-009`;
- `WO-SHB-002`; and
- release-integration work order `WO-RLS-005`.

The complete verification-contract union is `VER-DST-001`, `VER-DST-006`, `VER-DST-007`, `VER-DST-008`, and `VER-SHB-002`.

Governance-only work orders `WO-DST-006`, `WO-DST-008`, `WO-PUB-005`, `WO-VSP-002`, and `WO-SHB-003` were reviewed and deliberately excluded from payload coverage. The release allow-list is not inferred from dates or current status.

## Version and protected-control changes

The candidate identity is consistently set to `0.3.0` in package metadata, `se_harness.__version__`, repository harness configuration, the active workflow candidate declaration, rendered operator instructions, README installation guidance, and current version-bearing notes. Tests that validate current identity now derive it from `se_harness.__version__` instead of embedding `0.2.2`.

The two remaining `0.2.2` references in the active workflow and `tests/test_self_hosting_boundary.py` are intentional immutable historical release/VREC paths used by the independent-governor boundary. Historical engineering artifacts were not edited.

Protected control review found:

- `.self-hosting/governor.toml`: unchanged, selecting version `0.2.1`, tag `v0.2.1`, candidate commit `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5`, release record `RLS-SEH-002`, and wheel SHA-256 `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454`;
- `.github/workflows/engineering-harness.yml`: only `CANDIDATE_VERSION` changed from `0.2.2` to `0.3.0`; all governor fields remained unchanged;
- `.engineering-harness.toml`: `tool_version` changed to `0.3.0`, with repository policy retained; and
- `.engineering-harness.lock`: refreshed canonical hashes are `5f18b041620d378fb9cd1b9d8f69eeeda6ee04ae8f0cf61e99b77bb5b5bc8804` for `.engineering-harness.toml`, `60ea04e290629b197cb3b78591df348c18980e6210551bf148221867747d8f4a` for the workflow, and `7d3c4214af83b1caf395d2fcbca95052a09c610a3d1521396f82592986c38266` for `ENGINEERING_HARNESS.md`.

The release publishes the reconciler and candidate-acceptance runner but does not select 0.3.0 as governor. Promotion requires a later, separately authorized work order after immutable publication.

## Repository and test qualification

All commands completed with exit code 0 unless stated otherwise.

- `harnessctl doctor .`: passed candidate-source distribution, managed integrity, required files, and Python checks.
- Start preflight for `WO-RLS-005`: passed before implementation began.
- Formal `harnessctl validate .`: passed with 298 artifacts, 0 errors, and 38 compatibility warnings. The warnings are limited to declared legacy architecture fields/relations (`W014`/`W015`) and accepted historical non-canonical locations (`W013`); none is a new blocking finding.
- Full local suite on Python 3.14.6: 160 tests passed with 3 conditional skips.
- Full supported-runtime suite on Python 3.11.9: 160 tests passed with 3 conditional skips.
- Focused deterministic-sdist and PyPI-publication suite: 9 tests passed.
- The full suites exercise workflow parsing, source/package boundaries, managed parity, CLI behavior, archive safety, wheel RECORD checks, Explorer assets, and replayable self-hosting contracts.

Two repository Explorer generations each reported 298 artifacts, 1,074 relations, 0 errors, and 46 total validator/derived observations. Both produced:

- graph snapshot SHA-256 `634186ab6b32c08e62ba8fd7b0b2c3025cc9b21c660f66daa0b40a51eb8c780b`; and
- rendered dashboard SHA-256 `b3e3a79e87115abb209faaf130b135c917543de778f5de324870119757f25ff8`.

The 38 formal warnings are classified above; the additional Explorer observations are non-authoritative derived readiness/attention signals. Deterministic hashes match across both runs.

## Preliminary reproducible package exercise

Two independent clean tracked-source snapshots were built with Python 3.14.6, `python -m build --wheel --sdist --no-isolation`, and explicit preliminary epoch `1786786939`.

- wheel A SHA-256: `aa98ce1ded2775ce36da23933ed8faff028ff7820fb4eeea1b445d613c674208`;
- wheel B SHA-256: `aa98ce1ded2775ce36da23933ed8faff028ff7820fb4eeea1b445d613c674208`;
- raw sdist A SHA-256: `5a5f78fb037df0493c00bf5c36795b15922b3e7bb348087c682048fd13bb6de1`;
- raw sdist B SHA-256: `a68ea45da39514359acd2762370e936c04d9423c36bb92e090be532496fd9aaf`;
- normalized sdist A and B SHA-256: `f5fef738923e4237a678e3c901894759c600e6a3497279b2b2547fbc96bdf7a1`; and
- offline wheel reconstructed from the normalized sdist SHA-256: `aa98ce1ded2775ce36da23933ed8faff028ff7820fb4eeea1b445d613c674208`.

The raw gzip containers vary before normalization as designed. Wheels are byte-identical, normalized sdists are byte-identical, and the offline reconstructed wheel is byte-identical to both direct wheels.

A fresh Python 3.11.9 virtual environment installed the wheel with `pip --no-deps`. `harnessctl --version` returned `0.3.0`; its command surface included `reconcile-governor` and `accept-candidate`. A new repository initialized 33 files, `doctor` passed every distribution and managed-integrity check, validation passed with 0 artifacts/errors/warnings, and Explorer generation passed.

## Deviations and residual risks

- The first in-place build attempt could not update an existing ignored `se_harness.egg-info` directory because of the execution sandbox's file ACL. Repeating the same build from clean exported source succeeded twice; this is classified as a local staging constraint, not a package defect.
- Setuptools reports that the TOML-table form of `project.license` is deprecated with a stated 2027-02-18 deadline. It does not affect the 0.3.0 build or metadata checks. A later governed maintenance change should migrate to an SPDX expression.
- The current validator/Explorer compatibility warnings remain visible and are not converted into an aggregate health score or implicit satisfaction.
- The final exact candidate commit has not yet existed during this preliminary run. After the candidate commit, acceptance and reproducible builds must be repeated from an exact exported commit at that commit's epoch. Any mismatch invalidates this candidate and stops verification preparation.

## External actions deliberately not performed

No push, pull request, merge, `ready -> verified` transition, release record, release transition, tag, GitHub Release, PyPI publication, deployment, or governor reconciliation/promotion was performed by this work order.
