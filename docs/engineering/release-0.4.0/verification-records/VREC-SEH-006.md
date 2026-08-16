+++
id = "VREC-SEH-006"
type = "verification_record"
title = "Verification candidate for 10 work orders"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
commit = "2acc63af8933ee1dfa5ef78b67e2dbe6fb9a4e61"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-16T10:45:01Z"
artifact_snapshot_sha256 = "cebd3ef6d57baa417d65e0fd4517d02500a513afc0f216bd301f3fab77d8cb3a"
evidence_paths = ["docs/engineering/harness-distribution/evidence/WO-DOC-012-verification.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-006-verification.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-007-verification.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-008-verification.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-009-verification.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-010-verification.md", "docs/engineering/operating-contract-activation/evidence/WO-OCA-001-verification.md", "docs/engineering/operating-contract-activation/evidence/WO-OCA-002-verification.md", "docs/engineering/release-0.4.0/evidence/WO-RLS-006-verification.md", "docs/engineering/work-order-assurance-classification/evidence/WO-WAC-001-verification.md"]

[relations]
verifies_work_order = ["WO-DOC-012", "WO-IAR-006", "WO-IAR-007", "WO-IAR-008", "WO-IAR-009", "WO-IAR-010", "WO-OCA-001", "WO-OCA-002", "WO-RLS-006", "WO-WAC-001"]
conforms_to = ["VER-DST-001", "VER-DST-009", "VER-IAR-006", "VER-IAR-007", "VER-IAR-008", "VER-IAR-009", "VER-IAR-010", "VER-OCA-001", "VER-OCA-002", "VER-WAC-001"]
+++

# Verification Record Candidate

On 2026-08-16, after pull request #60 run `31942798447` passed the released-governor, candidate-source, and candidate-package planes for the exact candidate, the accountable owner explicitly instructed `i approve`. That human assurance decision transitions this record from `ready` to `verified`; automation did not grant the authority. The captured candidate commit, object format, clean worktree state, capture timestamp, artifact snapshot, evidence paths, work-order coverage, and verification-contract coverage remain unchanged.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Exact candidate qualification presented for assurance review

- Candidate commit: `2acc63af8933ee1dfa5ef78b67e2dbe6fb9a4e61`
- Candidate tree: `18a812d6a224cc34205af6f2882b0cccd05f3d9b`
- Git object format: `sha1`
- Candidate Unix timestamp and reproducibility epoch: `1786876848`
- Exact `git archive` SHA-256: `211475323aa812c787ad03040e27f6ddaba6a4e732bb1b0bfccdd0e63563c72`
- Candidate artifact snapshot SHA-256: `cebd3ef6d57baa417d65e0fd4517d02500a513afc0f216bd301f3fab77d8cb3a`
- Wheel A/B and normalized-sdist-reconstructed wheel SHA-256: `674489eb1e4798e84d0708b6e1b0c57cb794e7c59a23029186bbe413be209e13`
- Raw sdist A SHA-256: `a807ae3c10717971b1cf657f288c8554cd8f208c07ebd26db23e95c9a96b74be`
- Raw sdist B SHA-256: `51a861d0ddf7bf8360657e0be3fefded368c6e04de3ffc5094c4652c7c6f56a5`
- Normalized sdist A/B SHA-256: `0501056a5e49de88db6835613ff02f256bf5e695c16a6ed8dc3a7f507bfca13d`
- Released-governor acceptance manifest A/B SHA-256: `33d1ae793ea9eef4cb86e15d844653b70c5baf4422bc0589b98315cdc12400a8`
- Acceptance contract SHA-256: `48fc055e5123d61b6484656f9d53135188b2432f4d6976f3efef80742cee4349`

Two independent exact-source builds completed at the candidate epoch. Wheels were byte-identical; raw gzip sdists varied before the governed normalization step; normalized sdists were byte-identical. A wheel rebuilt from a safely extracted normalized sdist was byte-identical to both direct wheels. Archive paths and member types passed the normalizer's fail-closed checks.

## Independent governor assessment

The exact published governor remains version 0.3.0, release record `RLS-SEH-005`, candidate commit `dd06660a94f06d934adb1df0352b81e709f2ffd3`, and wheel SHA-256 `260e22371b05e5bb6c59143a1f0229855305a6bf7994984be50aa147a02ea516`. The wheel was downloaded from the immutable URL recorded by `.self-hosting/governor.toml`; its digest matched before installation. Its isolated Python 3.11.9 runtime resolved the module and distribution from the governor environment, outside the candidate checkout.

The released 0.3.0 governor assessed the exact 0.4.0 wheel and a clean export of candidate commit `2acc63af8933ee1dfa5ef78b67e2dbe6fb9a4e61` twice. All 11 replayable scenarios passed both times with byte-identical canonical manifests:

- installed identity;
- init and adopt;
- doctor, validate, and dashboard;
- safe upgrade;
- customized-content and corrupted-integrity refusal;
- protected self-hosting upgrade; and
- authority denial.

This is independent released-governor evidence for the candidate package and declared compatibility contract. It does not grant verification, release, merge, tag, publication, deployment, or governor-promotion authority.

## Integrated repository and package evidence

- Formal validation passed with 377 artifacts, zero errors, and 40 maintenance warnings: 11 `W013`, 14 `W014`, and 15 `W015`. Structure, governance, and policy planes are clear. The warnings are declared historical locations and legacy architecture compatibility observations, not hidden or converted into a score.
- Candidate-source doctor passed managed parity, lock integrity, required files, and the explicit 0.3.0 governor identity.
- Start and review preflight passed for `WO-RLS-006`, whose commit-bound assurance classification is `required` and decided by `repository-owner`.
- The complete suite passed on Python 3.14.6: 201 tests with three conditional skips.
- The complete suite passed on Python 3.11.9: 201 tests with the same three conditional skips.
- Deterministic candidate inspection and Explorer generation passed. Before VREC capture, inspection exposed exactly one expected assurance item, `WO-RLS-006`, and no active or decision-ready work.
- Protected candidate hashes are `f27881da7e21d73f9fec8aa1a2f9b514a6229db2fa74fbb819c930c6d0c8ffce` for `.engineering-harness.toml`, `711a7098b08d2a5d97aa7dd8c3b9c71bfbb86d37dc42573220ea7dfb811cb3f3` for `.github/workflows/engineering-harness.yml`, and `f2978acca17630dd8bb22cd7e31b92cacf10e9327a732c227eca44220921bfe8` for `ENGINEERING_HARNESS.md`.
- The candidate workflow changes only its candidate version to 0.4.0. The governor version, tag, wheel, immutable URL, SHA-256, release record, released candidate commit, reusable-workflow pin, permissions, and three-plane structure remain unchanged at 0.3.0.
- `git diff --check`, exact scope review, candidate ancestry, and clean candidate capture passed.

A fresh Python 3.11.9 environment installed the wheel reconstructed from the normalized sdist with `pip --no-index --no-deps`. From outside the checkout it resolved version, module, executable, distribution, and template data from the isolated environment; initialized 34 standard files; passed doctor and formal validation; produced no inspection findings; and generated Explorer snapshot SHA-256 `c7fc28c167fd0c8fa8c95cb67276c6083aa7af40f63356c6f84a0d1fbb148e48`.

## Deviations and residual conditions

- One preliminary fresh-install invocation was launched from the source checkout, so Python correctly placed the checkout ahead of site-packages. That run was discarded as package-origin evidence and repeated successfully from an external working directory.
- Setuptools emitted the existing non-blocking deprecation warning for the TOML-table form of `project.license`, with a stated 2027-02-18 deadline. This does not affect current metadata, archive safety, or reproducibility and requires a later governed maintenance change.
- Hosted pull-request CI run `31942798447` passed the released-governor, candidate-source, and candidate-package jobs after the PR body was corrected to declare the standalone `Harness-Work-Order: WO-RLS-006` field. This metadata-only repair did not change the candidate commit or the ready record committed at `eca66ea7170f5ae1084823046cd7392d3d728d3e`.

This record is `verified` by the accountable human decision above. That decision does not prepare or authorize a release record, merge the pull request, create a tag, publish to GitHub or PyPI, deploy, promote the governor, force-push, or rewrite history.
