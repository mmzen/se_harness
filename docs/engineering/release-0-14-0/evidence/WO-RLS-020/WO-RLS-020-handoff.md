```toml
artifact = "WO-RLS-020"
checkpoint = "handoff"
formal_snapshot_sha256 = "24100c9f2ba91fb982236cf0f0ba0e7444e0b53da16046544b0a4295dd7607d0"
rebound_at = "2026-09-02T09:17:58Z"
```

# WO-RLS-020 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The one clean 0.14.0 candidate commit exists on `release/0.14.0` off `main`
at `d005b98`, with the packaged bytes of `main`: this commit. The census
from `v0.13.0` is clean; no trace commit is needed. Qualification
readings, the census at the candidate, the hosted build of record and the
hosted lanes are recorded in the sections below as they complete.

## Evaluators

- Governing: released `se-harness 0.13.0` outside the checkout, `-I`,
  installed at `C:/Users/hok/se-harness-eval-0130` from the wheel file
  whose SHA-256 `1bbf3b74…` equals the distribution table of
  `RLS-SEH-022`, on this Windows checkout for every reading, the packet and
  the handoff check included.
- Candidate: this checkout, branch `release/0.14.0` off `main` at
  `d005b98`; `pyproject.toml` reads 0.14.0 (moved by `WO-HUP-014`).
- Build host: the hosted GitHub runner running the pinned linux/amd64
  producer image through Docker inside `release-qualification.yml`
  (`candidate` mode), dispatched on this branch at the bound candidate.

## Section 1: the candidate

This commit is the candidate: it retains this packet, and the branch
already carries the packet drafting, the approvals and the start. Every
commit on this branch carries the `Harness-Work-Order: WO-RLS-020` trailer
in its final block, so the census at the candidate needs no exemption.

## Section 2: readings at the candidate `5588235`

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | released 0.13.0, outside the checkout, `-I`, wheel-installed | 1,244 artifacts, 0 errors, 67 pre-existing maintenance warnings, 0 advisories |
| `doctor` | released 0.13.0 | 113 PASS, 0 FAIL |
| `preflight --work-order WO-RLS-020 --phase review` | released 0.13.0 | PASS, no diagnostic |
| `check --checkpoint handoff --from-git d005b98` | released 0.13.0 | Completed; eight `QGP-G4I-*` predicates pass; every changed path inside the declared scope; `complete: true` |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS (10 distribution-bearing records) |
| `scripts/check_portable_release_surface.py --repository .` / `--wheel` / `--harnessctl` | candidate | PASS / PASS / PASS, the latter two on an explicitly non-promotable ephemeral wheel (`63b23e49…`) built outside the checkout from a Git export of `5588235` and installed into a disposable environment |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13), LF checkout | section 2b |
| `python scripts/run_tests.py` | candidate, Linux | the hosted candidate-source lane at this head, section 5 |
| `qualify complete-candidate` | candidate, Linux | the hosted candidate-package lane at this head, section 5 (`RID018` boundary on Windows) |
| `repository_tools.upgrade_rehearsal` 0.13.0 -> 0.14.0 | hosted, Linux and Windows | the governance-migration lanes at this head, section 5 |

### Section 2b: the Windows suite

`PYTHONUTF8=1 python scripts/run_tests.py --scale full` over this branch on
this Windows 11 workstation (CPython 3.13, LF checkout), whose `tests/` and
packaged bytes are identical at every branch commit including `5588235`:
1,176 tests, 26 skipped, 1 error, the known baseline name present on
`main` and outside this work order
(`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
a Windows `PermissionError` on a temporary Git object during teardown), the
same reading `WO-RLS-019` and `WO-HUP-014` recorded. No other name differs.

## Section 3: census re-run at the candidate

`harnessctl release-unit . --from v0.13.0 --to 5588235 --contract REL-SEH-025`,
released 0.13.0, no `--exempt`: untraced 0, exempted 0; three work orders
traced: the member `WO-HUP-014`, the released `WO-RLS-019` through the
#313 merge (excluded, as the contract states by construction), and
`WO-RLS-020` through this branch's trailered commits. The comparison
reports the three `E-CIP-001` findings the contract predicts at this
stage: no `candidate_commit` is declared, the gates differ by exactly the
released `WO-RLS-019`, and `WO-RLS-020` is `in_progress`, the state this
reading is taken in.

## Section 4: build of record

The reading is the `workflow_dispatch` of `publication-rehearsal.yml` on
`release/0.14.0`, whose commit is the branch head (the pull-request event
builds the merge commit, not the head, as `WO-RLS-019` recorded).

### Reading at `5588235` (dispatch run 33613490609)

Two producer runs byte-identical, `state` `exact`, the pinned linux/amd64
image and the recipe `0c3f368c…` unchanged since `v0.12.0`. Wheel
`se_harness-0.14.0-py3-none-any.whl`
`d02db62bbb7839274353709d5dd7fd7974ccefcdaa49c42fc059e7ae25814960`; sdist
`se_harness-0.14.0.tar.gz`
`d5e18b071119fed662f603a1fd7a854e1643932d2f05fada6f4a1a0e546c2ff3`;
`SOURCE_DATE_EPOCH` 1788340681; source manifest `22807d8d…`. These are
the readings at this commit; the record binds the digests of the bound
candidate, read the same way at that head (section 4b).

## Section 5: hosted lanes

At `5588235`, push and pull-request events plus the dispatch, eight runs,
all `success`: Engineering Harness (33613351888, 33613358349), SE Harness
Candidate Evidence (33613351863, 33613358400), Governor Transition
Assessment (33613351841, 33613358464), Publication Rehearsal (33613358745
on the pull-request merge commit; 33613490609 the dispatch, section 4).

Retained by the candidate-evidence run 33613351863:

| Lane | Reading |
| --- | --- |
| candidate source, Linux | `run_tests.py --workers 4 --scale full` pass; portable surface `--repository` PASS; non-promotable candidate wheel `ab7f1e29…` built from `5588235` |
| `qualify complete-candidate`, Linux | `passed: true`; `CC001` to `CC004` pass |
| `qualify candidate-package` from the isolated released 0.13.0 verifier | `CP001`, `CP002` pass |
| `repository_tools.upgrade_rehearsal` 0.13.0 -> 0.14.0, Linux, twice | `overall_result` pass both runs; `semantic_sha256` `ba79f344bb3c8ccf…` both |
| the same, Windows, twice | `overall_result` pass both runs; the same `semantic_sha256` |
| integration package | built, verified on Linux and Windows, retained |

Recorded again below at the bound candidate head.
