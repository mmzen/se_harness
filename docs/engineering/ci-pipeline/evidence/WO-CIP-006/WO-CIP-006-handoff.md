```toml
artifact = "WO-CIP-006"
checkpoint = "handoff"
formal_snapshot_sha256 = "9f66eefb6ba76eb38dc0426399159b5052e492495c665023ba9b3d06ae65e7bc"
rebound_at = "2026-09-02T15:52:33Z"
```

# WO-CIP-006 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

On a pull-request event the publication rehearsal's `select` job fetches the
base branch head and the selector reads the release records at
`refs/remotes/origin/BASE` through the resolver's Git-tree reader, choosing
the newest schema-2 ready or released record there; pushes to `main` and
dispatches read the checkout as before. A release pull request therefore
rehearses the previous published record and its record-mode lane can be
green before its own merge. `release-qualification.yml`, `publish-pypi.yml`
and `release-candidate-replay.yml` are unchanged.

## Evaluators

- Governing: released `se-harness 0.14.0` outside the checkout
  (`C:/Users/hok/se-harness-eval-0140`), `-I`, wheel-installed, for every
  reading, this packet and the handoff check.
- Candidate: this checkout, branch `wo/cip-006-execution` off `main` at
  `0d694dc`; implementation commit `d5c39de`.

## The delegated route

The gate is `.engineering-harness.delegation.toml` (`github-checks`,
`check_name = "validate"`, `base_ref = "origin/main"`). Each mechanical
decision is taken on the evaluator's own restitution naming
`delegated-executor`, and each lifecycle event records the class, the
check-run id and the exact head:

- `DR-WO-START`: taken at head `4ab503c`, check-run `100317639331`,
  conclusion success.
- `DR-WO-COMPLETE` and `DR-VREC-PREPARE`: recorded below as they are
  taken, each on a fresh green reading of its own head.

The approval that granted the class, the verification of the prepared
record, and both merges are human decisions.

## Readings (VER-CIP-002)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | exact 0.14.0 | Artifacts: 1264 | Errors: 0 | Warnings: 69 | Advisories: 0 |
| `doctor` | exact 0.14.0 | 0 FAIL |
| review preflight `--work-order WO-CIP-006` | exact 0.14.0 | PASS |
| selection on a temporary Git repository | candidate | `test_rehearsal_record_selection_reads_the_base_ref_when_given`: with the base ref only the committed record is a candidate and the reason names the ref; without it the working tree's newer record is chosen; a request absent from the base and an unknown ref are refused |
| workflow YAML | candidate | `test_the_rehearsal_and_the_release_call_one_definition`'s new assertions: the fetch step and `--base-ref` are conditioned on `github.event_name == 'pull_request'`; `default_ref` and `require_status` of the record job unchanged |
| `python -m unittest tests.test_ci_pipeline tests.test_release_orchestration` | candidate, Windows 11, `PYTHONUTF8=1` | 48 tests OK |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 | section below |
| `check --checkpoint handoff --from-git 0d694dc` | exact 0.14.0 | section below |
| run observation | this pull request's own record-mode lane | section below |

### The Windows suite

`PYTHONUTF8=1 python scripts/run_tests.py --scale full` at `9dcdd49` on this
Windows 11 workstation (CPython 3.13, LF checkout): Ran 1177 tests in 364.846s (125 classes, 8 workers); FAILED (errors=1, skipped=26). The one
error is the known baseline name present on `main` and outside this work
order (`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`).
No other name differs; the suite gains one test.

### Handoff check

`check . --artifact WO-CIP-006 --checkpoint handoff --from-git 0d694dc`,
exact 0.14.0: Completed; eight `QGP-G4I-*` predicates pass; every changed
path inside the declared scope; `complete: true`; the self-binding result
retained as `handoff.json` beside this packet.

### Run observation

Pull request #322, Publication Rehearsal run 33652518089 at `9dcdd49`: the
`select` job fetched `main` and reported `release_record = RLS-SEH-023`
with the reason "newest ready or released schema-2 record at
refs/remotes/origin/main"; the record-mode leg replayed `RLS-SEH-023`'s
bound recipe and passed; the candidate leg passed. This is the first
release-record lane green on a pull request since the mechanism exists.
The run at the previous head `a822fb7` (33651491281) failed in the `select`
job because the `--base-ref` option had been registered after `return
parser`; the command-level test added at `9dcdd49` catches that class of
error.

## Material non-effects

No change to the reusable qualification definition, the publication
workflow, the dispatched replay, the Pages workflows, any managed path,
any release or publication; the rehearsal is not made a required check.

## Hosted lanes

All lanes of pull request #322 pass at `9dcdd49`, the Publication
Rehearsal in both modes among them; they are re-read at the completion and
record heads below, and the delegated decisions quote the check-run id and
head the gate read.
