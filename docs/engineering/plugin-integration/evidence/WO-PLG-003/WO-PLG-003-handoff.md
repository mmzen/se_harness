```toml
artifact = "WO-PLG-003"
checkpoint = "handoff"
formal_snapshot_sha256 = "b9d984333381cfe82288aee38a3893286e3bbe08f32ef5675b8cce76cbb3fa06"
rebound_at = "2026-09-09T06:36:42Z"
```

# WO-PLG-003: partial investigation handoff

**Work remains in progress. The current case matrix and remaining observations
are recorded in [the report](report.md).**
This packet retains the observations available so far and the current environment
limits. It is not a claim of completed implementation, verified conformance,
production support, or permission to merge.

The operator approved this packet and authorized its work in the current Codex
task. The actual definition approvals, WO approval, and separate start are
recorded in [governance](governance/). No completion or assurance transition was applied.

## Actual work and evidence

- [Host observations and remaining cases](report.md) distinguish real host events,
  direct fixture calibration, failed attempts, and unavailable observations.
- [Repository checks](repository-checks/) retain graph, managed-integrity,
  candidate CLI, and distribution-metadata results.
- The fixture instructions and focused test evidence document repeatable local
  checks. Passing observer tests are not passing host acceptance cases.
- The [2026-09-09 resumption check](20260909-resumption/auth-status.json)
  retains the earlier signed-out state. The operator subsequently completed
  isolated sign-in. [Live observations](20260909-live/) now include actual
  authenticated conversations and hook-trust interactions. Login output and
  credential material remain excluded from public evidence.
- Further case conclusions must follow the actual host events and evaluator
  results. A successful model response alone does not establish hook delivery,
  setup, readiness, or permission enforcement.
- C01 and C03-C07 now have complete behavioral observations for the recorded
  Windows route. The [fresh C07 sequence](20260909-live/complete-sequence-summary/)
  retains actual tool-call refusals, real setup and repair, released readiness
  and fresh host context. Its full 49-file repository comparison and bounded
  20-input metadata comparison are distinct from the earlier inventory gaps.
- C02 demonstrates guidance and stopping for an observer-confirmed missing
  selected interpreter; no agent prerequisite-check tool runs in that case.
  Genuine older/unusable interpreter variants and other platforms remain
  unavailable. The report retains all source, trust and inventory limitations.

## Decision and next action

The engineering owner must decide whether these observations and their explicit
coverage limits complete the authorized investigation.
Keep `WO-PLG-003` in `in_progress`. The accountable engineering owner has not accepted
completion. A mechanically passing handoff check would establish fresh, scoped
evidence only; it does not inspect the completeness of these host observations.

No VREC, production adapter, release, or integration decision is made by this packet.
