```toml
artifact = "WO-IAR-014"
checkpoint = "handoff"
formal_snapshot_sha256 = "b27e7ce1ad16bcbc7571867613262a792ca969f4f15764202403d82d503b4ac0"
rebound_at = "2026-09-27T09:33:28Z"
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
