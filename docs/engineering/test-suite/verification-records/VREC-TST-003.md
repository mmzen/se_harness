+++
id = "VREC-TST-003"
type = "verification_record"
title = "Verification candidate for WO-TST-003"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
commit = "2d2b4bdaf29fdcc6eddb93e4a7b28bfa0e340e9e"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-26T20:14:45Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "a2ded23fdc2df68b2e13728d5859e3899ed157cb41e50ab2c443e2136b8e59ba"
evidence_paths = ["docs/engineering/test-suite/evidence/WO-TST-003/WO-TST-003-verification.md"]
evaluator_evidence_path = "docs/engineering/test-suite/evidence/VREC-TST-003-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-26T20:16:22Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-TST-003"]
conforms_to = ["VER-TST-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-26T20:16:22Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-08-26 with 'I verify VREC-TST-003'; no deviation was recorded. Hosted reading at the time of this decision: pull request #181's rehearsal job (the definition in candidate mode with SE_HARNESS_TEST_SCALE=full) was still in progress; the workstation run of the suite at full scale through the runner reported 969 tests, OK, 24 skips."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-TST-003` to candidate commit `2d2b4bdaf29fdcc6eddb93e4a7b28bfa0e340e9e`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
