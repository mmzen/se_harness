```toml
artifact = "WO-RLS-030"
checkpoint = "handoff"
formal_snapshot_sha256 = "c2faa2a8c17025d52b49cd814097426adcb83c944a58f11ebd0c6881305f48e4"
rebound_at = "2026-10-01T10:57:25Z"
```

# WO-RLS-030 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

The only implementation change restores the README sentence: It does not download the harness from PyPI.

The focused suite passes 61 tests with one existing Windows skip. The full source regression at 0700cd0da99c4a732399c052f85f14eb1a0d2001 runs 1,189 tests, with 1,171 passes, 18 skips, and no failures. See commands/focused-tests.json, full-source-summary.json and review.json. The full runner retains an aggregate skip count; its output does not list each reason.

The tests and published package are unchanged. Commands/fix030-reused-evidence.json confirms protected records and reused evidence bytes; commands/fix030-public-ref-readback.json confirms the existing public marketplace revision. Failed CI evidence and the local reproduction remain available.

The complete change set for this correction starts at fe048340d39461cde161bfafd7f486b51a4c9ca6. New files are this work order and its allowed evidence. Preparing the aggregate VREC-PLG-029, its human decision, PR update, subsequent CI and merge remain separate. VREC-PLG-028 is preserved. Overall public delivery and release markers remain pending.
