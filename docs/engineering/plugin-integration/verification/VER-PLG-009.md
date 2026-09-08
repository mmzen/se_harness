+++
id = "VER-PLG-009"
type = "verification"
title = "Repository connection and discovery acceptance"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-015", "REQ-PLG-016"]
+++

# Verification Contract: Repository connection and discovery acceptance

## Independence

Expected file ownership and installer behavior come from the released command help and existing installer contracts. Host discovery is observed directly, not inferred from filenames.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-015 | test, inspection | C01–C04, C07, C08 | Only the authorized released installer changes the reviewed target; ownership conflicts preserve files. |
| REQ-PLG-016 | test, inspection | C05, C06 | Actual host discovery selects one approved compatible definition, or stays unready without deleting managed files. |

## Acceptance scenarios

Each case creates new test evidence under `evidence/WO-PLG-009/Cnn/`: `actions.txt`, `stdout.txt`, `stderr.txt`, and `observations.json`; these are not plugin APIs.
`observations.json` records expected/observed values, exit status, source evidence paths and a pass/fail/unavailable conclusion. The Evidence column names additional captures.

| Case | Starting fixture | Action | Observable result | Evidence |
| --- | --- | --- | --- | --- |
| C01 | Empty new target; released evaluator 0.16.0 | Run init REPO --dry-run --json, inspect, then authorized init REPO --json. | Preview writes nothing; application creates the planned managed files, including .engineering-harness.lock; doctor exits 0 on the intact fixture. | help; plan/result JSON; before/after inventory; doctor |
| C02 | Existing target; explicitly selected target release and upgrade authority | Run upgrade REPO --json, then upgrade REPO --apply --json. | Only the reviewed installer changes managed content/lock; requested installer evidence identifies actual changes. | reviewed plan; result; lock hashes; evidence output |
| C03 | Customized managed file, conflicting target path, or uncertain ownership | Attempt the relevant released installer operation. | The conflict is reported; customized owner bytes are unchanged and no manual deletion occurs. | installer finding; file hashes; tool trace |
| C04 | Reviewed operation followed by changed target/scope; interrupted application | Resume the setup skill. | Changed inputs trigger renewed checking or an authority blocker; partial writes are inventoried before retry. | old/new plans; authority transcript; partial inventory |
| C05 | Duplicate repository/plugin skills; positively accepted DEC-PLG-004 route | Connect and invoke each duplicated name in the host. | Discovery resolves exactly one compatible implementation per name, with retained source path and digest. | decision reference; host discovery and invocation log |
| C06 | No compatible route or unresolved DEC-PLG-004 | Attempt connection with duplicate skills. | Discovery remains unready; locked skill bytes and repository ownership records remain unchanged. | blocker output; managed-file/lock hashes |
| C07 | Ready repository; plugin-only update and repeated unchanged request | Reload setup without requesting repository upgrade. | Repository lock/owner bytes stay unchanged; no duplicate decision prompt or installer write is introduced. | before/after hashes; tool and prompt transcript |
| C08 | Existing repository with owner README/AGENTS content and no harness | Run released 0.16.0 adopt REPO --dry-run --json, then authorized adopt REPO --json. | Preview writes nothing; application preserves owner content and inserts only planned managed content; actual result matches the reviewed target. | command help; plan/result; owner-file diff; lock |

## Property and invariant tests

C01–C04 and C07 compare complete owner/managed inventories and locks. C05 retains the host-selected implementation path for each duplicate name.

## Static and architecture checks

Map to PLG-REPO-001–005 and SPEC-AEX-005. The example forms are confirmed against released 0.16.0; retain help for any selected later release.

## Security and privacy checks

C03/C06 prohibit manual locked-file deletion. Disposable fixtures isolate target conflicts from the developer’s actual repository.

## Performance and resilience checks

C04/C07 retain interruption points, repeated operations and decision prompts. Do not silently reuse a changed reviewed operation.

## Manual assessments

Record provided Python, selected evaluator and every claimed host/platform. Live coexistence requires the positively selected supported route and approved governing definitions.

## Evidence retention

Retain each case’s fixture revision, argv, exit status, raw output and listed observations under `evidence/WO-PLG-009/Cnn/`.
Record expected and observed values separately, with a pass/fail/unavailable conclusion. Keep original failures and bind later assurance to the exact implementation candidate.

## Residual uncertainty

An unresolved ownership decision blocks connection acceptance. A clean-repository demonstration alone cannot qualify migration.
