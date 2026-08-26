+++
id = "VREC-CIP-005"
type = "verification_record"
title = "Verification candidate for WO-CIP-005"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
commit = "04ef9f9157f025f8538f18d572489452de023c21"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-26T20:32:42Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "7fb37fef19560f1fd8133282ed65ca7dad30d96981de9d271de14f03f32f1c55"
evidence_paths = ["docs/engineering/ci-pipeline/evidence/WO-CIP-005/WO-CIP-005-verification.md"]
evaluator_evidence_path = "docs/engineering/ci-pipeline/evidence/VREC-CIP-005-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-26T20:34:15Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-CIP-005"]
conforms_to = ["VER-CIP-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-26T20:34:15Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-08-26 with 'I verify VREC-CIP-005', after accepting interactively the three recorded deviations: the predicate bound to QG-G5-RELEASE-PREPARATION (1); exemptions in release_unit.untraced_exemptions (2); two-segment work-order ids admitted (3). The predicate runs in the evaluator; no hosted reading is needed."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-CIP-005` to candidate commit `04ef9f9157f025f8538f18d572489452de023c21`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
