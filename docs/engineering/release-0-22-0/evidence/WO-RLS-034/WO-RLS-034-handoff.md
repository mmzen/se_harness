```toml
artifact = "WO-RLS-034"
checkpoint = "handoff"
formal_snapshot_sha256 = "49a12e664d571956b156cdc0ec49418aab003ed60d0706ad4bef7683527ead6c"
rebound_at = "2026-10-02T22:18:40Z"
```

# WO-RLS-034 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Release-preparation review

This packet supports the authorized draft review of WO-RLS-034 while it remains
in progress. It does not claim completion or verification of the release.

The approved version and documentation changes are implemented. The initial
Windows and Linux full suites each ran 1,255 tests and found the same README
word-limit failure. Windows skipped 22 tests; Linux skipped 2. The README was
shortened without changing tests; all 22 targeted onboarding/refresh checks pass.
See initial-checks.json for commands, runtimes, retained failure excerpts and raw
log identities. The earlier 64 focused checks and distribution validation pass.

Pending: corrected full Windows/Linux runs, hosted exact-candidate two-build
replay, installed package and upgrade qualification, final integration capture,
human verification and the exact release-record decision. No publication or
verification is claimed. The user approved the release package, required
verification and bounded review pushes/PRs; the work order retains that decision.

The diff stays within the approved paths. Provider-setting changes and repository
adoption are excluded. Public 0.21.0 / plugin 0.2.4 claims retain their historical
limits; the 0.22.0 / 0.2.5 availability is explicitly pending.
