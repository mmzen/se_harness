```toml
artifact = "WO-IAR-014"
checkpoint = "handoff"
formal_snapshot_sha256 = "3685616bbdbacd260fc575caadfe0ce494ef25d40e8349e68d1acba4ce643ae9"
rebound_at = "2026-09-27T10:21:58Z"
```

# WO-IAR-014 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Retained observations

Evaluator discovery and installer changes are retained for review.
migration-final-focused.stderr records 84 passing tests.
guarded-isolated-package.assertions.json and its logs retain the non-promotable
package observation, clean installation and missing-receipt refusal.
implementation-review.md is an earlier observation with failures; the later
WO-IAR-017 correction and ../WO-IAR-013/ci-correction/full-regression.stdout
retain subsequent passing regression results. Linux migration is unverified.

This is an interim handoff for the draft PR. The work order remains
in_progress. Native qualification gaps remain open; this packet and a
passing mechanical gate do not establish completion or verification.
