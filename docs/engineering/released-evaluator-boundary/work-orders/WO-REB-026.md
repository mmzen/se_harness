+++
id = "WO-REB-026"
type = "work_order"
title = "Materialize the complete governance snapshot as the Pages view when no predecessor view applies"
status = "draft"
owners = ["engineering-owner", "release-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The release-bound Pages build generates the public demonstration from the view directory; which tree it reads for an ordinary record decides what the public Explorer shows for 0.7.0."
decided_by = "repository-owner"

[execution_scope]
paths = [
  ".github/workflows/pages-publication.yml",
  "docs/engineering/released-evaluator-boundary/README.md",
  "docs/engineering/released-evaluator-boundary/work-orders/WO-REB-026.md",
  "docs/engineering/released-evaluator-boundary/evidence/",
]

[relations]
implements = ["REQ-REB-015"]
specifications = ["SPEC-REB-007"]
architecture = ["ARCH-REB-006", "ADR-REB-006"]
verification = ["VER-REB-006"]
+++

# Work Order: Materialize the complete governance snapshot as the Pages view when no predecessor view applies

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.

## Objective

`WO-REB-025` made the Pages build's *Validate with the released evaluator*
step exercise `qualify predecessor-view` only when the record's contract
declares a bootstrap tuple. The next step, *Generate the target-local
canonical Explorer*, still reads `$RUNNER_TEMP/predecessor-view/governance`,
the view directory that only the `qualify` command's `--view-output`
creates. On the exclusion branch that directory does not exist, so the
release-bound Pages build for `RLS-SEH-015` failed there (run
`33020380987`, job `98349453978`) after the tag, the GitHub Release and the
PyPI promotion had all succeeded. The public 0.7.0 is complete except for
its demonstration.

For an ordinary record the "view" is the complete governance snapshot: there
is nothing to omit. Make the exclusion branch materialize that snapshot at
the view path, so the generation step and everything after it run unchanged.

## In scope

- `.github/workflows/pages-publication.yml`, exclusion branch of *Validate
  with the released evaluator*: after writing the excluded observation, add
  a detached worktree of the resolved governance commit at
  `$RUNNER_TEMP/predecessor-view/governance` (from the trusted `main`
  checkout, `git worktree add --detach`), and assert that its `HEAD` equals
  the governance commit and that it is clean. The `declared` branch, the
  generation step, the payload attestation and the deploy job are untouched.
- Evidence under `docs/engineering/released-evaluator-boundary/evidence/`;
  one packet-index line.

## Out of scope

`publish-pypi.yml` (its resolve job needs no view), `se_harness/`, `tests/`,
`repository_tools/`, the specifications, and every 0.7.0 release artifact.
Re-running the demonstration is the release owner's separate dispatch of
`publish-dashboard-pages.yml` after merge.

## Authorized decision envelope

Whether the snapshot is a detached worktree or a `git archive` export; the
former is preferred because the generation step already runs against a
worktree in the bootstrap case.

## Constraints

No `tests/` byte: the Pages definition must keep exactly one
`mkdir "$RUNNER_TEMP/predecessor-view"` and its single
`predecessor-view-qualification.json` occurrence
(`tests/test_release_orchestration.py`, `tests/test_dashboard_publication.py`);
`permissions` and action pins do not move; the workflow must parse.

## Expected change surface

One workflow branch, this work order, one index line, evidence.

## Required verification

The workflow parses under PyYAML; the workflow suites and the full suite pass
unchanged; the exclusion branch, extracted from the YAML and executed
locally against a governance worktree, leaves the view path holding the
governance commit's tree; repository-required checks; handoff check. The
decisive reading is the release owner's dispatch of
`publish-dashboard-pages.yml` for `RLS-SEH-015` after merge.

## Evidence to record

`docs/engineering/released-evaluator-boundary/evidence/WO-REB-026-verification.md`.

## Stop and escalate conditions

Stop if the generation step needs any change, or if the worktree cannot be
added from the trusted checkout without touching `$RUNNER_TEMP/governance`.

## Completion report format

The `harnessctl check . --artifact WO-REB-026 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
