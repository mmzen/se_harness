+++
id = "VREC-ECP-033"
type = "verification_record"
title = "Verification candidate for WO-ECP-030"
status = "verified"
owners = ["assurance-owner"]
created = "2026-09-07"
updated = "2026-09-07"
commit = "43f83010dae23952193aa390b54cf1724e7abd4b"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-07T21:54:52Z"
prepared_by = "assurance-owner"
artifact_snapshot_sha256 = "d7d910cab959ccb82c487f7cb6e42dcb5465b4914b150b42324fa3aee976a7e9"
evidence_paths = ["docs/engineering/execution-control-plane/evidence/WO-ECP-030/WO-ECP-030-handoff.md", "docs/engineering/execution-control-plane/evidence/WO-ECP-030/handoff.json"]
evaluator_evidence_path = "docs/engineering/execution-control-plane/evidence/VREC-ECP-033-evaluator.json"
evaluator_evidence_sha256 = "e2cd0929fd42d0634d3bf23a73408665bac8ae473b98c81439dbffb828bff951"

verified_at = "2026-09-07T22:00:10Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-ECP-030"]
conforms_to = ["VER-ECP-024"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-07T22:00:10Z"
decided_by = "assurance-owner"
reason = "Verified on 2026-09-07 by the accountable assurance owner with the words 'i verify both' (DR-VREC-DECIDE, together with VREC-ECP-034), after the record was presented: bound to candidate commit 43f8301 (WO-ECP-030 implemented), to the retained evidence WO-ECP-030-handoff.md and handoff.json, and to the exact 0.16.0 evaluator evidence. Hosted lanes on PR #392 at the record commit 7ae163e: every lane that had finished passes, including the candidate-package lane; the Windows migration lane was running at the decision. The merge of PR #392 remains the owner's decision."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-ECP-030` to candidate commit `43f83010dae23952193aa390b54cf1724e7abd4b`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
