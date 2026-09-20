```toml
artifact = "WO-ECP-039"
checkpoint = "handoff"
formal_snapshot_sha256 = "7baff38fd623cb416bb27027832dbe6476af1e46296b564d5e6006a67538d180"
rebound_at = "2026-09-16T18:12:38Z"
```

# WO-ECP-039 handoff evidence

The [implementation report](implementation.md) records the bounded ownership
assertion correction, its review and acceptance. [Results](verification-results.json)
retain commands, runtime identities, original failures and successful retries.

The final implementation commit 2d79e0108084dfcd15efa16187e555a99ed70689 passes
the full 1,081-test source suite with 15 skips. Both real Windows 0.18.0-to-0.19.0
replays pass all six steps and produce the same schema-4 lock digest. The
operational checkout remained clean. The initial path-length failure, later
Git staging timeout and first full-suite Git timeout remain visible; no code
or timeout limit was changed to obtain the successful retries.

The released evaluator's integrity, graph, scope and review-preflight checks
pass. All 29 earlier cleanup/assessor evidence files and their relevant product,
plugin and evaluator inputs remain unchanged. Earlier verified records retain
their original meaning. Final candidate input comparison and the exact CI
planner/assessor commands accompany preparation of aggregate VREC-ECP-041.
Owner assurance and later hosted CI remain separate decisions/checks.
