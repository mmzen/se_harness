+++
id = "VREC-EVD-001"
type = "verification_record"
title = "Verification candidate for WO-EVD-001"
status = "verified"
owners = ["fixture-preparation-actor"]
created = "2026-09-10"
updated = "2026-09-10"
commit = "e7d76ee704848c0ac93d07aa014023039e2cb5cb"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-10T19:46:48Z"
prepared_by = "fixture-preparation-actor"
verified_at = "2026-09-10T19:40:00Z"
verified_by = "fixture-assurance-owner"
artifact_snapshot_sha256 = "7ee3404a96c19beed65824685cbaa269ab23af957e021dd94562b0994bfe31ba"
evidence_paths = ["docs/engineering/evidence-demo/evidence/WO-EVD-001/observations.md"]
evaluator_evidence_path = "docs/engineering/evidence-demo/evidence/VREC-EVD-001-evaluator.json"
evaluator_evidence_sha256 = "9cd3c7c8c9210b5d5438028383b92b64fb04146e56a9cd7c1096b40a94738845"

[relations]
verifies_work_order = ["WO-EVD-001"]
conforms_to = ["VER-EVD-001"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-EVD-001` to candidate commit `e7d76ee704848c0ac93d07aa014023039e2cb5cb`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
