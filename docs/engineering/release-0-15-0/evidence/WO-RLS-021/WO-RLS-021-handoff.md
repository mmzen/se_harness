```toml
artifact = "WO-RLS-021"
checkpoint = "handoff"
formal_snapshot_sha256 = "26a9e5471e734b580524cb2c558dceb554e1cadd47a13ce7d08b235296b33440"
rebound_at = "2026-09-04T21:57:28Z"
```

# WO-RLS-021 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The one clean 0.15.0 candidate commit exists on `release/0.15.0` off `main`
at `7e05a88`, with the packaged bytes of `main`: this commit. The census
from `v0.14.0` is complete with the eleven notes-only exemptions the
contract names; no trace commit is needed. Qualification readings, the
census at the candidate, the hosted build of record and the hosted lanes
are recorded in the sections below as they complete.

## Evaluators

- Governing: released `se-harness 0.14.0` outside the checkout, `-I`,
  installed at `C:/Users/mathi/se-harness-eval-0140` from the wheel file
  whose SHA-256 `70d438b5…` equals the distribution table of
  `RLS-SEH-023`, on this Windows checkout for every reading, the packet and
  the handoff check included.
- Candidate: this checkout, branch `release/0.15.0` off `main` at
  `7e05a88`; `pyproject.toml` reads 0.15.0 (moved by `WO-HUP-015`).
- Build host: the hosted GitHub runner running the pinned linux/amd64
  producer image through Docker inside `release-qualification.yml`
  (`candidate` mode), dispatched on this branch at the bound candidate.

## Section 1: the candidate

This commit is the candidate: it retains this packet, and the branch
already carries the start. The approvals of `REL-SEH-026` and `WO-RLS-021`
rode PR #345 to `main` before the cut. Every commit on this branch carries
the `Harness-Work-Order: WO-RLS-021` trailer in its final block, so the
census at the candidate needs no exemption beyond the eleven notes-only
merges between `v0.14.0` and the cut, which the contract names and whose
paths were verified one by one to lie under `docs/notes/`.

## Section 2: readings at the candidate (this commit)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | released 0.14.0, outside the checkout, `-I`, wheel-installed | 1,308 artifacts, 0 errors, 69 pre-existing maintenance warnings, 0 advisories |
| `doctor` | released 0.14.0 | 113 PASS, 0 FAIL, 40 `W013` location warnings on historical records |
| `preflight --work-order WO-RLS-021 --phase review` | released 0.14.0 | PASS, no diagnostic |
| `check --checkpoint handoff --from-git 7e05a88` | released 0.14.0 | Completed; eight `QGP-G4I-*` predicates pass; every changed path inside the declared scope; `complete: true` |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS (11 distribution-bearing records) |
| `scripts/check_portable_release_surface.py --repository .` / `--wheel` / `--harnessctl` | candidate | PASS / PASS / PASS, the latter two on an explicitly non-promotable ephemeral wheel (`aee7761d…`) built outside the checkout from a Git export of the branch head, the way the candidate lane builds it |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.14), LF checkout | section 2b |
| `python scripts/run_tests.py` | candidate, Linux | the hosted candidate-source lane at this head, section 5 |
| `qualify complete-candidate` | candidate, Linux | the hosted candidate-package lane at this head, section 5 (`RID018` boundary on Windows) |
| `repository_tools.upgrade_rehearsal` 0.14.0 -> 0.15.0 | hosted, Linux and Windows | the governance-migration lanes at this head, section 5 |

### Section 2b: the Windows suite

`PYTHONUTF8=1 python scripts/run_tests.py --scale full` over this branch on
this Windows 11 workstation (CPython 3.14.6, LF checkout), whose `tests/`
and packaged bytes are identical at every branch commit including the
candidate: 1,249 tests, 26 skipped, 1 error, the known baseline name
present on `main` and outside this work order
(`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
a Windows `PermissionError` on a temporary Git object during teardown), the
same reading `WO-RLS-020` and every work order of this cycle recorded. No
other name differs.

## Section 3: census re-run at the candidate

`harnessctl release-unit . --from v0.14.0 --to <this commit> --contract REL-SEH-026`,
released 0.14.0, with the eleven exempted commits passed as `--exempt`:
untraced 0, exempted 11; fourteen work orders traced: the twelve content
members, the released `WO-RLS-020` through the #315 merge (excluded, as the
contract states by construction), and `WO-RLS-021` through this branch's
trailered commits. The comparison reports the `E-CIP-001` findings the
contract predicts at this stage: no `candidate_commit` is declared, the
gates differ by exactly the released `WO-RLS-020`, and `WO-RLS-021` is
`in_progress`, the state this reading is taken in.

## Section 4: build of record

The reading is the `workflow_dispatch` of `publication-rehearsal.yml` on
`release/0.15.0`, whose commit is the branch head (the pull-request event
builds the merge commit, not the head, as `WO-RLS-019` and `WO-RLS-020`
recorded).

### Reading at `10b03bf` (dispatch run 33922502052)

Two producer runs byte-identical, `state` `exact`, the pinned linux/amd64
image and the recipe `0c3f368c…` unchanged since `v0.12.0`. Wheel
`se_harness-0.15.0-py3-none-any.whl`
`adc51fb51927be03051da91cc35acfefca9433f0753d0135dd69e635cbdf9e56`; sdist
`se_harness-0.15.0.tar.gz`
`4113ee5fac72278e520669b6f07a9eaf54e90aefa611a511b226afa12a60ae97`;
`SOURCE_DATE_EPOCH` 1788558290; source manifest `b872c158…`. `10b03bf` is
the first commit that retained this packet; its packaged bytes are those of
every commit on this branch. These are the readings at that commit; the
record binds the digests of the bound candidate, read the same way at that
head (section 4b).

## Section 4b: build re-verified at the bound candidate

`VREC-SEH-024` and `RLS-SEH-024` bind `ba7ec54`, the implemented-transition
commit, so the replay was dispatched again on `release/0.15.0` at that exact
head (run 33923485490): two producer runs byte-identical, `state` `exact`,
the same pinned image and recipe `0c3f368c…`. Wheel
`eb09343f65a52ecc7511aacbe7f4cc546cfe4bf28eeed62cf3ff2bccf838d947`; sdist
`0ad6c0d085065aaa49128ac81690ba8426aca77870390e7fece88782420ede16`;
`SOURCE_DATE_EPOCH` 1788559098; source manifest `82d242b9…`. The section-4
digests were the reading at `10b03bf`, whose packaged bytes are identical;
the archives differ only through the commit-derived `SOURCE_DATE_EPOCH`.
The run's `release-build-replay.json` `manifest`, with `commit` equal to
the bound candidate, is retained byte-for-byte in canonical form as
`RLS-SEH-024-bundle.json` when the record is prepared and is what the
record's distribution table carries; the hosted
`release-candidate-replay.yml` dispatch on this branch must reproduce it
from the bound record.

## Section 5: hosted lanes

At `10b03bf`, the packet's first commit, the `validate` lane was `failure`:
the packet body had been written with CRLF line endings, the evidence
header parser reads LF bytes at offset 0, and the handoff step therefore
found no readable evidence. The concurrency group cancelled the other lanes
of that push. `dbb35a0` rewrote the packet in LF bytes and bound the header;
nothing else changed, and no packaged byte differs between the two commits.

At `dbb35a0`, push and pull-request events, seven runs, all `success`:
Engineering Harness (33922705106, 33922708446), SE Harness Candidate
Evidence (33922705239, 33922708510), Governor Transition Assessment
(33922705206, 33922708525), Publication Rehearsal (33922708620 on the
pull-request merge commit; the dispatch at `10b03bf` is section 4).

Retained by the candidate-evidence run 33922705239:

| Lane | Reading |
| --- | --- |
| candidate source, Linux | `run_tests.py --workers 4 --scale full` pass; portable surface `--repository` PASS; non-promotable candidate wheel `75cf83b1…` built from `dbb35a0` |
| `qualify complete-candidate`, Linux | `passed: true`; `CC001` to `CC004` pass |
| `qualify candidate-package` from the isolated released 0.14.0 verifier | `passed: true`; `CP001`, `CP002` pass |
| `repository_tools.upgrade_rehearsal` 0.14.0 -> 0.15.0, Linux, twice | `overall_result` pass both runs; `semantic_sha256` `8b99564f7dff9781…` both |
| the same, Windows, twice | `overall_result` pass both runs; the same `semantic_sha256` |
| integration package | built, verified on Linux and Windows, retained |

### Section 5b: at the bound candidate `ba7ec54` and the record commit `12fddcc`

At `ba7ec54`: Engineering Harness `validate` success (check-run
101186618619), Governor Transition Assessment success, Publication
Rehearsal dispatch 33923485490 success (section 4b). The push-event
Candidate Evidence and Publication Rehearsal runs at `ba7ec54` were
cancelled by the concurrency group when the record commit `12fddcc` was
pushed, as happened at 0.14.0's bound candidate; the packaged bytes of the
two commits are identical, so their readings are taken at `12fddcc`.

At `12fddcc`, push and pull-request events, seven runs, all `success`:
Engineering Harness (33923557410, 33923560035), SE Harness Candidate
Evidence (33923557431, 33923560073), Governor Transition Assessment
(33923557407, 33923560093), Publication Rehearsal (33923560306 on the
pull-request merge commit). Retained by the candidate-evidence run
33923557431: `qualify complete-candidate` `passed: true`, `CC001` to
`CC004`; `qualify candidate-package` `CP001`, `CP002` from the isolated
released 0.14.0 verifier; the upgrade rehearsal 0.14.0 -> 0.15.0 `pass`
twice on Linux and twice on Windows, one `semantic_sha256`
`68c8bb7194a034ba…`; the non-promotable candidate wheel `bfedb884…` built
from `12fddcc`; the integration package built, verified on both platforms
and retained.

## Section 6: the record

`VREC-SEH-024` was prepared at `ba7ec54` by the quality owner from the
released 0.14.0 evaluator over the thirteen gates of `REL-SEH-026`, the
eleven verification contracts and the thirteen work-order-keyed handoff
packets; it is `ready` in the commit that follows the candidate. The
validator's warning count moved from 69 to 70 with it: one `W013` location
warning, because the release domain keeps its records beside their release
as every release domain since 0.10.0 has, the same warning the 0.14.0
records carry. The verification decision is the assurance owner's.
