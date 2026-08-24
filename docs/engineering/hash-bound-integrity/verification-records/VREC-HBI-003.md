+++
id = "VREC-HBI-003"
type = "verification_record"
title = "Verification candidate for WO-HBI-003"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"
commit = "c8fbaddb1297fe4f989f482e03a1092affd845ff"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-24T18:11:10Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "f6b22eb0ad234c90188a7ddf9c21abcb135307b49de9ffa9602f60429abce076"
evidence_paths = ["docs/engineering/hash-bound-integrity/evidence/WO-HBI-003-verification.md"]
evaluator_evidence_path = "docs/engineering/hash-bound-integrity/evidence/VREC-HBI-003-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-24T18:30:57Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-HBI-003"]
conforms_to = ["VER-HBI-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-24T18:30:57Z"
decided_by = "assurance-owner"
reason = "The accountable assurance owner accepted the retained evidence for WO-HBI-003 on 2026-08-24 through the statement 'i accept the verification record'. Every bound field was re-measured immediately before this transition, because a verified record can no longer be corrected: candidate commit c8fbadd is an ancestor of the branch tip with a clean worktree; artifact_snapshot_sha256 re-derives to f6b22eb0 in a full clone at that commit with a matching directory basename, over 794 artifacts with 0 errors and 50 maintenance warnings, where governing doctor exits 0 with 87 PASS and 0 FAIL; the bound evidence blob is 20641 bytes at 0b266797 both at the candidate and at the tip; and the evaluator packet matches its recorded raw digest over 873 CR-free bytes. Acceptance covers the evidence as recorded, including its disclosures: the guard is a unit test rather than a doctor check and no consumer inherits it, five of seven patterns exceed REQ-HBI-001's digest-bound trigger, an existing worktree does not re-materialize the sixteen paths, the clone matrix covers only autocrlf=true on one Windows workstation, the in-tree doctor skew is inherited from main, and one hosted red is unexplained. It authorizes no merge, release, publication or deployment."
+++

# Verification Record

This verified record binds retained evidence for `WO-HBI-003` to candidate commit
`c8fbaddb1297fe4f989f482e03a1092affd845ff`. The assurance owner accepted that evidence
at `2026-08-24T18:30:57Z`. Verification did not change the work order or authorize a
merge, release, publication, or deployment.

## The decision, and what was re-measured to take it

The accountable assurance owner accepted the retained evidence on 2026-08-24 through
the statement `i accept the verification record`. The lifecycle event above carries that
decision.

Every bound field was re-measured immediately before the transition, because a verified
record can no longer be corrected and this was the last commit in which any of its
figures could have been fixed. The candidate commit is an ancestor of the branch tip and
the worktree was clean; `artifact_snapshot_sha256` re-derives to
`f6b22eb0ad234c90188a7ddf9c21abcb135307b49de9ffa9602f60429abce076` in a full clone at
that commit with a matching directory basename, over 794 artifacts with 0 errors and 50
maintenance warnings, where the governing `0.6.0` evaluator's `doctor` exits 0 with 87
PASS and 0 FAIL; the bound evidence blob is 20641 bytes at
`0b2667978e10cc2922a94045fca4279700f78354eedf2b3ac4a42d7df70e810b` both at the candidate
and at the tip; and the evaluator packet matches its recorded raw digest over 873
CR-free bytes. Every value was unchanged from preparation.

Acceptance covers the evidence as recorded, including every disclosure in the section
below. It authorizes no merge, release, publication or deployment, and the manual
acceptances `VER-HBI-001` requires from the security, quality and repository owners
remain separate and outstanding.

## What the candidate evidence covers

`WO-HBI-003` declares seven byte rules in the owner-controlled region of
`.gitattributes` for sixteen tracked files whose exact bytes the candidate suite
compares, and adds `ByteExactSurfaceTests` so that a missing rule is a failing test
rather than a platform-dependent surprise. It exists because `WO-RLO-005`'s
publication-rehearsal lane measured the release orchestrator failing candidate
qualification on `windows-2022`: the orchestrator creates the checkout it qualifies
with `git worktree add`, which inherits `core.autocrlf=true`, so byte-exact assertions
read converted bytes there. The exposure is live rather than theoretical, because the
Windows leg's steps are gated on `distribution_schema == '1'` and `RLS-SEH-012`
declares distribution schema 1.

No committed byte changes. The index already held LF on all sixteen paths, and
`.github/workflows/publish-pypi.yml` is byte-unchanged; repairing the orchestrator's
checkout configuration instead was available and was not taken.

## Assurance-relevant limits of the candidate

The evidence states these; they are surfaced here so the assurance decision is taken
against them rather than around them.

- **The guard is a unit test, not a `doctor` check**, and these sixteen paths are in no
  declared hash-bound class. A consumer installation inherits neither the rules, which
  are `repository`-region, nor the guard, which lives in this repository's suite. That
  boundary is intended and the domain `README.md` amendment states it.
- **Five of the seven patterns fall outside `REQ-HBI-001`'s digest-bound trigger.** The
  work order delivers more than the requirement obliges, which is disclosed rather than
  absorbed and is why two artifacts were amended.
- **An existing worktree does not re-materialize.** Git rewrites a path on checkout only
  when its blob changes, and these blobs are unchanged, so a tree that materialized
  them under CRLF before the rule existed keeps the converted bytes; a clone taken at
  the default branch and then checked out onto the candidate fails 17 assertions. This
  does not reach the release orchestrator, which starts from an empty directory, and
  the guard fails rather than passing silently. Measured in the evidence.
- **The clone matrix is incomplete.** Only `core.autocrlf=true` was clone-checked, on one
  Windows workstation with one Git version. `input` and `false` were not, and no Linux
  clone was taken.
- **`build_recipe_sha256` stays in `unbound_digest_fields`.** Whether it should become a
  declared class so `doctor` rather than a unit test guards that recipe's bytes is open
  and unmeasured, and is tracked as repository issue 142 on the owner's decision of
  2026-08-24.
- **The in-tree `doctor` reports 84 PASS / 18 FAIL.** The control at `fc97103` reports the
  same 18 with identical names, so it is inherited candidate-versus-released skew. The
  governing released `0.6.0` evaluator from outside the checkout reports 87 PASS / 0
  FAIL.
- **One hosted red is unexplained.** The rehearsal reported eleven failing tests where
  this evidence measures ten; the eleventh exists at `fc97103` and passes in the local
  control. Two candidate causes were not separated, and the evidence says so rather
  than choosing one.

## What was measured for this record, and by what

Every bound field above was derived by the released `se-harness==0.6.0` evaluator run
from `C:\Users\mathi\se_harness_eval_060`, outside the checkout, and each was then
re-derived independently in a fresh full clone taken directly at this candidate with a
matching directory basename:

- `commit` is reachable and the worktree was clean at preparation in both.
- `artifact_snapshot_sha256` re-derives to
  `f6b22eb0ad234c90188a7ddf9c21abcb135307b49de9ffa9602f60429abce076` in that clone.
  The governing validator reports 794 artifacts with 0 errors and 50 maintenance
  warnings at this candidate, and governing `doctor` exits 0 with 87 PASS and 0 FAIL.
- The bound evidence path is present at the candidate at
  `0b2667978e10cc2922a94045fca4279700f78354eedf2b3ac4a42d7df70e810b`, 20641 bytes as
  the committed blob. That is the blob digest, not the on-disk digest: `.md` files under
  `docs/engineering/` carry no `eol=lf` rule, so a `core.autocrlf=true` checkout
  materializes this file with CR bytes while the index holds LF. The distinction is the
  work order's own subject and is not glossed here.
- `evaluator_evidence_sha256` matches its packet exactly over 873 bytes containing no
  CR, held LF by the managed `docs/engineering/**/evidence/*.json text eol=lf` rule.
  It is byte-identical to `VREC-HBI-002`'s packet, because the same evaluator venv
  produces the same evidence; the candidate binding lives in `commit` and in the
  snapshot, not in this digest.
- Pull request #141 reports 18 passing checks and 3 `skipping` at this candidate, with
  `mergeStateStatus` `CLEAN`. That is where the Linux half is exercised; the evidence
  file cannot record it, because those checks run over the commit that contains it.

The candidate commit was moved once during preparation and deliberately so. A record
prepared over `9742280` was discarded uncommitted when the clone re-derivation surfaced
the two fresh-clone facts above, because amending evidence a record already binds is
not available and a `ready` record cannot be superseded. Nothing bound this repository
at any point in that sequence.

## Scope of the decision that was taken

Verifying this record accepted the retained evidence as recorded, including every
disclosure above. It does not approve a merge, a release, a publication, a deployment,
a tag, a distribution build, or a governor adoption, and it does not discharge the
manual acceptances `VER-HBI-001` requires from the security, quality and repository
owners, which remain separate and outstanding.

The record is intentionally created after the candidate commit it names, avoiding
self-referential commit metadata.
