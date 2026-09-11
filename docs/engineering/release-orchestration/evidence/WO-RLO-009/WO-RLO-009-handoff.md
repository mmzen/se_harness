```toml
artifact = "WO-RLO-009"
checkpoint = "handoff"
formal_snapshot_sha256 = "f4ff72a64c06d3664e15b298f910f138ac2efece58e89a3b71ff6ebf65569a07"
rebound_at = "2026-09-11T13:11:43Z"
```

# WO-RLO-009 handoff evidence

## Implemented repair

Implementation commit: `9ac7e00458afc81d2161a94b7d2fda7fb23362f9`.
One publication path predicate applies the validator's existing exclusions
before parsing. The catalog, release search, first-parent history and checkout
rehearsal selector use it. Explicit evidence reads and true-duplicate errors
remain intact. No portable validator, CI definition or historical record changed.

## Retained results

[local-results.json](local-results.json), SHA-256
`6f88e824906e9919b2cf9b3558afc01b080ead50ee594d05826ab004fd07c185`,
contains 39 command observations, the replay scripts, and a Git-tree preservation
comparison. It retains failed attempts as well as successful results.

| Verification | Observed result |
| --- | --- |
| DISC01–DISC04, DISC06 | 94 focused tests pass on Windows CPython 3.14 and Linux CPython 3.12.3, including eight new regression tests. |
| DISC05 | Original resolution fails with the exact VREC-EVD-001 duplicate on both platforms. Repaired catalogs contain 1,538 artifacts and match canonical discovery. Repeated full resolution returns the independently checked RLS-SEH-026 identities on both platforms. |
| Release identity | Candidate `a9f4905dbd3ff7f0c00101906b9158d3d42f7ef6`; governance `e855cc9a7f97e3c38d654f5e5bf4c3d1590ca17b`; unchanged VREC-SEH-026 and distribution bindings. |
| Full Linux suite | 1,142 tests, four skips, pass. The disposable clone first needed its real repository origin metadata for an existing dashboard test. Both attempts are retained. |
| Full Windows suite | 1,142 tests, 23 skips, one error in an existing allocation test's deletion of a read-only Git object. The isolated case fails identically on unchanged pre-repair e78d257a. This is an unresolved test portability defect, not a pass. |
| Governing evaluator | Isolated released 0.17.0 doctor, graph validation, review preflight and Git-derived scope checks pass. |
| Candidate source doctor | Six distribution-template differences against the installed 0.17.0 managed root, the expected source/released boundary described by AGENTS.md; root managed files are unchanged. |
| Repository release validation | 14 distribution-bearing records pass. CLI help succeeds. |
| DISC07 preservation | Every pre-existing engineering path retains its blob and mode. The implementation archive contains 9,987 entries against the unchanged 10,000 limit. Final-head archive and CI observations remain to be retained. |

## Remaining work and authority

The hosted release-record rehearsal passes for the repair. The first managed
check refused the missing handoff packet, which this file now supplies. The
first Linux upgrade job failed during temporary-directory cleanup with
`Errno 39`; its raw log is retained. New-head hosted results remain pending.

The [scope extension proposal](scope-extension-proposal.md) names a minimal
fixture-only correction for the Windows failure. It is pending approval;
the affected test and approved scope remain unchanged. No failed required
check is waived. WO-RLO-009 remains `in_progress`; VREC-RLO-009 is not prepared.
Completion, preparation, assurance and merge require their separate decisions.
