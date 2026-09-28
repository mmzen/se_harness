+++
id = "VREC-IAR-014"
type = "verification_record"
title = "Verification candidate for 3 work orders"
status = "verified"
owners = ["Codex"]
created = "2026-09-28"
updated = "2026-09-28"
commit = "e2fe4fa3cf0a7549423260fbaba5ba1806631495"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-28T09:18:57Z"
prepared_by = "Codex"
artifact_snapshot_sha256 = "cc99671cc76a95818d97f52b0f8d610fa4e131f81a10bd4122396493b11b95f8"
evidence_paths = ["docs/engineering/instruction-architecture/evidence/WO-IAR-022/evidence-index.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-022/final-package-comparison.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-022/governance-capture.zip", "docs/engineering/instruction-architecture/evidence/WO-IAR-022/protected-files.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-022/raw-capture.zip", "docs/engineering/instruction-architecture/evidence/WO-IAR-022/review.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-024/review.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-024/shared-evidence.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-025/applied.patch", "docs/engineering/instruction-architecture/evidence/WO-IAR-025/review.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-025/shared-evidence.json"]
evaluator_evidence_path = "docs/engineering/instruction-architecture/evidence/VREC-IAR-014-evaluator.json"
evaluator_evidence_sha256 = "e47384120e30c37f16266e887354cc5e0f5cb956e4d93c53fc7a5bd43ffec9c2"

verified_at = "2026-09-28T09:21:27Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-IAR-022", "WO-IAR-024", "WO-IAR-025"]
conforms_to = ["VER-IAR-017"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-28T09:21:27Z"
decided_by = "assurance-owner"
reason = "Human repository owner mmzen: \"I verify VREC-IAR-014\". Codex applies this human assurance decision to candidate e2fe4fa3cf0a7549423260fbaba5ba1806631495 for WO-IAR-022, WO-IAR-024 and WO-IAR-025 with the reviewed evidence and documented limits. The selected 0.19.0 evaluator encodes the assurance right as assurance-owner; mmzen is the decision-maker. Only VREC-IAR-014 changes state. This does not verify WO-IAR-020 or authorize push, merge, release, publication or real host adoption."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-IAR-022`, `WO-IAR-024`, `WO-IAR-025` to candidate commit `e2fe4fa3cf0a7549423260fbaba5ba1806631495`. Preparation uses each selected work order's recorded execution approval. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
