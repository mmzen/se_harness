# WO-REB-014 Windows Git-Bash path evidence

## Hosted failure retained

Publication run `32598292643`, qualification job `97092604303`, resolved released authority and selected Windows Python 3.11.9 successfully. Candidate export then failed before validation or build because Git Bash passed native `D:\a\_temp/source-a` to tar, which reported `Cannot open: No such file or directory` and exited 2. No build, bundle transfer, GitHub Release, maintenance-line, PyPI, Pages, tag, root, history, distribution, or external-policy mutation ran.

The correction derives `temp_root="$(cygpath -u "$RUNNER_TEMP")"` independently in export, candidate verification, build, and bundle verification. All shell file operations use that POSIX root. The action-owned upload path remains `${{ runner.temp }}/release-bundle/`, preserving its native runner contract.

## Corrective qualification

Corrective candidate `b24daf0ff6f59c0e0224f29c7ed48b9fe47419d8` contains exactly four paths: the trusted workflow, its regression test, `WO-REB-014`, and this evidence. The stopped untracked `RLS-SEH-008` is absent. Static review proves exactly four `cygpath -u` conversions, no remaining direct quoted `$RUNNER_TEMP/...` reference in qualification shell, and the unchanged action-owned `${{ runner.temp }}/release-bundle/` upload path.

A clean exact-commit clone produced these results:

- focused release-workflow policy: 5 tests passed;
- complete release-orchestration module: 22 tests passed;
- complete isolated suite: 452 tests passed with seven declared platform skips in 215.909 seconds;
- complete current-semantics graph: 665 artifacts, zero errors, 50 maintenance warnings;
- exact released-distribution validation: passed with one distribution-bearing record;
- portable release surface, diff whitespace, and clean-checkout checks: passed.

At closeout C6 `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798`, `v0.6.0`, released `RLS-SEH-012`, distribution bytes, rejected history, the schema-2 root evaluator, and external policy remain unchanged. No publication credential, GitHub Release, PyPI file, Pages deployment, maintenance-line mutation, tag movement, root mutation, or distribution replacement occurred. A later commit-bound VREC must be accepted before this correction is pushed and publication resumes.
