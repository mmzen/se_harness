+++
id = "VER-PLG-012"
type = "verification"
title = "Retained orientation and explicit operator briefing"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-10"

[relations]
verifies = ["REQ-PLG-020", "REQ-PLG-021"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T18:19:50Z"
decided_by = "assurance-owner"
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only VER-PLG-012 approval under assurance-owner, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 8d19c23d400c0ec960f4761d0f160ee696b7ddeb03cf8d2c57e65e2683d8894b. The definition meaning is unchanged from the reviewed packet. Assurance of implementation, release and PR merge remain separate human decisions."
+++

# Verification Contract: Retained orientation and explicit operator briefing

## Independence

Expected fields and diagnostics come from the retained skill contracts, orient.py and check_brief.py. The verifier fixes protected source bytes independently of rendered output.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-020 | test, inspection | C01–C03, C08 | Existing orientation operations, inline receipt and zero target mutation remain intact. |
| REQ-PLG-021 | test, inspection | C04–C08 | Only explicit briefing proceeds; protected bytes and existing result schemas remain unchanged. |

## Acceptance scenarios

Each case creates new test evidence under `evidence/WO-PLG-012/Cnn/`: `actions.txt`, `stdout.txt`, `stderr.txt`, and `observations.json`; these are not plugin APIs.
`observations.json` records expected/observed values, exit status, source evidence paths and a pass/fail/unavailable conclusion. The Evidence column names additional captures.

| Case | Starting fixture | Action | Observable result | Evidence |
| --- | --- | --- | --- | --- |
| C01 | Valid external evaluator and selected artifact | Run packaged orient.py with the existing absolute launcher arguments. | Exit 0; outcome completed or documented degraded; receipt effects.changed_paths and execution.worker_results are []. | argv; orientation JSON; independent target snapshot |
| C02 | Same selection with and without explicit --preflight-phase | Run both orientations. | Only the requested run includes preflight; the other reports preflight.status=not_requested. Neither writes a receipt file. | operation lists; preflight field; directory diff |
| C03 | Wrong expected evaluator version; then wrong root/payload identity | Run orientation for each mismatch. | Exit 2; outcome blocked; wrong version reports AEXORI013; later inspection/repair calls do not occur. | orientation JSON; operation trace |
| C04 | Request does not explicitly name harness-operator-brief | Route the request, then test an invalid explicit_skill in check_brief.py input. | Implicit briefing is not invoked; direct invalid helper input exits 2 with TCM003. | skill/tool log; helper JSON |
| C05 | Explicit bounded source with valid protected spans and zero changed paths | Render and validate through check_brief.py --request-json INPUT. | Exit 0; outcome completed; source_sha256 matches; protected_binding_count equals the declared spans; existing result/receipt schemas remain inline. | request; rendered bytes; helper result; inline receipt |
| C06 | Wrong source digest, invalid span order, or altered protected output bytes | Validate each brief fixture. | Exit 2; wrong digest yields TCM006 and altered output TCM010; malformed spans retain their existing diagnostic. | requests; exit codes; diagnostic JSON |
| C07 | Brief needs current state absent from supplied source | Request the bounded brief. | Skill reports current-state-result-required/stopped; it does not invent current state or make an unrequested query. | source; skill result; tool-call log |
| C08 | All prior cases with synthetic network/credential/spawn and mutation sentinels | Inspect observed effects. | Repository/Git hashes match before/after; network, credential and spawn logs are empty; no lifecycle event or evidence file appears. | inventories; sentinel logs; artifact diffs |

## Property and invariant tests

C01/C02 compare receipt operations with requested inputs. C05/C06 compare protected bytes; C08 checks effects independently of the receipt.

## Static and architecture checks

Map cases to PLG-RO-001–006. Compare packaged helper/contract changes with their installed originals; installation-path adaptation must not add authority.

## Security and privacy checks

C08 uses synthetic credential and network interception, never real secrets. Empty logs are checked together with the enforced tool boundary.

## Performance and resilience checks

Retain interruption outputs and operation counts. Latency acceptance belongs to the qualified profile, not to removing existing helper checks.

## Manual assessments

Run Windows/Linux instruction/helper fixtures with provided Python 3.11+ and released evaluator 0.16.0. Host qualification and live migration remain separate.

## Evidence retention

Retain each case’s fixture revision, argv, exit status, raw output and listed observations under `evidence/WO-PLG-012/Cnn/`.
Record expected and observed values separately, with a pass/fail/unavailable conclusion. Keep original failures and bind later assurance to the exact implementation candidate.

## Residual uncertainty

These checks preserve the retained contracts; they do not grant multi-agent execution or human assurance.
