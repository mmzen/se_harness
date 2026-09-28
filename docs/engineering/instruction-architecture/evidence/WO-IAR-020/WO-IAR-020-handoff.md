```toml
artifact = "WO-IAR-020"
checkpoint = "handoff"
formal_snapshot_sha256 = "266dce2648c30ac20352b3ff404622d334b726c0ab6cbf77d0cc728b3b752275"
rebound_at = "2026-09-28T08:24:07Z"
```

# WO-IAR-020 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

Qualification is incomplete. This packet retains partial observations for the
combined review; it does not claim WO-IAR-020 is implemented or verified.
See inventory-of-evidence.json and ../../acceptance/plugin-adoption/README.md.
Codex native startup, manual compaction and boundary probes passed in the
isolated profile. Claude delivered the full startup root, but its expired
isolated OAuth login prevented model-response and compaction qualification.
Real profiles still select 0.1.0; their replacement requires the exact separate
adoption authority described in the handoff. No real profile was changed.
