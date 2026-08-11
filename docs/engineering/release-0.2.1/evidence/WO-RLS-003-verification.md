# Verification and Release Decision Evidence for WO-RLS-003

Date: 2026-08-11

## Accountable decision

After merging pull request #18, the repository owner instructed `i merged, you can perform the next steps`. The referenced steps explicitly included aggregate verification, release preparation and approval, immutable GitHub release publication, protected PyPI deployment, and final verification. This is the accountable assurance and release-owner decision; automation remains bounded to the exact identities and stop conditions in `WO-RLS-003`.

## Reviewed lineage

- Pull request #18 merge and governance base: `c3e0e417cfa422f3cab732d863e16a552675629e`.
- Exact release candidate: `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5`.
- Candidate timestamp and build epoch: `1786466022`.
- Ready aggregate-record commit: `afa3fcb05626bbb121647cf7a5a1597cee269ee6`.
- Aggregate verification record: `VREC-SEH-002`.
- Ready record SHA-256 before transition: `4d67bfb5f1db9f37bca640bdc8a54dac3c17ffd85a78619fcb026b15f2108472`.
- Captured artifact snapshot: `e5f05628548a70d50f7d91931e30f04ddd9d9aa01028d9abad81929e10cd9653`.
- Release-candidate evidence SHA-256: `e369b870ca0f36abc7f86808a01f544e3c9cbc00791803c8086c59efa792756a`.
- Release contract: `REL-SEH-002`.
- Exact released-work set: `WO-IAR-001`, `WO-PYP-001`, `WO-RLS-002`, and `WO-WLC-001`.

Candidate and ready-record commits are locally available ancestors of the governance checkout. The merge and later governance commits do not replace the candidate identity.

## Aggregate verification transition

The four retained evidence paths, five verification contracts, four work-order relations, candidate commit, Git object format, clean capture state, capture timestamp, and artifact snapshot were reviewed. `VREC-SEH-002` changed only from `ready` to `verified`, plus the human-decision note referencing this work order. No captured provenance field changed.

## Final artifact production

The exact candidate tree was exported twice with `git archive` into independent source directories. Both builds used Python `3.14.6`, `build 1.5.0`, `setuptools 84.0.0`, zlib-ng `1.3.1.zlib-ng`, `SOURCE_DATE_EPOCH=1786466022`, no build isolation, and no network dependency resolution.

| Artifact | Build A SHA-256 | Build B SHA-256 | Result |
|---|---|---|---|
| wheel | `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454` | `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454` | byte-identical |
| raw sdist | `c04dfbb82be20df95dee05649889394134c49733270de326a773749a6e18be06` | `1a309c4e08e86c6eaddf7cff0b03c185893903cb02db6361dd8fb51fbafee210` | expected producer-metadata difference |
| normalized sdist | `770d40cfe9f65970424acb72f9e235365be61e2e8c73dce58274a0f0eca198e4` | `770d40cfe9f65970424acb72f9e235365be61e2e8c73dce58274a0f0eca198e4` | byte-identical |

The normalized sdist rebuilt offline and reproduced the direct wheel exactly. The final asset set is:

| Asset | Size | SHA-256 |
|---|---:|---|
| `se_harness-0.2.1-py3-none-any.whl` | 92,061 | `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454` |
| `se_harness-0.2.1.tar.gz` | 95,569 | `770d40cfe9f65970424acb72f9e235365be61e2e8c73dce58274a0f0eca198e4` |
| `SHA256SUMS` | 190 | `b55951ffad4fda16a612e223e0773467c9cf241c92fb9c1ffe484e26367e65fd` |

`SHA256SUMS` is exactly the two lowercase hashes and filenames above with LF line endings and one final newline.

## Content and consumption checks

- Both raw and normalized sdists contain the same `71` unique path/type/mode/payload entries.
- Normalized members are sorted and use the candidate epoch, UID/GID zero, and empty owner/group names.
- The wheel contains `45` unique entries; its `39` source/template payload files match the candidate export byte-for-byte.
- METADATA reports version 0.2.1 and Python 3.11+; WHEEL reports purelib and `py3-none-any`; the `harnessctl` entry point is correct; every RECORD hash and size verifies.
- The exact wheel installed offline into a fresh Python `3.11.9` environment. `harnessctl --version` returned `0.2.1`; init installed all `32` standard files; doctor and installed formal validation passed; Explorer generated successfully with empty-graph snapshot `7ed0ba7f422e86c82c4a0c455445c7b38e4a2358a3889f5a6a6991a03bc20cfc`.

## Repository checks

Formal graph validation passed with `166` artifacts, `0` errors, and `0` warnings. Start and review preflight passed for this in-progress governance work order. Python `3.14.6` and Python `3.11.9` each passed all `70` tests with the same `2` expected Windows symlink skips. CLI and doctor passed every required and managed-integrity check. Explorer generated `166` artifacts and `582` relations with `0` errors, `1` unrelated historical stale-ready warning, and snapshot `379989d1fbaf9fd7f7b8e08a8b8aac67d4717e350dce1657534c81dc4a685de0`. Candidate/record ancestry, captured-field preservation, and diff hygiene passed.

The governance PR must still independently pass both its immutable 0.2.0 baseline and reviewed 0.2.1 candidate jobs before promotion.

## Release and publication authorization

The owner decision authorizes preparation of `RLS-SEH-002`, its transition to `released` for version 0.2.1 and tag `v0.2.1`, normal governance publication and merge after green checks, an annotated tag on candidate `94e13e3...`, a non-draft/non-prerelease GitHub release containing exactly the three assets above, and protected PyPI workflow dispatch with the two exact distribution hashes.

PyPI publication must use the repository's OIDC Trusted Publisher and `pypi` environment. No package may be rebuilt between GitHub and PyPI. External success, URLs, attestations, downloaded hashes, and exact-version installation are retained only after they actually exist.

## Deviations and residual risks

- Raw setuptools sdists are nondeterministic intermediates and are never publication assets.
- Two Windows symlink tests remain conditionally skipped when the host lacks symlink privileges; no symlink behavior changed.
- GitHub and PyPI are external dependencies. Environment approval may require an owner action, and any incomplete or failed upload must stop and be recorded rather than bypassed.
- Published tags and package files are immutable. Any defect requires a new version, never replacement.
- GitHub currently emits non-blocking Node.js 20 deprecation annotations for pinned action versions; the runner forces Node.js 24. Updating those action pins is a separately governed change.

## Current authority boundary

This evidence supports aggregate verification and release preparation. Until the governance PR is merged, no tag, GitHub release, PyPI workflow dispatch, package upload, or deployment may occur. Final external publication evidence is necessarily retained afterward.
