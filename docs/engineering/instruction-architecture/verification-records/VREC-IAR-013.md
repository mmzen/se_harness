+++
id = "VREC-IAR-013"
type = "verification_record"
title = "Verification candidate for 2 work orders"
status = "verified"
owners = ["Codex"]
created = "2026-09-28"
updated = "2026-09-28"
commit = "a0435434bcfa9ce385931e2d0e64bf98cab300e1"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-28T08:30:53Z"
prepared_by = "Codex"
artifact_snapshot_sha256 = "1b1a2f5401e412dea754bb0063d13909a3417c9583efbb0a3dff163bd5d30ee2"
evidence_paths = ["docs/engineering/instruction-architecture/evidence/WO-IAR-021/delivery-envelope.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-021/raw-capture.zip", "docs/engineering/instruction-architecture/evidence/WO-IAR-021/reading-traces.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-021/review.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-021/verification-evidence.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-023/applied.patch", "docs/engineering/instruction-architecture/evidence/WO-IAR-023/review.md"]
evaluator_evidence_path = "docs/engineering/instruction-architecture/evidence/VREC-IAR-013-evaluator.json"
evaluator_evidence_sha256 = "e47384120e30c37f16266e887354cc5e0f5cb956e4d93c53fc7a5bd43ffec9c2"

verified_at = "2026-09-28T08:36:01Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-IAR-021", "WO-IAR-023"]
conforms_to = ["VER-IAR-015"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-28T08:36:01Z"
decided_by = "assurance-owner"
reason = "Human repository owner mmzen: \"I verify VREC-IAR-013\". Codex applies this human assurance decision to candidate a0435434bcfa9ce385931e2d0e64bf98cab300e1 for WO-IAR-021 and WO-IAR-023 with the reviewed evidence and documented limits. The selected 0.19.0 evaluator encodes the assurance right as assurance-owner; mmzen is the decision-maker. Only VREC-IAR-013 changes state. This does not verify WO-IAR-020 or authorize publication, merge, release or real-profile adoption."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-IAR-021`, `WO-IAR-023` to candidate commit `a0435434bcfa9ce385931e2d0e64bf98cab300e1`. Preparation uses each selected work order's recorded execution approval. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
