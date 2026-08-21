+++
id = "VREC-WEX-001"
type = "verification_record"
title = "Verification candidate for WO-WEX-001"
status = "superseded"
owners = ["quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"
commit = "71bb61e8f25e6a6950e4a303340bab60717a3046"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-21T06:41:37Z"
artifact_snapshot_sha256 = "abd7a2a9eaea3bd937204b01f1ddac072edb7a8c9c779c87defd195eaaef885d"
evidence_paths = ["docs/engineering/workflow-execution/evidence/WO-WEX-001-verification.md"]
superseded_at = "2026-08-21T14:10:10Z"
supersession_authorized_by = "assurance-owner"

[relations]
verifies_work_order = ["WO-WEX-001"]
conforms_to = ["VER-WEX-001"]
superseded_by = ["VREC-WEX-005"]

[[lifecycle_events]]
from = "ready"
to = "superseded"
decided_at = "2026-08-21T14:10:10Z"
decided_by = "assurance-owner"
reason = "VREC-WEX-005"
+++

# Verification Record Candidate

This historical record binds retained evidence for `WO-WEX-001` to candidate commit `71bb61e8f25e6a6950e4a303340bab60717a3046`. The assurance owner explicitly superseded it with verified aggregate `VREC-WEX-005`, which preserves `WO-WEX-001` and `VER-WEX-001` coverage.

The record was intentionally created after the candidate commit it names, avoiding self-referential commit metadata. Supersession changes only its governance interpretation; its captured candidate and evidence facts remain unchanged.
