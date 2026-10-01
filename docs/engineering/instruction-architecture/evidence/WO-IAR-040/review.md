# Symlink assertion correction: verification review

The only executable change replaces `ValueError` with `installer.HarnessError`
in the existing linked-parent refusal assertion. The refusal text, no-write
assertions and host-capability skip remain unchanged. No installer behavior,
runtime code, packaged resources or host adapter changed.

## Evidence

Tested implementation commit: `7f86e37d00e9b5bc508564655e2594ffe5d9fc67`.

- Linux Python 3.12.3: the exact real-symlink test passed without a skip.
- Linux: all 11 MinimalInstallationTests passed without a skip.
- Linux full suite: 1,211 tests, no failures/errors, four skips, four workers,
  full scale. The restored Git tree and commit exactly match the tested source.
- Windows Python 3.14.6: 26 installer tests, no failures/errors, one skip because
  the host cannot create the required symlink.

The four Linux skips are the real-wheel acceptance fixture, Windows namespace
aliases and two historical-lock checks unavailable in the shallow test export.
The latter two did run in original CI. The original GitHub run used Python
3.11.16; the corrected PR must still pass its CI.

The original CI failure is retained in results.json with the actual synthetic
merge commit, run and downloaded artifact identity. Its raw artifact expires
on 2026-10-15T18:02:11Z. Local raw logs and digests remain outside the repository.
The initial full Linux run lacked Git metadata and failed repository-context
tests. A subsequent tree check caught an extra generated cache. Those attempts
remain recorded; the successful retry changed no product or test source.

## Assessment and limits

REQ-IAR-031 / SPEC-IAR-016 / VER-IAR-022 refusal coverage is preserved. The
existing refusal now satisfies its expected exception assertion. Previous
installed-wheel, migration and native results remain applicable to unchanged
production inputs; their evidence bytes are unchanged. VREC-IAR-020 remains
the historical verified aggregate record.

Codex Windows desktop remains unverified. This correction supplies no desktop
evidence or waiver. VREC-IAR-022 will bind this correction's exact candidate;
human verification remains a separate decision. Merge and release remain separate.
