# Replacement cleanup package — draft review

> Historical drafting-stage report. The owner subsequently approved the package.
> See the [implementation checks](implementation.md) and
> [bound handoff](WO-PLG-025-handoff.md) for execution results. The original
> drafting observations below are preserved.

## Result and state

The owner requested a replacement work order on 2026-09-16 after the original
cleanup encountered onboarding failures and the evaluator's scope-amendment
limitation. This package is drafted, not approved or implemented:

- WO-PLG-025: draft replacement execution scope.
- VER-PLG-025: draft acceptance contract for the final candidate.
- SPEC-DST-029: draft public-onboarding addendum.
- WO-PLG-024: still in_progress; its proposed replacement disposition is not applied.

No new test or corrective-note implementation, lifecycle transition, commit,
VREC, push or PR occurred during this drafting step. The previous cleanup and
exact approved README repair remain in place. The earlier failures remain
visible in the original evidence directory.

## Review and validation

Released SE Harness 0.18.0 created the three drafts through its artifact
commands. The all-ref scan checked 105 available refs for the proposed WO,
VER and future VREC IDs. SPEC-DST-025 was already occupied; the released
allocator selected the free SPEC-DST-029. Nothing was overwritten.

Released graph validation reports 1,657 artifacts, zero errors and the same
48 existing warnings. A complete diff comparison confirms that the proposed
30-path scope covers all current changes from baseline
`f05c478a29c39f94968fdc842a34c861d30a42ac`, including the first work-order package
and its evidence. This comparison does not approve the scope or pass the final
implementation gate. `git diff --check` passes.

The ordinary authoring review applied ARTIFACT_AUTHORING.md. The replacement
addresses the observed failures with existing tests, guides and workflow
commands. It keeps the reviewed README and prior facts, reuses unchanged
migration/native evidence after input comparisons, and requires fresh full-suite
acceptance for the final corrections. No evaluator development or extra test
framework is needed. SPEC-DST-029 prevents merely deleting assertions while
leaving the approved presentation contract inconsistent.

## Requested decisions

Approve SPEC-DST-029 as technical owner, VER-PLG-025 as assurance owner, and
WO-PLG-025 as engineering owner. Explicitly close WO-PLG-024 through the supported
`in_progress` to `rejected` transition with the replacement reason written in
WO-PLG-025. That closes its authorization without rewriting its history or
claiming its work passed. VER-PLG-024 remains unchanged.

Once these decisions and applicable gates pass, the replacement grants routine
execution and preparation of VREC-PLG-022. Assurance and external delivery remain
separate. The old reserved VREC-PLG-021 remains absent.

## Approval-preview limitation

Automatic approval review rejected an optional `transition` invocation without
`--apply`. It interpreted the approval and rejection arguments as exact decisions
the user had not yet authorized. The process did not run. No indirect retry or
workaround was used; transition legality has not been demonstrated by a preview.
The ordinary graph validation and draft review above did complete.

[draft-review.json](draft-review.json) retains exact reviewed input hashes,
roles, target states, proposed path coverage, original-evidence identities and
the actual validation/preview outcomes. Full raw drafting results remain in
the workspace's `work/plugin-publication-governance/` directory.
