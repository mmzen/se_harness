+++
id = "VREC-SEH-005"
type = "verification_record"
title = "Verification candidate for 9 work orders"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"
commit = "dd06660a94f06d934adb1df0352b81e709f2ffd3"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-15T10:24:04Z"
artifact_snapshot_sha256 = "2660075fde53dbdd1e660fb0b051b94afd024046418c75e103306322e264d86f"
evidence_paths = ["docs/engineering/harness-distribution/evidence/WO-DOC-007-verification.md", "docs/engineering/harness-distribution/evidence/WO-DOC-008-verification.md", "docs/engineering/harness-distribution/evidence/WO-DOC-009-verification.md", "docs/engineering/harness-distribution/evidence/WO-DOC-010-verification.md", "docs/engineering/harness-distribution/evidence/WO-DOC-011-verification.md", "docs/engineering/harness-distribution/evidence/WO-DST-007-verification.md", "docs/engineering/harness-distribution/evidence/WO-DST-009-verification.md", "docs/engineering/release-0.3.0/evidence/WO-RLS-005-verification.md", "docs/engineering/self-hosting-boundary/evidence/WO-SHB-002-verification.md"]

[relations]
verifies_work_order = ["WO-DOC-007", "WO-DOC-008", "WO-DOC-009", "WO-DOC-010", "WO-DOC-011", "WO-DST-007", "WO-DST-009", "WO-RLS-005", "WO-SHB-002"]
conforms_to = ["VER-DST-001", "VER-DST-006", "VER-DST-007", "VER-DST-008", "VER-SHB-002"]
+++

# Verification Record Candidate

This verified record binds retained evidence for `WO-DOC-007`, `WO-DOC-008`, `WO-DOC-009`, `WO-DOC-010`, `WO-DOC-011`, `WO-DST-007`, `WO-DST-009`, `WO-RLS-005`, `WO-SHB-002` to candidate commit `dd06660a94f06d934adb1df0352b81e709f2ffd3`. The capture command originally prepared it as `ready` and did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Exact candidate qualification presented for assurance review

- Candidate commit: `dd06660a94f06d934adb1df0352b81e709f2ffd3`
- Candidate tree: `f7af813414aa6da5fe9a478070e38a74eefe8305`
- Candidate Unix timestamp and reproducibility epoch: `1786789037`
- Exact `git archive` SHA-256: `ffdb1fe9bc379dcb7f1cb22ac23fa47b54058d017bc2c54a8be3a0a66269faa7`
- Wheel A/B and offline-reconstructed wheel SHA-256: `260e22371b05e5bb6c59143a1f0229855305a6bf7994984be50aa147a02ea516`
- Raw sdist A SHA-256: `3d99505c29e2427e8980eca82893215cdd7aecaf2b930a915777fb3246b138da`
- Raw sdist B SHA-256: `d06482513dac21453018aa62a2d32747c9a0d9632144f3b8d1e6e3a9fd16e6f2`
- Normalized sdist A/B SHA-256: `dc25b236c7c102bbbd7e99b36dfb6e90e1fe59b1d4fcdb9896d70f55b1d09704`
- Candidate-acceptance manifest A/B SHA-256: `0292f9948f9a6369bb11290253576089cca86e77a028fff07489d7a22c5731fe`
- Acceptance contract SHA-256: `48fc055e5123d61b6484656f9d53135188b2432f4d6976f3efef80742cee4349`

Both exact-source builds completed at the candidate epoch. Wheels were byte-identical; raw gzip sdists varied before the governed normalization step; normalized sdists were byte-identical. A no-index wheel reconstruction from the normalized sdist was byte-identical to both direct wheels.

The candidate-owned 0.3.0 acceptance runner passed the same 11 black-box scenarios twice and emitted byte-identical canonical manifests: installed identity, init, adopt, doctor, validate, dashboard, safe upgrade, customized-content refusal, corrupted-integrity refusal, protected self-hosting upgrade, and authority denial. This proves repeatability of the candidate contract; it is not relabelled as independent governor evidence.

The independently selected governor remains immutable 0.2.1 with wheel SHA-256 `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454`. `.self-hosting/governor.toml` did not change. Publishing 0.3.0 will not promote it as governor.

The complete suite passed on Python 3.14.6 (160 tests, 3 conditional skips) and Python 3.11.9 (160 tests, 3 conditional skips). Candidate-source doctor and review preflight passed. Candidate artifact validation passed with 298 artifacts, 0 errors, and 38 classified compatibility warnings. A fresh Python 3.11.9 environment installed the offline-reconstructed wheel without an index, reported version 0.3.0, initialized 33 managed/seed files, passed doctor and validation, and generated Harness Explorer successfully.

Setuptools emitted one known non-blocking deprecation warning for the TOML-table form of `project.license`, with a stated 2027-02-18 migration deadline.

On 2026-08-15, after reviewing the exact candidate and retained evidence, the accountable owner explicitly instructed `i approve verification record`. That human assurance decision transitioned this record from `ready` to `verified`; automation did not grant the authority. Release-record preparation, release approval, push, pull request, merge, tag, publication, deployment, and governor promotion remain separate decisions and were not performed by this transition.
