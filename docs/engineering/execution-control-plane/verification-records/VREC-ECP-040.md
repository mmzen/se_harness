+++
id = "VREC-ECP-040"
type = "verification_record"
title = "Verification candidate for WO-ECP-036"
status = "verified"
owners = ["quality-owner"]
created = "2026-09-08"
updated = "2026-09-08"
commit = "308cbcf829a0d1f7d6714e487b30675af373d099"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-08T19:41:32Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "27a727bf057430d9e0118f8867f125f83df576e06b9da6e83611d310bbdf880a"
evidence_paths = ["docs/engineering/execution-control-plane/evidence/WO-ECP-036/WO-ECP-036-handoff.md"]
evaluator_evidence_path = "docs/engineering/execution-control-plane/evidence/VREC-ECP-040-evaluator.json"
evaluator_evidence_sha256 = "e2cd0929fd42d0634d3bf23a73408665bac8ae473b98c81439dbffb828bff951"

verified_at = "2026-09-08T19:44:36Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-ECP-036"]
conforms_to = ["VER-ECP-026"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-08T19:44:36Z"
decided_by = "assurance-owner"
reason = "Verified on 2026-09-08 by the accountable assurance owner with the words 'i verify all 3 verification records' (DR-VREC-DECIDE, together with the other two wave 3 records), after the record was presented: bound to candidate commit 308cbcf8 of wo/ecp-036-seams (PR #414, lanes green), retaining the WO-ECP-036 handoff evidence whose handoff check passes every predicate over 43 paths, the validator, the generator and the compliance module split along their seams, no private cross-module import, no function above complexity 60, every recorded output byte-identical to the group B code, the Windows suite at its baseline and validate with 0 errors."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-ECP-036` to candidate commit `308cbcf829a0d1f7d6714e487b30675af373d099`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
