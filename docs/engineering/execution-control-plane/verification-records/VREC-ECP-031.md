+++
id = "VREC-ECP-031"
type = "verification_record"
title = "Verification candidate for WO-ECP-027"
status = "ready"
owners = ["assurance-owner"]
created = "2026-09-07"
updated = "2026-09-07"
commit = "7e6a50180e990580aa72b7cc4890366594172e51"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-07T20:05:32Z"
prepared_by = "assurance-owner"
artifact_snapshot_sha256 = "02a25313015a44ba71f6691482da56cd4fdf21e7f93b432ea8cee6b0f89f6814"
evidence_paths = ["docs/engineering/execution-control-plane/evidence/WO-ECP-027/WO-ECP-027-handoff.md", "docs/engineering/execution-control-plane/evidence/WO-ECP-027/handoff.json"]
evaluator_evidence_path = "docs/engineering/execution-control-plane/evidence/VREC-ECP-031-evaluator.json"
evaluator_evidence_sha256 = "e2cd0929fd42d0634d3bf23a73408665bac8ae473b98c81439dbffb828bff951"

[relations]
verifies_work_order = ["WO-ECP-027"]
conforms_to = ["VER-ECP-023"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-ECP-027` to candidate commit `7e6a50180e990580aa72b7cc4890366594172e51`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
