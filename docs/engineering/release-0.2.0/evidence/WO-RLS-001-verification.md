# Verification Evidence: WO-RLS-001

## Result

Local implementation and release-candidate qualification passed on 2026-08-11. The deterministic sdist correction produces byte-identical release archives from independent raw builds while preserving every member payload and mode. The wheel remains byte-identical to the pre-correction build because package runtime and installed-template contents did not change.

This evidence supports `WO-RLS-001` at status `implemented` and covers its deterministic source-distribution tooling as the tenth release-bearing item. It does not yet identify or approve a candidate commit: this evidence and its implementation must first be committed together, after which `VREC-SEH-001` can be captured as a separate `ready` governance record. No verification transition, release transition, tag, push, or publication occurred during qualification.

## Execution context

- Branch: `release/0.2.0`.
- Qualification base commit: `b01d5ee0e16147c460288491b2ce7662d9d9db2e`.
- Base commit timestamp and normalization epoch: `1786451057` (`2026-08-11T14:24:17+02:00`).
- Supported-runtime path: Python `3.11.9`.
- Local release builder: Python `3.14.6`, `build 1.5.0`, `setuptools 84.0.0`, zlib runtime `1.3.1.zlib-ng`.
- Cross-runtime observation: Python `3.11.9` uses zlib runtime `1.3.1`.
- Release version and planned immutable tag: `0.2.0`, `v0.2.0`.
- Publication scope: GitHub release only; PyPI remains out of scope.

The epoch above qualifies the uncommitted candidate contents. Final release assets must be rebuilt from the committed candidate with that candidate commit's Unix timestamp before `SHA256SUMS` is finalized.

## Requirement and contract coverage

| Contract | Evidence | Result |
|---|---|---|
| `REQ-AGR-002` | `REL-DST-001` and the release packet enumerate the exact ten-work-order payload and planned aggregate release record | PASS |
| `REQ-AGR-003` | the packet requires one clean final candidate and defers VREC/RLS capture until that commit exists | PASS |
| `REQ-AGR-005` | artifact validation accepts the expanded gate set and exact payload with zero errors or warnings | PASS |
| `REQ-AGR-007` | implementation created no approval, lifecycle transition, commit, tag, push, or publication | PASS |
| `REQ-DST-006` | versioned universal wheel metadata, complete standard template, source distribution, offline install, and initialized-target checks | PASS |
| `VER-AGR-001` | graph, aggregate-scope, exact-commit boundary, regression suite, dashboard, and authority review | PASS for implementation; VREC decision pending |
| `VER-DST-001` | package metadata, full template, complete tests, doctor, offline wheel install, validation, and dashboard | PASS |
| `REL-DST-001` | reproducible wheel and normalized sdist, Python 3.11 compatibility, content inspection, and retained hashes | PASS for candidate qualification; promotion gates pending |

## Implemented correction

- `scripts/normalize_sdist.py` reads one raw `.tar.gz`, validates all members before output, sorts paths, and normalizes tar ownership, timestamps, extended metadata, device fields, and the gzip header to an explicit epoch.
- Regular-file bytes and member modes are preserved. Directory and regular-file members are the only accepted types.
- Absolute, escaping, non-canonical, Windows-drive, backslash, duplicate, symlink, hard-link, device, FIFO, and other special members fail closed.
- Output is written to a same-directory temporary file and published through a non-overwriting hard link; failures leave no partial destination.
- `MANIFEST.in` includes the release helper in the source distribution.
- `tests/test_release_build.py` covers independent metadata and ordering variance, payload preservation, normalized metadata, unsafe and duplicate paths, symlink rejection, atomic failure, and non-overwrite.
- Repository context and the release packet document the approved two-stage raw-build and normalization procedure.

## Commands and results

### Artifact validation

```powershell
py -3.11 scripts\validate_engineering_artifacts.py --root .
.venv\Scripts\python.exe scripts\validate_engineering_artifacts.py --root .
```

Both runs passed with `105` artifacts, `0` errors, and `0` warnings.

### Full regression matrix

```powershell
py -3.11 -m unittest discover -s tests -p 'test_*.py'
.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_*.py'
```

Both runtimes passed `54` tests with `2` expected Windows privilege-dependent symlink skips:

- `test_symlinked_destination_directory_is_rejected_when_supported`;
- `test_symlinked_evidence_is_blocking_when_supported`.

The new focused module ran three tests successfully on both Python 3.11 and Python 3.14.

### CLI, source doctor, and dashboard

```powershell
py -3.11 -m se_harness --help
.venv\Scripts\python.exe -m se_harness doctor .
.venv\Scripts\python.exe -m se_harness dashboard .
```

- CLI help passed and exposed the versioned `harnessctl` command set.
- Doctor passed Python, configuration, lock, required-file, Claude adapter, and every managed-file check.
- Dashboard generation passed with `105` artifacts, `359` relations, `0` errors, `8` derived warnings, and final retained-state snapshot `f2862cf5d0acec3455388909ed342ee1eea70c24c6e777a3294da7d3aafebb37`.
- The eight non-blocking warnings are seven `W-REV-001` findings for verified work awaiting commit-bound aggregate coverage (`WO-DOC-001`, `WO-DOC-002`, `WO-DST-001`, and governance-only `WO-REV-002..005`) plus one `W-REV-004` stale-ready review for `VREC-AGR-001`, whose work is fully covered by `VREC-PMI-001`. The planned aggregate VREC resolves release-bearing coverage without inferring governance authority.

### Independent raw builds

The following command was run twice into distinct empty output directories with `SOURCE_DATE_EPOCH=1786451057`:

```powershell
.venv\Scripts\python.exe -m build --wheel --sdist --no-isolation --outdir <raw-output> .
```

| Artifact | Build A SHA-256 | Build B SHA-256 | Result |
|---|---|---|---|
| `se_harness-0.2.0-py3-none-any.whl` | `4138500f1dad283cabfdca1a75d69de11ba735341cbb3609743b57ca4a5e9f70` | `4138500f1dad283cabfdca1a75d69de11ba735341cbb3609743b57ca4a5e9f70` | byte-identical |
| raw `se_harness-0.2.0.tar.gz` | `ed23910b74583c5869ca83091dfca58dac8a6d4b13541ac17c80e597db66c0db` | `5155a93c0aeec0bab183523a60580a11f798e87c8d4dd995f29a3c0f9be7d3e2` | expected producer-metadata difference |

Inspection confirmed that the two raw sdists had identical member paths, types, modes, sizes, and file bytes. Their byte difference was confined to setuptools-generated archive timestamps and gzip compression.

### Deterministic normalization

```powershell
.venv\Scripts\python.exe scripts\normalize_sdist.py `
  <raw-output>/se_harness-0.2.0.tar.gz `
  <normalized-output>/se_harness-0.2.0.tar.gz `
  --epoch 1786451057
```

Both independent raw builds produced the same normalized SHA-256:

`0104353053153b33959b24e875c3b36863fa454e2c2b5139aca8b55e6b964bc7`

Detailed inspection passed:

- `66` unique sorted members;
- only regular files and directories;
- all member mtimes `1786451057`;
- UID and GID `0`, empty user and group names;
- deterministic PAX `path` metadata only for the three long paths that require it;
- deterministic gzip header with no embedded filename and mtime `1786451057`;
- raw A, raw B, normalized A, and normalized B have identical payload-and-mode manifests;
- `MANIFEST.in`, `scripts/normalize_sdist.py`, and `tests/test_release_build.py` are present and byte-identical to source.

### Normalized-sdist consumption

```powershell
.venv\Scripts\python.exe -m pip wheel `
  <normalized-output>/se_harness-0.2.0.tar.gz `
  --no-index --no-deps --no-build-isolation --wheel-dir <wheel-output>
```

The normalized sdist built offline successfully and reproduced the direct wheel exactly:

`4138500f1dad283cabfdca1a75d69de11ba735341cbb3609743b57ca4a5e9f70`

### Wheel inspection and fresh Python 3.11 installation

The wheel contains `42` entries. All six `se_harness` Python modules and all thirty canonical template payload files matched source byte-for-byte. ZIP CRC and RECORD hash/size verification passed. Metadata checks passed:

- `Version: 0.2.0`;
- `Requires-Python: >=3.11`;
- `harnessctl = se_harness.cli:main`;
- `Root-Is-Purelib: true`;
- `Tag: py3-none-any`.

The wheel was installed offline with `--no-index --no-deps` into a fresh Python `3.11.9` virtual environment. `harnessctl --version` returned `0.2.0`; `init` installed the complete 30-file standard harness into a new repository; doctor passed all checks; artifact validation passed with no findings; dashboard generation passed.

### Git hygiene

```powershell
git diff --check
```

Result: PASS. Git reported only the configured Windows LF-to-CRLF checkout notices for modified Markdown files; there were no whitespace errors, conflict markers, generated release assets, commits, tags, pushes, or remote mutations.

## Deviations and residual risks

1. Raw setuptools sdists remain byte-variable. They are explicitly intermediate inputs and must never be published; only the normalized output is a release artifact.
2. Python `3.11.9` with zlib `1.3.1` and Python `3.14.6` with zlib-ng `1.3.1.zlib-ng` produced identical uncompressed normalized tar streams but different gzip bytes (`9a26daab...` versus `01043530...`). Therefore the recorded release-builder runtime and compression implementation are part of the reproducibility environment. The 0.2.0 final build must use the qualified Python `3.14.6`/zlib-ng toolchain.
3. The helper deliberately preserves member modes. Reproducibility therefore requires the same Git source modes; both independent builds matched.
4. Two Windows symlink tests were skipped because the host account lacks symlink privileges. Their fail-closed branches remain exercised on hosts that can create symlinks, and the new normalizer's symlink-member rejection executed without OS symlink privileges.
5. Qualification hashes use the pre-candidate base epoch and are not final publication checksums. After the candidate commit is created, the release artifacts and `SHA256SUMS` must be reproduced using that candidate's timestamp and retained under the later release phase.
6. The eight dashboard warnings are derived review signals, not validator errors or approvals. They remain visible until the planned aggregate provenance and any separately authorized supersession decisions are recorded.

## Conclusion

The deterministic sdist fix and ten-work-order release packet are locally qualified and ready for the authorized candidate commit. The next phase is to commit this implementation and evidence together, then capture `VREC-SEH-001` against that exact clean candidate in a later governance commit. Quality verification, release transition, immutable tagging, and GitHub publication remain separate human-controlled gates.
