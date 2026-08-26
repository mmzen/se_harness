+++
id = "VREC-CIP-004"
type = "verification_record"
title = "Verification candidate for WO-CIP-004"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
commit = "fce0383325f6b15192eda4828406757b9c62b426"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-26T18:52:55Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "29939243c27581157012ad99b0e4371951555060de27aab0b0dfdd445b18c594"
evidence_paths = ["docs/engineering/ci-pipeline/evidence/WO-CIP-004/WO-CIP-004-verification.md", "docs/engineering/ci-pipeline/evidence/WO-CIP-004/release-unit-v0.6.0-e98b788.json"]
evaluator_evidence_path = "docs/engineering/ci-pipeline/evidence/VREC-CIP-004-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-26T18:54:24Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-CIP-004"]
conforms_to = ["VER-CIP-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-26T18:54:24Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-08-26 with 'I verify VREC-CIP-004', after accepting interactively the seven recorded deviations from SPEC-CIP-001 and the WO-CIP-004 scope: E-CIP-001 emitted by the command rather than the git-free managed validator, with an approval-time predicate as a follow-up (1); the 0.7.0 unit not reproducible from commit trailers, so 0.7.0 keeps its allow-list contract and the first unit frozen by candidate commit is the next one (2); template changes in the standard template only (3); declared packaged-surface prefixes (4); validator unchanged (5); the two unbound commits re-based onto main after the stack merged (6); a pre-existing brittle test on main fixed here (7). Verification rests on the retained evidence; the command is local and needs no hosted reading."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-CIP-004` to candidate commit `fce0383325f6b15192eda4828406757b9c62b426`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
