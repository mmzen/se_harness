+++
id = "VREC-HBI-004"
type = "verification_record"
title = "Verification candidate for WO-HBI-004"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"
commit = "74c770cd089cb6e9a3945165404743f10b413240"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-25T06:57:32Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "c4956a0733a8f5e995d96018e7cbf7beb6daea01f9d8611ba3a34fc02c5111bf"
evidence_paths = ["docs/engineering/hash-bound-integrity/evidence/WO-HBI-004-verification.md"]
evaluator_evidence_path = "docs/engineering/hash-bound-integrity/evidence/VREC-HBI-004-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-25T07:15:10Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-HBI-004"]
conforms_to = ["VER-HBI-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-25T07:15:10Z"
decided_by = "assurance-owner"
reason = "The accountable assurance owner accepted the retained evidence for WO-HBI-004 on 2026-08-25 through the statement 'I accept both verification record'. Every bound field was re-measured immediately before this transition, because a verified record can no longer be corrected: candidate commit 74c770cd089cb6e9a3945165404743f10b413240 is an ancestor of the branch tip with a clean worktree; artifact_snapshot_sha256 re-derives to c4956a0733a8f5e995d96018e7cbf7beb6daea01f9d8611ba3a34fc02c5111bf in a fresh full clone at that commit with the matching directory basename se_harness-hbi004, over 823 artifacts with 0 errors and 50 maintenance warnings, where the governing 0.6.0 evaluator's doctor exits 0 with 87 PASS and 0 FAIL; the bound evidence blob is 17093 bytes at 7fc210fb83ea44b61ad7d2ca6ad65dd450798171 both at the candidate and at the tip; and the evaluator packet matches its recorded raw digest fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962 over 873 CR-free bytes. Every generated field was byte-identical to preparation. Acceptance covers the evidence as recorded, including its twelve disclosures: the record binds a commit taken from main rather than the already-merged branch tip and the pull request must therefore be merged as a true merge; implementation departed from the owner's framing twice, a tree rule rather than a *.yaml rule and a tracked-set inventory rather than an assertion-derived one; VER-HBI-001's residual is narrowed rather than closed; the reserved-name fix's failing platform is not reproducible on this workstation, so its windows-2022 corroboration comes from WO-RLO-005's rehearsal lane on another branch; no Linux measurement is local and none runs CPython 3.11; and the in-tree doctor's 28 FAIL are inherited candidate-versus-released boundary skew with a FAIL set identical to the control's. It authorizes no merge, release, publication or deployment."
+++

# Verification Record

This verified record binds retained evidence for `WO-HBI-004` to candidate commit
`74c770cd089cb6e9a3945165404743f10b413240`. The assurance owner accepted that evidence at
`2026-08-25T07:15:10Z`. Verification did not change the work order or authorize a merge,
release, publication, or deployment.

The record was intentionally created after the candidate commit it names, avoiding
self-referential commit metadata.

The repository owner authorized preparation on 2026-08-25 with the statement `you can set
WO-RLO-005 and WO-HBI-004 as implemented, and prepare the verification record(s)`.
`WO-HBI-004` was already `implemented`, so no lifecycle transition was needed and none was
made. Every provenance field above was produced by the released `0.6.0` evaluator's
`capture-verification` run from outside the checkout, at commit
`74c770cd089cb6e9a3945165404743f10b413240` with a clean worktree.

## The decision, and what was re-measured to take it

The accountable assurance owner accepted both prepared records on 2026-08-25 through the
statement `I accept both verification record`. The lifecycle event above carries that
decision for this one, and the transition was applied by the released `0.6.0` evaluator's
`transition --apply` rather than by editing the frontmatter.

Every bound field was re-measured immediately before the transition, because a verified
record can no longer be corrected and this was the last commit in which any of its figures
could have been fixed. The candidate commit is an ancestor of the branch tip and the
worktree was clean; `artifact_snapshot_sha256` re-derives to
`c4956a0733a8f5e995d96018e7cbf7beb6daea01f9d8611ba3a34fc02c5111bf` in a fresh full clone at
that commit with the matching directory basename `se_harness-hbi004`, over 823 artifacts
with 0 errors and 50 maintenance warnings, where the governing `0.6.0` evaluator's `doctor`
exits 0 with 87 `PASS` and 0 `FAIL`; the bound evidence blob is 17093 bytes at
`7fc210fb83ea44b61ad7d2ca6ad65dd450798171` both at the candidate and at the tip; and the
evaluator packet matches its recorded raw digest over 873 CR-free bytes. Re-running
`capture-verification` in that clone reproduced every generated field byte-identically;
only `prepared_at`, a timestamp, differed.

Acceptance covers the evidence as recorded, including every disclosure in the section
below. It authorizes no merge, release, publication or deployment. Merging pull request
#146 is a separate owner act, and it must be a true merge: a squash or a rebase would
orphan `74c770c`, and a verified record can never be re-pointed at a later commit.

## What the candidate evidence covers

`WO-HBI-004` replaces three per-extension byte rules with one tree rule,
`templates/repository/standard/.agents/skills/** text eol=lf`, and changes
`ByteExactSurfaceTests` to derive its inventory from the tracked set — four named files plus
every tracked path under one declared prefix — instead of from the declared patterns. It
also fixes a reserved-name test whose precondition held on this workstation and not on
hosted `windows-2022`. No product source file changes, and no committed blob under
`templates/` changes: the rule alters what a checkout presents, not what the repository
stores.

The work order exists because a guard passed while the surfaces it protected were
converted. That is re-measured in the bound evidence from a control checkout at `ee8aea1`
rather than carried across from the implementation evidence: three `agents/openai.yaml`
files are `i/lf w/crlf attr/` there while the previous `ByteExactSurfaceTests` reports 3
tests `OK`. At the candidate all fifteen tracked files under the tree resolve
`text eol=lf`, and a fresh detached worktree at `1d459cf` with `core.autocrlf=true`
materializes all fifteen as LF unaided.

Falsifiability is re-measured twice at the candidate, and both mutations are reverted with
the restored state re-measured afterwards:

- `VER-HBI-001` scenario 9, the tree rule replaced by `WO-HBI-003`'s three per-extension
  rules: 8 failures across 3 tests, including the extension-independence case for a file
  with an extension no rule has ever named.
- `VER-HBI-001` scenario 8 on a named file, the `se_harness/agent_contract.json` rule
  removed: 2 failures.

Gates at the candidate, in a `core.autocrlf=true` checkout created with `git worktree add`,
which is the construction the release orchestrator uses: full suite 811 tests OK with 22
skipped against 807 tests and 3 failures in the control at `ee8aea1`; governing validator
PASS at 822 artifacts, 0 errors and 50 maintenance warnings, matched by the candidate
validator; governing `doctor` exit 0 over 87 checks with 0 `FAIL` and
`managed:.gitattributes: unchanged`; governing `preflight --phase review` PASS;
`validate_release_distributions.py` PASS.

## Assurance-relevant limits of the candidate

The bound evidence file states twelve disclosures. The ones that bear directly on an
assurance decision:

- The record binds a commit taken from `main` at `1d459cf`, not the work order's branch tip
  `74bb0e3`. That branch merged through pull request #145 before preparation was
  authorized, and a record binds a commit at which the evidence it binds is tracked. The
  candidate carries the packet exactly as merged plus the evidence file.
- Merging the pull request that carries this record must be a true merge. A squash or a
  rebase would orphan the bound commit, and a verified record can never be re-pointed at a
  later commit.
- Implementation departed from the owner's framing twice, in the same direction and
  disclosed in `WO-HBI-004` and in `VER-HBI-001`'s second amendment: a tree rule rather
  than a `*.yaml` rule, and a tracked-set inventory rather than one derived from the
  suite's byte-exact assertions. Verifying this record accepts both departures.
- The residual `VER-HBI-001` names is narrowed, not closed. A byte-exact assertion on a
  path in no declared tree and no named file remains invisible to `ByteExactSurfaceTests`;
  the only detector for that case is the full suite in a `core.autocrlf=true` checkout.
- The reserved-name fix's failing platform is not reproducible on this workstation. The
  `windows-2022` corroboration comes from `WO-RLO-005`'s rehearsal lane on another branch
  and is disclosed as corroboration, not as this candidate's own measurement.
- No Linux measurement is local, and no local measurement runs CPython 3.11.
- The in-tree `doctor` reports 28 `FAIL` with a `FAIL` set identical to the control's at
  `ee8aea1`, so that skew is inherited boundary state; the governing run has none.

## Scope of the decision that was taken

Verifying this record accepted the retained evidence as recorded, including every disclosure
above. It does not approve a merge, a release, a publication, a deployment, a tag, a
distribution build, or a governor adoption, it did not change `WO-HBI-004`, and it does not
discharge the manual acceptances `VER-HBI-001` requires from the security, quality and
repository owners, which remain separate and outstanding.
