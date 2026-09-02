+++
id = "SPEC-CIP-002"
type = "specification"
title = "Base-aware record selection for the publication rehearsal"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[relations]
specifies = ["REQ-CIP-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-02T15:40:23Z"
decided_by = "technical-owner"
reason = "Approved on 2026-09-02 by the accountable owner by selecting the presented option 'Approve; run it on the delegated route' for WO-CIP-006: on a pull-request event the publication rehearsal selects the newest schema-2 ready or released record the base branch already holds (issues #305 and #193). Rules CIP-REH-001 to CIP-REH-006."
+++

# Specification: Base-aware record selection for the publication rehearsal

## Scope

One selector function in `.github/scripts/publish_release.py`, one job in
`.github/workflows/publication-rehearsal.yml`, their tests, and the
rehearsal note. The reusable qualification definition, the publication
workflow and the dispatched replay are unchanged.

## Behavioral rules

**CIP-REH-001:** `select_rehearsal_record(repository, requested,
base_ref=None)` gains an optional base ref. Without it the selector reads
the release records of the checkout as today. With it the selector resolves
the ref to a commit and reads the release records at that commit through
the same Git-tree reader the resolver uses (`_release_records_at`), so the
candidates are exactly the records the base branch holds.

**CIP-REH-002:** The filter is unchanged: ready or released status,
`[distribution] schema = 2`, a canonical version; the newest by version is
chosen, an explicit request must be among the candidates, and an empty
selection is reported with its reason, not failed. The reason names the base
ref when one was used.

**CIP-REH-003:** The `select` job of `publication-rehearsal.yml`, on a
`pull_request` event only, fetches the base branch head
(`git fetch --no-tags --depth=1 origin BASE`) and passes
`--base-ref refs/remotes/origin/BASE, where BASE is the pull request's base branch` to the selector; on `push` and
`workflow_dispatch` it passes no base ref. The `rehearse-record` job is
unchanged: it still reads the selected record at `refs/remotes/origin/main`
with the status the selector reported.

**CIP-REH-004:** A base ref that does not resolve fails the select job with
the selector's error; the selector never falls back to the checkout when a
base ref was requested.

**CIP-REH-005:** `tests/test_ci_pipeline.py` asserts, on a temporary Git
repository, that the base-ref selection sees only the records committed on
the base and that the checkout selection still sees the working tree; and
asserts on the workflow YAML that the fetch step and the `--base-ref`
argument are conditioned on the pull-request event.

**CIP-REH-006:** `docs/notes/release-publication-rehearsal.md` and the
workflow's header comment state the rule: a pull request rehearses the
newest record its base already holds; the push to `main` rehearses the
record it carries.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-CIP-007 | CIP-REH-001 to CIP-REH-006 |

## Failure behaviour

A fetch or resolution failure fails the select job and therefore the
record leg, with the Git error in the log; the candidate leg runs
regardless. A base holding no schema-2 ready or released record skips the
leg with the reason, as an empty repository does today.

## Compatibility and migration

Pushes to `main` and dispatches select exactly as before. A release pull
request's record-mode lane changes meaning from "the new record, which
cannot be at the main head yet" to "the previous published record,
replayed with this candidate's definition"; the new record's own replay is
the dispatched `release-candidate-replay.yml` before the release decision
and the post-merge push.
