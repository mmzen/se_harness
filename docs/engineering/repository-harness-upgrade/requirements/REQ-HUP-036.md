+++
id = "REQ-HUP-036"
type = "requirement"
title = "Prove complete-graph operation under the 0.17.0 root and take the carried obligations into the root"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-09"
updated = "2026-09-09"
statement = "THE SYSTEM SHALL pass validation, doctor, qualification, identical Explorer generations, the suite at baseline and the managed lane under the new root, its configuration reduced and its ignore block hash-marked."
verification_method = ["test", "inspection"]
priority = "must"
source = "REQ-HUP-034's proof pattern for the previous adoption; SPEC-DST-026 rule DST-CFG-015 and SPEC-DST-027 rule DST-MWF-014, carried forward by WO-DST-025 and WO-DST-026 to this work order; the rehearsal of 2026-09-09 on the moved root"

[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-09T09:04:33Z"
decided_by = "repository-owner"
reason = "Approved by the accountable repository owner on 2026-09-09 by selecting the presented option 'Approve all five (Recommended)', after reviewing PR #426 (REQ-HUP-035, REQ-HUP-036, SPEC-HUP-018, VER-HUP-018, WO-HUP-018) and the rehearsal of the 0.17.0 root adoption on a throwaway LF clone of main at e855cc9a."
+++

# Requirement: Prove complete-graph operation under the 0.17.0 root and take the carried obligations into the root

## In plain words

A root move is proven by what the new evaluator reads over the whole graph
and by the test suite staying where it was. This move also discharges the
two obligations wave 5 carried to it.

## Why

The 0.17.0 gate read the rehearsal clone as 0.16.0 did: no error, no
advisory, an identical Explorer twice. `WO-DST-025` and `WO-DST-026` changed
the template copies only and left the root to this adoption. The candidate
must move to 0.18.0, or the derivation fails closed.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The moved root | Every 0.17.0 reading passes. The derivation yields the 0.17.0 to 0.18.0 pair. The configuration holds five keys; the ignore block sits between hash markers. The suite's failure set equals the control's. | The work order stops; the branch is amended or abandoned under the owner's decision |

## Examples

### Normal

**Given** the moved root, the candidate at 0.18.0 and the edits applied,

**When** the readings and the suite run,

**Then** every reading passes. The suite reads its baseline with one
workstation error and the platform skips.

### Failure

**Given** the candidate still at 0.17.0,

**When** the evaluator facts are derived,

**Then** the derivation fails closed with `PRE008`.

## Open decisions

None.
