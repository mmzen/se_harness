+++
id = "WO-TCM-002"
type = "work_order"
title = "Align router contract tests with the managed technical-communication route"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes executable assertions that protect the managed router boundary and routing-table ownership. Future engineering and assurance decisions depend on those assertions matching the approved route without weakening root managed-copy isolation."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "tests/test_artifact_catalog.py",
  "tests/test_context_routing_retirement.py",
]

[relations]
implements = ["REQ-TCM-001"]
specifications = ["SPEC-TCM-001"]
architecture = ["ARCH-TCM-001", "ADR-TCM-001"]
verification = ["VER-TCM-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T08:34:46Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-25T08:35:16Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-25T09:05:04Z"
decided_by = "engineering-owner"
+++

# Work Order: Align router contract tests with the managed technical-communication route

## Lifecycle

This companion work order remains `draft`. Approval would authorize changes to
exactly the two test files in `[execution_scope].paths`. A later explicit
engineering-owner start decision would still be required before either test can
be edited.

Draft preparation does not transition or start this work order, expand
`WO-TCM-001`, edit a test, mark work implemented, verify a candidate, mutate
Git, or perform an external action.





## Objective

Update the two router contract tests so they recognize the approved direct
technical-communication route, preserve one normative owner per subject, and
continue proving that the self-hosting root managed router is unchanged until a
separately governed harness upgrade.

## In scope

- In `tests/test_artifact_catalog.py`, replace the stale candidate/root equality
  assertion with exact assertions for intentional candidate-router isolation:
  the root copy remains unchanged, the candidate adds exactly one direct route,
  and all prior routed owners remain unchanged.
- In `tests/test_context_routing_retirement.py`, add the approved
  `Eligible operator and technical-artifact English prose` subject and
  `docs/engineering/TECHNICAL_COMMUNICATION.md` owner to the exact ordered
  routing baseline.
- Keep assertions deterministic and independent of line-ending representation.


## Out of scope


- Any path other than the two exact test paths.
- Changing the candidate router, policy, skill, implementation, package,
  fixtures, notes, formal definitions, or `WO-TCM-001`.
- Editing the self-hosting root `ENGINEERING_HARNESS.md` or managed lock.
- Weakening route uniqueness, root/candidate isolation, or existing policy
  ownership assertions.
- Applying a transition, starting work, creating completion evidence, making a
  Git change, using a network, or performing an external action.

## Authorized decision envelope


The implementation agent may decide assertion names, local expected-value
factoring, and failure-message wording inside the two authorized files.

The implementation agent may not change the expected new subject, normative
owner, routing order, one-owner invariant, root managed-copy isolation, or any
production behavior.


## Constraints


- Treat the approved candidate template as the intended future distribution and
  the root managed copy as the installed released baseline.
- Prove the candidate differs from the root only as required by the new direct
  route; do not replace equality with a broad or content-insensitive assertion.
- Preserve all existing context-retirement and artifact-catalog coverage.
- Do not use snapshots that conceal unexpected router changes.
- Test execution is read-only evidence and grants no lifecycle authority.


## Expected change surface
- Router baseline and isolation assertions in
  `tests/test_artifact_catalog.py`.
- Ordered routing-subject baseline and owner assertions in
  `tests/test_context_routing_retirement.py`.

No production, template, managed root, policy, skill, package, fixture, note, or
formal-definition file is expected to change.

## Required verification

1. Run both modified test modules in the actual Git worktree.
2. Run the five focused modules required by `WO-TCM-001` in a canonical-byte
   candidate.
3. Run the complete Python standard-library test suite in a Git worktree with
   canonical committed bytes.
4. Confirm that the only test expectation change is the one approved router
   subject and owner.
5. Confirm the root managed router and `.engineering-harness.lock` are
   unchanged.
6. Run released-evaluator validation and review preflight for both work orders.
7. Run `git diff --check` and exact changed-path review.

All deterministic tests must pass. Platform-only skips must be identified and
must not hide a failed router assertion.

## Evidence to record


Because this companion scope is intentionally limited to two test files, its
commands and results must be incorporated as a `WO-TCM-002`-keyed section in
the evidence retained by `WO-TCM-001` under the already-authorized
`docs/engineering/technical-communication/evidence/` path. Approval review
must confirm this combined-evidence arrangement or revise the scope before
starting `WO-TCM-002`.

Record exact commands, exit status, test counts, skips, canonical-byte
environment, released-evaluator results, changed paths, and proof that the root
managed router and lock were unchanged.

## Stop and escalate conditions

- The work order is not approved and explicitly started.
- Either required test needs a production or third test-file change.
- The candidate route cannot be asserted without weakening root/candidate
  isolation or one-owner routing.
- The combined-evidence arrangement is not accepted before start.
- A required test, evaluator check, graph check, or preflight fails.
- Completion would require a transition, Git mutation, network use, or external
  action not separately authorized.


## Completion report format

Report the selected work order, two exact changed paths, assertion semantics,
focused and full-suite results, released-evaluator results, combined evidence
location, root/lock non-change proof, residual uncertainty, unchanged lifecycle
state, and one canonical next decision.
