+++
id = "VREC-ECP-021"
type = "verification_record"
title = "Verification candidate for WO-ECP-006"
status = "ready"
owners = ["assurance-owner"]
created = "2026-08-29"
updated = "2026-08-29"
commit = "d62044e176e7d7a991ae0ed8eb2281af0dd29879"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-29T14:02:01Z"
prepared_by = "assurance-owner"
artifact_snapshot_sha256 = "7c287c4905f30aad1fe43887e53665efacc5d16ec60f58c9bcad5bd1c1806c27"
evidence_paths = ["docs/engineering/execution-control-plane/evidence/WO-ECP-006/WO-ECP-006-handoff.md", "docs/engineering/execution-control-plane/evidence/WO-ECP-006/handoff.json"]
evaluator_evidence_path = "docs/engineering/execution-control-plane/evidence/VREC-ECP-021-evaluator.json"
evaluator_evidence_sha256 = "41578bab531e143cd9864870c9af1495aed7465eff512571387403aa734a1f26"

[relations]
verifies_work_order = ["WO-ECP-006"]
conforms_to = ["VER-ECP-007", "VER-ECP-014"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-ECP-006` to candidate commit `d62044e176e7d7a991ae0ed8eb2281af0dd29879`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
