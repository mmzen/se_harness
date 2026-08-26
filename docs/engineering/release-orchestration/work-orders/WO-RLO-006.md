+++
id = "WO-RLO-006"
type = "work_order"
title = "Detect junctions without the 3.12 predicates so teardown never follows a link"
status = "implemented"
owners = ["engineering-owner", "release-owner", "quality-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[assurance]
commit_bound_verification = "required"
rationale = "This changes the predicate that decides whether teardown unlinks a path or recurses through it, which is the control SPEC-RLO-005 rules 19 and 21 rely on to keep a rehearsal from deleting anything it did not create. A wrong predicate deletes a link target outside the rehearsal root, and the credential-free rehearsal is a pre-release assurance signal that release approval reads, so assurance must bind the exact candidate commit that produced the repaired behaviour."
decided_by = "repository-owner"

[relations]
implements = ["REQ-RLO-015", "REQ-RLO-016"]
specifications = ["SPEC-RLO-005"]
architecture = ["ARCH-RLO-005", "ADR-RLO-005"]
verification = ["VER-RLO-005"]

[execution_scope]
paths = [
  ".github/scripts/rehearse_publication.py",
  "tests/test_publication_rehearsal.py",
  "docs/engineering/release-orchestration/README.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-006.md",
  "docs/engineering/release-orchestration/evidence/",
]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T17:55:39Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-25, on the routing decision of the same day that this defect takes its own work order rather than a scope amendment on WO-RLS-011, and that it is fixed before 0.7.0 ships. Approval ratifies the proposed commit_bound_verification classification of required, decided by the repository owner: the change replaces the predicate deciding whether teardown unlinks a path or recurses through it, which is the control SPEC-RLO-005 rules 19 and 21 depend on. Measured immediately before this transition, on Windows and against a control worktree at 826c72cfdaa3401cccf06c67943c5315221c3f72 so the defect is confirmed pre-existing rather than caused by the 0.7.0 version bump: on CPython 3.11.9 the suite reports 1002 tests with one failure and one error in TeardownTests; on CPython 3.14.6 the same suite is green at 1002; and under 3.11 the credential-free publication rehearsal's candidate-unit-suite mechanic fails on Windows naming exactly those two tests. Validation with the governing exact public 0.6.0 evaluator outside the checkout: PASS at 888 artifacts, 0 errors, 50 warnings, and inspect reports 167 findings with 0 errors and 64 warnings, composition unchanged. Approval authorizes start preflight and then only the declared work inside the five declared execution-scope paths. It authorizes no amendment to SPEC-RLO-005, VER-RLO-005, REQ-RLO-015, REQ-RLO-016, ARCH-RLO-005 or ADR-RLO-005; no change to the mechanic inventory, the divergence seam or the pinned runtime; no edit to the two existing failing teardown tests; no byte in the distributed surface; no work inside docs/engineering/release-0-7-0/; and no candidate commit, promotable build, VREC or RLS work, tag, publication, deployment, maintenance-line mutation, credential use or root-evaluator change. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-25T19:07:27Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-25, taken after the exact-candidate readings of WO-RLS-011 were put to them with the measured failure in front of them. Start preflight PASS at phase start over branch state 826c72cfdaa3401cccf06c67943c5315221c3f72, the true merge of pull request 154, run with the governing exact public 0.6.0 evaluator outside the checkout in isolated mode; commit-bound verification is required and decided by the repository owner. The defect is measured, not inferred. On CPython 3.11.9 on Windows, os.path.isjunction and DirEntry.is_junction are both absent, so both junction predicates in .github/scripts/rehearse_publication.py answer False for a real junction; the same path reports st_file_attributes 0x410 with the reparse-point bit set and st_reparse_tag 0xa0000003 equal to IO_REPARSE_TAG_MOUNT_POINT, through os.lstat and through DirEntry.stat(follow_symlinks=False) alike, and both stat constants and both stat members are present on that runtime. DirEntry.is_dir(follow_symlinks=False) answers True for the junction and os.scandir lists the target's contents, so teardown recurses through the link and deletes a path outside the rehearsal root, and a junction rehearsal root is not refused. That is a SPEC-RLO-005 rule 19 and rule 21 violation with real data loss, not a cosmetic red: the publication-rehearsal lane pins Python 3.11 on windows-2022 and the hosted run would reach the same code. Reproduced locally because this workstation withholds symbolic-link privilege with WinError 1314, so the suite's helper falls back to mklink /J. Bounded to the five declared execution-scope paths. This start authorizes no candidate commit, no push, no pull request, no verification record, no release work, no tag, no publication, no deployment, no maintenance-line mutation, no credential use and no root-evaluator change, and it changes nothing in the 0.7.0 candidate or in REL-SEH-015's frozen gates array."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-25T20:22:47Z"
decided_by = "engineering-owner"
reason = "Completed on the engineering owner's explicit decision of 2026-08-25, taken with the measured readings and the disclosed gap in front of them. QG-G4-IMPLEMENTATION-EVIDENCE: review preflight PASS with commit-bound verification required, decided by the repository owner; validate PASS at 888 artifacts, 0 errors, 50 pre-existing warnings; doctor 87 PASS, 0 FAIL; all three with the governing exact public 0.6.0 evaluator outside the checkout in isolated mode. Retained evidence is the release-orchestration record WO-RLO-006-implementation.md, naming artifact WO-RLO-006, checkpoint handoff, subject commit ceab133e64893ae98ccb0bc5167f5086ff185d6e, and formal snapshot 862e8e69a8b7bdd95cfd0302805d74447978834ed9c7c7b00674c6215c7ed4c6 with its checkout convention. Both junction predicates in the rehearsal program now fall back to the Windows reparse state, accepting exactly IO_REPARSE_TAG_MOUNT_POINT. Windows figures by runtime: unrepaired at 4a62ade, CPython 3.11.9 ran 1002 tests with 1 failure and 1 error; repaired at ceab133, 3.11.9 and 3.14.6 both run 1016 green, both pre-existing teardown tests passing unedited. Credential-free rehearsal at ceab133 on 3.11.9: REHEARSED, candidate unit suite passed at 1016 tests, teardown 7550 derived paths; divergence EXACT, so no mechanic moved. Measurement corrected the draft harm description: a junctioned root is the data-loss case and has no containment-guard fallback, while a junction inside the tree is refused by the guard and leaves residue. That is recorded as prose, not as a rewritten lifecycle reason. Disclosed and not softened: no hosted reading of the repaired program exists, because publication-rehearsal.yml runs only on pull_request, on push to main, or on dispatch; the hosted windows-2022 lane was green before this fix, so the defect was latent there rather than failing. This completion authorizes no verification record, no candidate commit, and no release, tag, publication, deployment, maintenance or credential act."
+++

# Work Order: Detect junctions without the 3.12 predicates so teardown never follows a link

## Lifecycle

This work order is `implemented`. Its authoritative state, and the timestamp and
reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above; read those rather than this prose.

It was approved by the accountable engineering owner on 2026-08-25, which
ratified the `required` commit-bound verification classification that was written
as a proposal while it was `draft`. Approval authorized start preflight and then
only the declared work inside the five declared execution-scope paths; the
approval reason above states exactly what it does not authorize.

Start preflight then read `PASS`, and the same owner took an explicit start
decision on 2026-08-25, recorded in the second lifecycle event above. That
transition moves status only, so this paragraph is what records that the state
described here has advanced: start preflight has been run and implementation is
under way. The start reason repeats the boundary — the exclusions the approval
listed are unchanged by starting, and nothing in the 0.7.0 candidate or in
`REL-SEH-015`'s frozen `gates` array moves under this work order.

The measurement quoted in that start reason is a direct probe of the primitive on
this workstation rather than an inference from release notes, and it is recorded
in full in the retained evidence.

The same owner then took an explicit completion decision on 2026-08-25, recorded
in the third lifecycle event above, against a review preflight reading `PASS` and
the retained record
`docs/engineering/release-orchestration/evidence/WO-RLO-006-implementation.md`.
That transition moves status only, so this paragraph is what records that the
state described here has advanced: the declared work is done inside the five
declared execution-scope paths, and what remains owed is the commit-bound
verification the approval classified as `required`. No verification record exists
yet, and none of the exclusions the approval and the start listed is relaxed by
completion.

Completion is recorded with one gap disclosed rather than closed: there is no
hosted reading of the repaired program, because `publication-rehearsal.yml` runs
only on `pull_request`, on `push` to `main`, or on dispatch. The reading that does
exist is the pre-fix one, and it says the hosted lane was **green**, so the
missing reading confirms a repair rather than clearing a red.

### What the measurement corrected

The implementation is committed as `ceab133e64893ae98ccb0bc5167f5086ff185d6e`.
Measuring the unrepaired program directly showed that the two consequences this
work order describes are not symmetrical, and one sentence written while it was
`draft` is wrong. The sections below are left as the owner approved them and the
recorded lifecycle reasons are immutable decision history, so the correction is
stated here rather than by editing either.

*The defect* and the start reason both say the recursion "deletes the target's
contents" or "deletes a path outside the rehearsal root". That is true of a
junctioned rehearsal **root** and false of a junction **inside** the derived tree.

- A junctioned root is the data-loss case, and it has no second line of defence:
  a junctioned root makes the target the reference the containment guard compares
  against, so every path inside the target is "within the root". Measured on
  CPython 3.11.9 on Windows against the unrepaired program, the target was
  emptied — `keep.txt`, `precious/deeper.txt` and `precious` deleted, four paths
  reported, then the junction removed.
- A junction inside the derived tree is the residue case. The walk does recurse
  into it, which is the `SPEC-RLO-005` rule 19 failure, but the containment guard
  then refuses the first path reached inside the target because that path's parent
  canonicalizes outside the root. Measured: the remover raised "teardown refused
  a path outside the rehearsal root", the target and its content survived, and the
  derived tree was left behind. The effect is an aborted teardown leaving residue,
  not a deletion outside the root.

Neither correction changes the repair, the scope, or the conclusion that the
defect is real and pre-existing. It changes which sentence may be quoted as the
harm, and the retained evidence carries a test that pins the guard's remaining
behaviour so the distinction cannot be lost again.

One required reading came back the opposite way from the local one, and the
answer is recorded rather than guessed, as *In scope* required. The hosted
`windows-2022` lane at the pinned 3.11 was **green** before this fix, not red:
run `32853109486` on `main` at `826c72c` read `REHEARSED` with the candidate unit
suite passing at 1002 tests on both runner platforms. The defect was latent
there, not failing. The retained evidence states what that reading does and does
not establish.

This work order exists because of an owner routing decision taken on 2026-08-25
while `WO-RLS-011` was qualifying the 0.7.0 candidate. That work order measured
the defect below and could not repair it: `.github/` is outside its approved
execution scope, and the owner chose a separate work order over widening it,
with the fix to land before 0.7.0 ships. The measurement is retained in
`docs/engineering/release-0-7-0/evidence/WO-RLS-011-verification.md`.

## Objective

Make the rehearsal's link detection independent of the interpreter version, so
that teardown unlinks a junction instead of recursing through it on every runtime
this project supports, and so that a junctioned rehearsal root is refused rather
than followed.

## The defect

`.github/scripts/rehearse_publication.py` detects junctions in two places, and
both are silently inert before Python 3.12:

- `_path_is_junction` reads `getattr(os.path, "isjunction", None)` and returns
  `False` when the attribute is absent.
- `_is_link` checks `entry.is_symlink()`, then reads
  `getattr(entry, "is_junction", None)` and returns `False` when that attribute
  is absent.

`os.path.isjunction` and `os.DirEntry.is_junction` were both added in Python
3.12. `pyproject.toml` declares `requires-python = ">=3.11"`, and every lane in
`.github/workflows/publication-rehearsal.yml` pins `PYTHON_VERSION: "3.11"`, so
the inert path is not a theoretical floor: **it is the runtime the rehearsal
actually runs on.**

Two consequences follow, and both defeat a rule the specification states
directly:

1. In `remove_tree_without_following_links`, `walk` treats a junction as an
   ordinary directory, recurses into it, and deletes the target's contents.
   `SPEC-RLO-005` rule 19 requires trees to be deleted "by unlinking links rather
   than recursing through their targets", and rule 21 requires the rehearsal to
   "never delete a path the rehearsal did not create".
2. The root guard `root.is_symlink() or _path_is_junction(root)` does not fire on
   a junctioned root, so the refusal that makes every containment test meaningful
   never happens.

The junction shape is not exotic on Windows. Directory-symlink creation is
privileged there, so a virtual environment or a build tool leaves a junction
behind instead, which is exactly why `tests/test_publication_rehearsal.py`'s
`try_directory_symlink` helper falls back to `cmd /c mklink /J`.

### Measured effect

Measured on Windows in the `WO-RLS-011` qualification, both against the bumped
0.7.0 tree and against a control worktree at
`826c72cfdaa3401cccf06c67943c5315221c3f72`, so the defect is confirmed
pre-existing and not caused by the version bump:

- On CPython 3.11.9 the full suite reports 1002 tests with one failure and one
  error: `TeardownTests.test_a_linked_root_is_refused_rather_than_followed`
  fails, and
  `TeardownTests.test_a_link_out_of_the_root_is_unlinked_and_its_target_survives`
  errors.
- On CPython 3.14.6 the same suite is green at 1002 tests, because the 3.12
  predicates exist.
- Under CPython 3.11.9 the credential-free publication rehearsal's
  `candidate-unit-suite` mechanic **fails on Windows**, naming exactly those two
  tests. Under CPython 3.14.6 the same mechanic passes.

**One fact is not yet measured and must be measured by this work order rather
than assumed:** the hosted `windows-2022` reading at the pinned 3.11. The hosted
runner may grant the symlink privilege, in which case `try_directory_symlink`
never falls back to a junction, `entry.is_symlink()` catches the link, and both
tests pass there — which would explain a lane that has been green. Linux has no
junctions and is unaffected either way. Whether the hosted lane is red or merely
latently unsafe changes nothing about the defect, but the report must state which
it is instead of guessing.

## In scope

- Replace both inert probes with detection that works on every supported
  runtime, keeping the 3.12 predicates as a fast path where they exist.
  Reparse-point state is available on Windows well below the floor through
  `os.stat_result.st_file_attributes` and `st_reparse_tag`, and the
  implementation agent decides the exact predicate.
- Keep the existing behaviour once a path is classified as a link: it is removed
  as a link, its target is never touched, and the parent rather than the
  candidate is canonicalized for the containment guard.
- Add deterministic tests that exercise the sub-3.12 path on any interpreter, so
  the regression cannot return silently on a newer runtime. Neutralizing the
  fast path in the test is the intended mechanism; a test that only passes on one
  interpreter version does not satisfy this.
- Add a deterministic test that a junctioned rehearsal root is refused, using the
  existing `try_directory_symlink` helper's fallback rather than a new one.
- Read the hosted `windows-2022` publication-rehearsal lane at the pinned 3.11
  and record whether it was red before this fix or green because the runner grants
  the symlink privilege.
- One entry in the domain index's publication-rehearsal packet section recording
  this work order, and no other change to that file.
- Retained implementation evidence under
  `docs/engineering/release-orchestration/evidence/`.

## Out of scope

- Any change to `SPEC-RLO-005`, `VER-RLO-005`, `REQ-RLO-015`, `REQ-RLO-016`,
  `ARCH-RLO-005`, or `ADR-RLO-005`. The specification already requires the
  correct behaviour in rules 19 and 21; the implementation does not meet it. If
  the implementation agent concludes a rule must change for the fix to be
  correct, that is a stop condition, not a licence to edit the rule.
- `publication_rehearsal_mechanics.json`, `.github/workflows/publication-rehearsal.yml`,
  the mechanic inventory, and the divergence seam.
- Raising `requires-python` or the pinned `PYTHON_VERSION`. Dropping 3.11 would
  hide this defect rather than fix it, and it is a separate decision with its own
  consumer consequences.
- Any file under `se_harness/` or `templates/`. This work order places no bytes in
  the distributed surface.
- Anything in `docs/engineering/release-0-7-0/`, including `REL-SEH-015`,
  `WO-RLS-011`, and its retained evidence.
- Every release act: candidate commit for 0.7.0, promotable build, `VREC-SEH-013`
  or `RLS-SEH-013` work, tag, publication, deployment, maintenance-line mutation,
  credential use, and root-evaluator change.

## Authorized decision envelope

The implementation agent decides locally: the exact reparse-point predicate and
whether junction and symlink cases share one helper; how the fast path is
neutralized in tests; test naming and placement within the existing
`TeardownTests`; and the wording of the domain-index entry and the retained
evidence.

The agent does not decide: whether any governing artifact changes; whether the
runtime floor moves; whether a test may be skipped on a platform to reach green;
or whether this work order's changes belong in the 0.7.0 release unit.

## Constraints

- A test that passes only because the interpreter is new does not demonstrate the
  fix. At least one test must fail against the current implementation on the
  runtime the agent is using.
- Do not widen the predicate so far that an ordinary Windows directory carrying a
  non-link reparse point is unlinked instead of walked. Prefer classifying by
  reparse tag over classifying by the reparse attribute alone, and state which
  was chosen and why.
- Do not weaken the containment guard, the root refusal, or the
  `RehearsalError` messages the existing tests match on.
- Treat every path, link target, and filesystem attribute as untrusted input.
- Confirm the repaired teardown still reports every removed path into `deleted`,
  since the rehearsal's own assertions and the reported derived-path count read
  that list.
- Run the suite on both a 3.11 and a newer interpreter, and label every figure
  with its runtime and platform. A green reading on one runtime is not a reading
  on the other.

## Expected change surface

- The two probe helpers in `.github/scripts/rehearse_publication.py`, and no
  other behaviour in that file.
- New tests in `tests/test_publication_rehearsal.py`, alongside the two existing
  teardown tests, which must go green unchanged. If either existing test needs
  editing to pass, stop and escalate: the fix is then changing what is asserted
  rather than what is asserted about.
- One entry in `docs/engineering/release-orchestration/README.md`.
- This work order and its retained evidence.

## Required verification

- The two currently failing teardown tests pass on CPython 3.11 on Windows,
  unedited.
- The new sub-3.12-path tests fail against the unrepaired implementation and pass
  against the repaired one, on whichever interpreter the agent runs.
- The full suite is green on Windows on both CPython 3.11 and a 3.12-or-newer
  interpreter, with counts and skip counts stated per runtime.
- The credential-free publication rehearsal completes on Windows under CPython
  3.11 with `candidate-unit-suite` executed rather than failed, and its
  `check-divergence` result stays exact.
- The hosted publication-rehearsal lane is read on both runner platforms at the
  pinned 3.11, through the runs API rather than from a summary badge, and the
  pre-fix hosted Windows state is recorded.
- A junctioned rehearsal root is refused, and a junction planted inside a derived
  tree is unlinked with its target intact.

## Evidence to record

Retain `docs/engineering/release-orchestration/evidence/WO-RLO-006-implementation.md`
with the artifact, checkpoint, and formal-snapshot binding block, recording:

- The predicate chosen, the reparse tags accepted, and why a narrower or wider
  classification was rejected.
- Every suite figure, labelled by interpreter version and platform, before and
  after.
- The publication-rehearsal readings on Windows under 3.11, before and after.
- The hosted lane reading on both platforms, with run and job identities, and an
  explicit statement of whether the hosted Windows lane was red before the fix.
- Any test that fails against the unrepaired implementation, named, as the
  demonstration that the new tests bite.
- Every action listed as out of scope that was not performed.

## Stop and escalate conditions

- A governing artifact appears to need amendment for the fix to be correct.
- An existing teardown test cannot pass without being edited.
- The hosted Windows lane is red for a reason other than these two tests.
- The reparse-point predicate cannot distinguish a link from an ordinary
  directory on any supported Windows configuration reachable here.
- The fix would require raising the runtime floor.
- Any change appears necessary outside the declared execution scope.

## Completion report format

State the predicate chosen; the before-and-after suite figures per interpreter
and platform; the publication-rehearsal outcome on Windows under 3.11; the hosted
lane reading on both platforms with the pre-fix Windows state stated plainly; the
new tests and the demonstration that each fails against the unrepaired
implementation; the retained evidence path; and every unperformed action.
