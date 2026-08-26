+++
id = "VREC-ADS-001"
type = "verification_record"
title = "Verification candidate for WO-ADS-001"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"
commit = "eda9e6d516bf331fb048f945072471bcc85b3228"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-25T11:16:25Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "a3fc89ba0ef4367ebd0808191616798a693dc544cb685ae884d9866edc940a97"
evidence_paths = ["docs/engineering/agent-directive-surface/evidence/WO-ADS-001/WO-ADS-001-verification.md"]
evaluator_evidence_path = "docs/engineering/agent-directive-surface/evidence/VREC-ADS-001-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-25T11:19:37Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-ADS-001"]
conforms_to = ["VER-ADS-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-25T11:19:37Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-08-25 with 'I verify VREC-ADS-001 as assurance owner', after accepting interactively: the third corrective kind 'response' (deviation 1); the router scope section after the invariants without a second HRN-003 occurrence and the manifest prefix still listing routed policies (deviations 7 and 4); W-ADS-001 and W-ADS-002 reported as blockers rather than a warning tier (deviation 6); and verification on retained evidence with Scenario 8 not run and the Linux figure pending the pull-request lane."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-ADS-001` to candidate commit `eda9e6d516bf331fb048f945072471bcc85b3228`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
