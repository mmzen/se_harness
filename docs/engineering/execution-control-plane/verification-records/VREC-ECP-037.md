+++
id = "VREC-ECP-037"
type = "verification_record"
title = "Verification candidate for WO-ECP-033"
status = "verified"
owners = ["quality-owner"]
created = "2026-09-08"
updated = "2026-09-08"
commit = "5bc0710fc476912b4e0cfab1cd5146e46b9642de"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-08T13:54:54Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "0e69deb5114ad0f487939e4fa0fd17d901f5f6042632f47ce7bba6976cd41e8b"
evidence_paths = ["docs/engineering/execution-control-plane/evidence/WO-ECP-033/WO-ECP-033-handoff.md"]
evaluator_evidence_path = "docs/engineering/execution-control-plane/evidence/VREC-ECP-037-evaluator.json"
evaluator_evidence_sha256 = "e2cd0929fd42d0634d3bf23a73408665bac8ae473b98c81439dbffb828bff951"

verified_at = "2026-09-08T14:07:08Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-ECP-033"]
conforms_to = ["VER-ECP-025"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-08T14:07:08Z"
decided_by = "assurance-owner"
reason = "Verified on 2026-09-08 by the accountable assurance owner with the words 'i verify both' (DR-VREC-DECIDE, together with VREC-ECP-036), after the record was presented: bound to candidate commit 5bc0710f of wo/ecp-033-codes-contract-tables (PR #400, 13 checks green), retaining the WO-ECP-033 handoff evidence whose handoff check passes all nine predicates over 32 paths, the Windows suite at its baseline (1324 tests), validate 1399 artifacts with 0 errors, DEC-ECP-002 accepted for ECP-PRM-027, and no recorded digest moved."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-ECP-033` to candidate commit `5bc0710fc476912b4e0cfab1cd5146e46b9642de`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Standing deviations

Accepted deviations standing on the selected work at this candidate; each names the rule it departs from and is retained here for the assurance decision:

- `DEC-ECP-002` against `SPEC-ECP-023#ECP-PRM-027`
