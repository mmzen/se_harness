+++
id = "VREC-SHB-001"
type = "verification_record"
title = "Verification candidate for WO-SHB-002"
status = "ready"
owners = ["quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"
commit = "94ef1ac10420d79c61aa43c916d2a1bae15d650a"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-15T09:23:57Z"
artifact_snapshot_sha256 = "d74924829798300bddaa635ef52e769535ddbc882f3d05913749bbc42f0fe026"
evidence_paths = ["docs/engineering/self-hosting-boundary/evidence/WO-SHB-002-verification.md"]

[relations]
verifies_work_order = ["WO-SHB-002"]
conforms_to = ["VER-SHB-002"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-SHB-002` to candidate commit `94ef1ac10420d79c61aa43c916d2a1bae15d650a`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Commit-bound bootstrap acceptance

The candidate was exported from the bound commit and built as non-promotable wheel SHA-256 `94f1c0a96769312691453ab8b1b1b71bde35955f0ff71f5029b1712fde43b197`. Two fresh Python 3.11.9 executions passed all 11 required black-box scenarios and produced byte-identical canonical manifests with SHA-256 `af126d5c62596aa931a740f615294adc92fce418c43b42fc95d9f440e55ef62a`.

This is candidate-owned bootstrap evidence: the installed verifier was the same candidate wheel because selected governor 0.2.1 predates `accept-candidate`. It demonstrates package behavior and deterministic replay, but it is not independent governor assessment and must not be treated as self-verification. Hosted three-plane CI and accountable review remain required before transition.
