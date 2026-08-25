# WO-RLO-006 Verification Evidence

Date: 2026-08-25

Authority: non-authoritative retained candidate evidence. This file does not approve an
artifact, authorize a diff, verify work, merge, release, publish, tag, or deploy. It
records what was measured, on which interpreter, on which platform, at which commit, and
what the measurements do not cover, so that an accountable assurance decision can be taken
over facts rather than over a summary. Every rehearsal figure quoted here carries the
rehearsal's own field `authority = "derived operational evidence; no formal lifecycle
transition"`.

Work order: `WO-RLO-006`, `status = "implemented"`, assurance classification
`commit_bound_verification = "required"` decided by the repository owner with the rationale
that "this changes the predicate that decides whether teardown unlinks a path or recurses
through it, which is the control `SPEC-RLO-005` rules 19 and 21 rely on to keep a rehearsal
from deleting anything it did not create. A wrong predicate deletes a link target outside
the rehearsal root, and the credential-free rehearsal is a pre-release assurance signal
that release approval reads, so assurance must bind the exact candidate commit that
produced the repaired behaviour."

Preparation of a `VREC` was authorized by the repository owner on 2026-08-25 through the
instruction `create the verification record for WO-RLO-006`, taken together with
`leave WO-RLO-006's retained record as it stands and carry the reading into the VREC`. The
second half of that instruction is a decision about this file: the retained implementation
evidence
`docs/engineering/release-orchestration/evidence/WO-RLO-006-implementation.md` is **not**
amended, and the hosted reading its limitation 2 said did not yet exist is carried here
instead. Preparation is not verification. The record this file supports is prepared
`ready`, and the assurance decision remains outstanding and is the owner's separate act.

## 1. Which tree the figures describe, and which commit the record binds

The repaired program is `.github/scripts/rehearse_publication.py`. Its content is
**byte-identical at every commit that matters here**, which is what makes the chain of
custody below possible at all:

| Commit | What it is | Blob of the repaired program |
|---|---|---|
| `ceab133e64893ae98ccb0bc5167f5086ff185d6e` | the repair, on `fix/wo-rlo-006-reparse-point-teardown` | `9e168266837330dc0f1338a02e94b79e4f9151b2` |
| `e9856a1da4221123a13459bfd2a9f61281942e4c` | the branch tip, the pull request's head | `9e168266837330dc0f1338a02e94b79e4f9151b2` |
| `95ef09f123fdb4d20ad39b06adf35564f5de969b` | GitHub's merge of `e9856a1` into `826c72c`, the tree the hosted run actually checked out | `9e168266837330dc0f1338a02e94b79e4f9151b2` |
| `d91ed5d362138adcece76dc1923443c5e9efbac4` | `origin/main`, after pull request #161 and then #162 merged | `9e168266837330dc0f1338a02e94b79e4f9151b2` |

`git diff --stat ceab133 e9856a1` reports three files and 299 insertions against 3
deletions — the domain index, the implementation evidence, and the work order's completion
transition. No executable content, no test, no workflow, no fixture and no recorded digest
differs between the commit that produced the behaviour and the head the hosted run read.
`ceab133` is an ancestor of `origin/main`; pull request #161 landed as a true merge, so it
is reachable and nothing this record says about it is orphaned.

**The record binds a fresh commit off `main`, not `ceab133`, and this departs from what the
implementation evidence expected.** That file's limitation 9 says a `VREC` "must bind
`ceab133`". It cannot: `capture-verification` requires every path passed to `--evidence` to
be tracked at the candidate commit, and this file does not exist at `ceab133` — nor does
the implementation evidence, which first appears at `e9856a1`. The work order was also
already `implemented` and merged before preparation was authorized. So the candidate is a
commit on `governance/vrec-rlo-006` off `d91ed5d` carrying this file, and the record's
provenance names it. What that costs and what it does not is stated in limitation 1 of
section 9. The figures below were measured over the tree of `d91ed5d`, which is `main`
itself and carries the merged repair unchanged.

This file is committed as the candidate and the record follows it in a later commit,
because a record cannot contain the hash of its own commit.

## 2. Environment

| Item | Value |
|---|---|
| Platform | `Windows-11-10.0.26200-SP0` |
| Interpreters | CPython 3.14.6 (default here) and CPython 3.11.9 (the version every hosted lane pins) |
| Git | 2.45.1.windows.1 |
| Checkout | `C:\Users\mathi\vrec_rlo006_9931`, `git worktree add` off `d91ed5d` |
| `core.autocrlf` | reads `true` from the system config; the worktree was created with it overridden to `false`, so nothing in it is converted |
| Line endings verified, not assumed | every one of the 1407 tracked files was compared to its blob: worktree bytes differ from blob bytes in **0** of them |
| CRLF control checkout | `C:\Users\mathi\snapctl_crlf_9931`, `git -c core.autocrlf=true worktree add --detach d91ed5d`, used only for section 8 |
| Pre-merge control checkout | `C:\Users\mathi\ctrl_9931` at `826c72c`, `main` before the repair merged |
| Governing evaluator | released `se-harness==0.6.0` in `C:\Users\mathi\se_harness_eval_060`, run from outside the checkout with `-I` |
| Hosted runners | `ubuntu-latest` and `windows-2022`, CPython 3.11 |

The retained implementation evidence for this work order is blob
`b7dc17d7e5f2dcbf0e43a5d1c63e9a43dfad6f64` at `d91ed5d`, 31318 bytes with zero CR bytes,
SHA-256 `5cd1371f6d1f1cf1c9e566f4459017c738503567b9d1b76ed47883058719c1f0`. It is referenced
by digest and deliberately **not** bound by this record, so that it stays exactly as the
owner decided it should. Everything an assurance decision needs is restated here.

## 3. What the candidate delivers

One defect repaired in `.github/scripts/rehearse_publication.py`: 60 changed lines, plus
352 insertions of tests in `tests/test_publication_rehearsal.py`, one domain-index line,
and the work order. Nothing else. No governing artifact is amended, no requirement is
added, and no byte enters the distributed surface — `.github/` is not packaged.

The defect. `SPEC-RLO-005` rules 19 and 21 require teardown to remove a derived tree by
unlinking links rather than recursing through their targets, and never to leave residue
silently. The two predicates that classified a Windows junction were
`os.path.isjunction` and `os.DirEntry.is_junction`, both of which arrived in CPython 3.12.
`requires-python` is `>=3.11` and every rehearsal lane pins 3.11, so on the pinned lane
neither predicate existed and both classifiers returned `False`.

The repair gives each classifier a second route that reads the Windows reparse state
directly, and names both routes as module constants rather than writing them inline so that
a test can withdraw either one on a runtime that has it and measure which surviving route
decided the answer:

- `OS_PATH_JUNCTION_PREDICATE = "isjunction"` and `ENTRY_JUNCTION_PREDICATE = "is_junction"`
  are tried first where present.
- `_reparse_state_reports_junction` reads `st_file_attributes` against
  `stat.FILE_ATTRIBUTE_REPARSE_POINT` and requires `st_reparse_tag` to equal
  `stat.IO_REPARSE_TAG_MOUNT_POINT` — **exactly** the mount-point tag. A platform or a stat
  result carrying neither answers `False` by construction, which is correct on POSIX, where
  there are no junctions and symbolic links are already classified by the symlink
  predicates.
- The classifier is duplicated from `se_harness/interpreter_safety.py` rather than imported,
  because this program must run from a bare interpreter with no repository module on the
  import path.

Fourteen tests were added in two classes, `JunctionTeardownTests` (four) and
`JunctionClassificationTests` (ten). The file's test count moves from 121 at the pre-merge
control `826c72c` to 135, and the suite total from 1002 to 1016.

## 4. Independent behavioural verification

`VER-RLO-005`'s *Independence* clause requires expectations to come from controlled
fixtures and independently derived facts, "not by calling the rehearsal's own declaration
or classifier to produce the expectation it is then compared against". The packet's own
fourteen tests satisfy the contract but read the same `stat` module attributes the program
reads, so a separate probe was written for this record that does not.

`C:\Users\mathi\probe_vrec_rlo006_9931.py` loads the merged program out of this checkout by
file path, plants a real junction with `cmd /c mklink /J`, and forms its expectation from
**literal** Windows constants — `0x400` for the reparse attribute and `0xA0000003` for the
mount-point tag — deliberately not from `stat.FILE_ATTRIBUTE_REPARSE_POINT` or
`stat.IO_REPARSE_TAG_MOUNT_POINT`. It then calls
`remove_tree_without_following_links` directly and reports, per case, the outcome, the
number of paths the program recorded as deleted, and what survives inside the junction
target.

| Case | Shape | 3.11.9 | 3.14.6 |
|---|---|---|---|
| predicates present | `os.path.isjunction` / `os.DirEntry.is_junction` | absent, absent | present, present |
| independent predicate on the planted root | literal-constant classification | `True` | `True` |
| **A** — the rehearsal root itself is a junction | 3 paths inside the target | `RehearsalError: teardown refused a linked rehearsal root`; 0 deletions; target intact | same; 0 deletions; target intact |
| **B** — a junction inside the derived tree | root, a subdirectory, its own file, and the link | completed; root gone; 4 deletions; target intact | same |
| **D** — case A with the reparse route withdrawn | the 3.12 predicates are the only route left | **NO REFUSAL**; 4 deletions; **target survivors `[]`** | refusal; 0 deletions; target intact |

Case D is the measurement that matters. On 3.11.9 — the runtime every lane pins —
withdrawing the reparse route empties the junction target: `keep.txt`, `precious/deeper.txt`
and `precious` are all deleted, along with the link, and the program reports 4 removals as
if they were its own derived paths. That is deletion of paths the rehearsal did not create,
which is the `SPEC-RLO-005` rule 21 violation. On 3.14.6 the same withdrawal changes
nothing, because the 3.12 predicate still classifies the junction.

This **independently reproduces** the figure the implementation evidence measured by a
different method — it loaded the unrepaired module out of a control worktree and recorded
"no refusal; 4 paths deleted … gone" — and adds one fact that method could not establish:
*which* route decides the answer on each runtime. It is not a stronger claim than the
implementation record's; it is the same claim reached without trusting either the program's
own constants or the pre-repair module.

Case B is a different tree shape from the implementation record's residue case, so its
deletion count of 4 is not comparable with that record's 3. It is reported to show the
in-tree junction is unlinked rather than followed, with the target intact.

The asymmetry between A and B is the thing the packet cannot fix and the implementation
record raised as an observation. A junctioned **root** has no second line of defence:
`root_real = os.path.realpath(root)` resolves it to its target, so every path inside the
target is "within the root" and the containment guard catches nothing. The predicate is the
only control there. An in-tree junction is still caught by the guard, which is why case D's
damage is confined to the root shape. Hardening the root would touch `SPEC-RLO-005`'s
teardown rules and is outside this work order.

## 5. The hosted two-platform reading of the repaired program

This closes the implementation evidence's limitation 2, which recorded that no hosted
reading of the fix existed when that file was written. It exists now, and it was confirmed
through the runs API rather than from a checks summary, because a `pull_request`-only lane
can silently never run while push-event checks show green.

Run [32895505173](https://github.com/mmzen/se_harness/actions/runs/32895505173), workflow
`Publication Rehearsal`, event `pull_request`, `run_attempt` 1, conclusion `success`, head
`e9856a1`, branch `fix/wo-rlo-006-reparse-point-teardown`. The tree it checked out is the
merge commit `95ef09f1`, whose parents are `826c72c` and `e9856a1` and whose copy of the
repaired program is the same blob `9e168266`.

| Job | Id | Runner | Result | Figures |
|---|---|---|---|---|
| Refuse orchestrator and rehearsal divergence | `97957138583` | `ubuntu-latest` | success | `No uncovered or stale mechanic.`; five excluded orchestrator jobs each with its causing attribute |
| Rehearse the credential-free path on Windows | `97957138809` | `windows-2022` | success | `REHEARSED`; candidate `95ef09f123fd`; `candidate unit suite passed (1016 tests)`; `teardown: 7552 derived paths removed without following a link`; `Inherited checkout: core.autocrlf=true, so the candidate checkout converts line endings` |
| Rehearse the credential-free path on Linux | `97957138945` | `ubuntu-latest` | success | `REHEARSED`; candidate `95ef09f123fd`; `candidate unit suite passed (1016 tests)`; `teardown: 7995 derived paths removed without following a link` |

Both legs report the same two exclusions in the same words, and both are the exclusions
`VER-RLO-005` already admits: `predecessor-view-qualification`, because no committed record
binds the resolved `0.6.0` evaluator as its predecessor — `RLS-SEH-012` binds `0.5.0` — and
`recipe-bound-build-replay`, because the one committed record declares distribution schema 1
and the replay has no schema-2 subject. Neither has ever executed here and neither is proven
by this candidate.

One further hosted reading of the repaired program, from a different workflow on the same
head: run `32895505163`, `SE Harness Candidate Evidence`, event `pull_request`, conclusion
`success`, job `Candidate source evidence` (`97957138196`, `ubuntu-latest`) reports the full
suite as `Ran 1016 tests` and `OK (skipped=11)`. That is the first Linux skip count taken
over the repaired program: the junction-shaped tests skip off Windows, as designed, and the
test total matches this workstation's exactly.

What the hosted reading establishes and what it does not. It establishes that the repaired
program rehearses `REHEARSED` on both runner types with the 1016-test suite passing, and
that teardown removed 7552 and 7995 derived paths respectively without following a link. It
does **not** read the Windows symlink privilege: the rehearsal reports the suite's pass and
its test count but no skip count, so the log cannot separate "the runner granted the
privilege, `try_directory_symlink` produced a symlink, and `entry.is_symlink()` classified
it" from "the runner took the junction route and the repaired predicate classified it".
Before the repair a green Windows leg carried information, because the junction route failed
the suite there; now both routes pass, so the pass no longer distinguishes them. Settling it
directly would need a `workflow_dispatch` printing the skip count, which is an owner
decision and is offered in section 9.

## 6. Local qualification at the candidate tree

Measured over `d91ed5d` in the checkout named in section 2.

| Measurement | 3.14.6 | 3.11.9 |
|---|---|---|
| Full suite | `Ran 1016 tests`, `OK (skipped=23)` | `Ran 1016 tests`, `OK (skipped=24)` |

The single extra skip on 3.11 is the new route-agreement test, which has no 3.12 predicate
to agree with there and reports that as its reason. The 23 common skips are the pre-existing
Windows-only guards. Neither figure is comparable with the hosted Linux 11, and skip counts
are a pass condition nowhere in this packet.

| Measurement | Result |
|---|---|
| `check-divergence --repository . --cross-check-yaml` | `EXACT`, exit 0, `Rehearsed jobs: qualify, resolve on Linux, Windows`, `Rehearsal lane platforms: Linux, Windows`, five excluded jobs each with its causing attribute, `No uncovered or stale mechanic.` |
| Independent probe, both interpreters | section 4 |
| `git diff --exit-code`, `git status --porcelain=v1 --untracked-files=all` | clean, 0 entries, before and after every measurement |

## 7. Gate results at the candidate

Every gate `AGENTS.md` names was run. The governing verdicts come from the released `0.6.0`
evaluator executed from outside the checkout in isolated mode; the in-tree runs are recorded
as boundary evidence and carry no verdict.

| Gate | Result |
|---|---|
| `python -m unittest discover -s tests -p "test_*.py"` | 1016 tests, OK, on both interpreters |
| Governing `validate` | `Artifacts: 889 | Errors: 0 | Warnings: 50`, all `maintenance` |
| Candidate `scripts/validate_engineering_artifacts.py --root .` | the same 889 / 0 / 50 |
| `python scripts/validate_release_distributions.py --root .` | `PASS (1 distribution-bearing record)` |
| `python -m se_harness --help` | usage reported |
| Governing `doctor` | 87 `PASS`, 0 `FAIL` |
| Governing `preflight . --work-order WO-RLO-006 --phase review` | `Harness preflight: PASS`, work order `WO-RLO-006 (implemented)`, assurance `required` decided by `repository-owner`, no diagnostic |
| In-tree `doctor` | 37 `FAIL` |

The in-tree `doctor` skew was controlled rather than explained away. The pre-merge control
checkout at `826c72c` reports **37** `FAIL` as well, and `diff` over the two sorted lists of
`FAIL` names is empty. The skew is therefore inherited candidate-versus-released boundary
state that this packet neither causes nor repairs. The governing `doctor`, which is the run
that carries a verdict, has none. The artifact count is 889 here against the 888 the
implementation evidence recorded; the difference is pull request #162's `WO-REB-023`
governing packet arriving on `main` afterwards, and is nothing to do with this work order.

## 8. The formal snapshot is a per-checkout figure, and both readings are given

The implementation evidence's limitation 6 measured this directly and it holds here.
`formal_snapshot_digest` hashes worktree bytes, `WO-RLO-006.md` is one of the artifacts it
hashes, and no `.gitattributes` rule pins these documentation paths, so the same commit
reads differently depending on how the checkout was made. Both readings below were taken at
`d91ed5d`, with the released `0.6.0` evaluator's own
`se_harness.workflow._validation` and `se_harness.workflow_compliance.formal_snapshot_digest`
— the exact pair `harnessctl check` calls — and both report 889 artifacts and 0 errors.

| Checkout | `WO-RLO-006.md` CR bytes | Digest |
|---|---|---|
| this checkout, no CRLF conversion (what the Linux lane reads) | 0 | `509659ac29b5df72ec441faabcf2fc54438d7200e09a02970713bc8cb96d1dcd` |
| `git -c core.autocrlf=true worktree add --detach d91ed5d` | 345 | `dcf122fd53ad09b10bb88d78f532ed032b96dbfcb8d60fed634f95d8528a3403` |

Neither is the `862e8e69…` the implementation evidence bound, and that is expected rather
than a discrepancy: that figure was taken over 888 artifacts before `main` gained pull
request #162's packet. A reader recomputing it against this tree will not reproduce it, and
the reason is an artifact count that moved for an unrelated reason, not tampering.

The record's own `artifact_snapshot_sha256` is produced by `capture-verification` in this
checkout, so it follows the first convention above. That is a property of the checkout the
record was captured in and travels with it.

## 9. Disclosures

These are the limits the assurance decision is taken over. None is a defect being hidden;
each is a boundary of what was measured. Limitations 3 through 9 carry the implementation
evidence's own disclosures forward unsoftened, because that record is not amended and a
reader of this one must not have to reconstruct them.

1. **The record binds a fresh commit off `main`, not the commit that produced the
   behaviour.** `ceab133` is what the implementation evidence expected to be bound, and it
   cannot be: the bound evidence must be tracked at the candidate, and neither this file nor
   the implementation evidence exists at `ceab133`. What is lost is the direct binding. What
   replaces it is measured, not asserted — the repaired program is blob `9e168266` at
   `ceab133`, at the pull request head `e9856a1`, at the merge commit `95ef09f1` the hosted
   run read, and at `d91ed5d` this candidate branches from. A reader who wants the behaviour
   bound to `ceab133` has that chain and can check every link. Merging this record's pull
   request must be a **true merge**: a squash or a rebase would rewrite the bound commit, and
   a verified record can never be re-pointed at a later one.
2. **The hosted Windows leg no longer distinguishes the two junction routes.** Section 5
   states this in full. Before the repair a Windows pass implied the symlink privilege; now
   both routes pass. A `workflow_dispatch` printing the suite's skip count would settle
   which primitive the runner offers, and that dispatch is an owner decision that has not
   been requested or taken.
3. **The root refusal is single-routed.** A junctioned root defeats the containment guard by
   construction. The repair makes the predicate correct on every supported runtime, but a
   future runtime or filesystem it cannot classify reopens the data-loss path with no
   fallback, unlike the in-tree case the guard still catches. A textual `realpath` comparison
   would add a second route and would refuse legitimate roots reached through a symlinked
   temporary directory or a Windows short-name alias, both of which this program
   deliberately supports.
4. **The added tests' failure against the unrepaired program is structural, not
   behavioural.** All fourteen error there on a missing module constant, because withdrawing
   a route that program does not read is not expressible. That satisfies the work order's
   requirement that a new test fail against the current implementation and it is a weak
   demonstration. The behavioural proof is the direct measurement in section 4 and the
   implementation evidence's before-and-after tables.
5. **The junction-shaped tests are Windows-only** and skip elsewhere; no lane off Windows
   exercises a real junction, because none can exist there. The classification rule is
   covered on every platform through substituted constants and the symlink shape through the
   pre-existing `TeardownTests`.
6. **The repaired classifier is duplicated from `se_harness/interpreter_safety.py`, not
   shared with it.** The duplication is required — the program must import no repository
   module — but a future correction to the canonical predicate will not propagate here.
   `ADR-RLO-005` records the deferred shared-implementation refactor and its revisiting
   condition; this is a second instance of the same deferral.
7. **Two mechanics are excluded in every run on every platform,** and neither is proven by
   this candidate: `predecessor-view-qualification` has no committed record binding the
   resolved `0.6.0` evaluator as its predecessor, and `recipe-bound-build-replay` has no
   released distribution-schema-2 subject. `VER-RLO-005` admits `excluded` with a reason
   naming the measured identities, and both do that.
8. **Five orchestrator jobs are excluded by construction and are never rehearsed:**
   `github_release`, `observe`, `pages_build`, `pages_deploy` and `pypi`. The
   credential-bearing publication path itself therefore remains unrehearsed, by design.
9. **The divergence check covers one orchestrator,** `.github/workflows/publish-pypi.yml`.
   `.github/workflows/release-candidate-replay.yml` is not read, so a change to it is
   invisible to this seam.
10. **No Linux measurement is local.** Every Linux figure comes from a hosted
    `ubuntu-latest` runner; every local figure comes from one Windows 11 workstation. The
    local interpreters are 3.14.6 and 3.11.9; the hosted lanes pin 3.11.
11. **`main` moved under this preparation.** The artifact count is 889 here against 888 in
    the implementation evidence, because pull request #162 merged in between. That is why the
    formal snapshot in section 8 does not reproduce the bound figure in that record, and it
    is the reason both are stated with the checkout that produced them.
12. **A green rehearsal is not a proof that publication succeeds.** It proves the
    credential-free mechanics execute on both runner types and that the rehearsal has not
    drifted from the orchestrator. Every release act needs its own authorization.

## 10. Actions not performed

No `VREC` field was written by hand: the record is produced by the released `0.6.0`
evaluator's `capture-verification` at the candidate commit with a clean worktree, and it is
prepared `ready`, not verified. The `ready` → `verified` transition is the repository
owner's separate accountable act and has not been taken.

The retained implementation evidence
`docs/engineering/release-orchestration/evidence/WO-RLO-006-implementation.md` was not
amended, edited, or re-bound, on the owner's explicit decision of 2026-08-25.

No merge of any pull request, no tag, no branch other than `governance/vrec-rlo-006`, no
GitHub Release, no PyPI publication, no Pages deployment, no protected-environment approval,
no `workflow_dispatch` of any lane, no release record, no release-record preparation or
transition, no promotable distribution build, no assurance decision, no governor adoption,
no root-evaluator change, no credential acquisition, and no hosting or branch-protection
change.

No recorded digest, `VREC`, `RLS`, `REL` or evidence fact was rewritten or re-pointed, no
managed file was edited, and no committed file's bytes were converted — measured, in section
2, over all 1407 tracked files rather than assumed.
