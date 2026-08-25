# WO-RLO-006 implementation evidence

Date: 2026-08-25

Authority: non-authoritative retained implementation evidence. This file does not approve, verify, release, publish, tag, deploy, or authorize anything. It records what was measured, on which interpreter, on which platform, and at which commit. Commit-bound assurance for this work order is `required` and was decided by the repository owner; that `VREC` is a separate accountable decision and this file is not it. Every rehearsal figure quoted here carries the rehearsal's own field `authority = "derived operational evidence; no formal lifecycle transition"`.

artifact: WO-RLO-006
checkpoint: handoff
subject_commit: ceab133e64893ae98ccb0bc5167f5086ff185d6e
formal_snapshot_sha256: 862e8e69a8b7bdd95cfd0302805d74447978834ed9c7c7b00674c6215c7ed4c6
formal_snapshot_checkout: a checkout carrying no CRLF conversion, which is what `core.autocrlf=false` produces here and what the Linux lane reads. The digest hashes worktree bytes, so it is a per-checkout figure; limitation 6 records every reading taken and the one that must not be quoted. This record names no hash of its own commit, because a record cannot contain one.
formal_snapshot_after_completion: 1cfb67eb5866bf0862e65dab587bb4e62abad1fa5682eb4ae8ccd614b52b6ed3, same convention. The bound figure above is the **handoff** snapshot, taken while the work order was `in_progress` and before the completion transition wrote a fourth `[[lifecycle_events]]` entry into it. `WO-RLO-006.md` is one of the artifacts the digest hashes, so recording implementation completion necessarily moved it. Both figures are given because a reader recomputing the digest against the tree that carries this file would otherwise find a mismatch and have no way to tell whether it meant tampering or the transition.

## 1. Governing packet, preflight, and what authorized this work

`WO-RLO-006` implements the already approved `REQ-RLO-015` and `REQ-RLO-016` under `SPEC-RLO-005`, `ARCH-RLO-005`, `ADR-RLO-005` and `VER-RLO-005`. It adds no requirement, amends no governing artifact, and places no byte in the distributed surface. The owner holds the engineering-owner, release-owner, quality-owner, security-owner and repository-owner roles in this repository, so nothing here is approved by implication.

The work order exists because of an owner routing decision taken on 2026-08-25 while `WO-RLS-011` was qualifying the 0.7.0 candidate: that work order measured the defect and could not repair it, because `.github/` is outside its approved execution scope, and the owner chose a separate work order over widening it, with the fix to land before 0.7.0 ships.

Four lifecycle acts, each on its own explicit owner decision and each applied with the governing exact public `0.6.0` evaluator from outside the checkout in isolated mode:

| Act | Recorded at | Applied how |
|---|---|---|
| `draft` → `approved` | 2026-08-25T17:55:39Z | released evaluator, outside the checkout |
| Start preflight | before the start transition | `PASS`, work order `approved` |
| `approved` → `in_progress` | 2026-08-25T19:07:27Z | released evaluator, outside the checkout |
| `in_progress` → `implemented` | 2026-08-25T20:22:47Z | released evaluator, outside the checkout |

The completion decision was taken against everything below, and `DR-WO-COMPLETE` requires `QG-G4-IMPLEMENTATION-EVIDENCE`: approved scope implemented, required checks passing, retained evidence identifying the work order, review preflight passing, and no scoped or repository blocker. Each of those five is a reading in this file, and the last was checked rather than assumed — the review preflight evaluates blockers and read `PASS`.

Review preflight at the handoff state this file describes: `PASS`, phase `review`, work order `WO-RLO-006 (in_progress)`, assurance `required` decided by `repository-owner`, reading manifest of 17 paths. Governing graph readings with the released evaluator outside the checkout: `validate` `PASS` at 888 artifacts, 0 errors, 50 pre-existing maintenance warnings; `doctor` 87 `PASS`, 0 `FAIL`. All three figures are unchanged from the approval reading, which is the point: this work order moves no artifact count and clears no warning.

## 2. Commits

| Commit | Subject | Contents |
|---|---|---|
| `826c72cfdaa3401cccf06c67943c5315221c3f72` | merge of pull request #154 | the branch point, `origin/main` |
| `4a62ade7442ff064fff537be7ee089cf695ab872` | `docs(release-orchestration): start WO-RLO-006 …` | the start transition and the domain-index bullet; no code |
| `ceab133e64893ae98ccb0bc5167f5086ff185d6e` | `fix(publication-rehearsal): classify a junction without the 3.12 predicates` | the repair and its tests: 2 files, 404 insertions, 8 deletions |

Branch `fix/wo-rlo-006-reparse-point-teardown`. The work-order prose correction in section 4 and this file followed in a third commit, because the readings in sections 6 and 7 could only be taken once `ceab133` existed. The completion transition is a fourth commit, the one this file is retained in; it names no hash of its own.

`ceab133` is the commit that produced the repaired behaviour, so it is the commit a `VREC` for this work order would bind. It has not been amended since the rehearsal reading in section 6 was taken against it, and it must not be.

## 3. The defect, and the primitive it rests on

`.github/scripts/rehearse_publication.py` classified junctions in two places, and both were silently inert before Python 3.12:

- `_path_is_junction` read `getattr(os.path, "isjunction", None)` and returned `False` when the attribute was absent.
- `_is_link` checked `entry.is_symlink()`, then read `getattr(entry, "is_junction", None)` and returned `False` when that attribute was absent.

`os.path.isjunction` and `os.DirEntry.is_junction` arrived in Python 3.12. `pyproject.toml` declares `requires-python = ">=3.11"` and every lane in `.github/workflows/publication-rehearsal.yml` pins `PYTHON_VERSION: "3.11"`, so the inert branch is not a floor for old interpreters: it is the runtime the rehearsal runs on. `publish-pypi.yml`, the orchestrator the rehearsal mirrors, pins 3.11 as well.

The primitive was measured directly on this workstation rather than inferred from release notes. A junction created with `cmd /c mklink /J`:

| Reading | CPython 3.11.9 on Windows | CPython 3.14.6 on Windows |
|---|---|---|
| `os.path.isjunction` present | no | yes |
| `Path.is_junction` present | no | yes |
| `os.DirEntry.is_junction` present | no | yes |
| `stat.FILE_ATTRIBUTE_REPARSE_POINT` present | yes | yes |
| `stat.IO_REPARSE_TAG_MOUNT_POINT` present | yes | yes |
| `os.stat_result.st_file_attributes` present | yes | yes |
| `os.stat_result.st_reparse_tag` present | yes | yes |
| `link.is_symlink()` | `False` | `False` |
| `os.lstat(link).st_file_attributes` | `0x410`, reparse bit set | same |
| `os.lstat(link).st_reparse_tag` | `0xa0000003` == `IO_REPARSE_TAG_MOUNT_POINT` | same |
| `DirEntry.stat(follow_symlinks=False)` | carries both members, same values | same |
| `DirEntry.is_dir(follow_symlinks=False)` | `True` | `True` |
| `os.scandir(link)` | lists the target's contents | same |
| directory symlink creation | withheld, `WinError 1314` | withheld, `WinError 1314` |

Two facts from that table decide the repair. The reparse state is fully observable on 3.11, so a route exists below the 3.12 predicates. And a junction is not a symbolic link on either interpreter, so the symlink predicates cannot cover it — which is why a junction needs a predicate of its own rather than a widened symlink check.

The last row is why the defect reproduces on this workstation at all: symbolic-link creation is withheld here, so `tests/test_publication_rehearsal.py`'s `try_directory_symlink` helper falls back to `mklink /J` and the tests exercise a junction. Where the privilege is granted the helper produces a symlink instead and the junction routes are never reached. Section 7 shows that this is exactly what happens on the hosted runner.

## 4. The two consequences are not symmetrical

This is the one place where measurement contradicted the description written while the work order was `draft`. Both *The defect* in `WO-RLO-006` and the recorded `approved` → `in_progress` reason say the recursion "deletes the target's contents" or "deletes a path outside the rehearsal root". That is true of a junctioned rehearsal **root** and false of a junction **inside** the derived tree. Recorded lifecycle reasons are immutable decision history and the approved sections are the basis the owner approved, so the correction is stated here and in a clearly marked subsection of the work order, and neither is rewritten.

Both cases were measured by loading the unrepaired module out of a control worktree at `4a62ade` and the repaired module out of the working tree, planting a real junction, and running `remove_tree_without_following_links` directly.

### A junctioned rehearsal root: the data-loss case

| Program and runtime | Outcome | Target content afterwards |
|---|---|---|
| unrepaired, 3.11.9 | no refusal; 4 paths deleted, then the junction removed | **gone** — `keep.txt`, `precious/deeper.txt` and `precious` all deleted |
| unrepaired, 3.14.6 | `RehearsalError: teardown refused a linked rehearsal root` | intact |
| repaired, 3.11.9 | `RehearsalError: teardown refused a linked rehearsal root` | intact |
| repaired, 3.14.6 | `RehearsalError: teardown refused a linked rehearsal root` | intact |

This is real deletion of paths the rehearsal did not create, and it is a `SPEC-RLO-005` rule 21 violation. The root refusal has **no second line of defence**: `root_real = os.path.realpath(root)` resolves a junctioned root to its target, so every path inside the target is "within the root" and the containment guard cannot catch anything. The predicate, not the guard, is what has to be right here. That asymmetry is recorded in a test docstring so it cannot be lost again, and it is offered to the owner in section 10 as an observation rather than acted on, because hardening the guard is outside this work order's scope.

### A junction inside the derived tree: the residue case

| Program and runtime | Outcome | Target content afterwards |
|---|---|---|
| unrepaired, 3.11.9 | `RehearsalError: teardown refused a path outside the rehearsal root: …\escape\keep.txt`; derived tree left behind; `deleted` empty | intact |
| unrepaired, 3.14.6 | junction unlinked; tree removed; 3 paths reported | intact |
| repaired, 3.11.9 | junction unlinked; tree removed; 3 paths reported | intact |
| repaired, 3.14.6 | junction unlinked; tree removed; 3 paths reported | intact |

The walk does recurse into the junction, which is the `SPEC-RLO-005` rule 19 violation — trees must be deleted "by unlinking links rather than recursing through their targets". But the containment guard then refuses the first path reached inside the target, because that path's parent canonicalizes outside the root. So the effect is an **aborted teardown that leaves residue**, not a deletion outside the root. Rule 21's "never leave residue silently" is not breached silently: the abort raises. The harm is a failed rehearsal and a derived tree left on disk, which is a gate failure rather than data loss.

Stating this precisely matters because the two readings support different claims. "The rehearsal can delete a path it did not create on the pinned runtime" is true, and the junctioned root is the case that establishes it.

## 5. The repair

Each probe keeps the 3.12 predicate as a fast path and falls back to the Windows reparse state through `os.stat_result.st_file_attributes` and `st_reparse_tag`. Both routes are named by a module constant rather than written inline, so a test can withdraw either one on an interpreter that has it and prove which surviving route decided the answer. The pattern mirrors `se_harness/interpreter_safety.py` and is **duplicated rather than imported**: the program's docstring and the suite's `PortableBoundaryTests` require it to run from a bare interpreter with no repository module on the import path, and the packaged `se_harness`, `templates` and `scripts` surfaces must not mention `rehearse_publication`.

The accepted reparse tag is **exactly** `IO_REPARSE_TAG_MOUNT_POINT`, which is the narrower of the two classifications the work order asked to be chosen between and stated. Classifying by the reparse attribute alone was rejected: deduplicated files, cloud placeholders and application execution aliases all carry that attribute and are ordinary files or directories that teardown must walk, and unlinking one of them would be a fresh defect of the same shape as the one being fixed. A symbolic link is already classified by `entry.is_symlink()` and `Path.is_symlink()`, so accepting `IO_REPARSE_TAG_SYMLINK` as well would add nothing and would blur two predicates the sibling loaders keep distinct.

A platform that publishes neither constant, or a stat result that carries neither member, answers `False` by construction. That is correct rather than merely safe: there are no junctions off Windows, and symbolic links there are classified by the symlink predicates.

Behaviour after classification is unchanged, and this was checked rather than assumed: the containment guard still canonicalizes the parent and never the candidate, the two `RehearsalError` messages the existing tests match on are untouched, an ordinary directory is still walked rather than unlinked, and every removal is still appended to `deleted` — the rehearsal's own assertions and its reported derived-path count read that list, and the figure it reports is unchanged at 7550 derived paths.

## 6. Test and rehearsal figures, each labelled by runtime and platform

Every figure below was taken on Windows 11 on this workstation. A reading on one runtime is not a reading on the other, and the two are never merged.

### Full suite

| Program and commit | Runtime | Tests | Result | Skips |
|---|---|---|---|---|
| unrepaired, `4a62ade` | CPython 3.11.9 | 1002 | **1 failure, 1 error** | 23 |
| unrepaired, `4a62ade` | CPython 3.14.6 | 1002 | `OK` | 23 |
| repaired, `ceab133` | CPython 3.11.9 | 1016 | `OK` | 24 |
| repaired, `ceab133` | CPython 3.14.6 | 1016 | `OK` | 23 |

The two pre-existing failures are `TeardownTests.test_a_linked_root_is_refused_rather_than_followed` (failure) and `TeardownTests.test_a_link_out_of_the_root_is_unlinked_and_its_target_survives` (error). Both pass on the repaired program **unedited**; neither test was touched, which the work order made a stop condition.

The count rises by exactly 14, which is the number of tests added. The single extra skip on 3.11 is the new route-agreement test, which has no 3.12 predicate to agree with there and reports that as its skip reason. The 23 skips common to every row are the pre-existing Windows-only guards.

### The added tests, and the demonstration that they bite

Fourteen tests were added, in two classes placed alongside the existing `TeardownTests`.

`JunctionTeardownTests`, four tests, all forcing the pinned lane's combination on whatever interpreter runs them:

1. a junction out of the root is unlinked and its target survives;
2. a junctioned rehearsal root is refused rather than followed, and `deleted` stays empty;
3. the containment guard still refuses when **no** route classifies a junction — the defence-in-depth case, which pins the residue-not-data-loss behaviour of section 4 and records in its docstring that the root refusal has no equivalent fallback;
4. a tree with no links is still removed on the pinned combination, so the repair cannot have turned ordinary directories into unlinked ones.

`JunctionClassificationTests`, ten tests: that a junction is not a symbolic link on any route; that the reparse route classifies a real junction with the 3.12 predicates withdrawn, for both the path form and the `DirEntry` form; that the reparse state of a real junction is the mount-point tag through `os.lstat` and through `DirEntry.stat(follow_symlinks=False)` alike; that the two routes agree where both exist; that an ordinary directory, a regular file, and an absent path are not junctions; that withdrawing every route classifies nothing rather than raising; that the mask and the tag must both agree; that absent constants classify nothing; and that no reparse tag other than the mount point is named anywhere in the program's own source, asserted over that source rather than trusted to a comment.

The mask-and-tag test substitutes two `stat` constants every runtime publishes, so the Linux lane exercises the same classification rule instead of skipping it. Its third row is the narrowness requirement of section 5: a reparse point carrying any other tag is not a junction.

Against the unrepaired program all fourteen tests error on both 3.11.9 and 3.14.6, because withdrawing a route that program does not read is not expressible there. That is a real failure and it satisfies the work order's requirement that at least one new test fail against the current implementation, but it is a weak demonstration and is reported as such rather than dressed up: the mechanism is a missing module constant, not a followed link. The behavioural demonstrations are the direct before-and-after measurements in section 4 and the two 3.11 baseline failures above.

The tests that need a real junction skip where no junction can be created, which off Windows is every lane. That is a platform-absent primitive, not a skip taken to reach green: the classification rule itself is covered on every platform by the substituted-constant test, and the symlink shape is covered on every platform by the pre-existing `TeardownTests`.

### Credential-free publication rehearsal, Windows, CPython 3.11.9

| Candidate | Result | `candidate-unit-suite` | Mechanics |
|---|---|---|---|
| `4a62ade` (unrepaired) | **FAILED** | `failed`: "candidate unit suite exited 1 with 2 failing tests: test_a_link_out_of_the_root_is_unlinked_and_its_target_survives, test_a_linked_root_is_refused_rather_than_followed" | 20 executed, 2 excluded, 1 failed |
| `ceab133` (repaired) | **REHEARSED** | `executed`: candidate unit suite passed (1016 tests) | 21 executed, 2 excluded |

Both runs report `teardown: 7550 derived paths removed without following a link`, so the repair changed nothing about the volume or the reporting of teardown.

The first run was taken with the repair present in the working tree but not yet committed, and it still failed. That is not a contradiction: the rehearsal exports the candidate from the repository archive, so it reads committed bytes and cannot see an uncommitted fix. It also reported `Inherited checkout: not clean, 2 uncommitted entries`. This is worth recording because it fixes the order of work — the fix must be committed before the rehearsal can confirm it, and the rehearsal reading therefore always describes a commit that already exists.

The two excluded mechanics are pre-existing exclusions with stated reasons, unrelated to this work order: `predecessor-view-qualification`, because no committed record binds the resolved `0.6.0` evaluator as its predecessor; and `recipe-bound-build-replay`, because no committed release record is a distribution-schema-2 subject with a bound build recipe.

### Divergence seam

`check-divergence` reads `EXACT` with `No uncovered or stale mechanic`, on CPython 3.11.9 on Windows. So this repair adds no mechanic, retires none, and moves no coverage — which is what the work order required and what keeps `publication_rehearsal_mechanics.json` untouched.

## 7. The hosted lane, read rather than guessed

The work order required the hosted `windows-2022` lane to be read at the pinned 3.11 and the pre-fix state recorded, "instead of guessing". It came back the opposite way from the local reading.

Run `32853109486`, event `push`, branch `main`, head `826c72cfdaa3` — the exact commit this branch is based on, carrying the unrepaired program. Read through the runs and jobs API rather than from a summary badge:

| Job | Id | Conclusion | Reading |
|---|---|---|---|
| Refuse orchestrator and rehearsal divergence | `97818512535` | success | divergence `EXACT`, no uncovered or stale mechanic |
| Rehearse the credential-free path on Linux | `97818512837` | success | `REHEARSED`; suite passed at 1002 tests; teardown 7991 paths |
| Rehearse the credential-free path on Windows | `97818512899` | success | `REHEARSED`; suite passed at 1002 tests; teardown 7548 paths; `Image: windows-2022` |

**The hosted Windows lane was green before this fix, not red.** The defect was latent there, not failing. The last fifteen runs of that workflow are all `success` or `cancelled`, with no failure on either platform.

What that reading establishes and what it does not. It establishes that the hosted Windows runner did not take the junction fallback, because a junction fallback fails the suite exactly as it does here. It does not directly read the privilege: the rehearsal reports only the suite's pass and its test count, so the log carries no skip count that would separate "the runner granted the symlink privilege, so `try_directory_symlink` produced a symlink and `entry.is_symlink()` classified it" from "the runner could create no directory link at all, so both tests skipped". The first is the near-certain reading, because `mklink /J` needs no privilege on NTFS and would have to have failed for the second to hold, but it is an inference from a pass rather than a measurement of the primitive. Settling it directly would need a `workflow_dispatch` on that lane, which is an owner decision and is offered in section 10.

**No hosted reading of the repaired program is available, and this is structural.** `publication-rehearsal.yml` triggers on `pull_request`, on `push` **to `main` only**, and on `workflow_dispatch`. A push of this branch cannot trigger it. A hosted reading of the fix therefore requires either a pull request or a `workflow_dispatch`. The owner authorized the pull request and declined the dispatch as redundant to it, so the reading will exist on the pull-request run and not in this record: **as written, the fix is proven on this workstation and unproven on the hosted runner** — where, per the paragraph above, the unrepaired code was already green, so the hosted lane is the weaker of the two readings for this particular defect.

## 8. Scope conformance

The five declared `[execution_scope]` paths, and what was actually changed:

| Declared path | Changed |
|---|---|
| `.github/scripts/rehearse_publication.py` | yes — the two probes and one shared classifier; 60 lines touched |
| `tests/test_publication_rehearsal.py` | yes — 14 new tests, 4 new module-level helpers, one added import; no existing test edited |
| `docs/engineering/release-orchestration/README.md` | yes — one bullet, as *In scope* allowed and no more |
| `docs/engineering/release-orchestration/work-orders/WO-RLO-006.md` | yes — two lifecycle events and the prose that records them |
| `docs/engineering/release-orchestration/evidence/` | yes — this file |

Nothing outside those five paths was touched. Verified by diff rather than asserted.

Every listed stop-and-escalate condition was checked and none fired. No governing artifact needed amendment: `SPEC-RLO-005` rules 19 and 21 already require the correct behaviour and the implementation simply did not meet them. No existing teardown test needed editing. The hosted Windows lane was not red for another reason — it was not red at all. The reparse predicate does distinguish a junction from an ordinary directory on the configuration reachable here, and section 5 records the narrower classification that keeps it distinguishable. The runtime floor did not need to move; raising it would have hidden the defect rather than fixed it, and it is a separate decision with its own consumer consequences.

## 9. Actions listed as out of scope, and not performed

None of the following was done: any change to `SPEC-RLO-005`, `VER-RLO-005`, `REQ-RLO-015`, `REQ-RLO-016`, `ARCH-RLO-005` or `ADR-RLO-005`; any change to `publication_rehearsal_mechanics.json`, `.github/workflows/publication-rehearsal.yml`, the mechanic inventory or the divergence seam; any change to `requires-python` or the pinned `PYTHON_VERSION`; any edit to the two existing teardown tests; any file under `se_harness/` or `templates/`; anything under `docs/engineering/release-0-7-0/`, including `REL-SEH-015`, `WO-RLS-011` and its retained evidence.

Performed, each on its own explicit owner decision taken with these readings in front of them and neither by implication: the `in_progress` → `implemented` transition, which is the owner's `DR-WO-COMPLETE` decision, recorded as the fourth lifecycle event; and a push of this branch with a pull request opened for the owner to merge. The owner was asked separately whether to `workflow_dispatch` the rehearsal lane and declined it, on the ground that the pull request runs the same lane on both platforms.

Not performed and not authorized: any `VREC` for this work order; any merge, which is the owner's act on the pull request; any promotable build; any `workflow_dispatch`; any tag creation or movement; any GitHub Release, PyPI publication or Pages deployment; any `release/0.7` maintenance-line mutation; any credential use; any root-evaluator or lock change; any force push; and any history rewrite.

## 10. Disclosed limitations and observations for the owner

Recorded unsoftened, because each one is a thing a reader could otherwise mistake for settled.

1. **The root refusal is single-routed.** A junctioned root defeats the containment guard by construction, so the predicate is the only control. The repair makes the predicate correct on every supported runtime, but a future runtime or filesystem the predicate cannot classify would reopen the data-loss path with no fallback, unlike the in-tree case which the guard still catches. A textual `realpath` comparison on the root would add a second route but would refuse legitimate roots reached through a symlinked temporary directory or a Windows short-name alias, both of which this program deliberately supports. This is offered as an observation; hardening it is outside this work order and would touch `SPEC-RLO-005`'s teardown rules.
2. **No hosted reading of the fix exists at the time this record was written,** and none can be taken from a branch push, because the lane's `push` trigger is restricted to `main`. A pull request or a `workflow_dispatch` is required. The owner authorized the pull request, so a hosted reading will exist on the pull-request run — but it is not in this record, and a `VREC` must read it from the run rather than from here. Two cautions apply to reading it: the `pull_request` lane can silently never run while push-event checks show green, so the lane's own run has to be confirmed through the runs API; and a green reading proves the repair only if the runner takes the junction route, which section 7 shows it may not.
3. **The hosted pre-fix reading is an inference at one step.** The lane was green; that it was green *because the runner granted the symlink privilege* follows from the suite passing rather than from a reading of the privilege itself. A dispatched run that printed the skip count would settle it.
4. **The new tests' failure against the unrepaired program is structural, not behavioural.** All fourteen error on a missing module constant. The behavioural proof is the direct measurement and the 3.11 baseline failures, and this file does not present the fourteen errors as more than they are.
5. **The junction-shaped tests are Windows-only** and skip elsewhere. The classification rule is covered on every platform through substituted constants, and the symlink shape through the pre-existing tests, but no lane off Windows exercises a real junction because none can exist there.
6. **This file's `formal_snapshot_sha256` is a per-checkout figure, not a per-commit one,** and this work order measured that directly rather than repeating it as a caution. The digest hashes worktree bytes through `read_bytes()`, and `WO-RLO-006.md` is one of the artifacts it hashes, so line-ending materialization moves it. `core.autocrlf` is `true` on this workstation and no `.gitattributes` rule pins these documentation paths, so one artifact tree reads differently depending on how the checkout was made. Three readings of the artifact tree this record is retained alongside, all `888` artifacts and `0` errors. No artifact changed between the commit that first carried this file and the one that carries it now, so every figure below holds at both:

   | Checkout | `WO-RLO-006.md` bytes | Digest |
   |---|---|---|
   | no CRLF conversion (`core.autocrlf=false`; what the Linux lane reads) | LF | `862e8e69a8b7bdd95cfd0302805d74447978834ed9c7c7b00674c6215c7ed4c6` |
   | fresh checkout on this workstation (`core.autocrlf=true`) | CRLF | `b65eadbafb1cff44442b2d5e84aa6470b2988a988e57134ba9513788353f5162` |
   | the authoring worktree `C:\Users\mathi\wo_rlo_006_9931` | LF, while sibling artifacts were CRLF | `0dda6ebc7455e2c203f57660ff90e0ec3a5e22128e9bfc8ea1667af16b6fe944` |

   The binding block carries the first. The third **must not be quoted**: it is the figure an earlier draft of this file recorded, and it is reproducible by nothing — Git had not yet re-materialized the newly written files, so that worktree held a mixed state no clean checkout produces. It is listed only so that a reader who finds it in this branch's history knows what it was. This is a general hazard for any record binding a snapshot, not a fact about this work order: the checkout that produced the figure has to be named alongside it, and a figure taken in the worktree that just authored the files is the one most likely to be unreproducible.
7. **The evidence file is outside the snapshot, and that was verified rather than assumed.** The digest was measured before this file existed and again with it present, in the same worktree, and did not move: `formal_snapshot_digest` hashes artifacts, and retained evidence is not one. That is what makes a binding block possible at all — a digest that covered this file could not be written into it.
8. **The repaired classifier is duplicated from `se_harness/interpreter_safety.py`, not shared with it.** That is required — the program must import no repository module — but it means a future correction to the canonical predicate does not propagate here. `ADR-RLO-005` already records the deferred shared-implementation refactor and its revisiting condition; this duplication is a second instance of the same deferral and is named here so it is visible when that condition is next examined.
9. **Commit-bound verification is `required`, is not satisfied by this file, and is still owed.** The work order is now `implemented`, which is the ordering precondition — capture refuses while a work order is `in_progress` — but no `VREC` exists. One must bind `ceab133`, the commit that produced the repaired behaviour, and its evidence must be tracked at that commit, so the record cannot bind the branch tip that carries it. Preparing it is a separate accountable act and has not been started.
