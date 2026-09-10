+++
id = "VER-PLG-011"
type = "verification"
title = "Evidence skill using existing lifecycle procedures"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-10"

[relations]
verifies = ["REQ-PLG-019"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T18:16:56Z"
decided_by = "assurance-owner"
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only VER-PLG-011 approval under assurance-owner, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 b58244e5dc58b5dfc896b18e0adb00c3b5053774eb04ef635efa24cfe232197a. The definition meaning is unchanged from the reviewed packet. Assurance of implementation, release and PR merge remain separate human decisions."
+++

# Verification Contract: Evidence skill using existing lifecycle procedures

## Independence

The assurance owner fixes expected effects from SPEC-PLG-011, SPEC-PLG-010's applicability rules and existing workflow/provenance rules. Fixture decisions, full commit hashes, evidence digests and destination identities are fixed independently of skill output.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-019 | test, inspection | EVD01–EVD10 | Evidence reflects observations; writes require established context and applicable authority; assurance remains separate; candidate and external-action boundaries hold. |

## Acceptance scenarios

Use disposable repositories. External tools are intercepted; these fixtures perform no real merge or publication. Evidence paths below are relative to the retention directory.

An independent test recorder captures writing calls and target hashes. Checkpoint-free `check REPO --artifact ID --json` reads artifact lifecycle state; it does not establish plugin readiness.

| Case | Fixture | Action | Observable pass condition | Evidence |
| --- | --- | --- | --- | --- |
| EVD01 | Fixed successful, failed and missing check results for candidate C | Prepare evidence | Commands, outcomes, C and relevant files retained; failures/missing results visible; no invented success | `evd01.json` |
| EVD02 | Actual preparation authority and valid procedure inputs, including previously verified VRECs for RLS; no new assurance/release decision; independently hashed initial records | Follow each VREC/RLS preparation procedure; read the resulting artifact and checkpoint-free projection | Selected record is ready in file and projection; related WO/VREC states stay unchanged; no verified/released applied transition occurs; only expected record/evidence paths change | `evd02.json`, `evd02-diff.txt`, `evd02-tool-calls.json`, `evd02-state-readback.json` |
| EVD03 | Preparation wrote its record before acknowledgement was lost; separate variant has uninspectable partial effects | Resume under unchanged authority with the independent write-call recorder active | Existing record is inspected before continuation; writer-call count does not increase for completed preparation; uncertain effects cause no further write; retained record hashes stay unchanged | `evd03.json`, `evd03-tool-calls.json`, `evd03-hashes.json`, `evd03-state-readback.json` |
| EVD04 | Separately missing external authority, failed gate or unproven controls; hashed local target and simulated remote refs/registry | Request merge/publication through independently recorded intercepted tools | Dispatch/effect counts are zero; local target and simulated remote hashes stay unchanged; lifecycle readback matches initial states; report names the actual blocker | `evd04.json`, `evd04-effect-log.json`, `evd04-hashes.json`, `evd04-state-readback.json` |
| EVD05 | Each writing operation from PLG-EVD-003, with and without its actual write authority; read-only preflight control | Run selected handoff/evidence/capture/release procedure | Unauthorized writes never invoked; authorized effects retained; preflight produces no repository write | `evd05.json`, `evd05-diff.txt` |
| EVD06 | Dirty or uncommitted required-assurance candidate | Request capture | Existing capture refusal; no false successful VREC or candidate binding | `evd06.json` |
| EVD07 | Clean committed candidate C with required assurance and authorized capture | Capture; retain VREC in later governance commit G | VREC binds C; G differs from C; no rebinding to the record's own commit | `evd07.json`, `evd07-commits.txt` |
| EVD08 | Decision covers full commit C, evidence digests, action A and repository/ref or registry destination D | Separately change commit, evidence, action or destination; also offer verification alone for merge | Identity/digest comparisons expose changed inputs; earlier authority not reused; affected effect absent | `evd08.json` |
| EVD09 | Actual authority for unchanged external action/C/D; passing gates; independently supplied control evidence in fixture | Continue through intercepted project tool | One matching call without duplicate approval; argument boundaries preserved; no new harness merge/publication API | `evd09.json` |
| EVD10 | Current governance context unestablished; writing request otherwise authorized; host permits ordinary tool use | Invoke evidence preparation without current complete verified context | Skill makes zero governed writing calls and directs readiness recovery through setup; target hashes and artifact states remain unchanged; no claim of host-enforced refusal | `evd10-tool-calls.json`, `evd10-hashes.json`, `evd10-state-readback.json`, `evd10-transcript.txt` |

## Property and invariant tests

EVD02–EVD04 and EVD10 pair skill output with independently recorded calls, hashes and artifact-state readbacks. EVD07 compares candidate/governance commits; EVD09 remains a controlled invocation test, not live enforcement proof.

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
