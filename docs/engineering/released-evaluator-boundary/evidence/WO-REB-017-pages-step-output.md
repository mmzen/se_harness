# WO-REB-017 Pages step-output evidence

## Hosted failure retained

Standalone recovery run `32601295455`, build job `97099823204`, checked out trusted main `a95df781745f577075943b56c08479cf63547868`, selected Python 3.11.16, and successfully resolved the canonical release plan. Resolver output included governance commit `c37ec5af43234ce66c518aa58355ec05c7b8aa21` and every released identity from `RLS-SEH-012`.

The producing step then executed `test "" = "$GOVERNANCE_COMMIT"` and failed. GitHub Actions expressions are resolved before a step begins, so `steps.plan.outputs.governance_commit` cannot consume output produced later in that same step. Every subsequent build and deploy step was skipped; Pages and all previously published release surfaces remained unchanged.

Review also found that the release publication workflow created `pages-predecessor-view` during initial authority resolution while its consumer is the later independent Pages build job. Runner filesystems are job-local, so that directory would not exist in the consumer job. Parent creation is moved to the exact evaluator step immediately before the adapter call.

## Bounded correction

The standalone workflow retains the same plan resolver and exact input comparison, but the comparison is now a separate next step that can consume the completed producer's outputs. The release workflow retains the same directory and exact `governance` leaf, but creates the parent in the Pages build job. Focused dashboard and release workflow policy passed 44 tests.

## Changed paths under review

- `.github/workflows/publish-dashboard-pages.yml`
- `.github/workflows/publish-pypi.yml`
- `tests/test_dashboard_publication.py`
- `tests/test_release_orchestration.py`
- `docs/engineering/released-evaluator-boundary/work-orders/WO-REB-017.md`
- `docs/engineering/released-evaluator-boundary/evidence/WO-REB-017-pages-step-output.md`

The stopped untracked `RLS-SEH-008` remains excluded and unchanged at SHA-256 `eea7a9953767e6b817754a517db72a2484561462fce1c9e440c5e5d1501a75fc`.

## Exact corrective qualification

Corrective commit `82fede2563e058529d9bcd7ece58a5fc551d45a0` contains exactly the six reviewed paths above. A canonical-LF detached clone at that commit was clean and produced:

- focused dashboard/release workflow policy: 44 tests passed;
- complete isolated suite: 452 tests passed with seven declared platform skips in 209.582 seconds;
- complete current graph: 671 artifacts, zero errors, 50 maintenance warnings;
- released-distribution validation: passed with one distribution-bearing record;
- portable repository release surface: passed;
- commit whitespace and detached-checkout cleanliness: passed.

Review confirmed the failed run's release plan resolved the exact `RLS-SEH-012` identities and only the same-step output consumption caused the stop. The new assertion is a distinct unprivileged step immediately after the producer. The release publication workflow has exactly one `pages-predecessor-view` parent creation, inside `pages_build`, and none in `resolve`.

## Pending gates

Commit-bound assurance, trusted-main integration, hosted standalone recovery, and public endpoint reconciliation remain pending. No hosted result is inferred from local success.
