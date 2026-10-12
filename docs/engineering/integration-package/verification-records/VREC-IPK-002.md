+++
id = "VREC-IPK-002"
type = "verification_record"
title = "Verification candidate for WO-IPK-002"
status = "verified"
owners = ["Codex"]
created = "2026-10-12"
updated = "2026-10-12"
commit = "938126a437514451166af7b66db1d9996abbbd68"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-10-12T08:21:38Z"
prepared_by = "Codex"
artifact_snapshot_sha256 = "36bc91cb062f2ad1034ee788c4f19d04c3d5703e1bf9e5c244b17e6aae10c4a8"
evidence_paths = ["docs/engineering/integration-package/evidence/WO-IPK-002/WO-IPK-002-handoff.md", "docs/engineering/integration-package/evidence/WO-IPK-002/candidate-relationship.json", "docs/engineering/integration-package/evidence/WO-IPK-002/ci-evidence-inventory.json", "docs/engineering/integration-package/evidence/WO-IPK-002/ci-evidence.zip", "docs/engineering/integration-package/evidence/WO-IPK-002/handoff-completion.zip", "docs/engineering/integration-package/evidence/WO-IPK-002/handoff.json", "docs/engineering/integration-package/evidence/WO-IPK-002/local-checks-inventory.json", "docs/engineering/integration-package/evidence/WO-IPK-002/local-checks.zip", "docs/engineering/integration-package/evidence/WO-IPK-002/verification-assessment.md"]
evaluator_evidence_path = "docs/engineering/integration-package/evidence/VREC-IPK-002-evaluator.json"
evaluator_evidence_sha256 = "5396a2aa38a2e0e1c858c04f63697d13a2f7aae16e977256b931a8d4f9c0c899"

verified_at = "2026-10-12T08:42:06Z"
verified_by = "mmzen"
[relations]
verifies_work_order = ["WO-IPK-002"]
conforms_to = ["VER-IPK-002"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-10-12T08:42:06Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"Verify result\" to the published VREC-IPK-002 request for candidate 938126a437514451166af7b66db1d9996abbbd68 and its unchanged retained evidence in PR #543. Accepts only WO-IPK-002 under VER-IPK-002. Does not verify remaining HAG work or authorize merge or release."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-IPK-002` to candidate commit `938126a437514451166af7b66db1d9996abbbd68`. Preparation uses each selected work order's recorded execution approval. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
