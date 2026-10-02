# Evaluator 0.22.0 qualification review

WO-RLS-034 prepares evaluator 0.22.0 and plugin source manifests 0.2.5.
Released evaluator 0.21.0 continues to govern this repository. This is an
agent assessment for human review, not a verification or release decision.

## Delivered result

The integrated release contains complete scope preparation, clear approval and
verification requests, review publication before verification, and the prospective
complete-release procedure with exact staging, delivery and recovery. The release
changes only version/current-documentation inputs and supporting evidence.
The new release route requires separate adoption and reviewed provider activation.

## Contract assessment

| Contract | Required result and evidence | Assessment |
| --- | --- | --- |
| VER-KIS-004 A-D | Current Windows/Linux full tests cover planned paths, automatic outputs, invalid inputs, no writes, digest and one-validation behavior. | Passed; Windows link privilege cases remain skipped and run on Linux. |
| VER-KIS-004 E-F | Current full tests run both unchanged-WO demonstrations. The existing WO-KIS-010 review assesses discovery and the approval card; relevant instruction bytes are unchanged since the merged RLO integration. | Passed; no measured usability or exhaustive impact-analysis claim. |
| VER-KIS-005 A-C | Current instruction/discovery suites pass. WO-KIS-012/review.md retains the six illustrative request cases. The integrated instructions retain result, evidence, limits, exact identity and decision scope; later KIS-006 adds confirmed PR links. | Passed by tests and inspection; examples remain synthetic. |
| VER-KIS-006 A-D | Current workflow, PR, discovery and Git-fixture tests cover review eligibility, exact final decision transport and refusal. WO-KIS-013/review.md retains the illustrative cases. This release review is already published as draft PR #528. | Passed; the final verification decision has not occurred. |
| VER-RLO-011 ONE01-04 | Current Windows/Linux source/package tests cover exact plans, staged packages, identities and narrow grants. Shared product inputs equal the previous integrated candidate except the version. | Passed; fixture approval is never real release authority. |
| VER-RLO-011 ONE05-08 | The manual publication rehearsal passed candidate replay, historical RLS replay, and complete-delivery/recovery fixtures. Existing WO-RLO-016 evidence retains the proposed reviewer-only provider change and unknown PyPI binding. | Passed for the implementation contract; activation readiness is not claimed. |
| VER-RLS-033 distribution | Both full source runs execute 1,255 tests. Windows skips 22; Linux skips 2. The corrected distribution check passes 21 records. Installed wheel and named/index-selected sdist initialization, integrity and validation pass. Two local upgrade runs and hosted Windows/Linux upgrade runs pass. | Passed for supported package routes, with the direct-sdist limitation below. |
| VER-RLS-033 release identity | The manual branch-head replay builds identical wheel/sdist pairs twice. The PR merge tree equals the assessed source tree; its package is explicitly non-promotable qualification input. | Preliminary replay passed. Final-candidate replay and aggregate capture are still required after completion is recorded. |
| REL-SEH-034 delivery | The existing v1 plan names evaluator, marketplace, documentation, Pages and release markers. WO-RLS-035/036 own downstream package/public qualification. | Plan prepared; public delivery remains pending. |

## Findings and limits

- The first source runs failed because README reached 725 words. The correction
  shortened it and preserved the existing 650-word test; both full reruns pass.
- The first Linux clone omitted historical tags. Adding those tags allowed the
  unchanged distribution validator to pass. Both results remain in the archive.
- The initial package identity command missed mandatory arguments; the corrected
  invocation passes. Local sandbox/ownership and occupied-output failures remain
  retained alongside corrected runs. They did not require product changes.
- Direct local `.tar.gz` installation fails initialization because the existing
  PEP 610 reader accepts wheel archive provenance only. That reader is unchanged
  from v0.21.0. Selecting the same sdist by name/version from a local index passes.
  Direct-file sdist support is not claimed; use the wheel or package-index route.
- Native Codex/Claude and desktop/public marketplace qualification are not source
  test results. They remain downstream obligations under WO-RLS-035/036. Earlier
  release-specific omissions are not reused as approvals for this release.
- Live provider configuration remains unchanged, and account-side PyPI binding
  remains unverified for future complete-route activation.

## Scope and simplicity review

The source diff uses the existing version fields, documentation and tests.
No product behavior, pipeline, provider setting or repository selection changes.
The only test edit changes expected candidate versions and the release pointer.
The bounded evidence archive retains commands, outputs and failures without
copying repositories, environments or packages into the source tree.

Existing inspection reviews are supporting evidence. Fresh full suites and the
new aggregate capture assess the final integration; previous human decisions
are not reused as verification of this candidate. The selected release defines
the ten-member release unit and five required contracts in the JSON assessment.

## Remaining decision sequence

After implementation completion, freeze the exact clean candidate, run its
pinned manual replay and aggregate capture, then publish the ready VREC in
PR #528 for human verification. Prepare and replay the exact RLS only after that
verification. The release decision, merge and current provider gate remain
separate steps in this rollout. Existing release execution grants are retained.
