+++
id = "WO-HBI-003"
type = "work_order"
title = "Declare a byte rule for the byte-exact surfaces no recorded digest binds"
status = "implemented"
owners = ["engineering-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "This changes the bytes a Windows checkout presents for the release build recipe, whose exact bytes `SPEC-RLO-004` rule 13 requires to resolve at the candidate commit, and for the toolchain lock that recipe pins. The release orchestrator qualifies the candidate inside a `git worktree` that inherits those bytes, so the change alters what qualification reads on one runner type. A wrong or incomplete path list would leave a surface converted while the suite reports green on Linux, which is the failure this work order removes, so verification must bind the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".gitattributes",
  "docs/engineering/hash-bound-integrity/",
  "tests/test_hash_bound_integrity.py",
]

[relations]
implements = ["REQ-HBI-001"]
specifications = ["SPEC-HBI-001"]
architecture = ["ARCH-HBI-001", "ADR-HBI-001"]
verification = ["VER-HBI-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T16:44:00Z"
decided_by = "engineering-owner"
reason = "Owner decision recorded 2026-08-24, selecting a separate work order and a separate pull request over folding this fix into WO-RLO-005: 'New small work order for the byte-exact line-ending declarations, its own PR, merged before #138.' Authorizes bounded local implementation, local qualification, one branch, and one pull request."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T16:46:00Z"
decided_by = "engineering-owner"
reason = "Same decision authorized an immediate start, because pull request #138's Windows rehearsal job stays red until this work order merges."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-24T17:12:00Z"
decided_by = "engineering-owner"
reason = "In-scope implementation complete and locally qualified on 2026-08-24: the full suite passes in a `core.autocrlf=true` checkout at 710 tests, where the same checkout at `fc97103` fails ten. Evidence retained under this domain. Verification, VREC preparation, merge, release and publication remain separately unauthorized."
+++

# Work Order: Declare a byte rule for the byte-exact surfaces no recorded digest binds

## Lifecycle and authorization

Approved and started on 2026-08-24 on one owner decision, recorded in the
lifecycle events above. The decision chose a separate work order and a separate
pull request over folding this fix into `WO-RLO-005`, whose branch surfaced the
defect.

That decision authorizes bounded local implementation, local qualification, one
implementation branch and one pull request declaring
`Harness-Work-Order: WO-HBI-003`. Merge, `VREC` preparation or transition, tag,
release, publication, deployment, credential use, maintenance mutation and
governor adoption each remain separately unauthorized.

Measurement preceded approval. The seven patterns and their effect were measured
first so the owner's choice between this work order and a scope amendment on
`WO-RLO-005` could be made against figures rather than an estimate. No
repository file was changed before the approval above.

## What was found, and by what

`WO-RLO-005`'s publication-rehearsal lane executed on hosted runners for the
first time on 2026-08-24. Its Linux job passed. Its Windows job failed one
mechanic, `candidate-unit-suite`, with eleven byte-exact tests failing and the
run reporting `core.autocrlf=true` as the inherited checkout state.

The failure is not the rehearsal's. `.github/workflows/publish-pypi.yml` creates
the candidate checkout its qualification reads with
`git worktree add --detach "$temp_root/candidate-checkout" "$CANDIDATE_COMMIT"`
and then runs `python -m unittest discover -s tests -p 'test_*.py'` inside it. A
`git worktree` inherits the checkout's `core.autocrlf`, which is `true` on
`windows-2022`. The rehearsal reproduces that construction deliberately, so it
reproduced the orchestrator's own outcome: on its Windows leg, the release
orchestrator would fail candidate qualification.

Every failing assertion surface was committed on 2026-08-24, after `0.6.0` was
released on 2026-08-22. No past publication exercised them, so this is a defect
that had not yet been reached rather than a regression in a shipped path. The
exposure is real and near: the Windows leg's steps are gated on
`needs.resolve.outputs.distribution_schema == '1'`, and `RLS-SEH-012`, the newest
released record, declares distribution schema 1.

## Objective

Give every committed file whose exact bytes the candidate suite compares an
effective versioned byte rule, so that a `core.autocrlf=true` checkout — including
the `git worktree` the release orchestrator creates on `windows-2022` — presents
the committed bytes, and so that the absence of such a rule is a failing test
rather than a platform-dependent surprise.

## Relationship to `REQ-HBI-001`, stated exactly

`REQ-HBI-001` triggers on a committed text file whose bytes are bound by a
recorded SHA-256. Two of the seven declared patterns meet that trigger directly:

- `release/build-recipe.json` is bound by `build_recipe_sha256`, and
  `SPEC-RLO-004` rule 13 requires the recipe path and bytes to resolve exactly at
  the candidate commit. `WO-RLO-004`'s retained verification deliberately declared
  that field outside portable hash-class interpretation, leaving its byte
  stability to repository policy. Repository policy had no mechanism. This work
  order supplies one, in the owner-controlled region `REQ-HBI-001`'s required
  response already contemplates.
- `release/build-toolchain.lock` is the toolchain the recipe pins, and the suite
  closes its hash and inventory together.

The remaining five patterns do not meet that trigger. `se_harness/agent_contract.json`,
`se_harness/hash_bound_classes.json` and the three skill-template extensions are
compared byte for byte by the suite rather than bound by a recorded digest. They
are included because the mechanism and the failure mode are identical, and
because `REQ-HBI-001`'s rationale states the obligation this work order is
discharging: "The mechanism does not generalize by itself, and nothing detects
its absence elsewhere."

Including them delivers more than `REQ-HBI-001` obliges. That is disclosed here
rather than absorbed, and it is why this work order also amends the domain
`README.md` scope boundary and `VER-HBI-001`'s coverage. Both amendments add
obligation and relax nothing. The accountable repository owner accepted both on
2026-08-24 through the statement `Accept both`; `VER-HBI-001`'s amendment section
records that decision and the framing it was taken over. The acceptance authorizes
no verification, merge, release, publication or deployment.

The same turn took one further decision on a question this work order deliberately
left open. Whether `build_recipe_sha256` should move out of `unbound_digest_fields`
and become a declared hash-bound class, so that `doctor` rather than a unit test
guards that recipe's bytes, stays open and unmeasured; the owner directed that it be
filed as an issue so it is tracked rather than resting in one evidence paragraph. It
is repository issue 142, which records the question, the two guards that exist today
and what a declared class would have to satisfy. Filing an issue authorizes no
implementation, and nothing in this work order changes as a result: the field stays in
`unbound_digest_fields` and no declared class moves.

## In scope

- Append seven byte rules to the owner-controlled region of `.gitattributes`,
  following `WO-REB-018`'s precedent of declaring a rule beside the surface that
  needs it: `se_harness/agent_contract.json`,
  `se_harness/hash_bound_classes.json`, `release/build-recipe.json`,
  `release/build-toolchain.lock`, and `*.json`, `*.md` and `*.py` under
  `templates/repository/standard/.agents/skills/`.
- Add `ByteExactSurfaceTests` to `tests/test_hash_bound_integrity.py`: every
  declared pattern selects a tracked file, every selected path resolves
  `text` set and `eol=lf` through the product's own resolver, and no selected path
  is converted in the working tree as `git ls-files --eol` reports it.
- Amend this domain's `README.md` scope boundary to admit byte-exact surfaces that
  no recorded digest binds.
- Amend `VER-HBI-001` with one requirement-matrix row, one acceptance scenario and
  one property test covering byte-rule completeness beyond declared classes.
- Retain work-order-keyed implementation evidence under this domain's `evidence/`.
- Commit on one branch and open one pull request declaring
  `Harness-Work-Order: WO-HBI-003`.

## Out of scope

- The declaration data, the class resolver, the attribute prober, the three
  `doctor` checks and every hash mode. Those are `WO-HBI-001` and `WO-HBI-002`.
- Adding, removing or changing a hash-bound class, and moving
  `build_recipe_sha256` out of `unbound_digest_fields`. Whether that field's
  repository-policy excuse should become a declared class so `doctor` enforces it
  is a real question this work order deliberately leaves open, and states in its
  evidence, rather than answering.
- Editing `.github/workflows/publish-pypi.yml`. The orchestrator is byte-unchanged
  by this work order. Changing its checkout configuration instead of the
  repository's byte rules was available and was not taken: it would repair one
  consumer of these bytes and leave every other Windows checkout converted.
- The managed region of `.gitattributes`, the canonical template fragment, root
  managed files, `.engineering-harness.lock` and `.engineering-harness.toml`.
- Any change to `WO-RLO-005`, its packet or its branch, and any rehearsal or
  divergence-check behaviour.
- Rewriting or repointing any recorded digest, `VREC`, `RLS`, `REL` or evidence
  fact.
- Converting any committed file's bytes. No blob changes; the rules make a
  checkout present bytes the repository already stores.
- Preparing a `VREC`, merging, tagging, releasing, publishing, deploying, or any
  credential-bearing operation.

## Authorized decision envelope

Implementation may choose the pattern spelling that selects the intended paths,
the placement and comment wording within the owner-controlled region, the test
class and method names, and how the inventory is expressed in the test.

It may not add a rule for a path outside the inventory above, weaken a rule to
`text=auto`, declare a rule in the managed region, change any committed file's
bytes, change a declared hash-bound class, or edit a file outside the execution
scope. If any declared pattern turns out to change a blob rather than only a
checkout, stop rather than proceeding.

## Constraints

- Python 3.11+ standard library only; the guard resolves attributes through
  `se_harness.hash_bound`, not through a second implementation.
- The seven rules must be effective from versioned repository content. A local
  `core.autocrlf`, a global attributes file or `.git/info/attributes` does not
  satisfy this work order, matching `VER-HBI-001`'s unversioned-source negative.
- The managed `.gitattributes` block must still match its recorded digest, and
  `doctor` must report `managed:.gitattributes: unchanged`.
- Qualify in a checkout with `core.autocrlf=true`. A green suite on an LF checkout
  proves nothing here, because the defect is invisible there.
- Run the governing evaluator — released `se-harness==0.6.0` — from outside the
  checkout for validation and preflight.
- Preserve all unrelated changes and owner content outside managed markers.
