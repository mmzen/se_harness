+++
id = "VREC-HBI-001"
type = "verification_record"
title = "Verification candidate for WO-HBI-001"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"
commit = "b92b395be484c39794bf7f6a63fe1c17c02bb65a"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-24T09:43:40Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "e31813daab1a75ba52c997f97adf6d5f1757e4f57fbf32309749e1eabf5f46d5"
evidence_paths = ["docs/engineering/hash-bound-integrity/evidence/WO-HBI-001-verification.md"]
evaluator_evidence_path = "docs/engineering/hash-bound-integrity/evidence/VREC-HBI-001-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-24T09:54:57Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-HBI-001"]
conforms_to = ["VER-HBI-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-24T09:54:57Z"
decided_by = "assurance-owner"
+++

# Verification Record

This verified record binds retained evidence for `WO-HBI-001` to candidate
commit `b92b395be484c39794bf7f6a63fe1c17c02bb65a`. The assurance owner accepted
that evidence at `2026-08-24T09:54:57Z`. Verification did not change the work
order or authorize a merge, release, publication, or deployment.

The accepted evidence discloses, rather than resolves, a `+0.09s` and about six
percent `doctor` runtime delta against `VER-HBI-001`'s "no measurable
regression", that these checks do not bind this repository's required CI gate
until a separately authorized governor upgrade, and a forward divergence in
`templates/repository/standard/gitattributes.fragment` for
`governance-migration-protocol`'s declared region. Acceptance covers the
evidence as recorded, including those disclosures.

Before the transition, every bound field was re-measured, because a verified
record can no longer be corrected. The candidate commit is reachable with a
clean worktree; `artifact_snapshot_sha256` regenerates to
`e31813daab1a75ba52c997f97adf6d5f1757e4f57fbf32309749e1eabf5f46d5` from the
managed dashboard generator at that commit; the retained evidence path is
present at the candidate and byte-identical here at
`997e1322d07ce165be2c7d7191e567e90c405c4ae2ecee1ab373885ae3d2238c`; and the
evaluator evidence matches its recorded raw digest exactly.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
