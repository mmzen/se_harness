+++
id = "VREC-HUP-017"
type = "verification_record"
title = "Verification candidate for WO-HUP-018"
status = "verified"
owners = ["quality-owner"]
created = "2026-09-09"
updated = "2026-09-09"
commit = "8f50f3aa913cc87c832655d47bf1ce184d4906d0"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-09T10:03:37Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "1c3658c3f17f490afa0fa4dd9675946063df344d39347cae4773b935d3b59e7e"
evidence_paths = ["docs/engineering/repository-harness-upgrade/evidence/WO-HUP-018/WO-HUP-018-handoff.md"]
evaluator_evidence_path = "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-017-evaluator.json"
evaluator_evidence_sha256 = "44d4b74d9febe03a0828dfeee8cd8322fd02db74ff866d7191440e17164e7abb"

verified_at = "2026-09-09T10:15:21Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-HUP-018"]
conforms_to = ["VER-HUP-018"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-09T10:15:21Z"
decided_by = "assurance-owner"
reason = "Verified on 2026-09-09 by the accountable assurance owner by selecting the presented option 'I verify VREC-HUP-017', after the record was presented: bound to candidate 8f50f3aa of governance/hup-018-adopt-0-17-0 (PR #427, 17 checks green), retaining the WO-HUP-018 handoff evidence whose handoff check passes every predicate over 21 paths; the root is exact public 0.17.0 by one transaction from the isolated wheel-file environment (archive 305c7cbc79f87baa76ea3bea939b134999f9cad3bfdfa0b4c9c2fd2d9caacced, payload dd48b16b69d90a04412f458c756876ec22a687c99282075e69d0f58316c43405), every VER-HUP-018 reading passed under exact 0.17.0, the Windows suite on the moved root equals its same-commit 0.16.0 control, and the governor-transition lane assessed the real 0.16.0 to 0.17.0 move with one transaction document and RLS-SEH-026 supplying the wheel."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-HUP-018` to candidate commit `8f50f3aa913cc87c832655d47bf1ce184d4906d0`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
