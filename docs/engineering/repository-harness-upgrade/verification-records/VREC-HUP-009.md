+++
id = "VREC-HUP-009"
type = "verification_record"
title = "Verification candidate for WO-HUP-010"
status = "verified"
owners = ["Mathieu Meadele"]
created = "2026-08-29"
updated = "2026-08-29"
commit = "6f21c98db61db45909fbaee7dcaca5e556da2592"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-29T10:55:08Z"
prepared_by = "Mathieu Meadele"
artifact_snapshot_sha256 = "6af5e08ec0494c3fb423dfb881dd9b683304e0fab7343ba181a94c8896cde94b"
evidence_paths = ["docs/engineering/repository-harness-upgrade/evidence/WO-HUP-010-evaluator-upgrade.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-010/WO-HUP-010-handoff.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-010/handoff.json"]
evaluator_evidence_path = "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-009-evaluator.json"
evaluator_evidence_sha256 = "41578bab531e143cd9864870c9af1495aed7465eff512571387403aa734a1f26"

verified_at = "2026-08-29T10:56:13Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-HUP-010"]
conforms_to = ["VER-HUP-010"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-29T10:56:13Z"
decided_by = "assurance-owner"
reason = "Verified by the accountable assurance owner on 2026-08-29, 'I verify VREC-HUP-009 as assurance owner'. Re-measured immediately before this transition: bound commit 6f21c98 is an ancestor of the branch tip with a clean worktree; WO-HUP-010 is implemented; the evaluator packet matches its recorded digest. The retained evidence shows the root moved from exact public 0.9.0 to exact public 0.10.0 by one upgrade --apply from a digest-verified wheel-file install outside the checkout, lock naming 0.10.0 with archive e2f80772 and payload 723c98ec, plan 6 update, replay 61 unchanged, 0.10.0 validate 0 errors, doctor 0 FAIL, released-root 143/143, the suite on the moved root failing nothing a same-commit control does not on Windows and OK on Linux, all thirteen lanes passing at e869c90 under the 0.10.0 root's own gate including the governor transition assessment, and the managed lane green at the implemented head fc8ce6e \u2014 VER-ECP-009 scenario 6 met, the first completion since #253 that did not turn it red. Every reading, the packet and the handoff check included, was produced by the released evaluator on the Windows checkout. VER-HUP-010's pass conditions are met. This verifies WO-HUP-010 only; it releases and publishes nothing."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-HUP-010` to candidate commit `6f21c98db61db45909fbaee7dcaca5e556da2592`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
