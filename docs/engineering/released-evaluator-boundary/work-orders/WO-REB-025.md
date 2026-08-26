+++
id = "WO-REB-025"
type = "work_order"
title = "Exercise the publication predecessor view only when its condition holds"
status = "draft"
owners = ["engineering-owner", "release-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The first job of the authorized last mile and the release-bound Pages build gate every privileged job on this step; whether it runs against an ordinary record decides whether 0.7.0 can be published at all."
decided_by = "repository-owner"

[execution_scope]
paths = [
  ".github/workflows/publish-pypi.yml",
  ".github/workflows/pages-publication.yml",
  "docs/engineering/released-evaluator-boundary/README.md",
  "docs/engineering/released-evaluator-boundary/work-orders/WO-REB-025.md",
  "docs/engineering/released-evaluator-boundary/evidence/",
]

[relations]
implements = ["REQ-REB-015"]
specifications = ["SPEC-REB-007"]
architecture = ["ARCH-REB-006", "ADR-REB-006"]
verification = ["VER-REB-006"]
+++

# Work Order: Exercise the publication predecessor view only when its condition holds

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.

## Objective

`REQ-REB-015` is conditional: *WHEN an authorized publication transaction
uses a predecessor evaluator that cannot parse retained rejected-bootstrap
history*, the system validates the complete graph with current semantics and
an exact read-only compatibility view. `SPEC-REB-007` scopes the adapter to
that two-omission view of the bootstrap history. The two workflows that
realise it — the resolve job of `.github/workflows/publish-pypi.yml` and the
release-bound build of `.github/workflows/pages-publication.yml` — run
`harnessctl qualify predecessor-view` unconditionally. On the first ordinary
release record, `RLS-SEH-015` (released 2026-08-27 under `REL-SEH-017`, no
`[bootstrap]` tuple, governed by the same 0.6.0 evaluator that validates the
complete graph), the operation fails `PV001`: *bootstrap field set is invalid
(missing evaluator_archive_name, …)*. The dispatched last mile (run
`33019109414`) stopped in its first job for that reason, before any
privileged step, while the release qualification in `release-record` mode had
passed on `main` for the same record.

Make both workflows exercise the view only when the requirement's condition
holds — the record's satisfying release contract declares a `[bootstrap]`
tuple — and otherwise retain, at the same path, an `excluded` observation
that names the resolved evaluator identity and the reason, so the retained
plan artifact keeps its file set and no later step is silently skipped.

## In scope

- `.github/workflows/publish-pypi.yml`, step *Acquire and prove the released
  evaluator*: after the evaluator identity proof, decide from the named
  record's contract whether a `[bootstrap]` table exists; run `qualify
  predecessor-view` when it does; otherwise write
  `predecessor-view-qualification.json` with `"operation":
  "predecessor-view"`, `"outcome": "excluded"`, the release record, the
  resolved evaluator version and archive digest, and the reason `record's
  contract declares no bootstrap tuple`. The evaluator download, hash proof
  and identity proof stay unconditional.
- `.github/workflows/pages-publication.yml`, step *Validate with the released
  evaluator*: the same decision and the same two branches, keeping the
  `mkdir "$RUNNER_TEMP/predecessor-view"` line and the retained file set.
- The decision is one inline `python -c` over the record and contract front
  matter with `tomllib`; no new script, no `se_harness` import, no change to
  `qualify predecessor-view` itself.
- Evidence under `docs/engineering/released-evaluator-boundary/evidence/`;
  one packet-index line.

## Out of scope

`se_harness/` (packaged; `REL-SEH-017`'s allow-list is frozen), `tests/`
(shipped in the source distribution, same reason), `repository_tools/`,
`SPEC-REB-007` and `REQ-REB-015` (already conditional), the qualification
definition `release-qualification.yml` (it does not run the view and passed),
and every 0.7.0 release artifact.

## Authorized decision envelope

The exact JSON field names of the excluded observation; whether the decision
reads the contract through the record's `satisfies` relation or through the
contract id the resolver already resolved.

## Constraints

Existing workflow assertions must stay true without editing `tests/`: the
string `predecessor-view-qualification.json` keeps its occurrence count
across the two workflows (`tests/test_release_orchestration.py`), the Pages
definition keeps exactly one `mkdir "$RUNNER_TEMP/predecessor-view"`
(`test_release_orchestration.py`) and still names the qualification file
(`test_dashboard_publication.py`); `permissions` and action pins do not
move. Both workflows must parse. The bootstrap path must behave exactly as
before: the command line of `qualify predecessor-view` is unchanged.

## Expected change surface

Two workflow steps, this work order, one index line, evidence.

## Required verification

Both workflows parse under PyYAML; `tests/test_ci_pipeline.py`,
`tests/test_release_orchestration.py`, `tests/test_dashboard_publication.py`
and the full suite pass unchanged; repository-required checks; the pull
request's lanes green; handoff check. The decisive reading is the re-dispatch
of `publish-pypi.yml` for `RLS-SEH-015` after merge, which is the release
owner's separate act.

## Evidence to record

`docs/engineering/released-evaluator-boundary/evidence/WO-REB-025-verification.md`.

## Stop and escalate conditions

Stop if satisfying the condition needs a `tests/` or `se_harness/` change,
if either workflow's bootstrap-path command line would change, or if the
contract lookup cannot be done from the front matter alone.

## Completion report format

The `harnessctl check . --artifact WO-REB-025 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
