```toml
artifact = "WO-IAR-031"
checkpoint = "handoff"
formal_snapshot_sha256 = "192eb36dabafbba7525242b3f00c299b30d23ac01f53d5a79c4bac5591908143"
rebound_at = "2026-09-30T11:55:35Z"
```

# WO-IAR-031 handoff evidence

The resource implementation and approved two-file workflow correction were
tested together at commit 6b6f64ed94ecfc89dcc9c74179a742b134edd87a.
The selected governing evaluator remains released 0.20.0.

See ../WO-IAR-031/implementation.json for the VER-IAR-020 criterion assessment,
the exact built wheel identity, commands, platform results, review and retained
failure history. See ../WO-IAR-028/implementation.json for earlier partial
resource qualification; its pending wording records that earlier stage.

The final focused suite ran 198 tests: 195 passed, three skipped. The same
committed candidate wheel passed 25 Windows and 26 offline Linux qualification
steps, including six legacy/external workflow comparisons on each platform.
Native host delivery, installer migration, human acceptance and publication
are outside this completed implementation unit.

Both work orders participate in the supported combined scope check. The
complete Git change set is derived from 3ed0fc5e89462011ea115ad4c4191067f815cf95
and checked against their union by released check-pr using a local event fixture.
The actual combined result is retained at ../WO-IAR-031/combined-handoff.json
once that check succeeds. No real pull request or external action is implied.
