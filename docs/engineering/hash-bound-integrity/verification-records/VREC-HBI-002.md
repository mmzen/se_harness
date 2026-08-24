+++
id = "VREC-HBI-002"
type = "verification_record"
title = "Verification candidate for WO-HBI-002"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"
commit = "4e94f7c36fdcf52004fdea69f823723e813a24e3"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-24T11:37:36Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "920f9d0af255919c4e0d0dd1fdc1caa2fbfeff5a4719c6c82eb741ffdae7d418"
evidence_paths = ["docs/engineering/hash-bound-integrity/evidence/WO-HBI-002-verification.md"]
evaluator_evidence_path = "docs/engineering/hash-bound-integrity/evidence/VREC-HBI-002-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-24T11:49:51Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-HBI-002"]
conforms_to = ["VER-HBI-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-24T11:49:51Z"
decided_by = "assurance-owner"
reason = "The assurance owner accepted the retained evidence for WO-HBI-002 on 2026-08-24. Every bound field was re-measured immediately before this transition: candidate commit 4e94f7c is reachable with a clean worktree, the artifact snapshot re-derives to 920f9d0a in a full clone at that commit with a matching directory basename, the bound evidence blob is 14408 bytes at e8b4df47 both at the candidate and here, and the evaluator evidence matches its recorded raw digest over 873 LF-only bytes. Acceptance covers the evidence as recorded, including its disclosures. It authorizes no merge, release, publication or deployment."
+++

# Verification Record

This verified record binds retained evidence for `WO-HBI-002` to candidate commit
`4e94f7c36fdcf52004fdea69f823723e813a24e3`. The assurance owner accepted that
evidence at `2026-08-24T11:49:51Z`. Verification did not change the work order or
authorize a merge, release, publication, or deployment.

The accepted evidence covers the change that makes every hashing caller for a
declared class take its mode from that class, resolves
`.engineering-harness.lock`'s raw-versus-canonical divergence in favour of the
canonical mode, and recognizes `WO-HUP-002`'s digest as a legacy newline variant
and reports it as one rather than rewriting it. Acceptance also covers the
bounded scope amendment the engineering owner granted during implementation,
which added `se_harness/installer.py` for the single key that reports the match.

The evidence discloses, rather than resolves, one pre-existing Windows suite
failure that `WO-HBI-003` repairs and that reproduces unchanged on `main` at
`d07523f`; two locally chosen lock canonicalizations left in out-of-scope
scripts, `scripts/validate_engineering_artifacts.py` and
`scripts/validate_governor_transition.py`, both of which agree with the declared
mode today; the duplication between `LOCK_RELATIVE` and `installer.LOCK_NAME`,
which a test pins; two tests that skip where the historical lock object is
absent, as a depth-1 checkout produces; that measurement was taken on one
Windows workstation; and that these checks do not bind this repository's
required CI gate until a separately authorized governor upgrade. Acceptance
covers the evidence as recorded, including those disclosures.

Before the transition, every bound field was re-measured, because a verified
record can no longer be corrected. The candidate commit is reachable with a
clean worktree; `artifact_snapshot_sha256` re-derives to
`920f9d0af255919c4e0d0dd1fdc1caa2fbfeff5a4719c6c82eb741ffdae7d418` from the
managed dashboard generator in a full clone at that commit with a matching
directory basename, over 720 artifacts with 0 errors; the retained evidence path
is present at the candidate and byte-identical here at
`e8b4df47fc390e701d38e913509d4e8e4e1cda0a3bb9fa0e361ccddc9f667c74`, 14408 bytes;
and the evaluator evidence matches its recorded raw digest exactly over its 873
LF-only bytes, whose archive and payload digests equal the lock's evaluator
identity for public `0.6.0`.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
