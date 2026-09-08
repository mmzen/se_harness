```toml
artifact = "WO-PLG-004"
checkpoint = "handoff"
formal_snapshot_sha256 = "e51678349daba4802f9c4eaf97a5ceec7a77113dfaa7e17fa68ada56c7316608"
rebound_at = "2026-09-08T22:05:33Z"
```

# WO-PLG-004: partial investigation handoff

**Work remains in progress. All seven full host acceptance cases are incomplete.**
This packet retains the observations available so far and the current environment
limits. It is not a claim of completed implementation, verified conformance,
production support, or permission to merge.

The operator approved this packet and authorized its work in the current Codex
task. The actual definition approvals, WO approval, and separate start are
recorded in [governance](governance/). No completion or assurance transition was applied.

## Actual work and evidence

- [Host observations and remaining cases](REPORT.md) distinguish real host events,
  direct fixture calibration, failed attempts, and unavailable observations.
- [Repository checks](repository-checks/) retain graph, managed-integrity,
  candidate CLI, and distribution-metadata results.
- The fixture instructions and focused test evidence document repeatable local
  checks. Passing observer tests are not passing host acceptance cases.
- No live authenticated conversation completed; setup/repair through the host's
  real tools and the remaining resume, compaction, trust, and permission observations
  must still be collected. Isolated sign-in is pending with the operator.

## Decision and next action

Continue the already authorized investigation once its isolated sign-in is available.
Keep `WO-PLG-004` in `in_progress`. The accountable engineering owner has not accepted
completion. A mechanically passing handoff check would establish fresh, scoped
evidence only; it does not inspect the completeness of these host observations.

No VREC, production adapter, release, or integration decision is made by this packet.
