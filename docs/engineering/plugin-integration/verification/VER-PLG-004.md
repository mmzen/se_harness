+++
id = "VER-PLG-004"
type = "verification"
title = "Claude Code compatibility evidence before support selection"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-007"]
+++

# Verification Contract: Claude Code compatibility evidence before support selection

## Independence

Expected event names and host behavior come from SPEC-PLG-004 and the exact Claude Code documentation assessed. An observation fixture records the host; it does not simulate proof of host support.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-007 | test, inspection | C01–C07 | Each claimed capability has a retained host observation; absent capability is recorded as incompatible or unavailable. |

## Acceptance scenarios

Each case creates new test evidence under `evidence/WO-PLG-004/Cnn/`: `actions.txt`, `stdout.txt`, `stderr.txt`, and `observations.json`; these are not plugin APIs.
`observations.json` records expected/observed values, exit status, source evidence paths and a pass/fail/unavailable conclusion. The Evidence column names additional captures.

| Case | Starting fixture | Action | Observable result | Evidence |
| --- | --- | --- | --- | --- |
| C01 | Disposable host profile; documented shell guard; no prepared evaluator | Attempt skill discovery, new-session activation, resume and compaction. | The guard requests setup without invoking missing Python; setup remains reachable, or the probe records the precise incompatible host behavior. | guard command; discovery output; ordered host transcript |
| C02 | Provided Python missing, older than 3.11, or without usable venv/ensurepip | Attempt the observed setup entry for each condition. | Operator guidance identifies the prerequisite; no Python installation, environment readiness, or repository initialization is claimed. | guidance; process trace; before/after repository inventory |
| C03 | Provided Python and an environment containing the selected released evaluator | Repeat the observed startup route twice from fresh sessions. | Each run records the discovered setup skill, event names, invoked interpreter and delivered governance bytes, or a reproducible incompatibility. | two host transcripts; interpreter identity; delivered bytes |
| C04 | Prepared environment; repository governance changed since the prior session | Resume and compact using the host’s documented actions. | The report identifies fresh event and content delivery, or records the unsupported restoration route; prior-session output is not evidence of fresh delivery. | event timestamps; old/new source digests; context capture |
| C05 | Claude Code required hooks disabled and then enabled | Start sessions in both configurations. | The report records the permission/enablement interaction and distinguishes an absent event from a handler result. | trust/settings transcript; event log |
| C06 | Plugin path contains spaces; plugin update/reload; removed environment interpreter | Repeat activation across each change. | Actual argv, persistent-data location, required restarts and launch failures are retained; removed Python is not attributed a successful script result. | argv log; data-directory inventory; launch/reload transcript |
| C07 | Session/tool hooks registered; no environment; verified provided Python and user-authorized setup | Through real Claude Code shell tools, create the external venv and install the exact bundled wheel offline. Before readiness, attempt a disposable governed write; after readiness, remove the interpreter and repeat authorized repair. | Ordinary host permissions remain active. The guard does not blanket-veto this bounded setup; governance stays unready until fresh identity/context checks. Retain the governed-write result: absent required refusal is a coverage failure, not checked success. Blocked setup/repair records bootstrap incompatibility. | real tool/event/permission transcript; venv/pip argv; governed-target hashes; repository inventory; identity/context results |

## Property and invariant tests

Each C01–C07 row names the host version and source transcript. C07 requires actual setup and repair; skill discovery alone cannot establish bootstrap compatibility.

## Static and architecture checks

Review the probe against its specification. Retain fixture source showing observation-only behavior and no second evaluator policy.

## Security and privacy checks

Use a disposable profile and repository. Compare normal-profile and repository inventories before/after; redact authentication material from event logs.

## Performance and resilience checks

C03–C06 record activation duration, restart count and every trust/permission interaction; retain both repeated runs.

## Manual assessments

Assess available Windows, Linux and macOS profiles for Claude Code, with provided Python and the named released evaluator. Evidence must distinguish observed, incompatible and unavailable combinations.

## Evidence retention

Retain each case’s fixture revision, argv, exit status, raw output and listed observations under `evidence/WO-PLG-004/Cnn/`.
Record expected and observed values separately, with a pass/fail/unavailable conclusion. Keep original failures and bind later assurance to the exact implementation candidate.

## Residual uncertainty

A reproducible incompatibility can complete this investigation. Production support still requires a positive route selected through DEC-PLG-002; no support decision is made here.
