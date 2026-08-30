```toml
artifact = "WO-ECP-021"
checkpoint = "handoff"
formal_snapshot_sha256 = "d0b440c1b417e64903e74651a567930f5ac3b4553c8e8d206238f86be093c39a"
rebound_at = "2026-08-30T17:22:26Z"
```

# WO-ECP-021 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The standard template's managed lane selects the `Harness-Work-Order` and
`Harness-Restitution` declarations from the pull request's current body:
one step guarded on `pull_request` fetches
`GET $GITHUB_API_URL/repos/$GITHUB_REPOSITORY/pulls/$PULL_REQUEST_NUMBER`
with the workflow token and `curl --fail`, reduces the response to
`{"pull_request": {"body": ...}}` at `$RUNNER_TEMP/live-event.json` with
the evaluator environment's interpreter, and both `select-work-order`
invocations read that file. `GITHUB_EVENT_PATH` no longer appears in the
template, the permissions block is `contents: read` then
`pull-requests: read`, and a corrected body is honoured by re-running the
failed check without a new push (`ECP-LPB-001` to `ECP-LPB-006`). The
hash-locked root lane of this repository is unchanged and keeps the
stored-payload behaviour until the next root adoption; the `AGENTS.md`
trap states both lanes.

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff
  check included.
- Candidate: this checkout, branch `wo/ecp-live-pr-body` off `main`
  `7cac025`, running candidate source for the test suite only.

## Change

- `templates/repository/standard/.github/workflows/engineering-harness.yml`:
  the `pull-requests: read` permission, the `Read the live pull-request
  body` step, the two selector event paths, the header comment.
- `tests/test_ci_pipeline.py`:
  `test_the_managed_lane_selects_from_the_live_pull_request_body`
  (`ECP-LPB-001` to `-004`, `-006` over the template bytes).
- `tests/test_instruction_architecture.py`:
  `test_selection_accepts_the_live_event_reduction` (`ECP-LPB-003`,
  `-005`: the reduced shape selects both fields; a `null` body is refused
  as non-text), and the consumer-workflow assertions extended with the
  permission pair and the absence of `GITHUB_EVENT_PATH`.
- `AGENTS.md` (owner region): the stored-payload trap restated for the
  0.11.0 root lane beside the template lane's re-run recovery, inside the
  owner-region size bound.
- `docs/engineering/execution-control-plane/README.md`: the `REQ-ECP-026`
  and `WO-ECP-021` index rows.
- The `WO-ECP-021` packet: `REQ-ECP-026`, `SPEC-ECP-015`, `VER-ECP-017`,
  `WO-ECP-021`, and this evidence directory.

## Checks

- `tests.test_ci_pipeline` and `tests.test_instruction_architecture`: 55
  tests OK after the change.
- Neighbouring suites `tests.test_standard_repository_lifecycle`,
  `tests.test_harnessctl`, `tests.test_release_orchestration`: 81 tests
  OK, 1 platform skip.
- Full Windows suite: 1155 tests, 26 Windows-only skips, and exactly the
  one known baseline error in `test_artifact_authoring` (temporary `.git`
  teardown `PermissionError`), unrelated to this change.
- `validate`: exit 0, no error, no warning or advisory on this packet's
  artifacts; `doctor`: 0 FAIL under the 0.11.0 root;
  `validate_release_distributions.py`: PASS (8 distribution-bearing
  records).
- `VER-ECP-017` executed in full: every matrix row is one of the test
  cases or retained assertions above.

## Deviations

None.
