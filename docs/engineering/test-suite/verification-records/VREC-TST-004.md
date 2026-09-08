+++
id = "VREC-TST-004"
type = "verification_record"
title = "Verification candidate for WO-TST-004"
status = "verified"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"
commit = "9e5b0e59f69a6a6801b74c0032f10a07c9ae3579"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-08T15:27:20Z"
prepared_by = "assurance-owner"
artifact_snapshot_sha256 = "af3f1f6eba98ccb3c047e637cf8410432bec5c0af8dbc920b97fe089c8a36fad"
evidence_paths = ["docs/engineering/test-suite/evidence/WO-TST-004/WO-TST-004-handoff.md"]
evaluator_evidence_path = "docs/engineering/test-suite/evidence/VREC-TST-004-evaluator.json"
evaluator_evidence_sha256 = "e2cd0929fd42d0634d3bf23a73408665bac8ae473b98c81439dbffb828bff951"

verified_at = "2026-09-08T15:45:22Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-TST-004"]
conforms_to = ["VER-TST-002"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-08T15:45:22Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-09-08 by selecting the presented option 'Verify only' (DR-VREC-DECIDE), after the seven disclosures of the WO-TST-004 evidence packet were presented. The record binds candidate commit 9e5b0e59 (WO-TST-004 implemented), VER-TST-002 and the retained handoff evidence; the released 0.16.0 evaluator prepared it and validates the graph with 0 errors, 73 warnings (the main baseline), 0 advisories; PR #402 at d65edcdd (main 0e7d718b merged in) has all 13 lanes green. Readings against main at 13a70218: 1,054 tests discovered for 1,054 defined (was 1,282 for 1,020); one invoke, one git, one write, one formal; no direct git launch, by-path load, import-time sys.path insert or cross-import of test modules; the failure set equals the two Windows baseline names; the Linux suite step 45 s against 51 s. The merge of PR #402 remains the owner's decision."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-TST-004` to candidate commit `9e5b0e59f69a6a6801b74c0032f10a07c9ae3579`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
