+++
id = "VREC-RSK-002"
type = "verification_record"
title = "Verification candidate for WO-RSK-002"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"
commit = "2d64df052482b0626c6c2c691ae72926877e1eea"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-25T17:58:03Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "0dfc8358219442d22a43a8fff818590acc51aaf1b22c9a79e6e19717e06b4599"
evidence_paths = ["docs/engineering/risk-management/evidence/WO-RSK-002/WO-RSK-002-verification.md"]
evaluator_evidence_path = "docs/engineering/risk-management/evidence/VREC-RSK-002-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-25T17:59:11Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-RSK-002"]
conforms_to = ["VER-RSK-002"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-25T17:59:11Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-08-25 with 'I verify VREC-RSK-002 as assurance owner', after accepting interactively the two recorded deviations from SPEC-RSK-002: the doctor check named risk-policy with C-RSK-001 in its detail (1), and the explicit risk-raise effect class in the skill helpers, profiles, and contracts (2). Verification rests on the retained evidence with the Linux figure taken from the pull-request lane of PR #158 (candidate source evidence: pass)."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-RSK-002` to candidate commit `2d64df052482b0626c6c2c691ae72926877e1eea`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
