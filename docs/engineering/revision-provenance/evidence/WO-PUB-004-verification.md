# WO-PUB-004 Verification-Decision Publication Preflight

Preflight recorded on 2026-08-11.

- Base governance merge: `main` at `17b6ab73abb305f2f9ca59a085558e8e63b01fd4`.
- Branch: `governance/verify-vrec-dst-003`.
- Decision: the accountable owner explicitly authorized `VREC-DST-003` to transition from `ready` to `verified` under `WO-REV-003`.
- Candidate binding: unchanged at `968c225eb16d887c5be5a297e12482cd2b1fde5f`; the commit is available locally and remains an ancestor of the governance checkout.
- Decision checks: artifact graph passed with 49 artifacts and zero diagnostics; all 29 tests passed with two conditional Windows symlink-privilege skips; CLI help and installed-harness doctor passed.
- GitHub CLI: version 2.97.0 installed at `C:\Program Files\GitHub CLI\gh.exe`; the existing Git credential will be supplied through a process-scoped environment variable and will not be printed or persisted by this workflow.
- Publication mode: normal commit, new-branch push, and pull request against `main`; no force, merge, release, tag, package publication, or deployment.

The publication preserves the verified candidate lineage and does not grant release authority.
