+++
id = "VREC-AUT-002"
type = "verification_record"
title = "Verification candidate for WO-AUT-002"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"
commit = "0b023637d4b95e5187acaa6438313b416e0cda47"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-25T19:45:05Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "16c4f5895ed151830449d29679b4e5ef558ee47624cce80449db65cc497e76a6"
evidence_paths = ["docs/engineering/artifact-authoring/evidence/WO-AUT-002/WO-AUT-002-verification.md", "docs/engineering/artifact-authoring/evidence/WO-AUT-002/verification-method-mapping.json"]
evaluator_evidence_path = "docs/engineering/artifact-authoring/evidence/VREC-AUT-002-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-25T19:48:30Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-AUT-002"]
conforms_to = ["VER-AUT-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-25T19:48:30Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-08-25 with 'I verify VREC-AUT-002 as assurance owner', after accepting interactively the four recorded deviations from SPEC-AUT-001: the string verification_method stays W-AUT-004 and the migration is built but not applied, both deferred to the governor-upgrade work order (1); four values (REQ-REB-004, -011, -014, -018) match no mapping rule and are the steward's decision at application time (2); in-scope paths left unchanged (3); the predicates are not yet enforced by the released governor on this root (4). Verification rests on the retained evidence with the Linux figure pending the pull-request lane."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-AUT-002` to candidate commit `0b023637d4b95e5187acaa6438313b416e0cda47`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
