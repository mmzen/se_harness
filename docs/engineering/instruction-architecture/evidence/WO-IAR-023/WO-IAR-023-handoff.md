```toml
artifact = "WO-IAR-023"
checkpoint = "handoff"
formal_snapshot_sha256 = "ee37efbcc9ceb83f00c950f152e78dd88cfcdd2a8fe320f2dc9e4d344aed4399"
rebound_at = "2026-09-28T08:24:42Z"
```

# WO-IAR-023 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

The exact approved patch is applied.patch. Both focused corrected cases pass.
The shared full Windows/Linux runs pass with 1,134 tests each; checks.json and
../WO-IAR-021/verification-evidence.json retain the exact results. The original
failures and baseline reproduction are preserved. Owner-byte assertions and
installer refusal behavior remain intact. See review.md for the contract
assessment. Human verification acceptance is pending.
