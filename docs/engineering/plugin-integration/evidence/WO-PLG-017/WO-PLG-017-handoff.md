```toml
artifact = "WO-PLG-017"
checkpoint = "handoff"
formal_snapshot_sha256 = "2344b4d72d50bcd7413a0a752570ffcf0819a3ee615d166abbebadcc258b5594"
rebound_at = "2026-09-11T06:26:55Z"
```

# WO-PLG-017 handoff evidence

All 56 approved files moved without byte changes. The original 55-file plan/map,
VREC008 and sidecar remain unchanged; C/G remain ancestors. The supplemental map
binds the separately approved 730-byte JSON.

Independent matching-depth Windows staging, Linux reconciliation and both tamper
cases passed. The checker enforces the ordinary 250-character checkout budget
and separate 259-character staging profile. All 13 hosted checks passed at
e5b48a16, including the Windows upgrade and downstream integration jobs.
Original failures and the exact observation versions remain retained separately.

The released evaluator applied delegated completion; WO-PLG-017 is implemented. No aggregate
VREC preparation, assurance, supersession, release or GitHub merge is inferred.
