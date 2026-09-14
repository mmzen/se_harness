```toml
artifact = "WO-KIS-007"
checkpoint = "handoff"
formal_snapshot_sha256 = "14492f6fff333da27b3dc539cb629578871a31980a1fbaa17d9cf05429aff5fe"
rebound_at = "2026-09-14T18:49:06Z"
```

# WO-KIS-007 implementation evidence

WO-KIS-007 is in progress. K32 removes internal-name inventories and source-shape
assertions. K33 replaces three checkout settings and aggressive GC with one real
checkout per supported OS. K34 keeps actual installations, real origin/path
failures and one unavailable-path failure; the original capability matrix was
already removed by WO-KIS-003.

Focused validation passed 105 tests (2 skipped); workflow and suite hygiene
passed 45 tests. A disposable copy of the interpreter path helper was renamed;
three existing behavior tests passed unchanged. The full suite and hosted
Windows/Linux evidence follow before completion. No speed improvement is claimed.
