# WO-PUB-003 Governance Publication Preflight

Preflight recorded on 2026-08-11.

- Candidate branch and commit: `main` at `968c225eb16d887c5be5a297e12482cd2b1fde5f` after merging pull request #1.
- Ready record: `VREC-DST-003`, bound to the same full SHA-1 candidate with clean worktree state and evidence for `WO-DST-003` under `VER-DST-002`.
- Capture result: ready record created without commit, tag, verification transition, release, or publication.
- Pre-capture checks on the candidate: artifact graph passed with 46 artifacts and zero diagnostics; all 29 tests passed with two conditional Windows symlink-privilege skips; CLI help and installed-harness doctor passed.
- Post-capture graph: 47 artifacts, zero errors, and zero warnings.
- Planned branch: `governance/vrec-dst-003` targeting `main` through a pull request.
- Publication mode: normal new-branch commit and push; no force, verification transition, release, tag, merge, package publication, or deployment.

The governance commit and pull request retain the ready record for accountable assurance review; they do not grant verification authority.
