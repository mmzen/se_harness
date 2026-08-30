+++
id = "SPEC-ECP-015"
type = "specification"
title = "The managed lane fetches the pull request live and hands the selector an event-shaped file"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[relations]
specifies = ["REQ-ECP-026"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T17:07:52Z"
decided_by = "technical-owner"
reason = "Approved by the technical owner on 2026-08-30 by selecting the presented option 'Approve and start WO-ECP-021': ECP-LPB-001 to ECP-LPB-006; the selector module, the check inputs and the hash-locked root lane are unchanged."
+++

# Specification: The managed lane fetches the pull request live and hands the selector an event-shaped file

## Scope

Changes only the standard template
`.github/workflows/engineering-harness.yml`: one added read permission, one
added fetch-and-reduce step, and the event path passed to the two
`select-work-order` invocations. No evaluator module, contract file, result
schema, selector rule or hash-locked root file of this repository changes.

## Terms

- **Stored event payload:** the file at `$GITHUB_EVENT_PATH`, a snapshot of
  the trigger.
- **Live event file:** `$RUNNER_TEMP/live-event.json`, written during the
  run from the hosting API's current pull-request object, in the one shape
  the selector reads: a JSON object whose `pull_request` member carries the
  `body`.

## Behavioral rules

**ECP-LPB-001:** The workflow's permissions block grants exactly
`contents: read` and `pull-requests: read`, in that order, and nothing
else.

**ECP-LPB-002:** A step guarded by `github.event_name == 'pull_request'`,
placed after the evaluator installation and before any selection, fetches
`GET $GITHUB_API_URL/repos/$GITHUB_REPOSITORY/pulls/<number>` with the
workflow token in the `Authorization` header, where `<number>` is the
trigger's pull-request number. The fetch fails the job on any HTTP or
transport error and writes the response to
`$RUNNER_TEMP/pull-request.json`.

**ECP-LPB-003:** The same step reduces the response to the live event file
with the installed evaluator environment's interpreter: it parses
`$RUNNER_TEMP/pull-request.json` and writes
`{"pull_request": {"body": <body>}}` where `<body>` is the response's
`body` member copied verbatim, `null` included. No other member of the
response is copied.

**ECP-LPB-004:** Every `select-work-order` invocation in the lane passes
`--event "$RUNNER_TEMP/live-event.json"`. `$GITHUB_EVENT_PATH` does not
appear anywhere in the template.

**ECP-LPB-005:** The selector and its bounds are unchanged:
`se_harness/github_ci.py` is not touched, and the live event file is
subject to the same two-mebibyte read bound as any event.

**ECP-LPB-006:** The change-set inputs are unchanged: the scope and handoff
checks keep reading the base commit from the trigger context
(`github.event.pull_request.base.sha`) and the step guards keep reading
`github.event_name`; no input of any `check` invocation comes from the
body.

## Failure behaviour

A failed fetch stops the lane at the fetch step with curl's error text; the
selection, preflight, scope and handoff steps do not run. A pull-request
body the selector refuses produces the same refusal as before, over the
current text instead of the snapshot.

## Consequence for operators

A wrong `Harness-Work-Order` or `Harness-Restitution` line is corrected
with a body edit followed by a re-run of the failed check. The push that
existed only to refresh the stored payload is retired. The hash-locked
root lane of this repository keeps the stored-payload behaviour until the
next root adoption; until then the trap note in `AGENTS.md` states both
behaviours.
