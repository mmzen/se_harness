+++
id = "VREC-CIP-002"
type = "verification_record"
title = "Verification candidate for WO-CIP-002"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
commit = "a199133c512566c96cac229539f1bb51373ef1d0"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-26T17:13:43Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "36ae678c6ecbc5fecf1cee16edd55edf7f7baae584c08d9cb777063dc46b26c0"
evidence_paths = ["docs/engineering/ci-pipeline/evidence/WO-CIP-002/WO-CIP-002-verification.md", "docs/engineering/release-orchestration/evidence/WO-CIP-002-rehearsal-mechanism.md"]
evaluator_evidence_path = "docs/engineering/ci-pipeline/evidence/VREC-CIP-002-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-26T17:19:30Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-CIP-002"]
conforms_to = ["VER-CIP-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-26T17:19:30Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-08-26 with 'I verify VREC-CIP-002', after accepting interactively the eight recorded deviations from SPEC-CIP-001 and the WO-CIP-002 scope (Linux-only recipe-path definition (1, 2); no schema-2 record for release-record mode yet (3); classify-pypi deleted (4); shared helpers in repository_tools (5); release-candidate-replay.yml unchanged (6); two scope amendments, the second correcting WO-CIP-003's migration job (7, 8)). Hosted reading disclosed at the time of this decision: pull request #173's rehearsal executed the reusable definition; resolve, qualify complete-candidate and the unit suite passed on the hosted runner; the candidate-mode recipe replay failed in repository_tools.release_build.replay_build's workspace teardown with 'Operation not permitted' on files the containerized producer wrote as root. That defect predates this work order: every hosted run of release-candidate-replay.yml in the repository's history fails the same way, including the 2026-08-26 run on the 0.7.0 contract branch, and it affects the 0.7.0 release path. The owner chose to verify with this disclosure and to raise a corrective work order in the release-orchestration domain."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-CIP-002` to candidate commit `a199133c512566c96cac229539f1bb51373ef1d0`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
