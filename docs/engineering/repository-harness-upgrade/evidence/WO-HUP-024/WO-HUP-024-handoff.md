```toml
artifact = "WO-HUP-024"
checkpoint = "handoff"
formal_snapshot_sha256 = "9f43b59cc784aa77d4a0805eb27b6bd2429cdc232f9f64849d1d0ea7ae2c0d7d"
rebound_at = "2026-09-29T20:34:01Z"
```

# WO-HUP-024 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Observed implementation

The released 0.20.0 installer completed the selected update and retained its
transaction. CI selects 0.20.0; source/package metadata agree at 0.21.0.
AGENTS.md and the six owner pointers retain their bytes. There are no changes
outside the approved paths. No host settings or external refs were changed.

## Verification evidence

See README.md, checks.json and review.json in this directory. The full suite
passed 1,162 tests with 17 skips. Exact released identity, doctor, graph
validation, released-root qualification, governor transition assessment,
distribution validation and CLI/version checks pass. Failed command attempts
and their corrected results remain retained. The no-op preview contains only
unchanged dispositions. The selected template matches the released payload.

## Limits and next decision

The candidate still needs its commit-bound verification record and human
verification acceptance. Hosted Linux and Windows CI remain required before
integration. This work makes no fresh native host-delivery claim and preserves
the old guide pointers pending separately reviewed cleanup.
