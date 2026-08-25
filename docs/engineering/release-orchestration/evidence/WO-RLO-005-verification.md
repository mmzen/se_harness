# WO-RLO-005 Verification Evidence

Date: 2026-08-25

Authority: non-authoritative retained candidate evidence. This file does not approve an
artifact, authorize a diff, verify work, merge, release, publish, or deploy. It records
what was measured, where, and what the measurements do not cover, so that an accountable
assurance decision can be taken over facts rather than over a summary.

Work order: `WO-RLO-005`, `status = "implemented"`, assurance classification
`commit_bound_verification = "required"` decided by the repository owner with the
rationale that "a green rehearsal becomes a pre-release assurance signal for both runner
platforms, and the divergence seam becomes a required check whose failure blocks
integration; both must be bound to the exact candidate that produced them".

Preparation of a `VREC` was authorized by the repository owner on 2026-08-25 through the
statement `you can set WO-RLO-005 and WO-HBI-004 as implemented, and prepare the
verification record(s)`. Both work orders were already `implemented` when that statement
was made, so no lifecycle transition was needed for either and none was invented.
Preparation is not verification: the record this file supports is prepared `ready` and
the assurance decision remains outstanding.

## Which commit the figures describe, and which commit the record binds

The local figures below were measured over the tree of `7918a1b`, the third merge with
`main`. Two later commits on this branch, `ec3fbf1` and `65a9af1`, add prose to
`docs/engineering/release-orchestration/evidence/WO-RLO-005-implementation.md` and nothing
else — `git diff --stat 7918a1b HEAD` reports that one file and 142 insertions — so no
executable content, no test, no workflow, no fixture and no recorded digest differs
between the measured tree and the branch tip.

This file is committed on top of those commits, because a file cannot contain the hash of
its own commit. The candidate commit the `VREC` binds is therefore the branch tip that
carries this file, and every field of that record is measured afresh at preparation.

## Environment

| Item | Value |
|---|---|
| Platform | `Windows-11-10.0.26200-SP0` |
| Python | 3.14.6 |
| Git | 2.45.1.windows.1 |
| Checkout | `C:\Users\mathi\se_harness-fix126-20260824-1518` |
| Branch | `feat/rlo-004-publication-rehearsal`, pull request #138 |
| `core.autocrlf` in the checkout | `true` |
| Third merge with `main` | `7918a1b`, parents `935a9d6` and `1d459cf` |
| Control worktree | `C:\Users\mathi\rlo005-control-m3`, `git worktree add --detach 1d459cf`, `core.autocrlf=true` |
| Governing evaluator | released `se-harness==0.6.0` in `C:\Users\mathi\se_harness_eval_060`, run from outside the checkout |
| Hosted runners | `ubuntu-latest` and `windows-2022`, CPython 3.11 |

The retained implementation evidence for this work order is
`docs/engineering/release-orchestration/evidence/WO-RLO-005-implementation.md`, blob
`3e6f063b1957271278ecf558ff445ff752140872` at the branch tip, 77941 bytes with zero CR
bytes, SHA-256 `6eb565b49d23fb3aefc6d2d2fc4806420e6198b97f1ccdd7a062e02e065d0e10`. It is
referenced by digest and deliberately not bound by the record, so that a later merge with
`main` can extend it without invalidating provenance. Everything an assurance decision
needs is restated here.

## What the candidate delivers

A repository-owned, credential-free rehearsal of the publication mechanics that runs on
both hosted runner types, plus a fail-closed divergence check between the rehearsal and
the publication orchestrator. `.github/workflows/publish-pypi.yml` is not modified by this
packet.

- `.github/scripts/rehearse_publication.py` and its data-only declaration
  `.github/scripts/publication_rehearsal_mechanics.json`: 22 mechanics, 9 declared
  orchestrator steps, required platforms `Linux` and `Windows`.
- `.github/workflows/publication-rehearsal.yml`: `contents: read` at workflow and job
  level, no environment, no secret, no token.
- `tests/test_publication_rehearsal.py`: 121 tests, plus four fixtures.
- Formal artifacts `CAP-RLO-003`, `REQ-RLO-015`, `REQ-RLO-016`, `SPEC-RLO-005`,
  `ARCH-RLO-005`, `ADR-RLO-005`, `VER-RLO-005`, `WO-RLO-005`, the acceptance feature, and
  the domain index.

## Local qualification at `7918a1b`

Measured in a `core.autocrlf=true` checkout, which is the construction the release
orchestrator uses for the candidate it qualifies.

| Measurement | Result |
|---|---|
| Full suite, branch | 932 tests, OK, 22 skipped — no failure, no error |
| Full suite, control at plain `1d459cf` | 811 tests, OK, 22 skipped |
| Delta | the packet adds 121 tests, all passing, and no failing test remains in either checkout |
| `tests/test_publication_rehearsal.py` | 121 tests, OK |
| `check-divergence --repository . --cross-check-yaml` | `EXACT`, exit 0, `Rehearsed jobs: qualify, resolve on Linux, Windows`, `Rehearsal lane platforms: Linux, Windows`, five excluded jobs each with its attribute, `No uncovered or stale mechanic.` |
| Governing validator, released `0.6.0` evaluator from outside the checkout | PASS, 830 artifacts, 0 errors, 50 warnings, all maintenance |
| Candidate validator | PASS, the same 830 / 0 / 50 |
| Governing preflight | `Harness preflight: PASS`, phase `review`, `WO-RLO-005` (`implemented`), no diagnostic |
| Governing `doctor` | exit 0, 87 checks, 0 `FAIL` |
| In-tree `doctor` | 81 `PASS`, 28 `FAIL`; `diff` against the control's `FAIL` list is empty |
| `validate_release_distributions.py --root .` | PASS, 1 distribution-bearing record |
| `git diff --check` | clean |

## Hosted execution on both runner types

Two hosted runs of the lane exist over this candidate's content, and both are recorded
because the second is the one that ran over the branch tip this record binds.

| Run | Head | Candidate commit | Divergence | Linux | Windows |
|---|---|---|---|---|---|
| [32775622117](https://github.com/mmzen/se_harness/actions/runs/32775622117), `pull_request`, 2026-08-24T20:44:44Z | `ec3fbf1` | `8a8fce53176a` | success, `EXACT` | success, `REHEARSED` | success, `REHEARSED` |
| [32776424455](https://github.com/mmzen/se_harness/actions/runs/32776424455), `pull_request`, 2026-08-24T20:53:15Z | `65a9af1` | GitHub's merge of `65a9af1` into `1d459cf` | success | success, `REHEARSED` | success, `REHEARSED` |

The first run's figures, read from the job logs:

| Leg | Result |
|---|---|
| Divergence | `EXACT`, `Rehearsed jobs: qualify, resolve on Linux, Windows`, `Rehearsal lane platforms: Linux, Windows`, `No uncovered or stale mechanic.` |
| Linux | `REHEARSED`, 21 mechanics executed, 2 excluded, `candidate unit suite passed (932 tests)`, `source_date_epoch = 1787604282`, both distribution sets byte-identical, teardown removed 7745 derived paths without following a link |
| Windows | `REHEARSED`, 21 mechanics executed, 2 excluded, `candidate unit suite passed (932 tests)`, the same `source_date_epoch = 1787604282`, both distribution sets byte-identical, teardown removed 7302 derived paths without following a link |

The second run's Windows leg reports `REHEARSED` with the same 21 executed and 2 excluded
mechanics, `candidate unit suite passed (932 tests)`, its own
`source_date_epoch = 1787604792`, and the same 7302 derived paths torn down. The epoch
differs between runs by construction — it is derived per run — and is identical across the
two platforms within a run, which is the property the determinism comparison depends on.

`REQ-RLO-015` is therefore proven by measurement on both halves. On `windows-2022` the
rehearsal executed temporary-path identity, release-record format validation, evaluator
resolution, evaluator acquisition with its hash proof through the `Scripts` layout,
identity proof through `harnessctl.exe`, distribution-policy validation, plan resolution,
the bounded resolution-refusal document, candidate export, pinned build-tool installation,
complete candidate graph qualification, a 932-test candidate suite, the CLI smoke check,
two independent builds, sdist normalization, the byte-for-byte determinism comparison,
bundle assembly, both manifest creations, both manifest verifications, and a real
teardown — with nothing injected and no credential.

## What the lane found, which is the case for keeping it

The lane's first hosted run measured the release orchestrator failing candidate
qualification on `windows-2022`, and the cause was outside this packet: the orchestrator
creates the checkout it qualifies with `git worktree add`, which inherits
`core.autocrlf=true`, so byte-exact assertions read converted bytes there. That finding was
routed into `WO-HBI-003` and then `WO-HBI-004` by owner decision rather than absorbed here.
Both merged, and this candidate's hosted Windows leg is green as a consequence. The lane
has now caught three distinct conditions that the required gates did not, at integration
time rather than on publication day, which is what `RC-060-11` asks of it.

Nothing in this packet was changed to accommodate those fixes. The packet's own 121 tests
were passing at every merge, and the figures that moved between merges are `main`'s.

## Provenance discipline across three merges with `main`

`main` was merged into this branch three times and never rebased, so no commit this branch
has published is rewritten and no record that binds one is orphaned by this packet's own
history.

| Merge | Commit | Conflict | Pinned orchestrator digest |
|---|---|---|---|
| First | `29c0db0` | one resolution in `docs/engineering/release-orchestration/README.md`, disclosed | re-derived, because `main` changed the orchestrator itself |
| Second | `6e16272` | none; one auto-merged path, `docs/notes/README.md` | re-verified, unchanged |
| Third | `7918a1b` | none, and no auto-merged path: the two changed-path sets from merge base `52e3702` are disjoint | re-verified, unchanged |

At the third merge the orchestrator is blob `902bb1978181b74918ad57370f77317e15c7bde3` at
`935a9d6`, at `1d459cf` and at `7918a1b`, and its bytes hash to
`2d3c3b775946d7667d9a175b0bb85446ff90db029d021e155a9b12105ff1f51e` over 38213 bytes,
which is the value pinned as `ORCHESTRATOR_LF_SHA256` in
`tests/test_publication_rehearsal.py`. The re-derivation at the first merge is disclosed
in the implementation evidence with the reason; the digest has never been re-derived to
accommodate a change made by this packet.

## Gate results at the candidate

Every gate `AGENTS.md` names was run, and the governing verdicts come from the released
`0.6.0` evaluator executed from outside the checkout.

| Gate | Result |
|---|---|
| `python -m unittest discover -s tests -p "test_*.py"` | 932 tests, OK, 22 skipped |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS, 830 artifacts, 0 errors, 50 warnings |
| `python scripts/validate_release_distributions.py --root .` | PASS, 1 distribution-bearing record |
| `python -m se_harness --help` | usage reported |
| Governing `doctor` | exit 0, 87 checks, 0 `FAIL` |
| Governing `preflight --phase review` | PASS, no diagnostic |
| Hosted required checks on pull request #138 | 21 pass, 3 skipping |

The three `skipping` entries are the integration-package jobs on the push-event run of
`SE Harness Candidate Evidence`; the same jobs pass on the `pull_request` run, which is
where that workflow gates them. No check on the pull request fails.

## Disclosures

These are the limits an assurance decision is taken over. None is a defect being hidden;
each is a boundary of what was measured.

1. **The rehearsal is derived evidence, not authority.** It takes no lifecycle
   transition, verifies nothing, and grants no permission. A green run is a signal that
   the credential-free mechanics work on both runner types, nothing more.
2. **Five orchestrator jobs are excluded by construction and are never rehearsed:**
   `github_release`, `observe`, `pages_build`, `pages_deploy` and `pypi`. Each carries a
   write permission, a protected environment, a token-named step or an external-state
   action, and the divergence check reports the attribute that excludes it. The
   credential-bearing publication path itself therefore remains unrehearsed, by design and
   not by omission.
3. **Two mechanics are excluded in every run on every platform.** The predecessor-view
   qualification has no committed record binding the resolved `0.6.0` evaluator as its
   predecessor, and the recipe-bound build replay has no released distribution-schema-2
   subject: `RLS-SEH-012` declares distribution schema 1. Neither has ever executed here,
   so neither is proven by this candidate.
4. **The divergence check covers one orchestrator.** `SPEC-RLO-005` names
   `.github/workflows/publish-pypi.yml`. `main`'s `.github/workflows/release-candidate-replay.yml`
   is not read, so a change to it is invisible to this seam. Widening the check would
   exceed the specification and was not done.
5. **The pinned orchestrator digest was re-derived once**, at the first merge with `main`,
   for an incoming change to the orchestrator, and the meaning of the assertion narrowed
   then to byte-unchanged *by this packet*. That is disclosed where it happened.
6. **No Linux measurement is local.** Every Linux figure comes from a hosted
   `ubuntu-latest` runner. Conversely the local figures come from one Windows 11
   workstation with CPython 3.14.6, while the hosted legs run CPython 3.11.
7. **Test counts and skip counts are not comparable across environments.** This
   workstation reports 932 tests with 22 skips; the hosted legs report the same 932 with 10
   skips. The skip difference is a platform-guard property and is not a pass condition
   anywhere in this packet.
8. **The in-tree `doctor` reports 28 `FAIL`.** The control at plain `main` reports the
   same 28 with identical names, so the skew is inherited candidate-versus-released
   boundary state — nine `distribution:` and nineteen `lock-entry:` — and none of it is
   caused or repaired by this packet. The governing `doctor`, which is the run that
   carries a verdict, has none.
9. **The evidence records a hosted run one head behind the candidate.** A commit that
   records a run necessarily follows it, so the implementation evidence's detailed figures
   come from run 32775622117 at head `ec3fbf1`. The branch tip's own run, 32776424455, is
   green with the same mechanic counts and the same suite result, and both are tabled
   above rather than one being presented as the other.
10. **The rehearsal does not prove a publication succeeds.** It proves the credential-free
    mechanics execute and that the rehearsal has not drifted from the orchestrator. Any
    release decision needs its own authorization, and `WO-RLO-005` transitions only to
    `implemented`.
11. **`build_recipe_sha256` remains in `unbound_digest_fields`**, tracked as repository
    issue 142 and untouched here.
12. **This record binds a branch commit.** Merging pull request #138 leaves the bound
    commit reachable only if the merge is a true merge; a squash or a rebase of this branch
    would orphan it, and a verified record cannot be re-pointed at a later commit.

## Actions not performed

No `VREC` field was written by hand: the record is produced by the released `0.6.0`
evaluator's `capture-verification` at the candidate commit with a clean worktree, and it is
prepared `ready`, not verified.

No merge of pull request #138, no tag, no branch other than this feature branch, no GitHub
Release, no PyPI publication, no Pages deployment, no protected-environment approval, no
workflow dispatch of the release orchestrator, no release record, no release-record
preparation or transition, no promotable distribution build, no assurance decision, no
governor adoption, no credential acquisition, and no hosting or branch-protection change.

No recorded digest, `VREC`, `RLS`, `REL` or evidence fact was rewritten or repointed, no
managed file was edited, and no committed file's bytes were converted.
