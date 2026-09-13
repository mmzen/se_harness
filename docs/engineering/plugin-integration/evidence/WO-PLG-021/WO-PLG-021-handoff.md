```toml
artifact = "WO-PLG-021"
checkpoint = "handoff"
formal_snapshot_sha256 = "19df1ddd176f4ab31ac80192f7afb0fc87c34eb6c99231c83898faffae40eca5"
rebound_at = "2026-09-13T07:35:08Z"
```

# WO-PLG-021 handoff evidence

This handoff covers the approved definition packet and the owner-directed CI prerequisite only.
WO-PLG-021 remains in_progress. The larger plugin simplification, its verification record,
and release are not complete. The remaining implementation follows the recorded delegated route.

## Change

The candidate-package job checks out only scripts/check_portable_release_surface.py.
It still tests the downloaded wheel with the exact released verifier and checks that
the materialized checkout stays unchanged. Other jobs retain full checkouts.
Old evidence remains tracked in Git; it no longer consumes this job's snapshot budget.

## Observed results

- All 39 tests in tests.test_ci_pipeline pass locally, including a real sparse-checkout
  regression that verifies the required script runs, omitted history remains tracked,
  and Git detects a change to the script.
- The real-repository rehearsal materialized 9,955 bytes. The unmodified released
  0.17.0 verifier successfully snapshotted it. See ci-checkout/local-rehearsal.json.
- Candidate source evidence and Candidate package evidence passed for commit
  b30e638f290339f81ead1f62d4a0ce53482f0cd9 in
  https://github.com/mmzen/se_harness/actions/runs/34745386838.
  Package job 103692493821 completed successfully in 25 seconds, including released
  qualification, package identity, disposable repository and unchanged-checkout checks.
- Downstream upgrade jobs and the final-head rerun remain pending at this handoff.

This records the bounded prerequisite's evidence. It does not assert completion
or verification of K1-K12 or of the whole work order.
