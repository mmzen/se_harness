# WO-AUT-003 implementation and verification evidence

Work-order-keyed evidence for `WO-AUT-003`. Readings taken on 2026-08-28 on
Linux (CPython 3.12.13, Git 2.52.0) from branch
`governance/aut-003-retarget-string-form-pin`, based on `main` at `11040ee`.

## 1. Defect

`tests/test_artifact_authoring_policy.py`,
`test_repository_dry_run_report_is_retained_and_matches_a_fresh_run`, last
assertion before this work order:

```python
# the repository itself is untouched: every requirement still carries the string form
self.assertEqual([], [f for f in (REPOSITORY_ROOT / "docs/engineering").rglob("requirements/REQ-*.md") if re.search(r"^verification_method = \[", ...)])
```

`main`'s `candidate-source` job (`candidate-evidence.yml`) and the candidate
leg of `publication-rehearsal.yml` fail on it: first red run
`33109947343` at `4a43d4e` (#231, 2026-08-27 19:45); still red at
`11040ee` (run of 2026-08-28 07:31). The dependent Windows and package lanes
are skipped, so no pull request has shown green hosted lanes since.

## 2. Change

The assertion is replaced by three that state the property the pin meant:

1. every path in the retained dry-run report
   (`docs/engineering/artifact-authoring/evidence/WO-AUT-002/verification-method-mapping.json`,
   252 requirements) still carries the string form;
2. no array-form requirement is listed in the retained report;
3. the array-form requirements are exactly the fresh run's `skipped`
   additions.

The report-is-a-dry-run, zero-skips, retained-observations-stable and
extended-counts assertions are unchanged. No requirement, no retained
evidence, no script, policy, template or workflow changed.

## 3. Readings at the candidate

- Array-form requirements in the tree: 18 (the 18 `REQ-ECP-*` of #231 and
  `REQ-HBI-003`, `REQ-HBI-004` of #236 are not in this branch's tree; at
  `main` the count is 18, at #236's head 20). None is in the retained report.
- `python -m unittest tests.test_artifact_authoring_policy`: OK.
- Full suite `python scripts/run_tests.py`: 958 tests, 1 failure, 4 skipped.
  The failure, `test_release_build...test_declared_mode_set_is_what_a_posix_export_already_carries`,
  compares declared file modes with this checkout's; it fails identically at
  `main` on this host and passes on the hosted runner (the only hosted
  failure at `11040ee` is the test this work order retargets).
- Released 0.7.1 evaluator outside the checkout: `validate` 1052 artifacts,
  0 errors, 471 warnings.

## 4. Disclosures

1. The fix is drafted and implemented on one branch and one pull request
   (#237), opened as a draft before approval; the approval and start were
   recorded on 2026-08-28 in one owner decision, and the pull request was
   marked ready only after both.
2. Windows readings are the hosted lanes', recorded in section 6.

## 5. Handoff checkpoint binding

artifact: WO-AUT-003
checkpoint: handoff
formal_snapshot_sha256: 6f91a21c6660af690baf9c6d9c2831cbdbccb7017666a3cbe6788f3b55a21f04

Rerun: outcome, compliance, result_sha256: completed pass 72abf25a05fbb6f3853794db0a3e0c61a324c1bc445dc8636269df196859f573

## 6. Hosted lanes

Recorded in a later commit once the pull request has run them.
