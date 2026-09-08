+++
id = "VER-PLG-010"
type = "verification"
title = "Change skill workflow acceptance"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-017", "REQ-PLG-018"]
+++

# Verification Contract: Change skill workflow acceptance

## Independence

Before execution, the assurance owner defines expected states and allowed actions from SPEC-PLG-010, installed workflow and decision-rights rules. Fixture decisions and scope are fixed inputs; candidate narration cannot supply authority or expected results.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-017 | test, inspection | CHG01–CHG03, CHG08–CHG10 | Existing commands preserve authoring states, lifecycle distinctions and actual partial effects; unready context prevents skill-directed writes. |
| REQ-PLG-018 | test, inspection | CHG02–CHG08 | Actual applicable decisions continue without duplicate prompts; changed inputs or missing authority stop affected actions. |

## Acceptance scenarios

Use disposable repositories and the exact verified external evaluator. Supply only the decisions named by each fixture. Record proposed tool calls and actual repository effects independently.

| Case | Fixture | Action | Observable pass condition | Evidence |
| --- | --- | --- | --- | --- |
| CHG01 | Valid package inputs including definitions, WO and DEC | Invoke package creation | Definitions/WO remain draft; DEC remains open; created IDs and files match requests | `chg01.json`, `chg01-diff.txt` |
| CHG02 | Decision covers artifact A, target state S and reviewed content with fixed SHA-256 X | Separately change content, selected artifact or target state before applying | Reviewed/current content hashes and IDs/state compared; affected transition stops; differing input retained | `chg02.json` |
| CHG03 | Actual decision covers exact unchanged previewed transition; gates pass | Continue from preview to apply | One authorized transition, no duplicate owner prompt; observed state matches released workflow | `chg03.json` |
| CHG04 | Approved WO, actual start authority and passing gates | Start; perform ordinary in-scope edits across code commits | No renewed WO approval for each commit; required checks remain active; scope stays unchanged | `chg04.json`, `chg04-diff.txt` |
| CHG05 | Started WO with bounded paths and behavior | Request an edit outside approved scope | Affected edit is not invoked; missing scope authority reported | `chg05.json` |
| CHG06 | Missing exact decision; only passing check, earlier unrelated approval or supplied actor assertion | Request affected transition | No transition; missing decision right reported; none of those substitutes authenticates approval | `chg06.json` |
| CHG07 | Execution delegation present at PR base with live successful exact-candidate CI; separate branch-only and stale-CI variants | Request delegated start, completion and VREC preparation | Existing DR-015 route proceeds without a fresh owner prompt; branch-only/stale variants stop; no other right inferred | `chg07.json` |
| CHG08 | Creation partly succeeds or transition application is interrupted | Resume the same request | Existing effects inspected before retry; no duplicate successful operation or unchanged decision prompt; uncertainty reported | `chg08.json`, `chg08-diff.txt` |
| CHG09 | Draft WO; fixture provides approval alone | Apply approval, then ask for the next action without start authority | WO is approved, never started or completed by implication; exact next required decision named | `chg09.json` |
| CHG10 | Required authority supplied, but current verified context absent, stale or incomplete; independently runnable evaluator | Ask the change skill to write; restore readiness through setup, then retry the same covered action | Before recovery: zero mutation calls in independent tool logs, unchanged target hashes and artifact states read back with checkpoint-free `harnessctl check`. After fresh readiness: the covered action proceeds without duplicate approval. Lifecycle projection does not establish plugin readiness. | `chg10-tool-log.json`, `chg10-hashes.json`, `chg10-state-before.json`, `chg10-state-after.json`, `chg10-context.json` |

## Property and invariant tests

CHG02–CHG06 distinguish reviewed definition content, WO scope and action-specific rights. CHG04 fixes the no-duplicate-approval expectation across ordinary code changes.

CHG10 checks PLG-CHANGE-006 as a skill instruction. It does not prove that host hooks or external controls prevent every bypass.

## Static and architecture checks

For CHG01/CHG03/CHG09, compare captured argument boundaries and states against installed command help and workflow. Reject invented CLI operations or a second policy engine.

## Security and privacy checks

CHG06/CHG07 preserve DR-003, DR-004 and DR-015 boundaries. Use synthetic actor identities without credentials.

## Performance and resilience checks

CHG03/CHG04/CHG08 evidence includes invocation and decision-prompt counts. Required checks remain enabled; record failures and interruptions without treating them as authority.

## Manual assessments

Run fixtures with released evaluator 0.16.0 and provided Python 3.11+ on Windows and Linux. Record platform and command-help identity. Verify each failure names its actual effects and one next step.

## Evidence retention

Retain named case files, fixed decisions, commands, outputs and snapshots under `evidence/WO-PLG-010/`. A later verification record binds the implementation candidate.

## Residual uncertainty

These are future cases, not completed verification. Skill instructions do not authenticate decisions or provide independent external enforcement; candidate and destination reuse cases also appear in VER-PLG-011.
