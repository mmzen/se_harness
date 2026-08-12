+++
id = "VER-SHB-001"
type = "verification"
title = "Verify self-hosting identity and assurance separation"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
verifies = ["REQ-SHB-001", "REQ-SHB-002", "REQ-SHB-003", "REQ-SHB-004", "REQ-SHB-005", "REQ-SHB-006"]
+++

# Verification Contract: Verify self-hosting identity and assurance separation

## Independence

Verification derives expected identities and state ownership from the approved three-plane contract. It must not use candidate success to prove governor independence, or use source execution to prove packaged acceptance.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
| --- | --- | --- |
| `REQ-SHB-001` | exact-wheel acquisition and isolated governor fixtures | Version, URL, filename, digest, module path, and external governor target identify one released governor; acquisition and identity failures stop. |
| `REQ-SHB-002` | source and installed-wheel boundary tests | Source resolves only from checkout; wheel resolves only from the candidate environment; both operate only on permitted targets and make no authority claim. |
| `REQ-SHB-003` | adversarial import/path matrix | CWD, `PYTHONPATH`, user-site, entry-point, subprocess, symlink/case, and equal-version substitutions are detected deterministically. |
| `REQ-SHB-004` | workflow structure and end-to-end CI simulation | Three required lanes have distinct environments, commands, targets, summaries, and dependencies; none substitutes for another. |
| `REQ-SHB-005` | published-artifact promotion fixture | Host remains on N-1 until a separate exact-hash transactional upgrade adopts published N with rollback provenance. |
| `REQ-SHB-006` | provenance and release recovery cases | Changed candidate cannot reuse old VREC/RLS for promotion; the failed attempt remains auditable on its closed PR, is absent from the recovery tree, and replacement records bind the new commit. |

## Critical regression

Reproduce pull request #28 behavior with a released N-1 governor and candidate N managed content. Prove:

- N-1 `doctor` against candidate N fails and is never used as the independent gate;
- N-1 `doctor` against an N-1-created temporary repository passes;
- the baseline compatibility process imports N-1 installed code even when the checkout contains N;
- candidate-source and candidate-package lanes still exercise N fully;
- candidate lane execution cannot be relabeled as governor evidence.

## Identity and path properties

- Resolve paths before containment and compare components, not string prefixes.
- Reject checkout modules in governor/package roles and installed modules in source role.
- Reject unexpected user-site packages, editable metadata, inherited `PYTHONPATH`, ambiguous case, and symlink escape.
- Validate both console entry points and `python -m se_harness` resolution.
- Assert identity JSON is deterministic, bounded, and credential-free.
- Reordering environment or artifact inputs does not change the decision.

## State and mutation properties

- Snapshot the checkout before and after governor and candidate-package lanes; no tracked or untracked repository write is permitted.
- Candidate-source derived outputs are restricted to declared ignored paths.
- Governor-target lock verifies against governor files; normal checkout files and fresh candidate targets verify against the candidate distribution, with only two explicit repository-specific controls excepted.
- Customized governor-upgrade target content blocks promotion transactionally.
- No test silently rewrites formal artifacts, historical VRECs, or release records.

## CI and package checks

- Parse workflow structure and assert the exact pinned governor hash is verified before install.
- Run Linux-oriented shell behavior through deterministic unit fixtures and GitHub Actions after review.
- Execute complete tests on Python 3.11 and the local supported runtime.
- Build two exact-candidate wheels and raw sdists; normalize and compare eligible artifacts.
- Inspect archive safety, metadata, RECORD, source completeness, and epoch.
- Install the exact wheel offline into a fresh Python 3.11 environment and exercise init, adopt/upgrade, doctor, validation, preflight-capable content, and Explorer.

## Governance checks

- Confirm implementation creates a new candidate after `9ba0cec3710167ad4568931747ed5f4e48a63532`.
- Confirm closed PR #28 remains the audit location for `VREC-SEH-003` and `RLS-SEH-003`, while both files are absent from the clean recovery candidate.
- Confirm no tag, publication, or deployment uses those records for the changed payload.
- Require later replacement VREC and release decision before promotion.

## Manual assessments

- Challenge whether any candidate-controlled executable is still presented as independent evidence.
- Confirm the two-file repository-specific parity exception is limited to developing the harness and does not create consumer profiles.
- Confirm bootstrap compatibility claims do not imply that an old governor understands new semantics.
- Review one-time migration and future post-release governor-promotion procedure.

## Evidence retention

Retain exact commands, versions, executable and module origins, wheel hashes, path matrices, mutation snapshots, workflow structure, lane outcomes, package hashes, compatibility limits, changed paths, deviations, and residual risks under `WO-SHB-001`.

## Stop conditions

Stop on ambiguous identity, cross-role import, checkout mutation by an isolated lane, required-lane skip, old-record mutation, package/source disagreement, failed exact-hash acquisition, hidden compatibility failure, or any claim that automation approved verification or release.
