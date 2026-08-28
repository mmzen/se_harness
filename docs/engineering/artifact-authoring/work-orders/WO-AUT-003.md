+++
id = "WO-AUT-003"
type = "work_order"
title = "Retarget the dry-run pin so requirements drafted in the closed vocabulary do not fail the suite"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[assurance]
commit_bound_verification = "required"
rationale = "The change edits a test that the candidate-source lane and the candidate qualification replay run on every pull request; both lanes are red on main because of it, and every later verification record depends on those lanes being trustworthy. The assertion being retargeted guards the retained WO-AUT-002 dry-run evidence, so a wrong retarget could silently stop protecting that history."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "tests/test_artifact_authoring_policy.py",
  "docs/engineering/artifact-authoring/",
]

[relations]
implements = ["REQ-AUT-003"]
specifications = ["SPEC-AUT-001"]
architecture = ["ARCH-AUT-001", "ADR-AUT-001"]
verification = ["VER-AUT-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T10:38:34Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'Approve and start', after choosing to retarget the dry-run pin rather than convert requirements. Authorizes only the stated scope: the final assertion of test_repository_dry_run_report_is_retained_and_matches_a_fresh_run in tests/test_artifact_authoring_policy.py, the packet index line, and work-order-keyed evidence. No requirement, retained report, script, policy, template or workflow. Completion, commit-bound verification and merge are separate decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-28T10:38:36Z"
decided_by = "engineering-owner"
reason = "Started on 2026-08-28 by the accountable owner in the same decision as the approval, 'Approve and start'. Execution is confined to the approved scope."
+++

# Work Order: Retarget the dry-run pin so requirements drafted in the closed vocabulary do not fail the suite

## Lifecycle

Draft. Approval by the engineering owner authorizes bounded local
implementation, local qualification, one implementation branch and one pull
request declaring `Harness-Work-Order: WO-AUT-003`. Start, completion,
commit-bound verification, merge and every later decision are separate acts.

## What was found, and by what

`tests/test_artifact_authoring_policy.py`,
`test_repository_dry_run_report_is_retained_and_matches_a_fresh_run`, ends with
the assertion that no `docs/engineering/*/requirements/REQ-*.md` carries
`verification_method` in array form: "the repository itself is untouched:
every requirement still carries the string form". That was true when
`WO-AUT-002` retained its dry-run report, and it expressed a real property:
the migration was built and not applied, so the 252 requirements the report
observed must still carry their original strings.

Since then, `REQ-AUT-003` (approved) requires `verification_method` to be a
non-empty array from the closed vocabulary, the 0.7.1 validator emits
`W-AUT-004` on every string value, and requirements drafted after the report
follow the rule: the eighteen `REQ-ECP-*` of the execution-control-plane
packet (#231, merged 2026-08-27) and `REQ-HBI-003`/`REQ-HBI-004` (#236). The
assertion therefore fails on `main`: the `candidate-source` job of
`candidate-evidence.yml` and the candidate leg of `publication-rehearsal.yml`
have been red on it since 2026-08-27 19:45, every dependent Windows lane is
skipped, and no pull request can show green hosted lanes. The pin conflates
"the observed history is untouched" with "no requirement may use the array
the policy requires".

## Objective

Keep the retained dry-run evidence protected and stop refusing requirements
that follow `REQ-AUT-003`.

## In scope

- In the test, replace the final assertion with two that state the property
  precisely: every requirement listed in the retained report still carries
  the string form (the history the dry run observed is untouched), and every
  requirement that carries the array form is absent from the retained report
  (drafted after it, under the closed vocabulary). The earlier assertions of
  the test — the report is a dry run with zero skips, every retained
  observation is stable against a fresh run, and the fresh counts extend the
  retained ones — are unchanged.
- The packet index line for this work order.
- Work-order-keyed evidence under this domain's `evidence/`.
- One branch and one pull request declaring `Harness-Work-Order: WO-AUT-003`.

## Out of scope

- Applying the migration to any requirement, promoting `W-AUT-004` to
  `E-AUT-001`, or changing `scripts/migrate_verification_methods.py`, the
  validator, the policy, the template, or any requirement's front matter.
- The retained report `verification-method-mapping.json` and every other
  file under `docs/engineering/artifact-authoring/evidence/WO-AUT-002/`.
- Any other test, and any workflow file.

## Authorized decision envelope

The implementer may choose assertion wording, helper names and the evidence
file's name. It may not weaken the retained-report stability assertions,
touch a requirement, or edit a path outside the execution scope.

## Constraints

- Python 3.11+ standard library only.
- Run the governing evaluator, released `se-harness==0.7.1`, from outside the
  checkout for validation, preflight and the handoff check.
- Preserve owner content and every unrelated change.

## Expected change surface

About ten lines in one test function; one index line; one evidence file.

## Required verification

The test module passes; the full suite on Linux reads no failure attributable
to this test; the hosted `candidate-source` job and the candidate
qualification replay are green on the pull request; `validate` reads zero
errors under the released evaluator; the `handoff` checkpoint completes.

## Evidence to record

Commands and results; the assertion before and after; the list of array-form
requirements at the candidate and confirmation that none is in the retained
report; hosted lane identifiers.

## Stop and escalate conditions

Stop if satisfying the property would require touching a requirement or the
retained report; if the retained-report stability assertions fail for any
reason; or if a path outside scope must change.

## Completion report format

The `harnessctl check . --artifact WO-AUT-003 --checkpoint handoff` schema-2
block with the complete changed-path set asserted, and its `result_sha256`.
