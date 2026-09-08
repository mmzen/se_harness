+++
id = "VER-PLG-007"
type = "verification"
title = "Session governance delivery acceptance"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-010", "REQ-PLG-011", "REQ-PLG-012"]
+++

# Verification Contract: Session governance delivery acceptance

## Independence

The assurance owner captures complete expected source bytes before exercising the handler. Output is compared with those bytes independently of the handler’s readiness claim.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-010 | test, inspection | C01, C02, C06–C08 | Only complete verified gate/router bytes reach readiness. |
| REQ-PLG-011 | test, inspection | C03, C07 | Resume/compaction rechecks current state; a missing interpreter gives no handler success. |
| REQ-PLG-012 | test, inspection | C04–C06 | Incomplete or changed fallback bytes cannot establish readiness. |

## Acceptance scenarios

Each case creates new test evidence under `evidence/WO-PLG-007/Cnn/`: `actions.txt`, `stdout.txt`, `stderr.txt`, and `observations.json`; these are not plugin APIs.
`observations.json` records expected/observed values, exit status, source evidence paths and a pass/fail/unavailable conclusion. The Evidence column names additional captures.

| Case | Starting fixture | Action | Observable result | Evidence |
| --- | --- | --- | --- | --- |
| C01 | Intact repository; independent copies of managed AGENTS.md block and ENGINEERING_HARNESS.md | Run session-context.py with a captured supported startup event. | Verification precedes delivery; delivered gate/router bytes equal both complete source copies, including end markers. | invocation order; source/output bytes and SHA-256 |
| C02 | Wrong evaluator identity, modified gate, or modified router | Run each startup fixture. | Existing identity/doctor refusal is retained; none of the variants emits content as verified or reports ready. | evaluator results; script output; source digests |
| C03 | Prior ready session; then source/runtime identity changes | Send supported resume and compaction events. | New evaluator invocations inspect current inputs; stale readiness and old source digests cannot substitute. | two event sequences; identity and source comparisons |
| C04 | Direct-output capacity smaller than the required governance content | Deliver through the accepted complete-read fallback. | The full fallback read matches verified source bytes before a readiness declaration. | capacity setting; fallback read; readiness ordering |
| C05 | Fallback unavailable, interrupted, or truncated | Attempt restoration for each condition. | Output identifies blocked delivery; no readiness declaration follows the partial read. | read trace; partial bytes; blocker output |
| C06 | Gate/router changes after verification or before fallback reading | Inject the change at each boundary. | Changed bytes are rejected and reverified; output never labels the changed content with the earlier verified identity. | injection point; old/new hashes; repeated verification trace |
| C07 | Prepared environment interpreter removed | Attempt the configured host invocation. | Host-launch failure is captured; no handler output or verification result is fabricated. | host launch error; empty handler invocation log |
| C08 | Repeated events; outside credential sentinel and path-escape fixture | Replay events and attempted unsafe reads. | Repository inventory is unchanged; output contains neither unrelated content nor the sentinel value. | before/after inventory; output scan; read trace |

## Property and invariant tests

C01/C04 compare exact bytes; C06 covers verification-to-use races. C08 compares the full repository inventory across repeated events.

## Static and architecture checks

Map cases to PLG-CTX-001–006 and ARCH-PLG-002/ADR-PLG-002. Retain the single verification-before-delivery call path.

## Security and privacy checks

Use a synthetic credential sentinel for C08. Retain its hash and match result, not any real secret.

## Performance and resilience checks

Retain startup/restoration timestamps for direct and fallback cases, including slow and interrupted reads; verification remains enabled.

## Manual assessments

Run captured Codex/Claude protocol fixtures with recorded OS, Python and released-evaluator identity. Live context delivery belongs to VER-PLG-005/006 and VER-PLG-015.

## Evidence retention

Retain each case’s fixture revision, argv, exit status, raw output and listed observations under `evidence/WO-PLG-007/Cnn/`.
Record expected and observed values separately, with a pass/fail/unavailable conclusion. Keep original failures and bind later assurance to the exact implementation candidate.

## Residual uncertainty

Fixture acceptance qualifies the shared handler only. These cases do not claim completed host delivery or execution results.
