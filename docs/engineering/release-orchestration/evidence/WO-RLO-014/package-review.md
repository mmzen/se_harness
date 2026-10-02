# Review: one approval for complete release delivery

## Decision requested

Approve the definitions below and **WO-RLO-014, WO-RLO-015 and WO-RLO-016**, with
**required verification tied to the exact implementation commit** under VER-RLO-011.
The proposed grant also covers an ordinary review branch push and draft PR to
`mmzen/se_harness:main`, followed by its verification-decision update.

The owner approved the direction on 2026-10-02. These concrete artifact contents,
file scopes and assurance classification are now presented for review. All twelve
approval artifacts remain drafts; no approval or implementation is claimed here.

## Result for the owner

Approve one prepared release. The agent then delivers the evaluator, GitHub
release, PyPI, plugin marketplace, demo pages, documentation and tags. It reports
completion only after the required public checks pass. An interruption does not
invalidate unchanged authority or require the owner to repeat the same approval.

## Work to approve

| Work order | Result | Dependencies |
| --- | --- | --- |
| [WO-RLO-014](../../work-orders/WO-RLO-014.md) | One complete-release approval request; matching authority reuse; plugin preparation before evaluator publication. | Approved package. |
| [WO-RLO-015](../../work-orders/WO-RLO-015.md) | Existing publication workflow extended to every output, public readback, latest/last and safe recovery. | WO-RLO-014 interfaces. |
| [WO-RLO-016](../../work-orders/WO-RLO-016.md) | Exact one-time provider configuration review and rollout prerequisites. | Verified implementation for the final readiness assessment. |

WO-RLO-016 prepares and reviews the live configuration change. It does not apply
it. The owner will see the exact before/after diff before that one-time action.
This is a setup decision, not another permission request during each release.

## Why preparation changes

The current plugin builder requires an already public evaluator wheel. As a
result, plugin verification currently follows evaluator publication. The new
staging path qualifies the exact plugin payload before release approval, then
compares the published evaluator wheel with the approved wheel before marketplace
publication. Public readback remains required; staging does not claim publication.

## GitHub setting identified

A read-only check on 2026-10-02 found that the `pypi` environment in
`mmzen/se_harness` requires reviewer `mmzen` and permits only branch `main`.
The proposed activation removes only the redundant reviewer, after the replacement
workflow checks are verified. OIDC, `main` restrictions, required checks and
credential isolation remain required. No live setting has been changed.

[RISK-RLO-001](../../risks/RISK-RLO-001.md) records the risk of removing this control
too early or missing subsequent configuration drift. Its next action is the
bounded review in WO-RLO-016; the risk is not accepted by drafting it.

## Definitions

| Artifact | Purpose |
| --- | --- |
| [INT-RLO-002](../../intent/INT-RLO-002.md) | The complete-release outcome and observable success. |
| [CAP-RLO-005](../../capabilities/CAP-RLO-005.md) | One approval with bounded continuing authority. |
| [REQ-RLO-021](../../requirements/REQ-RLO-021.md) | Approval covers the exact complete delivery plan. |
| [REQ-RLO-022](../../requirements/REQ-RLO-022.md) | Deliverables and required verification are ready before approval. |
| [REQ-RLO-023](../../requirements/REQ-RLO-023.md) | Complete delivery, recovery and honest reporting. |
| [SPEC-RLO-007](../../specifications/SPEC-RLO-007.md) | Detailed rules, legacy behavior and rollout boundary. |
| [ARCH-RLO-006](../../architecture/ARCH-RLO-006.md) | Preparation, human decision, trusted publisher and readback boundaries. |
| [ADR-RLO-006](../../architecture/adr/ADR-RLO-006.md) | Extend the existing flow instead of adding a service or changing only wording. |
| [VER-RLO-011](../../verification/VER-RLO-011.md) | Evidence and pass conditions for the three work orders. |

## What verification must prove

- One explicit approval permits only its listed actions; old or changed authority refuses.
- Both host packages qualify from the retained candidate before public publication.
- A public-wheel or payload mismatch stops marketplace publication.
- Exact successful stages survive interruption; conflicting or unknown state is inspected.
- All required public outputs and observations are checked before completion is reported.
- Provider controls, historical records and candidate/credential separation are preserved.

Use focused tests, the existing release rehearsal, ordinary full-suite checks and
required CI. Implementation rehearsals do not publish production packages. Required
live tests for a future actual release remain in that release's contract.

## Scope limits

This implementation package does not select a new release version, publish a
package, change a live provider setting, merge its PR, refresh credentials or
adopt a new evaluator. Human verification of the implementation remains a separate
decision. Each work order contains exact file/component scope and evidence paths.

Older accepted definitions and decisions remain intact. A new intent is needed
because the older release intent explicitly excluded the wider outcome now
requested. The complete-release route is prospectively selected; old approvals
do not receive new permissions. The currently installed evaluator governs this
implementation and its rollout.

## Validation

The released evaluator results and reviewed artifact digests are retained with
this package. See [validation-summary.md](validation-summary.md) for the current
draft findings and the evaluator's next action. Validation is not approval.
