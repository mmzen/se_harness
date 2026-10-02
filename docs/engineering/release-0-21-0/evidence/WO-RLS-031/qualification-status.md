# Qualification status for the first 0.21.0 review candidate

Candidate: `2b7d318fd00e955edfec0443d5d7158891a41509`.
Draft [PR #517](https://github.com/mmzen/se_harness/pull/517) remains open.
These observations are preparation evidence. WO-RLS-031 remains in progress.

## Observed results

- All executed PR checks passed. The PR-triggered release-record leg was skipped
  because no new record was selected. This does not stand in for the manual leg.
- The exact-head candidate leg of manual run
  [36919403159](https://github.com/mmzen/se_harness/actions/runs/36919403159)
  passed two digest-pinned Linux/amd64 builds. The replay and bundle manifest
  are retained alongside this file.
- Released 0.20.1 independently qualified the non-promotable test wheel on
  Windows and Linux. Installed lifecycle checks passed on both platforms.
- The 41-step adapter assessment passed. Windows and Linux migration checks
  passed, including missing-evidence refusal, customized-file refusal, rollback
  after an injected write failure, owner/history preservation and repeated no-op.
- Native Codex CLI/app-server and Claude Code observations passed startup,
  activation after cloning, manual and automatic compaction, and resume.
  Both hosts recovered the selected resource entry. Disposable repositories
  were preserved. The Codex disposable plugin was restored after the run.
- The Windows full-scale source run passed 1,211 tests with 20 skips, as retained
  in local-checks.json. That source run preceded this commit; it is not the final
  commit-bound capture. Hosted results retain their actual run/commit context.

## Two wheel identities

The pinned build produced wheel SHA-256
`b31cfdb7fb6a6a37290f88534709c60c191d8461e9d9b45dd61cad0c6883d3a6`
and normalized sdist SHA-256
`85ba6a756559d9e512c38968151e46c4a6c7430deab5ec73d96e1d8ac2391efc`.
These are candidate build observations, not a released distribution.

Local/native checks used a separately built, non-promotable qualification wheel:
archive SHA-256
`34806b8037ff24e56aa50831a1da8b0f2680345ca1a797fd3c41df838f03e755`,
payload SHA-256
`c86a3301491e4ef4188ed98e2fcf8c67bf2c8184bc5e73e97e663f235c7894ac`.
Its commands, independent expected identity and actual results are retained.
Do not claim that these two wheel archives are byte-identical.

## Open release criteria

1. The manual RLS-SEH-030 replay failed because the recursive record scanner
   counted its archived evidence copy as another RLS. It reported:
   `expected exactly one release record RLS-SEH-030; found 2`.
   The original log and both input digests are retained. WO-RLO-013 and
   VER-RLO-010 are draft proposals for a two-file repository tooling correction.
   Neither the formal record nor the archived copy has been edited or removed.
2. VER-IAR-021 requires the Codex Windows desktop path. CLI/app-server evidence
   does not satisfy this criterion. It remains unverified; no waiver is recorded.
3. Complete the remaining contract assessment at the final candidate, including
   any justified reuse after exact input comparison. Prepare the aggregate VREC
   only when its required checks pass. Human verification, tagged RLS preparation,
   bound-record replay, the release decision and integration remain separate.

No v0.21.0 publication, marketplace update, release-marker change, adoption,
root instruction deletion or final assurance decision occurred in this work.

## Evidence

`qualification-observations.json` retains original check results and transient
probe drivers. Source-file digests identify the original receipts; JSON framing
uses LF while embedded command output and trace text are preserved as values.
`native-codex-events.json` retains the complete observed app-server event text
and its raw-byte digests. Claude's complete stream output is in the observations.
The synthetic fixture decisions and injected write failure apply only to those
fixtures. They confer no product decision or publication authority.
