+++
id = "VREC-EVD-001"
type = "verification_record"
title = "Verification candidate for WO-EVD-001"
status = "ready"
owners = ["fixture-preparation-actor"]
created = "2026-09-10"
updated = "2026-09-10"
commit = "e7d76ee704848c0ac93d07aa014023039e2cb5cb"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-10T20:00:09Z"
prepared_by = "fixture-preparation-actor"
artifact_snapshot_sha256 = "aaca3f1d94e990a5d709602f5e8d2f6064f961b3414cf21ad3a4a7bdee897780"
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
