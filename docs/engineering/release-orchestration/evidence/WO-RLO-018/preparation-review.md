# Approval request: restore release publication

PR #528 is merged. RLS-SEH-032 remains released, but the publication preflight
stopped before any production workflow or external write. The shared publisher
lock reader rejects the repository's valid schema-5 lock. The evaluator
descriptor and release resolver both reproduce the refusal.

## Proposed correction

Approve [WO-RLO-018](../../work-orders/WO-RLO-018.md) and
[VER-RLO-012](../../verification/VER-RLO-012.md), including required verification
tied to the correction commit and its review branch push/PR.

| File | Proposed change |
| --- | --- |
| `.github/scripts/publish_dashboard.py` | Recognize valid schema-5 external-resource locks in the shared publisher reader. Preserve evaluator identity and evidence checks. |
| `tests/test_dashboard_publication.py` | Test schema-5 success and meaningful invalid inputs; preserve schema-3/4 behavior. |
| `tests/test_release_orchestration.py` | Cover the release resolver using the same supported lock and unchanged release identity. |

The implementation also retains its own work-order evidence and verification
record. It does not alter the approved 0.22.0 candidate, archives, release
record, verification, adopted evaluator or provider settings.

## Evidence and review

- [Original diagnosis](publication-refusal.json) retains both failing commands,
  their outputs and the current release/lock hashes.
- Formal draft validation: zero errors; 60 existing warnings.
- The approval gate requires confirmation of the proposed **required**
  commit-bound assurance classification (`QGS-ASSURANCE`). No human decision
  has been invented in the drafts.
- Planned checks include Windows/Linux focused tests, the full Windows suite,
  actual release resolution, a disposable Pages rehearsal, a hosted read-only
  replay and preservation of accepted release inputs.
- No implementation file has been edited and no correction test is claimed
  to pass. The work order and verification contract remain draft.

The correction needs separate scope approval because WO-RLS-034 does not
permit this helper or these test files and explicitly excludes new fixes.
Your existing release authorization remains valid. After the correction is
verified and merged, the release can resume through its original checks.
