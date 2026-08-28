+++
id = "VREC-ECP-013"
type = "verification_record"
title = "Verification candidate for WO-ECP-002"
status = "ready"
owners = ["Mathieu Meadele"]
created = "2026-08-28"
updated = "2026-08-28"
commit = "5eea42becbe62fab4f61c8dc50f060a91ec17a19"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-28T21:27:17Z"
prepared_by = "Mathieu Meadele"
artifact_snapshot_sha256 = "e2321f08befe6d9641cbe7e704511ae2bb8a2bc536929f240d15e2a26c6db9a3"
evidence_paths = ["docs/engineering/execution-control-plane/evidence/WO-ECP-002/WO-ECP-002-handoff.md", "docs/engineering/execution-control-plane/evidence/WO-ECP-002/handoff.json"]
evaluator_evidence_path = "docs/engineering/execution-control-plane/evidence/VREC-ECP-013-evaluator.json"
evaluator_evidence_sha256 = "8d217a429db288836d69c843e6f0017c0be29a2b743f589a7fe28bfa8b1cf560"

[relations]
verifies_work_order = ["WO-ECP-002"]
conforms_to = ["VER-ECP-002"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-ECP-002` to candidate commit `5eea42becbe62fab4f61c8dc50f060a91ec17a19`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
