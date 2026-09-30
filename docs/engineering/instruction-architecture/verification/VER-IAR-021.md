+++
id = "VER-IAR-021"
type = "verification"
title = "Verify plugin delivery for pinned external resources"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[relations]
verifies = ["REQ-IAR-030"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T11:12:12Z"
decided_by = "mmzen"
reason = "Human mmzen: I confirm and approve. Approves the updated external-resource package and required commit-bound verification for WO-IAR-028, WO-IAR-029 and WO-IAR-030. Clarification confirmed: Ok for this plan; short bootstrap before cloning, immediate activation of the actual checkout, per-session recovery after compaction/resume and independent parallel sessions. DEC-IAR-003 separately records future release and separate adoption. Reviewed file SHA-256 cc1db38ac5365d626ce2a38be6e4d79e7fc6819ec83c36093c5096ea94e0977f."
+++

# Verify plugin delivery for pinned external resources

## Independence

Expected behavior comes from REQ-IAR-030, SPEC-IAR-016 and unchanged lifecycle/authority
contracts, not candidate output. Use an independently built candidate wheel outside
the checkout. Released 0.20.0 remains the governing evaluator for this work.

## Requirement-to-evidence matrix

| Requirement | Check | Pass condition |
| --- | --- | --- |
| REQ-IAR-030 | Bootstrap and activation after cloning | Start real Codex and Claude Code sessions in a parent directory before the checkout exists. Observe the short bootstrap, clone a prepared fixture, activate the resulting exact path and receive its complete entry before governed work. No new session or repeated human path choice is needed. The hook performs no clone, install or repository write. |
| REQ-IAR-030 | Native host delivery and recovery | Retain startup, manual and automatic compaction, and resume traces with actual host/session identity, plugin version, selected checkout, release and entry digest. Keep the host cwd in the parent. The helper and hook recover the same selection and deliver the complete entry. Repository instruction copies are absent in successor-layout fixtures. Fake event tests do not establish native support. |
| REQ-IAR-030 | Two release selections | Switch between two repositories using distinct supported releases, including legacy 0.20.0 and the successor candidate. Demonstrate correct identity before/after compaction and after changing the compatible plugin package. |
| REQ-IAR-030 | Parallel sessions and setup | Run two native sessions from the same parent with separate checkouts and distinct supported releases. Interleave activation and compaction; each retains its own checkout and release. Exercise concurrent setup for the same and different release identities with controlled contention; no running environment is replaced and no partial environment becomes usable. A new independent session cannot inherit another session's record. |
| REQ-IAR-030 | Selection failure and switching | With no selection, observe bootstrap guidance. A removed selected checkout or corrupt session record produces a delivery gap without borrowing cwd policy or another session's selection. An interrupted record replacement leaves a complete old or new record, never mixed data. Failed activation preserves a previous valid record and does not permit work on the failed target. Explicit switching/clearing affects only the selected session. |
| REQ-IAR-030 | Offline and unavailable resources | With cached resources and network unavailable, delivery succeeds. With missing or changed resources, delivery reports the exact gap and makes no install, policy fallback or repository write. |
| REQ-IAR-030 | Repeated work and delivery handoff | In the activated fixture, follow the existing procedures for a newly proposed work order and a previously authorized work order. Repeat the cycle on another selected checkout. At delivery, the instructions and evaluator result identify the exact candidate, destination and required authority for push/PR; activation is never treated as approval. Observe the authorization boundary without publishing the product branch or creating a real PR under this work order. |
| REQ-IAR-030 | Packaging and ownership | Build both host packages with the existing assembly tool. Each includes the shared bootstrap, activation/resolver adapter and required skills, contains no duplicate policy edition, and leaves user settings and unrelated plugins unchanged. Session records stay outside repositories and the replaceable plugin package. |

## Procedure and platforms

Use Windows and Linux for portable evaluator/install checks. Use actual supported
Codex and Claude Code sessions, including the Codex Windows desktop path used by
this workflow, with temporary test repositories and existing authorized test
authentication. Do not substitute CLI observations for desktop delivery. Do not
alter real credentials or saved user settings. An unavailable host is an unassessed criterion,
not a passing mock or permission to omit its required qualification.

Use disposable fixture remotes/checkouts and private test data for the clone and
session-record scenarios. Record whether each compaction was manual or automatic.
A helper replay covers adapter logic only; it cannot satisfy a native-event row.
Exercise failures at meaningful boundaries rather than every host/case combination.

This contract qualifies instruction selection and the work-to-delivery handoff.
Actual external push/PR execution keeps its existing authority and verification
requirements. A prepared handoff is not evidence that a real PR was created.

Reuse and extend the existing suites for this component. New tests cover changed
behavior and real refusal boundaries; do not mirror every branch or create a new
test framework. Record actual commands, versions, inputs, exit codes and outputs.
The work order names the focused suite and evidence destination. Run the broad
suite on the integrated candidate; repeat only after relevant changes or failures.

## Evidence and completion

Retain the matrix assessment, resource identities, command output and meaningful
failures under the selected work order's evidence directory. Bind verification
to the exact clean committed candidate with the released capture procedure.
Preparation does not provide human acceptance. Integration CI and later public
release/adoption remain separate decisions.
