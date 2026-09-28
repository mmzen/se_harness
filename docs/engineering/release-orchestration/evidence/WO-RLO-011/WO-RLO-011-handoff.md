```toml
artifact = "WO-RLO-011"
checkpoint = "handoff"
formal_snapshot_sha256 = "99553fee2b67de9b4227bb7d318aab6493a686d806dd2124e6f44b405b4fb212"
rebound_at = "2026-09-28T19:50:22Z"
```

# WO-RLO-011 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

The reporting command, synthetic example, focused tests and bounded guide
updates are complete. See [assessment.md](assessment.md) for the requirement
matrix, review findings and limits. [checks.zip](checks.zip) retains the actual
commands, outputs and original missing-header refusal.

The final focused suite passed 18 tests with one native symlink case skipped
because this Windows host denies symlink creation. The existing release and
dashboard publication regressions passed. The documented example and new guide
links passed. No live marketplace update, host installation or publication was
performed. Verification acceptance remains a separate human decision on the
exact ready verification record.
