# WO-RLO-007 implementation evidence

artifact: WO-RLO-007
checkpoint: handoff
formal_snapshot_sha256: db5b5a184a504b105d37faac26aaacf9421cffe54386774a5b8eee3a0eaf9f20

Retained by the implementation actor on 2026-08-26. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, `python -m se_harness` from the repository root.
- Hosted: the publication rehearsal of the pull request that carries this
  change (the reusable qualification definition in `candidate` mode replays
  this commit's own recipe on `ubuntu-latest`).

## The defect, as observed before the change

Every hosted recipe replay in the repository's history fails after both
producer builds with `[Errno 1] Operation not permitted: <work root>/b/source/build`:

| Run | Workflow | Ref | Result |
| --- | --- | --- | --- |
| `32991888704` | `release-candidate-replay.yml` (dispatch, 2026-08-26) | `5e14e76` (0.7.0 contract branch) | `release build replay: FAIL: [Errno 1] Operation not permitted: /home/runner/work/_temp/.se-harness-release-build-…` |
| three runs of 2026-08-22 | `release-candidate-replay.yml` | — | failure |
| `32993878545` | `publication-rehearsal.yml`, job `Qualify and replay (candidate)` | `669f055` (PR #173, WO-CIP-002) | `release-build: [Errno 1] Operation not permitted: /home/runner/work/_temp/.se-harness-release-build-yboibwe8/b/source/build`; resolve, `qualify complete-candidate` and the unit suite had passed |

Cause: `_docker_build` bind-mounts the workspace into the producer container,
which runs as root and writes `source/build`, `final` and `producer.json` as
root; `tempfile.TemporaryDirectory`'s teardown runs as the runner user and
cannot remove them. `publish-pypi.yml`'s schema-2 replay had never run and
would fail identically.

## What was built

- `repository_tools/release_build.py`: `_hand_back_workspace(work_root,
  image)` runs the same pinned producer image once more —
  `docker run --rm --pull never --platform linux/amd64 --mount type=bind,source=<work root>,target=/workspace <image> chown -R <uid>:<gid> /workspace`
  — on POSIX hosts (`_is_posix()`), with the digest-resolved image from
  `_docker_image_identity`. `replay_build` calls it on both exit paths of the
  workspace: on the failure path its own failure is swallowed so the build
  error stays the reported result; on the success path its failure is raised
  as its own error (`replay built exactly but the workspace hand-back
  failed`). The workspace body moved unchanged into `_replay_in_workspace`;
  `TemporaryDirectory` is created with `ignore_cleanup_errors=True` so a
  leftover tree never masks either result. The recipe, the lock, the
  producer's arguments, the compared outputs and the result document are
  unchanged.
- Tests (`tests/test_release_build.py`): the hand-back command, its image,
  mount and `chown -R <uid>:<gid> /workspace` on POSIX; issued on the failure
  path without masking the build error; a hand-back failure after an exact
  build is its own error; skipped on a non-POSIX host. The existing
  determinism, hash and refusal tests are unchanged and pass.
- `docs/notes/developing-se-harness.md`, "Release sequences" (Build): one
  sentence on the hand-back. `README.md`: the `WO-RLO-007` row.

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-RLO-007 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 912 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (1 distribution-bearing record) |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `git diff --check` | git | clean |
| `harnessctl check . --artifact WO-RLO-007 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `db5b5a184a504b105d37faac26aaacf9421cffe54386774a5b8eee3a0eaf9f20` |
| `python -m unittest tests.test_release_build tests.test_interpreter_safety tests.test_release_orchestration` | candidate | OK, 10 skips (Windows-only guards) |
| `python -m unittest discover -s tests -p "test_*.py"` | candidate, Windows 11, CPython 3.14 | `Ran 911 tests in 332.131s` — `OK (skipped=23)`; the 23 skips are the Windows-only guards |
| Hosted, after the change | `publication-rehearsal.yml`, `Qualify and replay (candidate)` on the pull request | HOSTED_MARKER |

## Deviations, recorded for the completion decision

1. **The hand-back is a `chown` inside the pinned image, not a `--user` run.**
   Both were in the decision envelope; `chown -R` inside the `python`
   (Debian) image needs no extra tool and leaves the producer's own run
   untouched.
2. **Windows is not measured.** The hand-back is a no-op off POSIX by
   design; the workstation suite proves the branch is skipped. The hosted
   Linux run is the measurement that matters and is the reading recorded
   above.
3. **`release-candidate-replay.yml` is not re-run.** It needs a ready record;
   none exists. The rehearsal's `candidate` mode exercises the same
   `replay_build` on the same runner type.

## Complete changed-path set

```
docs/engineering/release-orchestration/README.md
docs/engineering/release-orchestration/evidence/WO-RLO-007/WO-RLO-007-verification.md
docs/engineering/release-orchestration/work-orders/WO-RLO-007.md
docs/notes/developing-se-harness.md
repository_tools/release_build.py
tests/test_release_build.py
```

## Not done

- The hosted reading after the change (needs the pull request); the
  completion transition; `VREC-RLO-007`.
