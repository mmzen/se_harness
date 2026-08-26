+++
id = "VREC-TST-001"
type = "verification_record"
title = "Verification candidate for WO-TST-001"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
commit = "d1df05d72608103aaff37af97610812b3751e8f2"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-26T19:46:51Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "cf1261ed30023e69f21931ff152bd6df8a10a3c9c0da693c13e99fb67dd1e227"
evidence_paths = ["docs/engineering/test-suite/evidence/WO-TST-001/WO-TST-001-verification.md"]
evaluator_evidence_path = "docs/engineering/test-suite/evidence/VREC-TST-001-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-26T19:48:19Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-TST-001"]
conforms_to = ["VER-TST-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-26T19:48:19Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-08-26 with 'I verify VREC-TST-001', after accepting interactively the four recorded deviations: the release qualification does not set the scale marker yet (1); ProcessPoolExecutor rather than multiprocessing.Pool (2); the scope amendment for the pinned suite-step assertion (3); a failed import counted as one run test in both runs (4). Hosted reading at the time of this decision: on pull request #178 the candidate-source suite step (python scripts/run_tests.py --workers 4 --scale full) completed in 32 seconds with success, against about six to seven minutes before; workstation readings: canonical serial 335 s and the runner at one worker 332 s with the same verdict (965 tests, 24 skips), 114 s at four workers with the full scale sizes, 80 s at eight."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-TST-001` to candidate commit `d1df05d72608103aaff37af97610812b3751e8f2`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
