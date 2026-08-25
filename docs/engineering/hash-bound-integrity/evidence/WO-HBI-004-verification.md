# WO-HBI-004 Verification Evidence

Date: 2026-08-25

Authority: non-authoritative retained candidate evidence. This file does not approve an
artifact, authorize a diff, verify work, merge, release, publish, or deploy. It records
what was measured, where, and what the measurements do not cover, so that an accountable
assurance decision can be taken over facts rather than over a summary.

Work order: `WO-HBI-004`, `status = "implemented"`, assurance classification
`commit_bound_verification = "required"` decided by the repository owner with the
rationale that "this changes which bytes a Windows checkout presents for the closed
phase-3 skill templates, and it replaces the mechanism `WO-HBI-003` used to decide that
set. The release orchestrator qualifies the candidate inside a `git worktree` that
inherits those bytes, so the change alters what qualification reads on one runner type.
`WO-HBI-003` was verified against three per-extension patterns and its guard still passed
while a fourth extension inside the same tree stayed converted; a wrong inventory here
would reproduce exactly that outcome, so verification must bind the exact candidate commit
rather than the branch."

Preparation of a `VREC` was authorized by the repository owner on 2026-08-25 through the
statement `you can set WO-RLO-005 and WO-HBI-004 as implemented, and prepare the
verification record(s)`. `WO-HBI-004` was already `implemented` when that statement was
made, so no lifecycle transition was needed and none was invented. Preparation is not
verification: the record this file supports is prepared `ready` and the assurance decision
remains outstanding.

## Which commit the figures describe, and which commit the record binds

The work order's own branch, `fix/hbi-004-byte-exact-surface-inventory`, merged into `main`
as `1d459cf724c203006d2263903478c9f46b701d7c` through pull request #145 before preparation
was authorized. A record binds a commit at which the evidence it binds is tracked, and this
file did not exist at the branch tip `74bb0e385ff3ab093773bc0c312aa658dc0b1ddd`. The
candidate is therefore a commit on a new branch taken from `main` at `1d459cf`, carrying
the work order's implementation exactly as merged plus this file, and the record is written
in a later commit because a file cannot contain the hash of its own commit.

Every local figure below was measured over the tree of `1d459cf`, before this file was
written. This file and the record add prose and one governance artifact and change no
executable content, no test, no rule, no workflow and no fixture, so no figure below
describes a tree that differs from the candidate's in anything a measurement reads. Where a
figure moves because the record itself is an artifact, both values are stated.

## Environment

| Item | Value |
|---|---|
| Platform | `Windows-11-10.0.26200-SP0` |
| Python | 3.14.6 |
| Git | 2.45.1.windows.1 |
| Checkout | `C:\Users\mathi\se_harness-hbi004`, created with `git worktree add` |
| `core.autocrlf` in the checkout | `true` |
| Branch | `docs/hbi-004-verification-record`, taken from `main` at `1d459cf` |
| Merge that put the packet on `main` | `1d459cf`, parents `ee8aea1` and `74bb0e3` |
| Control checkout, before the packet | `C:\Users\mathi\hbi004-control`, detached at `ee8aea1`, `core.autocrlf=true` |
| Control checkout, at `main` | `C:\Users\mathi\rlo005-control-m3`, detached at `1d459cf`, `core.autocrlf=true` |
| Governing evaluator | released `se-harness==0.6.0` in `C:\Users\mathi\se_harness_eval_060`, run from outside the checkout |

The checkout construction is the point of this work order, not an incidental detail.
`.github/workflows/publish-pypi.yml` qualifies a release candidate inside a checkout
created with `git worktree add`, which inherits `core.autocrlf=true` on Windows. A green
suite in an LF checkout proves nothing here, because the defect this work order fixes is
invisible there.

The retained implementation evidence is
`docs/engineering/hash-bound-integrity/evidence/WO-HBI-004-implementation.md`, 287 lines,
blob `4cebc9cdc20b820838da5b9b6e5cfcf75c746a20` at the candidate, 15792 bytes, SHA-256
`ed79334164ff49393b784384ad81cd31df8b3cd6ad5789f31a94ebd14afadf0a`. It is referenced by
digest rather than bound. Everything an assurance decision needs is re-measured and
restated here.

## What the candidate delivers, as merged

`git diff --stat ee8aea1 1d459cf` reports six files, 708 insertions and 18 deletions:

| Path | Change |
|---|---|
| `.gitattributes` | one owner-region tree rule replaces three per-extension rules, with the reason in comments |
| `tests/test_hash_bound_integrity.py` | `BYTE_EXACT_TREES`, a tracked-set inventory, `working_tree_attributes()`, and three new tests |
| `tests/test_agentic_execution.py` | the reserved-name precondition assert and `test_reserved_path_components_are_refused_on_every_platform` |
| `docs/engineering/hash-bound-integrity/verification/VER-HBI-001.md` | second amendment, accepted |
| `docs/engineering/hash-bound-integrity/work-orders/WO-HBI-004.md` | the work order |
| `.../evidence/WO-HBI-004-implementation.md` | retained implementation evidence |

No product source file is changed. The declared rule is
`templates/repository/standard/.agents/skills/** text eol=lf`; the inventory is
`BYTE_EXACT_FILES`, four named paths, plus every tracked path under the one prefix in
`BYTE_EXACT_TREES`, read from `hash_bound.tracked_paths` and never from `.gitattributes`.

## The finding, independently reproduced in the control

The claim this work order rests on is that a guard reported `OK` while the surfaces it
existed to protect were converted. Re-measured in the control checkout at `ee8aea1`, which
is `main` with `WO-HBI-003` merged and none of this packet:

```
i/lf w/crlf attr/    …/harness-draft-change/agents/openai.yaml
i/lf w/crlf attr/    …/harness-execute-work-order/agents/openai.yaml
i/lf w/crlf attr/    …/harness-prepare-assurance/agents/openai.yaml

python -m unittest discover -s tests -p "test_hash_bound_integrity.py" -k ByteExactSurfaceTests
Ran 3 tests in 0.082s
OK
```

Three committed files whose exact bytes the suite compares resolve no attribute, are
materialized converted, and the previous guard passes over them. The implementation
evidence recorded the same result; it is reproduced here from the control rather than
carried across.

At the candidate the same tree resolves `text eol=lf` for all fifteen tracked files with
none converted, and a fresh detached worktree at `1d459cf` with `core.autocrlf=true`
materializes all fifteen as LF unaided — so the property comes from versioned content and
not from a local repair.

## The guard is falsifiable, re-measured two ways at the candidate

Both measurements changed `.gitattributes` in the working tree only, re-materialized the
affected paths with `rm` plus `git checkout --`, and restored with `git checkout --`
afterwards. After each restore the worktree is clean, `.gitattributes` is blob
`bb9a3d8d4de3015ebc3019ced8ab22a23e4fa495` with its 23 CR bytes byte-identical to the
pre-experiment file, and the governing `doctor` reports `managed:.gitattributes: unchanged`
and `distribution:.gitattributes: matches distribution` at exit 0.

`VER-HBI-001` scenario 9 — the tree rule replaced by `WO-HBI-003`'s three per-extension
rules, which is exactly `ee8aea1`'s version of the file:

```
Ran 6 tests in 0.595s
FAILED (failures=8)
```

| Test | Failures | What each names |
|---|---|---|
| `test_a_novel_extension_in_a_byte_exact_tree_needs_no_new_rule` | 2 | `'set' != 'unspecified'` for the probe `agents/openai.yaml` and for `nested/deeper/probe.novel-extension` |
| `test_every_surface_resolves_the_required_attribute` | 3 | each `agents/openai.yaml` path, `'set' != 'unspecified'` |
| `test_no_surface_is_converted_in_this_working_tree` | 3 | each `agents/openai.yaml` path, `is crlf` |

Eight failures over the same repository state the previous guard reported `OK` for, and
`test_a_novel_extension_in_a_byte_exact_tree_needs_no_new_rule` is the case that closes the
mechanism rather than the instance: an extension no rule has ever named, four directories
inside the declared tree, is covered by the tree rule and uncovered by an extension list.

`VER-HBI-001` scenario 8, on a named file rather than a tree, to show the tracked-set
inventory did not weaken the part `WO-HBI-003` was verified against — the rule
`se_harness/agent_contract.json text eol=lf` removed:

```
Ran 6 tests in 0.570s
FAILED (failures=2)
```

`test_every_surface_resolves_the_required_attribute` reports `'set' != 'unspecified'` and
`test_no_surface_is_converted_in_this_working_tree` reports
`se_harness/agent_contract.json is crlf`. Restoring the rule returns the class to 6 tests
`OK` and the module to 102 tests `OK` with 1 skip.

## The reserved-name fix, and where it is and is not measured

`test_reserved_path_components_are_refused_on_every_platform` asserts the refusal directly
against `_validate_component` for `NUL.txt`, `nul`, `CON`, `PRN.md`, `aux.json`, `COM1.py`
and `lpt9.yaml`, and asserts that `openai.yaml`, `SKILL.md`, `skill-contract.json` and
`nullable.py` are accepted so it cannot pass vacuously. Both reserved-name tests pass here
(2 tests, `OK`), and the filesystem-based one now asserts its own precondition — that the
reserved entry is enumerable — instead of treating a successful write as proof.

What this workstation cannot measure is the image the defect appeared on. On Windows 11
build 26200 with CPython 3.14.6 a write to `NUL.txt` produces a real file; on hosted
`windows-2022` with CPython 3.11 the basename resolves to the device, which is why the
original assertion was unreachable there. The local measurement therefore covers the new
platform-independent assertion and the corrected precondition, not the hosted behaviour.

Corroboration exists on the runner, and it is disclosed as corroboration rather than
presented as this candidate's own figure. `WO-RLO-005`'s rehearsal lane, on branch
`feat/rlo-004-publication-rehearsal` in pull request #138, ran after this packet reached
`main`: runs [32775622117](https://github.com/mmzen/se_harness/actions/runs/32775622117)
and [32776424455](https://github.com/mmzen/se_harness/actions/runs/32776424455) both report
`REHEARSED` on `ubuntu-latest` and on `windows-2022` with `candidate unit suite passed
(932 tests)`. The previous run of that lane failed the same job on `windows-2022` with four
failures over 928 tests, three of them the `agents/openai.yaml` sub-cases and one the
reserved-name test. Those four are gone. That run's checkout is not the commit this record
binds and its suite is `WO-RLO-005`'s, not this candidate's.

## Local qualification at `1d459cf`

| Measurement | Control at `ee8aea1` | Candidate |
|---|---|---|
| Full suite, `git worktree` checkout, `core.autocrlf=true` | 807 tests, 3 failures, 22 skipped | **811 tests, OK, 22 skipped** |
| `tests/test_hash_bound_integrity.py` | 99 tests, OK, 1 skipped | 102 tests, OK, 1 skipped |
| `ByteExactSurfaceTests` | 3 tests, OK — while three surfaces are `w/crlf` | 6 tests, OK — no surface converted |
| `tests/test_agentic_execution.py` | 27 tests, 3 failures, 2 skipped | 28 tests, OK, 2 skipped |
| Reserved-name tests | 1, filesystem-dependent | 2, one of them platform-independent |
| Tracked files under the skills tree resolving `text eol=lf` | 12 of 15 | 15 of 15 |
| Byte-exact inventory | 4 named + 12 by pattern | 4 named + 15 by tree |
| In-tree `doctor` | 81 `PASS`, 28 `FAIL` | 81 `PASS`, 28 `FAIL`; `diff` over the two `FAIL` lists is empty |

## Gate results at the candidate

Every gate `AGENTS.md` names was run, and the governing verdicts come from the released
`0.6.0` evaluator executed from outside the checkout.

| Gate | Result |
|---|---|
| `python -m unittest discover -s tests -p "test_*.py"` | 811 tests, OK, 22 skipped |
| Governing `validate` | PASS, 822 artifacts, 0 errors, 50 warnings, all maintenance |
| Candidate `scripts/validate_engineering_artifacts.py --root .` | PASS, the same 822 / 0 / 50 |
| `python scripts/validate_release_distributions.py --root .` | PASS, 1 distribution-bearing record |
| `python -m se_harness --help` | usage reported, exit 0 |
| Governing `doctor` | exit 0, 87 checks, 0 `FAIL`, `managed:.gitattributes: unchanged` |
| Governing `preflight --work-order WO-HBI-004 --phase review` | `Harness preflight: PASS`, no diagnostic |
| `git status --porcelain` | empty |

The 822 artifact count is `main`'s. The verification record this file supports is itself an
artifact, so the count at the commit that carries it is 823; the error and warning counts do
not move.

## Disclosures

These are the limits an assurance decision is taken over. None is a defect being hidden;
each is a boundary of what was measured.

1. **The record binds a commit off `main`, not the work order's branch tip.** The branch
   merged before preparation was authorized, and the evidence a record binds must be
   tracked at the commit it names. The candidate carries the packet exactly as merged plus
   this file, and nothing else.
2. **Merging the pull request that carries this record must be a true merge.** A squash or
   a rebase of this branch would orphan the bound commit, and a verified record can never
   be re-pointed at a later commit.
3. **The implementation departed from the owner's framing twice**, in the same direction
   and disclosed in `WO-HBI-004` and in `VER-HBI-001`'s second amendment: a tree rule
   rather than a `*.yaml` rule, and a tracked-set inventory rather than one derived from
   the suite's byte-exact assertions. The second departure was measured, not preferred —
   the assertion that caused the defect resolves its path from a loop variable over a
   dictionary comprehension, so no source scan can name it without guessing. Accepting
   this record accepts those departures.
4. **The residual named in `VER-HBI-001` is narrowed, not closed.** A byte-exact assertion
   on a path in no declared tree and no named file is still invisible to
   `ByteExactSurfaceTests`. The only detector for that case is the full suite run in a
   `core.autocrlf=true` checkout created with `git worktree add`.
5. **No committed blob changed under `templates/`.** The rule changes what a checkout
   presents, not what the repository stores; every file in the tree was already `i/lf`.
   That was the work order's stated stop condition and it did not trigger.
6. **The falsifiability measurements mutated the working tree.** Both were reverted with
   `git checkout --`, and the restored state is re-measured above: clean status, the same
   `.gitattributes` blob and CR count, `managed:.gitattributes: unchanged`, and the class
   and module green again.
7. **The reserved-name fix's failing platform is not reproducible here.** The local
   measurement covers the corrected precondition and the new platform-independent
   assertion. The `windows-2022` evidence comes from `WO-RLO-005`'s lane on another
   branch and is disclosed as corroboration, not as this candidate's measurement.
8. **No Linux measurement is local**, and no local measurement runs CPython 3.11. Test and
   skip counts are not comparable across environments: this workstation reports 811 tests
   with 22 skips, and the hosted legs report 10 skips over a different suite.
9. **The in-tree `doctor` reports 28 `FAIL`.** The control at `ee8aea1` reports the same 28
   with identical names, so the skew is inherited candidate-versus-released boundary state
   and none of it is caused or repaired by this packet. The governing `doctor`, which is the
   run that carries a verdict, has none.
10. **`.gitattributes` remains a fragment-mode file.** The rule is in the owner region; the
    managed block between the `se-harness` markers is untouched and its digest is unchanged.
11. **`VER-AEX-001` was not amended.** The reserved-name fix brings the suite into
    conformance with that contract's existing security check on every platform rather than
    adding a pass condition, so no amendment was needed and none was made.
12. **`build_recipe_sha256` remains in `unbound_digest_fields`**, tracked as repository
    issue 142 and untouched here.

## Actions not performed

No `VREC` field was written by hand: the record is produced by the released `0.6.0`
evaluator's `capture-verification` at the candidate commit with a clean worktree, and it is
prepared `ready`, not verified.

No merge, no tag, no GitHub Release, no PyPI publication, no Pages deployment, no
protected-environment approval, no orchestrator workflow dispatch, no release record, no
release-record preparation or transition, no promotable distribution build, no assurance
decision, no governor adoption, no credential acquisition, and no hosting or
branch-protection change.

No recorded digest, `VREC`, `RLS`, `REL` or evidence fact was rewritten or repointed, no
managed file was edited, no lifecycle state was changed, and no committed file's bytes were
converted. `WO-RLO-005`, its branch and its pull request are untouched by this branch.
