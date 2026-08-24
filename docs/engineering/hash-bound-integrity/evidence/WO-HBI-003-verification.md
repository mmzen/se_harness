# WO-HBI-003 Verification Evidence

Date: 2026-08-24

Authority: non-authoritative retained implementation and local-qualification
evidence. This file does not approve an artifact, authorize a diff, verify work,
release, publish, deploy, or accept the two amendments it records. It records what
was measured on one Windows workstation at one commit.

Work order: `WO-HBI-003`, assurance classification `commit_bound_verification =
"required"` decided by the engineering owner. The figures below were measured over
the tree of implementation commit `a933d7260214f0fb642e45639336b3d910f7ab07`. This
evidence file is committed on top of that commit, because a file cannot contain the
hash of its own commit; the candidate commit the later `VREC` binds is therefore the
branch tip. The tip differs from `a933d72` by this file and by governance prose only:
later commits on this branch record the owner's acceptance of the two amendments in
`VER-HBI-001`, this domain's `README.md`, `WO-HBI-003` and this file, and name the
issue the same decision routed the open recipe question to. No executable content, no
test, no `.gitattributes` rule and no recorded digest differs between `a933d72` and
the tip, so every figure below still describes the tip's behaviour. That
`VREC` is a separate, separately authorized act, is not prepared here, and must
re-measure its own figures.

## Environment

| Item | Value |
|---|---|
| Platform | `Windows-11-10.0.26200-SP0` |
| Python | 3.14.6 |
| Git | 2.45.1.windows.1 |
| Checkout | `C:\Users\mathi\se_harness-hbi003` |
| Branch | `fix/hbi-003-byte-exact-checkout-rules` |
| Base commit | `fc97103bfeb3cb321f433beac2318984473b38ed` (`origin/main`, the merge of pull request #139) |
| Implementation commit | `a933d7260214f0fb642e45639336b3d910f7ab07` |
| `core.autocrlf` in the checkout | `true` |
| Control worktree | `fc97103` checked out with the same `core.autocrlf=true` |
| Governing evaluator | released `se-harness==0.6.0` in `C:\Users\mathi\se_harness_eval_060`, outside the checkout |

`core.autocrlf=true` is not incidental here. The defect this work order removes is
invisible on an LF checkout, so a green suite there would prove nothing, and
`WO-HBI-003`'s constraints require qualification in a converting checkout. Every
suite figure below was measured in one.

Linux was not exercised locally, and no measurement here is a Linux measurement. The
Linux half is a hosted check. It cannot be recorded in this file, because those checks
run over the commit that contains this file and therefore do not exist when it is
written; the verification record that binds the candidate commit is where that result
belongs.

## Changed paths

```text
 .gitattributes                                     |  11 ++
 docs/engineering/hash-bound-integrity/README.md    |   7 +
 .../verification/VER-HBI-001.md                    |  24 +++
 .../hash-bound-integrity/work-orders/WO-HBI-003.md | 198 +++++++++++++++++++++
 tests/test_hash_bound_integrity.py                 |  70 ++++++++
 5 files changed, 310 insertions(+)
```

310 insertions and zero deletions. Every path lies inside the work order's
`[execution_scope]`. This evidence file is a sixth path, also in scope under
`docs/engineering/hash-bound-integrity/`.

## The seven rules and the sixteen paths they select

The rules were appended to the owner-controlled region of `.gitattributes`,
following `WO-REB-018`'s precedent of declaring a rule beside the surface that needs
it. The managed block between `# se-harness:begin` and `# se-harness:end` was not
touched; the diff over `.gitattributes` contains eleven added lines and no removed
line.

Resolved through `se_harness.hash_bound.tracked_paths` against the same matcher the
guard uses, the seven patterns select sixteen tracked files out of 1244:

| Pattern | Tracked files selected |
|---|---|
| `se_harness/agent_contract.json` | 1 |
| `se_harness/hash_bound_classes.json` | 1 |
| `release/build-recipe.json` | 1 |
| `release/build-toolchain.lock` | 1 |
| `templates/repository/standard/.agents/skills/**/*.json` | 4 |
| `templates/repository/standard/.agents/skills/**/*.md` | 4 |
| `templates/repository/standard/.agents/skills/**/*.py` | 4 |

No pattern is dead, and no pattern reaches a path outside the inventory
`WO-HBI-003` authorizes.

## Before and after, measured on the same platform

`git ls-files --eol` over the four non-template surfaces and one template surface,
in the control worktree at `fc97103` and in this checkout at `a933d72`:

| Path | Control at `fc97103` | This checkout at `a933d72` | CR bytes on disk, control → here |
|---|---|---|---|
| `se_harness/agent_contract.json` | `i/lf w/crlf attr/` | `i/lf w/lf attr/text eol=lf` | 1 → 0 |
| `se_harness/hash_bound_classes.json` | `i/lf w/crlf attr/` | `i/lf w/lf attr/text eol=lf` | 83 → 0 |
| `release/build-recipe.json` | `i/lf w/crlf attr/` | `i/lf w/lf attr/text eol=lf` | 134 → 0 |
| `release/build-toolchain.lock` | `i/lf w/crlf attr/` | `i/lf w/lf attr/text eol=lf` | 7 → 0 |
| `templates/…/harness-orient/SKILL.md` | `i/lf w/crlf attr/` | `i/lf w/lf attr/text eol=lf` | 58 → 0 |

`i/lf` on both sides is the point: the index already held LF. Only the checkout's
materialization moved, which is what a byte rule can move. All sixteen selected
paths report `i/lf w/lf attr/text eol=lf` here; none reports `attr/` empty.

Controls in the same checkout still convert, so the rules are scoped rather than
global: `README.md` carries 200 CR bytes and `.gitattributes` itself carries 20.

## The suite, before and after

Both runs are `python -m unittest discover -s tests -p "test_*.py"` on this
platform with `core.autocrlf=true`.

| Run | Result |
|---|---|
| Control worktree at `fc97103` | `Ran 710 tests in 303.481s` — `FAILED (failures=5, errors=5, skipped=12)`, exit 1 |
| This checkout at `a933d72` | `Ran 713 tests in 300.884s` — `OK (skipped=12)`, exit 0 |

The ten reds the control reports, named:

```text
ERROR: test_agent_contract.CatalogAndParsingTests.test_catalog_is_canonical_closed_and_reference_complete
ERROR: test_release_build.BuildRecipeSchemaTests.test_canonical_recipe_binds_complete_identity
ERROR: test_release_build.BuildRecipeSchemaTests.test_producer_executes_arrays_with_only_declared_and_internal_environment
ERROR: test_release_build.DeterministicSdistTests.test_non_promotable_ephemeral_wheel_carries_and_fresh_installs_all_skill_cores_once
ERROR: test_release_build.DeterministicSdistTests.test_portable_skill_distribution_surface_is_explicit_and_unique
FAIL:  test_agentic_execution.Phase3EffectGuardTests.test_manifest_normalizes_line_endings_and_detects_content_changes
FAIL:  test_agentic_execution.SkillContractTests.test_contract_rejects_duplicate_and_unknown_fields
FAIL:  test_hash_bound_integrity.DeclarationShapeTests.test_declaration_is_data_only
FAIL:  test_release_build.BuildRecipeSchemaTests.test_noncanonical_duplicate_and_open_recipe_forms_fail
FAIL:  test_release_build.BuildRecipeSchemaTests.test_toolchain_lock_hash_and_inventory_are_closed
```

All ten pass here, and the three tests this work order adds bring the total from
710 to 713. No skip was added: 12 in both runs, and they are the platform guards
`main` already carries.

The hosted Windows rehearsal that found this reported eleven failing tests rather
than ten. Ten of its eleven names are exactly the ten above. The eleventh,
`test_manifest_rejects_missing_required_invalid_utf8_and_reserved_paths`, exists at
`fc97103` and passes in the control worktree here, so the extra red is not explained
by a difference in the test inventory and is not reproduced by this measurement. It
is stated rather than explained. Two candidate causes were not separated: a
`pull_request` run tests the merge commit `e77d3dd7d114`, whose
`tests/test_agentic_execution.py` is an automatic merge of two divergent copies and
need not equal `fc97103`'s; and the hosted interpreter is 3.11.9 against 3.14.6 here.
Its subject is `templates/repository/standard/.agents/skills/harness-orient`, which
these rules cover, so the fix reaches it either way — but this evidence claims only
the ten it measured.

## The guard is falsifiable, measured three ways

`ByteExactSurfaceTests` was exercised in a throwaway worktree at `a933d72` with the
same `core.autocrlf=true`, restoring the tree between cases:

| Case | Result |
|---|---|
| Unmodified | `Ran 3 tests` — `OK` |
| One rule removed (`se_harness/agent_contract.json`), path re-materialized | `FAILED (failures=2)` |
| All seven rules removed, all sixteen paths re-materialized | `FAILED (failures=32)` |
| A pattern added that selects no tracked file | `FAILED (failures=1)` |

The one-rule case is `VER-HBI-001` acceptance scenario 8 exactly, and it names both
the path and what was observed:

```text
AssertionError: 'crlf' not found in ('lf', 'none') : se_harness/agent_contract.json is crlf
AssertionError: 'set' != 'unspecified' : {'text': 'unspecified', 'eol': 'unspecified'}
```

Thirty-two failures for seven rules is sixteen paths failing the attribute
assertion and the same sixteen failing the conversion assertion, which is the two
independent readings the contract asks for: the product's own resolver, and `git
ls-files --eol` on the file as it actually sits on disk. The dead-pattern case fails
with `se_harness/no_such_surface.json selects no tracked file, so its byte rule is
dead`, so an inventory that drifts away from the tree fails rather than passing
vacuously.

## Two fresh clones, and the one case where the rules do not reach

Both clones were taken from `origin` on this workstation with `core.autocrlf=true`,
independently of the working checkout, and neither is a `git worktree` of it.

A clone taken directly at the candidate — `git clone --branch
fix/hbi-003-byte-exact-checkout-rules --single-branch` — materializes every one of the
sixteen paths as `i/lf w/lf attr/text eol=lf`, and `tests.test_hash_bound_integrity`
reports `Ran 99 tests` `OK (skipped=1)`. The control in the same clone still converts:
`README.md` is `i/lf w/crlf attr/`. This is the case the release orchestrator's Windows
leg exercises, and it passes.

The second clone was taken at the default branch and then checked out onto the
candidate with `git checkout --detach`. There, all sixteen paths report `attr/text
eol=lf` and yet remain `w/crlf`, and the module reports `FAILED (failures=17)`:
sixteen are `test_no_surface_is_converted_in_this_working_tree` naming one path each,
and the seventeenth is `DeclarationShapeTests.test_declaration_is_data_only`, one of
the ten reds this work order removes, returning because its surface is converted
again.

That is not a defect in the rules and not a fourth falsifiability case. Git
re-materializes a path on checkout only when its blob changes. These sixteen blobs are
identical either side of `a933d72`, so a working tree that had already materialized
them under CRLF before the rule existed keeps the converted bytes until the file
changes or is re-materialized deliberately — `rm <path> && git checkout -- <path>`, or
`git rm --cached -r . && git reset --hard`. A plain `git checkout --` on an unmodified
path is a no-op and does not re-apply a changed `.gitattributes`.

The limitation is therefore real and bounded, and it is stated rather than worked
around:

- It does not reach the release orchestrator. `git worktree add --detach` creates an
  empty directory, so every path materializes there for the first time with the rules
  already in effect. The same holds for `actions/checkout` and for the first clone
  above.
- It does reach an existing developer checkout that pulls this change. Those bytes stay
  converted until re-materialized, and the guard fails there rather than passing
  silently, which is the guard reporting the working tree it was asked about.
- No committed byte is at risk in either case. The index holds LF throughout, as the
  `i/lf` column shows in both clones.

## Nothing committed changed, and nothing recorded moved

- `git diff --stat fc97103 a933d72` over the sixteen selected paths is empty. The
  rules change what a checkout presents, not what the repository stores.
- `git diff --stat fc97103 a933d72 -- .github/` is empty.
  `.github/workflows/publish-pypi.yml` is byte-unchanged, as `WO-HBI-003` scopes it
  and as the owner's `WO-RLO-005` design requires.
- `git diff fc97103 a933d72 -- docs/` contains no added or removed `_sha256` field.
  The only `_sha256` occurrences in the diff are prose in `WO-HBI-003` discussing
  `build_recipe_sha256`.
- The `.gitattributes` diff has no removed content line, so the managed block is
  intact. The governing evaluator confirms it:
  `PASS managed:.gitattributes: unchanged`.

## Gate results

| Gate | Result |
|---|---|
| `python -m unittest discover -s tests -p "test_*.py"` | 713 tests, OK, 12 skipped, 300.9s, exit 0 |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS — 794 artifacts, 0 errors, 50 warnings, exit 0 |
| `python scripts/validate_release_distributions.py --root .` | PASS (1 distribution-bearing record) |
| `python -m se_harness --help` | exit 0 |
| governing `validate .` (0.6.0, outside the checkout) | PASS — 794 artifacts, 0 errors, 50 warnings |
| governing `doctor .` (0.6.0, outside the checkout) | exit 0 — 87 PASS, 0 FAIL |
| governing `preflight . --work-order WO-HBI-003 --phase review` | `Harness preflight: PASS`, `Work order: WO-HBI-003 (implemented)`, exit 0 |
| in-tree `python -m se_harness doctor .` | exit 1 — 84 PASS, 18 FAIL (candidate-versus-released skew) |

The candidate validator reports 793 artifacts at `fc97103` and 794 here; the one
added artifact is `WO-HBI-003`. Errors and warnings are unchanged at 0 and 50, and
the 50 are all maintenance-plane and pre-existing.

The in-tree `doctor` FAILs were compared against the control at `fc97103` rather
than reasoned about: the control reports the same 84 PASS and the same 18 FAIL, with
identical names — six `distribution:` skews including `.gitattributes`, and twelve
`lock-entry:` entries for the `.agents/skills/` files the released `0.6.0` lock does
not know about. This change causes none of them, and the governing evaluator from
outside the checkout reports `PASS distribution:.gitattributes: matches
distribution` alongside `PASS managed:.gitattributes: unchanged`. That divergence is
the documented candidate-source boundary. It is not authorization to overwrite a
root managed file.

## Amendments recorded and accepted

Two artifacts were amended under this work order. Both add obligation, relax no
pass condition, and change no approved `statement` field:

- `VER-HBI-001` — one requirement-matrix row for `REQ-HBI-001` covering byte-rule
  completeness beyond declared classes, acceptance scenario 8, and one property
  bullet. The amendment carries its own dated section stating why `main` forced it.
- `docs/engineering/hash-bound-integrity/README.md` — the scope boundary now admits
  committed files whose exact bytes the suite compares without a recorded digest
  binding them, and says they are guarded by a test rather than by a `doctor` check,
  because no class binds them.

The accountable repository owner accepted both on 2026-08-24 through the statement
`Accept both`. `VER-HBI-001`'s amendment section carries that decision and the
framing it was taken over; this file records that acceptance rather than granting it.
Acceptance scenario 8 was measured before the decision was put, not after — the
one-rule case in the falsifiability table above is that scenario.

Nothing in the acceptance authorizes verification, a `VREC`, a merge, a release, a
publication or a deployment, and the manual acceptances `VER-HBI-001` requires from
the security, quality and repository owners remain separate and outstanding.

## Disclosures

- Five of the seven patterns fall outside `REQ-HBI-001`'s trigger, which is a
  committed text file bound by a recorded SHA-256. `release/build-recipe.json` and
  `release/build-toolchain.lock` meet it; `se_harness/agent_contract.json`,
  `se_harness/hash_bound_classes.json` and the three skill-template extensions do
  not — the suite compares their bytes instead of hashing them into a record. They
  are included because the mechanism and the failure are identical. This delivers
  more than the requirement obliges, which is why the two amendments above exist
  rather than the excess being absorbed silently. `WO-HBI-003` states the same
  relation in its own words.
- `build_recipe_sha256` remains in `unbound_digest_fields`, so `doctor` still
  reports `9 digest fields declared out of scope` and does not enforce that
  recipe's bytes as a hash-bound class. `WO-RLO-004`'s retained verification put it
  there deliberately, leaving byte stability to repository policy, and repository
  policy now has a mechanism where it previously had none. Whether the field should
  instead become a declared class, so a `doctor` check rather than a unit test
  guards it, is a real question this work order deliberately leaves open. It is
  stated here rather than answered. On 2026-08-24 the owner directed that it be filed
  as an issue rather than measured now, so it is tracked outside this paragraph: it is
  repository issue 142. Filing an issue authorizes no implementation, and the two
  guards that exist today — the byte rule and `ByteExactSurfaceTests` — are unchanged
  by that routing.
- The guard is a unit test, not a `doctor` check. `doctor`'s three hash-bound checks
  read the declaration, and these sixteen paths are in no declared class, so no
  check assesses them. A consumer installation therefore inherits nothing from this
  work order: the rules are `repository`-region, and the guard lives in this
  repository's suite. That is the intended boundary, and the domain `README.md`
  amendment says so.
- The guard skips when Git is unavailable or the root is not a working tree, so a
  source tree without `.git` reports a skip rather than a pass. Twelve skips were
  observed in both runs and none is this class; the skip path was not forced.
- `templates/repository/standard/gitattributes.fragment`, the canonical consumer
  template, is unchanged. These rules are deliberately repository-owned and must not
  reach a consumer, which `VER-HBI-001` acceptance scenario 7 already asserts.
- The measurement of the sixteen paths' attributes uses
  `se_harness.hash_bound.resolved_attributes`, the product's own prober, and
  `git ls-files --eol` independently. Neither reading is derived from the other, and
  the guard fails if they disagree with the declaration.
- Two fresh clones were measured, in the section above, after the first draft of this
  file recorded that none had been. The before/after control remains a `git worktree`
  at `fc97103`, which is the construction the release orchestrator itself uses at
  `.github/workflows/publish-pypi.yml:209` and therefore the faithful one for this
  defect. The clones add an independent reading and one limitation the worktree control
  could not have surfaced.
- The clone matrix is not complete. Only `core.autocrlf=true` was exercised, on one
  Windows workstation, with one Git version; `input` and `false` were not, and Linux
  was not clone-checked either. `VER-HBI-001`'s three-value fresh-checkout matrix
  applies to declared hash-bound classes, and these sixteen paths are in no declared
  class, so that matrix is not this work order's obligation — but the gap is stated
  rather than implied to be covered.

## Actions not performed

Two commits were made on `fix/hbi-003-byte-exact-checkout-rules`: the
implementation `a933d72` and the commit carrying this file. Both rest on the
engineering owner's decision of 2026-08-24, which authorized bounded local
implementation, local qualification, one branch and one pull request declaring
`Harness-Work-Order: WO-HBI-003`.

Beyond that: no merge, no `VREC` or `RLS` preparation or transition, no workflow
dispatch of the release orchestrator, no tag, no GitHub Release, no PyPI
publication, no Pages deployment, no environment approval, no release record, no
promotable or ephemeral distribution build, no credential use, no maintenance
mutation, no operational governor adoption, no root managed file overwritten, no
historical digest rewritten, no change to `WO-RLO-005` or its branch, and no edit
outside the execution scope. The owner's `Accept both` of 2026-08-24 accepted the two
amendments above and nothing else; the manual acceptances `VER-HBI-001` requires from
the security, quality and repository owners remain outstanding and are not recorded
here.
