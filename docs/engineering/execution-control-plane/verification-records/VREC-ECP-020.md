+++
id = "VREC-ECP-020"
type = "verification_record"
title = "Verification candidate for WO-ECP-017"
status = "ready"
owners = ["assurance-owner"]
created = "2026-08-29"
updated = "2026-08-29"
commit = "94991fe38cca7982a5214ff57e554af4895adbde"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-29T12:48:02Z"
prepared_by = "assurance-owner"
artifact_snapshot_sha256 = "472e4ee6b3cc7b0eefee64177d6c111f340fb39948f8017a5161067d326d3d04"
evidence_paths = ["docs/engineering/execution-control-plane/evidence/WO-ECP-017/WO-ECP-017-handoff.md", "docs/engineering/execution-control-plane/evidence/WO-ECP-017/handoff.json"]
evaluator_evidence_path = "docs/engineering/execution-control-plane/evidence/VREC-ECP-020-evaluator.json"
evaluator_evidence_sha256 = "41578bab531e143cd9864870c9af1495aed7465eff512571387403aa734a1f26"

[relations]
verifies_work_order = ["WO-ECP-017"]
conforms_to = ["VER-ECP-011", "VER-ECP-013"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-ECP-017` to candidate commit `94991fe38cca7982a5214ff57e554af4895adbde`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
