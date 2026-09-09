```toml
artifact = "WO-RLS-023"
checkpoint = "handoff"
formal_snapshot_sha256 = "a183e98c2ec2b1c25ae13a2a8964c5e822b14301ef1f2744eeaf5ebf76c7b91d"
rebound_at = "2026-09-09T07:40:47Z"
```

# WO-RLS-023 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The one clean 0.17.0 candidate commit is the commit that transitions this
work order to `implemented` on `release/0.17.0` off `main` at `2bd2ae7c`, with
the packaged bytes of `main`. The census from `v0.16.0` is complete with the
seven exemptions the contract names: the five definition packets, the
execution merge of `WO-TST-004`, whose trace this branch repairs with the
empty commit `10e4face`, and, by the release owner's dated amendment of
2026-09-09, the merge of the contract's own packet `2bd2ae7c`. The released
`WO-RLS-022` is outside the unit by construction; no other trace commit is
needed. Qualification readings, the census at the candidate, the hosted
build of record and the hosted lanes are recorded in the sections below as
they complete.

## Evaluators

- Governing: released `se-harness 0.16.0` outside the checkout, `-I`,
  installed at `C:/Users/hok/se-harness-eval-0160` from the wheel file
  whose SHA-256 `a969d6ab…` equals the distribution table of
  `RLS-SEH-025`, on this Windows checkout (LF bytes, `core.autocrlf=input`)
  for every reading, the packet and the handoff check included.
- Candidate: this checkout, branch `release/0.17.0` off `main` at
  `2bd2ae7c`, the merge of the approved packet #424; `pyproject.toml` reads
  0.17.0 (moved by `WO-HUP-017`).
- Build host: the hosted GitHub runner running the pinned linux/amd64
  producer image through Docker inside `release-qualification.yml`
  (`candidate` mode), dispatched on this branch.

## Section 1: the candidate and the traces

The approvals of `REL-SEH-028` and `WO-RLS-023` rode PR #424 to `main`
before the cut. The branch's first commit starts this work order; its second,
`10e4face`, is empty and carries `Harness-Work-Order: WO-TST-004`, the trace
repair the contract names for the execution merge #402; its third amends the
contract's exemption list. Every other commit carries
`Harness-Work-Order: WO-RLS-023` in one trailer block.

One defect was found and repaired on the way. Git reads trailers from a
message's last paragraph only; the two packet commits of #424, and the first
two commits of this branch as first written, ended with the
`Harness-Work-Order` line, a blank line and a `Co-Authored-By` line, so
`release-unit` read no trailer on them. The two branch commits were amended
before any reading was retained; the packet merge `2bd2ae7c` cannot be
amended and is exempted by the release owner's decision, recorded on the
contract under "Amendment record". The seven exempted paths were verified
one by one: #391, #401, #409, #410 and #411 touch one domain's definitions
each, #402 touches `tests/` and the test-suite domain, #424 touches this
domain and one line of `docs/engineering/README.md`.

## Section 2: readings at `5c78221d`, the amendment commit

The packaged bytes and `tests/` are identical at every commit of this
branch, including the candidate; the readings below were taken at the
amendment commit (or at `10e4face` where stated, whose formal graph differs
only by the amendment record) and hold at the candidate.

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | released 0.16.0, outside the checkout, `-I`, wheel-installed | 1,435 artifacts, 0 errors, 44 pre-existing maintenance warnings, 0 advisories |
| `doctor` | released 0.16.0 | 97 PASS, 0 FAIL, 44 `W013` location warnings on historical records |
| `preflight --work-order WO-RLS-023 --phase start` at `2bd2ae7c`, before the start transition | released 0.16.0 | PASS, no diagnostic |
| `preflight --work-order WO-RLS-023 --phase review` | released 0.16.0 | PASS, no diagnostic |
| `check --checkpoint handoff --from-git main` | released 0.16.0 | section 2c |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS (13 distribution-bearing records) |
| `scripts/check_portable_release_surface.py --repository .` / `--wheel` / `--harnessctl` | candidate | PASS / PASS / PASS, the latter two on an explicitly non-promotable ephemeral wheel (`b1a8a1a4…`) built outside the checkout with `pip wheel --no-deps` from a Git export of this branch at `10e4face` and installed into a disposable environment for the `--harnessctl` reading; the wheel carries the fifteen `se_harness/engine/` modules and no `scripts/` data file (its two `scripts/` entries are the standard template's skill scripts under `share/se-harness/`) |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13.3), LF checkout | section 2b |
| `python scripts/run_tests.py` | candidate, Linux | the hosted candidate-source lane at this head, section 5 |
| `qualify complete-candidate` | candidate, Linux | the hosted candidate-source lane, section 5 (`RID018` boundary on Windows) |
| `repository_tools.upgrade_rehearsal` 0.16.0 -> 0.17.0 | hosted, Linux and Windows | the `upgrade-rehearsal` jobs at this head, section 5 |

### Section 2b: the Windows suite

`PYTHONUTF8=1 python scripts/run_tests.py --scale full` over this branch at
`10e4face`, on this Windows 11 workstation (CPython 3.13.3, LF checkout),
whose `tests/` and packaged bytes are identical at every branch commit
including the candidate: 1,098 tests, 23 skipped, 1 error, the known
baseline name present on `main` and outside this work order
(`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
a Windows `PermissionError` on a read-only temporary Git object during
teardown), the same reading every work order of this cycle recorded. The
twenty-third skip is the complexity test of `tests/test_module_seams.py`,
which runs only where radon is installed. No other name differs.

### Section 2c: the handoff check

`check --artifact WO-RLS-023 --checkpoint handoff --from-git main`,
released 0.16.0, over this packet: Completed; every `QGP-G4I-*` predicate
passes, the evidence predicate reading this packet's header at its formal
snapshot; every changed path inside the declared scope; `complete: true`.
The schema-2 result is retained beside this packet as `handoff.json`.

## Section 3: census re-run at `5c78221d`

`harnessctl release-unit . --from v0.16.0 --to 5c78221d --contract REL-SEH-028`,
released 0.16.0, with the seven exempted commits passed as `--exempt`:
untraced 0, exempted 7; nineteen work orders traced: the seventeen content
members (`WO-TST-004` through the trace commit `10e4face`), the released
`WO-RLS-022` through the #369 merge (excluded, as the contract states by
construction), and `WO-RLS-023` through this branch's trailered commits. The
comparison reports the `E-CIP-001` findings the contract predicts at this
stage: no `candidate_commit` is declared, the gates differ by exactly
`WO-RLS-022`, and the derivation is incomplete because `WO-RLS-023` is
`in_progress`, the state this reading is taken in. Before the amendment, at
`10e4face`, the same command with six exemptions read one untraced commit,
`2bd2ae7c`, the finding section 1 explains.

## Section 4: build of record

The reading is the `workflow_dispatch` of `publication-rehearsal.yml` on
`release/0.17.0`, whose commit is the branch head (the pull-request event
builds the merge commit, not the head, as every release work order since
`WO-RLS-019` recorded). Since `WO-CIP-007` the candidate leg replays the
recipe and nothing else; its qualification is the candidate-evidence lane's
(section 5).

### Reading at `10e4face` (dispatch run 34321911662)

Two producer runs byte-identical, `state` `exact`, the pinned linux/amd64
image `python@sha256:2856e6af…` and the recipe `0c3f368c…` unchanged since
`v0.12.0`, toolchain `build 1.3.0`, `setuptools 84.0.0`, `wheel 0.48.0`,
`pip 24.0` on CPython 3.11.9. Wheel `se_harness-0.17.0-py3-none-any.whl`
`52448ff65d53d7ad44de2ffc192ce001844aaea70b327920298eceb7b7eaa6d5`; sdist
`se_harness-0.17.0.tar.gz`
`8d680c46ef218eaa6a0fc2f9255c2f5786a8fdb78973bceb8a7c4fafc0f0a7ba`;
`SOURCE_DATE_EPOCH` 1788937364; source manifest `ebd07d2f…`; checksums
`ea9c41b1…`. These are the readings at the trace commit, whose packaged
bytes are those of every commit on this branch; the record binds the digests
of the bound candidate, read the same way at that head (section 4b).

## Section 5: hosted lanes

At `10e4face`, pull-request event, all `success`: SE Harness Candidate
Evidence 34321903659 (with the integration-package jobs), Predecessor
Evaluator Assessment 34321903709, Publication Rehearsal 34321903926; the
push-event Candidate Evidence 34321899511 also `success`. Engineering
Harness 34321903651 `failure` on the pull-request event by design: its scope
step runs the handoff check, whose evidence predicate reads this packet,
which did not yet exist; the lane turns green at the packet commit, as on
every release branch before this one.

Retained by the candidate-evidence run 34321903659:

| Lane | Reading |
| --- | --- |
| candidate source, Linux | `run_tests.py` pass; portable surface `--repository` PASS; non-promotable candidate wheel built from `10e4face` |
| `qualify complete-candidate`, Linux | `passed: true`; `CC001` to `CC004` pass (`CC003`: artifacts 1,435, errors 0, warnings 44) |
| `qualify candidate-package` from the isolated released 0.16.0 verifier | `passed: true`; `CP001`, `CP002` pass (10 released-verifier scenarios) |
| `repository_tools.upgrade_rehearsal` 0.16.0 -> 0.17.0, Linux, twice | `overall_result` pass both runs; `semantic_sha256` `f50c7b4847ac0323…` both |
| the same, Windows, twice | `overall_result` pass both runs; the same `semantic_sha256` |
| deterministic integration package | built, verified on Linux and Windows, retained (`f309ee6d…`) |

## Section 4b: build re-verified at the bound candidate

`VREC-SEH-026` and `RLS-SEH-026` bind `a9f4905d`, the implemented-transition
commit, so the replay was dispatched again on `release/0.17.0` at that exact
head (run 34326469527): two producer runs byte-identical, `state` `exact`,
the same pinned image `python@sha256:2856e6af…` and recipe `0c3f368c…`,
`candidate.commit` equal to `a9f4905d`. Wheel
`305c7cbc79f87baa76ea3bea939b134999f9cad3bfdfa0b4c9c2fd2d9caacced`; sdist
`dda4bc73190674f8837ab0669b6aeb205c72b9428cad052b6368ea229860c318`;
`SOURCE_DATE_EPOCH` 1788940609; source manifest `bd231484…`; checksums
`5148c154…`. The digests differ from section 4's because the epoch and the
exported tree (this packet, the transition) differ; the packaged Python
bytes are the same, as the identical `semantic_sha256` of the upgrade
rehearsal at both heads shows. The retained manifest is
`docs/engineering/release-0-17-0/evidence/RLS-SEH-026-bundle.json`, bound
into the record when it is prepared.

## Section 5b: hosted lanes at the candidate and the record

At `a9f4905d` the push-event Engineering Harness, Predecessor Evaluator
Assessment and SE Harness Candidate Evidence runs are `success`, and the
Publication Rehearsal dispatch of section 4b is `success`; the pull-request
event's runs at that head were cancelled by the push of the record commit
`3041c5b9` minutes later (concurrency by ref) and re-ran at `3041c5b9`, where
every pull-request lane is `success` and the Publication Rehearsal run
34326563944 is `success`. `VREC-SEH-026` was captured on the clean tree at
`a9f4905d` by the released 0.16.0 evaluator: eighteen work orders, twelve
verification contracts, eighteen evidence paths, `status` `ready`; the one
new warning of `validate` is the `W013` location note every release
domain's record carries.

## Section 6: the records and the replay from the bound record

`VREC-SEH-026` was verified by the assurance owner on 2026-09-09 at
`8cb6cb81`. `RLS-SEH-026` was prepared by the released 0.16.0 evaluator's
generic `prepare-release` on the clean tree at `a9f4905d` over the eighteen
work orders `VREC-SEH-026` verifies (the command requires every one; a first
call naming this work order alone was refused with `WEX404`, and a second
was refused with `WEX402` because the retained bundle manifest sat untracked
in the tree, so it was moved aside for the preparation and restored for the
binding), then bound by `scripts/bind_release_distribution.py` to the
manifest of section 4b, retained as `RLS-SEH-026-bundle.json`; the record
carries `commit` `a9f4905d`, `tag` `v0.17.0`, the wheel `305c7cbc…`, the
sdist `dda4bc73…`, `SOURCE_DATE_EPOCH` 1788940609, and `status` `ready` at
`11baacd3`. `scripts/validate_release_distributions.py` reads PASS over 14
distribution-bearing records; `validate` reads 1,437 artifacts, 0 errors,
46 warnings (the two new ones the `W013` location notes of the two records),
0 advisories.

`release-candidate-replay.yml` dispatched on `release/0.17.0` at `11baacd3`
with `release_record=RLS-SEH-026` (run 34328103886): two producer runs
byte-identical, `state` `exact`, `expected` equal to the bound digests,
`candidate.commit` `a9f4905d`, recipe `0c3f368c…`; the rebuilt wheel and
sdist equal the record byte for byte. Two earlier dispatches of the same
workflow (runs 34327827784 and 34327928584) failed by construction: they
were requested before the record existed, one by a command chain that did
not stop at a refused step; neither read or wrote anything of record.

Every pull-request lane at `11baacd3` is `success` (23 checks, the three
push-event integration rows skipping by the lane's own condition).

## Disclosures

1. The `Harness-Work-Order` trailer of every commit written in this
   repository since 2026-09-07 with a blank line before its `Co-Authored-By`
   line is unreadable to Git and to `release-unit`; the packet merge
   `2bd2ae7c` is exempted by the contract's dated amendment for that reason,
   and the release branch's commits are written in one trailer block. The
   earlier work orders were traced through other commits and their
   membership is unaffected.
2. The build-of-record digests at the trace commit (section 4) and at the
   candidate (section 4b) differ by the epoch and the exported tree; the
   record binds the candidate's, and the replay from the bound record
   reproduces them.
3. The candidate's readings of section 2 were taken at `5c78221d` and
   `10e4face`; the packaged bytes and `tests/` are identical at every commit
   of this branch, `git diff 2bd2ae7c..HEAD -- se_harness tests pyproject.toml
   templates` being empty.

