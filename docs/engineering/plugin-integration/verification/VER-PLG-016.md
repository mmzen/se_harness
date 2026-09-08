+++
id = "VER-PLG-016"
type = "verification"
title = "Truthful released installation guidance"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-027"]
+++

# Verification Contract: Truthful released installation guidance

## Independence

The verifier uses published package/catalog identities and approved host evidence, independently of the guide’s claims. Review commands against that exact released CLI help.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-027 | test, inspection | C01–C06 | Each instruction is reproducible for its named qualified release; unavailable paths and missing prerequisites never claim activation. |

## Acceptance scenarios

Each case creates new test evidence under `evidence/WO-PLG-016/Cnn/`: `actions.txt`, `stdout.txt`, `stderr.txt`, and `observations.json`; these are not plugin APIs.
`observations.json` records expected/observed values, exit status, source evidence paths and a pass/fail/unavailable conclusion. The Evidence column names additional captures.

| Case | Starting fixture | Action | Observable result | Evidence |
| --- | --- | --- | --- | --- |
| C01 | Named available release/catalog entry; provided Python; clean disposable repository | Operator follows the guide’s exact installation commands. | Catalog/package identities match the guide; setup and activation have separate observed results; the environment is outside the repository. | guide revision; commands; catalog identity; environment/discovery outputs |
| C02 | No suitable Python on the host | Follow the guide’s setup entry. | Guidance requests Python 3.11+ with venv/ensurepip; no Python download, repository initialization or readiness declaration occurs. | operator transcript; process log; repository inventory |
| C03 | Unavailable release or host absent from qualification matrix | Follow its documented link/route. | The guide marks it unavailable/prospective rather than usable; no unqualified support statement is produced. | link/catalog result; qualification matrix; quoted guide text |
| C04 | Repository version differs from the packaged evaluator | Attempt normal governed use. | Version mismatch is reported; the guide offers compatible plugin selection or authorized upgrade without silently changing the lock. | identity result; guide recovery text; lock hashes |
| C05 | Damaged environment or interrupted setup | Follow the documented recovery. | Fresh verified replacement precedes activation; the previous usable environment and owner content are preserved until replacement succeeds. | environment inventories; identity results; owner-file hashes |
| C06 | Passing local hook but no exact external-action authority/enforcement | Follow the guide’s authority explanation. | The text does not claim merge/publication permission; no external dispatch occurs during the onboarding rehearsal. | quoted limitation; command/dispatch log |

## Property and invariant tests

C01 distinguishes installation from activation. C02/C04 compare repository inventories and locks, preventing prerequisite failures from appearing as successful setup.

## Static and architecture checks

Map to PLG-DOC-001–006 and the qualified release. Retain checked links, exact command help and the guide revision; future commands must remain prospective.

## Security and privacy checks

Use disposable profiles and synthetic credentials only. C06 records zero external dispatch, without treating a local hook as remote enforcement.

## Performance and resilience checks

C05 retains interruption/recovery steps and resulting state. The onboarding guide must not advertise qualification timings from unrelated machines.

## Manual assessments

A separate operator rehearses each claimed host/platform route using the named available release. Record host, Python and evaluator identities; baseline 0.16.0 is not proof of a future plugin release.

## Evidence retention

Retain each case’s fixture revision, argv, exit status, raw output and listed observations under `evidence/WO-PLG-016/Cnn/`.
Record expected and observed values separately, with a pass/fail/unavailable conclusion. Keep original failures and bind later assurance to the exact implementation candidate.

## Residual uncertainty

Unavailable catalogs, unresolved onboarding direction or missing host proof prevent corresponding current-use claims. This document records planned verification only.
