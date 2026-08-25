+++
id = "VREC-TCM-001"
type = "verification_record"
title = "Verification candidate for WO-TCM-002"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"
commit = "1b94c82329e8cfd94ad61601384448c4dc1ed7e3"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-25T09:09:23Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "72eec6fa8547da28a412ec08848ca4848c7c8dc15f3ab2dd7ee2813b752219c6"
evidence_paths = ["docs/engineering/technical-communication/evidence/WO-TCM-001/WO-TCM-002-verification.md"]
evaluator_evidence_path = "docs/engineering/technical-communication/evidence/VREC-TCM-001-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-25T09:11:18Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-TCM-002"]
conforms_to = ["VER-TCM-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-25T09:11:18Z"
decided_by = "assurance-owner"
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-TCM-002` to candidate commit `1b94c82329e8cfd94ad61601384448c4dc1ed7e3`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
