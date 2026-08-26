+++
id = "VREC-TST-002"
type = "verification_record"
title = "Verification candidate for WO-TST-002"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
commit = "b5b062d4db971e5183a0f9f37695d8300d9533f2"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-26T20:08:49Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "2df812b96f8745a9b8e7d7e283d6b492e676edc3d27e72c940e40514ee2d2fff"
evidence_paths = ["docs/engineering/test-suite/evidence/WO-TST-002/WO-TST-002-verification.md"]
evaluator_evidence_path = "docs/engineering/test-suite/evidence/VREC-TST-002-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-26T20:10:05Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-TST-002"]
conforms_to = ["VER-TST-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-26T20:10:05Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-08-26 with 'I verify VREC-TST-002', after accepting interactively the three recorded deviations: eleven fixtures converted rather than about twenty-five (1); a cache-naming collision fixed before commit (2); the serial saving measured at 5 s rather than the predicted 100 s, the benefit being in the parallel runs, 80 to 56 s at eight workers and 114 to 86 s at four (3). The hosted reading of pull request #179 is read from its candidate-source suite step."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-TST-002` to candidate commit `b5b062d4db971e5183a0f9f37695d8300d9533f2`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
