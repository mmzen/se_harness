```toml
artifact = "WO-PLG-018"
checkpoint = "handoff"
formal_snapshot_sha256 = "531359248fbb926a3a5f0aab9ef730b3acfede2445dd491e78858a84d93d76fc"
rebound_at = "2026-09-11T10:37:57Z"
```

# WO-PLG-018 handoff evidence

The pinned plugin stack is assembled. All 3,177 imports retain their approved
modes/blobs and original ancestry. The new preservation checker and 22 synthetic
tests pass on Windows and Linux; independent historical inspection reads all
446 bound evidence selections. Old WOs and VRECs retain their pinned state/bytes.

All 17 reported hosted checks passed at `507bdb8d2bd978bcb02ea043c72a68617a9d9439`. The raw archive records each run/job identity, tested checkout and actual main base.

The [report](report.md) and [indexed raw archive](raw-index.json) retain actual
observations, failures, corrections and limitations. The source-doctor version
skew is documented; the external released evaluator supplies the governing result.
WO-PLG-018 remains in_progress. Completion requires full passing hosted checks;
VREC preparation follows only through its delegated gate. Assurance and merge
remain separate operator decisions.
