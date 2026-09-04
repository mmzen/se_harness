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

### Reading at CANDIDATE-SHORT (dispatch run RUN-A)

BUILD-A

## Section 4b: build re-verified at the bound candidate

BUILD-B

## Section 5: hosted lanes

LANES-A

### Section 5b: at the bound candidate

LANES-B
