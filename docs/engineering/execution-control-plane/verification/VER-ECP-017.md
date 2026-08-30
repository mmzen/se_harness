+++
id = "VER-ECP-017"
type = "verification"
title = "Independent evidence that the managed lane selects from the live body"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[relations]
verifies = ["REQ-ECP-026"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T17:07:52Z"
decided_by = "assurance-owner"
reason = "Approved by the assurance owner on 2026-08-30 by selecting the presented option 'Approve and start WO-ECP-021': template-byte rows for ECP-LPB-001 to -004 and -006, selector rows over the reduced shape for ECP-LPB-005, and the retained root-copy and consumer-workflow assertions."
+++

# Verification Contract: Independent evidence that the managed lane selects from the live body

## Independence

Expected behaviour derives from `REQ-ECP-026` and the `ECP-LPB-` rules of
`SPEC-ECP-015`. The template assertions read the template bytes and compare
them against strings stated here, never against strings computed from the
template; the selector cases drive `main()` over files written by the test
itself in the live event file's shape. No case executes the GitHub API;
the fetch contract is verified as template text plus the selector's
behaviour over the reduced shape it produces.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `ECP-LPB-001` permissions | test: read the template | `tests/test_ci_pipeline.py` | the permissions block is exactly `contents: read` then `pull-requests: read` |
| `ECP-LPB-002` guarded fetch | test: read the template | same | one step guarded on `pull_request` fetches `"$GITHUB_API_URL/repos/$GITHUB_REPOSITORY/pulls/$PULL_REQUEST_NUMBER"` with `--fail` and the token header, before the selection step |
| `ECP-LPB-003` reduction | test: read the template | same | the step writes `$RUNNER_TEMP/live-event.json` from `$RUNNER_TEMP/pull-request.json` with the evaluator environment's interpreter |
| `ECP-LPB-004` one event source | test: read the template | same | both `select-work-order` invocations pass `--event "$RUNNER_TEMP/live-event.json"`; `GITHUB_EVENT_PATH` is absent from the template |
| `ECP-LPB-005` selector over the reduced shape | test: `select-work-order` CLI over test-written files | `tests/test_instruction_architecture.py` | a `{"pull_request": {"body": ...}}` file selects the work order and the restitution digest; a `null` body exits 2 naming the body; the size bound still refuses |
| `ECP-LPB-006` change-set inputs unchanged | test: existing scope-step assertions | `tests/test_ci_pipeline.py` | `--from-git "$HARNESS_BASE_SHA"` and the event-name guards hold; no `check` input names the body |
| root copy untouched | test: existing root-copy assertion | same | the hash-locked root workflow matches its lock entry, unchanged by this work |
| installed copy behaviour | test: existing consumer-workflow assertions | `tests/test_instruction_architecture.py` | `${{ github.event.pull_request.body` stays absent; `select-work-order --event` present; one job |

## Acceptance scenarios

### Scenario 1: the selector over the live shape

Write `{"pull_request": {"body": "Harness-Work-Order: WO-X-001\n"}}` to a
file and run `main(["select-work-order", "--event", path])`, then the same
with `--field restitution-digest`. Assert the work order is printed, and
the digest selection prints empty text.

### Scenario 2: the corrected-body recovery is a re-run

Read the template and assert the fetch step precedes the selection step,
that the selection step reads only the live event file, and that no step
reads `$GITHUB_EVENT_PATH`; together these entail that a re-run selects
the current body.

### Scenario 3: no fallback

Assert the template contains `--fail` on the fetch and no reference to the
stored payload, so a failed fetch stops the lane rather than selecting a
stale body.
