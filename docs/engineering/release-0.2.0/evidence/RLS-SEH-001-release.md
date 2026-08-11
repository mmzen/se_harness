# Release Evidence for RLS-SEH-001

Date: 2026-08-11

## Accountable release decision

The repository and release owner explicitly instructed `make the release` after `VREC-SEH-001` was merged in status `verified`. This is the human release decision required by `WO-RLS-001` and `REL-DST-001`. It authorizes the bounded `RLS-SEH-001` transition, immutable candidate tag `v0.2.0`, and GitHub release publication. Automation only records and executes that decision.

## Released lineage

- Version: `0.2.0`.
- Immutable tag: `v0.2.0`.
- Candidate commit: `1329c7a4472f323c4b21d869545cad3c647fe568`.
- Candidate commit timestamp and final build epoch: `1786454202` (`2026-08-11T15:16:42+02:00`).
- Aggregate verification: `VREC-SEH-001`, status `verified`.
- Verification-governance merge: `afdcf99fa3e65fe1946de5f4128102b6dc934ddb`.
- Ready release-record governance commit: `7df4e7ec9bd114d662051d0347d721659e0fd337`.
- Release contract: `REL-DST-001`.
- Released work: `WO-AGR-001`, `WO-DOC-001`, `WO-DOC-002`, `WO-DST-001`, `WO-DST-002`, `WO-DST-003`, `WO-PMI-001`, `WO-REV-001`, `WO-RLS-001`, and `WO-VSP-001`.
- Publication target: GitHub repository `mmzen/se_harness`; PyPI remains out of scope.

The candidate is locally available and is an ancestor of the governance checkout. The release record, verified VREC, artifact source, version, and planned tag all identify the same candidate commit.

## Final artifact production

The exact candidate tree was exported twice with `git archive` into independent source directories. Both builds used:

- Python `3.14.6`;
- `build 1.5.0`;
- `setuptools 84.0.0`;
- zlib runtime `1.3.1.zlib-ng`;
- `SOURCE_DATE_EPOCH=1786454202`;
- no build isolation and no network dependency resolution.

The raw build command was run once in each independent export:

```powershell
.\.venv\Scripts\python.exe -m build `
  --wheel --sdist --no-isolation `
  --outdir <raw-output> <candidate-export>
```

Raw hashes:

| Artifact | Build A SHA-256 | Build B SHA-256 | Result |
|---|---|---|---|
| wheel | `56db717e5287492c421e11157545586b1e8f0ec2dd4011a9932ccf35f233d63d` | `56db717e5287492c421e11157545586b1e8f0ec2dd4011a9932ccf35f233d63d` | byte-identical |
| raw sdist | `a2d9409d349e6b18f7948890c48a3092aec5c8930a7601162625cb57aec7dd2e` | `e6b7ab7894fc137e969a5b82d7fa8b236807746f9537c636394bde525dbdce0f` | expected producer-metadata difference |

Each raw sdist was normalized independently with the candidate epoch:

```powershell
python scripts\normalize_sdist.py `
  <raw-output>\se_harness-0.2.0.tar.gz `
  <normalized-output>\se_harness-0.2.0.tar.gz `
  --epoch 1786454202
```

Both normalized sdists are byte-identical.

## Published asset manifest

| Asset | Size | SHA-256 |
|---|---:|---|
| `se_harness-0.2.0-py3-none-any.whl` | 82,377 bytes | `56db717e5287492c421e11157545586b1e8f0ec2dd4011a9932ccf35f233d63d` |
| `se_harness-0.2.0.tar.gz` | 82,773 bytes | `7c94cc0f4998b045b2766c60bc03a887bfdc53ae87f3494bb702e1d947bf873d` |
| `SHA256SUMS` | 190 bytes | manifest containing the two hashes above |

The GitHub release also provides host-generated source archives for immutable tag `v0.2.0`.

## Content and consumption checks

- Raw A, raw B, normalized A, and normalized B contain identical paths, member types, modes, and regular-file bytes.
- The normalized sdist contains `66` unique sorted members, fixed epoch `1786454202`, zero UID/GID, empty user/group names, and deterministic PAX path metadata for three long paths.
- `MANIFEST.in`, `scripts/normalize_sdist.py`, and `tests/test_release_build.py` are present and source-identical in the sdist.
- The wheel contains `42` entries; all `36` source and canonical-template payload files match the candidate export byte-for-byte.
- Wheel CRC, RECORD hashes and sizes, version `0.2.0`, `Requires-Python: >=3.11`, `harnessctl` entry point, purelib declaration, and `py3-none-any` tag all pass.
- An offline wheel build from the normalized sdist reproduced the direct wheel exactly at SHA-256 `56db717e5287492c421e11157545586b1e8f0ec2dd4011a9932ccf35f233d63d`.
- The final wheel installed offline with `--no-index --no-deps` into a fresh Python `3.11.9` virtual environment. `harnessctl --version` returned `0.2.0`; init installed all 30 standard harness files; doctor, validation, and dashboard generation passed.

## Repository and CI gates

```powershell
py -3.11 -m unittest discover -s tests -p "test_*.py"
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
.\.venv\Scripts\python.exe scripts\validate_engineering_artifacts.py --root .
.\.venv\Scripts\python.exe -m se_harness doctor .
.\.venv\Scripts\python.exe -m se_harness dashboard .
git diff --check
```

Final local result: PASS. Python `3.11.9` and Python `3.14.6` each passed all `54` tests with the same `2` conditional Windows symlink skips. Artifact validation passed with `108` artifacts, `0` errors, and `0` warnings. Doctor passed every required and managed-file check. Dashboard generation passed with `108` artifacts, `395` relations, `0` errors, `6` review-only warnings, and snapshot `d34205d4848e6c2c71e811da743616f1c349624e81c0707f65510f96b39d648b`. Diff hygiene passed.

Merged verification-governance CI run `31496171779` completed successfully for commit `02d530212f7ef63780b96ba023a4bb996de9a86b` before release preparation.

## Promotion and publication controls

- The ready release record was retained before this released transition.
- Before tagging, verify again that neither `refs/tags/v0.2.0` nor GitHub release `v0.2.0` exists.
- Merge the released record and evidence to `main` before tag creation.
- Create the annotated tag on candidate `1329c7a4472f323c4b21d869545cad3c647fe568`, never on a governance commit.
- Upload only the verified wheel, normalized sdist, and `SHA256SUMS` from the final assets directory.
- Verify the published tag target, release state, asset names, sizes, and downloaded SHA-256 values after publication.

## Deviations and residual risks

- Raw setuptools sdists remain nondeterministic intermediates and must never be published.
- Byte-identical gzip output is qualified against the recorded Python 3.14.6/zlib-ng release toolchain; other compression implementations may produce equivalent but byte-different archives.
- Two Windows symlink tests are conditionally skipped when the host lacks symlink privileges. No symlink behavior changed in this release phase, and archive symlink rejection remains executable without that privilege.
- GitHub-generated source archives are produced by the host and are distinct from the verified normalized sdist asset.

## Authority boundary

This decision authorizes `RLS-SEH-001` release transition, immutable tag `v0.2.0`, and GitHub release publication of the three verified assets. It does not authorize PyPI or another package index, deployment, force push, tag movement, history rewriting, or replacement of a published artifact. Any correction requires a separately verified new version.
