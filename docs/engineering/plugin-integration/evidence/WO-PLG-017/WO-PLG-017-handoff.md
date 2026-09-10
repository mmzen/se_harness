```toml
artifact = "WO-PLG-017"
checkpoint = "handoff"
formal_snapshot_sha256 = "694127693cc6a38ab00a9c21f680abf2b4007266b96943f42b9369f412e3c29a"
rebound_at = "2026-09-10T21:33:19Z"
```

# WO-PLG-017 handoff evidence

## Repair in progress

The released evaluator applied the delegated start after the operator approved
WO-PLG-017. All 55 approved native-product files now use short paths. The map
preserves original names, sizes and SHA-256 values; payload bytes, source
manifests and historical verification records remain unchanged.

The local retention checker passes. An independent reviewer identified that its
plan also needed an immutable approval binding; the checker now pins the exact
approved plan digest. Independent Windows/Linux and tamper checks, and all CI
outcomes, remain pending. Completion is not claimed from the local check alone.

This work does not verify VREC-PLG-008, authorize an aggregate replacement record,
supersede history or merge any PR. WO-PLG-017 remains in_progress.
