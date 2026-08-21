+++
id = "VREC-WEX-004"
type = "verification_record"
title = "Verification candidate for 2 work orders"
status = "superseded"
owners = ["quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"
commit = "3bef052bb6b4ae0f34b581b48b3810b0dd0bf0d6"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-21T12:08:34Z"
artifact_snapshot_sha256 = "78b683b9770d986af61911e2ae92cc26426eb966ceb3073537ce9ae3ae5cb445"
evidence_paths = ["docs/engineering/workflow-execution/evidence/WO-WEX-001-verification.md", "docs/engineering/workflow-execution/evidence/WO-WEX-002-verification.md"]
superseded_at = "2026-08-21T12:42:41Z"
supersession_authorized_by = "quality-owner"

[relations]
verifies_work_order = ["WO-WEX-001", "WO-WEX-002"]
conforms_to = ["VER-WEX-001", "VER-WEX-002"]
superseded_by = ["VREC-WEX-005"]

[[lifecycle_events]]
from = "ready"
to = "superseded"
decided_at = "2026-08-21T12:42:41Z"
decided_by = "quality-owner"
reason = "VREC-WEX-005"
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-WEX-001`, `WO-WEX-002` to candidate commit `3bef052bb6b4ae0f34b581b48b3810b0dd0bf0d6`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
