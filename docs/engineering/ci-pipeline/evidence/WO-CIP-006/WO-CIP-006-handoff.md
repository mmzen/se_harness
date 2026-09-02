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

Recorded when the run completes.

### Handoff check

Recorded with its self-binding result beside this packet.

### Run observation

Recorded when the lanes complete at this pull request's head: the `select`
job's output and the record-mode leg's conclusion.

## Material non-effects

No change to the reusable qualification definition, the publication
workflow, the dispatched replay, the Pages workflows, any managed path,
any release or publication; the rehearsal is not made a required check.

## Hosted lanes

Recorded when the lanes complete at the pull request's head.
