+++
id = "VREC-AUT-001"
type = "verification_record"
title = "Verification candidate for WO-AUT-001"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"
commit = "d4309c345aeba1ad32ce4f1ce4b24be8c6cbcf3c"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-25T19:07:50Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "4e8f18521c732142c42fda3e0e8fc4999c6aae87b026e81282f221b47c8c8a3e"
evidence_paths = ["docs/engineering/artifact-authoring/evidence/WO-AUT-001/WO-AUT-001-verification.md"]
evaluator_evidence_path = "docs/engineering/artifact-authoring/evidence/VREC-AUT-001-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-25T19:08:51Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-AUT-001"]
conforms_to = ["VER-AUT-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-25T19:08:51Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-08-25 with 'I verify VREC-AUT-001 as assurance owner', after accepting interactively the three recorded deviations from SPEC-AUT-001: guidance subsections written for some artifact types only (1); the harness-draft-change contract version 1.0.2 also claimed by PR #158, to be resolved at merge by a bump to 1.0.3 with a regenerated vector (2); a synthetic statement in place of REQ-AEX-008's literal text in the test (3). Verification rests on the retained evidence with the Linux figure pending the pull-request lane."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-AUT-001` to candidate commit `d4309c345aeba1ad32ce4f1ce4b24be8c6cbcf3c`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
