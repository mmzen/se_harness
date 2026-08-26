+++
id = "WO-REB-024"
type = "work_order"
title = "Select the closed predecessor history from bootstrap records only"
status = "implemented"
owners = ["engineering-owner", "release-owner", "quality-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[assurance]
commit_bound_verification = "required"
rationale = "The predecessor compatibility view is the mechanic every publication and rehearsal of a bootstrap-era record replays; which rejected records it admits decides whether the release qualification can run at all once the catalog holds ordinary rejected history."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "repository_tools/predecessor_preparation.py",
  "docs/engineering/released-evaluator-boundary/README.md",
  "docs/engineering/released-evaluator-boundary/work-orders/WO-REB-024.md",
  "docs/engineering/released-evaluator-boundary/evidence/",
]

[relations]
implements = ["REQ-REB-011", "REQ-REB-012"]
specifications = ["SPEC-REB-005"]
architecture = ["ARCH-REB-004", "ADR-REB-004"]
verification = ["VER-REB-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T21:51:52Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-26, 'Approve and start'. Authorizes only the three-line filter in repository_tools/predecessor_preparation.py that selects the closed predecessor history from bootstrap records as SPEC-REB-005 rule 3 states, the packet index line and the evidence; no tests/, se_harness/ or templates/ byte, so REL-SEH-017's frozen allow-list is not reopened. Measured before approval as a reverted scratch patch: predecessor suites 20 tests OK, full suite 995 OK."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-26T21:51:56Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's decision of 2026-08-26; start preflight PASS with the exact public 0.6.0 evaluator outside the checkout over the approval commit on branch fix/reb-024-rejected-record-scope off main be2f0cf."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-26T21:58:26Z"
decided_by = "engineering-owner"
reason = "Marked implemented by the accountable engineering owner on 2026-08-26 under DR-WO-COMPLETE, 'mark WO-REB-024 implemented', on the handoff gate reading Completed over c1096bb, formal snapshot b5426b638be48334a55f94df5d5a95752a22a26da9b3960bc53ea4954bdcd71b, change set asserted complete over four paths. Governing exact public 0.6.0 evaluator outside the checkout: validate PASS at 951 artifacts, 0 errors, 50 pre-existing warnings; doctor 0 FAIL; review preflight PASS. Candidate: predecessor suites 20 OK; full suite 995 OK with 24 platform-guard skips at full scale on Windows CPython 3.14; the existing real-catalog test fails in a worktree at a3bf411 without the change and passes with it. Hosted: Engineering Harness and Governor Transition Assessment success on the pull request; the rehearsal and candidate-evidence lanes were in progress at this decision and are recorded in the evidence when they conclude. One deviation, no new test, accepted by the owner. This authorizes no further act."
+++

# Work Order: Select the closed predecessor history from bootstrap records only

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.

## Objective

`SPEC-REB-005` rule 3 says the compatibility view omits *exactly one rejected
predecessor-bootstrap RLS* and its one exact rejected contract.
`repository_tools/predecessor_preparation.py::_derive_history` implements a
stricter rule than the specification: it requires the whole catalog to hold
exactly one rejected release record of any kind, and only then checks that
the one record is the bootstrap record for the version. The first ordinary
rejected release record — `RLS-SEH-014`, rejected on 2026-08-26 under
`REL-SEH-017` — makes every derivation fail with `compatibility view requires
exactly one rejected release record, for the successor version`, and with it
`tests/test_predecessor_publication.py::test_retained_rls_replays_one_exact_rejected_pair`
over the real catalog, the `candidate`-mode release qualification on every
pull request, and the `release-record` qualification that the 0.7.0
publication executes from `main`.

Make the implementation select the closed history exactly as rule 3 states:
among rejected release records, only those whose `preparation_schema` is the
predecessor-bootstrap schema are candidates, and exactly one of them, for the
successor version, must exist. Ordinary rejected records (`REQ-REB-019`:
non-authoritative history) are invisible to the selection.

## In scope

- `_derive_history` in `repository_tools/predecessor_preparation.py`: filter
  `rejected_records` to `preparation_schema == bootstrap.PREPARATION_SCHEMA`
  before the cardinality check. The version match, the contract checks and
  the tuple checks that follow are unchanged.
- No test file changes. The existing
  `test_retained_rls_replays_one_exact_rejected_pair` runs over the real
  catalog, which now holds two rejected release records (`RLS-SEH-009`,
  bootstrap, 0.6.0; `RLS-SEH-014`, ordinary, 0.7.0); it fails before this
  change and passes after it, and is therefore the regression proof. The
  fixture-based negative cases in `tests/test_predecessor_preparation.py`
  continue to pass.
- Evidence under `docs/engineering/released-evaluator-boundary/evidence/`,
  one line in the packet index.

## Out of scope

Any `tests/`, `se_harness/`, or `templates/` change; the release qualification
workflows; `SPEC-REB-005` itself, which already states the rule; the 0.7.0
release artifacts. Keeping `tests/` untouched is deliberate: `tests/` ships in
the source distribution, and `REL-SEH-017`'s approved allow-list is frozen,
so this work order must add no packaged-surface byte.

## Authorized decision envelope

None needed.

## Constraints

`repository_tools` stays free of `se_harness` imports; the change is three
lines of filtering and introduces no new name. Measured on 2026-08-26 before
approval, as a scratch patch that was reverted: the two predecessor suites
pass (20 tests) and the full suite reads `Ran 995 tests … OK (skipped=24)`
on Windows CPython 3.14 at full scale.

## Expected change surface

One function in one module, this work order, one index line, evidence.

## Required verification

`VER-REB-004`'s succession and preparation-view scenarios through the existing
suites; repository-required checks; the pull request's `candidate`-mode
rehearsal green; handoff check.

## Evidence to record

`docs/engineering/released-evaluator-boundary/evidence/WO-REB-024-verification.md`.

## Stop and escalate conditions

Stop if any fixture-based predecessor test needs changing to pass, or if the
`release-record` qualification fails for a reason other than the record not
yet being on `main`.

## Completion report format

The `harnessctl check . --artifact WO-REB-024 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
