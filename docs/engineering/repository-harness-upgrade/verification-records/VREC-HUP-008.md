+++
id = "VREC-HUP-008"
type = "verification_record"
title = "Verification candidate for WO-HUP-009"
status = "verified"
owners = ["Mathieu Meadele"]
created = "2026-08-29"
updated = "2026-08-29"
commit = "1108a0e9ed9f3a616942270517a5ad659cd2e5e7"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-29T07:24:17Z"
prepared_by = "Mathieu Meadele"
artifact_snapshot_sha256 = "723b8fff1ee683f48333d4f3af9ba4814762e4809b052ddd0b5b9ff620b57152"
evidence_paths = ["docs/engineering/repository-harness-upgrade/evidence/WO-HUP-009-evaluator-upgrade.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-009/WO-HUP-009-handoff.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-009/handoff.json"]
evaluator_evidence_path = "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-008-evaluator.json"
evaluator_evidence_sha256 = "e78737d57a52748c0381cddd376cd8627a9328f600210a957e5ddd308ef48d91"

verified_at = "2026-08-29T07:25:28Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-HUP-009"]
conforms_to = ["VER-HUP-009"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-29T07:25:28Z"
decided_by = "assurance-owner"
reason = "Verified by the accountable assurance owner on 2026-08-29, 'I verify VREC-HUP-008 as assurance owner'. Re-measured immediately before this transition: bound commit 1108a0e is an ancestor of the branch tip with a clean worktree; WO-HUP-009 is implemented; the evaluator packet matches its recorded digest e78737d5. The retained evidence shows the root moved from exact public 0.8.0 to exact public 0.9.0 by one upgrade --apply from a digest-verified wheel-file install outside the checkout, lock naming 0.9.0 with archive c4b56175 and payload e74ad2ae, plan 5 update, replay 61 unchanged, 0.9.0 validate 0 errors, doctor 0 FAIL, released-root 143/143, the suite on the moved root failing nothing a same-commit control does not, and all thirteen hosted lanes passing at 5957139 and 10e1994 including the governor transition assessment and the unconditional scope gate; the packet was rebound from an LF tree after the first push blocked on QGP-G4I-EVIDENCE, and it discloses that and the Windows backslash refusal (issue #254) as observations outside the work order. VER-HUP-009's pass conditions are met. This verifies WO-HUP-009 only; it releases and publishes nothing."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-HUP-009` to candidate commit `1108a0e9ed9f3a616942270517a5ad659cd2e5e7`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
