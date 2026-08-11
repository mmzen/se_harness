# Verification Evidence for WO-RLS-002

Date: 2026-08-11

## Result

The instruction-architecture assurance transition and the integrated 0.2.1 release-candidate qualification passed. Source and self-hosted managed metadata report version 0.2.1, the exact incremental payload is gated by `REL-SEH-002`, independent builds reproduce one wheel and one normalized source distribution, and an offline Python 3.11 installation passed the installed-harness checks.

This evidence supports `WO-RLS-002` at `implemented`. It does not authorize or report a final release, tag, GitHub release, PyPI workflow dispatch, package upload, or deployment. A later aggregate VREC must identify the committed candidate before release preparation can proceed.

## Accountable decision and reviewed lineage

The repository owner confirmed pull request #17 was merged, reviewed the retained instruction-architecture evidence, and explicitly instructed `i merged, then transition and governance commit + PR`. The owner also selected release `0.2.1` and stated that its promotion includes PyPI deployment. This is the human decision authorizing the bounded VREC transition and candidate work; automation only records and executes the reversible preparation steps.

- Merged base: `main` at pull request #17 merge commit `87b538bef1f7494f0c13860b567572c4271d530c`.
- Instruction-architecture candidate: `9b42d3b564eb107b161458c6d750d05680284618`.
- Ready-record governance commit: `39a7e2582ede1e2526fce33fb845ec3dce1ac53a`.
- Implementation work order and verification contract: `WO-IAR-001` under `VER-IAR-001`.
- Retained implementation evidence SHA-256: `cc26d94b36dcfb5157cd1d166c9a34cd0843d35df4203b6d6454ef47cdaf8b55`.
- Ready `VREC-IAR-001` SHA-256 before transition: `b889b42c373bd890593c9117120abfd2a7a8ed5b0338d35393d8b39fe5ba6f58`.
- Captured artifact snapshot SHA-256: `841db0dab7ad87f2e3f29dc60ca941f363f40757738516d30e34d5c23cadb697`.

The candidate and ready-record commits are locally available ancestors of the release checkout. The merge, release candidate, and later governance records do not replace the implementation commit named by `VREC-IAR-001`.

## Verification transition

`VREC-IAR-001` changed from `ready` to `verified`, with a human-decision note referencing this work order. Its candidate commit, Git object format, captured worktree state, capture timestamp, artifact snapshot, evidence path, work-order relation, and verification-contract relation remain unchanged.

## Release scope and versioning

`REL-SEH-002` gates exactly the release-bearing work introduced since immutable version 0.2.0:

- `WO-PYP-001`: PyPI Trusted Publishing automation;
- `WO-WLC-001`: work-order lifecycle consistency;
- `WO-IAR-001`: instruction architecture and preflight enforcement;
- `WO-RLS-002`: integrated versioning and qualification.

Governance-only decision and publication work orders are intentionally excluded from the released-work set. `pyproject.toml`, `se_harness.__version__`, the repository configuration, managed router, lock, and non-self candidate fallback now consistently render version 0.2.1. The independent external baseline remains immutably pinned to GitHub release 0.2.0 and its retained wheel hash during bootstrap.

## Commands and results

### Formal graph and preflight

```powershell
python scripts\validate_engineering_artifacts.py --root .
python -m se_harness preflight . --work-order WO-RLS-002
```

Result: PASS. Before aggregate VREC capture, the graph contains `164` formal artifacts with `0` errors and `0` warnings. Start preflight passed and returned the complete governing distribution manifest. The initial draft relation set was deliberately narrowed after preflight identified overclaimed aggregate/PyPI architecture coverage; those requirements remain owned by their original release-bearing work orders.

### Supported-runtime regression

```powershell
python -m unittest discover -s tests -p "test_*.py"
C:\Users\mathi\Documents\Codex\2026-08-10\st\v0.2.0-final-smoke-311\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

Result: PASS on Python `3.14.6` and Python `3.11.9`. Each runtime executed `70` tests with `2` expected conditional skips because this Windows host cannot create symbolic links.

### CLI, self-upgrade, and installation integrity

```powershell
python -m se_harness upgrade . --apply
python -m se_harness --version
python -m se_harness doctor .
```

Result: PASS. The transactional upgrade updated only the rendered configuration, managed workflow, managed router, and their schema-2 lock entries. CLI version is `0.2.1`; every required, distribution, fragment, seed, and managed-integrity doctor check passed.

### Harness Explorer

Result: PASS with `164` artifacts, `565` relations, `0` errors, and `1` derived warning. Snapshot SHA-256 is `ea3d95f240fb1793630b6b11d168d5206acc08fa9a847d2ada0a65f2f87095fb`. The sole warning is the unrelated historical stale-ready review for `VREC-AGR-001`; it is non-authoritative and does not affect this payload.

### Independent package builds

The existing isolated release builder used Python `3.14.6`, `build 1.5.0`, `setuptools 84.0.0`, and zlib-ng `1.3.1.zlib-ng`. Two builds used `SOURCE_DATE_EPOCH=1786465228`, the merged-base commit timestamp:

```powershell
python -m build --wheel --sdist --no-isolation --outdir <raw-a> .
python -m build --wheel --sdist --no-isolation --outdir <raw-b> .
python scripts\normalize_sdist.py <raw-sdist> <normalized-sdist> --epoch 1786465228
```

| Artifact | Build A SHA-256 | Build B SHA-256 | Result |
|---|---|---|---|
| wheel | `6af3a5e3cfb709de13a4a2bdcc9f409ed99932ba023658008f1bf2b0a17b2577` | `6af3a5e3cfb709de13a4a2bdcc9f409ed99932ba023658008f1bf2b0a17b2577` | byte-identical |
| raw sdist | `40b9501a02fb1ca9667cbcb8565ef2f12cf4fbf9835582b3a623fd2f014ad6c5` | `727ce77b371f70495b898266363095a04bdc0b2aa9670bca11c6d02aaf2c14df` | expected producer-metadata variance |
| normalized sdist | `3a154c36596cc969befc152995407f2b5066cddbb429e4ac624671267d957777` | `3a154c36596cc969befc152995407f2b5066cddbb429e4ac624671267d957777` | byte-identical |

The normalized sdist rebuilt offline with `--no-index --no-deps --no-build-isolation --no-cache-dir` and reproduced the direct wheel exactly at SHA-256 `6af3a5e3...b2577`.

### Archive and metadata inspection

Result: PASS. The wheel has `45` unique entries and `39` source/template payload files that match the checkout byte-for-byte. METADATA reports version 0.2.1 and Python 3.11+, WHEEL reports purelib and `py3-none-any`, the console entry point is correct, and every RECORD digest and size verifies.

Both raw and normalized sdists have the same `71`-member path/type/mode/payload manifest. The normalized members are unique and sorted; all use epoch `1786465228`, UID/GID zero, and empty owner/group names. Unsafe and special-member failure behavior remains covered by the regression suite.

### Fresh Python 3.11 installation

The qualified wheel was installed offline with `--no-index --no-deps` into a new Python `3.11.9` virtual environment. `harnessctl --version` returned `0.2.1`; `init` installed all `32` standard files into a new repository; doctor passed every check; the installed validator reported `0` diagnostics; and Explorer generation passed with snapshot `677afc5f3462766b2545400e130bb5c507e09cd9bc829533b68a570100bb4b24` for the intentionally empty new artifact graph.

## Deviations and residual risks

- The hashes above qualify the uncommitted candidate content at the merged-base epoch. They are not final publication hashes. After the candidate commit exists, release artifacts must be rebuilt from that exact tree using its commit timestamp and retained in later release evidence before any tag or publication.
- Raw setuptools sdists remain nondeterministic intermediates and must never be published; only the normalized sdist is eligible.
- Two Windows symlink tests are conditionally skipped because this host lacks symlink privileges. No symlink behavior changed, and archive special-member rejection remains tested without that privilege.
- Independent CI deliberately uses immutable 0.2.0 as its external baseline while candidate-source CI verifies 0.2.1. Advancing the external pin requires a later governed update after 0.2.1 exists independently.
- GitHub, PyPI, OIDC publisher configuration, protected-environment approval, and package-index immutability remain external controls. No external release or publication action has occurred.
- A newly initialized repository has no formal work order, so its smoke test validates installation integrity and empty-graph behavior; successful preflight is separately exercised against this repository's complete `WO-RLS-002` chain.

## Authority boundary

This work records the verified IAR decision and prepares a release candidate. It authorizes the candidate and later ready-VREC commits, normal branch push, and pull request. It does not transition `VREC-SEH-002`, prepare or transition `RLS-SEH-002`, merge the pull request, create or move `v0.2.1`, publish a GitHub release, dispatch or approve the PyPI workflow, upload a package, deploy, force push, or rewrite history.
