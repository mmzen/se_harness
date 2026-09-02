```toml
artifact = "WO-RLS-019"
checkpoint = "handoff"
formal_snapshot_sha256 = "e4eddb3abdab93d202986908f4ab5f08667a99b799cb00139cd9dccf02c411fa"
rebound_at = "2026-09-02T06:46:22Z"
```

# WO-RLS-019 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The one clean 0.13.0 candidate commit exists on `release/0.13.0` off `main`
at `75d1902`, with the packaged bytes of `main`: this commit. No trace
commit is needed; the census from `v0.12.0` is clean. Qualification
readings, the census at the candidate, the hosted build of record and the
hosted lanes are recorded in the sections below as they complete.

## Evaluators

- Governing: released `se-harness 0.12.0` outside the checkout, `-I`,
  installed at `C:/Users/hok/se-harness-eval-0120` from the wheel file
  whose SHA-256 `639edbee…` equals the distribution table of
  `RLS-SEH-021`, on this Windows checkout for every reading, the packet and
  the handoff check included.
- Candidate: this checkout, branch `release/0.13.0` off `main` at
  `75d1902`; `pyproject.toml` reads 0.13.0 (moved by `WO-HUP-013`).
- Build host: the hosted GitHub runner running the pinned linux/amd64
  producer image through Docker inside `release-qualification.yml`
  (`candidate` mode), because this workstation has no Docker engine.

## Section 1: the candidate

This commit is the candidate: it retains this packet and the release-note
line, and the branch already carries the packet drafting, the approvals
and the start. Every commit on this branch carries the
`Harness-Work-Order: WO-RLS-019` trailer in its final block, so the census
at the candidate needs no exemption.

## Section 2: readings at the candidate `aa14628`

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate` | released 0.12.0, outside the checkout, `-I`, wheel-installed | 1,233 artifacts, 0 errors, 65 pre-existing maintenance warnings, 0 advisories |
| `doctor` | released 0.12.0 | 113 PASS, 0 FAIL |
| `preflight --work-order WO-RLS-019 --phase review` | released 0.12.0 | PASS, no diagnostic |
| `check --checkpoint handoff --from-git 75d1902` | released 0.12.0 | Completed; eight `QGP-G4I-*` predicates pass; seven changed paths, all inside the declared scope; `complete: true`; section 6 |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS (9 distribution-bearing records) |
| `scripts/check_portable_release_surface.py --repository .` / `--wheel` / `--harnessctl` | candidate | PASS / PASS / PASS, the latter two on an explicitly non-promotable ephemeral wheel (`6a4b5b9b…`) built outside the checkout from a Git export of `aa14628` and installed into a disposable environment |
| `python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13), LF checkout | section 2b |
| `python scripts/run_tests.py` | candidate, Linux | the hosted candidate-source lane at this branch head, section 5 |
| `qualify complete-candidate` | candidate, Linux | the hosted candidate-package lane at this branch head, section 5 (`RID018` boundary on Windows, as `REL-SEH-023` records) |
| `repository_tools.upgrade_rehearsal` 0.12.0 -> 0.13.0 | hosted, Linux and Windows | the governance-migration lanes at this branch head, section 5 |

### Section 2b: the Windows suite

`python scripts/run_tests.py --scale full` at `aa14628` on this Windows 11
workstation (CPython 3.13, LF checkout): 1,176 tests, 26 skipped, 1 error,
the known baseline name present on `main` and outside this work order
(`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
a Windows `PermissionError` on a temporary Git object during teardown), the
same reading `WO-RLS-018` and `WO-HUP-013` recorded. The same run over the
committed packet before the candidate read the same numbers.

## Section 3: census re-run at the candidate

`harnessctl release-unit . --from v0.12.0 --to aa14628 --contract REL-SEH-024`,
released 0.12.0, no `--exempt`: untraced 0, exempted 0; ten work orders
traced: the three members, the six `RLS-SEH-021` members through the #304
merge (released and excluded, as the contract states by construction), and
`WO-RLS-019` through this branch's trailered commits. The comparison reports
the three `E-CIP-001` findings the contract predicts at this stage: no
`candidate_commit` is declared, the gates differ by exactly the six released
members, and `WO-RLS-019` is `in_progress`, the state this reading is taken
in.

## Section 4: build of record

The pull-request event of the Publication Rehearsal builds the pull
request's merge commit (`github.sha` of a `pull_request` event is the merge
ref, `1eae65f` for #313 at `aa14628`), so it is not a reading of the
candidate. The reading is the `workflow_dispatch` of
`publication-rehearsal.yml` on `release/0.13.0`, whose commit is the branch
head; its `candidate` job replays the head's own recipe twice on the pinned
linux/amd64 producer image and retains `release-build-replay.json` under
`qualification-candidate-<head>`.

### Reading at `aa14628` (dispatch run 33601305042)

Two producer runs byte-identical, `state` `exact`, image
`python@sha256:2856e6af…` linux/amd64, recipe `0c3f368c…` unchanged since
`v0.12.0`. Wheel `se_harness-0.13.0-py3-none-any.whl`
`cc1eb84ce5a576ede74991e089068ba4cba38de5558dc2e7fe4cdee031bb6005`; sdist
`se_harness-0.13.0.tar.gz`
`bc6ae245a0a2bdb85c899ed0bdead4c923f5454f4cd393fe42c91cabed94b630`;
`SOURCE_DATE_EPOCH` 1788331713; source manifest `10f48689…`. These are the
readings at this commit; the record binds the digests of the bound
candidate, read the same way at that head (section 4b).

## Section 4b: build re-verified at the bound candidate

`RLS-SEH-022` binds `79d6f6f`, the implemented-transition commit, so the
replay was dispatched again on `release/0.13.0` at that exact head (run
33602457588): two producer runs byte-identical, `state` `exact`, the same
pinned image and recipe. Wheel
`1bbf3b747b7ebbb07fd3fd975e87e3c11049e7a6a8e1377e3d35099f4fe862ae`; sdist
`d1f6b60ae149be5aad5509b88b768f6cfe22d9af8460f1fdc9d04bcf6670bdd4`;
`SOURCE_DATE_EPOCH` 1788333166; source manifest `66d329f7…`. The section-4
digests were the reading at `aa14628`, whose packaged bytes are identical;
the archives differ only through the commit-derived `SOURCE_DATE_EPOCH`.
The run's `release-build-replay.json` `manifest`, with `commit` equal to
the bound candidate, is retained byte-for-byte in canonical form as
`RLS-SEH-022-bundle.json` and is what the record's distribution table
carries; the hosted `release-candidate-replay.yml` dispatch on this branch
must reproduce it from the bound record.

## Section 5: hosted lanes

At `aa14628`, push and pull-request events, seven runs, all `success`:
Engineering Harness (33600676741, 33600679685: the live-body work-order
selection, review preflight and the Git-derived handoff check pass over
this packet), SE Harness Candidate Evidence (33600676768, 33600679686),
Governor Transition Assessment (33600676813, 33600679714), Publication
Rehearsal (33600679811, the pull-request merge commit; section 4).

Retained by the candidate-evidence run 33600676768:

| Lane | Reading |
| --- | --- |
| candidate source, Linux | `run_tests.py --workers 4 --scale full` pass; portable surface `--repository` PASS; non-promotable candidate wheel `fb5d2bc5…` built from `aa14628` |
| `qualify complete-candidate`, Linux | `passed: true`; `CC001` to `CC004` pass |
| `qualify candidate-package` from the isolated released 0.12.0 verifier | `CP001`, `CP002` pass |
| `repository_tools.upgrade_rehearsal` 0.12.0 -> 0.13.0, Linux, twice | `overall_result` pass both runs; `semantic_sha256` `ea98ff022481cd6223fa80366a7278349d8838b5bc34707a54209ea804437ccf` both |
| the same, Windows, twice | `overall_result` pass both runs; the same `semantic_sha256` `ea98ff02…` |
| integration package | built, verified on Linux and Windows, retained |

### Section 5b: at the bound candidate `79d6f6f`

Every lane success: Engineering Harness (push 33602455970, pull request
33602459601), Governor Transition Assessment (push 33602455974, pull
request 33602459575), Publication Rehearsal (pull request 33602459873 on
the merge commit; dispatch 33602457588 on the head, section 4b), SE Harness
Candidate Evidence (push 33602456034, `success` on its re-run after the
first attempt and the pull-request run 33602459614 were cancelled by the
workflow's `cancel-in-progress` concurrency when the next governance
commit was pushed; the re-run skips only the integration-package jobs,
which are not a release input). Retained by that run: `qualify
complete-candidate` `passed: true`, `CC001` to `CC004`; `qualify
candidate-package` `CP001`, `CP002` from the isolated released 0.12.0
verifier; the upgrade rehearsal 0.12.0 -> 0.13.0 `pass` twice on Linux and
twice on Windows, one `semantic_sha256`
`b4d28069ee9337929b94f23e82063d4ff65fd5af15ddbefefc51846abc013199`; the
non-promotable candidate wheel `40db49d0…` built from `79d6f6f`.
