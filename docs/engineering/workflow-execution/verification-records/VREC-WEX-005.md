+++
id = "VREC-WEX-005"
type = "verification_record"
title = "Verification candidate for 2 work orders"
status = "ready"
owners = ["quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"
commit = "38c06152ec571c8c6a959b1f8799e62858593e4b"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-21T12:37:31Z"
artifact_snapshot_sha256 = "7fba8cc79701c78c334ab5e624785242e5be1b7c11ffb2524119351566739096"
evidence_paths = ["docs/engineering/workflow-execution/evidence/WO-WEX-001-verification.md", "docs/engineering/workflow-execution/evidence/WO-WEX-002-verification.md"]

[relations]
verifies_work_order = ["WO-WEX-001", "WO-WEX-002"]
conforms_to = ["VER-WEX-001", "VER-WEX-002"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-WEX-001`, `WO-WEX-002` to candidate commit `38c06152ec571c8c6a959b1f8799e62858593e4b`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
