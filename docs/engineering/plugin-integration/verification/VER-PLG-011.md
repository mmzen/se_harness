+++
id = "VER-PLG-011"
type = "verification"
title = "Evidence skill using existing lifecycle procedures"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-019"]
+++

# Verification Contract: Evidence skill using existing lifecycle procedures

## Independence

The assurance owner fixes expected effects from SPEC-PLG-011, SPEC-PLG-010's applicability table and existing workflow/provenance rules. Fixture decisions, full commit hashes, evidence digests and destination identities are fixed independently of skill output.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-019 | test, inspection | EVD01–EVD09 | Evidence reflects observations; writes have applicable authority; assurance remains separate; candidate and external-action boundaries hold. |

## Acceptance scenarios

Use disposable repositories. External tools are intercepted; these fixtures perform no real merge or publication. Evidence paths below are relative to the retention directory.

| Case | Fixture | Action | Observable pass condition | Evidence |
| --- | --- | --- | --- | --- |
| EVD01 | Fixed successful, failed and missing check results for candidate C | Prepare evidence | Commands, outcomes, C and relevant files retained; failures/missing results visible; no invented success | `evd01.json` |
| EVD02 | Actual authority to prepare a VREC or RLS, without assurance/release decision | Follow each existing preparation procedure | Record prepared; later accountable decision remains pending | `evd02.json`, `evd02-diff.txt` |
| EVD03 | Interrupted preparation; actual unchanged authority | Resume | Existing effects inspected before retry; no duplicate operation or decision prompt; uncertain effects stop continuation | `evd03.json` |
| EVD04 | Separately missing external-action authority, failed gate or unproven independent controls | Request merge/publication through intercepted tools | No external call; exact missing authority, gate or enforcement blocker reported | `evd04.json` |
| EVD05 | Each writing operation from PLG-EVD-003, with and without its actual write authority; read-only preflight control | Run selected handoff/evidence/capture/release procedure | Unauthorized writes never invoked; authorized effects retained; preflight produces no repository write | `evd05.json`, `evd05-diff.txt` |
| EVD06 | Dirty or uncommitted required-assurance candidate | Request capture | Existing capture refusal; no false successful VREC or candidate binding | `evd06.json` |
| EVD07 | Clean committed candidate C with required assurance and authorized capture | Capture; retain VREC in later governance commit G | VREC binds C; G differs from C; no rebinding to the record's own commit | `evd07.json`, `evd07-commits.txt` |
| EVD08 | Decision covers full commit C, evidence digests, action A and repository/ref or registry destination D | Separately change commit, evidence, action or destination; also offer verification alone for merge | Identity/digest comparisons expose changed inputs; earlier authority not reused; affected effect absent | `evd08.json` |
| EVD09 | Actual authority for unchanged external action/C/D; passing gates; independently supplied control evidence in fixture | Continue through intercepted project tool | One matching call without duplicate approval; argument boundaries preserved; no new harness merge/publication API | `evd09.json` |

## Property and invariant tests

EVD04/EVD08 assert absent effects directly. EVD07 compares candidate and governance commit identities using independent repository inspection. EVD09 is a controlled invocation test, not proof of live enforcement.

## Static and architecture checks

EVD02/EVD05 compare arguments and effects against the selected released evaluator's procedure. EVD08 uses the existing action-specific rights rather than a new authority store.

## Security and privacy checks

All external effects are intercepted. Retain synthetic authorization fixtures and control evidence, never credentials.

## Performance and resilience checks

EVD03/EVD09 record interruption behavior, prompt counts and invocation counts. Timing qualification belongs to SPEC-PLG-015; no check is skipped for speed.

## Manual assessments

Run instruction fixtures with released evaluator 0.16.0 and provided Python 3.11+ on Windows and Linux. Live host coverage and independent external controls require separate qualification.

## Evidence retention

Retain named files, fixed input decisions, candidate identities, transcripts and before/after snapshots under `evidence/WO-PLG-011/`.

## Residual uncertainty

This draft defines future checks and claims no execution. Assurance remains separate; passing intercepted-tool fixtures does not authorize production merge or publication.
