+++
id = "VREC-REB-017"
type = "verification_record"
title = "Verification candidate for WO-REB-021"
status = "rejected"
owners = ["engineering-owner"]
created = "2026-08-24"
updated = "2026-08-24"
commit = "f9225f887d23303be01ba7d73219c53e0fec0f95"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-24T14:45:37Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "fdccdff0a94a3bce5d77e3f6d75034bcd4a3d3f26586bf94f3951f2a1035a9b5"
evidence_paths = ["docs/engineering/released-evaluator-boundary/evidence/WO-REB-021-entry-point-safety.md"]
evaluator_evidence_path = "docs/engineering/released-evaluator-boundary/evidence/VREC-REB-017-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

rejected_at = "2026-08-24T17:15:42Z"
rejected_by = "engineering-owner"
rejection_reason = "Accountable assurance decision under DR-VREC-DECIDE. The candidate this record binds, f9225f887d23303be01ba7d73219c53e0fec0f95, does not meet the VER-REB-010 pass criteria: the pinned ubuntu lane measured 764 tests with failures=33 and errors=38 at that commit. VREC-REB-019 is the authorized replacement and binds bfc08f0477475a1a128f9db68ba9b56685c5c10f, where the same lane reports 770 tests and OK (skipped=3). Supersession was refused with E002 because a superseded record must carry verified_at and this record was never verified, so the rejected history is retained rather than reopened or silently replaced."
[relations]
verifies_work_order = ["WO-REB-021"]
conforms_to = ["VER-REB-010"]

[[lifecycle_events]]
from = "ready"
to = "rejected"
decided_at = "2026-08-24T17:15:42Z"
decided_by = "engineering-owner"
reason = "Accountable assurance decision under DR-VREC-DECIDE. The candidate this record binds, f9225f887d23303be01ba7d73219c53e0fec0f95, does not meet the VER-REB-010 pass criteria: the pinned ubuntu lane measured 764 tests with failures=33 and errors=38 at that commit. VREC-REB-019 is the authorized replacement and binds bfc08f0477475a1a128f9db68ba9b56685c5c10f, where the same lane reports 770 tests and OK (skipped=3). Supersession was refused with E002 because a superseded record must carry verified_at and this record was never verified, so the rejected history is retained rather than reopened or silently replaced."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-REB-021` to candidate commit `f9225f887d23303be01ba7d73219c53e0fec0f95`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
