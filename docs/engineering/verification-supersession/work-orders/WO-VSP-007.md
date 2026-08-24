+++
id = "WO-VSP-007"
type = "work_order"
title = "Align prepared VREC supersession with lifecycle validation"
status = "implemented"
owners = ["engineering-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes portable managed governance validation and supported lifecycle behavior on which later assurance and release decisions rely."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/verification-supersession/README.md",
  "docs/engineering/verification-supersession/requirements/REQ-VSP-008.md",
  "docs/engineering/verification-supersession/specifications/SPEC-VSP-002.md",
  "docs/engineering/verification-supersession/architecture/ARCH-VSP-002.md",
  "docs/engineering/verification-supersession/architecture/adr/ADR-VSP-002.md",
  "docs/engineering/verification-supersession/verification/VER-VSP-002.md",
  "docs/engineering/verification-supersession/work-orders/WO-VSP-007.md",
  "docs/engineering/verification-supersession/evidence/WO-VSP-007-verification.md",
  "docs/notes/harnessctl-reference.md",
  "se_harness/workflow.py",
  "templates/repository/standard/docs/engineering/templates/VERIFICATION_RECORD.template.md",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "tests/test_revision_provenance.py",
  "tests/test_workflow_execution.py",
]

[relations]
implements = ["REQ-VSP-008"]
specifications = ["SPEC-VSP-002"]
architecture = ["ARCH-VSP-002", "ADR-VSP-002"]
verification = ["VER-VSP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:35:25Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T10:35:35Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-24T11:17:52Z"
decided_by = "engineering-owner"
+++

# Work Order: Align prepared VREC supersession with lifecycle validation

## Lifecycle

This draft is a bounded proposal for GitHub issue #123. Approval would authorize only the declared behavior, documentation, tests, retained evidence, and exact paths. Separate explicit transitions are required to approve the definition packet and start this work order. Implementation completion, candidate commit, VREC preparation or decision, repository integration, release, publication, deployment, and any concrete VREC disposition remain separate decisions.

## Objective

Make the supported `ready -> superseded` transition succeed for VRECs created by current `capture-verification`, without inventing verification authority and without invalidating immutable legacy records.

## In scope

- Define current preparation, verification-decision, rejection, and supersession field semantics.
- Correct the packaged managed validator's state-aware VREC field requirements.
- Preserve the existing transition interface and successor eligibility checks.
- Reject fabricated verification fields on current prepared superseded records.
- Preserve valid legacy no-preparation records carrying historical `verified_at` capture metadata.
- Add command-level and direct-validator tests for success, compatibility, failure, atomicity, installed behavior, and inspection queue removal.
- Clarify the managed VREC template, repository-owned command reference, and VSP packet index.
- Retain exact implementation and qualification evidence under this work-order key.

## Out of scope

Changing lifecycle states or edges; changing decision rights; superseding, rejecting, verifying, or editing any concrete VREC; rewriting legacy history; weakening successor type, status, work-coverage, cycle, active-release, evidence, or event checks; changing release-record provenance; modifying the installed root managed validator; schema or package version changes; release scope; commit, push, pull request, merge, tag, publication, deployment, credentials, maintenance mutation, or external policy.

## Authorized decision envelope

The implementation agent may choose local predicate names, diagnostic wording under existing stable codes, and test-fixture factoring. It may remove `se_harness/workflow.py` from the actual diff if tests prove its current status-specific mutation is already conformant. It may not introduce a new lifecycle edge, compatibility allowlist, migration writer, concrete-record exception, or broader optionality for verified authority.

## Constraints

- Use the current preparation-field pair as the current-generation discriminator.
- Preserve every captured source fact during supersession.
- Keep candidate template changes separate from the released root managed copy.
- Use one packaged validator for direct validation and transition final-graph validation.
- Fail before write or roll back atomically.
- Preserve unrelated repository work and the existing draft `WO-HBI-002`.

## Expected change surface

Exactly the fourteen paths declared in `[execution_scope]`; unchanged authorized paths need not appear in the final diff. No root hash-locked managed file may change.

## Required verification

Run issue reproduction, focused workflow and provenance tests, validator field matrices, installed-template tests, the complete unit suite, formal graph validation, release-distribution validation, CLI help, exact released 0.6.0 root health, start/review preflight at the appropriate stages, inspection, managed-source parity, `git diff --check`, and exact changed-path scope comparison.

## Evidence to record

Retain baseline and corrected command outputs, exact test counts, transition write fields, source/successor status and coverage, current and legacy field matrices, no-write results, candidate-versus-root boundary observations, formal validation, distribution checks, diff scope, deviations, and residual risks.

## Stop and escalate conditions

Stop if the fix requires a concrete VREC mutation, root managed-file edit, new lifecycle edge, weakened verified-authority rule, historical rewrite, release-record change, schema/version change, external action, or any path outside the declared execution scope.

## Completion report format

Report the corrected lifecycle invariant, current and legacy compatibility results, exact changed paths, tests and validation, retained evidence path, work-order state, candidate identity if separately authorized, and every excluded action.
