```toml
artifact = "WO-RLO-009"
checkpoint = "handoff"
formal_snapshot_sha256 = "5bd606f1f0eac95155ebf34a03d46ec73016cb798cf0fab932d1360b3c0c093f"
rebound_at = "2026-09-11T15:56:34Z"
```

# WO-RLO-009 handoff evidence

## Implemented repair

Implementation commit: `9ac7e00458afc81d2161a94b7d2fda7fb23362f9`.
One publication path predicate applies the validator's existing exclusions
before parsing. The catalog, release search, first-parent history and checkout
rehearsal selector use it. Explicit evidence reads and true-duplicate errors
remain intact. No portable validator, CI definition or historical record changed.

Approved extension commit: `cda9474c71a9f14b51d16a3f22ab6ecabff12e89`.
The named allocation test renames its disposable `.git` directory instead of
deleting read-only Git objects. Its unused local import is removed. A complete
file comparison confirms every assertion and all other tests are unchanged.
The [approval receipt](extension-approval.json) binds this correction and DISC08
to the operator's accepted proposal.

## Retained results

[local-results.json](local-results.json), SHA-256
`6f88e824906e9919b2cf9b3558afc01b080ead50ee594d05826ab004fd07c185`,
contains 39 command observations, the replay scripts, and a Git-tree preservation
comparison. It retains failed attempts as well as successful results.

[extension-results.json](extension-results.json), SHA-256
`438bb8918e9dfdbd27dfa3d74784d035dc397f0a02b2d95b62583910ecd83e00`,
retains the correction, both successful full suites, scope and governing checks,
preservation comparison, archive count, and all 17 successful hosted checks at
the preceding evidence head `a53f5663bb812aa0c91d9f01ad2d104311d20fc9`.

| Verification | Observed result |
| --- | --- |
| DISC01–DISC04, DISC06 | 94 focused tests pass on Windows CPython 3.14 and Linux CPython 3.12.3, including eight new regression tests. |
| DISC05 | Original resolution fails with the exact VREC-EVD-001 duplicate on both platforms. Repaired catalogs contain 1,538 artifacts and match canonical discovery. Repeated full resolution returns the independently checked RLS-SEH-026 identities on both platforms. |
| Release identity | Candidate `a9f4905dbd3ff7f0c00101906b9158d3d42f7ef6`; governance `e855cc9a7f97e3c38d654f5e5bf4c3d1590ca17b`; unchanged VREC-SEH-026 and distribution bindings. |
| Full Linux suite / DISC08 | 1,142 tests, four skips, pass at cda9474c. The isolated allocation case also passes. Earlier attempts, including the disposable clone's origin-metadata correction, remain retained. |
| Full Windows suite / DISC08 | 1,142 tests, 23 skips, pass at cda9474c. The isolated corrected case passes. The earlier read-only-object failure and its unchanged-baseline reproduction remain in the original bundle. No new skips or accepted failures. |
| Governing evaluator | Isolated released 0.17.0 doctor, graph validation, review preflight and Git-derived scope checks pass. |
| Candidate source doctor | Six distribution-template differences against the installed 0.17.0 managed root, the expected source/released boundary described by AGENTS.md; root managed files are unchanged. |
| Repository release validation | 14 distribution-bearing records pass. CLI help succeeds. |
| DISC07 preservation | Every engineering path present at the incident baseline retains its blob and mode. The reviewed evidence head 9c251f8e contains 9,993 archive entries against the unchanged 10,000 limit. All 17 hosted checks pass for that head and merge checkout ebb0905a. |

## Remaining work and authority

All 17 hosted checks pass at reviewed head
`9c251f8e2b9e513b7b15f7945a33cc5c088dd7b5`, including the release-record
rehearsal, both upgrade rehearsals and managed validation. The hosted merge
checkout is `ebb0905ae743a62f50b6ceefd055e608f8b9592c`, whose parents are
incident main `fb6f60d5069706e8ae0ca69d1263285cbb904f45` and the reviewed head.
Earlier failures remain retained. The managed gate's PR-description CRLF
refusal was corrected by writing LF input; its rerun passed. The final-head
observations and completion decision are retained in
[completion-results.json](completion-results.json).

The [scope extension proposal](scope-extension-proposal.md) is retained unchanged
as reviewed; its approval is recorded separately. Its fixture-only correction
and DISC08 checks are now complete. No failed required check is waived.
The operator stated "Mark WO-RLO-009 implemented" on 2026-09-11. The released
evaluator applied that completion decision after a passing transition preview.
WO-RLO-009 is `implemented`; VREC-RLO-009 is not prepared.
Preparation, assurance and merge require their separate decisions.
