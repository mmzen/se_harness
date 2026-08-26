+++
id = "VREC-CIP-001"
type = "verification_record"
title = "Verification candidate for WO-CIP-001"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
commit = "25a245f4b6d1cfc7436fe7844ac49e9fed356bc1"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-26T15:41:52Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "8854086954ef406622bf7dcc4de4cf4a23591268dd6b9f5451148feba77b330f"
evidence_paths = ["docs/engineering/ci-pipeline/evidence/WO-CIP-001/WO-CIP-001-verification.md"]
evaluator_evidence_path = "docs/engineering/ci-pipeline/evidence/VREC-CIP-001-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-26T15:49:07Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-CIP-001"]
conforms_to = ["VER-CIP-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-26T15:49:07Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-08-26 with 'I verify VREC-CIP-001', after accepting interactively the five recorded deviations from SPEC-CIP-001: the integration package keeps its own two builds (SPEC-IPK-001 rule 1) (1) and its retention job (rule 5) (2); the rehearsal runs twice per platform (REQ-REB-017) (3); the cross-platform comparison runs only where the integration lane runs (4); the managed workflow changed in the template only (5). Verification rests on the retained evidence; the hosted readings of VER-CIP-001 scenarios 1 and 2 come from pull request #171, whose runs were queued behind a GitHub Actions outage at the time of this decision: the pull-request runs were created and no push-event run exists for the repository-owned workflows."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-CIP-001` to candidate commit `25a245f4b6d1cfc7436fe7844ac49e9fed356bc1`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
