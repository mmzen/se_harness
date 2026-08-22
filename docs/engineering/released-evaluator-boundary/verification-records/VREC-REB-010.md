+++
id = "VREC-REB-010"
type = "verification_record"
title = "Verification candidate for WO-REB-014"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-22"
updated = "2026-08-22"
commit = "827ddc197f8cb801d9b817bf03fd51e301279de1"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-22T21:07:44Z"
artifact_snapshot_sha256 = "2b0820e6522e3d580b8e1641588e176f919dceb9925115e697201a89d44b592f"
evidence_paths = ["docs/engineering/released-evaluator-boundary/evidence/WO-REB-014-windows-bash-path.md"]
verified_by = "quality-owner"

[relations]
verifies_work_order = ["WO-REB-014"]
conforms_to = ["VER-REB-006"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-22T21:08:11Z"
decided_by = "quality-owner"
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-REB-014` to candidate commit `827ddc197f8cb801d9b817bf03fd51e301279de1`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

On 2026-08-22, the accountable assurance authority accepted this exact record under the repository owner's explicit authorization to finalize release 0.6.0. Review reconciled the bound commit and snapshot, retained Windows runner/runtime, exact Git-Bash failure, four bounded path conversions, unchanged action upload contract, complete 452-test qualification, current and predecessor graph results, and absence of external mutation. Automation did not infer acceptance from test success.

Exact released `se-harness==0.5.0` prepared this record in the deterministic two-omission compatibility view, which passed with 663 artifacts, zero errors, and 49 maintenance warnings. Complete current validation passed separately with 665 artifacts and zero errors.

The historical `verified_at` field records predecessor capture time while the proposal was prepared; the lifecycle event and `verified_by` field record the separate accountable verification decision.
